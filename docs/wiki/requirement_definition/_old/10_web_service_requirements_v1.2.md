# ariadne Webサービス化 要件定義書

- 文書版: 1.2
- 基準リポジトリ: `kousuke-ota-datascience/ariadne`
- 基準ブランチ: `main`
- 初版調査日: 2026-07-18
- 改訂日: 2026-07-20
- 対象: MVPおよびMVP後の拡張

### 改訂履歴

| 版 | 日付 | 変更内容 |
|---|---|---|
| 1.0 | 2026-07-18 | `ariadne` の当時の実装に合わせて全面改訂 |
| 1.1 | 2026-07-19 | ETL変換済みデータのprofile、集計、入力前後比較、保存済み可視化、export、権限制御を追加 |
| 1.2 | 2026-07-20 | MVPの価値をAnalysis-ready Datasetから因果探索・グラフ選択・因果推論までの接続と来歴管理に再定義。ETL、複数table登録、汎用BI可視化をWeb MVP主導線から除外し、単一table入力、Feature Semantics、保存済みCausal Graph Version、Causal Design、結果診断を中心に要件を再編。既存CLI、Complete Journey ETL、既存Feature Buildは後方互換を維持することを明文化 |

---

## 1. 文書の目的

本書は、Pythonパッケージとして実装されている `ariadne` を、Analysis-ready Datasetの登録、変数の意味付け、因果探索、探索結果の比較・選択、因果設計、因果推論、診断、再現性情報の管理を備えたWebサービスへ発展させるための要件を定義する。

本版では、MVPが証明すべき価値を次のように定める。

> 分析用に整備されたDataset Versionを入力すると、変数の意味付け、複数アルゴリズムによる因果探索、グラフ比較・選択、因果設計、因果推論、診断、来歴確認までを、一つのProject内で再現可能に実行できる。

本書の要件は次を原則とする。

1. ariadneは、汎用ETL基盤やData Warehouseの代替を目指さない。
2. データ収集、join、集計、Feature生成等の重いデータ整備は、Databricks等の外部データ基盤または既存パイプラインへ委譲可能とする。
3. MVPでは、1行が分析単位を表す単一のAnalysis-ready Tableを標準入力とする。
4. 因果探索・因果推論の数値実装をWeb層へ移植しない。
5. CLIを廃止せず、Web APIとCLIを同一Application Serviceへの別Adapterとして共存させる。
6. Dataset、Configuration、Run、Graph、Result、Artifactを不変versionまたは不変snapshotで結び付ける。
7. 因果探索結果を真のDAG、edge weightを識別済み因果効果として表示しない。
8. 因果的妥当性を自動保証するサービスとは位置付けず、分析者の判断、宣言した仮定、診断結果を明示する。
9. 新しいAnalysis-ready実行経路は、既存CLI・ETL・Feature Build経路を置換せず、追加経路として実装する。

### 1.1. v1.1からの優先順位変更

v1.1でMVP対象としていた次の機能は、本版ではMVPの主導線から外す。

- Complete Journey固有ETL
- 複数table Datasetのブラウザからの一括登録
- ETL入力前後比較
- 汎用group-by可視化およびBI dashboard相当の機能
- Visualization Specificationの高度な管理

ここでいう「MVPの主導線から外す」とは、通常のWeb画面で利用者へ明示的な操作を要求せず、Web MVPの成功判定に含めないという意味である。既存API、CLI、ETL class、Feature Build class、Configuration、回帰テストを削除または非互換変更してよいという意味ではない。

本MVPの実装変更において、既存CLI、Complete Journey ETL、既存Discovery/Inference Feature Buildは維持必須とする。新しいAnalysis-ready modeは、それらと併存すること。

### 1.2. 規範用語

本書では次の意味で用語を使用する。

| 表現 | 意味 |
|---|---|
| 「すること」「してはならない」 | MVP必須要件 |
| 「してよい」「可能とする」 | 許容またはoptional要件 |
| 「MVP対象外」 | Web MVPの新規実装・受入判定の対象外。既存コードの削除指示ではない |
| 「Web主導線から外す」 | 通常UIに操作stepを設けない。API、worker、CLI、classを廃止する意味ではない |
| 「維持する」 | public CLI、既存API契約、import可能なclass、既存testを非互換にしない |

要件間で解釈が競合する場合、既存CLI・ETL・Feature Buildの後方互換要件を優先する。

### 1.3. 本書における「前処理」の分類

「前処理」という語を一括して扱わず、次の3種類を区別する。

| 区分 | 例 | v1.2での扱い |
|---|---|---|
| A. Domain ETL / Feature Build | RDA/RDS読込、複数table join、campaign集計、household単位Feature生成 | 既存classとCLIを維持する。通常Web UIでは利用者へ明示操作させない |
| B. Algorithm Input Conditioning | 列選択、dtype検証、欠損値policy、categorical encoding、標準化、constant列除外、collinearity check | Discovery/Inferenceの内部処理として引き続き実行し、設定と結果を記録する |
| C. Web Orchestration | Dataset Version、Semantics、Run、Graph、Designの選択・来歴管理 | v1.2 Web MVPの中心機能とする |

Analysis-ready Datasetとは、AのDomain ETL / Feature Buildが完了しているDatasetを指す。BのAlgorithm Input Conditioningまで不要であることを意味しない。

### 1.4. 併存する2つの実行経路

実装は次の2経路を明示的に区別する。

#### CONFIGURED_FEATURE_BUILD経路

- 現行CLI、Complete Journey、既存Feature Configurationが使用する。
- Dataset Registry、既存Feature Build、既存preprocessing classを使用する。
- 本書の対応で削除、無効化、暗黙にAnalysis-ready modeへ変更してはならない。
- 既存CLI invocationでmode指定がない場合、従来と同じ挙動を維持する。

#### ANALYSIS_READY経路

- v1.2の通常Web UIが使用する新しい経路である。
- 単一のAnalysis-ready TableとFeature Semanticsを直接入力する。
- Domain固有join・集計・Feature Buildは実行しない。
- Algorithm Input Conditioningは明示設定に基づいて実行する。

Application層またはExecution Planで解決済み`input_mode`を保持すること。名称は実装設計で変更してよいが、2経路をtable数やfilenameから暗黙推測してはならない。Run、Execution Plan、Manifestには解決済みmodeを記録すること。

---

## 2. プロダクト仮説と責務境界

### 2.1. プロダクト仮説

因果分析では、次の情報がNotebook、YAML、CSV、画像、実行ログへ分散しやすい。

- 使用したデータのsnapshot
- 変数の意味と時点
- 因果探索アルゴリズムと設定
- アルゴリズムごとの探索結果
- 推論に採用したグラフ
- treatment、outcome、estimand
- adjustment setと因果仮定
- 推定方法、推定値、診断、警告

ariadneは、これらを一つの分析来歴として結び付けることで、次の価値を提供する。

1. 因果探索と因果推論の間の手作業を減らす。
2. 複数アルゴリズムの相違を確認した上で、推論に使うグラフを明示的に選択できる。
3. 推定値からDataset Version、Graph Version、Causal Design、仮定、診断へ遡れる。
4. 同じ入力と設定による再実行、レビュー、結果説明を容易にする。
5. 探索結果と因果効果を混同する科学的な誤表示を防ぐ。

### 2.2. 外部データ基盤との責務分担

```text
Databricks等の外部データ基盤
  - データ収集
  - クレンジング
  - join・集計
  - Feature生成
  - 品質管理
  - 大規模分散処理
                |
                v
Analysis-ready Dataset / immutable snapshot
                |
                v
ariadne
  - Dataset Versionの登録・参照固定
  - 変数の意味付け
  - 因果探索
  - アルゴリズム比較
  - 推論用グラフの選択・保存
  - 因果設計
  - 因果推論
  - 診断・結果表示
  - 分析来歴
```

ariadneは、入力データを必ず物理コピーすることを将来要件としない。外部Datasetの不変snapshotを一意に参照でき、実行時に権限付きでmaterializeまたはqueryできればよい。

ただしMVPでは、外部システム連携そのものではなく、CSVまたはParquet uploadによって上記の分析価値を検証してよい。

### 2.3. MVPで証明する価値

MVPは、少なくとも次の3点を利用者が完遂できることで価値を証明する。

#### V-001 DiscoveryとInferenceの接続

Discovery Runで生成された探索結果から、利用者が推論に使用するGraph Versionを選択し、そのGraph VersionをInference Runの入力にできる。

#### V-002 Algorithm比較による判断支援

同じDataset Versionに複数の探索アルゴリズムを適用し、共通edge、相違edge、orientation、score、stability、warningを比較できる。

#### V-003 結果の根拠と来歴

推定値だけでなく、Dataset Version、Feature Semantics、Discovery Run、Graph Version、Causal Design、adjustment set、仮定、診断へ遡れる。

### 2.4. 非目的

- 汎用ETL、ELTまたはData Integration製品の代替
- Databricks JobやNotebookの作成・スケジューリング
- Data Warehouse、LakehouseまたはFeature Storeの代替
- 任意SQLを実行するBIサービス
- 因果識別の自動証明
- 因果探索結果の真実性保証
- 完全自動の調整集合決定
- 任意コードを無制限に実行するNotebook SaaS
- 保存済みモデルのonline serving
- リアルタイムstreaming推論
- 業務施策の自動実行

---

## 3. 現行実装の把握とMVP Gap

### 3.1. 現行の主要責務

