# ENH-E5 D2 Planning Decision Freeze

- **Phase:** G — D2 unresolved planning decisions freeze
- **Status:** `FROZEN`
- **Date:** 2026-08-12 (Asia/Tokyo)
- **Scope:** `remediation_decision_matrix.csv` の D2 **35 Decision Item**
- **Freeze packages:** **11**
- **Unassigned D2 items:** **0**
- **Normative status:** 本書はpreflight planning decision recordでありCoding/Test Agent向けnormative contractではない。

## 0. Authority and use

本書は、D2裁定済み項目について、`10/21/22/23/30` および `06/Pxx/07` を作成する前に残っていたscope、algorithm、route、error semantics、persistence boundary等のplanning decisionをfreezeする。

情報流:

```text
source/static evidence
        ↓
this D2 planning freeze
        ↓
03 / 04 / 05
        ↓
10 / 21 / 22 / 23 / 30
        ↓
NFR-019 documentation audit PASS
        ↓
06 / Pxx / 07
```

禁止:

- Coding Agentが本書を読んで不足specを補完すること。
- 下流`06/Pxx`で本書と異なる設計decisionを新規に発明すること。
- D3 itemを本書からENH-E5 acceptanceへ復活させること。
- Navigation StageをExecution Stage/StageTypeへ対応付けること。

### 0.1 Evidence boundary

current implementation factの確認には、feature branch上のsourceおよびcurrent v5 documentsを用いた。これはE4 alignment baselineを置き換えるものではない。D2はE5 target decisionであり、current sourceに存在しない部分は本書のplanning decisionとして明示的にfreezeする。

## 1. Freeze package index

| Package | Title | Decision Items | Code | Migration |
|---|---|---|---|---|
| `PF-D2-01` | AnalysisView Typed Filter Validation | `FR-015`, `D21-005` | YES | NO |
| `PF-D2-02` | Exploratory Handoff & Provenance | `FR-020`, `FR-032`, `FR-034` | YES | NO |
| `PF-D2-03` | Predictive Subgroup Evaluation | `FR-067`, `AR-016` | YES | NO |
| `PF-D2-04` | Scientific Comparability & Exploratory-Reuse Guard | `AR-017`, `FR-072`, `FR-051`, `AR-004` | YES | NO |
| `PF-D2-05` | Command Idempotency & Retry-safe Artifact Commit | `FR-114b`, `FR-082`, `NFR-006b` | YES | NO* |
| `PF-D2-06` | Project Authorization & Sensitive Output Boundary | `D10-005b`, `FR-121`, `FR-123a`, `FR-124b`, `NFR-008b`, `AR-020` | YES | NO |
| `PF-D2-07` | Canonical Lineage Completion | `FR-008`, `FR-054`, `FR-095`, `NFR-002` | YES | NO |
| `PF-D2-08` | Reproducibility Metadata Completion | `FR-086a`, `FR-087b`, `NFR-001b` | YES | YES (StageAttempt effective_random_seed) |
| `PF-D2-09` | Frontend Deep Navigation, Action State & Accessibility | `FR-108`, `FR-107`, `FR-109`, `FR-111`, `NFR-012` | YES | NO |
| `PF-D2-10` | Derived E5 Test Architecture | `D22-013b`, `D30-018b` | TESTS/DOCS | NO |
| `PF-D2-11` | Documentation Self-containment & Navigation Architecture Freeze | `NFR-019` | DOCUMENTATION_ONLY for NFR-019; navigation decisions consumed by E5 code | NO |

---

## PF-D2-01 — AnalysisView Typed Filter Validation

### 1.1 Frozen type/operator compatibility

対象: `FR-015`, `D21-005`。

current `analysis-view/1` のfilter operator集合を変更せず、source Dataset columnのlogical typeとの互換性をdomain/application validationで追加する。新しいexpression language、operator taxonomy、Family-specific validator、derived-expressionのfull static type inferenceは追加しない。

