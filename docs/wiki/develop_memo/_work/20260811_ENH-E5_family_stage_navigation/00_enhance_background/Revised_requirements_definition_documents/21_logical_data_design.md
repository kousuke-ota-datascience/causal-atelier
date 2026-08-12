# 21 論理データ設計

- 文書状態: `APPROVED`
- 文書種別: 現行論理データモデルのeffective snapshot
- 上位文書: `10_requirements_definition.md`
- current code照合対象: `src/ariadne/product/domain/`

## 1. 設計目的

本書は、Research Topic、Research Context、Dataset、三つのAnalysis Family、Workflow、ResultおよびLineageを、実装技術に依存しない論理Resourceとして定義する。

論理Resource、Domain Entity、DB Table、API Resource、UI画面は一対一である必要はない。ただし、正本の識別子、version、状態、参照制約および不変性は全層で一致させる。

本書では、persistent Domain Resourceと、Domain Resourceではないapplication/navigation上の論理概念を明確に区別する。Family / Navigation Stage導入に際して、UI上の分類を理由に既存Domain Resourceへ不要なfield/resourceを追加しない。

## 2. 基本原則

1. すべての主要Resourceは一つのProjectに所属する
2. Dataset Version、固定済みContext、固定済みView、固定済みSpecification、Plan、Resultは上書きしない
3. 実行条件は参照IDだけでなくcanonical snapshotとhashを保持する
4. Analysis Family固有payloadは共通Envelopeとversioned Schemaに分離する
5. Lineageは推測ではなく、Command受付・Result作成時に保存する
6. JSONへ外部library object、NaN、Infinity、非決定的表現を保存しない
7. ResultとArtifactを分離する
8. Technical statusとanalytical statusを分離する

9. `AnalysisFamily`は既存domain enum/discriminatorを再利用する。
10. `NavigationStageDescriptor`とCurrent Navigation Stateはpersistent Domain Resourceへ人工的に昇格させない。
11. Navigation Stageを`AnalysisSpecification`、`ExecutionPlan`、`Execution`、`StageExecution`へ追加しない。
12. Navigation Stageとruntime `StageType / StageDefinition / StageExecution`を別概念として扱う。

## 3. 論理モデルの構成要素

### 3.1 Domain Resource

| Resource | Mutability | Primary ID | 責務 |
| --- | --- | --- | --- |
| Project | Mutable aggregate | project_id | Research Topic、status、権限境界 |
| ResearchContextVersion | Immutable after FIXED | research_context_version_id | 問題、問い、仮説、意思決定文脈 |
| DatasetVersion | Immutable | dataset_version_id | 入力データ、schema、hash、profile |
| AnalysisView | Versioned | analysis_view_id | 行・列・加工・時間条件 |
| AnalysisSpecification | Versioned | analysis_specification_id | Family固有の問い・方法・評価基準 |
| ExecutionPlan | Immutable | execution_plan_id | Stage DAG、binding、version |
| Execution | Stateful | execution_id | Planの実行単位、snapshot、status |
| StageExecution | Stateful | stage_execution_id | Stage単位のstatusとattempt |
| Result | Immutable | result_id | Family / Type固有の論理結果 |
| Artifact | Immutable metadata | artifact_id | 物理生成物のdescriptorとhash |
| GraphVersion | Versioned | graph_version_id | Graph semantics、origin、nodes、edges |
| Annotation | Mutable | annotation_id | ResultまたはGraphVersionに対するstatement / rationale / assumptions / limitations |
| WorkspaceAnnotation | Mutable with revision history | annotation_id | Project-scopedな選択・判断・next actionを含むannotation |
| ProjectMembership | Mutable | membership_id | Project user role（OWNER / EDITOR / VIEWER） |
| WorkspaceSelection | Mutable per user | workspace_selection_id | Research Context / Dataset / Analysis Viewのworkspace選択状態 |
| ExportBundle | Immutable | export_id | Result集合のexport manifest / binary |
| LineageEdge | Append-only | lineage_edge_id | Resource間の明示的関係 |

Compatibility/transition read modelとして `FamilyExecution / FamilyStageExecution / FamilyResult / FamilyArtifact` が現行DBに残る。これらはhistorical/compatibility read modelであり、新規Product lifecycle writeの正本とはしない。

### 3.2 Domain Resource外の論理概念

| Concept | 種別 | 永続化 | 責務 |
| --- | --- | --- | --- |
| `AnalysisFamily` | Enum / domain discriminator | Resourceとしては不要 | Exploratory / Causal / Predictiveの分析Family識別 |
| `StageType` | runtime value object | ExecutionPlan / StageExecutionの構成要素 | runtime Stage種別をnamespace / name / versionで識別 |
| `StageDefinition` | runtime value object | ExecutionPlan内 | runtime Stageのinput/output/parameter/resource policyを定義 |
| `StageBinding` | runtime value object | ExecutionPlan内 | runtime Stage間dependency / bindingを定義 |
| `NavigationStageDescriptor` | application metadata / immutable value | DB永続化しない | Family-local Stage ID、label、order等 |
| `FamilyNavigationDescriptor` | application metadata / immutable value | DB永続化しない | FamilyとStage catalog、default Stageの組 |
| Current Family | navigation state | DB永続化しない | 現在のglobal analytical context |
| Current Navigation Stage | navigation state | DB永続化しない | 現在のFamily-local work/view context |
| route representation | serialized navigation state | URL/history | Project / Family / Stageのdeep-link表現 |
| renderer binding | presentation mapping | code/config | `(family, stage)`から既存surface / use caseへのbinding |

#### 3.2.1 AnalysisFamilyの既存Domain Resourceとの関係

