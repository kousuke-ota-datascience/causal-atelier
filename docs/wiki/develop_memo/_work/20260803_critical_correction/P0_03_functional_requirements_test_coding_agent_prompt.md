# Coding Agent Prompt: 機能要件テスト体系の構築と不足テストの実装

## 0. ミッション

Ariadneの要件定義書に記載された機能要件を、テストケース、実行可能な自動テスト、実行結果へ追跡できる状態にしてください。

本作業の目的は、単にpytestの件数やcoverage率を増やすことではありません。各規範的な機能要件について、次の連鎖を証明可能にすることです。

```text
機能要件ID
  -> 受入条件
    -> テストケースID
      -> 自動テスト
        -> 実行環境
          -> 実行結果
```

根拠なしに「テスト済み」「実装済み」と判定してはなりません。既存テストを最大限再利用し、不足分だけを追加してください。

---

## 1. 作業前に必ず調査する対象

ファイル配置や名称が異なる場合はrepository内を検索して実体を特定してください。

### 1.1 規範文書

- `ariadne/docs/wiki/requirement_definition/01_web_service_requirements_v1.4.md`
- 上記より新しい要件定義書が存在する場合は最新版
- `ariadne/docs/wiki/requirement_definition/02_data_model_definition_v1.4.md`
- Execution語彙へ改訂済みのデータモデル設計書が存在する場合は最新版
- Execution管理とMLflow実験追跡の責務分離に関する文書
- API仕様
- CLI仕様
- Webサービス運用ガイド
- 再現性、セキュリティ、権限、Artifact、Workerに関する設計文書

### 1.2 実装

- `ariadne/src/ariadne/interfaces/api/`
- `ariadne/src/ariadne/interfaces/cli/`
- `ariadne/src/ariadne/application/`
- `ariadne/src/ariadne/workers/`
- `ariadne/src/ariadne/domain/metadata.py`
- `ariadne/src/ariadne/causal/discovery/`
- `ariadne/src/ariadne/causal/inference/`
- `ariadne/src/ariadne/causal/design/`
- `ariadne/src/ariadne/infrastructure/`
- `ariadne/alembic/`
- frontendがMVP受入条件に含まれる場合は`ariadne/frontend/`
- `experiments/004_discovery_inference_integration/`

### 1.3 既存テストとCI

- `ariadne/tests/`配下の全テスト
- pytest configuration
- fixture、factory、seed、sample dataset
- Docker Compose test構成
- PostgreSQL test構成
- CI workflow
- coverage configuration
- test report生成設定

---

## 2. 最初に作成する調査成果物

コードを変更する前に、以下を作成してください。

### 2.1 機能要件インベントリ

要件定義書から、規範的な機能要件をすべて抽出してください。

対象:

- `FR-*`形式の要件ID
- 「すること」「してはならない」と記述されたMVP必須要件
- MVP価値V-001、V-002、V-003を成立させる機能
- 状態遷移
- RBAC
- 冪等性
- Artifactおよびlineage
- 非同期Execution、Outbox、Worker、lease、heartbeat、retry、cancel
- Analysis-ready Dataset
- Feature Semantics
- Discovery
- Graph比較・選択・保存
- Causal Design
- Inference
- 診断
- 再現性および来歴
- 既存CLI、ETL、Feature Buildの後方互換性

同じ内容が複数文書に重複する場合、正本を特定し、重複要件を別件として水増ししないでください。文書間に矛盾がある場合は、勝手に一方を採用せず「Blocked by requirement conflict」と記録してください。

### 2.2 既存テストインベントリ

各既存テストについて、以下を記録してください。

- test file
- test function／class
- test level
- 対象機能
- 前提環境
- database種別
- 外部Adapterの実物／fake／mock
- 正常系／異常系／回復系
- assertionの要点
- 対応可能な要件ID

テスト名だけで対応要件を推測しないでください。テスト本体とassertionを読んで判定してください。

### 2.3 初期Traceability Matrix

次の形式で作成してください。

| Requirement ID | 規範要件 | 受入条件 | Test Case ID | Test File / Function | Level | Environment | Status | Evidence / Gap |
|---|---|---|---|---|---|---|---|---|

`Status`は以下に限定してください。

- `Covered`
- `Partially Covered`
- `Not Covered`
- `Blocked by Requirement Conflict`
- `Not Applicable`

`Covered`は、要件の全受入条件を実行可能なテストがassertしている場合だけ使用してください。

---

## 3. テスト設計原則

### 3.1 テストレベル

