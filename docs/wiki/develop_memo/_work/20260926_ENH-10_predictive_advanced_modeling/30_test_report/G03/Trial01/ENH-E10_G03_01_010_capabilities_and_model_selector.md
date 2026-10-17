# ENH-E10 G03 Trial 01 — Test Item 010: Capabilities and Model Selector

| Candidate | Tested SHA | AC | Result |
| --- | --- | --- | --- |
| `64bd2a18dd583349283cd5745edf63d9b28d61ad` | `df278f76ff476143545d73037fe55f96664dae28` | AC-01, AC-02, AC-08 | **PASS** |

## Method / command

```bash
MPLCONFIGDIR=/tmp/ariadne-mpl UV_CACHE_DIR=/tmp/ariadne-uv-cache \
uv run --extra predictive-advanced pytest -q \
 tests/enhancement/enh_e10/g03/integration/test_predictive_advanced_browser_readiness.py \
 tests/enhancement/enh_e10/g01 tests/enhancement/enh_e10/g02 \
 tests/product/test_predictive_training_e3.py tests/product/test_predictive_evaluation_e3.py \
 tests/product/test_predictive_explanation_e3.py tests/product/test_predictive_leakage_e3.py \
 tests/product/test_predictive_api_worker_e2e_e3.py \
 tests/product/test_enh_e8_g02_p02_causal_stage_surface_separation.py \
 tests/product/test_enh_e8_g02_p03_predictive_stage_feature_selector.py
```

```text
58 passed, 2 warnings in 15.03s
```

Browser scenario 100 additionally selected `lightgbm_classifier.v1`; scenario 110 selected `lightgbm_regressor.v1` through the visible Train selector. Both reached `SUCCEEDED`.

## Facts / interpretation

G01 capability and parameter validation tests protect logistic/linear defaults, LightGBM model task compatibility, deterministic model parameters and explicit error taxonomy. Browser journeys demonstrate that LightGBM options are selected through UI-to-API request construction rather than an inferred backend-only path. The two warnings are SHAP provider binary-array notifications, not selector/request failures. These observations satisfy capability-driven compatible selection, parameter serialization, and advanced-runtime availability for AC-01/02/08. **PASS**。

## Criterion evaluation / source mutation audit / reproduction

AC-01 requires compatible selector options; AC-02 requires capability-contract parameter serialization; AC-08 requires explicit availability behavior. The automated suite exit code is `0`; the browser command in item 100/110 also exits `0`. Candidate mutation is runtime/browser-test scoped and does not alter selector production source after candidate assembly. Reproduce by executing the exact command above, then the frozen browser command in item 100; require `58 passed` and both selected LightGBM journeys `SUCCEEDED`. Result rationale: all three MUST criteria have automated plus runtime evidence, therefore **PASS**。
