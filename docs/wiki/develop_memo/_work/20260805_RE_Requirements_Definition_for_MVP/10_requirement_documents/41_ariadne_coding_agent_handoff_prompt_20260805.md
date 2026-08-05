# Ariadne 初期価値検証版 — 実装移行継続プロンプト

以下の指示に従い、Ariadneコードベースの実装移行を継続し、初期価値検証版を完了させよ。

本プロンプトは、後続のコーディングエージェントが、既存コードを再調査するだけで終わらず、設計意図を維持したまま実装・テスト・切替まで進めるための引継ぎ指示である。

---

## 0. 任務

あなたの任務は、現在のコードベースに追加された新Product層の骨格を完成させ、次の状態へ到達させることである。

1. Phase 0〜3の未完了受入条件をすべて回収する
2. Phase 4の4 Workspace Web Appを実装する
3. 実在clientに必要な場合だけPhase 5のCompatibility Adapterを実装する
4. Phase 6のCutoverを成立させる
5. Phase 7でLegacy Control Planeを停止・廃止し、互換経路を縮退させる
6. 新Web App / API / Worker / Product DBだけでGolden Pathを完了できる状態にする

単なるレビュー、課題列挙、追加の計画書作成だけで終了してはならない。コード、migration、test、実行構成および必要な文書を実際に修正し、検証結果を残すこと。

---

## 1. 参照文書と優先順位

リポジトリルートを起点として、次の文書を参照すること。

```text
docs/wiki/develop_memo/_work/
  20260805_RE_Requirements_Definition_for_MVP/
    10_requirement_documents/
      00_プロダクトコンセプトメモ.md
      10_要件定義.md
      21_論理データ設計.md
      22_プロダクト基本設計.md
      23_API・インターフェース設計.md
      30_詳細設計.md
      40_実装移行計画.md
      91_migration_result.md
```

文書の優先順位は次のとおりとする。

1. `00_プロダクトコンセプトメモ.md`
2. `10_要件定義.md`
3. `21_論理データ設計.md`
4. `22_プロダクト基本設計.md`
5. `23_API・インターフェース設計.md`
6. `30_詳細設計.md`
7. `40_実装移行計画.md`
8. `91_migration_result.md`
9. 現在の実装コード

`91_migration_result.md`は実施者による進捗報告であり、設計上の完了証明ではない。上位文書、実コード、テスト結果と矛盾する場合は、上位文書と検証結果を優先すること。

実装時に設計文書の明白な欠落または矛盾を発見した場合は、暗黙に仕様を変更せず、最小限の設計判断を文書へ追記し、対応するContract Testを追加すること。

---

## 2. 元の改修計画

### 2.1 改修の基本方式

元の計画は、前身システム全体のインプレース改修でも、全コードの全面リライトでもない。

```text
Scientific Core
  = 前身コードの因果探索・因果推論資産を選択的に流用する

Product Domain / Metadata DB / API / Worker / Web App
  = 新しい境界で新規構築する

Backward Compatibility
  = 新システム外縁のCompatibility Adapterで提供する

Legacy Control Plane
  = 新規機能を追加せず、切替後に停止・廃止する
```

### 2.2 最優先事項

優先順位は次のとおりである。

1. 新システムの科学的・ドメイン的整合性
2. 新APIおよび新CLIの明確で自己完結した契約
3. 実在clientに必要な限定的後方互換性
4. 前身内部実装との類似性

後方互換の都合で、新Product Domain、DB schema、Scientific StatusまたはExecutionモデルを歪めてはならない。

### 2.3 DB移行方針

旧Metadata DB内のデータはすべて破棄してよい。次は実装しない。

- 旧DB record importer
- Legacy IDと新IDのmapping
- 過去Execution / Result / Artifact metadataの移行
- reverse migration
- 新旧DBへのdual-write
- Legacy tableを新APIのread sourceにする処理

新DBは空状態から独立したProduct baseline migrationだけで構築する。

### 2.4 新Product Domain

正本の業務Entityは次の7件だけである。

1. Project
2. Dataset Version
3. Execution
4. Result
5. Artifact
6. Graph Version
7. Annotation

次を初期版の独立Entityとして追加してはならない。

- Research Context
- Experiment
- Analysis Definition
- Execution Plan
- Comparison
- 汎用Lineage Relation
- Pipeline Definition
- Stage Execution
- Stage Attempt
- Claim Version
- Approval / Review workflow

ComparisonとLineageは、7 EntityとExecution Snapshotから要求時に生成するQuery Modelとする。

### 2.5 移行Phase

