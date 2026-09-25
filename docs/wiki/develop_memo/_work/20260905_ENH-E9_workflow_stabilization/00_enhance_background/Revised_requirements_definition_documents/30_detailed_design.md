# 30 詳細設計

- 文書状態: `APPROVED`
- 文書種別: 現行詳細設計のeffective snapshot
- 上位文書: `10_requirements_definition.md`, `21_logical_data_design.md`, `22_product_basic_design.md`, `23_api_interface_design.md`
- 基準Runtime: Python 3.12
- current source照合対象: `src/ariadne/product/`, `src/ariadne/capabilities/`, frontend/router関連実装

本書はAriadneのcurrent detailed designを記述する。Enhancement履歴や過去版との差分を知らなくても、現在有効なmodule responsibility、state authority、navigation contract、runtime boundary、Family-specific presentation binding、result/lineage contractを理解できることを目的とする。

本書は単体でcurrent detailed designの主責務と主要constraintを理解できるeffective snapshotである。過去Enhancement文書、baseline commit、差分addendum、source historyをcurrent design本文の代替authorityとして参照しない。

---

## 1. 実装原則

1. DomainはFramework / ORM / external analytical object / browser navigationへ依存しない。
2. Application ServiceはUnit of WorkとPortを通じてpersistence / external capabilityを利用する。
3. Scientific / ML library objectはAdapter境界の外へ持ち出さず、persistent payloadへ直接保存しない。
4. persistent snapshotはstrict schema validation、canonical JSON、content hashを持つ。
5. Runnerはruntime Stage input/output contractを受け取り、DB transactionやbrowser stateを直接操作しない。
6. Execution lifecycle authorityは`Execution`、runtime Stage lifecycle authorityは`StageExecution`に集約する。
7. `AnalysisFamily`は`EXPLORATORY / CAUSAL / PREDICTIVE`の3値を持つdomain enumをcanonical discriminatorとする。
8. Navigation Stageはapplication/presentation metadataであり、`AnalysisSpecification`、`ExecutionPlan`、`Execution`、`StageExecution`へ保存しない。
9. Navigation taxonomyの変更だけを理由にruntime `StageType`、stage dependency、retry/lease lifecycleを変更しない。
10. CLI / Python library / backend use caseはNavigation Stageを設定せずanalysis executionを開始できる。
11. UI上のNavigation Stageとruntime Stageに1:1 cardinalityを要求しない。
12. Project ManagementとAnalysis Workspaceは別navigation scopeとし、route/state authorityを混在させない。
13. Analysis Contextは新しいpersistent aggregateや専用backend APIではなく、既存resource/selectionのapplication-level projectionとして扱う。
14. UI / IA再編だけを理由に既存API contract、persistence schema、backend analysis/domain semanticsを変更しない。
15. Family-specific scientific semanticsをpresentation都合でgeneric score/statusへ平坦化しない。
16. Project境界をauthorization、resource ownership、lineage traversalの共通boundaryとする。
17. Stage Contentsのprimary identityはcurrent canonical Navigation Stageとし、legacy workspace groupingをcurrent Stage identityとして表示しない。
18. Stage固有のmain operation/result/explanationは、その責務を持つNavigation Stageが所有する。cross-stage情報はcompactなprerequisite/referenceに限定する。
19. 主要semantic sectionは縦方向reading flowを基本とし、独立sectionの横並びを理由にpage-level horizontal scrollを要求しない。
20. Predictive feature-column編集はSetupが所有し、Dataset Version schemaをcandidate authorityとする。Train/Predictは該当feature setをread-only表示する。

---

## 2. Software responsibility boundary

### 2.1 Layer responsibility

```text
Frontend / Browser
├─ Application Router
├─ Project Management UI
└─ Analysis Workspace UI
        │
        ▼
Interface / API
├─ Project / Context / Dataset / View API
├─ Analysis Specification / Execution / Result API
├─ Navigation metadata API
└─ Operation Availability API
        │
        ▼
Application
├─ Project / Context / Dataset / View use cases
├─ Analysis workflow use cases
├─ Navigation catalog aggregator
└─ authorization / Unit of Work orchestration
        │
        ▼
Domain / Capability / Runtime
├─ Product Domain
├─ Exploratory Capability
├─ Causal Capability
├─ Predictive Capability
├─ Planner / PlanValidator
├─ Runner Registry
└─ Generic Executor
        │
        ▼
Persistence / Artifact / External scientific adapters
```

### 2.2 Navigation metadataとruntimeの境界

| Concern | Owner | Navigationを参照 | Persistent |
| --- | --- | --- | --- |
| Family / Navigation Stage catalog | Capability + application/interface aggregator | する | しない |
| Browser route / current Family / current Stage | Frontend/application navigation | する | しない |
| Analysis Context selection | Frontend/application workspace state | route/resourceを参照 | 既存selection/resourceのみ |
| AnalysisSpecification | Product Domain | しない | する |
| ExecutionPlan / StageDefinition | workflow/domain | しない | snapshotとして保持し得る |
| Execution / StageExecution | runtime/domain | しない | する |
| Result / Artifact / Lineage | product/domain | しない | する |

新しいpersistent `navigation` aggregate/table、`AnalysisContext` table、`CurrentFamily` field、`CurrentNavigationStage` fieldを作らない。

### 2.3 Runtime packageへの禁止依存

次の責務からbrowser route / Navigation descriptor / Project Management componentをimportしない。

- Execution domain
- StageExecution domain
- Execution / StageExecution repository
- planner / plan validator
- runner registry
- generic executor
- worker claim / lease persistence
- scientific runner

architecture testで依存方向を検査可能にする。

---

## 3. Canonical domain/application value objects

### 3.1 AnalysisFamily

```python
class AnalysisFamily(str, Enum):
    EXPLORATORY = "EXPLORATORY"
    CAUSAL = "CAUSAL"
    PREDICTIVE = "PREDICTIVE"
```

利用箇所:

- `AnalysisSpecification.analysis_family`
- `ExecutionPlan.analysis_family`
- `Execution.analysis_family`
- planner / capability selection
- API request/response Family discriminator
- Navigation Family identity

navigation用に別のFamily enumを定義しない。

### 3.2 Runtime StageType

runtime StageはNavigation Stageとは独立したversioned keyを持つ。

```python
@dataclass(frozen=True, order=True)
class StageType:
    namespace: str
    name: str
    version: str
```

Validation:

- `namespace` / `name`: lower snake case、先頭は英小文字。
- `version`: 1以上の整数を表す文字列。
- runtime key: `"{namespace}.{name}.v{version}"`。

Serialization example:

```json
{"namespace":"predictive","name":"train","version":"1"}
```

StageTypeはRunner Registry / ExecutionPlan / StageExecutionのruntime contractであり、UI Stage slugから自動生成しない。

### 3.3 ResourceRef

runtime/application boundaryでresourceを参照する場合、domain objectそのものではなくstable identifierを用いる。

```python
@dataclass(frozen=True)
class ResourceRef:
    resource_type: str
    resource_id: str
    project_id: str
    schema_version: str | None = None
    content_hash: str | None = None
```

Project境界を保持し、versioned/canonical resourceではschema version / content hashを補助identityとして保持できる。Navigation Stageはpersistent Resourceではないため`ResourceRef(resource_type="NavigationStage", ...)`を作らない。

### 3.4 NavigationStageDescriptor

```text
NavigationStageDescriptor
├─ stage_id
├─ slug
├─ label
└─ order
```

### 3.5 FamilyNavigationDescriptor

```text
FamilyNavigationDescriptor
├─ family: AnalysisFamily
├─ slug
├─ label
├─ default_stage_id
└─ stages[]: NavigationStageDescriptor
```

Catalog invariant:

1. Familyは3件、各Family 1件。
2. Family slugはglobalに一意。
3. Family内`stage_id`と`slug`は一意。
4. `default_stage_id`は当該Family catalog内に存在する。
5. `order`はdeterministicである。
6. catalogからruntime StageType / StageDefinitionを生成しない。

### 3.6 Frozen navigation catalog

```text
EXPLORATORY / exploratory / default=profile
  profile
  data-quality
  distribution
  relationships
  comparison
  findings

PREDICTIVE / predictive / default=setup
  setup
  train
  predict
  metrics
  explainability
  model-management

CAUSAL / causal / default=setup
  setup
  discovery
  identification
  estimation
  effects
  diagnostics
  sensitivity
```

