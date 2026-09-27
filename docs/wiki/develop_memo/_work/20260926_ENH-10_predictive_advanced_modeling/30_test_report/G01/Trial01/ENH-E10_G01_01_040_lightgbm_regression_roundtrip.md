# G01 Trial 01 — 040 lightgbm_regression_roundtrip

## Scope

AC-05, AC-07, AC-09: deterministic regression training, v2 artifact round-trip, retained identity, and prediction parity.

## Method / raw evidence

The independent adapter/artifact command and its raw result are recorded in item 030: `15 passed in 8.36s`, exit code 0.

The direct regression fixture probe observed `lightgbm_regressor.v1`, `schema=fitted-model/2`, `payload_format=lightgbm-model-string/1`, feature order `[x, group]`, the 64-character preprocessor hash, and `parity=true` after fresh load. Artifact SHA-256: `b98ea0f06b944e4fb979da617b8571e5a78796809e3a711c37ac250b77b3d6f4`. Provenance/runtime recorded `objective=regression`, CPU deterministic settings (`deterministic=true`, `force_col_wise=true`, `num_threads=1`), seed `719`, and LightGBM `4.7.0`.

Target HEAD: `77f4c74601a4fd518f307542ae10730e1f8eb903`; fixed candidate: `936aebc9ac773cd9621ec8bf9b34fcc1b7f6324c`.

## Result

**PASS.**
