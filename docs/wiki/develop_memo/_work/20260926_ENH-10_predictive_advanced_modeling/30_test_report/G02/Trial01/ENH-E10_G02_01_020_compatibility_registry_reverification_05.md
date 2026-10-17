# ENH-E10 G02 Trial 01 — Test Item 020: Compatibility Registry（reverification 05）

| Fixed Candidate | Tested SHA | AC | 判定 |
| --- | --- | --- | --- |
| `fbd97c5b7a95084affe5e2381d85d86d0dfa2558` | `1bf3026ba1918c8ca74af64318bdd42e90d7ed67` | AC-02, AC-07 | **PASS** |

## 実行

```bash
MPLCONFIGDIR=/tmp/ariadne-mpl UV_CACHE_DIR=/tmp/ariadne-uv-cache \
uv run --extra predictive-advanced pytest -q \
 tests/product/test_enh_e10_g02_p01_explanation_capabilities.py
```

同 test を含む独立 suite の raw output は `43 passed, 2 warnings in 18.97s`、exit `0`。runtime は Python `3.12.3`、SHAP `0.52.0`、LIME `0.2.0.1`、LightGBM `4.7.0`。

## 観測事実

| 入力 | contract 結果 |
| --- | --- |
| unknown explanation method | `EXPLANATION_METHOD_NOT_REGISTERED` |
| `SHAP_TREE` + linear model | `EXPLANATION_METHOD_NOT_APPLICABLE` |
| `LIME_TABULAR` + `GLOBAL` | `EXPLANATION_SCOPE_NOT_SUPPORTED` |
| LightGBM + `SHAP_TREE` | GLOBAL / LOCAL available |
| linear / LightGBM + `LIME_TABULAR` | LOCAL only available |

## 解釈

capability registry は model × method × scope を明示的に解決する。unsupported 要求には fallback や pseudo-global 値を生成せず、frozen compatibility matrix と AC-02 / AC-07 を満たす。**PASS**。

## 検証境界

frozen matrix は、linear model では coefficient + LIME local、LightGBM では SHAP global/local + LIME local を許可する。ここでの PASS 条件は「unsupported request が何らかの値を返す」ことではなく、登録なし・model incompatibility・scope incompatibility を区別した explicit error が返り、既存 method に silently fallback しないことである。

## 実行証跡

P01 assertions は次の complete command の 43 tests に含まれる。

```bash
MPLCONFIGDIR=/tmp/ariadne-mpl UV_CACHE_DIR=/tmp/ariadne-uv-cache \
uv run --extra predictive-advanced pytest -q \
 tests/product/test_enh_e10_g02_p01_explanation_capabilities.py \
 tests/product/test_enh_e10_g02_p02_shap_backend.py \
 tests/product/test_enh_e10_g02_p03_lime_backend.py \
 tests/product/test_predictive_training_e3.py tests/product/test_predictive_evaluation_e3.py \
 tests/product/test_predictive_explanation_e3.py tests/product/test_predictive_leakage_e3.py \
 tests/product/test_enh_e10_g01_p02_lightgbm_adapters.py \
 tests/product/test_enh_e10_g01_p03_model_artifacts.py tests/product/test_predictive_api_worker_e2e_e3.py
```

```text
...........................................                              [100%]
43 passed, 2 warnings in 18.97s
```

## 判定の限定

availability は current runtime で SHAP `0.52.0` / LIME `0.2.0.1` が存在する状態の matrix 判定である。provider absence 時の availability/error behavior は別 isolation runtime で item 070 が検証する。本 item は provider output の数値内容を判定しない。