Catalog authorityはFamily Capability descriptorであり、application/interface aggregatorがread-only metadataとして公開する。

```text
GET /api/v1/navigation/analysis
schema_version = analysis-navigation/1
```

Frontendはlabel/order/default Stageを含むfull catalogをhard-codeしてduplicate ownershipしない。

---

## 4. Application navigation state

### 4.1 Project route state

Project Managementのroute stateは次のいずれかである。

```text
Projects index
Project register
Selected Project + Project section
```

Canonical route:

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

は`/projects/{project_id}/overview`へ`replace` semanticsでnormalizeする。

### 4.2 Analysis route state

Canonical Analysis route:

```text
/projects/{project_id}/analysis/{family_slug}/{stage_slug}
```

resource deep route:

```text
/projects/{project_id}/analysis/{family_slug}/{stage_slug}/resource/{resource_type}/{resource_id}
```

Conceptual navigation context:

```text
NavigationContext
├─ project_id
├─ family: AnalysisFamily
├─ navigation_stage_id
└─ optional resource reference
```

これはroute resolution resultでありpersistent Domain Value Objectではない。

### 4.3 Project routeとAnalysis routeのauthority separation

Application Routerはpath prefixとroute grammarからProject Management / Analysis Workspaceをdispatchする。

```text
URL intent
  ↓
Application Router
  ├─ Project Route Resolver
  │    └─ Project Management Shell
  └─ Analysis Route Resolver
       └─ Analysis Workspace Shell
```

Project navigation stateをFamily/Stage stateへ変換しない。Analysis navigation stateをOverview/Data等のProject section stateへ変換しない。

### 4.4 History policy

| Transition | History behavior |
| --- | --- |
| userによるProject section遷移 | `pushState`相当 |
| userによるFamily/Stage遷移 | `pushState`相当 |
| Selected ProjectからProject Listへの明示的parent navigation | `pushState`相当 |
| `/projects/{id}` → overview normalization | `replaceState`相当 |
| supported legacy analytical entry → canonical Analysis route | `replaceState`相当 |
| initial canonical route restore | 新しいhistory entryを作らない |
| Back / Forward (`popstate`) restore | 新しいhistory entryを作らない |
| current targetと同一route | duplicate entryを作らない |

route更新とapplication state更新のauthorityを1 transition coordinatorへ集約し、個別componentが独自にhistory/stateを書き換えない。

### 4.5 Invalid route

次をsilent correctionしない。

- unknown Project section
- unknown Family slug
- unknown Stage slug
- resourceとexplicit Family/Stageのsemantic mismatch
- Project境界外resource

canonical default resolutionが許可されるのは、Familyのみが指定されStageが省略された等、contractでdefault Stage resolutionが定義されている場合に限る。

### 4.6 Selected ProjectからProject Listへのparent navigation

Selected Project shellは、`overview`, `context`, `data`, `results` の各local sectionからcanonical Project List `/projects` へ戻る明示的parent navigation actionを提供する。

```text
return action activate
  ↓
Project navigation intent
  ↓
canonical /projectsへserialize
  ↓
Project transition coordinator
  ↓
push history entry
  ↓
Projects indexをrender
```

Invariant:

- target authorityはcanonical `/projects` である。
- `history.back()` をtarget resolutionとして使用しない。
- Selected Project routeへdirect entryした場合でも同じactionが成立する。
- parent navigation後のBackは元のSelected Project route、Forwardは`/projects`を復元する。
- alternative Project List routeを追加しない。

---

## 5. Analysis Context

### 5.1 Logical structure

```text
Analysis Context
├─ Current Project
├─ Active Research Context
├─ Dataset Version
└─ Analysis View
```

### 5.2 Authority

| Element | Authority | UI mutability in Analysis Workspace |
| --- | --- | --- |
| Current Project | Analysis route `project_id` | read-only |
| Active Research Context | existing Project-scoped selection/resource | selectable |
| Dataset Version | existing Project-scoped selection/resource | selectable |
| Analysis View | selected Dataset Version compatible existing view | selectable |

Project変更はProjects / Project Management経由で行う。

### 5.3 Restore algorithm

```text
parse canonical Analysis route
  ↓
resolve Current Project from project_id
  ↓
load Project-authorized existing selections/resources
  ↓
restore Research Context only if it belongs to Current Project
  ↓
restore Dataset Version only if it belongs to Current Project
  ↓
restore Analysis View only if it belongs to Current Project
and is compatible with selected Dataset Version
  ↓
render Analysis Context
```

無効なselectionは架空defaultへ置換せず`unselected`とする。

### 5.4 Dataset Version change

```text
select new Dataset Version
  ↓
selected Analysis View exists?
  ├─ no  → keep unselected
  └─ yes
       ↓
compatible with new Dataset Version?
  ├─ yes → keep
  └─ no  → deselect Analysis View
```

このselection変更だけを理由にFamily / Navigation Stage routeを書き換えない。

### 5.5 Missing context

必要contextが不足するoperationは`unavailable`として表示する。Family/Stage navigation自体は維持する。

禁止:

- missing contextを埋める架空resource生成
- context deficiencyを理由とするautomatic Family/Stage rewrite
- Analysis Context専用persistent recordの作成
- Analysis Context専用backend APIの新設

---

## 6. Schema registry / canonicalization

### 6.1 SchemaRegistry

Generic scientific/product payload schemaはversion stringをkeyとしてvalidatorを登録する。

```python
class SchemaRegistry:
    def register(self, schema_version, validator): ...
    def validate(self, schema_version, payload): ...
    def canonicalize(self, schema_version, payload) -> bytes: ...
    def hash(self, schema_version, payload) -> str: ...
```

Invariant:

- empty / duplicate schema version registrationを拒否する。
- unknown versionはunsupported version errorとする。
- payloadはMappingを要求する。
- canonicalization前にschema validationする。

Navigation metadata `analysis-navigation/1`はpresentation/application metadata contractであり、scientific generic SchemaRegistryへ登録しない。

### 6.2 Canonical JSON

canonicalizationは少なくとも次を満たす。

- dataclassはfield mappingへ変換する。
- Enumは`.value`へ変換する。
- UUID / datetimeはstable stringへ変換する。
- non-finite floatを拒否する。
- mapping keyはstringのみ。
- mapping key orderに依存しないcanonical serializationを行う。
- semantic payloadに含まれないbrowser navigation stateをhash inputへ混入しない。

### 6.3 Reproducibility metadata

Execution/Resultのreproducibility metadataには、実際に利用したlibrary version、input snapshot identifier、analysis specification/version、effective random seed等を必要に応じて記録する。

browser Navigation Stageはscientific reproducibility inputではない。

---

## 7. Research Context detailed contract

Research ContextはProject-scoped、versioned、immutable/fixed snapshotとして扱う。

主な責務:

- research question / hypothesis / assumptions等の分析文脈
- version history
- current active selection
- downstream AnalysisSpecification / Result lineageへの参照

Analysis Workspaceではexisting Research Contextをselectする。create/revise/history管理はProject Management / Research Context surfaceが担う。

Navigation Stage切替でResearch Context selectionを失わせない。

---

## 8. Analysis View detailed contract

### 8.1 Persistent contract

Analysis ViewはDataset Versionから派生するversioned logical viewである。

```text
AnalysisView
├─ analysis_view_id
├─ project_id
├─ source_dataset_version_id
├─ view_key
├─ version_number
├─ name
├─ status: DRAFT | FIXED
├─ schema_version: analysis-view/1
├─ spec_json
├─ content_hash
├─ manifest_json
├─ created_by / created_at
└─ fixed_at
```

logical specは少なくとも次のconcernを持ち得る。

```text
source_dataset_version_id
row_filter
selected_columns
derived_columns
missing_value_policy
time_cutoff
sampling
```

### 8.2 Ownership

- create/edit/version/fix/delete等のlifecycle ownership: Project Management / Data
- current input selection: Analysis Context
- execution input: existing fixed/supported Analysis View reference

Analysis ViewをExploratory専用resourceとして扱わない。

### 8.3 Filter validation contract

`row_filter` validationはsource `DatasetVersion`のlogical column typeをresolveし、create/update/validate/fixで同一ruleを適用する。

