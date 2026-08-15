# Ariadne ENH-E7 G04 Test Instruction — Gate Verification Contract

**文書種別:** Primary Execution Contract  
**Self-containment:** MUST  
**Verification contract status:** FROZEN

## 1. Acceptance authority

本書がG04 Gate Acceptance Criteria authority。
`PACKAGE_COMPLETE` / Coding self-check / `READY_FOR_TEST`はGate acceptanceではない。

## 2. Gate objective / claim

G03 surface architectureを維持したまま、
root/canonical/deep/legacy entry、Project Management、Analysis context、Family/Stage、
cross-surface history、resource/operation behaviorを一体としてcorrected Product-completeにする。

## 3. Verification原則

- Fixed Trial Candidate identity auditを最初に行う。
- G03 structural regressionはblocking。
- G01/G02/ENH-E6 protected semanticsはblocking。
- Test Agentはproduction/test/dependency/migration codeを変更しない。
- URLだけでなくvisible top-level surface / selected state / context stateを同時にassertする。
- Browser success journeyでscreenshotを保存する。
- console/page errorをblocking evidenceとして確認する。
- ACをTest Item名やCoding reportから推定してPASSにしない。direct assertionを要求する。

## 4. Candidate identity audit — MUST FIRST

1. Fixed Trial Candidate SHA取得。
2. actual checkout / HEAD記録。
3. Candidate後diff audit。
4. identity不明ならBLOCKED。

## 5. Acceptance Criteria

| AC ID | Criterion | Required evidence | Severity |
|---|---|---|---|
| AC-G04-01 | `/`がduplicate historyなしで`/projects`へnormalize | browser history + route assertion | MUST |
| AC-G04-02 | canonical Project routes/create/short-route semantics成立 | route/product/browser | MUST |
| AC-G04-03 | PM local navとURL/selected sectionが一致 | browser + frontend contract | MUST |
| AC-G04-04 | Analysis Context restore/selection semantics維持 | frontend/browser | MUST |
| AC-G04-05 | Family/Stage URL/selected/default Stage semantics維持 | frontend/browser/catalog evidence | MUST |
| AC-G04-06 | PM→Analysis transition成立 | browser | MUST |
| AC-G04-07 | Analysis→PM return成立 | browser | MUST |
| AC-G04-08 | Analysis→Results / Lineage成立 | browser | MUST |
| AC-G04-09 | deep-link/reload/Back/ForwardでURL/surface/state同期 | browser history | MUST |
| AC-G04-10 | legacy analytical URL normalize | frontend/browser | MUST |
| AC-G04-11 | resource route semantics維持 | frontend/integration | MUST |
| AC-G04-12 | Causal/Exploratory/Predictive existing semantics維持 | protected operation tests | MUST |
| AC-G04-13 | 全journeyでG03 surface architecture維持 | G03 regression + browser | MUST |
| AC-G04-14 | console/page error、duplicate history、stale shellなし | browser runtime + source audit | MUST |
| AC-G04-15 | Project/domain/backend/API/persistence protected semantics regressionなし | full regression | MUST |

## 6. Test Item plan

| ID | Name | Covers AC | Primary layer | Blocking | Method |
|---|---|---|---|---|---|
| 001 | candidate_identity | META | META | YES | candidate audit |
| 002 | root_and_project_route_contract | 01,02,09 | FRONTEND/BROWSER | YES | root/project normalization |
| 003 | project_management_navigation_state | 03,13 | FRONTEND/BROWSER | YES | local nav/section/surface |
| 004 | analysis_context_family_stage_state | 04,05,13 | FRONTEND/BROWSER | YES | context/catalog/selected state |
| 005 | cross_surface_history | 06,07,08,09,13,14 | BROWSER_E2E | YES | PM↔Analysis↔Results + history |
| 006 | legacy_resource_routing | 10,11 | FRONTEND/BROWSER | YES | legacy/resource routes |
| 007 | analysis_operation_regression | 12,15 | API_INTEGRATION/FRONTEND | YES | Causal/Exploratory/Predictive |
| 008 | full_product_browser_journey | 01-09,12-14 | BROWSER_E2E | YES | end-to-end success journey |
| 009 | history_reload_console_browser | 01,09,14 | BROWSER_E2E | YES | deep/reload/back/forward/console |
| 010 | protected_full_regression | 13,15 | REGRESSION | YES | G03 + G01/G02/ENH-E6 protected suite |

