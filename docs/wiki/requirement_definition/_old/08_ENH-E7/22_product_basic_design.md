# 22 プロダクト基本設計

- 文書状態: `APPROVED`
- 文書種別: 現行プロダクト基本設計のeffective snapshot
- 上位文書: `00_product_concept_memo.md`, `10_requirements_definition.md`, `21_logical_data_design.md`
- 下位文書: `23_api_interface_design.md`, `30_detailed_design.md`

## 1. 設計目的

本書は、AriadneのProduct Architecture、Project Management、Analysis Workspace、Capability、Workflow、状態制御、Persistence、Result / Artifact / Lineage、Security等の基本設計を定義する。

Family / Navigation Stageの導入はWorkspaceのinformation architectureとapplication navigation modelを変更するが、runtime execution lifecycleの責務をpresentation taxonomyへ従属させない。

## 2. System Context

```text
Analyst / Reviewer / Operator
            │
            ▼
        Web Frontend / CLI
            │
            ▼
        Versioned Web API
            │
   ┌────────┼────────┐
   ▼        ▼        ▼
Product  Query     Workflow
Domain   Services  Application
   │        │        │
   └────────┼────────┘
            ▼
Metadata DB / Artifact Store
            │
            ▼
           Worker
            │
   ┌────────┼─────────────┐
   ▼        ▼             ▼
Explore  Causal       Predictive
Runners  Runners       Runners
```

Web FrontendはProject-global surfaceとanalytical surfaceを提示する。現行実装のscientific CLIはWeb/API Resource lifecycleの薄い別表現ではなく、local configを入力としてdomain validationと`ScientificCoreAdapter`を直接呼び出すheadless interfaceである。少なくとも`ariadne-discover`はWeb/APIのExecution IDを作成せず、`ariadne-identify` / `ariadne-refute` / `ariadne-sensitivity`もlocal scientific stageとして実行される。Current architectureではこの既存境界を保持し、CLIへbrowser route、Current Family、Navigation Stageをrequired inputとして導入しない。

## 3. Architecture Principle

### 3.1 Layer

- Domain: Resource、state、invariant、value object
- Application: use case、transaction、policy、planner、executor control、navigation coordination
- Port: repositories、artifact_store、clock、scientific_core、unit_of_work
- Adapter: SQL、Filesystem（current `LocalArtifactStore`）、Scientific library、ML library
- Object Storage adapterは`NFR-020b = DEFERRED / NOT_IMPLEMENTED / FUTURE`であり、current implementationには含めない。
- Interface: Web API、Worker、CLI、Frontend

DomainはWeb Framework、ORM、plot library、ML library、browser routeおよびlegacy moduleへ依存しない。

### 3.2 Capability分離

```text
Shared Product Core
├── Project / Context
├── Data / Analysis View
├── Workflow Core
├── Result / Artifact / Lineage
└── Security / Project Authorization

Analysis Capabilities
├── Exploratory
├── Causal
└── Predictive
```

各Capabilityは少なくとも次のFamily-specific semanticsを所有する。

- Family Specification Schema
- Planner
- Stage Runner
- Family Validation
- Result Schema
- analytical UI surface / binding
- Navigation Stage catalog
- Benchmark / Acceptance Test

Generic Product/Application codeは、個別FamilyのStage literalや分析意味論を集中所有しない。

### 3.3 Family / Navigation Stage / Execution Stageの責務分離

- `AnalysisFamily`: analytical capability discriminator。
- `Navigation Stage`: Family内のユーザーのwork/view context。
- `Execution Stage`: runtime plan/lifecycle上の処理単位。

`Navigation Stage != Execution Stage`を基本invariantとする。Navigation Stageの追加・名称変更・並び替えだけを理由にExecution Plan、Stage dependency、retry、attempt、status等を変更しない。

## 4. Application Information Architecture

### 4.1 Top-level surface responsibility

Ariadneのapplication UIはProject ManagementとAnalysis Workspaceを別surface・別navigation scopeとして構成する。

```text
Application
├─ Projects Surface
│  ├─ Project List
│  └─ Project Register
│
├─ Project Management Shell
│  ├─ Project Header
│  ├─ Project Local Navigation
│  ├─ Overview
│  ├─ Research Context
│  ├─ Data
│  └─ Results / Lineage
│
└─ Analysis Workspace Shell
   ├─ Analysis Context
   ├─ Family tabs
   ├─ Family-local Stage sidebar
   └─ Stage Contents
```

Project lifecycle/resource managementとanalysis paradigm/work-view contextを同一navigation hierarchyへ混在させない。

### 4.2 Project Management

#### 4.2.1 Projects Surface

`/projects`はProject List、`/projects/new`はProject Registerのcanonical surfaceである。

