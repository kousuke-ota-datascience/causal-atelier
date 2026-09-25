# ENH-E9 G04 Trial 01 P02 — Package Status

- Gate: G04
- Package: P02
- Trial: 01
- State: PACKAGE_COMPLETE
- Normative contract: `10_enhance_instruction/G04/06_G04_P02_ipw_weight_stats_ess_persistence.md` (FROZEN)
- START_SHA: `48f5f79e9f8310f267266a9ff3f6dbabb7a7d12e`
- PACKAGE_CHECKPOINT_SHA: `654351a77fcbacf5286c117adcf4d41ac2ace349`

## Dependency evidence

`20_implementation_reports/G04/Trial01/packages/ENH-E9-G04_01_P01__status.md` is the exactly-one canonical P01 report and records `State: PACKAGE_COMPLETE`.

## Implemented scope

- Added IPW-only `diagnostics.weighting` persistence in the scientific estimation adapter.
- Summarized P01's authoritative positive observed treated/control analysis weights; the adapter does not reconstruct weights from propensity scores.
- Persisted the required applicability, estimand, exact definition, arm-specific finite ESS, and count/min/mean/p50/p95/p99/max/extreme statistics.
- Reused the frozen P01 `weight > 10.0` authority for `extreme_count`, preserving independence from overlap clipping counts.
- Preserved existing top-level diagnostics, Treatment Effect numerical/uncertainty semantics, overlap behavior, ResultType, and route grammar.

## Changed files

- `src/ariadne/scientific/inference/adapter.py`
- `tests/enhancement/enh_e9/g04/scientific/test_ipw_weighting_persistence.py`

## Focused verification

```text
uv run pytest -q \
  tests/enhancement/enh_e9/g04/scientific/test_ipw_weighting_persistence.py \
  tests/enhancement/enh_e9/g04/scientific/test_weighting_applicability_contract.py \
  tests/integration/test_inference.py \
  tests/scientific/test_product_adapters.py
```

Result: PASS — `25 passed in 9.52s`.

The tests independently construct expected ATE/ATT arm weights, ESS, linear quantiles, and extreme counts; verify DIAGNOSTICS_RESULT and its persisted JSON artifact; and retain existing Treatment Effect numeric and overlap diagnostic regressions.

## Remaining work / blockers

None within P02. AIPW/non-IPW persistence and frontend consumption are outside this P02 scope.
