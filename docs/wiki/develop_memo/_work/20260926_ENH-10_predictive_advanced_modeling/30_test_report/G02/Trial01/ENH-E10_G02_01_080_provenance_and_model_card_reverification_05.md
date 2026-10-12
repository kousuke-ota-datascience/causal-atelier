# ENH-E10 G02 Trial 01 — Test Item 080: Provenance and Model Card（reverification 05）

| Fixed Candidate | Tested SHA | AC | 判定 |
| --- | --- | --- | --- |
| `fbd97c5b7a95084affe5e2381d85d86d0dfa2558` | `1bf3026ba1918c8ca74af64318bdd42e90d7ed67` | AC-09, AC-11 | **PASS** |

## 実行

```bash
MPLCONFIGDIR=/tmp/ariadne-mpl UV_CACHE_DIR=/tmp/ariadne-uv-cache \
uv run --extra predictive-advanced pytest -q \
 tests/product/test_enh_e10_g02_p02_shap_backend.py \
 tests/product/test_enh_e10_g02_p03_lime_backend.py \
 tests/product/test_predictive_api_worker_e2e_e3.py
```

runtime: Python `3.12.3` / SHAP `0.52.0` / LIME `0.2.0.1` / LightGBM `4.7.0`。raw complete suite result は `43 passed, 2 warnings in 18.97s`、exit `0`。

## 観測事実

- SHAP binary / regression の `method_provenance` は method/version、model/task/schema、preprocessor canonical hash、feature order/hash、global TEST identity、local TEST row ordinal、tree-path background、raw output scale、sampling、frozen additivity parameters、provider/runtime versionsを含む。SHAP に TRAIN reference は存在しない。
- LIME binary / regression は同じ共通 identity に加え、TRAIN reference schema/count/hash/seed/partition、per-row effective seed、categorical indices、frozen LIME parameters を含む。raw TRAIN features は永続化しない。
- Explanation Result payload、PREDICTIVE_EXPLANATION JSON Artifact、MODEL_CARD_RESULT の `explanation_provenance`、MODEL_CARD JSON Artifact は method ごとに同一 provenance を保持した。
- limitations は一貫して `Predictive Explanation is not a Causal Explanation or Treatment Effect.` を含む。

## 解釈

Result / Artifact / Model Card に同一の再構成可能な provenance が到達しており、SHAP と LIME のいずれについても前回の SHAP stage gap は再現しない。AC-09 / AC-11 は **PASS**。
