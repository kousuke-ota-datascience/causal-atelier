# ENH-E10 G02 Trial 01 — Test Item 040: SHAP Regression（reverification 04）

AC-04 / AC-09 / AC-10 / AC-11。direct regression backend fixture は raw `PREDICTION` scale、tree-path-dependent reference、global/local mapping、frozen additivity toleranceを通過している。

actual EXPLAIN stage では `lightgbm_regressor.v1` + `SHAP_TREE` full DAG は `SUCCEEDED` するが、result は `NOT_APPLICABLE`、`global=null`、`local=[]`、`EXPLANATION_METHOD_NOT_APPLICABLE`、`method_provenance=null` となった。

backend wrapper と stage integration の間に contract gap があり、regression SHAP canonical representation / provenance は user-visible result/artifact/Model Card に到達しない。**FAIL**。