current sourceでは`AnalysisSpecification.analysis_family: AnalysisFamily`が既に存在し、Familyに応じてfamily-specific schemaを検証する。`ExecutionPlan`および`Execution`も`analysis_family`を保持する。したがってFamily discriminatorを重複field/enumとして追加しない。

#### 3.2.2 Navigation Stageの位置づけ

Navigation StageはAnalysis Specificationのsemantic inputでもruntime lifecycle fieldでもない。次のようなfieldを追加しない。

```text
AnalysisSpecification.navigation_stage
ExecutionPlan.navigation_stage
Execution.current_navigation_stage
StageExecution.navigation_stage
```

#### 3.2.3 Navigation catalog authority

Family-local Navigation catalogはpersistent Resourceではなく、各Family Capabilityが所有するimmutable `FamilyNavigationDescriptor`をapplication/interface aggregatorが集約する。

Canonical metadata interface:

```text
GET /api/v1/navigation/analysis
schema = analysis-navigation/1
```

`analysis-navigation/1`はpresentation/application metadata schemaであり、scientific generic `SchemaRegistry`へ登録しない。

Frozen catalog:

| Family | slug | default_stage_id | stage_id |
| --- | --- | --- | --- |
| EXPLORATORY | `exploratory` | `profile` | `profile`, `data-quality`, `distribution`, `relationships`, `comparison`, `findings` |
| PREDICTIVE | `predictive` | `setup` | `setup`, `train`, `predict`, `metrics`, `explainability`, `model-management` |
| CAUSAL | `causal` | `setup` | `setup`, `discovery`, `identification`, `estimation`, `effects`, `diagnostics`, `sensitivity` |

Current Family / Navigation Stageはcanonical route `/projects/{project_id}/analysis/{family_slug}/{stage_slug}`からresolveする。Navigation catalogはruntime Stage生成authorityを持たない。

### 3.3 論理概念の分類原則

- 新規概念はまず既存Domain Resourceの属性・関係として自然に表現可能か確認する。
- 独立identity / lifecycle / mutabilityを持つ場合のみ新規Domain Resource候補とする。
- enum / value / descriptor / navigation stateを人工的にDomain Resourceへ昇格させない。
- runtime entityとnavigation metadataを同一型へ統合しない。
- UI表示分類だけを理由にDB schemaを追加しない。

## 4. Domain Resource関係モデル

Canonical persistent authorityの主要関係:

```text
Project
├── ResearchContextVersion
├── DatasetVersion
│   └── AnalysisView
├── AnalysisSpecification
│   └── ExecutionPlan
├── GraphVersion
├── Execution
│   ├── StageExecution
│   │   └── StageAttempt
│   ├── Result
│   └── Artifact
├── Annotation
├── ProjectMembership
├── WorkspaceSelection
├── WorkspaceAnnotation
├── ExportBundle
└── LineageEdge
```

主要参照:

```text
DatasetVersion.source_artifact_id -> Artifact(SOURCE)
AnalysisSpecification -> ResearchContextVersion
AnalysisSpecification -> DatasetVersion
AnalysisSpecification -> optional AnalysisView
ExecutionPlan.analysis_specification_id -> AnalysisSpecification identity
Execution -> DatasetVersion
Execution -> optional GraphVersion / upstream Result
StageExecution -> Execution
StageAttempt -> StageExecution
Result -> Execution
STAGE_RESULT -> StageExecution
Artifact(EXECUTION_OUTPUT) -> Execution; optional StageExecution / Result
GraphVersion -> optional Result / parent GraphVersion
Annotation -> exactly one of Result / GraphVersion
WorkspaceAnnotation -> Project-scoped target resource
LineageEdge -> same-Project source/target
```

重要なcurrent implementation boundary:

- Canonical `Execution`に`execution_plan_id` FK/columnはない。
- Predictive/Exploratory等のcurrent application pathでは`analysis_spec_json`に`analysis_specification_id / analysis_view_id / execution_plan_id`等のmetadataを埋め込む場合がある。
- `FamilyExecution / FamilyStageExecution / FamilyResult / FamilyArtifact`はhistorical/compatibility read modelとして残るが、新規canonical lifecycle write authorityではない。

### 4.1 AnalysisFamily relation

`AnalysisFamily`はResourceではないが、次のcurrent resource discriminatorとして現れる。

```text
AnalysisSpecification.analysis_family
ExecutionPlan.analysis_family
Execution.analysis_family
```

`AnalysisSpecification.analysis_family`の許容値は`EXPLORATORY / CAUSAL / PREDICTIVE`である。Family discriminatorを重複field/enumとして追加しない。

### 4.2 Supporting Logical Concept relation

Persistent Resource relationとは分離して、navigation側は次の論理関係として扱う。

```text
AnalysisFamily
   │
   ▼
FamilyNavigationDescriptor
   │
   └─ NavigationStageDescriptor*
            │
            └─ presentation / use-case binding
```

この関係をER的なpersistent relationへ変換しない。

## 5. Domain Resource定義

### 5.1 Project

現行Domain Entity / persistenceの有効fieldは次のとおり。

| Field | Type | Required | 制約 |
| --- | --- | --- | --- |
| project_id | UUID/string(36) | 1 | 不変 |
| name | string(200) | 1 | 表示名 |
| topic | text | 0 | Research Topic |
| objective | text | 0 | 分析・意思決定目的 |
| memo | text | 0 | 補足 |
| status | ACTIVE / ARCHIVED | 1 | ACTIVEのみ更新可能 |
| created_at | datetime | 1 | 生成時刻 |
| updated_at | datetime | 1 | 更新時刻 |

`Project`自身には`decision_context_json`、`created_by`、`updated_by`を持たない。意思決定文脈は`ResearchContextVersion.decision_context_json`へ保持する。

