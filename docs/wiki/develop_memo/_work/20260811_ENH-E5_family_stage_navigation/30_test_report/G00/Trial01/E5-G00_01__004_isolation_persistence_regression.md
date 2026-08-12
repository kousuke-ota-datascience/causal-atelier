# ENH-E5 G00 Trial 01 — Test Item 004: Isolation, persistence, and execution regression

## Purpose

Verify AC-G00-008 through AC-G00-011: no runtime metadata coupling, persistence registration/migration, scientific SchemaRegistry registration, or regression in current execution / CLI / planner boundaries.

## Commands and raw evidence

```text
TEST_TARGET=61e5749387a152a793c1dddaf6fd6cf2c49751aa

$ UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 \\
  uv run pytest -q tests/product/test_enh_e5_g00_navigation.py tests/product/test_architecture.py
..........                                                               [100%]
10 passed in 3.16s

$ git diff --name-status 6e8eb6736a0d72403f5c6ca1a019e8f562d4533c^ \\
  6e8eb6736a0d72403f5c6ca1a019e8f562d4533c
M src/ariadne/interfaces/web_api/app.py
A src/ariadne/interfaces/web_api/routers/navigation.py
A src/ariadne/product/application/navigation_catalog.py
A tests/product/test_enh_e5_g00_navigation.py

$ git diff --name-only 6e8eb6736a0d72403f5c6ca1a019e8f562d4533c^ \\
  6e8eb6736a0d72403f5c6ca1a019e8f562d4533c -- alembic migrations src/ariadne/product/persistence
(no output)

$ UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 \\
  uv run pytest -q tests/product/test_enh_e4_g02_canonical_execution.py \\
  tests/product/test_enh_e4_g07_p03_cli_boundary.py \\
  tests/product/test_enh_e3_causal_workflow_regression.py
................                                                         [100%]
16 passed in 2.24s
```

The navigation static test passed while asserting no execution-plan / stage-execution imports, no product persistence import, and no `analysis-navigation/1` entry in `src/ariadne/product/domain/schemas.py`. Candidate file enumeration and the empty migration/persistence diff establish that this introduction added no migration or persistence registration. The 16 passing pre-existing tests cover canonical execution identity/state/lease behavior, CLI boundary behavior, and causal planner / operation registry behavior without navigation metadata.

## Result

**PASS.** No runtime input/output/status/retry/attempt/lease is exposed by the exact API response; no navigation persistence or migration was added; no scientific generic SchemaRegistry registration exists; execution, CLI, and planner regression evidence passed.