| Logical type | Allowed operators | Value contract |
|---|---|---|
| `BOOLEAN` | `EQ, NE, IN, NOT_IN, IS_NULL, NOT_NULL` | bool。IN系はbool list。 |
| `INTEGER` | `EQ, NE, LT, LTE, GT, GTE, IN, NOT_IN, IS_NULL, NOT_NULL` | boolを除くinteger。IN系はinteger list。 |
| `REAL` | `EQ, NE, LT, LTE, GT, GTE, IN, NOT_IN, IS_NULL, NOT_NULL` | boolを除くfinite int/float。IN系はfinite numeric list。 |
| `DATETIME` | `EQ, NE, LT, LTE, GT, GTE, IN, NOT_IN, IS_NULL, NOT_NULL` | ISO-8601 datetimeとしてparse可能なstring。IN系は同string list。 |
| `TEXT` | `EQ, NE, IN, NOT_IN, IS_NULL, NOT_NULL` | string。IN系はstring list。lexical order比較はE5では定義しない。 |
| `OTHER` | `IS_NULL, NOT_NULL` | valueなし。 |

共通:

- `IS_NULL / NOT_NULL`はvalueを持たない。
- `IN / NOT_IN`はnon-empty listを要求する。
- `time_cutoff`はsource columnが`DATETIME`で、operatorは既存どおり`LT / LTE`のみ。
- source Dataset columnのlogical typeが取得できない場合はvalidation成功にしない。
- derived columnをfilter参照する場合、E5は既存shape/reference/runtime validationを維持し、full static derived-type inferenceは追加しない。
- type mismatchはstable validation code `FILTER_TYPE_MISMATCH` とfield pathを返す。

### 1.2 Persistence/API

AnalysisView schema/persistent fieldsは変更しない。`validate`/`fix`およびcreate/update時のcanonical validation pathで同じcompatibility ruleを利用する。

---

## PF-D2-02 — Exploratory Handoff & Provenance

対象: `FR-020`, `FR-032`, `FR-034`。

### 2. Explore state → AnalysisView DRAFT

AnalysisViewへ移すのは**data-selection semanticsだけ**とする:

- `row_filter`
- `selected_columns`
- `derived_columns`
- `missing_value_policy`
- `time_cutoff`
- `sampling`

chart mark、encoding、aggregation、panel layout等のvisualization stateをAnalysisViewへ押し込まない。analysis-significant chart/aggregation parametersはExploratory `family_spec`側へ保持する。既存`POST /projects/{project_id}/analysis-views`を再利用し、新しいAnalysisView expression contractは作らない。

### 3. Exploratory Result → canonical AnalysisSpecification DRAFT

既存`create-analysis-draft`はpseudo draft identityではなく、canonical `AnalysisSpecification` resourceを**DRAFTとして実際にpersist**するようにする。

Frozen contract:

- `target_family`: `CAUSAL | PREDICTIVE`。
- requestに`analysis_mode: EXPLORATORY | CONFIRMATORY`を明示させ、serverが推測しない。
- `dataset_version_id` / `analysis_view_id`はsource Result→Execution/Specificationから導出し、requestからoverrideさせない。
- `research_context_version_id`はsource canonical lineage/snapshotから一意に導出できる場合は再利用する。導出不能ならrequestで明示必須とし、未解決なら作成を拒否する。
- `family_spec_schema_version`はtarget Familyのcanonical versionを使用する。
- DRAFTでは`family_spec={}`または未完成target specを許容し、ユーザーが編集後にvalidate/fixする。
- `Result --MOTIVATED--> AnalysisSpecification`のsemantic lineageを保存する。
- 自動FIXED、自動Execution submit、自動causal conclusion化は禁止。
- CONFIRMATORYかつsame-dataの場合はPF-D2-04のexploratory-reuse warningを付与する。

### 4. Exploratory provenance

保存対象は分析意味を再構成するparameterに限定する。

- row/filter/sampling identity → AnalysisView ID/hash
- operation/chart/aggregation parameter → normalized Exploratory family spec
- code/runtime identity → Execution snapshot
- Result/Artifact → canonical lineage

