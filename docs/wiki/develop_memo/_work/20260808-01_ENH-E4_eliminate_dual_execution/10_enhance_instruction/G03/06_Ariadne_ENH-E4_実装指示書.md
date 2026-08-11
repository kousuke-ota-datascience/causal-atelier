# Ariadne ENH-E4 E4-G03 実装指示書

* Project: Ariadne / causal-atelier
* Enhancement: ENH-E4 eliminate dual execution
* Branch: `refactor/ariadne_mvp_e4`
* Baseline commit: `cb28a18c07cad00cf12f01e9124651aa45aab16f`
* Active Gate: `E4-G03`
* Gate name: Persistent StageExecution and runner boundary
* Trial: `01`
* Expected starting Product migration head: `20260809_product_0007`
* Expected next Product migration revision: `20260809_product_0008`（baseline上の連番。実装開始時にactual headを再確認する）
* Trial ID format: 2-digit zero-padded decimal (`01`–`99`)
* Test Item ID format: 3-digit zero-padded decimal (`001`–`998`; `000` reserved; `999` Gate Decision)
* Preflight prerequisite: Test PostgreSQL Infrastructure `PASS_READY_FOR_G03`

---

# 1. Source of Truth

本書は **E4-G03 Trial 01のCoding Agentが従う唯一のGate-local implementation contract** である。

Coding Agentは、本書に明示された範囲を実装し、本書にないarchitecture decisionを独自に追加しない。

本書の設計根拠として参照してよい正本は次のみ。

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
40_operator_prompts/architecture_review/
06_target_architecture_decision_record_result.md

docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
40_operator_prompts/architecture_review/
07_gate_decomposition_result.md

docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
30_test_report/G02/
E4-G02_01_external_postgresql_verification_final_gate_decision.md

docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
40_operator_prompts/G03_Preflight/
02_test_postgresql_infrastructure_verification_result.md
```

さらに、baseline commit時点のcurrent production code / Product migration / automated testsを実装上の事実確認に使用する。

本書とcurrent codeの間に、実装選択では解消できないsemantic contradictionがある場合は、勝手にarchitectureを変更せず `DESIGN_BLOCKED` とする。

過去のdraft、古いoperator prompt、G02のtemporary external PostgreSQL runbookはG03の実装契約ではない。

---

# 2. Coding Agent Role

Coding Agentの責務は以下。

1. branch / starting commit / Product migration headを確認する。
2. unrelated working-tree artifactを保全する。
3. G03 scopeだけを実装する。
4. canonical `Execution` 配下にpersistent `StageExecution`を導入する。
5. stage persistence / attempt history / query contractを実装する。
6. `Execution` claim/leaseとstage mutation authorityを整合させる。
7. `GenericExecutor`をworkflow infrastructureへ限定する。
8. Causal / Exploratory / Predictiveのcanonical stage planを共通contractへmaterializeできるようにする。
9. E4-G03-AC-001〜005を直接検証するautomated test codeを追加する。
10. Product migrationを追加する。
11. standardized Test PostgreSQL infrastructureを用いて可能な範囲のself-checkを行う。
12. implementation commitを固定する。
13. Gate-local Implementation Completion Reportを作成する。
14. enhancement-wide cumulative implementation ledgerを更新する。
15. `READY_FOR_TEST` または `DESIGN_BLOCKED` で停止する。

Coding AgentはGate PASSを判定しない。

---

# 3. Prohibited Work

## 3.1 Gate越境

以下をG03で先行実装してはならない。

### G04 scope

* `ExecutionResult` / `StageResult` semantic consolidation
* Result ownership authorityの一本化
* Artifact metadata ownership authorityの一本化
* ArtifactStorePort再設計
* Result / Artifact cardinalityの全面再設計
* G04固有migration

### G05 scope

* old Causal / Family Product new-write pathの全面cutover
* old lifecycleの完全停止
* E4-TD-001 closure
* E4-TD-002 closure
* Product Execution convergenceの完成
* user-facing全routeのcanonical convergence

### G06 scope

* lineage authority consolidation
* structural generic lineage dual-write除去
* closure/export authority変更

### G07 scope

* legacy runtime retirement
* legacy source deletion/archive
* promoted CLI architecture変更
* root legacy migration削除

### G08 scope

* final clean bootstrap
* final architecture audit
* transition debt全閉鎖

## 3.2 Scientific scope

以下は禁止。

* scientific algorithm変更
* estimator / causal discovery / preprocessingのscientific behavior変更
* benchmark target変更
* family固有scientific semanticsを共通化の都合で削ること

## 3.3 Persistence scope

以下は禁止。

* root legacy migration chainへのschema追加
* `alembic.ini` 側legacy migrationをProduct targetとして使用
* development DBをtest reset対象にする
* Result / Artifact persistenceを`GenericExecutor`へ移す
* stageごとに独立claim authority / independent lease authorityを新設する
* stage persistenceをsecond Execution lifecycle authorityにする

## 3.4 Test infrastructure scope

G03 Preflightで確定した以下を、G03 product implementation都合で作り直さない。

```text
compose.test.yaml
Dockerfile.test
scripts/test/reset_product_test_db.py
scripts/test/run_product_postgres_tests.sh
scripts/test/run_product_postgres_tests_in_container.sh
scripts/test/README.md
```

Test Agent / Coding AgentのDocker access制約を理由に、G02型のmanual network workaroundをrepository contractへ戻してはならない。

## 3.5 Unrelated artifact

既知のunrelated artifact:

```text
deploy/.nfs000000000076202f00000088
```

が存在しても、

* stageしない
* restoreしない
* deleteしない
* recreateしない
* implementation commitへ含めない

---

# 4. Baseline / Current State

## 4.1 Gate status

baseline時点:

```text
E4-G01 = PASS
E4-G02 = PASS
Test PostgreSQL Infrastructure Preflight = PASS_READY_FOR_G03
E4-G03 = NOT_STARTED
```

G03 implementation開始後:

```text
E4-G03 = IN_PROGRESS
```

## 4.2 Baseline commit

```text
cb28a18c07cad00cf12f01e9124651aa45aab16f
```

このcommitはG03 Preflight documentationを含むbranch current stateであり、Product source / test infrastructure implementationはその直前までに確立済みである。

Coding Agentは開始時に必ず:

```bash
git branch --show-current
git rev-parse HEAD
git status --short
```

を記録する。

branchが異なる場合は作業しない。

HEADがbaseline以降へ進んでいる場合は、baselineからHEADまでのdiffを確認し、G03 production/test/migration contractへ影響する変更がないことを説明できなければ `DESIGN_BLOCKED`。

## 4.3 Product migration

expected starting head:

```text
20260809_product_0007
```

確認にはProduct migration chainのみを使う。

G03はpersistent StageExecution schemaを追加するため、**Product migration追加はMUST**。

baseline上のexpected next revision:

```text
20260809_product_0008
```

actual starting headが正当に変わっている場合は、そのheadのdirect childとしてrevisionを作り、reportへ理由とactual revisionを記録する。

root legacy migrationは変更しない。

## 4.4 Current StageExecution observation

baselineではproduct domainに`StageExecution` / `StageAttempt` / `StageExecutionStatus`が存在する。

しかしG03開始時点では、canonical Product `UnitOfWork` / repository / ORM schema上のpersistent StageExecution authorityは成立していない。

したがって、既存domain classの存在だけでは `E4-G03-AC-001/002` を満たさない。

## 4.5 Current GenericExecutor observation

baselineの`GenericExecutor`はshared workflow infrastructureとして存在するが、現実装ではin-memory `StageExecution`を生成し、stage attempt開始・成功/失敗・retry loop等も担っている。

G03ではtarget ADRに合わせて責務を縮小する。

## 4.6 Existing G02 contract

G02で成立済みの以下を破壊しない。

```text
one canonical Execution identity
one shared lifecycle
one canonical claim authority
explicit lease owner / expiry
owner-checked renew/update/complete
retry = same Execution ID
rerun = new Execution ID
revise = new Execution ID
cancel = terminal Execution transition
GenericExecutor != Execution claim authority
```

G03はこの上にstage persistenceを追加するGateであり、別claim architectureを作るGateではない。

---

# 5. Gate Status / Trial Rules

Status values:

```text
NOT_STARTED
IN_PROGRESS
READY_FOR_TEST
PASS
FAIL
BLOCKED
DESIGN_BLOCKED
```

Active Trial:

```text
E4-G03 Trial 01
```

Rules:

1. FAILが発生していない限りTrial番号を増やさない。
2. Coding AgentはTrial番号を勝手に進めない。
3. environment access failureはimplementation FAILとして扱わない。
4. semantic contradictionだけを `DESIGN_BLOCKED` とする。
5. passed Gate contractを暗黙に再定義しない。
6. implementation commitと後発report/evidence commitは分離してよい。
7. `READY_FOR_TEST` 後にCoding Agent自身でGate Decisionを行わない。

---

# 6. Gate Objective

E4-G03のObjective:

> 全canonical Executionにpersistent StageExecutionを持たせ、GenericExecutorをworkflow infrastructureへ限定する。

Architecture After Gate:

```text
Canonical Execution
  ├─ identity / family / state / claim / lease  ← G02 authority
  │
  └─ persistent StageExecution children        ← G03
       ├─ stage identity / key / type / ordinal / dependencies
       ├─ persistent state
       ├─ persistent attempt history
       ├─ serializable input/output binding metadata
       ├─ failure/cancellation details
       └─ timestamps
             │
             v
       Canonical stage orchestration service
             │
             v
       GenericExecutor
       ├─ plan validation
       ├─ stage ordering
       ├─ binding resolution
       ├─ runner invocation
       └─ non-authoritative in-memory outcome
             │
             v
       family/shared scientific runner