機能要件ごとに最小限必要なレベルを選択してください。

- Unit: 純粋なdomain rule、validator、数値helper
- Component: Application Service、Repository Adapter、Artifact Adapter
- API integration: FastAPIとDB transaction、RBAC、HTTP契約
- Worker integration: Outbox、claim、lease、Attempt、Result projection
- Database integration: PostgreSQL FK、UNIQUE、CHECK、trigger、transaction
- CLI integration: 実際のCLI entry pointとfilesystem／tracking Adapter
- End-to-End: DatasetからInference、診断、lineageまでのMVP Journey
- Scientific validation: 既知DGPを持つsynthetic dataによる統計的検証

すべてをE2Eへ寄せず、同時にすべてをmock unit testで済ませないでください。

### 3.2 テストケース構造

各テストケースは、可能な限り次を明記してください。

```text
Test Case ID
Requirement ID
目的
前提条件
入力
操作
期待結果
検証対象外
実行環境
```

pytest testには、要件IDとテストケースIDをmarker、docstring、parameter、または隣接metadataで追跡可能にしてください。

例:

```python
@pytest.mark.requirement("FR-EXE-001")
@pytest.mark.test_case("FT-EXE-001")
def test_submit_execution(...):
    ...
```

既存のtest metadata方式がある場合はそれを優先してください。

### 3.3 合否基準

- HTTP statusだけをassertして完了にしない
- DB状態、Event、Outbox、Artifact、Result、Audit、hash、lineageも要件に応じて確認する
- error message文字列だけに過剰依存しない
- 時刻やUUIDを不安定な値で比較しない
- 並行性要件は実際の競合を発生させて確認する
- PostgreSQL固有要件をSQLiteだけで代用しない
- 数値テストは許容誤差、seed、sample size、期待する統計的性質を明示する

---

## 4. 必須テスト領域

以下は最低限の領域です。要件インベントリから追加要件が判明した場合は補完してください。

### 4.1 ProjectとRBAC

検証項目:

- Project作成者がProject Adminになる
- Viewer、Analyst、Maintainer、Project Adminの許可操作
- 権限不足時の拒否
- 別ProjectのResource参照拒否
- 論理削除済みProjectの通常取得拒否
- member追加・role変更の監査記録
- system admin経路が要件化されている場合の権限

### 4.2 DatasetとArtifact登録

検証項目:

- CSV／Parquet登録
- 要件で維持対象ならRDA／RDS登録
- 未対応拡張子の拒否
- filename sanitization
- Artifact Store保存成功とDB登録の整合
- 保存失敗時のtransaction／cleanup
- checksum、size、format、media type
- Dataset slug重複
- Dataset Version番号
- schema/content hash
- Dataset Version一覧と詳細取得
- 不変Versionの変更拒否
- Project境界

### 4.3 Analysis-ready Dataset

検証項目:

- primary table binding
- unit identifierがprimary table所属であること
- 単一table条件
- schema hash snapshot
- readiness validation
- READYへ遷移できる条件
- validation issueがある場合にREADYにしないこと
- column policyによるpreview、analysis、download制御
- mask rule
- profile取得
- 許可されない列がprofile／previewへ漏れないこと

READYの意味が要件上曖昧な場合は、テストで推測せず要件Gapとして記録してください。

### 4.4 ConfigurationとVersion

検証項目:

- Configuration作成
- Version作成
- canonical JSON／YAMLの排他入力
- content hashによる重複拒否
- validation
- publish
- PUBLISHED内容の不変性
- supersedes関係
- Project境界
- Feature SemanticsとDataset Version／Table Versionのbinding

### 4.5 Feature Semantics

検証項目:

- Dataset列からsemantic itemを作成
- treatment、outcome、covariate、identifier等のrole
- source columnの存在確認
- Dataset schema hashとの一致
- post-treatment変数のadjustment禁止
- discovery可否、adjustment可否
- PUBLISHED Versionだけを実行入力にできる条件
- Dataset Versionをまたぐ不正bindingの拒否

### 4.6 Execution受付と冪等性

検証項目:

- `POST /executions`
- `execution_id`採番
- Project RBAC
- Execution Plan固定
- Stage Execution作成
- Outbox作成
- response status
- 同一Project・同一Idempotency-Key・同一requestの再送
- 同一key・異なるrequest hashのConflict
- 別Projectでの同一key
- transaction rollback時にExecutionとOutboxが片方だけ残らないこと
- `DRY_RUN`、`VALIDATE_ONLY`、`RUN`
- Execution Event sequence

