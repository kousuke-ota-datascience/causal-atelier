# G02 Trial 01 — 010 coefficient_protected_regression

AC-01/11. Command: `MPLCONFIGDIR=/tmp/ariadne-mpl UV_CACHE_DIR=/tmp/ariadne-uv-cache uv run --extra predictive-advanced pytest -q tests/product/test_predictive_explanation_e3.py` (included in the G02 suite below). Observed: suite total `11 passed, 1 warning in 15.73s`, exit 0. Existing assertions retain linear coefficient global/local behavior, LOG_ODDS coefficient / PROBABILITY prediction scales, feature order, and `predictive_not_causal` terminology.

Target: `b5fa47c8e3e299445a3efd4ef791242fc040ea50`; candidate: `67f1c4ef1281700a14b5a9acd0eacf00b5c904e0`.

Result: **PASS**.
