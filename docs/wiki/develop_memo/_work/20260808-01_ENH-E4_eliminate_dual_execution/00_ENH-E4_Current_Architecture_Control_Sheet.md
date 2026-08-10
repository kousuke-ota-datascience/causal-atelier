# ENH-E4 Current Architecture Control Sheet

> **Purpose:** ENH-E4「二重アーキテクチャ解消」の現在地を、開発者・Coding Agent・Test Agent が短時間で把握するための control plane。
>
> **This document is NOT a new source of truth.**
> 詳細な semantic contract は Architecture Decision Record / Gate-local `06`・`07` / passed Gate Decision / verified source code を正本とする。
> 本書はそれらの **現在状態・authority・未完了領域・traceability への索引** を圧縮したものである。

---

## 0. Control Metadata

| Item                                    | Current Value                                   |
| --------------------------------------- | ----------------------------------------------- |
| Project                                 | Ariadne / causal-atelier                        |
| Enhancement                             | ENH-E4 eliminate dual execution                 |
| Branch                                  | `refactor/ariadne_mvp_e4`                       |
| Control Sheet Snapshot                  | **after E4-G08 Trial01 PASS / ENH-E4 COMPLETE** |
| G07 fixed implementation/test candidate | `8e4d7cd6119bc995fca7ea44183bfc7d13ed3445`      |
| G08 fixed implementation/test candidate | `a6c3211d9873632c6e8a19d6c8db71a33d4bb6ef`      |
| G08 Independent Test execution HEAD     | `40bc30fb38e09221af2d421007c280c910b55dbd`      |
| G08 Independent Test Contract           | `bd2386e1f4df93c387422f38123ef5193d86832a`      |
| Product migration head                  | `20260809_product_0010`                         |
| Current Gate                            | **NONE — ENH-E4 COMPLETE**                      |
| OPEN Transition Debt                    | **`0`**                                         |
| G08 Test Items                          | `001–007 PASS`                                  |
| G08 Acceptance Criteria                 | `AC-001..005 PASS`                              |
| G08 Blocking Findings                   | `NONE`                                          |
| Material Unknown                        | `NONE`                                          |
| Final ENH-E4 Decision                   | **PASS**                                        |

### Snapshot Evidence

```text
30_test_report/G08/Trial01/
E4-G08_01_999_gate_decision.md

20_implementation_reports/G08/Trial01/
E4-G08_01_implementation_completion_report.md

20_implementation_reports/G08/Trial01/packages/
E4-G08_01_P01_implementation_checkpoint_report.md
E4-G08_01_P02_implementation_checkpoint_report.md
E4-G08_01_P03_implementation_checkpoint_report.md

30_test_report/G07/Trial01/
E4-G07_01_999_gate_decision.md

30_test_report/G06/Trial01/
E4-G06_01_999_gate_decision.md

40_operator_prompts/architecture_review/
06_target_architecture_decision_record_result.md
07_gate_decomposition_result.md
```

---

# 1. How to Read This Sheet

## 1.1 Status Vocabulary

| Status                       | Meaning                                                                                                                 |
| ---------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| **ESTABLISHED**              | production contract が実装され、Independent Test により Gate-level で検証済み。                                                        |
| **CLOSED**                   | Transition Debt または bounded transition が formal exit criterion を満たし、Independent Test により close 済み。                      |
| **ARCHIVED_NON_AUTHORITY**   | physical/read compatibility surface は残るが、active Product authority ではなく non-authoritative projection として明示的に archive 済み。 |
| **RETIRED_UNREACHABLE**      | physical source/history は存在し得るが、canonical Product runtime/deployment/bootstrap から authority として到達不能。                    |
| **HISTORY_ONLY**             | historical surface として保持。active Product authority ではない。                                                                 |
| **RETAIN_SHARED_CAPABILITY** | shared/scientific capability として意図的に保持。retired orchestration authority とは別物。                                            |
| **LOW_LEVEL_UTILITY**        | canonical Product lifecycle の外側にある standalone non-persistent utility。                                                   |

`TARGET FIXED` / `PENDING` / `TRANSITION OPEN` は ENH-E4 final state には残っていない。

## 1.2 Precedence

矛盾が見つかった場合の優先順:

```text
1. Passed Gate-local 06/07 contract + final Gate Decision
2. Target Architecture ADR / Invariant / Requirement / Constraint
3. Verified current source / Product migration
4. This Control Sheet
```

本書が上位 source of truth と矛盾した場合、**本書を修正する**。
上位 source of truth を本書に合わせて変更しない。

---

# 2. Executive Architecture Snapshot

## 2.1 Final Target

```text
Product API / auditable promoted CLI
              │
              v
     Canonical Execution Service
              │
              v
     Canonical Execution Aggregate
     ├─ execution_id
     ├─ family = CAUSAL | EXPLORATORY | PREDICTIVE
     ├─ lifecycle / claim / lease
     ├─ retry / rerun / revise / cancel
     │
     ├─ Persistent StageExecution
     │      └─ family workflow adapter
     │             └─ GenericExecutor
     │                    └─ shared scientific runner
     │
     ├─ ExecutionResult / StageResult
     │
     ├─ Product Artifact metadata
     │      └─ ArtifactStorePort / physical object store
     │
     └─ Lineage
            ├─ typed structural authority
            ├─ generic-only persisted authority
            └─ closure/export = read projection only

Legacy API / CLI / worker / persistence
    = retired / unreachable from canonical Product runtime
    = historical or archived compatibility role only where explicitly classified

Shared scientific implementation
    = retained independently

Canonical bootstrap
    = Product migrations only
```

## 2.2 What Is Actually Established Now

