# Ariadne ENH-E8 G01 Verification Contract

- Document class: Primary Execution Contract / Acceptance Authority
- Verification contract status: `FROZEN`
- Status: `FROZEN`
- Gate: `G01`

## Gate PASS rule

exact Fixed Trial Candidateに対して、blocking Acceptance CriterionがすべてPASSし、protected regressionがgreenの場合のみPASSとする。

environment/harnessのため判定不能な場合はproduct FAILではなく`BLOCKED`とする。

## Acceptance Criteria

| AC | Criterion | Primary layer |
|---|---|---|
| G01-AC01 | Project List return actionがoverview/context/data/resultsで表示される | frontend contract/DOM |
| G01-AC02 | activation targetがcanonical `/projects` である | navigation/frontend test |
| G01-AC03 | destinationがProject Listをrenderし、Selected Project contentではない | frontend integration |
| G01-AC04 | direct-entry Selected Project routeでもreturn actionが成立する | integration/browser |
| G01-AC05 | implementationが`history.back()` originに依存しない | code/contract test |
| G01-AC06 | user PUSH + browser Back/Forwardがdeterministicで余分なrestore entryを作らない | navigation integration + Browser E2E |
| G01-AC07 | actionがkeyboard操作可能でaccessible nameを持つ | DOM/accessibility |
| G01-AC08 | existing Project local navigation / Analysis launch-navigation regressionがPASSする | protected regression |
| G01-AC09 | API/schema/backend/runtime semantic changeがない | diff/architecture audit |

## Browser E2E critical journey

`Selected Project direct entry -> Project List -> Back -> Selected Project -> Forward -> Project List`

Canonical Browser E2E command:

```bash
docker compose -f compose.yaml -f compose.e1a.yaml -p ariadne-e8 \
  --profile e2e run --build --rm --entrypoint python browser-e2e \
  tests/browser_e2e/run_enh_e8_g01_project_return.py
```

Environment/bootstrap authority:

- Compose: `compose.yaml` + `compose.e1a.yaml`
- profile: `e2e`
- service: `browser-e2e`
- browser: Playwright Chromium
- default web URL: `ARIADNE_E2E_WEB_URL=http://127.0.0.1:8080`
- evidence root: `ARIADNE_E2E_OUTPUT_DIR` または `test-results/browser_e2e`
- current-source imageを`--build`で生成し、`--rm`でephemeral runnerを使用する
- scriptはAPI/frontend ready stateをsemanticに待機し、fixed sleepだけをsynchronization authorityにしない

## Decision

Test AgentはTest Item evidenceを作成した後、canonical `999` Gate Decisionを `PASS` / `FAIL` / `BLOCKED` のいずれかで記録する。
