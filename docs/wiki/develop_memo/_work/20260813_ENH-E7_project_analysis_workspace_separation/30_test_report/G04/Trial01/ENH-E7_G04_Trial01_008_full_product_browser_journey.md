# 008 full_product_browser_journey

- Result: PASS
- Fixed Trial Candidate full SHA: `4f9efd1a738303fba49a245511faf7ca3ba333b7`
- Tested Repository State full SHA: `ff6bf3b1f5dcb1c9630184fdcd7932fed510ecc6`
- Exact command / method: `docker compose -f compose.yaml -f compose.e1a.yaml -p ariadne-e1a --profile e2e run --build --rm --entrypoint python browser-e2e tests/browser_e2e/run_enh_e7_project_integration.py`
- Exit code: 0

## AC mapping

AC-G04-01 through AC-G04-09, AC-G04-12 through AC-G04-14 (browser-applicable scope).

## Direct assertion / predicate mapping

The fresh-browser journey asserts `/`→`/projects`, Project creation, PM context/data/results, Analysis launch, Family switch, Stage switch, Results, PM return, and exactly-one surface root / selected Project at each checkpoint.

## Raw relevant evidence

Evidence JSON status `PASS`; `create-to-overview`, `project-routes-reload-history`, `project-analysis-launcher`, `cross-surface-reload-history`, and `full-g04-root-pm-analysis-results-pm` are `PASS`.

## Facts

Every runner scenario passed in the executed browser context.

## Interpretation

The required success journey passes.

## Protected contract relation

G03 architecture, G01 Project, G02 Analysis transitions, ENH-E6 Family/Stage.

## Reproduction procedure

Run the command above.

## Browser evidence

`test-results/browser_e2e/enh-e7-project-integration-evidence.json`; success screenshots `enh-e7-g03-p06-projects.png`, `enh-e7-g03-p06-project-management.png`, `enh-e7-g03-p06-analysis.png`; no console/page errors asserted.
