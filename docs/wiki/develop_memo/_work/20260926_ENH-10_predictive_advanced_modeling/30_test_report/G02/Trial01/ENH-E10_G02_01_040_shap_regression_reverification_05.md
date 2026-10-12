# ENH-E10 G02 Trial 01 — Test Item 040: SHAP Regression（reverification 05）

| Fixed Candidate | Tested SHA | AC | 判定 |
| --- | --- | --- | --- |
| `fbd97c5b7a95084affe5e2381d85d86d0dfa2558` | `1bf3026ba1918c8ca74af64318bdd42e90d7ed67` | AC-04, AC-09, AC-10, AC-11 | **PASS** |

## 実行

```bash
MPLCONFIGDIR=/tmp/ariadne-mpl UV_CACHE_DIR=/tmp/ariadne-uv-cache \
uv run --extra predictive-advanced pytest -q \
 tests/product/test_enh_e10_g02_p02_shap_backend.py
```

runtime: Python `3.12.3` / LightGBM `4.7.0` / SHAP `0.52.0`。この test の parametrized actual DAG case は `REGRESSION` + `lightgbm_regressor.v1` を実行した。raw independent-suite result は `43 passed, 2 warnings in 18.97s`、exit `0`（warnings は binary SHAP provider notification のみ）。

## 観測事実

- `split → prepare → train → evaluate → explain` は全て `SUCCEEDED`、Explanation Result は `GENERATED`。
- global / local SHAP はともに非空で、local TEST row ordinals と provenance `test_instances` が一致した。
- raw model-output と prediction-output scale はともに `PREDICTION`。各 local output は `base_value + Σ contribution` と `atol=1e-6, rtol=1e-5` で一致した。
- method/provider version、model `lightgbm_regressor.v1` / task、preprocessor canonical hash、feature order/hash、TEST sample identity、`TREE_PATH_DEPENDENT` background、sampling、parameters、runtime versions、predictive-not-causal limitation を Result が記録した。
- Explanation Artifact の `method_provenance` と Model Card の `explanation_provenance` は Result の同値の provenance。training binding に TEST は入らない。

## 解釈

回帰 SHAP が actual EXPLAIN stage から canonical result/artifact/model-card まで到達することを確認した。direct provider unit test による推定ではない。AC-04、および関連 AC-09/10/11 は **PASS**。