### 4.7 Execution状態遷移

最低限、許可遷移と禁止遷移をテーブル駆動で検証してください。

代表的な許可遷移:

```text
SUBMITTED -> VALIDATING
VALIDATING -> QUEUED
QUEUED -> RUNNING
RUNNING -> SUCCEEDED
RUNNING -> FAILED
QUEUED -> CANCEL_REQUESTED
RUNNING -> CANCEL_REQUESTED
CANCEL_REQUESTED -> CANCELED
```

代表的な禁止遷移:

```text
SUCCEEDED -> RUNNING
FAILED -> QUEUED on the same Execution
CANCELED -> RUNNING
```

実際の規範状態集合と遷移規則は実装ではなく要件正本から抽出してください。差異があればGapとして報告してください。

### 4.8 CancelとRetry

検証項目:

- cancel可能状態
- terminal状態でのcancel拒否
- 重複cancelの冪等性
- `CANCEL_REQUESTED` event
- `CANCEL_EXECUTION` outbox
- best-effort semantics
- retry可能状態
- retryが元Executionを上書きしないこと
- 新しいExecutionを作成する場合の`retry_of_execution_id`
- Stage Attempt retryの場合のAttempt番号
- 入力snapshotの保持
- RBACとAudit

### 4.9 Transactional OutboxとWorker

検証項目:

- API transactionとOutboxの原子性
- 未処理eventのclaim
- 複数Workerによる二重claim防止
- lease取得
- heartbeat
- lease期限切れ後の再claim
- Worker crash後の回復
- publish attemptとlast error
- 同一event再処理時の冪等性
- Attempt履歴を上書きしないこと
- 成功時のEvent、Artifact、Result projection
- 失敗時の状態、error、Event
- cancelとの競合

PostgreSQLのロックや`SKIP LOCKED`等に依存する場合、実PostgreSQLで検証してください。

### 4.10 ArtifactとLineage

検証項目:

- Stored ObjectとArtifactの責務分離
- logical IDと物理location
- AVAILABLE後のcontent不変性
- download RBAC
- local absolute pathをAPIへ返さないこと
- upstream／downstream lineage
- cross-project lineage拒否
- checksum不一致
- orphan処理方針
- Manifestとの接続

### 4.11 Discovery

検証項目:

- Analysis-ready入力
- Configured Feature Build入力の後方互換
- 複数algorithm実行
- algorithmごとのResult
- node、edge、orientation、score、stability、warning
- 同一Dataset Versionへの適用
- scientific notice
- 探索結果をtrue DAGとして表示しない契約
- 不正な列、定数列、欠損、categorical処理
- seed固定時の再現性
- 列順変更時の仕様化された性質
- failure isolation

### 4.12 Graph比較・選択・保存

検証項目:

- 同一Dataset Versionのalgorithm比較
- 共通edge／相違edge／orientation差
- 選択済みedgeからGraph Version作成
- Discovery、Dataset、Feature SemanticsのProject一致
- Dataset Version一致
- PUBLISHED Feature Semantics要求
- canonical edge ordering
- Unicode normalization
- content hash
- 同一Graph重複拒否
- node／edge projection
- Artifact保存
- Artifact lineage
- Version番号の並行作成
- VALIDからPUBLISHEDへの遷移
- PUBLISHED Graph Versionの不変性

### 4.13 Causal Design

検証項目:

- treatment
- outcome
- estimand
- unit
- time zero／outcome window
- target population
- adjustment strategy／adjustment set
- declared assumptions
- Dataset、Feature Semantics、Graph Versionとの整合
- cross-project拒否
- publish前validation
- published designの不変性

### 4.14 Inference

検証項目:

- Edge WeightとTreatment Effectのmode分離
- Graph Version入力
- Causal Design入力
- Dataset Version一致
- treatment／outcome列の存在
- treatmentがbinary等、estimator前提の検証
- adjustment変数選択
- post-treatment除外
- missing／constant／collinearity処理
- IPW、AIPW等の要件対象estimator
- estimate、standard error、confidence interval
- overlap、effective sample size、extreme weight等の診断
- selected／excluded adjustment variableのprojection
- assumptionsの表示
- scientific notice
- Artifact、Manifest、lineage

### 4.15 Scientific Validation

既知のDGPを持つsynthetic datasetを使用してください。乱数seedを固定し、期待値と許容誤差を明示してください。

最低限:

- 既知ATEに対するestimatorの回復
- 交絡あり／なし
- overlap良好／不足
- treatment単一値
- outcome欠損
- 極端propensity
- 調整変数なし
- post-treatment変数が候補に入る場合
- estimator非収束または警告

