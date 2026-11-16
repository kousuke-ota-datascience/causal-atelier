# 30_40_project_workspace

**Status:** `RD02_STRUCTURAL_WORKING_COPY / E11_NOT_PUBLISHED`. Original chapter and source provenance retained; DD physical coverage remains partial.  
**Source blob:** `04d83541e55ab0364500afb4b92ef55c10785a0c`.

---

## 11. Project Management detailed design

### 11.1 Component responsibility

```text
Project Management Shell
├─ Project Header
├─ Project Parent Navigation
├─ Project Local Navigation
├─ Overview Surface
├─ Research Context Surface
├─ Data Surface
└─ Results / Lineage Surface
```

### 11.2 Projects Surface

`/projects`:

- Project一覧
- Project選択
- New Projectへの導線

`/projects/new`:

- Project register/create
- create成功後はcanonical selected Project routeへ遷移

### 11.3 Overview

ownership:

- Project identity
- Project metadata
- Project status
- archive lifecycle/action
- Project-level summary

Dataset / Analysis View create/edit lifecycleをOverviewへ置かない。

### 11.4 Research Context

ownership:

- Research Context create/revise
- active context selection where allowed
- version/history
- Project-scoped context inspection

### 11.5 Data

ownership:

- Dataset
- Dataset Version
- schema / preview
- Analysis View create/edit/version/fix lifecycle

Analysis View lifecycle authorityをAnalysis WorkspaceのStage componentへ重複させない。

### 11.6 Results / Lineage

ownership:

- persisted cross-analysis Result aggregation
- comparison
- Artifact browsing/export
- Lineage inspection
- Annotation

Stage-local execution/result presentationはAnalysis Workspaceに残す。

### 11.7 Project Parent Navigation

Selected Projectの各local sectionは、Project Listへの明示的parent actionを共通shellに持つ。

UI contract:

- accessible nameは`Project List` / `プロジェクト一覧へ戻る`等、遷移先が明確であること。
- actionはOverview / Research Context / Data / Results / Lineageのどのlocal surfaceでも利用できること。
- targetは常にcanonical `/projects`。
- browser history originに依存しないこと。
- keyboard activation可能であること。

---

## 12. Analysis Workspace detailed design

### 12.1 Component responsibility

```text
Analysis Workspace Shell
├─ Analysis Context
├─ Family Tabs
├─ Family Stage Sidebar
└─ Stage Contents
```

### 12.2 Family Tabs

- Catalog `families[].order`で表示する。
- current Familyをroute stateからderiveする。
- Family切替時、target Family catalogの`default_stage_id`を解決する。
- Research Context / Dataset Version / Analysis View selectionを不必要に初期化しない。
- Full Family catalogをfrontend constantとしてduplicate ownershipしない。

### 12.3 Family Stage Sidebar

- selected Family catalogのStageだけ表示する。
- `stages[].order`で表示する。
- current Stageをroute stateからderiveする。
- Stage clickはcanonical Analysis route transitionを発生させる。
- Stage orderをruntime dependency/progressionとして解釈しない。
- visual groupingを使用する場合、group labelはnon-interactive / non-routableで、selected Stage stateを持たない。

Causalでvisual groupingを使う場合の代表配置:

```text
分析設計
  Setup
因果構造
  Discovery
識別
  Identification
推定・評価
  Estimation
  Effects
  Diagnostics
  Sensitivity
```

このgroupingはpresentation-onlyであり、route、stage slug、Navigation Stage、runtime StageType、persistent stateを追加しない。

### 12.4 Stage Contents

Stage Contentsは`(family, navigation_stage_id)`からpresentation surfaceへbindingする。

```text
(family, stage)
  ↓
Stage Surface Resolver
  ↓
StagePresentation + existing use cases / operation availability / results
```

Stage Surface Resolverは新しいscientific execution semanticsを所有しない。

current Stageのprimary heading / descriptionはcurrent canonical Navigation Stageを示す。legacy workspace grouping（例: `Inference`）をcurrent Stageのprimary identityとして表示しない。

main operation/result/explanation surfaceはowning Stageに限定する。他Stageの情報が必要な場合は、compactなprerequisite、summary、link、read-only referenceとして提示する。

### 12.5 Availability

Stage surfaceはoperation availabilityをreadしてcontrol enablementを決めてよいが、availabilityはcommand validationの代替ではない。

```text
availability projection = UX pre-check
actual command validation = authoritative enforcement
```

projectionとcommandが不一致の場合はcommand denyを優先し、projection defectとして修正する。

### 12.6 StagePresentation

frontend presentation metadataは少なくとも次を表現できる。

```text
StagePresentation
├─ title
├─ 日本語の目的説明
├─ optional resource / operation guidance
└─ optional presentation-only group label
```

Presentation metadataはresolved canonical Stageをdecorateする。Stage identity/slug/order/defaultのauthorityにならない。

### 12.7 Stage layout / overflow

Stage Contentsのtop-level semantic sectionは縦方向に積む。

許可:

- compactで密接に関連するcontrolのlocal grid/flex
- wide table/chart/preformatted resultのcomponent-local horizontal overflow
- dialog内部のscrollable option list

禁止:

- 独立semantic sectionをmandatory horizontal rowへ連結し、page-level horizontal scrollを要求する構成
- hidden Stage surfaceをvisual concealmentだけで残し、focus/interaction可能にすること

### 12.8 Stage state preservation

Navigation Stage切替はpresentation visibilityの変更であり、同一analysis draft/specificationのvalid inputを無条件にresetしない。

Stage child componentのunmountだけで唯一のDRAFT stateを失う構造を避け、route-independent parent/application form state等へauthorityを一意化する。

---