| Phase | 内容 | 元の完了条件 |
|---|---|---|
| 0 | Baselineと互換対象の固定 | Scientific挙動記録、client単位の互換候補、互換対象外の明示 |
| 1 | Scientific Core Adapter | DBなしでDiscovery / Estimation実行、数値差許容、Graph round trip |
| 2 | Product Domain・新DB | 空DB構築、FK/CHECK/UNIQUE Test、Legacy ORM非依存 |
| 3 | 新API・Worker・CLI | Dataset登録からResult保存、技術失敗と科学的負結果の分離、独立CLI |
| 4 | 4 Workspace Web App | E2E-01〜03を新Web Appだけで完了 |
| 5 | Compatibility Adapter | 承認済みC2契約だけを変換し、新Coreと分離 |
| 6 | Cutover | 新システムだけで新規登録・分析、Legacy DB runtime接続なし |
| 7 | Legacy廃止・互換縮退 | Legacy runtime停止、C2縮退、最終的なAdapter削除 |

---

## 3. 初期価値検証版の完成像

### 3.1 Golden Path

半人工の売上改善Datasetを使い、利用者が次を一連で実行できること。

1. Dataset Versionを登録する
2. PCを含む2種類以上のDiscoveryを実行する
3. PC parameter sensitivityを実行する
4. 3件以上のGraph Resultを比較する
5. Graph Versionを選定・必要に応じて修正し、`FIXED`にする
6. 二値TreatmentについてATEまたはATTのCausal Designを指定する
7. 2種類以上のEstimatorを実行する
8. 推定値、uncertainty、overlap、balance等のdiagnosticsを比較する
9. 採用・不採用理由、仮定、限界をAnnotationとして記録する
10. ResultからDataset、Graph、Execution条件、code version、Artifactへ遡る

### 3.2 4 Workspace

新Web Appは、少なくとも次の4 Workspaceを持つこと。

1. Project / Data
2. Discovery
3. Inference
4. Results / Lineage

初期版では既存の静的Frontend構成を置換してよい。新しい大規模Frontend frameworkへの移行は必須ではない。Golden Pathを最小構成で完了できることを優先する。

### 3.3 科学的状態と技術状態

Executionの技術statusとResultのscientific statusを混同してはならない。

Execution status:

- `QUEUED`
- `RUNNING`
- `SUCCEEDED`
- `FAILED`
- `CANCELLED`

Result scientific status:

- `VALID`
- `NOT_IDENTIFIED`
- `INSUFFICIENT_OVERLAP`
- `INSUFFICIENT_SAMPLE`
- `ESTIMATION_UNRELIABLE`

Scientific negative outcomeをResultとして保存できた場合、Executionは`SUCCEEDED`である。入力Artifact破損、依存library障害、DB障害、未分類例外等は技術失敗であり、Executionを`FAILED`にする。

---

## 4. 現在までに回収済みの実装

現時点で、次の骨格は追加済みである。

### 4.1 新規package

```text
src/ariadne/
├── product/
│   ├── domain/
│   ├── ports/
│   ├── application/
│   └── persistence/
├── interfaces/
│   ├── web_api/
│   ├── worker/
│   └── cli/
├── scientific/
└── adapters/
```

前身Control Planeの一部は`src/ariadne/legacy/`へ移動されている。

### 4.2 Product層

次は実装済みである。

- 7 Domain Entity
- Domain enum / error
- 7 Repository Port
- Unit of Work Port / SQLAlchemy実装
- Product ORM
- Project / Dataset / Execution / Graph Version / Annotation Service
- Comparison Query Service
- Lineage Query Service
- Local Artifact Store

### 4.3 Scientific境界

次は存在する。

- `ScientificCorePort`
- `ScientificCoreAdapter`
- `DiscoveryAdapter`
- `EstimationAdapter`

`product/`から`ariadne.causal.*`または`ariadne.legacy.*`への直接importは確認されていない。この依存方向は維持すること。

### 4.4 DB

次は存在する。

- `alembic_product.ini`
- `product_migrations/`
- `alembic_version_product`
- Product baseline revision `20260805_product_0001`

`91_migration_result.md`の残作業に「`alembic_product.ini`を作成」とあるが、このファイルは既に存在する。新規作成ではなく、実Migrationとして検証・修正すること。

### 4.5 API / Worker / CLI

次の骨格は存在する。

- FastAPI application
- Project / Dataset Version / Execution / Result / Graph Version / Annotation / Comparison / Lineage router
- SQL polling Worker
- `ariadne-discover`
- `ariadne-estimate`

ただし、現在のSmoke TestはProject作成、Dataset Version登録、Executionを`QUEUED`で作成するところまでであり、Worker実行、Result保存、Artifact保存、Scientific Status確認までは検証されていない。

