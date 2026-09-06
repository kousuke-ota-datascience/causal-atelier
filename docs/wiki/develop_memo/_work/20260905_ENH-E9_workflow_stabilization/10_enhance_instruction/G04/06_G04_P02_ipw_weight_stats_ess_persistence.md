# G04 P02 — IPW Actual-Weight Statistics / ESS Persistence

**Status:** `FROZEN`  
**Depends on:** P01 `PACKAGE_COMPLETE`

## Scope
Persist IPW ATE/ATT actual arm-specific analysis-weight statistics and treated/control ESS in structured `DIAGNOSTICS_RESULT`, using the G04 06 contract and P01 applicability/extreme-rule definitions.

## Protected / forbidden
Do not alter Treatment Effect values/uncertainty, fabricate combined final weights, reuse propensity clipping counts as extreme-weight counts, or change API route grammar/lineage.

## Focused verification
Known-fixture IPW ATE and ATT tests independently recomputing `(sum w)^2 / sum(w^2)` and count/min/mean/p50/p95/p99/max/extreme_count from expected actual weights; backend persistence/integration checks. **No Browser E2E.**

## Completion boundary
Independent numeric expectations and persistence tests pass; checkpoint/report produced; P03 can consume persisted weighting semantics.
