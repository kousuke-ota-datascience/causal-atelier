# ENH-E10 G02 Trial 01 — Test Item 030: SHAP Binary（reverification 05）

| Fixed Candidate | Tested SHA | AC | 判定 |
| --- | --- | --- | --- |
| `fbd97c5b7a95084affe5e2381d85d86d0dfa2558` | `1bf3026ba1918c8ca74af64318bdd42e90d7ed67` | AC-03, AC-09, AC-10, AC-11 | **PASS** |

## 実行環境と再現コマンド

Python `3.12.3`、LightGBM `4.7.0`、SHAP `0.52.0`、NumPy `2.2.6`。backend 単体値ではなく、`lightgbm_classifier.v1 + SHAP_TREE` の actual SPLIT/PREPARE/TRAIN/EVALUATE/EXPLAIN DAG を実行する test を含めた。

```bash
MPLCONFIGDIR=/tmp/ariadne-mpl UV_CACHE_DIR=/tmp/ariadne-uv-cache \
uv run --extra predictive-advanced pytest -q \
 tests/product/test_enh_e10_g02_p02_shap_backend.py
```

```text
... [100%]
3 passed, 2 warnings in 10.97s
```

加えて全 frozen regression suite は `43 passed, 2 warnings in 18.97s`、exit `0`。2 warning は `shap` の LightGBM binary array-shape notification で、計算値・DAG status の failure ではない。

## 観測事実

- full DAG の stage key は `split, prepare, train, evaluate, explain`、全 stage `SUCCEEDED`、explanation analytical status は `GENERATED`。
- global explanation と 3 件の local explanation は非空。feature は transformed `score`、local の TEST `row_ordinal` は provenance `test_instances` と一致した。
- model output scale は raw `LOG_ODDS`、prediction output scale は `PROBABILITY`。各 local row で `base_value + Σ contribution == model_output` を frozen `atol=1e-6, rtol=1e-5` で満たした。
- background は `TREE_PATH_DEPENDENT` / `TREE_TRAINING_PATH_COUNTS`、global TEST sample count は 24、sampling は `FIRST_N,size=3,seed=17`。SHAP は TRAIN reference を fabricating していない。
- `method_id=SHAP_TREE`、version、provider `shap` / version、model/task/preprocessor hash、feature order/hash、TEST identities、parameters、runtime versions、predictive-not-causal limitation は Result に存在し、Explanation Artifact と Model Card の provenance は Result と等値だった。
- train binding に TEST training bundle は含まれない。

## 解釈

これは direct backend 成功だけではなく actual EXPLAIN stage の runtime evidence である。binary SHAP global/local、raw scale、tree-path semantics、additivity、provenance と TRAIN/TEST isolation を満たすため AC-03、および当該 AC-09/10/11 は **PASS**。
