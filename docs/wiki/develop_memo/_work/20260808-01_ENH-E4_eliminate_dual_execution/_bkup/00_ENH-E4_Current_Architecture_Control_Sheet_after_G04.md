# ENH-E4 Current Architecture Control Sheet

> **Purpose:** ENH-E4「二重アーキテクチャ解消」の現在地を、開発者・Coding Agent・Test Agentが短時間で把握するための control plane。
>
> **This document is NOT a new source of truth.**  
> 詳細なsemantic contractはArchitecture Decision Record / Gate-local 06・07 / passed Gate Decision / verified source codeを正本とする。  
> 本書はそれらの **現在状態・authority・未完了領域・traceabilityへの索引** を圧縮したものである。

---

## 0. Control Metadata

| Item | Current Value |
|---|---|
| Project | Ariadne / causal-atelier |
| Enhancement | ENH-E4 eliminate dual execution |
| Branch | `refactor/ariadne_mvp_e4` |
| Control Sheet Snapshot | **after E4-G04 Trial 02 PASS / before G05** |
| Repository evidence ref | `d2b0f311fda209608629114aaae9a1ea142bdd2d` |
| G04 tested implementation | `9c9db4454e0f08c4d46cb002f723ca6827917564` |
| Product migration head | `20260809_product_0009` |
| Current Gate | **G05 NEXT — Product Execution Convergence** |
| OPEN Transition Debt | `E4-TD-001`, `E4-TD-002`, `E4-TD-003` |
| G04 Trial 02 regression | `27 passed`, standardized PostgreSQL runner exit `0` |
| G04 targeted PostgreSQL | `3 passed` |
| G04 pure contract tests | `6 passed` |

### Snapshot Evidence

```text
30_test_report/G04/
E4-G04_02_999_gate_decision.md

20_implementation_reports/G04/
E4-G04_02_implementation_completion_report.md

30_test_report/G03/
E4-G03_02_999_gate_decision.md

40_operator_prompts/architecture_review/
06_target_architecture_decision_record_result.md
07_gate_decomposition_result.md
```

---

# 1. How to Read This Sheet

## 1.1 Status Vocabulary

| Status | Meaning |
|---|---|
| **ESTABLISHED** | Production contract is implemented and independently Gate-tested. |
| **ESTABLISHED / TRANSITION OPEN** | Canonical contract is proven, but old authority remains temporarily under registered Transition Debt. |
| **TARGET FIXED** | Target semantic contract is decided/frozen, but runtime convergence is not yet Gate-proven. |
| **PENDING** | Future Gate work; do not treat as current runtime architecture. |
| **RETIRE PENDING** | Non-canonical/legacy boundary is identified, but final retirement verification has not occurred. |

## 1.2 Precedence

矛盾が見つかった場合の優先順:

```text
1. Passed Gate-local 06/07 contract + final Gate Decision
2. Target Architecture ADR / Invariant / Requirement / Constraint
3. Verified current source / Product migration
4. This Control Sheet
```

本書が上位正本と矛盾した場合、**本書を修正する**。上位正本を本書に合わせて変更しない。

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
    = non-canonical retirement/archive boundary

Shared scientific implementation
    = retained independently

Canonical bootstrap
    = Product migrations only
```

## 2.2 What Is Actually Established Now

```text
Canonical Execution identity/lifecycle/claim/lease        ESTABLISHED
Persistent StageExecution across all 3 families           ESTABLISHED
GenericExecutor subordinate workflow-only boundary        ESTABLISHED

Explicit ExecutionResult / StageResult levels             ESTABLISHED
Canonical Result/Artifact typed ownership contract        ESTABLISHED
Artifact semantic ID != object_key                        ESTABLISHED
ArtifactStore physical/metadata boundary                  ESTABLISHED
Store/DB compensation + reconciliation contract           ESTABLISHED
Typed downstream Result reuse role/context                ESTABLISHED

