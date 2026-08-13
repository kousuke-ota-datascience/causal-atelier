# E5-G02 Trial 01 — Test Item 002: Compatibility, Runtime, and Navigation

## Verification purpose

Verify AC-G02-001 through AC-G02-005: Predictive control/payload compatibility, unchanged full runtime plan, six family-local Navigation Stages, Train/runtime separation, and absence of a required general-purpose scoring subsystem.

## Command / input

```bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run pytest -q \
  tests/product/test_enh_e5_g02_p01_predictive_compatibility.py \
  tests/product/test_enh_e5_g02_p03_predictive_read_surfaces.py
```

## Raw evidence

```text
.....                                                                    [100%]
5 passed in 2.45s
```

The assertions establish zero unmapped listed Predictive controls; the exact ten `predictive-analysis-spec/1` top-level fields; deterministic payload/hash output; the unchanged `split -> prepare -> train -> evaluate` runtime plan; and the six canonical routes `setup/train/predict/metrics/explainability/model-management`. The navigation catalog is verified independently of `ExecutionPlan` and `StageExecution` ownership.

## Result

`PASS`

## Decision rationale

The observed payload and plan checks preserve the existing Predictive semantic boundary. The client-side stage-route contract has all six required Stage names while the runtime remains the full predictive plan rather than a `predictive.train.v1` identity or a serving subsystem.
