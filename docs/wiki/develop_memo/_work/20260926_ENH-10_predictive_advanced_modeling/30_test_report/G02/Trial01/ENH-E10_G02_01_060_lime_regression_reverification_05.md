# ENH-E10 G02 Trial 01 — Test Item 060: LIME Regression Local（reverification 05）

| Fixed Candidate | Tested SHA | AC | 判定 |
| --- | --- | --- | --- |
| `fbd97c5b7a95084affe5e2381d85d86d0dfa2558` | `1bf3026ba1918c8ca74af64318bdd42e90d7ed67` | AC-06, AC-09, AC-10, AC-11 | **PASS** |

## 実行と raw output

```bash
MPLCONFIGDIR=/tmp/ariadne-mpl UV_CACHE_DIR=/tmp/ariadne-uv-cache \
uv run --extra predictive-advanced pytest -q \
 tests/product/test_enh_e10_g02_p03_lime_backend.py \
 tests/product/test_predictive_training_e3.py \
 tests/product/test_predictive_api_worker_e2e_e3.py
```

runtime は Python `3.12.3`、LIME `0.2.0.1`、LightGBM `4.7.0`。該当 test を含む独立 suite raw output は `43 passed, 2 warnings in 18.97s`、exit `0`。

## 観測事実

- regression provider の local explanation は `PREDICTION` scale と non-empty contributions を生成した。
- reference は `predictive-explanation-reference/1` / `TRAIN`。deterministic without-replacement sampling は最大 500 row、同一 seed は同 hash、seed `19` は異なる hash となることを確認した。
- TEST local instance identity、reference hash/count/partition/seed、effective per-row seed、frozen LIME parameters、provider/runtime versions を Result / Artifact / Model Card で監査可能にした。
- training selection は TRAIN/VALIDATION に限定され、explanation は immutable TEST を使い、predictive-not-causal limitation を保持する。

## 解釈

回帰 LIME local output とその provenance / isolation contract は実行時に満たされた。AC-06 と関連 AC-09/10/11 は **PASS**。

## 検証設計

regression case は binary LIME と provider class / prediction semantics を区別して実行する。PASS 条件は単に local list が生成されることではなく、regression `PREDICTION` scale、TEST instance identity、TRAIN reference identity、effective seeds、frozen parameters、artifact/model-card persistence が同時に成立することである。

## assertion の内訳

| contract element | 観測した runtime assertion |
| --- | --- |
| local value | non-empty signed feature contributions と `PREDICTION` output scale |
| TEST identity | local row ordinal と feature-order hash を Result provenance に記録 |
| TRAIN reference | schema `predictive-explanation-reference/1`、partition `TRAIN`、count/hash/seed を記録 |
| bounded sampling | `min(500, TRAIN row count)`、without replacement。同一 seed は同 hash、seed `19` は異 hash |
| method parameters | 2000 samples、`min(10,n_features)`、euclidean、kernel width、discretize false、sample-around false |
| durable consistency | Result、PREDICTIVE_EXPLANATION artifact、MODEL_CARD_RESULT、MODEL_CARD artifact の provenance を比較 |
| isolation | training selection に explanation TEST rows を混入させない |

## 実行範囲と非対象

実行 command と raw output は item 050 に全文記録した 43-test command と同一であり、exit `0`。LIME の global behavior はこの local regression test で推測せず item 020 で explicit reject を確認する。SHAP tree-path background は LIME に適用しないため item 030/040 の対象である。
