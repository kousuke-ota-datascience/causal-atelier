# ENH-E10 G02 Trial 01 — Test Item 090: G01 Protected Regression（reverification 05）

| Fixed Candidate | Tested SHA | AC | 判定 |
| --- | --- | --- | --- |
| `fbd97c5b7a95084affe5e2381d85d86d0dfa2558` | `1bf3026ba1918c8ca74af64318bdd42e90d7ed67` | AC-12 | **PASS** |

## 実行と raw output

G01 P01 は lazy-import assertion を保つため SHAP import 前の別 process で実行した。

```bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache uv run --extra predictive-advanced pytest -q \
 tests/product/test_enh_e10_g01_p01_model_capability.py
```

```text
....... [100%]
7 passed in 2.18s
```

以下は G02 independent suite に含めて実行した。

```bash
MPLCONFIGDIR=/tmp/ariadne-mpl UV_CACHE_DIR=/tmp/ariadne-uv-cache \
uv run --extra predictive-advanced pytest -q \
 tests/product/test_predictive_training_e3.py \
 tests/product/test_enh_e10_g01_p02_lightgbm_adapters.py \
 tests/product/test_enh_e10_g01_p03_model_artifacts.py \
 tests/product/test_predictive_leakage_e3.py
```

complete suite raw output: `43 passed, 2 warnings in 18.97s`、exit `0`。runtime は Python `3.12.3`、LightGBM `4.7.0`。

## 観測事実と解釈

empty `explanation_spec` の baseline G01 flow は `sampling` binding を要求せず、full DAG が成功した。previous `KeyError('sampling')` は再現しない。deterministic model behavior、artifact save/load/predict compatibility、model registry、TRAIN/TEST isolation assertions も成功した。よって SHAP/LIME integration は G01 artifact/load/predict contract を破壊せず、AC-12 は **PASS**。
