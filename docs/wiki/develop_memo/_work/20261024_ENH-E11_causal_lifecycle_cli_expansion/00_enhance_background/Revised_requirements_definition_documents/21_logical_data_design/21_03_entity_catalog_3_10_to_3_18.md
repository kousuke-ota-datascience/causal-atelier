<!-- ENH-E11 split working copy: not a formal approval. -->
# 21 — entity catalog 3 10 to 3 18

**Status:** `STRUCTURAL_COPY_DRAFT` (existing baseline text, not E11 canonical publication)

**Source:** [21_logical_data_design.md](https://github.com/kousuke-ota-datascience/causal-atelier/blob/3ba5fe2465ec591f0da7f998c21a5241984b73dc/docs/wiki/requirement_definition/21_logical_data_design.md) · blob `72903b9ad48b5b7edabaa7bb1c2cace42aa46ce7`  
**Index:** [Revised document inventory](../README_00_Revised_requirements_definition_documents.md)

---

## 3. 続き

### 3.10 StageAttempt

定義: StageExecutionに対するappend-only retry/attempt history。

| 属性 | PK | FK | データ型 | NOT NULL | その他制約 | 説明 |
| --- | --- | --- | --- | --- | --- | --- |
| `stage_attempt_id` | 1 |  | UUID / VARCHAR(36) | 1 | 不変 | StageAttempt識別子 |
| `stage_execution_id` |  | `StageExecution.stage_execution_id` | UUID / VARCHAR(36) | 1 | INDEX, `ON DELETE RESTRICT` | 対象StageExecution |
| `attempt_number` |  |  | INTEGER | 1 | `> 0`; UNIQUE(`stage_execution_id`,`attempt_number`) | attempt連番 |
| `worker_id` |  |  | VARCHAR(200) | 1 |  | worker識別子 |
| `started_at` |  |  | TIMESTAMP WITH TIME ZONE | 1 |  | 開始日時 |
| `finished_at` |  |  | TIMESTAMP WITH TIME ZONE |  |  | 終了日時 |
| `error_json` |  |  | JSON |  |  | 失敗detail |
| `effective_random_seed` |  |  | INTEGER |  |  | 実際に使用したseed |

設計判断・制約:
- StageAttemptはappend-onlyとし、過去attemptを上書きしない。

### 3.11 Result

定義: ExecutionまたはStageExecutionから生成され、分析判断・比較・Lineageの正本となる論理的科学結果。

| 属性 | PK | FK | データ型 | NOT NULL | その他制約 | 説明 |
| --- | --- | --- | --- | --- | --- | --- |
| `result_id` | 1 |  | UUID / VARCHAR(36) | 1 | 不変 | Result識別子 |
| `execution_id` |  | `Execution.execution_id` | UUID / VARCHAR(36) | 1 | INDEX, `ON DELETE RESTRICT` | 生成元Execution |
| `result_level` |  |  | VARCHAR(30) | 1 | `EXECUTION_RESULT / STAGE_RESULT` | ownership level |
| `stage_execution_id` |  | `StageExecution.stage_execution_id` | UUID / VARCHAR(36) |  | INDEX, 論理参照 | STAGE_RESULTの生成Stage。物理FKは必須としない |
| `result_type` |  |  | VARCHAR(40) | 1 | Result Type allowlist | Result種別 |
| `scientific_status` |  |  | VARCHAR(40) | 1 | Result Type別status matrix | 科学的評価状態 |
| `summary_json` |  |  | JSON | 1 | default `{}` | 比較表示用summary |
| `payload_json` |  |  | JSON | 1 | default `{}` | 構造化Result本体 |
| `diagnostics_json` |  |  | JSON | 1 | default `{}` | 診断情報 |
| `warning_json` |  |  | JSON | 1 | default `[]` | warning一覧 |
| `created_at` |  |  | TIMESTAMP WITH TIME ZONE | 1 |  | 生成日時 |

設計判断・制約:
- `EXECUTION_RESULT`では`stage_execution_id = NULL`、`STAGE_RESULT`では`stage_execution_id != NULL`とする。
- technical Execution statusとscientific Result statusを分離する。
- `result_type`と`scientific_status`の許容組合せは`6.6`で定義する。


Family別Result Type:

| Family | Result Type |
| --- | --- |
| EXPLORATORY | `DATA_PROFILE_RESULT`, `DISTRIBUTION_RESULT`, `ASSOCIATION_RESULT`, `GROUP_SUMMARY_RESULT`, `CHART_RESULT` |
| CAUSAL | `DISCOVERY_GRAPH_RESULT`, `IDENTIFICATION_RESULT`, `DATA_ELIGIBILITY_RESULT`, `TREATMENT_EFFECT_RESULT`, `DIAGNOSTICS_RESULT`, `REFUTATION_RESULT`, `SENSITIVITY_RESULT` |
| PREDICTIVE | `SPLIT_RESULT`, `TRAINING_RESULT`, `EVALUATION_RESULT`, `ERROR_ANALYSIS_RESULT`, `PREDICTIVE_EXPLANATION_RESULT`, `MODEL_CARD_RESULT` |

Result semantic levelはExecution-levelまたはStage-levelであり、別のResult architectureではない。physical storage locator / object key / URIはResult identityではない。

### 3.12 GraphVersion

定義: Causal Graphの構造、origin、provenanceをversionedに保持する。

| 属性 | PK | FK | データ型 | NOT NULL | その他制約 | 説明 |
| --- | --- | --- | --- | --- | --- | --- |
| `graph_version_id` | 1 |  | UUID / VARCHAR(36) | 1 | 不変 | GraphVersion識別子 |
| `project_id` |  | `Project.project_id` | UUID / VARCHAR(36) | 1 | INDEX, `ON DELETE RESTRICT` | 所属Project |
| `source_result_id` |  | `Result.result_id` | UUID / VARCHAR(36) |  | INDEX, `ON DELETE RESTRICT` | 発見等のsource Result |
| `parent_graph_version_id` |  | `GraphVersion.graph_version_id` | UUID / VARCHAR(36) |  | INDEX, `ON DELETE RESTRICT` | 編集/派生元GraphVersion |
| `designated_outcome_node` |  |  | VARCHAR(200) |  | INDEX | designated outcome |
| `name` |  |  | VARCHAR(200) | 1 |  | 表示名 |
| `graph_type` |  |  | VARCHAR(40) | 1 | `DAG / CPDAG / PAG` | Graph type |
| `graph_origin` |  |  | VARCHAR(40) | 1 | `DISCOVERED / CONSTRAINT_ADJUSTED / USER_DEFINED / IMPORTED / USER_EDITED` | 由来 |
| `provenance_json` |  |  | JSON | 1 | default `{}` | provenance metadata |
| `graph_json` |  |  | JSON | 1 | canonical graph structure | node/edge本体 |
| `content_hash` |  |  | VARCHAR(128) | 1 |  | 内容hash |
| `edit_rationale` |  |  | TEXT |  |  | 編集理由 |
| `status` |  |  | VARCHAR(20) | 1 | `DRAFT / FIXED` | 状態 |
| `created_by` |  |  | VARCHAR(200) | 1 |  | 作成者 |
| `created_at` |  |  | TIMESTAMP WITH TIME ZONE | 1 |  | 作成日時 |

設計判断・制約:
- `FIXED` GraphVersionを上書きしない。
- `graph_origin`と`source_result_id / parent_graph_version_id`の組合せを制約する。
- 親GraphVersion参照によりGraphVersion lineageを明示する。

### 3.13 Annotation

定義: ResultまたはGraphVersionに対するstatement、rationale、assumption、limitationを保持する。

| 属性 | PK | FK | データ型 | NOT NULL | その他制約 | 説明 |
| --- | --- | --- | --- | --- | --- | --- |
| `annotation_id` | 1 |  | UUID / VARCHAR(36) | 1 | 不変 | Annotation識別子 |
| `project_id` |  | `Project.project_id` | UUID / VARCHAR(36) | 1 | INDEX, `ON DELETE RESTRICT` | 所属Project |
| `target_result_id` |  | `Result.result_id` | UUID / VARCHAR(36) |  | INDEX, `ON DELETE RESTRICT` | 対象Result |
| `target_graph_version_id` |  | `GraphVersion.graph_version_id` | UUID / VARCHAR(36) |  | INDEX, `ON DELETE RESTRICT` | 対象GraphVersion |
| `statement` |  |  | TEXT | 1 |  | statement |
| `rationale` |  |  | TEXT |  |  | rationale |
| `assumptions_json` |  |  | JSON | 1 | default `[]` | assumptions |
| `limitations_json` |  |  | JSON | 1 | default `[]` | limitations |
| `created_by` |  |  | VARCHAR(200) | 1 |  | 作成者 |
| `created_at` |  |  | TIMESTAMP WITH TIME ZONE | 1 |  | 作成日時 |
| `updated_at` |  |  | TIMESTAMP WITH TIME ZONE | 1 |  | 更新日時 |

設計判断・制約:
- `target_result_id`と`target_graph_version_id`は排他的XORとし、必ずどちらか一方だけを指定する。
- targetは同一Projectに属さなければならない。

### 3.14 ProjectMembership

定義: Projectに対するuser roleを保持する。

| 属性 | PK | FK | データ型 | NOT NULL | その他制約 | 説明 |
| --- | --- | --- | --- | --- | --- | --- |
| `membership_id` | 1 |  | UUID / VARCHAR(36) | 1 | 不変 | Membership識別子 |
| `project_id` |  | `Project.project_id` | UUID / VARCHAR(36) | 1 | INDEX, `ON DELETE RESTRICT` | 所属Project |
| `user_id` |  |  | VARCHAR(200) | 1 | UNIQUE(`project_id`,`user_id`) | user識別子 |
| `role` |  |  | VARCHAR(20) | 1 | `OWNER / EDITOR / VIEWER` | Project role |
| `created_at` |  |  | TIMESTAMP WITH TIME ZONE | 1 |  | 作成日時 |
### 3.15 WorkspaceSelection

定義: userごとのProject-scopedなResearch Context / Dataset Version / Analysis View selection stateを保持する。

| 属性 | PK | FK | データ型 | NOT NULL | その他制約 | 説明 |
| --- | --- | --- | --- | --- | --- | --- |
| `workspace_selection_id` | 1 |  | UUID / VARCHAR(36) | 1 | 不変 | WorkspaceSelection識別子 |
| `project_id` |  | `Project.project_id` | UUID / VARCHAR(36) | 1 | INDEX, `ON DELETE RESTRICT` | 所属Project |
| `user_id` |  |  | VARCHAR(200) | 1 | UNIQUE(`project_id`,`user_id`) | user識別子 |
| `research_context_version_id` |  | `ResearchContextVersion.research_context_version_id` | UUID / VARCHAR(36) |  | `ON DELETE RESTRICT` | Active Research Context selection |
| `dataset_version_id` |  | `DatasetVersion.dataset_version_id` | UUID / VARCHAR(36) |  | `ON DELETE RESTRICT` | Dataset Version selection |
| `analysis_view_id` |  | `AnalysisView.analysis_view_id` | UUID / VARCHAR(36) |  | `ON DELETE RESTRICT` | Analysis View selection |
| `unsaved_draft` |  |  | BOOLEAN | 1 | default `false` | 未保存draft存在flag |
| `updated_at` |  |  | TIMESTAMP WITH TIME ZONE | 1 |  | 最終更新日時 |

設計判断・制約:
- selection targetはすべて`project_id`と同一Projectに属さなければならない。
- Analysis Viewはselected Dataset Versionと互換でなければならない。
- Dataset Version切替時にAnalysis Viewが非互換ならAnalysis View selectionを解除する。

### 3.16 WorkspaceAnnotation

定義: Project-scoped resourceに対する選択・判断・next actionを含むannotation。

| 属性 | PK | FK | データ型 | NOT NULL | その他制約 | 説明 |
| --- | --- | --- | --- | --- | --- | --- |
| `annotation_id` | 1 |  | UUID / VARCHAR(36) | 1 | 不変 | WorkspaceAnnotation識別子 |
| `project_id` |  | `Project.project_id` | UUID / VARCHAR(36) | 1 | INDEX, `ON DELETE RESTRICT` | 所属Project |
| `target_type` |  |  | VARCHAR(100) | 1 | target type allowlist | 対象Resource type |
| `target_id` |  |  | VARCHAR(100) | 1 | INDEX, polymorphic logical reference | 対象Resource ID |
| `statement` |  |  | TEXT | 1 |  | statement |
| `rationale` |  |  | TEXT |  |  | rationale |
| `assumptions_json` |  |  | JSON | 1 | default `[]` | assumptions |
| `limitations_json` |  |  | JSON | 1 | default `[]` | limitations |
| `decision` |  |  | VARCHAR(20) |  | NULL / `SELECTED / REJECTED / DEFERRED` | 判断 |
| `next_actions_json` |  |  | JSON | 1 | default `[]` | next action |
| `revision_history_json` |  |  | JSON | 1 | default `[]` | revision history |
| `created_by` |  |  | VARCHAR(200) | 1 |  | 作成者 |
| `created_at` |  |  | TIMESTAMP WITH TIME ZONE | 1 |  | 作成日時 |
| `updated_at` |  |  | TIMESTAMP WITH TIME ZONE | 1 |  | 更新日時 |

設計判断・制約:
- `target_type`は`Project / ResearchContextVersion / AnalysisView / AnalysisSpecification / Execution / Result / GraphVersion`に限定する。
- `target_id`はpolymorphic logical referenceであり、target_typeと組にして解決する。

### 3.17 ExportBundle

定義: 複数Resultを再配布・共有可能なmanifest/binaryとして固定したexport。

| 属性 | PK | FK | データ型 | NOT NULL | その他制約 | 説明 |
| --- | --- | --- | --- | --- | --- | --- |
| `export_id` | 1 |  | UUID / VARCHAR(36) | 1 | 不変 | Export識別子 |
| `project_id` |  | `Project.project_id` | UUID / VARCHAR(36) | 1 | INDEX, `ON DELETE RESTRICT` | 所属Project |
| `schema_version` |  |  | VARCHAR(100) | 1 | default `ariadne-export-manifest/1` | manifest schema |
| `result_ids_json` |  |  | JSON | 1 | 同一Project Resultのみ | export対象Result ID一覧 |
| `object_key` |  |  | TEXT | 1 | UNIQUE | export object所在 |
| `content_hash` |  |  | VARCHAR(64) | 1 |  | 内容hash |
| `media_type` |  |  | VARCHAR(100) | 1 |  | MIME type |
| `size_bytes` |  |  | BIGINT | 1 | `>= 0` | byte数 |
| `manifest_summary_json` |  |  | JSON | 1 |  | manifest summary |
| `created_by` |  |  | VARCHAR(200) | 1 |  | 作成者 |
| `created_at` |  |  | TIMESTAMP WITH TIME ZONE | 1 |  | 作成日時 |

設計判断・制約:
- ExportBundleは生成後に上書きしない。
- `result_ids_json`の各Resultは同一Projectに属さなければならない。

### 3.18 LineageEdge

定義: Resource間のsemantic relationを明示的・append-onlyに保持するcanonical lineage edge。

| 属性 | PK | FK | データ型 | NOT NULL | その他制約 | 説明 |
| --- | --- | --- | --- | --- | --- | --- |
| `lineage_edge_id` | 1 |  | UUID / VARCHAR(36) | 1 | 不変 | LineageEdge識別子 |
| `project_id` |  | `Project.project_id` | UUID / VARCHAR(36) | 1 | INDEX, `ON DELETE RESTRICT` | 所属Project |
| `source_type` |  |  | VARCHAR(100) | 1 | polymorphic source type | source Resource type |
| `source_id` |  |  | VARCHAR(100) | 1 | polymorphic logical reference | source Resource ID |
| `relation_type` |  |  | VARCHAR(100) | 1 | relation allowlist / authority | semantic relation |
| `target_type` |  |  | VARCHAR(100) | 1 | polymorphic target type | target Resource type |
| `target_id` |  |  | VARCHAR(100) | 1 | polymorphic logical reference | target Resource ID |
| `evidence_json` |  |  | JSON | 1 | default `{}` | relation evidence |
| `created_by` |  |  | VARCHAR(200) | 1 |  | 作成者 |
| `created_at` |  |  | TIMESTAMP WITH TIME ZONE | 1 |  | 作成日時 |

設計判断・制約:
- (`source_type`,`source_id`,`relation_type`,`target_type`,`target_id`)を一意とする。
- source/targetは同一Project境界内で解決する。
- LineageEdgeをUI表示時の推測で生成せず、Command受付・Result/Resource生成時に明示保存する。
