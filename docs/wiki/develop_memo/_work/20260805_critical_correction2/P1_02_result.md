# P1-02 実装結果

実施日: 2026-08-04

---

## 1. 変更概要

`interfaces/cli/discovery.py::main()` に集中していた全責務を分離し、Application Layer に
`DiscoveryApplicationService` を導入した。`DiscoveryStageRunner` の CLI 依存を除去し、
CLI・Pipeline Stage Runner・Worker が同一 Application Service を利用する構造に変更した。

---

## 2. 新しい依存方向

```
before:
  Application Pipeline Runner
    -> CLI Adapter (discovery.main)
        -> LogicalTableDataLoader
        -> CompleteJourneyPreprocessor
        -> CausalDiscovery
        -> CausalDiscoveryReporter

after:
  CLI ────────────────────────────────────────────\
  PipelineStageRunner (application layer) ─────────> DiscoveryApplicationService
                                                              │
                                              ┌───────────────┼───────────────┐
                                              ▼               ▼               ▼
                                   DiscoveryInputProvider  DiscoveryBackend  DiscoveryArtifactWriter
                                   (Protocol)              (Protocol)        (Protocol)
                                              │
                               ┌─────────────┼─────────────┐
                               ▼             ▼               ▼
                   CompleteJourney    SingleTable      DiscoveryInputProviderRegistry
                   Provider           Provider
```

**禁止された依存（除去済み）:**
- `application.pipeline.discovery` → `interfaces.cli.discovery`
- `interfaces.cli.discovery` → `pandas` (module-level)
- `interfaces.cli.discovery` → `LogicalTableDataLoader`
- `interfaces.cli.discovery` → `CompleteJourneyPreprocessor`
- `interfaces.cli.discovery` → `CausalDiscoveryReporter`

---

## 3. 変更後ファイル構成

```
src/ariadne/application/discovery/
    __init__.py
    dto.py                          # DiscoveryRequest, PreparedDiscoveryInput,
                                    # DiscoveryExecutionResult, DiscoveryArtifactResult,
                                    # DiscoveryInputSpecification
    ports.py                        # DiscoveryInputProvider, DiscoveryBackend,
                                    # DiscoveryArtifactWriter (Protocol)
    service.py                      # DiscoveryApplicationService
    factory.py                      # build_discovery_application_service,
                                    # build_discovery_request,
                                    # build_discovery_request_from_argv
    providers/
        __init__.py
        registry.py                 # DiscoveryInputProviderRegistry (allowlist)
        completejourney.py          # CompleteJourneyDiscoveryInputProvider
        single_table.py             # SingleTableDiscoveryInputProvider
    adapters/
        __init__.py
        backend.py                  # CausalLearnDiscoveryBackend
        artifact_writer.py          # LocalDiscoveryArtifactWriter

src/ariadne/interfaces/cli/discovery.py          # 薄い Adapter に変更
src/ariadne/application/pipeline/discovery.py   # CLI 依存除去
src/ariadne/causal/discovery/algorithms.py      # feature_config optional 化、
                                                 # background_knowledge パラメータ追加

tests/unit/discovery/
    __init__.py
    test_architecture.py            # 依存方向の強制
    test_stage_runner_no_cli.py     # Stage Runner が CLI を import しないことを保証
    test_provider_registry.py       # Registry の allowlist 動作
    test_request_mapping.py         # CLI args → DiscoveryRequest 変換
    test_single_table_provider.py   # SingleTableDiscoveryInputProvider
    test_application_service.py     # DiscoveryApplicationService オーケストレーション
```

---

## 4. 主要クラスと責務