Project作成成功時は`/projects/{new_project_id}/overview`へ遷移する。

#### 4.2.2 Selected Project shell

Selected Projectは次のlocal navigationを持つ。

```text
Overview
Research Context
Data
Results / Lineage
```

Resource ownership:

| Surface | Responsibility |
| --- | --- |
| Overview | Project metadata / identity / status / archive |
| Research Context | Research Context lifecycle / DRAFT-FIXED / history / related analysis |
| Data | Dataset / Dataset Version / Schema / Preview / Analysis View lifecycle |
| Results / Lineage | persisted cross-analysis aggregation / comparison / Artifact / Lineage / Annotation |

Analysis ViewはFamily横断のversioned analysis inputであり、create/edit/version-management authorityをDataが持つ。

#### 4.2.3 Project routes

```text
/projects
/projects/new
/projects/{project_id}/overview
/projects/{project_id}/context
/projects/{project_id}/data
/projects/{project_id}/results
```

Short route:

```text
/projects/{project_id}
```

は、history replace semanticsで`/projects/{project_id}/overview`へnormalizeする。

### 4.3 Analysis Workspace

Analysis WorkspaceはProject Managementから独立したanalysis execution/presentation surfaceである。

```text
┌──────────────────────────────────────────────────────────────┐
│ Current Project | Research Context | Dataset | Analysis View │
│                                      [Project Management]    │
├──────────────────────────────────────────────────────────────┤
│ Exploratory | Causal | Predictive                            │
├──────────────────┬───────────────────────────────────────────┤
│ Stage navigation │ Stage Contents                            │
└──────────────────┴───────────────────────────────────────────┘
```

- Family = 上部のanalytical navigation
- Navigation Stage = selected Family内の左navigation
- Stage Contents = selected Family/Stageのmain presentation
- Family / Stage navigationはAnalysis Workspace内だけに表示する

#### 4.3.1 Analysis Context

Analysis Contextは次の4要素からなる。

```text
Current Project
Active Research Context
Dataset Version
Analysis View
```

Current Projectはcanonical Analysis URLの`project_id`から決まり、Analysis Workspace内ではread-onlyとする。Project変更はProjects / Project Management経由で行う。

Research Context / Dataset Version / Analysis ViewはCurrent Projectと整合するexisting resource/stateから選択する。

Dataset Version変更時にselected Analysis Viewが互換でない場合、Analysis View selectionを解除する。有効なselectionを復元できない場合は架空default resourceを生成せずunselectedとする。

context不足だけを理由にFamily / Stage routeを書き換えない。必要input不足はoperation availability / validationで表現する。

#### 4.3.2 Family navigation

Exploratory / Predictive / CausalをAnalysis Familyとして常時認識可能にする。Family切替時はbackend read-only navigation catalogの`default_stage_id`をauthorityとする。

```text
GET /api/v1/navigation/analysis
schema = analysis-navigation/1
```

Frontendはfull catalog（label/order/default等）をduplicate ownershipしない。

| Family | slug | default_stage_id |
| --- | --- | --- |
| EXPLORATORY | `exploratory` | `profile` |
| PREDICTIVE | `predictive` | `setup` |
| CAUSAL | `causal` | `setup` |

#### 4.3.3 Family-local Navigation Stage

Selected FamilyのNavigation Stageのみを表示する。

Exploratory:

- Profile
- Data Quality
- Distribution
- Relationships
- Comparison
- Findings

Predictive:

- Setup
- Train
- Predict
- Metrics
- Explainability
- Model Management

Causal:

- Setup
- Discovery
- Identification
- Estimation
- Effects
- Diagnostics
- Sensitivity

Family間でStage数を揃えるためのdummy Stageは作らない。Stage順はpresentation orderでありruntime dependency / required progressionではない。

### 4.4 Route / deep link / history

Application NavigationはProject NavigationとAnalysis Navigationを別authorityとして扱う。

```text
Application Navigation
├─ Project Navigation
│  ├─ /projects
│  ├─ /projects/new
│  └─ /projects/{project_id}/{section}
│
└─ Analysis Navigation
   └─ /projects/{project_id}/analysis/{family_slug}/{stage_slug}[/resource/...]
```

Canonical Analysis route:

```text
/projects/{project_id}/analysis/{family_slug}/{stage_slug}
```

Resource deep route:

```text
/projects/{project_id}/analysis/{family_slug}/{stage_slug}/resource/{resource_type}/{resource_id}
```

Resource deep routeのFamily/Stageとresource semanticが矛盾する場合はsilent correctionせずroute errorとする。

Project/Analysis双方で次を成立させる。

- direct link
- reload
- browser Back
- browser Forward

Supported legacy analytical entryはcanonical Analysis routeへ一方向normalizeし、旧navigationをparallel authorityとして維持しない。

