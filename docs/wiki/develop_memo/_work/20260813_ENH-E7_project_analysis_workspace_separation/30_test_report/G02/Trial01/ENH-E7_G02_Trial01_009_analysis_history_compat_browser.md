# ENH-E7 G02 Trial01 Test Item 009 — analysis_history_compat_browser

- Result: PASS
- Fixed Trial Candidate full SHA: `ba9fd568e20458468f18edf312100499bb03290d`
- Tested Repository State full SHA: `9a0f42f8d8798c91245f3138d899ca77eb414cfb`
- Exact command / method: `docker compose -f compose.yaml -f compose.e1a.yaml -p ariadne-e1a --profile e2e run --rm -v /tmp/enh_e7_g02_browser_verify.py:/tmp/enh_e7_g02_browser_verify.py:ro --entrypoint python browser-e2e /tmp/enh_e7_g02_browser_verify.py`
- Exit code: 0

## AC mapping

| AC | Result |
| --- | --- |
| AC-G02-12, AC-G02-13, AC-G02-14, AC-G02-17, AC-G02-18, AC-G02-19 | PASS |

## Raw relevant evidence

- `test-results/browser_e2e/enh-e7-g02-independent-browser-evidence.json`: all three scenarios PASS; console/page errors empty。
- Browser は legacy deep link `/projects/97d83b3b-d453-46bd-884f-d7acf197527c/explore` を開き、canonical `/projects/97d83b3b-d453-46bd-884f-d7acf197527c/analysis/exploratory/profile` へのnormalizeを確認した。
- Causal family default `setup` と non-default `discovery` を選択後、reload、Back、Forward の各URLと selected contextを確認した。
- Test Item 003 / 007 の frontend contract と ENH-E6 protected tests も PASS。

## Facts

- legacy URL normalization、canonical URL、Family default stage、reload、Back、Forward、resource-route contract は browserおよび frontend contract の両方で成功した。

## Interpretation

- canonical/legacy deep link と history semantics は G02 transition 後も成立する。

## Protected contract / Transition Debt relation

- ENH-E6 canonical Analysis navigation を保護した。legacy analytical URLはparallel surfaceではなく canonical URLへの入口として残る。

## Reproduction procedure

1. repository root で上記 exact command を実行する。
2. evidence JSON の `legacy-deeplink-reload-history: PASS` を確認する。

## Browser evidence

- screenshot: `test-results/browser_e2e/enh-e7-g02-independent-browser.png`
- trace: `test-results/browser_e2e/enh-e7-g02-independent-browser-trace.zip`
- video: `test-results/browser_e2e/enh-e7-g02-independent-video/`
- console / page error: evidence JSON の `console: []`, `page_errors: []`
- network: legacy entry、navigation、reload、history traversal でfailed requestは記録なし。
- service log: compose command exit 0。依存サービスはhealthy/running。
- failed synchronization/assertion: なし。
- failure classification: 該当なし。
