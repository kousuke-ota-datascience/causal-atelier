# 30_10_domain_resources


---

## 3. Canonical domain/application value objects

### 3.1 AnalysisFamily

```python
class AnalysisFamily(str, Enum):
    EXPLORATORY = "EXPLORATORY"
    CAUSAL = "CAUSAL"
    PREDICTIVE = "PREDICTIVE"
```

利用箇所:

- `AnalysisSpecification.analysis_family`
- `ExecutionPlan.analysis_family`
- `Execution.analysis_family`
- planner / capability selection
- API request/response Family discriminator
- Navigation Family identity

navigation用に別のFamily enumを定義しない。

### 3.2 Runtime StageType

runtime StageはNavigation Stageとは独立したversioned keyを持つ。

```python
@dataclass(frozen=True, order=True)
class StageType:
    namespace: str
    name: str
    version: str
```

Validation:

- `namespace` / `name`: lower snake case、先頭は英小文字。
- `version`: 1以上の整数を表す文字列。
- runtime key: `"{namespace}.{name}.v{version}"`。

Serialization example:

```json
{"namespace":"predictive","name":"train","version":"1"}
```

StageTypeはRunner Registry / ExecutionPlan / StageExecutionのruntime contractであり、UI Stage slugから自動生成しない。

### 3.3 ResourceRef

runtime/application boundaryでresourceを参照する場合、domain objectそのものではなくstable identifierを用いる。

```python
@dataclass(frozen=True)
class ResourceRef:
    resource_type: str
    resource_id: str
    project_id: str
    schema_version: str | None = None
    content_hash: str | None = None
```

Project境界を保持し、versioned/canonical resourceではschema version / content hashを補助identityとして保持できる。Navigation Stageはpersistent Resourceではないため`ResourceRef(resource_type="NavigationStage", ...)`を作らない。

### 3.4 NavigationStageDescriptor

```text
NavigationStageDescriptor
├─ stage_id
├─ slug
├─ label
└─ order
```

### 3.5 FamilyNavigationDescriptor

```text
FamilyNavigationDescriptor
├─ family: AnalysisFamily
├─ slug
├─ label
├─ default_stage_id
└─ stages[]: NavigationStageDescriptor
```

Catalog invariant:

1. Familyは3件、各Family 1件。
2. Family slugはglobalに一意。
3. Family内`stage_id`と`slug`は一意。
4. `default_stage_id`は当該Family catalog内に存在する。
5. `order`はdeterministicである。
6. catalogからruntime StageType / StageDefinitionを生成しない。

### 3.6 Frozen navigation catalog

```text
EXPLORATORY / exploratory / default=profile
  profile
  data-quality
  distribution
  relationships
  comparison
  findings

PREDICTIVE / predictive / default=setup
  setup
  train
  predict
  metrics
  explainability
  model-management

CAUSAL / causal / default=setup
  setup
  discovery
  identification
  estimation
  effects
  diagnostics
  sensitivity
```

Catalog authorityはFamily Capability descriptorであり、application/interface aggregatorがread-only metadataとして公開する。

```text
GET /api/v1/navigation/analysis
schema_version = analysis-navigation/1
```

Frontendはlabel/order/default Stageを含むfull catalogをhard-codeしてduplicate ownershipしない。

---

### 3.7. `GraphVersion`（EXISTING Product Domain：Owner 7区分）

#### 3.7.1. 識別情報・責務

- **Class/module:** `ariadne.product.domain.graph_version.GraphVersion`。**EXISTING**、Source blob `37ff76e001c8e269a00127e18d375f1dbc34c0e3`。
- **責務:** Product Project-scoped Graph provenance、`DRAFT`での編集、`FIXED`での変更禁止、designated outcomeの妥当性。E11 LocalのPAG/temporal Graph Evidence、Estimand科学的識別、独立Graph Oracleは責務外。
- **Scope:** 既存DB/Product DomainのAuthority。E11 Localからの同一クラス無条件reuseはSourceで証明されていない。

#### 3.7.2. フィールド

