# ENH-E10 G02 Trial 01 — Test Item 050: LIME Binary Local（reverification 05）

| Fixed Candidate | Tested SHA | AC | 判定 |
| --- | --- | --- | --- |
| `fbd97c5b7a95084affe5e2381d85d86d0dfa2558` | `1bf3026ba1918c8ca74af64318bdd42e90d7ed67` | AC-05, AC-09, AC-10, AC-11 | **PASS** |

## 実行

```bash
MPLCONFIGDIR=/tmp/ariadne-mpl UV_CACHE_DIR=/tmp/ariadne-uv-cache \
uv run --extra predictive-advanced pytest -q \
 tests/product/test_enh_e10_g02_p03_lime_backend.py \
 tests/product/test_predictive_training_e3.py \
 tests/product/test_predictive_api_worker_e2e_e3.py
```

Python `3.12.3`、LIME `0.2.0.1`、LightGBM `4.7.0`。raw output は broader independent suite の `43 passed, 2 warnings in 18.97s`、exit `0`（LIME failure なし）。

## 観測事実

- binary local explanation は positive-class `PROBABILITY` scale、非空の signed contributions、preprocessed feature representation、TEST row identity を生成した。
- transformed one-hot `group=A` は actual provider configuration で categorical binary feature として `categorical_feature_indices=[1]` に渡った。
- `predictive-explanation-reference/1` は transformed TRAIN 由来で、partition、count、hash、sampling seed を provenance に記録する。raw TRAIN rows は artifact / model card に永続化されない。
- local row ごとの deterministic effective seed、2000 samples、feature 数に基づく num_features、euclidean distance、kernel width、continuous non-discretization / sample-around-instance false、provider/runtime versions を記録した。predictive-not-causal limitation を保持する。

## 解釈

frozen LIME binary local semantics、one-hot categorical configuration、reference / instance / parameter provenance、TEST isolation を実行時に満たす。AC-05 と関連 AC-09/10/11 は **PASS**。
