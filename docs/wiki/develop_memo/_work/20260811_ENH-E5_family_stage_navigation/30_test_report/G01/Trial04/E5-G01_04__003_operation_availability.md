# E5-G01 Trial 04 — Test Item 003: Operation Availability Contract

## Verification purpose

Verify AC-G01-007 and the Trial 03 remediation: malformed or unknown canonical routes must fail before an availability projection is returned.

## Command / input

```bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run pytest -q \
  tests/product/test_enh_e5_g01_trial04_route_validation.py
```

## Raw evidence

```text
......                                                                   [100%]
6 passed
```

The independent test invokes `ProductClosureService.operation_availability` with an OWNER Project membership. It verifies a valid canonical route produces the `RESOURCE_REQUIRED` projection and that each of these fails with `OperationAvailabilityError(code="INVALID_NAVIGATION_ROUTE", status=422)` before projection:

- unknown Stage: `/projects/p1/analysis/causal/unknown-stage`
- unknown Family: `/projects/p1/analysis/unknown/setup`
- malformed route: `/projects/p1/analysis/causal`
- unknown deep-route resource type: `/projects/p1/analysis/causal/setup/resource/unknown/id1`
- route project mismatch: `/projects/p2/analysis/causal/setup`

The implementation resolves the route Family and family-local Stage from the canonical navigation catalog; it does not rely on a structural regex alone.

## Result

`PASS`

## Decision rationale

The observed error code/status and ordering satisfy Gate 07's unknown-route and query semantics. The previously observed unknown-stage acceptance is no longer reproducible.