| 領域 | 現行責務 |
|---|---|
| `application` | 実行計画、Run管理、validation、stage実行契約 |
| `causal.discovery` | PC、GES、LiNGAM、NOTEARS、graph正規化、診断、reporting |
| `causal.inference` | edge weight、treatment effect、診断、reporting |
| `causal.design` | Causal Design schema |
| `etl` | Complete Journey固有ETLとDataset Registry loader |
| `preprocessing` | Complete Journeyを中心としたdiscovery/inference特徴量構築 |
| `interfaces.api` | Project、Dataset、Configuration、Run、Result、Artifact等のHTTP API |
| `interfaces.cli` | discovery、inference、統合pipelineのCLI |
| `workers` | 非同期Run、Artifact materialization、結果projection |

### 3.2. 再利用する現行機能

- ProjectとProject RBAC
- Dataset、Dataset Version、Dataset Table Version
- Object upload
- Table previewとprofile
- ConfigurationとConfiguration Version
- Feature SemanticsおよびCausal Designのvalidation基盤
- Run、Stage Run、Attempt、Event
- Discovery、Edge Weight、Treatment Effectの結果projection
- Artifact、Manifest、lineage
- dry-run、validate-only、run
- workerとlocal/S3/Azure Blob Artifact Store Adapter

### 3.3. 現行実装と新MVPのGap

| Gap | 内容 | MVP対応 |
|---|---|---|
| 単一table汎用Discovery | 現行DiscoveryはComplete Journey向けFeature Configurationへの依存が強い | 既存経路を維持した上で、Analysis-ready Tableを直接入力する追加modeを実装する |
| 単一table汎用Inference | 現行InferenceもComplete Journey向けFeature BuildとDataset Registryへの依存がある | 既存経路を維持した上で、Analysis-ready TableとFeature Semanticsを直接入力する追加modeを実装する |
| Dataset Version検索 | Dataset一覧はあるがVersion一覧APIがない | Dataset単位・Project単位のVersion一覧を追加する |
| Result導線 | RunからResult IDを直接取得しにくい | RunごとのResult一覧またはRun詳細へのResult参照を追加する |
| Graph永続化 | 探索edge Artifactはあるが、分析者が採用したGraph Version resourceがない | Saved Causal Graphと不変Graph Versionを追加する |
| Variable Semantics UI | Configuration APIはあるが、列役割を設定する一般利用者向けUIがない | Dataset列からFeature Semantics Versionを作成するUIを追加する |
| Generic Causal Design UI | YAML/ID入力中心である | treatment、outcome、estimand、adjustment set、assumptionをformで作成可能にする |
| 外部Dataset参照 | LOCAL/S3/Azure objectは扱えるがDatabricks Table契約はない | MVP後にExternal Dataset Reference Adapterを追加する |
| Browser保存 | 現状Frontendの保存グラフはlocalStorageに依存する | 正本をMetadata DatabaseとArtifact Storeへ移す |

### 3.4. Complete Journey実装の位置付け

Complete Journey ETL、8 table Registry、既存feature builderは、回帰テスト、デモデータ生成、CLI利用のために維持すること。v1.2対応を理由に削除、名称変更、引数変更、既定動作変更を行ってはならない。変更が必要な場合は、既存呼出しを維持する互換Adapterまたはdefaultを設けること。

ただし、新しい通常Web UIの標準入力は次のような単一tableである。

```text
household_key
treated
outcome_sales_value
pre_sales_value
pre_visit_count
coupon_redemption_count
age_group
income_group
...
```

Complete Journeyの複数raw tableをブラウザで登録・joinすることはWeb MVPの受入条件に含めない。これは、CLIまたはworkerで同処理を実行できなくしてよいという意味ではない。

---

## 4. 対象利用者

| Actor | 主な責務 |
|---|---|
| Viewer | Dataset概要、Run、Graph、結果、診断、レポート、来歴を閲覧する |
| Analyst | Datasetを登録し、Feature Semantics、Discovery、Graph、Causal Design、Inferenceを作成・実行する |
| Maintainer | Algorithm、runtime、worker、Artifact、外部接続Adapterを管理する |
| Project Admin | Project member、権限、column policy、retentionを管理する |
| System Admin | システム全体、tenant、監査、障害を管理する |

### 4.1. MVPの主利用者

MVPの主利用者は、分析用tableを準備でき、因果探索と因果推論の基本概念を理解するAnalystとする。

システムは専門用語を隠蔽しすぎず、次の判断をAnalystに求める。

- どのDataset Versionを用いるか。
- どの列を分析対象とするか。
- 各変数をどの役割・時点として扱うか。
- どの探索結果を推論の仮説として採用するか。
- どのestimand、adjustment set、assumptionを用いるか。
- 診断と警告を踏まえて結果を採用できるか。

---

## 5. 対象範囲

### 5.1. MVP必須範囲

- Project詳細画面
- Analysis-ready Datasetの単一CSV/Parquet upload
- Datasetと不変Dataset Versionの登録
- Dataset Version一覧と選択
- 単一tableのschema、preview、profile表示
- Dataset列のFeature Semantics設定
- Feature Semantics Versionのvalidation、publish
- Analysis-ready Tableを直接利用するDiscovery Run
- Analysis-ready Tableを直接利用するEdge Weight / Treatment Effect Inference Run
- PC、GES、DirectLiNGAMの選択実行
- algorithm別Discovery graph表示
- algorithm間のedge比較
- 推論に使用する探索graphの選択
- Saved Causal Graphおよび不変Graph Versionの永続化
- Causal Design作成、validation、publish
- Edge Weight Inference
- Treatment Effect Inference
- 推定値、信頼区間、adjustment set、assumption、diagnostic、warningの表示
- DatasetからInference Resultまでのlineage
- Run状態、event、retry、cancel
- Project単位認可と監査

### 5.2. MVPで許容する簡略化

- 入力は1 Dataset Versionにつき1 tableを標準とする。
- 物理入力はCSVまたはParquet uploadでよい。
- Databricks接続はmockまたは設計上のportに留めてよい。
- Graphの手動edge編集は行わず、algorithm結果の選択保存のみでよい。
- Background KnowledgeはConfiguration入力によって扱い、視覚的editorは必須としない。
- 高度な感度分析は既存実装の範囲に限定してよい。
- Project内の同時利用者数、Dataset sizeにはMVP用の上限を設けてよい。

### 5.3. Web MVPの新規UI・受入判定対象外

- 複数ファイルの一括uploadとlogical table mapping UI
- Complete Journey ETLのWeb主導線
- 汎用join、aggregate、window処理
- ETL pipeline editor
- ETL入力前後比較
- 汎用BI chart builder
- Visualization Specificationの高度な共有・dashboard化
- Databricks Jobの実行・監視
- 任意SQL
- 任意Python script upload
- Graphの自由編集、edge approval workflow
- CATE、ITE、uplift
- Effect Model scoring/serving
- schedule、event-triggered Run
- 任意DAG pipeline editor

この一覧は既存実装の削除一覧ではない。該当する既存CLI、API、worker、class、test fixtureは、7.17節の後方互換要件に従って維持すること。

### 5.4. MVP後の拡張

- Databricks Unity Catalog / Delta Table Version連携
- S3、Azure Blob上のAnalysis-ready Dataset参照
- 複数Dataset Versionまたは複数table入力
- Graphの手動編集、変更理由、review/approval
- CATE、ITE、uplift
- notebook連携
- MLflow等の外部tracking adapter
- custom algorithm plugin
- Kubernetes Job等の分離実行backend
- 高度な感度分析
- 定期実行と通知
- drift検知

---

## 6. システム構成要件

### 6.1. 論理構成

```text
Browser
  |
Web Frontend
  |
Control Plane API (FastAPI)
  |-- Metadata Database (PostgreSQL)
  |-- Artifact Store Adapter
  |-- Dataset Source Adapter
  |-- Job Queue / Transactional Outbox
  |-- Authentication / Authorization
  |
Worker
  |-- ariadne.application
  |-- ariadne.causal
  |-- Generic Analysis-ready Table Adapter
  |-- Local work directory
  |-- Artifact Store
```

### 6.2. Control Plane

Control Planeは次を担う。

- Project、Dataset、Configuration、Graph、Run等のResource管理
- 不変version管理
- Run受付とExecution Plan生成
- validation要求
- Run状態管理
- 認証・認可
- Artifact metadataとlineage
- UI向け検索・一覧API
- 監査

Control Planeは、因果探索・因果推論の重い数値計算をHTTP request内で行わない。

### 6.3. Execution Plane

Execution Planeは次を担う。

- workerによるRun validation
- Dataset、Configuration、Graphのworkspaceへのmaterialization
- Generic Analysis-ready Tableの読込
- DiscoveryおよびInference Stage Runnerの実行
- Artifact upload
- Result projection
- Manifest生成
- progress/event発行

### 6.4. Dataset Source Adapter

Datasetの登録元とworkerの読込方法を分離するため、Dataset Source Adapterを設ける。

MVP必須Adapter:

- Uploaded Object Adapter

MVP後Adapter:

- Databricks Delta Table Adapter
- S3 Object Adapter
- Azure Blob Adapter

Dataset Source Adapterは、少なくとも次の契約を持つ。

- snapshot identifierを解決する。
- schemaを取得する。
- 実行可能な形式へmaterializeまたはqueryする。
- source credentialをMetadataへ平文保存しない。
- 実行時に参照したsnapshotをManifestへ記録する。

