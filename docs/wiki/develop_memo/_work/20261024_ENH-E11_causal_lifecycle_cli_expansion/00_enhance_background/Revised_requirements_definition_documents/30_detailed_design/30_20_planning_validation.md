# 30_20_planning_validation


---

## 9. Planning / validation / Runner Registry

### 9.1 AnalysisSpecification to ExecutionPlan

Generic planner port:

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

`AnalysisSpecification.analysis_family`をplanner selectionのcanonical discriminatorとする。`policy`はplanner-level policy inputでありNavigation route stateの格納先にしない。

Family-specific planning:

- Exploratory: `exploratory-analysis-spec/1`のoperationを1 runtime Stage planへ変換する。
- Causal: `causal-analysis-spec/2`と、必要なcanonical Execution snapshot等のresource metadataからcompatibility planを構築する。
- Predictive: `predictive-analysis-spec/1`を用い、use caseに応じてsplit-only planまたはfull planを構築する。

Navigation Stageをplanner inputの必須fieldにしない。browser active tabからFamilyを推測してPlanを生成しない。

### 9.2 PlanValidator

`PlanValidator.validate(plan)`は次をgenericに検証する。

1. `plan_schema_version == execution-plan/1`。
2. `project_id`と`analysis_specification_id`が空でない。
3. `stage_key`が一意。
4. Planに1 Stage以上存在する。
5. enabled Stageの`StageRunnerRegistry.contains(stage.stage_type)`がtrue。
6. `resource_policy.timeout_seconds`が指定される場合、boolではないint、1以上、configured maximum以下。
7. dependency source/target StageがPlan内に存在する。
8. enabled Stageがdisabled Stageへ依存しない。
9. `source_output`がsource Stage output contractに存在する。
10. `target_input`がtarget Stage input contractに存在する。
11. source output schemaとtarget input schemaが一致する。
12. 同じ`(target_stage_key, target_input)`へ複数upstream bindingを定義しない。
13. dependency graphがacyclicでtopological sort可能。

返値はdeterministic topological stage orderとする。Family-specific scientific policy、Project boundary、AnalysisSpecification lifecycle、Navigation catalogのID/slug/default/renderer整合性はPlanValidatorへ混在させない。

検証対象外:

- Navigation Stage order/default
- sidebar visibility
- current browser route
- Project Management section

### 9.3 Runner Registry

Runner Registryのkeyはruntime `StageType`である。

```text
register(runner)
resolve(stage_type)
contains(stage_type)
capability_fingerprint
```

同じStageTypeのduplicate registrationを拒否する。unknown StageTypeはregistered runnerなしとして失敗させる。

Navigation Stage IDをRunner Registry keyにしない。

### 9.4 Navigation CatalogとRunner Registry

```text
Family Capability
├─ runtime runner/provider
└─ navigation descriptor/provider
```

同じCapabilityが両方を所有してよいが、両者は別contractである。

- navigation catalogからruntime Stageを生成しない。
- runtime registryからnavigation sidebarを推測しない。

---

### 9.5. `PlanValidator`（EXISTING：Owner 7区分）

#### 9.5.1. 識別情報・責務

- **Class/module:** `ariadne.product.workflow.plan_validator.PlanValidator`。**EXISTING**、source blob `53aab649a0ed3f0dbec78e5fa98271ff78f5dc12`。
- **責務:** ExecutionPlanの構造検証とdeterministic topological stage order。科学的因果識別・Navigation Catalog・Project RBACは責務外。E11のLocal科学Method Registryとは同一でない。

#### 9.5.2. フィールド

| Field | Type/default | Source | Invariant |
| --- | --- | --- | --- |
| `runners` | `StageRunnerRegistry` mandatory | Constructor argument | StageType availability authority |
| `max_timeout_seconds` | `int=86400` | Constructor keyword | per-stage timeoutの上限・bool不可 |

#### 9.5.3. Constructor / Factory

`__init__(self, runners: StageRunnerRegistry, *, max_timeout_seconds: int = 86_400) -> None` はrunnerとtimeout limitを保存。**N/A:** 専用FactoryはSourceに存在しない。Constructorで科学BackendやProduct DB transactionを起動しない。

#### 9.5.4. メソッド

| Method signature | Return | Side effect | Failure |
| --- | --- | --- | --- |
| `validate(self, plan: ExecutionPlan) -> tuple[str,...]` | stable topological stage keys | N/A（Validation read-only） | `InvalidExecutionPlan(code,message)` |
| `_error(code: str,message: str) -> None`（staticmethod） | normal returnなし | N/A | `InvalidExecutionPlan` |

#### 9.5.5. 処理仕様

