# 23 API・インターフェース設計

- 文書状態: `APPROVED`
- 文書種別: 現行API / interface設計のeffective snapshot
- 上位文書: `10_requirements_definition.md`, `21_logical_data_design.md`, `22_product_basic_design.md`
- API base: `/api/v1`

本書は、現在有効なAPI / browser / internal interface contractを本文内で説明する。`既存APIを使う`、`既存contractを維持する`という記述だけでinterfaceの内容を外部文書やsource codeへ委譲しない。

## 1. API原則

1. Resource IDとProject境界を明示する。
2. `Idempotency-Key`を実装済みのcommand endpointでは、同一commandの再送をidempotency serviceで収束させる。未対応endpointまで一律にidempotentと仮定しない。
3. Analysis Specification、Execution Plan、Family-specific scientific payload、Runner draft等、versioned JSON contractは各contract boundaryでschema versionを持つ。一方、すべてのpersistent entityが直接`schema_version` columnを持つとは仮定しない。
4. validation errorはcurrent error envelopeに従い、必要なfield path / error codeを`details`へ保持する。
5. async execution submissionはExecution identityと受理statusを返す。
6. UI専用のnavigation stateを正本Domain APIへ混入しない。
7. Result payloadとArtifact binary downloadを分離する。
8. Family固有analysis schemaは共通`AnalysisSpecification` envelopeへ埋め込む。
9. analytical Familyのcanonical discriminatorは`AnalysisFamily` / `analysis_family`とし、同義の`family` / `current_family`をpersistent analysis contractへ追加しない。
10. Navigation Stageはpresentation/application metadataであり、Analysis Specification / Execution Plan / Execution / StageExecutionの必須入力にしない。
11. Navigation Stageとruntime `StageType` / `StageExecution`を同一schemaへ統合しない。
12. CLI / Python library / backend use caseによるheadless executionはbrowser navigation metadata interfaceを経由しなくても成立する。
13. UI Stage名を理由として同名execution endpointを1:1で増設しない。
14. UI / application IA変更だけを理由に新しいbackend API/persistence contractを発明しない。必要なinterfaceは本書本文に具体的に記載する。

## 2. Authentication / Authorization

### 2.1 Current request identity

現行実装のFastAPI applicationには共通Bearer/OIDC authentication middlewareは存在しない。

Current request identity contract:

- request correlation: `X-Request-Id`
  - request headerにあればその値を使用する。
  - 未指定時はUUIDを生成する。
  - response headerにも`X-Request-Id`を返す。
- user identity:
  - user identityを必要とするrouterでは`X-User-Id`を読む。
  - 未指定時は`anonymous`を利用する実装がある。
- idempotent command:
  - 対応endpointでは`Idempotency-Key`を受け付ける。

Current interface contractはproduction Authentication方式の成立を前提化しない。`Authorization: Bearer`やproduction OIDCをcurrent implementationとして捏造せず、実装済みauthentication boundaryだけをauthorityとする。

### 2.2 Project role

Project Closure領域のpersisted roleは次の3値である。

- `OWNER`
- `EDITOR`
- `VIEWER`

`ProductClosureService`のrole policy:

```text
READ_ROLES  = OWNER / EDITOR / VIEWER
WRITE_ROLES = OWNER / EDITOR
```

Project作成時は`X-User-Id`（未指定時`anonymous`）をProject ownerとして登録する。

注意事項:

- 全routerがProjectMembership認可を一律に経由するわけではない。
- Current contractではNavigation改修を理由に、未実装の全API統一認可を既存contractとして記述しない。
- Navigation metadataをProject-scoped APIとして追加する場合は、少なくとも既存Project境界を弱めてはならない。


### 2.3 Project authorization coverage

全project-scoped routeはservice action前にProjectMembershipをresolveし、次のmatrixを適用する。

| Action | OWNER | EDITOR | VIEWER |
| --- | --- | --- | --- |
| READ | allow | allow | allow |
| WRITE / MUTATE | allow | allow | deny |
| Execution submit/cancel/retry/rerun/revise | allow | allow | deny |
| Export create | allow | allow | deny |
| Membership administration | allow | deny | deny |
| Explicit sensitive output | allow | allow | deny |

Project IDをpathに持たないlegacy/generic resource routeでも、resourceからProjectをresolveして同等のauthorizationを適用する。prediction row / local explanation row/detailはpotentially sensitive outputとし、VIEWERにはaggregate/suppressed responseのみ許可する。configurable sensitive-column policyおよびsystem-level Operator authorizationは`DEFERRED` scopeである。

## 3. Common Response

### 3.1 Error

Current error envelope:

```json
{
  "error": {
    "code": "INVALID_ANALYSIS_SPEC",
    "message": "human-readable message",
    "details": {},
    "request_id": "uuid-or-request-X-Request-Id"
  }
}
```

`details`はobjectである。Request validation errorでは`{"errors": [...]}`、Predictive validation errorでは`{"path": "..."}`等を格納する。

現行実装で明示されている主なmapping:

| HTTP | code例 | 意味 |
| --- | --- | --- |
| 404 | `ENTITY_NOT_FOUND` | Resource not found |
| 403 | `PROJECT_ACCESS_DENIED` | Project access denied |
| 409 | `PROJECT_ARCHIVED`, `IDEMPOTENCY_CONFLICT`, `RESOURCE_IMMUTABLE`, lifecycle conflict | state/conflict |
| 422 | `PROJECT_BOUNDARY_VIOLATION`, `INVALID_SCHEMA`, `INVALID_ANALYSIS_SPEC`, predictive validation code等 | semantic/domain validation |
| 400 | `INVALID_REQUEST`, fallback `DOMAIN_ERROR` | request validation / generic domain error |
| 500 | `ARTIFACT_HASH_MISMATCH` | persisted metadataとartifact contentのintegrity mismatch |

`401 / 413 / 429`は現行実装のcommon error handlerで一般contractとして定義されていないため、既存contractとして列挙しない。

Navigation catalog/route validation failureをruntime Execution failureへ変換しない。

### 3.2 Pagination

PaginationはAPIごとにcurrent contractが異なる。`AnalysisViewListResponse`やFamily系list response等には`next_cursor` fieldが存在するが、全list APIが共通cursor query contractを実装しているわけではない。

したがってCurrent contractで共通`?limit=&cursor=&sort=` contractが既に存在するものとして扱わない。新しいNavigation metadata APIがpaginationを必要とする場合は、そのAPI固有contractとして明示する。

### 3.3 Read-only presentation metadata

Navigation metadataをAPIで返す場合、そのresponseはpersistent Domain Resource responseではなくread-only presentation metadataとして扱う。

Target schema candidate:

```json
{
  "schema_version": "analysis-navigation/1",
  "families": [
    {
      "family": "PREDICTIVE",
      "slug": "predictive",
      "label": "Predictive",
      "default_stage_id": "setup",
      "stages": [
        {"stage_id": "setup", "slug": "setup", "label": "Setup", "order": 10},
        {"stage_id": "train", "slug": "train", "label": "Train", "order": 20}
      ]
    }
  ]
}
```

このpayloadはNavigation metadataであり、`ExecutionPlan`、`StageDefinition`、`StageExecution`のschemaではない。


#### 3.3.1 Frozen navigation metadata contract

Canonical endpoint:

```http
GET /api/v1/navigation/analysis
```

Response schema version:

```text
analysis-navigation/1
```

Frozen family catalog:

