# ariadne Webサービス化 要件定義書

- 文書版: 1.0
- 基準リポジトリ: `kousuke-ota-datascience/ariadne`
- 基準ブランチ: `main`
- 調査日: 2026-07-18
- 対象: MVPおよびMVP後の拡張

---

## 1. 文書の目的

本書は、Pythonパッケージとして実装されている `ariadne` を、データ管理、設定管理、非同期実行、実験管理、結果閲覧を備えたWebサービスへ発展させるための要件を定義する。

本書の要件は、既存コードの責務分割と実行契約を維持し、次を原則とする。

1. 因果探索・因果推論の数値実装をWeb層へ移植しない。
2. 既存のApplication Service、Stage Runner、Validation、Manifestを再利用する。
3. CLIを廃止せず、Web APIとCLIを同一Application Serviceへの別Adapterとして共存させる。
4. ローカルファイルパス中心の契約を、永続IDとArtifact URI中心の契約へ段階的に置換する。
5. 因果的妥当性を自動保証するサービスとは位置付けない。

---

## 2. 現行実装の把握

### 2.1. パッケージ構造

現行コードは、少なくとも以下の責務に分離されている。

| パッケージ | 現行責務 |
|---|---|
| `application` | 実行計画、実行戦略、stage実行、cross-stage validation |
| `causal.discovery` | 因果探索、graph正規化、診断、reporting |
| `causal.inference` | edge weight推定、treatment effect推定、診断、reporting |
| `causal.design` | Causal Design schema |
| `etl` | Complete Journey向けETLとdataset registry loader |
| `preprocessing` | discovery用・inference用の特徴量構築 |
| `infrastructure.config` | YAML読込、path解決、hash、snapshot |
| `infrastructure.artifacts` | Artifact RegistryとRun Manifest |
| `infrastructure.storage` | CSV、YAML、pickle、ParquetのFile I/O |
| `interfaces.cli` | discovery、inference、統合pipelineのCLI |
| `shared.validation` | ValidationIssueとValidationResult |

### 2.2. 現行の統合パイプライン

現行の `PipelinePlanner` は、固定された2 stageを解決する。

1. `discovery`
2. `inference`

実行戦略は次の3種類である。

- `dry_run`
- `validate_only`
- `run`

`discovery` から `inference` への接続は、discovery stageが生成する `manifest.yaml` を介して行われる。

### 2.3. 現行のInference mode

現行のinferenceは次の2 modeを持つ。

| mode | 意味 |
|---|---|
| `edge_weight` | 因果探索済みedgeについて回帰係数を推定する探索的分析 |
| `treatment_effect` | treatment、outcome、estimand、adjustment setを明示して効果推定する分析 |

`treatment_effect` では、ATE/ATT、複数推定法、ロバスト標準誤差、propensity clipping、cross-fitting設定、調整集合選択、診断出力が実装されている。

### 2.4. 現行の制約

現時点では次の制約がある。

- Web API実装は存在せず、公開interfaceはCLIである。
- FastAPIとUvicornは依存関係に含まれるが、API routerやHTTP schemaは未実装である。
- ETL Application ServiceはComplete Journey固有であり、統合pipelineのstageには組み込まれていない。
- Dataset RegistryはYAMLとローカルpathを正本としている。
- ArtifactおよびManifestはローカルpathを保持する。
- `StagePlan.name` は `discovery` と `inference` に固定されている。
- Run状態、再試行、cancel、worker lease等を永続化するDBはない。
- 保存済み効果モデルを新規データへ適用するscoring機能は実装されていない。
- MLflow等の外部Experiment Trackingは依存関係にも実装にも含まれていない。
- Causal Designが表現するestimandはATEとATTである。
- 本パイプラインは因果識別を証明せず、宣言した設計・feature semantics・adjustment setの整合性を検査する。

---

## 3. システム目的

### 3.1. 目的

本システムは、因果分析の入力、設定、実行、結果、診断、再現性情報を一元管理し、ブラウザおよびAPIから安全に操作できる分析基盤を提供する。

### 3.2. 解決する課題

- YAML、CLI引数、入力path、出力pathの組合せを利用者が手作業で管理している。
- 過去runの入力データ、設定、コード、成果物を検索しにくい。
- 長時間処理の状態、失敗理由、再試行履歴を管理できない。
- 複数runの因果探索結果、効果推定結果、診断結果を比較しにくい。
- 現行Manifestがlocal filesystemに依存し、複数worker構成へ移行しにくい。
- 分析結果をNotebookやCSVを直接開かずに閲覧できない。

