# ENH-E5 G00 Trial 01 — Test Item 003: Catalog invariants

## Purpose

Verify AC-G00-006 and AC-G00-007: catalog invariants and rejection behavior.

## Command and target

```text
TEST_TARGET=61e5749387a152a793c1dddaf6fd6cf2c49751aa
UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 \\
uv run pytest -q tests/product/test_enh_e5_g00_navigation.py tests/product/test_architecture.py
```

## Raw evidence

```text
..........                                                               [100%]
10 passed in 3.16s
```

Collected and passing invariant cases were:

```text
test_catalog_validation_rejects_invalid_catalogs[catalog0]  # duplicate Family
test_catalog_validation_rejects_invalid_catalogs[catalog1]  # blank Family slug
test_catalog_validation_rejects_invalid_catalogs[catalog2]  # invalid default
test_catalog_validation_rejects_invalid_catalogs[catalog3]  # empty stages
test_catalog_validation_rejects_invalid_catalogs[catalog4]  # duplicate Stage ID
```

The same validation function enforces exactly-once Family coverage, global nonblank unique Family slugs, nonempty stages, nonblank unique Family-local stage IDs and slugs, default membership, consecutive deterministic order, and `stage_id == slug`.

Additional independent mutation observation covered rejection cases not separately parameterized by the candidate test:

```text
$ ... uv run python -c '<construct invalid catalogs and call validate_navigation_catalog>'
blank-stage-id: rejected
blank-stage-slug: rejected
duplicate-stage-slug: rejected
non-deterministic-order: rejected
```

## Result

**PASS.** Gate 07's required invariant and rejection conditions are validated; no failing case was observed.
