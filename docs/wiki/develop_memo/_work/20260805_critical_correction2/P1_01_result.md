# 実装完了報告: P1 MLflow連携の実装

## 1. 調査結果と既存Gap

| 項目 | 現状 |
|---|---|
| `Execution`のMLflow列 | **未実装** → 追加済み |
| MLflow依存package | `mlflow-skinny>=2.15.0` 既存 ✓ |
| Tracker Port / Adapter | **未実装** → 作成済み |
| SDK直接呼出し | `experiments/004/run.py`でfluent API使用 → Port経由に移行済み |
| CLI MLflow options | **未実装** → 追加済み |
| `mlflow_tracking_status`設定 | **未実装** → ExecutionServiceで設定済み |
| Worker MLflow ensure | **未実装** → 実装済み |
| `shared/identity.py` | `ExecutionIdentity` / `cli_identity` / `web_identity` 既存 ✓ |

### 1.1 要件と実装のGap（未解決）

| Gap | 内容 | 対応 |
|---|---|---|
| Run作成不能時の計算停止是非 | 要件に明示なし | 最小限安全policy: 計算継続・`mlflow_tracking_status=ERROR`記録 |
| metrics記録失敗時の扱い | 要件に明示なし | 警告ログを出して継続 |
| Artifact upload失敗時の扱い | 要件に明示なし | `TrackingArtifactError`を記録して継続 |
| terminate失敗時の扱い | 要件に明示なし | `mlflow_tracking_status=ERROR`に更新して継続 |

---

## 2. 実装した成果物

### 2.1 新規ファイル

| ファイル | 役割 |
|---|---|
| `src/ariadne/application/ports/experiment_tracker.py` | `ExperimentTracker` Protocol + `TrackingRunReference` |
| `src/ariadne/infrastructure/tracking/__init__.py` | trackingモジュール公開 |
| `src/ariadne/infrastructure/tracking/exceptions.py` | Tracking例外階層（接続/認証/NotFound/Duplicate/Artifact/Terminal/Disabled） |
| `src/ariadne/infrastructure/tracking/redaction.py` | Secret redactionユーティリティ |
| `src/ariadne/infrastructure/tracking/settings.py` | `TrackingSettings`（CLI引数 > 環境変数 > デフォルト） |
| `src/ariadne/infrastructure/tracking/mlflow_tracker.py` | `MlflowClient`ベースのMLflow Adapter |
| `src/ariadne/infrastructure/tracking/null_tracker.py` | NullTracker（SDK呼出しなし・疑似ID生成なし） |
| `migrations/versions/20260804_0004_mlflow_tracking_columns.py` | Alembic migration（upgrade/downgrade） |
| `tests/unit/test_secret_redaction.py` | redactionユニットテスト |
| `tests/unit/test_null_tracker.py` | NullTrackerユニットテスト |
| `tests/unit/test_mlflow_tracker.py` | MlflowTrackerユニットテスト（mock使用） |
| `tests/unit/test_execution_mlflow_columns.py` | Executionドメインモデル / ExecutionServiceテスト |
| `tests/unit/test_worker_mlflow.py` | Worker ensure / terminate integration test |
| `tests/integration/test_mlflow_tracking.py` | 実MLflow SQLiteバックエンドを使ったintegration test |

### 2.2 変更ファイル

| ファイル | 変更内容 |
|---|---|
| `src/ariadne/domain/metadata.py` | `Execution`に`mlflow_experiment_id`・`mlflow_run_id`・`mlflow_tracking_status`・`mlflow_tracking_error`を追加。partial unique index（非NULLのみ）・CHECK constraint追加 |
| `src/ariadne/infrastructure/settings.py` | `WebSettings`に`mlflow_tracking_uri`・`mlflow_experiment_name`・`mlflow_enabled`・`mlflow_timeout_seconds`・`mlflow_tag_prefix`を追加 |
| `src/ariadne/application/run_execution/services.py` | `ExecutionService.create()`でmode別に`mlflow_tracking_status`を設定（`DRY_RUN`/`VALIDATE_ONLY`→`NOT_REQUIRED`、`RUN`→`PENDING`） |
| `src/ariadne/workers/executor.py` | `_build_tracker()`・`_ensure_mlflow_run()`（冪等・tag検索・重複検出）・`_terminate_mlflow_run()`を追加。成功/失敗/cancel時にMLflow terminal statusを反映 |
| `src/ariadne/interfaces/cli/pipeline.py` | `--mlflow-tracking-uri`・`--mlflow-experiment`・`--mlflow-run-name`・`--resume-mlflow-run-id`・`--disable-mlflow`を追加。CLIトラッキングbootstrap実装 |
| `experiments/004_discovery_inference_integration/run.py` | fluent API (`mlflow.start_run()`) からMlflowTracker Portへ移行。`format_validation`出力追加 |
| `pyproject.toml` | `mlflow`マーカーを追加 |