```text
Canonical Product runtime for new Product analysis             ESTABLISHED

Canonical Execution identity/lifecycle/claim/lease             ESTABLISHED
Persistent StageExecution across all 3 families                ESTABLISHED
GenericExecutor subordinate workflow-only boundary             ESTABLISHED

Explicit ExecutionResult / StageResult levels                  ESTABLISHED
Canonical Result/Artifact typed ownership contract             ESTABLISHED
Artifact semantic ID != object_key                             ESTABLISHED
ArtifactStore physical/metadata boundary                       ESTABLISHED
Store/DB compensation + reconciliation contract                ESTABLISHED
Typed downstream Result reuse role/context                     ESTABLISHED

CAUSAL Product submission -> canonical Execution               ESTABLISHED
EXPLORATORY Product submission -> canonical Execution          ESTABLISHED
PREDICTIVE Product submission -> canonical Execution           ESTABLISHED
One canonical claim authority across all 3 families            ESTABLISHED
Canonical Result/Artifact new-write path across all families   ESTABLISHED

Old FamilyExecution / Stage / Result / Artifact
new Product write authority                                    NONE

Canonical failure -> old Product authority fallback            NONE
GenericExecutor Product lifecycle/output authority             NONE

Typed structural lineage authority                             ESTABLISHED
Generic-only persisted semantic lineage authority              ESTABLISHED
Structural relation generic duplicate authority                NONE
Closure/export lineage authority                               NONE

Canonical Product runtime -> retired legacy dependency         NONE
Repository-managed deployment -> retired legacy invocation     NONE
Canonical Product bootstrap -> root legacy migration           NONE

Shared scientific capability                                   ESTABLISHED / RETAINED
Standalone scientific CLI                                      ESTABLISHED / LOW_LEVEL_UTILITY

Compatibility/read transition debt                             NONE
OPEN TRANSITION DEBT                                           0

Clean Product bootstrap + application startup                  ESTABLISHED
Three-family final Golden Path                                 ESTABLISHED
Mutation + lineage final verification                          ESTABLISHED
Final authority audit                                          ESTABLISHED

ENH-E4                                                         COMPLETE
```

G05 により、Execution / StageExecution / Result / Artifact に対する **sole new Product authority** が確立された。

G06 により、structural lineage に対する **single authority model** が確立され、generic representation との dual authority は解消された。

G07 により、legacy runtime / deployment / Product bootstrap boundary が確立され、shared scientific capability と standalone scientific CLI の role が確定した。

G08 により、これらすべてが one final candidate 上で integrated verification され、`TD-006` が formal `CLOSED`、`OPEN TRANSITION DEBT = 0` となった。

Physical legacy source、historical migrations、compatibility/read projections が残存する場合も、それらは active Product authority ではない。

---

# 3. Gate Progress

| Gate      | Name                                          | Status   | Architecture Established / Purpose                                                                                               |
| --------- | --------------------------------------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------- |
| G01       | Canonical contract/schema foundation          | **PASS** | target domain/schema contracts, relation authority allowlist, traceability foundation                                            |
| G02       | Canonical Execution aggregate and claim       | **PASS** | canonical Execution identity, family discriminator, lifecycle, claim/lease, retry/rerun/revise/cancel                            |
| Preflight | Test PostgreSQL infrastructure                | **PASS** | repository-managed isolated real PostgreSQL verification path                                                                    |
| G03       | Persistent StageExecution and runner boundary | **PASS** | persistent stage model for all families; queryable attempt/bindings; GenericExecutor authority removed                           |
| G04       | Result/Artifact ownership boundary            | **PASS** | explicit Result levels; typed Result/Artifact ownership; physical-store separation; compensation/reconciliation; typed reuse     |
| G05       | Product Execution Convergence                 | **PASS** | Causal/Exploratory/Predictive submission, claim, stage, Result and Artifact converge on sole canonical Product authority         |
| G06       | Lineage authority consolidation               | **PASS** | typed structural authority + generic-only persisted authority; structural dual authority removed; closure/export projection only |
| G07       | Legacy, CLI, migration boundary               | **PASS** | retired legacy runtime/deployment boundary; shared science preservation; Product-only bootstrap; standalone CLI boundary         |
| G08       | Final clean bootstrap and architecture audit  | **PASS** | clean bootstrap/startup; three-family Golden Path; mutation/lineage; final authority audit; OPEN TD = 0                          |

### Gate Sequencing Rule

```text
G01 → G02 → G03 → G04 → G05 → G06 → G07 → G08 → COMPLETE
```

ENH-E4 final status:

```text
G01 PASS
G02 PASS
G03 PASS
G04 PASS
G05 PASS
G06 PASS
G07 PASS
G08 PASS

ENH-E4 COMPLETE
```

No later ENH-E4 Gate remains.

---

# 4. Current Authority Map