| family | slug | default_stage_id | stages |
| --- | --- | --- | --- |
| `EXPLORATORY` | `exploratory` | `profile` | `profile`, `data-quality`, `distribution`, `relationships`, `comparison`, `findings` |
| `PREDICTIVE` | `predictive` | `setup` | `setup`, `train`, `predict`, `metrics`, `explainability`, `model-management` |
| `CAUSAL` | `causal` | `setup` | `setup`, `discovery`, `identification`, `estimation`, `effects`, `diagnostics`, `sensitivity` |

このresponseはread-only application/presentation metadataであり、runtime Plan/Stage生成、AnalysisSpecification mutation、current navigation persistenceを行わない。

## 4. Project / Research Context API

Project / Research ContextはFamily切替とは独立したProject-scoped resourceである。Project Managementがresource lifecycleを所有し、Family tab操作でresource identityを変更しない。

代表contract:

| Method | Path | 用途 |
| --- | --- | --- |
| POST | `/projects` | Project作成 |
| GET | `/projects` | Project一覧 |
| GET | `/projects/{project_id}` | Project取得 |
| PATCH | `/projects/{project_id}` | ACTIVE Project更新 |
| DELETE | `/projects/{project_id}` | Project archive |
| POST | `/projects/{project_id}/research-contexts` | Research Context DRAFT作成 |
| GET | `/projects/{project_id}/research-contexts` | Context一覧 |
| GET | `/projects/{project_id}/research-contexts/{context_id}` | Context取得 |
| PATCH | `/projects/{project_id}/research-contexts/{context_id}` | DRAFT更新 |
| POST | `/projects/{project_id}/research-contexts/{context_id}/fix` | FIXED化 |
| GET | `/projects/{project_id}/research-contexts/{context_id}/usage` | Analysis Specification利用状況とhistorical Family execution/result projectionを返す |

`research-contexts/{context_id}/usage`の現行実装実装は`AnalysisSpecificationOrm`に加え、historical/compatibility read modelである`FamilyExecutionOrm / FamilyResultOrm`を参照する。canonical `Execution / Result`全体の完全なusage indexではないため、そのように一般化しない。

Navigation routeはProject / Research Contextのidentity authorityではない。

## 5. Dataset / Analysis View API

Dataset Version / Analysis ViewはFamily横断のProject-level analytical inputである。

### 5.1 DatasetVersion

Current public routes:

| Method | Path | 用途 |
| --- | --- | --- |
| POST | `/projects/{project_id}/dataset-versions` | CSV/Parquet Dataset登録 |
| GET | `/projects/{project_id}/dataset-versions` | Project内Dataset一覧 |
| GET | `/dataset-versions/{dataset_version_id}` | Dataset metadata取得 |
| GET | `/dataset-versions/{dataset_version_id}/preview` | preview取得。default limit 20 |

Dataset responseの主要field:

```text
dataset_version_id
project_id
source_artifact_id
dataset_key
name
version_label
content_hash
schema
profile_summary
row_count
column_count
source_note
created_at
```

現行実装に`/dataset-versions/{id}/profile`専用endpointはない。profile summaryはDataset metadata response内の`profile_summary`として取得する。

### 5.2 AnalysisView

Current public routes:

| Method | Path | 用途 |
| --- | --- | --- |
| POST | `/projects/{project_id}/analysis-views` | DRAFT作成 |
| GET | `/projects/{project_id}/analysis-views` | 一覧 |
| GET | `/projects/{project_id}/analysis-views/{analysis_view_id}` | 取得 |
| PATCH | `/projects/{project_id}/analysis-views/{analysis_view_id}` | DRAFT更新 |
| POST | `/projects/{project_id}/analysis-views/{analysis_view_id}/validate` | schema/semantic validation |
| POST | `/projects/{project_id}/analysis-views/{analysis_view_id}/fix` | FIXED化 |

AnalysisView responseは`analysis_view_id / project_id / source_dataset_version_id / view_key / version_number / name / status / schema_version / spec / content_hash / manifest / created_by / created_at / fixed_at`を返す。

Current contractでは`POST/PATCH/validate/fix`の全boundaryで同じtyped filter validatorを利用する。Mismatch responseのcanonical error codeは`FILTER_TYPE_MISMATCH`。

Compatibility summary:

| logical type | allowed operator |
| --- | --- |
| BOOLEAN | `EQ, NE, IN, NOT_IN, IS_NULL, NOT_NULL` |
| INTEGER / REAL / DATETIME | `EQ, NE, LT, LTE, GT, GTE, IN, NOT_IN, IS_NULL, NOT_NULL` |
| TEXT | `EQ, NE, IN, NOT_IN, IS_NULL, NOT_NULL` |
| OTHER | `IS_NULL, NOT_NULL` |

`IS_NULL/NOT_NULL`はvalueなし、`IN/NOT_IN`はnon-empty list。DATETIMEはISO-8601、INTEGERはbooleanを許容せず、REALはfinite numeric。`time_cutoff`はDATETIME + `LT/LTE`。

Family tab切替だけでDatasetVersionやAnalysisViewを複製しない。

## 6. Analysis Specification API

### 6.1 Common envelope

Analysis Specificationのschema versionは`analysis-specification/1`であり、Family固有payloadを共通envelopeに保持する。

Canonical envelope field:

```json
{
  "schema_version": "analysis-specification/1",
  "analysis_family": "PREDICTIVE",
  "research_context_version_id": "uuid",
  "dataset_version_id": "uuid",
  "analysis_view_id": "uuid-or-null",
  "analysis_mode": "CONFIRMATORY",
  "family_spec_schema_version": "predictive-analysis-spec/1",
  "family_spec": {},
  "revision_context": null,
  "warnings": []
}
```

`analysis_family`は`AnalysisFamily` enumをserializationした値である。

| Enum value | API value | 意味 |
| --- | --- | --- |
| `AnalysisFamily.EXPLORATORY` | `EXPLORATORY` | 探索的分析Capability |
| `AnalysisFamily.CAUSAL` | `CAUSAL` | 因果分析Capability |
| `AnalysisFamily.PREDICTIVE` | `PREDICTIVE` | 予測分析Capability |

Family-specific schema mapping:

| analysis_family | family_spec_schema_version |
| --- | --- |
| `EXPLORATORY` | `exploratory-analysis-spec/1` |
| `CAUSAL` | `causal-analysis-spec/2` |
| `PREDICTIVE` | `predictive-analysis-spec/1` |

このdiscriminatorはAnalysis Specification自身の分析semanticを表す。browser上で現在選択されているtabを表す`current_family`とは意味が異なる。

### 6.2 Analysis Specification resource operations

Current public resource operations:

| Method | Path | 用途 |
| --- | --- | --- |
| POST | `/projects/{project_id}/analysis-specifications` | Family Specification DRAFT作成 |
| GET | `/projects/{project_id}/analysis-specifications` | Project内Specification一覧。現行実装ではFamily / Context / Dataset query filterは受けない |
| GET | `/projects/{project_id}/analysis-specifications/{spec_id}` | Specification取得 |
| PATCH | `/projects/{project_id}/analysis-specifications/{spec_id}` | DRAFT更新 |
| POST | `/projects/{project_id}/analysis-specifications/{spec_id}/validate` | 共通 + Family validation |
| POST | `/projects/{project_id}/analysis-specifications/{spec_id}/fix` | FIXED化 |
| POST | `/projects/{project_id}/analysis-specifications/{spec_id}/revise` | child DRAFT作成 |

### 6.3 Navigation Stageを保存しない

次のfieldはAnalysis Specification envelopeへ追加しない。

```json
{
  "current_family": "PREDICTIVE",
  "navigation_stage": "train",
  "current_stage": "train"
}
```

理由:

