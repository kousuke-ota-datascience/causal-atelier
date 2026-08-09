# {{ENHANCE_ID}} {{GATE_ID}} Implementation Report Detail

- Project: {{PROJECT_NAME}}
- Enhancement: {{ENHANCE_ID}}
- Gate: {{GATE_ID}}
- 06 Contract: {{PATH_06}}
- 07 Contract: {{PATH_07}}
- Current Trial: {{CURRENT_TRIAL}}
- Ledger status: ACTIVE / FINALIZED_AFTER_PASS / ABANDONED

## 1. Purpose

この文書は**当該Gate内部だけ**の累積implementation ledgerである。
未検証implementation stateを記録してよいが、verified current stateやGate PASSを宣言してはならない。

## 2. Trial history

| Trial | Starting commit | Implementation commit | Remediation | Completion report | Coding status |
|---|---|---|---|---|---|
| {{TRIAL_ID}} | {{START}} | {{IMPLEMENTATION}} | {{08_OR_NONE}} | {{REPORT_PATH}} | READY_FOR_TEST / BLOCKED |

## 3. Current implementation state — unverified until Gate PASS

{{CURRENT_IMPLEMENTATION_STATE}}

## 4. Files / components touched across this Gate

{{TOUCHED_COMPONENTS}}

## 5. Protected passed-Gate interactions

{{PROTECTED_INTERACTIONS_OR_NONE}}

## 6. Transition Debt implementation ledger

| TD ID | Trial | Action | Fact |
|---|---|---|---|
| {{TD_ID_OR_NONE}} | {{TRIAL}} | introduce / preserve / close | {{FACT}} |

## 7. Open Coding observations

{{OPEN_OBSERVATIONS_OR_NONE}}

## 8. Finalization rule

- final PASS後: `FINALIZED_AFTER_PASS`とし、Gate Decisionへのlinkを追加する。
- verified stateそのものはCurrent State Control Sheetで管理する。
- FAIL中: current implementation stateをverifiedとして表現しない。

## 9. Final Gate Decision

{{FINAL_GATE_DECISION_PATH_OR_PENDING}}
