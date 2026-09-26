# {{PROJECT_NAME}} {{ENHANCE_ID}} {{GATE_ID}} テスト指示書 — Gate Verification Contract

**Document class:** Primary Execution Contract  
**Self-containment:** MUST — Test / Audit AgentがGate acceptanceを判定するためのnormative criteriaを本書内に保持する。

- Project: {{PROJECT_NAME}}
- Enhancement: {{ENHANCE_ID}}
- Active Gate: {{GATE_ID}}
- Verification contract status: FROZEN
- canonical evidence-derived state model (verified-fact reference): {{CONTROL_SHEET_PATH}}

## 1. Acceptance authority

本書07がoriginal Gate Acceptance Criteria authorityである。Work Package completion、Coding self-check、Completion Reportの`READY_FOR_TEST`をGate acceptanceへ読み替えない。

## 2. Gate objective / acceptance claim

{{GATE_OBJECTIVE}}

PASS後にdownstreamが依存可能になるcontract:

{{DOWNSTREAM_USABLE_RESULT_AFTER_PASS}}

## 3. Effective verification context

本Gateを判定するために必要なsemantic assumptions / protected constraintsを、06を読まなくても理解できる粒度で記載する。

{{EFFECTIVE_VERIFICATION_CONTEXT}}

## 4. Required verification inputs — evidence / observation targets

- Implementation Completion Report: {{COMPLETION_REPORT_PATH_TO_BE_SPECIFIED_AT_EXECUTION}}
- Fixed Trial Candidate SHA: Completion Reportから取得
- Tested Repository State: Test Agentが実測して記録
- source / test / migration / runtime state: current observable facts
- previous PASS evidence: {{PREVIOUS_PASS_EVIDENCE_OR_NONE}}
- applicable remediation context: {{REMEDIATION_CONTEXT_OR_NONE}}

これらはevidence / fact sourceであり、本書のAcceptance Criteriaを外部から補完するためのnormative sourceではない。

## 5. Candidate identity audit — MUST FIRST

1. Fixed Trial Candidate SHAを取得する。
2. actual checkout / HEADを記録する。
3. 相違がある場合、Fixed Candidate以降のdiffを確認する。
4. production / automated-test / migration / dependency semantics変更の有無を判定する。
5. candidate identityが不明なら本体testへ進まず`BLOCKED`。

## 6. Acceptance Criteria

| AC ID | Criterion | Required evidence | Severity |
|---|---|---|---|
| AC-{{N}} | {{CRITERION}} | {{EVIDENCE}} | MUST / SHOULD |

ACは本書内にcomplete formで記載する。「06の要件を満たすこと」のように外部contractへ委譲しない。

## 7. Test Item plan

| Test Item ID | Name | Covers AC | Primary test layer | Gate blocking | Method |
|---|---|---|---|---|---|
| 001 | candidate_identity | META | META | YES | repository / diff audit |
| {{ITEM_ID}} | {{NAME}} | {{AC_IDS}} | META / UNIT_DOMAIN / API_INTEGRATION / FRONTEND_CONTRACT / BROWSER_E2E / OTHER | YES / NO | {{METHOD}} |

`999`はGate Decision reserved。

### 7.1 Test layer allocation

各Acceptance Criteria / Test Itemについて、最もdeterministicでfailure localizationしやすいprimary test layerを選ぶ。詳細correctnessをBrowser E2Eへ集中させない。

```text
Unit / domain tests
    = domain rule / validation
API integration tests
    = request / response / persistence contract
Frontend contract tests
    = caller payload / rendering contract
Browser E2E
    = critical user journey の real cross-layer connectivity
```

### 7.2 Gate blocking Browser E2E — conditional

Gate blockingとして維持するcanonical Browser E2E suite全体は原則3〜5本程度のcritical user journeyに限定する。本Gateの07は、そのcanonical suiteから本GateのACにrelevantなsubsetだけを選択する。Browser surfaceがないGateは0本でよい。各Gateへ3〜5本ずつ追加してsuiteを増殖させない。canonical suite全体が5本を超える場合、lower-level testでは代替できない理由をauthoring recordへ残す。

各Browser E2E Test Itemには最低限以下を本書内で具体化する。