- `analysis_family`は分析Capabilityのsemantic discriminatorである。
- Current Family / Navigation StageはUI/application navigation stateである。
- 同じ`AnalysisSpecification`を`Train`、`Metrics`、`Explainability`等の複数Navigation Stageから参照し得る。
- Navigation Stageをspecへ保存すると、UI taxonomy変更がscientific/reproducibility contractへ波及する。

### 6.4 Predictive specification contract

`predictive-analysis-spec/1`は次のtop-level fieldを持つ。

- `schema_version`
- `task_type`
- `prediction_question`
- `feature_spec`
- `split_spec`
- `preprocessing_spec`
- `model_spec`
- `tuning_spec`
- `evaluation_spec`
- `explanation_spec`

Task type:

- `BINARY_CLASSIFICATION`
- `REGRESSION`

Split strategy:

- `RANDOM`
- `STRATIFIED`
- `GROUP`
- `TIME_BASED`

Navigation Stage再配置を理由として、上記field、validation、default semanticsを削除・簡略化しない。

## 7. Exploratory Interface

Exploratory UIは`Profile / Data Quality / Distribution / Relationships / Comparison / Findings`をNavigation Stageとして持つが、各Navigation Stageに対応する新規Execution APIを1:1で要求しない。

現行実装で存在するExploratory / Analysis View interfaceは次である。

### 7.1 Analysis View

| Method | Path | 用途 |
| --- | --- | --- |
| POST | `/projects/{project_id}/analysis-views` | Analysis View作成 |
| GET | `/projects/{project_id}/analysis-views` | Analysis View一覧 |
| GET | `/projects/{project_id}/analysis-views/{analysis_view_id}` | Analysis View取得 |
| PATCH | `/projects/{project_id}/analysis-views/{analysis_view_id}` | DRAFT更新 |
| POST | `/projects/{project_id}/analysis-views/{analysis_view_id}/validate` | validation |
| POST | `/projects/{project_id}/analysis-views/{analysis_view_id}/fix` | FIXED化 |

### 7.2 Exploration

| Method | Path | 用途 |
| --- | --- | --- |
| POST | `/projects/{project_id}/exploration/preview` | 保存しない同期preview |
| POST | `/projects/{project_id}/exploration/executions` | persisted exploratory execution submit |
| GET | `/projects/{project_id}/exploration/executions` | exploratory execution一覧 |
| GET | `/projects/{project_id}/exploration/executions/{execution_id}` | exploratory execution取得 |
| GET | `/projects/{project_id}/exploration/results` | exploratory result一覧 |
| GET | `/projects/{project_id}/exploration/results/{result_id}` | exploratory result取得 |
| POST | `/projects/{project_id}/exploration/results/{result_id}/create-analysis-draft` | exploratory resultからCausal/Predictive analysis draft作成 |

`create-analysis-draft` request:

```json
{
  "target_family": "CAUSAL | PREDICTIVE",
  "analysis_mode": "EXPLORATORY | CONFIRMATORY",
  "research_context_version_id": "uuid-or-null",
  "family_spec_schema_version": "...",
  "family_spec": {}
}
```

Contract:

- `dataset_version_id / analysis_view_id`はsource Result lineageからderiveし、request overrideを受け付けない。
- research contextをsource lineageから一意に解決できない場合のみrequestで要求する。
- canonical `AnalysisSpecification`を`DRAFT`としてpersistする。
- source Resultからtarget AnalysisSpecificationへ`MOTIVATED` semantic lineageを保存する。
- auto FIX / auto Executionは行わない。
- same immutable `dataset_version_id` + `CONFIRMATORY`の場合、`EXPLORATORY_REUSE_SAME_DATA` warningとsource Result IDを返す。
| GET | `/projects/{project_id}/exploration/capabilities` | supported operation / chart mark metadata |

`ExplorationRequest`は`dataset_version_id / analysis_view_id? / family_spec`を受け取る。preview responseは`analysis_family = EXPLORATORY`、`result_type / analytical_status / summary / payload / warnings / view_manifest / saved=false`を返す。

Family-specific exploratory specのoperationは次である。

```text
PROFILE
DISTRIBUTION
ASSOCIATION
GROUP_SUMMARY
TIME_TREND
CHART
```

現行実装のExploratory plannerは各operationを1 runtime StageからなるExecution Planへ写像する。Navigation `Data Quality` / `Findings`等のために同名runtime endpointを追加せず、Dataset metadata、Result、Artifact、Annotation等のreadを組み合わせてよい。

## 8. Causal Interface

### 8.1 Graph

Causal analysisはGraph Version / candidate graphを扱う。現行実装のpublic interfaceは次である。

| Method | Path | 用途 |
| --- | --- | --- |
| POST | `/projects/{project_id}/graph-versions` | Graph Version作成。`Idempotency-Key`対応 |
| POST | `/projects/{project_id}/graph-edit-drafts` | candidateを基に編集DRAFT作成。`Idempotency-Key`対応 |
| GET | `/projects/{project_id}/graph-versions` | Project内Graph Version一覧 |
| GET | `/graph-versions/{graph_version_id}` | Graph Version取得 |
| GET | `/projects/{project_id}/graph-versions/{graph_version_id}` | Project境界を検証して取得 |
| PATCH | `/graph-versions/{graph_version_id}` | DRAFT更新 |
| PATCH | `/projects/{project_id}/graph-versions/{graph_version_id}` | Project-scoped DRAFT更新 |
| POST | `/graph-versions/{graph_version_id}/fix` | FIXED化 |
| POST | `/projects/{project_id}/graph-versions/{graph_version_id}/fix` | Project-scoped FIXED化 |
| GET | `/projects/{project_id}/graph-candidates` | Discovery ResultとGraph Versionのcandidate一覧 |
| GET | `/projects/{project_id}/graph-candidates/{candidate_kind}/{candidate_id}` | candidate取得 |
| POST | `/projects/{project_id}/graph-candidate-comparisons/query` | Graph candidate比較 |

Graph Version responseは少なくとも`graph_version_id / project_id / source_result_id / parent_graph_version_id / name / graph_type / graph_origin / provenance / designated_outcome_node / graph / content_hash / edit_rationale / status / created_by / created_at / allowed_actions`を返す。Navigation Stage IDをGraph Version identityへ追加しない。

### 8.2 Causal operation

Runtime causal operation discriminatorは次である。

- `DISCOVERY`
- `IDENTIFICATION`
- `ESTIMATION`
- `REFUTATION`
- `SENSITIVITY`

現行実装の`CausalPlanner`はcanonical `Execution.operation`から**1 runtime Stageだけを持つcompatibility plan**を生成する。

| ExecutionOperation | StageType |
| --- | --- |
| `DISCOVERY` | `causal.discovery.v1` |
| `IDENTIFICATION` | `causal.identification.v1` |
| `ESTIMATION` | `causal.estimation.v2` |
| `REFUTATION` | `causal.refutation.v1` |
| `SENSITIVITY` | `causal.sensitivity.v1` |

したがって、`Identification / Estimation / Effects / Diagnostics`等のNavigation Stageを理由にCausal API/runtimeを単一Plan内の多段Stageへ作り替えない。科学的な前提関係はcanonical Executionの`input_graph_version_id / input_result_id`とResult/Lineageで扱う。

## 9. Predictive Interface

Predictive analysisは`predictive-analysis-spec/1`を入力契約とする。現行実装のfull runtime planは`split -> prepare -> train -> evaluate -> optional explain`である。

Predictive Navigation Stage:

- Setup
- Train
- Predict
- Metrics
- Explainability
- Model Management

これらのStage名に合わせて独立execution APIを6本新設することは要件ではない。

現行実装で存在するPredictive support API:

| Method | Path | 用途 |
| --- | --- | --- |
| GET | `/projects/{project_id}/predictive/capabilities` | Predictive capability metadata |
| POST | `/projects/{project_id}/predictive/split-validations` | split validationを実行しpartition artifactを保存 |
| GET | `/projects/{project_id}/predictive/partition-artifacts/{artifact_id}` | partition artifact metadata取得 |

Split validation requestは`dataset_version_id / analysis_view_id? / family_spec`を受け取る。responseは`predictive-split-validation/1`で、`status=VALID / execution_id / task_type / strategy / partition_counts / partition_artifact / source_snapshot`を返す。

`Metrics`は保存済み`EVALUATION_RESULT`をreadして成立し得る。`Model Management`は`TRAINING_RESULT`、`MODEL_CARD_RESULT`、`FITTED_MODEL`、`MODEL_CARD`等のResult / Artifactをreadするsurfaceとして成立し得る。Navigation再配置を理由にPredictive spec/validation/defaultを変更しない。


### 9.1 Predictive subgroup evaluation response contract

Predictive evaluation outputは指定subgroupごとにrecord listを返す。group valueをJSON object keyへ埋め込まない。

```json
{
  "subgroup_metrics": [
    {
      "subgroup_column": "segment",
      "subgroup_value": "A",
      "is_null_group": false,
      "metric": "roc_auc",
      "sample_count": 120,
      "value": 0.81,
      "uncertainty": {
        "method": "percentile_bootstrap",
        "confidence": 0.95,
        "lower": 0.76,
        "upper": 0.86,
        "requested_resamples": 1000,
        "valid_resamples": 1000
      },
      "status": "OK",
      "warnings": []
    }
  ]
}
```

- evaluation population = untouched TEST。
- specified subgroup columnごとに独立sliceし、自動intersection/discoveryをしない。
- `sample_count`は常に必須。
- bootstrapはnonparametric percentile、confidence=0.95、1000 resamples、deterministic seed。
- `n < 2`またはvalid resamples < 200では`uncertainty=null` + warning。
- metric計算不能は`value=null`、`uncertainty=null`、status/warningを返す。値を捏造しない。

## 10. Execution Interface

現行branchには、canonical/common Execution APIとPredictive workflow向けProject-scoped APIが併存する。current snapshotはNavigation再構成を理由にこれらを暗黙統合・削除しない。

### 10.1 Canonical/common Execution Web API

| Method | Path | 用途 |
| --- | --- | --- |
| POST | `/projects/{project_id}/execution-batches` | canonical Execution batchを非同期submit |
| GET | `/projects/{project_id}/executions` | canonical + predictive family executionのproject list projection |
| GET | `/executions/{execution_id}` | canonical Execution詳細 |
| GET | `/executions/{execution_id}/prefill` | rerun/revision用prefill |
| POST | `/executions/{execution_id}/cancel` | cancel |
| POST | `/executions/{execution_id}/retry` | FAILEDをretry |

Batch submitの主要input:

```text
dataset_version_id
analysis_family
operation
analysis_spec
variants[].algorithm_or_estimator
variants[].parameters
variants[].random_seed
input_graph_version_id
input_result_id
code_version
runtime_versions
objective / rationale
base_execution_id / change_reason
```

Navigation Stageはrequired inputではない。

### 10.2 Canonical Execution response

Current response field:

```text
execution_id
project_id
dataset_version_id
analysis_family
input_graph_version_id
input_result_id
snapshot_schema_version
batch_key
operation
algorithm_or_estimator
status
retry_count
requested_by
requested_at
started_at
finished_at
last_error_summary
analysis_mode
scientific_warnings
revision_context
```

Status: `QUEUED / RUNNING / SUCCEEDED / FAILED / CANCELLED`。

### 10.3 Predictive workflow interface

Current Predictive workflowはExecutionPlanをfirst-class APIとして公開する。

| Method | Path | 用途 |
| --- | --- | --- |
| POST | `/projects/{project_id}/execution-plans` | `analysis_specification_id`からPlan作成 |
| GET | `/projects/{project_id}/execution-plans/{plan_id}` | Plan取得 |
| POST | `/projects/{project_id}/execution-plans/{plan_id}/validate` | Plan validation |
| POST | `/projects/{project_id}/executions` | `analysis_specification_id / execution_plan_id / seed`でpredictive Execution submit |
| GET | `/projects/{project_id}/executions/{execution_id}` | Predictive execution取得 |
| GET | `/projects/{project_id}/executions/{execution_id}/stages` | StageExecution一覧 |
| GET | `/projects/{project_id}/executions/{execution_id}/results` | Result一覧 |
| GET | `/projects/{project_id}/executions/{execution_id}/artifacts` | Artifact一覧 |
| GET | `/projects/{project_id}/executions/{execution_id}/lineage` | Lineage一覧 |
| POST | `/projects/{project_id}/executions/{execution_id}/cancel` | cancel |
| POST | `/projects/{project_id}/executions/{execution_id}/retry` | retry |
| POST | `/projects/{project_id}/executions/{execution_id}/rerun` | rerun |
| POST | `/projects/{project_id}/executions/{execution_id}/revise` | revised execution |
| GET | `/projects/{project_id}/executions/{execution_id}/prefill` | prefill |

### 10.4 Execution Plan / runtime Stage

`ExecutionPlan`は次を保持する。

```text
execution_plan_id
project_id
analysis_specification_id
analysis_family
plan_schema_version
planner_id / planner_version
stages
dependencies
plan_hash
created_at
```

`StageDefinition.stage_type`はruntime `StageType(namespace, name, version)`でありNavigation Stage IDではない。

Canonical `Execution`には`execution_plan_id`独立field/FKはない。Predictive/Exploratory current pathではexecution metadataとして`analysis_spec_json`内にplan/spec/view identityを保持し得る。この差を無視して、Navigation StageをExecutionPlanまたはExecutionの共通fieldとして追加しない。

## 11. Result / Comparison / Lineage API

### 11.1 Canonical Result API

Current canonical routes:

| Method | Path | 用途 |
| --- | --- | --- |
| GET | `/executions/{execution_id}/results` | canonical Result一覧 |
| GET | `/results/{result_id}` | canonical Result取得 |
| POST | `/comparisons/query` | canonical Result比較 |
| GET | `/results/{result_id}/lineage` | Result起点lineage projection |
| POST | `/results/{result_id}/export` | Result export projection |

Canonical Result response:

```text
result_id
execution_id
result_type
scientific_status
summary
payload
diagnostics
warnings
artifact_ids
created_at
```

Canonical responseには`project_id / analysis_family / schema_version / analytical_status`を直接持たない。

### 11.2 Project-scoped Product Closure

Current Project Closure routes:

| Method | Path | 用途 |
| --- | --- | --- |
| GET | `/projects/{project_id}/results` | Project result list |
| GET | `/projects/{project_id}/results/summary` | Project result summary |
| GET | `/projects/{project_id}/results/{result_id}` | Project boundary / membership付きresult detail |
| POST | `/projects/{project_id}/comparisons` | Project-scoped comparison |
| GET | `/projects/{project_id}/results/{result_id}/lineage` | Project-scoped result lineage |
| GET | `/projects/{project_id}/lineage` | Project lineage |
| POST | `/projects/{project_id}/lineage-links` | manual generic lineage link |
| POST | `/projects/{project_id}/exports` | Result集合export |
| GET | `/projects/{project_id}/exports/{export_id}` | Export metadata |
| GET | `/projects/{project_id}/exports/{export_id}/download` | Export download |

`POST /results/{result_id}/export`とProject-scoped`/exports`はcurrent branchで併存する別interfaceである。

### 11.3 Comparison semantics

