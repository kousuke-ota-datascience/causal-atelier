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
| Control Sheet Snapshot | **after E4-G05 Trial 02 PASS / before G06** |
| G05 tested implementation | `ad3e3e124ee47f9cbaa2470b25263b7289795262` |
| G05 final Gate Decision | `30_test_report/G05/E4-G05_02_999_gate_decision.md` |
| Product migration head | `20260809_product_0010` |
| Current Gate | **G06 NEXT — Lineage authority consolidation** |
| OPEN Transition Debt | `E4-TD-004` |
| G05 Test Items | `001–010 PASS` |
| G05 Acceptance Criteria | `AC-001..005 SATISFIED` |
| G05 Blocking Findings | `NONE` |

### Snapshot Evidence

```text
30_test_report/G05/
E4-G05_02_999_gate_decision.md

20_implementation_reports/G05/Trial02/
E4-G05_02_implementation_completion_report.md

20_implementation_reports/G05/Trial02/
E4-G05_02_R1_predictive_retry_remediation_report.md
E4-G05_02_R2_combined_regression_remediation_report.md

30_test_report/G04/
E4-G04_02_999_gate_decision.md

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

Final lineage authority consolidation                          NOT YET ESTABLISHED
Legacy source/runtime retirement                               NOT YET FINALIZED
Final Product-only clean bootstrap audit                       NOT YET FINALIZED
```

G05 established the **sole new Product authority** for Execution / StageExecution / Result / Artifact.
Legacy source and bounded compatibility/read surfaces may still exist, but they are not permitted to become a new Product write authority.

---

# 3. Gate Progress

| Gate | Name | Status | Architecture Established / Purpose |
|---|---|---|---|
| G01 | Canonical contract/schema foundation | **PASS** | Target domain/schema contracts, relation authority allowlist, traceability foundation |
| G02 | Canonical Execution aggregate and claim | **PASS** | Canonical Execution identity, family discriminator, lifecycle, claim/lease, retry/rerun/revise/cancel |
| Preflight | Test PostgreSQL infrastructure | **PASS** | Repository-managed isolated real PostgreSQL verification path |
| G03 | Persistent StageExecution and runner boundary | **PASS** | Persistent stage model for all families; queryable attempt/bindings; GenericExecutor authority removed |
| G04 | Result/Artifact ownership boundary | **PASS** | Explicit Result levels; typed Result/Artifact ownership; physical-store separation; compensation/reconciliation; typed reuse |
| G05 | Product Execution Convergence | **PASS** | Causal/Exploratory/Predictive Product submissions, claim, stage, Result and Artifact converge on the sole canonical Product authority |
| **G06** | **Lineage authority consolidation** | **NEXT** | Eliminate duplicate lineage authority; typed structural authority + generic-only persisted authority; closure/export projection only |
| G07 | Legacy, CLI, migration boundary | PENDING | legacy retirement boundary, shared science preservation, Product-only bootstrap/CLI boundary |
| G08 | Final clean bootstrap and architecture audit | PENDING | final convergence; all invariants/requirements/constraints; OPEN TD = 0 |

### Gate Sequencing Rule

```text
G01 → G02 → G03 → G04 → G05 → G06 → G07 → G08
```

G05 has completed the only Product Execution Convergence cutover.
G06 must not reopen Execution / StageExecution / Result / Artifact authority; it may only consolidate lineage authority while preserving the passed G02–G05 contracts.

---

# 4. Current Authority Map

