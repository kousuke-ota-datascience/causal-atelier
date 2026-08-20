# 30 詳細設計 — ENH-E8 Effective Frontend Addendum

- 文書状態: `APPROVED`
- Baseline canonical document: `docs/wiki/requirement_definition/30_detailed_design.md`
- Baseline commit: `386521d18e9c5cc4d42fb99c97c212430908afc3`
- Scope: ENH-E8対象のfrontend navigation / presentationのみ

> 本書はENH-E8のapproved Detailed Design deltaである。baseline commit `386521d18e9c5cc4d42fb99c97c212430908afc3` のcanonical approved `30_detailed_design.md` と一体のimmutable composite effective snapshotとしてfreezeする。baseline documentの未変更backend/domain sectionを再定義しない。

## E8.1 維持するbaseline invariant

1. Navigation Stageはapplication/presentation metadataであり、`AnalysisSpecification`, `ExecutionPlan`, `Execution`, `StageExecution`へ永続化しない。
2. Navigation taxonomy変更だけを理由にruntime `StageType`、dependency、retry/lease lifecycle、scientific runner behaviorを変更しない。
3. Project ManagementとAnalysis Workspaceは別navigation scopeである。
4. UI/IA再編だけを理由にexisting API、persistence schema、backend analysis/domain semanticsを変更しない。
5. Family-specific scientific meaningをgeneric presentation status/scoreへflattenしない。
6. canonical Causal/Predictive Stage catalogを変更しない。

## E8.2 Project List return action

### DOM / presentation

Selected Project chromeに、`Project List` / `プロジェクト一覧へ戻る` 相当のaccessible nameを持つ明示的controlを配置する。

対象section: `overview`, `context`, `data`, `results`

### Navigation behavior

```text
return actionをactivate
  -> ProjectNavigation collection intentを生成
  -> /projectsへserialize
  -> existing application transition coordinatorがuser PUSH navigationを実行
  -> Project List surfaceをrender
```

禁止:

- `history.back()` によるtarget解決
- canonical transition coordinatorを迂回する直接mutation
- alternative project-list routeの追加

## E8.3 Current Stage presentation descriptor

frontendは少なくとも以下をrenderできるpresentation metadataを持つ。

```text
StagePresentation
- title
- 日本語の目的説明
- optional resource / operation guidance
- optional presentation-only sidebar group label
```

presentation metadataをbackend navigation catalog authorityにしない。canonical Stage identity/slug/order/defaultはexisting catalog authorityを維持し、frontend metadataはresolved Stageをdecorateする。

## E8.4 Causal renderer binding

existing `AnalysisPresentation` のlegacy workspace bindingはrefactorしても内部保持してもよいが、renderingは以下を満たす。

- current Stage heading = selected Causal Navigation Stage
- shared `Inference` workspace nameをcurrent Stage identityとして表示しない
- Stage-specific main containerを明示的ownershipで選択する

### Causal visibility matrix

| Surface | identification | estimation | effects | diagnostics | sensitivity |
|---|---:|---:|---:|---:|---:|
| Identification purpose/input/action | ON | OFF | OFF | OFF | OFF |
| Identification / Eligibility / Gate result | ON | 必要な場合のみprerequisite reference | OFF | OFF | OFF |
| Estimation config/action | OFF | ON | OFF | OFF | OFF |
| Treatment effect primary result/comparison | OFF | compact completion/link可 | ON | optional referenceのみ | prerequisite selector/referenceのみ |
| Diagnostics result/warnings | OFF | OFF | OFF | ON | optional prerequisite/referenceのみ |
| Refutation controls/results | OFF | OFF | OFF | OFF | ON |
| Sensitivity controls/results | OFF | OFF | OFF | OFF | ON |

複数Stageのmain responsibilityを持つcontainerは、EffectsとDiagnosticsのprimary meaningが分かれるようsplitまたはStage-specific presentationへ再構成する。

### 日本語guidance

Causalのprimary purpose summaryは日本語を基本とする。ATE、ATT、CATE、estimand、overlap、ESS等はtechnical Englishのままでよい。

説明文は「このStageで何を判断・閲覧するか」と「隣接Stageと何が異なるか」が分かる内容とする。

## E8.5 Predictive renderer binding

canonical Stage catalog:

`setup / train / predict / metrics / explainability / model-management`

### Predictive visibility / ownership matrix

| Surface | setup | train | predict | metrics | explainability | model-management |
|---|---:|---:|---:|---:|---:|---:|
| Task/context/input/split specification | ON | compact reference | compact reference | compact reference | compact reference | compact reference |
| Training config + execute | OFF | ON | OFF | OFF | OFF | OFF |
| Execution status | OFF | ON | optional read reference | optional read reference | optional read reference | optional read reference |
| Prediction output/artifact | OFF | OFF | ON | OFF | OFF | reference可 |
| Evaluation metrics | OFF | OFF | OFF | ON | OFF | reference可 |
| Explanation result/artifact | OFF | OFF | OFF | OFF | ON | reference可 |
| Model card / fitted model / lineage | OFF | OFF | OFF | OFF | OFF | ON |

