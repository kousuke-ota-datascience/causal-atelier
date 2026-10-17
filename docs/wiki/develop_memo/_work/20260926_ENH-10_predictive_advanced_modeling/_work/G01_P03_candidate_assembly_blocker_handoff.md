# ENH-E10 G01 P03 — Candidate Assembly Blocker Handoff

## Status

`BLOCKED_INTEGRATION_VERIFICATION`

Candidate Assembly was run for `GATE_ID=G01`, `TRIAL_NO=01`.

| Item | Value |
| --- | --- |
| Candidate SHA under audit | `0dc58489448e2f3d293c4be80386791c887df755` |
| P01 checkpoint | `488ba81d5d8d6177f0f0ac80b9dc43364fc32a06` |
| P02 checkpoint | `e6037709d955ed21027bc591ad815ebabc507ba7` |
| P03 checkpoint | `0dc58489448e2f3d293c4be80386791c887df755` |
| Package-chain audit | PASS — ordered ancestry verified |
| Working tree at block | clean |

## Reproduction

```bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache uv run --extra predictive-advanced pytest -q \
  tests/product/test_enh_e10_g01_p01_model_capability.py \
  tests/product/test_enh_e10_g01_p02_lightgbm_adapters.py \
  tests/product/test_enh_e10_g01_p03_model_artifacts.py \
  tests/product/test_predictive_training_e3.py \
  tests/product/test_predictive_evaluation_e3.py \
  tests/product/test_predictive_explanation_e3.py
```

Observed result: `29 passed, 2 failed`.

Failing tests:

- `test_lightgbm_binary_fit_predict_is_deterministic_and_returns_probability`
- `test_lightgbm_regression_fit_predict_is_deterministic_and_numeric`

## Established cause

P03 changed `predict()` to call `load_model_artifact()`. The loader requires durable model identity fields `preprocessor_hash` and `feature_order`. Direct P02 calls to `fit_model()` return an in-memory `fitted-model/1` dictionary before `PredictiveTrainRunner` adds these fields, so the subsequent direct `predict()` call fails with `MODEL_ARTIFACT_LOAD_FAILED`.

The observed failure is deterministic and occurs in `src/ariadne/capabilities/predictive/modeling.py` at `load_model_artifact()` required-field validation.

## Required remediation boundary

This is P03 artifact/load integration work. Do not change Candidate Assembly, package reports, acceptance criteria, or weaken tests.

The remediation must make the loader/predict boundary distinguish an in-memory model returned by `fit_model()` from a durable artifact requiring feature/preprocessor identity, while preserving:

- durable `fitted-model/2` identity validation;
- `fitted-model/1` read compatibility;
- `MODEL_FEATURE_MISMATCH` and `PREPROCESSOR_MODEL_MISMATCH` behavior for persisted artifacts;
- no silent fallback and optional LightGBM behavior;
- existing TRAIN-only preprocessing and TEST isolation.

## Completion condition

Re-run the reproduction command above. Candidate Assembly may resume only after all tests pass and the remediation is checkpointed/reported under the formal remediation workflow.
