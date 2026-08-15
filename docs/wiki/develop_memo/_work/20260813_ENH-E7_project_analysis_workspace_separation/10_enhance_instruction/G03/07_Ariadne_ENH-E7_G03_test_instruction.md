# Ariadne ENH-E7 G03 Test Instruction — Gate Verification Contract

文書種別: Primary Execution Contract  
Self-containment: MUST  
Verification contract status: FROZEN

## 1. Acceptance authority

本書がG03 Gate Acceptance Criteria authorityである。
`PACKAGE_COMPLETE` / Coding self-check / `READY_FOR_TEST`はGate acceptanceではない。

## 2. Gate objective / claim

Projects Surface / Project Management Shell / Analysis Workspace Shellを
DOM ownership・runtime visibility・navigation hierarchy・layout topologyで分離し、
old global shell / duplicate navigationを除去する。

## 3. Verification原則

- Fixed Trial Candidate identity auditを最初に行う。
- Test Agentはproduction/test/dependency/migration codeを変更しない。
- Coding reportはAcceptance authorityではない。
- UI structure ACはelement ID / label文字列の存在だけでPASSにしない。
- `surface separation`はDOM containment + runtime visibilityで直接証明する。
- `horizontal / vertical`はcomputed CSSまたはbounding-box relationshipで直接証明する。
- negative invariantはabsence query / source audit / runtime visibilityで直接証明する。
- success screenshotはBrowser Test Itemの必須supplemental evidenceとする。screenshot単独でPASS判定しない。

## 4. Candidate identity audit — MUST FIRST

1. Fixed Trial Candidate SHA取得。
2. actual checkout / HEAD記録。
3. Candidate後diff audit。
4. identity不明ならBLOCKED。

## 5. Acceptance Criteria

| AC ID | Criterion | Required evidence | Severity |
|---|---|---|---|
| AC-G03-01 | `/projects`と`/projects/new`がProjects SurfaceでありPM-local/Analysis-only chromeを表示しない | DOM containment + browser visibility | MUST |
| AC-G03-02 | selected Project routesがProject Management Shellとlocal navigationを持つ | DOM containment + browser visibility | MUST |
| AC-G03-03 | Project ManagementでAnalysis Context/Family/Stageが非表示 | browser negative assertion | MUST |
| AC-G03-04 | Analysis routeがProject Managementとは別top-level Analysis Workspace | DOM containment + browser visibility | MUST |
| AC-G03-05 | Analysis ContextとProject Management return actionがAnalysis上部に属する | DOM containment + browser evidence | MUST |
| AC-G03-06 | Family navigationがAnalysis内だけのhorizontal navigation | computed layout / bounding box + visibility | MUST |
| AC-G03-07 | Stage navigationがAnalysis内だけのvertical navigation、Contentsが右main area | computed layout / bounding box + visibility | MUST |
| AC-G03-08 | old global mixed sidebarがproduction DOMに存在しない | source + runtime absence | MUST |
| AC-G03-09 | global common Analysis Context headerが存在しない | source + runtime absence | MUST |
| AC-G03-10 | duplicate navigation / stale presentation bindingがない | source/diff + runtime query | MUST |
| AC-G03-11 | obsolete architectureをhidden DOMとして温存していない | source + runtime DOM audit | MUST |
| AC-G03-12 | backend/API/persistence/domain/analysis execution semantics変更なし | diff + protected tests | MUST |
| AC-G03-13 | G01/G02 canonical route/domain/navigation semanticsがregressionしない | protected regression | MUST |

## 6. Test Item plan

| Test Item ID | Name | Covers AC | Primary layer | Blocking | Method |
|---|---|---|---|---|---|
| 001 | candidate_identity | META | META | YES | Fixed Candidate audit |
| 002 | projects_surface_topology | 01,08,09,10,11 | FRONTEND_CONTRACT/BROWSER | YES | containment + negative visibility |
| 003 | project_management_shell_topology | 02,03,08,09,10 | FRONTEND_CONTRACT/BROWSER | YES | PM shell/local nav ownership |
| 004 | analysis_workspace_shell_topology | 04,05,06,07,09,10 | FRONTEND_CONTRACT/BROWSER | YES | Analysis ownership / containment |
| 005 | layout_orientation_runtime | 06,07 | BROWSER_E2E | YES | computed CSS / bounding boxes |
| 006 | obsolete_shell_absence | 08,09,10,11 | SOURCE/FRONTEND_CONTRACT | YES | obsolete DOM/CSS/JS absence |
| 007 | protected_semantic_smoke | 12,13 | REGRESSION | YES | G01/G02 protected tests |
| 008 | surface_architecture_browser_journey | 01-07,10,13 | BROWSER_E2E | YES | Projects→PM→Analysis; success screenshots |

