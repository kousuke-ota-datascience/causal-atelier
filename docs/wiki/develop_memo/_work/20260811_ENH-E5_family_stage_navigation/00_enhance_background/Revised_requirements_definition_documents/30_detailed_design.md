# 30 詳細設計

- 文書状態: `DRAFT_FOR_REVIEW`
- 文書種別: 現行詳細設計のeffective snapshot
- 上位文書: `10_requirements_definition.md`, `21_logical_data_design.md`, `22_product_basic_design.md`, `23_api_interface_design.md`
- 基準Runtime: Python 3.12
- current source照合対象: `src/ariadne/product/`, `src/ariadne/capabilities/`, frontend/router関連実装

## 1. 実装原則

1. DomainはFramework / ORM / external analytical object / browser navigationへ依存しない。
2. Application ServiceはUnit of WorkとPortを通じてpersistent / external capabilityを利用する。
3. Scientific / ML library objectはAdapter境界の外へ持ち出さず、persistent payloadへ直接保存しない。
4. persistent snapshotはstrict schema validation、canonical JSON、content hashを持つ。
5. RunnerはStage input/output contractを受け取り、DB transactionやbrowser stateを直接操作しない。
6. Execution lifecycle authorityは`Execution`、runtime Stage lifecycle authorityは`StageExecution`に集約する。
7. `AnalysisFamily`は`EXPLORATORY / CAUSAL / PREDICTIVE`の3値を持つdomain enumをcanonical discriminatorとする。
8. `Navigation Stage`はapplication/presentation metadataであり、`AnalysisSpecification`、`ExecutionPlan`、`Execution`、`StageExecution`へ保存しない。
9. Navigation taxonomyの変更だけを理由にruntime `StageType`、stage dependency、retry/lease lifecycleを変更しない。
10. CLI / Python library / backend use caseはNavigation Stageを設定せずanalysis executionを開始できる。
11. UI上のStageとruntime Stageに1:1 cardinalityを要求しない。
12. 本詳細設計内で再利用対象とする型・schema・interfaceは、必要なfield/value/transitionを本文内へ記載し、「既存を利用する」という一文だけで外部参照へ委譲しない。

実装依存方向:

```text
Presentation / Navigation
        ↓
Application / Capability
        ↓
Planning / Runtime Execution
        ↓
Persistence / Adapter
```

禁止依存方向:

```text
Runtime Execution
        ↓
Browser route / Current Navigation Stage
```

## 2. Package構成

### 2.0 Current package baseline

ENH-E5で変更しない領域については、Planning baselineの実ファイル構成を設計上の基準とする。存在しないservice/module名を既存構造として記載しない。

```text
src/ariadne/
├── product/
│   ├── domain/
│   │   ├── analysis_spec.py
│   │   ├── analysis_specification.py
│   │   ├── analysis_view.py
│   │   ├── annotation.py
│   │   ├── artifact.py
│   │   ├── dataset_version.py
│   │   ├── enums.py
│   │   ├── errors.py
│   │   ├── execution.py
│   │   ├── execution_plan.py
│   │   ├── graph_semantics.py
│   │   ├── graph_version.py
│   │   ├── lineage.py
│   │   ├── project.py
│   │   ├── research_context.py
│   │   ├── result.py
│   │   ├── schemas.py
│   │   └── stage_execution.py
│   ├── application/
│   │   ├── analysis_frame_service.py
│   │   ├── annotation_service.py
│   │   ├── artifact_service.py
│   │   ├── comparison_query_service.py
│   │   ├── execution_service.py
│   │   ├── exploratory_service.py
│   │   ├── graph_candidate_query_service.py
│   │   ├── graph_version_service.py
│   │   ├── lineage_query_service.py
│   │   ├── output_ownership_service.py
│   │   ├── predictive_split_service.py
│   │   ├── predictive_workflow_service.py
│   │   ├── product_closure_service.py
│   │   ├── project_data_service.py
│   │   ├── project_policy.py
│   │   ├── query_service.py
│   │   ├── scientific_validation_service.py
│   │   ├── stage_execution_service.py
│   │   └── workspace_lifecycle_service.py
│   ├── workflow/
│   │   ├── bindings.py
│   │   ├── canonical_plan_provider.py
│   │   ├── contracts.py
│   │   ├── executor.py
│   │   ├── output_contract.py
│   │   ├── plan_validator.py
│   │   ├── planner_registry.py
│   │   ├── runner_registry.py
│   │   └── stage_materialization.py
│   ├── ports/
│   └── persistence/
├── capabilities/
│   ├── causal/
│   │   └── workflow.py
│   ├── exploratory/
│   │   ├── planner.py
│   │   ├── runners.py
│   │   └── view_compiler.py
│   └── predictive/
│       ├── explanation_runner.py
│       ├── metrics.py
│       ├── modeling.py
│       ├── planner.py
│       ├── preprocessing.py
│       ├── split_runner.py
│       ├── splitting.py
│       ├── training_runners.py
│       └── validation.py
├── interfaces/
│   ├── cli/
│   │   ├── config_schema.py
│   │   ├── discovery.py
│   │   ├── estimation.py
│   │   ├── identification.py
│   │   ├── manifest.py
│   │   ├── refutation.py
│   │   ├── scientific_stage.py
│   │   └── sensitivity.py
│   ├── web_api/
│   └── worker/
│       ├── execution_processor.py
│       └── runner.py
└── adapters/
    └── local_artifact_store.py
```

この一覧は**current implementation fact**であり、ENH-E5のNavigation実装ファイル名を先取りして固定するものではない。新規Navigation codeの配置は、既存責務境界を壊さない最小変更としてG00/G01のfreeze済みcontractで確定する。

### 2.1 Navigation関連module配置

Navigation実装は以下の責務へ分割する。

| 責務 | 配置責務 | Runtimeへの依存 | Persistence authority |
| --- | --- | --- | --- |
| Family別Stage catalog定義 | `capabilities/<family>/`またはCapability descriptor | なし | なし |
| catalog aggregate / validation | application/interface support | なし | なし |
| route parse / serialize | frontend/router | なし | なし |
| browser history同期 | frontend/router | なし | なし |
| `(family, stage_id)` surface binding | frontend/presentation | use case呼出しのみ | なし |
| Execution Plan / StageExecution | workflow/domain | navigationを参照しない | あり |

新しいpersistent `navigation` aggregate/tableを作らない。Navigation descriptorをdomain resourceとしてRepository/UoWへ登録しない。

### 2.2 Runtime packageとの境界

以下のmoduleはNavigation descriptorをimportしてはならない。

- `execution_plan.py`
- `execution.py`
- `stage_execution.py`
- planner / plan validator
- runner registry
- generic executor
- worker claim / lease persistence

CIまたはarchitecture testでimport dependencyを検査可能にする。

## 3. Domain Value Objects

### 3.1 AnalysisFamily

Domain enum定義:

```python
class AnalysisFamily(str, Enum):
    EXPLORATORY = "EXPLORATORY"
    CAUSAL = "CAUSAL"
    PREDICTIVE = "PREDICTIVE"
```

定義位置: `src/ariadne/product/domain/enums.py`

| Enum | serialization | analytical responsibility |
| --- | --- | --- |
| `EXPLORATORY` | `"EXPLORATORY"` | exploratory analysis |
| `CAUSAL` | `"CAUSAL"` | causal analysis |
| `PREDICTIVE` | `"PREDICTIVE"` | predictive analysis |

利用箇所:

- `AnalysisSpecification.analysis_family`
- `ExecutionPlan.analysis_family`
- `Execution.analysis_family`
- planner / capability selection
- API request/responseのFamily discriminator
- Navigation Family tab identity

同じenumをnavigationでも参照できるが、`CurrentFamily`というpersistent Domain Value Objectを追加しない。

`AnalysisSpecification.analysis_family`はenvelope serialization時に`.value`を用いて上記uppercase文字列を出力する。

### 3.2 StageType

Runtime operation identity:

```python
@dataclass(frozen=True, order=True)
class StageType:
    namespace: str
    name: str
    version: str
```