Old Causal/Family new Execution write paths               STILL TRANSITIONAL
Old/ephemeral stage paths                                 STILL TRANSITIONAL
Old Causal/Family Result/Artifact metadata writers        STILL TRANSITIONAL

Final Product path convergence                            NOT YET ESTABLISHED
Final lineage authority consolidation                     NOT YET ESTABLISHED
Legacy runtime retirement                                 NOT YET FINALIZED
Final Product-only clean bootstrap audit                  NOT YET FINALIZED
```

---

# 3. Gate Progress

| Gate | Name | Status | Architecture Established / Purpose |
|---|---|---|---|
| G01 | Canonical contract/schema foundation | **PASS** | Target domain/schema contracts, relation authority allowlist, traceability foundation |
| G02 | Canonical Execution aggregate and claim | **PASS** | Canonical Execution identity, family discriminator, lifecycle, claim/lease, retry/rerun/revise/cancel |
| Preflight | Test PostgreSQL infrastructure | **PASS** | Repository-managed isolated real PostgreSQL verification path |
| G03 | Persistent StageExecution and runner boundary | **PASS** | Persistent stage model for all families; queryable attempt/bindings; GenericExecutor authority removed |
| G04 | Result/Artifact ownership boundary | **PASS** | Explicit Result levels; typed Result/Artifact ownership; physical-store separation; compensation/reconciliation; typed reuse |
| **G05** | **Product Execution Convergence** | **NEXT** | Cut over Causal/Exploratory/Predictive submissions, claim, stage, Result and Artifact to the sole canonical Product path |
| G06 | Lineage authority consolidation | PENDING | typed structural vs generic-only authority; closure/export projection |
| G07 | Legacy, CLI, migration boundary | PENDING | legacy retirement boundary, shared science preservation, Product-only bootstrap/CLI boundary |
| G08 | Final clean bootstrap and architecture audit | PENDING | final convergence; all invariants/requirements/constraints; OPEN TD = 0 |

### Gate Sequencing Rule

```text
G01 → G02 → G03 → G04 → G05 → G06 → G07 → G08
```

G05 is the **only Product Execution Convergence Gate**.  
G02/G03/G04 establish canonical contracts before the old write paths are finally cut over.

---

# 4. Current Authority Map

| Domain | Current Canonical State | Transitional / Old Authority | Status | Exit / Next Gate |
|---|---|---|---|---|
| Product runtime | Product runtime is canonical direction | legacy roots remain in source | TARGET FIXED / RETIRE PENDING | G07 |
| Execution identity | canonical Product Execution aggregate | old Causal/Family new-write paths remain | **ESTABLISHED / TRANSITION OPEN** | TD-001 → G05 |
| Execution lifecycle | common state/claim/lease/mutation contract | old lifecycle paths may still exist | **ESTABLISHED / TRANSITION OPEN** | G05 |
| StageExecution | persistent canonical child for CAUSAL/EXPLORATORY/PREDICTIVE | old stage persistence/ephemeral behavior remains | **ESTABLISHED / TRANSITION OPEN** | TD-002 → G05 |
| GenericExecutor | plan/order/binding/runner outcome only | must not become lifecycle/output authority | **ESTABLISHED** | preserve through G08 |
| Result | explicit `EXECUTION_RESULT` / `STAGE_RESULT`, typed canonical ownership | old Causal/Family Result writers remain | **ESTABLISHED / TRANSITION OPEN** | TD-003 → G05 |
| Artifact metadata | canonical typed ownership; `artifact_id` is semantic identity | old Causal/Family Artifact writers remain | **ESTABLISHED / TRANSITION OPEN** | TD-003 → G05 |
| Physical Artifact storage | `ArtifactStorePort`; physical locator separate from Product identity | non-atomic DB/store writes handled by compensation/reconciliation | **ESTABLISHED** | preserve |
| Typed downstream reuse | Result ID + typed role/context; Artifact ID for artifact reuse | old physical-key/untyped paths may remain outside converged route | **ESTABLISHED / TRANSITION OPEN** | G05 route convergence |
| Lineage | target policy fixed: typed structural + generic-only | current hybrid/duplicate representation may remain | TARGET FIXED / PENDING | G06 |
| Closure/export | target = read projection, never authority | current hybrid readers require consolidation | PENDING | G06 |
| Legacy runtime | non-canonical target | source / compatibility boundary remains | RETIRE PENDING | G07 |
| Shared science | must survive legacy retirement | used independently of orchestration | TARGET FIXED | verify G07/G08 |
| Migration/bootstrap | Product-only target; current head `0009` | root legacy migrations remain historical | TARGET FIXED | final verification G07/G08 |
| Low-level CLI | target = outside persistent Product lifecycle | final boundary not yet audited | TARGET FIXED | G07 |
| Auditable Product CLI | must submit canonical Execution | convergence not final | PENDING | G05/G07 |

---|---|---|---|---|
| Product runtime | Product runtime is canonical direction | legacy roots remain in source | TARGET FIXED / RETIRE PENDING | G07 |
| Execution identity | canonical Product Execution aggregate | old Causal/Family new-write paths remain | **ESTABLISHED / TRANSITION OPEN** | TD-001 → G05 |
| Execution lifecycle | common state/claim/lease/mutation contract | old lifecycle paths may still exist | **ESTABLISHED / TRANSITION OPEN** | G05 |
| StageExecution | persistent canonical child for CAUSAL/EXPLORATORY/PREDICTIVE | old stage persistence/ephemeral behavior remains | **ESTABLISHED / TRANSITION OPEN** | TD-002 → G05 |
| GenericExecutor | plan/order/binding/runner outcome only | must not become lifecycle authority | **ESTABLISHED** | preserve through G08 |
| Result | target = ExecutionResult / StageResult under one ownership contract | Causal/Family Result ownership still dual | **PENDING** | G04, then converge G05 |
| Artifact metadata | target = one Product metadata owner | current Causal/Family metadata owners remain | **PENDING** | G04, then converge G05 |
| Physical Artifact storage | `ArtifactStorePort` separate from metadata authority | DB/store atomicity requires compensation | TARGET FIXED | G04 |
| Lineage | target policy fixed: typed structural + generic-only | current hybrid/duplicate representation may remain | TARGET FIXED / PENDING | G06 |
| Closure/export | target = read projection, never authority | current hybrid readers require consolidation | PENDING | G06 |
| Legacy runtime | non-canonical target | source / compatibility boundary remains | RETIRE PENDING | G07 |
| Shared science | must survive legacy retirement | used independently of orchestration | TARGET FIXED | verify G07/G08 |
| Migration/bootstrap | Product-only target; current head `0008` | root legacy migrations remain historical | TARGET FIXED | final verification G07/G08 |
| Low-level CLI | target = outside persistent Product lifecycle | final boundary not yet audited | TARGET FIXED | G07 |
| Auditable Product CLI | must submit canonical Execution | convergence not final | PENDING | G05/G07 |

---

# 5. Passed-Gate Contracts That Must Not Regress

## 5.1 G02 — Execution Contract

The following are now protected architecture:

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
retry = same Execution ID
rerun = new Execution ID + typed source relation
revise = new Execution ID + typed base relation
cancel = terminal Execution transition
GenericExecutor != claim/lifecycle authority
```