---

## 5. 現在のPhase判定

| Phase | 現在の判定 | 理由 |
|---|---|---|
| Phase 0 | 未完了 | Characterization Test、互換性台帳、実在client/owner棚卸しがない |
| Phase 1 | 一部実装 | Port / Adapterはあるが、数値差、Graph round trip、科学的契約が未検証 |
| Phase 2 | 一部実装 | Entity / ORM / Repository / migrationファイルはあるが、DB受入Testがない |
| Phase 3 | 一部実装 | API / Worker / CLI骨格はあるが、Result保存までのComponent Testがない |
| Phase 4 | 未着手 | 既存FrontendはLegacy API契約のまま |
| Phase 5 | 未着手 | `interfaces/legacy_compat/`と互換性台帳がない |
| Phase 6 | 未着手 | Docker / Composeが新Product構成へ切り替わっていない |
| Phase 7 | 未着手 | Legacy API / Worker / Frontend / entrypointが残存している |

したがって、作業をPhase 4から開始してはならない。先にPhase 0〜3の未完了受入条件を閉じること。

---

## 6. 現在確認されている具体的な問題

以下は、現コードで既に確認されている問題である。再調査で解消済みと確認できない限り、必ず対応すること。

### 6.1 Test suiteが収集段階で失敗する

現状の確認結果:

```text
76 tests collected, 20 errors during collection
```

旧namespaceへの参照が残っている。

例:

- `ariadne.application`
- `ariadne.domain`
- `ariadne.interfaces.api`
- `ariadne.etl`

新Product層を検証するTestはほとんど存在しない。

**禁止:** 旧Testを通すためだけに、`ariadne.application`等の互換shimを新規作成してLegacy Control Planeを復活させないこと。

旧Control Plane専用Testは、次のいずれかへ明示的に分類すること。

- Scientific Characterization Testとして残す
- C2 Compatibility Contract Testとして残す
- Legacy archive用の非既定Testへ移す
- 廃止対象として削除する

既定の`pytest`は収集エラーなしで完走させること。

### 6.2 Scientific Statusが設計と不一致

`src/ariadne/product/domain/enums.py`には、設計にない次の値がある。

- `IDENTIFIED`
- `ESTIMATION_RELIABLE`
- `GRAPH_PRODUCED`
- `GRAPH_EMPTY`
- `SCIENTIFIC_ERROR`

一方、設計上必要な次の値がない。

- `VALID`
- `INSUFFICIENT_OVERLAP`
- `INSUFFICIENT_SAMPLE`

実装を設計契約へ合わせること。技術例外を`SCIENTIFIC_ERROR`というResultへ変換して隠してはならない。

### 6.3 Estimation Adapterが科学的に不適切

`src/ariadne/scientific/inference/adapter.py`は、存在しない`run_ate_estimation`をimportし、失敗時に`econml.DRLearner`へfallbackする。

fallbackには次の問題がある。

- estimator指定を実質的に無視する
- Graphを使用しない
- `analysis_spec.adjustment_set`を使用しない
- treatment / outcome以外の全列を共変量にする
- confidence intervalを返さない
- silent conversionになる

このfallbackは削除すること。

既存の次の資産を明示的にAdapterへ接続すること。

```text
src/ariadne/causal/inference/estimators/treatment_effect.py
src/ariadne/causal/inference/diagnostics/
src/ariadne/causal/design/schemas.py
```

最低限、次を実装すること。

- Difference in means
- OLS / Outcome regression
- IPW
- AIPWはSHOULD
- ATE / ATT
- `analysis_spec.adjustment_set`の厳密な使用
- estimate
- standard error
- confidence interval
- overlap / balance / sample-size等のdiagnostics
- warning
- scientific status判定

共変量を推測で補完してはならない。

### 6.4 Discovery Adapterの意味論が不足する

`src/ariadne/scientific/discovery/adapter.py`は、成功時に`GRAPH_PRODUCED` / `GRAPH_EMPTY`を返し、例外を`SCIENTIFIC_ERROR`へ変換している。

次を修正すること。

- PCとGESをMUSTとして実行可能にする
- feature columnsを尊重する
- 対応可能なgraph constraintsを明示的に適用する
- Graph typeを保持する
- endpoint semanticsを保持する
- Graph serialization round tripを成立させる
- 技術例外はtyped infrastructure errorとして上位へ伝播する
- 正常な空Graph等を扱う場合は、設計済みstatusとwarningで表現し、未定義enumを追加しない

### 6.5 Graph Versionのsource検証が不足する

`src/ariadne/product/application/graph_version_service.py`は、source Resultの存在しか確認していない。

次を保証すること。

