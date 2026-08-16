# Ariadne ENH-E7 G03 Implementation Instruction — Gate Coding Contract

**文書種別:** Primary Execution Contract  
**Self-containment:** MUST  
**Project:** Ariadne  
**Enhancement:** ENH-E7  
**Active Gate:** G03  
**Branch:** `feature/ariadne_mvp_e7`  
**Baseline:** `REQUIRES_LOCAL_VERIFICATION`  
**Contract status:** FROZEN  
**Execution Mode:** WORK_PACKAGE

## 1. Gate定義 / Acceptance claim

### Gate objective

current E7 frontendに残った旧global presentation shellを、
既存ENH-E7 target IAに適合するtop-level surface architectureへ置換する。
routing/domain/application semanticsは再利用し、誤ったpresentation ownershipは保護しない。

### PASSで成立するcontract claim

以下3つのsurface ownershipが、DOM / runtime visibility / navigation hierarchy / layout topologyで明確に分離される。

```text
Projects Surface
├─ Project List
└─ New Project

Project Management Shell
├─ selected Project identity / header
├─ local vertical navigation
│  ├─ Overview
│  ├─ Research Context
│  ├─ Data
│  └─ Results / Lineage
└─ project section contents

Analysis Workspace Shell
├─ Analysis Context
│  ├─ Current Project (read-only)
│  ├─ Active Research Context
│  ├─ Dataset Version
│  └─ Analysis View
├─ Project Management return action
├─ Family tabs (horizontal)
├─ Stage navigation (vertical)
└─ Stage Contents
```

### この範囲を1 Gateとして扱う理由

本acceptance escapeはroute/stateの欠落ではなくsurface topologyの誤実装である。
DOM ownership、visibility、layout、obsolete shell removalを同一semantic boundaryで閉じなければ、
旧shellと新shellの重複というtransition debtを恒久化するため、本Gateで不可分に是正する。

## 2. Effective implementation context

- G03はG02 final PASS後のpost-Gate UI inspectionで判明したacceptance escapeを是正する。
- G01/G02のrequirements / Gate ACは変更しない。
- current sourceに存在する旧global sidebar / global common context placementはtarget architectureではない。
- routing、Project/domain semantics、Analysis operation semantics、resource semanticsは原則再利用する。
- current non-conforming DOM/CSS topologyを「passed code」として保護しない。
- pixel-perfect stylingは要求しないが、horizontal / vertical / containment / visibilityはProduct contractである。
- package completionはGate PASSではない。

## 3. Execution Mode

`WORK_PACKAGE`。
P00はHuman/operator用orchestration traceabilityであり、Coding Agentは仕様補完目的で読まない。

## 4. 必須implementation semantics

- AC-G03-01: `/projects`と`/projects/new`はProjects Surfaceとして成立し、Selected Project local navigationおよびAnalysis Context/Family/Stageを表示しない。
- AC-G03-02: `/projects/<id>/{overview,context,data,results}`はProject Management Shellとして成立し、Project-local navigationを持つ。
- AC-G03-03: Project Management ShellではAnalysis Context / Family / Stage navigationを表示しない。
- AC-G03-04: `/projects/<id>/analysis/<family>/<stage>`はProject Management Shellとは別のAnalysis Workspace Shellとして成立する。
- AC-G03-05: Analysis Workspace上部にCurrent Project / Active Research Context / Dataset Version / Analysis ViewとProject Management return actionを配置する。
- AC-G03-06: Family navigationはAnalysis Workspace内だけに存在し、horizontal layoutでselected stateを持つ。
- AC-G03-07: Stage navigationはactive Family配下でAnalysis Workspace内だけに存在し、vertical layoutでselected stateを持つ。Stage Contentsはその右側main areaに配置する。
- AC-G03-08: 旧global sidebarのProject Management / Research Context / Project・Data / Results・Lineage混在navigationを除去する。
- AC-G03-09: globalに常駐するAnalysis Context/common workspace headerを除去し、context ownershipをAnalysis Workspaceへ限定する。
- AC-G03-10: obsolete shell/navigationのduplicate DOM、duplicate event binding、dead presentation selectorを残さない。
- AC-G03-11: obsolete architectureをDOMに残しCSS `display:none`等だけで恒久的に隠す方式を採用しない。
- AC-G03-12: backend API / persistence / domain / analysis execution semanticsを変更しない。
- AC-G03-13: G01/G02で確認済みのcanonical route、Project lifecycle、Family/Stage catalog、existing operation semanticsをblocking regressionとして保護する。

## 5. Allowed scope

- frontend DOM / HTML structure
- frontend CSS / layout
- presentation state / top-level surface activation
- presentation event binding cleanup
- routeからsurfaceへ投影する最小限のfrontend integration
- focused product tests
- Browser E2E structural assertions
- obsolete presentation codeの削除

## 6. Explicitly prohibited scope

- 新backend endpoint / operation
- persistence/schema変更
- Project/domain semantics変更
- Causal/Exploratory/Predictive execution semantics変更
- Family / Stage taxonomy変更
- G01/G02 Acceptance Criteriaをcurrent implementationへ合わせて弱めること
- 旧global shellを互換性目的で残すこと
- unrelated framework migration / design-system rewrite

## 7. Protected contract

保護するのはG01/G02のnormative behaviorであり、非適合presentation implementationではない。

Protected:
- canonical Project route semantics
- Project lifecycle / Research Context / Dataset / Analysis View / Results ownership semantics
- canonical Analysis route
- Family / Stage catalog/default semantics
- existing Causal / Exploratory / Predictive operation behavior
- browser history semantics（G04でfull reintegrationするまで少なくとも破壊しない）

Not protected:
- old global sidebar DOM
- global common-workspace-header placement
- all-workspaces-in-one-shell presentation topology
- horizontal Stage list
- duplicate Project/Analysis navigation

## 8. Transition Debt

Intentional temporary duplicate shell / duplicate navigationは許可しない。
G03 PASS時点でold presentation hierarchyを削除済みであること。

## 9. API / persistence方針

```text
Persistence migration: NONE
API contract change: NONE
Backend domain semantic change: NOT AUTHORIZED
```

必要と判明した場合はaffected packageを`PACKAGE_BLOCKED`としcontract amendmentを要求する。

## 10. Automated test obligation

- 002: projects_surface_topology
- 003: project_management_shell_topology
- 004: analysis_workspace_shell_topology
- 005: layout_orientation_runtime
- 006: obsolete_shell_absence
- 007: protected_semantic_smoke
- 008: surface_architecture_browser_journey

UI architectureのTest Itemはelement ID / label文字列の存在だけをevidenceとしない。

## 11. Candidate Assembly条件

- G03 required Pxxすべて`PACKAGE_COMPLETE`
- integration self-check PASS
- obsolete shell cleanup audit PASS
- protected regression PASS
- candidate-affecting unresolved changeなし
- Fixed Trial Candidate full SHA固定
- Implementation Completion Report作成

## 12. Coding-side prohibited work

- Gate PASS/FAIL判定
- 07変更
- Acceptance Criteria変更
- protected semantic変更
- package scope外convenience change

## 13. 必須output

各package execution status report、およびCandidate Assembly時のGate-level Completion Report。

## 14. External reference policy

本06はHuman/operator用Gate authority。
Coding Agentはassigned Pxxだけをnormative implementation contractとして使用する。

## 15. Stop condition

Coding sideは`READY_FOR_TEST`または明示的`BLOCKED_*`で停止し、Gate PASSを宣言しない。
