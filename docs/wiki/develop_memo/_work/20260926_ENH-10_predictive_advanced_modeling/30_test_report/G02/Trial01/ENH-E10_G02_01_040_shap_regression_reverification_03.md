# G02 Trial 01 — 040 shap_regression (reverification 03)

## Scope / command

AC-04. A fixed synthetic 60-row LightGBM regression fixture (seed 3, two features `x`/`group`, `num_boost_round=8`, `min_data_in_leaf=4`) invoked `explain_shap_tree` with local size 2.

## Raw observation

```text
method=SHAP_TREE; output_scale=PREDICTION; background=TREE_PATH_DEPENDENT;
global_features=[x, group]; local_rows=[0, 1];
additivity residuals=[1.0658141036401503e-14, 1.0658141036401503e-14]
exit code: 0
```

Exit code was 0. Residuals are within frozen `atol=1e-6, rtol=1e-5`; the largest is approximately `1.1e-14`.

**Interpretation:** regression SHAP produces raw PREDICTION-scale values, mapped features, TEST-row identity, and tree-path-dependent reference semantics. Target/candidate identities are in item 001. **Result: PASS.**

## 判定境界・再現条件

PASS 条件は、regression task で `PREDICTION` scale を返し、feature mapping と row identity を維持し、base value + contributions が model output と frozen tolerance 内で一致することである。単に `shap_values` が返ることは PASS 条件ではない。

再現は本 report の fixture 条件で `explain_shap_tree` を呼び、local row 0/1 の residual を算出する。`1.0658e-14` は `1e-6` より小さく、runtime numeric evidence として additivity を支持する。Fixed Candidate / tested state は item 001 の audit を使用する。
