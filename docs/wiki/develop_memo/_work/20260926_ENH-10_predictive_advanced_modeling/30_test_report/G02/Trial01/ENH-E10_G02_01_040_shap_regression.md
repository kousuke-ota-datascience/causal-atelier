# G02 Trial 01 — 040 shap_regression

AC-04/09/10/11. Independent fixed synthetic regression probe trained `lightgbm_regressor.v1` with seed 3, invoked `explain_shap_tree`, and observed:

```text
{"method":"SHAP_TREE","output_scale":"PREDICTION","background":{"kind":"TREE_PATH_DEPENDENT"},"global_features":["x","group"],"local_rows":[0,1],"additivity_residuals":[1.0658141036401503e-14,1.0658141036401503e-14]}
exit code: 0
```

Residuals are within the frozen tolerance. Target/candidate identities are as in item 001.

Result: **PASS** for the SHAP adapter contract; see item 080 for missing result/artifact integration.
