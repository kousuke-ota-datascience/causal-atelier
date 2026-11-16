# 30_21_execution_runtime


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

### 10.5. `ExecutionOutcome`（EXISTING：Owner 7区分）

#### 10.5.1. 識別情報・責務

- **Class/module:** `ariadne.product.workflow.executor.ExecutionOutcome`。**EXISTING**、source blob `81d91e7de0fc0eb5a582711968b698fa4ac44761`。
- **Responsibility:** Product GenericExecutorからのimmutable synchronous run outcome snapshot。E11 Local Science/ManifestやProduct DB lifecycleのauthorityではない。

#### 10.5.2. フィールド

| Field | Type/default | Invariant |
| --- | --- | --- |
| `status` | `str` | technical outcome summary、科学合否とは異なる |
| `stages` | `tuple[StageExecution,...]` | immutable tuple |
| `results` | `tuple[Any,...]` | runner results; typed Sci canonical bridgeではない |
| `artifacts` | `tuple[Any,...]` | runtime artifact collection |
| `stage_results` | `tuple[tuple[str, StageRunResult],...]=()` | stage key→outcome references |

#### 10.5.3. Constructor / Factory

`@dataclass(frozen=True)`の自動生成`__init__`を使用。**N/A:** 明示Factory、外部Backend wiring、I/O side effects無し。Exact generated constructor signatureはdataclass fieldsに従う。

#### 10.5.4. メソッド

User-defined methodsはSourceに存在しない。**N/A理由:** immutable dataclassのみ。Dataclass生成`__init__`/`__repr__`等の既定演算を利用する。

#### 10.5.5. 処理仕様

GenericExecutorがStageExecutionとResult/Artifact collectionsを収集した後に生成するimmutable snapshot。Scientific Estimand、Identification Status、AR Confidence Setの意味をこのResult型から推測しない。

#### 10.5.6. I/O・連携・失敗処理

`GenericExecutor.execute`の戻り値であるin-memory DTO。**N/A:** DTO自身にDB/FS I/O・retry・rollback・外部例外は無し。保存可否は別のApplication Service/Portで審査する。

#### 10.5.7. 検証

**Unit:** field preservation、immutability、empty stage_results default。**Contract:** Product GenericExecutor戻り値の型とstage linkage。**Negative:** 異なるMethodのScience合否をDTO statusから捏造しない。Source構造確認のみ／テストNOT_RUN。

### 10.6. `GenericExecutor`（EXISTING：Owner 7区分）

#### 10.6.1. 識別情報・責務

- **Class/module:** `ariadne.product.workflow.executor.GenericExecutor`、**EXISTING**、source blob `81d91e7de0fc0eb5a582711968b698fa4ac44761`。
- **Responsibility:** Product Runtime Planの検証、topological Stage sequencing、Runner invocationとStage結果収集。Execution Lease/DB authority、Browser navigation、E11 Local scientific Estimand authorityは責務外。
- **Reuse boundary:** E11 Local CLIからの直接流用はOwner未決であり、既存Product Stage lifecycleを暗黙にE11 run lifecycleへ昇格しない。

#### 10.6.2. フィールド

| Field | Type | Origin/constraint |
| --- | --- | --- |
| `runners` | `StageRunnerRegistry` | required constructor injection |
| `validator` | `PlanValidator` | constructor creates from runners |
| `bindings` | `BindingResolver` | constructor creates |
| `clock` | `Callable[[], datetime]` | injected or UTC now default |
| `compensate` | `Callable[[StageExecution,Exception],None]` | injected or no-op default |

#### 10.6.3. Constructor / Factory

`__init__(self, runners: StageRunnerRegistry, *, clock: Callable[[],datetime]|None=None, compensate: Callable[[StageExecution,Exception],None]|None=None) -> None`。Inject runner registry and clock/compensation policy; initialize`PlanValidator` and`BindingResolver`. **N/A:** Separate Factory not implemented in this Source.

#### 10.6.4. メソッド

```python
def execute(self, execution_id: str, plan: ExecutionPlan, *,
            external_inputs: dict[str,dict[str,Any]]|None=None,
            snapshots: dict[str,Any]|None=None,
            worker_id: str="local-worker",
            cancelled: Callable[[],bool]|None=None,
            stage_executions: tuple[StageExecution,...]|None=None,
            effective_random_seed: int|None=None) -> ExecutionOutcome: ...
```

Public method `execute` accepts a Product Plan and emits `ExecutionOutcome`; it may invoke runners and compensation (side effects controlled by injected collaborators). Constructor is described in §10.6.3.

#### 10.6.5. 処理仕様

`PlanValidator.validate` generates deterministic order; executor creates/merges StageExecutions by key, resolves upstream bindings, and invokes registered Runner for enabled Stages, collecting typed StageRunResult and artifacts. It respects supplied StageExecution identity and cancellation semantics. **Source inspection rather than execution** supports this outline; actual error and compensation branches require independent unit/negative tests. §10.2 defines higher-level Product worker lifecycle; DB claim/lease/Result metadata commit is performed outside this Class.

#### 10.6.6. I/O・連携・失敗処理

- Input: Product ExecutionPlan, StageRunnerRegistry, optional supplied StageExecution and cancellation callback.
- Output: immutable ExecutionOutcome. External interactions happen through injected runners; direct Web API/DB authority is N/A.
- Failure: InvalidExecutionPlan, unregistered StageType, cancelled Stage, invalid supplied StageExecution, Runner or compensation exception. **Retry/rollback:** Product application/worker owns lease/retry/commit; `compensate` callback may be invoked within this component but cannot guarantee cross-store rollback alone.
- E11 Local CLI must not reuse this lifecycle without verified Port/authority ADR and regressions.

#### 10.6.7. 検証

**Unit:** valid dependency order, external inputs and binding, cancellation, supplied StageExecution, runner failure/compensation, seed preservation. **Negative:** bad dependency/StageType, mismatch, late failure. **Regression:** existing Product E9/E10 and Worker lifecycle, avoid conflating E11 Local run. **Trace:** FR-080/086a/089、NFR-001b/006a/006b、AR-019。No test execution reported.

### 10.7. Chapter-wide Requirement Trace

- `FR-086a`：stochastic Stageのactual effective random seedを`StageAttempt.effective_random_seed`へ保存し、同一logical Stageのretryで同じseedを再利用する
- `FR-086b`（将来拡張・現行提供対象外）：Stageごとのtimeout / operational resource limitをpersistent/configurable policyとして保持する
- `NFR-001b`：actual scientific library versionとStageAttempt effective seedを含むenvironment再構築metadataを保持する
- `NFR-006a`：current claim/lease/retry mechanicsでExecution/Stage lifecycleを安全に再試行できる
- `NFR-006b`：retry/restartでsuccessful Stage outputのduplicate durable Artifact materializationを防止する。exactly-once executionは保証しない
- `AR-019`：random seedだけでなくsplit indexまたはpartition artifactを保存する
