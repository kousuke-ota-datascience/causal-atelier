<!-- ENH-E11 split working copy: not a formal approval. -->
# 30 — domain context

**Status:** `STRUCTURAL_COPY_DRAFT` (existing baseline text, not E11 canonical publication)

**Source:** [30_detailed_design.md](https://github.com/kousuke-ota-datascience/causal-atelier/blob/3ba5fe2465ec591f0da7f998c21a5241984b73dc/docs/wiki/requirement_definition/30_detailed_design.md) · blob `04d83541e55ab0364500afb4b92ef55c10785a0c`  
**Index:** [Revised document inventory](../README_00_Revised_requirements_definition_documents.md)

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