| Domain                             | Current Canonical State                                                                    | Historical / Non-authoritative Surface                                               | Status                       | Final Control |
| ---------------------------------- | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------ | ---------------------------- | ------------- |
| Product runtime                    | Causal/Exploratory/Predictive Product analysis は canonical Product Execution authority を使用 | physical legacy source は存在し得るが runtime authority ではない                                | **ESTABLISHED**              | final         |
| Execution identity                 | one canonical Product Execution aggregate                                                  | old Causal/Family new Product write authority なし                                     | **ESTABLISHED**              | final         |
| Execution lifecycle                | one common state/claim/lease/mutation contract                                             | family-specific legacy mutation/claim authority なし                                   | **ESTABLISHED**              | final         |
| StageExecution                     | persistent canonical child for CAUSAL/EXPLORATORY/PREDICTIVE                               | old/ephemeral Product stage authority なし                                             | **ESTABLISHED**              | final         |
| GenericExecutor                    | plan/order/binding/runner outcome を担当                                                      | lifecycle/output authority なし                                                        | **ESTABLISHED**              | final         |
| Result                             | explicit `EXECUTION_RESULT` / `STAGE_RESULT`; typed canonical ownership                    | Causal/Family new Product Result authority なし                                        | **ESTABLISHED**              | final         |
| Artifact metadata                  | canonical typed ownership; `artifact_id` = semantic identity                               | Causal/Family new Product Artifact metadata authority なし                             | **ESTABLISHED**              | final         |
| Physical Artifact storage          | `ArtifactStorePort`; physical locator と Product identity を分離                               | DB/store non-atomicity は compensation/reconciliation で処理                             | **ESTABLISHED**              | final         |
| Typed downstream reuse             | Result ID + typed role/context; Artifact ID                                                | authoritative physical-key/untyped fallback なし                                       | **ESTABLISHED**              | final         |
| Family read projection             | family-specific URL/DTO/read surface は canonical data を projection 可                       | current compatibility consumers 向け projection は non-authoritative                    | **ARCHIVED_NON_AUTHORITY**   | final         |
| Lineage                            | typed structural authority + approved generic-only persisted authority                     | structural generic duplicate authority なし                                            | **ESTABLISHED**              | final         |
| Closure/export                     | derived read projection / traversal                                                        | independent lineage authority なし                                                     | **ESTABLISHED**              | final         |
| Legacy runtime                     | canonical Product runtime/deployment から非到達                                                 | physical `src/ariadne/legacy/` 等は historical residue として存在可能                         | **RETIRED_UNREACHABLE**      | final         |
| Shared science                     | legacy orchestration から独立して利用可能                                                            | scientific implementation を継続利用                                                      | **RETAIN_SHARED_CAPABILITY** | final         |
| Migration/bootstrap                | `alembic_product.ini -> product_migrations/`; head `0010`                                  | root legacy migrations は historical                                                  | **ESTABLISHED**              | final         |
| Root `alembic.ini` / `migrations/` | canonical Product bootstrap authority なし                                                   | historical migration surface                                                         | **HISTORY_ONLY**             | final         |
| Low-level scientific CLI           | persistent Product lifecycle の外側                                                           | standalone scientific utility として存続                                                  | **LOW_LEVEL_UTILITY**        | final         |
| Auditable Product submission       | canonical Execution submission boundary                                                    | alternate lifecycle authority なし                                                     | **ESTABLISHED**              | final         |
| Compatibility/read projection      | canonical authority の read projection のみ                                                   | current consumers が存在する historical reader を non-authoritative projection として archive | **ARCHIVED_NON_AUTHORITY**   | TD-006 CLOSED |

---

# 5. Passed-Gate Contracts That Must Not Regress

## 5.1 G02 — Execution Contract

以下は protected architecture である。

```text
one canonical Execution identity

family discriminator:
    CAUSAL
    EXPLORATORY
    PREDICTIVE

one shared lifecycle/state contract
one repository/service claim authority
atomic claim
explicit lease owner / expiry
owner-checked mutation

retry:
    same Execution ID

rerun:
    new Execution ID
    typed source relation

revise:
    new Execution ID
    typed base relation

cancel:
    terminal canonical Execution transition

GenericExecutor:
    != claim/lifecycle authority
```

### G05 convergence status

```text
E4-TD-001 = CLOSED by G05
```

G05 により、new Product identity / lifecycle / claim authority が old Causal/Family authority へ fallback しないことが independently verified された。

G08 final regression でもこの contract は維持された。

---

## 5.2 G03 — Stage Contract

以下は protected architecture である。

```text
Every canonical Execution family has persistent StageExecution children.

StageExecution is queryable outside scientific runner internals:
    stage identity
    stage state
    input/output binding metadata
    attempt history
    error/timestamps

Retry:
    same Execution ID
    persistent StageExecution semantics
    append attempt history

Execution ↔ Stage state must remain consistent.

Stage mutation:
    governed by canonical Execution claim/lease ownership

GenericExecutor:
    MAY:
        plan validation
        stage ordering
        binding resolution
        runner invocation
        detached/in-memory outcome

    MUST NOT:
        claim Execution
        own lease
        commit Product DB/UoW
        own canonical StageExecution lifecycle
        decide canonical retry policy
        own canonical Result/Artifact persistence
```

### G05 convergence status

```text
E4-TD-002 = CLOSED by G05
```

全3 Product families が canonical claim/lease authority 配下の persistent StageExecution を使用する。

Legacy stage source が physical に存在しても、それは new Product stage authority ではない。

G08 final Golden Path でもこの contract は維持された。

---

## 5.3 G04 — Result / Artifact Ownership Contract

以下は protected architecture である。

```text
Result semantic level:
    EXECUTION_RESULT
    STAGE_RESULT

ExecutionResult:
    belongs to canonical Execution
    must not carry StageExecution association

StageResult:
    belongs to canonical Execution
    must carry canonical StageExecution association
    stage.execution_id == result.execution_id

Result level != scientific result_type

Artifact:
    artifact_id = semantic Product identity
    object_key = physical ArtifactStore locator
    content_hash = integrity evidence

Canonical execution-output ownership:
    one common Product application/repository boundary
    typed Execution association
    optional typed StageExecution association
    optional typed Result association
    cross-execution mismatches rejected

Physical store:
    ArtifactStorePort remains physical-only
    DB/store failure is compensated/reconciled
    cleanup failure is observable, not silent success

Typed downstream reuse:
    Result reuse = result_id + typed ResultReuseRole/context
    Artifact reuse = artifact_id
    object_key/content_hash cannot substitute semantic identity
```

### G05 convergence status

```text
E4-TD-003 = CLOSED by G05
```

G05 により、Causal / Exploratory / Predictive の new Product Result / Artifact metadata ownership が canonical boundary に収束した。

G08 final Golden Path でも canonical Result / Artifact ownership は維持された。

---

## 5.4 G05 — Product Execution Convergence Contract

以下は protected architecture である。

```text
CAUSAL Product submission
    -> canonical Execution

EXPLORATORY Product submission
    -> canonical Execution

PREDICTIVE Product submission
    -> canonical Execution

All three families:
    one canonical claim / lease authority
    persistent canonical StageExecution
    canonical Result owner
    canonical Artifact metadata owner

FamilyExecution / FamilyStageExecution / FamilyResult / FamilyArtifact:
    no new Product write authority

Canonical processing failure:
    no fallback to old Product authority

Family-facing mutations:
    delegate canonical retry / rerun / revise / cancel semantics

Family-facing read surfaces:
    may remain as adapters/projections
    project canonical authority

GenericExecutor:
    workflow/scientific infrastructure only
    not Product lifecycle / Result / Artifact authority
```

### G05 independent evidence