DOM/CSS/panel size等のpure presentation stateはscientific provenanceへ保存しない。

---

## PF-D2-03 — Predictive Subgroup Evaluation

対象: `FR-067`, `AR-016`。

### 5. Subgroup metric and uncertainty contract

Frozen scope:

- evaluation populationは既存contractどおり**untouched TESTのみ**。
- `evaluation_spec.subgroups`に指定されたcolumnを**各column独立**でsliceする。automatic intersection、automatic subgroup discovery、protected-attribute detectionはしない。
- subgroup columnはfeatureである必要はない。TEST rowと同一row ordinalでoriginal dataから値をevaluation bundleへ運ぶ。
- null/missing subgroup valueはsilent dropせず明示的な`null` groupとして扱う。
- metric集合は`primary_metric + secondary_metrics`。task incompatibilityは既存metric validationに従う。
- `sample_count`は常に出力する。

Uncertainty:

- method: **nonparametric percentile bootstrap**
- confidence level: **0.95**
- resamples: **1000**
- resampling unit: subgroup内row
- deterministic seed: immutable split/spec seed + subgroup column + canonical subgroup value + metric + fixed namespaceから導出
- original metricがcomputableでない場合: `value=null`, `uncertainty=null`, explicit status/warning
- original metricがcomputableでも`sample_count < 2`: uncertaintyを出さずwarning
- bootstrap metricがcomputableなresampleのみCIへ使用し、`valid_resamples`を記録
- `valid_resamples < 200`: uncertaintyを出さずwarning

Output shapeはmap-keyへgroup valueを埋め込まずlist recordとする:

```json
{
  "subgroup_metrics": [
    {
      "subgroup_column": "segment",
      "subgroup_value": "A",
      "sample_count": 42,
      "metrics": {
        "ROC_AUC": {
          "value": 0.81,
          "uncertainty": {
            "method": "PERCENTILE_BOOTSTRAP",
            "confidence_level": 0.95,
            "lower": 0.73,
            "upper": 0.88,
            "resamples": 1000,
            "valid_resamples": 997,
            "seed": 123456
          }
        }
      },
      "status": "GENERATED",
      "warnings": []
    }
  ]
}
```

E5 non-goals: fairness framework、significance ranking、multiple-testing correction、fairness-constrained training。

---

## PF-D2-04 — Scientific Comparability & Exploratory-Reuse Guard

対象: `AR-017`, `FR-072`, `FR-051`, `AR-004`。

### 6. Two-tier comparability

Comparisonは二段階とする:

1. `semantic_compatible`: 同じ科学的問い/estimand/taskを比較しているか。
2. `direct_metric_comparable`: 同じevaluation basisでquantitative delta/rankingを主張できるか。

different Familyまたはdifferent Result typeは既存どおりinvalid comparison request。same Family/typeでもsemantic key不一致の場合はHTTP success responseで`compatible=false`と`incompatibility_reasons[]`を返し、quantitative delta/rankingを生成しない。

Predictive semantic key:

- `task_type`
- prediction target/outcome
- prediction unit
- prediction time
- horizon
- deployment/evaluation population semantics

model、features、hyperparameters、split methodは**比較したい差分**になり得るためsemantic keyへ入れない。

Predictive direct metric comparabilityは追加で:

- same `dataset_version_id`
- same TEST-row identity/hash
- same metric name/definition

Causal semantic key:

- treatment/exposure
- outcome
- estimand definition/type
- target population

Causal direct quantitative comparisonは追加でsame data/view/analysis populationを要求する。

Exploratoryはsame operation/result typeかつmeasured variable semanticsがcompatibleな場合のみ比較する。cross-metric rankingは行わない。

### 7. Exploratory reuse / confirmatory warning

`same-data`は**同一immutable `dataset_version_id`**と定義する。AnalysisViewが違ってもsame-dataである。

CONFIRMATORY AnalysisSpecificationをvalidate/fixするとき、同一Project・同一DatasetVersionに先行Exploratory Resultが存在する場合:

- warning code: `EXPLORATORY_REUSE_SAME_DATA`
- non-blocking warningとする。
- evidenceとして先行Exploratory Result ID群を保持する。
- warningはAnalysisSpecification → Execution snapshotへ伝播する。
- PF-D2-02のResult→AnalysisSpecification handoffは`MOTIVATED` lineageを保存する。

---

## PF-D2-05 — Command Idempotency & Retry-safe Artifact Commit

対象: `FR-114b`, `FR-082`, `NFR-006b`。

### 8. Idempotency applicability inventory

適用基準はHTTP POST/createではなく、**同一request再送でduplicate durable side effectを生成し得るCommandか**とする。

#### Required

- DatasetVersion create（existing）
- Execution batch create（existing）
- GraphVersion create（existing）
- GraphEditDraft create（existing）
- Result export create（existing）
- AnalysisView create
- Exploration execution submit
- Exploratory Result → canonical AnalysisSpecification DRAFT create
- ResearchContext create
- AnalysisSpecification create
- AnalysisSpecification revise
- Predictive split-validation（durable Execution/Artifact作成）
- Predictive Execution submit
- Predictive Execution rerun
- Predictive Execution revise
- Annotation create / WorkspaceAnnotation create
- Product Export create

#### Not required by E5 idempotency header contract

- pure GET/query/compare/preview/validate
- ExecutionPlan create: existing content/plan-hash deduplicationをcanonical natural idempotencyとして維持
- explicit lineage-link create: existing uniqueness/re-fetch semanticsをnatural idempotencyとして維持
- Project create: current project-scoped idempotency mechanismのscope外。FR-114aの裁定どおり「全create」を対象化しない。
- cancel/fix/update等: duplicate durable resourceを作らないstate-transition commandはstate-machine/idempotent updateで扱う。

### 9. Key/scope/replay/conflict contract

- scope identity: `(project_id, command_scope, idempotency_key)`を維持する。
- Required endpointでは`Idempotency-Key`を必須とする。missingは`IDEMPOTENCY_KEY_REQUIRED` validation error。
- same key + same canonical semantic request → stored responseをreplayし、新しいside effectを作らない。
- same key + different canonical semantic request → HTTP `409`, code `IDEMPOTENCY_CONFLICT`。
- `command_scope`はendpoint/actionごとのstable literal。
- request hashにはbodyだけでなく、semantic identityへ影響するpath resource IDも含める。Project IDはscopeに含む。
- concurrent same keyはDB uniqueness/advisory transaction lockでserializeする。SQLite test pathではprocess lockを許容する。
- replay recordはCommand side effectと同じDB transaction boundaryでcommitできるpathでは同一transactionに含める。

### 10. NFR-006b retry-safe Artifact materialization

E5は**exactly-once execution**を保証しない。保証するのは、同じsuccessful Stage outputをretry/restartしてもdurable Artifact materializationがduplicateしないこと。

Frozen contract:

- Artifact logical identity/object keyは`execution_id + stage_execution_id + stable output slot/ordinal + artifact_type`からdeterministically導出する。
- retryでsame logical outputかつsame content hashなら既存Artifact row/objectをreuseする。
- same logical outputでcontent hashが変化した場合はnondeterministic-output conflictとしてfailし、silent overwrite/new duplicateを作らない。
- Result/Artifact output bindingのDB persistenceはtransactionalにcommitする。
- store-before-DB crashで発生し得るorphan cleanup/compensationは`NFR-007=D3`のためE5では一般化しない。
- 上記deterministic identityを採用するため、本D2では新しいArtifact uniqueness columnのDB migrationを必須にしない。実装上既存schemaで保証不能と判明した場合は30でmigrationを明示し、06で発明しない。

---

## PF-D2-06 — Project Authorization & Sensitive Output Boundary

対象: `D10-005b`, `FR-121`, `FR-123a`, `FR-124b`, `NFR-008b`, `AR-020`。

### 11. Project role/action matrix

persisted Project roleは既存の3値のみ:

