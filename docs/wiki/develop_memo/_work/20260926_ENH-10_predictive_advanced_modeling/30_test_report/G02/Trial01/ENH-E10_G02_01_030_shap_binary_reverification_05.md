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

## fixture と実行経路

full-DAG test は deterministic synthetic frame（`score=-60..59`、target は `score >= 0`）を使い、`preprocessing_spec` を TRAIN fit / numeric mean / scaled / one-hot、model を `lightgbm_classifier.v1`（`num_boost_round=8`, `min_data_in_leaf=4`）に固定する。explanation request は `SHAP_TREE`、dataset `TEST`、`FIRST_N,size=3,seed=17`、local enabled である。

従って検証経路は provider function を直接呼ぶだけではなく、planner が作る SPLIT → PREPARE → TRAIN → EVALUATE → EXPLAIN と result/artifact emission を経由する。前回 04 の failure はまさにこの stage dispatch にあったため、同じ境界を今回の PASS 根拠にしている。

## assertion の具体化

| 対象 | 実行時 assertion |
| --- | --- |
| stage outcome | 5 stage の key と status が全て期待値、overall `SUCCEEDED` |
| canonical output | `GENERATED`、global/local とも non-empty、feature `score`、TEST row ordinal 一致 |
| binary numeric meaning | model output `LOG_ODDS`、prediction `PROBABILITY` |
| additivity | base + local feature contribution 合計と raw model output を `atol=1e-6, rtol=1e-5` で比較 |
| provenance | SHAP method/provider、tree-path background、sampling、feature/preprocessor/model/TEST identity、runtime versions |
| persistence | Result、Explanation Artifact、Model Card の provenance を JSON equality で比較 |
| isolation / wording | train input に TEST bundle なし、predictive-not-causal limitation あり |

## 警告の判断

binary provider warning は SHAP の ndarray shape notification である。test は `np.asarray` 正規化後の contribution と上記 additivity / provenance assertions を通過しており、frozen result semantics の失敗を示さない。warning を PASS 根拠から除外しても、全 MUST assertion は成功している。