```text
Trial02 tested implementation:
    ad3e3e124ee47f9cbaa2470b25263b7289795262

Test Items:
    001–010 PASS

Acceptance:
    AC-001 SATISFIED
    AC-002 SATISFIED
    AC-003 SATISFIED
    AC-004 SATISFIED
    AC-005 SATISFIED

Transition Debt:
    TD-001 CLOSED
    TD-002 CLOSED
    TD-003 CLOSED
    TD-004 OPEN -> G06

Blocking findings:
    NONE

Migration head:
    20260809_product_0010
```

### G05 final preservation status

```text
Product Execution convergence:
    PRESERVED THROUGH G08
```

---

## 5.5 G06 — Lineage Authority Consolidation Contract

以下は protected architecture である。

```text
For every lineage semantic relation:

typed structural relation
    -> canonical typed structural authority

approved generic-only semantic relation
    -> generic persisted authority

closure / traversal / export
    -> derived read projection only
```

Authority classification は relation name 単独ではなく semantic tuple により決まる。

Example:

```text
Execution DERIVED_FROM Execution
    = TYPED_STRUCTURAL

Artifact DERIVED_FROM Artifact
    = may be GENERIC_ONLY when explicitly approved
```

Canonical projection:

```text
typed reconstructed structural edges
+
persisted approved GENERIC_ONLY edges
    ->
deduplicated lineage projection
```

Structural relation は generic authority として duplicate persistence しない。

Mutation lineage:

```text
retry:
    same Execution ID
    no lineage authority relation solely because of retry

rerun:
    new Execution ID
    base_execution_id = original
    revision_kind = RERUN
    typed DERIVED_FROM

revise:
    new Execution ID
    base_execution_id = original
    revision_kind = REVISED
    change_reason preserved
    typed REVISED_FROM
```

### G06 independent evidence

```text
Trial:
    E4-G06 Trial01 PASS

Fixed implementation/test candidate:
    9816ed87daec1efcb1c860f0c9c0ebe72fb9bc92

Tested repository state:
    8a4c0042cd766fa182fdc8c5edc346a8e22c807b

Acceptance:
    AC-001 PASS
    AC-002 PASS
    AC-003 PASS
    AC-004 PASS
    AC-005 PASS

Persisted lineage authority audit:
    TYPED_STRUCTURAL generic duplicate = 0
    unapproved persisted relation = 0

Migration head:
    20260809_product_0010
```

### G06 convergence status

```text
E4-TD-004 = CLOSED by G06
```

G08 mutation + lineage verification により、この authority model が final candidate でも維持されていることが再確認された。

---

## 5.6 G07 — Legacy / CLI / Migration Boundary Contract

以下は protected architecture である。

```text
canonical Product runtime
    -> no retired legacy runtime dependency

repository-managed deployment
    -> no retired legacy API / CLI / worker invocation

shared scientific capability
    -> usable independently of retired legacy orchestration

canonical Product bootstrap
    -> Product migration chain only

standalone scientific CLI
    -> low-level non-persistent utility
    -> not Product lifecycle authority
```

Physical legacy source や historical root migrations は、non-authoritative であれば残存可能である。

Classification は filename や terminology ではなく:

```text
runtime reachability
deployment reachability
bootstrap reachability
persistent authority
consumer semantics
```

に基づく。

### G07 independent evidence

```text
E4-G07 Trial01:
    PASS

E4-G07:
    PASS

Fixed implementation/test candidate:
    8e4d7cd6119bc995fca7ea44183bfc7d13ed3445

Independent Test execution HEAD:
    0923461bbc724bbfbc6410b7b18793ff4cf2f491

Independent Test Contract:
    b3d03b270f3c64bf380a37a1934d871ba7406696

Candidate equivalence:
    PASS

Test Items:
    001 Candidate identity                  PASS
    002 Runtime/deployment boundary         PASS
    003 Shared scientific boundary          PASS
    004 Product-only bootstrap              PASS
    005 CLI/compatibility boundary          PASS
    006 Protected G02-G06 regression        PASS
    007 Architecture exit audit             PASS

Acceptance:
    AC-001 PASS
    AC-002 PASS
    AC-003 PASS
    AC-004 PASS
    AC-005 PASS

Protected regression:
    42 local tests PASS
    18 PostgreSQL tests PASS

Product runtime legacy dependency:
    0

Product bootstrap legacy migration dependency:
    0

Material Unknown:
    NONE

Migration head:
    20260809_product_0010
```

### G07 convergence status

```text
E4-TD-005 = CLOSED by G07
E4-TD-006 = handed to G08
```

G08 final authority audit / clean bootstrap でも G07 boundary は維持された。

---

## 5.7 G08 — Final Clean Bootstrap and Architecture Audit Contract

G08 は新しい authority architecture を導入する Gate ではなく、G01–G07 で確立した architecture を one final candidate に対して統合検証する final Gate である。

G08 が検証した contract:

```text
AC-001:
    empty/reset Product DB
    -> Product-only migration
    -> current Product migration head
    -> application/runtime startup

AC-002:
    CAUSAL
    EXPLORATORY
    PREDICTIVE

    each:
        Execution
        StageExecution
        Result
        Artifact

    under same canonical ownership architecture

AC-003:
    retry
    rerun
    revise
    cancel
    +
    canonical lineage authority

AC-004:
    final authority model
    runtime/deployment/bootstrap boundary
    no alternate Product authority

AC-005:
    shared scientific capability preserved
    +
    OPEN TRANSITION DEBT = 0
```

### G08 Independent Test identity

```text
E4-G08 Trial01:
    PASS

E4-G08:
    PASS

Fixed candidate SHA:
    a6c3211d9873632c6e8a19d6c8db71a33d4bb6ef

Independent Test execution HEAD:
    40bc30fb38e09221af2d421007c280c910b55dbd

Independent Test Contract SHA:
    bd2386e1f4df93c387422f38123ef5193d86832a

Candidate equivalence:
    PASS
    execution-relevant diff = documentation only

Product migration head:
    20260809_product_0010
```

### G08 Independent Test results