### 3.3. 非目的

- 因果識別の自動証明
- 因果探索結果の真実性保証
- 完全自動の調整集合決定
- 任意コードを無制限に実行するNotebook SaaS
- リアルタイムstreaming推論
- 保存済みモデルのonline serving
- 業務施策の自動実行

---

## 4. 対象利用者

| Actor | 主な責務 |
|---|---|
| Viewer | Run、結果、診断、レポートを閲覧する |
| Analyst | Dataset、設定、Pipelineを作成し、Runを実行する |
| Maintainer | Algorithm、runtime、worker、Artifactを管理する |
| Project Admin | Project member、権限、retentionを管理する |
| System Admin | システム全体、tenant、監査、障害を管理する |

---

## 5. 対象範囲

### 5.1. MVP対象

- Project管理
- Dataset collectionとversion管理
- 複数tableで構成されるDatasetの登録
- CSV/Parquet/Object Storage objectの登録
- Complete Journey ETLの非同期実行
- 現行YAML設定の登録、validation、version管理
- Pipelineのdry-run、validate-only、run
- discovery stageの非同期実行
- inference stageの非同期実行
- inference mode `edge_weight`
- inference mode `treatment_effect`
- Run、Stage Run、Attempt、Eventの管理
- Manifest、Artifact、lineage管理
- 因果探索edgeの可視化
- edge weight結果の閲覧
- treatment effectと診断結果の閲覧
- 実験単位でのRun整理と比較
- 認証、Project単位認可、監査ログ

### 5.2. MVP後の拡張

- ETL plugin化および任意Datasetへの適用
- preprocessingを独立stageへ分割
- 任意DAG pipeline editor
- Schedules、event-triggered run
- MLflow等の外部tracking adapter
- 保存済みEffect Modelの登録とscoring
- CATE/ITE/uplift
- notebook連携
- custom algorithm plugin管理
- Kubernetes job等の分離実行backend
- review/approval workflow

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
  |-- Job Queue
  |-- Authentication / Authorization
  |
Worker
  |-- ariadne.application
  |-- ariadne.causal
  |-- ariadne.preprocessing
  |-- ariadne.etl
  |-- Local work directory
  |-- Artifact Store
