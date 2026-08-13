# ENH-E5 G01 Trial 01 P01 — Package status

- PROJECT_NAME: Ariadne
- ENHANCE_ID: ENH-E5
- GATE_ID: G01
- PACKAGE_ID: P01
- TRIAL_NO: 01
- Normative Pxx contract: `docs/wiki/develop_memo/_work/20260811_ENH-E5_family_stage_navigation/10_enhance_instruction/G01/06_G01_P01_route_and_navigation_state.md`
- START_SHA: `e80364492070c5aa90abcf452e086ae9b3a3b175`
- Package status: PACKAGE_READY
- PACKAGE_CHECKPOINT_SHA: `0ce00c547efea4bb20dd4c466f00eed857e7c12e`
- Blocker / remaining work: NONE

## Changed files

- `frontend/navigation_state.js`
- `frontend/app.js`
- `frontend/index.html`
- `tests/product/test_enh_e5_g01_navigation_state.py`

## Implementation summary

- Added URL-authoritative analysis NavigationContext parsing and serialization for canonical Stage and resource deep routes.
- Validates family, family-local Stage, and allowed resource type with deterministic navigation errors.
- Derives a generic resource link's family and routes it to the catalog default Stage; an explicit route/resource family mismatch raises an explicit error.
- Normalizes retained project-scoped legacy analysis routes one-way to the specified canonical routes.
- Restores canonical contexts on browser navigation without persisting navigation state to domain resources or schema.

## Executed verification

```text
UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run pytest -q tests/product/test_enh_e5_g01_navigation_state.py tests/product/test_enh_e5_g00_navigation.py tests/product/test_predictive_frontend_contract_e3.py
```

Result: `11 passed in 2.22s`.

```text
git diff --check
```

Result: success (no whitespace errors).
