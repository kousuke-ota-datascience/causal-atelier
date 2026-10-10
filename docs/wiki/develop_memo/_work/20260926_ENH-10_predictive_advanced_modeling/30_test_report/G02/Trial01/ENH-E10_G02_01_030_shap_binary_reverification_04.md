# ENH-E10 G02 Trial 01 — Test Item 030: SHAP Binary（reverification 04）

AC-03 / AC-09 / AC-10 / AC-11。direct backend test は fixed LightGBM binary fixture で raw `LOG_ODDS`、tree-path-dependent reference、named global values、local rows、frozen additivity toleranceを通過した。

しかし acceptance は backend unit success だけでは満たされない。actual EXPLAIN stage の binary `lightgbm_classifier.v1` + `SHAP_TREE` probe は DAG 自体は `SUCCEEDED` したが、出力は以下だった。

```text
explanation_status=NOT_APPLICABLE
global=null
local=[]
warning=EXPLANATION_METHOD_NOT_APPLICABLE
method_provenance=null
model_card_provenance=null
```

従って binary SHAP canonical output / provenance は product integration で生成されない。**FAIL**。