Project archiveは論理削除であり、`ACTIVE -> ARCHIVED`のみを許可する。archive後も子ResourceとLineageを保持する。

### 5.2 ResearchContextVersion

#### 5.2.1 Field

| Field | Type | Required | 説明 |
| --- | --- | --- | --- |
| research_context_version_id | UUID | 1 | Version ID |
| project_id | UUID | 1 | 所属Project |
| context_key | string | 1 | 同一Context系列 |
| version_number | integer | 1 | Project / context_key内で正のversion |
| status | DRAFT / FIXED | 1 | FIXED後不変 |
| schema_version | `research-context/1` | 1 | versioned schema |
| problem_statement | text | 1 | 解決対象 |
| research_questions_json | array | 1 | 一つ以上の問い |
| significance | text | 0 | 重要性 |
| hypotheses_json | array | 0 | 仮説 |
| decision_context_json | object | 0 | 意思決定用途 |
| relations_json | array | 1 | 他Context Versionとの関係。default empty |
| canonical_hash | sha256 / null | 0 | canonical content hash |
| created_by | actor string | 1 | 作成者 |
| created_at | datetime | 1 | 作成時刻 |
| fixed_at | datetime / null | 0 | FIXED化時刻 |

#### 5.2.2 Relation

許可relation:

- `REFINES`
- `DERIVED_FROM`
- `SUPERSEDES`
- `RELATED_TO`

relation targetはFIX時に同一Project内の`ResearchContextVersion`として解決し、自己参照を禁止する。Planning baselineではrelation graph全体に対する一般cycle検出は実装されていないため、「特定relationではcycleを禁止する」という追加制約をcurrent contractとして記載しない。

### 5.3 DatasetVersion

現行Resourceはraw Datasetを`Artifact`へ保存し、そのArtifactを`source_artifact_id`で一意に参照する。

| Field | Type | Required | 説明 |
| --- | --- | --- | --- |
| dataset_version_id | UUID/string(36) | 1 | 不変ID |
| project_id | UUID/string(36) | 1 | 所属Project |
| source_artifact_id | UUID/string(36) | 1 | SOURCE Artifact。DB上unique |
| dataset_key | string(100) | 1 | Dataset系列 |
| name | string(200) | 1 | 表示名 |
| version_label | string(100) | 1 | 利用者label |
| content_hash | string(128) | 1 | content hash |
| schema_json | object | 1 | column -> logical type |
| profile_summary_json | object | 1 | profile summary。default `{}` |
| row_count | integer >= 0 | 1 | 行数 |
| column_count | integer >= 0 | 1 | 列数 |
| source_note | text | 0 | 出所 |
| created_at | datetime | 1 | 生成時刻 |

Unique constraint:

- `(project_id, dataset_key, version_label)`
- `(project_id, dataset_key, content_hash)`
- `source_artifact_id`

`DatasetVersion`自身に`created_by` fieldはない。

### 5.4 AnalysisView

#### 5.4.1 Envelope

```json
{
  "schema_version": "analysis-view/1",
  "source_dataset_version_id": "uuid",
  "row_filter": [],
  "selected_columns": [],
  "derived_columns": [],
  "missing_value_policy": {},
  "time_cutoff": null,
  "sampling": null
}
```

#### 5.4.2 制約

- filter operatorとvalue typeをcolumn logical typeへ整合させる
- selected columnとderived expressionの参照列が存在する
- derived column名が重複しない
- 非決定的関数、外部I/O、任意コードを禁止する
- time cutoffは予測時点・因果time zeroと独立に保存し、Specification側で意味付けする
- 固定時にcanonical JSONとhashを生成する

#### 5.4.3 ENH-E5 typed filter compatibility

current operator taxonomyは変更しない。source Dataset logical type × operator × valueのcompatibilityは次をcanonical validation ruleとする。

| Logical Type | Allowed operators | Value contract |
| --- | --- | --- |
| BOOLEAN | `EQ, NE, IN, NOT_IN, IS_NULL, NOT_NULL` | boolean。`IN/NOT_IN`はboolean list |
| INTEGER | `EQ, NE, LT, LTE, GT, GTE, IN, NOT_IN, IS_NULL, NOT_NULL` | integer。booleanはintegerとして受理しない |
| REAL | `EQ, NE, LT, LTE, GT, GTE, IN, NOT_IN, IS_NULL, NOT_NULL` | finite int/float。booleanは禁止 |
| DATETIME | `EQ, NE, LT, LTE, GT, GTE, IN, NOT_IN, IS_NULL, NOT_NULL` | ISO-8601 string |
| TEXT | `EQ, NE, IN, NOT_IN, IS_NULL, NOT_NULL` | string。lexical orderingは提供しない |
| OTHER | `IS_NULL, NOT_NULL` | valueなし |

追加invariant:

- `IS_NULL / NOT_NULL`はvalueを持たない。
- `IN / NOT_IN`はnon-empty listを要求する。
- `time_cutoff`はDATETIME columnと`LT / LTE` semanticsのみ。
- source logical typeを解決できない場合はvalidation successにしない。
- mismatchはstable code `FILTER_TYPE_MISMATCH`。
- create/update/validate/fixで同じcompatibility validatorを利用する。
- new expression language、derived expressionのfull static typing、Family-specific typingはENH-E5 scope外。

AnalysisView persistent envelope/schema fieldはこのvalidation追加を理由に変更しない。

### 5.5 AnalysisSpecification

#### 5.5.1 共通Envelope

```json
{
  "schema_version": "analysis-specification/1",
  "analysis_family": "EXPLORATORY | CAUSAL | PREDICTIVE",
  "research_context_version_id": "uuid",
  "dataset_version_id": "uuid",
  "analysis_view_id": "uuid-or-null",
  "analysis_mode": "EXPLORATORY | CONFIRMATORY",
  "family_spec_schema_version": "...",
  "family_spec": {},
  "revision_context": null,
  "warnings": []
}
```

