# G05 P01 — Integrated Regression Acceptance Preparation

**Status:** `FROZEN`  
**Depends on:** G01–G04 canonical `999_gate_decision = PASS`

## Scope
Prepare the integrated repository state for independent G05 verification without changing passed Gate semantics:

- integration-only defect correction within G01–G04 established contracts;
- canonical critical-journey fixture/orchestration/synchronization wiring;
- non-browser protected regression self-check;
- candidate finalization inputs/evidence.

Critical journey: Analysis Context → Discovery → Graph review/comparison → FIXED Graph → Identification → Estimation → Effects → Diagnostics.

## Protected / forbidden
Do not change G01–G04 semantic claims or AC. If a passed Gate semantic change is required, stop and route to that Gate's amendment path. Preserve Result/Execution/Graph lineage and Navigation Stage/runtime separation.

## Focused verification
Run static/syntax and relevant non-browser integration/regression/self-checks only. Validate fixture/orchestration readiness without executing the Browser E2E journey.

**Do not run Browser E2E in this Package.** The canonical Browser E2E is reserved for the final item of Independent Verification after all non-browser blocking verification has completed and been evaluated.

## Completion boundary
Non-browser self-checks pass, browser fixture/environment prerequisites are ready, candidate-affecting working tree is clean, and package checkpoint/report are produced. Package completion is not G05 PASS.