Validation:

- `namespace` / `name`: lower snake case、先頭は英小文字
- `version`: 1以上の整数文字列
- runtime key: `"{namespace}.{name}.v{version}"`

Serialization:

```json
{"namespace":"predictive","name":"train","version":"1"}
```

`StageType`はruntime stage implementation/versionを識別する。Navigation Stage ID (`metrics`, `model-management`等)とは別conceptである。

### 3.3 StageDefinition / StageBinding

`StageDefinition`:

```text
stage_key
stage_type: StageType
input_contract: dict[str, str]
output_contract: dict[str, str]
parameters: dict
resource_policy: dict
enabled: bool
```

`StageBinding`:

```text
source_stage_key
source_output
target_stage_key
target_input
```

Navigation sidebar orderを`ordinal`やdependencyへ変換しない。

### 3.4 ResourceRef

Lineage上のresource referenceは次のimmutable valueである。

```python
@dataclass(frozen=True)
class ResourceRef:
    resource_type: str
    resource_id: str
    project_id: str
    schema_version: str | None = None
    content_hash: str | None = None
```

責務:

- lineage nodeのresource type / identityを明示する。
- Project境界を保持する。
- versioned/canonical resourceではschema version / content hashを補助identityとして保持できる。

Navigation Stageはpersistent Resourceではないため`ResourceRef(resource_type="NavigationStage", ...)`を作らない。

### 3.5 NavigationStageDescriptor

Navigation Stageを実装する場合のimmutable metadata contract:

```python
@dataclass(frozen=True)
class NavigationStageDescriptor:
    stage_id: str
    slug: str
    label: str
    order: int

@dataclass(frozen=True)
class FamilyNavigationDescriptor:
    family: AnalysisFamily
    slug: str
    label: str
    default_stage_id: str
    stages: tuple[NavigationStageDescriptor, ...]
```

Required invariants:

- `family`は`AnalysisFamily`の3値のみ。
- Family descriptorはFamilyごとに1件。
- `stages`は1件以上。
- `stage_id` / `slug`はFamily内で一意。
- `default_stage_id`は`stages`内に存在。
- `order`でdeterministic ordering可能。
- runtime input/output、status、retry、attempt、leaseを持たない。

### 3.6 Navigation state

Current Family / Current Navigation Stageはbrowser URL/application stateとして表現する。

Conceptual state:

```text
project_id
family: AnalysisFamily
navigation_stage_id: str
```

これはpersistent Domain Value Objectではなく、route resolutionの結果である。DB column、Analysis Specification field、Execution fieldへ保存しない。

## 4. Schema Registry / Versioned Schema

### 4.1 Current SchemaRegistry contract

Generic `SchemaRegistry`は`schema_version`文字列だけをkeyにvalidatorを保持する。

```python
class SchemaRegistry:
    _validators: dict[str, SchemaValidator]

    def register(self, schema_version: str, validator: SchemaValidator) -> None: ...
    def validate(self, schema_version: str, payload: Mapping[str, Any]) -> dict[str, Any]: ...
    def canonicalize(self, schema_version: str, payload: Mapping[str, Any]) -> bytes: ...
    def hash(self, schema_version: str, payload: Mapping[str, Any]) -> str: ...
```

Invariant:

- emptyまたはduplicate `schema_version` registrationを拒否。
- unknown versionは`UnsupportedSchemaVersion`。
- payloadはMapping必須。
- validatorがnormalized Mappingを返せる。
- `resource_type + schema_version`複合key lookupは現行contractではない。

### 4.2 Analysis Specification envelope

Schema version: `analysis-specification/1`

許可semantic field:

```text
schema_version
analysis_family
research_context_version_id
dataset_version_id
analysis_view_id
analysis_mode
family_spec_schema_version
family_spec
revision_context
warnings
```

Persistence identity/lifecycle field:

```text
analysis_specification_id
project_id
specification_key
version_number
status
canonical_hash
created_by
created_at
fixed_at
```

Family mapping:

| AnalysisFamily | family_spec_schema_version |
| --- | --- |
| EXPLORATORY | `exploratory-analysis-spec/1` |
| CAUSAL | `causal-analysis-spec/2` |
| PREDICTIVE | `predictive-analysis-spec/1` |

Navigation Stage / current Family fieldを追加しない。

### 4.3 Execution Plan schema

`execution-plan/1` canonical payload:

```text
plan_schema_version
project_id
analysis_specification_id
analysis_family
planner_id
planner_version
stages[]
dependencies[]
```

Persistent entityはさらに`execution_plan_id / plan_hash / created_at`を持つ。

Canonical `Execution`には`execution_plan_id` fieldを持たない。Predictive等のcurrent submission pathがplan identityを必要とする場合は、API requestおよび`analysis_spec_json`内metadataとして扱うcurrent実装を前提にする。

### 4.4 Predictive schema

`predictive-analysis-spec/1` top-level:

```text
schema_version
task_type
prediction_question
feature_spec
split_spec
preprocessing_spec
model_spec
tuning_spec
evaluation_spec
explanation_spec
```

Task type:

- `BINARY_CLASSIFICATION`
- `REGRESSION`

Split strategy:

- `RANDOM`
- `STRATIFIED`
- `GROUP`
- `TIME_BASED`

ENH-E5のStage再配置でschemaを簡略化しない。

### 4.5 Navigation metadata schema

Backend read-model方式をArchitecture Reviewで採用した場合のみ、scientific schemaとは別に`analysis-navigation/1`を定義する。

```text
schema_version
families[].family
families[].slug
families[].label
families[].default_stage_id
families[].stages[].stage_id
families[].stages[].slug
families[].stages[].label
families[].stages[].order
```

このschemaをcurrent `SchemaRegistry`へ登録するか、presentation専用validatorとして別ownershipにするかはfreeze前に確定する。Execution Plan / runtime Stage versionと連動させない。

## 5. Canonicalization Algorithm

Current generic canonicalization:

```python
def _normalize(value):
    if dataclass: return _normalize(asdict(value))
    if Enum: return value.value
    if UUID or datetime: return str(value)
    if None/str/bool/int: return value
    if float:
        reject non-finite
        if value == 0: return 0
        if value.is_integer(): return int(value)
        return value
    if Mapping:
        require all keys are str
        return {k: _normalize(v) for k, v in value.items()}
    if list/tuple:
        return [_normalize(v) for v in value]  # order preserved
    reject unsupported object

def canonical_bytes(payload):
    return json.dumps(
        _normalize(payload),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
```

重要事項:

- generic layerはlist/tupleの入力順を保持する。意味のないlistを自動sortしない。
- object key orderingには依存しない。
- `NaN / Infinity`を拒否する。
- `-0.0 / 0.0`は`0`へnormalizeする。
- integral floatはintegerへnormalizeする。
- unknown field rejectionはschema validator / `reject_unknown`の責務である。
- canonical hashはcanonical bytesのSHA-256。

browser pathname、active Family tab、Current Navigation Stage、sidebar order/labelをAnalysis Specification / Execution Plan / Execution snapshotのscientific hashへ混入させない。

## 6. Research Context Design

### 6.1 Resource shape / lifecycle

Current persistent field:

```text
research_context_version_id
project_id
context_key
version_number
status: DRAFT | FIXED
schema_version: research-context/1
problem_statement
research_questions_json
significance
hypotheses_json
decision_context_json
relations_json
canonical_hash
created_by
created_at
fixed_at
```

Unique `(project_id, context_key, version_number)`、`version_number > 0`。

DRAFTは更新可能、FIXED後はimmutableとする。Family / Navigation Stage切替でResearch Context Versionを暗黙更新・固定しない。

### 6.2 Execution reproducibility boundary

Canonical `Execution`が直接保持する再現性関連fieldは次である。

```text
dataset_version_id
input_graph_version_id
input_result_id
objective_snapshot
rationale_snapshot
analysis_spec_json
algorithm_or_estimator
parameter_json
random_seed
code_version
runtime_version_json
snapshot_hash
snapshot_schema_version
```

