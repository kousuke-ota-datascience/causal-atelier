# 21_11_entity_dataset_view

**Status:** `RD02_STRUCTURAL_WORKING_COPY / E11_NOT_PUBLISHED`; original ID, level and state retained.  
**Source blob:** `72903b9ad48b5b7edabaa7bb1c2cace42aa46ce7`.

---

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