| logical type | allowed operators | value contract |
| --- | --- | --- |
| BOOLEAN | EQ, NE, IN, NOT_IN, IS_NULL, NOT_NULL | bool |
| INTEGER | EQ, NE, LT, LTE, GT, GTE, IN, NOT_IN, IS_NULL, NOT_NULL | boolを除くinteger |
| REAL | EQ, NE, LT, LTE, GT, GTE, IN, NOT_IN, IS_NULL, NOT_NULL | finite int/float、bool除外 |
| DATETIME | EQ, NE, LT, LTE, GT, GTE, IN, NOT_IN, IS_NULL, NOT_NULL | ISO-8601 string |
| TEXT | EQ, NE, IN, NOT_IN, IS_NULL, NOT_NULL | string |
| OTHER | IS_NULL, NOT_NULL | valueなし |

Invariant:

- `IS_NULL / NOT_NULL`はvalueを受け取らない。
- `IN / NOT_IN`はnon-empty list。
- `TEXT`へlexical LT/LTE/GT/GTEを許可しない。
- `time_cutoff`はDATETIME column + `LT / LTE`。
- source logical typeを決定できない場合はvalidation successにしない。
- type/operator/value incompatibilityはstable code `FILTER_TYPE_MISMATCH`。
- current operator taxonomy自体は変更しない。
- このvalidationは`analysis-view/1` persistent schemaを変更しない。

---

## 9. Planning / validation / Runner Registry

### 9.1 AnalysisSpecification to ExecutionPlan

Generic planner port:

```python
@dataclass(frozen=True)
class PlanningContext:
    specification: AnalysisSpecification
    resource_metadata: dict[str, Any]
    policy: dict[str, Any]

class AnalysisPlanner(Protocol):
    family: AnalysisFamily
    spec_versions: frozenset[str]
    planner_id: str
    planner_version: str
    def build_plan(self, context: PlanningContext) -> ExecutionPlan: ...
```

`AnalysisSpecification.analysis_family`をplanner selectionのcanonical discriminatorとする。`policy`はplanner-level policy inputでありNavigation route stateの格納先にしない。

Family-specific planning:

- Exploratory: `exploratory-analysis-spec/1`のoperationを1 runtime Stage planへ変換する。
- Causal: `causal-analysis-spec/2`と、必要なcanonical Execution snapshot等のresource metadataからcompatibility planを構築する。
- Predictive: `predictive-analysis-spec/1`を用い、use caseに応じてsplit-only planまたはfull planを構築する。

Navigation Stageをplanner inputの必須fieldにしない。browser active tabからFamilyを推測してPlanを生成しない。

### 9.2 PlanValidator

`PlanValidator.validate(plan)`は次をgenericに検証する。

1. `plan_schema_version == execution-plan/1`。
2. `project_id`と`analysis_specification_id`が空でない。
3. `stage_key`が一意。
4. Planに1 Stage以上存在する。
5. enabled Stageの`StageRunnerRegistry.contains(stage.stage_type)`がtrue。
6. `resource_policy.timeout_seconds`が指定される場合、boolではないint、1以上、configured maximum以下。
7. dependency source/target StageがPlan内に存在する。
8. enabled Stageがdisabled Stageへ依存しない。
9. `source_output`がsource Stage output contractに存在する。
10. `target_input`がtarget Stage input contractに存在する。
11. source output schemaとtarget input schemaが一致する。
12. 同じ`(target_stage_key, target_input)`へ複数upstream bindingを定義しない。
13. dependency graphがacyclicでtopological sort可能。

返値はdeterministic topological stage orderとする。Family-specific scientific policy、Project boundary、AnalysisSpecification lifecycle、Navigation catalogのID/slug/default/renderer整合性はPlanValidatorへ混在させない。

検証対象外:

- Navigation Stage order/default
- sidebar visibility
- current browser route
- Project Management section

### 9.3 Runner Registry

Runner Registryのkeyはruntime `StageType`である。

```text
register(runner)
resolve(stage_type)
contains(stage_type)
capability_fingerprint
```

同じStageTypeのduplicate registrationを拒否する。unknown StageTypeはregistered runnerなしとして失敗させる。

Navigation Stage IDをRunner Registry keyにしない。

### 9.4 Navigation CatalogとRunner Registry

```text
Family Capability
├─ runtime runner/provider
└─ navigation descriptor/provider
```

同じCapabilityが両方を所有してよいが、両者は別contractである。

- navigation catalogからruntime Stageを生成しない。
- runtime registryからnavigation sidebarを推測しない。

---

## 10. Generic Executor / Worker

### 10.1 Execution / StageExecution persistent contract

`Execution`主要field:

```text
execution_id
project_id
analysis_family
dataset_version_id
input_graph_version_id
input_result_id
batch_key
operation
objective_snapshot
rationale_snapshot
analysis_spec_json
algorithm_or_estimator
parameter_json
random_seed
code_version
runtime_version_json
snapshot_hash
snapshot_schema_version
status
retry_count
last_error_summary
requested_by / requested_at
started_at / finished_at
base_execution_id
revision_kind
change_reason
lease_owner
lease_expires_at
```

Execution status:

```text
QUEUED -> RUNNING -> SUCCEEDED
             └----> FAILED -> QUEUED (retry)
QUEUED/RUNNING -> CANCELLED
```

`StageExecution`主要field:

```text
stage_execution_id
execution_id
stage_key
stage_type: StageType
ordinal
dependencies
status
input_binding
output_binding
attempts[]
last_error
started_at
finished_at
```

StageExecution status transition:

```text
PENDING -> READY -> RUNNING -> SUCCEEDED
                     └------> FAILED -> PENDING/ RUNNING (retry lifecycle)
PENDING/READY -> SKIPPED_DUE_TO_PREREQUISITE
PENDING/READY/RUNNING -> CANCELLED
```

`StageAttempt`はappend-only attempt metadataとして少なくとも`attempt_number / worker_id / stage_attempt_id / effective_random_seed / started_at / finished_at / error`を保持する。stochastic Stageのtechnical retryでは同一logical Stage seedを再利用する。

### 10.2 Execution sequence

```text
worker claims canonical Execution lease
  ↓
application/family workflow resolves Execution Plan and required snapshots
  ↓
GenericExecutor validates plan structure / runner availability
  ↓
materialize/list StageExecution
  ↓
resolve READY runtime Stage
  ↓
create append-only StageAttempt
  ↓
runner.validate(context)
  ↓
runner.run(context)
  ↓
validate output binding / Result / Artifact
  ↓
persist stage outcome under current Execution lease owner
  ↓
repeat until terminal
  ↓
complete Execution when all StageExecution are terminal-success compatible
```

### 10.3 Retry / lease

- lease ownerだけがcurrent execution stateを更新する。
- technical retryはappend-only StageAttemptとして記録する。
- stochastic Stageのtechnical retryでは同じeffective random seedを再利用する。
- retry/lease semanticsにbrowser navigationを関与させない。

### 10.4 Navigation dependency prohibition

Executor/Workerは次を知らない。

- current Project Management section
- current Family tab presentation state
- current Navigation Stage
- browser history position
- sidebar order/default Stage

Allowed cardinality:

- Navigation context 1 : Execution 0
- Navigation context 1 : Execution N
- Execution 1 : Navigation consumer N

UI上の1 Stageから複数Executionを開始してよく、1 Executionを複数Stage surfaceから参照してよい。

---

## 11. Project Management detailed design

### 11.1 Component responsibility

```text
Project Management Shell
├─ Project Header
├─ Project Parent Navigation
├─ Project Local Navigation
├─ Overview Surface
├─ Research Context Surface
├─ Data Surface
└─ Results / Lineage Surface
```

### 11.2 Projects Surface

`/projects`:

- Project一覧
- Project選択
- New Projectへの導線

`/projects/new`:

- Project register/create
- create成功後はcanonical selected Project routeへ遷移

### 11.3 Overview

ownership:

- Project identity
- Project metadata
- Project status
- archive lifecycle/action
- Project-level summary

Dataset / Analysis View create/edit lifecycleをOverviewへ置かない。

### 11.4 Research Context

ownership:

- Research Context create/revise
- active context selection where allowed
- version/history
- Project-scoped context inspection

### 11.5 Data

ownership:

- Dataset
- Dataset Version
- schema / preview
- Analysis View create/edit/version/fix lifecycle