Research Context / Analysis Specification / Analysis View / Execution Planとのidentityを必要とするFamily workflowでは、current application layerが`analysis_spec_json`へそのmetadata/snapshotを格納する場合がある。ただしcanonical Executionにそれぞれの独立FK columnがあると仮定しない。

browser Navigation Stageはreproducibility inputではない。

## 7. Analysis View Design

### 7.1 Persistent contract

Current `AnalysisView`:

```text
analysis_view_id
project_id
source_dataset_version_id
view_key
version_number
name
status: DRAFT | FIXED
schema_version: analysis-view/1
spec_json
content_hash
manifest_json
created_by
created_at
fixed_at
```

Unique `(project_id, view_key, version_number)`。

`analysis-view/1` specは次のfieldを持つ。

```text
schema_version
source_dataset_version_id
row_filter
selected_columns
derived_columns
missing_value_policy
time_cutoff
sampling
```

### 7.2 Validation / use boundary

Analysis View lifecycle serviceはcreate/list/get/update/validate/fixを提供する。Family tab切替だけでAnalysis Viewを複製しない。

Exploratory / Predictive / Causal use caseはAnalysis Viewをoptional input/contextとして利用できるが、Analysis Viewへ`navigation_stage`を保存しない。

## 8. Planner Protocol

Planning baselineのgeneric planner portは次である。

```python
@dataclass(frozen=True)
class PlanningContext:
    specification: AnalysisSpecification
    resource_metadata: dict[str, Any]
    policy: dict[str, Any]

class AnalysisPlanner(Protocol):
    family: AnalysisFamily
    spec_versions: frozenset[str]
    planner_id: str
    planner_version: str

    def build_plan(self, context: PlanningContext) -> ExecutionPlan: ...
```

Generic port自体は`AnalysisSpecification.status == FIXED`等のlifecycle条件を宣言しない。どのstatus/resource metadataを要求するかはFamily planner/application serviceの責務である。

`PlanningContext`の意味:

- `specification`: canonical `AnalysisSpecification`。`analysis_family`がplanner selectionのcanonical discriminatorになる。
- `resource_metadata`: plannerが必要とする既存resource snapshot/metadata。Causal compatibility plannerではimmutable canonical `Execution` snapshotを`resource_metadata["execution"]`から受け取る。
- `policy`: planner-level policy input。Navigation route stateの格納先にはしない。

Outputは`ExecutionPlan`であり、`planner_id / planner_version / StageDefinition / StageBinding / plan_hash`によりruntime plan identityを形成する。

### 8.1 Navigation independence

Planner signature / `PlanningContext`へNavigation Stageをrequired inputとして追加しない。

禁止:

```python
def build_plan(context, navigation_stage): ...
```

Navigation `Train`をruntime `StageDefinition(stage_key="train")`へ機械的に変換する処理も作らない。Predictiveに同名runtime stageが存在しても、それはplannerがanalysis semanticsから生成するruntime stageであり、sidebar identityから生成するものではない。

### 8.2 Family discriminator

Planner selectionには`AnalysisSpecification.analysis_family`を利用する。値集合は`EXPLORATORY / CAUSAL / PREDICTIVE`である。browserのactive tabからFamilyを推測してPlanを生成しない。

Family planner固有の前提:

- Exploratory planner: `exploratory-analysis-spec/1`のoperationを1 Stage planへ変換する。
- Causal planner: `causal-analysis-spec/2`に加え、`resource_metadata["execution"]`としてcanonical `Execution` snapshotを要求するcompatibility plannerである。
- Predictive planner: `predictive-analysis-spec/1`を用い、use caseに応じてsplit-only planまたはfull planを構築する。

## 9. Plan Validator

Planning baselineの`PlanValidator.validate(plan)`は次の順序・責務でgeneric Execution Planを検証する。

1. `plan.plan_schema_version`がcanonical `execution-plan/1`であること。
2. `project_id`と`analysis_specification_id`が空でないこと。
3. `stage_key`が一意であること。
4. Planに少なくとも1 Stageが存在すること。
5. enabled Stageについて`StageRunnerRegistry.contains(stage.stage_type)`がtrueであること。
6. `resource_policy.timeout_seconds`が指定される場合、`bool`ではない`int`で、1以上かつ`max_timeout_seconds`以下であること。Planning baseline default upper boundは86400秒。
7. 各dependencyのsource / target StageがPlan内に存在すること。
8. enabled Stageがdisabled Stageへ依存しないこと。
9. `source_output`がsource Stageの`output_contract`に存在すること。
10. `target_input`がtarget Stageの`input_contract`に存在すること。
11. source output schemaとtarget input schemaが完全一致すること。
12. 同じ`(target_stage_key, target_input)`へ複数upstream bindingを定義しないこと。
13. dependency graphをtopological sortでき、cycleが存在しないこと。

返値はdeterministicなtopological stage order `tuple[str, ...]`である。

`StageType(namespace, name, version)`のsyntax validationは`StageType` value object生成時に行うため、PlanValidatorに同じvalidationを重複実装しない。

Family固有scientific policy、Project boundary、Analysis Specification lifecycle、Navigation catalogのID/slug/default/renderer整合性はPlanValidatorの責務ではない。必要な各layerで個別に検証する。

Navigation Stage order/defaultをruntime dependency ruleへ追加しない。

## 10. Runner Registry

Planning baselineのregistry interface:

```python
class StageRunnerRegistry:
    def register(self, runner: StageRunner) -> None: ...
    def resolve(self, stage_type: StageType) -> StageRunner: ...
    def contains(self, stage_type: StageType) -> bool: ...

    @property
    def capability_fingerprint(self) -> tuple[str, ...]: ...
```

内部keyは`runner.stage_type: StageType`である。

Rules:

- `register(runner)`時、同一`runner.stage_type`が登録済みなら`DuplicateRegistration`。
- `resolve(stage_type)`で未登録なら`RunnerNotRegistered(stage_type.key)`。
- `contains(stage_type)`はPlanValidatorがenabled StageのRunner availabilityを検証するために使う。
- `capability_fingerprint`は登録済み`StageType.key`をsortしたtupleであり、process capabilityのdeterministic fingerprintとなる。
- registry keyはruntime `StageType`でありNavigation Stage IDではない。

### 10.1 Capability-owned Navigation Catalog

Navigation catalogはRunner Registryと別registry/providerとして扱う。

```text
exploratory capability -> exploratory navigation catalog
causal capability      -> causal navigation catalog
predictive capability  -> predictive navigation catalog
           │
           ▼
generic navigation catalog aggregator
```

Stage catalog target:

Exploratory:

```text
profile
data-quality
distribution
relationships
comparison
findings
```

Predictive:

```text
setup
train
predict
metrics
explainability
model-management
```

Causal:

```text
setup
discovery
identification
estimation
effects
diagnostics
sensitivity
```

Family descriptor default StageはHuman Architecture Reviewでfreezeする。Runtime planner/runner registryはこのdefault値を参照しない。

## 11. Generic Executor / Worker Sequence

### 11.1 Execution entity

`Execution`の主要field:

```text
execution_id
project_id
analysis_family
dataset_version_id
input_graph_version_id
input_result_id
batch_key
operation
objective_snapshot
rationale_snapshot
analysis_spec_json
algorithm_or_estimator
parameter_json
random_seed
code_version
runtime_version_json
snapshot_hash
snapshot_schema_version
status
retry_count
last_error_summary
requested_by / requested_at
started_at / finished_at
base_execution_id
revision_kind
change_reason
lease_owner
lease_expires_at
```

Execution status:

```text
QUEUED -> RUNNING -> SUCCEEDED
                 └-> FAILED -> QUEUED (retry)
QUEUED/RUNNING -> CANCELLED
```

`lease_owner` / `lease_expires_at`はWorker claim authorityであり、Navigation stateではない。

### 11.2 Worker claim

Repository contract:

```python
def claim_next(
    worker_token: str,
    *,
    worker_id: str | None = None,
    lease_seconds: int = 1800,
) -> Execution | None: ...
```

