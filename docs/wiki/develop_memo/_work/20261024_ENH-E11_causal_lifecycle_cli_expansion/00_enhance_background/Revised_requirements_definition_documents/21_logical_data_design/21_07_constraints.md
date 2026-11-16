<!-- ENH-E11 split working copy: not a formal approval. -->
# 21 — constraints

**Status:** `STRUCTURAL_COPY_DRAFT` (existing baseline text, not E11 canonical publication)

**Source:** [21_logical_data_design.md](https://github.com/kousuke-ota-datascience/causal-atelier/blob/3ba5fe2465ec591f0da7f998c21a5241984b73dc/docs/wiki/requirement_definition/21_logical_data_design.md) · blob `72903b9ad48b5b7edabaa7bb1c2cace42aa46ce7`  
**Index:** [Revised document inventory](../README_00_Revised_requirements_definition_documents.md)

---

## 6. 整合性制約

### 6.1 Project境界

- Project-scoped Entityの参照先は原則同一Projectに属する。
- `AnalysisSpecification`のResearchContextVersion / DatasetVersion / AnalysisViewは同一Project。
- `Execution`のDatasetVersion / input GraphVersion / input Result / base Executionは同一Project。
- `Annotation` target、WorkspaceSelection target、WorkspaceAnnotation target、ExportBundle Result、LineageEdge source/targetも同一Project。
- Project境界を越える比較が必要な場合はread-only projectionとして明示し、canonical Entity間FKを暗黙に跨がせない。

### 6.2 Version / 不変性

- DatasetVersionは登録後不変。
- ResearchContextVersion / AnalysisView / AnalysisSpecification / GraphVersionはFIXED後不変。
- ExecutionPlanは生成後不変。
- Executionのinput/snapshot/method/parameterはSubmit後不変。
- Result / Artifact / ExportBundleは生成後不変。
- 変更は新Version / 新Execution / 新Result等として明示する。

### 6.3 Referential / Cardinality制約

- DatasetVersionは1つのSOURCE Artifactを必須参照する。
- AnalysisViewは1つのsource DatasetVersionを必須参照する。
- AnalysisSpecificationはResearchContextVersionとDatasetVersionを必須参照し、AnalysisViewは任意。
- StageExecutionは1つのExecutionに所属する。
- StageAttemptは1つのStageExecutionに所属し、attempt numberはStageExecution内で一意。
- Resultは1つのExecutionに所属する。STAGE_RESULTのみStageExecutionを必須参照する。
- AnnotationはResultまたはGraphVersionのどちらか一方だけを対象とする。
- WorkspaceSelectionはProject/userにつき最大1件。
- ProjectMembershipはProject/userにつき最大1件。
- LineageEdgeのsemantic tupleは重複登録しない。

### 6.4 Operation別入力制約

Canonical Causal Operationの最低参照制約:

| Operation | Dataset | Graph | Input Result |
| --- | --- | --- | --- |
| DISCOVERY | 必須 | 禁止 | 禁止 |
| IDENTIFICATION | 必須 | 必須 | 禁止 |
| ESTIMATION | 必須 | 必須 | Identification Resultを要求。ただし明示されたlegacy snapshot互換を除く |
| REFUTATION | 必須 | 必須 | Treatment Effect等のupstream Resultを必須 |
| SENSITIVITY | 必須 | 必須 | Treatment Effect等のupstream Resultを必須 |

Family固有runtime planでOperation taxonomyが異なる場合も、input ownershipとsnapshotの不変性を維持する。

### 6.5 AnalysisView整合性

- selected / derived columnがsource Dataset schemaに対して解決可能である。
- derived column名を重複させない。
- filter operator/value typeがlogical typeに適合する。
- 非決定的関数、任意code execution、外部I/OをAnalysisView expressionとして許可しない。
- AnalysisViewのDataset compatibilityをWorkspaceSelection変更時にも再検証する。

### 6.6 Result type / scientific status matrix

`Result.result_type`と`scientific_status`は任意組合せではない。少なくとも次を満たす。

| Result Type | Allowed Scientific Status |
| --- | --- |
| `DATA_PROFILE_RESULT`, `DISTRIBUTION_RESULT`, `ASSOCIATION_RESULT`, `GROUP_SUMMARY_RESULT`, `CHART_RESULT`, `ERROR_ANALYSIS_RESULT`, `MODEL_CARD_RESULT` | `GENERATED`, `GENERATED_WITH_WARNINGS` |
| `SPLIT_RESULT` | `PASS` |
| `TRAINING_RESULT` | `TRAINED`, `TRAINED_WITH_WARNINGS` |
| `EVALUATION_RESULT` | `EVALUATED`, `INSUFFICIENT_TEST_SAMPLE` |
| `PREDICTIVE_EXPLANATION_RESULT` | `GENERATED`, `GENERATED_WITH_WARNINGS`, `NOT_APPLICABLE` |
| `DISCOVERY_GRAPH_RESULT` | `GENERATED`, `GENERATED_WITH_WARNINGS`, `UNRELIABLE` |
| `IDENTIFICATION_RESULT` | `IDENTIFIED`, `NOT_IDENTIFIED`, `PARTIALLY_IDENTIFIED`, `REQUIRES_REVIEW` |
| `DATA_ELIGIBILITY_RESULT`, `DIAGNOSTICS_RESULT` | `PASS`, `WARN`, `FAIL` |
| `TREATMENT_EFFECT_RESULT` | `ESTIMATED`, `INSUFFICIENT_OVERLAP`, `INSUFFICIENT_SAMPLE`, `ESTIMATION_UNRELIABLE`, `REQUIRES_REVIEW` |
| `REFUTATION_RESULT` | `NO_FAILURE_DETECTED`, `FAILURE_DETECTED`, `INCONCLUSIVE` |
| `SENSITIVITY_RESULT` | `ROBUST`, `FRAGILE`, `INCONCLUSIVE` |

### 6.7 Artifact ownership

- `artifact_scope = SOURCE`の場合、execution / stage execution / result ownershipを持たない。
- `artifact_scope = EXECUTION_OUTPUT`の場合、Executionを必須参照する。
- stage/result referenceを持つArtifactは、そのExecution/Project ownershipと整合する。
- `object_key`は一意であり、同一physical objectを別のcanonical Artifact identityとして二重管理しない。

### 6.8 GraphVersion整合性

`graph_origin`とsource/parent referenceの整合を保証する。

- `DISCOVERED`: `source_result_id`必須。
- `CONSTRAINT_ADJUSTED`: source Resultまたはparent GraphVersionの少なくとも一方を要求。
- `USER_DEFINED / IMPORTED`: source Resultとparent GraphVersionを持たない。
- `USER_EDITED`: parent GraphVersion必須、source Resultは持たない。
- 自己parentを禁止する。
- Graph lineageでcycleを許容する設計にしてはならない。cycle検出の実装方式は詳細設計で定める。

### 6.9 ResearchContext relation整合性

- relation targetは同一ProjectのResearchContextVersion。
- self referenceを禁止する。
- relation typeは`REFINES / DERIVED_FROM / SUPERSEDES / RELATED_TO`。
- 特定relationのDAG性を要求する場合は、一般cycle検出を実装するまで「保証済み」と扱わない。

### 6.10 Lineage整合性

- LineageEdgeはsource/target存在確認後に保存する。
- source/targetは同一Project。
- semantic tupleを一意とする。
- direct FK/referenceとLineageEdgeが同じrelationを表す場合、両者の意味が矛盾してはならない。
- lineage queryはcanonical Entity / LineageEdgeをauthorityとし、presentation stateから推測しない。

### 6.11 Navigation / runtime境界

- Navigation Stageを`AnalysisSpecification / ExecutionPlan / Execution / StageExecution`へ追加しない。
- Current Family / Navigation Stageはbrowser route/navigation stateをauthorityとする。
- Navigation catalogはapplication metadataでありscientific schema registryへ登録しない。
- context selection不足をruntime Stage failureとして記録しない。Operation availabilityとして事前に表現する。

### 6.12 Unique / index論理制約

主要unique constraint:

| Entity | Unique key |
| --- | --- |
| DatasetVersion | (`project_id`,`dataset_key`,`version_label`) |
| DatasetVersion | (`project_id`,`dataset_key`,`content_hash`) |
| DatasetVersion | `source_artifact_id` |
| ResearchContextVersion | (`project_id`,`context_key`,`version_number`) |
| AnalysisView | (`project_id`,`view_key`,`version_number`) |
| AnalysisSpecification | (`project_id`,`specification_key`,`version_number`) |
| ExecutionPlan | `plan_hash` |
| StageExecution | (`execution_id`,`stage_key`) |
| StageAttempt | (`stage_execution_id`,`attempt_number`) |
| ProjectMembership | (`project_id`,`user_id`) |
| WorkspaceSelection | (`project_id`,`user_id`) |
| Artifact | `object_key` |
| ExportBundle | `object_key` |
| LineageEdge | (`source_type`,`source_id`,`relation_type`,`target_type`,`target_id`) |

Indexは検索・ownership validation・Lineage traversalに必要なFK/referenceを中心に設計し、logical uniquenessとphysical performance indexを混同しない。

### 6.13 Schema reader contract

Dataset schemaを参照するvalidator / application serviceは、`DatasetVersion.schema_json`からlogical typeを一貫して解決しなければならない。

最低要件:

- column名からlogical typeを取得できる。
- unknown/missing columnをsilent successにしない。
- logical type aliasの正規化規則を一箇所へ集約する。
- filter/type validationとUI schema表示で異なる型解釈を持たない。
