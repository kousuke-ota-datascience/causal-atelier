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

## fixture と検証手順

同じ parametrized full-DAG test の regression branch は target `3 * score - 2`、model `lightgbm_regressor.v1`、`num_boost_round=8`、`min_data_in_leaf=4`、`SHAP_TREE/FIRST_N,size=3,seed=17` を使用する。これは classification branch と model/task/output-scale を独立に切り替えるため、binary assertion の偶然の通過を regression PASS に読み替えていない。

```text
test_shap_tree_full_dag_persists_canonical_provenance
  [BINARY_CLASSIFICATION-LOG_ODDS]   PASS
  [REGRESSION-PREDICTION]            PASS
```

## assertion と判断根拠

- output は raw `PREDICTION` であり、binary 専用 `PROBABILITY` を使用しない。
- global full immutable TEST aggregation と local FIRST_N TEST instances は共に非空で、feature-order hash は instance provenance と一致する。
- tree-path-dependent background、provider `shap` / version、frozen additivity tolerances、preprocessor canonical hash、model/task identity、runtime versions を記録する。
- local `base_value + sum(contribution)` と raw regressor output を frozen tolerance で比較する。
- Result の method provenance と二つの JSON artifacts / Model Card provenance の equality を検証する。
- train input に TEST training bundle がないこと、および predictive-not-causal limitation を検証する。

## 非対象

LightGBM 以外への SHAP support は frozen matrix の範囲外であり、本 item は主張しない。unsupported model error は item 020、dependency absence は item 070、LIME reference contract は item 050/060 でそれぞれ独立に検証する。
