# Ariadne ENH-E7 G02 Test Instruction — Gate Verification Contract

**文書種別:** Primary Execution Contract  
**Self-containment:** MUST  
**Verification contract status:** DRAFT_NOT_FROZEN

## 1. Acceptance authority

Human/operatorがexecution前に本07をFROZENへ変更した時点で、本書がGate Acceptance Criteria authorityになる。

`PACKAGE_COMPLETE` / Coding self-check / `READY_FOR_TEST`はGate acceptanceではない。

## 2. Gate objective / claim

Analysis domain/execution semanticsを変更せず最終ENH-E7 Analysis Workspaceを成立させ、replacement surfaceが操作可能になってから重複analytical navigationを除去する。

PASSで以下を成立させる。

Analysis WorkspaceがProject Managementとは別analysis surfaceとして成立し、Analysis Context、Family/Stage navigation、既存Causal/Exploratory/Predictive surfaceのStage Contents配置、cross-surface navigation、legacy compatibility、browser history semanticsを一体として利用できる。

## 3. Verification原則

- Fixed Trial Candidate identity auditを最初に行う。
- G01 / ENH-E6 protected regressionはblocking。
- Test Agentはproduction/test/dependency/migration codeを変更しない。
- Coding reportはAcceptance authorityではない。

## 4. Candidate identity audit — MUST FIRST

1. Fixed Trial Candidate SHA取得。
2. actual checkout / HEAD記録。
3. Candidate後diff audit。
4. identity不明ならBLOCKED。

## 5. Acceptance Criteria

| AC ID | Criterion | Required evidence | Severity |
|---|---|---|---|
| AC-G02-01 | Analysis WorkspaceがProject Managementとは別surfaceである。 | independent source/test/runtime evidence | MUST |
| AC-G02-02 | Analysis ContextにCurrent Project / Research Context / Dataset Version / Analysis Viewが表示される。 | independent source/test/runtime evidence | MUST |
| AC-G02-03 | Current Projectがread-onlyである。 | independent source/test/runtime evidence | MUST |
| AC-G02-04 | Project変更はProjects / Project Management経由で行う。 | independent source/test/runtime evidence | MUST |
| AC-G02-05 | Research Context / Dataset Version / Analysis Viewをcurrent inputとして選択できる。 | independent source/test/runtime evidence | MUST |
| AC-G02-06 | Family navigationがAnalysis Workspace内だけに存在する。 | independent source/test/runtime evidence | MUST |
| AC-G02-07 | Stage navigationがactive Family配下の縦navigationでselected stateを持つ。 | independent source/test/runtime evidence | MUST |
| AC-G02-08 | existing Causal surfaceをmapped Stageから操作できる。 | independent source/test/runtime evidence | MUST |
| AC-G02-09 | existing Exploratory surfaceをmapped Stageから操作できる。 | independent source/test/runtime evidence | MUST |
| AC-G02-10 | existing Predictive surfaceをmapped Stageから操作できる。 | independent source/test/runtime evidence | MUST |
| AC-G02-11 | Predictive Execution semanticsが変更されていない。 | independent source/test/runtime evidence | MUST |
| AC-G02-12 | canonical Analysis URL semanticsが変更されていない。 | independent source/test/runtime evidence | MUST |
| AC-G02-13 | Family default Stage semanticsがcatalog-authoritativeである。 | independent source/test/runtime evidence | MUST |
| AC-G02-14 | legacy analytical URLがcanonical Analysis routeへnormalizeする。 | independent source/test/runtime evidence | MUST |
| AC-G02-15 | Project → Analysis → Project navigationが成立する。 | independent source/test/runtime evidence | MUST |
| AC-G02-16 | Analysis → Results / Lineage navigationが成立する。 | independent source/test/runtime evidence | MUST |
| AC-G02-17 | deep-link / reload / Back / Forwardが成立する。 | independent source/test/runtime evidence | MUST |
| AC-G02-18 | existing resource-route semanticsが維持される。 | independent source/test/runtime evidence | MUST |
| AC-G02-19 | ENH-E6 protected Analysis navigation semanticsがregressionしない。 | independent source/test/runtime evidence | MUST |

## 6. Test Item plan

| Test Item ID | Name | Covers AC | Primary test layer | Gate blocking | Method |
|---|---|---|---|---|---|
| 001 | candidate_identity | META | META | YES | Fixed Trial Candidate SHAとtested checkoutをaudit。 |
| 002 | analysis_context_contract | AC-G02-01,02,03,04,05,06,07 | FRONTEND_CONTRACT | YES | shell/contextとduplicate navigation absenceを検証。 |
| 003 | analysis_navigation_contract | AC-G02-12,13,14,17,18,19 | FRONTEND_CONTRACT | YES | AnalysisNavigation / legacy / resource / history regression。 |
| 004 | causal_stage_operability | AC-G02-08,19 | FRONTEND_CONTRACT/API_INTEGRATION | YES | Causal mapped-surface operability / regression。 |
| 005 | exploratory_stage_operability | AC-G02-09,19 | FRONTEND_CONTRACT/API_INTEGRATION | YES | Exploratory mapped-surface operability / regression。 |
| 006 | predictive_stage_semantics | AC-G02-10,11,19 | FRONTEND_CONTRACT/API_INTEGRATION | YES | Predictive mapped presentation / execution-model regression。 |
| 007 | legacy_and_cross_surface_routing | AC-G02-14,15,16,17,18 | FRONTEND_CONTRACT | YES | legacy normalization / Project-Analysis-Results routing。 |
| 008 | analysis_main_browser_journey | AC-G02-01,02,06,07,08,09,10,15,16 | BROWSER_E2E | YES | Project → Analysis → Family/Stage/surface → Results → Project Management。 |
| 009 | analysis_history_compat_browser | AC-G02-12,13,14,17,18,19 | BROWSER_E2E | YES | canonical/legacy deep link → normalization → Family/Stage変更 → reload → Back/Forward。 |

`999`はGate Decision専用。

## 7. Browser E2E

repository既存Browser E2E harnessとcurrent-source environmentを使用する。
harness/environment defectでProduct判定不能ならFAILではなくBLOCKED。

## 8. Protected passed-Gate regression

G01 final PASS contract、およびENH-E6 canonical Analysis route / Family / Stage navigation semantics。

## 9. Test Agent prohibited work

- production/test/migration/dependency code変更
- Acceptance Criteria変更
- implementation修復
- Fixed Trial Candidateの差し替え
- Coding Agent PxxをAcceptance authorityとして使用

## 10. Decision semantics

### PASS
すべてのMUST AC / candidate identity / required regression / blocking Test ItemがPASS。

### FAIL
testable candidateにMUST AC/protected semantic violationがverified evidenceで確認される。

### BLOCKED
identity / environment / harness / prerequisite / contract ambiguityで妥当なProduct判定ができない。

## 11. Required output

各Test Item reportと`999_gate_decision`を作成して停止する。