| クラス | 責務 |
|---|---|
| `DiscoveryApplicationService` | use case のオーケストレーション。Provider → Backend → Writer を呼び出し結果 DTO を返す |
| `DiscoveryInputProviderRegistry` | allowlist ベースの Provider 解決。未登録キーは ValueError |
| `CompleteJourneyDiscoveryInputProvider` | CJ テーブル読込・前処理・background knowledge 構築 → PreparedDiscoveryInput |
| `SingleTableDiscoveryInputProvider` | 単一 CSV/Parquet 読込・列選択・欠損処理・標準化 → PreparedDiscoveryInput |
| `CausalLearnDiscoveryBackend` | CausalDiscovery を wrap し pre-built background knowledge を注入して run_all を呼ぶ |
| `LocalDiscoveryArtifactWriter` | CausalDiscoveryReporter + write_resolved_config を wrap してローカル保存 |
| `build_discovery_application_service` | Composition Root。completejourney / single_table を登録した Service を返す |
| `build_discovery_request_from_argv` | Stage Runner 用。resolved_args リストから DiscoveryRequest を構築 |

---

## 5. Complete Journey 実行経路

```
ariadne-discovery (CLI entrypoint)
  └── interfaces/cli/discovery.py::main(argv)
        parse_args(argv)
        → build_discovery_request(args, project_root)   # factory.py
            load_analysis_config / merge_cli_overrides
            provider_type = "completejourney" (default)
            → DiscoveryRequest(input_specification=DiscoveryInputSpecification("completejourney"))
        → build_discovery_application_service(project_root)
        → service.execute(request)
            registry.create("completejourney", request)
            → CompleteJourneyDiscoveryInputProvider.prepare(request)
                LogicalTableDataLoader.load_all()
                CompleteJourneyPreprocessor.preprocess()
                build_background_knowledge()
                → PreparedDiscoveryInput(analysis_frame, raw_frame, transformed_frame,
                                         variable_metadata, background_knowledge,
                                         metadata={campaign_id, pre_weeks, ...})
            → CausalLearnDiscoveryBackend.discover(prepared, analysis_config)
                CausalDiscovery.run_all(frame, background_knowledge=prepared.background_knowledge)
                → dict[str, DiscoveryResult]
            → LocalDiscoveryArtifactWriter.write(request, prepared, results)
                write_resolved_config(...)
                CausalDiscoveryReporter.write_outputs(...)
                → DiscoveryArtifactResult(artifacts={...})
            → DiscoveryExecutionResult(status, algorithm_results, artifacts,
                                        sample_count, variable_count, ...)
        print_discovery_summary(result)
```

---

## 6. Single Table 実行経路

```
ariadne-discovery --input-provider single_table \
                  --analysis-config configs/causal/discovery.yaml \
                  --output-dir artifacts/my_output
  └── interfaces/cli/discovery.py::main(argv)
        parse_args(argv)
        → build_discovery_request(args, project_root)
            provider_type = "single_table"
            feature_config = None
            → DiscoveryRequest(input_specification=DiscoveryInputSpecification(
                  "single_table",
                  options={"table_path": "...", "columns": [...], "standardization": "zscore"}
              ))
        → service.execute(request)
            registry.create("single_table", request)
            → SingleTableDiscoveryInputProvider.prepare(request)
                _load_table(table_path)         # CSV or Parquet
                column selection / unit_id drop
                _apply_missing_value_policy()
                constant column detection/drop
                _standardize_zscore()
                _build_simple_variable_metadata()
                → PreparedDiscoveryInput(background_knowledge=None,
                                          metadata={"table_path": ...})
            → CausalLearnDiscoveryBackend.discover(prepared, analysis_config)
                # use_background_knowledge=False, background_knowledge=None
            → LocalDiscoveryArtifactWriter.write(...)
```

---

## 7. Compatibility mapping

| 旧設定 | 新マッピング先 | 優先順位 |
|---|---|---|
| `dataset.yaml_path` | `analysis_config.dataset.yaml_path` → CompleteJourney Provider が使用 | 3 (legacy) |
| `run.campaign_id` | `analysis_config.run.campaign_id` → CompleteJourney Provider が使用 | 3 (legacy) |
| `run.pre_weeks` | `analysis_config.run.pre_weeks` → CompleteJourney Provider が使用 | 3 (legacy) |
| `--campaign-id` (CLI) | `merge_cli_overrides` → `analysis_config.run.campaign_id` | 1 (CLI) |
| `--dataset-yaml` (CLI) | `merge_cli_overrides` → `analysis_config.dataset.yaml_path` | 1 (CLI) |

