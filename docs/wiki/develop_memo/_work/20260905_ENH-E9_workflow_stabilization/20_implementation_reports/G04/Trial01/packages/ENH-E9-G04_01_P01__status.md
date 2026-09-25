# ENH-E9 G04 Trial 01 P01 — Package Status

- Gate: G04
- Package: P01
- Trial: 01
- State: PACKAGE_COMPLETE
- Normative contract: `10_enhance_instruction/G04/06_G04_P01_contract_applicability_estimator_exposure.md` (FROZEN)
- START_SHA: `00481d7c8691e7bcc2cac8c5a55c1ac31da8e6f1`
- PACKAGE_CHECKPOINT_SHA: `882e8de0583a1fc669c4ae597b78850af34252e7`

## Dependency evidence

`30_test_report/G03/Trial01/ENH-E9-G03_01__999_gate_decision.md` is the exactly-one current canonical G03 decision and records `Status: 999 / PASS` and `PASS — PROMOTION_ALLOWED`.

## Implemented scope

- Added the exact stable `WeightingApplicability` values: `ESTIMATOR_WEIGHT`, `PROPENSITY_COMPONENT`, and `NOT_APPLICABLE`.
- Exposed typed estimator-side `WeightingDiagnosticsInput` with a definition, estimand, and positive observed treated/control components for downstream diagnostics construction.
- Centralized IPW ATE/ATT arm-weight construction so effect calculation and exposed diagnostics input use the same authoritative formula after propensity clipping.
- Applied the frozen `weight > 10.0` extreme-count rule independently of propensity clipping counts.
- Classified OLS/difference-in-means as `NOT_APPLICABLE` without weight or ESS input, and AIPW as a non-final-weight `PROPENSITY_COMPONENT`; cross-fitted AIPW exposure uses the propensity actually used by its score.

## Changed files

- `src/ariadne/causal/inference/estimators/treatment_effect.py`
- `tests/enhancement/enh_e9/g04/scientific/test_weighting_applicability_contract.py`

## Focused verification

```text
uv run pytest -q \
  tests/enhancement/enh_e9/g04/scientific/test_weighting_applicability_contract.py \
  tests/integration/test_inference.py
```

Result: PASS — `13 passed in 4.19s`.

The tests cover all three stable applicability values, IPW ATE/ATT formula and effect-weight identity, positive observed-row exposure, the `10.0` boundary, separation from propensity overlap counting, OLS/difference-in-means null boundary, AIPW non-final component semantics, cross-fitted component identity, and existing Treatment Effect numeric regression.

## Remaining work / blockers

None within P01. Persistence and frontend consumption remain outside this P01 scope.
