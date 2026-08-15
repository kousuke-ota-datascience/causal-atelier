# ENH-E7 G04 Trial01 Implementation Report Detail

## Package ledger

| Package | State | Status report | Optional implementation HEAD |
|---|---|---|---|
| P01 | PACKAGE_COMPLETE | `packages/ENH-E7_G04_P01_Trial01_package_execution_status.md` | cc4fb35b66545af50ed96fd2f80aff7f9a619a5e |
| P02 | PACKAGE_COMPLETE | `packages/ENH-E7_G04_P02_Trial01_package_execution_status.md` | cc4fb35b66545af50ed96fd2f80aff7f9a619a5e |
| P03 | PACKAGE_COMPLETE | `packages/ENH-E7_G04_P03_Trial01_package_execution_status.md` | cc4fb35b66545af50ed96fd2f80aff7f9a619a5e |
| P04 | PACKAGE_COMPLETE | `packages/ENH-E7_G04_P04_Trial01_package_execution_status.md` | cc4fb35b66545af50ed96fd2f80aff7f9a619a5e |
| P05 | PACKAGE_COMPLETE | `packages/ENH-E7_G04_P05_Trial01_package_execution_status.md` | cc4fb35b66545af50ed96fd2f80aff7f9a619a5e |
| P06 | PACKAGE_COMPLETE | `packages/ENH-E7_G04_P06_Trial01_package_execution_status.md` | cc4fb35b66545af50ed96fd2f80aff7f9a619a5e |

## Integration observations

- `/`→`/projects`, Project routes, Analysis deep links, Family/Stage transitions, Results, reload, Back, and Forward were exercised by the shared Chromium harness.
- Each workspace was checked against the expected sole top-level surface root.
- Project identity remained selected across PM↔Analysis↔Results transitions.

## Protected contract observations

- Legacy analytical URLs normalize through `AnalysisNavigation.legacyContext`.
- Resource routes retain resource identity through `AnalysisNavigation.contextForResource`.
- Data Quality remains read-only; TIME_TREND and CHART retain their result/artifact contracts; Causal/Predictive stage transitions remain presentation-only.

## Candidate-affecting diff audit

- Candidate commit `4f9efd1a738303fba49a245511faf7ca3ba333b7` contains only G04 implementation/test files: `frontend/app.js`, `tests/browser_e2e/run_enh_e7_project_integration.py`, and six G04 focused product tests.
- Existing uncommitted planning/contract/architecture-review/G03 evidence artifacts were excluded as non-candidate changes.
- No candidate-affecting file is modified after the Fixed Candidate commit.

## Candidate Assembly verification commands/results

- `UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run pytest -q [G04 P01–P06 focused tests and G03 P01–P06 structural tests]` — PASS, 35 passed.
- `docker compose -f compose.yaml -f compose.e1a.yaml -p ariadne-e1a --profile e2e run --build --rm --entrypoint python browser-e2e tests/browser_e2e/run_enh_e7_project_integration.py` — PASS.
- `node --check frontend/app.js` — PASS.
- `python3 -m py_compile tests/browser_e2e/run_enh_e7_project_integration.py` — PASS.
- `git diff --check` and cached-diff audit — PASS.

## Fixed Trial Candidate full SHA

`4f9efd1a738303fba49a245511faf7ca3ba333b7`