Canonical `POST /comparisons/query`は最低2 Resultを受ける。Different Project、different Family/Result category等request shape自体が無効な場合はvalidation errorとする。意味上の比較可能性は`semantic_compatible`と`direct_metric_comparable`の二段階で返す。返却projection:

```text
operation
common_conditions
changed_conditions
result_differences
warnings
lineage_summary
```

Cross-familyで意味の異なるResultを単一`score`へ平坦化しない。

Current comparability responseには最低限次を追加する。

```json
{
  "semantic_compatible": true,
  "direct_metric_comparable": false,
  "compatibility_reasons": [],
  "direct_comparison_blockers": ["TEST_ROW_IDENTITY_MISMATCH"]
}
```

Predictive semantic keyは`task_type / target(outcome) / prediction_unit / prediction_time / horizon / deployment/evaluation population semantics`。Direct metric comparisonはさらにsame `dataset_version_id`、same TEST-row identity/hash、same metric definitionを要求する。

Causal semantic keyは`treatment/exposure / outcome / estimand / target population`。Direct comparisonはsame data/view/analysis populationを要求する。

semantic mismatchではHTTP successのまま`semantic_compatible=false`とreasonを返し、quantitative delta/rankを生成しない。

### 11.4 Lineage relationの二層

Result lineage projectionはtyped relationを表示用に次のような名称へmappingする。

```text
Project -> Execution: CONTEXT_FOR
Artifact -> DatasetVersion: SOURCE_OF
DatasetVersion -> Execution: INPUT_TO
Execution -> Result: GENERATED
Result -> GraphVersion: SOURCE_OF
GraphVersion -> Execution: INPUT_TO
Result -> Artifact: HAS_ARTIFACT
Result -> Annotation: HAS_ANNOTATION
GraphVersion -> Annotation: HAS_ANNOTATION
Execution -> Execution: REVISED_FROM
fallback: RELATED_TO
```

一方、manual generic lineage link APIが受け付けるrelationは次のsubsetである。

```text
USED_INPUT
GENERATED
DERIVED_FROM
REVISED_FROM
SUPPORTED_BY
MOTIVATED
SELECTED
REJECTED
```

projection relation名とgeneric authoritative write relationを混同しない。Navigation Stageをいずれのlineage identityにも追加しない。

Current canonical lineage read responseは`ResearchContextVersion -> AnalysisSpecification -> ExecutionPlan -> Execution -> StageExecution -> Result -> Artifact`を再構成し、DatasetVersion / AnalysisView / GraphVersion / input Result / base Executionを含める。deterministic structural relationをmanual/generic LineageEdgeとして二重writeしない。

## 12. Annotation / Artifact API

### 12.1 Canonical/simple Annotation

Current routes:

| Method | Path | 用途 |
| --- | --- | --- |
| POST | `/projects/{project_id}/annotations` | ResultまたはGraphVersion向けAnnotation作成 |
| GET | `/annotations/{annotation_id}` | 取得 |
| PATCH | `/annotations/{annotation_id}` | 更新 |

Response field:

```text
annotation_id
project_id
target_result_id
target_graph_version_id
statement
rationale
assumptions
limitations
created_by
created_at
updated_at
```

exactly one target constraintを持つ。

### 12.2 WorkspaceAnnotation

Product Closureには別のProject-scoped annotation APIがある。

| Method | Path | 用途 |
| --- | --- | --- |
| GET | `/projects/{project_id}/workspace-annotations` | list/filter |
| POST | `/projects/{project_id}/workspace-annotations` | create |
| PATCH | `/projects/{project_id}/workspace-annotations/{annotation_id}` | update |

Allowed target:

```text
Project
ResearchContextVersion
AnalysisView
AnalysisSpecification
Execution
Result
GraphVersion
```

追加fieldとして`decision: SELECTED / REJECTED / DEFERRED / null`、`next_actions`を扱い、persistenceではrevision historyも保持する。

### 12.3 Canonical Artifact

Current unscoped-by-project routes:

| Method | Path | 用途 |
| --- | --- | --- |
| GET | `/artifacts/{artifact_id}` | metadata |
| GET | `/artifacts/{artifact_id}/download` | SHA-256検証済みdownload |

Metadata response:

```text
artifact_id
project_id
execution_id
result_id
artifact_type
object_key
content_hash
media_type
size_bytes
metadata
created_at
```

Canonical persistenceにはさらに`stage_execution_id / artifact_scope`が存在するが、current `ArtifactResponse`では公開していない。

Project Closureにも`GET /projects/{project_id}/artifacts/{artifact_id}`および`.../download`があり、membership / Project境界を付加して同じartifact contentを扱う。

Current contractではunscoped legacy routeもArtifactからProjectをresolveして同じmembership authorizationを適用する。Explicit sensitive Artifact/output detailはOWNER/EDITORのみ。

Canonical `ArtifactType`はfixed enumであり、Predictive関連では`PARTITION_INDEX / FITTED_PREPROCESSOR / FITTED_MODEL / PREDICTION / PREDICTIVE_EXPLANATION / MODEL_CARD`等を含む。

### 12.4 Findings / Model Management

`Findings`はcanonical Result、simple AnnotationまたはWorkspaceAnnotation、Artifact、Lineage projectionを組み合わせて構成する。decision/next actionが必要な場合はWorkspaceAnnotationの既存責務を利用する。

`Model Management`は`TRAINING_RESULT / EVALUATION_RESULT / MODEL_CARD_RESULT`と`FITTED_PREPROCESSOR / FITTED_MODEL / MODEL_CARD`等をreadするsurfaceとして構成できる。

これらのNavigation Stageのために重複Result/Annotation/Artifact Resourceを新設しない。

## 13. Frontend Support API

### 13.1 Operation Availability

Operation availabilityのcanonical current interface:

```text
GET /projects/{project_id}/operation-availability
```

本endpointはFrontend向けのread-only projectionであり、authorization bypass、scientific validation bypass、Execution commandそのものではない。実commandのauthorization / lifecycle / scientific validationが最終authorityであり、本projectionとの不一致はimplementation defectとして扱う。

#### 13.1.1 Canonical operation key set

`operations` mapのkeyは次の3値だけをcanonicalとする。

```text
RUN
EDIT
EXPORT
```

このkey setはclosed setである。Current contractで`CREATE / DELETE / CANCEL / RETRY / RERUN / REVISE / DOWNLOAD`等を追加keyとして返してはならない。

- `RUN`: analytical executionを開始、または既存Executionを基点に既存のretry/rerun/revise系run-family commandを開始できるかを表すpresentation operation class。
- `EDIT`: mutable analytical resourceを既存mutation contractで編集できるかを表すpresentation operation class。
- `EXPORT`: Resultを既存export contractでexportできるかを表すpresentation operation class。

`RUN`はcanonical `Execution.operation` discriminator (`DISCOVERY / IDENTIFICATION / ESTIMATION / REFUTATION / SENSITIVITY`等)とは別conceptである。Navigation Stage名、runtime StageType、endpoint verbをoperation keyへ1:1転写しない。

Responseは常に3 keyすべてを返す。

```json
{
  "operations": {
    "RUN": {"allowed": false, "reason_code": "SPEC_NOT_FIXED", "message": "Fix the specification first."},
    "EDIT": {"allowed": true},
    "EXPORT": {"allowed": false, "reason_code": "UNSUPPORTED_OPERATION"}
  }
}
```

Operation item contract:

```text
allowed: bool
reason_code?: string
message?: string
```

- `allowed=true`では`reason_code`を返してはならない。`message`は原則返さない。
- `allowed=false`では`reason_code`を必須とする。`message`はoptional human-readable explanationでありFrontend logicの判定材料にしてはならない。
- top-level `operations` mapはrequired。