```text
Item 001 / candidate identity:
    PASS

Item 002 / AC-001 clean bootstrap + startup:
    PASS

Item 003 / AC-002 three-family canonical path:
    PASS

Item 004 / AC-003 mutation + lineage:
    PASS

Item 005 / AC-004 final authority audit:
    PASS

Item 006 / AC-005 shared science + zero debt:
    PASS

Item 007 / protected final regression:
    PASS
```

### G08 execution evidence

```text
Real PostgreSQL G08 selection:
    23 passed

DB reset:
    exit 0

Product migration:
    exit 0

migration current check:
    exit 0

pytest:
    exit 0

Local protected selection:
    106 passed
    2 skipped

Skipped local nodes:
    PostgreSQL-only
    PASS in real PostgreSQL selection

Independent Test Contract ancestor proof:
    PASS
    exit 0
```

### G08 final convergence status

```text
TD-006 = CLOSED

OPEN TRANSITION DEBT = 0

Material Unknown:
    NONE

ENH-E4:
    COMPLETE
```

Historical readers could be physically deleted, but current compatibility consumers are evidenced.

Therefore the supported final state is:

```text
historical compatibility readers
    -> archived non-authoritative projections

not:
    active Product authority

not:
    open Transition Debt
```

---

# 6. Transition Debt — Final Control Register

## 6.1 Active Now

```text
NONE
```

Final:

```text
OPEN TRANSITION DEBT = 0
```

## 6.2 Closed by Passed Gates

| TD        | State      | Closed By | Verified Exit                                                                                                                        |
| --------- | ---------- | --------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| E4-TD-001 | **CLOSED** | G05       | old Causal/Family lifecycle accepts no new Product writes                                                                            |
| E4-TD-002 | **CLOSED** | G05       | all Product paths use persistent canonical StageExecution                                                                            |
| E4-TD-003 | **CLOSED** | G05       | one canonical Result/Artifact new-write ownership boundary                                                                           |
| E4-TD-004 | **CLOSED** | G06       | one authority representation per lineage semantic relation; generic persistence = generic-only; closure/export = projection-only     |
| E4-TD-005 | **CLOSED** | G07       | Product runtime legacy dependency = 0; Product bootstrap legacy migration dependency = 0                                             |
| E4-TD-006 | **CLOSED** | G08       | bounded compatibility/read transition removed or explicitly archived; remaining historical readers are non-authoritative projections |

## 6.3 Final Transition Debt State

```text
TD-001 CLOSED
TD-002 CLOSED
TD-003 CLOSED
TD-004 CLOSED
TD-005 CLOSED
TD-006 CLOSED

OPEN TRANSITION DEBT = 0
```

No Transition Debt remains after ENH-E4.

### Rule Preserved after ENH-E4

```text
No transition debt may become indefinite architecture.
```

Future changes that introduce temporary dual-read/write or compatibility bridges require a new explicit owner / duration / exit criterion / verification contract.

---

# 7. Architecture Decision Index

> Original Phase-06 ADR records retain `PROPOSED_FOR_HUMAN_APPROVAL` metadata.
> For ENH-E4 execution, the target set was subsequently taken forward through G01 and the approved Gate sequence.
> 以下の status は **runtime realization status** を表し、original ADR metadata の rewrite ではない。

| ADR        | Decision                                                         | Final Runtime Realization                                                   |
| ---------- | ---------------------------------------------------------------- | --------------------------------------------------------------------------- |
| E4-ADR-001 | Canonical Product runtime                                        | **ESTABLISHED** — G05 convergence; G07 retirement boundary; G08 final audit |
| E4-ADR-002 | Unified canonical persistent Execution aggregate                 | **ESTABLISHED** — G02/G05/G08                                               |
| E4-ADR-003 | Common Execution identity and mutation semantics                 | **ESTABLISHED** — G02/G05/G06/G08                                           |
| E4-ADR-004 | Persistent StageExecution for canonical workflows                | **ESTABLISHED** — G03/G05/G08                                               |
| E4-ADR-005 | GenericExecutor remains workflow infrastructure                  | **ESTABLISHED** — G03/G05/G06/G08                                           |
| E4-ADR-006 | Explicit Result semantic levels under one ownership contract     | **ESTABLISHED** — G04/G05/G08                                               |
| E4-ADR-007 | One Product Artifact metadata authority, separate physical store | **ESTABLISHED** — G04/G05/G08                                               |
| E4-ADR-008 | Typed authority plus generic-only lineage                        | **ESTABLISHED** — G06/G08                                                   |
| E4-ADR-009 | Legacy runtime retirement/archive boundary                       | **ESTABLISHED** — G07/G08                                                   |
| E4-ADR-010 | Product-only canonical migration/bootstrap                       | **ESTABLISHED** — G07; clean bootstrap/startup G08                          |
| E4-ADR-011 | Standalone CLI boundary                                          | **ESTABLISHED** — G05/G07/G08                                               |
| E4-ADR-012 | Compatibility terminology is non-architectural unless consumed   | **ESTABLISHED** — G07 classification; G08 TD-006 closure                    |

---

# 8. Invariant Status

| Invariant  | Short Meaning                                                              | Final Status                  | Primary Gate    |
| ---------- | -------------------------------------------------------------------------- | ----------------------------- | --------------- |
| E4-INV-001 | one canonical persistent Execution identity                                | **ESTABLISHED**               | G02/G05/G08     |
| E4-INV-002 | family changes workflow, not lifecycle authority                           | **ESTABLISHED**               | G02/G05/G08     |
| E4-INV-003 | retry keeps identity; differs from rerun/revise                            | **ESTABLISHED**               | G02/G06/G08     |
| E4-INV-004 | auditable claim/state transitions                                          | **ESTABLISHED**               | G02/G03/G05/G08 |
| E4-INV-005 | centralized claim/lease authority                                          | **ESTABLISHED**               | G02/G05/G08     |
| E4-INV-006 | every canonical Execution has persistent stages                            | **ESTABLISHED**               | G03/G05/G08     |
| E4-INV-007 | GenericExecutor cannot own canonical lifecycle/Result/Artifact persistence | **ESTABLISHED**               | G03/G05/G06/G08 |
| E4-INV-008 | every Result belongs to canonical Execution and declares level             | **ESTABLISHED**               | G04/G05/G08     |
| E4-INV-009 | one Artifact metadata owner; locator distinct                              | **ESTABLISHED**               | G04/G05/G08     |
| E4-INV-010 | DB/store compensation/reconciliation semantics                             | **ESTABLISHED**               | G04/G08         |
| E4-INV-011 | one lineage authority per semantic relation                                | **ESTABLISHED**               | G06/G08         |
| E4-INV-012 | closure/export cannot become lineage authority                             | **ESTABLISHED**               | G06/G08         |
| E4-INV-013 | canonical runtime imports no retired legacy runtime                        | **ESTABLISHED**               | G07/G08         |
| E4-INV-014 | shared science survives without legacy orchestration                       | **ESTABLISHED**               | G07/G08         |
| E4-INV-015 | canonical bootstrap does not invoke root legacy migrations                 | **ESTABLISHED**               | G07/G08         |
| E4-INV-016 | no indefinite dual read/write final architecture                           | **ESTABLISHED — OPEN TD = 0** | G08             |

