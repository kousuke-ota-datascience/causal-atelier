<!-- ENH-E11 split working copy: not a formal approval. -->
# 22 — validation results

**Status:** `STRUCTURAL_COPY_DRAFT` (existing baseline text, not E11 canonical publication)

**Source:** [22_product_basic_design.md](https://github.com/kousuke-ota-datascience/causal-atelier/blob/3ba5fe2465ec591f0da7f998c21a5241984b73dc/docs/wiki/requirement_definition/22_product_basic_design.md) · blob `87196f2f03a7f3367724bc05fb254d1a4d98109e`  
**Index:** [Revised document inventory](../README_00_Revised_requirements_definition_documents.md)

---

## 11. Validation Architecture

### 11.1 Generic Validation

Validation責務は、現行実装の`PlanValidator`が直接行う検証と、それ以外のapplication/domain validationを分離する。

#### 11.1.1 PlanValidatorが行う検証

`PlanValidator`は現在、次を検証する。

1. `plan_schema_version == execution-plan/1`。
2. `project_id`と`analysis_specification_id`が空でない。
3. `stage_key`が一意で、Planに少なくとも1 Stageが存在する。
4. enabled Stageの`StageType`にRunnerが登録済みである。
5. `resource_policy.timeout_seconds`が指定される場合、整数かつ1..86400以内である。
6. dependencyのsource/target Stageが存在する。
7. enabled Stageがdisabled Stageへ依存しない。
8. dependencyが参照するsource output / target input名が各contractに存在する。
9. source output schemaとtarget input schemaが一致する。
10. 同じtarget Stage inputへ複数upstream bindingを作らない。
11. topological sortが成立し、cycleがない。

`StageType.namespace/name/version`のsyntax validationは`StageType`生成時のdomain invariantであり、PlanValidatorの独立stepとして重複実装しない。

#### 11.1.2 PlanValidator外のvalidation

次は別のdomain/application boundaryで扱う。

- Project / Resource boundary・ownership
- Analysis Specification schema/lifecycle validation
- Family固有scientific validation
- supported endpointにおけるidempotency
- Dataset/Artifact size等、個別use caseのresource policy
- Navigation catalogのFamily/Stage ID、slug、order、default Stage、renderer binding整合性

Navigation catalog validationをruntime Plan dependency validationへ混入しない。

#### 11.1.3 AnalysisView typed filter validation

AnalysisView create/update/validate/fixは同じDataset logical-type compatibility validatorを利用する。

| Logical Type | Operator |
| --- | --- |
| BOOLEAN | `EQ, NE, IN, NOT_IN, IS_NULL, NOT_NULL` |
| INTEGER / REAL / DATETIME | `EQ, NE, LT, LTE, GT, GTE, IN, NOT_IN, IS_NULL, NOT_NULL` |
| TEXT | `EQ, NE, IN, NOT_IN, IS_NULL, NOT_NULL` |
| OTHER | `IS_NULL, NOT_NULL` |

`IS_NULL/NOT_NULL`はvalueなし、`IN/NOT_IN`はnon-empty list。DATETIME valueはISO-8601、REALはfinite numeric、INTEGERはbooleanを許容しない。`time_cutoff`はDATETIME + `LT/LTE`。logical type unknownをsuccess扱いしない。Mismatch codeは`FILTER_TYPE_MISMATCH`。

### 11.2 Exploratory Validation

- column typeとchart encoding
- aggregation compatibility
- empty population
- sampling disclosure
- exploratory findingをcausal claimへ変換しない

### 11.3 Causal Validation

- Graph semantics
- Causal Question completeness
- identification strategy
- adjustment set
- inferred type
- eligibility
- estimator compatibility
- post-discovery warning

### 11.4 Predictive Validation

- target existence / type
- feature availability
- target / future / group leakage
- split overlap
- preprocessing fit boundary
- metric / task compatibility
- test isolation
- existing setting/spec parity

### 11.5 Navigation Validation

- supported Familyのみ。
- Stage ID / slugはFamily内一意。
- default Stageはcatalog内に存在する。
- Family / Stage orderingはdeterministic。
- renderer binding欠落を検出する。
- Navigation descriptorにruntime input/output、status、retry semanticsを持たせない。


## 12. Result / Artifact / Lineage

### 12.1 Canonical Resultとcompatibility read model

現行のcanonical `Result` authorityは、`execution_id / result_level / stage_execution_id / result_type / scientific_status / summary / payload / diagnostics / warnings`を持つ。ProjectとAnalysis Familyは親Executionから解決する。

同時に、過去のFamily workflowを読むための`FamilyResult` compatibility read modelが残っており、こちらは`project_id / analysis_family / schema_version / analytical_status`を持つ。新規write authorityはcanonical Resultに寄せ、両者を同一entityとして扱わない。

Navigation StageをResult ownership keyとして必須化しない。

### 12.2 Artifact

Canonical Artifactは`SOURCE`または`EXECUTION_OUTPUT` scopeを持ち、`object_key / content_hash / media_type / size_bytes`でArtifactStore上のcontentを参照する。Artifact readでは保存済み`content_hash`と取得contentのSHA-256を照合する。

Predictive等のhistorical Family read modelとして`FamilyArtifact`が残るが、新規canonical Artifact ownershipと区別する。

### 12.3 Lineage

Lineageには2つの表現層がある。

1. canonical/generic authority: `LineageEdge(ResourceRef -> ResourceRef)`およびtyped structural relation。
2. Result起点read projection: Project / Dataset / Execution / Result / GraphVersion / Artifact / Annotationをtraverseし、表示用relation名へ変換する。

表示用`CONTEXT_FOR / SOURCE_OF / INPUT_TO / HAS_ARTIFACT / HAS_ANNOTATION`等と、generic authoritative relation typeを同一のwrite contractにしない。

Navigation Stageをpersistent lineage resourceとして追加しない。

Current lineage read modelは`ResearchContextVersion -> AnalysisSpecification -> ExecutionPlan -> Execution -> StageExecution -> Result -> Artifact`を最低chainとし、DatasetVersion / AnalysisView / GraphVersion / input Result / base Executionを接続する。FK/snapshotからdeterministically導出できるstructural relationをgeneric LineageEdgeへ二重persistせず、`MOTIVATED`等のsemantic relationだけをgeneric edgeとして保持する。

Exploratory ResultからAnalysisSpecification DRAFTへのhandoffは`Result --MOTIVATED--> AnalysisSpecification`を明示保存する。


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
