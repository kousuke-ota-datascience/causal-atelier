# Ariadne ENH-E7 G02 Implementation Instruction — Gate Coding Contract

**文書種別:** Primary Execution Contract  
**Self-containment:** MUST（Gate implementation semanticsについて本文内で完結）  
**Project:** Ariadne  
**Enhancement:** ENH-E7  
**Active Gate:** G02  
**Branch:** `feature/ariadne_mvp_e7`  
**Baseline:** `REQUIRES_LOCAL_VERIFICATION`  
**Contract status:** FROZEN
**Execution Mode:** WORK_PACKAGE  
**Current State:** `docs/wiki/develop_memo/_work/20260813_ENH-E7_project_analysis_workspace_separation/Current_State_Control_Sheet.md`

## 1. Gate定義 / Acceptance claim

### Gate objective

Analysis domain/execution semanticsを変更せず最終ENH-E7 Analysis Workspaceを成立させ、replacement surfaceが操作可能になってから重複analytical navigationを除去する。

### PASSで成立するcontract claim

Analysis WorkspaceがProject Managementとは別analysis surfaceとして成立し、Analysis Context、Family/Stage navigation、既存Causal/Exploratory/Predictive surfaceのStage Contents配置、cross-surface navigation、legacy compatibility、browser history semanticsを一体として利用できる。

### Downstreamが利用できる結果

ENH-E7をProduct-completeと判定可能になり、後続EnhancementはProject/Analysis surface分離とStage-local presentation ownershipへ依存できる。

### この範囲を1 Gateとして扱う理由

Analysis shellだけではdownstream-relyableなProduct contractにならない。
Analysis Context、Family/Stage navigation、既存surface operability、cross-surface routing、
legacy compatibility、browser semanticsが一体として成立した時点を1つのsemantic acceptance boundaryとする。

## 2. Effective implementation context

- G02はG01 final PASS後にのみ実行可能。
- ENH-E6 canonical Analysis route / Family / Stage semanticsを保護する。
- Stage UIへ移設してもexisting backend execution semanticsを変更しない。
- browser history / direct-linkはProduct semantics。
- package completionはGate PASSではない。

## 3. Execution Mode

`WORK_PACKAGE`を使用する。
P00はHuman/operator用orchestration traceabilityであり、Coding Agentは仕様補完目的で読まない。

## 4. 必須implementation semantics

- AC-G02-01: Analysis WorkspaceがProject Managementとは別surfaceである。
- AC-G02-02: Analysis ContextにCurrent Project / Research Context / Dataset Version / Analysis Viewが表示される。
- AC-G02-03: Current Projectがread-onlyである。
- AC-G02-04: Project変更はProjects / Project Management経由で行う。
- AC-G02-05: Research Context / Dataset Version / Analysis Viewをcurrent inputとして選択できる。
- AC-G02-06: Family navigationがAnalysis Workspace内だけに存在する。
- AC-G02-07: Stage navigationがactive Family配下の縦navigationでselected stateを持つ。
- AC-G02-08: existing Causal surfaceをmapped Stageから操作できる。
- AC-G02-09: existing Exploratory surfaceをmapped Stageから操作できる。
- AC-G02-10: existing Predictive surfaceをmapped Stageから操作できる。
- AC-G02-11: Predictive Execution semanticsが変更されていない。
- AC-G02-12: canonical Analysis URL semanticsが変更されていない。
- AC-G02-13: Family default Stage semanticsがcatalog-authoritativeである。
- AC-G02-14: legacy analytical URLがcanonical Analysis routeへnormalizeする。
- AC-G02-15: Project → Analysis → Project navigationが成立する。
- AC-G02-16: Analysis → Results / Lineage navigationが成立する。
- AC-G02-17: deep-link / reload / Back / Forwardが成立する。
- AC-G02-18: existing resource-route semanticsが維持される。
- AC-G02-19: ENH-E6 protected Analysis navigation semanticsがregressionしない。

### Frozen Exploratory placement decision

