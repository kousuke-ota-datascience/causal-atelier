# ENH-E4 Current Architecture Control Sheet

> **Purpose:** ENH-E4「二重アーキテクチャ解消」の現在地を、開発者・Coding Agent・Test Agent が短時間で把握するための control plane。
>
> **This document is NOT a new source of truth.**
> 詳細な semantic contract は Architecture Decision Record / Gate-local `06`・`07` / passed Gate Decision / verified source code を正本とする。
> 本書はそれらの **現在状態・authority・未完了領域・traceability への索引** を圧縮したものである。

---

## 0. Control Metadata

| Item                                    | Current Value                                               |
| --------------------------------------- | ----------------------------------------------------------- |
| Project                                 | Ariadne / causal-atelier                                    |
| Enhancement                             | ENH-E4 eliminate dual execution                             |
| Branch                                  | `refactor/ariadne_mvp_e4`                                   |
| Control Sheet Snapshot                  | **after E4-G07 Trial01 PASS / before G08**                  |
| G06 fixed implementation/test candidate | `9816ed87daec1efcb1c860f0c9c0ebe72fb9bc92`                  |
| G06 tested repository state             | `8a4c0042cd766fa182fdc8c5edc346a8e22c807b`                  |
| G07 fixed implementation/test candidate | `8e4d7cd6119bc995fca7ea44183bfc7d13ed3445`                  |
| G07 Independent Test execution HEAD     | `0923461bbc724bbfbc6410b7b18793ff4cf2f491`                  |
| G07 Independent Test Contract           | `b3d03b270f3c64bf380a37a1934d871ba7406696`                  |
| G07 Independent Test report commit      | `5edf48a2a2fb38aa8bb3bdfb76373e223b1bf7be`                  |
| Product migration head                  | `20260809_product_0010`                                     |
| Current Gate                            | **G08 NEXT — Final clean bootstrap and architecture audit** |
| OPEN Transition Debt                    | `E4-TD-006`                                                 |
| G07 Test Items                          | `001–007 PASS`                                              |
| G07 Acceptance Criteria                 | `AC-001..005 PASS`                                          |
| G07 Blocking Findings                   | `NONE`                                                      |

### Snapshot Evidence

```text
30_test_report/G07/Trial01/
E4-G07_01_999_gate_decision.md

20_implementation_reports/G07/Trial01/
E4-G07_01_implementation_completion_report.md

30_test_report/G07/Trial01/
E4-G07_01_007_architecture_exit_audit.md

30_test_report/G06/Trial01/
E4-G06_01_999_gate_decision.md

20_implementation_reports/G06/Trial01/
E4-G06_01_implementation_completion_report.md

40_operator_prompts/architecture_review/
06_target_architecture_decision_record_result.md
07_gate_decomposition_result.md
```

---

# 1. How to Read This Sheet

## 1.1 Status Vocabulary

| Status                            | Meaning                                                                                              |
| --------------------------------- | ---------------------------------------------------------------------------------------------------- |
| **ESTABLISHED**                   | production contract が実装され、Independent Test により Gate-level で検証済み。                                     |
| **ESTABLISHED / TRANSITION OPEN** | canonical contract は検証済みだが、registered Transition Debt として bounded transition が残る。                    |
| **TARGET FIXED**                  | target semantic contract は確定しているが、runtime/final convergence はまだ Gate-proven ではない。                    |
| **PENDING**                       | future Gate work。current verified architecture として扱わない。                                              |
| **RETIRED_UNREACHABLE**           | physical source/history は存在し得るが、canonical Product runtime/deployment/bootstrap から authority として到達不能。 |
| **HISTORY_ONLY**                  | historical surface として保持。active Product authority ではない。                                              |
| **RETAIN_SHARED_CAPABILITY**      | shared/scientific capability として意図的に保持。retired orchestration authority とは別物。                         |
| **LOW_LEVEL_UTILITY**             | canonical Product lifecycle の外側にある standalone non-persistent utility。                                |

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
    = historical or compatibility role only where explicitly classified

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

