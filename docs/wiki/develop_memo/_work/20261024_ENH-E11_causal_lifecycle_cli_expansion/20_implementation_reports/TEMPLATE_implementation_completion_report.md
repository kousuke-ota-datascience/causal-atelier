# {{ENHANCE_ID}} {{GATE_ID}} Trial {{TRIAL_NO}} Implementation Completion Report

> **Document class:** Evidence Artifact  
> **Self-containment:** MUST for own responsibility.


> **Evidence self-containment**: このreportだけでstatus・実施内容・observed facts・判断理由を理解できるよう記載する。external path / SHA / logはevidenceとして参照してよいが、reportの結論を参照先へ委譲しない。


- Project: {{PROJECT_NAME}}
- Enhancement: {{ENHANCE_ID}}
- Gate: {{GATE_ID}}
- Trial: {{TRIAL_NO}}
- Execution Mode: SINGLE_EXECUTION / WORK_PACKAGE
- Status: READY_FOR_TEST / BLOCKED
- Starting commit: {{STARTING_COMMIT_FULL_SHA}}
- Fixed Trial Candidate SHA: {{FIXED_TRIAL_CANDIDATE_FULL_SHA_OR_NONE}}
- 06 Contract: {{PATH_06}}
- P00 Plan: {{PATH_P00_OR_NA}}
- Applicable 08 Remediation: {{PATH_OR_NONE}}
- Previous Failed Candidate SHA: {{PREVIOUS_FAILED_CANDIDATE_SHA_OR_NA}}
- Completion responsibility: SINGLE_EXECUTION_CODING / WORK_PACKAGE_CANDIDATE_ASSEMBLY / FAIL_REWORK_CODING
- Timestamp: {{TIMESTAMP_ISO8601_TZ}}

## 1. Candidate summary
{{SUMMARY}}

## 2. Package checkpoint chain

For SINGLE_EXECUTION use one row with Package=`N/A`.

| Package | Status | Checkpoint SHA | Checkpoint report | Report-only SHA |
|---|---|---|---|---|
| {{PACKAGE_ID_OR_NA}} | COMPLETE / N/A | {{SHA}} | {{PATH_OR_NA}} | {{SHA_OR_NONE}} |

## 3. Candidate Assembly evidence

- Required package set complete: YES / NO / N/A
- Dependency chain complete: YES / NO / N/A
- Unresolved package blocker: NONE / {{DETAIL}}
- Integration check: {{RESULT}}
- Gate-wide regression: {{RESULT}}
- Candidate-affecting uncommitted change: NONE / {{DETAIL}}
- Fixed Candidate fixation command / method: {{METHOD}}

## 4. Fixed Trial Candidate identity

```text
{{FIXED_TRIAL_CANDIDATE_FULL_SHA}}
```

This is the candidate submitted to Independent Verification. Evidence-only commits created after this report must not replace this identity.
Package checkpoint SHA must not substitute for this field.

## 5. Changed files / candidate semantics
{{CHANGED_FILES_AND_SEMANTICS}}

## 6. Protected passed-Gate impact
| Passed Gate | Preserved semantic | Coding-side regression evidence |
|---|---|---|
| {{GATE_OR_NONE}} | {{SEMANTIC}} | {{EVIDENCE}} |

## 7. Transition Debt impact
| TD ID | Action | Fact |
|---|---|---|
| {{TD_ID_OR_NONE}} | introduce / preserve / close / NONE | {{FACT}} |

## 8. Coding-side self-checks
| Command | Exit code | Result |
|---|---:|---|
| `{{COMMAND}}` | {{EXIT}} | {{RESULT}} |

These are not Gate acceptance evidence.

## 9. Post-candidate changes

- Changes after Fixed Candidate: NONE / DOCUMENTATION_ONLY / CANDIDATE_AFFECTING
- If not NONE: {{DIFF_DESCRIPTION}}
- Candidate semantics unchanged: YES / NO / UNKNOWN

If candidate-affecting change exists, READY_FOR_TEST must not be claimed until candidate is re-fixed.

## 10. Handoff to Test / Audit Agent

- Fixed Trial Candidate SHA: {{FIXED_TRIAL_CANDIDATE_FULL_SHA}}
- Completion report: this file
- Expected next action: candidate identity audit then independent verification under 07

## 11. Facts / Interpretation

### Facts
{{FACTS}}

### Interpretation
{{INTERPRETATION}}

## 12. Evidence commit identity

`EVIDENCE_COMMIT_SHA`はこのreportをcommitした後に得られるruntime-derived valueであるため、本report本文の事前必須値としない。Agent terminal handoffで報告し、必要なら後続traceability artifactへ記録する。架空SHAを予約しない。
