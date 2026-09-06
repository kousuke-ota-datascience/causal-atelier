# ENH-E9 G04 Trial 01 P03 — Package Status

- Gate: G04
- Package: P03
- Trial: 01
- State: PACKAGE_COMPLETE
- Normative contract: `10_enhance_instruction/G04/06_G04_P03_balance_applicability.md` (FROZEN)
- START_SHA: `7870a1e0fc4bed30dc2ce3a193443a0660ad0f89`
- PACKAGE_CHECKPOINT_SHA: `aa6577a81cd3be5ceba4bbf5713c3d822d08d7e0`

## Dependency evidence

`20_implementation_reports/G04/Trial01/packages/ENH-E9-G04_01_P02__status.md` is the exactly-one canonical P02 report and records `State: PACKAGE_COMPLETE`.

## Implemented scope

- Replaced the legacy single `balance` row list with the structured contract: unweighted `before`, weighted-or-null `after`, and `after_applicability`.
- Added a balance-only row-aligned projection of IPW's actual arm-specific analysis weights. It is explicitly not a combined/final estimator weight and is used only by the existing weighted balance function.
- Persisted IPW ATE/ATT `after` balance using actual clipped-propensity arm weights.
- Persisted `after = null` for AIPW, OLS, and difference-in-means; AIPW retains `PROPENSITY_COMPONENT`, while OLS/difference-in-means retain `NOT_APPLICABLE`.
- Added non-IPW weighting companion payloads containing classification only and null weight/ESS fields, avoiding fabricated diagnostics.

## Changed files

- `src/ariadne/causal/inference/estimators/treatment_effect.py`
- `src/ariadne/scientific/inference/adapter.py`
- `tests/enhancement/enh_e9/g04/scientific/test_balance_applicability.py`

## Focused verification

```text
uv run pytest -q \
  tests/enhancement/enh_e9/g04/scientific/test_balance_applicability.py \
  tests/enhancement/enh_e9/g04/scientific/test_ipw_weighting_persistence.py \
  tests/enhancement/enh_e9/g04/scientific/test_weighting_applicability_contract.py \
  tests/integration/test_inference.py \
  tests/scientific/test_product_adapters.py
```

Result: PASS — `30 passed in 8.70s`.

The tests independently compute unweighted before balance and ATE/ATT actual-weight after balance, prove before is not copied into after, verify AIPW/OLS/difference-in-means applicability/null boundaries, reject invalid JSON numeric values, and retain IPW persistence, Treatment Effect numeric, and overlap regressions.

## Remaining work / blockers

None within P03. Frontend structured consumption remains outside this P03 scope.