| Domain | Current Canonical State | Transitional / Old Authority | Status | Exit / Next Gate |
|---|---|---|---|---|
| Product runtime | new Causal/Exploratory/Predictive Product analysis uses canonical Product Execution authority | legacy roots remain in source/compatibility boundary only | **ESTABLISHED / RETIRE PENDING** | G07 |
| Execution identity | one canonical Product Execution aggregate | no old Causal/Family new Product write authority | **ESTABLISHED** | preserve |
| Execution lifecycle | one common state/claim/lease/mutation contract | family-specific legacy mutation/claim authority disabled | **ESTABLISHED** | preserve |
| StageExecution | persistent canonical child for CAUSAL/EXPLORATORY/PREDICTIVE | no old/ephemeral Product stage authority | **ESTABLISHED** | preserve |
| GenericExecutor | plan/order/binding/runner outcome only | must not become lifecycle/output authority | **ESTABLISHED** | preserve through G08 |
| Result | explicit `EXECUTION_RESULT` / `STAGE_RESULT`, typed canonical ownership | no Causal/Family new Product Result authority | **ESTABLISHED** | preserve |
| Artifact metadata | canonical typed ownership; `artifact_id` is semantic identity | no Causal/Family new Product Artifact metadata authority | **ESTABLISHED** | preserve |
| Physical Artifact storage | `ArtifactStorePort`; physical locator separate from Product identity | non-atomic DB/store writes handled by compensation/reconciliation | **ESTABLISHED** | preserve |
| Typed downstream reuse | Result ID + typed role/context; Artifact ID for artifact reuse | no authoritative physical-key/untyped fallback on converged Product paths | **ESTABLISHED** | preserve |
| Family read projection | family-specific URL/DTO/read surfaces may project canonical data | bounded read compatibility may remain | **ESTABLISHED / RETIRE PENDING** | G07 |
| Lineage | target policy fixed: typed structural authority + generic-only persisted authority | structural relation may still be duplicated through generic lineage write paths | **ESTABLISHED / TRANSITION OPEN** | TD-004 → G06 |
| Closure/export | must be read projection only, never lineage authority | hybrid readers/projections still require consolidation | **TARGET FIXED / PENDING** | G06 |
| Legacy runtime | non-canonical; cannot receive new Product authority | source / compatibility boundary remains | **RETIRE PENDING** | G07 |
| Shared science | retained independently of legacy orchestration | scientific implementation remains reusable | **TARGET FIXED** | verify G07/G08 |
| Migration/bootstrap | Product migration head `0010`; canonical direction established | root legacy migrations remain historical | **TARGET FIXED** | final verification G07/G08 |
| Low-level scientific CLI | outside persistent Product lifecycle | final retirement/classification audit remains | **ESTABLISHED / RETIRE PENDING** | G07 |
| Auditable Product CLI | submits canonical Execution | compatibility/legacy CLI cleanup remains | **ESTABLISHED / RETIRE PENDING** | G07 |

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

### G05 convergence status

```text
E4-TD-001 = CLOSED by G05
```

G05 independently verified that new Product identity / lifecycle / claim authority no longer falls back to old Causal/Family authority.

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

### G05 convergence status

```text
E4-TD-002 = CLOSED by G05
```

All three Product families use persistent canonical StageExecution under canonical claim/lease authority.
Legacy stage source may remain for later retirement, but it is not a new Product stage authority.

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

### G05 convergence status

```text
E4-TD-003 = CLOSED by G05
```

G05 verified that new Product Result / Artifact metadata ownership is canonical across Causal / Exploratory / Predictive and that old Family writers are not reachable as new Product authority.


## 5.4 G05 — Product Execution Convergence Contract

The following is now protected architecture:

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
    must not fall back to old Product authority

Family-facing mutations:
    delegate canonical retry / rerun / revise / cancel semantics

Family-facing read surfaces:
    may remain as adapters/projections
    must project canonical authority

GenericExecutor:
    workflow/scientific infrastructure only
    not Product lifecycle / Result / Artifact authority

CLI boundary:
    auditable Product CLI submits canonical Execution
    low-level scientific CLI remains outside persistent Product lifecycle
```

### G05 independent evidence

```text
Trial 02 tested implementation:
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

G05 does **not** imply final lineage consolidation or broad legacy deletion.

```text
E4-TD-004 = OPEN until G06
legacy source/runtime retirement = G07
final clean bootstrap / architecture audit = G08
```

---

# 6. Transition Debt — Current Control Register

## 6.1 Active Now