### Current caveat

This does **not** mean old Product write paths are already gone.

```text
E4-TD-001 = OPEN until G05
```

G05 is responsible for making canonical Execution the **sole** new-write authority.

---

## 5.2 G03 — Stage Contract

The following are now protected architecture:

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
    same StageExecution ID
    append attempt history

Execution ↔ Stage state must remain consistent.

Stage mutation is governed by canonical Execution claim/lease ownership.

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
        persist canonical StageExecution
        decide canonical retry policy
        persist Result
        persist Artifact metadata
        persist lineage
```

### G03 independent evidence

```text
AC-001 PASS — all 3 canonical families persist/reload stages
AC-002 PASS — queryable state and attempts [1,2]
AC-003 PASS — no GenericExecutor persistence/claim/retry authority
AC-004 PASS — zero-stage/materialization failures rollback
AC-005 PASS — failure/retry/cancel/lease/invalid-success consistency

GenericExecutor boundary/unit:
    6 passed

Standardized PostgreSQL:
    22 passed
    migration current = 20260809_product_0008
```

### Current caveat

Old/transitional stage behavior may still exist outside converged Product paths.

```text
E4-TD-002 = OPEN until G05
```

---

## 5.3 G04 — Result / Artifact Ownership Contract

The following are now protected architecture:

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

Artifact-only output:
    explicitly allowed/rejected by workflow/family output contract
```

