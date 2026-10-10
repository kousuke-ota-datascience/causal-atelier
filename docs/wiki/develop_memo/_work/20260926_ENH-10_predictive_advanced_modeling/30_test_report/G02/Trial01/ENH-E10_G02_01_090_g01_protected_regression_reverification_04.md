# ENH-E10 G02 Trial 01 — Test Item 090: G01 Protected Regression（reverification 04）

AC-12。以下 command を independent process で実行した。

```bash
MPLCONFIGDIR=/tmp/ariadne-mpl UV_CACHE_DIR=/tmp/ariadne-uv-cache \
uv run --extra predictive-advanced pytest -q \
  tests/product/test_predictive_training_e3.py \
  tests/product/test_enh_e10_g01_p02_lightgbm_adapters.py \
  tests/product/test_enh_e10_g01_p03_model_artifacts.py \
  tests/product/test_predictive_leakage_e3.py
```

G01 p01 optional dependency test は SHAP process import-order interactionを避けて別 process で `7 passed`。残りの command は 41-test independent suite 内で PASS。baseline empty `explanation_spec` flow は PREPARE sampling binding を作らず、full DAG は success、deterministic artifacts/load/predict と TRAIN/TEST isolation assertion は通過した。

従って prior `KeyError: 'sampling'` regression は candidate で再現しない。**PASS**。
