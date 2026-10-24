# ENH-E11 — Enhance構想承認記録

**Document class:** Planning / Decision Artifact  
**Decision:** PENDING_FULL_CONCEPT_APPROVAL  
**Decision timestamp:** Not yet issued  
**Decision authority:** Human owner (not inferred from draft documents)  
**Reviewed proposal:** `01_enhancement_concept_and_requirement_revision_plan.md`  
**Evidence:** 2026-10-24 owner conversation; [tracking Issue #13](https://github.com/kousuke-ota-datascience/causal-atelier/issues/13)

## Owner direction established for planning (not a Gate approval)

1. ENH-E11 implementation target is **all mandatory 2026-08-04 Phase 1–3
   causal inference capabilities** (with existing implementations reused).
2. Scope of **new** functions: Scientific Core, local CLI execution and
   persistent local file artifacts. New Web UI, Web API, Worker and DB integration
   are deferred to other enhancements.
3. Reconcile current canonical requirements and implementation, the historical
   August blueprint, and the September Notion ENH-E11 handoff before coding.
4. Manage enhancement implementation scope with GitHub Issues **in addition to**
   required workflow documents, with explicit Issue-to-Gate/AC traceability.

## Approval still needed

- Final concept/title and version of the expanded mandatory method list.
- Requirement additions/deletions and treatment of canonical §11 external-engine
  exclusion; new FR/NFR/AR semantics.
- Architecture/ownership of method specifications, optional libraries,
  CLI-file contracts and scientific verification thresholds.
- Gate decomposition, 06/07 contract freeze and fixed baseline SHA.

## Conditions and constraints

- No new Web API, Worker, DB or UI integration for E11 scientific enhancements.
- Do not silently turn exploratory/temporal graphs into identified DAGs.
- Unverifiable scientific results must expose review/warning/negative statuses.
- Preserve FR/NFR/AR existing baseline semantics and independent Gate evidence.
- GitHub Issue completion **does not** equal formal Gate PASS.

## Explicit non-approval

- No implementation agent launch, Gate 06/07 freeze or claim of accepted software.
- No change to canonical requirement documents without reviewed semantic delta.
- No Phase 4 policy automation, monitoring or automated decision authority.

## Required follow-up

1. Review `06_three_source_reconciliation_matrix.md`, `03_requirements_revision.md`
   and `04_design_revision.md` against fixed source SHA and tests.
2. Complete Architecture Review and update `05...traceability_review.md`.
3. Request and record an explicit human full-concept / requirement/design decision
   here, with actual date and decision evidence; do not backdate it.
4. Only after approval, populate approved canonical snapshots and Gate 06/07.