### 4.5 Stage Contents / existing capability placement

#### 4.5.1 Causal

Existing Causal surfaceを次へ配置する。

| Stage | Primary responsibility |
| --- | --- |
| Setup | causal question / design preparation / Direct Graph Registration |
| Discovery | Discovery specification / PC-GES / Graph Candidates / comparison-edit-adopt-fix |
| Identification | Identification input / Data Eligibility / Gate |
| Estimation | estimator selection / override / execution / revision |
| Effects | Treatment Effect Results / result comparison |
| Diagnostics | diagnostics / scientific warnings |
| Sensitivity | Refutation / Sensitivity analysis |

Causal execution semanticsはNavigation Stage配置を理由に変更しない。

#### 4.5.2 Exploratory

| Stage | Existing operation / availability | Placement behavior |
| --- | --- | --- |
| Profile | `PROFILE` | operation controlとProfile result |
| Data Quality | dedicated operationなし | read-only availability。existing `PROFILE` resultを表示し、存在しなければ`NO_PROFILE_RESULT`とProfileへの導線を表示。新Execution/resource/backend stateを作らない |
| Distribution | `DISTRIBUTION` | operation controlとresult |
| Relationships | `ASSOCIATION` | operation controlとresult |
| Comparison | `GROUP_SUMMARY`, `TIME_TREND` | 両operationのcontrol/result。`TIME_TREND`は既存grouping/aggregation semanticsを維持し、新しい時系列モデル/時刻型validationを追加しない |
| Findings | `CHART` + saved Exploratory Results | `CHART` control、Chart result/artifact、saved result。`CHART`はexisting persistent operation semanticsを維持する |

`DATA_QUALITY` operationをtaxonomy充足のために新設しない。Stage placementはpresentation/navigation decisionであり、Exploratory planner、runner、Result type、artifact type、API/persistenceを変更しない。

#### 4.5.3 Predictive

Existing semantics:

```text
Prediction Task
→ Split
→ Training
→ Evaluation
→ Explanation
→ Model Card
```

を保持する。

Navigation Stageはpresentation/navigation viewであり、新しいPredictive backend Execution modelではない。

| Stage | Primary presentation |
| --- | --- |
| Setup | Prediction Task / target-feature / Split configuration |
| Train | Training / status / result |
| Predict | existing prediction output presentationの範囲 |
| Metrics | Evaluation / metrics |
| Explainability | Explanation |
| Model Management | Model Card / existing model management surface |

### 4.6 Loading / Error / Accessibility

- presentation stateは`IDLE / LOADING / READY / EMPTY / PARTIAL / ERROR / CANCELLED`を区別する。
- navigation metadata loadingを明示する。
- unknown Family / Stageをsilent fallbackしない。
- renderer binding欠落はunsupported stateとして検出する。
- current main surfacesはkeyboard操作、deterministic focus、accessible name、error association、non-color semanticsを満たす。
- normal text contrastは4.5:1以上、large text / UI graphics / focus indicatorは3:1以上をtargetとする。
- small viewportでもProject scope / Family dimension / Stage dimensionを混同させない。

## 5. Generic Workflow Core

### 5.1 Planner

`PlannerRegistry`はAnalysis FamilyとSpecification Schema VersionからPlannerを解決する。

```text
AnalysisSpecification
  ↓
PlannerRegistry.resolve(family, schema_version)
  ↓
Family Planner
  ↓
ExecutionPlan
```

PlannerはDomain上のruntime planを生成し、browser navigation stateを入力として要求しない。

### 5.2 Plan

Execution Planはruntime Stage DAGである。

- Stage keyはPlan内一意。
- Stage Typeはruntime operation identityを表す。
- Edgeはoutput / input bindingを表す。
- cycle禁止。
- required input未解決禁止。
- Runner未登録禁止。

Navigation Stageのsidebar orderをExecution Plan dependencyへ変換しない。

### 5.3 Executor

Generic Executorはcanonical lifecycle/application serviceが所有するworkflow execution context内で、Analysis内容を知らずにruntime Stageを実行する。

1. dependency解決
2. runtime Stage sequencing
3. Runner解決・invocation
4. workflow-level validation
5. temporary output binding

canonical Execution lifecycleはNavigation改修の対象外とし、current contractを維持する。基本設計上の境界は次のとおり。

- Execution technical statusは`QUEUED / RUNNING / SUCCEEDED / FAILED / CANCELLED`で管理する。
- Worker ownershipは`Execution.lease_owner / lease_expires_at`とrepository-level claim / renew / completeで管理し、Navigation stateをclaim条件へ追加しない。
- retry/rerun/reviseはcanonical Execution / revision semanticsとして扱い、Navigation Stage遷移へ変換しない。
- runtime Stageの進行は`StageExecution`とappend-only `StageAttempt`で表現する。
- Result / Artifactはcanonical Execution / StageExecution ownershipから生成・永続化し、browser routeやCurrent Navigation Stageをpersistent ownership fieldへ追加しない。
- transaction境界とpersistent lifecycle authorityはproduct application / persistence側に残し、Navigation componentへ移さない。

