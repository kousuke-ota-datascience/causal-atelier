# 21_10_entity_project_context

**Status:** `RD02_STRUCTURAL_WORKING_COPY / E11_NOT_PUBLISHED`; original ID, level and state retained.  
**Source blob:** `72903b9ad48b5b7edabaa7bb1c2cace42aa46ce7`.

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


## 98. RD-04：要求の論理データ制約の受入・Trace

**Status:** `DESIGN_CONSTRAINT_MIGRATION / OWNER_CONTENT_REVIEW_PENDING`。以下はRD-04で抽象化した元要件のうち、データ定義・同一性・来歴・正本性に関係する条項を論理設計側に残したもの。原文は出典保証目的で保持する。現行コードで検証済みと主張しない。

### 98.FR-002. FR-002（SPLIT）

- 元要件（設計上の拘束を含む）：Projectはtopic、objective、memoを保持し、decision contextはversioned `ResearchContextVersion`の責務として保持する
- RD改訂後の要求：Projectの研究目的と意思決定文脈を区別して保持・参照できる
- Trace：`FR-002`; Status=`ACTIVE`; Implementation=`IMPLEMENTED`; [逐条レビュー](../95_rd04_fr_application_review.md)

### 98.FR-006. FR-006（SPLIT）

- 元要件（設計上の拘束を含む）：Analysis Specificationは一つのResearch Context Versionを参照する
- RD改訂後の要求：分析仕様が参照する研究文脈の版を特定できる
- Trace：`FR-006`; Status=`ACTIVE`; Implementation=`IMPLEMENTED`; [逐条レビュー](../95_rd04_fr_application_review.md)

### 98.FR-007. FR-007（SPLIT）

- 元要件（設計上の拘束を含む）：Executionは参照ResearchContextVersionを固定し、受付時のobjective/rationale等の再現に必要なsnapshot metadata/hashを保持する。ResearchContext全体の重複保存を必須化しない
- RD改訂後の要求：分析実行時点の研究目的と理由を後から再現できる
- Trace：`FR-007`; Status=`ACTIVE`; Implementation=`IMPLEMENTED`; [逐条レビュー](../95_rd04_fr_application_review.md)

### 98.FR-008. FR-008（REWRITE_RD）

- 元要件（設計上の拘束を含む）：ResearchContextVersionから利用AnalysisSpecification、Execution、Resultへcanonical lineage/read modelで遡及・追跡できる
- RD改訂後の要求：研究文脈から分析仕様・実行・結果までの来歴を追跡できる
- Trace：`FR-008`; Status=`ACTIVE`; Implementation=`PARTIAL`; [逐条レビュー](../95_rd04_fr_application_review.md)
