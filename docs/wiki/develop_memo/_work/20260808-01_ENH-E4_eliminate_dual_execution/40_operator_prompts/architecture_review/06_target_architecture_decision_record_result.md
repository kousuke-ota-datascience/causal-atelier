# 06 Target Architecture Decision Record

## 1. Metadata

- Prompt: `06_target_architecture_decision_record_prompt.md`
- Prior phases: Architecture Review Phase 01–05; database reinitialization completion decision record.
- Repository: `/loc0/bigbrother/repositories/causal-atelier`
- Branch: `refactor/ariadne_mvp_e4`
- HEAD: `a2d499c19e19df16caa7900c1c080743ea702532`
- Working tree at start: existing ` D deploy/.nfs000000000076202f00000088`; Phase 06 prompt untracked.
- Started at: `2026-08-08T11:24:00Z`
- Finished at: `2026-08-08T11:29:00Z`
- Status: `COMPLETED_WITH_HUMAN_DECISIONS`
- Method: static architecture and database-decision-record synthesis; no production/schema/test/code change.

## 2. Executive Decision Summary

### Recommended Target Architecture

Adopt one canonical repository-managed Product persistent Execution aggregate for user-visible Causal, Exploratory, and Predictive analyses. Use a common execution identity, state/claim contract, transaction boundary, retry/rerun/revise semantics, and Result/Artifact/Lineage ownership boundary. Preserve family-specific scientific workflow semantics through an execution-family discriminator, workflow specification/plan, and persistent StageExecution contract.

The target is not “make every scientific operation identical.” It is “remove multiple authoritative Product execution lifecycles while retaining explicit workflow-specific semantics.”

Recommended authority split:

- canonical Execution: one Product aggregate and one lifecycle contract;
- StageExecution: first-class persistent child for all canonical workflows;
- Result: explicit ExecutionResult and StageResult concepts where semantics differ, with one ownership contract and one API identity policy;
- Artifact metadata: one Product metadata ownership boundary; physical bytes remain behind `ArtifactStorePort`;
- Lineage: typed relationships are authoritative for relations represented by typed persistent fields; generic lineage is retained only for explicit generic-only relations; closure is a read projection;
- Legacy runtime/persistence/orchestration: non-canonical and proposed for bounded retirement/archive after external-consumer decision;
- shared scientific modules: retained independently and not treated as legacy runtime.

### Decisions Requiring Human Approval

- Approval of one unified Product Execution aggregate and persistent StageExecution contract.
- Approval of the Result/Artifact unification boundary, especially whether a new unified metadata table is in scope for ENH-E4 implementation.
- Approval of generic-only LineageEdge authority policy.
- Approval of legacy external-compatibility assumption and retirement/archive boundary.
- Approval of Product-only migration/bootstrap as the target clean-install path.

### Decisions Blocked by Evidence

No core Product target decision is blocked. Legacy source removal is conditionally blocked by unresolved external consumers (E4-UNK-024..029). The decision record therefore proposes a repository-local target with an explicit external compatibility gate; it does not assert that no external consumer exists.

## 3. Current Architecture Problem Statement

### 3.1 Runtime

Repository-managed runtime already uses Product API, Product worker, Product migrations, and Product scientific adapters. Standalone Product CLIs are direct scientific-core utilities. Legacy API/worker/CLI roots remain in source but are excluded from current package/deployment surfaces. Thus the repository contains multiple runtime families, while only one is repository-managed as the active Product runtime.

Evidence: Phase 01/05; `pyproject.toml:19-64`; `.dockerignore:14-24`; `Dockerfile:10-20`; `compose.yaml:18-53`.

### 3.2 Execution

Causal uses `ExecutionOrm`/`product_execution`, domain/repository UoW, and a Product worker branch. Exploratory/Predictive use `FamilyExecutionOrm`/`product_family_execution`, direct service sessions, family stages, and separate claim/mutation paths. They share `GenericExecutor` only as in-memory stage sequencing/runner infrastructure, not as lifecycle owner.

Consequence: user-visible Product analyses have multiple authoritative execution identities, claimers, state mutation paths, and retry semantics.

Evidence: Phase 02 E4-OBS-014..032 and Phase 02 lifecycle matrices.

### 3.3 Result / Artifact

Causal Results/Artifacts use `product_result`/`product_artifact`; family Results/Artifacts use `product_family_result`/`product_family_artifact`. Causal Result is execution-scoped; family Result is execution+stage-scoped; family Artifact may exist without a Result. Causal and family services also use different repository/ORM persistence styles and different retry cleanup.

Consequence: common conceptual outputs do not currently have one ownership model or one mutation contract.

Evidence: Phase 03 E4-OBS-033..041 and E4-INF-013..018.

### 3.4 Lineage

Product contains typed/derived readers, persisted `product_lineage_edge`, hybrid closure, and export-synthetic lineage. Family services write generic edges; normal Causal processing has no confirmed generic write path. The same semantic relation may be derived and persisted, while no cross-source reconciliation mechanism is confirmed.

Consequence: lineage authority and duplicate representation are ambiguous.

Evidence: Phase 04 E4-OBS-042..051 and E4-INF-019..025.

### 3.5 Legacy

Legacy contains separate API, CLI, execution/control plane, worker, Result/Artifact/ArtifactLineage persistence, and old infrastructure. No Product/shared production import into `ariadne.legacy` was confirmed. Shared scientific modules such as `ariadne.causal` and preprocessing are consumed by both Product adapters and legacy adapters.

Consequence: legacy orchestration and shared scientific capability must be decided separately; deleting a legacy directory wholesale would conflate them.

Evidence: Phase 05 E4-OBS-052..063 and E4-INF-026..032.

### 3.6 Migration

Database reinitialization evidence shows pre-production application data had no retention requirement, Product clean rebuild succeeded from `product_migrations` alone, the active database had Product tables only, and legacy migration state did not reappear after startup.

Consequence: Product-only migration/bootstrap is evidence-supported for the clean target path. It does not prove that arbitrary external legacy databases or external consumers can be discarded.

Evidence: `database_reinitialization/99_completion_summary_decision_record.md:40-44,183-217,288-371,756-813,1010-1038`.

## 4. Architectural Goals

1. Exactly one canonical persistent Product Execution architecture for user-visible analyses.
2. One execution identity and lifecycle contract across Causal, Exploratory, and Predictive.
3. Explicit separation between lifecycle orchestration and scientific workflow execution.
4. One Result/Artifact ownership contract while preserving execution-level versus stage-level semantics.
5. One physical object-storage port and one metadata ownership boundary.
6. One explicit authority rule per semantic lineage relation.
7. Eliminate indefinite dual authoritative Product execution/Result/Artifact/Lineage management.
8. Preserve shared scientific implementations without retaining legacy orchestration as an active authority.
9. Bootstrap the target Product schema through the Product migration chain only.
10. Keep external compatibility assumptions visible and bounded.

## 5. Non-goals

- Scientific algorithm or statistical-method redesign.
- Numerical correctness revalidation.
- Frontend UX redesign.
- Unrelated dataset, authentication, or deployment redesign.
- Immediate deletion of legacy source or historical migrations.
- Historical data migration unless a separate retention requirement is approved.
- General plugin architecture.
- Automatic acceptance of any ADR by this agent.
- Gate-by-gate coding or implementation in this phase.