### 5.4 Runner Registry

runtime Runner Registryは`StageType`によりrunnerを解決する。

Navigation Stage IDを`StageType`として登録しない。巨大な`if navigation_stage == ...`をExecutorへ追加しない。

### 5.5 Navigation Stageとの境界

次を禁止する。

- `NavigationStageDescriptor`を`StageDefinition` / `StageExecution`のsubtypeにする。
- Navigation Stage IDをruntime `StageType`へ流用する。
- `AnalysisSpecification.navigation_stage`をexecution prerequisiteとして追加する。
- runtime moduleからbrowser route / Navigation Stage moduleへ依存する。

#### 5.5.1 Distribution

`Exploratory / Distribution`がDataset/profile/resultのreadだけで成立する場合、対応するruntime Execution Stageを作らない。

#### 5.5.2 Metrics

`Predictive / Metrics`は既存evaluation Resultを読むだけで成立してよい。Navigation taxonomyを理由に`METRICS` runtime Stageを新設しない。

#### 5.5.3 Explainability

1 Navigation Stageから複数read/compute use caseを呼び出してよい。Navigation StageとExecution Stageのcardinalityを1:1へ固定しない。

### 5.6 CLI / Library independence

CLI / Python library / backend use caseは、Analysis Specificationまたは既存use-case inputだけでexecutionを開始できる。

`Current Navigation Stage`、browser route、sidebar stateをrequired inputへ追加しない。

## 6. Family別Workflow / Capability

この章で扱う`Workflow`はruntime execution semanticsであり、4章のNavigation Stage一覧とは別概念である。

### 6.1 Exploratory

現行実装の`ExploratoryPlanner`は、`exploratory-analysis-spec/1`のoperationを次のruntime Stageへ写像し、**1 Execution Planにつき1 runtime Stage**を生成する。

| family_spec.operation | runtime stage_key | StageType |
| --- | --- | --- |
| `PROFILE` | `profile` | `exploratory.profile.v1` |
| `DISTRIBUTION` | `distribution` | `exploratory.distribution.v1` |
| `ASSOCIATION` | `association` | `exploratory.association.v1` |
| `GROUP_SUMMARY` | `aggregate` | `exploratory.aggregate.v1` |
| `TIME_TREND` | `time_trend` | `exploratory.time_trend.v1` |
| `CHART` | `chart` | `exploratory.chart.v1` |

Navigation Stage:

```text
Profile / Data Quality / Distribution / Relationships / Comparison / Findings
```

は上記runtime operationと同一taxonomyではない。例えば`Data Quality`や`Findings`に同名runtime Stageは存在しなくてよく、保存済みDataset/Result/Annotation/Artifactのreadで成立してよい。Navigation Stageを開いたことだけを理由にpersistent Executionを作らない。

### 6.2 Causal

現行実装の`CausalPlanner`は`causal-analysis-spec/2`向けcompatibility plannerである。canonical `Execution.operation`を次のruntime StageTypeへ写像し、**1 canonical Executionにつき1 runtime StageからなるExecution Plan**を生成する。

| ExecutionOperation | StageType |
| --- | --- |
| `DISCOVERY` | `causal.discovery.v1` |
| `IDENTIFICATION` | `causal.identification.v1` |
| `ESTIMATION` | `causal.estimation.v2` |
| `REFUTATION` | `causal.refutation.v1` |
| `SENSITIVITY` | `causal.sensitivity.v1` |

したがって、現行実装のruntimeを次のような単一Plan内のDAGとして扱わない。

```text
IDENTIFICATION -> ELIGIBILITY -> ESTIMATION -> ...
```

`IDENTIFICATION`処理から`DATA_ELIGIBILITY_RESULT`等が生成され得ることと、`ELIGIBILITY`というruntime Stageが存在することは別である。科学的な前提関係はcanonical Executionの`input_graph_version_id` / `input_result_id`等とResult lineageで表現される。

Navigation側の`Setup / Discovery / Identification / Estimation / Effects / Diagnostics / Sensitivity`はユーザーの作業・閲覧コンテキストであり、runtime StageTypeと1:1対応させない。Identification / Estimationの科学的責務分離はNavigation設計として維持するが、それを理由に既存Causal runtime planを多段化しない。

### 6.3 Predictive

現行実装のfull Predictive planは次のruntime Stageを生成する。

