# 21_14_entity_result_artifact_lineage

**Status:** `RD02_STRUCTURAL_WORKING_COPY / E11_NOT_PUBLISHED`; original ID, level and state retained.  
**Source blob:** `72903b9ad48b5b7edabaa7bb1c2cace42aa46ce7`.

---

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


## 98. RD-04：要求の論理データ制約の受入・Trace

**Status:** `DESIGN_CONSTRAINT_MIGRATION / OWNER_CONTENT_REVIEW_PENDING`。以下はRD-04で抽象化した元要件のうち、データ定義・同一性・来歴・正本性に関係する条項を論理設計側に残したもの。原文は出典保証目的で保持する。現行コードで検証済みと主張しない。

### 98.FR-090. FR-090（SPLIT）

- 元要件（設計上の拘束を含む）：canonical Resultはexecution/stage relation、result type、scientific status、summary/payload/diagnostics/warningsを保持する。family/generic schema_versionをResult direct fieldへ重複保持しない
- RD改訂後の要求：分析結果について実行・科学的状態・診断・警告を一貫して参照できる
- Trace：`FR-090`; Status=`ACTIVE`; Implementation=`IMPLEMENTED`; [逐条レビュー](../95_rd04_fr_application_review.md)

### 98.FR-091. FR-091（SPLIT）

- 元要件（設計上の拘束を含む）：Result payloadはFamily・Type別Schemaで検証する
- RD改訂後の要求：結果の種類に適合した検証を行い不正な結果を受け入れない
- Trace：`FR-091`; Status=`ACTIVE`; Implementation=`IMPLEMENTED`; [逐条レビュー](../95_rd04_fr_application_review.md)

### 98.FR-092. FR-092（SPLIT）

- 元要件（設計上の拘束を含む）：canonical Artifactはproject/execution/stage/result relation、artifact type/scope、object_key、media type、hash、size、metadataを保持する。family/generic schema_versionをdirect fieldへ重複保持しない
- RD改訂後の要求：成果物について帰属先・種類・同一性・取得情報を追跡できる
- Trace：`FR-092`; Status=`ACTIVE`; Implementation=`IMPLEMENTED`; [逐条レビュー](../95_rd04_fr_application_review.md)

### 98.FR-095. FR-095（SPLIT）

- 元要件（設計上の拘束を含む）：ResultからResearchContextVersion、AnalysisSpecification、ExecutionPlan、Execution、StageExecution、DatasetVersion、AnalysisView、GraphVersion、input Result、base Execution、Artifactへ遡れるcanonical lineage read modelを提供する
- RD改訂後の要求：結果に影響した研究条件・データ・実行・上流結果・成果物を追跡できる
- Trace：`FR-095`; Status=`ACTIVE`; Implementation=`PARTIAL`; [逐条レビュー](../95_rd04_fr_application_review.md)

### 98.NFR-002. NFR-002（SPLIT）

- 元要件（設計上の拘束を含む）：canonical lineage read modelでResearchContextVersion→AnalysisSpecification→ExecutionPlan→Execution→StageExecution→Result→Artifactを追跡し、DatasetVersion/AnalysisView/GraphVersion/input Result/base Executionも接続する
- RD改訂後の要求：研究条件から入力・計画・実行・結果・成果物までの追跡が可能である
- Trace：`NFR-002`; Status=`ACTIVE`; Implementation=`PARTIAL`; [逐条レビュー](../96_rd04_nfr_ar_application_review.md)