## 6. Decision Criteria

| Criterion | Meaning |
|---|---|
| Single Source of Truth | one authoritative lifecycle/relationship owner |
| Semantic Coherence | preserves meaningful family/stage distinctions |
| Lifecycle Consistency | common claim/state/retry/cancel contract |
| Persistence Consistency | common aggregate and transaction ownership |
| Failure Correctness | deterministic failure/partial-output behavior |
| Lineage Integrity | no ambiguous independent authorities |
| Auditability | identity, stage, result, artifact and lineage traceability |
| Scientific Preservation | shared estimators/algorithms remain unchanged |
| Migration Simplicity | clean bootstrap and bounded data policy |
| Operational Simplicity | one repository-managed runtime family |
| Testability | one contract with explicit family-specific cases |
| Extensibility | new workflow families do not create another lifecycle |
| Compatibility Risk | external/legacy breakage is explicit and gated |

## 7. Candidate Architecture Overview

### Candidate A — Causal Execution canonical

Extend `product_execution` and its domain/UoW to absorb family executions and stages.

### Candidate B — Family Execution canonical

Extend `product_family_execution` and direct service model to absorb causal executions and add causal-specific semantics.

### Candidate C — New unified Execution aggregate

Define a new canonical Product Execution aggregate with family discriminator, common lifecycle/claim/state contract, and persistent StageExecution child. Migrate Causal and Family adapters behind it.

### Candidate D — Keep two persistent lifecycles with documented roles

Retain `product_execution` and `product_family_execution` as independent authorities and document their intended boundaries.

### Candidate E — External orchestration only

Move common lifecycle to a generic external scheduler while retaining domain-specific persistence internally.

## 8. Candidate Comparison Matrix

| Criterion | A | B | C | D | E | Notes |
|---|---|---|---|---|---|---|
| Single execution authority | ACCEPTABLE after large causal extension | ACCEPTABLE after large family extension | STRONG | WEAK | UNKNOWN | D preserves current dual authority |
| Semantic family/stage fidelity | WEAK/ACCEPTABLE | ACCEPTABLE | STRONG | STRONG | UNKNOWN | C models differences explicitly |
| Common claim/state/retry | ACCEPTABLE | ACCEPTABLE | STRONG | WEAK | UNKNOWN | current claimers differ |
| Migration complexity | ACCEPTABLE | ACCEPTABLE | WEAK | STRONG short-term | WEAK | C has highest transition cost |
| Result/Artifact alignment | ACCEPTABLE | ACCEPTABLE | STRONG | WEAK | UNKNOWN | C can define one ownership contract |
| Lineage authority | ACCEPTABLE | ACCEPTABLE | STRONG | WEAK | UNKNOWN | requires separate lineage decision |
| Scientific preservation | STRONG | STRONG | STRONG | STRONG | UNKNOWN | all can preserve shared modules |
| Operational simplicity | ACCEPTABLE | ACCEPTABLE | STRONG | WEAK | WEAK | E adds another authority |
| Testability | ACCEPTABLE | ACCEPTABLE | STRONG | WEAK | UNKNOWN | one contract is easier to assert |
| ENH-E4 objective | ACCEPTABLE | ACCEPTABLE | STRONG | UNACCEPTABLE | UNKNOWN | D does not eliminate dual execution |
| Recommendation | not selected | not selected | **recommended** | rejected | out of scope | rationale below |

Candidate C is recommended because the problem is not only that one current table is smaller/cleaner; it is that two current Product lifecycle authorities differ in claim, stage, result, lineage, and mutation semantics. A new aggregate makes the target contract independent of either current table’s accidental boundaries. The cost is higher migration/implementation complexity and therefore requires human approval.

## 9. Recommended Target Architecture

### 9.1 Runtime

Canonical repository-managed runtime:

```text
Product API / Product CLI adapters
        ↓
Canonical Execution Application Service
        ↓
Canonical Execution repository + Unit of Work
        ↓
Canonical worker claim/lease
        ↓
Family-specific workflow adapter / scientific runner
```

Legacy API/worker/CLI are non-canonical runtime surfaces. Shared scientific modules remain active shared capability.

### 9.2 Execution

Use one canonical persistent Execution aggregate with:

- globally unique Product `execution_id` for every user-visible Product analysis;
- explicit execution family/type: `CAUSAL`, `EXPLORATORY`, `PREDICTIVE`;
- immutable submission/specification snapshot;
- common state, claim token/lease, timestamps, retry count, and terminal outcome;
- family-specific workflow specification/plan references;
- explicit parent/base execution reference for rerun/revise lineage;
- one repository/claim abstraction and one UoW boundary.

The target aggregate is a semantic contract, not a requirement to preserve either current table unchanged.

### 9.3 Stage

Make StageExecution a persistent first-class child of every canonical Execution. A stage row must carry workflow-specific stage key/type, ordinal/dependencies, state, attempt history, timestamps, input/output bindings, and failure details. Causal workflows with currently ephemeral stages receive an explicit stage representation; family workflows retain their existing stage semantics behind the common contract.

This is recommended over Option B because retry granularity, progress, auditability, Result ownership, and failure recovery require a stable stage boundary across families.

### 9.4 Worker

Use one canonical claim mechanism:

- repository-level atomic claim;
- row lock/skip-locked equivalent appropriate to the storage;
- claim token and lease expiry;
- explicit claim commit before processing;
- family-neutral state transitions;
- family adapter dispatch after claim;
- terminal state/result/artifact commit through the same aggregate UoW;
- heartbeat/lease-renewal contract if processing can exceed lease duration.

The target requires lease renewal semantics even though current Phase 02 evidence did not confirm complete heartbeat behavior.

### 9.5 GenericExecutor

Keep `GenericExecutor` subordinate to the canonical lifecycle. It may own plan validation, stage ordering, binding resolution, runner invocation, and in-memory stage outcome production. It must not own canonical claim, lease, execution identity, transaction commit, retry policy, Result persistence, Artifact metadata persistence, or generic lineage authority.

### 9.6 Result

Use two explicit semantic levels under one Result ownership contract:

- ExecutionResult: final/aggregate scientific output associated with canonical Execution;
- StageResult: stage output associated with canonical StageExecution where a stage produces a persistent scientific result.

They are not duplicate implementations of one indistinguishable concept. They must have explicit type/level discriminators, stable IDs, execution relation, optional stage relation, status/payload/diagnostics, and defined cardinality. The target API may expose a unified Result resource with level metadata, but persistence semantics must remain explicit.

A single current-table choice is not recommended because Causal execution-level and Family stage-level semantics differ materially.

### 9.7 Artifact

Use one Product Artifact metadata ownership contract separate from physical storage:

- one Product-level Artifact metadata authority;
- artifact ID separate from physical `object_key`;
- mandatory canonical Execution association;
- optional Result and StageExecution associations;
- explicit artifact kind/schema/hash/media/size/metadata;
- one `ArtifactStorePort` for physical store;
- exactly one service/aggregate boundary creates, persists, links, and deletes owned metadata;
- DB commit and physical object store remain separate resources with compensating cleanup unless a stronger storage transaction is introduced.