```

### 6.2. デプロイ単位

MVPでは次の4単位を必須とする。

1. Frontend
2. API
3. Worker
4. Metadata Database

Job QueueとArtifact Storeは、開発環境では簡易実装を許可し、本番環境では分離可能とする。

### 6.3. Modular Monolith優先

初期段階では、Data、ETL、Discovery、Inferenceを別々のHTTP microserviceへ分割しない。

理由:

- 現行コードは1 Python package内で明確にmodule分離されている。
- stage間で共通の設定、Feature Semantics、Manifest、Validationを利用する。
- 早期の物理分割は分散transaction、schema互換、運用負荷を増大させる。

ただし、API processと重い分析workerは物理的に分離する。

### 6.4. Control PlaneとExecution Plane

#### Control Plane

- Resource CRUD
- version管理
- Run受付
- Execution Plan生成
- 状態管理
- 認証・認可
- Artifact metadata管理
- UI向け検索API

#### Execution Plane

- workerによるvalidation
- local workspaceへのinput materialization
- 既存Stage Runnerの実行
- Artifact upload
- Manifest生成
- progress/event発行

---

## 7. 機能要件

## 7.1. Project・権限管理

### FR-PRJ-001

利用者はProjectを作成、閲覧、更新、論理削除できること。

### FR-PRJ-002

Dataset、Configuration、Experiment、Pipeline、Run、ArtifactはProjectに所属すること。

### FR-PRJ-003

ProjectごとにViewer、Analyst、Maintainer、Project Adminを割り当てられること。

### FR-PRJ-004

APIはすべてのProject resourceについてtenant境界とProject権限を検査すること。

---

## 7.2. Dataset管理

現行のComplete Journeyは複数の論理tableから構成されるため、Datasetを単一fileとしてのみ扱ってはならない。

### FR-DAT-001

利用者は論理Dataset collectionを登録できること。

### FR-DAT-002

Dataset Versionは不変のsnapshotであること。

### FR-DAT-003

Dataset Versionは1件以上のDataset Table Versionを持てること。

例:

- campaigns
- transactions
- demographics
- products

### FR-DAT-004

Dataset Table Versionは次を保持すること。

- logical table name
- physical object reference
- file format
- row count
- column count
- schema
- checksum
- partition情報
- source metadata

### FR-DAT-005

MVPで登録可能なformatはCSVとParquetとする。既存Object Storage objectの参照登録を許可する。

### FR-DAT-006

利用者はtable単位でschema、sample、基本統計、欠損、unique数を閲覧できること。

### FR-DAT-007

大容量データのpreviewはpage/limitを持ち、API processへ全量loadしないこと。

### FR-DAT-008

Dataset Versionから現行 `load.yaml` 相当のdataset registry snapshotを生成できること。

### FR-DAT-009

現行YAML dataset registryをimportし、DatasetおよびDataset Versionへ変換できること。

---

## 7.3. ETL管理・実行

### FR-ETL-001

MVPではComplete Journey ETLを1つの組込ETL typeとして提供すること。

### FR-ETL-002

ETL Runはextract、normalize、Parquet loadの結果を追跡できること。

### FR-ETL-003

ETL出力は新しいDataset Versionとして登録すること。

### FR-ETL-004

ETL Runは、入力raw object、使用設定、出力table、行数、schema、checksum、warning、errorを記録すること。

### FR-ETL-005

ETL処理はAPI request内で実行せず、非同期workerで実行すること。

### FR-ETL-006

MVPでは任意Python script uploadを許可しないこと。

### FR-ETL-007

MVP後はETL implementationをplugin化し、dataset typeごとにAdapterを登録可能とすること。

---

## 7.4. Configuration管理

現行コードのYAML単位を初期version管理単位とする。

### Configuration Type

- `ETL_EXTRACT`
- `ETL_TRANSFORM`
- `ETL_LOAD`
- `DISCOVERY_ANALYSIS`
- `DISCOVERY_FEATURE`
- `INFERENCE_ANALYSIS`
- `INFERENCE_FEATURE`
- `FEATURE_SEMANTICS`
- `CAUSAL_DESIGN`
- `PIPELINE`

### FR-CFG-001

Configurationは論理resourceと不変のConfiguration Versionに分離すること。

### FR-CFG-002

Configuration Versionは次を保持すること。

- canonical JSON/YAML
- schema version
- content hash
- status
-作成者
- 作成日時
- validation result

### FR-CFG-003

状態は少なくとも `DRAFT`、`PUBLISHED`、`DEPRECATED` を持つこと。

### FR-CFG-004

`PUBLISHED`後の内容を変更してはならない。変更時は新versionを作成すること。

### FR-CFG-005

現行YAMLをimport/exportできること。

### FR-CFG-006

API入力はConfiguration Typeごとにschema validationすること。

### FR-CFG-007

worker実行時には、DB上のConfiguration Versionから現行コードが読めるYAML snapshotをlocal workspaceへmaterializeすること。

---

## 7.5. Feature Semantics管理

### FR-SEM-001

featureごとに次を管理できること。

- name
- role
- source table
- source column
- unit ID
- aggregation
- transform
- dtype
- allowed for adjustment
- post-treatment flag
- metadata

### FR-SEM-002

現行で利用可能なroleを保持すること。

- treatment
- outcome
- covariate
- mediator
- collider
- post_treatment

### FR-SEM-003

Discovery Feature Configurationからresolved Feature Semanticsを導出し、Artifactとして保存できること。

### FR-SEM-004

DiscoveryとInferenceで同名featureのsemanticsが不一致の場合、Run前validationをerrorとすること。

### FR-SEM-005

adjustment variableについて次を検査すること。

- roleがcovariateである。
- `allowed_for_adjustment=true` である。
- `post_treatment=false` である。
- treatment、outcome、mediator、colliderではない。

---

## 7.6. Causal Design管理

### FR-CDS-001

Causal Designは次を保持すること。

- estimand
- treatment name
- treatment time
- treatment levels
- outcome name
- outcome window
- unit
- time zero
- adjustment set name
- assumptions

### FR-CDS-002

MVPで利用可能なestimandはATEとATTとする。

### FR-CDS-003

Causal Design VersionはFeature Semantics Versionと組み合わせてvalidationできること。

### FR-CDS-004

Causal Designの宣言とRunで指定されたtreatment、outcome、estimandが不一致の場合、warningまたはerror policyを選択できること。MVP既定はerrorとする。

### FR-CDS-005

assumptionは「宣言」であり、システムによる証明済み事実として表示してはならない。

---

## 7.7. Pipeline定義

### FR-PLN-001

Pipeline Definitionはversion管理されること。

### FR-PLN-002

MVPで利用可能なstage typeは次とする。

- `ETL`
- `DISCOVERY`
- `INFERENCE`

### FR-PLN-003

MVPの統合分析pipelineは、現行実装と同じく `DISCOVERY -> INFERENCE` を基本形とすること。

### FR-PLN-004

`INFERENCE` stageはanalysis modeとして次を持つこと。

- `EDGE_WEIGHT`
- `TREATMENT_EFFECT`

### FR-PLN-005

Pipeline Stageは次を参照できること。

- Configuration Version
- Dataset Version
- 上流Artifact output
- runtime parameter

### FR-PLN-006

Pipeline実行前にExecution Planを生成し、次を解決すること。

- run ID
- stage順序
- stage enable/disable
- input resource ID
- configuration version ID
- resolved arguments
- output declaration
- random seed
- runtime image/code version
- validation check list

### FR-PLN-007

Execution PlanはRun受付後に不変とすること。

### FR-PLN-008

MVP後はstage graphを一般DAGへ拡張可能なschemaとするが、MVP UIで任意DAG editorを提供する必要はない。

---

## 7.8. Pipeline実行戦略

### FR-RUN-001

現行の3戦略をWeb APIでも提供すること。

- `DRY_RUN`
- `VALIDATE_ONLY`
- `RUN`

### FR-RUN-002

`DRY_RUN` はstage codeを実行せず、解決済みExecution Planを返すこと。

### FR-RUN-003

`VALIDATE_ONLY` はstage codeを実行せず、cross-stage validation結果を返すこと。

### FR-RUN-004

`RUN` はvalidation成功後にstageを実行すること。

### FR-RUN-005

Run受付APIは分析完了を待たず、`run_id` と初期statusを返すこと。

### FR-RUN-006

同一Project・同一Idempotency-Keyの重複Run作成を防止すること。

### FR-RUN-007

Run、Stage Run、Attemptを分離し、再試行履歴を上書きしないこと。

### FR-RUN-008

利用者はRunのcancelを要求できること。cancelはbest effortであることを明示すること。

### FR-RUN-009

RunとStage Runのprogress、warning、error、Artifact生成をeventとして取得できること。

---

## 7.9. Causal Discovery

### FR-DIS-001

Discovery Runは次を入力とすること。

- Dataset Version
- Discovery Analysis Configuration Version
- Discovery Feature Configuration Version
- random seed
- runtime override

### FR-DIS-002

MVPで現行実装が許可するalgorithmを選択できること。

- PC
- GES
- DirectLiNGAM
- NOTEARS

Optional dependencyが不足するalgorithmは、実行前または実行時に明確なunsupported/skipとして記録すること。

### FR-DIS-003

Discovery Runは最低限次をArtifactとして登録すること。

- resolved analysis config
- resolved feature config
- resolved feature semantics
- edge table
- algorithm summary
- variable metadata
- diagnostics
- report
- stage manifest

### FR-DIS-004

複数algorithmを実行した場合、algorithmごとにstatus、message、edge Artifactを区別すること。

### FR-DIS-005

PCのalpha sensitivity、bootstrap stability等、設定で有効化された診断をArtifactとして追跡すること。

### FR-DIS-006

因果探索結果を確定的な因果構造として表示してはならず、algorithm、設定、diagnostic、warningを併記すること。

---

## 7.10. Edge Weight Inference

### FR-EWI-001

Edge Weight modeはDiscovery ManifestまたはDiscovery Edge Artifactを入力として要求すること。

### FR-EWI-002

algorithmごとのedgeに対し係数推定結果を生成すること。

### FR-EWI-003

結果には可能な範囲で次を含めること。

- algorithm
- source/target
- coefficient
- standard error
- p-value
- adjusted p-value
- sample count
- robust SE type
- status
- warning

### FR-EWI-004

出力を `exploratory_edge_coefficient` として明示し、識別済みcausal effectと同一視しないこと。

### FR-EWI-005

skipped edge、dropped column、non-estimable reasonを閲覧できること。

---

## 7.11. Treatment Effect Inference

### FR-TEI-001

Treatment Effect modeは次を入力とすること。

- Dataset Version
- Inference Feature Configuration Version
- Feature Semantics Version
- Causal Design Version
- Inference Analysis Configuration Version
- optional Discovery Edge Artifact

### FR-TEI-002

MVPで次のestimandを扱うこと。

- ATE
- ATT

### FR-TEI-003

現行実装のeffect methodを選択できること。

- difference in means
- OLS coefficient
- g-computation ATE/ATT
- IPW ATE/ATT
- AIPW ATE/ATT

### FR-TEI-004

adjustment strategyは次を扱うこと。

- pre-treatment covariates
- manual
- graph parents

### FR-TEI-005

複数methodを実行した場合、各methodの推定値、標準誤差、信頼区間、p-value、補正p-value、noteを個別に保持すること。

### FR-TEI-006

p-value多重性補正方法を結果に記録すること。

### FR-TEI-007

最低限次の診断Artifactを登録すること。

- treatment counts/design diagnostics
- covariate balance
- propensity overlap
- outcome distribution
- selected adjustment set
- excluded adjustment candidates
- report
- manifest

### FR-TEI-008

結果画面には、推定値だけでなくestimand、adjustment set、assumption、diagnostic status、warningを表示すること。

### FR-TEI-009

保存済みモデルのscoringはMVP対象外とする。現行の推定器が安定したserialization/compatibility契約を持たないためである。

---

## 7.12. 実験管理

現行repositoryの `experiments/<連番>_<サブテーマ>` と `notebooks/<連番>_<サブテーマ>` に対応する論理単位をWeb上に持つ。

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

Experiment内のRunを設定、Dataset、algorithm、estimand、method、resultで比較できること。

### FR-EXP-004

外部Experiment Trackingとの連携はoptional adapterとし、Metadata Databaseの代替にしないこと。

---

## 7.13. Artifact・Manifest管理

### FR-ART-001

Artifactは論理ID、Artifact kind、Object URI、checksum、size、media type、生成Attemptを持つこと。

### FR-ART-002

開発環境ではlocal filesystem、本番ではS3互換storeを選択可能なAdapterとすること。

### FR-ART-003

local pathをAPIの永続契約として公開しないこと。

### FR-ART-004

現行Run ManifestをVersion 2へ拡張し、次を含めること。

- run ID
- stage run ID
- attempt ID
- stage type
- analysis mode
- input resource IDs
- configuration version IDsとhash
- artifact IDsとchecksum
- random seed
- code commit
- package version
- container image digest
- runtime metadata
- warning

### FR-ART-005

Manifest本体は不変Artifactとし、DBには検索用projectionを保存すること。

### FR-ART-006

上流・下流ArtifactのlineageをIDで追跡できること。

---

## 7.14. 結果可視化

### FR-VIS-001 Dataset

- schema
- sample
- 欠損
- distribution
- table間件数

### FR-VIS-002 Discovery

- node/edge graph
- algorithm filter
- edge direction/type
- stability/score
- treatment/outcome強調
- Run差分

### FR-VIS-003 Edge Weight

- edge coefficient table
- confidence interval
- p-value/adjusted p-value
- skipped edges
- dropped columns

### FR-VIS-004 Treatment Effect

- method別point estimateとconfidence interval
- ATE/ATT
- adjustment set
- balance
- propensity overlap
- outcome distribution
- warning

### FR-VIS-005

画面上のすべての結果から、生成元Run、Stage Run、Artifact、Configuration Version、Dataset Versionへ遡れること。

---

## 7.15. API要件

### 代表Endpoint

```text
POST   /api/v1/projects
GET    /api/v1/projects/{project_id}

