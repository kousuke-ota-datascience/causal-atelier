# ENH-E10 G03 Trial 01 — Test Item 100: Browser Binary LightGBM SHAP

| Candidate | Tested SHA | AC | Result |
| --- | --- | --- | --- |
| `64bd2a18dd583349283cd5745edf63d9b28d61ad` | `df278f76ff476143545d73037fe55f96664dae28` | AC-09, AC-03, AC-04, AC-06, AC-07 | **PASS** |

## Frozen command / runtime

```bash
docker compose -f compose.yaml -f compose.e1a.yaml -f compose.enh_e10.yaml \
  -p ariadne-enh-e10 down -v --remove-orphans
docker compose -f compose.yaml -f compose.e1a.yaml -f compose.enh_e10.yaml \
  -p ariadne-enh-e10 --profile e2e run --build --rm --entrypoint python browser-e2e \
  tests/enhancement/enh_e10/g03/browser_e2e/run_predictive_advanced.py
```

Runtime: clean compose project `ariadne-enh-e10`; API/worker `Dockerfile.predictive-advanced`; browser image Playwright Chromium `1.62.0`. Final cleanup `down -v --remove-orphans` completed.

## Raw evidence

`test-results/browser_e2e/enh_e10/evidence.json` records scenario `100` as `PASS`, execution `4e45628b-a05e-4ceb-8b6f-782c88d4b992`. `split`, `prepare`, `train`, `evaluate`, `explain` are all `SUCCEEDED` on attempt 1. Result types include `PREDICTIVE_EXPLANATION_RESULT` and `MODEL_CARD_RESULT`; artifacts include `FITTED_MODEL`, `PREDICTIVE_EXPLANATION`, `MODEL_CARD`, and `PREDICTION`. Trace and video are retained under the same evidence directory.

## Facts / interpretation

The browser selected Binary Classification, `lightgbm_classifier.v1`, and `SHAP_TREE`; runner synchronization waited for API terminal execution, persisted result/artifact retrieval, and final UI visibility. It required generated explanation output, Model Card model identity, and predictive-not-causal text. This proves the frozen cross-layer binary journey rather than merely direct SHAP backend success. **PASS**。
