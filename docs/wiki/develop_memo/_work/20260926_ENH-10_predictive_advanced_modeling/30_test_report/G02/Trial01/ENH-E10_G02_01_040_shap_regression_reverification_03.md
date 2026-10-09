# G02 Trial 01 — 040 shap_regression (reverification 03)

AC-04: **PASS.** Fixed synthetic LightGBM regression probe observed:

```text
method=SHAP_TREE; output_scale=PREDICTION; background=TREE_PATH_DEPENDENT;
global_features=[x, group]; local_rows=[0, 1];
additivity residuals=[1.0658141036401503e-14, 1.0658141036401503e-14]
exit code: 0
```

Residuals are within frozen `atol=1e-6, rtol=1e-5`. Target/candidate identities are in item 001.
