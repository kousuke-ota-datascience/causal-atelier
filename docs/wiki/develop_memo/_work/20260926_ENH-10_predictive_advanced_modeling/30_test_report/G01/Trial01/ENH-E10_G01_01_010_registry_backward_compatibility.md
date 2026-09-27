# G01 Trial 01 — 010 registry_backward_compatibility

## Scope

AC-01 and AC-02: existing linear models remain usable; task/model registry compatibility and explicit rejection are preserved.

## Method / raw evidence

Test target: `77f4c74601a4fd518f307542ae10730e1f8eb903` (identity audit 001 establishes semantic equivalence to fixed candidate `936aebc9ac773cd9621ec8bf9b34fcc1b7f6324c`).

```text
UV_CACHE_DIR=/tmp/ariadne-uv-cache uv run --extra predictive-advanced pytest -q tests/product/test_enh_e10_g01_p01_model_capability.py
.......                                                                  [100%]
7 passed in 2.06s
exit code: 0
```

The executed contract tests cover default logistic/linear selections, their capability descriptors, unknown-model rejection (`MODEL_NOT_REGISTERED`), incompatible model/task rejection (`MODEL_TASK_MISMATCH`), and invalid-parameter rejection (`MODEL_PARAMETER_INVALID`).

## Result

**PASS.** The observed assertions satisfy AC-01/AC-02 for the registry and task matrix.