### G04 evidence

```text
Trial 01 = FAIL
    AC-003: compensation durability used MemoryUow only
    AC-004: ResultReuseRef lacked typed role/context

Trial 02 implementation:
    9c9db4454e0f08c4d46cb002f723ca6827917564

Trial 02:
    AC-001 PASS
    AC-002 PASS
    AC-003 PASS
    AC-004 PASS
    AC-005 PASS
    pure contract: 6 passed
    targeted PostgreSQL: 3 passed
    G02/G03/G04 regression: 27 passed
    migration: 20260809_product_0009
```

### Current caveat

```text
E4-TD-003 = OPEN until G05
```

G05 must stop old Result/Artifact new-write authorities rather than introducing permanent dual-write.

# 6. Transition Debt — Current Control Register

## 6.1 Active Now

| TD | State | Temporary Authority | Why It Is Allowed | Exit Gate | Exit Criterion |
|---|---|---|---|---|---|
| **E4-TD-001** | **OPEN** | old Causal/Family new Execution writes | G02 established canonical Execution before full path cutover | G05 | old lifecycle accepts no new Product writes |
| **E4-TD-002** | **OPEN** | old stage persistence / ephemeral behavior | G03 established persistent canonical StageExecution before full path cutover | G05 | all Product paths use canonical persistent StageExecution |
| **E4-TD-003** | **OPEN** | old Causal/Family Result/Artifact metadata ownership | G04 established canonical output ownership before full path cutover | G05 | one canonical Result/Artifact new-write boundary |

## 6.2 Planned but Not Yet Introduced

| TD | Introduced By | Purpose / Temporary Authority | Exit |
|---|---|---|---|
| E4-TD-004 | G05 | structural lineage generic duplicate writes | G06 |
| E4-TD-005 | G06 | legacy runtime/migration surface | G07 |
| E4-TD-006 | G07 | temporary compatibility/read projection | G08 |

### Rule

```text
No transition debt may become indefinite architecture.
```

Any temporary dual-read/write must have:

```text
owner
bounded duration
exit criterion
reconciliation / verification evidence
```

Final G08 requires:

```text
OPEN TRANSITION DEBT = 0
```

---

# 7. Architecture Decision Index

> Original Phase-06 ADR records retain `PROPOSED_FOR_HUMAN_APPROVAL` metadata.  
> For ENH-E4 execution, the target set was subsequently taken forward through G01 and the approved Gate sequence.  
> The status below therefore means **runtime realization status**, not a rewrite of the original ADR metadata.

