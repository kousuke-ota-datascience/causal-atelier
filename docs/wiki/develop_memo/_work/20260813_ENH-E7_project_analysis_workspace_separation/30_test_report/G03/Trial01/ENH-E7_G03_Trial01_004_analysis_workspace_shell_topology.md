# ENH-E7 G03 Trial01 Test Item 004 — analysis_workspace_shell_topology

- Result: PASS
- Fixed Trial Candidate full SHA: `cc4fb35b66545af50ed96fd2f80aff7f9a619a5e`
- Tested Repository State full SHA: `cc4fb35b66545af50ed96fd2f80aff7f9a619a5e`
- Exact command / method: G03 focused pytest suite; Chromium direct DOM/visibility probe for `/projects/832a905a-7808-49ec-8901-c4bf5d8dd219/analysis/exploratory/profile`.
- Exit code: 0

## AC mapping

| AC | Result |
| --- | --- |
| AC-G03-04, AC-G03-05, AC-G03-06, AC-G03-07 | PASS |
| AC-G03-09, AC-G03-10 | PASS (Analysis topology portion) |

## Direct assertion / predicate mapping

- visible root は唯一の `analysis`。
- Analysis root は Context、family、stage を descendant として所有し、PM nav は非表示。
- Analysis root 内の `#return-to-project-management` は visible。

## Raw relevant evidence

- Chromium: `activeRoots:["analysis"]`, `rootOwnsContext:true`, `rootOwnsFamily:true`, `rootOwnsStage:true`, `rootOwnsProjectNav:false`, `projectNavVisible:false`, `contextVisible:true`, `returnVisible:true`。
- G03 focused structural suite: 15 passed。

## Facts

- Analysis is a separate top-level root; context/return action are owned by it.

## Interpretation

- Analysis Workspace Shell の ownership/visibility predicate は成立する。

## Protected contract relation

- Project-to-Analysis canonical route を用い、PM shell を hidden DOM の visible substitute にしていない。

## Reproduction procedure

1. Item 002 の pytest command を実行する。
2. 上記 Analysis route で root containment/visibility を evaluate する。

## Browser evidence

- Success screenshot: `test-results/browser_e2e/enh-e7-g03-independent-direct-analysis.png`。
- console/page error: none。network/service log: API READY。