Final TD-006 compatibility/read transition resolution          NOT YET FINALIZED
Final clean bootstrap + application startup audit              NOT YET FINALIZED
Final integrated architecture audit                            NOT YET FINALIZED
```

G05 により、Execution / StageExecution / Result / Artifact に対する **sole new Product authority** が確立された。

G06 により、structural lineage に対する **single authority model** が確立され、generic representation との dual authority は解消された。

G07 により、legacy runtime / deployment / Product bootstrap boundary が確立され、shared scientific capability と standalone scientific CLI の役割が明確化された。

Physical legacy source、historical migrations、compatibility/read surfaces が存在すること自体は active Product authority を意味しない。

---

# 3. Gate Progress

| Gate      | Name                                             | Status   | Architecture Established / Purpose                                                                                               |
| --------- | ------------------------------------------------ | -------- | -------------------------------------------------------------------------------------------------------------------------------- |
| G01       | Canonical contract/schema foundation             | **PASS** | target domain/schema contracts, relation authority allowlist, traceability foundation                                            |
| G02       | Canonical Execution aggregate and claim          | **PASS** | canonical Execution identity, family discriminator, lifecycle, claim/lease, retry/rerun/revise/cancel                            |
| Preflight | Test PostgreSQL infrastructure                   | **PASS** | repository-managed isolated real PostgreSQL verification path                                                                    |
| G03       | Persistent StageExecution and runner boundary    | **PASS** | persistent stage model for all families; queryable attempt/bindings; GenericExecutor authority removed                           |
| G04       | Result/Artifact ownership boundary               | **PASS** | explicit Result levels; typed Result/Artifact ownership; physical-store separation; compensation/reconciliation; typed reuse     |
| G05       | Product Execution Convergence                    | **PASS** | Causal/Exploratory/Predictive Product submission, claim, stage, Result and Artifact converge on sole canonical Product authority |
| G06       | Lineage authority consolidation                  | **PASS** | typed structural authority + generic-only persisted authority; structural dual authority removed; closure/export projection only |
| G07       | Legacy, CLI, migration boundary                  | **PASS** | retired legacy runtime/deployment boundary; shared science preservation; Product-only bootstrap; standalone CLI boundary         |
| **G08**   | **Final clean bootstrap and architecture audit** | **NEXT** | final clean bootstrap/startup; three-family Golden Path; mutation/lineage; final authority audit; OPEN TD = 0                    |

### Gate Sequencing Rule

```text
G01 → G02 → G03 → G04 → G05 → G06 → G07 → G08
```

G05 completed Product Execution Convergence.

G06 completed lineage authority consolidation.

G07 completed legacy/runtime/deployment/bootstrap/CLI boundary establishment.

G08 は ENH-E4 の final Gate であり、passed G02–G07 contracts を再設計するのではなく、final integrated verification と TD-006 closure を行う。

---

# 4. Current Authority Map

| Domain                             | Current Canonical State                                                                    | Transitional / Old Authority                             | Status                            | Exit / Next Gate                |
| ---------------------------------- | ------------------------------------------------------------------------------------------ | -------------------------------------------------------- | --------------------------------- | ------------------------------- |
| Product runtime                    | Causal/Exploratory/Predictive Product analysis は canonical Product Execution authority を使用 | physical legacy source は存在し得るが runtime authority ではない    | **ESTABLISHED**                   | preserve / final G08 audit      |
| Execution identity                 | one canonical Product Execution aggregate                                                  | old Causal/Family new Product write authority なし         | **ESTABLISHED**                   | preserve                        |
| Execution lifecycle                | one common state/claim/lease/mutation contract                                             | family-specific legacy mutation/claim authority なし       | **ESTABLISHED**                   | preserve                        |
| StageExecution                     | persistent canonical child for CAUSAL/EXPLORATORY/PREDICTIVE                               | old/ephemeral Product stage authority なし                 | **ESTABLISHED**                   | preserve                        |
| GenericExecutor                    | plan/order/binding/runner outcome を担当                                                      | lifecycle/output authority なし                            | **ESTABLISHED**                   | preserve through G08            |
| Result                             | explicit `EXECUTION_RESULT` / `STAGE_RESULT`; typed canonical ownership                    | Causal/Family new Product Result authority なし            | **ESTABLISHED**                   | preserve                        |
| Artifact metadata                  | canonical typed ownership; `artifact_id` = semantic identity                               | Causal/Family new Product Artifact metadata authority なし | **ESTABLISHED**                   | preserve                        |
| Physical Artifact storage          | `ArtifactStorePort`; physical locator と Product identity を分離                               | DB/store non-atomicity は compensation/reconciliation で処理 | **ESTABLISHED**                   | preserve                        |
| Typed downstream reuse             | Result ID + typed role/context; Artifact ID                                                | authoritative physical-key/untyped fallback なし           | **ESTABLISHED**                   | preserve                        |
| Family read projection             | family-specific URL/DTO/read surface は canonical data を projection 可                       | bounded compatibility/read projection が残る可能性あり           | **ESTABLISHED / TRANSITION OPEN** | TD-006 → G08                    |
| Lineage                            | typed structural authority + approved generic-only persisted authority                     | structural generic duplicate authority なし                | **ESTABLISHED**                   | preserve                        |
| Closure/export                     | derived read projection / traversal                                                        | independent lineage authority なし                         | **ESTABLISHED**                   | preserve                        |
| Legacy runtime                     | canonical Product runtime/deployment から非到達                                                 | physical `src/ariadne/legacy/` は存在し得る                    | **RETIRED_UNREACHABLE**           | final G08 classification/audit  |
| Shared science                     | legacy orchestration から独立して利用可能                                                            | scientific implementation を継続利用                          | **RETAIN_SHARED_CAPABILITY**      | preserve G08                    |
| Migration/bootstrap                | `alembic_product.ini -> product_migrations/`; head `0010`                                  | root legacy migrations は historical                      | **ESTABLISHED**                   | final clean-bootstrap audit G08 |
| Root `alembic.ini` / `migrations/` | canonical Product bootstrap authority なし                                                   | historical migration surface                             | **HISTORY_ONLY**                  | final G08 classification/audit  |
| Low-level scientific CLI           | persistent Product lifecycle の外側                                                           | standalone scientific utility として存続                      | **LOW_LEVEL_UTILITY**             | preserve                        |
| Auditable Product submission       | canonical Execution submission boundary                                                    | alternate lifecycle authority なし                         | **ESTABLISHED**                   | preserve                        |
| Compatibility/read projection      | non-authoritative compatibility surface                                                    | exact TD-006 scope は未確定                                  | **ESTABLISHED / TRANSITION OPEN** | TD-006 → G08                    |

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

G05 により、Causal / Exploratory / Predictive の new Product Result / Artifact metadata ownership が canonical boundary に収束し、old Family writers が new Product authority として reachable でないことが verified された。

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

### G05 residual boundary

G05 は final lineage consolidation や broad legacy deletion を意味しない。

```text
E4-TD-004 -> G06
legacy runtime boundary -> G07
final clean bootstrap / architecture audit -> G08
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
E4-TD-005 = handed to G07
```

G06 は G02–G05 で成立した Product Execution / StageExecution / Result / Artifact authority を維持したまま lineage authority を consolidate した。

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
E4-TD-006 = OPEN -> G08
```

