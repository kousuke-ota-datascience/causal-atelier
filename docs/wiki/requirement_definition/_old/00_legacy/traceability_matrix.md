# ariadne 要件トレーサビリティマトリクス

- 文書版: 2.0
- 作成日: 2026-08-04
- 更新日: 2026-08-04 (P0 functional requirements coverage expansion)
- 対象: 矛盾解消P0作業 + 機能要件テスト体系構築

## Execution Identity関連

| Requirement ID | 規範要件 | 実装file | Test file | 状態 |
|---|---|---|---|---|
| FR-EXE-IDENTITY-001 | CLIはAriadne Executionを作成しない | `src/ariadne/interfaces/cli/pipeline.py` (DB接続なし) | `tests/unit/test_cli_no_execution_creation.py::TestCLINoAriadneExecutionCreated` | Implemented |
| FR-EXE-IDENTITY-001 | CLIはMetadata DBを必須としない | `src/ariadne/application/pipeline/end_to_end.py` (DB依存なし) | `tests/unit/test_cli_no_execution_creation.py::TestCLINoMetadataDBConnection` | Implemented |
| FR-EXE-IDENTITY-001 | PlannerはUUIDを生成しない | `src/ariadne/application/pipeline/planning.py` (fallbackなし) | `tests/unit/test_cli_no_execution_creation.py::TestPlannerNoUUIDGeneration::test_run_label_is_not_a_uuid_hex` | Implemented |
| FR-EXE-IDENTITY-001 | MLflow有効時にMLflow IDを採番する | 未実装 (MLflow統合待ち) | 未作成 | Not Implemented |
| FR-EXE-IDENTITY-001 | tracking無効時に擬似IDを生成しない | `src/ariadne/application/pipeline/planning.py` (run_label=None) | `tests/unit/test_cli_no_execution_creation.py::TestPlannerNoUUIDGeneration::test_run_label_is_none_when_not_provided` | Implemented |
| FR-EXE-IDENTITY-002 | `POST /executions`がExecutionを作成する | `src/ariadne/interfaces/api/routers/` | `tests/unit/web/test_web_mvp.py` | Implemented |
| FR-EXE-IDENTITY-002 | API responseの正式IDが`execution_id` | `src/ariadne/interfaces/api/routers/` | `tests/unit/web/test_web_mvp.py` | Implemented |
| FR-EXE-IDENTITY-002 | Worker開始前は`mlflow_run_id`がnull | 未実装 (`Execution`テーブルに列なし) | 未作成 | Not Implemented |
| FR-EXE-IDENTITY-002 | WorkerがMLflow Runをensureする | 未実装 | 未作成 | Not Implemented |
| FR-EXE-IDENTITY-002 | DRY_RUN/VALIDATE_ONLYはMLflow Runを作成しない | 未実装 (MLflow統合待ち) | 未作成 | Not Implemented |
| FR-EXE-IDENTITY-003 | `ExecutionIdentity`型が存在する | `src/ariadne/shared/identity.py` | `tests/unit/test_execution_identity.py` | Implemented |
| FR-EXE-IDENTITY-003 | WEB identityはexecution_id必須 | `src/ariadne/shared/identity.py::ExecutionIdentity.__post_init__` | `tests/unit/test_execution_identity.py::TestWebIdentityInvariants::test_web_identity_requires_execution_id` | Implemented |
| FR-EXE-IDENTITY-003 | CLI identityはexecution_idなし | `src/ariadne/shared/identity.py::ExecutionIdentity.__post_init__` | `tests/unit/test_execution_identity.py::TestCLIIdentityInvariants::test_cli_identity_with_execution_id_raises` | Implemented |
| FR-EXE-IDENTITY-003 | MLflow無効時はprimary_namespace=NONE | `src/ariadne/shared/identity.py::cli_identity` | `tests/unit/test_execution_identity.py::TestCLIIdentityInvariants::test_cli_identity_without_tracking` | Implemented |

## Manifest / CLI option関連

