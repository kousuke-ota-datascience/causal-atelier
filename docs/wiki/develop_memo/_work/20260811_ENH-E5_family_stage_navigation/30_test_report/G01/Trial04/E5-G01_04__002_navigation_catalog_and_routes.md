# E5-G01 Trial 04 — Test Item 002: Navigation Catalog and Routes

## Verification purpose

Verify AC-G01-001 through AC-G01-006: canonical catalog, URL-driven navigation state, route handling, shell behavior, and absence of runtime/persistence ownership.

## Command / input

```bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run pytest -q \
  tests/product/test_enh_e5_g00_navigation.py \
  tests/product/test_enh_e5_g01_navigation_state.py \
  tests/product/test_enh_e5_g01_navigation_shell.py \
  tests/product/test_enh_e5_g01_history_accessibility.py \
  tests/product/test_enh_e5_g01_trial04_route_validation.py \
  tests/product/test_predictive_frontend_contract_e3.py
```

## Raw evidence

```text
....................                                                     [100%]
20 passed in 12.77s
```

The assertions cover the exact metadata catalog; invalid catalog rejection; no runtime execution/persistence ownership; canonical route parse/serialize; unknown family, stage, and resource-type rejection; legacy normalization; generic resource deep link to a family default Stage; explicit Family mismatch rejection; and catalog-driven deterministic shell ordering.

## Result

`PASS`

## Decision rationale

All automated assertions passed against the audited semantic candidate state.
