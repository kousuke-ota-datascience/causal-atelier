# 22_10_comparison


---

## 13. Comparison Design

### 13.1 Canonical comparison query

現行`ComparisonQueryService`は2件以上のcanonical Resultを比較し、以下を要求する。

- 全Resultが同一Projectに属する。
- 全Resultの親Executionが同一`operation`である。
- 全Resultが同一`result_type`である。

比較projectionは次を返す。

- `operation`
- `common_conditions`
- `changed_conditions`
- `result_differences`
- `warnings`
- `lineage_summary`

Execution snapshot差分として、少なくとも`algorithm_or_estimator / parameter_json / random_seed / analysis_spec_json / dataset_version_id / input_graph_version_id`を比較する。

### 13.1.1 Scientific comparability gate

Comparisonは二段階で評価する。

1. `semantic_compatible`
2. `direct_metric_comparable`

Predictive semantic key:

```text
task_type
prediction target/outcome
prediction unit
prediction time
horizon
deployment/evaluation population semantics
```

Model/feature/hyperparameter/split method差分は比較対象だがsemantic keyそのものではない。Direct metric comparisonではさらに`same dataset_version_id / same TEST-row identity(hash) / same metric definition`を要求する。

Causal semantic keyは`treatment/exposure / outcome / estimand / target population`。Direct comparisonではsame data/view/analysis populationも要求する。

同一immutable `dataset_version_id`をExploratoryとconfirmatory analysisで再利用した場合はAnalysisViewが異なってもsame-dataと判定し、`EXPLORATORY_REUSE_SAME_DATA`をnon-blocking warningとして先行Exploratory Result IDとともに保持する。

semantic mismatchはHTTP-level failureにせず`compatible=false`とreasonを返し、quantitative delta/rankを生成しない。Different Family / incompatible Result Typeなどrequest shape自体が無効な場合はvalidation errorとする。

### 13.2 Project-scoped comparison

Project Closure APIにも`POST /projects/{project_id}/comparisons`が存在する。これはProject membership境界を通った比較surfaceであり、canonical Result比較の意味を変えない。

### 13.3 Cross-family summaryの将来境界

現行canonical comparisonはsame operation / same Result Typeを要求するため、異なるFamily semanticを直接同一comparisonへ入れる設計ではない。

将来Cross-family summaryを行う場合も、Predictive metricとCausal effectを単一scoreへ平坦化せず、Research Context / Dataset / Analysis View / evidence relation等を用いたpresentation summaryとして設計する。