単一の小標本結果が理論値に偶然近いことをもって正当性を証明しないでください。必要に応じて複数seedまたは統計的property testを用いてください。ただしCIを不安定にしない設計にしてください。

### 4.16 Result、診断、来歴

検証項目:

- ExecutionからResult一覧を取得
- Result ID、type、status、URL
- Discovery、Edge Weight、Treatment Effect詳細
- Dataset Versionへの遡及
- Feature Semanticsへの遡及
- Graph Versionへの遡及
- Causal Designへの遡及
- selected adjustment set
- diagnostic
- Artifact lineage
- Manifest hash
- Project RBAC

### 4.17 CLIと後方互換

正本要件に従い検証してください。

最低限:

- 既存CLI invocation
- Complete Journey ETL
- 既存Feature Build
- default input modeの後方互換
- CLIとWebが共通Application Serviceを利用する範囲
- CLI identity方針
- deprecated optionがある場合の警告
- import可能な既存classの維持
- regression testの維持

要件正本が矛盾している場合、矛盾をテスト実装で勝手に解消しないでください。

### 4.18 PostgreSQL制約とMigration

検証項目:

- FK
- UNIQUE
- partial unique index
- CHECK
- timezone-aware column
- append-only trigger
- Version不変trigger
- Artifact不変trigger
- fresh migration
- upgrade migration
- freshとupgradedのschema一致
- 代表データ保持

SQLite testは補助として使用してよいですが、PostgreSQL固有要件の代替にはしないでください。

### 4.19 セキュリティ上の機能要件

要件に明記された範囲をテストしてください。

- Project境界
- RBAC
- column policy
- path traversal防止
- filename sanitization
- secret redaction
- Artifact location非公開
- YAMLのsafe load
- unsupported format拒否
- error responseへ秘密情報を含めない
- audit記録

追加のpenetration testを実施する場合は、要件テストと探索的security testを区別してください。

---

## 5. MVP End-to-Endテスト

少なくとも次の一連のJourneyを、同一Project内で自動実行してください。

```text
Project作成
-> Analyst割当て
-> Analysis-ready CSVまたはParquet登録
-> Dataset Version作成
-> Analysis Dataset BindingをREADY化
-> Feature Semantics Version作成・検証・publish
-> Discovery Execution作成
-> Worker実行
-> 複数algorithm result取得
-> algorithm比較
-> Causal Graph作成
-> Graph Version選択・保存・publish
-> Causal Design作成・検証・publish
-> Inference Execution作成
-> Worker実行
-> Treatment Effect Result取得
-> 診断確認
-> Dataset、Semantics、Discovery、Graph、Design、Artifactへのlineage確認
```

このE2Eでは、少なくとも以下をassertしてください。

- すべてのResourceが同一Project境界にある
- 参照したVersion IDとhashが固定されている
- ExecutionとStage Executionの状態が正しく進む
- Event sequenceが一貫する
- ResultがExecutionから取得できる
- Graph選択がInferenceへ明示的に接続される
- 推定値だけでなく診断・仮定・来歴が取得できる
- Discovery edgeをtrue DAG、Edge Weightを識別済み因果効果として表現しない

さらに以下のnegative E2Eを追加してください。

- 別ProjectのDataset／Graph／Designを混在させると拒否
- Dataset Version不一致でGraph Version作成を拒否
- 未publishのSemanticsまたはDesignを使用して拒否
- 権限不足のViewerによる作成操作を拒否

---

## 6. Test Data方針

- 実在の個人情報・機密データをtest fixtureへ含めない
- synthetic dataであることを明示する
- small fixtureとscientific validation datasetを分離する
- hash検証用データはbyte-levelで安定化する
- timezone、Unicode、null、categorical、large integerを含む境界fixtureを用意する
- testごとに独立したProject／Datasetを作成する
- test orderへ依存しない
- random seedを固定する

---

## 7. CI構成

テストを少なくとも以下へ分類してください。

```text
unit
component
api
postgres
worker
cli
e2e
scientific
```

推奨marker例:

```text
@pytest.mark.unit
@pytest.mark.postgres
@pytest.mark.worker
@pytest.mark.e2e
@pytest.mark.scientific
@pytest.mark.requirement("FR-...")
```

CIでは、少なくとも次を実行してください。

1. fast suite: unit、component
2. PostgreSQL integration suite
3. API／Worker suite
4. CLI regression suite
5. MVP E2E suite
6. scientific validation suite
7. requirement coverage report生成

