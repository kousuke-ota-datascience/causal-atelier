<!-- ENH-E11 split working copy: not a formal approval. -->
# 30 — results frontend

**Status:** `STRUCTURAL_COPY_DRAFT` (existing baseline text, not E11 canonical publication)

**Source:** [30_detailed_design.md](https://github.com/kousuke-ota-datascience/causal-atelier/blob/3ba5fe2465ec591f0da7f998c21a5241984b73dc/docs/wiki/requirement_definition/30_detailed_design.md) · blob `04d83541e55ab0364500afb4b92ef55c10785a0c`  
**Index:** [Revised document inventory](../README_00_Revised_requirements_definition_documents.md)

---

## 16. Result Type / Scientific Status

### 16.1 Result Type

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

### 16.2 Scientific status

status vocabularyはresult type/schemaに応じて意味を保持する。例:

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

Family-specific statusをgeneric success/failureへ平坦化しない。

---

## 17. Comparison / Lineage

### 17.1 Result comparison

comparisonは二段階gateとする。

```text
same Family / same Result Type
        ↓
semantic_compatible
        ↓
direct_metric_comparable
```

異なるFamilyまたはResult Typeをgeneric direct comparisonへ投入しない。同一Family/Result Typeでもsemantic key不一致ならrequest自体を失敗させず、`semantic_compatible=false / direct_metric_comparable=false / reasons[]`を返しquantitative delta/rankを生成しない。

Predictive semantic keyにはtask type、prediction target/outcome、prediction unit、prediction time、horizon、population semanticsを含む。direct metric comparisonには同一Dataset Version、同一TEST-row identity/hash、同一metric definitionを要求する。

Causal semantic keyにはtreatment/exposure、outcome、estimand、target populationを含む。direct quantitative comparisonには同じdataset/view/analysis populationを要求する。

「画面上に並べられる」と「scientifically direct-comparable」を同一視しない。

### 17.2 Cross-family comparison

Exploratory statistic、Predictive metric、Causal effectは同じ数値fieldへflattenしない。

cross-family surfaceでは、共通metadata/lineageとFamily-specific payloadを分離して表示する。

### 17.3 Lineage

lineageはProject境界を越えない。

代表的typed structural relation:

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

Generic relationには`Artifact --DERIVED_FROM--> Artifact`、`Result --SUMMARIZES--> Result/Artifact`、`Result --MOTIVATED--> Execution/AnalysisSpecification`等を許可し得る。unknown tupleはclosed-by-defaultでrejectし、typed structural tupleをgeneric LineageEdgeとして二重writeしない。

Navigation Stageをpersistent Lineage node/edgeへ追加しない。どのStageからResultを表示するかはFamily / Result Type / presentation bindingからderiveする。

---

## 18. Frontend / Routing detailed design

### 18.1 Root component responsibility

```text
ApplicationRoot
├─ ApplicationRouter
├─ ProjectsSurface
│  ├─ ProjectList
│  └─ ProjectRegister
├─ ProjectManagementShell
│  ├─ ProjectHeader
│  ├─ ProjectParentNavigation
│  ├─ ProjectLocalNavigation
│  └─ ProjectSectionSurface
│     ├─ Overview
│     ├─ ResearchContext
│     ├─ Data
│     └─ ResultsLineage
└─ AnalysisWorkspaceShell
   ├─ AnalysisContextPanel
   ├─ FamilyTabs
   ├─ FamilyStageSidebar
   └─ StageContents
```

名称はresponsibility roleであり、具体実装のcomponent名を不必要に固定しない。

### 18.2 Navigation catalog loading

Frontend catalog authority:

```text
GET /api/v1/navigation/analysis
response schema = analysis-navigation/1
```

Normalized in-memory model:

```typescript
type AnalysisNavigationCatalog = {
  schemaVersion: "analysis-navigation/1";
  families: FamilyNavigationDescriptor[];
};
```

Catalog load state:

```text
IDLE → LOADING → READY
              ├→ ERROR
              └→ EMPTY/INVALID = contract error
```

invalid catalog時にhard-coded fallback catalogをsilent採用しない。

### 18.3 Analysis transition coordinator

Analysis navigation transitionは単一authorityで次を順序化する。

```text
entry intent / parsed URL
  ↓
resolve + validate NavigationContext from catalog
  ↓
validate project/resource route context
  ↓
commit current navigation state
  ↓
apply history policy
  ↓
render FamilyTabs / StageSidebar / StageContents
  ↓
load operation availability / resource data
  ↓
focus / error presentation
```

FamilyTabs、StageSidebar、StageContentsが独立にhistoryを書き換えない。

### 18.4 Project transition coordinator

Project Management側はProject routeだけを扱う。

```text
project navigation intent
  ↓
resolve route + authorization
  ↓
normalize short route if needed
  ↓
commit Project section / Projects index state
  ↓
apply history policy
  ↓
render ProjectsSurface / ProjectManagementShell
```

Selected ProjectからProject Listへのparent actionもこのcoordinatorを利用する。

Analysis Family/StageをProject section transitionへ暗黙付与しない。

### 18.5 Direct link / reload / Back / Forward

Project routeとAnalysis routeの双方で次を保証する。

- direct link
- reload
- Back
- Forward
- same-target duplicate history suppression
- normalizationのreplace behavior
- Selected Project direct entryからのProject List parent navigation

### 18.6 Legacy analytical entry

supported legacy analytical entryはcanonical Analysis routeへ一方向normalizeする。

legacy path/stateを第二のnavigation authorityとして維持しない。旧route tokenの具体形そのものはcurrent public contractとして固定しない。

### 18.7 Project switching

Analysis Workspace内のCurrent Projectはread-onlyである。

Project switch controlをAnalysis Contextへ持たせない。別Projectへ移動する場合はProjects / Project Managementへ遷移してProjectを選択する。

### 18.8 Async presentation state

共通presentation vocabulary:

```text
IDLE
LOADING
READY
EMPTY
PARTIAL
ERROR
CANCELLED
```

scientific statusとHTTP/loading statusを同一enumへ統合しない。

### 18.9 Accessibility

- active Family / Stage / Project sectionをsemantically表現する。
- current Stage headingをreal headingとして公開する。
- presentation-only sidebar group labelはnon-interactiveとし、active/selected route semanticsを持たせない。
- Project List parent navigation、Stage navigation、selector trigger等のactionはaccessible nameとkeyboard activationを持つ。
- keyboard navigation/focus orderをroute structureと整合させる。
- route transition後のfocus targetをdeterministicにする。
- Stage-owned surfaceをhideする場合、visual concealmentだけでなくinteraction/focus orderから除外する。
- loading/error/unavailableを色だけで表現しない。
- URLで復元したscreenも同じaccessible name/stateを持つ。

### 18.10 Stage presentation binding

frontendはcurrent `(family, navigation_stage_id)`に対し、StagePresentationとStage-owned surface visibilityをdeterministicにresolveする。

```text
route-authoritative current Stage
  ↓
Stage presentation resolver
  ├─ title / guidance
  ├─ main surface ownership
  ├─ prerequisite/reference surfaces
  └─ presentation-only group label
```

Causalのlegacy `Inference` workspaceやPredictiveのgeneric result containerを内部実装として共有してもよいが、複数Stageのprimary identity / responsibilityを同一surfaceへflattenしない。

### 18.11 Layout / responsive overflow

- Stage main areaはsemantic section/cardを縦方向に並べる。
- compact pair/group controlはlocal grid/flexを使用してよい。
- intrinsically wide table/chart/preformatted resultはcomponent-local overflowを許可する。
- narrow viewportでもsemantic section orderとcontrol usabilityを維持する。
- page全体のhorizontal overflowをStage section compositionで発生させない。

---

## 19. Operation Availability

### 19.1 Purpose

Operation Availabilityは現在のProject/resource/route contextにおいて、どのcommand/controlを実行可能かをread-only projectionする。

Frontend route parser、Navigation catalog、Stage visibilityはscientific truthを所有しない。

### 19.2 Authority

```text
availability projection
  ≠ command authorization/validation
```

actual commandがdenyした場合、そのdenyをauthoritativeとする。

### 19.3 Representative reason codes

```text
PROJECT_ACCESS_DENIED
UNSUPPORTED_OPERATION
RESOURCE_REQUIRED
ROUTE_REQUIRED
RESOURCE_IMMUTABLE
SPEC_NOT_FIXED
GRAPH_NOT_FIXED
IDENTIFICATION_REQUIRED
INPUT_GRAPH_REQUIRED
INPUT_RESULT_REQUIRED
EXECUTION_STATE_NOT_RUNNABLE
RESULT_NOT_EXPORTABLE
DOMAIN_PREREQUISITE_NOT_SATISFIED
```

request-level error例:

```text
INVALID_OPERATION_AVAILABILITY_QUERY
UNSUPPORTED_RESOURCE_TYPE
ENTITY_NOT_FOUND
PROJECT_ACCESS_DENIED
INVALID_NAVIGATION_ROUTE
ROUTE_RESOURCE_FAMILY_MISMATCH
```

closed vocabularyをimplementation都合で無秩序に拡張しない。

### 19.4 Data Quality availability

Data Quality Stageは専用operationを持たないため、Profile result availabilityをprojectionする。

```text
PROFILE result present → read-only READY
PROFILE result absent  → unavailable(NO_PROFILE_RESULT) + Profile link
```

このreasonはUI-local presentation contractとして扱う場合でも、backend runtime operation/stateを作成しない。

---
