# ENH-E10 G02 Trial 01 — 独立検証詳細実行報告（reverification 04）

## 実行 identity

- Fixed Trial Candidate: `e9a5b412349b10ced45d822aa08a54b6d9df00ba`
- Previous failed candidate: `d2d87e074338b06fc740252506ae1dba2b2a5c04`
- TEST_START_SHA: `0f5345bb87dfbbc4b677c153d12a2164d6ca99b5`
- Branch: `feature/ariadne_mvp_e10` / clean working tree
- Runtime: Python `3.12.3`; `uv run --extra predictive-advanced`; `MPLCONFIGDIR=/tmp/ariadne-mpl`

Candidate object / ancestry checks exited 0. Candidate semantic diff versus previous failed candidate contains 4 production and 4 test paths, 208 additions / 25 deletions. Candidate-to-tested-HEAD diff contains only remediation instruction and completion-report documentation; no post-candidate semantic product change was found.

## Independent automated regression command

```bash
MPLCONFIGDIR=/tmp/ariadne-mpl UV_CACHE_DIR=/tmp/ariadne-uv-cache \
uv run --extra predictive-advanced pytest -q \
 tests/product/test_enh_e10_g02_p01_explanation_capabilities.py \
 tests/product/test_enh_e10_g02_p02_shap_backend.py \
 tests/product/test_enh_e10_g02_p03_lime_backend.py \
 tests/product/test_predictive_training_e3.py \
 tests/product/test_predictive_evaluation_e3.py \
 tests/product/test_predictive_explanation_e3.py \
 tests/product/test_predictive_leakage_e3.py \
 tests/product/test_enh_e10_g01_p02_lightgbm_adapters.py \
 tests/product/test_enh_e10_g01_p03_model_artifacts.py \
 tests/product/test_predictive_api_worker_e2e_e3.py
```

```text
.........................................                                [100%]
41 passed, 1 warning in 13.90s
```

warning は SHAP provider の binary array-shape notification のみ。G01 p01 lightgbm lazy-import assertion は、SHAP が同 process に import された一括 command では test-order failure になるため、独立 process で再実行し `7 passed in 2.01s` を確認した。これは product failure ではなく test isolation の必要条件であり、dependency absence は item 070 の `python -S` runtime で別途検証した。

## SHAP actual EXPLAIN-stage probe（FAIL evidence）

binary `lightgbm_classifier.v1` + `SHAP_TREE` full DAG:

```text
outcome=SUCCEEDED
split=SUCCEEDED, prepare=SUCCEEDED, train=SUCCEEDED, evaluate=SUCCEEDED, explain=SUCCEEDED
explanation_status=NOT_APPLICABLE
method=SHAP_TREE
global=null
local=[]
warning=EXPLANATION_METHOD_NOT_APPLICABLE
method_provenance=null
model_card_provenance=null
```

regression `lightgbm_regressor.v1` + `SHAP_TREE` full DAG:

```text
outcome=SUCCEEDED
explanation_status=NOT_APPLICABLE
method=SHAP_TREE
global=null
local=[]
warning=EXPLANATION_METHOD_NOT_APPLICABLE
method_provenance=null
```

事実: DAG infrastructure は成功するが SHAP explanation output は生成されない。解釈: direct `explain_shap_tree` backend success は stage integration / result / artifact / Model Card successを証明しない。AC-03、AC-04、SHAP に関わる AC-09/10/11 は FAIL。

## LIME / provenance / reference observations

focused command `test_enh_e10_g02_p03_lime_backend.py tests/product/test_predictive_training_e3.py tests/product/test_predictive_api_worker_e2e_e3.py` は `10 passed in 12.61s`。LIME tests verify provider-valued binary probability / regression prediction contributions, one-hot categorical index configuration, deterministic TRAIN reference sampling without replacement / maximum 500, seed-dependent hash, no persisted raw reference rows, and equality of explanation result / artifact / Model Card provenance.

isolated dependency absence runtime:

```text
SHAP_TREE availability=False; error=EXPLANATION_DEPENDENCY_UNAVAILABLE
LIME_TABULAR availability=False; error=EXPLANATION_DEPENDENCY_UNAVAILABLE
exit code: 0
```

## Decision

candidate identity and LIME/G01 remediation are verified, but actual SHAP execution integration is absent. PASS requires all MUST criteria; therefore Gate Decision is **FAIL** and promotion remains prohibited.