| ADR | Decision | Runtime Realization |
|---|---|---|
| E4-ADR-001 | Canonical Product runtime | PARTIAL; final legacy/runtime boundary G07 |
| E4-ADR-002 | Unified canonical persistent Execution aggregate | **ESTABLISHED G02**, sole-authority convergence G05 |
| E4-ADR-003 | Common Execution identity and mutation semantics | **ESTABLISHED G02**, reverify later |
| E4-ADR-004 | Persistent StageExecution for canonical workflows | **ESTABLISHED G03**, full path convergence G05 |
| E4-ADR-005 | GenericExecutor remains workflow infrastructure | **ESTABLISHED G03** |
| E4-ADR-006 | Explicit Result semantic levels under one ownership contract | **ESTABLISHED G04**, sole-path convergence G05 |
| E4-ADR-007 | One Product Artifact metadata authority, separate physical store | **ESTABLISHED G04**, sole-path convergence G05 |
| E4-ADR-008 | Typed authority plus generic-only lineage | contract fixed; runtime consolidation G06 |
| E4-ADR-009 | Legacy runtime retirement/archive boundary | G07 |
| E4-ADR-010 | Product-only canonical migration/bootstrap | direction/evidence exists; final boundary G07/G08 |
| E4-ADR-011 | Standalone CLI boundary | G05/G07 |
| E4-ADR-012 | Compatibility terminology is non-architectural unless consumed | G07 |

---

# 8. Invariant Status

| Invariant | Short Meaning | Current Status | Primary Gate |
|---|---|---|---|
| E4-INV-001 | one canonical persistent Execution identity | **ESTABLISHED / TD-001 OPEN** | G02 |
| E4-INV-002 | family changes workflow, not lifecycle authority | **ESTABLISHED / TD-001 OPEN** | G02 |
| E4-INV-003 | retry keeps identity; differs from rerun/revise | **ESTABLISHED** | G02 |
| E4-INV-004 | auditable claim/state transitions | **ESTABLISHED, REVERIFIED G03** | G02/G03 |
| E4-INV-005 | centralized claim/lease authority | **ESTABLISHED / TD-001 OPEN** | G02 |
| E4-INV-006 | every canonical Execution has persistent stages | **ESTABLISHED / TD-002 OPEN** | G03 |
| E4-INV-007 | GenericExecutor cannot commit canonical lifecycle/Result/Artifact metadata | **ESTABLISHED** | G03 |
| E4-INV-008 | every Result belongs to canonical Execution and declares level | **ESTABLISHED / TD-003 OPEN** | G04/G05 |
| E4-INV-009 | one Artifact metadata owner; locator distinct | **ESTABLISHED / TD-003 OPEN** | G04/G05 |
| E4-INV-010 | DB/store compensation/reconciliation semantics | **ESTABLISHED** | G04 |
| E4-INV-011 | one lineage authority per semantic relation | TARGET FIXED; runtime pending | G06 |
| E4-INV-012 | closure/export cannot become lineage authority | TARGET FIXED; runtime pending | G06 |
| E4-INV-013 | canonical runtime imports no retired legacy runtime | PENDING final audit | G07 |
| E4-INV-014 | shared science survives without legacy orchestration | TARGET FIXED; verify later | G07 |
| E4-INV-015 | canonical bootstrap does not invoke root legacy migrations | TARGET FIXED; final verify later | G07 |
| E4-INV-016 | no indefinite dual read/write final architecture | **NOT FINAL YET; bounded TDs active** | G06/G08 |

---

# 9. Requirement Families — Where to Look

The 35 requirements should not be memorized individually during normal implementation. Use these ranges.

| Requirement Range | Concern | Current State |
|---|---|---|
| E4-REQ-001..002 | Product runtime / legacy roots | partially established; final G07/G08 |
| E4-REQ-003..010 | Execution identity/lifecycle/claim/mutations | **G02 established** |
| E4-REQ-011..014 | persistent stage / query / GenericExecutor boundary | **G03 established** |
| E4-REQ-013 | stage-side ownership relation | stage side established; Result/Artifact completion continues in G04 |
| E4-REQ-015..020 | Result / Artifact / typed downstream reuse | **G04 established; sole-path convergence G05** |
| E4-REQ-021..025 | lineage authority | G06 |
| E4-REQ-026..029 | shared science / legacy retirement classification | G07 |
| E4-REQ-030..032 | Product-only migration/bootstrap/data policy | evidence exists; final G07/G08 |
| E4-REQ-033..035 | CLI / compatibility terminology | G05/G07 |

