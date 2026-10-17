# G01 Trial 01 — 030 lightgbm_binary_roundtrip

## Scope

AC-04, AC-07, AC-09: deterministic binary training, v2 artifact serialization, fresh load, identity retention, and prediction parity.

## Method / raw evidence

```text
UV_CACHE_DIR=/tmp/ariadne-uv-cache uv run --extra predictive-advanced pytest -q \
  tests/product/test_enh_e10_g01_p02_lightgbm_adapters.py \
  tests/product/test_enh_e10_g01_p03_model_artifacts.py
...............                                                          [100%]
15 passed in 8.36s
exit code: 0
```

Direct deterministic fixture probe additionally observed for `lightgbm_classifier.v1`: `schema=fitted-model/2`; `payload_format=lightgbm-model-string/1`; `feature_order=[x, group]`; 64-character preprocessor hash; `parity=true` after `load_model_artifact`; artifact SHA-256 `6690bd3352e51025289db2e218cd1f3482fa4153cafa7624f563251c4da902be`. Runtime/provenance recorded CPU, `deterministic=true`, `force_col_wise=true`, `num_threads=1`, seed `719`, task objective `binary`, and LightGBM `4.7.0`.

Target HEAD: `77f4c74601a4fd518f307542ae10730e1f8eb903`; fixed candidate: `936aebc9ac773cd9621ec8bf9b34fcc1b7f6324c`.

## Result

**PASS.**
