# ENH-E7 G03 Trial01 Test Item 008 — surface_architecture_browser_journey

- Result: PASS
- Fixed Trial Candidate full SHA: `cc4fb35b66545af50ed96fd2f80aff7f9a619a5e`
- Tested Repository State full SHA: `cc4fb35b66545af50ed96fd2f80aff7f9a619a5e`
- Exact command / method: `docker compose -f compose.yaml -f compose.e1a.yaml -p ariadne-e1a --profile e2e run --build --rm --entrypoint python browser-e2e tests/browser_e2e/run_enh_e7_project_integration.py`; followed by independent Chromium DOM/computed-layout probe.
- Exit code: 0

## AC mapping

| AC | Result |
| --- | --- |
| AC-G03-01 through AC-G03-07, AC-G03-10, AC-G03-13 | PASS |

## Direct assertion / predicate mapping

- Browser journey creates a Project, reaches PM overview, covers context/data/results reload/history, then launches Analysis.
- Independent probe directly verifies exclusive visible root and all containment/visibility predicates in Items 002–005.

## Raw relevant evidence

- runner output: `{"status":"PASS","evidence":"/evidence/enh-e7-project-integration-evidence.json"}`。
- evidence scenarios PASS: `create-to-overview`, `project-routes-reload-history`, `project-analysis-launcher`。
- direct Analysis probe: PM nav false; Context/family/stage/return true; family row; stage column; stage right=301 < main left=319。

## Facts

- Projects → PM → Analysis browser journey passes on Compose services.

## Interpretation

- end-to-end runtime evidence corroborates direct DOM and layout predicates; screenshots are supplemental, not sole evidence.

## Protected contract relation

- Project route/reload/history and Analysis launch are preserved in a real Chromium session.

## Reproduction procedure

1. repository root で上記 Compose command を実行する。
2. evidence JSON の全 scenario PASS と screenshots を確認する。
3. root/visibility/layout predicate を browser evaluate で再確認する。

## Browser evidence

- Success screenshots: `test-results/browser_e2e/enh-e7-g03-p06-projects.png`, `test-results/browser_e2e/enh-e7-g03-p06-project-management.png`, `test-results/browser_e2e/enh-e7-g03-p06-analysis.png`, `test-results/browser_e2e/enh-e7-g03-independent-direct-analysis.png`。
- console/page error: none。network/service log: API READY; Compose API health check passed.
