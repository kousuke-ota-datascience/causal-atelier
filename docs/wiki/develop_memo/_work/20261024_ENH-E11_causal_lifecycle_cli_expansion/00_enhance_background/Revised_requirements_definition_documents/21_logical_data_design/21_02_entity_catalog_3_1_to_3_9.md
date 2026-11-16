<!-- ENH-E11 split working copy: not a formal approval. -->
# 21 — entity catalog 3 1 to 3 9

**Status:** `STRUCTURAL_COPY_DRAFT` (existing baseline text, not E11 canonical publication)

**Source:** [21_logical_data_design.md](https://github.com/kousuke-ota-datascience/causal-atelier/blob/3ba5fe2465ec591f0da7f998c21a5241984b73dc/docs/wiki/requirement_definition/21_logical_data_design.md) · blob `72903b9ad48b5b7edabaa7bb1c2cace42aa46ce7`  
**Index:** [Revised document inventory](../README_00_Revised_requirements_definition_documents.md)

---

## 3. Entity定義

### 3.1 Project

定義: 1つの分析テーマと、そのResearch Context、Dataset、Analysis、Result、Lineageの責務境界。

| 属性 | PK | FK | データ型 | NOT NULL | その他制約 | 説明 |
| --- | --- | --- | --- | --- | --- | --- |
| `project_id` | 1 |  | UUID / VARCHAR(36) | 1 | 不変 | Project識別子 |
| `name` |  |  | VARCHAR(200) | 1 |  | 表示名 |
| `topic` |  |  | TEXT |  |  | Research Topic |
| `objective` |  |  | TEXT |  |  | 分析・意思決定目的 |
| `memo` |  |  | TEXT |  |  | 補足 |
| `status` |  |  | VARCHAR(20) | 1 | `ACTIVE` / `ARCHIVED` | Project状態 |
| `created_at` |  |  | TIMESTAMP WITH TIME ZONE | 1 |  | 作成日時 |
| `updated_at` |  |  | TIMESTAMP WITH TIME ZONE | 1 |  | 更新日時 |

設計判断・制約:
- Projectの利用停止はhard deleteではなく`ACTIVE -> ARCHIVED`で表現する。
- `ARCHIVED` Projectでは新規writeを禁止し、既存ResourceとLineageをread-onlyで保持する。
- Research Contextのversioned contentはProject本体へ埋め込まず`ResearchContextVersion`で管理する。

### 3.2 Artifact

定義: Dataset sourceまたはExecutionが生成した物理生成物について、所在、内容hash、media type、所有関係を管理するdescriptor。

| 属性 | PK | FK | データ型 | NOT NULL | その他制約 | 説明 |
| --- | --- | --- | --- | --- | --- | --- |
| `artifact_id` | 1 |  | UUID / VARCHAR(36) | 1 | 不変 | Artifact識別子 |
| `project_id` |  | `Project.project_id` | UUID / VARCHAR(36) | 1 | INDEX, `ON DELETE RESTRICT` | 所属Project |
| `execution_id` |  | `Execution.execution_id` | UUID / VARCHAR(36) |  | INDEX, `ON DELETE RESTRICT` | 生成元Execution。SOURCE ArtifactではNULL |
| `stage_execution_id` |  | `StageExecution.stage_execution_id` | UUID / VARCHAR(36) |  | INDEX, 論理参照 | 生成元StageExecution。物理FKは必須としない |
| `result_id` |  | `Result.result_id` | UUID / VARCHAR(36) |  | INDEX, `ON DELETE RESTRICT` | 対応Result |
| `artifact_scope` |  |  | VARCHAR(30) | 1 | `SOURCE` / `EXECUTION_OUTPUT` | 所有scope |
| `artifact_type` |  |  | VARCHAR(40) | 1 | 許容type allowlist | Artifact種別 |
| `object_key` |  |  | TEXT | 1 | UNIQUE | Artifact Store上の論理所在 |
| `content_hash` |  |  | VARCHAR(128) | 1 |  | 内容hash |
| `media_type` |  |  | VARCHAR(100) | 1 |  | MIME type |
| `size_bytes` |  |  | BIGINT | 1 | `>= 0` | byte数 |
| `metadata_json` |  |  | JSON | 1 | default `{}` | 補足metadata |
| `created_at` |  |  | TIMESTAMP WITH TIME ZONE | 1 |  | 作成日時 |

設計判断・制約:
- `SOURCE`では`execution_id / stage_execution_id / result_id`を持たない。
- `EXECUTION_OUTPUT`では`execution_id`を必須とする。
- APIはlocal absolute pathを正本識別子として返さない。


現行`ArtifactType`の許容値:

```text
DATASET_FILE
GRAPH_JSON
GRAPH_IMAGE
EFFECT_TABLE
DIAGNOSTICS_TABLE
MANIFEST
CONFIG_SNAPSHOT
LOG
SCIENTIFIC_RESULT_JSON
SCIENTIFIC_REPORT
CHART_SPECIFICATION
PARTITION_INDEX
FITTED_PREPROCESSOR
FITTED_MODEL
PREDICTION
PREDICTIVE_EXPLANATION
MODEL_CARD
```

Canonical Artifactに`family`、汎用`schema_version`、`storage_uri`、`deleted_at`、`deletion_reason`を追加しない。historical `FamilyArtifact`のfieldとcanonical Artifactを混同しない。

### 3.3 DatasetVersion

定義: Executionで参照する入力Datasetの不変Version。Dataset系列は`dataset_key`で表現する。

| 属性 | PK | FK | データ型 | NOT NULL | その他制約 | 説明 |
| --- | --- | --- | --- | --- | --- | --- |
| `dataset_version_id` | 1 |  | UUID / VARCHAR(36) | 1 | 不変 | Dataset Version識別子 |
| `project_id` |  | `Project.project_id` | UUID / VARCHAR(36) | 1 | INDEX, `ON DELETE RESTRICT` | 所属Project |
| `source_artifact_id` |  | `Artifact.artifact_id` | UUID / VARCHAR(36) | 1 | UNIQUE, `ON DELETE RESTRICT` | SOURCE Artifact |
| `dataset_key` |  |  | VARCHAR(100) | 1 | INDEX | Dataset系列key |
| `name` |  |  | VARCHAR(200) | 1 |  | 表示名 |
| `version_label` |  |  | VARCHAR(100) | 1 | UNIQUE(`project_id`,`dataset_key`,`version_label`) | Version表示label |
| `content_hash` |  |  | VARCHAR(128) | 1 | UNIQUE(`project_id`,`dataset_key`,`content_hash`) | Dataset内容hash |
| `schema_json` |  |  | JSON | 1 | default `{}` | column名とlogical type等 |
| `profile_summary_json` |  |  | JSON | 1 | default `{}` | profile summary |
| `row_count` |  |  | BIGINT | 1 | `>= 0` | 行数 |
| `column_count` |  |  | INTEGER | 1 | `>= 0` | 列数 |
| `source_note` |  |  | TEXT |  |  | 出所・補足 |
| `created_at` |  |  | TIMESTAMP WITH TIME ZONE | 1 |  | 登録日時 |

設計判断・制約:
- 登録後のDataset内容を上書きしない。変更は新しいDatasetVersionとする。
- `source_artifact_id`はSOURCE scopeのArtifactを参照しなければならない。

### 3.4 ResearchContextVersion

定義: 問題設定、Research Question、仮説、意思決定文脈をversioned resourceとして保持する。

| 属性 | PK | FK | データ型 | NOT NULL | その他制約 | 説明 |
| --- | --- | --- | --- | --- | --- | --- |
| `research_context_version_id` | 1 |  | UUID / VARCHAR(36) | 1 | 不変 | Research Context Version識別子 |
| `project_id` |  | `Project.project_id` | UUID / VARCHAR(36) | 1 | INDEX, `ON DELETE RESTRICT` | 所属Project |
| `context_key` |  |  | VARCHAR(100) | 1 | UNIQUE tuple構成要素 | Context系列key |
| `version_number` |  |  | INTEGER | 1 | `> 0`; UNIQUE(`project_id`,`context_key`,`version_number`) | version番号 |
| `status` |  |  | VARCHAR(20) | 1 | `DRAFT` / `FIXED` | 状態 |
| `schema_version` |  |  | VARCHAR(100) | 1 | default `research-context/1` | schema version |
| `problem_statement` |  |  | TEXT | 1 |  | 問題設定 |
| `research_questions_json` |  |  | JSON | 1 | 1件以上を要求 | Research Question |
| `significance` |  |  | TEXT |  |  | 重要性 |
| `hypotheses_json` |  |  | JSON | 1 | default `[]` | 仮説 |
| `decision_context_json` |  |  | JSON | 1 | default `{}` | 意思決定文脈 |
| `relations_json` |  |  | JSON | 1 | default `[]`; self-reference禁止 | 他ResearchContextVersionとのrelation |
| `canonical_hash` |  |  | VARCHAR(64) |  | FIXED時に生成 | canonical content hash |
| `created_by` |  |  | VARCHAR(200) | 1 |  | 作成者 |
| `created_at` |  |  | TIMESTAMP WITH TIME ZONE | 1 |  | 作成日時 |
| `fixed_at` |  |  | TIMESTAMP WITH TIME ZONE |  | FIXED時のみ | 固定日時 |

設計判断・制約:
- `FIXED`後のcontentを上書きしない。
- `relations_json`で許容するrelationは`REFINES / DERIVED_FROM / SUPERSEDES / RELATED_TO`とする。
- relation targetは同一Project内で解決する。

### 3.5 AnalysisView

定義: DatasetVersionに対するrow filter、column selection、derived column、missing-value policy等をversionedに保持する。

| 属性 | PK | FK | データ型 | NOT NULL | その他制約 | 説明 |
| --- | --- | --- | --- | --- | --- | --- |
| `analysis_view_id` | 1 |  | UUID / VARCHAR(36) | 1 | 不変 | Analysis View識別子 |
| `project_id` |  | `Project.project_id` | UUID / VARCHAR(36) | 1 | INDEX, `ON DELETE RESTRICT` | 所属Project |
| `source_dataset_version_id` |  | `DatasetVersion.dataset_version_id` | UUID / VARCHAR(36) | 1 | INDEX, `ON DELETE RESTRICT` | source Dataset Version |
| `view_key` |  |  | VARCHAR(100) | 1 | UNIQUE tuple構成要素 | View系列key |
| `version_number` |  |  | INTEGER | 1 | `> 0`; UNIQUE(`project_id`,`view_key`,`version_number`) | version番号 |
| `name` |  |  | VARCHAR(200) | 1 |  | 表示名 |
| `status` |  |  | VARCHAR(20) | 1 | `DRAFT` / `FIXED` | 状態 |
| `schema_version` |  |  | VARCHAR(100) | 1 | default `analysis-view/1` | schema version |
| `spec_json` |  |  | JSON | 1 |  | row/column/derived/filter/time/sampling specification |
| `content_hash` |  |  | VARCHAR(64) |  | FIXED時に生成 | canonical content hash |
| `manifest_json` |  |  | JSON | 1 | default `{}` | materialization/validation summary |
| `created_by` |  |  | VARCHAR(200) | 1 |  | 作成者 |
| `created_at` |  |  | TIMESTAMP WITH TIME ZONE | 1 |  | 作成日時 |
| `fixed_at` |  |  | TIMESTAMP WITH TIME ZONE |  | FIXED時のみ | 固定日時 |

設計判断・制約:
- `FIXED`後のspecを上書きしない。
- filter operator/valueはsource Dataset logical typeと互換でなければならない。
- Analysis Viewはsource Dataset Versionに対してのみ有効であり、別Dataset Versionへ暗黙再利用しない。

### 3.6 AnalysisSpecification

定義: Research Context、Dataset、任意のAnalysisViewと、Analysis Family固有の問い・方法・評価条件を結び付けるversioned specification。

| 属性 | PK | FK | データ型 | NOT NULL | その他制約 | 説明 |
| --- | --- | --- | --- | --- | --- | --- |
| `analysis_specification_id` | 1 |  | UUID / VARCHAR(36) | 1 | 不変 | Analysis Specification識別子 |
| `project_id` |  | `Project.project_id` | UUID / VARCHAR(36) | 1 | INDEX, `ON DELETE RESTRICT` | 所属Project |
| `specification_key` |  |  | VARCHAR(100) | 1 | UNIQUE tuple構成要素 | Specification系列key |
| `version_number` |  |  | INTEGER | 1 | `> 0`; UNIQUE(`project_id`,`specification_key`,`version_number`) | version番号 |
| `status` |  |  | VARCHAR(20) | 1 | `DRAFT` / `FIXED` | 状態 |
| `schema_version` |  |  | VARCHAR(100) | 1 | default `analysis-specification/1` | 共通Envelope schema |
| `analysis_family` |  |  | VARCHAR(20) | 1 | `EXPLORATORY / CAUSAL / PREDICTIVE` | Analysis Family discriminator |
| `research_context_version_id` |  | `ResearchContextVersion.research_context_version_id` | UUID / VARCHAR(36) | 1 | INDEX, `ON DELETE RESTRICT` | Research Context |
| `dataset_version_id` |  | `DatasetVersion.dataset_version_id` | UUID / VARCHAR(36) | 1 | INDEX, `ON DELETE RESTRICT` | Dataset Version |
| `analysis_view_id` |  | `AnalysisView.analysis_view_id` | UUID / VARCHAR(36) |  | INDEX, `ON DELETE RESTRICT` | 任意Analysis View |
| `analysis_mode` |  |  | VARCHAR(20) | 1 | `EXPLORATORY / CONFIRMATORY` | 分析mode |
| `family_spec_schema_version` |  |  | VARCHAR(100) | 1 |  | Family-specific schema version |
| `family_spec_json` |  |  | JSON | 1 |  | Family-specific specification |
| `revision_context_json` |  |  | JSON |  |  | revision rationale/context |
| `warnings_json` |  |  | JSON | 1 | default `[]` | scientific / reuse warning |
| `canonical_hash` |  |  | VARCHAR(64) |  | FIXED時に生成 | canonical content hash |
| `created_by` |  |  | VARCHAR(200) | 1 |  | 作成者 |
| `created_at` |  |  | TIMESTAMP WITH TIME ZONE | 1 |  | 作成日時 |
| `fixed_at` |  |  | TIMESTAMP WITH TIME ZONE |  | FIXED時のみ | 固定日時 |

設計判断・制約:
- `analysis_family`と`family_spec_schema_version / family_spec_json`のschemaは整合しなければならない。
- Research Context、Dataset Version、Analysis Viewはすべて同一Projectに属さなければならない。
- Navigation StageはAnalysisSpecificationのsemantic inputではないため属性として追加しない。

### 3.7 ExecutionPlan

定義: 固定されたAnalysisSpecificationからplannerが生成するruntime Stage DAGの不変plan。

| 属性 | PK | FK | データ型 | NOT NULL | その他制約 | 説明 |
| --- | --- | --- | --- | --- | --- | --- |
| `execution_plan_id` | 1 |  | UUID / VARCHAR(36) | 1 | 不変 | Execution Plan識別子 |
| `project_id` |  | `Project.project_id` | UUID / VARCHAR(36) | 1 | INDEX, `ON DELETE RESTRICT` | 所属Project |
| `analysis_specification_id` |  | `AnalysisSpecification.analysis_specification_id` | UUID / VARCHAR(100) | 1 | INDEX; logical FK | 入力Specification。物理FK有無に依存しない論理参照 |
| `analysis_family` |  |  | VARCHAR(20) | 1 | `EXPLORATORY / CAUSAL / PREDICTIVE` | Family |
| `plan_schema_version` |  |  | VARCHAR(100) | 1 |  | Plan schema version |
| `planner_id` |  |  | VARCHAR(100) | 1 |  | Planner識別子 |
| `planner_version` |  |  | VARCHAR(40) | 1 |  | Planner version |
| `stages_json` |  |  | JSON | 1 |  | StageDefinition一覧 |
| `dependencies_json` |  |  | JSON | 1 |  | Stage dependency/binding DAG |
| `plan_hash` |  |  | VARCHAR(64) | 1 | UNIQUE | canonical Plan hash |
| `created_at` |  |  | TIMESTAMP WITH TIME ZONE | 1 |  | 生成日時 |

設計判断・制約:
- ExecutionPlanは生成後に上書きしない。
- `analysis_family`は入力AnalysisSpecificationのFamilyと一致しなければならない。
- Navigation Stage / browser routeをExecutionPlanへ保存しない。

### 3.8 Execution

定義: 一つのAnalysis Operationを、固定されたinputとsnapshotで実行するcanonical execution。

| 属性 | PK | FK | データ型 | NOT NULL | その他制約 | 説明 |
| --- | --- | --- | --- | --- | --- | --- |
| `execution_id` | 1 |  | UUID / VARCHAR(36) | 1 | 不変 | Execution識別子 |
| `project_id` |  | `Project.project_id` | UUID / VARCHAR(36) | 1 | INDEX, `ON DELETE RESTRICT` | 所属Project |
| `analysis_family` |  |  | VARCHAR(20) | 1 | `CAUSAL / EXPLORATORY / PREDICTIVE` | Analysis Family |
| `dataset_version_id` |  | `DatasetVersion.dataset_version_id` | UUID / VARCHAR(36) | 1 | INDEX, `ON DELETE RESTRICT` | 入力Dataset Version |
| `input_graph_version_id` |  | `GraphVersion.graph_version_id` | UUID / VARCHAR(36) |  | INDEX, `ON DELETE RESTRICT` | 入力Graph Version |
| `input_result_id` |  | `Result.result_id` | UUID / VARCHAR(36) |  | INDEX, `ON DELETE RESTRICT` | 上流Result |
| `batch_key` |  |  | UUID / VARCHAR(36) | 1 | INDEX | batch / comparison単位 |
| `operation` |  |  | VARCHAR(20) | 1 | `DISCOVERY / IDENTIFICATION / ESTIMATION / REFUTATION / SENSITIVITY` | Operation |
| `objective_snapshot` |  |  | TEXT |  |  | 受付時objective snapshot |
| `rationale_snapshot` |  |  | TEXT |  |  | 受付時rationale snapshot |
| `analysis_spec_json` |  |  | JSON | 1 | canonical execution snapshot | 実行用Analysis Specification snapshot |
| `algorithm_or_estimator` |  |  | VARCHAR(100) | 1 |  | algorithm / estimator |
| `parameter_json` |  |  | JSON | 1 | default `{}` | parameter snapshot |
| `random_seed` |  |  | BIGINT |  |  | random seed |
| `code_version` |  |  | VARCHAR(200) | 1 |  | code version |
| `runtime_version_json` |  |  | JSON | 1 | default `{}` | runtime/library versions |
| `snapshot_hash` |  |  | VARCHAR(128) | 1 |  | canonical snapshot hash |
| `snapshot_schema_version` |  |  | VARCHAR(100) | 1 |  | snapshot schema version |
| `status` |  |  | VARCHAR(20) | 1 | `QUEUED / RUNNING / SUCCEEDED / FAILED / CANCELLED` | technical status |
| `retry_count` |  |  | INTEGER | 1 | default `0`, `>= 0` | retry回数 |
| `last_error_summary` |  |  | TEXT |  |  | 最終technical error |
| `requested_by` |  |  | VARCHAR(200) | 1 |  | 要求者 |
| `requested_at` |  |  | TIMESTAMP WITH TIME ZONE | 1 |  | 受付日時 |
| `started_at` |  |  | TIMESTAMP WITH TIME ZONE |  |  | 開始日時 |
| `finished_at` |  |  | TIMESTAMP WITH TIME ZONE |  |  | 終了日時 |
| `base_execution_id` |  | `Execution.execution_id` | UUID / VARCHAR(36) |  | INDEX, self reference | rerun/revision元Execution |
| `revision_kind` |  |  | VARCHAR(20) |  | NULL / `RERUN / REVISED` | revision種別 |
| `change_reason` |  |  | TEXT |  |  | 変更理由 |
| `lease_owner` |  |  | VARCHAR(200) |  | INDEX | worker lease owner |
| `lease_expires_at` |  |  | TIMESTAMP WITH TIME ZONE |  | INDEX | worker lease期限 |

設計判断・制約:
- Submit後のinput Dataset/Graph/Result、analysis snapshot、method、parameterを上書きしない。
- Operation別input制約は`6.4`で定義する。
- `base_execution_id`を使うrevisionも新しいExecution identityを持つ。
- worker token等の内部実装属性は論理Domain属性に含めない。


`runtime_version_json`は最低限、実際の実行環境を再構築するための次のmetadataを保持する。

```text
ariadne_code_version
python_version
platform_system
platform_release
machine
libraries
```

`libraries`には実際にregistered/used runner dependencyとして使用したscientific library versionを保存する。version取得だけを目的にfuture optional dependencyをimportしない。

Canonical `Execution`には`execution_plan_id`を独立属性として必須化しない。ExecutionPlan identityを保持するapplication pathでは`analysis_spec_json`内metadataとして扱い得るが、canonical Execution FKと同一視しない。

### 3.9 StageExecution

定義: ExecutionPlanで定義されたruntime Stageのcanonical実行状態。

| 属性 | PK | FK | データ型 | NOT NULL | その他制約 | 説明 |
| --- | --- | --- | --- | --- | --- | --- |
| `stage_execution_id` | 1 |  | UUID / VARCHAR(36) | 1 | 不変 | StageExecution識別子 |
| `execution_id` |  | `Execution.execution_id` | UUID / VARCHAR(36) | 1 | INDEX, `ON DELETE RESTRICT` | 親Execution |
| `stage_key` |  |  | VARCHAR(100) | 1 | UNIQUE(`execution_id`,`stage_key`) | Execution内Stage key |
| `stage_type_json` |  |  | JSON | 1 |  | runtime StageType |
| `ordinal` |  |  | INTEGER | 1 | `>= 0` | 表示/plan順序 |
| `dependencies_json` |  |  | JSON | 1 | default `[]` | 依存Stage key |
| `status` |  |  | VARCHAR(40) | 1 | StageExecution状態allowlist | technical stage status |
| `input_binding_json` |  |  | JSON | 1 | default `{}` | resolved input binding |
| `output_binding_json` |  |  | JSON | 1 | default `{}` | produced output binding |
| `last_error_json` |  |  | JSON |  |  | 最終error detail |
| `started_at` |  |  | TIMESTAMP WITH TIME ZONE |  |  | 開始日時 |
| `finished_at` |  |  | TIMESTAMP WITH TIME ZONE |  |  | 終了日時 |
| `created_at` |  |  | TIMESTAMP WITH TIME ZONE | 1 |  | 生成日時 |

設計判断・制約:
- `stage_execution_id`と`execution_id`のidentity pairは一意である。
- Navigation Stageとは別概念であり、Family-local UI Stage IDをruntime lifecycleへ流用しない。