- `OWNER`
- `EDITOR`
- `VIEWER`

| Action class | OWNER | EDITOR | VIEWER |
|---|---:|---:|---:|
| Project-scoped READ | allow | allow | allow |
| WRITE / MUTATE | allow | allow | deny |
| Execution submit/cancel/retry/rerun/revise | allow | allow | deny |
| Export create | allow | allow | deny |
| Membership role administration | allow | deny | deny |
| Explicit sensitive-output access | allow | allow | deny |

独立`EXECUTE` permission/roleは追加しない。Execution mutationはWRITEとして扱う。

全project-scoped routeはservice action前にProject membership authorizationを通す。legacy generic routeを残す場合もresource→projectをresolveし、同じrole policyを適用する。

### 12. Sensitive Result / Artifact / Prediction boundary

- Result一覧/通常detailはVIEWERを含むREAD roleで取得可。
- `include_sensitive`相当のexplicit opt-inはOWNER/EDITORのみ。
- prediction rowおよびlocal explanation row/detailは潜在的sensitive outputとして扱い、VIEWERにはaggregate/suppressed surfaceのみ返す。
- Artifact metadata/downloadもresource→project ownershipをresolveしてREAD authorizationを通す。
- sensitive column metadata/configurable minimization policyはD3なので、本D2で新taxonomyを作らない。

---

## PF-D2-07 — Canonical Lineage Completion

対象: `FR-008`, `FR-054`, `FR-095`, `NFR-002`。

### 13. Structural vs semantic lineage

canonical FK/snapshot/identityからdeterministically導出できるstructural relationを、generic `LineageEdge`へ重複persistしない。`LineageEdge`は`MOTIVATED`, `SUPPORTED_BY`, `SELECTED`, `REJECTED`, `DERIVED_FROM`等、構造だけでは表せないsemantic relationへ使う。

lineage read modelは最低限以下のchainを辿れること:

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

さらに入力としてDatasetVersion / AnalysisView / GraphVersion / input Result / base Executionを接続する。

Frozen rules:

- `research_context_usage`はcompatibility FamilyExecutionだけでなくcanonical AnalysisSpecification/Execution metadataからExecutionまでprojectしなければならない。
- Predictive/Causal/ExploratoryすべてでSpec→Plan→Execution→Stage→Result→Artifactをread model上辿れる。
- Causal lineageではtreatment graph/input Result、identification、estimation、refutation/sensitivityの実在identityを使い、存在しないedgeを推測しない。
- Result lineage responseはupstream Specification/Plan/Stage chainを含む。
- FR-032 handoff等の科学的意味を持つcross-resource relationはexplicit semantic edgeとして保存する。
- universal new lineage persistence tableは追加しない。

---

## PF-D2-08 — Reproducibility Metadata Completion

対象: `FR-086a`, `FR-087b`, `NFR-001b`。

### 14. Per-attempt effective random seed

- `Execution.random_seed`はtop-level request/spec seedとして維持。
- stochastic Stageが実際に使用したseedは**StageAttempt単位**で`effective_random_seed: int | null`として保存する。
- deterministic Stageは`null`。
- retryされた同一logical Stageは、immutable specification/revisionでseed変更がない限り同じeffective seedを再利用する。各attemptに記録する。
- StageRunner/StageRunResult boundaryがactual effective seedをprocessorへ報告できるcontractを持つ。
- このfield追加はDB migration対象。

### 15. Runtime dependency manifest

Execution snapshotの`runtime_version_json`へ、再実行環境を識別するmanifestをimmutableに保存する。

最低field:

- `ariadne_code_version`
- `python_version`
- `platform_system`
- `platform_release`
- `machine`
- `libraries`: 実際にregistered/used runnerが依存するscientific library名→version

E5 common baselineとして少なくとも`numpy`, `pandas`を、Predictive runnerが利用する場合は`scikit-learn`等を記録する。optional/future libraryをversion取得だけのためimportしない。runner/capabilityがruntime dependency setを宣言し、capture側がversionをresolveする。

