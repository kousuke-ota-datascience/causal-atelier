# G04 P04 — Frontend Structured Diagnostics Consumption

**Status:** `FROZEN`  
**Depends on:** P03 `PACKAGE_COMPLETE`

## Scope
Make frontend consume persisted structured `balance.before/after` and `weighting` fields directly, including not-applicable/unavailable rendering and any required legacy compatibility projection.

## Protected / forbidden
Frontend must not recompute ESS, weights or weighted balance and must not infer scientific semantics from strings. Preserve Effects/Diagnostics Stage ownership, Result/Execution lineage and existing route grammar.

## Focused verification
Frontend unit/integration and backend-contract compatibility regression proving direct structured consumption and absence of string parsing/recomputation. **No Browser E2E.**

## Completion boundary
Focused non-browser tests pass; all G04 required packages are complete; checkpoint/report produced and Candidate Assembly may begin.