G07 は physical legacy source の一律削除を要求していない。

G08 では、remaining compatibility/read projection が genuine Transition Debt かを current consumer / reachability / authority から判断し、必要なものだけを remove または explicitly archive する。

---

# 6. Transition Debt — Current Control Register

## 6.1 Active Now

| TD            | State    | Temporary Authority / Transition          | Why It Is Allowed                                                                                                     | Exit Gate | Exit Criterion                                        |
| ------------- | -------- | ----------------------------------------- | --------------------------------------------------------------------------------------------------------------------- | --------- | ----------------------------------------------------- |
| **E4-TD-006** | **OPEN** | temporary compatibility / read projection | G07 では active legacy/runtime/bootstrap authority の retirement を完了し、final compatibility/read classification を G08 に残した | G08       | bounded transition removed **OR** explicitly archived |

## 6.2 Closed by Passed Gates

| TD        | State      | Closed By | Verified Exit                                                                                                                    |
| --------- | ---------- | --------- | -------------------------------------------------------------------------------------------------------------------------------- |
| E4-TD-001 | **CLOSED** | G05       | old Causal/Family lifecycle accepts no new Product writes                                                                        |
| E4-TD-002 | **CLOSED** | G05       | all Product paths use persistent canonical StageExecution                                                                        |
| E4-TD-003 | **CLOSED** | G05       | one canonical Result/Artifact new-write ownership boundary                                                                       |
| E4-TD-004 | **CLOSED** | G06       | one authority representation per lineage semantic relation; generic persistence = generic-only; closure/export = projection-only |
| E4-TD-005 | **CLOSED** | G07       | Product runtime legacy dependency = 0; Product bootstrap legacy migration dependency = 0                                         |