```text
SPLIT -> PREPARE -> TRAIN -> EVALUATE -> optional EXPLAIN
```

主なdependencyは次である。

- `split.partition_manifest -> prepare.partition_manifest`
- `prepare.training_bundle / fitted_preprocessor -> train`
- `prepare.evaluation_bundle / fitted_preprocessor`および`train.frozen_model -> evaluate`
- Explainが有効な場合はprepare/train/evaluateの必要outputをExplainへbindingする。

各runtime Stageの責務:

- SPLIT: immutable partition artifactを生成する。
- PREPARE: partition manifestを用いてtraining/evaluation bundle、fitted preprocessor、explanation向け入力を生成する。
- TRAIN: training bundleとfitted preprocessorからfrozen modelとtraining summaryを生成する。
- EVALUATE: frozen modelとevaluation bundleを用いてevaluation summaryを生成する。
- EXPLAIN: 有効なexplanation specificationに従ってexplanation summary / model card等を生成する。

Navigation側の`Setup / Train / Predict / Metrics / Explainability / Model Management`は、これらruntime stageと1:1対応させない。特にNavigation `Train`はruntime `train`単体実行を意味せず、`Metrics`は保存済みevaluation Resultのreadで成立し得る。

Predictiveの既存設定項目、default、validation、generated `predictive-analysis-spec/1` semanticsは全量保持する。

#### 6.3.1 Predictive subgroup evaluation

- evaluation populationはuntouched TEST。
- user-specified subgroup columnごとに独立sliceし、automatic intersection/discovery/fairness frameworkは追加しない。
- subgroup columnはfeatureである必要はなく、partition row identity/ordinalによりTEST rowへ対応付ける。
- nullはexplicit subgroupとして扱う。
- primary/secondary metricそれぞれに`sample_count`を必須で返す。
- uncertaintyはnonparametric percentile bootstrap、confidence=0.95、resamples=1000、deterministic seed。
- `n < 2`またはvalid resamples < 200ではCIを返さずwarningを返す。
- metricが計算不能なgroupではvalue/uncertaintyを`null`とし値を捏造しない。
- outputはgroup valueをmap keyに埋め込まずrecord listとする。

## 7. Validation Architecture

### 7.1 Generic Validation

Validation責務は、現行実装の`PlanValidator`が直接行う検証と、それ以外のapplication/domain validationを分離する。

#### 7.1.1 PlanValidatorが行う検証

`PlanValidator`は現在、次を検証する。

1. `plan_schema_version == execution-plan/1`。
2. `project_id`と`analysis_specification_id`が空でない。
3. `stage_key`が一意で、Planに少なくとも1 Stageが存在する。
4. enabled Stageの`StageType`にRunnerが登録済みである。
5. `resource_policy.timeout_seconds`が指定される場合、整数かつ1..86400以内である。
6. dependencyのsource/target Stageが存在する。
7. enabled Stageがdisabled Stageへ依存しない。
8. dependencyが参照するsource output / target input名が各contractに存在する。
9. source output schemaとtarget input schemaが一致する。
10. 同じtarget Stage inputへ複数upstream bindingを作らない。
11. topological sortが成立し、cycleがない。

`StageType.namespace/name/version`のsyntax validationは`StageType`生成時のdomain invariantであり、PlanValidatorの独立stepとして重複実装しない。

#### 7.1.2 PlanValidator外のvalidation

次は別のdomain/application boundaryで扱う。

- Project / Resource boundary・ownership
- Analysis Specification schema/lifecycle validation
- Family固有scientific validation
- supported endpointにおけるidempotency
- Dataset/Artifact size等、個別use caseのresource policy
- Navigation catalogのFamily/Stage ID、slug、order、default Stage、renderer binding整合性

Navigation catalog validationをruntime Plan dependency validationへ混入しない。

#### 7.1.3 AnalysisView typed filter validation

AnalysisView create/update/validate/fixは同じDataset logical-type compatibility validatorを利用する。

| Logical Type | Operator |
| --- | --- |
| BOOLEAN | `EQ, NE, IN, NOT_IN, IS_NULL, NOT_NULL` |
| INTEGER / REAL / DATETIME | `EQ, NE, LT, LTE, GT, GTE, IN, NOT_IN, IS_NULL, NOT_NULL` |
| TEXT | `EQ, NE, IN, NOT_IN, IS_NULL, NOT_NULL` |
| OTHER | `IS_NULL, NOT_NULL` |

`IS_NULL/NOT_NULL`はvalueなし、`IN/NOT_IN`はnon-empty list。DATETIME valueはISO-8601、REALはfinite numeric、INTEGERはbooleanを許容しない。`time_cutoff`はDATETIME + `LT/LTE`。logical type unknownをsuccess扱いしない。Mismatch codeは`FILTER_TYPE_MISMATCH`。