Analysis View lifecycle authorityをAnalysis WorkspaceのStage componentへ重複させない。

### 11.6 Results / Lineage

ownership:

- persisted cross-analysis Result aggregation
- comparison
- Artifact browsing/export
- Lineage inspection
- Annotation

Stage-local execution/result presentationはAnalysis Workspaceに残す。

### 11.7 Project Parent Navigation

Selected Projectの各local sectionは、Project Listへの明示的parent actionを共通shellに持つ。

UI contract:

- accessible nameは`Project List` / `プロジェクト一覧へ戻る`等、遷移先が明確であること。
- actionはOverview / Research Context / Data / Results / Lineageのどのlocal surfaceでも利用できること。
- targetは常にcanonical `/projects`。
- browser history originに依存しないこと。
- keyboard activation可能であること。

---

## 12. Analysis Workspace detailed design

### 12.1 Component responsibility

```text
Analysis Workspace Shell
├─ Analysis Context
├─ Family Tabs
├─ Family Stage Sidebar
└─ Stage Contents
```

### 12.2 Family Tabs

- Catalog `families[].order`で表示する。
- current Familyをroute stateからderiveする。
- Family切替時、target Family catalogの`default_stage_id`を解決する。
- Research Context / Dataset Version / Analysis View selectionを不必要に初期化しない。
- Full Family catalogをfrontend constantとしてduplicate ownershipしない。

### 12.3 Family Stage Sidebar

- selected Family catalogのStageだけ表示する。
- `stages[].order`で表示する。
- current Stageをroute stateからderiveする。
- Stage clickはcanonical Analysis route transitionを発生させる。
- Stage orderをruntime dependency/progressionとして解釈しない。
- visual groupingを使用する場合、group labelはnon-interactive / non-routableで、selected Stage stateを持たない。

Causalでvisual groupingを使う場合の代表配置:

```text
分析設計
  Setup
因果構造
  Discovery
識別
  Identification
推定・評価
  Estimation
  Effects
  Diagnostics
  Sensitivity
```

このgroupingはpresentation-onlyであり、route、stage slug、Navigation Stage、runtime StageType、persistent stateを追加しない。

### 12.4 Stage Contents

Stage Contentsは`(family, navigation_stage_id)`からpresentation surfaceへbindingする。

```text
(family, stage)
  ↓
Stage Surface Resolver
  ↓
StagePresentation + existing use cases / operation availability / results
```

Stage Surface Resolverは新しいscientific execution semanticsを所有しない。

current Stageのprimary heading / descriptionはcurrent canonical Navigation Stageを示す。legacy workspace grouping（例: `Inference`）をcurrent Stageのprimary identityとして表示しない。

main operation/result/explanation surfaceはowning Stageに限定する。他Stageの情報が必要な場合は、compactなprerequisite、summary、link、read-only referenceとして提示する。

### 12.5 Availability

Stage surfaceはoperation availabilityをreadしてcontrol enablementを決めてよいが、availabilityはcommand validationの代替ではない。

```text
availability projection = UX pre-check
actual command validation = authoritative enforcement
```

projectionとcommandが不一致の場合はcommand denyを優先し、projection defectとして修正する。

### 12.6 StagePresentation

frontend presentation metadataは少なくとも次を表現できる。

```text
StagePresentation
├─ title
├─ 日本語の目的説明
├─ optional resource / operation guidance
└─ optional presentation-only group label
```

Presentation metadataはresolved canonical Stageをdecorateする。Stage identity/slug/order/defaultのauthorityにならない。

### 12.7 Stage layout / overflow

Stage Contentsのtop-level semantic sectionは縦方向に積む。

許可:

- compactで密接に関連するcontrolのlocal grid/flex
- wide table/chart/preformatted resultのcomponent-local horizontal overflow
- dialog内部のscrollable option list

禁止:

- 独立semantic sectionをmandatory horizontal rowへ連結し、page-level horizontal scrollを要求する構成
- hidden Stage surfaceをvisual concealmentだけで残し、focus/interaction可能にすること

### 12.8 Stage state preservation

Navigation Stage切替はpresentation visibilityの変更であり、同一analysis draft/specificationのvalid inputを無条件にresetしない。

Stage child componentのunmountだけで唯一のDRAFT stateを失う構造を避け、route-independent parent/application form state等へauthorityを一意化する。

---

## 13. Exploratory Capability / Stage Contents

### 13.1 Mapping

| Navigation Stage | Current operation / resource | Detailed placement |
| --- | --- | --- |
| Profile | `PROFILE` | profile execution/control/result |
| Data Quality | dedicated operationなし | `PROFILE` resultのread-only projection |
| Distribution | `DISTRIBUTION` | distribution control/result |
| Relationships | `ASSOCIATION` | association control/result |
| Comparison | `GROUP_SUMMARY`, `TIME_TREND` | comparison/grouping controls/results |
| Findings | `CHART`, saved Exploratory Results | chart control/result/artifact + saved results |

### 13.2 Profile

ProfileはDataset/Analysis Viewのdescriptive profileを生成・表示する。

Profile resultはData Quality Stageからもread-only参照され得る。

### 13.3 Data Quality

Data Quality専用backend operationを作らない。

```text
PROFILE result found
  → render read-only data-quality availability/summary

PROFILE result absent
  → NO_PROFILE_RESULT
  → Profileへの導線
  → Execution/resource/backend stateを新規作成しない
```

`DATA_QUALITY` runtime operation、Result Type、persistent stateを追加しない。

### 13.4 Distribution

`DISTRIBUTION` operation/resultを配置する。Navigation Stage名を理由にruntime StageTypeを増設しない。

### 13.5 Relationships

`ASSOCIATION` operation/resultを配置する。

### 13.6 Comparison

`GROUP_SUMMARY`と`TIME_TREND`を同一Navigation Stageへ配置できる。

`TIME_TREND`はcurrent grouping/aggregation semanticsを維持する。

禁止:

- 新しい時系列モデルの導入
- UI Stage都合だけのtime type validation追加
- time orderingをscientific model semanticsとして暗黙導入

### 13.7 Findings

`CHART`はpersistent operationであり、表示専用mechanismへ置換しない。

- `CHART_RESULT`
- `CHART_SPECIFICATION`等のartifact/specification
- saved Exploratory Results

をcurrent contractに従って扱う。

---

## 14. Causal Capability / Stage Contents

### 14.1 Runtime discriminator / mapping

Causal family spec schema versionは`causal-analysis-spec/2`。runtime operationは次のdiscriminatorを使用する。

```text
DISCOVERY
IDENTIFICATION
ESTIMATION
REFUTATION
SENSITIVITY
```

Representative mapping:

| ExecutionOperation | stage_key | StageType |
| --- | --- | --- |
| `DISCOVERY` | `discovery` | `causal.discovery.v1` |
| `IDENTIFICATION` | `identification` | `causal.identification.v1` |
| `ESTIMATION` | `estimation` | `causal.estimation.v2` |
| `REFUTATION` | `refutation` | `causal.refutation.v1` |
| `SENSITIVITY` | `sensitivity` | `causal.sensitivity.v1` |

runtime input matrix:

| ExecutionOperation | input_graph_version_id | input_result_id |
| --- | ---: | ---: |
| DISCOVERY | なし | なし |
| IDENTIFICATION | 必須 | なし |
| ESTIMATION | 必須 | 必須 |
| REFUTATION | 必須 | 必須 |
| SENSITIVITY | 必須 | 必須 |

`Effects` / `Diagnostics`等のNavigation Stageはsaved Result readで成立し得るため、同名ExecutionOperation/StageTypeを追加しない。

### 14.2 Setup

primary responsibility:

- causal question / design preparation
- direct graph registration where supported
- Research Context / Dataset / Analysis View確認

Identification/Estimation/Sensitivityのmain operationをSetupへ複製しない。

### 14.3 Discovery

primary responsibility:

- discovery specification
- PC / GES等のcurrent discovery operation
- graph candidate
- candidate comparison/edit/adopt/fix
- confounder / mediator / collider / temporal ordering / domain assumption検討

Discoveryのnavigation placementはruntime graph/discovery semanticsを変更しない。

### 14.4 Identification

目的は、causal question / estimandについて識別可能性とdata eligibilityを明示することである。

primary surface:

