<!-- ENH-E11 split working copy: not a formal approval. -->
# 30 — planning execution

**Status:** `STRUCTURAL_COPY_DRAFT` (existing baseline text, not E11 canonical publication)

**Source:** [30_detailed_design.md](https://github.com/kousuke-ota-datascience/causal-atelier/blob/3ba5fe2465ec591f0da7f998c21a5241984b73dc/docs/wiki/requirement_definition/30_detailed_design.md) · blob `04d83541e55ab0364500afb4b92ef55c10785a0c`  
**Index:** [Revised document inventory](../README_00_Revised_requirements_definition_documents.md)

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