#### 13.1.2 resource_type × operation structural support

`resource_type`は次の4値だけを受理する。

```text
analysis-specification
execution
result
graph-version
```

Structural support matrix:

| resource_type | RUN | EDIT | EXPORT |
| --- | --- | --- | --- |
| `analysis-specification` | supported | supported | unsupported |
| `execution` | supported | unsupported | unsupported |
| `result` | supported | unsupported | supported |
| `graph-version` | supported | supported | unsupported |

意味:

- `analysis-specification/RUN`: FIXED specificationを基点に既存Execution submission contractを利用する。
- `analysis-specification/EDIT`: AnalysisSpecification lifecycleがmutationを許可する場合だけ許可する。
- `execution/RUN`: 既存Execution lifecycleが許可するretry/rerun/revise等のrun-family commandの少なくとも1つへ進める場合に許可する。新しいgeneric run commandを作らない。
- `result/RUN`: 現在のroute/use-caseが既存`input_result_id`を受けるanalytical commandへ対応する場合にのみ候補となる。route/use-case上対応しなければ`UNSUPPORTED_OPERATION`。
- `result/EXPORT`: 既存Result export / Project-scoped export policyへ委譲する。
- `graph-version/RUN`: 現在のroute/use-caseが既存`input_graph_version_id`を受けるcausal commandへ対応する場合にのみ候補となる。
- `graph-version/EDIT`: GraphVersion lifecycleがmutationを許可する場合だけ許可する。

matrixで`unsupported`の組合せはHTTP 200のまま`allowed=false, reason_code=UNSUPPORTED_OPERATION`を返す。

#### 13.1.3 Query contract

Query parameter:

```text
resource_type?: string
resource_id?: string
route?: string
```

必須・任意条件:

1. `resource_type`と`resource_id`はpairである。両方指定または両方未指定のみ有効。
2. pairの片方だけを指定したrequestはHTTP 422 / `INVALID_OPERATION_AVAILABILITY_QUERY`。
3. resource pairを指定しない場合、`route`は必須。3 parameterすべて未指定はHTTP 422 / `INVALID_OPERATION_AVAILABILITY_QUERY`。
4. resource pairを指定した場合、`route`はoptional。ただし`result/RUN`または`graph-version/RUN`のようにresourceだけではscientific use-caseを一意に決められないoperationでは、`RUN.allowed=false, reason_code=ROUTE_REQUIRED`とする。
5. `route`はcanonical browser routeをpresentation contextとして渡す。routeはresource identity、authorization identity、scientific truthのauthorityではない。
6. `route`にresource segmentが含まれる場合、その`resource_type/resource_id`はquery pairと一致しなければならない。
7. explicit route Familyとresolved resource Familyが不一致の場合はHTTP 422 / `ROUTE_RESOURCE_FAMILY_MISMATCH`。silent normalizationしない。

resource未指定時semantics:

- `route`だけを指定したrequestは有効である。
- Backendはrouteからresource IDを推測・自動選択してはならない。
- concrete resourceを必要とするcanonical operationは`allowed=false, reason_code=RESOURCE_REQUIRED`を返す。
- operation availability queryを理由にAnalysisSpecification / Execution / Result / GraphVersionを生成・変更してはならない。

#### 13.1.4 Authorization class

endpoint自体のreadにはProject-scoped `READ` authorizationを適用する。ProjectMembershipをresolveできない、またはREAD不可の場合はHTTP 403 / `PROJECT_ACCESS_DENIED`でrequest全体を拒否する。

各canonical operationのauthorization class:

| operation | authorization class | OWNER | EDITOR | VIEWER |
| --- | --- | --- | --- | --- |
| `RUN` | `EXECUTION_MUTATION` | allow | allow | deny |
| `EDIT` | `WRITE_MUTATE` | allow | allow | deny |
| `EXPORT` | `EXPORT_CREATE` | allow | allow | deny |

Structural support判定後、scientific/domain prerequisite判定前にoperation authorizationを評価する。structurally supported operationでrole不足の場合、HTTP 200のoperation itemとして`allowed=false, reason_code=PROJECT_ACCESS_DENIED`を返す。

#### 13.1.5 Scientific/domain prerequisite authority

scientific/domain prerequisiteのauthorityは**実際のcommandを検証するApplication/Domain policy / validator / lifecycle service**である。Operation Availability専用にscientific ruleを複製してはならない。

最低限、次のauthority境界を維持する。

- AnalysisSpecification lifecycle / validation: specification domain/application validator。
- GraphVersion lifecycle / validation: graph domain/application validator。
- Execution retry/rerun/revise可否: Execution lifecycle/application service。
- Causal input prerequisite (`input_graph_version_id / input_result_id`, identification prerequisite等): causal planner/use-case validation + persisted Result/Lineage。
- Result exportability: Result / output ownership / export policy。
- Project role: persisted ProjectMembership policy。

Evaluation order:

```text
query validation
  -> Project READ authorization
  -> resource resolution / project boundary
  -> resource_type × operation structural support
  -> per-operation authorization
  -> lifecycle mutability/state
  -> scientific/domain prerequisite
  -> allowed=true
```

Frontend、browser route、Navigation Stage visibilityはscientific/domain prerequisite authorityではない。

#### 13.1.6 Unknown resource / unsupported operation semantics

- unknown `resource_type`: HTTP 422 / `UNSUPPORTED_RESOURCE_TYPE`。
- known `resource_type` + `resource_id`が当該Project内で解決できない場合（別ProjectのIDを含む）: HTTP 404 / `ENTITY_NOT_FOUND`。cross-project existenceを開示しない。
- malformed/unknown canonical route: HTTP 422 / `INVALID_NAVIGATION_ROUTE`。
- route/resource Family mismatch: HTTP 422 / `ROUTE_RESOURCE_FAMILY_MISMATCH`。
- structural matrixまたはroute/use-case上unsupportedなcanonical operation: HTTP 200、`allowed=false, reason_code=UNSUPPORTED_OPERATION`。
- responseは非canonical operation keyを返してはならない。内部実装でunknown operation keyが要求された場合はfail closedし、configuration/programming defectとして扱う。

#### 13.1.7 reason_code taxonomy

Current Operation Availabilityのoperation item `reason_code`は次のclosed vocabularyとする。

| reason_code | class | meaning |
| --- | --- | --- |
| `PROJECT_ACCESS_DENIED` | authorization | roleが当該operationを許可しない |
| `UNSUPPORTED_OPERATION` | structural | resource type / route use-caseがoperationを提供しない |
| `RESOURCE_REQUIRED` | query/context | concrete resourceが必要だが指定されていない |
| `ROUTE_REQUIRED` | query/context | resourceだけではRUN use-caseを一意に決められない |
| `RESOURCE_IMMUTABLE` | lifecycle | resource lifecycleがEDIT等のmutationを許可しない |
| `SPEC_NOT_FIXED` | lifecycle/domain | AnalysisSpecificationがRUN可能なfixed stateでない |
| `GRAPH_NOT_FIXED` | lifecycle/domain | GraphVersionがRUN inputとしてfixed stateでない |
| `IDENTIFICATION_REQUIRED` | scientific | estimation等に必要なidentification prerequisiteが未成立 |
| `INPUT_GRAPH_REQUIRED` | scientific | current commandに必要なGraphVersion inputがない |
| `INPUT_RESULT_REQUIRED` | scientific | current commandに必要なResult inputがない |
| `EXECUTION_STATE_NOT_RUNNABLE` | lifecycle | Executionに利用可能なrun-family transitionがない |
| `RESULT_NOT_EXPORTABLE` | lifecycle/domain | Result/export policyがexportを許可しない |
| `DOMAIN_PREREQUISITE_NOT_SATISFIED` | domain | 上記個別codeへ分類できない既存domain prerequisiteが未成立 |