`999`はGate Decision専用。

## 7. Browser E2E minimum journey

最低限以下をfresh browser contextで検証する。

```text
/
  -> /projects
  -> Project select
  -> /projects/<id>/overview
  -> context
  -> data
  -> analysis launcher
  -> /projects/<id>/analysis/<family>/<stage>
  -> Family switch
  -> Stage switch
  -> Results / Lineage
  -> /projects/<id>/results
  -> Analysis
  -> Project Management return
  -> Back / Forward / reload
```

各stepで確認:

- pathname
- visible top-level surface root
- selected local nav / Family / Stage
- current Project identity
- forbidden shell/navigation hidden/absent
- console/page error

## 8. Protected regression

- G03 full structural contract
- G01 canonical Project semantics
- G02 canonical Analysis / cross-surface / operation semantics
- ENH-E6 Family/Stage navigation semantics
- backend/API/persistence schemas

## 9. Test Agent prohibited work

- production/test/migration/dependency code変更
- Acceptance Criteria変更
- implementation修復
- Fixed Trial Candidate差し替え

## 10. Decision semantics

### PASS

全MUST ACをdirect evidenceで証明し、全blocking Test Itemとprotected regressionがPASS。

### FAIL

testable candidateにMUST AC/protected semantic violationがverified evidenceで確認される。

### BLOCKED

identity/environment/harness/prerequisite/contract ambiguityで妥当な判定不能。

## 11. Required output artifact contract

| Item | Name | Canonical path |
|---|---|---|
| 001 | candidate_identity | `30_test_report/G04/Trial<TRIAL_NO>/ENH-E7_G04_Trial<TRIAL_NO>_001_candidate_identity.md` |
| 002 | root_and_project_route_contract | `30_test_report/G04/Trial<TRIAL_NO>/ENH-E7_G04_Trial<TRIAL_NO>_002_root_and_project_route_contract.md` |
| 003 | project_management_navigation_state | `30_test_report/G04/Trial<TRIAL_NO>/ENH-E7_G04_Trial<TRIAL_NO>_003_project_management_navigation_state.md` |
| 004 | analysis_context_family_stage_state | `30_test_report/G04/Trial<TRIAL_NO>/ENH-E7_G04_Trial<TRIAL_NO>_004_analysis_context_family_stage_state.md` |
| 005 | cross_surface_history | `30_test_report/G04/Trial<TRIAL_NO>/ENH-E7_G04_Trial<TRIAL_NO>_005_cross_surface_history.md` |
| 006 | legacy_resource_routing | `30_test_report/G04/Trial<TRIAL_NO>/ENH-E7_G04_Trial<TRIAL_NO>_006_legacy_resource_routing.md` |
| 007 | analysis_operation_regression | `30_test_report/G04/Trial<TRIAL_NO>/ENH-E7_G04_Trial<TRIAL_NO>_007_analysis_operation_regression.md` |
| 008 | full_product_browser_journey | `30_test_report/G04/Trial<TRIAL_NO>/ENH-E7_G04_Trial<TRIAL_NO>_008_full_product_browser_journey.md` |
| 009 | history_reload_console_browser | `30_test_report/G04/Trial<TRIAL_NO>/ENH-E7_G04_Trial<TRIAL_NO>_009_history_reload_console_browser.md` |
| 010 | protected_full_regression | `30_test_report/G04/Trial<TRIAL_NO>/ENH-E7_G04_Trial<TRIAL_NO>_010_protected_full_regression.md` |

各Test Item reportには以下を含める。

```text
- Result
- Fixed Trial Candidate full SHA
- Tested Repository State full SHA
- Exact command / method
- Exit code

## AC mapping
## Direct assertion / predicate mapping
## Raw relevant evidence
## Facts
## Interpretation
## Protected contract relation
## Reproduction procedure
## Browser evidence
  - success/failure screenshots
  - console/page errors
  - URL/surface/state checkpoints
  - network/service log where applicable
```

### 11.2 Gate Decision

`30_test_report/G04/Trial<TRIAL_NO>/ENH-E7_G04_Trial<TRIAL_NO>_999_gate_decision.md`

Gate Decisionでは各ACについてSupporting Test Itemに加え、
direct assertion/predicate summaryを記録する。

## 12. Evidence commit rule

Product candidate identityはFixed Trial Candidate SHA。
reportはverification後evidence-only commit可能。
999作成後にProduct/test implementationを修復しない。
