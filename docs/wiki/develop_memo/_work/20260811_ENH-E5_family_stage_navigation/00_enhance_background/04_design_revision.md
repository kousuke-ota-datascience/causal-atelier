# ENH-E5 設計改定

- 文書状態: `APPROVED`
- Revised effective design targets:
  - `21_logical_data_design.md`
  - `22_product_basic_design.md`
  - `23_api_interface_design.md`
  - `30_detailed_design.md`
- D2 freeze authority: `40_operator_workflows/preflight_analysis/d2_planning_decision_freeze.md`

## 0. 設計改定の結論

Phase Iでは設計を次の3層として再構成する。

1. **D1 current contract correction** — source-aligned current implementationを正本へ反映。
2. **D2 ENH-E5 target design** — Phase G freeze済みcontractを正本へ具体化。
3. **D3 deferred design** — current E5 targetから除外しRequirement/90 ledgerへtrace。

Phase H以降、`06/Pxx`で設計decisionを新規発明してはならない。

## 1. D1 — Current implementation correction

### 1.1 Domain / logical data

- `AnalysisFamily={EXPLORATORY, CAUSAL, PREDICTIVE}`をcurrent identityとして維持する。
- `AnalysisSpecification.analysis_family`をdiscriminatorとして維持し、`family/current_family`等を追加しない。
- Project direct fieldに`decision_context`を追加せずResearchContextVersion ownershipを維持する。
- canonical `Execution`へ架空の`execution_plan_id` direct columnを追加しない。
- retry attemptは`StageExecution.attempt_count`ではなくappend-only `StageAttempt`として扱う。
- Result/Artifact direct fieldにfamily/generic schema_version等を捏造しない。
- `Artifact.object_key`をstorage locatorとし、存在しない`storage_uri/deleted_at`をcurrent field化しない。
- schema registryはcurrent `schema_version` key semanticsを正とする。
- generic listをcanonicalization時に自動sortしない。

### 1.2 Runtime / workflow

- current `StageType / StageDefinition / ExecutionPlan / StageExecution`をruntime責務として維持する。
- Causal current compatibility plannerはone-operation/one-stage mapping。
- Predictive full planは`split -> prepare -> train -> evaluate -> optional explain`。
- Exploratory current plannerはoperationごとに1 runtime Stage。
- `PlanValidator`はgeneric plan/runner/dependency/binding/cycle validationを担当し、Family-specific policyを過大に持たせない。
- `StageRunnerRegistry.register(runner)` / `resolve(stage_type)` / `contains(stage_type)`のcurrent contractを正とする。
- `StageExecution`のCANCELLED transitionをcurrent state modelへ反映する。

### 1.3 Authorization / API / Ports

- persisted Project roleは`OWNER / EDITOR / VIEWER`。
- current request identityはBearer/OIDCを前提とせず、現実装のidentity boundaryを正確に記載する。
- Worker claim/lease authorityはrepository `claim_next / renew_lease / complete`とExecution lease fields。
- 架空のpublic Execution/Stage event publisherをcurrent componentとして記載しない。
- current CLIはscientific local/headless boundaryでありgeneric Product submit/poll CLIではない。
- current Port setをsourceに合わせ、存在しないrunner/auth/event Portをcurrent architectureとして記載しない。
- `ArtifactStore` Portはcurrent baseline、adapterは`LocalArtifactStore`をcurrentとして記載する。
- current architectureから未実装Outboxを除去する。

### 1.4 Result / Artifact / Lineage

- canonical Result/Artifact responsibilityをcurrent sourceへ合わせる。
- Predictive metric/errorをすべてArtifact化せずResult payloadとの責務を保持する。
- current lineage classifierのtyped/generic-only relationをsource-aligned authorityとして記載する。

## 2. Navigation architecture — frozen target

### 2.1 Concept boundary

`NavigationStageDescriptor` / `FamilyNavigationDescriptor` / current Family/StageはDomain Resource外のapplication/navigation conceptとする。

Navigation Stageを次へpersistしない。

- AnalysisSpecification
- ExecutionPlan
- Execution
- StageExecution

Navigation Stageをruntime StageType/StageDefinitionへ変換するgeneric mapperを作らない。

### 2.2 Catalog ownership

```text
Family Capability
  owns immutable FamilyNavigationDescriptor
        ↓
Application / Interface aggregator
        ↓
GET /api/v1/navigation/analysis
        ↓
Frontend
```

Endpoint:

```text
GET /api/v1/navigation/analysis
```

Schema:

```text
analysis-navigation/1
```

`analysis-navigation/1`はpresentation/API metadata schemaでありscientific generic `SchemaRegistry`へ登録しない。

Frontendはlabel/order/default Stageのfull catalogをduplicate ownershipしない。

### 2.3 Canonical route