Request-level error codeは次を使用する。

```text
INVALID_OPERATION_AVAILABILITY_QUERY
UNSUPPORTED_RESOURCE_TYPE
ENTITY_NOT_FOUND
PROJECT_ACCESS_DENIED
INVALID_NAVIGATION_ROUTE
ROUTE_RESOURCE_FAMILY_MISMATCH
```

current implementationでad-hoc reason codeを追加してはならない。新しいcodeが必要な場合はcanonical design amendmentを先に行う。

Stage visibilityとaction availabilityは別contractとする。`allowed=false`をStage自体の非表示で表現することを基本挙動にしない。
### 13.2 Analytical Navigation Metadata

Capability-owned Family / Navigation Stage catalogのcanonical endpoint:

```http
GET /api/v1/navigation/analysis
```

Response schemaは`analysis-navigation/1`。

Responsibility:

- supported Family identity
- Family slug / display label
- Family-local Navigation Stage ID / slug / display label / order
- Family default Stage
- metadata schema version

Non-responsibility:

- Execution Plan生成
- Runner selection
- StageExecution status
- Analysis Specification mutation
- persistent current navigation state
- Family-specific analytical result payload

Catalog source of truthは**backend read-only metadata endpoint**へfreeze済みである。Family Capability descriptorをapplication/interface aggregatorが集約し、Frontendはfull catalogをduplicate ownershipしない。Execution Agentが別方式へ変更してはならない。

### 13.3 Catalog source of truth

Concrete Navigation Stage catalogはFamily Capabilityが所有する。Frontend rendererは`(family, stage_id) -> surface` bindingを保持できるが、stage label/order/defaultのfull catalogを独自に二重管理しない。


### 13.4 Browser deep navigation contract

Browser interfaceはProject NavigationとAnalysis Navigationを別route authorityとして扱う。

Project routes:

```text
/projects
/projects/new
/projects/{project_id}/overview
/projects/{project_id}/context
/projects/{project_id}/data
/projects/{project_id}/results
```

Short route:

```text
/projects/{project_id}
```

は`/projects/{project_id}/overview`へhistory-replace semanticsでnormalizeする。

Canonical Analysis route:

```text
/projects/{project_id}/analysis/{family_slug}/{stage_slug}
```

Resource deep route:

```text
/projects/{project_id}/analysis/{family_slug}/{stage_slug}/resource/{resource_type}/{resource_id}
```

`resource_type`:

- `analysis-specification`
- `execution`
- `result`
- `graph-version`

Browser semantics:

- Project routeとAnalysis routeの双方でdirect link / reload / Back / Forwardを成立させる。
- Analysis WorkspaceのCurrent ProjectはAnalysis routeの`project_id`をauthorityとしread-onlyとする。
- Family切替時のdefault Stageは`GET /api/v1/navigation/analysis`の`default_stage_id`をauthorityとする。
- Explicit Family/Stageとresource semantic mismatchはsilent correctionせずroute errorとする。
- Supported legacy analytical entryはcanonical Analysis routeへ一方向normalizeし、parallel route/state authorityとして維持しない。
- 旧route tokenそのものの永続的存続をcurrent contractとはしない。

Analysis Contextは新しいbackend API resourceではない。Current Project / Research Context / Dataset Version / Analysis Viewは既存Project / Context / Dataset / Analysis View interfaceとclient/workspace stateをcompositionして扱う。

Async presentation state vocabulary:

`IDLE / LOADING / READY / EMPTY / PARTIAL / ERROR / CANCELLED`

## 14. Worker / Runtime Internal Interface

Worker claimはpublic Web APIではなく、worker processとExecution repository / Unit of Work間の内部interfaceである。

### 14.1 Execution claim / lease

Repository-level interface:

```python
def claim_next(
    worker_token: str,
    *,
    worker_id: str | None = None,
    lease_seconds: int = 1800,
) -> Execution | None: ...
```

Claim対象:

- `QUEUED`
- `RUNNING`かつexpired lease

Selection/mutation:

- `requested_at`順
- row lock + skip locked
- `status = RUNNING`
- `started_at = now`
- `lease_owner = worker_id or worker_token`
- `lease_expires_at = now + lease_seconds`

Worker processはprocess-local UUID `worker_token`を生成し、current runnerでは`claim_next(worker_token, worker_id=worker_token)`を呼ぶ。`claim_token`というpublic/domain resourceは存在しない。

### 14.2 Lease renewal / ownership

```python
renew_lease(execution_id, owner, lease_seconds=1800)
```

positive duration、Execution存在、`lease_owner == owner`、`status == RUNNING`を要求する。lease ownerが設定されたExecutionのupdate/completeもowner一致を要求する。

### 14.3 Completion boundary

Executionを`SUCCEEDED`としてcompleteする場合、StageExecutionが1件以上あり、全件が`SUCCEEDED`または`SKIPPED_DUE_TO_PREREQUISITE`でなければならない。

### 14.4 Stage runtime contract

`StageExecution` status:

```text
PENDING
READY
RUNNING
SUCCEEDED
FAILED
SKIPPED_DUE_TO_PREREQUISITE
CANCELLED
```

Attemptは`stage_attempt_id / attempt_number / worker_id / effective_random_seed / started_at / finished_at / error`をappend-only履歴として保持する。`effective_random_seed`はstochastic Stageのactual seed、deterministic Stageはnull。同一logical Stageのtechnical retryでは同じeffective seedを再利用する。

### 14.5 Runner contract

Current protocol:

```python
class StageRunner(Protocol):
    stage_type: StageType
    def validate(self, context: StageContext) -> None: ...
    def run(self, context: StageContext) -> StageRunResult: ...
```

`StageRunResult`:

```text
output_bindings
results: ResultDraft*
artifacts: ArtifactDraft*
warnings
metrics
effective_random_seed: int | null
```

`ResultDraft`と`ArtifactDraft`は`schema_version`を持つが、canonical persistent Result/Artifactが同一fieldを直接持つことを意味しない。Runner/output adapterでcanonical persistence contractへ変換する。

Execution `runtime_version_json`は最低限`ariadne_code_version / python_version / platform_system / platform_release / machine / libraries`を含む。`libraries`は実際に利用したregistered runner dependencyのversionをcaptureする。

### 14.6 Runtime state observation / event policy

現行実装に独立したpublic`ExecutionEventPublisher / StageEventPublisher`はない。runtime lifecycle authorityはpersistent `Execution / StageExecution` stateである。

Family tab/Navigation route changeをruntime lifecycle eventへ変換しない。

## 15. CLI / Library Interface

現行実装のproduct script entry pointは次である。

```text
ariadne-discover
ariadne-estimate
ariadne-identify
ariadne-refute
ariadne-sensitivity
ariadne-api
ariadne-worker
```

scientific CLIの既存境界:

- `ariadne-discover`はstandalone discovery CLIであり、**Web/API Execution IDを作成しない**。
- `ariadne-identify` / `ariadne-refute` / `ariadne-sensitivity`は共通local scientific-stage implementationを利用し、`--config`でYAMLを読み、domain analysis-spec validation後に`ScientificCoreAdapter`を直接呼び出す。
- `ariadne-estimate`もlocal estimation commandとして提供される。
- CLIは実行manifest等のlocal outputを生成するが、browser route / sidebar stateを入力契約にしない。

したがってCurrent contractでは、存在しない次のようなgeneric Resource CLIをcurrent interfaceとして捏造しない。

```text
ariadne project list
ariadne execution submit
ariadne result show
```