`999`はGate Decision専用。

## 7. Direct verification requirements

以下のようなassertionは単独では不十分。

```text
assert 'id="analysis-stage-sidebar"' in html
assert 'Project Management' in html
```

以下のpredicateまで確認すること。

```text
Projects:
  visible top-level root == projects
  project-local nav hidden
  analysis context/family/stage hidden

Project Management:
  visible top-level root == project-management
  local nav descendant of PM root
  analysis context/family/stage hidden

Analysis:
  visible top-level root == analysis
  analysis context/family/stage descendant of Analysis root
  project-local nav hidden
  family horizontal
  stage vertical
  stage contents right of stage navigation
```

## 8. Protected regression

- canonical Project route / lifecycle behavior
- canonical Analysis route / Family / Stage catalog
- existing operation semantics
- backend/API/persistence schemas

## 9. Test Agent prohibited work

- production/test/migration/dependency code変更
- Acceptance Criteria変更
- implementation修復
- Fixed Trial Candidate差し替え

## 10. Decision semantics

### PASS

全MUST ACに対してdirect verification predicateが成立し、全blocking Test ItemがPASS。

### FAIL

testable candidateにMUST AC/protected semantic violationがverified evidenceで確認される。

### BLOCKED

identity/environment/harness/prerequisite/contract ambiguityにより妥当な判定ができない。

## 11. Required output artifact contract

`<TRIAL_NO>`は2桁runtime値。

| Item | Name | Canonical path |
|---|---|---|
| 001 | candidate_identity | `30_test_report/G03/Trial<TRIAL_NO>/ENH-E7_G03_Trial<TRIAL_NO>_001_candidate_identity.md` |
| 002 | projects_surface_topology | `30_test_report/G03/Trial<TRIAL_NO>/ENH-E7_G03_Trial<TRIAL_NO>_002_projects_surface_topology.md` |
| 003 | project_management_shell_topology | `30_test_report/G03/Trial<TRIAL_NO>/ENH-E7_G03_Trial<TRIAL_NO>_003_project_management_shell_topology.md` |
| 004 | analysis_workspace_shell_topology | `30_test_report/G03/Trial<TRIAL_NO>/ENH-E7_G03_Trial<TRIAL_NO>_004_analysis_workspace_shell_topology.md` |
| 005 | layout_orientation_runtime | `30_test_report/G03/Trial<TRIAL_NO>/ENH-E7_G03_Trial<TRIAL_NO>_005_layout_orientation_runtime.md` |
| 006 | obsolete_shell_absence | `30_test_report/G03/Trial<TRIAL_NO>/ENH-E7_G03_Trial<TRIAL_NO>_006_obsolete_shell_absence.md` |
| 007 | protected_semantic_smoke | `30_test_report/G03/Trial<TRIAL_NO>/ENH-E7_G03_Trial<TRIAL_NO>_007_protected_semantic_smoke.md` |
| 008 | surface_architecture_browser_journey | `30_test_report/G03/Trial<TRIAL_NO>/ENH-E7_G03_Trial<TRIAL_NO>_008_surface_architecture_browser_journey.md` |

各reportには最低限以下を持つ。

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
  - success/failure screenshot
  - computed layout / bounding-box evidence where applicable
  - console/page error
  - network/service log where applicable
```

### 11.2 Gate Decision

`30_test_report/G03/Trial<TRIAL_NO>/ENH-E7_G03_Trial<TRIAL_NO>_999_gate_decision.md`

Gate Decisionでは各ACについて、単にSupporting Test Item IDを列挙するだけでなく、
**そのACを直接証明したpredicate/assertionの要約**を記載する。

## 12. Evidence commit rule

Product candidate identityはFixed Trial Candidate SHA。
Test reportはverification後にevidence-only commitとしてcommit可能。
999作成後にProduct/test implementationを修復してはならない。