### 6.5. Modular Monolith優先

初期段階では、Dataset、Discovery、Graph、Inferenceを別々のHTTP microserviceへ分割しない。ただしAPI processと重い分析workerは物理的に分離する。

---

## 7. 機能要件

## 7.1. Project・権限管理

### FR-PRJ-001

利用者はProjectを作成、閲覧、更新、論理削除できること。

Project論理削除の受入条件は次のとおりとする。

- FrontendのProject詳細画面から削除操作へ遷移できること。
- 削除を実行できるのはProject Admin以上とし、APIでも権限を検査すること。
- 誤操作防止のため、確認画面で対象Projectのslugと完全一致する文字列の再入力を要求すること。
- 削除時はProjectの`status`を`DELETED`、`deleted_at`を削除日時へ更新し、Project一覧およびProject詳細の通常取得対象から除外すること。
- Dataset、Run、Saved Graph、Artifact等をProject削除と同時に物理削除せず、各Resourceのretention policyに従って保持すること。
- MVP Frontendから復元できないことと、保持Resourceが即時物理削除されないことを確認画面へ明示すること。
- 削除成功後は実行中のFrontend pollingを停止し、Project一覧へ遷移すること。

### FR-PRJ-002

Dataset、Configuration、Experiment、Run、Graph、Artifact、ResultはProjectに所属すること。

### FR-PRJ-003

ProjectごとにViewer、Analyst、Maintainer、Project Adminを割り当てられること。

### FR-PRJ-004

APIはすべてのProject Resourceについてtenant境界とProject権限を検査すること。

### FR-PRJ-005

Project詳細画面から、Dataset、Discovery、Saved Graph、Causal Design、Inference、Run履歴へ遷移できること。

### FR-PRJ-006

Project概要には最低限次を表示すること。

- Dataset数
- Discovery Run数
- 保存済みGraph数
- Inference Run数
- 直近Runと状態
- 推奨される次の操作

---

## 7.2. Analysis Dataset管理

### FR-DAT-001

利用者はAnalysis-ready Datasetを論理Resourceとして登録できること。

### FR-DAT-002

DatasetとDataset Versionを分離し、Dataset Versionは不変snapshotとすること。

### FR-DAT-003

MVPの標準入力は、1 Dataset Versionにつき1 Dataset Table Versionとすること。

既存schemaが複数tableを許容することを妨げないが、MVP UIは複数table登録を必須としない。

### FR-DAT-004

MVPではCSVとParquetをupload可能とすること。RDA、RDSは標準入力に含めない。

### FR-DAT-005

Dataset Kindは少なくとも次を選択できること。

- `PROCESSED`
- `DISCOVERY_FEATURE`
- `INFERENCE_FEATURE`

既存互換のため`RAW`および`INTERIM`を保持してよいが、MVP UIの主選択肢としない。

### FR-DAT-006

Dataset Versionは最低限次を保持すること。

- Dataset ID
- Version番号
- status
- source type
- source metadata
- schema hash
- content hash
- row count
- column count
- file format
- 作成者
- 作成日時
- optional upstream pipeline reference

### FR-DAT-007

uploadされたobjectはArtifact Storeへstreaming保存し、API processのmemoryへ全量保持しないこと。

### FR-DAT-008

利用者はProject内のDataset一覧、DatasetごとのVersion一覧、最新Versionを確認できること。

### FR-DAT-009

利用者はDataset Versionを選択し、次を確認できること。

- schema
- page/limit付きpreview
- row count、column count
- null count / null ratio
- distinct count
- numeric summary
- categorical top values
- 作成元とcontent hash

### FR-DAT-010

大容量データのpreviewとprofileで、API processへ全量loadしないこと。

### FR-DAT-011

同一content hashの重複uploadを検出可能とすること。重複を拒否するか同一objectを再利用するかはProject policyで決定できること。

### FR-DAT-012

Dataset Versionは将来のExternal Dataset Referenceを表現可能であること。

External Dataset Referenceは少なくとも次を保持できるschemaとする。

- provider
- catalog
- schema
- tableまたはview
- snapshot versionまたはtimestamp
- source URI
- source pipeline Run ID
- schema hash
- optional content fingerprint

### FR-DAT-013

外部Datasetを参照する場合、`latest`等の可変参照をRunの不変入力として使用してはならない。Run受付時までにsnapshot versionを解決すること。

### FR-DAT-014

Dataset VersionがDiscoveryまたはInferenceに使用可能か、次をvalidationできること。

- statusがREADYである。
- tableが1件以上存在する。
- schemaを取得できる。
- 選択列が存在する。
- objectまたはexternal snapshotへアクセスできる。

### FR-DAT-015

Analysis-ready Datasetには、1行が表す分析単位の説明と、optional unit identifier columnを設定できること。identifierを設定した場合、重複数とnull数を確認できること。

### FR-DAT-016

MVPの通常UIでは、DiscoveryまたはInference Runのたびに利用者へlocal pathやDataset Registry YAMLの指定を要求しないこと。workerはDataset Versionのmetadataから必要な実行時registryまたはinput snapshotを生成すること。

---

## 7.3. Feature Semantics管理

### FR-SEM-001

利用者はDataset Versionの列一覧からFeature Semanticsを作成できること。

### FR-SEM-002

featureごとに少なくとも次を管理できること。

- name
- source column
- dtype
- role
- unit identifier flag
- categorical flag
- time metadata
- allowed for discovery
- allowed for adjustment
- post-treatment flag
- description
- optional domain metadata

### FR-SEM-003

MVPで利用可能なroleは少なくとも次とする。

- identifier
- treatment
- outcome
- covariate
- mediator
- collider
- post_treatment
- excluded

### FR-SEM-004

Feature Semanticsは論理Configurationと不変のFeature Semantics Versionに分離すること。

### FR-SEM-005

Feature Semantics VersionはDataset Versionまたは互換schema hashと関連付けること。

### FR-SEM-006

Feature Semanticsは次をvalidationすること。

- 指定列がDataset Versionに存在する。
- feature名が重複しない。
- identifierを分析変数として暗黙利用しない。
- treatmentとoutcomeが同一列ではない。
- post-treatment変数をadjustmentへ使用しない。
- collider、mediator、outcome、treatmentをadjustmentへ暗黙追加しない。

### FR-SEM-007

adjustment variableについて次を検査すること。

- roleがcovariateである。
- `allowed_for_adjustment=true` である。
- `post_treatment=false` である。
- treatment、outcome、mediator、colliderではない。

### FR-SEM-008

Feature Semantics VersionはDRAFT、VALID、PUBLISHED、DEPRECATEDの状態を持てること。Run modeが`RUN`の場合、原則としてPUBLISHED Versionを要求すること。

### FR-SEM-009

画面はroleの設定を単なる技術的column typeと混同せず、特にpost-treatment、mediator、colliderの調整リスクを説明すること。

---

## 7.4. Configuration管理

### Configuration Type

MVPで中心となるConfiguration Typeは次とする。

- `DISCOVERY_ANALYSIS`
- `FEATURE_SEMANTICS`
- `CAUSAL_DESIGN`
- `INFERENCE_ANALYSIS`

互換性のため次を保持してよい。

- `DISCOVERY_FEATURE`
- `INFERENCE_FEATURE`
- `ETL_EXTRACT`
- `ETL_TRANSFORM`
- `ETL_LOAD`
- `PIPELINE`

### FR-CFG-001

Configurationは論理Resourceと不変のConfiguration Versionに分離すること。

### FR-CFG-002

Configuration Versionは次を保持すること。

- canonical JSON/YAML
- schema version
- content hash
- status
- 作成者
- 作成日時
- validation result
- optional publish日時

### FR-CFG-003

状態は少なくともDRAFT、VALID、PUBLISHED、DEPRECATEDを持てること。

### FR-CFG-004

PUBLISHED後の内容を変更してはならない。変更時は新Versionを作成すること。

### FR-CFG-005

YAML/JSONのimport/exportを提供できること。ただし、MVPの主要操作は一般利用者向けformから実行可能とすること。

### FR-CFG-006

Configuration Typeごとにschema validationすること。

### FR-CFG-007

worker実行時には、DB上のConfiguration VersionからStage Runnerが読めるsnapshotをlocal workspaceへmaterializeすること。

### FR-CFG-008

Runは使用したConfiguration Version IDとcontent hashをExecution PlanおよびManifestへ記録すること。

---

## 7.5. Causal Discovery

### FR-DIS-001

Discovery Runは次を入力とすること。

- input mode
- Dataset Version
- Feature Semantics Version
- Discovery Analysis Configuration Version
- 選択した分析列
- random seed
- optional runtime override

### FR-DIS-002

MVPではAnalysis-ready Tableを直接読み込む`ANALYSIS_READY`相当の実行modeを、既存の`CONFIGURED_FEATURE_BUILD`相当modeに追加して提供すること。この新modeでは、複数table joinまたはComplete Journey固有Feature Buildを要求してはならない。既存modeの処理を削除または新modeへ置換してはならない。

### FR-DIS-003

Analysis-ready modeで許可する前処理は、再現可能で明示された最小限の処理に限定する。

- 列選択
- dtype validation
- 欠損値policy
- categorical encoding policy
- numeric standardization
- constant column除外
- collinearity check

join、業務集計、時間window Feature生成はAnalysis-ready modeの責務としない。

### FR-DIS-004

MVPで次のalgorithmを選択できること。