```text
/projects/{project_id}/analysis/{family_slug}/{stage_slug}
```

Legacy `/explore`, `/causal`, `/predictive`を残す場合、Family default Stageへ一方向normalizeする。

URL/Application stateがcurrent navigation authority。

### 2.4 Family catalogs

| Family | slug | default | Stages |
|---|---|---|---|
| EXPLORATORY | `exploratory` | `profile` | profile, data-quality, distribution, relationships, comparison, findings |
| PREDICTIVE | `predictive` | `setup` | setup, train, predict, metrics, explainability, model-management |
| CAUSAL | `causal` | `setup` | setup, discovery, identification, estimation, effects, diagnostics, sensitivity |

## 3. PF-D2-01 — AnalysisView Typed Filter Validation

### 3.1 Compatibility

current operator taxonomyを維持し、Dataset source column logical typeとoperator/valueのcompatibilityをdomain/application validationへ追加する。

Required rule summary:

- BOOLEAN: EQ/NE/IN/NOT_IN/IS_NULL/NOT_NULL
- INTEGER/REAL/DATETIME: relational + membership + null operators
- TEXT: EQ/NE/IN/NOT_IN/IS_NULL/NOT_NULL
- OTHER: IS_NULL/NOT_NULL only
- IS_NULL/NOT_NULLはvalueなし
- IN/NOT_INはnon-empty list
- time_cutoffはDATETIME + LT/LTE
- type不明はvalidation successにしない

Stable code:

`FILTER_TYPE_MISMATCH`

AnalysisView persistent schemaは変更しない。

## 4. PF-D2-02 — Exploratory Handoff & Provenance

### 4.1 Explore → AnalysisView DRAFT

AnalysisViewへ移すdata-selection semantics:

- row_filter
- selected_columns
- derived_columns
- missing_value_policy
- time_cutoff
- sampling

chart mark/encoding/panel layout等のpresentation-only stateは移さない。

### 4.2 Exploratory Result → AnalysisSpecification DRAFT

- canonical AnalysisSpecification resourceをDRAFTとしてpersist。
- target_family = CAUSAL / PREDICTIVE。
- requestはanalysis_mode = EXPLORATORY / CONFIRMATORYを明示。
- dataset_version_id / analysis_view_idはsource lineageから導出。
- DRAFTは未完成family_specを許容。
- Result `--MOTIVATED-->` AnalysisSpecification semantic lineageを保存。
- auto FIX / auto executionは禁止。
- same-data confirmatoryはPF-D2-04 warningを付与。

## 5. PF-D2-03 — Predictive Subgroup Evaluation

- evaluation population = untouched TEST。
- specified subgroup columnを各column独立でslice。
- automatic intersection/discovery/fairness frameworkは追加しない。
- null subgroupはexplicit null group。
- sample_countは必須。
- uncertainty = nonparametric percentile bootstrap。
- confidence=0.95。
- resamples=1000。
- deterministic seed。
- valid_resamples < 200はCIなし + warning。
- non-computable metricはvalue/uncertaintyをnullとしstatus/warningを返す。
- outputはgroup valueをmap keyへ埋め込まずlist record。

## 6. PF-D2-04 — Scientific Comparability & Exploratory-Reuse Guard

Comparison:

1. `semantic_compatible`
2. `direct_metric_comparable`

Predictive semantic key:

- task_type
- target/outcome
- prediction unit
- prediction time
- horizon
- deployment/evaluation population semantics

Direct metric comparability:

- same dataset_version_id
- same TEST-row identity/hash
- same metric definition

Causal semantic key:

- treatment/exposure
- outcome
- estimand
- target population

same-data:

> same immutable `dataset_version_id`

warning:

`EXPLORATORY_REUSE_SAME_DATA`

non-blocking。先行Exploratory Result IDをevidenceとして保持しExecution snapshotへwarningを伝播する。

## 7. PF-D2-05 — Command Idempotency & Retry-safe Artifact Commit

### 7.1 Applicability

idempotency対象は「POST/create」ではなくduplicate durable side effectを生成し得るCommand。

Scope:

```text
(project_id, command_scope, idempotency_key)
```

Required endpoint:

- missing key → `IDEMPOTENCY_KEY_REQUIRED`
- same key + same canonical semantic request → stored response replay
- same key + different request → HTTP 409 / `IDEMPOTENCY_CONFLICT`

ExecutionPlan create等、existing natural idempotencyがあるものへheaderを無理に要求しない。

### 7.2 Artifact retry safety

exactly-once executionは保証しない。

same successful Stage outputのretry/restartでdurable Artifactを重複materializeしない。

logical identity/object keyをExecution/Stage/output slot/Artifact typeからdeterministically導出する。

same logical output + same content hashはreuse。

same logical output + different content hashはnondeterministic-output conflict。

cross-store compensationはNFR-007=D3。