- source Resultが同一Projectに属する
- source Resultが`DISCOVERY_GRAPH_RESULT`である
- source Executionのoperationが`DISCOVERY`である
- parent Graph Versionが同一Projectに属する
- Graph typeとgraph JSONのendpoint semanticsが整合する

### 6.6 DRAFT GraphをEstimationに使用できる

`src/ariadne/product/application/execution_service.py`は、Graph VersionのProject一致だけを確認している。

Estimation Executionには`FIXED` Graph Versionだけを許可すること。

### 6.7 AnnotationのProject境界が不足する

`src/ariadne/product/application/annotation_service.py`は、target Result / Graph Versionの存在およびProject一致を確認していない。

次を保証すること。

- targetは必ず存在する
- target ResultまたはGraph VersionはAnnotationと同一Projectに属する
- target XOR制約をDomain、Application、DBの適切な層で検証する

### 6.8 Execution Snapshotが不完全

現在のsnapshot hashには、設計上必要な情報の一部が不足する。

最低限、次をcanonical化し、submit後に不変とすること。

- objective / rationale
- Dataset Version IDとcontent hash
- Estimation時のGraph Version IDとcontent hash
- operation
- analysis specification
- algorithm / estimator
- parameters
- random seed
- code version
- runtime versions

JSON key順、数値表現、NULL表現を固定し、同一入力から同一hashを生成するTestを追加すること。

### 6.9 Worker claimがatomicではない

`SqlExecutionRepository.claim_next()`は`FOR UPDATE SKIP LOCKED`で取得するだけで、同じtransaction内に`RUNNING`更新を行っていない。

現在の流れでは、lockをcommitで解放した後、別transactionで`RUNNING`へ更新するため、複数Workerが同じExecutionを取得できる。

次を同一の短い専用transaction内で行うこと。

1. 次の`QUEUED`行を`FOR UPDATE SKIP LOCKED`で取得
2. `RUNNING`へ更新
3. `started_at`設定
4. worker token設定
5. commit

PostgreSQL上で複数Workerによる排他性Testを追加すること。

### 6.10 Workerの処理契約が未検証

Dataset登録からResult保存までをComponent Testで検証すること。

少なくとも次を確認する。

- Artifact取得時のcontent hash検証
- Estimation時のFIXED Graph取得
- Scientific Core呼出し
- Artifact Store保存
- ResultとArtifact metadataの同一DB transaction保存
- Executionの`SUCCEEDED`更新
- Scientific negative outcome時も`SUCCEEDED`
- technical exception時は`FAILED`
- cancel safe point
- Artifact保存後DB失敗時の最小限のorphan cleanup管理

### 6.11 Product baseline migrationが受入れ未完了

`ProductBase.metadata.create_all()`の成功は、Alembic baseline migrationの成功証明ではない。

PostgreSQLを正本の実行DBとし、次を検証すること。

```bash
alembic -c alembic_product.ini upgrade head
```

次をTestすること。

- 空DBからのbaseline migration
- `alembic_version_product`の独立性
- FK
- CHECK
- UNIQUE
- transaction rollback
- backup / restore
- Legacy schemaへのruntime接続なし

Production runtimeにSQLite fallbackを残して、PostgreSQL専用機能が動作するように見せかけてはならない。SQLiteをunit testで使う場合は、PostgreSQL Integration Testを必須とし、対応範囲を明示すること。

### 6.12 API契約が未完了

現在のAPIには、次が不足する。

- `/api/v1` major version prefix
- Dataset preview
- Execution prefill
- Result export
- Artifact metadata取得
- Artifact download
- 作成系Commandのidempotency
- 設計どおりのError Response envelope
- unknown field reject
- Project境界Contract Test

設計上の不足として、Web AppでProject選択に必要なProject一覧APIが文書に明示されていない。次のいずれかで解決すること。

- 最小の`GET /api/v1/projects`を追加し、`23_API・インターフェース設計.md`を更新する
- 同等のProject選択手段を設計へ明示する

未文書のAPIへFrontendを暗黙依存させてはならない。

Routerからprivateな`_uow_context`を直接呼ぶ暫定実装を除去し、Application Service / Query Serviceを介すこと。

### 6.13 CLI契約が未完了

新CLIはWeb/APIのExecution IDを生成してはならない。

次を保証すること。

- config validation
- Dataset / Graph hash
- analysis specとの意味的一致
- code / runtime version
- `manifest_version`
- scientific status
- Result summary
- Artifact一覧
- 設計済みexit code

Scientific negative outcomeはexit code 0とする。

### 6.14 Docker / ComposeがLegacy構成のまま