```

Authority boundary:

```text
Execution claim / lease         = canonical Execution repository/service
Stage persistence/state         = canonical application service + StageExecution repository/UoW
Retry policy                    = canonical application/service boundary
GenericExecutor                 = no claim / no commit / no canonical retry authority
Result/Artifact metadata        = current authority retained until G04
```

---

# 7. Canonical StageExecution Contract

## 7.1 Ownership

Every **canonical** `Execution` MUST own one or more persistent `StageExecution` children.

The ownership relation is:

```text
Execution 1 ── owns ──> 1..N StageExecution
```

Requirements:

* `StageExecution.execution_id` references the canonical Execution ID.
* Stage identity is subordinate to, but distinct from, Execution identity.
* Stage identity MUST remain stable across stage retry.
* rerun/revise creates a new Execution and therefore new StageExecution identities.
* legacy/family transitional rows are not allowed to become a second canonical stage authority.

## 7.2 Stage identity

Minimum logical fields:

```text
stage_execution_id
execution_id
stage_key
stage_type
ordinal
dependencies
status
input_binding
output_binding
last_error
started_at
finished_at
created_at / equivalent audit timestamp if repository convention requires
attempt history
```

The physical schema MAY use repository naming conventions, but the logical contract above MUST be reconstructable.

Required uniqueness:

```text
stage_execution_id                     globally unique
(execution_id, stage_key)              unique
```

`ordinal` MUST be deterministic within the materialized workflow plan.

If multiple same-ordinal stages are intentionally supported for parallel semantics, `(execution_id, ordinal)` need not be unique; otherwise it SHOULD be unique. The implementation report MUST state the chosen rule.

## 7.3 Dependencies

The persistent stage representation MUST preserve enough dependency information to reconstruct the executable order without reading runner internals.

Allowed physical forms include:

* JSON array of prerequisite stage keys
* normalized dependency relation

Do not create generic Product lineage edges for stage dependencies in G03.

Stage dependency persistence is workflow orchestration metadata, not G06 lineage authority.

## 7.4 Materialization timing

A canonical Execution MUST NOT be durably committed as a valid new Product write while its canonical stage plan is absent.

Required transaction boundary:

```text
canonical submit/create
    ↓
validate execution
    ↓
resolve family workflow plan
    ↓
materialize StageExecution skeletons
    ↓
persist Execution + StageExecution children
    ↓
single UoW commit
```

If:

* family planner is unavailable
* plan is invalid
* plan contains no executable canonical stage
* stage materialization fails

then the canonical new-write transaction MUST fail without leaving a committed canonical Execution that has zero StageExecution children.

This is the primary implementation rule for `E4-G03-AC-004`.

## 7.5 Family coverage

The common materialization contract MUST work for:

```text
CAUSAL
EXPLORATORY
PREDICTIVE
```

Do not implement three independent persistence authorities.

Family-specific differences belong in plan/provider/adapter definitions.

The canonical persistence contract is common.

## 7.6 Transitional boundary

`E4-TD-002` permits old stage persistence / ephemeral behavior to remain until G05.

Therefore G03 does **not** require deletion or complete cutover of every historical/old family path.

However:

* any new write that is explicitly on the **canonical G02 Execution path** MUST satisfy G03 StageExecution contract;
* old/transitional paths MUST NOT be used as the canonical evidence for G03;
* G03 MUST NOT introduce another new ephemeral canonical path.

---

# 8. Stage Attempt History Contract

## 8.1 Purpose

Stage persistence is the common audit/retry boundary.

Attempt history MUST be queryable independently of scientific runner internals.

Minimum attempt fields:

```text
stage_execution_id
attempt_number
worker_id / execution lease owner identity
started_at
finished_at
error / failure detail
```

A separate `stage_attempt_id` MAY be added.

## 8.2 Attempt numbering

For one `StageExecution`:

```text
attempt_number = 1, 2, 3, ...
```

must be monotonic and unique.

Required constraint:

```text
(stage_execution_id, attempt_number) unique
```

## 8.3 History preservation

Completed attempt history MUST NOT be deleted or renumbered by retry.

When a failed stage is retried:

```text
same execution_id
same stage_execution_id
new attempt_number
old attempt row preserved
```

## 8.4 Append-only meaning

An active attempt record may be finalized with:

```text
finished_at
error
terminal attempt outcome fields
```

After completion, past attempt records MUST NOT be rewritten to make a later retry appear to have been the original attempt.

## 8.5 Retry authority

`GenericExecutor` MUST NOT decide whether a failed stage is retryable.

Retry policy belongs to the canonical orchestration/application boundary.

The runner / GenericExecutor MAY return failure classification or exception metadata required by that policy.

It MUST NOT:

* increment canonical Execution retry count
* create a new Execution for retry
* decide max attempts as canonical policy
* persist retry state
* commit a stage retry transaction

---

# 9. Stage Lifecycle Contract

## 9.1 Required states

Existing common states are retained:

```text
PENDING
READY
RUNNING
SUCCEEDED
FAILED
SKIPPED_DUE_TO_PREREQUISITE
```

G03 additionally requires an explicit persistent representation for cancellation.

Preferred and expected implementation:

```text
CANCELLED
```

as a `StageExecutionStatus`.

If the Coding Agent finds a repository-level constraint that makes a distinct `CANCELLED` state impossible without contradicting an approved contract, it MUST stop as `DESIGN_BLOCKED`; it MUST NOT encode cancellation as a misleading prerequisite skip.

## 9.2 Allowed transition intent

Minimum valid lifecycle:

```text
PENDING -> READY
PENDING -> CANCELLED

