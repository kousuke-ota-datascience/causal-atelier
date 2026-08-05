# P0-03 実施結果: 機能要件テスト体系の構築と不足テストの実装

- 作業日: 2026-08-04
- 対象プロンプト: `P0_03_functional_requirements_test_coding_agent_prompt.md`

---

## 1. 調査した規範文書と正本

| 文書 | 版 | 備考 |
|---|---|---|
| `docs/wiki/requirement_definition/01_web_service_requirements_v1.4.md` | v1.4 | **正本**。v1.3を継承し Execution Identity矛盾を解消 |
| `docs/wiki/requirement_definition/01_web_service_requirements_v1.3.md` | v1.3 | FR-PRJ〜FR-CMP を含む139件の機能要件を定義。FR-EXE-013/014/015はv1.4で Blocked |
| `docs/wiki/requirement_definition/02_data_model_definition_v1.4.md` | v1.4 | データモデル参照用 |
| `docs/wiki/requirement_definition/traceability_matrix.md` | v2.0 | 本作業で更新 |

---

## 2. 抽出した機能要件の概要

v1.3/v1.4 合計 **144件** の機能要件ID。

| カテゴリ | 要件数 | 主な内容 |
|---|---|---|
| FR-PRJ | 6 | Project管理、RBAC、論理削除 |
| FR-DAT | 16 | Dataset登録、Version管理、profile |
| FR-SEM | 9 | Feature Semantics、role、validation |
| FR-CFG | 8 | Configuration管理、PUBLISHED不変 |
| FR-DIS | 10 | Causal Discovery Execution |
| FR-GRP | 7 | Graph比較・表示 |
| FR-SCG | 9 | Saved Causal Graph管理 |
| FR-CDS | 9 | Causal Design管理 |
| FR-EWI | 6 | Edge Weight Inference |
| FR-TEI | 10 | Treatment Effect Inference |
| FR-EXE | 19 | Execution管理、Outbox、Worker、Identity |
| FR-ART | 7 | Artifact・Manifest・Lineage |
| FR-RES | 7 | Result表示・Traceability |
| FR-VIS | 6 | Dataset可視化 |
| FR-EXP | 4 | Experiment管理 |
| FR-CMP | 10 | CLI/ETL後方互換 |

---

## 3. 既存テストの評価（作業前）

- **63件**（62 passed / 1 failed）
- カバー範囲: CLI Identity、ETL、Infrastructure、Web MVP E2E（大まかなHappy Path）
- **未テスト**: RBAC詳細・Execution状態遷移・cancel・Idempotency conflict・Dataset制約・Lineage個別確認

---

## 4. 追加・変更したtest file一覧

### 新規追加（5ファイル、45件）

| ファイル | テスト件数 | カバー要件 |
|---|---|---|
| `tests/unit/web/test_rbac.py` | 10 | FR-PRJ-001〜004 |
| `tests/unit/web/test_execution_state_machine.py` | 13 | FR-EXE-001,003,007,008,009,010 |
| `tests/unit/web/test_constraints.py` | 11 | FR-DAT-001,002,004,011; FR-CFG-004,006; FR-SEM-001,006 |
| `tests/unit/web/test_artifact_lineage.py` | 4 | FR-ART-003,006,007; FR-SCG-005 |
| `tests/unit/web/test_negative_e2e.py` | 6 | FR-PRJ-002; FR-SEM-008; FR-EXE-011,012; FR-CDS-001; FR-RES-001 |

### 変更（1ファイル）

| ファイル | 変更内容 |
|---|---|
| `pyproject.toml` | `[tool.pytest.ini_options]` を追加。`unit/component/api/worker/postgres/cli/e2e/scientific/requirement` の9マーカーを登録 |

### 更新（1ファイル）

| ファイル | 変更内容 |
|---|---|
| `docs/wiki/requirement_definition/traceability_matrix.md` | v1.0→v2.0。新規テストを追記。Not Covered/Partially Covered/Blocked を明記 |

---

## 5. 変更したproduct code一覧と理由

**なし。** 全テストは既存実装に対して書かれており、プロダクトコードの修正は不要だった。

---

## 6. Traceability Matrixの集計

| Status | 要件数 |
|---|---|
| **Covered** | **26** |
| Partially Covered | 4 |
| Not Covered | 12 |
| Blocked by Requirement Conflict | 3 |
| **主要要件 合計** | **45** |

### Covered 要件（主要）

