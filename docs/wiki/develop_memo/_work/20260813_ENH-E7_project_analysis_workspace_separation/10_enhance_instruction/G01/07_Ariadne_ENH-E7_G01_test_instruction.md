# Ariadne ENH-E7 G01 Test Instruction — Gate Verification Contract

**文書種別:** Primary Execution Contract  
**Self-containment:** MUST  
**Verification contract status:** FROZEN

## 1. Acceptance authority

Human/operatorがGate execution前に本07をFROZENにした時点で、
本書がoriginal Gate Acceptance Criteria authorityになる。

Work Package completion、Coding self-check、`READY_FOR_TEST`はGate acceptanceではない。

## 2. Gate objective / claim

canonical Project Management routingを確立し、Project lifecycle / Research Context / Data・Analysis View / Results・Lineageを明示的Project-local responsibilityへ移設する。domain semanticsは変更しない。

PASSで以下を成立させる。

Projectの作成・選択・管理が独立したURL-authoritative Project Management surfaceとして成立し、downstreamがProject route、section ownership、analysis input resource ownershipへ安全に依存できる。

## 3. Verification原則

- Product testより先にFixed Trial Candidate identityをauditする。
- protected upstream regressionはblocking。
- Test Agentはproduction/test/dependency/migration codeを変更しない。
- Coding reportはevidence inputでありAcceptance authorityではない。

## 4. Candidate identity audit — MUST FIRST

1. Fixed Trial Candidate SHAを取得。
2. actual checkout / HEADを記録。
3. Fixed Candidate後のdiffをaudit。
4. candidate identityが曖昧ならBLOCKED。

## 5. Acceptance Criteria

| AC ID | Criterion | Required evidence | Severity |
|---|---|---|---|
| AC-G01-01 | `/projects`がcanonical Project List surfaceである。 | independent source/test/runtime evidence | MUST |
| AC-G01-02 | `/projects/new`がcanonical Project Register surfaceである。 | independent source/test/runtime evidence | MUST |
| AC-G01-03 | Project作成後`/projects/<id>/overview`へ遷移する。 | independent source/test/runtime evidence | MUST |
| AC-G01-04 | `/projects/<id>`がduplicate historyなしで`/overview`へnormalizeする。 | independent source/test/runtime evidence | MUST |
| AC-G01-05 | Overview / Context / Data / Results local navigationとURLが一致する。 | independent source/test/runtime evidence | MUST |
| AC-G01-06 | Project metadataとDataset/Analysis View managementが分離される。 | independent source/test/runtime evidence | MUST |
| AC-G01-07 | Project ArchiveがOverviewに属する。 | independent source/test/runtime evidence | MUST |
| AC-G01-08 | Analysis View lifecycleがDataに属する。 | independent source/test/runtime evidence | MUST |
| AC-G01-09 | Analysis ViewがFamily横断inputとして利用可能である。 | independent source/test/runtime evidence | MUST |
| AC-G01-10 | Results / Lineageのexisting cross-analysis機能が維持される。 | independent source/test/runtime evidence | MUST |
| AC-G01-11 | Project routeのdirect link/reload/Back/Forwardが成立する。 | independent source/test/runtime evidence | MUST |
| AC-G01-12 | existing Project/domain semanticsとENH-E6 protected Analysis semanticsがregressionしない。 | independent source/test/runtime evidence | MUST |

## 6. Test Item plan

| Test Item ID | Name | Covers AC | Primary test layer | Gate blocking | Method |
|---|---|---|---|---|---|
| 001 | candidate_identity | META | META | YES | Fixed Trial Candidate SHAとtested checkoutをaudit。 |
| 002 | project_route_contract | AC-G01-01,02,03,04,05,11 | FRONTEND_CONTRACT | YES | route parse/serialize/normalization/history test。 |
| 003 | project_surface_ownership | AC-G01-06,07,08,09,10 | FRONTEND_CONTRACT | YES | DOM/static/frontend ownership contract test。 |
| 004 | project_domain_regression | AC-G01-03,07,08,10,12 | API_INTEGRATION/UNIT_DOMAIN | YES | existing Project/Context/Data/Result regression。 |
| 005 | project_browser_journey | AC-G01-01,02,03,05,11 | BROWSER_E2E | YES | Projects → select/create → Overview → Context → Data → Results → Back/Forward/reload。 |
| 006 | protected_analysis_regression | AC-G01-12 | FRONTEND_CONTRACT | YES | ENH-E6 protected Analysis navigation regression。 |

`999`はGate Decision専用。

## 7. Browser E2E

