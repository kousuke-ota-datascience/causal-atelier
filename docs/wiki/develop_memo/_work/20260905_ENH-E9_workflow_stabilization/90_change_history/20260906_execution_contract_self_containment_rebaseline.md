# 2026-09-06 — Execution Contract Self-Containment Rebaseline

- Enhancement: `ENH-E9`
- Classification: `NON_SEMANTIC_EXECUTION_CONTRACT_REBASELINE`
- Trigger: Human review requested E7/E8-level implementation-contract sufficiency and whole-enhancement consistency.
- Reference remote HEAD at review start: `a25aaa9e8d6c19a1e82ae2fa8af6493859e448bb`
- Gate claim change: `NONE`
- Acceptance Criteria change: `NONE`
- Requirement/design semantic change: `NONE`

## Findings

1. G03/G05 had been normalized to WORK_PACKAGE execution but root MANIFEST/README still contained stale SINGLE_EXECUTION metadata.
2. G03 P01 was executable but lacked some E7/E8-style self-contained implementation boundaries.
3. G04 P01–P04 contained normative references to Gate 06/07 or another Pxx, which conflicts with the shared Coding Agent rule that assigned Pxx alone is normative.
4. G05 P01 needed tighter integration-only correction and stop boundaries.
5. Browser E2E must remain the final Gate-level connectivity proof, never a Package-level or G04 numeric/scientific primary proof.
6. G02 Trial01 was `READY_FOR_TEST` at review start; no remote canonical G02 `999_gate_decision` existed. Therefore G03 entry was not canonically satisfied.

## Rebaseline rule

- G01 PASS authority is not modified.
- G02 Trial01 candidate contract/provenance is not modified; finish G02 Independent Verification first.
- G03–G05 contracts and shared execution rules are re-baselined for self-containment without changing Gate claims/AC.
- Any G03 Trial01/P01 implementation started before this rebaseline is not eligible as Fixed Trial Candidate evidence. After G02 PASS, restart P01 from the post-rebaseline repository state.

## Why this is not 09 Amendment

09 is reserved for a defect in Gate semantic claim or Acceptance Criteria. This change does not alter what the product must do; it changes how the already-frozen semantics are projected into isolated Coding Agent execution contracts and how workflow state is represented consistently.

If later review requires changing a Gate claim or AC, stop and create a formal 09 Gate Contract Amendment.