設定優先順位（高→低）: 明示的 CLI override > provider/input 設定 > legacy compatibility mapping > default

---

## 8. 実行したテストと結果

### 新規テスト (tests/unit/discovery/)

| テストファイル | テスト数 | 結果 |
|---|---|---|
| test_architecture.py | 7 | PASSED |
| test_stage_runner_no_cli.py | 3 | PASSED |
| test_provider_registry.py | 7 | PASSED |
| test_request_mapping.py | 10 | PASSED |
| test_single_table_provider.py | 11 | PASSED |
| test_application_service.py | 7 | PASSED |
| **合計** | **45** | **45 PASSED** |

### 既存テスト（回帰確認）

| テストスイート | 件数 | 結果 |
|---|---|---|
| tests/unit/ (既存) | 149 | PASSED |
| tests/integration/ | 39 | PASSED |
| **合計** | **233** | **233 PASSED, 0 FAILED** |

---

## 9. 未解決の制約

- `CausalDiscoveryReporter.write_algorithm_report()` は `campaign_id` / `pre_weeks` を Markdown レポートに埋め込む仕様のまま。Single Table Provider では空文字・0 が入る。将来的にレポートテンプレートを Provider 非依存にすることが望ましい。
- `LocalDiscoveryArtifactWriter` は CausalDiscovery インスタンスを diagnostics helper 用に再生成している（アルゴリズムは実行しない）。将来的に `CausalDiscoveryDiagnostics` を直接 Backend 側に保持させることで除去可能。

---

## 10. 新しい Provider を追加する手順

1. `src/ariadne/application/discovery/providers/my_provider.py` を作成し `prepare(request: DiscoveryRequest) -> PreparedDiscoveryInput` を実装する
2. `src/ariadne/application/discovery/factory.py` の `_build_default_provider_registry()` に 1 行追加する:
   ```python
   registry.register("my_provider", lambda request: MyProvider(request))
   ```
3. **変更不要:** CLI、`DiscoveryApplicationService`、`CausalLearnDiscoveryBackend`、`DiscoveryStageRunner`
4. Provider 向け Unit Test を `tests/unit/discovery/test_my_provider.py` に追加する

---

## 11. 変更ファイル一覧

| 変更種別 | ファイル |
|---|---|
| 変更 | `src/ariadne/interfaces/cli/discovery.py` |
| 変更 | `src/ariadne/application/pipeline/discovery.py` |
| 変更 | `src/ariadne/causal/discovery/algorithms.py` |
| 新規 | `src/ariadne/application/discovery/__init__.py` |
| 新規 | `src/ariadne/application/discovery/dto.py` |
| 新規 | `src/ariadne/application/discovery/ports.py` |
| 新規 | `src/ariadne/application/discovery/service.py` |
| 新規 | `src/ariadne/application/discovery/factory.py` |
| 新規 | `src/ariadne/application/discovery/providers/__init__.py` |
| 新規 | `src/ariadne/application/discovery/providers/registry.py` |
| 新規 | `src/ariadne/application/discovery/providers/completejourney.py` |
| 新規 | `src/ariadne/application/discovery/providers/single_table.py` |
| 新規 | `src/ariadne/application/discovery/adapters/__init__.py` |
| 新規 | `src/ariadne/application/discovery/adapters/backend.py` |
| 新規 | `src/ariadne/application/discovery/adapters/artifact_writer.py` |
| 新規 | `tests/unit/discovery/__init__.py` |
| 新規 | `tests/unit/discovery/test_architecture.py` |
| 新規 | `tests/unit/discovery/test_stage_runner_no_cli.py` |
| 新規 | `tests/unit/discovery/test_provider_registry.py` |
| 新規 | `tests/unit/discovery/test_request_mapping.py` |
| 新規 | `tests/unit/discovery/test_single_table_provider.py` |
| 新規 | `tests/unit/discovery/test_application_service.py` |

---

## 12. migration の有無と内容

DB スキーマ変更なし。Alembic migration 不要。

既存の CLI オプション・出力 Artifact 名・Manifest 契約はすべて維持されており、
既存の YAML 設定・実験スクリプト・Pipeline 設定の変更は不要。
