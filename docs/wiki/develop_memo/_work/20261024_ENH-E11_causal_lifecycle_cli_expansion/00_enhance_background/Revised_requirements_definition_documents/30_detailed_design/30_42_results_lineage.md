# 30_42_results_lineage


---

## 16. Result Type / Scientific Status

### 16.1 Result Type

Exploratory:

```text
DATA_PROFILE_RESULT
DISTRIBUTION_RESULT
ASSOCIATION_RESULT
GROUP_SUMMARY_RESULT
CHART_RESULT
```

Predictive:

```text
SPLIT_RESULT
TRAINING_RESULT
EVALUATION_RESULT
ERROR_ANALYSIS_RESULT
PREDICTIVE_EXPLANATION_RESULT
MODEL_CARD_RESULT
```

Causal:

```text
DISCOVERY_GRAPH_RESULT
IDENTIFICATION_RESULT
DATA_ELIGIBILITY_RESULT
TREATMENT_EFFECT_RESULT
DIAGNOSTICS_RESULT
REFUTATION_RESULT
SENSITIVITY_RESULT
```

Navigation Stage名をResult Typeへ自動変換しない。

### 16.2 Scientific status

status vocabularyはresult type/schemaに応じて意味を保持する。例:

```text
GENERATED
GENERATED_WITH_WARNINGS
UNRELIABLE
IDENTIFIED
NOT_IDENTIFIED
PARTIALLY_IDENTIFIED
REQUIRES_REVIEW
PASS
WARN
FAIL
ESTIMATED
INSUFFICIENT_OVERLAP
INSUFFICIENT_SAMPLE
ESTIMATION_UNRELIABLE
NO_FAILURE_DETECTED
FAILURE_DETECTED
INCONCLUSIVE
ROBUST
FRAGILE
TRAINED
TRAINED_WITH_WARNINGS
EVALUATED
INSUFFICIENT_TEST_SAMPLE
NOT_APPLICABLE
```

Family-specific statusをgeneric success/failureへ平坦化しない。

---

## 17. Comparison / Lineage

### 17.1 Result comparison

comparisonは二段階gateとする。

```text
same Family / same Result Type
        ↓
semantic_compatible
        ↓
direct_metric_comparable
```

異なるFamilyまたはResult Typeをgeneric direct comparisonへ投入しない。同一Family/Result Typeでもsemantic key不一致ならrequest自体を失敗させず、`semantic_compatible=false / direct_metric_comparable=false / reasons[]`を返しquantitative delta/rankを生成しない。

Predictive semantic keyにはtask type、prediction target/outcome、prediction unit、prediction time、horizon、population semanticsを含む。direct metric comparisonには同一Dataset Version、同一TEST-row identity/hash、同一metric definitionを要求する。

Causal semantic keyにはtreatment/exposure、outcome、estimand、target populationを含む。direct quantitative comparisonには同じdataset/view/analysis populationを要求する。

「画面上に並べられる」と「scientifically direct-comparable」を同一視しない。

### 17.2 Cross-family comparison

Exploratory statistic、Predictive metric、Causal effectは同じ数値fieldへflattenしない。

cross-family surfaceでは、共通metadata/lineageとFamily-specific payloadを分離して表示する。

### 17.3 Lineage

lineageはProject境界を越えない。

代表的typed structural relation:

```text
Execution --GENERATED--> Result
Result --GENERATED--> Artifact
DatasetVersion --USED_INPUT--> Execution
AnalysisView --USED_INPUT--> Execution
Result --USED_INPUT--> Execution
Result --DERIVED_FROM--> GraphVersion
Artifact --DERIVED_FROM--> DatasetVersion
Execution --DERIVED_FROM--> Execution
Execution --REVISED_FROM--> Execution
```

Generic relationには`Artifact --DERIVED_FROM--> Artifact`、`Result --SUMMARIZES--> Result/Artifact`、`Result --MOTIVATED--> Execution/AnalysisSpecification`等を許可し得る。unknown tupleはclosed-by-defaultでrejectし、typed structural tupleをgeneric LineageEdgeとして二重writeしない。

Navigation Stageをpersistent Lineage node/edgeへ追加しない。どのStageからResultを表示するかはFamily / Result Type / presentation bindingからderiveする。

---