現在の`Dockerfile`と`compose.yaml`には、次の問題がある。

- Product migrationをimageへコピーしない
- `alembic`の旧migrationを実行する
- 存在しない`ariadne.interfaces.api.app`を起動する
- healthcheckが存在しない`/health/ready`を参照する
- FrontendがLegacy API契約を使用する

新Product runtimeへ全面的に切り替えること。

### 6.15 Legacy CLI aliasが壊れている

現在のentrypoint:

```text
ariadne-discovery
ariadne-inference
ariadne-pipeline
```

は、移動前のnamespaceを内部参照してimport時に失敗する。

互換性台帳に基づき、次のいずれかへ明示的に変更すること。

- C0: 削除する
- C1: 新CLIへのaliasとdeprecation案内だけを提供する
- C2: 実在client、owner、fixture、semantic mapping、期限が揃う場合だけAdapterを実装する

`ariadne-pipeline`は新Golden Pathに対応概念がないため、原則C0とする。

---

## 7. 必須の作業順序

以下のGate順で進めること。後段のGateを先に実装して、前段の不整合を隠してはならない。

---

## Gate A — Phase 0: Baseline・Test・互換対象を固定する

### 作業

1. 現在のcommit IDまたは入力アーカイブhashをBaselineとして記録する
2. 既存Testを次へ分類する
   - Active Product Test
   - Scientific Characterization Test
   - Compatibility Contract Test
   - Retired Legacy Control Plane Test
3. 既定`pytest`の収集エラーを解消する
4. Scientific Characterization Testを追加する
5. 互換性台帳を作成する

互換性台帳は、例えば次へ追加する。

```text
docs/wiki/develop_memo/_work/
  20260805_RE_Requirements_Definition_for_MVP/
    10_requirement_documents/
      41_互換性台帳.md
```

台帳には次を記録する。

- Compatibility ID
- Client / Owner
- Legacy contract
- New contract
- C0〜C3
- Semantic gap
- Test fixture
- Deprecation date
- Removal condition

実在clientまたはownerの根拠がない契約をC2にしてはならない。リポジトリ内に証拠がない場合、C2集合は空でよい。推測で互換範囲を拡大しないこと。

### Gate A完了条件

- `pytest --collect-only`が0 error
- Scientific Characterization Testが再現可能
- PC / GES、主要Estimator、Graph serialization、CLI manifest / exit codeのBaselineが記録される
- C2候補がclient単位で特定されるか、C2対象なしと明示される
- 互換対象外endpoint / commandが明示される

---

## Gate B — Phase 1: Scientific Core Adapterを完成させる

### 作業

1. Scientific Statusを設計契約へ統一する
2. Discovery AdapterをPC / GESのMUST要件へ接続する
3. Graph typeとendpoint semanticsを保存する
4. Estimation Adapterを既存`TreatmentEffectEstimator`へ接続する
5. adjustment set、estimand、treatment、outcomeを厳密に使用する
6. diagnosticsとwarningを共通Outputへ変換する
7. technical exceptionをtyped infrastructure errorとして扱う
8. Scientific CoreからDB、Repository、Web schema、Execution statusへの依存を禁止する

### Gate B完了条件

- DBなしでDiscovery / Estimationを実行できる
- PCとGESがsynthetic dataで動作する
- Difference in means、OLS、IPWのうち2種類以上を同一Causal Designで比較できる
- Estimatorごとの数値許容差がTestで定義される
- Graph serializationがround tripする
- `NOT_IDENTIFIED`、`INSUFFICIENT_OVERLAP`、`INSUFFICIENT_SAMPLE`、`ESTIMATION_UNRELIABLE`を技術失敗と分離できる
- silent defaultまたは全列自動調整がない

---

## Gate C — Phase 2: Product Domain・Persistenceを完成させる

### 作業

1. 7 Entityの状態遷移と不変条件をUnit Testする
2. Project境界をApplication validationまたはDB制約で保証する
3. Estimationには`FIXED` Graphだけを許可する
4. source Discovery Resultの整合性を検証する
5. canonical Execution Snapshotを実装する
6. Product baseline migrationをPostgreSQLで成立させる
7. FK / CHECK / UNIQUE / rollback Testを追加する
8. Comparison分類とLineage traversalをTestする
9. Product ApplicationがLegacy ORMをimportしないArchitecture Testを追加する

### Gate C完了条件

- 空PostgreSQL DBからProduct baselineだけで構築できる
- 7 Entityと技術用補助tableだけが新Product schemaに存在する
- FK / CHECK / UNIQUE Testが成功する
- Project外参照が拒否される
- FIXED Graphの上書きとDRAFT Graphの推論利用が拒否される
- Legacy ORMなしでApplication Testが成功する

