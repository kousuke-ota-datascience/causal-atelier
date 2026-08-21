# G02 Trial01 — Focused and Protected Regression

- Gate: `G02`
- Trial: `01`
- Test Item ID: `002`
- Fixed Trial Candidate SHA: `a2399662f4f81ceadf36ae2aa71850d49786cae4`
- Result: `PASS`

## Acceptance Criteria

`G02-AC01`–`G02-AC21` static/contract/state portions, including Causal/Predictive surface ownership, selector serialization/state, protected Causal selector behavior, parent navigation, and no backend/runtime semantics in the candidate diff. Browser-journey portions remain governed by Test Item `003`.

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
git diff --check a99b059f3479d6d9cf92862eb283ebdbc8866952 \
  a2399662f4f81ceadf36ae2aa71850d49786cae4
```

## Evidence

- All seven test modules passed: `19 passed in 0.65s`.
- All three JavaScript syntax checks and both Browser E2E runner Python compile checks passed.
- `git diff --check` passed.
- Candidate executable source changes are limited to frontend presentation files and the G02 product/browser test files; no `src/`, migration, API contract, persistence, worker/runtime implementation, or dependency-lock change is present.

## 判定理由

The focused deterministic tests establish the covered DOM/state/serialization and protected-regression assertions. They do not substitute for frozen Chromium journeys; those are separately required and assessed in Test Item `003`.
