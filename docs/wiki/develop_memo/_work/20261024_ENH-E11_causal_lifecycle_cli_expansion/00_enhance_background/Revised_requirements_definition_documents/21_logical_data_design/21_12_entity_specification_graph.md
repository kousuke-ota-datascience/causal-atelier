# 21_12_entity_specification_graph

**Status:** `RD02_STRUCTURAL_WORKING_COPY / E11_NOT_PUBLISHED`; original ID, level and state retained.  
**Source blob:** `72903b9ad48b5b7edabaa7bb1c2cace42aa46ce7`.

---

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

**適用する論理データ制約（関連Requirement）**

- **`FR-045`**：Treatment / Outcome inferred typeを正規化文字列で保存し、外部型objectを永続化しない
- **`FR-051`**：同一immutable `dataset_version_id`の先行Exploratory Resultを用いたconfirmatory分析では`EXPLORATORY_REUSE_SAME_DATA` warningとevidence Result IDを保持する
- **`FR-054`**：Causal ResultからResearchContextVersion、AnalysisSpecification、ExecutionPlan、Execution、StageExecution、DatasetVersion/AnalysisView、GraphVersion、上流Result、Artifactへcanonical lineageで遡れる
