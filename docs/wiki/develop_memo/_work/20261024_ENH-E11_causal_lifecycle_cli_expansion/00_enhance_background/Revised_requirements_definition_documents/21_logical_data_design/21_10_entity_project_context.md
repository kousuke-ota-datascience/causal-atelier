# 21_10_entity_project_context


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

**適用する論理データ制約（関連Requirement）**

- **`FR-002`**：Projectはtopic、objective、memoを保持し、decision contextはversioned `ResearchContextVersion`の責務として保持する
- **`FR-006`**：Analysis Specificationは一つのResearch Context Versionを参照する
- **`FR-007`**：Executionは参照ResearchContextVersionを固定し、受付時のobjective/rationale等の再現に必要なsnapshot metadata/hashを保持する。ResearchContext全体の重複保存を必須化しない
- **`FR-008`**：ResearchContextVersionから利用AnalysisSpecification、Execution、Resultへcanonical lineage/read modelで遡及・追跡できる