- Dataset / Analysis View / FIXED Graph prerequisite
- estimand / causal question
- identification strategy
- adjustment set
- exchangeability
- positivity
- consistency
- IV / parallel trends等のstrategy-specific assumption
- Identification execution/result
- Data Eligibility / Estimation gate
- identified / not identified / partially identified等のstatus
- warning/failure reason

estimator tuning、Refutation、Sensitivity controlをIdentificationのmain surfaceへ置かない。

### 14.5 Estimation

目的は、identified estimandを有限標本データから推定することである。

primary surface:

- selected Identification Resultのcompact prerequisite/reference
- estimator selection
- nuisance model configuration
- bootstrap / uncertainty configuration
- revision / override where supported
- execution submission/status
- estimation result linkage

Identification assumptionをestimator parameterへ埋没させない。Identification/Data Eligibilityの全文説明をEstimationのpage purposeとして再掲しない。

### 14.6 Effects

目的は、保存済みTreatment Effect Resultを読み、effect量とuncertaintyを解釈・比較することである。

primary surface:

- `TREATMENT_EFFECT_RESULT`
- ATE / ATT / CATE等、result schemaが持つeffect payload
- uncertainty / interval
- subgroup / heterogeneity projection
- supported comparison/reference

Diagnosticsと同一primary card/headingを共有しない。

### 14.7 Diagnostics

目的は、推定の支持条件・安定性・diagnostic warningを確認することである。

primary surface:

- `DIAGNOSTICS_RESULT`
- balance
- overlap
- effective sample size
- weight diagnostics
- scientific warning

Effects Resultをprerequisite/referenceとして参照してよいが、Effect comparisonをDiagnosticsのpage purposeにしない。

### 14.8 Sensitivity

目的は、推定結果が仮定・仕様変更に対してどの程度頑健かを確認することである。

primary surface:

- target Treatment Effect Result reference
- `REFUTATION_RESULT`
- `SENSITIVITY_RESULT`
- Refutation control/result
- Sensitivity control/result
- alternate assumption/specification依存性
- robustness interpretation

Refutation/Sensitivity operation controlはSensitivity Stageのみが所有する。Identification / Estimation / Effects / Diagnosticsではこれらをeditable controlとして表示しない。

### 14.9 Causal visibility matrix

| Surface | identification | estimation | effects | diagnostics | sensitivity |
| --- | ---: | ---: | ---: | ---: | ---: |
| Identification purpose/input/action | ON | OFF | OFF | OFF | OFF |
| Identification / Eligibility / Gate result | ON | compact prerequisite/reference | OFF | OFF | OFF |
| Estimation config/action | OFF | ON | OFF | OFF | OFF |
| Treatment effect primary result/comparison | OFF | compact completion/reference | ON | optional reference | prerequisite reference |
| Diagnostics result/warnings | OFF | OFF | OFF | ON | optional prerequisite/reference |
| Refutation controls/results | OFF | OFF | OFF | OFF | ON |
| Sensitivity controls/results | OFF | OFF | OFF | OFF | ON |

### 14.10 Causal presentation guidance

Causal Stageのprimary purpose summaryは日本語を基本とする。ATE、ATT、CATE、estimand、overlap、ESS等、実装・分析概念との対応上英語が明確な専門語は英語を維持してよい。

説明文から、少なくとも次を理解できること。

- このStageで何を判断・閲覧するか
- 前後Stageと何が異なるか
- current operationがscientific executionかsaved Result readか

---

## 15. Predictive Capability / Stage Contents

Predictive family schema versionは`predictive-analysis-spec/1`。

Top-level fields:

```text
schema_version
task_type
prediction_question
feature_spec
split_spec
preprocessing_spec
model_spec
tuning_spec
evaluation_spec
explanation_spec
```

Task typeは`BINARY_CLASSIFICATION / REGRESSION`。Split strategyは`RANDOM / STRATIFIED / GROUP / TIME_BASED`。

Key validation:

- targetをfeatureに含めない。
- feature availabilityは`feature_columns`全件をcoverする。
- prediction timeより後のfeatureを拒否する。
- split ratioは正数かつ合計1（TIME_BASEDを除く）。
- `GROUP`は`group_column`必須。
- `TIME_BASED`は`time_column / train_cutoff / validation_cutoff`必須でcutoff順序を保証する。
- stratified splitはbinary classificationに限定する。
- preprocessing fit partitionは`TRAIN`のみ。
- tuning selectionに`TEST`を使わない。

backend lifecycle:

```text
Prediction Task
  → Split
  → Training
  → Evaluation
  → Explanation
  → Model Card
```

Navigation presentation:

```text
Setup
Train
Predict
Metrics
Explainability
Model Management
```

両者を1:1 runtime Stage modelとして一致させない。

### 15.1 Setup

目的はprediction taskとanalysis specificationを定義することである。

primary surface:

- Analysis Context / selected Dataset Version / Analysis View
- task type
- prediction question
- target
- feature set
- prediction time / horizon where applicable
- split/specification-level configuration
- specification validation

feature-column editingはSetupのみが所有する。

### 15.2 Predictive feature-column selector

feature selectionのcandidate authorityはcurrently selected Dataset Versionのschemaである。

primary interaction:

```text
selected Dataset Version
  ↓
Dataset schema columns
  ↓
Feature selector dialog
  ├─ checkbox pending selection
  ├─ Confirm
  └─ Cancel
  ↓
feature_spec.feature_columns
```

Detailed contract:

1. primary editing interactionをcomma-delimited free textにしない。
2. Dataset Version/schemaがない場合、selector unavailableを明示し、架空column optionを生成しない。
3. dialog open時にcurrent confirmed feature selectionをchecked stateとして復元する。
4. checkbox toggleはpending stateのみを変更し、Confirm前にconfirmed draftを変更しない。
5. `Cancel`はconfirmed feature selectionを変更しない。
6. `Confirm`はchecked featureをdeterministic Dataset schema orderでcommitする。
7. committed valueは`predictive-analysis-spec/1 -> feature_spec.feature_columns`を生成する同一draft/form authorityへ反映する。
8. free-text入力とcheckboxを同時に競合editable authorityとして保持しない。
9. Dataset Version変更時、新schemaに存在しないselected columnをsilentに保持しない。全clearまたはvalid intersection保持を許可するが、破壊的reconcileは利用者へ示す。
10. target / excluded column、feature availability、split、leakage、task validationは上記current Predictive validationをauthorityとし、selector独自のscientific ruleを追加しない。
11. selector実現だけを理由にnew Dataset schema APIやnew Predictive specification versionを追加しない。

Accessibility:

- selector triggerにaccessible nameがある。
- dialogにaccessible nameがある。
- checkboxにlabelがある。
- keyboardでopen / Confirm / Cancelできる。
- closed/hidden dialog contentをfocus可能にしない。
- close後にfocusをinvoking controlへ戻す。

Causal Discovery等のschema-backed column selectorとimplementation helperを共通化してよいが、そのFamily固有のrequest validationやscientific semanticsを変更しない。

### 15.3 Train

目的はfixed/draft Predictive specificationに基づいてmodel trainingを実行・確認することである。

primary surface:

- selected draft/specification feature setのread-only context
- preprocessing configuration
- model configuration
- tuning configuration
- training execution/status
- fitted model/preprocessor artifact
- Training Result reference

Trainではfeature setをeditableにしない。feature setを変更する場合はSetupへ戻ってspecificationを改訂する。

### 15.4 Predict

目的はcurrent prediction/inference outputとそのprovenanceを確認することである。

- relevant saved execution specificationに記録されたfeature setをread-only表示する。
- prediction output/result/artifactを表示する。
- current unrelated draftのfeature setで既存execution結果を上書きして見せない。
- Navigation Stage名だけを理由にstandalone scoring engine/new runtime execution modelを作らない。
- feature selectorをeditable controlとして提供しない。

### 15.5 Metrics

目的はEvaluation Resultからpredictive performanceを評価することである。

primary surface:

- evaluation result
- primary/secondary metrics
- subgroup/error analysis where supported
- evaluation provenance/reference

Trainのconfig/execution UIをpage purposeとして複製しない。

### 15.6 Explainability

目的はPredictive Explanationを確認することである。

primary surface:

- `PREDICTIVE_EXPLANATION_RESULT`
- predictive explanation artifact
- relevant Model Card reference
- feature/model provenance

