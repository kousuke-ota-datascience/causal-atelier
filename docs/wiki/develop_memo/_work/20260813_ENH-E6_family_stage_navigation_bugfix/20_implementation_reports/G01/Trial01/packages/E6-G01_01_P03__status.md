# ENH-E6 G01 Trial01 P03 Package Status

- PROJECT_NAME: Ariadne
- ENHANCE_ID: ENH-E6
- GATE_ID: G01
- PACKAGE_ID: P03
- TRIAL_NO: 01
- Normative Pxx contract: `docs/wiki/develop_memo/_work/20260813_ENH-E6_family_stage_navigation_bugfix/10_enhance_instruction/G01/06_G01_P03_browser_regression_and_test_strengthening.md`
- START_SHA: `2241a7aa43f1921009f1e6340017c1dc383545cb`
- Package status: `PACKAGE_READY`
- PACKAGE_CHECKPOINT_SHA: `575cdd139aea09d4f19b46ab6a6d38545f645c71`

## Changed files

- `tests/browser_e2e/run_enh_e6_family_stage_navigation.py`
- `tests/product/test_enh_e6_g01_p03_browser_runner.py`
- `Dockerfile.browser-e2e`
- `.dockerignore`

## Implementation summary

- Added an additive Playwright/Chromium runner that creates a deterministic Project and drives the actual analytical left-nav, Family tabs, and Stage sidebar.
- Implemented B01 normal entry/family switching, B02 Causal Discovery/Inference boundary, and B03 Back/Forward/reload restore checks against canonical routes and visible selected controls.
- Added failure snapshots (URL, Family/Stage outerHTML and state, active presentation/workspace, console), screenshot, video, trace, and JSON evidence.
- Added the runner to the browser image and explicitly unignored it from Docker build context.

## Focused verification

Static command:

```bash
.venv/bin/python -m py_compile tests/browser_e2e/run_enh_e6_family_stage_navigation.py
.venv/bin/pytest -q tests/product/test_enh_e6_g01_p03_browser_runner.py tests/product/test_enh_e6_g01_p02_stage_presentation.py tests/product/test_enh_e6_g01_p01_navigation_transition.py tests/product/test_enh_e5_g01_navigation_state.py tests/product/test_enh_e5_g01_navigation_shell.py tests/product/test_enh_e5_g03_p01_causal_stage_mapping.py
git check-ignore -v --non-matching tests/browser_e2e/run_enh_e6_family_stage_navigation.py
git diff --check
```

Result: `13 passed in 3.95s`; `git check-ignore` returned non-matching (`::`), proving the runner is not excluded.

Canonical browser command:

```bash
docker compose -f compose.yaml -f compose.e1a.yaml -p ariadne-e1a --profile e2e run --build --rm --entrypoint python browser-e2e tests/browser_e2e/run_enh_e6_family_stage_navigation.py
```

Result: passed. Browser: `Chromium 151.0.7922.34`. B01, B02, and B03 are `PASS` in `test-results/browser_e2e/enh-e6-family-stage-navigation-evidence.json`; screenshot and trace are stored beside it.

## Blocker / remaining work

None for P03. This package provides self-check evidence only and is not a G01 PASS decision.