### 7.2 Exploratory Validation

- column typeとchart encoding
- aggregation compatibility
- empty population
- sampling disclosure
- exploratory findingをcausal claimへ変換しない

### 7.3 Causal Validation

- Graph semantics
- Causal Question completeness
- identification strategy
- adjustment set
- inferred type
- eligibility
- estimator compatibility
- post-discovery warning

### 7.4 Predictive Validation

- target existence / type
- feature availability
- target / future / group leakage
- split overlap
- preprocessing fit boundary
- metric / task compatibility
- test isolation
- existing setting/spec parity

### 7.5 Navigation Validation

- supported Familyのみ。
- Stage ID / slugはFamily内一意。
- default Stageはcatalog内に存在する。
- Family / Stage orderingはdeterministic。
- renderer binding欠落を検出する。
- Navigation descriptorにruntime input/output、status、retry semanticsを持たせない。

## 8. Result / Artifact / Lineage

### 8.1 Canonical Resultとcompatibility read model

現行のcanonical `Result` authorityは、`execution_id / result_level / stage_execution_id / result_type / scientific_status / summary / payload / diagnostics / warnings`を持つ。ProjectとAnalysis Familyは親Executionから解決する。

同時に、過去のFamily workflowを読むための`FamilyResult` compatibility read modelが残っており、こちらは`project_id / analysis_family / schema_version / analytical_status`を持つ。新規write authorityはcanonical Resultに寄せ、両者を同一entityとして扱わない。

Navigation StageをResult ownership keyとして必須化しない。

### 8.2 Artifact

Canonical Artifactは`SOURCE`または`EXECUTION_OUTPUT` scopeを持ち、`object_key / content_hash / media_type / size_bytes`でArtifactStore上のcontentを参照する。Artifact readでは保存済み`content_hash`と取得contentのSHA-256を照合する。

Predictive等のhistorical Family read modelとして`FamilyArtifact`が残るが、新規canonical Artifact ownershipと区別する。

### 8.3 Lineage

Lineageには2つの表現層がある。

1. canonical/generic authority: `LineageEdge(ResourceRef -> ResourceRef)`およびtyped structural relation。
2. Result起点read projection: Project / Dataset / Execution / Result / GraphVersion / Artifact / Annotationをtraverseし、表示用relation名へ変換する。

表示用`CONTEXT_FOR / SOURCE_OF / INPUT_TO / HAS_ARTIFACT / HAS_ANNOTATION`等と、generic authoritative relation typeを同一のwrite contractにしない。

Navigation Stageをpersistent lineage resourceとして追加しない。

Current lineage read modelは`ResearchContextVersion -> AnalysisSpecification -> ExecutionPlan -> Execution -> StageExecution -> Result -> Artifact`を最低chainとし、DatasetVersion / AnalysisView / GraphVersion / input Result / base Executionを接続する。FK/snapshotからdeterministically導出できるstructural relationをgeneric LineageEdgeへ二重persistせず、`MOTIVATED`等のsemantic relationだけをgeneric edgeとして保持する。

Exploratory ResultからAnalysisSpecification DRAFTへのhandoffは`Result --MOTIVATED--> AnalysisSpecification`を明示保存する。

## 9. Comparison Design

### 9.1 Canonical comparison query

現行`ComparisonQueryService`は2件以上のcanonical Resultを比較し、以下を要求する。

- 全Resultが同一Projectに属する。
- 全Resultの親Executionが同一`operation`である。
- 全Resultが同一`result_type`である。

比較projectionは次を返す。

- `operation`
- `common_conditions`
- `changed_conditions`
- `result_differences`
- `warnings`
- `lineage_summary`

Execution snapshot差分として、少なくとも`algorithm_or_estimator / parameter_json / random_seed / analysis_spec_json / dataset_version_id / input_graph_version_id`を比較する。

### 9.1.1 Scientific comparability gate

Comparisonは二段階で評価する。

1. `semantic_compatible`
2. `direct_metric_comparable`

Predictive semantic key:

```text
task_type
prediction target/outcome
prediction unit
prediction time
horizon
deployment/evaluation population semantics
```

Model/feature/hyperparameter/split method差分は比較対象だがsemantic keyそのものではない。Direct metric comparisonではさらに`same dataset_version_id / same TEST-row identity(hash) / same metric definition`を要求する。

Causal semantic keyは`treatment/exposure / outcome / estimand / target population`。Direct comparisonではsame data/view/analysis populationも要求する。

同一immutable `dataset_version_id`をExploratoryとconfirmatory analysisで再利用した場合はAnalysisViewが異なってもsame-dataと判定し、`EXPLORATORY_REUSE_SAME_DATA`をnon-blocking warningとして先行Exploratory Result IDとともに保持する。