Artifact-only stage outputs remain valid; Result linkage is optional where the workflow contract permits it.

### 9.8 Downstream Reuse

Canonical downstream references are typed Product IDs:

- Result reuse uses Result ID plus a typed relation/role;
- Artifact reuse uses Artifact ID plus metadata/hash validation;
- physical `object_key` is an implementation locator, not the semantic input identity;
- DatasetVersion/GraphVersion remain typed domain references;
- family-to-causal reuse must use an explicit typed bridge or normalized input contract, not an untyped family Result ID passed into causal `input_result_id`;
- content hashes are snapshots/integrity evidence, not substitutes for ownership IDs.

### 9.9 Lineage

Use an explicit hybrid authority policy:

1. Typed persistent relationships are authoritative for structural relations represented by typed fields: input Result/Graph/Dataset, execution/result ownership, result/artifact ownership, and revision/base relations.
2. Generic persisted lineage is authoritative only for generic-only relations not represented by typed fields, such as explicit evidence, documentation, model-card, stage artifact derivation, and user-authored links.
3. Closure is a read projection, not an additional authority.
4. Structural relations must not be independently written to generic lineage as a second authority in the final state.
5. Generic-only edges require endpoint validation, project scope validation, unique identity, and deletion/retention semantics.
6. Export is a snapshot projection and must identify whether each edge is typed-derived or generic persisted.

This is Candidate C (explicit hybrid) with a materialized read closure, not indefinite dual write.

### 9.10 Legacy

Separate legacy runtime/persistence/orchestration from shared scientific capability:

- propose `RETIRE_RUNTIME` for legacy API/worker/CLI as Product runtime surfaces;
- propose `ARCHIVE_SOURCE` or `REPLACE_BEFORE_RETIRE` for legacy orchestration/domain/persistence/lineage source after external boundary approval;
- retain `ariadne.causal`, `ariadne.preprocessing`, and `ariadne.shared` as independent shared capability;
- retain historical migration files as archive/history until a separate repository policy approves their removal;
- retain compatibility data strings only while a concrete Product/external contract requires them;
- do not remove legacy source solely because the name contains “legacy.”

### 9.11 Migration

Use `alembic_product.ini` → `product_migrations` as the canonical target bootstrap chain. The database reinitialization record confirms a clean Product rebuild without running root legacy migrations and confirms no legacy schema state was regenerated.

For existing data, the current project context states no application-data retention requirement for this pre-production environment. Therefore the proposed ENH-E4 target policy is clean rebuild/bootstrap rather than an assumed historical data migration. If a retention requirement is introduced, it becomes a separate human-approved migration decision.

### 9.12 CLI

Keep standalone Product scientific CLIs outside the persistent Product Execution lifecycle when they are explicitly low-level scientific utilities and do not promise Product auditability/persistence. They must not become a second hidden orchestration architecture. If a CLI is promoted to a user-visible Product analysis command, it must submit through the canonical Execution service.

## 10. Current Architecture Diagram

```text
Product API ────────┬─> Causal ExecutionService ─> product_execution
                    │                         └─> Product worker branch
                    ├─> ExploratoryService ──> product_family_execution
                    │                         └─> family stages/results/artifacts
                    └─> PredictiveService ───> product_family_execution
                                              └─> family stages/results/artifacts

GenericExecutor: shared in-memory stage sequencing/runner dispatch
Result: product_result OR product_family_result
Artifact: product_artifact OR product_family_artifact
Lineage: typed-derived readers + product_lineage_edge + hybrid closure
Legacy: separate API/CLI/worker/persistence/ArtifactLineage
Scientific: shared ariadne.causal/preprocessing modules
Migrations: product_migrations (active) + root migrations (legacy/history)
```

## 11. Target Architecture Diagram

```text
Product API / promoted CLI
          │
          v
Canonical Execution Service
          │
          v
Canonical Execution Aggregate
  execution_id + family + state + claim/lease + snapshot
          │
          ├── persistent StageExecution children
          │       │
          │       └── family workflow adapter / GenericExecutor
          │                               │
          │                               └── shared scientific runner
          │
          ├── ExecutionResult / StageResult
          │
          ├── Product Artifact metadata ──> ArtifactStorePort/object store
          │
          └── typed lineage authority
                      └── generic-only LineageEdge store
                              └── closure/export read projections

Legacy API/CLI/worker/persistence: retired/archive boundary
Shared scientific modules: retained independently
Canonical bootstrap: product_migrations only
```

## 12. Architecture Decisions

### E4-ADR-001 — Canonical Product runtime

- Status: `PROPOSED_FOR_HUMAN_APPROVAL`
- Context: Product runtime is repository-managed; legacy roots are excluded from packaging/deployment but remain in source.
- Evidence: E4-OBS-052..058; Phase 01; database decision record.
- Decision: Product API, canonical Product worker, Product persistence, and promoted Product CLI are the canonical runtime family. Legacy runtime roots are non-canonical.
- Alternatives: retain both runtime families; make legacy canonical; external scheduler.
- Rationale: removes repository-managed ambiguity while preserving shared scientific modules.
- Consequences: legacy external compatibility requires explicit gate; standalone utility CLI remains distinct.
- Risks: external consumers may depend on legacy roots.
- Human approval required: yes.
- Derived requirements: E4-REQ-001, E4-REQ-002.

### E4-ADR-002 — Unified canonical persistent Execution aggregate

- Status: `PROPOSED_FOR_HUMAN_APPROVAL`
- Context: Causal and Family Product executions have separate entities/tables, claimers, state paths, and mutation semantics.
- Evidence: Phase 02 E4-OBS-014..032; E4-INF-012.
- Decision: introduce one canonical persistent Execution aggregate with family discriminator and workflow-specific plan/specification.
- Alternatives: Candidate A, B, D.
- Rationale: Candidate D preserves the dual authoritative lifecycle that ENH-E4 is intended to eliminate; A/B privilege accidental current table shape; C addresses semantics directly.
- Consequences: substantial migration/implementation work; current tables cannot remain independent authorities in final state.
- Risks: aggregate may become over-generalized.
- Human approval required: yes.
- Derived requirements: E4-REQ-003..006.

### E4-ADR-003 — Common Execution identity and mutation semantics

