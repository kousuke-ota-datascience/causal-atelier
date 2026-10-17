# ENH-E10 G03 Trial 01 — テスト項目 100: Browser Binary LightGBM SHAP

| Candidate | Tested SHA | AC | 結果 |
| --- | --- | --- | --- |
| `64bd2a18dd583349283cd5745edf63d9b28d61ad` | `df278f76ff476143545d73037fe55f96664dae28` | AC-09, AC-03, AC-04, AC-06, AC-07 | **PASS** |

## Frozen command・実行環境

正本記載の frozen lifecycle、すなわち `docker compose -f compose.yaml -f compose.e1a.yaml -f compose.enh_e10.yaml -p ariadne-enh-e10 down -v --remove-orphans`、`--profile e2e run --build --rm --entrypoint python browser-e2e tests/enhancement/enh_e10/g03/browser_e2e/run_predictive_advanced.py`、最終 cleanup を実行した。runtime は clean compose project `ariadne-enh-e10`、API/worker は `Dockerfile.predictive-advanced`、browser image は Playwright Chromium `1.62.0`。最終 cleanup は完了した。

## 生証跡・事実

`test-results/browser_e2e/enh_e10/evidence.json` は scenario `100` を `PASS`、execution `4e45628b-a05e-4ceb-8b6f-782c88d4b992` と記録する。`split`、`prepare`、`train`、`evaluate`、`explain` は全て attempt 1 で `SUCCEEDED`。result types は `PREDICTIVE_EXPLANATION_RESULT` と `MODEL_CARD_RESULT`、artifacts は `FITTED_MODEL`、`PREDICTIVE_EXPLANATION`、`MODEL_CARD`、`PREDICTION` を含む。trace/video は同じ evidence directory に保持される。

browser は Binary Classification、`lightgbm_classifier.v1`、`SHAP_TREE` を選択した。runner は API terminal execution、persisted result/artifact retrieval、最終 UI visibility を待機し、generated explanation output、Model Card model identity、predictive-not-causal text を要求した。これは direct SHAP backend success だけではなく frozen cross-layer binary journey を証明する。

## 診断・再現・判定

runner 前に database/API は healthy、migrate は exit `0`、worker/frontend は起動した。runner と final teardown は exit `0`。failed synchronization point、page error、console failure、failure classification はない。network evidence は記録済 execution ID の API terminal-status polling と `/results`、`/artifacts` retrieval である。clean project で上記 3 lifecycle commands を実行して再現する。candidate は advanced runtime と runner のみを変更し、candidate 後に未監査の product mutation はない。AC-09 の observable sequence/persistence requirement は全て満たす。**PASS**。
