# G02 Trial 01 — 020 compatibility_registry

AC-02/07. Command: `MPLCONFIGDIR=/tmp/ariadne-mpl UV_CACHE_DIR=/tmp/ariadne-uv-cache uv run --extra predictive-advanced pytest -q tests/product/test_enh_e10_g02_p01_explanation_capabilities.py`; included in the independent G02 suite: `11 passed, 1 warning`, exit 0. Observed asserted boundaries: unknown method → `EXPLANATION_METHOD_NOT_REGISTERED`; SHAP on linear → `EXPLANATION_METHOD_NOT_APPLICABLE`; global LIME → `EXPLANATION_SCOPE_NOT_SUPPORTED`, with no fallback.

Target/candidate identities are as in item 001. Result: **PASS**.
