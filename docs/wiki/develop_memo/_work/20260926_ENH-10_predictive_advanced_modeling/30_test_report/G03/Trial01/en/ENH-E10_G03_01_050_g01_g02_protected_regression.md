# ENH-E10 G03 Trial 01 — Test Item 050: G01/G02 Protected Regression

| Candidate | Tested SHA | AC | Result |
| --- | --- | --- | --- |
| `64bd2a18dd583349283cd5745edf63d9b28d61ad` | `df278f76ff476143545d73037fe55f96664dae28` | AC-11 | **PASS** |

## Command / raw output

Use the independent command and raw output in item 010: `58 passed, 2 warnings in 15.03s`, exit 0. It executes ENH-E10 G01 contract/unit/integration tests, ENH-E10 G02 contract/integration tests, and baseline predictive training/evaluation/explanation/leakage/API-worker tests.

## Observed facts

- G01 retained model registry, deterministic LightGBM adapter behavior, artifact serialization/load/predict parity, and explicit invalid parameter/model errors.
- G02 retained coefficient, SHAP binary/regression, LIME binary/regression, TRAIN reference provenance, dependency absence, output-scale and Result/Artifact/Model Card contracts.
- no assertion failed; the two warnings are non-failing SHAP provider notifications only.

## Interpretation

The required G01 and G02 protected semantics remain valid under G03 product integration. AC-11 is **PASS**。

## Reproduction / mutation audit / criterion evaluation

```bash
MPLCONFIGDIR=/tmp/ariadne-mpl UV_CACHE_DIR=/tmp/ariadne-uv-cache uv run --extra predictive-advanced pytest -q tests/enhancement/enh_e10/g01 tests/enhancement/enh_e10/g02 tests/product/test_predictive_training_e3.py tests/product/test_predictive_evaluation_e3.py tests/product/test_predictive_explanation_e3.py tests/product/test_predictive_leakage_e3.py tests/product/test_predictive_api_worker_e2e_e3.py
```

Exit code `0`; raw result is `58 passed, 2 warnings in 15.03s` when run with the complete G03 suite. Candidate change is advanced runtime/browser verification scoped, not a G01/G02 implementation mutation; post-candidate diff is documentation-only. Therefore protected G01 model and G02 explanation contracts meet AC-11. **PASS**。