## 6.3 Planned but Not Yet Introduced

```text
NONE
```

G08 が final ENH-E4 Gate である。

G08 より後に Transition Debt を残す計画はない。

### Rule

```text
No transition debt may become indefinite architecture.
```

Temporary compatibility/read transition には:

```text
owner
bounded duration
exit criterion
verification evidence
```

が必要である。

Final G08 requires:

```text
OPEN TRANSITION DEBT = 0
```

---

# 7. Architecture Decision Index

> Original Phase-06 ADR records retain `PROPOSED_FOR_HUMAN_APPROVAL` metadata.
> For ENH-E4 execution, the target set was subsequently taken forward through G01 and the approved Gate sequence.
> 以下の status は **runtime realization status** を表し、original ADR metadata の rewrite ではない。

| ADR        | Decision                                                         | Runtime Realization                                                      |
| ---------- | ---------------------------------------------------------------- | ------------------------------------------------------------------------ |
| E4-ADR-001 | Canonical Product runtime                                        | **ESTABLISHED G05; retired legacy runtime boundary verified G07**        |
| E4-ADR-002 | Unified canonical persistent Execution aggregate                 | **ESTABLISHED G02; sole Product authority verified G05**                 |
| E4-ADR-003 | Common Execution identity and mutation semantics                 | **ESTABLISHED G02; cross-family convergence G05; lineage semantics G06** |
| E4-ADR-004 | Persistent StageExecution for canonical workflows                | **ESTABLISHED G03; full Product convergence G05**                        |
| E4-ADR-005 | GenericExecutor remains workflow infrastructure                  | **ESTABLISHED G03; non-authoritative boundary reverified G05/G06**       |
| E4-ADR-006 | Explicit Result semantic levels under one ownership contract     | **ESTABLISHED G04; sole Product path verified G05**                      |
| E4-ADR-007 | One Product Artifact metadata authority, separate physical store | **ESTABLISHED G04; sole Product path verified G05**                      |
| E4-ADR-008 | Typed authority plus generic-only lineage                        | **ESTABLISHED G06**                                                      |
| E4-ADR-009 | Legacy runtime retirement/archive boundary                       | **ESTABLISHED G07**                                                      |
| E4-ADR-010 | Product-only canonical migration/bootstrap                       | **ESTABLISHED G07; final clean-bootstrap audit G08**                     |
| E4-ADR-011 | Standalone CLI boundary                                          | **ESTABLISHED G05/G07**                                                  |
| E4-ADR-012 | Compatibility terminology is non-architectural unless consumed   | **POLICY ESTABLISHED; final TD-006 classification G08**                  |

---

# 8. Invariant Status

