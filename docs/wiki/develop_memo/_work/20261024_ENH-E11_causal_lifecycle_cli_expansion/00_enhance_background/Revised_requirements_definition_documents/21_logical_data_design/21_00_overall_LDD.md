<!-- ENH-E11 split working copy: not a formal approval. -->
# 21 — overall

**Status:** `STRUCTURAL_COPY_DRAFT` (existing baseline text, not E11 canonical publication)

**Source:** [21_logical_data_design.md](https://github.com/kousuke-ota-datascience/causal-atelier/blob/3ba5fe2465ec591f0da7f998c21a5241984b73dc/docs/wiki/requirement_definition/21_logical_data_design.md) · blob `72903b9ad48b5b7edabaa7bb1c2cace42aa46ce7`  
**Index:** [Revised document inventory](../README_00_Revised_requirements_definition_documents.md)

---

## 1. 設計方針

### 1.1 設計目的

本書は、Research Topic、Research Context、Dataset、Analysis View、三つのAnalysis Family、Workflow、Result、ArtifactおよびLineageを、実装技術から独立した論理Entity / Value / Projectionとして定義する。

論理Entity、Domain Entity、DB Table、API Resource、UI画面は一対一である必要はない。ただし、正本のidentity、version、状態、参照、cardinality、不変条件は各層で意味的に一致しなければならない。

### 1.2 基本原則

1. 主要な分析Resourceは一つのProject境界に所属する。
2. Dataset Version、FIXED済みResearch Context / Analysis View / Analysis Specification、Execution Plan、Result、Artifact等、再現性に関与するResourceは上書きしない。
3. 実行条件は参照IDだけでなくcanonical snapshot / hashを保持し、後から同一条件を検証できるようにする。
4. Analysis Family固有payloadは共通Envelopeとversioned schemaへ分離する。
5. Lineageは表示時に推測せず、Resource生成・Command受付時に明示保存する。
6. JSONへ外部library object、NaN、Infinity、非決定的表現を保存しない。
7. ResultとArtifactを分離し、科学的意味と物理生成物を混同しない。
8. Technical execution statusとscientific / analytical statusを分離する。
9. `AnalysisFamily`は既存domain discriminatorを再利用し、duplicate Family discriminatorを作らない。
10. Navigation Stageとruntime StageType / StageExecutionを別概念として扱う。
11. `NavigationStageDescriptor`、Current Family、Current Navigation Stageはpersistent Entityへ昇格させない。
12. Analysis Contextは既存Project-scoped selection/resourceの論理projectionとして扱い、専用persistent aggregateを新設しない。

### 1.3 論理モデルの構成要素

本書では、persistentなbusiness authorityを持つ`Domain Resource`と、Domain Resourceではないapplication / runtime / navigation上の論理概念を明確に区別する。

この分類は、UIやworkflow上に概念が存在することだけを理由にpersistent Entityを追加したり、navigation metadataをruntime lifecycleへ混入させたりすることを防ぐための設計境界である。

#### 1.3.1 Domain Resource

Domain Resourceは、独立したidentity、ownership、lifecycle、mutabilityまたは監査上のauthorityを持つ論理Resourceである。論理Resource、Domain Entity、DB Table、API Resource、UI画面は一対一である必要はない。

| Resource | Mutability | Primary ID | 責務 |
| --- | --- | --- | --- |
| Project | Mutable aggregate | `project_id` | Research TopicとProject境界 |
| Artifact | Immutable metadata | `artifact_id` | 物理生成物descriptor |
| DatasetVersion | Immutable | `dataset_version_id` | 入力Dataset version |
| ResearchContextVersion | DRAFT -> FIXED | `research_context_version_id` | 問題・問い・仮説・意思決定文脈 |
| AnalysisView | DRAFT -> FIXED | `analysis_view_id` | Datasetに対する分析用View |
| AnalysisSpecification | DRAFT -> FIXED | `analysis_specification_id` | Family固有分析仕様 |
| ExecutionPlan | Immutable | `execution_plan_id` | runtime Stage DAG |
| Execution | Stateful | `execution_id` | canonical execution |
| StageExecution | Stateful | `stage_execution_id` | runtime Stage実行状態 |
| StageAttempt | Append-only | `stage_attempt_id` | Stage retry / attempt履歴 |
| Result | Immutable | `result_id` | 科学的・分析的Result |
| GraphVersion | DRAFT -> FIXED | `graph_version_id` | causal graph version |
| Annotation | Mutable | `annotation_id` | Result / Graphへの注釈 |
| ProjectMembership | Mutable | `membership_id` | Project権限 |
| WorkspaceSelection | Mutable per user | `workspace_selection_id` | Analysis Context selection |
| WorkspaceAnnotation | Mutable with revision history | `annotation_id` | Project-scoped判断 / 注釈 |
| ExportBundle | Immutable | `export_id` | Result export |
| LineageEdge | Append-only | `lineage_edge_id` | semantic lineage relation |

Compatibility / transition用の`FamilyExecution / FamilyStageExecution / FamilyResult / FamilyArtifact`はhistorical read modelとして残り得るが、新規Product lifecycle writeの正本Domain Resourceではない。`IdempotencyRecord`はtechnical persistence recordでありbusiness Domain Resourceではない。

#### 1.3.2 Domain Resource外の論理概念

次の概念はAriadneの論理モデル上重要であるが、それ自体を独立persistent Domain Resourceとして扱わない。

| Concept | 種別 | 永続化 | 責務 |
| --- | --- | --- | --- |
| `AnalysisFamily` | Enum / domain discriminator | Resourceとしては不要 | Exploratory / Causal / Predictiveの分析Family識別 |
| Analysis Context | application-level logical projection | 専用aggregateを永続化しない | Current Project / Research Context / Dataset Version / Analysis Viewを一つの分析文脈として投影 |
| `StageType` | runtime value object | ExecutionPlan / StageExecutionの構成要素 | runtime Stage種別をnamespace / name / versionで識別 |
| `StageDefinition` | runtime value object | ExecutionPlan内 | runtime Stageのinput / output / parameter / resource policyを定義 |
| `StageBinding` | runtime value object | ExecutionPlan内 | runtime Stage間dependency / bindingを定義 |
| `NavigationStageDescriptor` | application metadata / immutable value | DB永続化しない | Family-local Stage ID、label、order等 |
| `FamilyNavigationDescriptor` | application metadata / immutable value | DB永続化しない | FamilyとStage catalog、default Stageの組 |
| Current Family | navigation state | DB永続化しない | 現在のanalysis Family context |
| Current Navigation Stage | navigation state | DB永続化しない | 現在のFamily-local work / view context |
| route representation | serialized navigation state | URL / browser history | Project / Family / Stageのdeep-link表現 |
| renderer binding | presentation mapping | code / config | `(family, stage)`から既存surface / use caseへのbinding |
| Operation Availability View | query / projection model | 専用Entityを原則作らない | 現在のContext / Resource状態からoperation可否を導出 |

詳細な非Entity modelは`## 4. 非Entityのデータモデル`で定義する。

#### 1.3.3 論理概念の分類原則

- 新規概念は、まず既存Domain Resourceの属性・関係・projectionとして自然に表現可能か確認する。
- 独立identity / lifecycle / mutability / audit authorityを持つ場合のみ、新規Domain Resource候補とする。
- enum / value object / descriptor / navigation state / query projectionを人工的にDomain Resourceへ昇格させない。
- runtime Entity / valueとnavigation metadataを同一型へ統合しない。
- UI上の分類・画面分割だけを理由にDB schema、persistent aggregate、cardinalityを変更しない。
- Analysis Contextは既存Project-scoped Resourceとselectionのprojectionであり、専用persistent aggregateを新設しない。
- Navigation StageはAnalysis Specificationのsemantic inputでもruntime lifecycle fieldでもないため、`AnalysisSpecification`、`ExecutionPlan`、`Execution`、`StageExecution`へnavigation fieldを追加しない。

### 1.4 型と制約の表記

- データ型は論理型を基本とし、必要に応じて現行の長さ制約を併記する。物理DB製品固有の実装差は詳細設計へ写像する。
- `PK`および`NOT NULL`欄の`1`は制約あり、空欄は制約なしを表す。
- `FK`欄には論理参照先Entityと属性を記載する。物理DBでFKを持たないpolymorphic/logical referenceは「その他制約」で明示する。
- Project配下Entity間の参照では、参照先が同一Projectに属することをDB制約またはApplication validationで保証する。
- current sourceとの照合で物理FKが未設定であっても、論理設計上reference authorityが明確な場合は論理FKとして記載し、物理実装差を注記する。
