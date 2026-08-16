# 002 root_and_project_route_contract

- Result: PASS
- Fixed Trial Candidate full SHA: `d2d5a9a7f6df352d787c8d561fce937012eef854`
- Tested Repository State full SHA: `9e85e4a6a2365869b48e5bc6c0b0ac6845698869`
- Exact command / method: `.venv/bin/pytest -q tests/product/test_enh_e7_g04_p01_root_project_route_reintegration.py`; fresh-browser runner `docker compose -f compose.yaml -f compose.e1a.yaml -p ariadne-e1a --profile e2e run --build --rm --entrypoint python browser-e2e tests/browser_e2e/run_enh_e7_project_integration.py`
- Exit code: 0

## AC mapping

AC-G04-01, AC-G04-02, AC-G04-09.

## Direct assertion / predicate mapping

The three direct tests assert exclusive expected top-level surface for Project routes, `/` replacement normalization to `/projects` without a legacy workspace, and create-success replacement navigation to the new Project overview.  The browser runner independently asserts root normalization, Project creation, route/reload/history behavior, visible root, and selected Project identity.

## Raw relevant evidence

`3 passed` in the G04 P01 file; browser evidence status `PASS`, including `create-to-overview=PASS` and `project-routes-reload-history=PASS`.

## Facts

The asserted route and history predicates passed.

## Interpretation

Root and canonical Project route contract is satisfied.

## Protected contract relation

G01 canonical Project semantics and G04 reintegration contract.

## Reproduction procedure

Run the commands above.

## Browser evidence

`test-results/browser_e2e/enh-e7-project-integration-evidence.json`; screenshots: `enh-e7-g03-p06-projects.png`, `enh-e7-g03-p06-project-management.png`.
