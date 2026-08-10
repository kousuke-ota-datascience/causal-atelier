# {{ENHANCE_ID}} {{GATE_ID}} Implementation Report Detail

- Project: {{PROJECT_NAME}}
- Enhancement: {{ENHANCE_ID}}
- Gate: {{GATE_ID}}
- 06 Contract: {{PATH_06}}
- 07 Contract: {{PATH_07}}
- Execution Mode: SINGLE_EXECUTION / WORK_PACKAGE
- Current Trial: {{CURRENT_TRIAL}}
- Current Package: {{CURRENT_PACKAGE_OR_NA}}
- Ledger status: ACTIVE / FINALIZED_AFTER_PASS / ABANDONED

## 1. Purpose

当該Gate内部の累積implementation ledger。未検証stateを記録してよいが、verified current stateやGate PASSを宣言しない。

## 2. Trial history
| Trial | Fixed Candidate | Remediation | Completion report | Independent decision |
|---|---|---|---|---|
| {{TRIAL_NO}} | {{FIXED_SHA_OR_NONE}} | {{08_OR_NONE}} | {{REPORT_PATH_OR_PENDING}} | PASS / FAIL / BLOCKED / PENDING |

## 3. Package history
| Trial | Package | Status | Checkpoint SHA | Status report | Checkpoint report | Restart count |
|---|---|---|---|---|---|---:|
| {{TRIAL}} | {{PACKAGE}} | COMPLETE / BLOCKED / IN_PROGRESS | {{SHA}} | {{PATH}} | {{PATH}} | {{COUNT}} |

## 4. Current implementation state — unverified until Gate PASS
{{CURRENT_IMPLEMENTATION_STATE}}

## 5. Candidate assembly state
- State: NOT_STARTED / IN_PROGRESS / READY_FOR_TEST / UNDER_TEST / DECIDED
- Fixed Candidate SHA: {{SHA_OR_NONE}}
- Outstanding candidate-affecting issue: {{NONE_OR_DETAIL}}

## 6. Protected passed-Gate interactions
{{PROTECTED_INTERACTIONS_OR_NONE}}

## 7. Transition Debt implementation ledger
| TD ID | Trial | Package | Action | Fact |
|---|---|---|---|---|
| {{TD_ID_OR_NONE}} | {{TRIAL}} | {{PACKAGE_OR_NA}} | introduce / preserve / close | {{FACT}} |

## 8. Open Coding observations
{{OPEN_OBSERVATIONS_OR_NONE}}

## 9. Finalization rule

- package completeではfinalizeしない。
- READY_FOR_TESTでもverified promotionしない。
- final PASS後に`FINALIZED_AFTER_PASS`としてGate Decisionをlinkする。
- verified stateはCurrent State Control Sheetで管理する。

## 10. Final Gate Decision
{{FINAL_GATE_DECISION_PATH_OR_PENDING}}
