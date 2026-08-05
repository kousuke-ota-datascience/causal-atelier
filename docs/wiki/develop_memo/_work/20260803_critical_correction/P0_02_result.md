# 最終報告: Migrationの再現性・安全性修正

## 1. 根本原因

`20260719_0001_initial_metadata.py` が `Base.metadata.create_all()` / `drop_all()` を呼び出しており、将来のORM変更によって同じrevisionを適用した結果が変化するという問題。`20260720_0002_analysis_ready_mvp.py` も `model.__table__.create(bind=bind, checkfirst=True)` で現在のORMモデルに依存していた。

## 2. 採用したmigration方針

既存revisionを**直接書き換え**（このrepositoryに本番DBへの配布実績がなく、テスト前提から判断）。ORM依存を排除し、revision作成時点のスキーマをAlembic operationで固定する。Run→Executionのリネームは0003のguarded renames で継続対応する。

## 3. 変更ファイル一覧

| ファイル | 変更内容 |
|---------|---------|
| `migrations/versions/20260719_0001_initial_metadata.py` | 完全書き換え：全テーブルをRun-era名で明示的DDL (`op.create_table`) で作成。`downgrade()` も明示的 `op.drop_table` |
| `migrations/versions/20260720_0002_analysis_ready_mvp.py` | 完全書き換え：新テーブル7個を明示的DDLで作成、既存テーブルへの列追加も `op.add_column` で固定 |
| `tests/integration/test_migration_schema.py` | 新規作成：8テスト（ORM独立性・新規DB・アップグレードパス・等価性） |

## 4. スキーマ変更内容

### 0001（固定）
- `run`, `stage_run`, `stage_run_dependency`, `stage_attempt`, `stage_run_input_preparation`, `stage_attempt_input_preparation`, `run_event`, `validation_run` 等、全テーブルをRun-era名で明示DDL化
- use_alter FK（`fk_dataset_version_origin_stage_run`, `fk_data_profile_artifact`）はPostgreSQL限定で明示的に作成・削除
- `run_event` のappend-onlyトリガーを正しくRun-era名（`run_event`）で定義
- `downgrade()` で全テーブルを依存逆順でdrop、PostgreSQLのトリガー・関数も明示的にdrop

### 0002（固定）
- 新規テーブル7個を明示的 `op.create_table` で作成：
  - `analysis_dataset_binding`
  - `feature_semantics_dataset_binding`
  - `causal_graph`
  - `causal_graph_version`（check constraintあり）
  - `causal_graph_node`
  - `causal_graph_edge`（check constraintあり）
  - `stage_run_graph_input`（Run-era名、0003でリネーム）
- 既存テーブルへの列追加を `op.add_column` で固定：
  - `pipeline_stage_definition.input_mode`
  - `stage_run.input_mode`
  - `feature_semantic_item`: `dataset_column_id`, `categorical`, `allowed_for_discovery`, `time_metadata_json`, `description`
  - `causal_design_projection`: `dataset_version_id`, `causal_graph_version_id`, `target_population`, `adjustment_strategy`, `adjustment_set_json`, `analyst_note`
  - `discovery_result`: `input_mode`, `feature_semantics_version_id`, `input_preparation_attempt_id`, `resolved_semantics_artifact_id`
  - `edge_weight_result`: `input_mode`, `feature_semantics_version_id`, `causal_graph_version_id`, `input_preparation_attempt_id`
  - `treatment_effect_result`: `input_mode`, `causal_graph_version_id`, `input_preparation_attempt_id`
- nullability変更（`discovery_feature_version_id`, `inference_feature_version_id` × 2をnullable化）はPostgreSQL限定guard
- `downgrade()` で追加列を `op.drop_column` / `batch_alter_table` で削除、追加テーブルを依存逆順でdrop

### 0003（変更なし）
- Guards付きrename処理はすでに正しい（`old_table in tables and new_table not in tables` チェック）
- `stage_run_graph_input` → `stage_execution_graph_input` の処理が固定0002と整合する

## 5. データ保持の検証内容

- `upgrade head` → `downgrade base` → `upgrade head` サイクルがSQLiteで正常動作
- 全65テーブルが `upgrade head` 後に存在することを確認
- `downgrade base` 後にアプリケーションテーブルが0件であることを確認
- `stage_attempt_input_preparation` テーブルはリネームなし、column `stage_run_id` → `stage_execution_id` のみ（0003）
- 旧Run名テーブルは0001で作成され、0003でguardつきリネームにより既存DB上でもExecutionへ移行される

## 6. テストコマンドと結果

### 新規migrationテスト

```
python -m pytest tests/integration/test_migration_schema.py -v
```

```
tests/integration/test_migration_schema.py::test_initial_revision_has_no_orm_dependency PASSED
tests/integration/test_migration_schema.py::test_second_revision_has_no_orm_dependency PASSED
tests/integration/test_migration_schema.py::test_fresh_upgrade_head_creates_all_orm_tables PASSED
tests/integration/test_migration_schema.py::test_fresh_upgrade_head_has_no_unexpected_tables PASSED
tests/integration/test_migration_schema.py::test_upgrade_step_by_step_reaches_all_tables PASSED
tests/integration/test_migration_schema.py::test_downgrade_base_drops_all_tables PASSED
tests/integration/test_migration_schema.py::test_upgrade_downgrade_upgrade_is_idempotent PASSED
tests/integration/test_migration_schema.py::test_fresh_path_equals_step_by_step_path PASSED

8 passed in 42.70s
```

### 既存テスト（回帰確認）

```
python -m pytest tests/ --ignore=tests/integration/test_migration_schema.py
```

```
62 passed, 1 failed
```

失敗は `test_cli_validate_only_and_dry_run_smoke`（変更前から存在する無関係なCLI smoke test）。

## 7. 残存リスク

| リスク | 影響範囲 | 備考 |
|--------|---------|------|
| PostgreSQL trigger test（Category E）未実装 | `execution_event` / `audit_event` のappend-only、`artifact` 等のimmutabilityトリガー | PostgreSQL接続が必要。SQLiteではトリガーが強制されないため別途CI環境でのテストが必要 |
| SQLite FK非強制 | `if is_pg` ブロック内のFK制約がSQLite testで作成・検証されない | 設計上の限界として`test_migration_schema.py`のdocstringに明記済み |
| 既存旧DB（配布済みの場合） | 0002実行済みDBでは `stage_execution_input_preparation` が0002で作成済みのため、0003の`stage_run_input_preparation`リネームがskipされる | 本repositoryに本番配布DBの証拠なし。存在する場合は別途repair migrationが必要 |
