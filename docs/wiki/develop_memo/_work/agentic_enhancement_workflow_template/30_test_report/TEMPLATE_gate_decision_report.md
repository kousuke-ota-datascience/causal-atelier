# {{ENHANCE_ID}} {{GATE_ID}} Trial {{TRIAL_NO}} Gate Decision

- Project: {{PROJECT_NAME}}
- Enhancement: {{ENHANCE_ID}}
- Gate: {{GATE_ID}}
- Trial: {{TRIAL_NO}}
- Reserved Test Item ID: 999
- Status: PASS / FAIL / BLOCKED
- Fixed Trial Candidate SHA: {{FIXED_TRIAL_CANDIDATE_FULL_SHA}}
- Tested Repository State: {{TESTED_REPOSITORY_FULL_SHA}}
- 07 Contract: {{PATH_07}}
- Completion report: {{COMPLETION_REPORT_PATH}}
- Applicable 08: {{PATH_OR_NONE}}
- Decision timestamp: {{TIMESTAMP_ISO8601_TZ}}

## 1. Decision summary
{{DECISION_SUMMARY}}

## 2. Candidate identity decision

- Fixed Candidate established by Completion Report: YES / NO
- Tested state equals candidate: YES / NO
- If NO, post-candidate diff classification: DOCUMENTATION_ONLY / CANDIDATE_AFFECTING / UNKNOWN
- Candidate identity valid for acceptance: YES / NO
- Evidence: {{PATHS}}

## 3. Package-chain provenance audit

For SINGLE_EXECUTION: `N/A`.

| Package | Checkpoint present | Report present | Required for candidate | Provenance status |
|---|---|---|---|---|
| {{PACKAGE_ID}} | YES / NO | YES / NO | YES / NO | COMPLETE / GAP |

Package provenance is supporting evidence; package completion alone does not decide Gate PASS.

## 4. Test Item evidence index
| Item | Name | Status | AC | Evidence path |
|---|---|---|---|---|
| {{ITEM_ID}} | {{NAME}} | PASS / FAIL / BLOCKED | {{AC}} | {{PATH}} |

## 5. Acceptance Criteria evaluation
| AC | Result | Evidence |
|---|---|---|
| {{AC_ID}} | PASS / FAIL / BLOCKED | {{ITEM_PATHS}} |

## 6. Protected passed-Gate regression
| Previous Gate | Protected semantic | Regression result | Evidence |
|---|---|---|---|
| {{GATE_OR_NONE}} | {{SEMANTIC}} | PASS / FAIL / N/A | {{PATH}} |

## 7. Transition Debt decision
| TD ID | Before | After | Decision / evidence |
|---|---|---|---|
| {{TD_ID_OR_NONE}} | OPEN / NONE | OPEN / CLOSED / CANCELLED / NONE | {{EVIDENCE}} |

## 8. Established contract after PASS

Complete only when Status=PASS.

### Established semantic claim
{{NEWLY_ESTABLISHED_SEMANTICS_OR_NA}}

### Downstream reliance now allowed
{{DOWNSTREAM_RELIANCE_OR_NA}}

This section is the acceptance-contract consequence of Gate PASS.

## 9. Current State Control Sheet promotion

- Eligible: YES only if final Status=PASS
- Sections to update: {{SECTIONS_OR_NONE}}
- Promotion basis: this Gate Decision + referenced Test Item evidence

## 10. Failure remediation input

Complete only when Status=FAIL.

- Failure facts: {{FAILURE_FACTS_OR_NA}}
- Suggested 08 scope: {{REMEDIATION_SCOPE_OR_NA}}
- Acceptance Criteria remain unchanged: YES
- Next Trial required: YES
- Rxx decomposition candidate: {{YES_NO_NA}}

## 11. Blocker record

Complete only when Status=BLOCKED.

- Blocker class: prerequisite / environment / candidate identity / contract ambiguity / unsafe operation / other
- Facts: {{BLOCKER_FACTS_OR_NA}}
- Required owner/action: {{OWNER_ACTION_OR_NA}}
- Trial identity handling: SAME_TRIAL / NEW_TRIAL_BY_EXPLICIT_DECISION / UNDECIDED

## 12. Final rationale
{{FINAL_RATIONALE}}
