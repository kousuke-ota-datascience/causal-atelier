# E5-G02 Trial 01 — Test Item 003: Subgroup Evaluation Contract

## Verification purpose

Verify AC-G02-007: TEST-only independent subgroup evaluation, non-feature subgroup retention, null-group handling, metric behavior, deterministic percentile bootstrap, and record-list serialization.

## Command / input

```bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run pytest -q \
  tests/product/test_enh_e5_g02_p02_subgroup_evaluation.py
```

## Raw evidence

```text
.....                                                                    [100%]
5 passed
```

The test executes `PredictivePrepareRunner` with a non-feature subgroup column and verifies retained TEST row ordinals. It evaluates independent TEST slices twice and obtains identical records. Each record has `subgroup_value`, `is_null_group`, `metric`, `sample_count`, `value`, `uncertainty`, `status`, and `warnings`; null values are explicit null groups. It also verifies 1,000 requested bootstrap resamples, non-computable metric behavior, `n < 2` uncertainty suppression, and the `valid_resamples < 200` warning path.

## Result

`PASS`

## Decision rationale

The execution evidence covers the Gate 07 scientific and serialization invariants without manufacturing a numeric result for non-computable slices.