将来generic product CLIを追加する場合は別scopeでinterface contractを設計する。Current mandatory contractでは、既存headless scientific CLIおよびPython/backend use caseへ`current_family` / `navigation_stage` / browser routeをrequired inputとして追加しない。

禁止例:

```text
ariadne-identify --navigation-stage identification --config ...
```

`AnalysisFamily` / `ExecutionOperation`等のdomain discriminatorと、UI Navigation Stageを区別する。

## 16. Idempotency

Idempotencyはretryでduplicate durable side effectを生成し得るCommandへ適用する。HTTP methodや「create」一般を判定基準にしない。

Scope:

```text
(project_id, command_scope, idempotency_key)
```

Required semantics:

- required key missing → `IDEMPOTENCY_KEY_REQUIRED`
- same key + same canonical semantic request → stored response replay、duplicate durable side effectなし
- same key + different request → HTTP 409 `IDEMPOTENCY_CONFLICT`
- request hashはpath上のsemantic resource identityを含む
- concurrent same-key requestはDB uniqueness/advisory lock等でsingle durable effectへ収束する
- idempotency replay recordは可能な限り対象metadata mutationと同一transactionでcommitする

Current contractでidempotency対象とするCommand:

- DatasetVersion create
- Execution batch create
- GraphVersion create
- GraphEditDraft create
- Result export create
- AnalysisView create
- Exploration execution submit
- Exploratory Result → AnalysisSpecification DRAFT create
- ResearchContext create
- AnalysisSpecification create / revise
- Predictive split-validation（durable Execution/Artifactを生成する場合）
- Predictive Execution submit / rerun / revise
- Annotation / WorkspaceAnnotation create
- Project Export create

対象外:

- pure GET/query/compare/preview/validate
- existing natural plan-hash idempotencyを持つExecutionPlan create
- uniquenessで重複を防ぐexplicit lineage link
- Project create
- cancel/fix/update等のstate-machine Command（別途自然なstate conflictで制御）

### 16.1 Retry-safe Artifact materialization

exactly-once executionは保証しない。successful Stage outputのretry/restartでdurable Artifactを重複materializeしない。

- logical identity/object keyはExecution + Stage + output slot/ordinal + Artifact typeからdeterministically導出する。
- same logical output + same content hashは既存Artifactをreuseする。
- same logical output + different content hashはnondeterministic-output conflictとして失敗させる。
- Result/Artifact bindingはmetadata transactionでatomicに確定する。
- ArtifactStoreとmetadata DBのcross-store compensationはNFR-007に対応する`DEFERRED` scopeである。

## 17. Contract Versioning

Version axis:

- URL major: `/api/v1`
- Analysis Specification envelope: `analysis-specification/1`
- Family spec: `family_spec_schema_version`
- Execution Plan: `execution-plan/1`
- runtime Stage identity: `namespace / name / version`
- Navigation metadata: `analysis-navigation/1`

Navigation Stageのlabel/order変更をruntime `StageType.version`変更と連動させない。

破壊的persistent/scientific contract変更は新schema versionとして扱う。Presentation-only metadata変更とscientific snapshot versioningを同一version axisへ混在させない。

## 18. 禁止interface

次のinterfaceを導入しない。

1. `AnalysisSpecification.current_family`
2. `AnalysisSpecification.navigation_stage`
3. `Execution.navigation_stage`
4. `StageExecution.navigation_stage`
5. Navigation Stage IDを`StageType`として流用するcontract
6. Navigation Stageごとの機械的なExecution endpoint増設
7. public `claim_token` resource/API
8. Family/Stage route changeをruntime lifecycle eventへ変換するevent contract
9. Findings / Model ManagementというUI名だけを理由とする重複Result/Artifact/Annotation resource
10. Navigation metadataをscientific generic `SchemaRegistry`へ登録するinterface
11. persisted `EXECUTE` role / system Operator roleをcurrent project authorizationへ無根拠に追加するinterface
12. Analysis Context専用backend resource/APIをUI都合だけで新設するinterface
13. Project route stateをAnalysis navigation stateへ混在させるinterface
14. UI Stage配置を理由にExploratory/Predictive/Causalのbackend operation/APIを増設するinterface

## 19. Interface verification観点

- `analysis_family`の値集合が`EXPLORATORY / CAUSAL / PREDICTIVE`で一意である。
- `AnalysisSpecification`にnavigation-only fieldが追加されていない。
- CLI/library/backend executionがNavigation metadata readなしで成立する。
- runtime `StageType`とNavigation Stage IDが別type/namespaceとして扱われる。
- Worker claimが`Execution.lease_owner / lease_expires_at`をauthorityとし、存在しないpublic claim resourceを前提にしない。
- Result / Annotation / Artifactのpublic pathとresponse fieldが本文contractと一致する。
- Findings / Model Managementのread surfaceが§11〜12で定義したResult / Annotation / Artifact / Lineage responsibilityを利用し、UI名だけの重複Resourceを作らない。
- Navigation route changeがExecution / StageExecution stateを変化させない。
- Project Management routeとAnalysis routeが別authorityとしてdirect-link / reload / Back / Forwardを復元できる。
- Analysis Contextは既存Project/Context/Dataset/Analysis View contractを再利用し、専用persistent/API resourceを要求しない。
- Dataset Version変更時のincompatible Analysis View deselectionをclient/application stateで扱い、Family/Stage routeを書き換えない。
- `GET /api/v1/navigation/analysis`が`analysis-navigation/1`のfrozen catalogを返す。
- AnalysisView type mismatchが`FILTER_TYPE_MISMATCH`を返す。
- required idempotency key missingが`IDEMPOTENCY_KEY_REQUIRED`、same key/different requestが409 `IDEMPOTENCY_CONFLICT`となる。
- VIEWERがexplicit sensitive prediction/local-explanation detailへアクセスできない。
- `StageAttempt.effective_random_seed`と`runtime_version_json`がreproducibility contractを満たす。
- `DEFERRED` interface（general AuditLog/retention/object-store等）をcurrent mandatory acceptanceへ混ぜない。

## 20. CHANGE LOG

### 20.4 ENH-E4 Canonical Execution Interface Contract

Canonical persistent Execution identity、generic runtime Stage、Result / Artifact / Lineage authority、headless CLI independenceを有効contractとして保持する。

### 20.5 ENH-E5 Family × Navigation Stage Interface Contract

Family / Navigation Stageをpresentation/application navigation modelとして追加する。`AnalysisFamily`は`EXPLORATORY / CAUSAL / PREDICTIVE`のdomain discriminatorとしてAnalysis Specification / Execution Plan / Executionで利用し、Navigation Stageをpersistent scientific/runtime contractへ追加しない。

Worker interfaceについては、Execution repositoryのlease ownership contractを本文に明示し、存在しないpublic `claim_token` APIや独立Execution/Stage event publish schemaを前提としない設計へ明確化した。

### 20.6 ENH-E5 Phase I Canonical Interface Convergence

- Navigation metadata endpoint/schema/route/resource deep routeをcanonicalにfreezeした。
- typed AnalysisView validation、Exploratory handoff、subgroup output、comparability response、authorization、idempotency、retry-safe Artifact、StageAttempt seedを具体化した。
- Phase G freezeに残っていたcandidate/Architecture Review待ち表現を除去した。


### 20.7 Project / Analysis Browser Interface Contract

Project routesとAnalysis routesを別navigation authorityとして定義し、Project short-route normalization、Analysis Context composition、direct link / reload / Back / Forward、legacy analytical entry normalizationをcurrent browser interface contractへ統合した。Backend API/persistence contractはUI再配置だけを理由に変更しない。
