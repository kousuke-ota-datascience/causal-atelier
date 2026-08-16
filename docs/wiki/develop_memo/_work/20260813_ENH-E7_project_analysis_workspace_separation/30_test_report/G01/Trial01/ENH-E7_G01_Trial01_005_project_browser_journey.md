# ENH-E7 G01 Trial01 Test Item 005 — project_browser_journey

- Result: PASS
- Fixed Trial Candidate full SHA: `7936151d98de7fe467c176039add47da6af987c4`
- Tested Repository State full SHA: `fe3b59cca9b5ed5b250beb1b79dd0d451a161db7`
- Exact command / method: `docker compose -f compose.yaml -f compose.e1a.yaml -p ariadne-e1a --profile e2e run --rm --no-deps --entrypoint python browser-e2e tests/browser_e2e/run_enh_e7_project_integration.py`
- Exit code: 0

## AC mapping

| AC | Result |
| --- | --- |
| AC-G01-01 | PASS |
| AC-G01-02 | PASS |
| AC-G01-03 | PASS |
| AC-G01-05 | PASS |
| AC-G01-11 | PASS |

## Raw relevant evidence

- `test-results/browser_e2e/enh-e7-project-integration-evidence.json`は2026-08-14 UTCに`status: PASS`を記録した。
- `create-to-overview`: PASS（Project ID `e971ac22-2e5e-432d-9526-42c43b8e7651`）。
- `project-routes-reload-history`: PASS。
- `legacy-analysis-shortcut`: PASS。

## Facts

- Chromiumは`/projects`からNew Projectを開き、作成後の`/projects/<id>/overview`を確認した。
- Context / Data / Resultsへのlocal navigation、Resultsでのreload、Back / Forwardを確認した。
- legacy Analysis shortcutが`/projects/<id>/analysis/exploratory/profile`へ遷移することを確認した。

## Interpretation

- 必須Project Management journeyおよびProject route direct runtime / browser history behaviorに違反は検出されなかった。

## Protected contract / Transition Debt relation

- legacy Analysis shortcutがPASSしたため、G02 replacement surface成立前の互換shortcut保護に対する回帰は検出されなかった。Transition Debtの追加はない。

## Reproduction procedure

1. `ariadne-e1a` compose environmentを起動する。
2. current `browser-e2e` imageを使用して記載のcompose run commandを実行する。
3. exit code 0およびevidence JSON内の3 scenarioすべて`PASS`を確認する。

## Browser evidence

- screenshot / trace / video: failureなしのため生成なし。
- console / page error: evidenceにerror記録なし。
- network: failureなし。API READYを待機して各routeを確認した。
- service log: failureなしのため追加採取なし。
- failed synchronization/assertion: なし。
- failure classification: N/A（PASS）。