READY -> RUNNING
READY -> SKIPPED_DUE_TO_PREREQUISITE
READY -> CANCELLED

RUNNING -> SUCCEEDED
RUNNING -> FAILED
RUNNING -> CANCELLED

FAILED -> RUNNING   only after canonical retry authorization
```

Terminal unless a future explicit contract says otherwise:

```text
SUCCEEDED
SKIPPED_DUE_TO_PREREQUISITE
CANCELLED
```

`FAILED` is terminal for the current attempt, but the same StageExecution may start a new attempt after retry authorization.

## 9.3 Invalid transitions

At minimum reject:

* SUCCEEDED → RUNNING
* CANCELLED → RUNNING
* SKIPPED_DUE_TO_PREREQUISITE → RUNNING
* READY → SUCCEEDED without RUNNING attempt
* PENDING → SUCCEEDED
* second concurrent RUNNING attempt for one StageExecution
* attempt start without a RUNNING canonical Execution / valid owner

## 9.4 Timestamps

At minimum:

* first actual attempt start sets stage `started_at` if unset
* successful/finally failed/cancelled terminalization records `finished_at`
* retry MUST NOT destroy prior attempt timestamps
* stage-level timestamps and attempt-level timestamps must remain semantically distinguishable

---

# 10. Execution ↔ Stage State Consistency

This section is mandatory for `E4-G03-AC-005`.

## 10.1 Claim/lease authority

StageExecution MUST NOT introduce an independent claim/lease system.

While an Execution is claimed:

```text
Execution.lease_owner / lease_expires_at
```

remain the authority.

A state-changing StageExecution mutation performed by a worker MUST be authorized by the current Execution claim owner or by an equivalent canonical owner-checked service operation.

A stale worker MUST NOT be able to mutate stage state after ownership has moved or expired.

## 10.2 RUNNING invariant

A StageExecution may enter `RUNNING` only when:

```text
parent Execution.status == RUNNING
```

and the caller is authorized by the current Execution claim/lease contract.

## 10.3 Execution success

An Execution MUST NOT be marked `SUCCEEDED` while a required canonical stage is:

```text
PENDING
READY
RUNNING
FAILED
```

Required terminal successful set is workflow-valid combinations of:

```text
SUCCEEDED
SKIPPED_DUE_TO_PREREQUISITE
```

Cancellation is not success.

## 10.4 Failure

When a stage attempt fails:

1. the attempt history is finalized;
2. the stage becomes `FAILED`;
3. canonical retry policy decides whether another attempt is permitted;
4. if retry is exhausted/not permitted, the parent Execution becomes `FAILED`;
5. Execution failure persistence and stage failure persistence MUST be transactionally consistent enough that the repository cannot report Execution `SUCCEEDED` with a required failed stage.

No requirement is introduced in G03 to redesign Result/Artifact cleanup.

## 10.5 Cancellation

Execution cancellation semantics from G02 remain authoritative.

Required stage behavior:

* already `SUCCEEDED` stage remains `SUCCEEDED`;
* no new stage attempt may start after parent Execution is `CANCELLED`;
* active/not-yet-started nonterminal stages receive explicit cancellation terminalization according to the G03 stage lifecycle;
* successful prior stage history/output binding metadata is not silently rewritten;
* cancellation does not create a new Execution ID.

## 10.6 Execution retry

G02 rule:

```text
retry = same Execution ID
```

G03 extension:

* existing StageExecution IDs remain the same;
* completed attempt history remains;
* failed stage may receive a new attempt after the Execution is re-claimed;
* a retry MUST NOT create a fresh duplicate StageExecution row for the same `(execution_id, stage_key)`;
* already successful stage state MUST NOT be erased merely to hide prior progress.

Exact restart-point optimization is not a G03 scientific concern; what is mandatory is stable stage identity and auditable attempt history.

---

# 11. Persistent Binding Contract

## 11.1 Queryability

For `E4-G03-AC-002`, repository/application code outside the scientific runner MUST be able to query:

```text
stage status
attempt history
input binding metadata
output binding metadata
failure/cancellation detail
timestamps
```

by at least:

```text
stage_execution_id
execution_id
```

and SHOULD support deterministic ordered listing by execution.

## 11.2 JSON-safe metadata

Persistent input/output bindings MUST be serializable Product metadata.

Do not persist arbitrary Python runner objects directly.

If in-memory runner output contains non-serializable scientific descriptors, persist a normalized JSON-safe orchestration projection or stable references sufficient for audit/query.

## 11.3 G04 boundary

Persistent `output_binding` in G03 MUST NOT become a substitute Result/Artifact metadata authority.

Specifically, G03 MUST NOT:

* define the final ExecutionResult/StageResult semantic model
* make physical object keys semantic Result IDs
* duplicate Product Artifact metadata into StageExecution as a new authority
* change Result/Artifact ownership cardinality beyond what is required to preserve current behavior

G04 will define canonical Result/Artifact ownership.

---

# 12. Repository / Unit of Work Contract

## 12.1 StageExecution repository

Introduce a canonical StageExecution repository port and persistence adapter.

Minimum operations required by G03 semantics include equivalents of:

```text
add / add_many
get(stage_execution_id)
list_for_execution(execution_id)
update with state validation / owner authorization
query attempt history
append/start/finalize attempt through canonical service/repository
```

Exact method names may follow repository conventions.

## 12.2 Unit of Work

Canonical Product `UnitOfWork` MUST expose the canonical StageExecution repository.

Execution + stage materialization at submission MUST be committed within one UoW boundary.

Stage + Execution state changes that must remain consistent SHOULD use one UoW transaction where practical.

## 12.3 No second UoW

Do not create family-specific UoWs or Causal-only StageExecution UoW.

## 12.4 Persistence reconstruction

Repository round-trip MUST reconstruct:

* StageExecution identity/owner
* status
* stage key/type/order/dependencies
* input/output binding metadata
* last error
* timestamps
* ordered attempt history

---

# 13. GenericExecutor Boundary

## 13.1 Allowed responsibilities

`GenericExecutor` MAY own:

* plan validation
* stage ordering
* dependency-ready sequencing
* binding resolution
* runner registry lookup
* runner validation/invocation
* non-authoritative in-memory stage outcome production
* cancellation signal observation sufficient to stop runner sequencing

## 13.2 Forbidden responsibilities

`GenericExecutor` MUST NOT own or invoke:

```text
canonical Execution claim
lease acquisition/renewal
Execution identity creation
UnitOfWork commit
SQLAlchemy Session commit
canonical StageExecution persistence
canonical StageExecution retry policy
Execution retry policy
Result persistence
Artifact metadata persistence
generic lineage persistence
```

It MUST NOT be the component that decides canonical `max_attempts`.

## 13.3 API cleanup

The current `GenericExecutor` API MUST be reshaped so that persistence/retry authority is not injectable through ambiguous callbacks.

In particular:

* a generic DB/persistence `commit` callback MUST NOT remain part of its canonical contract;
* a canonical `retryable` policy callback MUST NOT remain part of its canonical contract;
* `GenericExecutor` SHOULD return an explicit non-persistent outcome DTO rather than treating canonical persistent `StageExecution` entities as its owned state.

A transient cleanup/compensation callback MAY remain only if it is demonstrably runner-local and does not persist Product lifecycle, Result, Artifact metadata, or lineage.

## 13.4 No persistence imports

`ariadne.product.workflow.executor` and equivalent GenericExecutor implementation MUST NOT import:

* Product UnitOfWork
* repository persistence adapters
* ORM models / SQLAlchemy session
* Result repository
* Artifact metadata repository
* claim repository/service
* migration/database code

Static architecture test MUST enforce this boundary.

---

# 14. Canonical Stage Orchestration Service

G03 requires one canonical application-layer owner for persistent stage lifecycle.

The exact class/file name may follow repository conventions.

Its responsibilities include:

1. materialize StageExecution children from the family plan;
2. load ordered persistent stages;
3. validate parent Execution state and owner;
4. mark stage ready/running;
5. open/finalize attempt records;
6. invoke GenericExecutor/runner infrastructure without giving it persistence authority;
7. persist stage outcome;
8. decide/refer retry policy outside GenericExecutor;
9. propagate final stage failure/cancellation consistently to Execution;
10. preserve G02 claim/lease contract.

It MUST NOT become a new Result/Artifact ownership authority in G03.

---

# 15. Family Workflow Adapter Contract

A canonical family → workflow plan mapping MUST exist for:

```text
CAUSAL
EXPLORATORY
PREDICTIVE
```

Required common stage-definition information:

```text
stage_key
stage_type
ordinal / deterministic order
dependencies
enabled/executable decision
runner selection information
resource/runtime policy only where it does not become canonical retry authority
```

Family-specific runner registration/scientific implementation remains behind the adapter.

No duplicate StageExecution repository/service per family.

---

# 16. Product Migration Contract

## 16.1 Required migration

G03 schema persistence requires a Product migration.

Expected revision at baseline:

```text
20260809_product_0008
```

The migration MUST be in:

```text
product_migrations/
```

or the repository's current Product migration path used by `alembic_product.ini`.

## 16.2 Required schema outcome

The migration MUST create canonical persistence sufficient for:

```text
StageExecution
StageAttempt history
Execution ownership FK
status
stage plan metadata
bindings
errors
timestamps
required uniqueness constraints
```

## 16.3 Product-only chain

Verification must use:

```bash
alembic -c alembic_product.ini upgrade head
```

through the standardized PostgreSQL runner.

Do not execute root legacy migration chain as part of G03 verification.

## 16.4 Existing data

Project policy is pre-production clean rebuild.

G03 does not require historical backfill from old Causal/Family stage tables.

Do not add broad dual-read/data-copy machinery for hypothetical production data retention.

---

# 17. Automated Test Code Contract

Coding Agent MUST add/update automated tests that directly map to all G03 ACs.

Recommended Gate-local test files:

```text
tests/product/test_enh_e4_g03_persistent_stage_execution.py
tests/product/test_enh_e4_g03_generic_executor_boundary.py
```

The exact split may differ, but report MUST provide exact AC → pytest node mapping.

## 17.1 AC-001 coverage

Must prove for canonical:

```text
CAUSAL
EXPLORATORY
PREDICTIVE
```

that a committed canonical Execution has persistent StageExecution child/children.

At least one real PostgreSQL integration test MUST verify persistence, not only in-memory fake repository behavior.

## 17.2 AC-002 coverage

Must prove repository/application query can reconstruct:

* state
* ordered attempt history
* input binding
* output binding
* error/timestamps

without invoking a scientific runner.

## 17.3 AC-003 coverage

Must include static/architecture assertion that `GenericExecutor` has no persistence/claim/retry authority.

Must include behavior showing one runner failure does not cause GenericExecutor itself to execute canonical retry policy.

## 17.4 AC-004 coverage

Must include negative lifecycle test:

* empty/missing Causal canonical stage plan cannot commit a valid new canonical Execution;
* stage materialization failure rolls back parent Execution creation;
* Family-only persistence does not satisfy canonical Causal creation.

## 17.5 AC-005 coverage

Must test at least:

* stage failure → Execution failure when retry not allowed
* stage retry preserves Execution ID + StageExecution ID and appends attempt
* cancellation prevents new attempts and leaves no stale `RUNNING` stage
* stale/wrong lease owner cannot mutate current stage state
* Execution cannot become `SUCCEEDED` with required failed/nonterminal stage

## 17.6 Regression

G02 core regression remains mandatory:

```text
tests/product/test_enh_e4_g02_canonical_execution.py
tests/product/test_postgres_contract.py
```

Do not weaken G02 claim/concurrency assertions to make G03 pass.

---

# 18. Standardized Test PostgreSQL Infrastructure

## 18.1 Sole PostgreSQL entry point

For any G03 self-check requiring real PostgreSQL, use:

```bash
scripts/test/run_product_postgres_tests.sh <pytest-path-or-node> [pytest-options]
```

Example:

```bash
scripts/test/run_product_postgres_tests.sh \
  tests/product/test_enh_e4_g03_persistent_stage_execution.py