- PC
- GES
- DirectLiNGAM

NOTEARSはoptional dependencyと実行安定性が確認できた場合に追加してよい。

### FR-DIS-005

同一Discovery Runで複数algorithmを実行できること。

### FR-DIS-006

algorithmごとに次を保持すること。

- algorithm名とVersion
- status
- message
- resolved parameter
- node count
- edge count
- edge table
- diagnostic
- warning
- optional score/stability

### FR-DIS-007

Discovery Runは最低限次をArtifactとして登録すること。

- resolved analysis config
- resolved feature semantics
- analysis column list
- edge table
- algorithm summary
- diagnostics
- report
- stage manifest

### FR-DIS-008

PCのalpha sensitivity、bootstrap stability等、設定で有効化された診断をArtifactとして追跡すること。

### FR-DIS-009

optional dependencyが不足するalgorithmは、Run全体を不明な状態にせず、実行前validation errorまたはalgorithm単位の明確なUNSUPPORTED/SKIPPEDとして記録すること。

### FR-DIS-010

因果探索結果を確定的な因果構造として表示してはならず、algorithm、設定、diagnostic、warningを併記すること。

---

## 7.6. Discovery Graph比較

### FR-GRP-001

利用者はDiscovery Resultをalgorithm別のnode/edge graphとして閲覧できること。

### FR-GRP-002

graphには少なくとも次を表現できること。

- node名
- source / target
- edge directionまたはorientation
- directed / undirected / partially oriented等のedge type
- score
- stability
- treatment/outcomeの強調

### FR-GRP-003

2つ以上のalgorithm結果を並列表示できること。

### FR-GRP-004

比較画面は少なくとも次を集計すること。

- 共通edge
- algorithm Aのみに存在するedge
- algorithm Bのみに存在するedge
- orientationが異なるedge
- algorithmごとのnode/edge数

### FR-GRP-005

比較は、source/target文字列だけでなくedge orientationを区別可能なcanonical表現を用いること。

### FR-GRP-006

利用者はedge tableへ切り替え、filter、sort、score/stability確認ができること。

### FR-GRP-007

画面は、algorithm間の一致を因果的真実の証明として表示してはならない。

---

## 7.7. Saved Causal Graph管理

### FR-SCG-001

利用者はDiscovery Algorithm Resultを、推論に使用するSaved Causal Graphとして選択できること。

### FR-SCG-002

Saved Causal Graphは論理Resourceと不変のGraph Versionに分離すること。

### FR-SCG-003

Graph Versionは最低限次を保持すること。

- Project ID
- Graph ID
- Version番号
- source Discovery Run ID
- source Discovery Result ID
- source Algorithm Result ID
- source Dataset Version ID
- Feature Semantics Version ID
- algorithm
- resolved algorithm parameter hash
- node set
- edge set
- edge count
- graph content hash
- status
- 選択者
- 選択理由またはnote
- 作成日時

### FR-SCG-004

Graph Versionのedge setはArtifactとして保存し、DBには検索・表示に必要なprojectionを保持すること。

### FR-SCG-005

PUBLISHED Graph Versionは変更してはならない。別algorithmの採用またはedge変更は新Versionとすること。

### FR-SCG-006

MVPでは、algorithm出力をそのまま選択保存できればよく、edgeの手動追加・削除は必須としない。

### FR-SCG-007

Graph VersionをブラウザのlocalStorageのみへ保存してはならない。Metadata DatabaseとArtifact Storeを正本とすること。

### FR-SCG-008

Inference Runは、入力に使用したGraph Version IDとcontent hashをExecution PlanおよびManifestへ記録すること。

### FR-SCG-009

Graph Versionが参照するDataset VersionまたはFeature SemanticsとInference入力が不整合の場合、Run前にerrorとすること。

---

## 7.8. Causal Design管理

### FR-CDS-001

Causal Designは次を保持すること。

- estimand
- treatment name
- treatment levels
- treatment timeまたはtime zero
- outcome name
- outcome window
- unit
- target population
- adjustment strategy
- adjustment set
- assumptions
- optional Saved Graph Version
- analyst note

### FR-CDS-002

MVPで利用可能なestimandはATEとATTとする。

### FR-CDS-003

Causal Designは論理Resourceと不変のCausal Design Versionに分離すること。

### FR-CDS-004

Causal Design VersionはFeature Semantics VersionおよびDataset Versionと組み合わせてvalidationできること。

### FR-CDS-005

Causal Designの宣言とRunで指定されたtreatment、outcome、estimandが不一致の場合、MVPではerrorとすること。

### FR-CDS-006

adjustment setは自動決定結果を無言で採用せず、候補、除外理由、最終選択を利用者が確認できること。

### FR-CDS-007

Saved Graphからadjustment候補を導出する場合、導出規則とGraph Versionを記録すること。

### FR-CDS-008

assumptionは分析者の宣言または診断対象であり、システムによる証明済み事実として表示してはならない。

### FR-CDS-009

画面からtreatment、outcome、estimand、adjustment set、assumptionを入力し、validation、publishできること。YAMLの直接編集を必須としてはならない。

---

## 7.9. Edge Weight Inference

### FR-EWI-001

Edge Weight modeは次を入力とすること。

- input mode
- Dataset Version
- Feature Semantics Version
- Inference Analysis Configuration Version
- Saved Graph Version

互換性のためDiscovery Edge Artifactを直接指定するAPIを保持してよいが、MVP UIの主導線ではSaved Graph Versionを用いる。

### FR-EWI-002

入力Dataset Version、Feature Semantics Version、Saved Graph Versionのnode/column互換性をRun前に検証すること。

### FR-EWI-003

algorithm由来の各edgeに対し係数推定結果を生成すること。

Analysis-ready modeでは、Complete Journey固有Feature Buildまたは複数table joinを要求せず、入力tableの列を直接使用すること。

### FR-EWI-004

結果には可能な範囲で次を含めること。

- algorithm
- source / target
- coefficient
- standard error
- confidence interval
- p-value
- adjusted p-value
- sample count
- robust SE type
- status
- warning

### FR-EWI-005

出力を`exploratory_edge_coefficient`として明示し、識別済みcausal effectと同一視しないこと。

### FR-EWI-006

skipped edge、dropped column、non-estimable reasonを閲覧できること。

---

## 7.10. Treatment Effect Inference

### FR-TEI-001

Treatment Effect modeは次を入力とすること。

- input mode
- Dataset Version
- Feature Semantics Version
- Causal Design Version
- Inference Analysis Configuration Version
- Saved Graph Version

### FR-TEI-002

Analysis-ready modeでは、Complete Journey固有Feature Buildまたは複数table joinを要求せず、入力tableの列とFeature Semanticsを直接使用すること。

### FR-TEI-003

MVPで次のestimandを扱うこと。

- ATE
- ATT

### FR-TEI-004

MVPでは、実装済みかつvalidation済みの次のeffect methodを選択できること。

- difference in means
- OLS coefficient
- g-computation ATE/ATT
- IPW ATE/ATT
- AIPW ATE/ATT

### FR-TEI-005

adjustment strategyは少なくとも次を扱うこと。

- pre-treatment covariates
- manual
- graph-derived candidates

### FR-TEI-006

複数methodを実行した場合、各methodの推定値、標準誤差、信頼区間、p-value、adjusted p-value、sample count、note、warningを個別に保持すること。

### FR-TEI-007

p-value多重性補正方法を結果に記録すること。

### FR-TEI-008

最低限次の診断Artifactを登録すること。

- treatment counts / design diagnostics
- covariate balance
- propensity overlap
- selected adjustment set
- excluded adjustment candidates
- outcome distribution
- report
- manifest

### FR-TEI-009

結果画面には、推定値だけでなく次を同時表示すること。

- estimand
- treatment / outcome
- adjustment strategy
- adjustment set
- assumptions
- diagnostic status
- confidence interval
- warning
- Dataset Version
- Saved Graph Version

### FR-TEI-010

保存済みEffect ModelのscoringはMVP対象外とする。

---

## 7.11. Run・Execution Plan

### FR-RUN-001

次の実行modeを提供すること。

- `DRY_RUN`
- `VALIDATE_ONLY`
- `RUN`

### FR-RUN-002

DRY_RUNはstage codeを実行せず、解決済みExecution Planを返すこと。

### FR-RUN-003

VALIDATE_ONLYはstage codeを実行せず、resourceおよびcross-stage validation結果を返すこと。

### FR-RUN-004

RUNはvalidation成功後に非同期workerへ投入すること。

### FR-RUN-005

Run受付APIは分析完了を待たず、Run IDと初期statusを返すこと。

### FR-RUN-006

Execution Planは最低限次を解決すること。

- Run ID
- stage順序
- input mode
- Dataset Version IDとhash
- Feature Semantics Version IDとhash
- Configuration Version IDとhash
- optional Saved Graph Version IDとhash
- optional Causal Design Version IDとhash
- algorithm / inference method
- random seed
- resolved argument
- output declaration
- code/package/runtime version
- validation checklist

### FR-RUN-007

Execution PlanはRun受付後に不変とすること。

### FR-RUN-008

同一Project・同一Idempotency-Keyの重複Run作成を防止すること。

### FR-RUN-009

Run、Stage Run、Attemptを分離し、再試行履歴を上書きしないこと。

### FR-RUN-010

利用者はRunのcancelを要求できること。cancelはbest effortであることを明示すること。

### FR-RUN-011