| TD | State | Temporary Authority | Why It Is Allowed | Exit Gate | Exit Criterion |
|---|---|---|---|---|---|
| **E4-TD-004** | **OPEN** | structural lineage relation may still be persisted through generic lineage representation in addition to typed structural authority | G05 intentionally deferred final lineage consolidation to a dedicated Gate | G06 | each semantic relation has one authoritative lineage representation; generic persistence is generic-only; closure/export is projection only |

## 6.2 Closed by Passed Gates

| TD | State | Closed By | Verified Exit |
|---|---|---|---|
| E4-TD-001 | **CLOSED** | G05 | old Causal/Family lifecycle accepts no new Product writes |
| E4-TD-002 | **CLOSED** | G05 | all Product paths use persistent canonical StageExecution |
| E4-TD-003 | **CLOSED** | G05 | one canonical Result/Artifact new-write ownership boundary |

## 6.3 Planned but Not Yet Introduced

| TD | Introduced By | Purpose / Temporary Authority | Exit |
|---|---|---|---|
| E4-TD-005 | G06 | legacy runtime/migration surface pending explicit retirement boundary | G07 |
| E4-TD-006 | G07 | temporary compatibility/read projection pending final clean audit | G08 |

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
| E4-ADR-001 | Canonical Product runtime | **ESTABLISHED for new Product authority by G05**; final legacy/runtime retirement boundary G07 |
| E4-ADR-002 | Unified canonical persistent Execution aggregate | **ESTABLISHED G02; sole Product authority verified G05** |
| E4-ADR-003 | Common Execution identity and mutation semantics | **ESTABLISHED G02; cross-family convergence reverified G05** |
| E4-ADR-004 | Persistent StageExecution for canonical workflows | **ESTABLISHED G03; full Product path convergence verified G05** |
| E4-ADR-005 | GenericExecutor remains workflow infrastructure | **ESTABLISHED G03; reverified non-authoritative G05** |
| E4-ADR-006 | Explicit Result semantic levels under one ownership contract | **ESTABLISHED G04; sole Product path verified G05** |
| E4-ADR-007 | One Product Artifact metadata authority, separate physical store | **ESTABLISHED G04; sole Product path verified G05** |
| E4-ADR-008 | Typed authority plus generic-only lineage | contract fixed; **runtime consolidation NEXT G06** |
| E4-ADR-009 | Legacy runtime retirement/archive boundary | G07 |
| E4-ADR-010 | Product-only canonical migration/bootstrap | migration head `0010`; final boundary G07/G08 |
| E4-ADR-011 | Standalone CLI boundary | Product canonical-submit boundary **verified G05**; final legacy/standalone cleanup G07 |
| E4-ADR-012 | Compatibility terminology is non-architectural unless consumed | G07 |

---

# 8. Invariant Status

| Invariant | Short Meaning | Current Status | Primary Gate |
|---|---|---|---|
| E4-INV-001 | one canonical persistent Execution identity | **ESTABLISHED; TD-001 CLOSED G05** | G02/G05 |
| E4-INV-002 | family changes workflow, not lifecycle authority | **ESTABLISHED; sole authority verified G05** | G02/G05 |
| E4-INV-003 | retry keeps identity; differs from rerun/revise | **ESTABLISHED** | G02 |
| E4-INV-004 | auditable claim/state transitions | **ESTABLISHED; REVERIFIED G03/G05** | G02/G03/G05 |
| E4-INV-005 | centralized claim/lease authority | **ESTABLISHED; TD-001 CLOSED G05** | G02/G05 |
| E4-INV-006 | every canonical Execution has persistent stages | **ESTABLISHED; TD-002 CLOSED G05** | G03/G05 |
| E4-INV-007 | GenericExecutor cannot commit canonical lifecycle/Result/Artifact metadata | **ESTABLISHED; REVERIFIED G05** | G03/G05 |
| E4-INV-008 | every Result belongs to canonical Execution and declares level | **ESTABLISHED; TD-003 CLOSED G05** | G04/G05 |
| E4-INV-009 | one Artifact metadata owner; locator distinct | **ESTABLISHED; TD-003 CLOSED G05** | G04/G05 |
| E4-INV-010 | DB/store compensation/reconciliation semantics | **ESTABLISHED** | G04 |
| E4-INV-011 | one lineage authority per semantic relation | **TARGET FIXED / TD-004 OPEN** | G06 |
| E4-INV-012 | closure/export cannot become lineage authority | **TARGET FIXED; runtime consolidation G06** | G06 |
| E4-INV-013 | canonical runtime imports no retired legacy runtime | PENDING final audit | G07 |
| E4-INV-014 | shared science survives without legacy orchestration | TARGET FIXED; verify later | G07 |
| E4-INV-015 | canonical bootstrap does not invoke root legacy migrations | TARGET FIXED; final verify later | G07/G08 |
| E4-INV-016 | no indefinite dual read/write final architecture | **NOT FINAL; bounded TD-004 active** | G06/G08 |