```

Combined regression example:

```bash
scripts/test/run_product_postgres_tests.sh \
  tests/product/test_enh_e4_g03_persistent_stage_execution.py \
  tests/product/test_postgres_contract.py \
  tests/product/test_enh_e4_g02_canonical_execution.py
```

## 18.2 What the command owns

The repository-managed command owns:

```text
test-only image build
database_test start/reuse
health readiness
clean ariadne_test reset
Product migration upgrade head
migration current/head verification
requested pytest invocation
raw evidence
metadata evidence
pytest exit status propagation
```

## 18.3 Forbidden G02-style manual reconstruction

Do NOT replace the standard command with:

```text
manual docker run
manual Docker network inspection
127.0.0.1 / 172.17.0.1 route probing
manual DSN export
manual psql DB recreation
manual alembic
manual pytest
hand-built evidence
```

## 18.4 Agent Docker restriction

If the Coding Agent environment cannot access Docker:

* do not classify product implementation as FAIL solely for that reason;
* do not modify test infrastructure to bypass isolation;
* execute non-PostgreSQL tests that are available;
* record the unavailable PostgreSQL self-check as an environment limitation in the Implementation Completion Report;
* leave independent real PostgreSQL verification to the Test Agent / Human one-command fallback defined by 07.

This does not waive required automated test code.

---

# 19. Allowed Change Areas

Expected/allowed areas include, as required by the chosen minimal implementation:

```text
src/ariadne/product/domain/stage_execution.py
src/ariadne/product/domain/enums.py
src/ariadne/product/ports/repositories.py
src/ariadne/product/ports/unit_of_work.py
src/ariadne/product/workflow/
src/ariadne/product/application/
src/ariadne/interfaces/worker/
current Product persistence ORM/repository adapters
current Product family workflow adapters/planners
product_migrations/
tests/product/
docs/wiki/develop_memo/_work/
  20260808-01_ENH-E4_eliminate_dual_execution/
  20_implementation_reports/G03/
