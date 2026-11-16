# 30_41_navigation_routing

**Status:** `RD02_STRUCTURAL_WORKING_COPY / E11_NOT_PUBLISHED`. Original chapter and source provenance retained; DD physical coverage remains partial.  
**Source blob:** `04d83541e55ab0364500afb4b92ef55c10785a0c`.

---

## 4. Application navigation state

### 4.1 Project route state

Project Managementのroute stateは次のいずれかである。

```text
Projects index
Project register
Selected Project + Project section
```

Canonical route:

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

は`/projects/{project_id}/overview`へ`replace` semanticsでnormalizeする。

### 4.2 Analysis route state

Canonical Analysis route:

```text
/projects/{project_id}/analysis/{family_slug}/{stage_slug}
```

resource deep route:

```text
/projects/{project_id}/analysis/{family_slug}/{stage_slug}/resource/{resource_type}/{resource_id}
```

Conceptual navigation context:

```text
NavigationContext
├─ project_id
├─ family: AnalysisFamily
├─ navigation_stage_id
└─ optional resource reference
```

これはroute resolution resultでありpersistent Domain Value Objectではない。

### 4.3 Project routeとAnalysis routeのauthority separation

Application Routerはpath prefixとroute grammarからProject Management / Analysis Workspaceをdispatchする。

```text
URL intent
  ↓
Application Router
  ├─ Project Route Resolver
  │    └─ Project Management Shell
  └─ Analysis Route Resolver
       └─ Analysis Workspace Shell
```

Project navigation stateをFamily/Stage stateへ変換しない。Analysis navigation stateをOverview/Data等のProject section stateへ変換しない。

### 4.4 History policy

| Transition | History behavior |
| --- | --- |
| userによるProject section遷移 | `pushState`相当 |
| userによるFamily/Stage遷移 | `pushState`相当 |
| Selected ProjectからProject Listへの明示的parent navigation | `pushState`相当 |
| `/projects/{id}` → overview normalization | `replaceState`相当 |
| supported legacy analytical entry → canonical Analysis route | `replaceState`相当 |
| initial canonical route restore | 新しいhistory entryを作らない |
| Back / Forward (`popstate`) restore | 新しいhistory entryを作らない |
| current targetと同一route | duplicate entryを作らない |

route更新とapplication state更新のauthorityを1 transition coordinatorへ集約し、個別componentが独自にhistory/stateを書き換えない。

### 4.5 Invalid route

次をsilent correctionしない。

- unknown Project section
- unknown Family slug
- unknown Stage slug
- resourceとexplicit Family/Stageのsemantic mismatch
- Project境界外resource

canonical default resolutionが許可されるのは、Familyのみが指定されStageが省略された等、contractでdefault Stage resolutionが定義されている場合に限る。

### 4.6 Selected ProjectからProject Listへのparent navigation

Selected Project shellは、`overview`, `context`, `data`, `results` の各local sectionからcanonical Project List `/projects` へ戻る明示的parent navigation actionを提供する。

```text
return action activate
  ↓
Project navigation intent
  ↓
canonical /projectsへserialize
  ↓
Project transition coordinator
  ↓
push history entry
  ↓
Projects indexをrender
```

Invariant:

- target authorityはcanonical `/projects` である。
- `history.back()` をtarget resolutionとして使用しない。
- Selected Project routeへdirect entryした場合でも同じactionが成立する。
- parent navigation後のBackは元のSelected Project route、Forwardは`/projects`を復元する。
- alternative Project List routeを追加しない。

---

## 5. Analysis Context

### 5.1 Logical structure

```text
Analysis Context
├─ Current Project
├─ Active Research Context
├─ Dataset Version
└─ Analysis View
```

### 5.2 Authority

| Element | Authority | UI mutability in Analysis Workspace |
| --- | --- | --- |
| Current Project | Analysis route `project_id` | read-only |
| Active Research Context | existing Project-scoped selection/resource | selectable |
| Dataset Version | existing Project-scoped selection/resource | selectable |
| Analysis View | selected Dataset Version compatible existing view | selectable |

Project変更はProjects / Project Management経由で行う。

### 5.3 Restore algorithm

```text
parse canonical Analysis route
  ↓
resolve Current Project from project_id
  ↓
load Project-authorized existing selections/resources
  ↓
restore Research Context only if it belongs to Current Project
  ↓
restore Dataset Version only if it belongs to Current Project
  ↓
restore Analysis View only if it belongs to Current Project
and is compatible with selected Dataset Version
  ↓
render Analysis Context
```

無効なselectionは架空defaultへ置換せず`unselected`とする。

### 5.4 Dataset Version change

```text
select new Dataset Version
  ↓
selected Analysis View exists?
  ├─ no  → keep unselected
  └─ yes
       ↓
compatible with new Dataset Version?
  ├─ yes → keep
  └─ no  → deselect Analysis View
```

このselection変更だけを理由にFamily / Navigation Stage routeを書き換えない。

### 5.5 Missing context

必要contextが不足するoperationは`unavailable`として表示する。Family/Stage navigation自体は維持する。

禁止:

- missing contextを埋める架空resource生成
- context deficiencyを理由とするautomatic Family/Stage rewrite
- Analysis Context専用persistent recordの作成
- Analysis Context専用backend APIの新設

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

**当該構成要素の詳細設計制約（関連Requirement）**

- **`FR-143`**：runtime layerはNavigation Stage ID、browser route、tab/sidebar stateへ依存しない
- **`FR-140`**：Navigation Stageをruntime `StageType` / `StageDefinition` / `StageExecution`として再利用・継承しない
- **`FR-145`**：generic application layerはFamily-specific Stage semanticsを集中所有しない
- **`NFR-025`**：CLI / library executionがWeb UI route、tab/sidebar state、NavigationStageDescriptorへ依存しない