Eligibility:

- `QUEUED`
- `RUNNING`かつlease expiryが現在時刻以前

Selection:

- `requested_at`順
- row lock + skip locked
- 1件

Mutation:

```text
status = RUNNING
started_at = now
lease_owner = worker_id or worker_token
lease_expires_at = now + lease_seconds
```

`claim_token`というpublic/domain fieldは作らない。process-local `worker_token`はrepository内部のclaim ownershipに利用する。

### 11.3 Lease renewal / update

```python
def renew_lease(execution_id, owner, lease_seconds=1800): ...
```

- positive lease durationを要求する。
- `Execution.lease_owner == owner`を要求する。
- `Execution.status == RUNNING`を要求する。
- update/completeもlease owner mismatchを拒否する。

### 11.4 StageExecution

`StageExecution`:

```text
stage_execution_id
execution_id
stage_key
stage_type: StageType
ordinal
dependencies
status
input_binding
output_binding
attempts[]
last_error
started_at
finished_at
```

Status transition:

```text
PENDING -> READY
READY -> RUNNING
FAILED -> RUNNING          # retry attempt開始時
RUNNING -> SUCCEEDED
RUNNING -> FAILED
FAILED -> PENDING          # prepare_retry
PENDING/READY -> SKIPPED_DUE_TO_PREREQUISITE
PENDING/READY/RUNNING -> CANCELLED
```

Attempt:

```text
attempt_number
worker_id
stage_attempt_id
started_at
finished_at
error
```

### 11.5 Execution completion

Executionを`SUCCEEDED`としてpersistent completeする前に、配下StageExecutionが1件以上存在し、全件が次のどちらかであることを要求する。

- `SUCCEEDED`
- `SKIPPED_DUE_TO_PREREQUISITE`

### 11.6 Runtime processing sequence

```text
worker orchestration claims canonical Execution lease
  ↓
application/family workflow resolves the Execution Plan and external inputs/snapshots required by that execution path
  ↓
GenericExecutor validates Plan structure / Runner availability, then each Runner validates StageContext inputs
  ↓
materialize/list StageExecution
  ↓
resolve READY runtime Stage
  ↓
create append-only StageAttempt
  ↓
runner.validate(context)
  ↓
runner.run(context)
  ↓
validate output binding / Result / Artifact
  ↓
persist stage outcome under current Execution lease owner
  ↓
repeat until terminal
  ↓
complete Execution when all StageExecution are terminal-success compatible
```

### 11.7 Navigation dependency prohibition

以下からNavigation descriptor/routerをimportしない。

- Execution domain
- StageExecution domain
- Execution repository / StageExecution repository
- planner / plan validator
- runner registry
- generic executor
- worker process

Allowed cardinality:

- Navigation 1 : Execution 0
- Navigation 1 : Execution N
- Execution 1 : Navigation N consumers

Examples:

- `Distribution`: read-only Dataset/Resultで表示し、Execution 0でもよい。
- `Metrics`: `EVALUATION_RESULT` readだけで表示できる。
- `Explainability`: saved explanation Result read、または必要なcompute use caseを複数呼び得る。

### 11.8 Runtime event policy

Planning baselineに独立した`ExecutionEventPublisher` / `StageEventPublisher` public interfaceはない。Lifecycle authorityはpersistent `Execution` / `StageExecution` stateである。

したがってFamily tab/route changeを`ExecutionEvent`、`StageEvent`へ変換しない。Navigation telemetryが将来必要になってもruntime scientific lifecycleとは別contractとする。

### 11.9 Standalone scientific CLI boundary

Planning baselineのCLI entry pointは次である。

```text
ariadne-discover
ariadne-estimate
ariadne-identify
ariadne-refute
ariadne-sensitivity
```

このCLI群はgeneric Web Resource CLIではない。

- `ariadne-discover`: local configを読み、standalone discoveryを実行し、Web/API Execution IDを作らない。
- `ariadne-identify` / `ariadne-refute` / `ariadne-sensitivity`: `--config`を入力にdomain analysis-spec validationと`ScientificCoreAdapter`を直接使用するlocal scientific-stage command。
- `ariadne-estimate`: local estimation interface。

したがってFrontend navigation改修のために、これらCLIへ`--current-family` / `--navigation-stage` / route metadataを追加しない。CLIとWeb/API canonical Execution lifecycleが同一interfaceであるとも仮定しない。

## 12. Exploratory Capability

Exploratory Familyは、分析を厳密な一本道workflowとして扱わず、探索観点をNavigation Stageとして提供する。

Navigation Stage:

```text
Profile
Data Quality
Distribution
Relationships
Comparison
Findings
```

### 12.1 Family specification

`exploratory-analysis-spec/1`が受理するoperationとPlanning baseline runtime mapping:

| operation | stage_key | StageType |
| --- | --- | --- |
| `PROFILE` | `profile` | `exploratory.profile.v1` |
| `DISTRIBUTION` | `distribution` | `exploratory.distribution.v1` |
| `ASSOCIATION` | `association` | `exploratory.association.v1` |
| `GROUP_SUMMARY` | `aggregate` | `exploratory.aggregate.v1` |
| `TIME_TREND` | `time_trend` | `exploratory.time_trend.v1` |
| `CHART` | `chart` | `exploratory.chart.v1` |

`ExploratoryPlanner.build_for_spec()`は`family_spec.operation`を上表でresolveし、次のcontractを持つ**1 StageだけのExecution Plan**を生成する。

```text
input:  frame -> analysis-frame/1
output: exploration_result -> exploratory-result/1
parameters: family_spec
```

Family specの主要field:

```text
schema_version
operation
columns
grouping
aggregation
chart_encoding
filter
sampling
expected_output_type
```

Navigation Stage IDを`operation`の別名として強制しない。例えばNavigation `Data Quality` / `Findings`は上表に同名operationを持たなくてよい。

### 12.2 Profile / Data Quality

`Profile`はDataset shape/schema/type/cardinality/summary metadataを表示する。

`Data Quality`はmissing、duplicate、invalid value、outlier candidate、unexpected category、coverage等を扱う。

実装bindingは次の順で選択する。

1. Dataset Versionに保存済みmetadata/profileがあればreadする。
2. 必要な情報が保存済みでなければ、`exploratory-analysis-spec/1`の`PROFILE`等、本文§12.1で定義したcompute operationを利用する。
3. Navigation Stageを開いただけで必ず新Executionを作成する設計にはしない。

### 12.3 Distribution / Relationships / Comparison

- `Distribution`: 主として単変量分布。`DISTRIBUTION` / chart projectionを利用する。
- `Relationships`: association / cross-tab / grouped relation。`ASSOCIATION`等へbindingする。
- `Comparison`: segment/group/cohort比較。`GROUP_SUMMARY`等へbindingする。

1 Navigation Stageから複数operationを利用してよい。

### 12.4 Findings

専用persistent `Finding` aggregateは本Enhancementでは追加しない。

Finding surfaceは次を組み合わせる。

- Exploratory Result types: `DATA_PROFILE_RESULT`, `DISTRIBUTION_RESULT`, `ASSOCIATION_RESULT`, `GROUP_SUMMARY_RESULT`, `CHART_RESULT`
- Annotation: `statement`, `rationale`, `assumptions`, `limitations`
- Artifact: chart/report等
- Lineage: Resultの入力Dataset/Execution/Artifact等

Findingは探索上の観察・仮説生成であり、causal conclusionへ自動昇格しない。

### 12.5 Visualization

VisualizationはNavigation Stageではなくrepresentation concernとする。

Chart Specificationは少なくとも次の情報を表現できる設計とする。

- mark/chart type
- encoding
- aggregation
- binning
- sort
- filter
- sampling/disclosure
- axis/legend metadata

`Distribution -> histogram`、`Relationships -> scatter`、`Comparison -> box/grouped chart`のように各Navigation Stageから利用する。

## 13. Causal Capability

Causal Family Navigation Stage:

```text
Setup
Discovery
Identification
Estimation
Effects
Diagnostics
Sensitivity
```