Sourceの`validate`に従い、Plan schema version・Project/Spec references・stage count/unique keys・registered runner・timeout type/range・dependency endpoints・enabled/disabled関係・output/input binding/schema・duplicate target binding・cycleを検証し、ready setをsortしてdeterministic topological順を返す。成功時に入力Planを変更しない。詳細条件は本書§9.2。Navigation Stage slugによってStageTypeを生成しない。

#### 9.5.6. I/O・連携・失敗処理

入力は`ExecutionPlan`と注入`StageRunnerRegistry`、出力は順序tuple。**N/A:** Persistence・FS・HTTP・Retry・Rollbackは無い。Error code：`UNSUPPORTED_PLAN_SCHEMA`、`MISSING_PLAN_REFERENCE`、`DUPLICATE_STAGE_KEY`、`EMPTY_PLAN`、`RUNNER_NOT_REGISTERED`、`RESOURCE_POLICY_EXCEEDED`、`MISSING_DEPENDENCY_NODE`、`DISABLED_DEPENDENCY`、`MISSING_OUTPUT`、`MISSING_INPUT`、`SCHEMA_MISMATCH`、`DUPLICATE_BINDING`、`PLAN_CYCLE`。正確な入力型・Exceptionは上記blobをauthorityとする。

#### 9.5.7. 検証

**Unit:** valid DAG deterministic order、empty/cycle、schema mismatch、disabled dependency、timeout bool/range、unknown StageType、duplicate binding。**Contract:** valid Planのtopological order repeatability。**Negative:** unsupported version/error codes。**Trace:** FR-079/089、Product runtime regression。試験実行と独立検証は本PREP-01ではNOT_RUN。

### 9.6. `StageRunnerRegistry`（EXISTING：Owner 7区分）

#### 9.6.1. 識別情報・責務

- **Class/module:** `ariadne.product.workflow.runner_registry.StageRunnerRegistry`。**EXISTING**、source blob `7ffa673d92818e597c4349737860df0ff75b4f97`。
- **責務:** Runtime StageType→StageRunner登録・resolve・contains。E11 MethodCapabilityRegistry（Method/Estimand/Inference/Backend選択）やNavigation Stage Catalogの実装ではない。

#### 9.6.2. フィールド

| Field | Type | Default | Constraint |
| --- | --- | --- | --- |
| `_runners` | `dict[StageType, StageRunner]` | `{}` in constructor | StageType unique、runner.stage_type一致 |

#### 9.6.3. Constructor / Factory

`__init__(self) -> None`で空dictを設定。**N/A:** 専用Factory無し。外部科学libraryのimportやArtifact書込みはしない。

#### 9.6.4. メソッド

| Signature | Return | Side effect / failure |
| --- | --- | --- |
| `register(self, runner: StageRunner) -> None` | None | registryへmutate、duplicateで`DuplicateRegistration` |
| `resolve(self, stage_type: StageType) -> StageRunner` | StageRunner | read-only、missingで`RunnerNotRegistered` |
| `contains(self, stage_type: StageType) -> bool` | bool | read-only |
| `capability_fingerprint(self) -> tuple[str,...]`（property） | stable sorted StageType.key tuple | read-only |

#### 9.6.5. 処理仕様

`register`は同じStageTypeの二重登録を拒否。解決は完全一致key。Fingerprintは`stage_type.key`をsortしたtuple。Runtime StageTypeはNavigation Stage IDから導かない。E11 Local Scientific AdapterをこのRegistryのStageTypeへ無理に詰め込まない。

#### 9.6.6. I/O・連携・失敗処理

入力は純粋StageTypeとStageRunner、出力はin-memory Registry。**N/A:** DB/FS/Network I/O・retry/rollback、Science Status。失敗は上記typed Domain exception。外部Side effectは登録用dict変更のみ。

#### 9.6.7. 検証

**Unit:** register/resolve/contains、unknown/duplicate、fingerprint order invariant。**Negative:** duplicate StageType／invalid missing lookup。**Regression:** Product Runner選択とE11 Local Method Registry非混合。**Trace:** FR-075/079/080/128a、Product E9/E10 protected contract。Source一致は静的確認済み、テストはNOT_RUN。

### 9.7. Chapter-wide Requirement Trace

- `FR-075`：Family別PlannerをRegistryから解決する
- `FR-079`：Stage RunnerをRegistryから解決し、Executorへif/elif分岐を集約しない
- `FR-080`：canonical lifecycle/application serviceがExecutionのclaim、state、cancel、retry、Result/Artifact metadata commitを所有し、Generic Executorはowned workflow context内で依存順、Stage sequencing、runner invocationを実行する
- `FR-089`：Generic validationとFamily-specific validationを分離して実行する
- `FR-128a`：Algorithm/Runnerをregistry/capabilityから解決・管理するcurrent contractを維持する
- `FR-128b`（将来拡張・現行提供対象外）：size limit、timeout等のoperational resource configurationを一元管理する