Reproducibility requirementは**bit-for-bit numerical identityの保証**ではなく、同じscientific input/seed/code/runtime/library environmentを再構築するのに必要な情報を保持することとする。

---

## PF-D2-09 — Frontend Deep Navigation, Action State & Accessibility

対象: `FR-108`, `FR-107`, `FR-109`, `FR-111`, `NFR-012`。

### 16. Resource deep route

canonical Family/Stage routeを維持し、その下にresource focus tailを追加する:

```text
/projects/{project_id}/analysis/{family_slug}/{stage_slug}/resource/{resource_type}/{resource_id}
```

E5 resource_type:

- `analysis-specification`
- `execution`
- `result`
- `graph-version`

routeはNavigation/Application stateでありDBへ保存しない。explicit Family/Stage付きlinkではそのStageを保持する。generic resource direct-link解決時はresource ownershipからFamilyを解決し、そのFamilyのdefault Stageへ遷移してresourceをfocusする。Project/Family/resource不一致はexplicit errorでありsilent fallbackしない。

### 17. Backend-authoritative action availability

- UIはbackendのaction availabilityを正本とする。
- local form invalid等で追加disableは可能だが、backendがdenyしたactionをfrontend判断でenableしてはならない。
- action responseは`{allowed, reason_code?, message?}`を持つ。
- Stage visibilityとaction availabilityは別state。
- operation availability read endpointはproject-scopedとする。

### 18. Async UI state taxonomy

presentation-only state:

- `IDLE`
- `LOADING`
- `READY`
- `EMPTY`
- `PARTIAL`
- `ERROR`
- `CANCELLED`

`PARTIAL`は利用可能なprimary dataが存在するがwarning/secondary data不足がある状態。`ERROR`とは区別する。`CANCELLED`はbackend execution stateがcancelledの場合のみ使用し、Navigation Stage変更をcancel扱いしない。

### 19. Accessibility acceptance

ENH-E5で新規/変更するFamily/Stage surfaceに対して:

- keyboard onlyで主要navigation/actionを操作可能。
- deterministic focus orderとvisible focus indicator。
- Family/Stage route切替後はmain heading/regionへdeterministic focus management。
- icon/controlにsemantic accessible nameを持たせる。
- error/warningを該当control/regionへ関連付ける。
- status/selection/errorを色だけで表現しない。
- text contrast: normal text 4.5:1以上、large textおよびUI graphics/focus等3:1以上をE5 acceptance thresholdとする。
- full product全体のretroactive conformanceはE5 scope外。変更surfaceを対象とする。

---

## PF-D2-10 — Derived E5 Test Architecture

対象: `D22-013b`, `D30-018b`。

### 20. Verification derivation rule

- 本書の各PF-D2 packageを`07`へtraceする。
- domain/business invariant → unit/domain test
- persistence/concurrency/authorization/lineage → integration test
- API route/header/error/response → API test
- Navigation/async/accessibility → frontend/browser test
- import/dependency prohibition → architecture/static test
- D3 targetのverificationをENH-E5 acceptanceへ混入させない。
- `06/Pxx`のimplementation completionだけでPASS扱いにせず、`07`の独立verificationを必要とする。

---

## PF-D2-11 — Documentation Self-containment & Navigation Architecture Freeze

対象: `NFR-019`。

NFR-019自体はdocumentation-only D2だが、現在の10/22/23/30に残るNavigationの未freeze decisionをここで確定し、`30 → 06`のauthority順序を回復させる。

### 21.1 Navigation catalog authority

**Backend read-only metadata endpoint方式を採用する。**

- canonical endpoint: `GET /api/v1/navigation/analysis`
- response schema: `analysis-navigation/1`
- each Family capability owns immutable `FamilyNavigationDescriptor`。
- application/interface aggregatorが3 Family descriptorをvalidate/aggregateしてendpointから返す。
- frontendはendpointをcatalog authorityとして利用し、label/order/default Stageのfull catalogをduplicate ownershipしない。
- Runner registry / planner registry / Execution Planとは別authority。Navigation catalogからruntime Stageを生成しない。

