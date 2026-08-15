# 005 cross_surface_history

- Result: PASS
- Fixed Trial Candidate full SHA: `4f9efd1a738303fba49a245511faf7ca3ba333b7`
- Tested Repository State full SHA: `ff6bf3b1f5dcb1c9630184fdcd7932fed510ecc6`
- Exact command / method: `docker compose -f compose.yaml -f compose.e1a.yaml -p ariadne-e1a --profile e2e run --build --rm --entrypoint python browser-e2e tests/browser_e2e/run_enh_e7_project_integration.py`
- Exit code: 0

## AC mapping

AC-G04-06, AC-G04-07, AC-G04-08, AC-G04-09, AC-G04-13, AC-G04-14.

## Direct assertion / predicate mapping

Fresh Chromium creates a Project; PM→Analysis, Analysis→Results, Results→Analysis back/forward, Analysis→PM, reload, selected Project identity, and exactly-one visible top-level surface are asserted. Page error and console error lists are asserted empty.

## Raw relevant evidence

`enh-e7-project-integration-evidence.json` status is `PASS`; scenarios `project-analysis-launcher`, `cross-surface-reload-history`, and `full-g04-root-pm-analysis-results-pm` are all `PASS`.

## Facts

The browser runner's runtime assertions passed.

## Interpretation

Cross-surface transition/history behavior meets this item's scope.

## Protected contract relation

G02 canonical Analysis/cross-surface semantics; G03 architecture.

## Reproduction procedure

Run the command above.

## Browser evidence

JSON plus `enh-e7-g03-p06-project-management.png` and `enh-e7-g03-p06-analysis.png`; runner asserts no console/page errors.