### 13.1 Analysis / Execution discriminator

Causal family spec schema versionは`causal-analysis-spec/2`。

Runtime causal operationは`ExecutionOperation`の次の値を使用する。

- `DISCOVERY`
- `IDENTIFICATION`
- `ESTIMATION`
- `REFUTATION`
- `SENSITIVITY`

Planning baselineの`CausalPlanner`は`planner_id = causal.compatibility`、`planner_version = 1`であり、`PlanningContext.resource_metadata["execution"]`にimmutable canonical `Execution` snapshotを要求する。

`Execution.operation`から次の`StageType`へ写像する。

| ExecutionOperation | stage_key | StageType |
| --- | --- | --- |
| `DISCOVERY` | `discovery` | `causal.discovery.v1` |
| `IDENTIFICATION` | `identification` | `causal.identification.v1` |
| `ESTIMATION` | `estimation` | `causal.estimation.v2` |
| `REFUTATION` | `refutation` | `causal.refutation.v1` |
| `SENSITIVITY` | `sensitivity` | `causal.sensitivity.v1` |

各canonical Executionから生成されるPlanは**1 runtime Stageのみ**である。Stage input contractはDiscovery以外で`graph_path`を要求し、`input_result_id`がある場合は`upstream_result / upstream_execution`を追加する。outputは`scientific_descriptors: causal-result-descriptors/1`である。

`IDENTIFICATION` runnerが`IDENTIFICATION_RESULT`に加えて`DATA_ELIGIBILITY_RESULT`等のdescriptorを出力し得ることと、`ELIGIBILITY`というruntime Stageが存在することを混同しない。

Navigation `Effects` / `Diagnostics`等はsaved Result read contextとして成立し得るため、同名ExecutionOperation/StageTypeを追加する必要はない。

### 13.2 Execution input matrix

`Execution.validate_input_contract()`が`causal-analysis-spec/2`系snapshotに対して要求するinput matrix:

| ExecutionOperation | input_graph_version_id | input_result_id |
| --- | ---: | ---: |
| DISCOVERY | なし | なし |
| IDENTIFICATION | 必須 | なし |
| ESTIMATION | 必須 | 必須 |
| REFUTATION | 必須 | 必須 |
| SENSITIVITY | 必須 | 必須 |

このruntime prerequisiteをsidebar順序へ置き換えない。

### 13.3 Discovery

Navigation `Discovery`はDAG/candidate confounder/mediator/collider/temporal ordering/domain assumption等を検討するsurfaceである。Discovery結果はGraph candidate / Resultとして後続分析に利用できる。

### 13.4 Identification

Navigation `Identification`では、推定アルゴリズム選択より前に次のsemanticを明示する。

- causal estimand / question
- identification strategy
- adjustment set
- exchangeability
- positivity
- consistency
- IV / parallel trends等、採用strategyに固有のassumption
- identified / not identified / partially identified等のstatus
- failure/warning reason

Identification surfaceにestimator tuningを混在させない。

### 13.5 Estimation

Navigation `Estimation`では、Identification成立後のestimator / nuisance model / estimation executionを扱う。

- estimator selection
- nuisance model configuration
- bootstrap / uncertainty configuration
- analysis execution submission
- estimation result linkage

Identification assumptionそのものをestimator parameterへ埋没させない。

### 13.6 Effects / Diagnostics / Sensitivity

`Effects`:

- `TREATMENT_EFFECT_RESULT`等のeffect result
- ATE / ATT / CATE等、result schemaが持つeffect payload
- uncertainty / interval
- subgroup / heterogeneity projection

`Diagnostics`:

- `DIAGNOSTICS_RESULT`
- balance / overlap / effective sample size / weight等のdiagnostic payload

`Sensitivity`:

- `SENSITIVITY_RESULT`
- alternate assumptions/specificationへの依存性

これらはsaved Result readで成立する場合があり、Navigation Stageごとの新runtime Stageを必須にしない。

### 13.7 Revision semantics

Execution revision relationには`RERUN` / `REVISED`を区別して扱う。`base_execution_id`、`revision_kind`、`change_reason`等のrevision metadataをNavigation route変更で生成しない。

## 14. Predictive Capability

Predictive Navigation Stage:

```text
Setup
Train
Predict
Metrics
Explainability
Model Management
```

### 14.1 Predictive specification contract

Schema version: `predictive-analysis-spec/1`

Top-level required field:

```text
schema_version
task_type
prediction_question
feature_spec
split_spec
preprocessing_spec
model_spec
tuning_spec
evaluation_spec
explanation_spec
```

Task type:

- `BINARY_CLASSIFICATION`
- `REGRESSION`

`prediction_question` fields:

```text
prediction_unit
target
prediction_time
horizon
intended_use
deployment_population
```

`feature_spec`:

```text
feature_columns
availability_cutoff
excluded_columns
```

`split_spec`:

```text
strategy
train_ratio
validation_ratio
test_ratio
group_column
time_column
train_cutoff
validation_cutoff
stratify
seed
```

`preprocessing_spec`:

```text
fit_partition
numeric_imputation
scale_numeric
categorical_encoding
```

`tuning_spec`:

```text
selection_partitions
candidates
objective_metric
```

`evaluation_spec`:

```text
primary_metric
secondary_metrics
subgroups
```

`explanation_spec`:

```text
method
dataset
sampling
local_explanations
```

Stage再配置では上記fieldを削除・rename・default変更しない。実装前inventoryは、UI controlがこれらfieldへどう投影されるかを100% traceするために行う。

### 14.2 Validation contract

Split strategy:

- `RANDOM`
- `STRATIFIED`
- `GROUP`
- `TIME_BASED`

Classification metrics:

- `ROC_AUC`
- `PR_AUC`
- `LOG_LOSS`
- `BRIER`
- `ACCURACY`
- `F1`

Regression metrics:

- `MAE`
- `RMSE`
- `R2`

Key validation:

- targetをfeatureに含めない。
- feature availabilityはfeature_columns全件をcoverする。
- prediction timeより後のfeatureを拒否する。
- split ratioは正数かつ合計1（TIME_BASEDを除く）。
- `GROUP`は`group_column`必須。
- `TIME_BASED`は`time_column / train_cutoff / validation_cutoff`必須でcutoff順序を保証する。
- stratified splitはbinary classificationに限定する。
- preprocessing fit partitionは`TRAIN`のみ。
- deterministic numeric imputationは`MEAN`、categorical encodingは`ONE_HOT`を`predictive-analysis-spec/1`のvalidation contractとする。
- tuning selectionに`TEST`を使わない。
- explanation datasetは`TEST`。
- explanation sampling strategyは`FIRST_N`、sizeは1..1000。

Navigation Stage再構成によってこのvalidationを弱めない。

### 14.3 Runtime predictive plan

Full predictive planは次のruntime Stageを生成する。

```text
split
  ↓
prepare
  ↓
train
  ↓
evaluate
  ↓
explain (explanation_specが有効な場合)
```

Runtime StageType:

```text
predictive.split.v1
predictive.prepare.v1
predictive.train.v1
predictive.evaluate.v1
predictive.explain.v1
```

主要output contract:

- split -> `partition_manifest: partition-artifact/1`
- prepare -> `training_bundle`, `evaluation_bundle`, `fitted_preprocessor`, explanation dataset/spec/sampling
- train -> `frozen_model: fitted-model/1`, `training_summary`
- evaluate -> `evaluation_summary`
- explain -> `explanation_summary`, `model_card`

このruntime sequenceとNavigation Stage taxonomyは一致しない。特にNavigation `Predict` / `Metrics` / `Model Management`に同名runtime Stageが必要とは限らない。

### 14.4 Setup

Predictive `Setup`は、少なくとも以下の設定を編集・検証するsurfaceである。

- task / prediction question
- target
- feature selection / availability / exclusion
- split strategy / ratio / group / time boundaries / seed
- preprocessing
- model spec
- tuning selection
- evaluation metrics / subgroups
- explanation method / sampling

