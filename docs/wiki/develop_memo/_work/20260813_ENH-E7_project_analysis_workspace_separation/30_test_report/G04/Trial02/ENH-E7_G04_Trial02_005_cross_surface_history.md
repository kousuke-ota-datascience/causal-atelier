# 005 cross_surface_history

- Result: PASS
- Fixed Trial Candidate full SHA: `d2d5a9a7f6df352d787c8d561fce937012eef854`
- Tested Repository State full SHA: `9e85e4a6a2365869b48e5bc6c0b0ac6845698869`
- Exact command / method: `.venv/bin/pytest -q tests/product/test_enh_e7_g04_p04_cross_surface_history_navigation.py`; fresh-browser runner `docker compose -f compose.yaml -f compose.e1a.yaml -p ariadne-e1a --profile e2e run --build --rm --entrypoint python browser-e2e tests/browser_e2e/run_enh_e7_project_integration.py`
- Exit code: 0

## AC mapping

AC-G04-06, AC-G04-07, AC-G04-08, AC-G04-09, AC-G04-13, AC-G04-14.

## Direct assertion / predicate mapping

The direct tests assert browser-runner coverage for PM→Analysis→Results reload/Back/Forward, shared transition authority retaining Project without duplicate entries, and stale Analysis shell clearing on PM/Results restore.  Chromium executes the corresponding visible-surface journey and asserts no console/page errors.

## Raw relevant evidence

`3 passed` in G04 P04.  Browser `cross-surface-reload-history=PASS`; browser `full-g04-root-pm-analysis-results-pm=PASS`; no console/page errors were captured.

## Facts

Route, visible-root, project identity, reload, Back/Forward, and error predicates passed.

## Interpretation

Cross-surface transition/history contract is satisfied without stale shell or duplicate history evidence.

## Protected contract relation

G02 cross-surface history and G03 exclusive top-level-surface architecture.

## Reproduction procedure

Run the commands above.

## Browser evidence

`test-results/browser_e2e/enh-e7-project-integration-evidence.json`; success screenshots include `enh-e7-g03-p06-analysis.png`.
