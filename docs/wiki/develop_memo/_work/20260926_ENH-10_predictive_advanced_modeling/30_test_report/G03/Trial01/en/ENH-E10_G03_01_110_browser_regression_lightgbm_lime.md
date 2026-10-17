# ENH-E10 G03 Trial 01 — Test Item 110: Browser Regression LightGBM LIME

| Candidate | Tested SHA | AC | Result |
| --- | --- | --- | --- |
| `64bd2a18dd583349283cd5745edf63d9b28d61ad` | `df278f76ff476143545d73037fe55f96664dae28` | AC-10, AC-03, AC-04, AC-06, AC-07 | **PASS** |

## Method / runtime

Executed by the same frozen clean-compose command and Playwright Chromium `1.62.0` lifecycle recorded in item 100. The runner generated a distinct deterministic regression project/dataset/context identity and did not use state from scenario 100.

## Raw evidence

`test-results/browser_e2e/enh_e10/evidence.json` records scenario `110` as `PASS`, execution `96b4c134-37bc-498c-a751-4a00aa613c84`. All `split`, `prepare`, `train`, `evaluate`, and `explain` stages succeeded on first attempt. Persisted result types contain `PREDICTIVE_EXPLANATION_RESULT` and `MODEL_CARD_RESULT`; artifacts contain `FITTED_MODEL`, `PREDICTIVE_EXPLANATION`, `MODEL_CARD`, and `PREDICTION`. Trace/video are available in the frozen evidence path.

## Facts / interpretation

The browser selected Regression, `lightgbm_regressor.v1`, and explicit local `LIME_TABULAR`; the runner awaited API terminal status and Result/Artifact availability, then asserted generated explanation, Model Card model identity, artifact presence, and predictive-not-causal UI wording. G02 protected tests separately verify LIME PREDICTION scale, TRAIN reference/row provenance, and global-LIME explicit unavailability. Together these satisfy the frozen regression critical journey without pseudo-global fallback. **PASS**。

## Exact reproduction / environment / diagnostics

```bash
docker compose -f compose.yaml -f compose.e1a.yaml -f compose.enh_e10.yaml -p ariadne-enh-e10 down -v --remove-orphans
docker compose -f compose.yaml -f compose.e1a.yaml -f compose.enh_e10.yaml -p ariadne-enh-e10 --profile e2e run --build --rm --entrypoint python browser-e2e tests/enhancement/enh_e10/g03/browser_e2e/run_predictive_advanced.py
docker compose -f compose.yaml -f compose.e1a.yaml -f compose.enh_e10.yaml -p ariadne-enh-e10 down -v --remove-orphans
```

Browser image is Playwright Chromium `1.62.0`; API/worker use `Dockerfile.predictive-advanced`. Runner and final teardown exit codes were `0`. Trace/video, terminal execution polling, `/results`, and `/artifacts` evidence are retained under `test-results/browser_e2e/enh_e10/`. No failure classification applies because no synchronization, page, console, network, API, or worker failure occurred. Candidate/post-candidate mutation audit is as item 001. Criterion evaluation: all AC-10 observable journey requirements are satisfied. **PASS**。
