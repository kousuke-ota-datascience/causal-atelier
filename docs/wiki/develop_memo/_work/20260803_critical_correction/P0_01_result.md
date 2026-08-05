# P0 要件正本の矛盾解消 完了報告

- 作業日: 2026-08-04
- 対象プロンプト: `P0_requirements_source_of_truth_coding_agent_prompt.md`

---

## 矛盾の原因と解消

**矛盾**: 要件定義書v1.3 第1節第5項「CLIとWeb APIが単一の`Execution`集約と`execution_id`を共有する」が、補足設計文書「Execution管理とMLflow実験追跡の責務分離」の「CLIはAriadne Executionを作成しない」と両立しない。

**調査結果（実装事実）**:
1. CLIはDBへ接続しておらず、Ariadne Executionは作成していない → 補足設計文書の方針が正しい
2. しかし`planning.py`に`uuid.uuid4().hex[:12]`フォールバックがあり、`ExecutionPlan.execution_id`・`RunManifest.execution_id`の命名が「Ariadne実行管理ID」と誤認させる → **正本方針違反**
3. MLflow統合は未実装（`ExperimentTracker`・NullTracker・Worker MLflow連携なし）

---

## 変更ファイル一覧

| ファイル | 変更 |
|---|---|
| `src/ariadne/application/pipeline/planning.py` | `execution_id`→`run_label`、UUID fallback削除 |
| `src/ariadne/application/pipeline/artifacts.py` | `RunManifest.execution_id`→`run_label` |
| `src/ariadne/application/pipeline/execution.py` | `RunManifest.build`引数更新 |
| `src/ariadne/application/pipeline/validation.py` | 必須キーを`run_label`へ、旧フィールドbackward compat追加 |
| `src/ariadne/interfaces/cli/pipeline.py` | `--execution-id`削除、`--run-label`追加、`--run-id`deprecated化 |
| `src/ariadne/shared/identity.py` | **新規**: `ExecutionIdentity`型 |
| `tests/integration/test_runtime.py` | `--run-id`→`--run-label`、manifest keyアサーション更新 |
| `tests/unit/test_execution_identity.py` | **新規**: Identity invariant 10テスト |
| `tests/unit/test_cli_no_execution_creation.py` | **新規**: CLI no-execution/no-UUID 8テスト |
| `docs/wiki/requirement_definition/01_web_service_requirements_v1.4.md` | **新規**: 矛盾解消済み要件定義書 |
| `docs/wiki/requirement_definition/00_glossary.md` | **新規**: 用語集 |
| `docs/wiki/requirement_definition/traceability_matrix.md` | **新規**: トレーサビリティマトリクス |
| `docs/wiki/develop_memo/_work/20260802_issues/Execution管理とMLflow実験追跡の責務分離.md` | 冒頭に補足設計文書である旨・実装状況・要件定義書優先を明記 |

---

## テスト結果

**46 passed** (既存26 + 新規18 + regression 0)

### 新規テスト詳細

#### `tests/unit/test_execution_identity.py` (10テスト)

| テスト | 内容 | 結果 |
|---|---|---|
| `test_cli_identity_has_no_execution_id` | CLI identityはexecution_idなし | PASSED |
| `test_cli_identity_with_mlflow_run_id` | CLI identity MLflow有効時 | PASSED |
| `test_cli_identity_without_tracking` | CLI identity tracking無効時 (primary_namespace=NONE) | PASSED |
| `test_cli_identity_with_execution_id_raises` | CLI identityにexecution_idを設定すると失敗 | PASSED |
| `test_web_identity_requires_execution_id` | WEB identityはexecution_id必須 | PASSED |
| `test_web_identity_execution_id_is_primary` | WEB identityのprimary_namespace=ARIADNE | PASSED |
| `test_web_identity_mlflow_run_id_may_be_none` | WEB identityのmlflow_run_idはnull許容 | PASSED |
| `test_web_identity_mlflow_run_id_optional` | WEB identity + mlflow_run_id | PASSED |
| `test_ariadne_namespace_requires_execution_id` | ARIADNE namespaceはexecution_id必須 | PASSED |
| `test_mlflow_namespace_requires_mlflow_run_id` | MLFLOW namespaceはmlflow_run_id必須 | PASSED |

#### `tests/unit/test_cli_no_execution_creation.py` (8テスト)

| テスト | 内容 | 結果 |
|---|---|---|
| `test_run_label_is_none_when_not_provided` | ラベル未指定時はNone (UUIDを生成しない) | PASSED |
| `test_run_label_from_run_label_option` | `--run-label`オプション | PASSED |
| `test_run_label_from_deprecated_run_id` | `--run-id` deprecated alias | PASSED |
| `test_run_label_is_not_a_uuid_hex` | PlannerがUUIDを生成しないことを明示的に検証 | PASSED |
| `test_execution_plan_has_no_ariadne_execution_id_field` | `ExecutionPlan`に`execution_id`属性なし | PASSED |
| `test_execution_plan_dry_run_output_has_run_label_not_execution_id` | dry-run出力のキーが`run_label` | PASSED |
| `test_no_execution_id_option_in_cli_parser` | `--execution-id`が削除済み | PASSED |
| `test_dry_run_does_not_require_database` | CLIがDB接続なしで動作 | PASSED |

---

## 将来実装として残る項目 (Not Implemented)

以下はMLflow統合が完了していないため未実装。`traceability_matrix.md`に`Not Implemented`として記録済み。

- `Execution`テーブルへの`mlflow_run_id`/`mlflow_tracking_status`列追加とmigration
- `ExperimentTracker` Port / MLflow Adapter / NullTracker (`src/ariadne/application/ports/`、`src/ariadne/infrastructure/tracking/`)
- Worker による MLflow Run ensure（冪等生成、タグ設定、DB保存）
- CLI Bootstrap への MLflow Run 開始・`ExecutionIdentity`注入
- `DRY_RUN`/`VALIDATE_ONLY`でMLflow Runを作成しないことの明示的テスト

---

## 正本方針サマリー

| 項目 | Web/API | CLI |
|---|---|---|
| Ariadne Execution | 作成する | 作成しない |
| 正式ID | `execution_id` (Ariadne採番) | `mlflow_run_id` (MLflow採番) |
| tracking無効時ID | N/A | null (擬似ID禁止) |
| マニフェストラベル | N/A | `run_label` (人間指定、任意) |
| Metadata DB | 必須 | 不要 |
| 主要要件ID | FR-EXE-IDENTITY-002 | FR-EXE-IDENTITY-001 |
