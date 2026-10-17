# G02 Trial 01 — 010 coefficient_protected_regression (reverification 03)

## Scope

AC-01 / AC-11: compatible linear coefficient explanation, feature-order/scale protection, and predictive-not-causal terminology.

Command: `MPLCONFIGDIR=/tmp/ariadne-mpl UV_CACHE_DIR=/tmp/ariadne-uv-cache uv run --extra predictive-advanced pytest -q tests/product/test_enh_e10_g02_p01_explanation_capabilities.py tests/product/test_enh_e10_g02_p02_shap_backend.py tests/product/test_enh_e10_g02_p03_lime_backend.py tests/product/test_predictive_explanation_e3.py`.

## Raw result

```text
.............  [100%]
13 passed, 1 warning in 14.24s
exit code: 0
```

The included baseline explanation assertions verify coefficient global/local output, binary LOG_ODDS model scale with PROBABILITY prediction output, preserved feature order, TEST-only explanation dataset, and the `predictive_not_causal` diagnostic/limitation.

Target/candidate: `7de36e443e193fd0fdf1ba6ce00b71f8ba0551eb` / `d2d87e074338b06fc740252506ae1dba2b2a5c04`.

**Facts:** automated assertions passed. **Interpretation:** AC-01/AC-11 coefficient boundary is preserved. **Result: PASS.**

## 実行 identity・再現条件

- Fixed Trial Candidate: `d2d87e074338b06fc740252506ae1dba2b2a5c04`
- Tested semantic state: `7de36e443e193fd0fdf1ba6ce00b71f8ba0551eb`（001 audit により documentation-only post-candidate diff と確認済み）
- 依存環境: `uv run --extra predictive-advanced`、`MPLCONFIGDIR=/tmp/ariadne-mpl`、Python `3.12.3`

本 item は既存 coefficient explanation の backward compatibility を確認する。LIME/SHAP の provider 成功を coefficient behavior の PASS 根拠として扱っていない。上記 command を repository root で実行し、`test_predictive_explanation_e3.py` を含む 13-test suite が exit `0` となることを再現条件とする。

制約: Model Card の method-specific provenance はこの item の対象外であり、item 080 で独立判定した。