---

## 3. 設計の要点

### 3.1 DB制約とApplication invariantの分担

| 制約 | 場所 | 内容 |
|---|---|---|
| `mlflow_tracking_status` CHECK | DB | `NOT_REQUIRED`/`PENDING`/`ACTIVE`/`FINISHED`/`ERROR`のみ許可 |
| `mlflow_run_id` partial unique | DB | 非NULL値に対してのみ一意。複数NULLを許容 |
| `ACTIVE`/`FINISHED`で`mlflow_run_id`が必要 | Application | DB CHECKは設けず（障害回復の中間状態を許容するため） |
| `NOT_REQUIRED`では`mlflow_run_id IS NULL` | Application | 同上 |

### 3.2 障害窓と回復方針

| 障害窓 | 回復方針 |
|---|---|
| MLflow Run作成後・DB保存前にcrash | Worker再実行時に`ariadne.execution_id` tag検索でRunを回収 |
| 複数Run一致 | 自動選択せず`TrackingDuplicateRunError`→`mlflow_tracking_status=ERROR` |
| MLflow ensemble失敗 | `mlflow_tracking_status=ERROR`・`mlflow_tracking_error`にredacted概要を保存・計算は継続 |
| terminate失敗 | `mlflow_tracking_status=ERROR`に更新・例外を伝播しない |

### 3.3 MLflow 2.15+対応事項

- ファイルバックエンド（`file:./mlruns`）は廃止予定。デフォルトを`sqlite:///mlflow.db`に変更
- `MlflowClient.create_run()`の`tags`引数は`dict[str, str]`（`RunTag`リストではない）
- `MlflowClient.log_batch()`の`params`/`metrics`/`tags`は各エンティティオブジェクトのリスト

---

## 4. Traceability Matrix

