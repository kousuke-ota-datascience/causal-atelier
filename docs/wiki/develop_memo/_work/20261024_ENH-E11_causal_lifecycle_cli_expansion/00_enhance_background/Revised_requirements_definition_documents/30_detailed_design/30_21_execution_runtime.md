# 30_21_execution_runtime

**Status:** `RD02_STRUCTURAL_WORKING_COPY / E11_NOT_PUBLISHED`. Original chapter and source provenance retained; DD physical coverage remains partial.  
**Source blob:** `04d83541e55ab0364500afb4b92ef55c10785a0c`.

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

## 4. `ExecutionOutcome` / `GenericExecutor`

**Responsibility:** Generic synchronous Stage lifecycle; no Browser navigation or scientific Estimand authority.

| Symbol/field | Python type | Invariant |
|---|---|---|
| `ExecutionOutcome.status` | `str` | Overall technical status |
| `ExecutionOutcome.stages` | `tuple[StageExecution, ...]` | Stage snapshots |
| `ExecutionOutcome.results` / `artifacts` | `tuple[Any, ...]` | Stage output collections |
| `ExecutionOutcome.stage_results` | `tuple[tuple[str, StageRunResult], ...]=()` | Identified stage output |
| `GenericExecutor.runners` | `StageRunnerRegistry` | Stage resolution |
| `GenericExecutor.validator` | `PlanValidator` | Refuses invalid plan |
| `GenericExecutor.bindings` | `BindingResolver` | Typed upstream output binding |
| `GenericExecutor.clock` | `Callable[[], datetime]` | Injected UTC clock default |
| `GenericExecutor.compensate` | `Callable[[StageExecution, Exception], None]` | Injected stage compensation default no-op |

```python
def execute(
    self, execution_id: str, plan: ExecutionPlan, *,
    external_inputs: dict[str, dict[str, Any]] | None = None,
    snapshots: dict[str, Any] | None = None,
    worker_id: str = "local-worker",
    cancelled: Callable[[], bool] | None = None,
    stage_executions: tuple[StageExecution, ...] | None = None,
    effective_random_seed: int | None = None,
) -> ExecutionOutcome: ...
```

**Execution sequence:** validate Plan; create/merge StageExecution by stage_key; iterate topological stage keys; skip disabled Stage; resolve input bindings and invoke registry-provided runner; collect results/artifacts and lifecycle state. Existing source owns the exact cancel/compensation semantics; any E11 extension must be reviewed and tested, not inferred from this outline.

**Negative:** Unregistered Stage, mismatched supplied StageExecution, invalid dependency, cancelled Stage and compensating failure. Product lifecycle owner remains outside the local E11 CLI-only design.


## 98. RD-04：詳細設計へ引き継ぐ要求起源の具体制約

**Status:** `RD04_DETAILED_CONSTRAINT_TRACE / OWNER_CONTENT_REVIEW_PENDING`。RD-04で抽象化した原文から、モジュール・Class・Method・I/O・失敗処理へ落とすべき実現制約を保持する。実装されていると確認した記録ではない。クラスレベル仕様は[共通テンプレート](30_01_class_design_template.md)に従い別途DD設計確認する。

### 98.1. FR-086a（SPLIT）

- 移管する原条項の具体内容：stochastic Stageのactual effective random seedを`StageAttempt.effective_random_seed`へ保存し、同一logical Stageのretryで同じseedを再利用する
- 上位Requirementと整合する要求核：確率的処理を再試行しても同じ実効乱数条件を再現できる
- `FR-086a`；Status=`ACTIVE`；Implementation=`PARTIAL`；[逐条Disposition](../95_rd04_fr_application_review.md)

### 98.2. FR-086b（SPLIT）

- 移管する原条項の具体内容：Stageごとのtimeout / operational resource limitをpersistent/configurable policyとして保持する
- 上位Requirementと整合する要求核：処理ごとの時間・資源上限を設定できる
- `FR-086b`；Status=`DEFERRED`；Implementation=`PARTIAL`；[逐条Disposition](../95_rd04_fr_application_review.md)

### 98.3. NFR-001b（SPLIT）

- 移管する原条項の具体内容：actual scientific library versionとStageAttempt effective seedを含むenvironment再構築metadataを保持する
- 上位Requirementと整合する要求核：解析結果を再現するため実効ライブラリ版・乱数条件を取得できる
- `NFR-001b`；Status=`ACTIVE`；Implementation=`PARTIAL`；[逐条Disposition](../96_rd04_nfr_ar_application_review.md)

### 98.4. NFR-006a（SPLIT）

- 移管する原条項の具体内容：current claim/lease/retry mechanicsでExecution/Stage lifecycleを安全に再試行できる
- 上位Requirementと整合する要求核：中断・再送時にExecutionを安全に再開・再試行できる
- `NFR-006a`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[逐条Disposition](../96_rd04_nfr_ar_application_review.md)

### 98.5. NFR-006b（SPLIT）

- 移管する原条項の具体内容：retry/restartでsuccessful Stage outputのduplicate durable Artifact materializationを防止する。exactly-once executionは保証しない
- 上位Requirementと整合する要求核：再試行・再起動で成功済み成果物の重複作成を防止する
- `NFR-006b`；Status=`ACTIVE`；Implementation=`PARTIAL`；[逐条Disposition](../96_rd04_nfr_ar_application_review.md)

### 98.6. AR-019（SPLIT）

- 移管する原条項の具体内容：random seedだけでなくsplit indexまたはpartition artifactを保存する
- 上位Requirementと整合する要求核：分析のデータ分割を再現可能な情報として保持しなければならない
- `AR-019`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[逐条Disposition](../96_rd04_nfr_ar_application_review.md)