RunとStage Runのprogress、warning、error、Artifact生成をeventとして取得できること。

### FR-RUN-012

Run詳細またはRun Result APIから、生成されたDiscovery Result、Edge Weight Result、Treatment Effect ResultのIDを取得できること。

---

## 7.12. Artifact・Manifest・Lineage

### FR-ART-001

Artifactは論理ID、Artifact kind、Object URI、checksum、size、media type、生成Attemptを持つこと。

### FR-ART-002

開発環境ではlocal filesystem、本番ではS3またはAzure Blob等を選択可能なAdapterとすること。

### FR-ART-003

local pathをAPIの永続契約として公開しないこと。

### FR-ART-004

Run Manifestは次を含むこと。

- Run ID
- Stage Run ID
- Attempt ID
- stage type
- analysis mode
- input resource IDs
- resource content hash
- Artifact IDsとchecksum
- random seed
- code commit
- package version
- dependency lock hash
- container image digest
- runtime metadata
- warning

### FR-ART-005

Manifest本体は不変Artifactとし、DBには検索用projectionを保存すること。

### FR-ART-006

次のlineageをResource IDで追跡できること。

```text
Dataset Version
  -> Feature Semantics Version
  -> Discovery Configuration Version
  -> Discovery Run / Result
  -> Saved Graph Version
  -> Causal Design Version
  -> Inference Configuration Version
  -> Inference Run / Result
  -> Diagnostic / Report Artifact
```

### FR-ART-007

Artifact downloadとmetadata閲覧にはProject権限とcolumn policyを適用すること。

---

## 7.13. 結果表示

### FR-RES-001 Discovery Result

Discovery Result画面は次を表示すること。

- Dataset Version
- Feature Semantics Version
- algorithm
- resolved parameter
- node / edge graph
- edge table
- score / stability
- diagnostic
- warning
- scientific notice

### FR-RES-002 Graph Comparison

Graph比較画面はFR-GRP-001からFR-GRP-007を満たし、選択したalgorithm結果からSaved Graph作成へ遷移できること。

### FR-RES-003 Edge Weight Result

Edge Weight Result画面は次を表示すること。

- Saved Graph Version
- edge coefficient table
- confidence interval
- p-value / adjusted p-value
- skipped edge
- dropped column
- warning
- exploratory coefficientである旨

### FR-RES-004 Treatment Effect Result

Treatment Effect Result画面は次を表示すること。

- point estimate
- confidence interval
- method
- ATE / ATT
- treatment / outcome
- adjustment set
- selected/excluded variable
- balance
- overlap
- assumptions
- diagnostic status
- warning

### FR-RES-005 Traceability

画面上のすべての結果から、生成元Run、Stage Run、Artifact、Configuration Version、Dataset Version、Saved Graph Versionへ遡れること。

### FR-RES-006 Result discoverability

利用者はResult IDを手入力しなくても、Project、RunまたはExperimentから結果へ到達できること。

### FR-RES-007 Export

MVPでは次のexportを提供すること。

- Discovery edge CSV
- Saved Graph JSONまたはCSV
- Edge Weight result CSV
- Treatment Effect result CSV
- Report Markdown
- Manifest JSON/YAML

---

## 7.14. Dataset確認・安全な可視化

v1.1の汎用BI可視化をMVP必須から外し、分析入力の妥当性確認に必要な範囲へ限定する。

### FR-VIS-001

Dataset Versionの単一tableについて、page/limit付きpreviewを表示できること。

### FR-VIS-002

columnごとにdtype、null count、distinct count、numeric summaryまたはcategorical top valuesを表示できること。

### FR-VIS-003

profileがsamplingまたはapproximationを用いた場合、そのmethod、sample size、seedを表示すること。

### FR-VIS-004

preview不可のcolumn値を画面へ含めてはならない。mask対象columnはpolicyに従ってmaskすること。

### FR-VIS-005

analysis不可のcolumnをDiscovery対象、treatment、outcome、adjustment variableへ指定させないこと。

### FR-VIS-006

histogram、scatter等の探索的データ可視化は追加可能だが、MVP受入条件には含めない。

---

## 7.15. Experiment管理

### FR-EXP-001

利用者はExperimentを作成し、複数Runを所属させられること。

### FR-EXP-002

Experimentは次を保持できること。

- title
- objective
- hypothesis
- notes
- source repository
- source commit
- notebook reference
- tags

### FR-EXP-003

Experiment内のRunをDataset、algorithm、Graph Version、estimand、method、resultで比較できること。

### FR-EXP-004

Experiment一覧・詳細UIはMVPの分析主導線完成後に実装してよい。

---

## 7.16. API要件

### 7.16.1. MVP代表Endpoint

既存Endpointを維持し、`*`を付けたEndpointまたは同等の機能を追加する。

```text
POST   /api/v1/projects
GET    /api/v1/projects
GET    /api/v1/projects/{project_id}

POST   /api/v1/projects/{project_id}/objects
POST   /api/v1/datasets
GET    /api/v1/datasets
POST   /api/v1/datasets/{dataset_id}/versions
GET    /api/v1/datasets/{dataset_id}/versions                    *
GET    /api/v1/dataset-versions/{version_id}
GET    /api/v1/dataset-table-versions/{table_version_id}/preview
GET    /api/v1/dataset-table-versions/{table_version_id}/profile

POST   /api/v1/configurations
GET    /api/v1/configurations
POST   /api/v1/configurations/{configuration_id}/versions
GET    /api/v1/configuration-versions/{version_id}
POST   /api/v1/configuration-versions/{version_id}/validate
POST   /api/v1/configuration-versions/{version_id}/publish

POST   /api/v1/runs
GET    /api/v1/runs
GET    /api/v1/runs/{run_id}
GET    /api/v1/runs/{run_id}/results                             *
GET    /api/v1/runs/{run_id}/events
GET    /api/v1/runs/{run_id}/artifacts
POST   /api/v1/runs/{run_id}/cancel
POST   /api/v1/runs/{run_id}/retry

GET    /api/v1/discovery-results/{result_id}
POST   /api/v1/causal-graphs                                    *
GET    /api/v1/causal-graphs                                    *
GET    /api/v1/causal-graphs/{graph_id}                          *
POST   /api/v1/causal-graphs/{graph_id}/versions                 *
GET    /api/v1/causal-graph-versions/{version_id}                *
POST   /api/v1/causal-graph-versions/{version_id}/publish        *

GET    /api/v1/edge-weight-results/{result_id}
GET    /api/v1/treatment-effect-results/{result_id}

GET    /api/v1/artifacts/{artifact_id}
GET    /api/v1/artifacts/{artifact_id}/content
GET    /api/v1/artifacts/{artifact_id}/lineage
```

Endpoint名は実装設計で変更してよいが、Dataset Version一覧、RunからResultへの導線、Saved Graphの永続化を欠落させてはならない。

### 7.16.2. API原則

- OpenAPIを生成する。
- HTTP schemaとdomain modelを直接同一化しない。
- 破壊的変更にはAPI Versionを付与する。
- list APIはpagination、filter、sortを提供する。
- timezone付きISO 8601を使用する。
- error responseを統一する。
- request IDとcorrelation IDを返す。
- 大容量Artifactは署名付きURL等で直接配信可能とする。
- Resource IDの手入力を通常UIの必須操作にしない。
- PUBLISHED Versionは更新APIで上書きできないようにする。

---

## 7.17. 既存CLI・ETL・Preprocessing後方互換要件

本節は、v1.2をもとにコードを変更する際の必須制約である。本節の「既存」は、v1.2実装着手時点の`main`ブランチで動作しているinterface、class、testを指す。

### FR-CMP-001 CLI entrypoint

次の既存CLI entrypointを維持すること。

- `ariadne-discovery`
- `ariadne-inference`
- `ariadne-pipeline`
- その他、既存テストまたは文書から使用されるETL entrypoint

既存引数で起動した場合、v1.2対応前と同じConfigured Feature Build経路を使用すること。

### FR-CMP-002 Complete Journey ETL

`src/ariadne/etl/completejourney/`および`src/ariadne/application/pipeline/etl.py`の既存class/functionを維持し、既存入力から既存の8つのParquet出力を生成できること。

### FR-CMP-003 Existing Feature Build

既存Discovery/Inference Feature Configuration、Dataset Registry、Feature Build classを維持し、既存CLIおよび既存Pipelineから利用可能であること。

### FR-CMP-004 Additive implementation

ANALYSIS_READY経路は追加実装とする。既存classの本体を単一table専用実装へ置き換えてはならない。共通化する場合も、既存class/functionのimport path、呼出契約、既定動作を互換Adapterで維持すること。

### FR-CMP-005 Explicit mode resolution

Webの新規RunはANALYSIS_READY相当modeを明示すること。既存CLI/API requestがmodeを持たない場合は、従来のConfigured Feature Build挙動を維持すること。入力table数、filename、Dataset Kindだけを根拠にmodeを暗黙切替してはならない。

### FR-CMP-006 Web visibility boundary

通常Web UIでは、Complete Journey ETL、複数raw file mapping、Dataset Registry YAML指定、Domain Feature Buildを必須stepとして表示しないこと。ただし、既存ETL APIやworker処理を削除してはならない。Advanced UIを将来追加できる構造を許容する。

### FR-CMP-007 Algorithm Input Conditioning