| Requirement ID | 規範要件 | 実装ファイル | テストファイル | Status | Evidence / Gap |
|---|---|---|---|---|---|
| DM-EX-MLF-01 | `execution`にMLflow関連列追加 | `domain/metadata.py` | `test_execution_mlflow_columns.py` | Implemented | 4列追加・partial unique・CHECK |
| DM-EX-MLF-02 | 非NULL `mlflow_run_id`一意・複数NULL許容 | `domain/metadata.py` | `test_execution_mlflow_columns.py` | Implemented | partial unique index |
| DM-EX-MLF-03 | tracking状態のDB CHECK | `domain/metadata.py` + migration | `test_migration_schema.py` | Implemented | CHECK constraint |
| PORT-01 | MLflow非依存のApplication Port | `ports/experiment_tracker.py` | `test_mlflow_tracker.py` | Implemented | Protocol定義 |
| PORT-02 | `TrackingRunReference`明示型 | `ports/experiment_tracker.py` | `test_mlflow_tracker.py` | Implemented | frozen dataclass |
| ADAPT-01 | MLflow Adapter（`MlflowClient`ベース） | `tracking/mlflow_tracker.py` | `test_mlflow_tracker.py` + `test_mlflow_tracking.py` | Implemented | global state非依存・explicit run_id |
| ADAPT-02 | Null Adapter | `tracking/null_tracker.py` | `test_null_tracker.py` | Implemented | SDK非呼出し・疑似ID生成なし |
| ADAPT-03 | bounded retry | `tracking/mlflow_tracker.py` | `test_mlflow_tracker.py` | Implemented | `max_retry_attempts`設定可能 |
| ADAPT-04 | secret redaction | `tracking/redaction.py` | `test_secret_redaction.py` | Implemented | password/token/credential等 |
| CFG-01 | MLflow設定の一元解決 | `tracking/settings.py` + `settings.py` | — | Implemented | CLI引数>環境変数>デフォルト |
| API-01 | API受付時にMLflow Run未作成 | `services.py` | `test_execution_mlflow_columns.py` | Implemented | `PENDING`/`NOT_REQUIRED`のみ設定 |
| API-02 | `DRY_RUN`/`VALIDATE_ONLY`→`NOT_REQUIRED` | `services.py` | `test_execution_mlflow_columns.py` | Implemented | mode分岐 |
| WORKER-01 | Worker開始時に冪等ensure | `workers/executor.py` | `test_worker_mlflow.py` | Implemented | `_ensure_mlflow_run` |
| WORKER-02 | Run作成後DB保存前crash回復 | `workers/executor.py` | `test_worker_mlflow.py` | Implemented | tag検索でRunを回収 |
| WORKER-03 | 重複Run自動選択しない | `workers/executor.py` | `test_worker_mlflow.py` | Implemented | `TrackingDuplicateRunError` |
| WORKER-04 | 成功時FINISHED・失敗時FAILED・cancel時KILLED | `workers/executor.py` | `test_worker_mlflow.py` | Implemented | `_terminate_mlflow_run` |
| WORKER-05 | MLflow障害で計算を止めない | `workers/executor.py` | `test_worker_mlflow.py` | Implemented | 例外を握り潰さず`ERROR`記録して継続 |
| CLI-01 | `--disable-mlflow`でNullTracker | `interfaces/cli/pipeline.py` | — | Implemented | `NullTracker`使用 |
| CLI-02 | `--resume-mlflow-run-id` | `interfaces/cli/pipeline.py` | — | Implemented | 既存Run再開 |
| CLI-03 | CLIはAriadne Executionを作成しない | `interfaces/cli/pipeline.py` | `test_cli_no_execution_creation.py` (既存) | Implemented | `execution_id=None` |
| CLI-04 | 実験entry pointが同じbootstrapを使用 | `experiments/004/run.py` | `test_runtime.py` | Implemented | fluent APIから移行 |
| SEC-01 | credentialをDB/log/tag/paramへ漏らさない | `tracking/redaction.py` | `test_secret_redaction.py` | Implemented | `redact_secret`適用 |
| MIG-01 | Alembic migration（upgrade/downgrade） | `migrations/versions/20260804_0004_*` | `test_migration_schema.py` | Implemented | 既存データ保持・バックフィル |
| MIG-02 | fresh DBとupgraded DBのschema一致 | migration | `test_migration_schema.py` | Implemented | 既存テストが検証 |

---

## 5. 実行したテストコマンドと結果

```
python -m pytest tests/unit/ tests/integration/ -q --tb=no
190 passed, 13 warnings in 317.10s (0:05:17)
```

### テストスイート別内訳

| スイート | テストファイル | 結果 |
|---|---|---|
| unit (redaction) | `test_secret_redaction.py` | 11 passed |
| unit (null tracker) | `test_null_tracker.py` | 8 passed |
| unit (mlflow tracker) | `test_mlflow_tracker.py` | 21 passed |
| unit (execution columns) | `test_execution_mlflow_columns.py` | 7 passed |
| unit (worker mlflow) | `test_worker_mlflow.py` | 8 passed |
| integration (mlflow) | `test_mlflow_tracking.py` | 14 passed |
| integration (migration) | `test_migration_schema.py` | 8 passed |
| 既存テスト全体 | tests/unit/ + tests/integration/ | 190 passed (regression 0件) |

---

## 6. 未解決Gap一覧

| Gap ID | 内容 | 採用した最小限安全policy |
|---|---|---|
| GAP-01 | Run作成不能時に計算を停止するか | 継続。`mlflow_tracking_status=ERROR`・`mlflow_tracking_error`に記録 |
| GAP-02 | metrics記録失敗時に計算結果を成功扱いできるか | 継続。警告ログを出力 |
| GAP-03 | Artifact upload失敗時の扱い | 継続。`TrackingArtifactError`を記録 |
| GAP-04 | terminate失敗時の扱い | `mlflow_tracking_status=ERROR`に更新。Ariadne Execution statusには影響しない |
| GAP-05 | concurrencyテスト（実PostgreSQL + 複数Worker） | 設計上DB unique constraintで最終的に一意性を保証。実PostgreSQL並行テストは未実施（postgres環境なし） |
