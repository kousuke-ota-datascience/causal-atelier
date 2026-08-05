# Coding Agent Prompt: P0 Migrationの再現性・安全性修正

## 目的

AriadneのAlembic migrationを、revisionごとに再現可能で、既存データを保持し、新規DBとupgrade済みDBのschemaが一致する構成へ修正してください。

本作業の最優先事項は、初期migrationが実行時点の最新ORM metadataへ依存している問題を除去することです。現状の `20260719_0001_initial_metadata.py` は `Base.metadata.create_all()` と `Base.metadata.drop_all()` を呼び出しており、revision作成時点のDDLが固定されていません。この構造では、ORM変更後に空DBへmigrationを適用した結果が変化し得ます。

## 作業前に参照するファイル

最初に、少なくとも以下を全文確認してください。ファイル名や配置が異なる場合は、repository内検索により実体を特定してください。

- `ariadne/alembic/versions/20260719_0001_initial_metadata.py`
- `ariadne/alembic/versions/` 配下の全revision
- `ariadne/alembic/env.py`
- `ariadne/src/ariadne/domain/metadata.py`
- `ariadne/src/ariadne/infrastructure/persistence/models.py`
- `ariadne/src/ariadne/application/run_execution/`
- migration test、schema test、DB fixture
- `ariadne/docs/wiki/requirement_definition/02_data_model_definition_v1.4.md`
- Execution語彙へ改訂済みのデータモデル定義書がrepositoryに存在する場合は、その最新版

作業開始前に、次を一覧化してください。

1. Alembic revision graph
2. 各revisionが作成・変更するtable、column、FK、index、unique constraint、check constraint、trigger、function
3. 現行ORM metadataとの差分
4. 旧Run系物理名称の有無
5. PostgreSQL専用DDLとSQLite test代替処理

## 必須要件

### 1. 初期revisionを固定DDLへ変更する

`20260719_0001_initial_metadata.py` から、次の実行時ORM依存を除去してください。

```python
Base.metadata.create_all(...)
Base.metadata.drop_all(...)
```

代わりに、revision作成時点のschemaを明示的なAlembic operationとして固定してください。

使用対象の例:

- `op.create_table`
- `op.drop_table`
- `op.create_index`
- `op.drop_index`
- `op.create_foreign_key`
- `op.create_unique_constraint`
- `op.create_check_constraint`
- `op.execute`

初期revision内でapplication ORM modelまたは現在の`Base.metadata`をimportしてはなりません。revision実行結果が、将来のORM変更により変化しないようにしてください。

### 2. revision履歴の意味を維持する

既存の後続revisionがある場合、初期revisionへ現在の最終schemaを丸ごと埋め込まないでください。

- 初期revisionは初期時点のschemaだけを作成する
- 後続変更は既存または新規revisionで適用する
- 同じtable、column、constraintを複数revisionで重複作成しない
- 空DBへ`upgrade head`した結果と、既存の旧revision DBを`upgrade head`した結果を一致させる

revisionの改変が既存配布環境で危険な場合は、既存revisionを直接書き換える方針と、新しい修復revisionを追加する方針の影響を評価してください。ただし、単に問題を説明して終了せず、このrepositoryの配布状況とtest前提から最も安全な方針を選び、実装してください。

### 3. RunからExecutionへの移行をデータ保持renameとして扱う

旧schemaまたは旧revisionに次の名称が存在する場合、drop-and-createではなくrenameを優先してください。

```text
run                                -> execution
stage_run                          -> stage_execution
run_event                          -> execution_event
validation_run                     -> validation_execution
run_result_summary                 -> execution_result_summary
stage_run_dependency               -> stage_execution_dependency
stage_run_dataset_input            -> stage_execution_dataset_input
stage_run_config_input             -> stage_execution_config_input
stage_run_artifact_input           -> stage_execution_artifact_input
stage_run_graph_input              -> stage_execution_graph_input
stage_run_parameter                -> stage_execution_parameter
stage_run_input_preparation        -> stage_execution_input_preparation
```

対応するcolumnも必要に応じてrenameしてください。

```text
run_id                             -> execution_id
stage_run_id                       -> stage_execution_id
retry_of_run_id                    -> retry_of_execution_id
reused_from_stage_run_id           -> reused_from_stage_execution_id
origin_stage_run_id                -> origin_stage_execution_id
validation_run_id                  -> validation_execution_id
```

以下も漏れなく更新してください。