repository既存Browser E2E harnessとcurrent-source environmentを使用する。
failure時はURL/state、expected state、screenshot/trace、console、network、service log、
exact failing assertionを可能な範囲で記録する。

Harness/environment defectでProduct判定不能ならFAILではなくBLOCKED。

## 8. Protected passed-Gate regression

- Previous Gate: ENH-E6 G01
- Protected semantic: ENH-E6 G01 PASS candidate `575cdd139aea09d4f19b46ab6a6d38545f645c71` が確立したcanonical Analysis Family/Stage navigation / transition semantics。
- Required result: PASS

## 9. Test Agent prohibited work

- production/test/migration/dependency code変更
- Acceptance Criteria変更
- implementation修復
- Fixed Trial Candidateをpackage-level handoff evidenceへ置換
- Coding Agent PxxをAcceptance authorityとして使用

## 10. Decision semantics

### PASS
すべてのMUST AC、candidate identity audit、required regression、blocking Test ItemがPASS。

### FAIL
candidateがtestableで、verified evidenceがMUST AC/protected semantic violationを示す。

### BLOCKED
candidate identity / environment / harness / prerequisite / contract ambiguityにより妥当なProduct判定ができない。

## 11. Required output artifact contract

`<TRIAL_NO>` はHuman/operatorから指定された2桁runtime値（例: `01`）。

### 11.1 Test Item report canonical path

| Test Item | Name | Canonical path |
|---|---|---|
| 001 | `candidate_identity` | `30_test_report/G01/Trial<TRIAL_NO>/ENH-E7_G01_Trial<TRIAL_NO>_001_candidate_identity.md` |
| 002 | `project_route_contract` | `30_test_report/G01/Trial<TRIAL_NO>/ENH-E7_G01_Trial<TRIAL_NO>_002_project_route_contract.md` |
| 003 | `project_surface_ownership` | `30_test_report/G01/Trial<TRIAL_NO>/ENH-E7_G01_Trial<TRIAL_NO>_003_project_surface_ownership.md` |
| 004 | `project_domain_regression` | `30_test_report/G01/Trial<TRIAL_NO>/ENH-E7_G01_Trial<TRIAL_NO>_004_project_domain_regression.md` |
| 005 | `project_browser_journey` | `30_test_report/G01/Trial<TRIAL_NO>/ENH-E7_G01_Trial<TRIAL_NO>_005_project_browser_journey.md` |
| 006 | `protected_analysis_regression` | `30_test_report/G01/Trial<TRIAL_NO>/ENH-E7_G01_Trial<TRIAL_NO>_006_protected_analysis_regression.md` |

各Test Item reportは最低限以下を本文内に持つ。

```text
# ENH-E7 G01 Trial<TRIAL_NO> Test Item <TEST_ITEM_ID> — <TEST_ITEM_NAME>

- Result: PASS | FAIL | BLOCKED
- Fixed Trial Candidate full SHA: <40-hex SHA>
- Tested Repository State full SHA: <40-hex SHA>
- Exact command / method:
- Exit code:

## AC mapping
## Raw relevant evidence
## Facts
## Interpretation
## Protected contract / Transition Debt relation
## Reproduction procedure
## Browser evidence（Browser Test Itemの場合）
  - screenshot / trace / video
  - console / page error
  - network
  - service log
  - failed synchronization/assertion
  - failure classification
```

### 11.2 Gate Decision report

Canonical path:

```text
30_test_report/G01/Trial<TRIAL_NO>/
ENH-E7_G01_Trial<TRIAL_NO>_999_gate_decision.md
```

必須内容:

```text
# ENH-E7 G01 Trial<TRIAL_NO> Test Item 999 — Gate Decision

- Gate decision: PASS | FAIL | BLOCKED
- Enhancement: ENH-E7
- Gate: G01
- Trial: <TRIAL_NO>
- Fixed Trial Candidate full SHA: <40-hex SHA>
- Tested Repository State full SHA: <40-hex SHA>

## Test Item result summary
| Test Item | Result | Evidence path |

## Acceptance Criteria conclusion
| AC | Supporting Test Items | Result |

## Candidate identity conclusion
## Protected contract conclusion
## Transition Debt conclusion
## Promotion eligibility
## Facts
## Interpretation
```

### 11.3 Evidence commit rule

Test execution対象のProduct candidate identityはFixed Trial Candidate SHAである。
Test report作成・commitによってSHAを自己参照させない。

Test reportはverification後にevidence-only commitとしてcommitしてよい。
report自身のcommit SHAを同report本文へ自己記録することは要求しない。

Test Item reportをすべて作成した後、最後に`999_gate_decision`を作成する。
Gate Decision作成後にProduct/test implementationを修復してはならない。

