# G01 Trial01 — Browser Integration and Protected Regression Evidence

- Gate: `G01`
- Trial: `01`
- Test Item ID: `002`
- Candidate SHA: `f62e3e75ba474928d6f2ca886e9992375c6f16e5`
- Result: `PASS`

## Acceptance Criteria

- `G01-AC03`, `G01-AC04`, `G01-AC06`, `G01-AC08`

## Method / command

The frozen Gate 07 command was invoked independently from the clean isolated exact-candidate worktree after the user-authorized runtime preparation (`mkdir -p test-results/browser_e2e` and `ARIADNE_E2E_USER=1000:1000`):

```bash
docker compose -f compose.yaml -f compose.e1a.yaml -p ariadne-e8 \
  --profile e2e run --build --rm --entrypoint python browser-e2e \
  tests/browser_e2e/run_enh_e8_g01_project_return.py
```

The applicable protected regression was then independently executed from the same exact-candidate worktree:

```bash
docker compose -f compose.yaml -f compose.e1a.yaml -p ariadne-e8 \
  --profile e2e run --build --rm --entrypoint python browser-e2e \
  tests/browser_e2e/run_enh_e7_project_integration.py
```

## Evidence

- Isolated worktree `HEAD` was `f62e3e75ba474928d6f2ca886e9992375c6f16e5` and clean before execution.
- The frozen G01 runner wrote `test-results/browser_e2e/enh-e8-g01-project-return-evidence.json` with `status: PASS`, zero `page_errors`, and four PASS scenarios: direct entry from `overview`, `context`, `data`, and `results`; each keyboard-activates the named return button, reaches `/projects`, then validates Back and Forward.
- The protected runner wrote `test-results/browser_e2e/enh-e7-project-integration-evidence.json` with `status: PASS`. Its PASS scenarios include `project-routes-reload-history`, `project-analysis-launcher`, `cross-surface-reload-history`, and `full-g04-root-pm-analysis-results-pm`.
- Both commands built their source images with `--build` and ran the candidate's Playwright Chromium runner.

## 判定理由

All browser/integration criteria covered by this item passed on the exact candidate. The G01 runner proves the critical direct-entry return/back/forward journey; the protected runner proves existing Project local-navigation and Analysis launch-navigation behavior remains green.