Predictive Explanationをcausal effect / causal explanationとして表現しない。Navigation requirementだけを理由に特定external explanation libraryを必須化しない。

### 15.7 Model Management

read-oriented model surfaceとしてResult / Artifact / Lineageを使用する。

対象:

- `TRAINING_RESULT`
- `EVALUATION_RESULT`
- `MODEL_CARD_RESULT`
- fitted preprocessor/model artifact
- Model Card artifact
- revised/rerun lineage

UI名だけを理由に別`ModelRegistry` persistent aggregateを追加しない。

### 15.8 Draft state preservation

Navigation Stage切替時に未保存DRAFT inputを意図せず初期化しない。

state authorityはroute-independent parent/application form store等へ一意化し、Stage child unmountだけで唯一のDRAFT stateを失う構造を避ける。

valid confirmed feature selectionも同じdraft-state contractで保持する。

---

## 16. Result Type / Scientific Status

### 16.1 Result Type

Exploratory:

```text
DATA_PROFILE_RESULT
DISTRIBUTION_RESULT
ASSOCIATION_RESULT
GROUP_SUMMARY_RESULT
CHART_RESULT
```

Predictive:

```text
SPLIT_RESULT
TRAINING_RESULT
EVALUATION_RESULT
ERROR_ANALYSIS_RESULT
PREDICTIVE_EXPLANATION_RESULT
MODEL_CARD_RESULT
```

Causal:

```text
DISCOVERY_GRAPH_RESULT
IDENTIFICATION_RESULT
DATA_ELIGIBILITY_RESULT
TREATMENT_EFFECT_RESULT
DIAGNOSTICS_RESULT
REFUTATION_RESULT
SENSITIVITY_RESULT
```

Navigation Stage名をResult Typeへ自動変換しない。

### 16.2 Scientific status

status vocabularyはresult type/schemaに応じて意味を保持する。例:

```text
GENERATED
GENERATED_WITH_WARNINGS
UNRELIABLE
IDENTIFIED
NOT_IDENTIFIED
PARTIALLY_IDENTIFIED
REQUIRES_REVIEW
PASS
WARN
FAIL
ESTIMATED
INSUFFICIENT_OVERLAP
INSUFFICIENT_SAMPLE
ESTIMATION_UNRELIABLE
NO_FAILURE_DETECTED
FAILURE_DETECTED
INCONCLUSIVE
ROBUST
FRAGILE
TRAINED
TRAINED_WITH_WARNINGS
EVALUATED
INSUFFICIENT_TEST_SAMPLE
NOT_APPLICABLE
```

Family-specific statusをgeneric success/failureへ平坦化しない。

---

## 17. Comparison / Lineage

### 17.1 Result comparison

comparisonは二段階gateとする。

```text
same Family / same Result Type
        ↓
semantic_compatible
        ↓
direct_metric_comparable
```

異なるFamilyまたはResult Typeをgeneric direct comparisonへ投入しない。同一Family/Result Typeでもsemantic key不一致ならrequest自体を失敗させず、`semantic_compatible=false / direct_metric_comparable=false / reasons[]`を返しquantitative delta/rankを生成しない。

Predictive semantic keyにはtask type、prediction target/outcome、prediction unit、prediction time、horizon、population semanticsを含む。direct metric comparisonには同一Dataset Version、同一TEST-row identity/hash、同一metric definitionを要求する。

Causal semantic keyにはtreatment/exposure、outcome、estimand、target populationを含む。direct quantitative comparisonには同じdataset/view/analysis populationを要求する。

「画面上に並べられる」と「scientifically direct-comparable」を同一視しない。

### 17.2 Cross-family comparison

Exploratory statistic、Predictive metric、Causal effectは同じ数値fieldへflattenしない。

cross-family surfaceでは、共通metadata/lineageとFamily-specific payloadを分離して表示する。

### 17.3 Lineage

lineageはProject境界を越えない。

代表的typed structural relation:

```text
Execution --GENERATED--> Result
Result --GENERATED--> Artifact
DatasetVersion --USED_INPUT--> Execution
AnalysisView --USED_INPUT--> Execution
Result --USED_INPUT--> Execution
Result --DERIVED_FROM--> GraphVersion
Artifact --DERIVED_FROM--> DatasetVersion
Execution --DERIVED_FROM--> Execution
Execution --REVISED_FROM--> Execution
```

Generic relationには`Artifact --DERIVED_FROM--> Artifact`、`Result --SUMMARIZES--> Result/Artifact`、`Result --MOTIVATED--> Execution/AnalysisSpecification`等を許可し得る。unknown tupleはclosed-by-defaultでrejectし、typed structural tupleをgeneric LineageEdgeとして二重writeしない。

Navigation Stageをpersistent Lineage node/edgeへ追加しない。どのStageからResultを表示するかはFamily / Result Type / presentation bindingからderiveする。

---

## 18. Frontend / Routing detailed design

### 18.1 Root component responsibility

```text
ApplicationRoot
├─ ApplicationRouter
├─ ProjectsSurface
│  ├─ ProjectList
│  └─ ProjectRegister
├─ ProjectManagementShell
│  ├─ ProjectHeader
│  ├─ ProjectParentNavigation
│  ├─ ProjectLocalNavigation
│  └─ ProjectSectionSurface
│     ├─ Overview
│     ├─ ResearchContext
│     ├─ Data
│     └─ ResultsLineage
└─ AnalysisWorkspaceShell
   ├─ AnalysisContextPanel
   ├─ FamilyTabs
   ├─ FamilyStageSidebar
   └─ StageContents
```

名称はresponsibility roleであり、具体実装のcomponent名を不必要に固定しない。

### 18.2 Navigation catalog loading

Frontend catalog authority:

```text
GET /api/v1/navigation/analysis
response schema = analysis-navigation/1
```

Normalized in-memory model:

```typescript
type AnalysisNavigationCatalog = {
  schemaVersion: "analysis-navigation/1";
  families: FamilyNavigationDescriptor[];
};
```

Catalog load state:

```text
IDLE → LOADING → READY
              ├→ ERROR
              └→ EMPTY/INVALID = contract error
```

invalid catalog時にhard-coded fallback catalogをsilent採用しない。

### 18.3 Analysis transition coordinator

Analysis navigation transitionは単一authorityで次を順序化する。

```text
entry intent / parsed URL
  ↓
resolve + validate NavigationContext from catalog
  ↓
validate project/resource route context
  ↓
commit current navigation state
  ↓
apply history policy
  ↓
render FamilyTabs / StageSidebar / StageContents
  ↓
load operation availability / resource data
  ↓
focus / error presentation
```

FamilyTabs、StageSidebar、StageContentsが独立にhistoryを書き換えない。

### 18.4 Project transition coordinator

Project Management側はProject routeだけを扱う。

```text
project navigation intent
  ↓
resolve route + authorization
  ↓
normalize short route if needed
  ↓
commit Project section / Projects index state
  ↓
apply history policy
  ↓
render ProjectsSurface / ProjectManagementShell
```

Selected ProjectからProject Listへのparent actionもこのcoordinatorを利用する。

Analysis Family/StageをProject section transitionへ暗黙付与しない。

### 18.5 Direct link / reload / Back / Forward

Project routeとAnalysis routeの双方で次を保証する。

- direct link
- reload
- Back
- Forward
- same-target duplicate history suppression
- normalizationのreplace behavior
- Selected Project direct entryからのProject List parent navigation

### 18.6 Legacy analytical entry

supported legacy analytical entryはcanonical Analysis routeへ一方向normalizeする。

legacy path/stateを第二のnavigation authorityとして維持しない。旧route tokenの具体形そのものはcurrent public contractとして固定しない。

### 18.7 Project switching

Analysis Workspace内のCurrent Projectはread-onlyである。

Project switch controlをAnalysis Contextへ持たせない。別Projectへ移動する場合はProjects / Project Managementへ遷移してProjectを選択する。

### 18.8 Async presentation state

共通presentation vocabulary:

```text
IDLE
LOADING
READY
EMPTY
PARTIAL
ERROR
CANCELLED
```

scientific statusとHTTP/loading statusを同一enumへ統合しない。

### 18.9 Accessibility

