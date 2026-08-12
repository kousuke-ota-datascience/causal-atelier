# ENH-E5 G01 Trial 02 P02 — Package status

- PROJECT_NAME: Ariadne
- ENHANCE_ID: ENH-E5
- GATE_ID: G01
- PACKAGE_ID: P02
- TRIAL_NO: 02
- Normative Pxx contract: `docs/wiki/develop_memo/_work/20260811_ENH-E5_family_stage_navigation/10_enhance_instruction/G01/06_G01_P02_navigation_shell_ui.md`
- START_SHA: `492e7e9586e7f6ce5f7c8abd9a0099f54a5cadc3`
- Package status: PACKAGE_READY
- PACKAGE_CHECKPOINT_SHA: `d628c2c9454c947a08afedeb7e4e48e811252cca`
- Blocker / remaining work: NONE

## Changed files

- `frontend/index.html`
- `frontend/app.js`
- `src/ariadne/product/application/product_closure_service.py`
- `src/ariadne/interfaces/web_api/routers/product_closure.py`
- `src/ariadne/interfaces/web_api/error_handlers.py`
- `src/ariadne/product/domain/errors.py`
- `tests/product/test_enh_e5_g01_navigation_shell.py`

## Implementation summary

- Added catalog-driven Family tabs and family-local, order-sorted Stage navigation bound to canonical URL navigation state.
- Added a read-only project-scoped operation-availability projection with the closed `RUN` / `EDIT` / `EXPORT` envelope, resource-type support handling, role gating, lifecycle checks, and canonical route/resource validation.
- The frontend displays backend availability results and does not infer scientific eligibility from navigation state.
- Added explicit operation-availability request error codes without schema or migration changes.

## Executed verification

```text
PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/tmp/ariadne-uv-cache uv run python -m compileall -q src
UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run pytest -q tests/product/test_enh_e5_g01_navigation_shell.py tests/product/test_enh_e5_g01_navigation_state.py tests/product/test_enh_e5_g00_navigation.py tests/product/test_predictive_frontend_contract_e3.py
```

Result: `13 passed in 3.54s`; compile succeeded.

```text
git diff --check
```

Result: success.