CI時間短縮だけを理由にPostgreSQL、Worker、E2E、scientific suiteを恒常的にskipしないでください。実行頻度を分ける場合も、mergeまたはreleaseのgateを明示してください。

---

## 8. Requirement Coverage Report

自動または半自動で次を生成してください。

- 全機能要件数
- Covered
- Partially Covered
- Not Covered
- Blocked by Requirement Conflict
- テスト失敗中の要件
- 要件IDごとのtest file／function
- 最終実行結果

数値は実際の抽出結果から計算し、推測しないでください。

coverage reportはline coverageと分離してください。line coverageが高くても、要件coverageの代替にはなりません。

出力例:

```text
artifacts/requirements-test-report.md
artifacts/requirements-traceability.csv
artifacts/junit.xml
```

repositoryの既存artifact規約がある場合はそれに従ってください。

---

## 9. 実装上の禁止事項

- 要件IDをtest名へ付けただけでCoveredにしない
- product codeをtestの期待値に合わせて無断で弱体化しない
- 失敗testをskip／xfailして完了扱いにしない
- mockだけでDB、Worker、Artifact、MLflow等の結合要件を証明しない
- SQLiteだけでPostgreSQL固有要件を証明しない
- 数値結果を固定文字列snapshotだけで検証しない
- 非決定的testをretryで隠さない
- 実装から期待結果をコピーし、同じバグを再実装しない
- 要件矛盾を推測で埋めない
- 既存CLI・ETL・Feature Buildの回帰テストを削除しない
- test用のbackdoorを本番codeへ追加しない
- 秘密情報、access token、実データをfixtureへ保存しない

---

## 10. Product Code変更の扱い

テスト追加により実装不備が判明した場合、次のルールに従ってください。

1. 要件が明確で、実装が不一致なら、最小限のproduct code修正を行う
2. 要件が曖昧なら、推測で実装せずGapとして報告する
3. 要件文書同士が矛盾するなら、`Blocked by Requirement Conflict`とする
4. 大規模refactorが必要なら、原因・影響範囲・分割案を示し、テストbasisを先に固定する
5. testを通すためだけの仕様変更をしない

product codeを変更した場合、Traceability Matrixと変更理由を更新してください。

---

## 11. 期待する成果物

1. 機能要件インベントリ
2. 既存テストインベントリ
3. 完成したTraceability Matrix
4. 要件ごとの受入条件
5. 不足分の自動テスト
6. PostgreSQL integration test
7. Worker／Outbox／lease／retry／cancel test
8. MVP Journey E2E test
9. scientific validation test
10. CLI後方互換test
11. requirement coverage report生成処理
12. CI更新
13. 必要な最小限のproduct code修正
14. test実行結果
15. 未解決Gap一覧

---

## 12. 完了条件

次をすべて満たした場合のみ完了としてください。

- 規範的な全機能要件がInventoryへ登録されている
- 各要件に明示的な受入条件がある
- 各要件がTest Caseへ対応付けられている
- `Covered`判定には実行可能な自動テストとassertion根拠がある
- `Partially Covered`と`Not Covered`が隠されていない
- MVP Journey E2Eが成功する
- Project境界、RBAC、冪等性、状態遷移、Outbox、Worker、lease、cancel、retryが検証される
- Dataset、Semantics、Discovery、Graph、Design、Inference、診断、lineageが一連で検証される
- PostgreSQL固有制約が実PostgreSQLで検証される
- 既存CLI、ETL、Feature Buildの後方互換要件が検証される
- scientific validationの期待値、seed、許容誤差が明示される
- requirement coverage reportが生成される
- CIが必要なsuiteを実行する
- 全失敗、skip、xfail、Blocked項目が理由付きで報告される

全要件がCoveredでない場合でも、結果を偽らず、完成したTraceability Matrixと実行結果を提出してください。未実装機能に対する失敗は、要件Gapとして明確化することに価値があります。

---

## 13. 最終報告形式

最終回答は次の順で出力してください。

1. 調査した規範文書と正本
2. 抽出した機能要件の概要
3. 既存テストの評価
4. 追加・変更したtest file一覧
5. 変更したproduct code一覧と理由
6. Traceability Matrixの集計
7. MVP E2E結果
8. PostgreSQL／Worker／CLI／scientific suiteの結果
9. 実行したcommandと終了code
10. Not Covered、Partially Covered、Blocked項目
11. 残存リスク

数値、件数、成功率は実際のreportから引用し、推測で補完しないでください。
