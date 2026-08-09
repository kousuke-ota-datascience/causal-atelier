# {{ENHANCE_ID}} {{GATE_ID}} Trial {{TRIAL_ID}} Gate Decision

- Project: {{PROJECT_NAME}}
- Enhancement: {{ENHANCE_ID}}
- Gate: {{GATE_ID}}
- Trial: {{TRIAL_ID}}
- Reserved Test Item ID: 999
- Status: PASS / FAIL / BLOCKED
- Tested commit: {{TESTED_COMMIT_FULL_SHA}}
- 07 Contract: {{PATH_07}}
- Completion report: {{COMPLETION_REPORT_PATH}}
- Applicable 08: {{PATH_OR_NONE}}
- Decision timestamp: {{TIMESTAMP_ISO8601_TZ}}

## 1. Decision summary

{{DECISION_SUMMARY}}

## 2. Test Item evidence index

| Item | Name | Status | AC | Evidence path |
|---|---|---|---|---|
| {{ITEM_ID}} | {{NAME}} | PASS / FAIL / BLOCKED | {{AC}} | {{PATH}} |

## 3. Acceptance Criteria evaluation

| AC | Result | Evidence |
|---|---|---|
| {{AC_ID}} | PASS / FAIL / BLOCKED | {{ITEM_PATHS}} |

## 4. Protected passed-Gate regression

| Previous Gate | Protected semantic | Regression result | Evidence |
|---|---|---|---|
| {{GATE_OR_NONE}} | {{SEMANTIC}} | PASS / FAIL / N/A | {{PATH}} |

## 5. Transition Debt decision

| TD ID | Before | After | Decision / evidence |
|---|---|---|---|
| {{TD_ID_OR_NONE}} | OPEN / NONE | OPEN / CLOSED / CANCELLED / NONE | {{EVIDENCE}} |

## 6. Established contract after PASS

Complete only when Status = PASS.

{{NEWLY_ESTABLISHED_SEMANTICS_OR_NA}}

## 7. Control Sheet update eligibility

- Eligible: YES only if final Status = PASS; otherwise NO
- Sections to update: {{SECTIONS_OR_NONE}}
- Promotion basis: this Gate Decision + referenced Test Item evidence

## 8. Failure remediation input

Complete only when Status = FAIL.

- Failure facts requiring correction: {{FAILURE_FACTS_OR_NA}}
- Suggested scope for 08 authoring: {{REMEDIATION_SCOPE_OR_NA}}
- Acceptance Criteria remain unchanged: YES

Test Agent does not author the implementation fix.

## 9. Blocker record

Complete only when Status = BLOCKED.

- Blocker class: prerequisite / environment / contract ambiguity / unsafe operation / other
- Facts: {{BLOCKER_FACTS_OR_NA}}
- Required owner/action: {{OWNER_ACTION_OR_NA}}

## 10. Final rationale

{{FINAL_RATIONALE}}
