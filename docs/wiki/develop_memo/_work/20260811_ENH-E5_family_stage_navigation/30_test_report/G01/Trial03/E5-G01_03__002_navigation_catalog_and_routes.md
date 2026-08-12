# E5-G01 Trial 03 — Test Item 002: Navigation Catalog and Routes

## Verification purpose

Verify AC-G01-001 through AC-G01-006: canonical catalog, URL-driven navigation state, route handling, shell behavior, and absence of runtime/persistence ownership.

## Command / input

```bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run pytest -q \
  tests/product/test_enh_e5_g00_navigation.py \
  tests/product/test_enh_e5_g01_navigation_state.py \
  tests/product/test_enh_e5_g01_navigation_shell.py \
  tests/product/test_enh_e5_g01_history_accessibility.py \
  tests/product/test_predictive_frontend_contract_e3.py
```

## Raw evidence

```text
..............                                                           [100%]
14 passed in 4.35s
```

The executed assertions cover the exact analysis-navigation catalog API response; invalid catalog rejection; no `execution_plan`, `stage_execution`, or persistence registration dependency; canonical route parse/serialize; unknown family, stage, and resource-type rejection in navigation state; legacy one-way mapping; generic execution resource links to the resource Family default stage; explicit Family mismatch rejection; catalog-driven family/stage rendering; and deterministic stage sorting.

## Result

`PASS`

## Decision rationale

All automated assertions for the listed ACs passed against the audited semantic candidate state.
