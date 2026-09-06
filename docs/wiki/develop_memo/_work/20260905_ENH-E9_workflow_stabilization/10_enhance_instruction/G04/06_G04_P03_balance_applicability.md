# G04 P03 — Before/After Balance and Estimator Applicability

**Status:** `FROZEN`  
**Depends on:** P02 `PACKAGE_COMPLETE`

## Scope
Implement `balance.before/after` and `after_applicability`; wire scientifically defined weighted/component balance; encode AIPW as `PROPENSITY_COMPONENT` and OLS/difference-in-means as `NOT_APPLICABLE` without fabricated after-balance/weight/ESS.

## Protected / forbidden
`balance.before` remains unweighted; never copy before into after; do not force IPW diagnostics onto AIPW/non-weighted estimators; preserve Result/Execution lineage and treatment-effect semantics.

## Focused verification
Weighted-balance fixture tests, AIPW applicability tests, non-weighted NOT_APPLICABLE tests, backend payload/persistence regression. **No Browser E2E.**

## Completion boundary
All applicability/balance non-browser tests pass and persisted semantics satisfy G04 06/07; checkpoint/report produced.