---

# 9. Requirement Families — Where to Look

The 35 requirements should not be memorized individually during normal implementation. Use these ranges.

| Requirement Range | Concern | Current State |
|---|---|---|
| E4-REQ-001..002 | Product runtime / legacy roots | **new Product authority converged G05**; final legacy root retirement G07/G08 |
| E4-REQ-003..010 | Execution identity/lifecycle/claim/mutations | **G02 established; sole cross-family Product path verified G05** |
| E4-REQ-011..014 | persistent stage / query / GenericExecutor boundary | **G03 established; full Product convergence verified G05** |
| E4-REQ-013 | stage-side ownership relation | **G03/G04 established; G05 converged** |
| E4-REQ-015..020 | Result / Artifact / typed downstream reuse | **G04 established; sole Product path verified G05** |
| E4-REQ-021..025 | lineage authority | **G06 NEXT** |
| E4-REQ-026..029 | shared science / legacy retirement classification | G07 |
| E4-REQ-030..032 | Product-only migration/bootstrap/data policy | evidence exists through migration `0010`; final G07/G08 |
| E4-REQ-033..035 | CLI / compatibility terminology | Product canonical-submit/read boundary verified G05; final legacy/terminology boundary G07 |

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

# 11. G06 — Immediate Next Gate Control Card

## 11.1 Objective

> Consolidate lineage authority so that each semantic relation has exactly one authoritative representation: typed structural authority for known structural relations, generic persistence only for relations that are genuinely generic-only, and closure/export as read projection only.

G06 must close `E4-TD-004` without reopening the Product Execution authority already verified by G05.

## 11.2 Architecture Before G06

```text
G02 canonical Execution authority              ESTABLISHED
G03 persistent StageExecution                  ESTABLISHED
G04 Result / Artifact ownership                ESTABLISHED
G05 sole Product Execution convergence         ESTABLISHED

TD-001                                           CLOSED
TD-002                                           CLOSED
TD-003                                           CLOSED

BUT:

TD-004 structural lineage generic duplication   OPEN
typed structural lineage target                 FIXED
generic-only persisted lineage target           FIXED
closure/export projection-only target           FIXED
```

## 11.3 G06 Must Establish

```text
For every lineage relation family:

1. identify semantic authority
2. classify relation as:
       typed structural
       generic-only
3. ensure one persisted authority per semantic relation
4. stop duplicate generic writes for structural relations
5. preserve generic persistence only for generic-only relations
6. make closure/export read projection only
7. keep lineage readers consistent with the authoritative relation model
```

G06 must cover lineage emitted or consumed by Causal / Exploratory / Predictive canonical Product flows.

## 11.4 G06 Primary Audit Question

> Can the same semantic lineage relation become authoritative in more than one persisted representation, or can a closure/export projection become an authority?

G06 may PASS only if the verified answer is:

```text
NO
```

## 11.5 G06 Must Close

```text
E4-TD-004
```

Exit criterion:

```text
one semantic relation -> one authoritative lineage representation

typed structural relations:
    typed authority only

generic-only relations:
    generic persistence only

closure/export:
    projection only
    never authority
```

## 11.6 G06 MUST NOT Do

```text
DO NOT reopen G05 Product Execution / Stage / Result / Artifact authority.
DO NOT reintroduce Family new-write authority.
DO NOT make GenericExecutor a lineage persistence authority.
DO NOT broadly delete/archive legacy runtime source.      # G07
DO NOT finalize CLI / migration retirement.               # G07
DO NOT perform final clean bootstrap architecture audit.  # G08
DO NOT redesign scientific algorithms.
```

## 11.7 Expected Next Transition Debt

If required by the approved Gate decomposition:

```text
E4-TD-005
Introduced: G06
Exit Gate: G07
Purpose: bounded legacy runtime / migration surface pending explicit retirement boundary
```

This Control Card is a condensed operational index only.
Formal G06 implementation/test acceptance authority must come from the G06 Gate-local `06` / `07` when created.

---

# 12. What Is Deliberately Still Unresolved

The following are **not defects at this snapshot** because their exit Gates are later.

### Lineage — active Transition Debt

```text
E4-TD-004 OPEN -> G06
```

Canonical Product Execution / StageExecution / Result / Artifact authority is established.
What remains is lineage authority consolidation: structural relations must stop being dual-authored through generic representations, generic persistence must become generic-only, and closure/export must remain projection-only.

### Legacy retirement

Legacy source/runtime/compatibility surfaces may remain, but they are **not** allowed to recover new Product authority.
Their final retirement/archive classification is G07.

### CLI / migration boundary

G05 verified the canonical Product submission boundary and preserved low-level scientific CLI separation.
Final legacy CLI classification and Product-only migration/bootstrap retirement boundary remain G07.

### Final bootstrap / architecture audit

The repository-managed PostgreSQL runner proves Product migration operation through:

```text
20260809_product_0010
```

The final clean-bootstrap convergence and `OPEN TRANSITION DEBT = 0` audit remain G08.

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


## G05

Trial 01 is retained as failed evidence:

```text
30_test_report/G05/
E4-G05_01_999_gate_decision.md
Decision: FAIL
```

Trial 02 fixed implementation/test candidate:

```text
ad3e3e124ee47f9cbaa2470b25263b7289795262
```

Trial 02 implementation completion report:

```text
20_implementation_reports/G05/Trial02/
E4-G05_02_implementation_completion_report.md
```

Trial 02 remediation evidence:

```text
20_implementation_reports/G05/Trial02/
E4-G05_02_R1_predictive_retry_remediation_report.md

20_implementation_reports/G05/Trial02/
E4-G05_02_R2_combined_regression_remediation_report.md
```

Trial 02 final decision:

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
   -> G06 NEXT

2. What is already protected?
   -> G02 canonical Execution identity/lifecycle/claim
   -> G03 persistent StageExecution
   -> G03 GenericExecutor non-authority
   -> G04 Result / Artifact ownership and typed reuse
   -> G05 all-family canonical Product convergence
   -> G05 no Family new Product write authority
   -> G05 no canonical-failure fallback to old authority

3. What Transition Debt is intentionally alive?
   -> TD-004 lineage authority duplication only
   -> TD-001 / TD-002 / TD-003 are CLOSED

4. What must G06 do?
   -> identify one authoritative lineage representation per semantic relation
   -> keep typed structural relations typed-authoritative
   -> keep generic persistence generic-only
   -> make closure/export projection-only
   -> close TD-004

5. What must NOT be touched yet?
   -> G07 broad legacy / CLI / migration retirement
   -> G08 final clean bootstrap / architecture audit
   -> passed G02-G05 authority contracts

6. What is the G06 exit condition?
   -> no semantic lineage relation is dual-authoritative
   -> structural relation generic duplicate writes are stopped
   -> generic persistence is generic-only
   -> closure/export is never authority
   -> TD-004 CLOSED
```

If these six answers remain true, the work is still aligned with ENH-E4.