- Foreign Key
- Index
- Unique Constraint
- Check Constraint
- PostgreSQL trigger
- PostgreSQL function内のtable名参照
- ORM queryが期待する物理名称
- Outbox payload migrationが必要な場合のJSON key
- Audit `resource_type`
- seed data
- fixture

旧名称が実際には一度も永続化されていない場合、不要なrename migrationを捏造しないでください。その場合は、revision履歴とtest fixtureに基づき「rename不要」をコードコメントまたは検証資料に明記してください。

### 4. PostgreSQLの不変性・append-only制約を維持する

現行migrationにある以下の保護を失わないでください。

- published configuration contentの不変性
- ready dataset version contentの不変性
- published pipeline definition versionの不変性
- dataset table contentの不変性
- available artifact contentの不変性
- `execution_event`のappend-only
- `audit_event`のappend-only

Execution改称後のtable名と整合するよう、triggerおよびfunctionを確認してください。

`downgrade()`では、triggerやfunctionのdrop順序を含め、依存関係違反が起きないようにしてください。

### 5. downgradeをrevision固定にする

`Base.metadata.drop_all()`は禁止です。

`downgrade()`は、そのrevisionが`upgrade()`で作成・変更したobjectだけを、依存関係の逆順で戻してください。

- 後続revisionで追加されたtableを初期revisionのdowngradeが暗黙にdropしない
- extension、function、trigger、index、constraintのdropを明示する
- downgrade非対応とする場合は、黙って全dropせず、repository方針に沿った明示的な扱いにする

### 6. schema drift検証を追加する

少なくとも次の自動testを追加してください。

#### A. Fresh database test

1. 空DBを作成
2. `alembic upgrade head`
3. 実際のDB schemaをintrospect
4. 現行ORM metadataと比較
5. table、column、型、nullable、PK、FK、index、unique、checkの差分がないことを検証

#### B. Upgrade path test

1. 対象となる旧revisionまでupgrade
2. 代表データを投入
3. `alembic upgrade head`
4. データが保持されることを検証
5. PK、FK、idempotency、retry関係、Stage Execution、Stage Attempt、Eventが保持されることを検証

#### C. Fresh vs upgraded equivalence test

- 空DBからheadへ到達したschema
- 旧revisionからheadへ到達したschema

上記を正規化して比較し、同一であることを検証してください。

#### D. ORM独立性test

初期revisionが次をimportまたは呼び出していないことを検証してください。

```text
ariadne.domain.metadata
ariadne.infrastructure.persistence.models.Base
Base.metadata.create_all
Base.metadata.drop_all
```

#### E. PostgreSQL trigger test

PostgreSQL環境で、保護対象rowの禁止UPDATEおよびappend-only tableのUPDATE/DELETEが失敗することを検証してください。

SQLiteではPostgreSQL triggerと同等でないことを隠さず、SQLite testの保証範囲を明示してください。

## 実装上の禁止事項

- データを失うdrop-and-createをrenameの代用にしない
- revision実行中にapplication serviceを呼ばない
- revision実行中に最新ORM classを参照しない
- migration testをSQLiteだけで完了扱いにしない
- testを通すためにFK、unique、check、triggerを削除しない
- 既存データを仮定で補完しない
- migration失敗を握り潰さない
- `checkfirst=True`でschema不整合を隠さない

## 期待する成果物

1. 修正済みAlembic revision
2. 必要ならRun→Executionの明示的rename revision
3. migration test一式
4. schema equivalence test
5. PostgreSQL trigger test
6. migration方針を説明する短い文書または既存文書の更新
7. 変更したfile一覧
8. 実行したtest commandと結果
9. 未解決事項がある場合、その根拠と影響範囲

## 完了条件

次をすべて満たした場合のみ完了としてください。

- `alembic upgrade head`が空PostgreSQL DBで成功する
- 対象旧revisionから`upgrade head`が成功する
- 代表データが保持される
- fresh DBとupgraded DBのschemaが一致する
- head schemaと現行ORM metadataが一致する
- 初期revisionが現在のORM metadataへ依存しない
- downgradeが現在のORM metadataへ依存しない
- Execution語彙の物理名称、FK、index、triggerが整合する
- PostgreSQLの不変性・append-only制約が維持される
- 全migration testが成功する

## 最終報告形式

最終回答は次の順で出力してください。

1. 根本原因
2. 採用したmigration方針
3. 変更file一覧
4. schema変更内容
5. データ保持の検証内容
6. test commandと結果
7. 残存リスク