UI再配置前後でgenerated `predictive-analysis-spec/1` canonical payloadのparityを検証する。

### 14.5 Train

Navigation `Train`はtraining use caseへの入口だが、runtimeではsplit / prepare / train / evaluate / optional explainを含むfull planを起動し得る。

したがって`NavigationStage.TRAIN == StageType("predictive","train","1")`という同一性を仮定しない。

### 14.6 Predict

本Enhancementではgeneral-purpose standalone scoring engineを新規必須scopeとしない。

Navigation `Predict`は、Planning baselineに存在するmodel/result/prediction artifact capabilityの範囲でsurfaceを構成する。新しいonline serving / model deployment subsystemが必要になった場合は別Enhancementとして要件化する。

### 14.7 Metrics

`Metrics`は`EVALUATION_RESULT`をread/compareして表示できる。

Evaluation Resultの例:

- classification metric
- regression metric
- subgroup evaluation
- diagnostics / warnings

`Metrics` Navigation Stageを開くためだけに新Executionを要求しない。

### 14.8 Explainability

Predictive explanationには次を利用できる。

- `PREDICTIVE_EXPLANATION_RESULT`
- `PREDICTIVE_EXPLANATION` Artifact
- `MODEL_CARD_RESULT`
- `MODEL_CARD` Artifact

本EnhancementではSHAP等の新external analytical library導入を必須にしない。

### 14.9 Model Management

Read-oriented model surfaceとして次を利用する。

Result:

- `TRAINING_RESULT`
- `EVALUATION_RESULT`
- `MODEL_CARD_RESULT`

Artifact:

- `FITTED_PREPROCESSOR`
- `FITTED_MODEL`
- `MODEL_CARD`

Lineage:

- Execution -> Result
- Result -> Artifact
- revised/rerun relation

UI名だけを理由として別`ModelRegistry` persistent aggregateを追加しない。

### 14.10 Draft state preservation

Navigation Stage切替時にPredictive formをunmount/remountする場合でも、未保存DRAFT inputを意図せず初期化しない。

State ownershipは以下のどちらかへ一意化する。

- route-independent application form store
- parent analytical workspace component state

Stage child componentだけに唯一のDRAFT authorityを持たせ、Stage switchで消失する構造は避ける。

## 15. Result Type / Scientific Status

### 15.1 Result Type

Exploratory:

```text
DATA_PROFILE_RESULT
DISTRIBUTION_RESULT
ASSOCIATION_RESULT
GROUP_SUMMARY_RESULT
CHART_RESULT
```

Predictive:

```text
SPLIT_RESULT
TRAINING_RESULT
EVALUATION_RESULT
ERROR_ANALYSIS_RESULT
PREDICTIVE_EXPLANATION_RESULT
MODEL_CARD_RESULT
```

Causal:

```text
DISCOVERY_GRAPH_RESULT
IDENTIFICATION_RESULT
DATA_ELIGIBILITY_RESULT
TREATMENT_EFFECT_RESULT
DIAGNOSTICS_RESULT
REFUTATION_RESULT
SENSITIVITY_RESULT
```

Navigation Stage名をResult Typeへ自動変換しない。

### 15.2 Scientific Status

Domainで利用するscientific statusには次がある。

```text
GENERATED
GENERATED_WITH_WARNINGS
UNRELIABLE
IDENTIFIED
NOT_IDENTIFIED
PARTIALLY_IDENTIFIED
REQUIRES_REVIEW
PASS
WARN
FAIL
ESTIMATED
INSUFFICIENT_OVERLAP
INSUFFICIENT_SAMPLE
ESTIMATION_UNRELIABLE
NO_FAILURE_DETECTED
FAILURE_DETECTED
INCONCLUSIVE
ROBUST
FRAGILE
TRAINED
TRAINED_WITH_WARNINGS
EVALUATED
INSUFFICIENT_TEST_SAMPLE
NOT_APPLICABLE
```

`VALID`はcompatibility inputとして扱われ得るが、Navigation statusには転用しない。

## 16. Comparison Algorithm

### 16.1 Canonical ComparisonQueryService

Current comparisonは2件以上のcanonical Result IDを入力し、次を検証する。

1. 全Resultが存在する。
2. 全Resultの親Executionが存在する。
3. 全Executionが同一Projectに属する。
4. requestでProject IDが指定された場合、そのProjectと一致する。
5. 全Executionが同一`operation`である。
6. 全Resultが同一`result_type`である。

比較対象Execution snapshot field:

```text
algorithm_or_estimator
parameter_json
random_seed
analysis_spec_json
dataset_version_id
input_graph_version_id
```

各fieldについて全値が一致すれば`common_conditions`、異なれば`changed_conditions[{field, values}]`へ分類する。

Result差分:

```text
result_id
scientific_status
summary
warnings
```

Lineage summary:

```text
execution_ids
result_ids
```

Causal question内`estimand / outcome / population`が不一致の場合、`INCOMPARABLE` warningを返す。

### 16.2 Cross-family boundary

このcurrent canonical comparisonはsame operation / same Result Typeを要求するため、異なるFamily semanticを直接比較する一般アルゴリズムではない。

将来Cross-family overviewを提供する場合は別presentation projectionとして設計し、Predictive metricとCausal effectを単一scoreへ平坦化しない。

## 17. Lineage Projection

### 17.1 Domain authority

`ResourceRef`:

```text
resource_type
resource_id
project_id
schema_version?
content_hash?
```

Typed structural tuple:

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

Generic-only authorityの固定tuple:

```text
Artifact --DERIVED_FROM--> Artifact
Result --SUMMARIZES--> Result
Result --SUMMARIZES--> Artifact
Result --MOTIVATED--> Execution
Result --MOTIVATED--> AnalysisSpecification
Result --MOTIVATED--> AnalysisSpecificationDraft
```

`Result / Artifact --DOCUMENTS|SUPPORTED_BY|EVIDENCE_FOR--> target`のtarget許可集合:

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

`SELECTED / REJECTED`は次のsource typeから`Annotation`へのtupleのみgeneric-onlyである。

```text
Project
ResearchContextVersion
AnalysisView
AnalysisSpecification
Execution
Result
GraphVersion
```

Unknown tupleはclosed-by-defaultでrejectする。typed structural tupleをgeneric `LineageEdge`として二重writeしない。relation名だけを見てgeneric write可否を判断しない。

### 17.2 Current Result lineage projection

`LineageQueryService`はcanonical Resultをrootとして、Project / Execution / DatasetVersion / source Artifact / GraphVersion / upstream Result / output Artifact / Annotationを最大深度32でtraverseする。

Internal projection edgeはID pairとして作られ、Web API layerでsource/target node typeから次の表示relationへ変換する。

```text
CONTEXT_FOR
SOURCE_OF
INPUT_TO
GENERATED
HAS_ARTIFACT
HAS_ANNOTATION
REVISED_FROM
RELATED_TO
```

この表示relationをgeneric lineage write allowlistとして使用しない。

### 17.3 Project boundary

Result lineage traversalおよびgeneric LineageEdgeはProject境界を越えない。

### 17.4 Navigationとの関係

Navigation Stageをpersistent Lineage node/edgeへ追加しない。どのNavigation StageからResultを表示するかはFamily / Result Type / presentation bindingからderiveする。

## 18. Frontend / Navigation Components

### 18.1 Component responsibility

Target component responsibilityを以下のように分離する。名称は設計上のrole名であり、実装時にはこの責務を一意に担うcomponent/moduleへ対応させる。

```text
ProjectShell
├── ProjectGlobalNavigation
│   ├── Research Context
│   ├── Data
│   └── Results / Lineage
├── AnalyticalWorkspace
│   ├── FamilyTabs
│   ├── FamilyStageSidebar
│   └── AnalyticalStageSurface
└── CrossFamilyResultSurface
```

`FamilyTabs`と`FamilyStageSidebar`は別navigation dimensionである。

### 18.2 Navigation catalog loading

Catalog input sourceはArchitecture Reviewで次のいずれかへfreezeする。

