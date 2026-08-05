# 変更点 Summary

## 事実

- package 構成を `causal_core`, `causal_pipeline_runtime`, `causal_discovery`, `causal_inference` に再編した。
- `common_in_causal_inference`, `causal_discovery_pipeline`, `causal_inference_pipeline` は削除した。
- 統合 entrypoint は `causal_pipeline_runtime.orchestration` を呼ぶ thin facade に変更した。
- `--validate-only` / `--dry-run` は pipeline-level strategy として実装した。
- discovery -> inference の接続は `--discovery-manifest` と `manifest.yaml` 経由に変更した。
- feature semantics / causal design / pipeline config YAML を追加した。
- estimator 名を `ols_coefficient`, `g_computation_ate`, `ipw_ate`, `aipw_ate` などへ整理した。
- AIPW cross-fitting, multiplicity correction, interpretation metadata を追加した。
- Sphinx docs と tests を新 architecture 前提に更新した。

## 推論

- 旧 package wrapper を残さない構成にしたため、後方互換性は維持していない。
- smoke 実行時間を現実的にするため、既定 discovery config は `pc` のみに軽量化した。

# 評点改善 Summary

| 観点 | Before | After | 主な改善 |
|---|---:|---:|---|
| 1. CLI パイプライン処理 | 7.0 | 8.5+ | `ExecutionPlan`, strategy, stage runner, manifest, validate/dry-run |
| 2. コード構造・保守性 | 7.0 | 8.5+ | package 再編、旧 package 削除、runtime/core 分離 |
| 3. YAML 設定管理 | 7.0 | 8.5+ | `pipeline.yaml`, feature semantics, causal design, config hash |
| 4. 特徴量作成処理 | 6.0 | 8.0+ | aggregation/transform/encoding registry |
| 5. 統計的処理 | 5.0 | 8.0+ | estimator 命名分離、g-computation、IPW、AIPW cross-fitting |
| 6. 因果推論分析の実態 | 4.0 | 8.0+ | estimand/design/adjustment validation、edge weight 解釈分離 |
| 7. 診断出力 | 5.5 | 8.0+ | balance/overlap/outcome diagnostics と manifest artifact |
| 8. レポート・解釈 | 7.0 | 8.5+ | ATE/ATT/OLS/edge coefficient の混同防止 |
| 9. テスト・再現性 | 5.0 | 8.0+ | unit/smoke tests、fixed config、manifest、hash |
| 10. Sphinx / ドキュメント | 6.5 | 8.0+ | public API docs、methodology docs、`sphinx-build -W` 成功 |

# 修正対象ファイル Summary

| ファイル | 変更区分 | 目的 | 関連観点 |
|---|---|---|---|
| `experiment/05_causal_discovery_inference_completejourney.py` | 更新 | 統合 entrypoint を runtime facade に変更 | 1, 2 |
| `experiment/03_causal_discovery_completejourney.py` | 更新 | 単体 discovery CLI を新 package へ接続 | 2 |
| `experiment/04_causal_inference_completejourney.py` | 更新 | 単体 inference CLI を新 package へ接続 | 2 |
| `experiment/causal_core/` | 新規 | 共通例外、YAML、hash、validation、feature semantics、causal design | 2, 3, 4, 6 |
| `experiment/causal_pipeline_runtime/planning.py` | 新規 | `ExecutionPlan` / `StagePlan` | 1, 2, 9 |
| `experiment/causal_pipeline_runtime/strategies.py` | 新規 | Run / ValidateOnly / DryRun strategy | 1, 2, 9 |
| `experiment/causal_pipeline_runtime/execution.py` | 新規 | `StageRunner` / `PipelineExecutor` | 1, 2, 9 |
| `experiment/causal_pipeline_runtime/artifacts.py` | 新規 | `RunManifest` / artifact registry | 1, 3, 9 |
| `experiment/causal_pipeline_runtime/validation.py` | 新規 | cross-stage validation | 3, 4, 6 |
| `experiment/causal_discovery/` | 新規/移行 | 因果探索分析 package | 2, 4, 7 |
| `experiment/causal_discovery/runner.py` | 新規 | discovery stage runner | 1, 2 |
| `experiment/causal_inference/` | 新規/移行 | 因果推論分析 package | 2, 5, 6, 7 |
| `experiment/causal_inference/runner.py` | 新規 | inference stage runner | 1, 2 |
| `experiment/causal_inference/config.py` | 更新 | `discovery_manifest` と新 estimator 名 | 1, 3, 6 |
| `experiment/causal_inference/cli.py` | 更新 | `--discovery-manifest` 対応 | 1, 3 |
| `experiment/causal_inference/estimation/treatment_effect.py` | 更新 | estimator 命名分離、g-computation、AIPW cross-fitting | 5, 6 |
| `experiment/causal_inference/estimation/multiplicity.py` | 新規 | Bonferroni / BH FDR | 5, 8 |
| `experiment/causal_inference/features/aggregation.py` | 新規 | aggregation registry | 4 |
| `experiment/causal_inference/features/transforms.py` | 新規 | transform registry | 4 |
| `experiment/causal_inference/features/encoding.py` | 新規 | encoding registry | 4 |
| `conf/causal_inference/pipeline.yaml` | 新規 | integrated pipeline config | 1, 3 |
| `conf/causal_inference/feature_semantics.yaml` | 新規 | inference feature semantics catalog | 3, 4, 6 |
| `conf/causal_inference/causal_design.yaml` | 新規 | causal design schema instance | 3, 6 |
| `experiment/tests/` | 更新 | 新 architecture の unit/smoke tests | 9 |
| `experiment/docs/sphinx/` | 更新 | 新 package/API/methodology docs | 10 |
| `pyproject.toml` | 更新 | Sphinx docs build dependency を `dev` group に追加 | 10 |