Idempotency等の技術用tableは追加してよいが、業務Entityとして公開してはならない。

---

## Gate D — Phase 3: Workerを完成させる

### 作業

1. claimをatomicにする
2. 複数Worker排他性TestをPostgreSQLで作る
3. Artifact hashを検証する
4. Worker Result保存transactionを設計どおりにする
5. technical failureとscientific negative outcomeを分離する
6. cancel / retry規則を実装・Testする
7. Dataset登録からResult保存までComponent Testを作る

### Gate D完了条件

- 1 Executionを複数Workerが重複実行しない
- Dataset Version登録からWorker実行、Result / Artifact保存まで自動Testが通る
- Scientific negative outcomeはResult保存 + Execution `SUCCEEDED`
- technical exceptionはExecution `FAILED`
- retry時にSnapshotが変化しない
- Result、Artifact metadata、Execution statusのDB整合性が維持される

---

## Gate E — Phase 3: Web API・CLIを完成させる

### Web API作業

1. `/api/v1`へ統一する
2. `23_API・インターフェース設計.md`のEndpointを実装する
3. Dataset previewを実装する
4. Execution prefillを実装する
5. Result exportを実装する
6. Artifact metadata / downloadを実装する
7. Idempotencyを実装する
8. Error envelopeを設計へ合わせる
9. Pydantic unknown field rejectを有効にする
10. Project境界、Graph固定、idempotency、error codeのContract Testを追加する

### CLI作業

1. Discovery / InferenceをScientific Core Adapter経由に統一する
2. Web/APIのExecutionを作成しない
3. Manifestを設計契約へ合わせる
4. config validationとhash検証を実装する
5. exit codeを設計へ合わせる

### Gate E完了条件

- API Contract Testが成功する
- 新APIだけでGolden Pathに必要な全操作が可能
- 作成系再送で重複Resourceが作られない
- CLIがDBおよびWeb APIなしで実行できる
- CLI Manifestから入力・設定・code version・Result・Artifactを復元できる

---

## Gate F — Phase 4: 4 Workspace Web Appを実装する

既存FrontendをLegacy APIへつなぎ直して延命してはならない。新API契約へ置換すること。

### Project / Data Workspace

- Project作成・選択・更新
- Dataset Version登録
- Dataset一覧
- preview
- schema / row / column / hash表示

### Discovery Workspace

- Dataset Version選択
- PC / GES等のAlgorithm選択
- parameter grid
- 複数Execution受付
- status表示
- 3件以上のGraph Result比較
- Graph差分
- Graph Version作成・編集・固定
- 選定理由Annotation

### Inference Workspace

- Dataset Version選択
- FIXED Graph Version選択
- treatment / outcome
- ATE / ATT
- adjustment set
- assumptions
- 複数Estimator選択
- preflight表示
- 複数Execution受付
- estimate / uncertainty / diagnostics比較

### Results / Lineage Workspace

- Result詳細
- scientific status
- warnings
- diagnostics
- Artifact一覧とdownload
- Annotation
- Dataset / Graph / Execution / Result / ArtifactのLineage

### Gate F完了条件

- E2E-01〜03を新Web Appだけで完了できる
- Legacy FrontendまたはLegacy APIを参照しない
- JSON直接編集なしでMUST条件を入力できる
- ComparisonとLineageを視覚的に確認できる

---

## Gate G — Phase 5: Compatibility Adapterを実装する

### 原則

`interfaces/legacy_compat/`配下だけに置くこと。

```text
Legacy Client
  → Compatibility Adapter
  → New Product Application Service
  → Compatibility Response Translator
```

Adapterは次を独自実装してはならない。

- business logic
- Scientific Core呼出し
- Repository
- transaction
- Legacy DB access

### 作業

1. 互換性台帳でC2と承認された契約だけを実装する
2. Request / Response / status mappingを明示する
3. 変換不能なfieldをerrorにする
4. scientific statusの欠落を禁止する
5. Deprecation / Sunset情報を返す
6. Compatibility Contract Testを作る

実在client根拠がなくC2集合が空の場合、Phase 5は「C2実装なし、C0/C1のみ」として完了してよい。その場合も、壊れたLegacy entrypointは残さないこと。

### Gate G完了条件

- Adapterを無効にしても新Web App / API / Worker / CLIが完全に動く
- Legacy固有fieldが新Domain / DBに存在しない
- semantic gapが文書とTestに残る
- C2対象が存在する場合は実在client fixtureでContract Testが通る

---

## Gate H — Phase 6: Cutoverを成立させる

### 作業