- critical journey / cross-layer boundary
- canonical command / method
- clean/current-source environment bootstrap / teardown rule
- semantic synchronization point
- observable behavior assertion
- failure evidence requirement
- failure classificationとFAIL / BLOCKED boundary

共通方針は`40_operator_workflows/BROWSER_E2E_GATE_POLICY.md`に保持してよいが、Test AgentがGate判定するために必要な具体的ruleを本書外へ委譲しない。

## 8. Protected passed-Gate regression

| Previous Gate | Protected semantic | Regression Test Item | Required result |
|---|---|---|---|
| {{GATE_OR_NONE}} | {{SEMANTIC}} | {{ITEM_ID}} | PASS |

## 9. Transition Debt audit

| TD ID | Expected after Gate | Scope / exit criterion | Test Item |
|---|---|---|---|
| {{TD_ID_OR_NONE}} | OPEN / CLOSED / NONE | {{CRITERION}} | {{ITEM_ID_OR_NA}} |

## 10. Test Agent prohibited work

- production code modification
- automated test code modification
- migration modification
- dependency modification
- Acceptance Criteria modification
- implementation repair
- package checkpointをFixed Candidateへ勝手に差し替えること

## 11. Evidence requirements

各Test Item Reportに最低限:

- Fixed Trial Candidate SHA
- Tested Repository State full SHA
- exact command / method
- exit code
- relevant raw evidence
- observed Facts / Interpretation separated
- AC mapping
- protected Gate / TD relation
- reproduction procedure

Browser E2E Test Itemでは、利用可能な範囲で追加して以下を要求する。

- Playwright trace / screenshot / video
- browser console / page errors
- relevant network request / response（URL / method / request body / response status / response body。secretはredact）
- API / worker logs
- Compose / service state
- failed synchronization point / assertion
- failure classification: `PRODUCT_INTEGRATION_DEFECT / TEST_IMPLEMENTATION_DEFECT / TEST_ORCHESTRATION_DEFECT / TEST_ENVIRONMENT_DEFECT / UNKNOWN`

HTTP status単体をroot causeとせず、intentional negative responseとactual failing assertionを区別する。

## 12. Decision semantics

### PASS
全MUST AC、candidate identity audit、required regression、blocking TD conditionが成立。

### FAIL
test実行可能であり、Fixed Trial CandidateがMUST ACまたはprotected contractを満たさない。

Browser E2Eの場合、`PRODUCT_INTEGRATION_DEFECT`等としてproduct / contract violationがevidenceでverifiedされていること。

### BLOCKED
environment / prerequisite / candidate identity / contract ambiguity等により妥当なproduct判定ができない。Browser E2Eの`TEST_IMPLEMENTATION_DEFECT / TEST_ORCHESTRATION_DEFECT / TEST_ENVIRONMENT_DEFECT / UNKNOWN`によりproduct correctnessを判定できない場合も原則BLOCKEDとし、product FAILへ読み替えない。

## 13. Remediation Trial handling

formal FAIL後のnext Trialでは08が存在し得る。

- `08 DELTA`: Test Agentへ08を追加contextとして与える場合、07のACは本書のままimmutable。08はfailure-specific test method / re-verification deltaを定義できるがACを変更できない。
- `08 CONSOLIDATED`: operatorが08をnext Trialのeffective remediation contractとして使用する場合でも、Gate acceptance claim / ACの変更は認めない。08内のverification requirementと本書ACが衝突した場合は`BLOCKED_CONTRACT_AMBIGUITY`。
- Browser E2Eがtriggerの場合、formal FAIL remediationへ渡すfailure factsはproduct / contract violationがverifiedされたものに限定する。test implementation / orchestration / environment defectだけでproduct判定不能ならBLOCKEDとして扱い、production remediation 08を自動生成しない。

## 14. Required outputs

- `30_test_report/{{GATE_ID}}/Trial{{TRIAL_NO}}/..._{{TEST_ITEM_ID}}_*.md`
- `30_test_report/{{GATE_ID}}/Trial{{TRIAL_NO}}/..._999_gate_decision.md`
- PASS / FAIL / BLOCKED後に停止