semantic mismatchはHTTP-level failureにせず`compatible=false`とreasonを返し、quantitative delta/rankを生成しない。Different Family / incompatible Result Typeなどrequest shape自体が無効な場合はvalidation errorとする。

### 9.2 Project-scoped comparison

Project Closure APIにも`POST /projects/{project_id}/comparisons`が存在する。これはProject membership境界を通った比較surfaceであり、canonical Result比較の意味を変えない。

### 9.3 Cross-family summaryの将来境界

現行canonical comparisonはsame operation / same Result Typeを要求するため、異なるFamily semanticを直接同一comparisonへ入れる設計ではない。

将来Cross-family summaryを行う場合も、Predictive metricとCausal effectを単一scoreへ平坦化せず、Research Context / Dataset / Analysis View / evidence relation等を用いたpresentation summaryとして設計する。

## 10. Frontend State Design

Frontend stateは次の責務へ分離する。

- server state: API query cache
- Project route state: Project list/registerまたはProject / Project section
- Analysis route state: Project / Family / Navigation Stage / optional resource identity
- Analysis Context selection: Research Context / Dataset Version / Analysis View
- draft state: unsaved form
- authoritative resource state: backend Resource status
- async presentation state: `IDLE / LOADING / READY / EMPTY / PARTIAL / ERROR / CANCELLED`

Authority rule:

1. Analysis WorkspaceのCurrent ProjectはURL `project_id`をauthorityとしread-only。
2. Current Family / Navigation Stageはcanonical Analysis route / application navigation stateをauthorityとする。
3. Research Context / Dataset Version / Analysis Viewはcurrent Projectと整合するexisting resource/stateだけを復元する。
4. Dataset Version変更でAnalysis Viewが互換でなくなればAnalysis View selectionを解除する。
5. context selection不足だけを理由にFamily / Stage routeを書き換えない。
6. Family / Navigation StageをDB/workspace persistent stateへ昇格させない。
7. Predictive等のdraft inputをStage切替で不必要に破棄しない。
8. Button enablementはclient local stateだけで決定せず、backend validation / operation availabilityを利用する。

Backend action availabilityは最低限`{allowed, reason_code?, message?}`を返し、action visibilityとaction allowedを別conceptとして扱う。

## 11. Security Design

### 11.1 Current request identity

現行実装のWeb APIには共通Bearer/OIDC authentication middlewareは存在しない。request identityが必要なrouterでは`X-User-Id`を読み、未指定時は`anonymous`として扱う実装がある。

Request correlationは`X-Request-Id`をmiddlewareで受理し、未指定時はUUIDを生成してresponse headerへ返す。

したがってCurrent architectureでは、Navigation改修を理由に「production OIDCが既に成立している」と仮定しない。Authentication hardeningは別scopeである。

### 11.2 Project membership

Project Closure領域のProject roleは次の3値である。

- `OWNER`
- `EDITOR`
- `VIEWER`

`ProductClosureService`ではreadを`OWNER / EDITOR / VIEWER`、writeを`OWNER / EDITOR`へ許可する。Project作成時にはrequestの`X-User-Id`をownerとしてmembership登録する。

**全project-scoped route**はservice action前にProject membership authorizationを通す。routerごとの実装差異をauthorization bypassの理由にしてはならない。

Role/action matrix:

| Action | OWNER | EDITOR | VIEWER |
| --- | --- | --- | --- |
| READ | allow | allow | allow |
| WRITE / MUTATE | allow | allow | deny |
| Execution mutation | allow | allow | deny |
| Export create | allow | allow | deny |
| Membership admin | allow | deny | deny |
| Explicit sensitive output | allow | allow | deny |

独立`EXECUTE` roleは追加しない。system-level Operator authorizationは`DEFERRED` scopeである。

### 11.3 Artifact / sensitive output

Artifact downloadはcontent hashを検証して返す。Project-scoped closure downloadでは`Content-Disposition`、`Digest`、`X-Content-Type-Options: nosniff`、`Cache-Control: private, no-store`を付与する。

Prediction / local explanation等のsensitive output policyをNavigation Stage名称で緩和しない。

prediction row / local explanation row/detailはpotentially sensitive outputとして扱う。VIEWERにはaggregate/suppressed viewのみ許可し、explicit sensitive detailはOWNER/EDITORに限定する。configurable sensitive-column metadata/policyは`DEFERRED`でありcurrent mandatory designへ含めない。


### 11.4 Command Idempotency / Retry-safe Artifact Commit

Idempotency対象は「全POST/create」ではなく、retryでduplicate durable side effectを生成し得るCommandである。Scopeは`(project_id, command_scope, idempotency_key)`。

