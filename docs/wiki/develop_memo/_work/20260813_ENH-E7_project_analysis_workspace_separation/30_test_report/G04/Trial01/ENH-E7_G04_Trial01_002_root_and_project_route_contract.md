# 002 root_and_project_route_contract

- Result: PASS
- Fixed Trial Candidate full SHA: `4f9efd1a738303fba49a245511faf7ca3ba333b7`
- Tested Repository State full SHA: `ff6bf3b1f5dcb1c9630184fdcd7932fed510ecc6`
- Exact command / method: `.venv/bin/pytest -q tests/product/test_enh_e7_g04_p01_root_project_route_reintegration.py`
- Exit code: 0

## AC mapping

AC-G04-01, AC-G04-02, AC-G04-09.

## Direct assertion / predicate mapping

Route classifier maps `/projects`, `/projects/new`, `/projects/<id>`, `/projects/<id>/overview` to the correct surface; short route serializes to overview; root restore uses `REPLACE`; creation uses `REPLACE` to overview.

## Raw relevant evidence

`3 passed in 2.01s` within the six-file focused command (`20 passed` total). Browser evidence records `/` normalized to `/projects` and `project-routes-reload-history: PASS`.

## Facts

The asserted route and history predicates passed.

## Interpretation

Root normalization and canonical Project route semantics pass.

## Protected contract relation

G01 canonical Project semantics.

## Reproduction procedure

Run the command above; browser procedure is in item 009.

## Browser evidence

`test-results/browser_e2e/enh-e7-project-integration-evidence.json`: `project-routes-reload-history: PASS`; screenshots `enh-e7-g03-p06-projects.png`, `enh-e7-g03-p06-project-management.png`.