- Status: `PROPOSED_FOR_HUMAN_APPROVAL`
- Context: current retry/rerun/revise semantics differ by lifecycle.
- Evidence: Phase 02; Phase 03; Phase 04.
- Decision: one globally unique Product `execution_id); retry preserves identity and creates a new attempt/retry record; rerun creates a new execution; revise creates a new execution with typed base/source relation; cancel is a terminal execution transition and does not silently delete successful prior outputs.
- Alternatives: per-family IDs; retry creates new execution; in-place revise.
- Rationale: preserves traceability and separates attempt from new analytical execution.
- Consequences: old rows need explicit output/attempt cleanup semantics.
- Risks: current causal duplication behavior is unresolved.
- Human approval required: yes.
- Derived requirements: E4-REQ-007..010.

### E4-ADR-004 — Persistent StageExecution for canonical workflows

- Status: `PROPOSED_FOR_HUMAN_APPROVAL`
- Context: family has persistent stages; causal stage persistence is not confirmed.
- Evidence: Phase 02 E4-OBS-018, E4-OBS-021, E4-OBS-024, E4-OBS-026, E4-UNK-007.
- Decision: all canonical Executions have persistent StageExecution children; stage persistence is the audit/retry boundary.
- Alternatives: causal ephemeral stages; family-only stage persistence.
- Rationale: common progress, failure, result ownership, and lineage semantics.
- Consequences: additional persistence for currently causal stage boundaries.
- Risks: schema complexity and migration cost.
- Human approval required: yes.
- Derived requirements: E4-REQ-011..013.

### E4-ADR-005 — GenericExecutor remains workflow infrastructure

- Status: `PROPOSED_FOR_HUMAN_APPROVAL`
- Context: current GenericExecutor has no persistence/claim/commit ownership.
- Evidence: Phase 02 E4-OBS-026 and E4-INF-009.
- Decision: keep it responsible for plan/stage sequencing and runner invocation only.
- Alternatives: make it lifecycle owner; duplicate family-specific executors.
- Rationale: preserves separation of orchestration and scientific execution.
- Consequences: canonical service owns persistence and state transitions.
- Human approval required: yes.
- Derived requirements: E4-REQ-014.

### E4-ADR-006 — Explicit Result semantic levels under one ownership contract

- Status: `PROPOSED_FOR_HUMAN_APPROVAL`
- Context: Causal Result is execution-scoped; Family Result is execution+stage-scoped.
- Evidence: Phase 03 E4-OBS-033..035; E4-INF-013..014.
- Decision: retain explicit ExecutionResult/StageResult semantic levels, with one canonical ownership/API contract; do not pretend they are identical payload units.
- Alternatives: causal table canonical; family table canonical; one undifferentiated Result row.
- Rationale: avoids both duplicate ownership and semantic erasure.
- Consequences: Result level/type/cardinality contracts must be explicit.
- Human approval required: yes.
- Derived requirements: E4-REQ-015..017.

### E4-ADR-007 — One Product Artifact metadata authority, separate physical store

- Status: `PROPOSED_FOR_HUMAN_APPROVAL`
- Context: current causal/family Artifact tables differ but share physical store port.
- Evidence: Phase 03 E4-OBS-035..037; E4-INF-015.
- Decision: unify metadata ownership contract and retain `ArtifactStorePort` as physical storage boundary; object key is not semantic identity.
- Alternatives: retain two metadata authorities; DB BLOB; physical key as canonical identity.
- Rationale: separates domain ownership from storage implementation.
- Consequences: artifact-only stage outputs and optional Result links remain supported.
- Human approval required: yes.
- Derived requirements: E4-REQ-018..020.

### E4-ADR-008 — Typed authority plus generic-only lineage

- Status: `PROPOSED_FOR_HUMAN_APPROVAL`
- Context: current Product uses typed derivation, family generic writes, and hybrid closure without reconciliation.
- Evidence: Phase 04 E4-OBS-042..051; E4-INF-019..025.
- Decision: typed fields are authoritative for structural relations; generic lineage is authoritative only for generic-only relations; closure/export are projections.
- Alternatives: derived-only; generic-only; indefinite dual authority.
- Rationale: preserves non-reconstructable relations without allowing duplicate authority.
- Consequences: current family duplicate structural writes must be bounded/transitional; generic-only edge validation is required.
- Human approval required: yes.
- Derived requirements: E4-REQ-021..025.

### E4-ADR-009 — Legacy runtime retirement/archive boundary

- Status: `PROPOSED_FOR_HUMAN_APPROVAL`
- Context: no repository-local Product inbound dependency; external consumers are unknown; shared scientific code is independently used.
- Evidence: Phase 05 E4-OBS-052..063; E4-INF-026..032.
- Decision: retire legacy API/CLI/worker as Product runtime surfaces; retain shared scientific modules; archive or replace legacy orchestration/persistence/lineage source only after external compatibility gate.
- Alternatives: keep all legacy active; remove all legacy immediately; migrate all legacy science.
- Rationale: separates orchestration retirement from capability preservation and respects external boundary.
- Consequences: a bounded external inventory/approval is required before source removal.
- Human approval required: yes.
- Derived requirements: E4-REQ-026..029.

### E4-ADR-010 — Product-only canonical migration/bootstrap

- Status: `PROPOSED_FOR_HUMAN_APPROVAL`
- Context: clean Product rebuild succeeded from Product migrations; no application-data retention requirement was recorded.
- Evidence: database completion decision record, especially DR-02 and clean-state verification.
- Decision: Product target bootstrap uses `product_migrations` only; root legacy migrations remain historical/archive until separately decided; default ENH-E4 data policy is clean rebuild for pre-production.
- Alternatives: run both chains; dual-read transition; in-place historical migration.
- Rationale: observed clean rebuild works and active database had no legacy schema coexistence.
- Consequences: historical data retention is out of scope unless a new requirement is approved.
- Human approval required: yes.
- Derived requirements: E4-REQ-030..032.

### E4-ADR-011 — Standalone CLI boundary

- Status: `PROPOSED_FOR_HUMAN_APPROVAL`
- Context: Product CLI calls scientific adapters directly and writes local manifests without Product Execution persistence.
- Evidence: Phase 01/02 E4-OBS-010, E4-OBS-011, E4-OBS-027.
- Decision: keep low-level scientific CLI outside canonical persistent lifecycle; any user-visible auditable analysis CLI must submit to canonical Execution.
- Alternatives: integrate all CLI commands now; keep undocumented dual orchestration.
- Rationale: distinguishes utility purpose from Product analysis semantics.
- Consequences: CLI output is not a Product Execution/Result unless explicitly submitted.
- Human approval required: yes.
- Derived requirements: E4-REQ-033..034.

### E4-ADR-012 — Compatibility terminology is non-architectural unless consumed

- Status: `PROPOSED_FOR_HUMAN_APPROVAL`
- Context: Product retains `legacy-product-snapshot/1` and legacy-named test/data contracts.
- Evidence: Phase 05 E4-OBS-062; `product/domain/execution.py:15,63-73`; database/test evidence.
- Decision: retain names temporarily where Product validation or data compatibility consumes them; do not treat names as imports/dependencies; rename only through a separately scoped contract decision.
- Alternatives: immediate rename; treat all legacy-named strings as legacy runtime.
- Rationale: avoids unnecessary compatibility break and false dependency classification.
- Consequences: terminology debt remains explicitly tracked.
- Human approval required: yes.
- Derived requirements: E4-REQ-035.

## 13. Architecture Invariants

| ID | Invariant | Derived From |
|---|---|---|
| E4-INV-001 | Every user-visible Product analysis has exactly one canonical persistent Execution identity. | ADR-002 |
| E4-INV-002 | Execution family/type changes workflow semantics, not lifecycle authority. | ADR-002 |
| E4-INV-003 | Retry preserves execution identity and is distinguishable from rerun/revise. | ADR-003 |
| E4-INV-004 | Every canonical Execution has an auditable claim/state transition record. | ADR-003/004 |
| E4-INV-005 | Worker claim/lease ownership is centralized in the canonical Execution repository/service. | ADR-002/003 |
| E4-INV-006 | Every canonical Execution has persistent StageExecution children, including causal workflows. | ADR-004 |
| E4-INV-007 | GenericExecutor cannot commit canonical lifecycle or Result/Artifact metadata. | ADR-005 |
| E4-INV-008 | Every Result belongs to one canonical Execution and declares its semantic level. | ADR-006 |
| E4-INV-009 | Every Artifact metadata row has one canonical owner and a distinct physical locator. | ADR-007 |
| E4-INV-010 | Physical object storage and metadata commit have explicit compensation/reconciliation semantics. | ADR-007 |
| E4-INV-011 | Each semantic lineage relation has exactly one authority: typed or generic-only. | ADR-008 |
| E4-INV-012 | Closure/export cannot become an independent lineage authority. | ADR-008 |
| E4-INV-013 | Canonical Product runtime imports no retired legacy runtime module. | ADR-001/009 |
| E4-INV-014 | Shared scientific implementations remain importable without legacy orchestration. | ADR-009 |
| E4-INV-015 | Canonical bootstrap does not invoke root legacy migrations. | ADR-010 |
| E4-INV-016 | No indefinite dual-write/dual-read state remains as the final architecture. | ADR-008/010 |

## 14. Target Architecture Requirements

| ID | Requirement | ADR | Verification Concept |
|---|---|---|---|
| E4-REQ-001 | The repository-managed Product runtime SHALL use Product API and canonical Product worker as its production roots. | ADR-001 | static entry/deployment inspection |
| E4-REQ-002 | Legacy API/CLI/worker SHALL not be registered as canonical Product runtime roots. | ADR-001/009 | packaging/deployment contract |
| E4-REQ-003 | Every user-visible Product analysis SHALL create one canonical Execution aggregate. | ADR-002 | application contract/integration test |
| E4-REQ-004 | Canonical Execution SHALL carry an explicit CAUSAL/EXPLORATORY/PREDICTIVE family discriminator. | ADR-002 | schema/domain contract |
| E4-REQ-005 | Canonical lifecycle state transitions SHALL be shared across families, with family-specific invalid operations explicit. | ADR-002/003 | state-machine tests |
| E4-REQ-006 | Claim SHALL be performed through one repository/service abstraction with atomic ownership acquisition. | ADR-002/003 | concurrent claim test |
| E4-REQ-007 | Retry SHALL preserve execution ID and create a distinguishable attempt/retry record. | ADR-003 | mutation contract test |
| E4-REQ-008 | Rerun SHALL create a new execution ID and preserve a typed source relation. | ADR-003 | rerun lineage test |
| E4-REQ-009 | Revise SHALL create a new execution ID and preserve a typed base relation. | ADR-003 | revise lineage test |
| E4-REQ-010 | Cancel SHALL define terminal/partial-output behavior without silently rewriting successful prior outputs. | ADR-003 | cancellation contract test |
| E4-REQ-011 | Every canonical Execution SHALL have persistent StageExecution children. | ADR-004 | schema and lifecycle tests |
| E4-REQ-012 | Stage state and attempt history SHALL be queryable independently of scientific runner internals. | ADR-004/005 | API/repository contract |
| E4-REQ-013 | Stage result/artifact ownership SHALL identify execution and, where applicable, stage. | ADR-004/006/007 | FK/constraint tests |
| E4-REQ-014 | GenericExecutor SHALL not claim, commit, retry, or own canonical persistence. | ADR-005 | architecture/import tests |
| E4-REQ-015 | Result records SHALL declare ExecutionResult or StageResult semantic level. | ADR-006 | schema/domain validation |
| E4-REQ-016 | Result reuse SHALL use typed Result IDs and role/context, not physical object keys. | ADR-006/008 | downstream input contract |
| E4-REQ-017 | Execution-level and Stage-level Result cardinality SHALL be explicit per workflow family. | ADR-006 | schema/service tests |
| E4-REQ-018 | Product Artifact metadata SHALL have one ownership API/service boundary. | ADR-007 | architecture/service contract |
| E4-REQ-019 | Physical Artifact bytes SHALL be accessed through ArtifactStorePort; object key SHALL not be the semantic identity. | ADR-007 | port/contract test |
| E4-REQ-020 | Artifact-only stage outputs SHALL either be explicitly allowed by family contract or rejected; they SHALL not be accidental. | ADR-006/007 | validation test |
| E4-REQ-021 | Typed structural relations SHALL be the sole authority for reconstructable lineage relations. | ADR-008 | lineage authority tests |
| E4-REQ-022 | Generic lineage SHALL be restricted to typed-unrepresented relations or explicitly approved user links. | ADR-008 | relation allowlist test |
| E4-REQ-023 | Closure/export SHALL label or preserve the source class of each lineage relation. | ADR-008 | API/export contract |
| E4-REQ-024 | Generic-only lineage edges SHALL validate project scope, endpoint existence policy, uniqueness, and deletion behavior. | ADR-008 | persistence/service tests |
| E4-REQ-025 | Structural lineage SHALL not be independently dual-written indefinitely. | ADR-008 | architecture/reconciliation test |
| E4-REQ-026 | Shared scientific modules SHALL remain independent of legacy orchestration. | ADR-009 | import architecture test |
| E4-REQ-027 | Legacy runtime retirement SHALL be preceded by an explicit external-consumer decision. | ADR-009 | release gate/document review |
| E4-REQ-028 | Legacy source classification SHALL distinguish shared scientific capability, runtime, persistence, migration, and lineage. | ADR-009 | inventory review |
| E4-REQ-029 | Legacy ArtifactLineage/Result persistence SHALL not become a Product authority. | ADR-009 |
| E4-REQ-030 | Clean Product bootstrap SHALL use `product_migrations` and not the legacy migration chain. | ADR-010 | clean rebuild verification |
| E4-REQ-031 | Existing-data policy SHALL be explicit before destructive clean rebuild is used. | ADR-010 | decision record/release gate |
| E4-REQ-032 | Root legacy migrations SHALL remain history-only unless separately approved. | ADR-010 | migration configuration review |
| E4-REQ-033 | Low-level scientific CLI SHALL not silently create a second persistent Product lifecycle. | ADR-011 | CLI contract test |
| E4-REQ-034 | A user-visible auditable CLI analysis SHALL submit through canonical Execution. | ADR-011 | CLI/API contract |
| E4-REQ-035 | Legacy-named Product contracts SHALL be retained or renamed only through explicit compatibility evidence. | ADR-012 | contract inventory |

## 15. Implementation Constraints

| ID | Constraint | Rationale | ADR |
|---|---|---|---|
| E4-CON-001 | Do not redesign scientific algorithms as part of Execution unification. | preserve shared capability | ADR-009/011 |
| E4-CON-002 | Do not make GenericExecutor the lifecycle owner. | current responsibility/evidence | ADR-005 |
| E4-CON-003 | Do not leave current Causal and Family tables as independent final authorities. | violates canonical Execution decision | ADR-002 |
| E4-CON-004 | Do not use physical object keys as Result/Artifact semantic IDs. | storage/metadata separation | ADR-007 |
| E4-CON-005 | Do not independently write the same structural lineage relation to typed and generic authorities in the final state. | prevents dual authority | ADR-008 |
| E4-CON-006 | Any transition dual-read/write must have an owner, bounded duration, exit criterion, and reconciliation evidence. | no indefinite dual architecture | ADR-008 |
| E4-CON-007 | Do not run root legacy migrations in canonical Product bootstrap. | clean rebuild evidence | ADR-010 |
| E4-CON-008 | Do not remove legacy source before external compatibility decision. | external boundary unknown | ADR-009 |
| E4-CON-009 | Do not rename legacy-named data contracts solely from terminology. | compatibility evidence | ADR-012 |
| E4-CON-010 | Do not change unrelated frontend/auth/dataset behavior without direct dependency proof. | minimum necessary change | Section 5/ADR scope |

## 16. Legacy Component Target Classification

| Legacy Component | Proposed Target Status | Reason | Dependency Evidence | Human Approval |
|---|---|---|---|---|
| Legacy API | RETIRE_RUNTIME | no Product inbound path; non-canonical | E4-OBS-052,058 | yes |
| Legacy CLI | RETIRE_RUNTIME | Product CLI is separate; external users unknown | E4-OBS-053,058 | yes |
| Legacy worker | RETIRE_RUNTIME | Product worker is canonical | E4-OBS-055,058 | yes |
| Legacy execution/control plane | ARCHIVE_SOURCE | separate lifecycle/persistence; external boundary unresolved | E4-OBS-061,063 | yes |
| Legacy pipeline | REPLACE_BEFORE_RETIRE | shared preprocessing/ETL responsibilities require capability audit | E4-OBS-059 | yes |
| Legacy discovery | RETAIN_SHARED_CAPABILITY | retain shared `ariadne.causal` capability, not legacy orchestration | E4-OBS-059,060 | yes |
| Legacy inference/analysis-ready | REPLACE_BEFORE_RETIRE | shared estimators must remain; orchestration can be replaced | E4-OBS-059,060 | yes |
| Legacy domain/persistence | ARCHIVE_SOURCE | Product clean bootstrap does not need it; external data unknown | E4-OBS-056,057 | yes |
| Legacy Artifact/materialization | REPLACE_BEFORE_RETIRE | Product ArtifactStore boundary differs | Phase 03/05 | yes |
| Legacy ArtifactLineage | ARCHIVE_SOURCE | Product lineage policy is separate | Phase 04/05 | yes |
| Legacy infrastructure/contracts | ARCHIVE_SOURCE | old namespace/external dependency unresolved | E4-OBS-063 | yes |
| Legacy ETL/catalog | REPLACE_BEFORE_RETIRE | no Product equivalent fully confirmed | E4-UNK-025 | yes |
| `ariadne.causal`, `ariadne.preprocessing`, `ariadne.shared` | RETAIN_SHARED_CAPABILITY | consumed by Product and legacy; not legacy orchestration | E4-OBS-059,060 | yes |

## 17. Lineage Relation Target Classification

| Relation | Current Representation | Proposed Authority | Secondary Representation | Rationale |
|---|---|---|---|---|
| Execution→Result | typed FK + family generic edge | typed | closure projection | structural ownership |
| Result→Artifact | typed FK + family generic edge | typed | closure projection | structural ownership |
| Dataset/View→Execution | typed fields + family generic edge | typed | closure projection | input contract |
| Result→Execution input | `input_result_id` + derived/possible generic | typed | closure projection | causal downstream contract |
| Result→GraphVersion | `source_result_id` + derived | typed | closure projection | graph provenance |
| Artifact→DatasetVersion | `source_artifact_id` + derived | typed | closure projection | dataset source |
| Execution revision/base | revision context + predictive generic edge | typed base relation | generic only if additional evidence | identity relation |
| Artifact→Artifact stage derivation | generic only | generic-only LineageEdge | closure projection | no typed equivalent confirmed |
| Result→Result SUMMARIZES | generic only | generic-only LineageEdge | closure projection | semantic relation not typed |
| Result/Artifact DOCUMENTS/EVIDENCE_FOR | generic only | generic-only LineageEdge | closure/export | non-structural relation |
| User-authored links | generic only | generic-only LineageEdge | closure/export | explicit user relation |
| Legacy ArtifactLineage | legacy table | non-Product legacy authority | legacy API projection | separate architecture, no Product authority |

## 18. Execution Mutation Semantics

| Operation | Target Identity Semantics | Result Semantics | Lineage Semantics |
|---|---|---|---|
| retry | same Execution ID; new attempt/retry record | owned incomplete outputs are replaced or explicitly versioned under contract; no silent duplicate | attempt relation typed/persisted as defined; prior successful outputs protected |
| rerun | new Execution ID | new Results/Artifacts; source retained | typed RERUN/DERIVED_FROM relation |
| revise | new Execution ID; typed base/revision relation | new snapshot and outputs; source retained | typed REVISED_FROM relation |
| cancel | same ID becomes terminal/cancelled according to state contract | partial outputs explicitly marked/retained/deleted by family policy; no silent mutation of prior execution | cancellation does not erase historical lineage without explicit retention rule |

## 19. Data / Migration Policy

### Existing Data Assumption

Database decision evidence states this is pre-production and existing application data has no retention requirement. The proposed ENH-E4 default is therefore a clean rebuild assumption, not a general statement that all historical data may be destroyed.

### Target Bootstrap

Use Product migrations from empty persistence; verify Product application rows are empty after migration and before startup, then run Product startup/functional verification.

### Migration Chain

Canonical chain: `alembic_product.ini` → `product_migrations`. Root `alembic.ini` → `migrations` remains history-only and is not invoked by Product bootstrap.

### Compatibility

If a data-retention or external-schema requirement is later identified, stop clean-rebuild implementation and create a separate migration/compatibility ADR. No dual migration chain is part of the proposed final target.

## 20. Scientific Capability Preservation

| Capability | Current Owner | Target Owner | Change Allowed? | Evidence |
|---|---|---|---|---|
| Causal discovery | shared `ariadne.causal.discovery` plus legacy adapters | shared scientific module behind Product workflow adapter | orchestration adapter only | E4-OBS-059,060 |
| Treatment effect | shared estimator plus legacy/Product adapters | shared estimator behind canonical workflow | no algorithm rewrite | E4-DEP-003 |
| Edge weight | shared estimator plus legacy analysis-ready | shared estimator behind canonical workflow | no scientific redesign | E4-DEP-003 |
| Preprocessing/feature semantics | shared preprocessing plus family adapters | shared module with canonical workflow adapters | contract adaptation only | E4-DEP-004 |
| Validation/constants | shared modules | shared modules | preserve | E4-DEP-005 |
| Legacy CompleteJourney orchestration | legacy ETL namespace | not assumed canonical; replace/audit separately | only if required by Product workflow | E4-UNK-025 |

## 21. Compatibility Boundary

### Repository-local

Repository-local Product compatibility is the scope of this ADR. Current Product source must remain independent of `ariadne.legacy`; Product-only clean bootstrap is the target.

### External

External invocation of legacy roots is unknown. Before source/runtime removal, human approval must confirm either that external compatibility is explicitly out of ENH-E4 scope or that a bounded compatibility window is required.

### Data formats

`legacy-product-snapshot/1` and legacy-named fields are retained only while consumed by Product tests/domain/schema. They are not evidence of runtime package dependency.

### API/CLI

Legacy API/CLI are not canonical Product endpoints. Any externally promised legacy API/CLI requires a separate compatibility decision and exit date.

## 22. Risks

| Risk | Cause | Impact | Mitigation / Verification |
|---|---|---|---|
| unified aggregate becomes over-generalized | all family differences forced into one schema | semantic loss | explicit family workflow/stage contracts; ADR review |
| migration complexity | current Causal/Family tables are separate | implementation defects/data ambiguity | design schema transition separately; clean rebuild evidence |
| retry behavior changes | current causal/family cleanup differs | duplicate/lost outputs | define attempt/result retention tests before code |
| lineage duplication during transition | current family generic writes overlap typed derivation | stale/conflicting graph | bounded transition and reconciliation evidence |
| external legacy breakage | external consumers unknown | operational compatibility failure | external inventory gate before retirement |
| shared science accidentally removed | legacy and Product both use `ariadne.causal` | scientific regression | retain shared modules and import tests |
| artifact orphaning | DB/object store separate resources | storage leak or missing object | compensation/reconciliation invariant |
| historical data assumption wrong | no retention evidence could change | irreversible data loss | require explicit data policy before reset |
| CLI semantics misunderstood | utility vs user-visible analysis unclear | hidden second lifecycle | classify CLI purpose and route auditable use through Execution |

## 23. Human Decisions Required

| ID | Question | Options | Recommendation | Evidence | Blocking? |
|---|---|---|---|---|---|
| HD-001 | Approve unified canonical Execution aggregate? | A/B/C/D | C | Phase 02; ADR-002 | yes for implementation |
| HD-002 | Approve persistent StageExecution for Causal? | A/B/C | all canonical workflows | Phase 02 E4-UNK-007; ADR-004 | yes for schema |
| HD-003 | Approve Result semantic-level model? | unified/levelled | levelled under one ownership contract | Phase 03 | yes for Result design |
| HD-004 | Approve typed + generic-only lineage authority? | derived/generic/hybrid | explicit hybrid | Phase 04 | yes for lineage design |
| HD-005 | Is external legacy compatibility out of ENH-E4 scope? | yes/no/compatibility window | yes by default, but confirm | Phase 05 E4-UNK-024..029 | yes for legacy retirement |
| HD-006 | Approve Product-only clean bootstrap and no historical data migration? | clean rebuild/migrate/dual | clean rebuild for pre-production | database decision record | yes for destructive migration policy |
| HD-007 | Is standalone Product CLI permanently a utility boundary? | utility/integrated | utility unless user-visible audit is required | Phase 01/02 | no for core execution design |

## 24. ADR Dependency Graph

```text
ADR-001 runtime
   ├── ADR-002 unified Execution
   │      ├── ADR-003 identity/state mutation
   │      ├── ADR-004 persistent StageExecution
   │      └── ADR-005 GenericExecutor boundary
   ├── ADR-006 Result
   │      └── ADR-007 Artifact
   ├── ADR-008 Lineage
   ├── ADR-009 Legacy
   ├── ADR-010 Migration
   ├── ADR-011 CLI boundary
   └── ADR-012 compatibility terminology