POST   /api/v1/datasets
POST   /api/v1/datasets/{dataset_id}/versions
GET    /api/v1/dataset-versions/{version_id}
GET    /api/v1/dataset-table-versions/{table_version_id}/preview

POST   /api/v1/configurations
POST   /api/v1/configurations/{configuration_id}/versions
POST   /api/v1/configuration-versions/{version_id}/validate
POST   /api/v1/configuration-versions/{version_id}/publish

POST   /api/v1/experiments
POST   /api/v1/pipeline-definitions
POST   /api/v1/runs
GET    /api/v1/runs/{run_id}
POST   /api/v1/runs/{run_id}/cancel
POST   /api/v1/runs/{run_id}/retry
GET    /api/v1/runs/{run_id}/events
GET    /api/v1/runs/{run_id}/artifacts

GET    /api/v1/discovery-results/{result_id}
GET    /api/v1/edge-weight-results/{result_id}
GET    /api/v1/treatment-effect-results/{result_id}
```

### API原則

- OpenAPIを生成する。
- HTTP schemaとdomain dataclassを直接同一化しない。
- 破壊的変更にはAPI versionを付与する。
- pagination、filter、sortを提供する。
- timezone付きISO 8601を使用する。
- error responseを統一する。
- request IDとcorrelation IDを返す。
- 大容量Artifactは署名付きURL等で直接配信する。

---

## 8. 非機能要件

## 8.1. 再現性

### NFR-REP-001

各Runから次を追跡可能であること。

- Dataset Version
- Configuration Version
- Execution Plan
- Manifest
- code commit
- package version
- dependency lock hash
- container image digest
- random seed
- Artifact checksum

### NFR-REP-002

同一Run条件から再実行要求を作成できること。ただし、新しいRun IDを発行すること。

### NFR-REP-003

数値的非決定性や外部library差異によりbitwise一致を保証しない場合、その保証範囲を明示すること。

---

## 8.2. 信頼性

- Queueはat-least-once deliveryを前提とする。
- workerは冪等なArtifact登録を行う。
- retryごとにAttemptを追加する。
- worker heartbeat/leaseを持つ。
- staleなRUNNINGを検出する。
- transient errorとpermanent errorを分類する。
- DB updateとqueue publishにはTransactional Outboxを利用する。

---

## 8.3. 性能・拡張性

具体値は利用規模確定後に設定する。少なくとも以下を満たす。

- Run受付APIは分析完了を待たない。
- previewで全量loadしない。
- workerを水平増設できる。
- RunごとにCPU、memory、timeout上限を設定できる。
- Artifact upload/downloadはstreamingまたは直接転送を利用する。

決定が必要なSLO:

- Run受付API p95
- metadata list API p95
- 最大upload size
- 最大table row/column数
- 同時Run数
- queue wait time
- retention期間

---

## 8.4. セキュリティ

- OIDC等で認証する。
- Project単位RBACを適用する。
- secretをConfiguration/Manifestに平文保存しない。
- Artifact Storeをpublic公開しない。
- download URLには期限を設ける。
- column単位の機密classificationを保持可能とする。
- 任意Python実行をMVPで禁止する。
- Run、download、設定publish、権限変更、削除を監査する。

---

## 8.5. 可観測性

- API request、Run、Stage Run、Attemptをcorrelation IDで関連付ける。
- JSON構造化logを出力する。
- queue length、wait time、Run success/failure、stage duration、worker heartbeat、Artifact errorをmetric化する。
- 利用者向けerror summaryと技術者向けstack traceを分離する。

---

## 8.6. 科学的表示要件

- 因果探索graphを真のDAGとして断定表示しない。
- edge weightを識別済みcausal effectとして表示しない。
- treatment effectにはestimand、adjustment set、assumptions、diagnosticsを併記する。
- p-valueのみで成功・失敗を判定しない。
- warningとlimitationをresultと同じ画面で確認可能にする。

---

## 9. Run状態

### Run/Stage Run

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

### Attempt

```text
CREATED
  -> QUEUED
  -> LEASED
  -> RUNNING
  -> SUCCEEDED | FAILED | CANCELLED | TIMED_OUT | LOST