共通Envelopeの固定後、family_specを上書きしない。

#### 5.5.1a Exploratory handoff DRAFT contract

Exploratory ResultからCausal/Predictiveへhandoffする場合、canonical `AnalysisSpecification`を**DRAFTとしてpersist**する。

- target `analysis_family`: `CAUSAL`または`PREDICTIVE`
- `analysis_mode`: requestで`EXPLORATORY / CONFIRMATORY`を明示
- `dataset_version_id / analysis_view_id`: source Result lineageからderiveし、arbitrary overrideしない
- `research_context_version_id`: source lineageから一意にderiveできる場合は継承し、曖昧ならrequestで要求
- DRAFTではfamily_specの未完成を許容する
- source Resultからtarget AnalysisSpecificationへsemantic `MOTIVATED` edgeを保存する
- auto FIX / auto Executionは行わない
- same immutable `dataset_version_id`でconfirmatory analysisへhandoffする場合は`EXPLORATORY_REUSE_SAME_DATA` warningを付与する

Explore stateからAnalysisView DRAFTへ持ち込むのは`row_filter / selected_columns / derived_columns / missing_value_policy / time_cutoff / sampling`のみである。chart mark/encoding/panel layout等のpresentation-only stateはAnalysisViewへ押し込まない。

#### 5.5.2 Exploratory Schema

`exploratory-analysis-spec/1`:

- operation: `PROFILE | DISTRIBUTION | ASSOCIATION | GROUP_SUMMARY | TIME_TREND | CHART`
- columns
- grouping
- aggregation
- chart encoding
- filter / sampling reference
- expected output type

#### 5.5.3 Causal Schema

`causal-analysis-spec/2`を正規Schemaとする。必須構造:

- analysis_mode
- research_context
- causal_question
- causal_design
- operation_spec
- validation_override
- optional revision_context
- optional scientific_warnings

Operationは`DISCOVERY | IDENTIFICATION | ESTIMATION | REFUTATION | SENSITIVITY`である。未知Fieldをrejectする。

#### 5.5.4 Predictive Schema

`predictive-analysis-spec/1`:

- task_type: `BINARY_CLASSIFICATION | REGRESSION`
- prediction_question
  - prediction_unit
  - target
  - prediction_time
  - horizon
  - intended_use
  - deployment_population
- feature_spec
  - feature_columns
  - availability_cutoff
  - excluded_columns
- split_spec
  - strategy
  - train / validation / test ratioまたはcutoff
  - group_column
  - stratify
  - seed
- preprocessing_spec
- model_spec
- tuning_spec
- evaluation_spec
- explanation_spec

#### 5.5.5 Family discriminator / Navigation境界

- `analysis_family`は既存fieldを再利用する。duplicate Family discriminatorを追加しない。
- Navigation StageはAnalysis Specificationの問い・方法・評価基準ではないためfieldへ追加しない。

### 5.6 ExecutionPlan

| Field | Type | Required | 説明 |
| --- | --- | --- | --- |
| execution_plan_id | UUID | 1 | 不変ID |
| project_id | UUID | 1 | 所属Project |
| analysis_specification_id | UUID | 1 | 入力Specification |
| analysis_family | enum | 1 | Family |
| plan_schema_version | string | 1 | `execution-plan/1` |
| planner_id / planner_version | string | 1 | 生成Planner |
| stages_json | array | 1 | Stage定義 |
| dependencies_json | array | 1 | DAG edgeとbinding |
| plan_hash | sha256 | 1 | canonical hash |
| created_at | datetime | 1 | 生成時刻 |

#### 5.6.1 Runtime StageDefinition / StageType

Stage定義:

```json
{
  "stage_key": "train",
  "stage_type": {"namespace":"predictive","name":"train","version":"1"},
  "input_contract": {},
  "output_contract": {},
  "parameters": {},
  "resource_policy": {},
  "enabled": true
}
```

NavigationStageDescriptor、Current Family、Current Navigation Stage、browser routeをExecutionPlanへ含めない。

### 5.7 Execution

Canonical `Execution`のlogical/persistent fieldは次のとおりである。

| Field | 説明 |
| --- | --- |
| execution_id | 実行ID |
| project_id | 所属Project |
| analysis_family | `EXPLORATORY / CAUSAL / PREDICTIVE` |
| dataset_version_id | 入力Dataset |
| input_graph_version_id | optional Graph input |
| input_result_id | optional upstream Result input |
| batch_key | batch識別 |
| operation | `DISCOVERY / IDENTIFICATION / ESTIMATION / REFUTATION / SENSITIVITY` |
| objective_snapshot / rationale_snapshot | 受付時説明snapshot |
| analysis_spec_json | 実行用analysis specification snapshot |
| algorithm_or_estimator | algorithm / estimator識別 |
| parameter_json | parameter snapshot |
| random_seed | optional seed |
| code_version | code version |
| runtime_version_json | runtime versions |
| snapshot_hash | 実行snapshot hash |
| snapshot_schema_version | snapshot schema version |
| status | QUEUED / RUNNING / SUCCEEDED / FAILED / CANCELLED |
| retry_count | technical retry回数 |
| last_error_summary | latest technical error |
| requested_by / requested_at | submit audit |
| started_at / finished_at | lifecycle time |
| base_execution_id | rerun/revision起点 |
| revision_kind | `RERUN / REVISED`またはnull |
| change_reason | revision reason |
| lease_owner / lease_expires_at | Worker lease authority |

`runtime_version_json`はENH-E5 targetで最低限次の再構築metadataを保持する。

