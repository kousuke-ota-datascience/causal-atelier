# 008 full_product_browser_journey

- Result: PASS
- Fixed Trial Candidate full SHA: `d2d5a9a7f6df352d787c8d561fce937012eef854`
- Tested Repository State full SHA: `9e85e4a6a2365869b48e5bc6c0b0ac6845698869`
- Exact command / method: `docker compose -f compose.yaml -f compose.e1a.yaml -p ariadne-e1a --profile e2e run --build --rm --entrypoint python browser-e2e tests/browser_e2e/run_enh_e7_project_integration.py`
- Exit code: 0

## AC mapping

AC-G04-01 through AC-G04-09, AC-G04-12 through AC-G04-14 (browser-applicable scope).

## Direct assertion / predicate mapping

A fresh Chromium context asserts `/`→`/projects`; Project creation and overview; PM Context/Data/Results; canonical Analysis launch; Family switch; Stage switch; Results return; PM return; reload; Back/Forward.  At each route checkpoint it asserts pathname, exactly one visible top-level surface root, and selected Project identity.  It captures console/page errors and asserts the list is empty.

## Raw relevant evidence

Evidence JSON status `PASS`.  `create-to-overview`, `project-routes-reload-history`, `project-analysis-launcher`, `cross-surface-reload-history`, and `full-g04-root-pm-analysis-results-pm` are all `PASS`.

## Facts

All five browser scenarios passed in the fresh browser context.

## Interpretation

The G04 end-to-end journey meets the browser-applicable direct assertions while preserving G03 surface architecture.

## Protected contract relation

G01 Project, G02 Analysis/cross-surface behavior, G03 surface architecture, ENH-E6 Family/Stage.

## Reproduction procedure

Run the command above.

## Browser evidence

`test-results/browser_e2e/enh-e7-project-integration-evidence.json`; success screenshots: `enh-e7-g03-p06-projects.png`, `enh-e7-g03-p06-project-management.png`, `enh-e7-g03-p06-analysis.png`; console/page errors: none.