20_implementation_reports/ENH-E4_implementation_report_detail.md
```

Only change files actually required by G03.

---

# 20. Forbidden Change Areas

Unless needed only to preserve compile/import compatibility, do not modify:

```text
legacy runtime roots
legacy migration chain
shared scientific algorithm implementations
frontend
auth
dataset ingestion semantics
Result semantic model for G04
Artifact metadata authority for G04
lineage authority for G06
CLI architecture for G07
deployment production topology
G03 Preflight infrastructure
```

A minimal compatibility import adjustment is allowed only if unavoidable and must be reported.

---

# 21. Acceptance Criteria

These are the authoritative Gate ACs.

## E4-G03-AC-001

> 全canonical Execution familyにpersistent StageExecution childがある。

Verification concept:

```text
schema / structural audit
cross-family PostgreSQL lifecycle
```

PASS requires canonical Causal / Exploratory / Predictive new writes all materialize persistent stage children.

## E4-G03-AC-002

> stage state/attempt/input/outputがrunner外からqueryできる。

Verification concept:

```text
repository / application query test
```

PASS requires persistence round-trip independent of runner internals.

## E4-G03-AC-003

> GenericExecutorはplan/stage/runner outcomeのみを扱う。

Verification concept:

```text
import / ownership audit
behavior test
```

Mandatory negative:

```text
no DB commit
no claim
no Result persistence
no Artifact metadata persistence
no canonical retry policy
```

from `GenericExecutor`.

## E4-G03-AC-004

> Causalにstageが欠落し、Familyだけstageを持つ状態を新規writeで作れない。

Verification concept:

```text
negative lifecycle / transaction test
```

Canonical Causal creation without materialized stage MUST fail atomically.

## E4-G03-AC-005

> stage failure/cancel/retryのstateがExecution stateと整合する。

Verification concept:

```text
behavioral regression
owner/lease negative tests
```

Stage lifecycle must not contradict parent Execution lifecycle.

---

# 22. Negative Acceptance Criteria

Any of the following is an implementation defect:

* canonical Causal Execution can be committed with zero StageExecution children
* only Exploratory/Predictive have persistent stages
* StageExecution exists only as an in-memory dataclass
* stage attempt history disappears after retry
* retry creates a new StageExecution ID for the same canonical stage
* `GenericExecutor` calls UoW/DB commit
* `GenericExecutor` claims or renews Execution lease
* `GenericExecutor` owns canonical retry policy
* `GenericExecutor` persists Result/Artifact metadata
* stale lease owner can update a StageExecution
* parent Execution reports `SUCCEEDED` while a required stage is failed/nonterminal
* parent cancellation permits a new stage attempt
* cancellation is silently mislabeled as prerequisite skip
* G03 introduces a second family-specific StageExecution persistence authority
* G03 changes root legacy migration
* G03 reintroduces manual PostgreSQL verification workflow
* G03 closes TD-001 or TD-002 prematurely
* G03 performs G04/G05/G06/G07/G08 work

---

# 23. Transition Debt

## 23.1 Existing debt

Keep OPEN:

```text
E4-TD-001
Introduced: G02
Exit Gate: G05
Authority: old Causal/Family new Execution writes
```

G03 MUST NOT close it.

## 23.2 New debt

Introduce and record:

```text
E4-TD-002
Introduced: G03
State: OPEN until G05
Authority: old stage persistence / ephemeral behavior
Exit Gate: G05
Exit criterion: all canonical families use persistent StageExecution through converged Product paths
```

## 23.3 Interpretation

At G03 PASS:

* canonical StageExecution contract is implemented and testable across all canonical family values;
* old/transitional stage behavior may still exist behind non-converged paths;
* G05 remains responsible for eliminating those old new-write authorities and closing TD-001/TD-002.

Do not confuse bounded transition debt with a license to create new dual architecture.

---

# 24. Passed-Gate Regression Contract

G03 modifies code near G02 execution/worker lifecycle, so G02 regression is mandatory.

At minimum preserve:

* canonical Execution family discriminator
* one claim abstraction
* atomic PostgreSQL claim
* lease owner/expiry
* owner-checked mutation
* retry same execution ID
* rerun/revise new execution ID
* cancel terminal behavior

If G03 requires changing a G02 file, Implementation Completion Report MUST state:

```text
affected passed Gate
changed file/component
why change was necessary
which G02 contract is preserved
which regression test proves it
```

---

# 25. Coding Agent Self-check

Before `READY_FOR_TEST`, run as much as environment permits.

## 25.1 Static / unit

Example:

```bash
uv run pytest \
  tests/product/test_enh_e4_g03_generic_executor_boundary.py