| Requirement ID | 規範要件 | 実装file | Test file | 状態 |
|---|---|---|---|---|
| FR-EXE-MANIFEST-001 | マニフェストに`run_label`を記録する | `src/ariadne/application/pipeline/artifacts.py::RunManifest` | `tests/unit/test_cli_no_execution_creation.py::test_execution_plan_dry_run_output_has_run_label_not_execution_id` | Implemented |
| FR-EXE-MANIFEST-001 | `run_label`未指定時はnullを記録する | `src/ariadne/application/pipeline/planning.py::PipelinePlanner.build_plan` | `tests/unit/test_cli_no_execution_creation.py::test_run_label_is_none_when_not_provided` | Implemented |
| FR-EXE-MANIFEST-001 | 旧マニフェストの`execution_id`/`run_id`を後方互換で読み込む | `src/ariadne/application/pipeline/validation.py::CrossStageValidator.validate_discovery_manifest_schema` | 既存integration test (compat path) | Implemented |
| FR-COMPAT-001 | `--run-id`をdeprecated aliasとして維持する | `src/ariadne/interfaces/cli/pipeline.py` | `tests/unit/test_cli_no_execution_creation.py::test_run_label_from_deprecated_run_id` | Implemented |
| FR-COMPAT-001 | `--execution-id`は削除済み | `src/ariadne/interfaces/cli/pipeline.py` | `tests/unit/test_cli_no_execution_creation.py::test_no_execution_id_option_in_cli_parser` | Implemented |

## Web/API実行管理（既存）

| Requirement ID | 規範要件 | 実装file | Test file | 状態 |
|---|---|---|---|---|
| FR-EXE-001 | Executionを作成する | `src/ariadne/application/run_execution/services.py` | `tests/unit/web/test_web_mvp.py` | Implemented |
| FR-EXE-002 | retry、cancel、events、artifactsがexecution_idで動作する | `src/ariadne/interfaces/api/routers/` | `tests/unit/web/test_web_mvp.py::test_retry_adds_an_attempt_without_overwriting_failure_history` | Implemented |
| FR-EXE-003 | Execution状態管理 (SUBMITTED/VALIDATING/QUEUED/RUNNING/SUCCEEDED/FAILED/CANCELED) | `src/ariadne/workers/state_management.py` | `tests/unit/web/test_web_mvp.py` | Implemented |

## MLflow統合（将来実装）

| Requirement ID | 規範要件 | 実装file | Test file | 状態 |
|---|---|---|---|---|
| FR-MLFLOW-001 | `Execution`テーブルに`mlflow_run_id`列を追加する | 未実装 | 未作成 | Not Implemented |
| FR-MLFLOW-002 | `Execution`テーブルに`mlflow_tracking_status`列を追加する | 未実装 | 未作成 | Not Implemented |
| FR-MLFLOW-003 | WorkerがMLflow Runを冪等にensureする | 未実装 | 未作成 | Not Implemented |
| FR-MLFLOW-004 | `ExperimentTracker` Portを導入する | 未実装 | 未作成 | Not Implemented |
| FR-MLFLOW-005 | `NullTracker`でMLflow無効時を処理する | 未実装 | 未作成 | Not Implemented |
| FR-MLFLOW-006 | CLI BootstrapでMLflow Runを開始してidentityへ注入する | 未実装 | 未作成 | Not Implemented |

## 矛盾解消サマリー

### 解消前（v1.3の誤記述）

> 要件定義書v1.3 第1節第5項:
> 「CLIとWeb APIが単一のExecution集約と`execution_id`を共有する」
> 「PlannerがUUID採番する」（UUID fallback実装）

### 解消後（v1.4正規方針）

| 項目 | Web/API | CLI |
|---|---|---|
| Ariadne Execution | 作成する | 作成しない |
| 正式ID | `execution_id` (Ariadne採番) | `mlflow_run_id` (MLflow採番) |
| tracking無効時ID | N/A | null (擬似ID禁止) |
| マニフェストラベル | N/A | `run_label` (人間指定、任意) |
| Metadata DB | 必須 | 不要 |

