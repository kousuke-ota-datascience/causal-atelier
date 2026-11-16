# 30_10_domain_resources


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

## 5. `GraphVersion` (Product Domain)

**Responsibility:** Product-scoped graph provenance, editable DRAFT and immutable FIXED state.

| Field group | Fields and types | Constraints |
|---|---|---|
| Identity | `graph_version_id: str`, `project_id: str`, `name: str` | ID default generated, owner Project |
| Provenance | `source_result_id: str|None`, `parent_graph_version_id: str|None`, `graph_origin: GraphOrigin`, `provenance_json: dict[str,Any]`, `edit_rationale: str|None` | Source/parent match origin rules |
| Graph | `graph_type: GraphType`, `graph_json: dict[str,Any]`, `content_hash: str`, `designated_outcome_node: str|None` | Edit is canonicalized, outcome node must exist |
| Lifecycle | `status: GraphVersionStatus`, `created_by: str`, `created_at: datetime|None` | Initial DRAFT; FIXED not re-edited |

| Method | Return | Behavior / error |
|---|---|---|
| `__post_init__()` | `None` | Checks origin via validate_origin |
| `validate_origin()` | `None` | Invalid origin/link combination raises `ValueError` |
| `apply_edit(graph_json, edit_rationale=None, designated_outcome_node=None, *, update_outcome=False)` | `None` | FIXED raises `GraphAlreadyFixed`; invalid outcome or missing edit reason raises `InvalidAnalysisSpec`; uses `canonical_graph` |
| `fix()` | `None` | FIXED→FIXED raises `InvalidStateTransition` |
| `validate_outcome()` | `None` | Invalid outcome raises `InvalidAnalysisSpec` |

**E11 caution:** This is Product GraphVersion; new local Graph fidelity and versioning cannot claim Product persistence without explicit ADR/Scope change. FCI circle/Temporal oracle behavior is not proven by this class alone.

**当該構成要素の詳細設計制約（関連Requirement）**

- **`FR-007`**：Executionは参照ResearchContextVersionを固定し、受付時のobjective/rationale等の再現に必要なsnapshot metadata/hashを保持する。ResearchContext全体の重複保存を必須化しない
