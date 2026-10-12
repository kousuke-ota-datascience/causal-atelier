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