### 変更ファイル一覧

| ファイル | 変更種別 | 内容 |
|---|---|---|
| `src/ariadne/application/pipeline/planning.py` | 修正 | `execution_id`→`run_label`改称、UUID fallback削除 |
| `src/ariadne/application/pipeline/artifacts.py` | 修正 | `RunManifest.execution_id`→`run_label`改称 |
| `src/ariadne/application/pipeline/execution.py` | 修正 | `RunManifest.build`引数名更新 |
| `src/ariadne/application/pipeline/validation.py` | 修正 | 必須キーを`run_label`へ変更、backward compat追加 |
| `src/ariadne/interfaces/cli/pipeline.py` | 修正 | `--execution-id`削除、`--run-label`追加、`--run-id`deprecated化 |
| `src/ariadne/shared/identity.py` | 新規 | `ExecutionIdentity`型 |
| `tests/integration/test_runtime.py` | 修正 | `--run-id`→`--run-label`、manifest key更新 |
| `tests/unit/test_execution_identity.py` | 新規 | Identity invariant tests |
| `tests/unit/test_cli_no_execution_creation.py` | 新規 | CLI no-execution, no-UUID tests |
| `docs/wiki/requirement_definition/01_web_service_requirements_v1.4.md` | 新規 | 矛盾解消済み要件定義書 |
| `docs/wiki/requirement_definition/00_glossary.md` | 新規 | 用語集 |
| `docs/wiki/requirement_definition/traceability_matrix.md` | 新規 | 本ファイル |

## 機能要件テスト体系（2026-08-04 追加）