backendがTraining/Evaluation/Explanationを1workflowで生成するexisting behaviorは維持してよい。presentation分離のためにnew backend operationを追加しない。

### Draft state

Stage切替によって、owning presentation sectionがhiddenになっただけのvalid Predictive analysis specification fieldをresetしない。

form state serialization / submissionはexisting generated `predictive-analysis-spec/1` semanticsを維持する。

### Predictive feature selector

baseline Predictive formは `feature_columns` を `predictive-analysis-spec/1 -> feature_spec.feature_columns` へserializeする。ENH-E8が変更するのはuser interactionであり、serialization contractではない。

#### Ownership

- Editable selector owner: Predictive `setup`
- Train reference: current draft/specification feature set、read-only
- Predict reference: selected/existing execution specificationのfeature set、read-only
- Metrics / Explainability / Model Management: 必要な場合のみfeature provenanceをread-only表示

#### Candidate loading

```text
selected Dataset Version
  -> existing client Dataset Version resource
  -> dataset.schema column names
  -> checkbox option model
```

このselectorのためだけにnew backend schema endpointを作らない。

Dataset Version未選択、またはschema未取得の場合、selector openは利用者にunavailable stateを明示し、架空のcolumn optionを生成しない。

#### Interaction

1. dialog open時にcurrent confirmed feature selectionをpending stateへsnapshotする。
2. schema columnをlabel付きcheckboxとしてrenderする。type metadataをsecondary textとして表示してよい。
3. checkbox toggleはdialog内のpending selectionのみを変更する。
4. `Cancel` はconfirmed Predictive draftを変更せずdialogを閉じる。
5. `Confirm` はchecked columnをdeterministic schema orderでcommitする。
6. committed valueはexisting Predictive specification serializationが読む同一form/draft authorityへ反映する。
7. comma-delimited free-text editingはprimary editable pathから除去するかread-only/internalにし、同じfeature setに2つの競合editable authorityを持たせない。
8. Dataset Version変更時、新schemaに存在しないcolumnをsilentに保持しない。全clearまたはvalid intersection保持を許可するが、破壊的reconcileを利用者へ示す。
9. feature set、target、excluded column、availability cutoff、taskに対するexisting frontend/backend validationを変更しない。

#### Accessibility

- dialogにaccessible nameがある
- 各checkboxにaccessible labelがある
- keyboardでopen / Confirm / Cancelできる
- native dialog semanticsに従ってfocusを管理し、close後にinvokerへ戻す
- hidden dialog/optionをfocus可能にしない

#### Causal Discovery protected regression

existing Causal Discovery feature modalからgeneric column-selector helper/componentを抽出する場合、以下をprotected regressionとする。

- schema-derived candidate list
- current selection restoration
- deterministic confirmed ordering
- designated-outcome synchronization
- Dataset change handling
- Discovery request validation

## E8.6 Layout / overflow

- Stage main areaはsemantic section/cardを縦方向に並べる。
- independent semantic sectionをmandatory horizontal rowにしない。
- compact pair controlはlocal grid/flexを使用してよい。
- table/chart/preformatted result dataはlocal horizontal overflowを許可する。
- narrow viewportでもcontrol usabilityとsection orderを維持する。

## E8.7 Accessibility

- current Stage headingをreal headingとして公開する。
- sidebar group labelはnon-interactiveとし、selected/active route semanticsを持たせない。
- navigation/action controlはaccessible nameとkeyboard activationを持つ。
- Stage-owned surfaceをhideする場合、visual concealmentだけでなくinteraction/focus orderから除外する。

## E8.8 State / history regression

- direct canonical routeで正しいFamily/Stageとvisible surfaceを復元する。
- reload後もroute-authoritative current Stageを維持する。
- user Stage changeはnormal PUSH navigationとする。
- browser Back/Forwardはhistory entryを追加せずprior/next Stageを復元する。
- G01 Project List return actionも同じcanonical history policyに従う。

## E8.9 Implementation target / likely touch point

Primary frontend candidate:

- `frontend/index.html`
- `frontend/app.js`
- `frontend/styles.css`
- `frontend/analysis_presentation.js`
- `frontend/causal_stage_presentation.js`
- `frontend/project_navigation.js` はhelper exposureが必要な場合のみ

testはexisting product/frontend test structureへ追加・更新する。

`src/ariadne/**` のbackend semanticsはENH-E8のprotected scopeとする。

## E8.10 Test seam

deterministic testで直接確認する。

- G01 route serialization / transition intent
- Stage descriptor / heading resolution
- affected Causal/Predictive Stageのpositive/negative visibility
- presentation groupがroute/stage authorityでないこと
- Predictive draft preservation
- Predictive feature selector
  - schema-derived option
  - pending vs confirmed state
  - Cancel no-op
  - deterministic Confirm
  - Dataset change時のstale column
  - exact `feature_spec.feature_columns` serialization
  - Train/Predict read-only presentation
- common selectorを使う場合のCausal Discovery regression
- layout class/DOM structureとstage-level forced horizontal composition absence

Browser E2Eはcritical journey connectivityに限定し、exhaustive visibility correctnessの一次証明にはしない。
