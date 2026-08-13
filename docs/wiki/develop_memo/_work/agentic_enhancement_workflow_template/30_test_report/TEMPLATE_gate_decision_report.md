# {{ENHANCE_ID}} {{GATE_ID}} Trial {{TRIAL_NO}} Gate Decision

> **Document class:** Decision / Evidence Artifact  
> **Self-containment:** MUST for own responsibility.


> **Evidence self-containment**: このartifactだけでtest/decisionの対象・observed facts・criterion evaluation・rationaleを理解できるよう記載する。external Test Item / log / source / report pathはevidence参照として利用してよい。


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
- Previous Failed Candidate SHA (remediation Trial only): {{PREVIOUS_FAILED_CANDIDATE_SHA_OR_NA}}
- New candidate differs from previous failed candidate: YES / NO / N/A
- Evidence: {{PATHS}}

Remediation Trialでnew candidateがprevious failed candidateと同一、またはrequired semantic remediation diffを確認できない場合は、Acceptance Criteria実行前に`BLOCKED_CANDIDATE_IDENTITY`または`BLOCKED_REMEDIATION_NOT_APPLIED`として停止する。

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

### Browser E2E diagnostic summary — conditional

| Test Item | Failure classification | Product judgment possible | Key evidence |
|---|---|---|---|
| {{ITEM_ID_OR_NA}} | PRODUCT_INTEGRATION_DEFECT / TEST_IMPLEMENTATION_DEFECT / TEST_ORCHESTRATION_DEFECT / TEST_ENVIRONMENT_DEFECT / UNKNOWN / N/A | YES / NO / N/A | {{PATHS_OR_NA}} |

Test implementation / orchestration / environment defectまたはUNKNOWNによりproduct correctnessを判定できない場合、そのBrowser E2E failureだけを根拠にGate FAILとしない。

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
- Browser E2E failure classification (if applicable): {{CLASSIFICATION_OR_NA}}
- Verified failure facts summary: {{FAILURE_FACTS_OR_NA}}
- Original Gate semantic claim appears valid: YES / NO / UNDECIDED
- Original Acceptance Criteria appear valid: YES / NO / UNDECIDED
- Remediation scope candidate: {{REMEDIATION_SCOPE_OR_NA}}
- 08 mode recommendation: DELTA / CONSOLIDATED / UNDECIDED
- Rxx decomposition candidate: {{YES_NO_NA}}

The Gate Decision records failure evidence. Final 08 mode selection is performed after failure analysis; if the Gate contract itself is invalid, use an explicit amendment instead.

## 11. Blocker record

Complete only when Status=BLOCKED.

- Blocker class: prerequisite / environment / test implementation / test orchestration / candidate identity / contract ambiguity / unsafe operation / other
- Browser E2E failure classification (if applicable): {{CLASSIFICATION_OR_NA}}
- Facts: {{BLOCKER_FACTS_OR_NA}}
- Required owner/action: {{OWNER_ACTION_OR_NA}}
- Trial identity handling: SAME_TRIAL / NEW_TRIAL_BY_EXPLICIT_DECISION / UNDECIDED

## 12. Final rationale
{{FINAL_RATIONALE}}
