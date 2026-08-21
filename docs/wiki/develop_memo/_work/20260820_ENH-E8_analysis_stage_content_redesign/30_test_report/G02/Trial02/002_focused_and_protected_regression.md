# G02 Trial02 — Focused and Protected Regression

- Gate: `G02`
- Trial: `02`
- Test Item ID: `002`
- Fixed Trial Candidate SHA: `7e1bbab9f4509a7ef139b0660bc7d8976ab84f4a`
- Result: `PASS`

## Acceptance Criteria

Static/contract/state portions of `G02-AC01`–`G02-AC21`, including Causal/Predictive surface ownership, feature selector behavior/serialization, protected Causal selector behavior, parent navigation, and architecture/diff protections. Browser journeys are assessed in Test Item `003`.

## Method / command

```bash
uv run pytest -q \
  tests/product/test_enh_e8_g02_p02_causal_stage_surface_separation.py \
  tests/product/test_enh_e8_g02_p03_predictive_stage_feature_selector.py \
  tests/product/test_enh_e7_g02_p03_causal_stage_surface_migration.py \
  tests/product/test_enh_e7_g02_p05_predictive_stage_surface_migration.py \
  tests/product/test_enh_e7_g01_p07_project_integration_regression.py \
  tests/product/test_enh_e7_g03_p06_surface_architecture_integration.py \
  tests/product/test_enh_e7_g04_p04_cross_surface_history_navigation.py
node --check frontend/app.js
node --check frontend/analysis_stage_presentation.js
node --check frontend/causal_stage_presentation.js
python3 -m py_compile \
  tests/browser_e2e/run_enh_e8_g02_causal_stage_content.py \
  tests/browser_e2e/run_enh_e8_g02_predictive_stage_content.py
git diff --check a2399662f4f81ceadf36ae2aa71850d49786cae4 \
  7e1bbab9f4509a7ef139b0660bc7d8976ab84f4a
```

## Evidence

- All seven test modules passed: `19 passed in 0.52s`.
- JavaScript syntax checks and both Browser E2E runner Python compile checks passed.
- `git diff --check` passed.
- Trial02 remediation delta is `.dockerignore`, `Dockerfile.browser-e2e`, its remediation instruction, and workflow evidence. The product implementation, runner semantics, API/backend/runtime, and frozen Gate contracts are unchanged.
- The exact candidate's Dockerfile and `.dockerignore` now include both required G02 browser runner paths.

## 判定理由

All deterministic focused/protected checks passed. They cannot replace the frozen Browser E2E cross-layer journeys, which remain blocked as documented in Test Item `003`.