```text
ariadne_code_version
python_version
platform_system
platform_release
machine
libraries
```

`libraries`は実際にregistered/used runner dependencyとして利用したscientific library versionを保存する。少なくとも共通依存（例: numpy/pandas）と、Predictive利用時のscikit-learn等の実利用dependencyをcaptureする。version取得だけを目的にfuture optional dependencyをimportしない。これはbit-for-bit numerical identityの保証ではない。

Canonical `Execution`には`execution_plan_id` columnを持たない。Predictive/Exploratoryの一部current application pathでは、`analysis_spec_json`内のmetadataとして`analysis_specification_id` / `analysis_view_id` / `execution_plan_id`を保持し得るが、これはcanonical Executionの独立FK fieldではない。

Planning baseline DB constraintにおけるoperation別input invariant:

| operation | input_graph_version_id | input_result_id |
| --- | --- | --- |
| `DISCOVERY` | null | null |
| `IDENTIFICATION` | non-null | null |
| `ESTIMATION` | non-null | 原則non-null。ただし`legacy-product-snapshot/1` compatibility snapshotではnullを許容 |
| `REFUTATION` | non-null | non-null |
| `SENSITIVITY` | non-null | non-null |

このinput invariantはCausalのcanonical Execution prerequisiteであり、Navigation Stageの順序や完了状態を保存するものではない。

`changed_dimensions` fieldおよびCurrent Navigation Stageを保持しない。

### 5.8 StageExecution

Canonical `StageExecution`とappend-only `StageAttempt`を分ける。

`StageExecution`:

| Field | 説明 |
| --- | --- |
| stage_execution_id | Stage実行ID |
| execution_id | 親canonical Execution |
| stage_key | Execution内Stage key |
| stage_type_json | `StageType(namespace, name, version)` serialization |
| ordinal | plan materialization order |
| dependencies_json | dependency stage keys |
| status | PENDING / READY / RUNNING / SUCCEEDED / FAILED / SKIPPED_DUE_TO_PREREQUISITE / CANCELLED |
| input_binding_json | 解決済み入力 |
| output_binding_json | 生成output |
| last_error_json | latest technical error |
| started_at / finished_at | lifecycle time |
| created_at | materialization time |

Unique constraint: `(execution_id, stage_key)`。

`StageAttempt`:

| Field | 説明 |
| --- | --- |
| stage_attempt_id | Attempt ID |
| stage_execution_id | 親StageExecution |
| attempt_number | 1始まり。StageExecution内unique |
| worker_id | 実行worker |
| effective_random_seed | stochastic Stageが実際に用いたseed。deterministic Stageはnull |
| started_at / finished_at | attempt time |
| error_json | optional error |

`attempt_count`をStageExecutionの独立fieldとして保存しない。回数はStageAttempt履歴から導出する。

`effective_random_seed`はENH-E5のpersistent migration対象である。stochastic Stageではactual seedをattempt単位で保存し、同一logical Stageのtechnical retryでは同じeffective seedを再利用する。

Navigation Stage / browser routeをStageExecutionまたはStageAttemptへ保持しない。

### 5.9 Result

#### 5.9.1 Canonical Result

Canonical `Result`はFamily横断のpersistent result authorityであり、次のfieldを持つ。

```text
result_id
execution_id
result_level: EXECUTION_RESULT | STAGE_RESULT
stage_execution_id: optional
result_type: ResultType
scientific_status: ScientificStatus
summary_json
payload_json
diagnostics_json
warning_json
created_at
```

Ownership invariant:

- `EXECUTION_RESULT`では`stage_execution_id == null`
- `STAGE_RESULT`では`stage_execution_id != null`

Canonical Result自体には`project_id`、`analysis_family`、汎用`schema_version`、`analytical_status`という別fieldを持たない。Project / Familyは親Executionから解決し、status field名は`scientific_status`である。

一方、移行互換用の`FamilyResult` read modelは`project_id / analysis_family / schema_version / analytical_status`を保持する。これはhistorical/compatibility projectionであり、canonical Result ownershipと混同しない。

#### 5.9.2 Family別Result Type

| Family | Result Type |
| --- | --- |
| EXPLORATORY | DATA_PROFILE_RESULT、DISTRIBUTION_RESULT、ASSOCIATION_RESULT、GROUP_SUMMARY_RESULT、CHART_RESULT |
| CAUSAL | DISCOVERY_GRAPH_RESULT、IDENTIFICATION_RESULT、DATA_ELIGIBILITY_RESULT、TREATMENT_EFFECT_RESULT、DIAGNOSTICS_RESULT、REFUTATION_RESULT、SENSITIVITY_RESULT |
| PREDICTIVE | SPLIT_RESULT、TRAINING_RESULT、EVALUATION_RESULT、ERROR_ANALYSIS_RESULT、PREDICTIVE_EXPLANATION_RESULT、MODEL_CARD_RESULT |

Result Typeごとに許可analytical statusをSchemaで定義する。

#### 5.9.3 Causal Result Status

| Result Type | Allowed analytical status |
| --- | --- |
| DISCOVERY_GRAPH_RESULT | GENERATED / GENERATED_WITH_WARNINGS / UNRELIABLE |
| IDENTIFICATION_RESULT | IDENTIFIED / NOT_IDENTIFIED / PARTIALLY_IDENTIFIED / REQUIRES_REVIEW |
| DATA_ELIGIBILITY_RESULT | PASS / WARN / FAIL |
| TREATMENT_EFFECT_RESULT | ESTIMATED / INSUFFICIENT_OVERLAP / INSUFFICIENT_SAMPLE / ESTIMATION_UNRELIABLE / REQUIRES_REVIEW |
| DIAGNOSTICS_RESULT | PASS / WARN / FAIL |
| REFUTATION_RESULT | NO_FAILURE_DETECTED / FAILURE_DETECTED / INCONCLUSIVE |
| SENSITIVITY_RESULT | ROBUST / FRAGILE / INCONCLUSIVE |

