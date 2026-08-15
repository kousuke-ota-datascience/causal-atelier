# Ariadne ENH-E7 G04 Implementation Instruction — Gate Coding Contract

**文書種別:** Primary Execution Contract  
**Self-containment:** MUST  
**Project:** Ariadne  
**Enhancement:** ENH-E7  
**Active Gate:** G04  
**Branch:** `feature/ariadne_mvp_e7`  
**Baseline:** `REQUIRES_LOCAL_VERIFICATION`  
**Contract status:** FROZEN  
**Execution Mode:** WORK_PACKAGE

## 1. Gate定義 / Acceptance claim

### Gate objective

G03で成立したProjects / Project Management / Analysisのsurface architectureへ、
既存canonical route/state/history/resource/operation semanticsを完全に再結合し、
root entry defectを含むnavigation regressionを閉じる。

### PASSで成立するcontract claim

ユーザーが`/`またはcanonical/deep/legacy routeから開始しても、
正しいtop-level surface・selected state・analysis input・browser historyへ到達し、
Project Management ↔ Analysis Workspaceを往復しながら既存operationを利用できる。

## 2. Effective implementation context

- G04はG03 final PASS後のみ実行可能。
- G03 surface topologyはblocking protected contract。
- G01/G02 canonical route/domain/analysis semanticsを維持する。
- `/`で旧Project/Data workspaceが初期表示される状態を許容しない。
- current ProjectはAnalysis URLのproject_id authorityを維持する。
- Family default Stageはexisting navigation catalog authorityを維持する。
- backend/API/persistence semantic changeは不要であることを前提とする。
- package completionはGate PASSではない。

## 3. Execution Mode

`WORK_PACKAGE`。
P00はHuman/operator用でありCoding Agentは仕様補完目的で読まない。

## 4. 必須implementation semantics

- AC-G04-01: `/`はduplicate historyを作らず`/projects`へnormalizeし、legacy default workspaceを表示しない。
- AC-G04-02: `/projects` / `/projects/new` / create→`/projects/<id>/overview` / `/projects/<id>`→`/overview` semanticsが成立する。
- AC-G04-03: Overview / Context / Data / Results local navigationとURL/selected stateが一致する。
- AC-G04-04: Analysis ContextのCurrent Project / Research Context / Dataset Version / Analysis View restore・selection semanticsが維持される。
- AC-G04-05: Family/Stage routeとselected stateが一致し、Family切替時default Stageはcatalog-authoritativeである。
- AC-G04-06: Project Management → Analysis Workspace launcher/transitionがselected Projectを維持して成立する。
- AC-G04-07: Analysis Workspace → Project Management returnがcurrent Projectの適切なProject Management routeへ遷移する。
- AC-G04-08: Analysis → Results / Lineage navigationがProject Management Resultsへ遷移する。
- AC-G04-09: canonical deep-link / reload / Back / Forwardでrouteとvisible surface/stateが一致する。
- AC-G04-10: legacy analytical URLがcanonical Analysis routeへnormalizeする。
- AC-G04-11: existing resource-route semanticsが維持される。
- AC-G04-12: existing Causal / Exploratory / Predictive mapped operation semanticsが維持される。
- AC-G04-13: G03 surface architecture invariantが全navigation journeyで維持される。
- AC-G04-14: browser console/page error、duplicate handlerによる二重history、stale visible shellがない。
- AC-G04-15: existing Project/domain/backend/API/persistence semanticsとENH-E6/G01/G02 protected semanticsがregressionしない。

## 5. Allowed scope

- frontend route restore / normalization / history integration
- Project Management local navigation state
- Analysis Context / Family / Stage state integration
- cross-surface launcher/return actions
- legacy URL normalization integration
- existing operation/resource presentation binding
- focused tests / Browser E2E
- G03後に判明したstale presentation binding cleanup

## 6. Explicitly prohibited scope

- G03 surface topologyを旧global shellへ戻すこと
- backend operation追加
- persistence/schema redesign
- Family / Stage taxonomy変更
- Predictive execution model変更
- Causal domain semantics変更
- implementationに合わせたAC変更
- unrelated UI polish/framework rewrite

## 7. Protected contract

### G03 protected

- Projects / Project Management / Analysis top-level surface separation
- PM local navigation ownership
- Analysis Context ownership
- Family horizontal / Stage vertical
- obsolete global shell absence

### Existing semantic protected

- Project lifecycle / resource ownership
- canonical Analysis navigation catalog
- existing Causal/Exploratory/Predictive operations
- resource route / legacy compatibility requirements

## 8. Transition Debt

G04 PASS時にtemporary routing shim、duplicate handler、old/new navigation fallbackを残さない。

## 9. API / persistence方針

```text
Persistence migration: NONE
API contract change: NONE
Backend domain semantic change: NOT AUTHORIZED
```

## 10. Automated test obligation

- 002: root_and_project_route_contract
- 003: project_management_navigation_state
- 004: analysis_context_family_stage_state
- 005: cross_surface_history
- 006: legacy_resource_routing
- 007: analysis_operation_regression
- 008: full_product_browser_journey
- 009: history_reload_console_browser
- 010: protected_full_regression

## 11. Candidate Assembly条件

- required Pxxすべて`PACKAGE_COMPLETE`
- G03 protected architecture regression PASS
- route/state/history integration self-check PASS
- existing operation/resource regression PASS
- unresolved candidate-affecting changeなし
- Fixed Trial Candidate SHA固定
- Completion Report作成

## 12. Coding-side prohibited work

- Gate PASS/FAIL判定
- 07変更
- Acceptance Criteria変更
- protected semantic変更

## 13. 必須output

各package execution status report、Candidate Assembly時のGate-level Completion Report。

## 14. External reference policy

本06はHuman/operator用Gate authority。
Coding Agentはassigned Pxxだけをnormative implementation contractとして使用する。

## 15. Stop condition

Coding sideは`READY_FOR_TEST`または明示的`BLOCKED_*`で停止し、Gate PASSを宣言しない。
