# ENH-E10 G02 Trial 01 — Test Item 020: Compatibility Registry（reverification 04）

AC-02 / AC-07。command は item 010 の independent suite。対象 test は `test_enh_e10_g02_p01_explanation_capabilities.py`。

観測された明示 error taxonomy:

| 入力 | 観測 code |
| --- | --- |
| unknown method | `EXPLANATION_METHOD_NOT_REGISTERED` |
| `SHAP_TREE` + linear model | `EXPLANATION_METHOD_NOT_APPLICABLE` |
| `LIME_TABULAR` + `GLOBAL` | `EXPLANATION_SCOPE_NOT_SUPPORTED` |

global LIME は pseudo-global output / silent fallback を生成せず、model-method compatibility は明示的に解決される。suite exit 0。**PASS**。