- required key missing: `IDEMPOTENCY_KEY_REQUIRED`
- same key + same canonical semantic request: stored response replay、duplicate side effectなし
- same key + different request: HTTP 409 `IDEMPOTENCY_CONFLICT`
- natural idempotency/uniquenessが成立するCommandへheaderを機械的に要求しない
- exactly-once executionは保証しない

Artifact materializationはlogical Execution/Stage/output slot/typeからdeterministic identity/object keyを導出し、same logical output + same content hashはreuse、different content hashはnondeterministic-output conflictとする。Result/Artifact bindingは可能な限りmetadata transaction内でcommitする。cross-store compensationは`DEFERRED` scopeである。


## 12. Deployment

現行実装ではFastAPI Web API、polling Worker、Product persistence DB、ArtifactStore Port（default LocalArtifactStore）が分離されている。Family / Navigation Stage導入のために別runtime execution serviceを新設しない。

## 13. Failure Model

| Failure | 扱い |
| --- | --- |
| Navigation descriptor invalid | startup/query validation error。runtime execution failureへ変換しない |
| Unknown Family / Stage route | explicit 4xx / unsupported state。silent fallbackしない |
| Renderer binding missing | presentation/configuration defectとして検出 |
| Validation rejection | Executionを作成せず4xxまたはREJECTED Command Result |
| Technical runtime stage failure | Stage FAILED、Execution FAILED、既存retry policy |
| Analytical prerequisite unmet | Result/operation availabilityとして表現。Navigation Stage存在自体とは分離 |
| Artifact read integrity failure | `ArtifactHashMismatch`として扱い、破損contentを正常として返さない |
| Client disconnect | server-side Execution継続。cancelは明示Command |

## 14. Schema / Dependency Boundary

- `analysis-specification/1`の既存`analysis_family`を再利用する。
- Navigation Stage fieldをAnalysisSpecificationへ追加しない。
- ExecutionPlan / Execution / StageExecutionへNavigation Stage fieldを追加しない。
- Product Domainはbrowser route/navigation implementationへ依存しない。
- Scientific / ML / visualization libraryはPort / Adapter背後へ隔離する。
- Capability固有Adapterはcanonical runtime lifecycleを制御しない。
- Navigation metadata/stateについてはDB migrationを行わない。
- Reproducibility contractとして`StageAttempt.effective_random_seed: int | null`を追加するDB migrationを行う。
- `Execution.runtime_version_json`へ`ariadne_code_version / python_version / platform_system / platform_release / machine / libraries`を保存する。

## 15. Test Architecture

Current design concernを次のtest layerへtraceする。

- domain invariant / typed filter / scientific guard → unit/domain test
- persistence / StageAttempt seed / concurrency / idempotency / authorization / lineage → integration test
- route/header/error/response/authorization → API contract test
- Navigation/deep link/history/async state/accessibility → frontend/browser test
- Navigation→runtime import prohibition / optional future dependency prohibition → architecture/static test
- Planner golden / Plan DAG / Runner contract / worker lifecycle → workflow regression
- CLI / library direct execution → headless regression
- Predictive existing setting/spec parity → compatibility regression
- Causal scientific benchmark / Predictive leakage/split/subgroup → scientific test
- Family横断browser E2E

`DEFERRED` concern（general AuditLog、retention、object storage、hard limits、production auth hardening、cross-store compensation等）のtest targetをcurrent mandatory acceptanceへ混ぜない。

## 20. CHANGE LOG

### 20.4 ENH-E4 Canonical Execution Architecture

canonical Product runtime Execution authority、generic workflow core、persistent StageExecution、Result / Artifact / Lineage authority等の設計を継承する。

### 20.5 ENH-E5 Family × Navigation Stage Application Architecture

Project Workspaceのanalytical navigationをFamily / Family-local Navigation Stageへ再構成する。Navigation taxonomyはPresentation / Application / Capabilityの責務として追加し、Generic Workflow Coreおよびruntime Execution Stageへ依存を逆流させない。

### 20.6 ENH-E5 Phase I Canonical Convergence

- Outbox/nonexistent Port overstatementをD1 current contractへ訂正した。
- Navigation metadata endpoint/schema/route/default Stageをfreezeした。
- typed filter、subgroup、comparability、authorization、idempotency、lineage、reproducibility、frontend accessibilityをD2 targetとして具体化した。
- `StageAttempt.effective_random_seed` migrationを明示し、D3 capabilityをE5 acceptanceから分離した。


### 20.7 Project Management / Analysis Workspace Basic Architecture

Application IAをProject ManagementとAnalysis Workspaceへ分離し、Project route、Analysis Context、resource ownership、existing Causal/Exploratory/Predictive surface placementをcurrent basic designへ統合した。API/persistence/backend execution semanticsはUI再配置だけを理由に変更しない。