| Field | Python type / default | 生成元・制約 |
| --- | --- | --- |
| `graph_version_id` | `str`、UUID4 factory | immutable conceptual identity |
| `project_id` | `str=""` | Product Project scope |
| `source_result_id` | `str|None` | DISCOVERED origin reference |
| `parent_graph_version_id` | `str|None` | USER_EDITED/CONSTRAINT_ADJUSTED provenance |
| `designated_outcome_node` | `str|None` | must be node of graph when checked |
| `name` | `str=""` | human label |
| `graph_type` | `GraphType=DAG` | passed to canonical_graph |
| `graph_origin` | `GraphOrigin=USER_DEFINED` | origin-specific source/parent rule |
| `provenance_json` | `dict[str,Any]` / factory | origin metadata |
| `graph_json` | `dict[str,Any]` / factory | canonicalized by apply_edit |
| `content_hash` | `str=""` | source Class does not itself recompute it in apply_edit |
| `edit_rationale` | `str|None` | required when changing designated outcome |
| `status` | `GraphVersionStatus=DRAFT` | transition to FIXED |
| `created_by` | `str=""` | caller |
| `created_at` | `datetime|None` | caller/persistence |

#### 3.7.3. Constructor / Factory

`@dataclass`の自動生成`__init__`を使用し、`graph_version_id`はUUID4 factory、複数のdictは個別factory。構築後の`__post_init__()`は`validate_origin()`を呼び、`graph_origin`と`source_result_id`／`parent_graph_version_id`の組合せを検証する。**N/A:** 専用static factory・外部Backend importは実Sourceにない。

#### 3.7.4. メソッド

| Signature（Sourceの概形） | Return | Behavior / Failure |
| --- | --- | --- |
| `__post_init__(self) -> None` | None | origin validation |
| `validate_origin(self) -> None` | None | source/parent rule違反で`ValueError` |
| `apply_edit(self, graph_json: dict[str,Any], edit_rationale: str|None=None, designated_outcome_node: str|None=None, *, update_outcome: bool=False) -> None` | None | DRAFTのみmutation、canonical_graph、outcome不整合はInvalidAnalysisSpec、FIXEDはGraphAlreadyFixed |
| `fix(self) -> None` | None | DRAFT→FIXED、二重fixはInvalidStateTransition |
| `validate_outcome(self) -> None` | None | designated outcomeがnodesに無い場合InvalidAnalysisSpec |

#### 3.7.5. 処理仕様

- `validate_origin`は DISCOVERED→source required、CONSTRAINT_ADJUSTED→sourceまたはparent、USER_DEFINED/IMPORTED→source・parentとも無し、USER_EDITED→parentありsource無し。
- `apply_edit`は`FIXED`を拒否、`canonical_graph(self.graph_type, graph_json)`を適用し、必要ならoutcomeを更新。指定Outcome変更時は空でないedit_rationale必須。Source Methodは`graph_json`を更新するが`content_hash`を再計算していないため、Hashの整合性はService/ORM等の別責務として追跡する必要がある。
- `fix`はStatusのみ更新して固定化。GraphがFIXEDでも科学的に正しい因果グラフとは限らない。ProductのGraphVersionをそのままE11 LocalのFCI circle・PAG・time-lagのlossless Codecとみなさない。

#### 3.7.6. I/O・連携・失敗処理

- **I/O:** Class自体はin-memory Domain Entity（FS/DB CRUDはN/A）。Product Graph persistence・Content Hash・Lineageの完全性は呼出元Service／Repository adapterが保証する。
- **Technical errors:** `ValueError`（origin）、`GraphAlreadyFixed`、`InvalidAnalysisSpec`（outcome）、`InvalidStateTransition`（fix）。原Classにはretry/rollback実装無し（N/A）。`FIXED`状態の編集は不可。
- **E11 boundary:** Proposed Local GraphEvidenceは別Domain version/Schema、ProductとGraph型の同等性は独立Adapter＋Graph Oracleで判定する。

#### 3.7.7. 検証

**Unit:** origin組合せ全種、canonical edit、outcome node変更のrationale、FIXED再編集/二重fix拒否、`content_hash`の所有者責務。**Contract:** Product GraphVersion persistenceとのroundtrip、Graph identity/hash、legacy v2 regression。**Negative:** PAG circle/temporal graphをこのClassに入れても科学的lossless成功を無根拠に宣言しない。**Trace:** Product Graph/Lineageの既存要件、E11 FR-186/196／AR-028/036、BD01-F04/F06/F07。Source静的確認のみ。テスト実測NOT_RUN。

### 3.8. Chapter-wide Requirement Trace

- **`FR-007`**：Executionは参照ResearchContextVersionを固定し、受付時のobjective/rationale等の再現に必要なsnapshot metadata/hashを保持する。ResearchContext全体の重複保存を必須化しない

