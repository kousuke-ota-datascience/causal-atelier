# G02 Trial 01 — 090 g01_protected_regression

AC-12. Command:

```text
UV_CACHE_DIR=/tmp/ariadne-uv-cache uv run --extra predictive-advanced pytest -q \
 tests/product/test_enh_e10_g01_p01_model_capability.py \
 tests/product/test_enh_e10_g01_p02_lightgbm_adapters.py \
 tests/product/test_enh_e10_g01_p03_model_artifacts.py \
 tests/product/test_predictive_training_e3.py tests/product/test_predictive_leakage_e3.py
...........................  [100%]
27 passed in 14.42s
exit code: 0
```

Target/candidate identities are as in item 001. Result: **PASS**.