1. `Dockerfile`をProduct runtimeへ修正する
2. `alembic_product.ini`と`product_migrations/`をimageへ含める
3. Compose migrateをProduct baselineへ変更する
4. API起動moduleを`ariadne.interfaces.web_api.app`へ変更する
5. healthcheckを実Endpointへ合わせる
6. WorkerをProduct DBへ接続する
7. Frontendを新APIへ接続する
8. Legacy DBへのruntime接続を除去する
9. backup / restore Testを行う
10. Golden Path smoke testを行う
11. rollback smoke testを行う

### Gate H完了条件

- `docker compose up --build`でProduct DB、migration、API、Worker、Frontendが起動する
- 新システムだけでDataset登録から分析まで完了する
- Legacy DB tableへのSQLがない
- 新DBのbackup / restore後にGolden Path smoke testが成功する
- Compatibility障害時に新API / Web Appを停止せず互換経路だけ停止できる

---

## Gate I — Phase 7: Legacyを廃止する

### 作業

1. Legacy APIを停止・削除する
2. Legacy Workerを停止・削除する
3. Legacy Frontendを置換・削除する
4. Legacy DB migrationとruntime接続を削除する
5. 旧Control Plane codeをarchiveまたは削除する
6. Legacy CLI aliasを互換性台帳に従ってC2→C1→C0へ縮退する
7. Compatibility Adapterの削除条件を明示する

Scientific Coreとして選択的に流用した`ariadne.causal.*`等は、Legacy Control Planeとは別物である。Scientific Adapter経由の依存は残してよい。

### Gate I完了条件

- Legacy runtime dependencyがScientific Adapter経由の再利用資産だけになる
- Legacy API / Frontend / Worker / DBが起動構成に存在しない
- 互換性台帳の各項目がC0、削除済み、または期限付きC1である
- 新Domain / DBにLegacy互換専用属性がない

---

## 8. Architecture Testで固定する依存規則

最低限、次を自動Testすること。

```text
product
  -X-> legacy
  -X-> legacy_compat
  -X-> Legacy ORM

product.application
  -X-> Legacy Router
  -X-> Legacy Worker
  -X-> Legacy DB client

scientific / scientific_adapter
  -X-> Product Repository
  -X-> Web API schema
  -X-> ORM

interfaces.web_api
  -X-> Legacy DB

legacy_compat
  -X-> 独自Repository実装
  -X-> Scientific Core直接呼出し
```

Runtime importだけでなく、ASTまたはimport graphを使って静的に検証すること。

---

## 9. 過剰設計を避けるための禁止事項

次を実装してはならない。

- 旧DBデータ移行
- dual-write
- Legacy IDの恒久保存
- Pipeline / Stage / Attemptの復活
- Comparison Entity
- 汎用Lineage Relation Entity
- Research Contextの独立Resource
- Experiment Workspace
- 詳細RBAC
- 承認workflow
- CATE / HTE
- 連続Treatment
- IV / DiD / RDD / Synthetic Control
- 複数Artifact Store abstractionの先行実装
- Cloud SDKをScientific Coreの必須依存にすること
- 実在client不明のC2互換
- 未知parameterのsilent ignore
- estimator / adjustment setの推測補完
- 旧Testを通すためだけのLegacy namespace shim
- Frontend framework刷新そのものを目的にした改修

必要性がGolden PathまたはMUST要件から直接説明できない機能は追加しないこと。

---

## 10. 必須Test構成

少なくとも次のTest群を用意すること。

### Unit Test

- Entity状態遷移
- Analysis Spec validation
- canonical snapshot hash
- Graph semantics validation
- Comparison分類
- Lineage traversal
- Domain Error

### Repository Integration Test

- Product baseline migration
- FK / CHECK / UNIQUE
- transaction rollback
- Project境界
- Result + Artifact metadata + Execution statusの同時保存
- Execution claim排他性

### Scientific Regression / Differential Test

- PC / GES synthetic data
- Graph type / endpoint semantics
- Graph serialization round trip
- Difference in means / OLS / IPW / AIPWの数値許容差
- overlap / sample-size等のScientific Status
- warning

### API Contract Test

- `/api/v1`
- Request / Response schema
- unknown field reject
- Error envelope / error code
- Project境界
- Idempotency
- Graph FIXED後の更新拒否
- Artifact download
- Result export

### Compatibility Contract Test

C2対象がある場合だけ実施する。

- field mapping
- validation error
- status mapping
- idempotency
- scientific status欠落防止
- deprecation header
- New Application Serviceと同一side effect

### E2E Test

1. Dataset Version登録
2. PC / GES等の複数Discovery
3. Graph比較
4. Graph Version固定
5. 複数Estimator
6. Result / diagnostics比較
7. Annotation
8. Lineage
9. Artifact download / export

