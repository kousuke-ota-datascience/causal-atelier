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

## 分離 process を用いた理由

G01 P01 の `lightgbm` lazy-import assertion は、SHAP test が同一 pytest process で LightGBM を import した後に実行すると test-order-dependent に失敗し得る。これは product behavior ではなく当該 test の import-isolation contractである。したがって P01 を provider import 前の独立 process として 7/7 PASS と確認し、他の G01 regression を G02 suite で確認した。test-order failure を product PASS/FAIL へ恣意的に読み替えていない。

## protected contract coverage

| protected behavior | verification evidence |
| --- | --- |
| no explanation request | empty `explanation_spec` で sampling binding を作らず DAG succeeds |
| original regression | prior `KeyError('sampling')` が再現しない |
| registry / optional model capability | P01 isolated suite `7 passed` |
| LightGBM adapter | G01 P02 tests in complete suite |
| artifact persistence | G01 P03 save/load/predict tests in complete suite |
| deterministic / leakage boundary | predictive training + leakage tests in complete suite |
| data isolation | TEST explanation が training selection を変更しない assertions |

## 限界

本 item は G01 frozen contract の protected regression であり、G02 explanation semantic correctnessの代用にはならない。SHAP/LIME method-specific conditions は item 030–080 の証跡によって別に PASS している。
