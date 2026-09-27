# G01 Trial 01 — 060 leakage_and_test_isolation

## Scope

AC-08: TRAIN-only preprocessing and TEST final-evaluation isolation remain intact.

## Method / raw evidence

```text
UV_CACHE_DIR=/tmp/ariadne-uv-cache uv run --extra predictive-advanced pytest -q \
  tests/product/test_predictive_training_e3.py \
  tests/product/test_predictive_leakage_e3.py \
  tests/product/test_predictive_evaluation_e3.py \
  tests/product/test_predictive_explanation_e3.py
.............                                                            [100%]
13 passed in 4.16s
exit code: 0
```

The training/isolation assertions cover `fit_partition == TRAIN`, no `test` training input, selection partitions `[TRAIN, VALIDATION]`, `selection_allowed == False` for evaluation data, and `final_evaluation_only == True`. Leakage tests also verify target/future/derivative/group/split-overlap rejections.

Target HEAD: `77f4c74601a4fd518f307542ae10730e1f8eb903`; fixed candidate: `936aebc9ac773cd9621ec8bf9b34fcc1b7f6324c`.

## Result

**PASS.**
