# ENH-E8 G01 Trial01 Implementation Completion Evidence

## Candidate

- Gate: `G01`
- Trial: `01`
- Fixed Trial Candidate SHA: `f62e3e75ba474928d6f2ca886e9992375c6f16e5`
- Candidate status: `IMPLEMENTED / SELF-CHECKED`

This record is implementation evidence only. It does not declare Gate PASS.

## Implemented contract items

- Added one native `Project Listへ戻る` button to the shared Selected Project shell; it is therefore visible in `overview`, `context`, `data`, and `results` (`Results / Lineage`).
- Wired the action through existing `ProjectNavigation` collection-route serialization and the existing `synchronizeProjectHistory(..., 'PUSH')` / workspace transition path. The target is `/projects`; `history.back()` is not used to choose it.
- Added responsive shell styling for the action.
- Added the frozen G01 browser candidate runner and its browser-image build inputs.

## Focused self-check

| Check | Result | Evidence |
|---|---|---|
| JavaScript syntax | PASS | `node --check frontend/app.js` |
| Browser runner syntax | PASS | `python3 -m py_compile tests/browser_e2e/run_enh_e8_g01_project_return.py` |
| Candidate diff whitespace | PASS | `git diff --check -- .dockerignore Dockerfile.browser-e2e frontend/app.js frontend/index.html frontend/styles.css tests/browser_e2e/run_enh_e8_g01_project_return.py` |
| Direct entry / return / Back / Forward | PASS | Four real-Chromium scenarios in `test-results/browser_e2e/enh-e8-g01-project-return-evidence.json` |
| Keyboard activation and accessible name | PASS | Each scenario focuses the native button named `Project Listへ戻る` and activates it with Enter. |
| Project local-navigation and Analysis launcher regression | PASS (focused) | The test traverses all existing local section routes, and the implementation only adds a sibling shell action; it does not modify local-navigation or Analysis-launcher handlers. |

Browser command executed:

```text
docker compose -f compose.yaml -f compose.e1a.yaml -p ariadne-e1a --profile e2e run --build --rm --entrypoint python browser-e2e tests/browser_e2e/run_enh_e8_g01_project_return.py
```

The generated browser evidence reports `status: PASS`, no page errors, and four PASS scenarios for `overview`, `context`, `data`, and `results`.

## Limits

- This is a coding-agent self-check, not independent verification.
- No Gate PASS decision is made in this report.