---

## 11. 実行・検証コマンド

プロジェクト標準の`uv`を優先して使用すること。最終的に、少なくとも次に相当する検証を実行する。

```bash
uv sync --frozen
uv run pytest -q --collect-only
uv run pytest -q
```

PostgreSQL Integration Test:

```bash
docker compose up -d database
ARIADNE_PRODUCT_DATABASE_URL='postgresql+psycopg://...' \
  uv run alembic -c alembic_product.ini upgrade head
```

全体起動:

```bash
docker compose down -v
docker compose up --build -d
docker compose ps
```

Architecture確認例:

```bash
rg -n 'ariadne\.legacy|ariadne\.domain|ariadne\.application|ariadne\.interfaces\.api' \
  src/ariadne/product src/ariadne/interfaces/web_api src/ariadne/scientific
```

上記`rg`は補助確認であり、最終的にはArchitecture Testを正本とする。

Golden Pathは自動E2E Testまたは完全に再現可能なscriptとして保存すること。

---

## 12. 最終完了条件

以下をすべて満たした場合だけ、実装移行完了と報告すること。

1. 新Web App / API / Worker / Product DBだけでGolden Pathが完了する
2. Scientific CoreはPort / Adapter境界を介して呼び出される
3. Product DomainがLegacy ORM、Router、Worker、DBへ依存しない
4. 正本業務Entityが7件に限定される
5. 空PostgreSQL DBから独立Product baselineで再構築できる
6. 旧DBデータ移行コードが存在しない
7. C2互換が互換性台帳に登録された契約だけに限定される
8. Compatibility Adapterなしでも新システムが完全に動作する
9. Legacy固有属性が新Domain / DBに存在しない
10. Legacy API、Frontend、Worker、DBが起動構成から除去される
11. Scientific Regression、API Contract、DB、Architecture、E2E Testが成功する
12. C2対象がある場合、Compatibility Contract Testが成功する
13. Compatibility Adapterに廃止期限と削除条件がある
14. `pytest`が収集エラーなしで全件成功する
15. `docker compose up --build`で再現可能に起動する
16. backup / restore後にGolden Path smoke testが成功する
17. Executionの重複claimが発生しない
18. Scientific negative outcomeとtechnical failureが分離される
19. ResultからDataset、Graph、Execution条件、Artifactへ遡れる
20. 4 WorkspaceでE2E-01〜03を完了できる

一つでも未達の場合は、「完了」と記載せず、未達Gate、原因、再現コマンド、残作業を明示すること。

---

## 13. 文書更新

作業完了時に、少なくとも次を更新すること。

1. `91_migration_result.md`
   - Phase 0〜3の未完了作業とPhase 4以降を分離する
   - 実際に実行したcommandと結果を書く
   - `create_all()`とAlembic migrationを混同しない
   - Smoke Testの到達点を正確に書く
2. `41_互換性台帳.md`
3. API契約を変更した場合は`23_API・インターフェース設計.md`
4. 実装上の最小判断を追加した場合は対応する設計文書

数値、test件数、成功結果を推測で記載してはならない。実行ログから得た事実だけを書くこと。

---

## 14. 最終報告形式

最終応答または最終レポートは、次の順で記載すること。

```text
# 実装結果

## 1. 結論
- 完了 / 未完了
- 到達したGate

## 2. Phase別状態
- Phase 0〜7

## 3. 主な変更
- code
- migration
- API
- Worker
- Web App
- Compatibility
- Legacy retirement

## 4. Test結果
- command
- pass / fail / skip件数
- PostgreSQL Integration
- E2E
- Architecture

## 5. 設計との差分
- 意図的な最小変更だけを記載

## 6. 残課題
- 未達がある場合のみ
- 再現手順とblocker
```

「ファイルを追加した」「moduleをimportできた」だけを完了根拠にしてはならない。各Gateの受入条件と実行Testを根拠に判定すること。

---

## 15. 作業上の判断規則

- 軽微な実装詳細は、上位文書の意味を変えない範囲で合理的に決定してよい
- 実在client情報が不足する場合、C2を推測実装せずC0/C1とする
- 将来機能のための抽象化を先行実装しない
- 既存Scientific資産はCharacterization Testで挙動を固定してから変更する
- 不具合修正と同時に、再発防止Testを追加する
- 設計と実装が衝突する場合、実装を設計へ合わせることを原則とする
- 設計変更が不可避な場合は、変更理由、代替案、影響範囲を文書化する
- 完了条件を満たすまで、`91_migration_result.md`の「実施済み」という表現を根拠に作業を省略しない

以上。