| Invariant  | Short Meaning                                                              | Current Status                                       | Primary Gate |
| ---------- | -------------------------------------------------------------------------- | ---------------------------------------------------- | ------------ |
| E4-INV-001 | one canonical persistent Execution identity                                | **ESTABLISHED; TD-001 CLOSED G05**                   | G02/G05      |
| E4-INV-002 | family changes workflow, not lifecycle authority                           | **ESTABLISHED; sole authority verified G05**         | G02/G05      |
| E4-INV-003 | retry keeps identity; differs from rerun/revise                            | **ESTABLISHED; lineage semantics reverified G06**    | G02/G06      |
| E4-INV-004 | auditable claim/state transitions                                          | **ESTABLISHED; REVERIFIED G03/G05**                  | G02/G03/G05  |
| E4-INV-005 | centralized claim/lease authority                                          | **ESTABLISHED; TD-001 CLOSED G05**                   | G02/G05      |
| E4-INV-006 | every canonical Execution has persistent stages                            | **ESTABLISHED; TD-002 CLOSED G05**                   | G03/G05      |
| E4-INV-007 | GenericExecutor cannot own canonical lifecycle/Result/Artifact persistence | **ESTABLISHED; REVERIFIED G05/G06**                  | G03/G05/G06  |
| E4-INV-008 | every Result belongs to canonical Execution and declares level             | **ESTABLISHED; TD-003 CLOSED G05**                   | G04/G05      |
| E4-INV-009 | one Artifact metadata owner; locator distinct                              | **ESTABLISHED; TD-003 CLOSED G05**                   | G04/G05      |
| E4-INV-010 | DB/store compensation/reconciliation semantics                             | **ESTABLISHED**                                      | G04          |
| E4-INV-011 | one lineage authority per semantic relation                                | **ESTABLISHED; TD-004 CLOSED G06**                   | G06          |
| E4-INV-012 | closure/export cannot become lineage authority                             | **ESTABLISHED G06**                                  | G06          |
| E4-INV-013 | canonical runtime imports no retired legacy runtime                        | **ESTABLISHED G07**                                  | G07          |
| E4-INV-014 | shared science survives without legacy orchestration                       | **ESTABLISHED G07**                                  | G07          |
| E4-INV-015 | canonical bootstrap does not invoke root legacy migrations                 | **ESTABLISHED G07; final clean-bootstrap audit G08** | G07/G08      |
| E4-INV-016 | no indefinite dual read/write final architecture                           | **TD-006 OPEN; final G08**                           | G08          |

---

# 9. Requirement Families — Where to Look

35 requirements を通常実装時に個別記憶する必要はない。以下の range を使用する。

| Requirement Range | Concern                                             | Current State                                                                 |
| ----------------- | --------------------------------------------------- | ----------------------------------------------------------------------------- |
| E4-REQ-001..002   | Product runtime / legacy roots                      | **Product authority converged G05; runtime retirement boundary verified G07** |
| E4-REQ-003..010   | Execution identity/lifecycle/claim/mutations        | **G02 established; sole cross-family Product path G05; mutation lineage G06** |
| E4-REQ-011..014   | persistent stage / query / GenericExecutor boundary | **G03 established; full Product convergence G05**                             |
| E4-REQ-015..020   | Result / Artifact / typed downstream reuse          | **G04 established; sole Product path G05**                                    |
| E4-REQ-021..025   | lineage authority                                   | **ESTABLISHED G06**                                                           |
| E4-REQ-026..029   | shared science / legacy retirement classification   | **ESTABLISHED G07**                                                           |
| E4-REQ-030..032   | Product-only migration/bootstrap/data policy        | **Product-only authority ESTABLISHED G07; final clean-bootstrap G08**         |
| E4-REQ-033..035   | CLI / compatibility terminology                     | **CLI boundary ESTABLISHED G07; final compatibility/read TD-006 audit G08**   |

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
| E4-CON-005 | same structural lineage relation を final state で dual-author しない。                       |
| E4-CON-006 | temporary dual read/write または compatibility transition は bounded かつ exit criterion を持つ。 |
| E4-CON-007 | root legacy migrations を canonical Product bootstrap で実行しない。                            |
| E4-CON-008 | compatibility evidence なしに legacy source を削除しない。                                        |
| E4-CON-009 | legacy-named data contract を terminology だけを理由に rename しない。                             |
| E4-CON-010 | dependency proof なしに unrelated frontend/auth/dataset behavior を変更しない。                   |

