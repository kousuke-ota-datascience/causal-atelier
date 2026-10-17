# ENH-E10 G03 Trial 01 — テスト項目 110: Browser Regression LightGBM LIME

| Candidate | Tested SHA | AC | 結果 |
| --- | --- | --- | --- |
| `64bd2a18dd583349283cd5745edf63d9b28d61ad` | `df278f76ff476143545d73037fe55f96664dae28` | AC-10, AC-03, AC-04, AC-06, AC-07 | **PASS** |

## 方法・生証跡

item 100 と同じ frozen clean-compose command と Playwright Chromium `1.62.0` lifecycle を実行した。runner は scenario 100 の状態を使わず、distinct deterministic regression project/dataset/context identity を生成した。

`test-results/browser_e2e/enh_e10/evidence.json` は scenario `110` を `PASS`、execution `96b4c134-37bc-498c-a751-4a00aa613c84` と記録する。`split`、`prepare`、`train`、`evaluate`、`explain` は全て first attempt で成功した。persisted result types は `PREDICTIVE_EXPLANATION_RESULT` と `MODEL_CARD_RESULT`、artifacts は `FITTED_MODEL`、`PREDICTIVE_EXPLANATION`、`MODEL_CARD`、`PREDICTION` を含む。trace/video は frozen evidence path にある。

## 事実・解釈

browser は Regression、`lightgbm_regressor.v1`、explicit local `LIME_TABULAR` を選択した。runner は API terminal status と Result/Artifact availability を待機し、generated explanation、Model Card model identity、artifact presence、predictive-not-causal UI wording を検証した。G02 protected tests は LIME `PREDICTION` scale、TRAIN reference/row provenance、global-LIME の明示的 unavailable behavior を別途検証する。合わせて pseudo-global fallback なしに frozen regression critical journey を満たす。

## 再現・診断・判定

正本の 3 compose lifecycle commands を clean project で実行する。API/worker は `Dockerfile.predictive-advanced`、browser image は Playwright Chromium `1.62.0`。runner と final teardown は exit `0`。trace/video、terminal execution polling、`/results`、`/artifacts` は `test-results/browser_e2e/enh_e10/` に保持する。synchronization/page/console/network/API/worker failure はない。candidate/post-candidate mutation audit は item 001 のとおり。AC-10 の observable journey requirement は全て満たす。**PASS**。