## 8. PF-D2-06 — Project Authorization & Sensitive Output Boundary

Persisted role:

`OWNER / EDITOR / VIEWER`

| Action | OWNER | EDITOR | VIEWER |
|---|---:|---:|---:|
| Project READ | allow | allow | allow |
| WRITE/MUTATE | allow | allow | deny |
| Execution mutation | allow | allow | deny |
| Export create | allow | allow | deny |
| Membership admin | allow | deny | deny |
| Explicit sensitive output | allow | allow | deny |

独立EXECUTE roleは追加しない。

全project-scoped routeはservice action前にProject membership authorizationを通す。

prediction/local explanation row/detailはpotentially sensitive output。

configurable sensitive-column policyはD3。

## 9. PF-D2-07 — Canonical Lineage Completion

Read model minimum:

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

追加input:

- DatasetVersion
- AnalysisView
- GraphVersion
- input Result
- base Execution

canonical FK/snapshotで決定可能なstructural relationをgeneric LineageEdgeへ重複persistしない。

LineageEdgeはMOTIVATED等のsemantic relationへ利用する。

## 10. PF-D2-08 — Reproducibility Metadata Completion

### 10.1 Migration

従来の`DB migration: NONE`は撤回する。

追加:

```text
StageAttempt.effective_random_seed: int | null
```

- stochastic Stage actual seedをattempt単位で保存。
- deterministic Stageはnull。
- retry同一logical Stageはsame effective seedを再利用。
- runner boundaryがactual seedをprocessorへ返却可能にする。

### 10.2 Runtime manifest

Execution snapshot `runtime_version_json`へ最低限:

- ariadne_code_version
- python_version
- platform_system
- platform_release
- machine
- libraries

scientific library versionは実際のregistered/used runner dependency setからcaptureする。

## 11. PF-D2-09 — Frontend Deep Navigation, Action State & Accessibility

Resource route:

```text
/projects/{project_id}/analysis/{family_slug}/{stage_slug}/resource/{resource_type}/{resource_id}
```

resource_type:

- analysis-specification
- execution
- result
- graph-version

Backend action availability response:

```text
{allowed, reason_code?, message?}
```

Presentation state:

`IDLE / LOADING / READY / EMPTY / PARTIAL / ERROR / CANCELLED`

Accessibility対象はENH-E5変更surface。

- keyboard
- deterministic focus
- accessible names
- error association
- non-color semantics
- normal text contrast >= 4.5:1
- large text / UI graphics / focus >= 3:1

full legacy UI retroactive conformanceはscope外。

## 12. PF-D2-10 — Derived E5 Test Architecture

D2 packageごとに07へverificationをtraceする。

- domain invariant → unit/domain
- persistence/concurrency/auth/lineage → integration
- API route/header/error/response → API
- Navigation/async/accessibility → frontend/browser
- import/dependency prohibition → architecture/static

D3 verification targetをE5 acceptanceへ混ぜない。

## 13. PF-D2-11 — Documentation Self-containment

`10/21/22/23/30`へD1/D2/D3と本設計freezeを反映した後、NFR-019の`DOC-019-01〜08`を再監査する。

all PASSまで`06/Pxx/07`をfinal freezeしない。

## 14. D3 — Deferred design isolation

ENH-E5 current targetから次を除外する。

- D10-005c: system/operator-level authorization
- D10-006a: general Audit contract
- D10-006b: retention/deletion contract
- D22-003b: object-storage / broader adapter variants
- D22-013c: D3 verification surfaces
- D30-018c: D3 detailed verification surfaces
- Requirement側D3に対応するimplementation/design target

D3のRequirement存在・Status/Deliveryは10、詳細ledgerは90をauthorityとする。

## 15. Predictive compatibility design

Predictive existing visible controls / generated `predictive-analysis-spec/1` semanticsを100%保持する。

禁止:

- field削除
- field rename
- default semantics変更
- stage再配置を理由にexecution semanticsを変更
- LightGBM等のfuture engine追加

Stage再配置:

- setup
- train
- predict
- metrics
- explainability
- model-management

## 16. CLI / library independence

backend execution function signatureへNavigation Stage required argumentを追加しない。

scientific CLI/library/runtime contractはNavigation metadata APIから独立する。

## 17. Phase I文書別反映

| Canonical document | Phase I responsibility |
|---|---|
| 21 | persistent/current logical data + navigation non-resource concepts + lineage + StageAttempt seed |
| 22 | responsibility boundaries, capability/application/runtime, authorization, test architecture |
| 23 | exact API/routes/errors/headers/response contracts |
| 30 | class/module responsibilities, validation algorithms, persistence/migration, test seams |

Phase Iで不足が見つかった場合は、Phase G freezeと矛盾する仕様を30/06で発明しない。必要ならpreflight decision recordを先にamendする。