ANALYSIS_READY経路でも、列選択、dtype検証、欠損値policy、categorical encoding、標準化、constant列除外、collinearity check等のAlgorithm Input Conditioningを必要に応じて実行すること。これらを「前処理はMVP対象外」という理由で削除または無効化してはならない。

### FR-CMP-008 Provenance

両経路について、使用mode、実行したFeature BuildまたはAlgorithm Input Conditioning、入力列、出力列、除外列、resolved parameterをExecution Plan、Manifestまたは専用Artifactへ記録すること。

### FR-CMP-009 Regression tests

v1.2実装後も、少なくとも次の回帰テストを維持すること。

- Complete Journey ETLの既存fixtureから8 tableを生成できる。
- 既存Discovery CLIを既存引数で実行できる。
- 既存Inference CLIを既存引数で実行できる。
- 既存統合Pipelineを既存設定で実行またはvalidationできる。
- 新しいANALYSIS_READY経路が単一tableで実行できる。
- 一方のmode追加が他方のExecution Planを変更しない。

### FR-CMP-010 No dead-code deletion in MVP

通常Web UIから参照されなくなったことだけを理由として、既存ETL、preprocessing、registry、CLI、Configuration Type、API Endpointをdead codeとして削除してはならない。削除は、別途deprecation計画、利用状況確認、migration、major version変更を定義した場合に限る。

---

## 8. 非機能要件

## 8.1. 再現性

### NFR-REP-001

各Runから次を追跡可能であること。

- Dataset Versionとcontent hash
- Feature Semantics Versionとcontent hash
- Configuration Versionとcontent hash
- optional Saved Graph Versionとcontent hash
- optional Causal Design Versionとcontent hash
- Execution Plan
- Manifest
- code commit
- package version
- dependency lock hash
- container image digest
- random seed
- Artifact checksum

### NFR-REP-002

同一Run条件から再実行要求を作成できること。ただし新しいRun IDを発行すること。

### NFR-REP-003

数値的非決定性、外部library、並列実行差異によりbitwise一致を保証しない場合、その保証範囲を明示すること。

### NFR-REP-004

外部Datasetを使用する場合、Runには解決済みsnapshot identifierを記録すること。

---

## 8.2. 信頼性

- Queueはat-least-once deliveryを前提とする。
- workerは冪等なArtifact登録を行う。
- retryごとにAttemptを追加する。
- worker heartbeat/leaseを持つ。
- staleなRUNNINGを検出する。
- transient errorとpermanent errorを分類する。
- DB updateとqueue publishにはTransactional Outboxを利用する。
- Graph Version publishとArtifact登録は、正本が不整合にならないtransaction境界を持つ。

---

## 8.3. 性能・拡張性

具体値は利用規模確定後に設定する。少なくとも以下を満たす。

- Run受付APIは分析完了を待たない。
- uploadはstreaming処理する。
- preview/profileで全量をAPI processへloadしない。
- workerを水平増設できる。
- RunごとにCPU、memory、timeout上限を設定できる。
- Artifact upload/downloadはstreamingまたは直接転送を利用する。
- graph描画はnode/edge数の上限を設け、大規模graphではtable表示やfilterへ退避できる。

決定が必要なSLO:

- Run受付API p95
- metadata list API p95
- 最大upload size
- 最大row数・column数
- Discovery graph最大node/edge数
- 同時Run数
- queue wait time
- Run timeout
- retention期間

---

## 8.4. セキュリティ

- OIDC等で認証する。
- Project単位RBACを適用する。
- secretをConfiguration、Manifest、Dataset Source Referenceへ平文保存しない。
- Artifact Storeをpublic公開しない。
- download URLには期限を設ける。
- column単位の機密classificationを保持可能とする。
- preview、profile、Discovery列選択、Inference列選択、exportにcolumn policyを適用する。
- 任意Python実行をMVPで禁止する。
- Run、download、設定publish、Graph publish、権限変更、削除を監査する。
- 外部Dataset credentialはSecret Manager等から実行時に取得する。

---

## 8.5. 可観測性

- API request、Run、Stage Run、Attemptをcorrelation IDで関連付ける。
- JSON構造化logを出力する。
- queue length、wait time、Run success/failure、stage duration、worker heartbeat、Artifact errorをmetric化する。
- algorithm単位のsuccess、skip、failureをmetric化できること。
- 利用者向けerror summaryと技術者向けstack traceを分離する。

---

## 8.6. 科学的表示要件

### NFR-SCI-001

因果探索graphを真のDAGとして断定表示しない。

### NFR-SCI-002

edge weightを識別済みcausal effectとして表示しない。

### NFR-SCI-003

treatment effectにはestimand、adjustment set、assumptions、diagnosticsを併記する。

### NFR-SCI-004

p-valueのみで成功・失敗を判定しない。

### NFR-SCI-005

warningとlimitationをresultと同じ画面で確認可能にする。

### NFR-SCI-006

algorithm間でedgeが一致したことを、因果関係が証明された根拠として表示しない。

### NFR-SCI-007

Graph Versionの「保存」または「公開」は分析者が採用した仮説の固定を意味し、真実性の承認を意味しないことを画面へ明示する。

### NFR-SCI-008

自動提案されたadjustment candidateと、Analystが最終採用したadjustment setを区別して表示する。

---

## 8.7. Usability・Accessibility

- ProjectからDataset、Discovery、Graph、Causal Design、Inferenceへ順に進めるguided flowを提供する。
- UUIDやResult IDの手入力を通常操作として要求しない。
- validation errorは対象列、設定項目、修正方法を示す。
- 長時間Runでは状態、stage、開始時刻、最新eventを表示する。
- keyboard操作、focus表示、適切なlabel、色以外の状態表現を提供する。
- 日本語UIをMVPの標準とし、algorithm名、estimand等の専門用語は英語表記を併記してよい。

---

## 9. Resource状態

### 9.1. Dataset Version

```text
REGISTERING -> READY | FAILED
READY -> DEPRECATED
```

### 9.2. Configuration / Feature Semantics / Causal Design Version

```text
DRAFT -> VALID -> PUBLISHED -> DEPRECATED
        -> INVALID
```

### 9.3. Saved Graph Version

```text
DRAFT -> VALID -> PUBLISHED -> DEPRECATED
        -> INVALID
```

### 9.4. Run / Stage Run

```text
SUBMITTED
  -> QUEUED
  -> VALIDATING
  -> RUNNING
  -> SUCCEEDED | FAILED | CANCELLED

QUEUED | VALIDATING | RUNNING
  -> CANCEL_REQUESTED
  -> CANCELLED | FAILED | SUCCEEDED
```

### 9.5. Attempt

```text
CREATED
  -> QUEUED
  -> LEASED
  -> RUNNING
  -> SUCCEEDED | FAILED | CANCELLED | TIMED_OUT | LOST
```

---

## 10. MVP画面・中心フロー

### 10.1. 中心フロー

```text
1. Projectを開く
   |
2. Analysis Datasetを登録・選択する
   |
3. schema / preview / profileを確認する
   |
4. Feature Semanticsを定義・publishする
   |
5. 複数algorithmでDiscovery Runを実行する
   |
6. graphを比較する
   |
7. 推論に使用するGraph Versionを選択・publishする
   |
8. Causal Designを定義・publishする
   |
9. Inference Runを実行する
   |
10. 推定値・診断・仮定・lineageを確認する
```

### 10.2. 必須画面

| 画面 | 主な機能 |
|---|---|
| Project一覧 | Project作成、選択 |
| Project詳細 | 指標、最近のRun、中心フロー、次の操作 |
| Dataset一覧 | Dataset、Version、Kind、status |
| Dataset登録 | CSV/Parquet upload、Kind、説明 |
| Dataset Version詳細 | schema、preview、profile、hash |
| Feature Semantics editor | 列role、adjustment可否、post-treatment等 |
| Discovery設定 | Dataset、Semantics、algorithm、parameter |
| Discovery Run詳細 | status、event、Artifact、warning |
| Graph比較 | algorithm別graph、edge差分 |
| Saved Graph詳細 | source、edge、Version、note、publish |
| Causal Design editor | treatment、outcome、estimand、adjustment、assumption |
| Inference設定 | Graph、Design、method、runtime |
| Inference Result | estimate、CI、diagnostic、warning、lineage |

### 10.3. 前処理の扱い

MVP画面の主ナビゲーションでは「Data preparation」を「Analysis Dataset」へ変更する。

```text
旧:
  ファイルを登録
  前処理Runを作成

新:
  Analysis-ready Datasetを登録
  Dataset Versionを確認
  変数の意味を定義
  因果探索へ進む
```

Complete Journey ETL、既存Feature Build、Dataset Registry loaderは、CLI、既存Pipeline、開発用データ生成、回帰テスト、将来のAdvanced機能として残すこと。

通常Web UIからETL stepを外す変更は、Frontendのnavigation、form、API呼出しに限定する。API router、worker、Application Service、ETL/preprocessing class、Configuration Type、CLI entrypointを同時に削除してはならない。

実行時の関係は次のとおりとする。

```text
既存CLI / 既存Pipeline
  -> CONFIGURED_FEATURE_BUILD
  -> 既存Domain ETL / Feature Build
  -> Algorithm Input Conditioning
  -> Discovery / Inference

通常Web UI
  -> ANALYSIS_READY
  -> Domain ETL / Feature Buildをskip
  -> Algorithm Input Conditioning
  -> Discovery / Inference
```

したがって、通常Web UIに「前処理Run」画面が存在しないことと、プログラム内部に前処理classが存在し利用されることは矛盾しない。

