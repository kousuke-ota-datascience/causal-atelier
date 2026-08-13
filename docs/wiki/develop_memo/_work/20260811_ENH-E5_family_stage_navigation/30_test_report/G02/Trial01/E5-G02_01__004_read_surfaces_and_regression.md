# E5-G02 Trial 01 — Test Item 004: Read Surfaces, Draft Preservation, and Protected Regression

## Verification purpose

Verify AC-G02-006 and AC-G02-008 through AC-G02-010, plus the protected Predictive regressions: saved Result/Artifact reading, no causal explanation claim, no ModelRegistry aggregate, and route-independent unsaved draft state.

## Command / input

```bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run pytest -q \
  tests/product/test_enh_e5_g02_p01_predictive_compatibility.py \
  tests/product/test_enh_e5_g02_p02_subgroup_evaluation.py \
  tests/product/test_enh_e5_g02_p03_predictive_read_surfaces.py \
  tests/product/test_predictive_spec_e3.py \
  tests/product/test_predictive_leakage_e3.py \
  tests/product/test_predictive_training_e3.py \
  tests/product/test_predictive_evaluation_e3.py \
  tests/product/test_predictive_explanation_e3.py \
  tests/product/test_predictive_frontend_contract_e3.py \
  tests/product/test_enh_e5_g00_navigation.py \
  tests/product/test_enh_e5_g01_navigation_state.py
```

## Raw evidence

```text
.......................................                                  [100%]
39 passed in 6.30s
```

The read-surface assertions verify that detail rendering reads `state.predictiveDetails` and does not post to `/executions`; it renders saved `PREDICTIVE_EXPLANATION_RESULT` data and carries the explicit non-causal terminology. They also verify capture/restore of `predictiveDraft`, no `ModelRegistry`, and no navigation persistence/runtime ownership. The broader suite preserves the existing specification, leakage, training, evaluation, explanation, frontend, catalog, and navigation-state contracts.

## Result

`PASS`

## Decision rationale

All protected regressions passed on the candidate-equivalent state. Metrics and Model Management remain read-oriented; no new execution, registry aggregate, or causal-explanation representation was observed.