```

---

## 10. 受入条件

### AC-001 Dataset import

現行Complete Journey `load.yaml` をimportすると、1つのDataset Versionと8つのDataset Table Versionが登録される。

### AC-002 ETL

Complete Journey ETL Runを開始すると非同期実行され、出力Parquet群が新Dataset Versionとして登録される。

### AC-003 Configuration version

YAMLを登録・publishすると不変Configuration Versionが生成され、同一内容のhashを確認できる。

### AC-004 Dry-run

統合Pipelineをdry-runすると、stage、input、configuration、resolved argument、output予定、validation項目を取得できる。

### AC-005 Validate-only

Feature Semantics不一致、Causal Design不整合、bad controlをstage code実行前に検出できる。

### AC-006 Discovery to Inference

Discovery Runで生成されたManifest/Edge ArtifactをInference RunがIDで参照できる。

### AC-007 Treatment Effect

ATEまたはATTを指定し、複数methodの推定結果とbalance/overlap等の診断を閲覧できる。

### AC-008 Retry

Stage失敗後にretryすると新しいAttemptが作成され、過去Attemptのerrorが保持される。

### AC-009 Traceability

画面上の推定値からDataset Version、Configuration Version、Run、Artifact、Manifest、code commitへ遡れる。

### AC-010 Idempotency

同一Project・同一Idempotency-KeyのRun作成要求でRunが重複しない。

---

## 11. 現行コードへの変更方針

### 11.1. 維持するもの

- `ariadne.causal.*` の数値実装
- `preprocessing.*` のfeature build
- `CrossStageValidator`
- `StageRunner` protocol
- dry-run/validate-only/run strategy
- CLI entrypoint
- YAML import/export

### 11.2. 追加するもの

```text
src/ariadne/
  interfaces/
    api/
      app.py
      routers/
      schemas/
      dependencies/
  application/
    use_cases/
    ports/
    services/
  infrastructure/
    persistence/
    queue/
    artifact_store/
    auth/
  workers/