- `PROFILE` → Profile、`DISTRIBUTION` → Distribution、`ASSOCIATION` → Relationships、`GROUP_SUMMARY` / `TIME_TREND` → Comparison、`CHART`およびsaved Exploratory Results → Findings。
- Data Qualityはoperationではないread-only availability stageである。existing Profile resultを表示し、存在しない場合は`NO_PROFILE_RESULT`とProfileへの導線を表示する。`DATA_QUALITY` operation、execution、resource、API/persistenceを作らない。
- `TIME_TREND`は既存grouping / aggregation operationであり、時刻型validation、順序推論、trend modelを追加しない。既存`GROUP_SUMMARY_RESULT`を維持する。
- `CHART`は`CHART_RESULT`とVega-Lite chart artifactを保存する既存operationである。presentation-only mechanismへの置換や新execution modelの作成をしない。

## 5. Allowed scope

- Analysis shell / context / routing / Stage Contentsへのexisting surface migration。
- legacy analytical UI shortcut removalとlegacy URL normalization。
- focused automated test / repository-standard Browser E2E。
- existing responsibilityを特定するためのsource discovery。

## 6. Explicitly prohibited scope

- UI taxonomyを埋めるための新backend operation。
- Predictive Execution model変更。
- Causal domain semantics変更。
- Family / Stage taxonomyの大幅変更。
- persistence/schema redesign。
- `DATA_QUALITY` operationの新設、またはTIME_TRENDへの未承認time-series semantics追加。
- implementationに合わせたAC変更。

## 7. Protected passed-Gate contract

- G01 final PASS contract。
- G01 final PASS contract、およびENH-E6 canonical Analysis route / Family / Stage navigation semantics。

## 8. Transition Debt

Intentional temporary product debtは計画しない。
legacy URL compatibilityはProduct requirementでありtemporary debtではない。

## 9. API / persistence方針

```text
Persistence migration: NONE EXPECTED
API contract change: NONE EXPECTED
Backend domain semantic change: NOT AUTHORIZED
```

必要と判明した場合はaffected packageをBLOCKEDとし、contract amendmentを要求する。

## 10. Automated test obligation

- 002: analysis_context_contract（FRONTEND_CONTRACT）
- 003: analysis_navigation_contract（FRONTEND_CONTRACT）
- 004: causal_stage_operability（FRONTEND_CONTRACT/API_INTEGRATION）
- 005: exploratory_stage_operability（FRONTEND_CONTRACT/API_INTEGRATION）
- 006: predictive_stage_semantics（FRONTEND_CONTRACT/API_INTEGRATION）
- 007: legacy_and_cross_surface_routing（FRONTEND_CONTRACT）
- 008: analysis_main_browser_journey（BROWSER_E2E）
- 009: analysis_history_compat_browser（BROWSER_E2E）

詳細correctnessはlower layerで検証し、Browser E2Eはcritical journeyに限定する。

## 11. Candidate Assembly条件

- G02 required Pxxすべて`PACKAGE_COMPLETE`。
- integration self-check PASS。
- G01 / ENH-E6 protected regression PASS。
- candidate-affecting unresolved changeなし。
- Fixed Trial Candidate full SHA固定。
- Implementation Completion Report作成。

## 12. Coding-side prohibited work

- Gate PASS/FAIL判定。
- 07変更。
- Acceptance Criteria変更。
- protected semantic変更。
- package scope外のconvenience change。

## 13. 必須output

各packageのpackage execution status report、Candidate Assembly時のGate-level Fixed Trial Candidate / Completion Report。package単位のcheckpoint report / SHA lockは必須にしない。

## 13.1 Package report contract

各Pxxのpackage handoff report contract（保存先・filename・必須内容）はassigned Pxxにself-containedで定義する。
Coding Agentは20-layer templateを参照せず、assigned PxxとCoding Agent promptだけでhandoff reportを作成できなければならない。

## 14. External reference policy

本06はHuman/operator用Gate authority。
Coding Agentはassigned Pxxだけをnormative implementation contractとして使用する。

## 15. Stop condition

Coding sideは`READY_FOR_TEST`または明示的`BLOCKED_*`で停止し、Gate PASSを宣言しない。
