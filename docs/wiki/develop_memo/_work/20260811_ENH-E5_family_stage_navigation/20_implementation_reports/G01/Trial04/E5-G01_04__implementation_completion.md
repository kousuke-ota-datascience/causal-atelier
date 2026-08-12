# ENH-E5 G01 Trial 04 — Remediation Implementation Completion

- PROJECT_NAME: Ariadne
- ENHANCE_ID: ENH-E5
- GATE_ID: G01
- TRIAL_NO: 04
- Execution status: READY_FOR_TEST
- PREVIOUS_FAILED_CANDIDATE_SHA: `27e87faecd2b5dac0da6a688201931456c1a6077`
- FIXED_TRIAL_CANDIDATE_SHA: `1fb9e0f3bd8850782433a2475900fce45d420cd4`
- Blocker / remaining work: NONE

## Changed production files

- `src/ariadne/product/application/product_closure_service.py`

## Changed automated test files

- `tests/product/test_enh_e5_g01_trial04_route_validation.py`

## Remediation summary

- Canonical route validation now resolves Family and family-local Stage membership from `navigation_catalog.CATALOG`; a structural regex alone does not establish validity.
- Unknown/malformed routes, unknown Family/Stage, unknown deep-route resource type, and endpoint/route project mismatch fail with `INVALID_NAVIGATION_ROUTE` before availability projection.
- Added direct `ProductClosureService.operation_availability(...)` regression coverage for the required route cases and error code/status.

## Executed verification

```text
PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/tmp/ariadne-uv-cache uv run python -m compileall -q src
UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run pytest -q tests/product/test_enh_e5_g00_navigation.py tests/product/test_enh_e5_g01_navigation_state.py tests/product/test_enh_e5_g01_navigation_shell.py tests/product/test_enh_e5_g01_history_accessibility.py tests/product/test_enh_e5_g01_trial04_route_validation.py tests/product/test_predictive_frontend_contract_e3.py
git diff --check
git diff --name-only 27e87faecd2b5dac0da6a688201931456c1a6077..1fb9e0f3bd8850782433a2475900fce45d420cd4 -- src frontend tests pyproject.toml uv.lock alembic
```

Result: compile success; `20 passed in 9.91s`; whitespace check success. The semantic diff contains the required `src/` and `tests/` changes.

This completion report is evidence-only; therefore `HEAD != FIXED_TRIAL_CANDIDATE_SHA` is expected after its commit.