---

# 9. Requirement Families — Where to Look

35 requirements を通常実装時に個別記憶する必要はない。以下の range を使用する。

| Requirement Range | Concern                                             | Final State                                               |
| ----------------- | --------------------------------------------------- | --------------------------------------------------------- |
| E4-REQ-001..002   | Product runtime / legacy roots                      | **ESTABLISHED G05/G07; final verified G08**               |
| E4-REQ-003..010   | Execution identity/lifecycle/claim/mutations        | **ESTABLISHED G02/G05/G06; final verified G08**           |
| E4-REQ-011..014   | persistent stage / query / GenericExecutor boundary | **ESTABLISHED G03/G05; final verified G08**               |
| E4-REQ-015..020   | Result / Artifact / typed downstream reuse          | **ESTABLISHED G04/G05; final verified G08**               |
| E4-REQ-021..025   | lineage authority                                   | **ESTABLISHED G06; final verified G08**                   |
| E4-REQ-026..029   | shared science / legacy retirement classification   | **ESTABLISHED G07; final verified G08**                   |
| E4-REQ-030..032   | Product-only migration/bootstrap/data policy        | **ESTABLISHED G07; clean bootstrap/startup verified G08** |
| E4-REQ-033..035   | CLI / compatibility terminology                     | **ESTABLISHED G07; compatibility/read TD-006 closed G08** |

Detailed wording:

```text
40_operator_prompts/architecture_review/
06_target_architecture_decision_record_result.md
```

---

# 10. Constraints — Always-On Guardrails

| Constraint | Guardrail                                                                               |
| ---------- | --------------------------------------------------------------------------------------- |
| E4-CON-001 | scientific algorithms は Execution unification の対象外。                                     |
| E4-CON-002 | GenericExecutor を lifecycle owner にしない。                                                 |
| E4-CON-003 | Causal/Family tables を independent **final authority** として残さない。                         |
| E4-CON-004 | physical object key を Result/Artifact semantic ID として使用しない。                             |
| E4-CON-005 | same structural lineage relation を dual-author しない。                                     |
| E4-CON-006 | temporary dual read/write または compatibility transition は bounded かつ exit criterion を持つ。 |
| E4-CON-007 | root legacy migrations を canonical Product bootstrap で実行しない。                            |
| E4-CON-008 | compatibility evidence なしに legacy source を削除しない。                                        |
| E4-CON-009 | legacy-named data contract を terminology だけを理由に rename しない。                             |
| E4-CON-010 | dependency proof なしに unrelated frontend/auth/dataset behavior を変更しない。                   |

これらは ENH-E4 完了後も architecture regression guardrail として有効である。

---

# 11. ENH-E4 — Final State Control Card

## 11.1 Final Objective

> Eliminate the dual `Execution / Result / Lineage` authority architecture and converge Causal / Exploratory / Predictive onto one canonical Product architecture while preserving shared scientific capability and reducing Transition Debt to zero.

Final result:

```text
ACHIEVED
```

## 11.2 Final Architecture

```text
Canonical Product Execution authority                 ESTABLISHED
Persistent StageExecution                             ESTABLISHED
Canonical Result / Artifact ownership                 ESTABLISHED
Three-family Product convergence                      ESTABLISHED
Typed structural lineage authority                    ESTABLISHED
Generic-only semantic lineage authority               ESTABLISHED
Closure/export projection-only boundary               ESTABLISHED
Legacy runtime/deployment retirement boundary         ESTABLISHED
Product-only bootstrap                                ESTABLISHED
Shared science preservation                           ESTABLISHED
Standalone scientific CLI boundary                    ESTABLISHED
Compatibility/read projection non-authority           ESTABLISHED

TD-001                                                CLOSED
TD-002                                                CLOSED
TD-003                                                CLOSED
TD-004                                                CLOSED
TD-005                                                CLOSED
TD-006                                                CLOSED

OPEN TRANSITION DEBT                                  0
```

## 11.3 Final Authority Model

```text
Product lifecycle
    -> canonical Execution

stage lifecycle
    -> persistent StageExecution

workflow/scientific execution mechanism
    -> GenericExecutor
    -> subordinate only

Result authority
    -> canonical Result

Artifact metadata authority
    -> canonical Artifact

physical Artifact storage
    -> ArtifactStorePort

structural lineage
    -> typed structural authority

generic semantic lineage
    -> approved GENERIC_ONLY persistence

closure / traversal / export
    -> derived projection only

Product bootstrap
    -> alembic_product.ini
    -> product_migrations/

shared science
    -> retained independent capability

legacy runtime
    -> retired / unreachable

historical compatibility readers
    -> non-authoritative archived projections
```

## 11.4 Final Audit Question

> Can any canonical Product lifecycle, output, lineage, bootstrap, runtime, or compatibility path act as a second authority alongside the final canonical architecture?

Final verified answer:

```text
NO
```

## 11.5 Final Transition Debt

```text
OPEN TRANSITION DEBT = 0
```

There is no planned ENH-E4 follow-up Gate.