#### 5.9.4 Predictive Result Status

| Result Type | Allowed analytical status |
| --- | --- |
| SPLIT_RESULT | PASS |
| TRAINING_RESULT | TRAINED / TRAINED_WITH_WARNINGS |
| EVALUATION_RESULT | EVALUATED / INSUFFICIENT_TEST_SAMPLE |
| ERROR_ANALYSIS_RESULT | GENERATED / GENERATED_WITH_WARNINGS |
| PREDICTIVE_EXPLANATION_RESULT | GENERATED / GENERATED_WITH_WARNINGS / NOT_APPLICABLE |
| MODEL_CARD_RESULT | GENERATED / GENERATED_WITH_WARNINGS |

#### 5.9.5 Exploratory Result Status

Exploratory Result（`DATA_PROFILE_RESULT / DISTRIBUTION_RESULT / ASSOCIATION_RESULT / GROUP_SUMMARY_RESULT / CHART_RESULT`）は`GENERATED | GENERATED_WITH_WARNINGS`を許可する。`INSUFFICIENT_DATA`はPlanning baselineのpersistent `ScientificStatus`には存在しないため、必要な不足情報はwarning/payload等で表現する。

#### 5.9.6 Result semantic level and logical ownership

Resultは一つのcanonical Result ownership contractの下に属する。Result semantic levelはExecution-levelまたはStage-levelであり、これらは別のResult architectureではない。

- ExecutionResult: exactly one canonical Executionに属する。Stage ownershipはnot applicableであり、特定StageExecutionをrequired ownerとしない。Execution-level outcomeを表す。
- StageResult: exactly one canonical Executionに属し、exactly one StageExecutionをownerとする。参照StageExecutionは同じcanonical Executionに属さなければならない。特定persistent StageExecutionが生成したstage-level outcomeを表す。
- Execution→StageExecution: one Executionからzero-or-more StageExecution children。canonical workflowのlifecycleではrequired stagesが生成されるが、exact stage countはPlan/Workflow contractで定義する。
- Execution→Result: each Result has exactly one parent Execution。ResultのExecution-level/Stage-level multiplicityはworkflow contractで定義し、未承認の最大数を推測しない。
- StageExecution→StageResult: StageResultはexactly one StageExecution ownerを持つ。StageResultの生成可否・個数はstage contractに従う。
- Result→Artifact: Resultはzero-or-more Artifact metadata referencesを持ち得る。artifact-only outputの許可はfamily contractで明示し、同一physical objectのreuseはmetadata ownershipを複製しない。

physical storage locator、object key、URIはsemantic Result/Artifact identityではない。

#### 5.9.7 Relation-level lineage authority allowlist

current domainの`classify_lineage_authority(source_type, relation_type, target_type)`は、semantic tupleをclosed-by-defaultで分類する。同じrelation名でもsource/target typeが異なればauthorityは異なるため、relation名だけをgeneric write allowlistとして扱わない。

`TYPED_STRUCTURAL`として分類されるtupleは次である。これらをgeneric `LineageEdge`として二重writeしてはならない。

```text
Execution --GENERATED--> Result
Result --GENERATED--> Artifact
DatasetVersion --USED_INPUT--> Execution
AnalysisView --USED_INPUT--> Execution
Result --USED_INPUT--> Execution
Result --DERIVED_FROM--> GraphVersion
Artifact --DERIVED_FROM--> DatasetVersion
Execution --DERIVED_FROM--> Execution
Execution --REVISED_FROM--> Execution
```

`GENERIC_ONLY`としてgeneric persistenceがauthorityになるtupleは次である。

```text
Artifact --DERIVED_FROM--> Artifact
Result --SUMMARIZES--> Result
Result --SUMMARIZES--> Artifact
Result --MOTIVATED--> Execution
Result --MOTIVATED--> AnalysisSpecification
```

加えて、`Result`または`Artifact`をsourceとする`DOCUMENTS / SUPPORTED_BY / EVIDENCE_FOR`は、target typeが次のいずれかである場合に`GENERIC_ONLY`となる。

```text
Project
ResearchContextVersion
DatasetVersion
AnalysisView
AnalysisSpecification
Execution
Result
Artifact
GraphVersion
Annotation
```

`SELECTED / REJECTED`は、source typeが次のいずれかでtargetが`Annotation`の場合に`GENERIC_ONLY`となる。

```text
Project
ResearchContextVersion
AnalysisView
AnalysisSpecification
Execution
Result
GraphVersion
```

上記以外のsemantic tupleは`None`となり、generic persistenceは許可しない。`assert_generic_lineage_allowed(...)`は`GENERIC_ONLY`以外をrejectする。

なお、`Result --DERIVED_FROM--> GraphVersion`はcurrent authority classifierに実装されているtupleをそのまま記載している。GraphVersion側の`source_result_id`というfield名から逆向きrelationを推測して設計を変更しない。lineage authorityはclassifierのsemantic tupleを正とする。

Web APIのmanual lineage link入力は、このdomain allowlist全体ではなく、別途API schemaで制限されたrelation type subsetを受け付ける。domain authority classificationとAPI入力syntaxを同一contractとみなさない。

### 5.10 Artifact

Canonical `Artifact`:

| Field | 説明 |
| --- | --- |
| artifact_id | UUID |
| project_id | 所属Project |
| execution_id | optional canonical Execution |
| stage_execution_id | optional StageExecution |
| result_id | optional Result |
| artifact_scope | `SOURCE / EXECUTION_OUTPUT` |
| artifact_type | fixed `ArtifactType` enum |
| object_key | ArtifactStore key。DB上unique |
| content_hash | content hash |
| media_type | MIME |
| size_bytes | 0以上 |
| metadata_json | 任意metadata |
| created_at | 生成時刻 |