Detailed wording remains in:

```text
40_operator_prompts/architecture_review/
06_target_architecture_decision_record_result.md
```

---

# 10. Constraints — Always-On Guardrails

| Constraint | Guardrail |
|---|---|
| E4-CON-001 | Do not redesign scientific algorithms as part of Execution unification. |
| E4-CON-002 | Do not make GenericExecutor the lifecycle owner. |
| E4-CON-003 | Do not leave Causal/Family tables as independent **final** authorities. |
| E4-CON-004 | Do not use physical object keys as Result/Artifact semantic IDs. |
| E4-CON-005 | Do not dual-author the same structural lineage relation in final state. |
| E4-CON-006 | Any temporary dual read/write must be bounded and have an exit criterion. |
| E4-CON-007 | Do not run root legacy migrations in canonical Product bootstrap. |
| E4-CON-008 | Do not remove legacy source before external compatibility decision. |
| E4-CON-009 | Do not rename legacy-named data contracts solely because of terminology. |
| E4-CON-010 | Do not modify unrelated frontend/auth/dataset behavior without dependency proof. |

---

# 11. G04 — Immediate Next Gate Control Card

# 11. G05 — Immediate Next Gate Control Card

## 11.1 Objective

> Cut over Causal / Exploratory / Predictive so that every new Product submission, claim, stage, Result and Artifact uses the sole canonical Product Execution authority.

G05 is the **only Product Execution Convergence Gate**.

## 11.2 Architecture Before G05

```text
G02 canonical Execution contract          established
G03 persistent StageExecution contract    established
G04 Result/Artifact ownership contract    established

BUT:

TD-001 old Execution new-write paths      OPEN
TD-002 old/ephemeral stage paths          OPEN
TD-003 old Result/Artifact writers        OPEN
```

## 11.3 G05 Must Establish

```text
CAUSAL submission       -> canonical Execution
EXPLORATORY submission  -> canonical Execution
PREDICTIVE submission   -> canonical Execution

All three families:
    same canonical claim authority
    persistent StageExecution
    canonical Result owner
    canonical Artifact owner

Old Product lifecycle:
    accepts no new Product writes

GenericExecutor:
    remains subordinate workflow infrastructure
```

## 11.4 G05 Acceptance Criteria

```text
E4-G05-AC-001
Causal submission creates canonical Execution.

E4-G05-AC-002
Exploratory submission creates canonical Execution.

E4-G05-AC-003
Predictive submission creates canonical Execution.

E4-G05-AC-004
All three families use the same claim authority,
persistent StageExecution, and canonical Result/Artifact owner.

E4-G05-AC-005
Old Causal/Family lifecycle accepts no new Product writes,
and GenericExecutor remains non-authoritative.
```

## 11.5 G05 Must Close

```text
E4-TD-001
E4-TD-002
E4-TD-003
```

## 11.6 G05 MUST NOT Do

```text
DO NOT finalize generic-only lineage consolidation.  # G06
DO NOT delete/archive legacy source broadly.         # G07
DO NOT perform historical application-data migration.
DO NOT redesign scientific algorithms/payload semantics.
DO NOT resurrect old write authority as rollback strategy.
DO NOT weaken G02/G03/G04 contracts.
DO NOT make GenericExecutor lifecycle/output owner.
```

## 11.7 Expected New Transition Debt

```text
E4-TD-004
Introduced: G05
Exit Gate: G06
Authority: structural lineage generic duplicate writes
```

# 12. What Is Deliberately Still Unresolved

The following are **not defects at this snapshot** because their exit Gates are later.

### Product path convergence

```text
E4-TD-001 OPEN
E4-TD-002 OPEN
E4-TD-003 OPEN
```

Canonical Execution, StageExecution and Result/Artifact contracts are established, but old Product new-write paths may still exist until G05.

### Lineage