---

# 11. G08 — Immediate Next Gate Control Card

## 11.1 Objective

> final clean bootstrap and architecture audit を実施し、all three Product families、mutation、lineage、runtime/bootstrap boundary、shared science を含む canonical Product architecture 全体を検証し、OPEN Transition Debt を zero にする。

G08 は `E4-TD-006` を close しつつ、G02–G07 で verified された architecture contract を preserve する。

## 11.2 Architecture Before G08

```text
G02 canonical Execution authority                  ESTABLISHED
G03 persistent StageExecution                      ESTABLISHED
G04 Result / Artifact ownership                    ESTABLISHED
G05 sole Product Execution convergence             ESTABLISHED
G06 lineage authority consolidation                ESTABLISHED
G07 legacy/runtime/bootstrap/CLI boundary           ESTABLISHED

TD-001                                             CLOSED
TD-002                                             CLOSED
TD-003                                             CLOSED
TD-004                                             CLOSED
TD-005                                             CLOSED

BUT:

TD-006 compatibility/read transition               OPEN
final clean bootstrap/startup audit                PENDING
final integrated three-family architecture audit   PENDING
OPEN TRANSITION DEBT = 0                           NOT YET VERIFIED
```

## 11.3 G08 Must Establish

```text
1. current repository における actual TD-006 scope を確定する

2. material residual を以下に classify する:
       REMOVE
       ARCHIVE
       RETAIN_NON_AUTHORITY
       RETAIN_SHARED_CAPABILITY
       NOT_TD

3. genuine bounded transition を:
       remove
       OR
       explicitly archive

4. empty Product DB から:
       Product-only migration
       current Product migration head
       application startup
   を verify する

5. all 3 Product families:
       CAUSAL
       EXPLORATORY
       PREDICTIVE

   について:
       Execution
       StageExecution
       Result
       Artifact
   を verify する

6. mutation semantics:
       retry
       rerun
       revise
       cancel
   と canonical lineage semantics を verify する

7. final authority model:
       Execution = Product lifecycle authority
       StageExecution = persistent stage authority
       Result / Artifact = output authority
       typed structural lineage = structural authority
       Product migrations = bootstrap authority
       GenericExecutor = subordinate mechanism
   を verify する

8. shared scientific capability が利用可能であることを verify する

9. final state:
       TD-006 CLOSED
       OPEN TRANSITION DEBT = 0
   を establish する
```

## 11.4 G08 Primary Audit Question

> active Product path、lineage representation、bootstrap path、または compatibility/read surface に、second authority または unresolved Transition Debt が残っているか？

G08 may PASS only if verified answer is:

```text
NO
```

and:

```text
OPEN TRANSITION DEBT = 0
```

## 11.5 G08 Must Close

```text
E4-TD-006
```

Exit criterion:

```text
bounded transition removed
OR
explicitly archived
```

Final Transition Debt state:

```text
TD-001 CLOSED
TD-002 CLOSED
TD-003 CLOSED
TD-004 CLOSED
TD-005 CLOSED
TD-006 CLOSED

OPEN TRANSITION DEBT = 0
```

## 11.6 G08 Preservation Boundary

G08 は final convergence/audit Gate である。

Implementation scope は:

```text
formal G08 Acceptance Criteria
+
actual TD-006 evidence
```

によって決める。

Physical legacy source、historical migration files、compatibility terminology は、それだけでは removal の根拠にならない。

G08 preserves:

```text
G02 Execution authority
G03 StageExecution / GenericExecutor boundary
G04 Result / Artifact ownership
G05 three-family Product convergence
G06 lineage authority
G07 runtime / deployment / bootstrap / shared-science / CLI boundary
```

## 11.7 G08 Exit Condition

G08 may PASS only when:

```text
E4-G08-AC-001 PASS
    clean Product bootstrap + application startup

E4-G08-AC-002 PASS
    three-family Golden Path

E4-G08-AC-003 PASS
    mutation + lineage

E4-G08-AC-004 PASS
    final authority audit

E4-G08-AC-005 PASS
    shared science + zero debt

AND

TD-001 CLOSED
TD-002 CLOSED
TD-003 CLOSED
TD-004 CLOSED
TD-005 CLOSED
TD-006 CLOSED

AND

OPEN TRANSITION DEBT = 0
```

This Control Card is a condensed operational index only.

Formal G08 implementation/test acceptance authority comes from Gate-local `06` / `07`.

---

# 12. What Is Deliberately Still Unresolved

以下は G08 exit scope であり、current snapshot における defect ではない。

### TD-006 — active Transition Debt

```text
E4-TD-006 OPEN -> G08
```

Formal scope:

```text
temporary compatibility / read projection
```

Exact current material inventory はまだ確定していない。

G08 は candidate residual を:

```text
current consumer
runtime reachability
deployment reachability
bootstrap reachability
persistent authority
compatibility semantics
```

に基づいて classify する。

Filename / directory name / terminology のみでは Transition Debt と判定しない。

### Physical legacy source

G07 independently established:

```text
Product runtime legacy dependency = 0
repository-managed deployment legacy dependency = 0
```

したがって physical legacy source が存在しても active Product authority とは限らない。

G08 では、それが:

```text
ARCHIVE
RETAIN_NON_AUTHORITY
RETAIN_SHARED_CAPABILITY
NOT_TD
```

等のどれに相当するかを current evidence から判断する。

### Root migration history

G07 independently established:

```text
Product bootstrap legacy migration dependency = 0
```

Canonical Product bootstrap:

```text
alembic_product.ini
    ->
product_migrations/
```

Root migration history は historical surface として残存可能である。

G08 では final:

```text
empty DB
+
Product-only migration
+
application startup
```

を verify する。

### Compatibility/read projection

Family/read/compatibility surface は stable non-authoritative contract であれば保持可能である。

G08 は、それが genuine bounded transition なのか stable retained contract なのかを current consumer semantics から決定する。

### Final architecture audit

以下は個別には passed Gate により established 済みである。

```text
Execution authority
StageExecution
Result / Artifact ownership
three-family convergence
lineage authority
legacy/runtime boundary
Product bootstrap boundary
shared science
CLI boundary
```

G08 はそれらを one final candidate に対して integrated verification する。

---

# 13. Evidence / Traceability Index

## Architecture

```text
40_operator_prompts/architecture_review/
06_target_architecture_decision_record_result.md

40_operator_prompts/architecture_review/
07_gate_decomposition_result.md
```

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

Architecture exit audit:

```text
30_test_report/G07/Trial01/
E4-G07_01_007_architecture_exit_audit.md
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

# 14. Operational Rules for Future Gates

## 14.1 Passed Gate Immutability

After a Gate PASS:

```text
passed 06/07 contract
passed production semantics
passed acceptance evidence
```

are protected.

Later Gate はそれらを extend / verify できるが、silently redefine してはならない。

Passed-Gate component を変更する必要がある場合:

```text
affected Gate
affected invariant/requirement
reason
preserved semantic
regression test
```

を明示する。

## 14.2 Gate-local Work Only

各 Gate では:

```text
implement current Gate
preserve earlier Gate contracts
perform changes required by:
    current Gate acceptance
    OR
    registered Transition Debt