---

## 11. 受入条件

### AC-001 Analysis Dataset登録

単一のCSVまたはParquetをuploadすると、指定したDataset Kindを持つDatasetと不変Dataset Versionが登録される。

### AC-002 Dataset Version確認

登録したDataset Versionについて、Version ID、content hash、schema、row/column count、preview、profileを画面から確認できる。

### AC-003 Dataset Version選択

利用者はUUIDを手入力せず、Project内のDatasetとDataset Versionを選択できる。

### AC-004 Feature Semantics

Dataset列にidentifier、treatment、outcome、covariate、excluded等のroleを設定し、validation済みFeature Semantics Versionとしてpublishできる。

### AC-005 Bad control validation

post-treatment、mediator、collider、treatment、outcomeを不正にadjustment setへ指定した場合、Inference実行前に検出できる。

### AC-006 Generic Discovery

Complete Journey固有の複数tableまたはFeature Buildを使わず、Analysis-readyな単一tableの選択列にDiscovery Runを実行できる。

### AC-007 Multi-algorithm Discovery

同一Dataset VersionとFeature Semantics Versionに対し、PC、GES、DirectLiNGAMのうち2つ以上を指定して実行し、algorithmごとのstatusとedgeを取得できる。

### AC-008 Graph表示

Discovery Resultをalgorithm別のnode/edge graphとedge tableで確認できる。

### AC-009 Graph比較

2つのalgorithmについて、共通edge、片方のみに存在するedge、orientationが異なるedgeを確認できる。

### AC-010 Saved Graph Version

利用者が選択したalgorithm結果を、source Run、Dataset Version、Feature Semantics Version、algorithm、edge hashを持つ不変Graph Versionとしてサーバーへ保存・publishできる。

### AC-011 Graph永続性

ブラウザを閉じ、別のブラウザsessionまたは別の権限ある利用者がProjectを開いても、保存済みGraph Versionを取得できる。

### AC-012 Causal Design

treatment、outcome、ATEまたはATT、adjustment set、assumptionを画面から入力し、Feature Semanticsと整合するCausal Design Versionとしてpublishできる。

### AC-013 Discovery to Inference

Saved Graph Versionを選択してInference Runを作成し、RunのExecution PlanとManifestから同Graph Versionへ遡れる。

### AC-014 Edge Weight

Saved Graphのedgeについて係数、標準誤差、信頼区間、p-value、status、warningを確認でき、画面に探索的係数である旨が表示される。

### AC-015 Treatment Effect

ATEまたはATTを指定し、1つ以上の推定methodについて推定値、信頼区間、adjustment set、balance/overlap等の診断、warningを確認できる。

### AC-016 Result導線

利用者はResult IDを手入力せず、ProjectまたはRun詳細からDiscovery ResultとInference Resultへ移動できる。

### AC-017 Traceability

画面上の推定値からDataset Version、Feature Semantics Version、Discovery Run、Saved Graph Version、Causal Design Version、Inference Run、Artifact、code versionへ遡れる。

### AC-018 Dry-run / Validate-only

DRY_RUNで解決済みExecution Planを取得でき、VALIDATE_ONLYでDataset、Semantics、Graph、Designの不整合を数値処理開始前に検出できる。

### AC-019 Retry

Stage失敗後にretryすると新しいAttemptが作成され、過去Attemptのerrorが保持される。

### AC-020 Idempotency

同一Project・同一Idempotency-KeyのRun作成要求でRunが重複しない。

### AC-021 Scientific notice

Discovery Graph、Saved Graph、Edge Weight、Treatment Effectの各画面に、結果の解釈範囲、仮定、warningが適切に表示される。

### AC-022 Existing CLI compatibility

v1.2変更前に成功していたDiscovery、Inference、統合PipelineのCLI commandを同じ必須引数で実行し、Configured Feature Build経路のExecution Planまたは結果を取得できる。

### AC-023 Complete Journey preprocessing compatibility

既存Complete Journey fixtureと既存class/functionを使用し、従来どおり8つのlogical tableをParquetとして生成できる。

### AC-024 Execution mode isolation

同じコードベース上でCONFIGURED_FEATURE_BUILDとANALYSIS_READYをそれぞれ明示して実行でき、一方の追加によって他方の入力解決、Feature Build、Artifact宣言が変化しない。

### AC-025 Analysis-ready conditioning

ANALYSIS_READY Runでも、設定された欠損値処理、encoding、標準化、constant列除外、collinearity checkが実行され、そのresolved設定と除外列をArtifactまたはManifestから確認できる。

### AC-026 Web/CLI responsibility boundary

通常Web UIではComplete Journeyの複数file、Registry YAML、ETL Runを指定せず中心フローを完遂できる。同時に、既存CLIからComplete Journey ETLとFeature Buildを引き続き実行できる。

---

## 12. 現行コードへの変更方針

### 12.1. 維持するもの

- `ariadne.causal.*` の数値実装
- `ariadne.etl.completejourney.*` のETL class
- `ariadne.application.pipeline.etl.execute_completejourney_etl`
- `ariadne.preprocessing.*` の既存Discovery/Inference Feature Build
- Dataset Registry loaderと既存YAML Configuration
- Run、Stage Run、Attempt、Eventの永続化
- dry-run / validate-only / run
- workerとTransactional Outbox
- Dataset VersionとArtifact Store
- Configuration Version
- Discovery、Edge Weight、Treatment Effectのprojection
- CLI entrypointと既存CLI引数
- Complete Journeyの既存test fixtureと回帰テスト

上記は「再利用できれば望ましい」項目ではなく、v1.2実装中の後方互換制約である。Frontendから呼ばれないことを理由に削除してはならない。

### 12.2. 優先して追加・変更するもの

#### P0-001 Generic Analysis-ready Discovery / Inference

単一tableを直接読み込み、選択列、Feature Semantics、明示的なAlgorithm Input ConditioningをDiscoveryおよびInferenceへ渡すApplication ServiceまたはStage Runner modeを追加する。既存Configured Feature Build modeとは別の明示的な分岐として追加し、Complete Journey固有Feature BuildをAnalysis-ready modeの暗黙依存にしない。

#### P0-002 Dataset Version list

Project/DatasetからVersionを選択するAPIとUIを追加する。

#### P0-003 Feature Semantics editor

Dataset schemaからFeature Semanticsを作成、validation、publishするUIとApplication Serviceを整備する。

#### P0-004 Saved Causal Graph

次を追加する。

```text
CausalGraph
CausalGraphVersion
CausalGraphNode
CausalGraphEdge
GraphVersionArtifact
GraphVersionLineage
```

名称はData Model設計で調整してよい。

#### P0-005 Run Result link

RunからDiscovery Result、Edge Weight Result、Treatment Effect Resultへ到達するprojection/APIを追加する。

#### P0-006 Causal Design form

YAMLやVersion IDの手入力ではなく、formからCausal Design Versionを作成できるようにする。

#### P0-007 Frontend workflow revision

現在のData preparation / ETL中心UIを、10章の中心フローへ変更する。

### 12.3. MVP後に追加するもの

```text
application/
  dataset_sources/
    ports.py
    databricks.py
infrastructure/
  databricks/
    client.py
    credentials.py
```

実際のpackage構造は既存Architectureに合わせて調整する。

### 12.4. 既存ETL機能の扱い

- API、worker、Application Service、domain class、Configuration Typeから削除しない。
- class/functionのimport pathと既存呼出契約を維持する。
- Complete Journeyの回帰テストを維持し、v1.2変更後も実行する。
- Frontendの通常主導線からのみ外す。
- CLI、既存Pipeline、開発用データ生成、Advanced利用として文書化する。
- 新しい汎用ETL機能へ拡張することをMVPの前提としない。

### 12.5. コンポーネント別変更指示

コーディングエージェントは、次の表を実装範囲の基準とすること。

| コンポーネント | v1.2で行うこと | v1.2で行ってはならないこと |
|---|---|---|
| `frontend/` | ETL中心の通常導線をAnalysis Dataset、Semantics、Discovery、Graph、Design、Inferenceへ変更する | Frontend変更に伴ってbackend ETL codeを削除する |
| Dataset API | Version一覧・選択を追加し、単一CSV/Parquet登録を使いやすくする | 複数tableを許す既存schemaを単一table専用へ破壊変更する |
| Run schema/planner | 解決済みinput modeを追加し、Plan/Manifestへ記録する | mode未指定の既存requestを勝手にANALYSIS_READYへ変更する |
| Discovery worker | ANALYSIS_READY分岐を追加する | 既存Configured Feature Build分岐を置換する |
| Inference worker | ANALYSIS_READY分岐を追加する | 既存Configured Feature Build分岐を置換する |
| Algorithm Input Conditioning | 両modeで必要な処理を明示設定・記録する | 「前処理対象外」を理由に無効化する |
| Complete Journey ETL | 現行挙動とtestを維持する | 削除、単一table化、Web専用契約への変更を行う |
| Existing preprocessing | CLI/Pipelineからの現行利用を維持する | unused判定して削除する |
| CLI | 既存commandと引数を維持する | Webの新flowに合わせて必須引数や既定動作を変える |
| Saved Graph | server-side Resource/Versionとして新規追加する | localStorageを正本にする |

### 12.6. input mode解決規則

実装上の名称にかかわらず、次の規則を満たすこと。