Relation-level target policy exists, but runtime writer authority is not yet consolidated. This is G06.

### Legacy

Legacy source/runtime boundaries are not yet finally retired/audited. This is G07.

### Final bootstrap

The repository-managed PostgreSQL runner already proves Product migration operation, but ENH-E4 final clean-bootstrap convergence is G07/G08.

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

## G03

Trial 01 is retained as failed evidence:

```text
30_test_report/G03/
E4-G03_01_999_gate_decision.md
```

Trial 02 implementation:

```text
bac1814bb713f32b859fbe7e2b445fa6cd557f2b
```

Trial 02 implementation report:

```text
20_implementation_reports/G03/
E4-G03_02_implementation_completion_report.md
```

Trial 02 final decision:

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

Trial 01 implementation:

```text
3d88781c1b69ba03bb06c0b8f143612b81feb4bf
```

Trial 01 decision:

```text
E4-G04_01_999_gate_decision.md
Decision: FAIL
```

Trial 02 implementation:

```text
9c9db4454e0f08c4d46cb002f723ca6827917564
```

Trial 02 implementation report:

```text
20_implementation_reports/G04/
E4-G04_02_implementation_completion_report.md
```

Trial 02 final decision:

```text
30_test_report/G04/
E4-G04_02_999_gate_decision.md
Decision: PASS
```

Repository evidence commit:

```text
d2b0f311fda209608629114aaae9a1ea142bdd2d
```

# 14. Operational Rules for Future Gates

## 14.1 Passed Gate Immutability

After a Gate PASS:

```text
passed 06/07 contract
passed production semantics
passed acceptance evidence
```

are protected.

A later Gate may extend them, but must not silently redefine them.

If a later implementation needs to change a passed-Gate component:

```text
affected Gate
affected invariant/requirement
reason
preserved semantic
regression test
```

must be explicitly recorded.

## 14.2 Gate-local Work Only

At each Gate:

```text
implement current Gate
preserve earlier Gate contracts
do not pre-implement later authority cutovers
```

Transition Debt is used to bridge Gates deliberately rather than doing uncontrolled cross-Gate work.

## 14.3 Test Evidence Discipline

Every Test Item report must keep:

```text
exact command
environment
expected result
actual result
exit code
raw evidence path
fact findings
interpretation
PASS / FAIL / BLOCKED
```

`PASS` is not accepted from prose-only inspection where the Gate requires executable evidence.

## 14.4 Model / Agent Role Separation

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
7. Do **not** duplicate detailed Gate-local 06/07 text.
8. If a Gate FAILs, leave the current architecture snapshot unchanged; add no “established” state.

This makes the sheet a record of **verified architecture**, not intended architecture.

---

# 16. Developer Quick Check — 30 Seconds

Before approving any next action, answer these questions:

```text
1. Which Gate are we in?
   → G05 NEXT

2. What is already protected?
   → G02 canonical Execution
   → G03 persistent StageExecution
   → G03 GenericExecutor non-authority
   → G04 explicit Result levels
   → G04 canonical Result/Artifact ownership
   → G04 ArtifactStore compensation/reconciliation
   → G04 typed Result/Artifact reuse identity

3. What old authority is still intentionally alive?
   → TD-001 old Execution writes
   → TD-002 old/ephemeral stage paths
   → TD-003 old Result/Artifact writers

4. What must G05 do?
   → cut over CAUSAL / EXPLORATORY / PREDICTIVE
   → make canonical Product path the sole new-write authority
   → close TD-001 / TD-002 / TD-003

5. What must NOT be touched yet?
   → G06 lineage final cutover
   → G07 legacy retirement
   → G08 final bootstrap/audit

6. What is the G05 exit condition?
   → all three families submit/claim/stage/result/artifact canonically
   → old Causal/Family lifecycle accepts no new Product writes
   → GenericExecutor remains non-authoritative
```

If these six answers remain true, the work is still aligned with ENH-E4.