```

Run any directly affected existing unit/component/worker tests.

## 25.2 Real PostgreSQL

Use only:

```bash
scripts/test/run_product_postgres_tests.sh \
  tests/product/test_enh_e4_g03_persistent_stage_execution.py \
  tests/product/test_postgres_contract.py \
  tests/product/test_enh_e4_g02_canonical_execution.py
```

The exact node list may be extended based on changed code.

Do not substitute manual PostgreSQL commands.

## 25.3 Self-check is not Gate PASS

Coding Agent self-check can support `READY_FOR_TEST`.

Only independent 07 Test Agent can produce G03 Gate Decision.

---

# 26. Implementation Completion Conditions

Coding Agent may declare `READY_FOR_TEST` only when all implementation conditions are met:

1. G03 scope implementation is complete.
2. Product migration for persistent StageExecution is present.
3. canonical Execution creation materializes stage children atomically.
4. Causal / Exploratory / Predictive canonical family values are supported.
5. StageExecution repository/UoW persistence exists.
6. stage attempt history is persistent/queryable.
7. input/output binding metadata is queryable outside runners.
8. cancellation has explicit persistent stage representation.
9. retry preserves Execution ID and StageExecution ID while appending attempts.
10. claim/lease owner controls stage mutation.
11. GenericExecutor no longer owns persistence/claim/canonical retry policy.
12. AC-001〜005 each have automated test code.
13. G02 regression tests are not weakened.
14. Product-only migration contract is preserved.
15. G03 Preflight test infrastructure is not bypassed.
16. E4-TD-001 remains OPEN.
17. E4-TD-002 is recorded OPEN until G05.
18. G04+ scope is not implemented.
19. implementation commit is created.
20. Gate-local Implementation Completion Report is created.
21. cumulative implementation ledger is updated.
22. unrelated working-tree artifact is not included.
23. any unavailable Docker/PostgreSQL self-check is explicitly recorded as environment limitation, not hidden.

Coding Agent self-check PASS does not mean E4-G03 PASS.

---

# 27. Required Outputs

## 27.1 Implementation commit

Create one implementation commit that fixes:

```text
production source
automated test source
Product migration
```

for G03 Trial 01.

Do not mix unrelated working-tree artifacts.

Record full SHA.

## 27.2 Gate-local Implementation Completion Report

Create:

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
20_implementation_reports/G03/
E4-G03_01_implementation_completion_report.md
```