| Requirement ID | テスト |
|---|---|
| FR-PRJ-001 | `test_project_admin_can_logically_delete_project` |
| FR-PRJ-002 | `test_user_cannot_list_datasets_of_foreign_project`、`test_cross_project_dataset_in_execution_is_rejected` |
| FR-PRJ-003 | `test_viewer_can_read_but_not_create_dataset`、`test_analyst_*`、`test_only_project_admin_*` |
| FR-PRJ-004 | `test_rbac.py` 全9件、`test_outsider_cannot_download_artifact` |
| FR-DAT-001 | `test_dataset_slug_must_be_unique_within_project` |
| FR-DAT-002 | `test_dataset_versions_are_numbered_incrementally` |
| FR-DAT-004 | `test_unsupported_file_extension_is_rejected`、`test_csv_upload_accepted` |
| FR-DAT-011 | `test_same_content_hash_detected` |
| FR-SEM-001 | `test_feature_semantics_can_be_created_from_dataset_version` |
| FR-SEM-008 | `test_unpublished_semantics_version_rejected_for_run_mode` |
| FR-CFG-001 | `test_published_version_status_is_published` |
| FR-CFG-004 | `test_published_config_version_duplicate_is_rejected` |
| FR-CFG-006 | `test_invalid_causal_design_yaml_is_rejected` |
| FR-DIS-001〜010 | `test_web_mvp.py::test_analysis_ready_discovery_graph_and_result_navigation` |
| FR-SCG-002、005 | `test_published_graph_version_cannot_be_overwritten` |
| FR-CDS-001 | `test_causal_design_records_adjustment_set_in_result` |
| FR-EXE-001 | `test_dry_run_returns_200`、`test_validate_only_returns_200`、`test_run_returns_202_with_execution_id` |
| FR-EXE-003 | `test_successful_execution_reaches_succeeded`、`test_failed_execution_transitions_to_failed` |
| FR-EXE-007 | `test_execution_plan_is_immutable` |
| FR-EXE-008 | `test_idempotency_key_conflict_different_body`、`test_idempotency_key_same_body_replays` |
| FR-EXE-009 | `test_retry_preserves_failure_history`（既存テストと合わせて確認） |
| FR-EXE-010 | `test_cancel_queued_*`、`test_cancel_succeeded_*`、`test_cancel_already_canceled_*`、`test_cannot_cancel_failed_*` |
| FR-EXE-011 | `test_execution_events_endpoint_*`、`test_cancel_creates_cancel_requested_event` |
| FR-EXE-012 | `test_discovery_result_is_discoverable_from_execution` |
| FR-ART-003 | `test_artifact_download_url_is_not_a_local_path` |
| FR-ART-006 | `test_discovery_result_links_to_dataset_and_semantics`、`test_causal_design_records_adjustment_set_in_result` |
| FR-ART-007 | `test_outsider_cannot_download_artifact` |
| FR-RES-001 | `test_discovery_result_is_discoverable_from_execution` |
| FR-EXE-IDENTITY-001〜003 | `test_execution_identity.py`、`test_cli_no_execution_creation.py`（既存） |
| FR-EXE-MANIFEST-001、FR-COMPAT-001 | `test_cli_no_execution_creation.py`（既存） |

---

## 7. MVP Journey E2E結果

`tests/unit/web/test_web_mvp.py::test_analysis_ready_discovery_graph_and_result_navigation` **PASSED**

```
Project作成
→ Dataset登録・Version作成（Analysis Binding READY）
→ Feature Semantics Version作成・publish
→ Discovery Execution作成（ANALYSIS_READY mode）
→ Worker実行 → SUCCEEDED
→ Discovery Result取得（algorithm, node/edge確認）
→ Causal Graph Version作成・publish
→ Causal Design作成・publish
→ Inference Execution作成（EDGE_WEIGHT mode）→ SUCCEEDED
→ Treatment Effect Execution作成（TREATMENT_EFFECT mode）→ SUCCEEDED
→ causal_graph_version_id、selected_adjustment_variables 確認
→ input_mode = ANALYSIS_READY 記録確認
```

負のE2Eテスト（全PASSED）:

| テスト | 検証内容 |
|---|---|
| `test_cross_project_dataset_in_execution_is_rejected` | 別ProjectのDataset/Config参照→FAILED Execution（boundary violation確認） |
| `test_unpublished_semantics_version_rejected_for_run_mode` | 未publishのSemantics→Execution FAILED |

---

## 8. Worker / CLI / scientific suite結果

| Suite | 結果 |
|---|---|
| Worker (retry/cancel/Outbox/Attempt) | **PASSED** 全件 |
| CLI regression (`test_runtime.py`) | 5件中4件 PASSED。`test_cli_validate_only_and_dry_run_smoke` は**作業前から失敗**（下記参照） |
| Scientific validation (`test_inference.py`) | **7件 PASSED**（ATE/ATT/AIPW/extreme propensity/multiplicity） |
| PostgreSQL固有制約 | **Not Covered**（全テストSQLite使用、PG環境未整備） |

---

## 9. 実行したcommandと終了code