1. 新しい通常Web UIはANALYSIS_READY相当modeを明示してRunを作成する。
2. 既存CLI/API requestに新mode項目が存在しない場合、従来のConfigured Feature Build挙動へ解決する。
3. Dataset Kindが`PROCESSED`であることだけを理由にANALYSIS_READYへ切り替えない。
4. table数が1件であることだけを理由にANALYSIS_READYへ切り替えない。
5. modeと必要入力が矛盾する場合、worker実行前のvalidation errorとする。
6. resolved modeをExecution Plan、Run detail、Manifestへ含める。
7. DRY_RUNとVALIDATE_ONLYでも本番RUNと同じmode解決規則を使用する。

### 12.7. 実装完了時の必須検証

実装者は、変更した機能の新規テストに加え、次を実行すること。

1. repository全体の既存test suite
2. Complete Journey ETL unit/integration test
3. Discovery CLI regression test
4. Inference CLI regression test
5. Pipeline CLI regression test
6. ANALYSIS_READY Discovery test
7. ANALYSIS_READY Edge Weight test
8. ANALYSIS_READY Treatment Effect test
9. 両input modeのExecution Plan snapshot比較

既存testが新要件と無関係に失敗する場合を除き、既存testの削除またはassertion緩和で通過させてはならない。

---

## 13. 実装優先順位

### Phase 0: 要件・契約固定

1. Analysis-ready Tableの入力契約を決定する。
2. Feature Semantics schemaを新MVPに合わせる。
3. Saved Causal GraphのData Modelと状態遷移を決定する。
4. Discovery ResultからGraph Versionへのlineageを決定する。
5. Causal DesignとGraph Versionの整合validationを決定する。
6. CONFIGURED_FEATURE_BUILDとANALYSIS_READYのinput mode契約を固定する。
7. 既存CLI、Complete Journey ETL、既存Feature Buildの回帰テストを先に固定する。

### Phase 1: DatasetとSemantics

1. CSV/Parquet upload
2. Dataset Kind選択
3. Dataset Version一覧・詳細
4. preview/profile
5. Feature Semantics editor
6. validation/publish

### Phase 2: Generic Discoveryと比較

1. 既存Configured Feature Buildの回帰確認
2. 追加のAnalysis-ready mode
3. PC/GES/DirectLiNGAM
4. Run監視
5. Result自動導線
6. graph表示
7. edge差分比較

### Phase 3: Saved GraphとCausal Design

1. Graph Resource/Version
2. Graph Artifactとhash
3. Graph publish
4. Causal Design form
5. Semantics/Graph/Design validation

### Phase 4: Inferenceと来歴

1. 既存Configured Feature Build Inferenceの回帰確認
2. 追加のGeneric Analysis-ready Inference mode
3. Edge Weight
4. Treatment Effect
5. diagnostics
6. Result UI
7. lineage UI
8. export

### Phase 5: External Dataset Source

1. Dataset Source Port
2. Databricks credential方式
3. Unity Catalog/Delta snapshot解決
4. schema取得
5. worker materializationまたはquery方式
6. source lineage

---

## 14. 重要な設計判断

### 14.1. ETLをMVPの価値仮説から外す

ETLは重要だが、通常Web UIでETLを構築・操作させる価値はDatabricks等の成熟した外部基盤と重複する。そのためWeb MVPはAnalysis-ready Dataset以後の因果分析に集中する。

これはariadne packageからETL責務や前処理classを除去する判断ではない。CLI、既存Pipeline、デモ、テスト、Advanced利用における既存ETL・Feature Buildは維持する。

### 14.2. 単一tableをMVP標準とする

複数table対応はDataset model上で維持できるが、MVPの利用者体験とgeneric analysis runnerは単一tableを前提とする。これにより、logical table mapping、join、RDA/RDS処理を価値検証から切り離す。

### 14.3. Uploadは製品の中心ではなく検証手段とする

CSV/Parquet uploadは、ariadne単体でMVP価値を試すための簡易入力Adapterである。将来的な本番入力は不変の外部Dataset Referenceを想定する。

### 14.4. Saved Graphを独立Resourceとする

Discovery Algorithm Resultは計算結果であり、分析者が推論に採用した仮説とは意味が異なる。両者を分離し、選択行為、Version、理由、lineageを保存する。

### 14.5. localStorageを正本にしない

ブラウザ保存は一時的UI stateに限定する。Dataset選択、Graph選択、Causal Design、結果の正本はサーバー側へ保存する。

### 14.6. MLflowをMVP必須にしない

MVPの正本はMetadata DatabaseとArtifact Storeとする。外部trackingはAdapterとして追加可能にする。

### 14.7. Model RegistryをMVP必須にしない

MVPは推定結果・診断・reportを管理する。保存モデルの安定したserialization、互換性、scoring契約は別要件とする。

### 14.8. Feature Buildを暗黙実行しない

Analysis-ready modeでは、業務Feature Buildやjoinを暗黙に行わない。一方、Configured Feature Build modeでは既存Feature Buildを従来どおり実行する。両modeで実行するAlgorithm Input ConditioningはExecution PlanとArtifactへ記録する。

### 14.9. Graphからの自動Adjustmentを最終判断にしない

Graphはalgorithm依存の探索仮説である。Graphからadjustment候補を導出しても、最終adjustment setとassumptionはAnalystが確認・保存する。

---

## 15. 未決事項

### 15.1. MVP開始前に決定が必要

1. Analysis-ready modeが許可するdtype
2. 欠損値policy
3. categorical encodingの方式と責務
4. Discovery対象にできる最大column数
5. DirectLiNGAM optional dependencyのcontainer組込方針
6. Saved Graphのcanonical edge表現
7. partially oriented edgeをInferenceへ渡す際のpolicy
8. Graph VersionのVALID/PUBLISHED validation内容
9. Treatment EffectでSaved Graphを必須にする範囲
10. Graph由来adjustment candidateの導出規則
11. Feature SemanticsとDataset Versionのschema互換規則
12. Dataset Version一覧APIのURLとpagination
13. Run Result APIのresponse schema
14. Result/Graphのretentionと論理削除policy

### 15.2. 運用開始前に決定が必要

1. Frontend frameworkを現行Vanilla JSのまま継続するか
2. Job Queue製品
3. 本番Object Storage製品
4. 認証provider
5. 最大Dataset size
6. worker実行backend
7. Run timeout
8. Artifact retention
9. tenant分離方式
10. graph描画library
11. default sampling size
12. small-cell suppressionの既定値
13. algorithm container image戦略

### 15.3. Databricks連携前に決定が必要

1. Unity Catalog必須とするか
2. Delta Versionまたはtimestampのどちらをsnapshot IDとするか
3. Databricks SQL WarehouseとSpark Connectのどちらを利用するか
4. データをArtifact Storeへcopyするか、実行時queryするか
5. OAuth、Service Principal、Managed Identity等の認証方式
6. row/column policyをどちらのシステムで正本管理するか
7. Databricks Job Run IDとariadne lineageの接続方法

---

## 16. 調査・設計根拠

- `README.md`
- `pyproject.toml`
- `frontend/index.html`
- `frontend/app.js`
- `frontend/styles.css`
- `src/ariadne/interfaces/api/app.py`
- `src/ariadne/interfaces/api/schemas/resources.py`
- `src/ariadne/interfaces/api/routers/projects.py`
- `src/ariadne/interfaces/api/routers/datasets.py`
- `src/ariadne/interfaces/api/routers/configurations.py`
- `src/ariadne/interfaces/api/routers/runs.py`
- `src/ariadne/application/run_execution/services.py`
- `src/ariadne/application/pipeline/etl.py`
- `src/ariadne/workers/executor.py`
- `src/ariadne/workers/materialization.py`
- `src/ariadne/workers/projection.py`
- `src/ariadne/etl/completejourney/extract.py`
- `src/ariadne/etl/completejourney/load.py`
- `src/ariadne/preprocessing/common/semantics.py`
- `src/ariadne/causal/design/schemas.py`
- `src/ariadne/causal/inference/constants.py`
- `configs/etl/completejourney/extract.yaml`
- `configs/etl/completejourney/load.yaml`
- `configs/causal/discovery.yaml`
- `configs/causal/inference/defaults.yaml`
- `configs/preprocessing/feature_semantics.yaml`
- `configs/causal/inference/designs/completejourney_household.yaml`
- `_work/20260718_requirements_of_web_service/01_web_service_requirements_v1.1.md`
- `_work/20260720_expand_flontend/20260720_prompt_memo_01.md`

---

## 17. MVP完了の定義

本MVPは、単にAPIが存在すること、因果探索グラフを表示できること、または推定値を出力できることだけでは完了としない。

次の一連の操作を、通常UIからResource IDの手入力なしで完遂できた時点をMVP完了とする。

```text
Analysis-ready Datasetを登録する
  -> Dataset Versionを確認する
  -> Feature Semanticsを定義・publishする
  -> 複数algorithmでDiscoveryを実行する
  -> graphを比較する
  -> 推論に使用するGraph Versionを保存・publishする
  -> Causal Designを定義・publishする
  -> Inferenceを実行する
  -> 推定値、診断、仮定、warningを確認する
  -> DatasetからResultまでのlineageを確認する
```

この中心フローが成立した後に、Databricks等の外部Dataset Source、Graph編集、ETLのWeb UI公開または汎用化、汎用可視化、高度な分析機能を追加する。既存CLI・ETL・Feature Buildは、この中心フローの実装前後を通じて維持する。
