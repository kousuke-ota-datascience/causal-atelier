# 21_15_entity_membership_workspace


---

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