## 11.6 Future Change Rule

Future enhancement がこの architecture を変更する場合、それは ENH-E4 の continuation として暗黙に扱わない。

必要に応じて new enhancement / ADR / Gate contract を作成し、影響を受ける established authority を明示する。

---

# 12. What Is Deliberately Still Unresolved

```text
NONE MATERIAL TO ENH-E4
```

G08 Independent Test により:

```text
No material unknown remains.
```

が formal finding となった。

ただし、次の physical/historical residue は存在可能である。

### Historical compatibility readers

Current compatibility consumers が存在するため、physical deletion は final architecture の必須条件ではない。

Final classification:

```text
ARCHIVED_NON_AUTHORITY
```

Meaning:

```text
read/projection use may remain

but:

no Product lifecycle authority
no new-write authority
no bootstrap authority
no structural lineage authority
no open Transition Debt
```

### Physical legacy source

Physical source の存在は active runtime authority を意味しない。

G07/G08 で canonical Product runtime/deployment からの retirement boundary が verified 済み。

### Root migration history

Root historical migrations の physical existence は canonical Product bootstrap authority を意味しない。

Final canonical Product bootstrap:

```text
alembic_product.ini
    ->
product_migrations/
    ->
20260809_product_0010
```

### Shared scientific implementation

Shared science は cleanup residue ではなく intentional retained capability である。

### Low-level scientific CLI

Standalone scientific CLI は persistent Product lifecycle authority ではなく `LOW_LEVEL_UTILITY` として保持される。

これらは **unresolved architecture debt ではない**。

---

# 13. Evidence / Traceability Index

## Architecture

```text
40_operator_prompts/architecture_review/
06_target_architecture_decision_record_result.md

40_operator_prompts/architecture_review/
07_gate_decomposition_result.md
```

---

## G02

```text
30_test_report/G02/
E4-G02_01_external_postgresql_verification_final_gate_decision.md
```

Key production implementation:

```text
166e90cd1c2d0e523fb863795a88343403d8cc44
```

Final G02 decision ref:

```text
5888783
```

---

## G03

Trial01 failed evidence:

```text
30_test_report/G03/
E4-G03_01_999_gate_decision.md
```

Trial02 implementation:

```text
bac1814bb713f32b859fbe7e2b445fa6cd557f2b
```

Trial02 implementation report:

```text
20_implementation_reports/G03/
E4-G03_02_implementation_completion_report.md
```

Trial02 final decision:

```text
30_test_report/G03/
E4-G03_02_999_gate_decision.md
```

Repository report commit:

```text
852a276
```

---

## G04

Trial01 implementation:

```text
3d88781c1b69ba03bb06c0b8f143612b81feb4bf
```

Trial01 decision:

```text
E4-G04_01_999_gate_decision.md
Decision: FAIL
```

Trial02 implementation:

```text
9c9db4454e0f08c4d46cb002f723ca6827917564
```

Trial02 implementation report:

```text
20_implementation_reports/G04/
E4-G04_02_implementation_completion_report.md
```

Trial02 final decision:

```text
30_test_report/G04/
E4-G04_02_999_gate_decision.md
Decision: PASS
```

Repository evidence commit:

```text
d2b0f311fda209608629114aaae9a1ea142bdd2d
```

---

## G05

Trial01 failed evidence:

```text
30_test_report/G05/
E4-G05_01_999_gate_decision.md
Decision: FAIL
```

Trial02 fixed implementation/test candidate:

```text
ad3e3e124ee47f9cbaa2470b25263b7289795262
```

Trial02 implementation completion report:

```text
20_implementation_reports/G05/Trial02/
E4-G05_02_implementation_completion_report.md
```

Trial02 remediation evidence:

```text
20_implementation_reports/G05/Trial02/
E4-G05_02_R1_predictive_retry_remediation_report.md

20_implementation_reports/G05/Trial02/
E4-G05_02_R2_combined_regression_remediation_report.md
```

Trial02 final decision:

```text
30_test_report/G05/
E4-G05_02_999_gate_decision.md
Decision: PASS
```

Verified summary:

```text
Test Items 001–010: PASS
AC-001..005: SATISFIED
TD-001/002/003: CLOSED
TD-004: OPEN -> G06
Blocking findings: NONE
Migration head: 20260809_product_0010
```

---

## G06

Fixed implementation/test candidate:

```text
9816ed87daec1efcb1c860f0c9c0ebe72fb9bc92
```

Tested repository state:

```text
8a4c0042cd766fa182fdc8c5edc346a8e22c807b
```

Implementation completion report:

```text
20_implementation_reports/G06/Trial01/
E4-G06_01_implementation_completion_report.md
```

Final decision:

```text
30_test_report/G06/Trial01/
E4-G06_01_999_gate_decision.md
Decision: PASS
```

Verified summary:

```text
AC-001..005: PASS
typed structural authority: ESTABLISHED
generic-only persisted authority: ESTABLISHED
structural generic duplicate authority: 0
closure/export authority: 0
TD-004: CLOSED
TD-005: -> G07
Migration head: 20260809_product_0010
```

---

## G07

Fixed implementation/test candidate:

```text
8e4d7cd6119bc995fca7ea44183bfc7d13ed3445
```

Independent Test execution HEAD:

```text
0923461bbc724bbfbc6410b7b18793ff4cf2f491
```

Independent Test Contract:

```text
b3d03b270f3c64bf380a37a1934d871ba7406696
```

Independent Test report commit:

```text
5edf48a2a2fb38aa8bb3bdfb76373e223b1bf7be
```

Implementation completion report:

```text
20_implementation_reports/G07/Trial01/
E4-G07_01_implementation_completion_report.md
```

Final decision:

```text
30_test_report/G07/Trial01/
E4-G07_01_999_gate_decision.md
Decision: PASS
```

Verified summary:

```text
Test Items 001–007: PASS
AC-001..005: PASS

Product runtime legacy dependency:
    0

Product bootstrap legacy migration dependency:
    0

Shared science:
    preserved

Standalone scientific CLI:
    LOW_LEVEL_UTILITY
    non-persistent
    non-lifecycle-authority

Protected regression:
    42 local PASS
    18 PostgreSQL PASS

TD-005:
    CLOSED

TD-006:
    OPEN -> G08

Material Unknown:
    NONE

Migration head:
    20260809_product_0010
```