- active Family / Stage / Project sectionをsemantically表現する。
- current Stage headingをreal headingとして公開する。
- presentation-only sidebar group labelはnon-interactiveとし、active/selected route semanticsを持たせない。
- Project List parent navigation、Stage navigation、selector trigger等のactionはaccessible nameとkeyboard activationを持つ。
- keyboard navigation/focus orderをroute structureと整合させる。
- route transition後のfocus targetをdeterministicにする。
- Stage-owned surfaceをhideする場合、visual concealmentだけでなくinteraction/focus orderから除外する。
- loading/error/unavailableを色だけで表現しない。
- URLで復元したscreenも同じaccessible name/stateを持つ。

### 18.10 Stage presentation binding

frontendはcurrent `(family, navigation_stage_id)`に対し、StagePresentationとStage-owned surface visibilityをdeterministicにresolveする。

```text
route-authoritative current Stage
  ↓
Stage presentation resolver
  ├─ title / guidance
  ├─ main surface ownership
  ├─ prerequisite/reference surfaces
  └─ presentation-only group label
```

Causalのlegacy `Inference` workspaceやPredictiveのgeneric result containerを内部実装として共有してもよいが、複数Stageのprimary identity / responsibilityを同一surfaceへflattenしない。

### 18.11 Layout / responsive overflow

- Stage main areaはsemantic section/cardを縦方向に並べる。
- compact pair/group controlはlocal grid/flexを使用してよい。
- intrinsically wide table/chart/preformatted resultはcomponent-local overflowを許可する。
- narrow viewportでもsemantic section orderとcontrol usabilityを維持する。
- page全体のhorizontal overflowをStage section compositionで発生させない。

---

## 19. Operation Availability

### 19.1 Purpose

Operation Availabilityは現在のProject/resource/route contextにおいて、どのcommand/controlを実行可能かをread-only projectionする。

Frontend route parser、Navigation catalog、Stage visibilityはscientific truthを所有しない。

### 19.2 Authority

```text
availability projection
  ≠ command authorization/validation
```

actual commandがdenyした場合、そのdenyをauthoritativeとする。

### 19.3 Representative reason codes

```text
PROJECT_ACCESS_DENIED
UNSUPPORTED_OPERATION
RESOURCE_REQUIRED
ROUTE_REQUIRED
RESOURCE_IMMUTABLE
SPEC_NOT_FIXED
GRAPH_NOT_FIXED
IDENTIFICATION_REQUIRED
INPUT_GRAPH_REQUIRED
INPUT_RESULT_REQUIRED
EXECUTION_STATE_NOT_RUNNABLE
RESULT_NOT_EXPORTABLE
DOMAIN_PREREQUISITE_NOT_SATISFIED
```

request-level error例:

```text
INVALID_OPERATION_AVAILABILITY_QUERY
UNSUPPORTED_RESOURCE_TYPE
ENTITY_NOT_FOUND
PROJECT_ACCESS_DENIED
INVALID_NAVIGATION_ROUTE
ROUTE_RESOURCE_FAMILY_MISMATCH
```

closed vocabularyをimplementation都合で無秩序に拡張しない。

### 19.4 Data Quality availability

Data Quality Stageは専用operationを持たないため、Profile result availabilityをprojectionする。

```text
PROFILE result present → read-only READY
PROFILE result absent  → unavailable(NO_PROFILE_RESULT) + Profile link
```

このreasonはUI-local presentation contractとして扱う場合でも、backend runtime operation/stateを作成しない。

---

## 20. Persistence / transaction / idempotency

### 20.1 Persistence rule

Project Management / Analysis Workspace分離やStage presentation再編に伴う新DB migrationを要求しない。

current persistent entitiesとrelationをauthorityとする。

- Project
- Research Context Version
- Dataset / Dataset Version
- Analysis View
- Analysis Specification
- Execution / StageExecution / StageAttempt
- Result
- Artifact
- Lineage
- Annotation
- Workspace Selection等のselection state

Navigation state / Analysis Context composite / presentation grouping / current Stage presentation stateを新しいpersistent aggregateにしない。

### 20.2 Transaction boundary

Application commandはUnit of Workでdomain mutationとpersistenceを一貫させる。external scientific executionはtransactionを不必要に長時間保持しない。

### 20.3 Command idempotency

Idempotency keyを全POSTへ一律要求せず、duplicate durable side effectを作り得るcommandを対象とする。

logical scope:

```text
(project_id, command_scope, idempotency_key)
```

behavior:

```text
same scope/key + same semantic request
  → stored result/response replay
  → duplicate side effectなし

same scope/key + different semantic request
  → conflict
```

path上のsemantic resource IDもrequest hash inputへ含める。

browser route/history/presentation stateはidempotent command hashのsemantic inputに含めない。

### 20.4 Artifact materialization

retryでduplicate artifactを生成しない。Artifactのcontent identity / lineage / idempotency contractを用いてsingle durable outcomeへ収束させる。

---

## 21. Security / authorization

### 21.1 Project boundary

すべてのProject-scoped resource read/writeはactorのProject accessを検証する。

URLの`project_id`だけを信頼せず、resourceが同じProjectに所属することを検証する。

### 21.2 Navigation and authorization

route visibilityやdisabled controlをauthorization enforcementの代替にしない。

Project/Context/Data/Result/Analysis API commandはserver-side authorizationを実施する。

### 21.3 Cross-project prohibition

- Research Context restore
- Dataset Version restore
- Analysis View restore
- deep-linked resource resolve
- Result / Lineage traversal

でProject境界外resourceを採用しない。

---

## 22. Failure / error handling

### 22.1 Route failure

invalid routeはexplicit navigation errorとして扱い、無関係なdefaultへsilent redirectしない。

### 22.2 Context failure

selection restore失敗はunselected stateへ落とし、架空defaultを作らない。

### 22.3 API failure

loading/error stateとlast known current routeを分離する。API failureだけを理由にrouteを別Family/Stageへ書き換えない。

### 22.4 Runtime failure

runtime failureはExecution/StageExecution/Result scientific status contractで表現し、Navigation Stage自体をruntime statusとして更新しない。

### 22.5 Feature selector failure

Predictive feature selectorでDataset Version/schemaを取得できない場合はselectorをunavailable/errorとして表示し、架空column optionやstale selectionをscientific inputとして確定しない。

Dataset Version変更によりselected featureが無効になった場合は、無効featureをsilent保持しない。clearまたはvalid intersectionへのreconcileを行う場合、利用者に変更を示す。

---

## 23. Verification / test design

### 23.1 Architecture tests

- Domain/runtimeからbrowser/router/navigation descriptorへの禁止依存。
- Navigation descriptorをpersistent repository/UoWへ登録していないこと。
- Navigation Stage fieldをAnalysisSpecification / ExecutionPlan / Execution / StageExecutionへ追加していないこと。
- Project Management frontend responsibilityがAnalysis runtime moduleへ逆依存しないこと。
- presentation grouping / StagePresentationをruntime/persistence authorityへ流入させていないこと。

### 23.2 Catalog tests

- 3 Familyが各1件。
- exact Family slug/default Stage。
- Family内Stage id/slug uniqueness。
- deterministic order。
- backend catalogとfrontend表示一致。
- frontend duplicate full catalogなし。

### 23.3 Project routing / parent navigation tests

対象:

```text
/projects
/projects/new
/projects/{id}
/projects/{id}/overview
/projects/{id}/context
/projects/{id}/data
/projects/{id}/results
```

検証:

- direct link
- reload
- Back / Forward
- short-route replace normalization
- unauthorized Project
- unknown section
- Selected Project各sectionにProject List parent actionがある
- parent action targetがcanonical `/projects`
- parent actionが`history.back()`に依存しない
- direct-entry Selected Project -> Project List -> Back -> Selected Project -> Forward -> Project List
- keyboard activation / accessible name

### 23.4 Analysis routing tests

対象:

```text
/projects/{id}/analysis/{family}/{stage}
/resource/{resource_type}/{resource_id}
```

検証:

- direct link
- reload
- Back / Forward
- Family switch → catalog default Stage
- Stage switch
- resource/family mismatch
- invalid Family/Stage
- supported legacy entry one-way normalization
- current Stage heading/descriptionがroute-authoritative Stageと一致
- presentation-only groupがroute/stage authorityになっていない

### 23.5 Analysis Context tests

