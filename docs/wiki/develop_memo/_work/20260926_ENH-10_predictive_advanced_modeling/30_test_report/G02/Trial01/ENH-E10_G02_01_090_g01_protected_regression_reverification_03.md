# G02 Trial 01 — 090 g01_protected_regression (reverification 03)

## Scope / command

AC-12: preserve G01 model registry/artifact/load/predict/provenance and baseline predictive flow. The following protected command was executed separately from SHAP/LIME tests to avoid provider import-order effects:

```text
MPLCONFIGDIR=/tmp/ariadne-mpl UV_CACHE_DIR=/tmp/ariadne-uv-cache \
uv run --extra predictive-advanced pytest -q tests/product/test_predictive_training_e3.py
```

## Raw failure evidence

```text
tests/product/test_predictive_training_e3.py::test_full_predictive_dag_is_deterministic_and_keeps_test_out_of_training FAILED
tests/product/test_predictive_training_e3.py::test_regression_uses_only_registered_deterministic_linear_model FAILED
2 failed in 4.64s

outcome_status=FAILED
split=SUCCEEDED
prepare=FAILED error={'type': 'KeyError', 'message': "'sampling'"}
train=SKIPPED_DUE_TO_PREREQUISITE
evaluate=SKIPPED_DUE_TO_PREREQUISITE
```

## Diagnosis / result

Candidate diff inspection locates the failure in `PredictivePrepareRunner`: the remediation unconditionally indexes `explanation_specification["sampling"]`. Existing baseline flows legitimately use an empty `explanation_spec`; their PREPARE stage now fails before model train/evaluate.

Other isolated G01 registry/adapter/artifact/leakage tests passed (`25 passed in 5.39s`), but they do not negate this protected integration regression. This is a verified product defect. Target/candidate identities are in item 001. **Result: FAIL.**