---

## G08

Fixed implementation/test candidate:

```text
a6c3211d9873632c6e8a19d6c8db71a33d4bb6ef
```

Independent Test execution HEAD:

```text
40bc30fb38e09221af2d421007c280c910b55dbd
```

Independent Test Contract:

```text
bd2386e1f4df93c387422f38123ef5193d86832a
```

Implementation completion report:

```text
20_implementation_reports/G08/Trial01/
E4-G08_01_implementation_completion_report.md
```

Final decision:

```text
30_test_report/G08/Trial01/
E4-G08_01_999_gate_decision.md
Decision: PASS
```

Verified summary:

```text
Item 001:
    PASS

Item 002 / AC-001 clean bootstrap + startup:
    PASS

Item 003 / AC-002 three-family canonical path:
    PASS

Item 004 / AC-003 mutation + lineage:
    PASS

Item 005 / AC-004 final authority audit:
    PASS

Item 006 / AC-005 shared science + zero debt:
    PASS

Item 007 / protected final regression:
    PASS

Real PostgreSQL:
    23 passed

Local protected:
    106 passed
    2 skipped
    skipped nodes passed in PostgreSQL selection

Candidate equivalence:
    PASS

Contract ancestor proof:
    PASS

TD-001:
    CLOSED

TD-002:
    CLOSED

TD-003:
    CLOSED

TD-004:
    CLOSED

TD-005:
    CLOSED

TD-006:
    CLOSED

OPEN TRANSITION DEBT:
    0

Material Unknown:
    NONE

Migration head:
    20260809_product_0010

Final ENH-E4 decision:
    PASS
```

---

# 14. Operational Rules After ENH-E4

## 14.1 Passed Gate Immutability

ENH-E4 completion後、以下は protected architecture として扱う。

```text
G02 canonical Execution authority
G03 persistent StageExecution / GenericExecutor boundary
G04 Result / Artifact ownership
G05 three-family Product convergence
G06 lineage authority
G07 runtime / deployment / bootstrap / CLI boundary
G08 final integrated architecture state
```

Future enhancement がこれらを変更する場合、silent redefinition は行わない。

必要に応じて:

```text
affected Gate / ADR / invariant / requirement
reason
new semantic decision
migration/compatibility impact
regression verification
```

を明示する。

## 14.2 New Enhancement Boundary

ENH-E4 is complete.

新しい architecture change は原則として:

```text
new enhancement
new ADR/decision record when needed
new Gate sequence
```

として扱う。

ENH-E4 の completed Gate を再度 open work queue として使用しない。

## 14.3 Evidence Discipline

Architecture-affecting future change の verification では:

```text
exact command
environment
expected result
actual result
exit code
raw evidence path
Fact
Interpretation
Unknown
PASS / FAIL / BLOCKED
```

を維持する。

Migration/bootstrap/persistence semantics では real PostgreSQL evidence を使用する。

## 14.4 Authority Classification

Future code review では physical residue/name より authority semantics を優先する。

```text
consumer
runtime reachability
deployment reachability
bootstrap reachability
persistent authority
new-write authority
lineage authority
```

に基づいて判断する。

## 14.5 Shared Science Preservation

```text
shared science
!=
retired legacy orchestration
```

Shared scientific implementation は intentional retained capability であり、legacy cleanup の対象として自動分類しない。

## 14.6 Product Bootstrap

Canonical Product bootstrap remains:

```text
alembic_product.ini
    ->
product_migrations/
```

Root historical migration chain を canonical Product bootstrap authority として再導入しない。

## 14.7 Lineage Authority

Final lineage rule:

```text
typed structural relation
    -> typed authority

approved generic-only relation
    -> generic persisted authority

closure/export
    -> projection only
```

Future relation 追加時も one semantic relation / one authority principle を維持する。

---

# 15. Control Sheet Update Rule

ENH-E4 は complete したため、本書は **final ENH-E4 architecture snapshot** である。

今後このファイルを更新するのは、以下の場合に限定する。

1. ENH-E4 evidence の factual correction が必要になった場合。
2. Repository ref/commit/path の traceability correction が必要になった場合。
3. Completed architecture の historical record として annotation が必要になった場合。

Future enhancement により architecture が変更された場合、その current-state control plane は原則として新しい enhancement 側で管理する。

この ENH-E4 Control Sheet を、新しい未検証 architecture の current-state sheet として書き換えない。

---

# 16. Developer Quick Check — 30 Seconds

ENH-E4 final architecture を確認する場合:

```text
1. What is the ENH-E4 state?
   -> COMPLETE
   -> G01-G08 PASS

2. What is the canonical Product lifecycle authority?
   -> Execution

3. What is the canonical stage authority?
   -> persistent StageExecution

4. What owns Product Result / Artifact metadata?
   -> canonical Result / Artifact ownership boundary

5. What is GenericExecutor?
   -> subordinate workflow/scientific execution mechanism
   -> not lifecycle/output authority

6. What is the lineage authority model?
   -> typed structural relation = typed authority
   -> approved generic-only relation = generic persistence
   -> closure/export = projection only

7. What is the canonical Product bootstrap?
   -> alembic_product.ini
   -> product_migrations/
   -> current head 20260809_product_0010

8. Is retired legacy runtime part of canonical Product runtime?
   -> NO

9. Is shared science retired?
   -> NO
   -> RETAIN_SHARED_CAPABILITY

10. Is standalone scientific CLI Product lifecycle authority?
    -> NO
    -> LOW_LEVEL_UTILITY

11. Can historical compatibility readers remain?
    -> YES
    -> only as non-authoritative archived projections

12. What Transition Debt is open?
    -> NONE

13. What is OPEN TRANSITION DEBT?
    -> 0

14. What is the final ENH-E4 decision?
    -> PASS
```

If these answers remain true, the repository remains aligned with the ENH-E4 final architecture.