- backend read-only `analysis-navigation/1` endpoint
- deploy-time Capability descriptor aggregate

Execution Agentが方式を選択しない。

Catalog normalize後のin-memory model:

```typescript
type AnalysisNavigationCatalog = {
  schemaVersion: string;
  families: FamilyNavigationDescriptor[];
};

type FamilyNavigationDescriptor = {
  family: "EXPLORATORY" | "CAUSAL" | "PREDICTIVE";
  slug: string;
  label: string;
  defaultStageId: string;
  stages: NavigationStageDescriptor[];
};

type NavigationStageDescriptor = {
  stageId: string;
  slug: string;
  label: string;
  order: number;
};
```

Load state:

```text
IDLE -> LOADING -> READY(catalog)
                -> ERROR(error)
```

Catalog validation failureをsilent fallbackしない。

### 18.3 FamilyTabs

Input:

- validated Family catalog
- current route

Output/action:

- supported Family tabをorder通りにrender
- active Familyをsemantic state (`aria-current`等)で表現
- Family click時にtarget Familyのdefault Stage routeを生成

Pseudo-code:

```typescript
function onFamilySelected(targetFamily) {
  const descriptor = catalog.requireFamily(targetFamily);
  const stage = descriptor.requireStage(descriptor.defaultStageId);
  navigate(toAnalysisRoute(projectId, descriptor.slug, stage.slug));
}
```

Familyごとのlast-stage memoryは本Enhancementのrequired behaviorではない。

### 18.4 FamilyStageSidebar

Input:

- current Family descriptor
- current Stage ID

Behavior:

- current FamilyのStageのみ表示する。
- `order`昇順で表示する。
- Stage clickはFamilyを変えずStage slugのみ変更する。
- sidebar orderをruntime dependencyとして利用しない。

Pseudo-code:

```typescript
function onStageSelected(stageId) {
  const family = currentFamilyDescriptor();
  const stage = family.requireStage(stageId);
  navigate(toAnalysisRoute(projectId, family.slug, stage.slug));
}
```

### 18.5 Renderer binding

Presentation binding:

```text
(AnalysisFamily, navigation_stage_id) -> StageSurfaceRenderer / UseCaseAdapter
```

Binding registryはsurface/component selectionだけを所有する。

禁止:

- label/order/default Stageのduplicate catalog ownership
- Stage IDからruntime `StageType`を生成する処理
- renderer missing時のsilent fallback

### 18.6 Route contract

Target canonical route:

```text
/projects/{project_id}/analysis/{family_slug}/{stage_slug}
```

Required parser:

```python
def parse_analysis_route(project_id, family_slug, stage_slug, catalog):
    family = catalog.find_family_by_slug(family_slug)
    if family is None:
        raise UnknownAnalysisFamily(family_slug)
    stage = family.find_stage_by_slug(stage_slug)
    if stage is None:
        raise UnknownNavigationStage(family.family, stage_slug)
    return NavigationContext(project_id, family.family, stage.stage_id)
```

Required serializer:

```python
def to_analysis_route(project_id, family, stage_id, catalog):
    family_desc = catalog.require_family(family)
    stage_desc = family_desc.require_stage(stage_id)
    return f"/projects/{project_id}/analysis/{family_desc.slug}/{stage_desc.slug}"
```

Invariant:

```text
parse(serialize(context)) == context
```

### 18.7 Deep link / reload / browser history

- direct URL openでFamily/Stageを復元する。
- reload後もURLから同じNavigationContextを復元する。
- browser back/forwardでrouteとactive tab/sidebarを同期する。
- UI local stateだけをcanonical current Family/Stage authorityにしない。

### 18.8 Legacy route normalization

Legacy `/explore`, `/causal`, `/predictive`等をサポートする場合、canonical analysis routeへ一方向normalizeする。

```text
legacy route
   ↓ resolve family
canonical family default Stage route
```

Legacy routeと新routeを二つの独立navigation state authorityとして維持しない。

### 18.9 Operation availability

Stage visibilityとaction availabilityを別stateとする。

例:

```text
Causal / Estimation Stage = visible
Identification prerequisite = unsatisfied
Run action = disabled(reason_code="IDENTIFICATION_REQUIRED")
```

Stageを非表示にしてscientific prerequisiteを表現することを基本挙動にしない。

### 18.10 Error handling

| Error | UI behavior | Runtime side effect |
| --- | --- | --- |
| unknown Family slug | explicit not-found/unsupported | なし |
| known Family + unknown Stage | explicit stage error | なし |
| duplicate Stage ID/slug | catalog configuration error / fail-fast | なし |
| missing default Stage | catalog configuration error / fail-fast | なし |
| renderer missing | configuration defect | なし |
| catalog load failure | navigation error state | なし |
| action prerequisite failure | operation disabled / backend error表示 | Executionは勝手に生成しない |

別Stageへsilent fallbackして入力ミスやconfiguration defectを隠さない。

### 18.11 Terminology Guard

- Predictive resultを一般に`effect`と呼ばない。
- Feature importance / explanationをcausal effectとして表示しない。
- Exploratory findingをcausal conclusionへ自動変換しない。
- Runtime Stage statusをNavigation Stage completion indicatorとして転用しない。

## 19. Persistence Mapping

### 19.1 Canonical persistent authority

主要canonical/current Resource:

- Project
- Artifact
- DatasetVersion
- Execution
- StageExecution
- StageAttempt
- Result
- GraphVersion
- Annotation
- ResearchContextVersion
- AnalysisSpecification
- AnalysisView
- ExecutionPlan
- LineageEdge
- ProjectMembership
- WorkspaceSelection
- WorkspaceAnnotation
- ExportBundle

### 19.2 Compatibility / archived persistence

次のtableはhistorical/compatibility read modelとして残る。

```text
FamilyExecution
FamilyStageExecution
FamilyResult
FamilyArtifact
```

`FamilyExecutionOrm`のdoc contract上、新規Product lifecycle write authorityはcanonical `Execution`側である。Family read modelの`analysis_family / schema_version / analytical_status`等をcanonical Result/Artifact fieldへ誤ってコピーしない。

### 19.3 Execution persistence

Canonical Executionの全主要field:

```text
execution_id
project_id
analysis_family
dataset_version_id
input_graph_version_id
input_result_id
batch_key
operation
objective_snapshot
rationale_snapshot
analysis_spec_json
algorithm_or_estimator
parameter_json
random_seed
code_version
runtime_version_json
snapshot_hash
snapshot_schema_version
status
retry_count
last_error_summary
requested_by
requested_at
started_at
finished_at
base_execution_id
revision_kind
change_reason
lease_owner
lease_expires_at
```

`execution_plan_id`、`navigation_stage`、`current_family` columnを追加しない。

### 19.4 StageExecution / StageAttempt persistence

StageExecution:

```text
stage_execution_id
execution_id
stage_key
stage_type_json
ordinal
dependencies_json
status
input_binding_json
output_binding_json
last_error_json
started_at
finished_at
created_at
```

StageAttempt:

```text
stage_attempt_id
stage_execution_id
attempt_number
worker_id
started_at
finished_at
error_json
```

AttemptをJSON historyへ畳み込まず、canonical pathでは別append-only rowとして保持する。

### 19.5 Result / Artifact persistence

Canonical Result:

```text
result_id
execution_id
result_level
stage_execution_id
result_type
scientific_status
summary_json
payload_json
diagnostics_json
warning_json
created_at
```

Canonical Artifact:

```text
artifact_id
project_id
execution_id
stage_execution_id
result_id
artifact_scope
artifact_type
object_key
content_hash
media_type
size_bytes
metadata_json
created_at
```

Canonical Resultに`project_id / analysis_family / schema_version`を追加しない。Canonical Artifactに`family / schema_version / storage_uri / deleted_at`を追加しない。

### 19.6 Navigation persistence prohibition

ENH-E5 targetでは次を追加しない。

```text
current_family
current_navigation_stage
navigation_stage_descriptor table
analysis_specification.navigation_stage
execution.navigation_stage
stage_execution.navigation_stage
```