```

### 11.3. 変更するもの

1. `StagePlan` のpath型入力を、resource referenceとworker-local pathの二層へ分離する。
2. `PipelinePlanner` がDB上のConfiguration VersionとDataset VersionからExecution Planを生成できるようにする。
3. `PipelineExecutor` を同期CLI実行だけでなく、1 stage単位のworker実行へ分割可能にする。
4. `RunManifest` をVersion 2へ拡張し、ID、checksum、runtime provenanceを保持する。
5. `ArtifactRegistry` をlocal path registryからArtifact declarationへ拡張する。
6. ETLをStage Runner化し、Run/Manifest契約へ接続する。
7. `Path.mkdir` 等のvalidation副作用をControl Plane validationから除去し、worker workspace validationへ移す。

---

## 12. 重要な設計判断

### 12.1. MLflowはMVP必須にしない

現行packageにMLflow依存・integrationがないため、MVPの正本はPostgreSQLとArtifact Storeとする。外部trackingはadapterとして後付け可能にする。

### 12.2. Model RegistryをMVP必須にしない

現行Inferenceは推定結果・診断・reportを出力するが、安定した保存モデルscoring契約を提供していない。したがって、Artifact管理は必須、Model Registryは将来拡張とする。

### 12.3. Stage粒度を過度に細分化しない

現行Discovery/Inference CLIは内部でpreprocessingも実行する。MVPでは既存境界を維持し、性能・再利用要求が明確になった段階でFEATURE_BUILDを独立stage化する。

---

## 13. 未決事項

1. Frontend framework
2. Job Queue製品
3. Object Storage製品
4. 認証provider
5. 最大Dataset size
6. worker実行backend
7. local developmentのqueue方式
8. Artifact retention
9. tenant分離方式
10. Discovery graph描画library
11. Configuration editorをform中心にするかYAML editor中心にするか
12. raw data uploadを初期から許可するか、Object Storage参照登録に限定するか
13. Daskを実運用で有効化するDataset size閾値
14. optional algorithm dependencyのcontainer image戦略

---

## 14. 調査根拠ファイル

- `README.md`
- `pyproject.toml`
- `tree.txt`
- `src/ariadne/application/planning.py`
- `src/ariadne/application/execution.py`
- `src/ariadne/application/strategies.py`
- `src/ariadne/application/validation.py`
- `src/ariadne/application/etl_pipeline.py`
- `src/ariadne/infrastructure/artifacts/registry.py`
- `src/ariadne/infrastructure/storage/files.py`
- `src/ariadne/preprocessing/common/semantics.py`
- `src/ariadne/causal/design/schemas.py`
- `src/ariadne/causal/inference/constants.py`
- `src/ariadne/causal/inference/modes/edge_weight_mode.py`
- `src/ariadne/causal/inference/modes/treatment_effect_mode.py`
- `configs/causal/inference/pipeline.yaml`
- `configs/causal/inference/defaults.yaml`
- `configs/causal/discovery.yaml`
- `configs/preprocessing/feature_semantics.yaml`
- `configs/causal/inference/designs/completejourney_household.yaml`
- `docs/reproducibility.rst`
- `docs/methodology/limitations.rst`
