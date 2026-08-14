# ENH-E7 G02 Trial01 Test Item 008 — analysis_main_browser_journey

- Result: PASS
- Fixed Trial Candidate full SHA: `ba9fd568e20458468f18edf312100499bb03290d`
- Tested Repository State full SHA: `9a0f42f8d8798c91245f3138d899ca77eb414cfb`
- Exact command / method: `docker compose -f compose.yaml -f compose.e1a.yaml -p ariadne-e1a --profile e2e run --build --rm --entrypoint python browser-e2e tests/browser_e2e/run_enh_e7_project_integration.py`; independent Playwright method: `docker compose -f compose.yaml -f compose.e1a.yaml -p ariadne-e1a --profile e2e run --rm -v /tmp/enh_e7_g02_browser_verify.py:/tmp/enh_e7_g02_browser_verify.py:ro --entrypoint python browser-e2e /tmp/enh_e7_g02_browser_verify.py`
- Exit code: 0 (both commands)

## AC mapping

| AC | Result |
| --- | --- |
| AC-G02-01, AC-G02-02, AC-G02-06, AC-G02-07, AC-G02-08, AC-G02-09, AC-G02-10, AC-G02-15, AC-G02-16 | PASS |

## Raw relevant evidence

- repository Browser harness output: `{\"evidence\": \"/evidence/enh-e7-project-integration-evidence.json\", \"status\": \"PASS\"}`。
- independent browser evidence は project `97d83b3b-d453-46bd-884f-d7acf197527c` に対して `workspace-family-stage`、`analysis-results-project`、`legacy-deeplink-reload-history` の全て PASS。
- independent journey は Project Overview → Exploratory/Profile → Distribution → Predictive/Setup → Results → Project Overview を実行した。
- Causal mapped surfaceと Exploratory/Predictive operabilityの具体的な handler/operation contract は Test Item 004–006 で別途PASSした。

## Facts

- real Chromium で Project launcher、Analysis Family/Stage selected state、Results / Project routing が稼働した。
- browser console と page errors は空配列。

## Interpretation

- Analysis Workspace は Project Management から起動でき、Family/Stage surfaceおよび Results / Projectへの遷移が実ブラウザで成立する。

## Protected contract / Transition Debt relation

- 独立 analytical sidebar shortcut に頼らず、Project launcher と Analysis Workspace 内 navigation が使われる。

## Reproduction procedure

1. repository root で上記 first command を実行する。
2. 追加の independent journey は同じ compose environment と `/tmp/enh_e7_g02_browser_verify.py` を用いて second command を実行する。
3. evidence JSON の全scenarioが PASS であることを確認する。

## Browser evidence

- screenshot: `test-results/browser_e2e/enh-e7-g02-independent-browser.png`
- trace: `test-results/browser_e2e/enh-e7-g02-independent-browser-trace.zip`
- video: `test-results/browser_e2e/enh-e7-g02-independent-video/`
- console / page error: `enh-e7-g02-independent-browser-evidence.json` の `console: []`, `page_errors: []`
- network: Browser journey failed synchronizationなし。API health ready を待機し、project creation / catalog / workspace routeが成功。
- service log: compose command exit 0。api / worker / frontend / database healthy/running。
- failed synchronization/assertion: なし。
- failure classification: 該当なし。