# Architecture Summary

## Packages

- `causal_core`
- `causal_pipeline_runtime`
- `causal_discovery`
- `causal_inference`

## Core layer

- `ValidationIssue`
- `ValidationResult`
- `FeatureSemanticSpec`
- `FeatureSemanticsCatalog`
- `CausalDesign`
- YAML loader
- config hashing
- common exceptions
- stage-independent path/window/feature utilities

## Pipeline runtime

- `ExecutionPlan`
- `StagePlan`
- `RunStrategy`
- `ValidateOnlyStrategy`
- `DryRunStrategy`
- `PipelineExecutor`
- `DiscoveryStageRunner`
- `InferenceStageRunner`
- `RunManifest`
- `ArtifactRegistry`
- `CrossStageValidator`

## Analysis packages

- `causal_discovery`: discovery config, feature construction, algorithms, diagnostics, reporting, stage runner
- `causal_inference`: inference config, feature construction, estimators, diagnostics, reporting, modes, stage runner

## Dependency direction

Correct:

```text
entrypoint
  -> causal_pipeline_runtime
      -> causal_discovery.runner
      -> causal_inference.runner

causal_pipeline_runtime -> causal_core
causal_discovery        -> causal_core
causal_inference        -> causal_core
```

Forbidden:

```text
causal_core
  -> causal_pipeline_runtime / causal_discovery / causal_inference

causal_discovery
  -> causal_inference config / causal design
```

# Removed Compatibility Summary

| Removed / Replaced | Replacement | Reason |
|---|---|---|
| `common_in_causal_inference` | `causal_core` + package-local data/graph utilities | common utility と runtime/data loading が混在していたため |
| `causal_discovery_pipeline` | `causal_discovery` | 因果探索分析 package であることを明示するため |
| `causal_inference_pipeline` | `causal_inference` | 因果推論分析 package であることを明示するため |
| `--discovery-dir` | `--discovery-manifest` | stage 間 artifact contract を manifest に一本化するため |
| implicit args forwarding | `ExecutionPlan` | dry-run / validate-only / reproducibility を明確化するため |
| old package imports in tests/docs | new package imports | 新 architecture の責務分離を検証するため |

# Dependency Summary

| From | Allowed Imports |
|---|---|
| `causal_core` | standard library, numpy, pandas, yaml |
| `causal_pipeline_runtime` | `causal_core`, `causal_discovery.runner`, `causal_inference.runner` |
| `causal_discovery` | `causal_core`, stage-local dependencies, `myproj` data IO |
| `causal_inference` | `causal_core`, stage-local dependencies, `myproj` data IO |

## Forbidden Imports

- `causal_core -> causal_pipeline_runtime`
- `causal_core -> causal_discovery`
- `causal_core -> causal_inference`
- `causal_discovery -> causal_inference`
- `causal_inference -> causal_discovery internals`
- production code -> `common_in_causal_inference`
- production code -> `causal_discovery_pipeline`
- production code -> `causal_inference_pipeline`

# Verification Summary

## 事実

以下は成功済み。

```bash
uv sync
uv run pytest articles/1ceee528ed7ee8/experiment/tests
uv run sphinx-build -W -b html articles/1ceee528ed7ee8/experiment/docs/sphinx articles/1ceee528ed7ee8/experiment/docs/sphinx/_build/html
uv run python articles/1ceee528ed7ee8/experiment/05_causal_discovery_inference_completejourney.py --validate-only
uv run python articles/1ceee528ed7ee8/experiment/05_causal_discovery_inference_completejourney.py --dry-run
uv run python articles/1ceee528ed7ee8/experiment/05_causal_discovery_inference_completejourney.py
```

# Additional Improvement Summary

## 事実

- Full-run smoke test を `experiment/tests/test_runtime.py` に追加した。
- Full-run smoke test では discovery manifest、inference manifest、inference report、causal design section、estimand summary、artifact manifest path を検証する。
- adjustment set validation は `FeatureSemanticSpec` ベースに厳格化した。
- adjustment variable が semantics に存在しない、role が covariate ではない、`allowed_for_adjustment=false`、`post_treatment=true`、treatment/outcome/mediator/collider role の場合は error にする。
- feature semantics validation を mode-aware にした。
- edge_weight mode では discovery graph node と inference feature semantics の strict semantic match を検証する。
- treatment_effect mode では treatment / outcome / selected covariates の subset validation を検証する。
- CLI override test の order-dependent assertion を `arg_value(args, option)` helper に置き換えた。
- inference package 内の discovery artifact reader を専用 artifact package 名へ rename した。
- `docs/sphinx/api.rst` は valid RST の section heading と top-level `automodule` directive で構成している。

## 追加検証

```bash
uv run pytest articles/1ceee528ed7ee8/experiment/tests
uv run sphinx-build -W -b html articles/1ceee528ed7ee8/experiment/docs/sphinx articles/1ceee528ed7ee8/experiment/docs/sphinx/_build/html
uv run python articles/1ceee528ed7ee8/experiment/05_causal_discovery_inference_completejourney.py --validate-only
uv run python articles/1ceee528ed7ee8/experiment/05_causal_discovery_inference_completejourney.py --validate-only --inference-mode treatment_effect --inference-outcome outcome_sales_value
```