```

## 25. Traceability Matrix

| Evidence | ADR | Invariant | Requirement | Implementation Area |
|---|---|---|---|---|
| Phase 02 E4-OBS-014..032 | ADR-001..005 | INV-001..007 | REQ-001..014 | execution service/repository/worker/stage |
| Phase 03 E4-OBS-033..041 | ADR-006..007 | INV-008..010 | REQ-015..020 | Result/Artifact aggregate/store |
| Phase 04 E4-OBS-042..051 | ADR-008 | INV-011..012,016 | REQ-021..025 | lineage writers/readers/closure |
| Phase 05 E4-OBS-052..063 | ADR-001,009,012 | INV-013..014 | REQ-001,002,026..029,035 | package/deploy/shared/legacy boundary |
| DB DR-02 and clean rebuild evidence | ADR-010 | INV-015 | REQ-030..032 | migration/bootstrap/data policy |
| Phase 01 E4-OBS-010..013 | ADR-001,011 | INV-001,013 | REQ-001,033,034 | CLI/runtime entry points |
| E4-UNK-024..029 | ADR-009,012 | INV-013,014 | REQ-027,035 | external compatibility gate |

## 26. Implementation Area Impact

| Area | Requirements | Expected Change Type |
|---|---|---|
| Product execution domain/application | REQ-003..010 | unified lifecycle contract and adapters |
| Product persistence/schema | REQ-004,011,013,015,017,018 | target aggregate/result/artifact schema design |
| Product repositories/UoW | REQ-006,012 | common claim and transaction abstraction |
| Worker runner | REQ-006,010,012,014 | canonical claim/dispatch/terminal boundary |
| Family workflow adapters | REQ-004,011,014,020 | adapt existing workflows without new lifecycle owners |
| Result/Artifact services | REQ-015..020 | ownership/cardinality/reference contract |
| Lineage/closure/export | REQ-021..025 | authority split and projection/source labeling |
| Packaging/deployment | REQ-001,002,026 | retain Product-only runtime surface |
| Shared scientific modules | REQ-026 | preserve; no algorithm rewrite |
| Legacy source/migrations | REQ-027..032 | bounded retirement/archive decision, not immediate deletion |
| CLI interfaces | REQ-033..035 | utility/user-visible boundary and compatibility contracts |
| Tests | all contract requirements | architecture, state, lineage, migration, compatibility verification |

## 27. Rejected Alternatives

### Alternative A — Keep both Product Execution lifecycles

- Why considered: lowest immediate code change.
- Why not recommended: leaves two authoritative claim/state/retry/result/lineage owners and directly fails ENH-E4’s dual-execution objective.
- Evidence: Phase 02; current Causal/Family matrices.

### Alternative B — Make Causal table/model canonical

- Why considered: mature domain/repository/UoW and direct causal reuse.
- Why not recommended: family stage semantics, artifact-only outputs, and workflow-specific state would be forced into a model without those native boundaries.
- Evidence: Phase 03 E4-OBS-034..035.

### Alternative C — Make Family table/model canonical

- Why considered: persistent stages and family workflow coverage.
- Why not recommended: Causal Result/input/graph relationships and repository abstractions differ; simply promoting family rows would preserve semantic ambiguity.
- Evidence: Phase 03 and Phase 04.

### Alternative D — Derived-only lineage

- Why considered: typed relations are reconstructable for structural Product relations.
- Why not recommended: generic-only Predictive stage/artifact/model-card/user-authored relations are not fully reconstructable.
- Evidence: Phase 04 E4-INF-022.

### Alternative E — Generic persisted lineage authoritative for all relations

- Why considered: common graph representation.
- Why not recommended: current Causal normal processing does not write generic edges, and typed FK integrity would be demoted without a complete writer/reconciliation contract.
- Evidence: Phase 04 E4-OBS-048, E4-OBS-057.

### Alternative F — Immediate deletion of all legacy source

- Why considered: no Product inbound import and Product-only clean rebuild.
- Why not recommended: external consumers and shared-scientific usage are not fully known; shared capability must be preserved.
- Evidence: Phase 05 E4-UNK-024..029.

## 28. Remaining Unknowns

| ID | Impact on Target Architecture | Blocking? | Handling |
|---|---|---|---|
| E4-UNK-009 | causal retry result/output retention | implementation semantics | yes for retry implementation; define before coding |
| E4-UNK-012 | family Artifact reuse | downstream contract completeness | no core target block; inventory before adapter implementation |
| E4-UNK-014 | production object backend/GC | artifact operations | no core aggregate block; define store contract/reconciliation |
| E4-UNK-015 | legacy cleanup | archive/removal safety | yes for source deletion; external/retention review |
| E4-UNK-016..022 | external lineage/collision/export details | lineage transition/compatibility | no core authority block; explicit tests/contract review |
| E4-UNK-023 | current legacy namespace executable status | legacy archive approach | no Product target block; source/archive review |
| E4-UNK-024..029 | external legacy/data/compatibility consumers | retirement/data destruction | yes for legacy removal or destructive data policy |
| E4-UNK-005..008 | family schema intent, leases, causal stages, legacy retry | detailed implementation | no target block except corresponding invariant design |

## 29. New Facts

No additional repository fact beyond E4-OBS-001..063 was required for the decision. Database reinitialization evidence was incorporated as existing decision-record evidence; no runtime investigation was performed in Phase 06.

## 30. New Inferences

- E4-INF-033: Candidate C is the only evaluated candidate that removes multiple authoritative Product Execution lifecycles without requiring Causal or Family semantics to be erased.
- E4-INF-034: Persistent StageExecution is the smallest common audit boundary that explains current Family semantics and closes the current Causal stage observability gap.
- E4-INF-035: Explicit hybrid lineage is viable only if typed structural relations and generic-only relations have non-overlapping authority in the final state.
- E4-INF-036: Product-only clean bootstrap is evidence-supported for the current pre-production context but is not a universal historical-data policy.
- E4-INF-037: Legacy retirement can be proposed for repository-managed runtime surfaces while remaining conditional for source/data removal because external consumers are unknown.

## 31. Decision Quality Check

1. Exactly one authoritative persistent Product Execution lifecycle? **NO currently; YES proposed target.** Current duality is the problem; ADR-002 resolves it.
2. More than one authoritative Result ownership model for the same semantic Result? **NO proposed.** ExecutionResult/StageResult are explicit semantic levels under one ownership contract.
3. More than one authoritative Artifact ownership model for the same semantic Artifact? **NO proposed.** One Product metadata owner; physical store is separate infrastructure.
4. Can one semantic Lineage relation have two independent authoritative sources? **NO proposed.** Typed structural versus generic-only authority is disjoint.
5. Active Product runtime depends on retired legacy runtime code? **NO_PATH_CONFIRMED currently and NO proposed.**
6. Proposed bootstrap requires legacy migration chain? **NO.**
7. Shared scientific implementations preserved independently? **YES.**
8. Any dual-read/write final state temporary and bounded? **YES.** Any transition is bounded by exit criteria; final target has one authority.
9. Each decision traceable to evidence? **YES.** Traceability matrix provided.
10. External compatibility assumptions explicit? **YES.** E4-UNK-024..029 and HD-005 are explicit.

## 32. Recommendation

`READY_FOR_HUMAN_APPROVAL` for the architectural direction, with human approval required for the seven decisions in Section 23. Implementation is not authorized by this record. Legacy source/runtime removal and destructive data policy remain conditional on the external-compatibility and retention decisions.

## 33. Completion Status

`COMPLETED_WITH_HUMAN_DECISIONS`.

# 53. Mandatory Decision Quality Requirements

## Q1

**YES proposed.** One canonical persistent Product Execution aggregate is required; current Causal/Family duality is explicitly not the target.

## Q2

**YES.** Canonical Execution owns identity, state, claim, retry/rerun/revise, persistence, and terminal outcome. Scientific workflow execution owns family-specific plan/stage runner behavior behind the aggregate.

## Q3

**YES.** Result semantics are defined as ExecutionResult versus StageResult, independently of current `product_result` and `product_family_result` table names.

## Q4

**YES.** Artifact metadata ownership is one Product contract; physical object storage remains behind `ArtifactStorePort`.

## Q5

**YES.** Each relation is assigned one authority: typed structural relation or generic-only relation.

## Q6

**YES.** Generic `LineageEdge` is an explicit generic-only relation store plus read source for user-authored/non-typed relations; it is not an ambiguous universal authority.

## Q7

**YES.** Current Causal and Family persistent lifecycles are proposed to converge into the canonical aggregate; neither remains an independent final authority.

## Q8

**YES.** Persistent StageExecution is proposed for every canonical Execution, while scientific runner internals remain workflow-specific.

## Q9

**YES.** Retry preserves Execution ID with a new attempt; rerun/revise create new IDs with typed source/base relations.

## Q10

**YES.** Legacy orchestration/persistence/runtime is separated from `ariadne.causal`, `ariadne.preprocessing`, and `ariadne.shared`.

## Q11

**YES.** Current pre-production database decision supports Product-only clean bootstrap with no assumed application-data retention; any changed retention requirement blocks destructive implementation.

## Q12

**YES.** No indefinite dual write/read is proposed; any transition must be bounded, reconciled, and removed from final authority.

# 54. Prohibited Conclusions

This ADR is a proposal for human approval. It does not authorize code/schema/migration/test changes, legacy deletion, data destruction, or Gate execution. It does not claim external consumers are absent.

# 55. Completeness Criteria

C1 Phase 01–05 results read: PASS.  
C2 database reinitialization decision evidence read: PASS.  
C3 current problem statement: PASS.  
C4 candidates compared: PASS.  
C5 canonical Execution proposed: PASS.  
C6 identity/state/mutation semantics: PASS.  
C7 worker claim: PASS.  
C8 StageExecution policy: PASS.  
C9 GenericExecutor responsibility: PASS.  
C10 Result ownership: PASS.  
C11 Artifact ownership: PASS.  
C12 downstream reuse: PASS.  
C13 lineage authority: PASS.  
C14 generic-only lineage: PASS.  
C15 legacy policy: PASS.  
C16 shared scientific separation: PASS.  
C17 external boundary: PASS.  
C18 migration/data policy: PASS.  
C19 CLI policy: PASS.  
C20 compatibility terminology: PASS.  
C21 ADR/invariants/requirements: PASS.  
C22 traceability matrix: PASS.  
C23 rejected alternatives: PASS.  
C24 risks: PASS.  
C25 human decisions: PASS.  
C26 no code changes: PASS.  
C27 no Gate decomposition: PASS.

# 56. Final Self-Check

Performed after result generation:

```text
git status --short
git diff --stat
git diff -- docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/40_operator_prompts/architecture_review/06_target_architecture_decision_record_result.md
```

Existing `deploy/.nfs000000000076202f00000088` change was preserved.