Scope invariant:

- `SOURCE`: execution/stage/result associationを持たない。
- `EXECUTION_OUTPUT`: `execution_id`必須。

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

Canonical Artifactに`family`、汎用`schema_version`、`storage_uri`、`deleted_at`、`deletion_reason` fieldはない。ArtifactStore上の位置は`object_key`で表現する。

移行互換用`FamilyArtifact`には`family / schema_version`が存在するが、canonical Artifact ownershipとは区別する。

### 5.11 GraphVersion

| Field | 説明 |
| --- | --- |
| graph_version_id | Graph Version ID |
| project_id | 所属Project |
| source_result_id | optional source Result |
| parent_graph_version_id | optional parent GraphVersion |
| designated_outcome_node | optional outcome node |
| name | 表示名 |
| graph_type | DAG / CPDAG / PAG |
| graph_origin | DISCOVERED / CONSTRAINT_ADJUSTED / USER_DEFINED / IMPORTED / USER_EDITED |
| provenance_json | provenance metadata |
| graph_json | graph document |
| content_hash | graph content hash |
| edit_rationale | optional edit rationale |
| status | DRAFT / FIXED |
| created_by / created_at | audit |

Origin reference invariant:

- `DISCOVERED`: `source_result_id`必須
- `CONSTRAINT_ADJUSTED`: source Resultまたはparent Graph必須
- `USER_DEFINED / IMPORTED`: source/parentを持たない
- `USER_EDITED`: parent Graph必須、source Resultなし

FIXED Graphは不変であり、編集はchild DRAFTを作る。

### 5.12 Annotation

現行実装には責務の異なる2種類のannotation persistenceが存在するため、混同しない。

#### 5.12.1 Canonical/simple Annotation

`Annotation`はResultまたはGraphVersionの**どちらか一方**のみを対象とする。

| Field | 説明 |
| --- | --- |
| annotation_id | ID |
| project_id | 所属Project |
| target_result_id | optional Result |
| target_graph_version_id | optional GraphVersion |
| statement | 本文 |
| rationale | optional rationale |
| assumptions_json | assumptions |
| limitations_json | limitations |
| created_by | 作成者 |
| created_at / updated_at | audit |

Target XOR constraintを持つ。`decision`、`next_actions`、revision history fieldは持たない。

#### 5.12.2 WorkspaceAnnotation

Project-scoped product closureで使用する`WorkspaceAnnotation`は次のtarget typeを許可する。

```text
Project
ResearchContextVersion
AnalysisView
AnalysisSpecification
Execution
Result
GraphVersion
```

主要field:

```text
annotation_id
project_id
target_type / target_id
statement
rationale
assumptions_json
limitations_json
decision: SELECTED | REJECTED | DEFERRED | null
next_actions_json
revision_history_json
created_by
created_at / updated_at
```

`Findings`でdecision/next actionまで扱う場合はWorkspaceAnnotationの責務と整合させる。新たなFinding Resourceを自動的に追加しない。

### 5.13 LineageEdge

Domain上は`ResourceRef`を介してsource/targetを表現する。

`ResourceRef`:

```text
resource_type
resource_id
project_id
schema_version: optional
content_hash: optional
```

`LineageEdge`:

```text
lineage_edge_id
project_id
source: ResourceRef
relation_type
target: ResourceRef
evidence
created_by
created_at
```

Persistenceではsource/targetを`source_type / source_id / target_type / target_id`へflattenし、次をuniqueとする。

```text
(source_type, source_id, relation_type, target_type, target_id)
```

同一Project外edgeを禁止する。

Domain relation typeには`USED_INPUT / GENERATED / DERIVED_FROM / REVISED_FROM / SUPPORTED_BY / EVIDENCE_FOR / DOCUMENTS / SUMMARIZES / MOTIVATED / SELECTED / REJECTED`が存在する。Product-closureのmanual lineage link APIが受け付けるsubsetは`USED_INPUT / GENERATED / DERIVED_FROM / REVISED_FROM / SUPPORTED_BY / MOTIVATED / SELECTED / REJECTED`である。

Result lineage projection APIには、typed structural relationshipを表示用に`CONTEXT_FOR / SOURCE_OF / INPUT_TO / HAS_ARTIFACT / HAS_ANNOTATION / RELATED_TO`等へ変換する既存projectionがある。これらの表示relation名とgeneric authoritative `LineageEdge.relation_type`を同一contractとみなさない。

#### 5.13.1 ENH-E5 canonical lineage completion

Canonical read modelは最低限次のstructural chainを再構成できなければならない。

```text
ResearchContextVersion
  ↓
AnalysisSpecification
  ↓
ExecutionPlan
  ↓
Execution
  ↓
StageExecution
  ↓
Result
  ↓
Artifact
```

さらに`DatasetVersion / AnalysisView / GraphVersion / input Result / base Execution`を接続する。

Authority rule:

- FK、snapshot identity、Execution/Stage/Result/Artifact relationからdeterministically導出できるstructural relationはread modelでprojectionする。
- 上記structural relationをgeneric `LineageEdge`へ二重persistしない。
- `MOTIVATED / SUPPORTED_BY / SELECTED / REJECTED`等のsemantic relationのみgeneric LineageEdgeを用いる。
- canonical usage/lineage queryはhistorical `Family*` compatibility read modelだけに依存しない。
- source type/identityを推測できないedgeを生成しない。

## 6. Canonicalization

現行generic canonicalizationは次の規則を持つ。