| Requirement ID | 規範要件 | Test file / function | Level | Status | Evidence / Gap |
|---|---|---|---|---|---|
| FR-PRJ-001 | Project論理削除（Admin only） | `test_rbac.py::test_project_admin_can_logically_delete_project` | api | Covered | DB status=DELETED, deleted_at確認 |
| FR-PRJ-002 | Resources are Project-scoped | `test_rbac.py::test_user_cannot_list_datasets_of_foreign_project`<br>`test_negative_e2e.py::test_cross_project_dataset_in_execution_is_rejected` | api | Covered | 別Project参照時のvalidation issueを確認 |
| FR-PRJ-003 | Viewer/Analyst/Maintainer/Admin役割割当て | `test_rbac.py::test_viewer_can_read_but_not_create_dataset`<br>`test_rbac.py::test_analyst_can_upload_but_not_delete_project`<br>`test_rbac.py::test_only_project_admin_can_add_member` | api | Covered | 各ロールの許可/拒否操作を検証 |
| FR-PRJ-004 | APIはtenant境界とProject権限を検査する | `test_rbac.py::*`（9件）<br>`test_artifact_lineage.py::test_outsider_cannot_download_artifact` | api | Covered | 404 NOT_FOUND で存在を隠蔽 |
| FR-DAT-001 | Analysis-ready Datasetの論理Resource登録 | `test_constraints.py::test_dataset_slug_must_be_unique_within_project` | api | Covered | slug重複409確認 |
| FR-DAT-002 | DatasetとDataset Versionを分離；Version不変 | `test_constraints.py::test_dataset_versions_are_numbered_incrementally` | api | Covered | version_number=1,2確認 |
| FR-DAT-004 | CSV/Parquet許可；未対応拡張子拒否 | `test_constraints.py::test_unsupported_file_extension_is_rejected`<br>`test_constraints.py::test_csv_upload_accepted` | api | Covered | 422拒否/201受付確認 |
| FR-DAT-011 | 同一content hashの重複検出 | `test_constraints.py::test_same_content_hash_detected` | api | Covered | checksum一致確認 |
| FR-SEM-001 | DatasetVersionの列からFeature Semantics作成 | `test_constraints.py::test_feature_semantics_can_be_created_from_dataset_version` | api | Covered | PUBLISHED状態確認 |
| FR-SEM-006 | Feature Semantics validation規則 | `test_constraints.py::test_feature_semantics_duplicate_feature_name_is_invalid`<br>`test_constraints.py::test_feature_semantics_post_treatment_adjustment_is_invalid` | api | Partially Covered | 同一source_column重複は未検証（実装がname重複チェックのみ） |
| FR-SEM-008 | RUN modeはPUBLISHED Version必須 | `test_negative_e2e.py::test_unpublished_semantics_version_rejected_for_run_mode` | api | Covered | FAILED Executionでの検証エラーを確認 |
| FR-CFG-001 | ConfigurationとVersion分離 | `test_constraints.py::test_published_version_status_is_published` | api | Covered | |
| FR-CFG-004 | PUBLISHED後は変更不可（新Version要） | `test_constraints.py::test_published_config_version_duplicate_is_rejected` | api | Covered | 409 Conflict確認 |
| FR-CFG-006 | TypeごとのSchema validation | `test_constraints.py::test_invalid_causal_design_yaml_is_rejected` | api | Covered | INVALID status確認 |
| FR-DIS-001〜010 | Discovery Execution全般 | `test_web_mvp.py::test_analysis_ready_discovery_graph_and_result_navigation` | e2e | Covered | ANALYSIS_READYモードでの完全Discovery確認 |
| FR-SCG-002 | CausalGraphとGraphVersion分離 | `test_artifact_lineage.py::test_published_graph_version_cannot_be_overwritten` | api/worker | Covered | content_hash不変確認 |
| FR-SCG-005 | PUBLISHED GraphVersion変更不可 | `test_artifact_lineage.py::test_published_graph_version_cannot_be_overwritten` | api/worker | Covered | publish後content_hash一致 |
| FR-CDS-001 | Causal Designの必須フィールド | `test_negative_e2e.py::test_causal_design_records_adjustment_set_in_result` | api/worker/e2e | Covered | adjustment_set, estimand, graph_version_id確認 |
| FR-EXE-001 | DRY_RUN/VALIDATE_ONLY/RUN mode | `test_execution_state_machine.py::test_dry_run_returns_200`<br>`test_execution_state_machine.py::test_validate_only_returns_200`<br>`test_execution_state_machine.py::test_run_returns_202_with_execution_id` | api | Covered | 各modeのHTTP status確認 |
| FR-EXE-003 | Execution状態遷移 | `test_execution_state_machine.py::test_successful_execution_reaches_succeeded`<br>`test_execution_state_machine.py::test_failed_execution_transitions_to_failed` | api/worker | Covered | 状態遷移確認 |
| FR-EXE-007 | Execution Plan受付後不変 | `test_execution_state_machine.py::test_execution_plan_is_immutable` | api | Covered | plan_hash確認 |
| FR-EXE-008 | 同一key/同一body replay；同一key/異なるbody 409 | `test_execution_state_machine.py::test_idempotency_key_conflict_different_body`<br>`test_execution_state_machine.py::test_idempotency_key_same_body_replays` | api | Covered | 409/Idempotency-Replayed確認 |
| FR-EXE-009 | Execution/StageExecution/Attempt分離；retry不上書き | `test_web_mvp.py::test_retry_adds_an_attempt_without_overwriting_failure_history`<br>`test_execution_state_machine.py::test_retry_preserves_failure_history` | api/worker | Covered | attempt_number=[1,2]確認 |
| FR-EXE-010 | Cancel: 許可状態/terminal状態拒否/重複idempotent | `test_execution_state_machine.py::test_cancel_queued_execution_sets_cancel_requested`<br>`test_execution_state_machine.py::test_cancel_succeeded_execution_is_conflict`<br>`test_execution_state_machine.py::test_cancel_already_canceled_is_idempotent`<br>`test_execution_state_machine.py::test_cannot_cancel_failed_execution` | api | Covered | 各状態のcancel動作確認 |
| FR-EXE-011 | ExecutionイベントAPI | `test_negative_e2e.py::test_execution_events_endpoint_returns_event_sequence`<br>`test_negative_e2e.py::test_cancel_creates_cancel_requested_event` | api | Covered | event_type, sequence_number確認 |
| FR-EXE-012 | ResultがExecutionから取得可 | `test_negative_e2e.py::test_discovery_result_is_discoverable_from_execution` | api/worker | Covered | result_type, algorithmフィールド確認 |
| FR-ART-003 | local pathをAPIに公開しない | `test_artifact_lineage.py::test_artifact_download_url_is_not_a_local_path` | api/worker | Covered | URLに`..`なし・絶対パスなし |
| FR-ART-006 | Lineage追跡: Dataset→Discovery→Graph→Design→Inference | `test_artifact_lineage.py::test_discovery_result_links_to_dataset_and_semantics`<br>`test_negative_e2e.py::test_causal_design_records_adjustment_set_in_result` | api/worker/e2e | Covered | feature_semantics_version_id, causal_graph_version_id確認 |
| FR-ART-007 | Artifact download/metadata閲覧にProject権限 | `test_artifact_lineage.py::test_outsider_cannot_download_artifact` | api | Covered | 別Project 404確認 |
| FR-RES-001 | Discovery Result: algorithm, node/edge, diagnostic | `test_negative_e2e.py::test_discovery_result_is_discoverable_from_execution` | api/worker | Covered | algorithms[].algorithm, status確認 |

