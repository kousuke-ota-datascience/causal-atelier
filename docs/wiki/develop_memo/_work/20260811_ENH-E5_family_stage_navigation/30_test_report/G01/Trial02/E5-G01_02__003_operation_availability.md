# E5-G01 Trial 02 — Test Item 003: Operation Availability Contract

## Verification purpose

Verify AC-G01-007, specifically that the endpoint accepts only canonical browser routes and returns `INVALID_NAVIGATION_ROUTE` for malformed or unknown canonical routes.

## Command / input

```bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run python -
```

The command instantiated `ProductClosureService` with an OWNER session double and called:

```text
project_id=p1
resource_type=None
resource_id=None
route=/projects/p1/analysis/causal/unknown-stage
```

## Raw evidence

```text
{'operations': {'RUN': {'allowed': False, 'reason_code': 'RESOURCE_REQUIRED'}, 'EDIT': {'allowed': False, 'reason_code': 'RESOURCE_REQUIRED'}, 'EXPORT': {'allowed': False, 'reason_code': 'RESOURCE_REQUIRED'}}}
OBSERVED: unknown stage was accepted; expected OperationAvailabilityError(INVALID_NAVIGATION_ROUTE) per G01 07.
```

The endpoint's route validator uses a regex whose stage segment is `([^/]+)`, so `unknown-stage` passes validation. Gate 07 instead requires an unknown Stage to produce a deterministic not-found/unsupported error and defines malformed/unknown canonical routes as HTTP 422 / `INVALID_NAVIGATION_ROUTE`.

## Result

`FAIL`

## Decision rationale

This is a direct contradiction of Gate 07's Canonical Route Contract and its Operation Availability unknown-route semantics. The result is an implementation defect, not a test-environment blocker.
