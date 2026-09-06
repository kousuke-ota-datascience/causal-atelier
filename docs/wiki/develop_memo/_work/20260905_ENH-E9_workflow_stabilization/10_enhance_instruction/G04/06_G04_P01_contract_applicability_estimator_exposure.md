# G04 P01 — Diagnostics Contract / Applicability / Estimator Exposure

**Status:** `FROZEN`  
**Depends on:** G03 canonical `999_gate_decision = PASS`

## Scope
Define and implement the structured diagnostics applicability boundary required by G04 06: `ESTIMATOR_WEIGHT | PROPENSITY_COMPONENT | NOT_APPLICABLE`; expose scientifically defined estimator/component weight inputs needed by later packages; fix `extreme_rule` semantics and fixture boundaries.

## Protected / forbidden
Preserve Treatment Effect calculation, Result/Execution lineage and existing API route grammar. Do not fabricate weights/ESS, represent AIPW as one final weight, or change Gate semantics/AC.

## Focused verification
Scientific/unit and contract tests for applicability enum/serialization, estimator exposure, extreme-rule boundary and fixture construction. **No Browser E2E.**

## Completion boundary
Non-browser focused tests pass; downstream P02 can consume the stable contract; checkpoint/report produced; no unresolved semantic ambiguity.