## Not Covered / Partially Covered / Blocked 要件一覧

| Requirement ID | 規範要件 | Status | Gap / 理由 |
|---|---|---|---|
| FR-SEM-006 | treatment/outcomeが同一source_column不可 | Partially Covered | 実装がfeature**名**の重複のみチェック。source_column重複は未検証。要件定義の意図確認が必要 |
| FR-EXE-IDENTITY-001 | MLflow有効時にMLflow IDを採番 | Not Covered | MLflow統合未実装。将来実装待ち |
| FR-EXE-IDENTITY-002 | Worker開始前mlflow_run_id=null | Not Covered | Executionテーブルにmlflow_run_id列なし |
| FR-EXE-IDENTITY-002 | WorkerがMLflow Runをensure | Not Covered | MLflow統合未実装 |
| FR-EXE-IDENTITY-002 | DRY_RUN/VALIDATE_ONLYはMLflow Run不作成 | Not Covered | MLflow統合未実装 |
| FR-EXE-013 | Web/CLIが単一execution_idを共有する | Blocked by Requirement Conflict | v1.3に記載されたが v1.4で削除・修正済み。v1.4が正本 |
| FR-EXE-014 | CLIから外部execution_id指定可 | Blocked by Requirement Conflict | v1.3に記載されたが v1.4で削除・修正済み |
| FR-EXE-015 | execution_idでWeb/CLIから来歴追跡 | Blocked by Requirement Conflict | v1.3に記載されたが v1.4で削除・修正済み |
| FR-DAT-012〜016 | External Dataset Reference | Not Covered | MVP実装なし。スキーマのみ |
| FR-GRP-003〜007 | Graph比較画面 | Not Covered | Frontend/UI機能。API levelでは部分的に確認可能だが未テスト |
| FR-TEI-003〜010 | Treatment Effect詳細 | Partially Covered | `test_web_mvp.py`でATE/ATTのE2E確認済みだが診断/overlap/balance未確認 |
| FR-VIS-* | Dataset可視化 | Partially Covered | `test_web_mvp.py`でprofile/preview/aggregation確認済み |
| FR-CMP-* | CLI/ETL後方互換 | Partially Covered | `test_runtime.py`で一部確認済み。`test_cli_validate_only_and_dry_run_smoke`は既存失敗 |
| FR-*-PostgreSQL固有制約 | FK/UNIQUE/CHECK/trigger等 | Not Covered | 全テストSQLite使用。PostgreSQL環境が必要 |
| FR-MLFLOW-* | MLflow統合全般 | Not Covered | 将来実装。未着手 |

