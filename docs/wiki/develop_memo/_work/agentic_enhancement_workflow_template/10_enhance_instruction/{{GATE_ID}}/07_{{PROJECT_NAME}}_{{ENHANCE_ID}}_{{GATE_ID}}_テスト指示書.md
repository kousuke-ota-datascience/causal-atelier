# {{PROJECT_NAME}} {{ENHANCE_ID}} {{GATE_ID}} テスト指示書 — Gate Verification Contract

- Project: {{PROJECT_NAME}}
- Enhancement: {{ENHANCE_ID}}
- Active Gate: {{GATE_ID}}
- Verification contract status: FROZEN
- Current State Control Sheet: {{CONTROL_SHEET_PATH}}

## 1. Acceptance authority

本書07がAcceptance Criteria authorityである。

Test / Audit AgentはWork Package completionやCoding self-checkをGate acceptanceへ読み替えない。

## 2. Document precedence

1. Human-approved Gate Contract Amendment
2. 本書07
3. 06 Gate Coding Contract
4. applicable 08 remediation
5. P00 / package instruction — execution context only
6. final PASS previous Gate Decision
7. Current State Control Sheet
8. Implementation Completion Report
9. Package Checkpoint Reports
10. current observable source/test/migration

矛盾がGate判定に影響する場合は`BLOCKED`とする。

## 3. Required verification input

- Implementation Completion Report: {{COMPLETION_REPORT_PATH_TO_BE_SPECIFIED_AT_EXECUTION}}
- Fixed Trial Candidate SHA: completion report内full SHA
- Tested Repository State: Test Agentが実測して記録
- 06: {{PATH_06}}
- Applicable 08: {{REMEDIATION_PATH_OR_NONE}}
- P00 / package reports: candidate provenance確認に必要な範囲のみ

## 4. Candidate identity audit — MUST FIRST

Test開始前に:

1. Fixed Trial Candidate SHAを取得。
2. actual checkout / HEADを記録。
3. 相違がある場合、Fixed Candidate以降のdiffを確認。
4. production / automated-test / migration / dependency semantics変更がないことを確認。
5. candidate identityが不明なら本体testへ進まず`BLOCKED`。

## 5. Gate objective / acceptance claim

{{GATE_OBJECTIVE}}

PASS後にdownstreamが依存可能になるcontract:

{{DOWNSTREAM_USABLE_RESULT_AFTER_PASS}}

## 6. Acceptance Criteria

| AC ID | Criterion | Required evidence | Severity |
|---|---|---|---|
| AC-{{N}} | {{CRITERION}} | {{EVIDENCE}} | MUST / SHOULD |

## 7. Test Item plan

| Test Item ID | Name | Covers AC | Method |
|---|---|---|---|
| 001 | candidate_identity | META | repository / diff audit |
| {{ITEM_ID}} | {{NAME}} | {{AC_IDS}} | {{METHOD}} |

`999`はGate Decision reserved。

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

各Test Item Report:

- Fixed Trial Candidate SHA
- Tested Repository State full SHA
- exact command
- exit code
- relevant raw output
- observed Facts
- Interpretation separated
- AC mapping
- protected Gate / TD relation
- reproduction steps

## 12. Decision semantics

### PASS

全MUST AC、candidate identity audit、required regression、blocking TD conditionが成立。

### FAIL

test実行可能であり、Fixed Trial CandidateがMUST ACまたはprotected contractを満たさない。

### BLOCKED

environment / prerequisite / candidate identity / contract ambiguity等により妥当なproduct判定ができない。

## 13. Required outputs

- `30_test_report/{{GATE_ID}}/Trial{{TRIAL_NO}}/..._{{TEST_ITEM_ID}}_*.md`
- `30_test_report/{{GATE_ID}}/Trial{{TRIAL_NO}}/..._999_gate_decision.md`
- PASS / FAIL / BLOCKED後に停止