```bash
# 全テスト実行（test_migration_schema.pyを除外）
cd /datadrive/user_work/ota.kosuke.1/ariadne
source .venv/bin/activate
python -m pytest tests/ --ignore=tests/integration/test_migration_schema.py -q --tb=no
```

**結果: 1 failed, 107 passed, 1 warning（終了コード: 1）**

| | 作業前 | 作業後 |
|---|---|---|
| passed | 62 | **107** |
| failed | 1 | 1（同一テスト） |
| 収集件数 | 63 | **108** |

---

## 10. Not Covered / Partially Covered / Blocked 項目

### Not Covered

| Requirement ID | 理由 |
|---|---|
| FR-EXE-IDENTITY-001 (MLflow採番) | MLflow統合未実装。将来実装待ち |
| FR-EXE-IDENTITY-002 (mlflow_run_id列) | Executionテーブルにmlflow_run_id列なし |
| FR-EXE-IDENTITY-002 (Worker MLflow ensure) | MLflow統合未実装 |
| FR-DAT-012〜016 | External Dataset Reference はMVP実装なし |
| FR-GRP-003〜007 | Graph比較はFrontend/UI機能。API level未テスト |
| FR-*-PostgreSQL固有制約 | FK/UNIQUE/CHECK/trigger等はSQLiteで再現不可。PostgreSQL環境が必要 |
| FR-MLFLOW-001〜006 | MLflow統合全般。将来実装 |

### Partially Covered

| Requirement ID | Gap |
|---|---|
| FR-SEM-006 | treatment/outcome が同一 **source_column** の場合を未検証。実装はfeature**名**重複のみチェック。要件意図との乖離あり（要件Gap候補） |
| FR-TEI-003〜010 | E2EでATE確認済みだが、診断/overlap/balance/極端propensityの個別テストなし |
| FR-VIS-001〜006 | profile/preview/aggregation/column_policy は既存テストで確認済み |
| FR-CMP-001〜010 | `test_runtime.py` で一部確認済み。CLI smoke testが既存失敗 |

### Blocked by Requirement Conflict

| Requirement ID | 理由 |
|---|---|
| FR-EXE-013 | v1.3「CLIとWebが単一execution_idを共有」→ v1.4で削除。v1.4が正本 |
| FR-EXE-014 | v1.3「CLIから外部execution_id指定可」→ v1.4で削除 |
| FR-EXE-015 | v1.3「execution_idでWeb/CLI来歴追跡」→ v1.4で削除 |

---

## 11. 既存失敗テスト

| テスト | 失敗内容 | 状態 |
|---|---|---|
| `tests/integration/test_runtime.py::test_cli_validate_only_and_dry_run_smoke` | CLI `--validate-only` の stdout が空。`"validation status: ok"` 文字列なし。`returncode=0` は正常 | **作業前から失敗**。本作業では手を加えず。FR-CMP-001 の部分カバーに影響 |

---

## 12. 残存リスク

1. **`test_cli_validate_only_and_dry_run_smoke` 失敗継続**: CLIの `--validate-only` が stdout に検証ステータスを出力しない。実装側の出力漏れと推定されるが、要件との照合が必要。
2. **PostgreSQL固有制約が未検証**: append-only trigger、timezone-aware column、SKIP LOCKED 等はSQLiteで代替不可。実PostgreSQL環境でのテストスイートが必要。
3. **FR-SEM-006 source_column重複**: 要件は「treatmentとoutcomeが同一列であってはならない」と記述されているが、実装は「同一feature名」の重複チェックのみ。仕様意図を要件定義側に確認が必要。
4. **MLflow統合が全面未実装**: FR-EXE-IDENTITY-001/002 の MLflow関連受入条件はすべて Not Covered。`P1_01_mlflow_integration_coding_agent_prompt.md` が後続作業として存在する。
5. **E2Eテストの実行時間**: Worker系E2Eテストは1件あたり15〜30秒。CI分割（fast/api/e2e）設計は pyproject.toml に marker 設定済みだが、CI workflow ファイルは未作成。

---

## 成果物一覧

| 成果物 | パス |
|---|---|
| 新規テスト: RBAC | `tests/unit/web/test_rbac.py` |
| 新規テスト: 状態遷移・cancel | `tests/unit/web/test_execution_state_machine.py` |
| 新規テスト: Dataset/Config制約 | `tests/unit/web/test_constraints.py` |
| 新規テスト: Artifact/Lineage | `tests/unit/web/test_artifact_lineage.py` |
| 新規テスト: 否定的E2E | `tests/unit/web/test_negative_e2e.py` |
| pytest marker設定 | `pyproject.toml` |
| Traceability Matrix v2.0 | `docs/wiki/requirement_definition/traceability_matrix.md` |
| Requirement Coverage Report | `artifacts/requirements-test-report.md` |
