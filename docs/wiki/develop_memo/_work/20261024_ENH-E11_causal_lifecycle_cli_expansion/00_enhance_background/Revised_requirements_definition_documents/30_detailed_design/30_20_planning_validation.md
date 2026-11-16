# 30_20_planning_validation

**Status:** `RD02_STRUCTURAL_WORKING_COPY / E11_NOT_PUBLISHED`. Original chapter and source provenance retained; DD physical coverage remains partial.  
**Source blob:** `04d83541e55ab0364500afb4b92ef55c10785a0c`.

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

## 2. `PlanValidator`

**Responsibility:** Verify the structural validity of an `ExecutionPlan` and produce deterministic topological execution order. This is not a causal identification oracle.

| Field | Python type / default | Role |
|---|---|---|
| `runners` | `StageRunnerRegistry`, required | Registered runtime Stage capabilities |
| `max_timeout_seconds` | `int=86400` | Resource policy upper bound |

| Method | Return | Preconditions and operations | Exceptions |
|---|---|---|---|
| `__init__(runners: StageRunnerRegistry, *, max_timeout_seconds: int = 86_400)` | `None` | store dependencies and limit | none specified |
| `validate(plan: ExecutionPlan)` | `tuple[str, ...]` | Validate plan schema/reference, unique Stage key, registered runner, timeout, edge endpoint, binding and schema agreement; perform deterministic topological sort | `InvalidExecutionPlan(code, message)` |
| `_error(code: str, message: str)` | `None` (never returns normally) | raise the above exception | `InvalidExecutionPlan` |

**Negative codes checked by source:** `UNSUPPORTED_PLAN_SCHEMA`, `MISSING_PLAN_REFERENCE`, `DUPLICATE_STAGE_KEY`, `EMPTY_PLAN`, `RUNNER_NOT_REGISTERED`, `RESOURCE_POLICY_EXCEEDED`, `MISSING_DEPENDENCY_NODE`, `DISABLED_DEPENDENCY`, `MISSING_OUTPUT`, `MISSING_INPUT`, `SCHEMA_MISMATCH`, `DUPLICATE_BINDING`, `PLAN_CYCLE`.

**Test obligations:** Graph DAG deterministic order, empty/cycle, type mismatch, disabled dependency, timeout/boundary, missing runner; E11 must not bypass these checks if reusing this component.

## 3. `StageRunnerRegistry`

**Responsibility:** Runtime StageType to concrete StageRunner lookup, not E11 scientific estimator registry unless independently decided.

| Field | Type / default | Invariant |
|---|---|---|
| `_runners` | `dict[StageType, StageRunner]={}` | unique stage_type |

| Method | Return | Behavior / error |
|---|---|---|
| `register(runner: StageRunner)` | `None` | Duplicate type raises `DuplicateRegistration` |
| `resolve(stage_type: StageType)` | `StageRunner` | Missing raises `RunnerNotRegistered` |
| `contains(stage_type: StageType)` | `bool` | Structural membership |
| `capability_fingerprint` (property) | `tuple[str, ...]` | Sorted StageType.key fingerprint |

**当該構成要素の詳細設計制約（関連Requirement）**

- **`FR-075`**：Family別PlannerをRegistryから解決する
- **`FR-079`**：Stage RunnerをRegistryから解決し、Executorへif/elif分岐を集約しない
- **`FR-080`**：canonical lifecycle/application serviceがExecutionのclaim、state、cancel、retry、Result/Artifact metadata commitを所有し、Generic Executorはowned workflow context内で依存順、Stage sequencing、runner invocationを実行する
- **`FR-089`**：Generic validationとFamily-specific validationを分離して実行する
- **`FR-128a`**：Algorithm/Runnerをregistry/capabilityから解決・管理するcurrent contractを維持する
- **`FR-128b`（将来拡張・現行提供対象外）**：size limit、timeout等のoperational resource configurationを一元管理する