1. dataclassは`asdict`後に再帰normalizeする。
2. Enumは`.value`へ変換する。
3. UUID / datetimeは文字列へ変換する。
4. `None / str / bool / int`はそのまま扱う。
5. finite floatのみ許可し、`-0.0 / 0.0`は`0`、整数値floatはintegerへnormalizeする。
6. JSON object keyはstringのみ許可する。
7. list / tupleは**入力順を保持したまま**各要素をnormalizeする。generic layerでは意味のないlistを自動sortしない。
8. unsupported Python/library object、NaN、Infinityをrejectする。
9. JSON serializationは`ensure_ascii=False`, `sort_keys=True`, `separators=(",", ":")`, `allow_nan=False`とする。
10. canonical hashはcanonical bytesのSHA-256とする。

Schema固有のunknown-field rejectionは各validatorまたは`reject_unknown`で行う。generic canonicalizer自身が全schemaのunknown fieldを知るわけではない。

Navigation descriptorをAPI/cache向けにcanonicalizeする場合も、scientific snapshot/hashとは別contractとする。Analysis Specification / Execution Plan等のcanonical hashへbrowser pathname、active Family tab、Current Navigation Stage、display order/labelを混入させない。

## 7. Index / Unique Constraint

現行persistenceで確認できる主要constraintを以下に示す。

- Project: status CHECK `ACTIVE / ARCHIVED`。専用unique/indexなし。
- Artifact: `object_key` unique。`project_id / execution_id / stage_execution_id / result_id` index。scope/type/size CHECK。
- DatasetVersion:
  - unique `(project_id, dataset_key, version_label)`
  - unique `(project_id, dataset_key, content_hash)`
  - `source_artifact_id` unique
- ResearchContextVersion: unique `(project_id, context_key, version_number)`。
- AnalysisView: unique `(project_id, view_key, version_number)`。
- AnalysisSpecification: unique `(project_id, specification_key, version_number)`。
- ExecutionPlan: `plan_hash` unique。
- Execution: `project_id / analysis_family / dataset_version_id / input_graph_version_id / input_result_id / batch_key / status / base_execution_id`等をindex化。`(project_id, analysis_family, status, requested_at)`という単一composite indexは現行constraintではない。
- StageExecution:
  - unique `(execution_id, stage_key)`
  - unique `(stage_execution_id, execution_id)`
- StageAttempt: unique `(stage_execution_id, attempt_number)`。 ENH-E5で`effective_random_seed: int | null`を追加するが、unique constraintは追加しない。
- Result: unique `(result_id, execution_id)`。`execution_id / stage_execution_id` index。Result自身に`project_id / analysis_family`列はない。
- LineageEdge: unique `(source_type, source_id, relation_type, target_type, target_id)`。
- ProjectMembership: unique `(project_id, user_id)`、role CHECK `OWNER / EDITOR / VIEWER`。
- WorkspaceSelection: unique `(project_id, user_id)`。
- ExportBundle: `object_key` unique。

Navigation Stage ID / slugはFamily内で一意でなければならないが、DB unique constraintとしては実装しない。Family navigation descriptorはsupported `AnalysisFamily`ごとに一意とする。

## 8. Schema Reader Contract

現行`SchemaRegistry`は**`schema_version`文字列のみ**をkeyとしてvalidatorを登録・解決する。

```text
register(schema_version, validator)
validate(schema_version, payload)
canonicalize(schema_version, payload)
hash(schema_version, payload)
```

- duplicate schema version registrationはrejectする。
- unknown schema versionは`UnsupportedSchemaVersion`とする。
- payloadがMappingでない場合は`InvalidSchema`とする。
- validatorがnormalized mappingを返した場合はそれを採用し、`None`なら入力payloadを採用する。

`resource_type + schema_version`の複合key registryは現行contractではない。

Schema versionを直接持つ主なversioned JSON resourceにはResearchContextVersion、AnalysisView、AnalysisSpecification、ExecutionPlan等がある。一方、canonical `Result`とcanonical `Artifact`には共通`schema_version` fieldを直接持たない。Runner境界の`ResultDraft / ArtifactDraft`や移行互換`FamilyResult / FamilyArtifact`にはschema versionが存在するため、runner draft / compatibility projectionとcanonical persistence entityを区別する。

Navigation metadataに`analysis-navigation/1`はbackend read-only Navigation metadata contractとして利用するが、scientific generic `SchemaRegistry`へ登録しない。Family Capability descriptor / application-interface aggregatorがownershipを持ち、Execution Stage schemaとは独立する。

## 20. CHANGE LOG

### 20.4. ENH-E4 Canonical Execution Architecture

- Canonical Execution、persistent StageExecution、Result semantic level、Artifact ownership、typed/generic lineage authorityを論理データモデルへ統合した。
- Analysis Specification / Execution Plan / Result / Artifact descriptorのversioned schema reader contractを確立した。

### 20.5. ENH-E5 Family × Navigation Stage Application Architecture

- 既存`AnalysisFamily`をFamily discriminatorとして再利用する。
- Navigation StageをAnalysisSpecification / ExecutionPlan / Execution / StageExecutionへ追加しない。
- Navigation descriptor / navigation stateをDomain Resource外の論理概念として定義する。
- runtime `StageType / StageDefinition`をExecutionPlan内value objectとして維持し、Navigation Stageと同一化しない。

### 20.6. ENH-E5 Phase I Canonical Convergence

- Navigation catalog authority/route/default StageをPhase G freezeへ収束した。
- AnalysisView typed filter compatibility、Exploratory handoff/provenance、canonical lineage completionを追加した。
- `StageAttempt.effective_random_seed` migrationと`runtime_version_json` environment metadataを追加した。
- D1 current resource responsibilityを維持し、Navigation persistenceを禁止した。