Current Family / Current Navigation StageはURL/application stateからresolveする。

### 19.7 Migration判定

Navigation catalogをnon-persistent metadataとして実装し、上記canonical tablesの既存contractを変更しない限り、Navigation導入自体を理由とするDB schema migrationは不要である。

persistent field/tableが必要と判明した場合はCoding Agent判断で追加せず、architecture amendmentへ戻す。

## 20. Test Design

詳細設計のtest seamは、Navigationとruntimeの責務分離を直接検証できる単位で設ける。

### 20.1 Domain / Schema tests

`AnalysisFamily`:

- value集合が`EXPLORATORY / CAUSAL / PREDICTIVE`と完全一致する。
- `AnalysisSpecification.envelope()`が`analysis_family.value`を出力する。
- unknown Family文字列をdomain conversionで拒否する。

`AnalysisSpecification`:

- `analysis-specification/1`の許可field以外を拒否する。
- `navigation_stage / current_stage / current_family`をunknown fieldとして受理しない。
- FIXED後のupdateを拒否する。

`ExecutionPlan` / `StageType`:

- plan canonical payloadにNavigation Stageが含まれない。
- `StageType`のnamespace/name/version validationを検証する。
- Plan hashがnavigation label/order変更で変化しない。

`ResourceRef / LineageEdge`:

- Project境界越えを拒否する。
- Navigation Stageをresource typeとして要求しない。

### 20.2 Execution / Worker tests

Execution lifecycle:

- `QUEUED -> RUNNING -> SUCCEEDED`を許可する。
- `RUNNING -> FAILED -> QUEUED` retryを検証する。
- invalid transitionを拒否する。

Claim/lease:

- QUEUED Executionを1 workerだけがclaimできる。
- expired RUNNING leaseをreclaimできる。
- unexpired RUNNING leaseはclaim対象外。
- `lease_seconds <= 0`を拒否する。
- lease owner mismatchでrenew/update/completeを拒否する。
- `claim_token` public field/APIが追加されていない。

StageExecution:

- PENDING/READY/RUNNING/SUCCEEDED/FAILED/SKIPPED/CANCELLED transitionを§11.4どおり検証する。
- retryごとにStageAttemptがappendされattempt_numberが増加する。
- SUCCEEDED Execution complete時、全StageがSUCCEEDEDまたはSKIPPEDであることを要求する。

Architecture:

- runtime moduleからnavigation moduleへのprohibited importを検出する。
- worker claim / executorをNavigation Stageなしで実行できる。

### 20.3 Navigation catalog tests

- Family descriptorが3 Familyを一意に持つ。
- Family内Stage ID / slugが一意。
- default Stageがcatalog内に存在。
- orderがdeterministic。
- empty Stage listを拒否。
- renderer binding欠落をconfiguration errorとして検出。

### 20.4 Route / browser state tests

- route serialize -> parse round-trip。
- direct deep linkでFamily/Stage復元。
- reloadで同じroute contextを復元。
- browser back/forward同期。
- unknown Familyをexplicit error。
- known Family + unknown Stageをexplicit error。
- legacy routeを採用する場合、canonical routeへ一方向normalize。
- Family switch時にtarget default Stageへ遷移。
- Stage switch時にFamily保持。
- navigation操作でExecution/StageExecution stateが変化しない。

### 20.5 Exploratory tests

- 6 Navigation Stageのbinding coverage。
- `Distribution`がread-only pathで表示可能な場合、新Executionを要求しない。
- `Findings`がResult / Annotation / Artifact / Lineageから構成できる。
- `Finding` persistent aggregateをUI都合だけで追加しない。
- Visualizationが独立Stageとしてcatalogへ混入しない。
- finding textをcausal conclusionとして自動変換しない。

### 20.6 Causal tests

- `CausalPlanner`がcanonical Execution 1件につき1 runtime Stage planを生成する。
- operation -> StageType mappingが§13.1と一致する。
- `ELIGIBILITY` runtime Stageを存在前提にしない。
- §13.2 input matrixをoperationごとに検証する。
- Identification surfaceとEstimation surfaceの入力責務が分離される。
- Identification結果をEstimation use caseへ渡すcontractを検証する。
- Effects / Diagnostics / Sensitivityがsaved Resultからreadできるケースで新runtime Stageを要求しない。
- Navigation orderがExecution Plan dependencyへ流入しない。

### 20.7 Predictive compatibility tests

Inventory:

- current UI controlを全量列挙し、各controlにgenerated spec fieldと新Stage配置先がある。
- unmapped control count = 0。

Schema parity:

- UI再配置前後のcanonical `predictive-analysis-spec/1`が同一入力に対して等価。
- default/hidden/generated semanticsが変化しない。

Leakage/split:

- target leakage拒否。
- future feature拒否。
- GROUP key leakage拒否。
- partition overlap拒否。
- group overlap拒否。
- TEST selection利用拒否。
- preprocessing TRAIN-only fit。

Runtime:

- full planが`split -> prepare -> train -> evaluate -> optional explain`を生成する。
- Navigation `Train`がruntime `train`単体実行を意味しない。
- `Metrics`が`EVALUATION_RESULT` readだけで成立できる。
- `Model Management`が`TRAINING_RESULT / EVALUATION_RESULT / MODEL_CARD_RESULT`および`FITTED_MODEL / MODEL_CARD`を利用する。

DRAFT state:

- Stage切替往復後も入力値が保持される。
- browser route stateとform DRAFT stateのauthorityを混同しない。

### 20.8 API contract tests

- Result API: `/executions/{execution_id}/results`, `/results/{result_id}`。
- Comparison API: `/comparisons/query`。
- Lineage API: `/results/{result_id}/lineage`。
- Annotation API: POST project-scoped、GET/PATCH resource-scoped。
- Artifact API: GET metadata / download、Digest hash一致。
- public `claim_token` endpointが存在しない。
- Navigation metadata APIを採用する場合、`analysis-navigation/1`にruntime status/input/output fieldがない。

### 20.9 E2E

- Project -> analytical Family -> Navigation Stage -> use case -> Result/Artifact/Lineageの一連動作。
- Family switch後もProject / Research Context / Dataset contextが保持される。
- `ariadne-discover / estimate / identify / refute / sensitivity`等のheadless CLI/backend direct executionがbrowser route / Navigation Stageなしで成功する。
- authorization boundary。
- Worker + DB + Artifact Store integration。
- cross-family Result/Lineage continuity。

## 21. Definition of Done

- Domain、API、DB、UIの用語・Enum・Schema Versionが一致する。
- `AnalysisFamily`のduplicate discriminatorを導入していない。
- AnalysisSpecification / ExecutionPlan / Execution / StageExecutionへNavigation Stageを追加していない。
- Navigation StageとExecution Stageの1:1 mappingを要求していない。
- CLI / library / backend use caseがNavigation Stageなしで実行できる。
- Predictiveの全UI設定項目がinventoryされ、generated `predictive-analysis-spec/1`、validation、default semanticsのparityが検証される。
- Identification / Estimation等のFamily-specific semanticsが保持される。
- route / deep-link / historyがFamily / Stageと整合する。
- DB/runtime schema migrationが必要な場合は事前にarchitecture amendmentが承認されている。targetはmigrationなし。
- mandatory testおよびprotected regressionが成功する。

## 30. CHANGE LOG

### 30.4 ENH-E4 Canonical Execution Detailed Contract

one canonical persistent Execution identity、generic workflow core、persistent StageExecution、one Result / Artifact / Lineage authority、standalone low-level CLI independence等の設計を継承する。

### 30.5 ENH-E5 Family × Navigation Stage Detailed Contract

Capability-owned Navigation Stage catalog、Family/Stage route/history、presentation bindingを追加する。一方、canonical Family discriminatorは`AnalysisFamily(EXPLORATORY / CAUSAL / PREDICTIVE)`および`AnalysisSpecification.analysis_family`とし、Navigation Stageをpersistent analysis/runtime contractへ追加しない。runtime planner/executor/worker/CLI/libraryはNavigation Stageから独立させる。