```

に限定する。

G08 では:

```text
actual TD-006 inventory first
implementation scope second
```

とする。

## 14.3 Minimum Sufficient Context

G08 Package execution の通常 input:

```text
1. current Package instruction
2. G08 P00
3. immediately previous checkpoint
4. current relevant source/tests/migrations/config
```

Earlier Gate documents は:

```text
architecture contradiction
unclear invariant
unclear provenance
unclear mutation/lineage contract
```

が発生した場合にのみ参照する。

## 14.4 Positive Authority First

判断の起点は final positive authority model とする。

```text
Execution
StageExecution
Result
Artifact
typed structural lineage
approved generic-only semantic lineage
Product migration chain
shared science
```

Legacy name の列挙から architecture を逆算しない。

## 14.5 Test Evidence Discipline

Every Test Item report keeps:

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

Executable evidence が必要な Gate で prose-only inspection を `PASS` としない。

Migration/bootstrap/persistence semantics では real PostgreSQL evidence を使用する。

## 14.6 Model / Agent Role Separation

Architecture owner / developer:

```text
owns semantic decisions
approves Gate progression
reviews condensed current state
```

Coding Agent:

```text
compiles Gate contract into implementation + required automated tests
does not issue final Gate PASS
```

Independent Test Agent:

```text
tests fixed implementation ref
does not repair implementation
issues PASS / FAIL / BLOCKED
```

## 14.7 Trial Discipline

```text
Trial increments only after formal Independent Test FAIL.
```

Implementation/self-test correction within current Trial does not create a new Trial.

## 14.8 Fixed Candidate Discipline

Independent Test 前に:

```text
one fixed implementation/test candidate SHA
```

を確定する。

Documentation/report commits により later HEAD が異なる場合:

```text
fixed candidate
test execution HEAD
test-report commit
```

を区別する。

---

# 15. Control Sheet Update Rule

Update this file **only after a Gate reaches final PASS**, not during a Coding/Test Trial.

For each PASS:

1. Update snapshot commit / migration head.
2. Mark newly established ADR / INV / REQ groups.
3. Update Current Authority Map.
4. Add/close Transition Debt.
5. Add Gate evidence refs.
6. Replace the “Immediate Next Gate Control Card”.
7. Do **not** duplicate detailed Gate-local `06` / `07`.
8. If a Gate FAILs, leave current architecture snapshot unchanged; add no `ESTABLISHED` state.

This makes the sheet a record of **verified architecture**, not intended architecture.

G08 instruction set が prepared であっても、それ自体は G08 architecture が `ESTABLISHED` である evidence ではない。

---

# 16. Developer Quick Check — 30 Seconds

Before approving any next action:

```text
1. Which Gate are we in?
   -> G08 NEXT

2. What is already protected?
   -> G02 canonical Execution identity/lifecycle/claim
   -> G03 persistent StageExecution
   -> G03 GenericExecutor non-authority
   -> G04 Result / Artifact ownership and typed reuse
   -> G05 all-family canonical Product convergence
   -> G05 no Family new Product write authority
   -> G06 typed structural lineage authority
   -> G06 generic-only persisted lineage authority
   -> G06 closure/export projection-only boundary
   -> G07 retired legacy runtime/deployment boundary
   -> G07 Product-only bootstrap authority
   -> G07 shared science preservation
   -> G07 LOW_LEVEL_UTILITY scientific CLI boundary

3. What Transition Debt is intentionally alive?
   -> TD-006 only

   CLOSED:
   -> TD-001
   -> TD-002
   -> TD-003
   -> TD-004
   -> TD-005

4. What must G08 do?
   -> determine actual TD-006 inventory
   -> classify material residuals
   -> remove or explicitly archive genuine bounded transition
   -> verify empty Product DB -> Product migration -> application startup
   -> verify Causal / Exploratory / Predictive Golden Path
   -> verify retry / rerun / revise / cancel
   -> verify final lineage authority
   -> verify final Product/runtime/bootstrap authority
   -> preserve shared science
   -> establish OPEN TRANSITION DEBT = 0

5. What is not implied by G08?
   -> physical legacy source != automatically active authority
   -> historical root migrations != automatically Transition Debt
   -> compatibility terminology != automatically Transition Debt
   -> G08 != redesign of G02-G07 architecture

6. What is the G08 exit condition?
   -> AC-001 PASS
   -> AC-002 PASS
   -> AC-003 PASS
   -> AC-004 PASS
   -> AC-005 PASS

   -> TD-001 CLOSED
   -> TD-002 CLOSED
   -> TD-003 CLOSED
   -> TD-004 CLOSED
   -> TD-005 CLOSED
   -> TD-006 CLOSED

   -> OPEN TRANSITION DEBT = 0
```

If these six answers remain true, the work is still aligned with ENH-E4.