### 21.2 Schema ownership

`analysis-navigation/1`はpresentation/API metadata schemaであり、generic scientific `SchemaRegistry`へ登録しない。専用Navigation catalog validator/providerがshape/invariantを検証する。

### 21.3 Family slug / default Stage

| Family | slug | default_stage_id |
|---|---|---|
| `EXPLORATORY` | `exploratory` | `profile` |
| `CAUSAL` | `causal` | `setup` |
| `PREDICTIVE` | `predictive` | `setup` |

Stage catalogsはcurrent E5 designの列挙を維持:

- Exploratory: `profile`, `data-quality`, `distribution`, `relationships`, `comparison`, `findings`
- Predictive: `setup`, `train`, `predict`, `metrics`, `explainability`, `model-management`
- Causal: `setup`, `discovery`, `identification`, `estimation`, `effects`, `diagnostics`, `sensitivity`

### 21.4 Route authority

canonical current Family/Stage route:

```text
/projects/{project_id}/analysis/{family_slug}/{stage_slug}
```

legacy `/explore`, `/causal`, `/predictive`を残す場合はFamily default Stageへ一方向normalizeする。URL/application stateがcurrent navigation authorityであり、DB/AnalysisSpecification/ExecutionへNavigation stateを保存しない。

### 21.5 NFR-019 completion rule

10/21/22/23/30へ上記および全D1/D2/D3 decisionを反映した後、既存`DOC-019-01`〜`DOC-019-08`を再監査し、**all PASSになるまで06/Pxx/07を最終freezeしない**。

---

## 22. D2 Freeze completeness

- remediation matrix D2 rows: **35**
- freeze matrix rows: **35**
- packages: **11**
- unassigned: **0**
- duplicate assignment: **0**
- freeze status not FROZEN: **0**

### 22.1 Remaining unresolved planning decisions

**0件。**

以後、上記decisionに不足・矛盾が発見された場合は`06/Pxx`で補完せず、本書および`d2_planning_decision_matrix.csv`を先にamendして再freezeする。

## 23. Downstream document obligations

| Package | Required downstream convergence |
|---|---|
| `PF-D2-01` | `10,21,23,30,06,07` |
| `PF-D2-02` | `10,21,22,23,30,06,07` |
| `PF-D2-03` | `10,22,23,30,06,07` |
| `PF-D2-04` | `10,21,22,23,30,06,07` |
| `PF-D2-05` | `10,21,22,23,30,06,07` |
| `PF-D2-06` | `10,22,23,30,06,07` |
| `PF-D2-07` | `10,21,22,23,30,06,07` |
| `PF-D2-08` | `10,21,22,23,30,06,07` |
| `PF-D2-09` | `10,22,23,30,06,07` |
| `PF-D2-10` | `22,30,06,07` |
| `PF-D2-11` | `10,21,22,23,30,06,07` |

特に`PF-D2-11`のNavigation決定は23/30へ先に反映し、NFR-019再監査PASS後に06/Pxxへ転記する。

## 24. Static evidence inspected

Planning freeze時に少なくとも以下をcurrent feature branchで照合した。

- `src/ariadne/product/domain/analysis_view.py`
- `src/ariadne/capabilities/exploratory/view_compiler.py`
- `src/ariadne/interfaces/web_api/routers/exploration.py`
- `src/ariadne/interfaces/web_api/routers/workspace_lifecycle.py`
- `src/ariadne/product/application/workspace_lifecycle_service.py`
- `src/ariadne/capabilities/predictive/validation.py`
- `src/ariadne/capabilities/predictive/training_runners.py`
- `src/ariadne/product/application/predictive_workflow_service.py`
- `src/ariadne/interfaces/web_api/idempotency.py`
- `src/ariadne/product/application/product_closure_service.py`
- `00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design.md`
- `00_enhance_background/Revised_requirements_definition_documents/30_detailed_design.md`

このevidence listはnormative referenceではない。下流contractは10/21/22/23/30および06/07へ収束させる。