Use the repository implementation completion report template/specification.

Status must be one of:

```text
READY_FOR_TEST
DESIGN_BLOCKED
```

Do not write PASS/FAIL/BLOCKED as Coding Agent Gate Decision.

The report MUST include:

* baseline full SHA
* starting full SHA
* implementation full SHA
* migration previous/new head
* changed files
* exact schema/repository/application boundary
* GenericExecutor API changes
* family plan materialization mechanism
* cancellation/retry semantics
* claim/lease-stage ownership semantics
* AC → exact pytest node mapping
* self-check commands/exit codes
* standardized PostgreSQL evidence path if executed
* E4-TD-001 state
* E4-TD-002 state
* passed-Gate changes/regressions
* known limitations
* unrelated working-tree state

## 27.3 Cumulative implementation ledger

Update the existing enhancement-wide ledger if present:

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
20_implementation_reports/
ENH-E4_implementation_report_detail.md
```

Add G03 implementation facts without rewriting prior Gate evidence.

## 27.4 Report commit

A report-only commit may follow the implementation commit.

The Test Agent MUST still test the fixed implementation commit.

---

# 28. Git Integrity Rules

Before implementation commit:

```bash
git status --short
git diff --check
```

Inspect staged files:

```bash
git diff --cached --name-status
```

The unrelated NFS artifact MUST NOT be staged.

After commit, record:

```bash
git rev-parse HEAD
git status --short
```

If report is committed separately, distinguish:

```text
implementation commit
report commit
```

---

# 29. Stop Conditions

## READY_FOR_TEST

All Implementation Completion Conditions are met.

Then:

* implementation commitを固定
* G03 completion reportを作成
* Test Agentへhandoff可能にする
* **Test Agent作業を自分で開始しない**
* **G04へ進まない**

## DESIGN_BLOCKED

Current architecture contractだけでは解消不能なsemantic contradictionがある。

Reportへ最低限:

* conflicting contract
* current source evidence
* why implementation choice requires new architecture decision
* minimum human decision required
* partial changes, if any
* whether implementation commit exists

を記録し、停止する。

Environment-only Docker access failureは自動的に `DESIGN_BLOCKED` ではない。

---

# 30. Primary Risk Focus

G03の主眼は「StageExecutionというclassをDBへ保存した」だけではない。

PASS可能なarchitectureは:

```text
one canonical Execution authority
        │
        └─ persistent, auditable StageExecution children
                 │
                 ├─ stable stage identity
                 ├─ append-preserving attempt history
                 ├─ queryable bindings/state
                 └─ owner-checked lifecycle
                          │
                          v
                 GenericExecutor
                 = workflow/runner infrastructure only
```

である。

次の状態はG03未達である。

```text
Causal stage = still ephemeral
Family stage = persistent
GenericExecutor = retry/lifecycle owner
```

また、G03でold pathsを全面削除してG05まで先取りすることも誤りである。

E4-TD-002を明示して、**canonical contractの成立**と**後続convergence**を分離すること。