- Current Project = route `project_id`
- Analysis WorkspaceでProject switch不可/read-only
- cross-project Research Contextをrestoreしない
- cross-project Dataset Versionをrestoreしない
- incompatible Analysis Viewをrestoreしない
- Dataset Version変更 → incompatible Analysis View deselect
- missing context → Family/Stage route維持
- fake default resourceを生成しない

### 23.6 Exploratory placement tests

- Profile → `PROFILE`
- Data Quality → Profile result read-only
- Data Quality absence → `NO_PROFILE_RESULT` + Profile導線、Execution作成なし
- Distribution → `DISTRIBUTION`
- Relationships → `ASSOCIATION`
- Comparison → `GROUP_SUMMARY` + `TIME_TREND`
- TIME_TRENDで新しいtime-series model/type validationなし
- Findings → `CHART` + saved result
- CHARTがpersistent operation/result/artifact semanticsを維持

### 23.7 Causal placement / visibility tests

- Setup / Discovery / Identification / Estimation / Effects / Diagnostics / Sensitivityのcurrent semanticsを保持する。
- Navigation Stage切替がExecution Stage/lifecycleを変更しない。
- IdentificationはIdentification input/actionとEligibility/Gateをprimary表示する。
- Estimationはestimator config/actionをprimary表示し、Identification/Sensitivity controlを所有しない。
- EffectsとDiagnosticsはdistinct primary surfaceである。
- Refutation/Sensitivity control/resultはSensitivityだけがprimary ownerである。
- wrong-stage main controlはhiddenかつnon-interactiveである。
- affected Causal Stageに日本語中心のpurpose guidanceがある。
- current Stage headingをlegacy `Inference` headingで置換しない。

### 23.8 Predictive placement / feature selector tests

- Setup / Train / Predict / Metrics / Explainability / Model Managementを表示できる。
- Prediction Task → Split → Training → Evaluation → Explanation → Model Cardのbackend lifecycleを維持する。
- Navigation Stageとruntime Stageの1:1 mappingを要求しない。
- DRAFT form stateがStage switchで消失しない。
- Setup feature selector optionがselected Dataset Version schemaと一致する。
- Dataset/schemaなしではexplicit unavailable stateになり、架空optionを作らない。
- confirmed feature selectionがdialog open時にchecked stateへ復元される。
- pending change + Cancelでconfirmed selectionを変更しない。
- Confirmでchecked featureをdeterministic schema orderでcommitする。
- same logical feature listが`predictive-analysis-spec/1.feature_spec.feature_columns`へ同一semanticsでserializeされる。
- Dataset Version changeでnew schemaにないfeatureをsilent保持しない。
- Setup -> Train -> Setupでvalid confirmed feature selectionを保持する。
- Trainはfeature setをread-only表示しeditable selectorを持たない。
- Predictはrelevant execution specificationのfeature setをread-only表示しeditable selectorを持たない。
- ExplainabilityはPredictive Explanationをcausal effectとして表現しない。
- column-selector helperをFamily間で共有する場合、Causal Discovery等のcurrent selector/request validationをprotected regressionとする。

### 23.9 Layout / accessibility tests

- major semantic sectionがvertical flowである。
- supported desktop/narrow viewportでsection composition起因のpage-level horizontal overflowがない。
- wide table/chartはcomponent-local overflowで扱える。
- hidden wrong-stage surfaceがfocus/interaction orderから除外される。
- current Stage heading、Project List parent action、feature selector dialog/checkbox/Confirm/Cancelがaccessible name/keyboard要件を満たす。

### 23.10 API / persistence regression tests

Project Management / Analysis Workspace分離やStage Content再編だけを理由とする次の変更がないことを確認する。

- new persistent navigation/AnalysisContext/presentation-group table
- new AnalysisContext backend API
- changed scientific operation semantics
- new DATA_QUALITY backend operation
- new Effects/Diagnostics Navigation-only runtime operation
- new standalone Predict scoring engine
- new Predictive specification version solely forfeature selector
- TIME_TREND scientific model mutation
- CHART display-only化

### 23.11 Headless execution tests

CLI / Python library / backend use caseからNavigation Stageなしでanalysis executionできることを確認する。

### 23.12 Browser E2E test seam

critical journeyはreal browserでcross-layer connectivityを確認する。

Project Management:

```text
Selected Project direct entry
  -> Project List
  -> Back
  -> Selected Project
  -> Forward
  -> Project List
```

Causal:

```text
Identification
  -> Estimation
  -> Effects
  -> Diagnostics
  -> Sensitivity
```

各transitionでcurrent headingとwrong-stage primary control absenceをkey checkpointとして確認する。

Predictive:

```text
Setup
  -> feature selector open / multi-select / Confirm
  -> Train (read-only selected feature context)
  -> Predict (execution-recorded feature context)
  -> Metrics
  -> Explainability
  -> Model Management
```

exhaustive visibility/state correctnessはdeterministic lower-level testをprimary proofとし、Browser E2Eはcross-layer journey proofとする。

---

## 24. Current design invariants

次はcurrent detailed designのMUST NOT invariantである。

1. Project ManagementとAnalysis Workspaceを1つのpeer-tab navigationへ再混在させない。
2. Project-global resource管理をAnalytical Familyとして扱わない。
3. Family/Navigation StageをExecution/StageExecution statusへ読み替えない。
4. current Navigation Stageをscientific reproducibility inputへ保存しない。
5. frontendにbackend catalogのduplicate full definitionを持たせない。
6. Analysis Contextをnew persistent aggregate/APIとして実装しない。
7. Analysis Workspace内でCurrent Projectを直接switchさせない。
8. missing contextをfake default resourceで補完しない。
9. Data Quality用backend operationをUI都合で新設しない。
10. TIME_TRENDへ新しい時系列scientific semanticsをUI都合で導入しない。
11. CHARTのpersistent operation semanticsを表示専用へ退化させない。
12. legacy analytical entryをparallel navigation authorityとして維持しない。
13. Project/Analysis route stateをruntime domainへ逆流させない。
14. UI IA変更だけを理由にDB/API/backend domain semanticsを変更しない。
15. Selected ProjectからProject Listへのparent actionを`history.back()`で実装しない。
16. legacy `Inference`等のworkspace groupingをcurrent canonical Stage identityとして表示しない。
17. Causal presentation groupingをroute/Navigation Stage/runtime Stage/persistent stateへ昇格させない。
18. Identification / Estimation / Effects / Diagnostics / Sensitivityのmain responsibilityを1つのgeneric surfaceへflattenしない。
19. Refutation/Sensitivity editable controlをSensitivity以外のStageへ配置しない。
20. Predictive Train/Predictでfeature setをad-hocに編集させない。
21. feature selectorのためだけにnew Predictive specification/API/backend operationを追加しない。
22. Predict Navigation Stageのためだけにstandalone scoring engineを新設しない。
23. UI/IA再編だけを理由にLightGBM / LIME / SHAP等のnew analytical capabilityを暗黙追加しない。
24. major semantic sectionの横並びを理由にpage-level horizontal scrollを必須化しない。

---

## 30. CHANGE LOG

### 30.1 Effective snapshot baseline

Domain/runtime/capability/result/lineage、Family/Navigation Stage catalog、browser navigation、operation availability等のcurrent detailed designをeffective snapshotとして統合した。

### 30.2 Project Management / Analysis Workspace separation

Project ManagementとAnalysis Workspaceを別application/navigation scopeとして定義し、Project routes、resource ownership、Analysis Context、browser restoration、frontend component responsibilityをcurrent detailed designへ統合した。

### 30.3 Analytical surface placement

Causal / Exploratory / Predictiveのanalytical semanticsをNavigation Stage Contentsへ配置した。Exploratory Data Quality、TIME_TREND、CHARTについてbackend semanticsを変更しないcontractを明文化した。

### 30.4 Analysis Stage Content Architecture

Selected ProjectからProject Listへの明示的parent navigation、current Navigation Stageをprimary identityとするStage presentation、Causal Stage responsibility separation、Predictive Stage responsibility separation、Dataset-schema-backed Predictive feature selector、vertical layout/accessibility/history/test seamをcurrent effective detailed design本文へ統合した。

この変更はUI/IA/presentation designの具体化であり、canonical Navigation Stage catalog、API、persistence schema、backend analytical semantics、runtime execution lifecycleを変更しない。
