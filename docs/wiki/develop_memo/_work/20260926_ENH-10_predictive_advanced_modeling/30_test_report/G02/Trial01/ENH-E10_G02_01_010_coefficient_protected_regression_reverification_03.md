# G02 Trial 01 — 010 coefficient_protected_regression (reverification 03)

AC-01/11: **PASS.** The independent G02 suite below completed `13 passed, 1 warning`, exit 0. It includes `test_predictive_explanation_e3.py`, preserving coefficient global/local semantics and predictive-not-causal terminology.

Command: `MPLCONFIGDIR=/tmp/ariadne-mpl UV_CACHE_DIR=/tmp/ariadne-uv-cache uv run --extra predictive-advanced pytest -q tests/product/test_enh_e10_g02_p01_explanation_capabilities.py tests/product/test_enh_e10_g02_p02_shap_backend.py tests/product/test_enh_e10_g02_p03_lime_backend.py tests/product/test_predictive_explanation_e3.py`.

Target/candidate: `7de36e443e193fd0fdf1ba6ce00b71f8ba0551eb` / `d2d87e074338b06fc740252506ae1dba2b2a5c04`.
