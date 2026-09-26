# {{ENHANCE_ID}} {{GATE_ID}} Trial {{TRIAL_NO}} {{PACKAGE_ID}} Implementation Checkpoint Report

> **Document class:** Evidence Artifact  
> **Self-containment:** MUST for own responsibility.


> **Evidence self-containment**: このreportだけでstatus・実施内容・observed facts・判断理由を理解できるよう記載する。external path / SHA / logはevidenceとして参照してよいが、reportの結論を参照先へ委譲しない。


- Project: {{PROJECT_NAME}}
- Enhancement: {{ENHANCE_ID}}
- Gate: {{GATE_ID}}
- Trial: {{TRIAL_NO}}
- Package: {{PACKAGE_ID}}
- Package status: PACKAGE_COMPLETE / PACKAGE_BLOCKED
- Instruction: {{PACKAGE_INSTRUCTION_PATH}}
- Starting commit: {{STARTING_COMMIT_FULL_SHA}}
- Implementation checkpoint SHA: {{CHECKPOINT_FULL_SHA_OR_NONE}}
- Report commit SHA: {{REPORT_COMMIT_FULL_SHA_OR_PENDING}}
- Timestamp: {{TIMESTAMP_ISO8601_TZ}}

## 1. Package objective
{{OBJECTIVE}}

## 2. Implementation summary
{{SUMMARY}}

## 3. Changed files
| Path | Change | Reason |
|---|---|---|
| {{PATH}} | add / modify / delete | {{REASON}} |

## 4. Observable implementation facts
{{FACTS}}

## 5. Focused verification
| Command | Exit code | Result summary |
|---|---:|---|
| `{{COMMAND}}` | {{EXIT_CODE}} | {{SUMMARY}} |

## 6. Dependency / handoff state
- Dependencies satisfied: {{YES_NO}}
- Next package(s): {{NEXT_PACKAGE_OR_NONE}}
- Handoff facts: {{HANDOFF}}

## 7. Protected contract / Transition Debt impact
{{PROTECTED_TD_FACTS_OR_NONE}}

## 8. Known limitations / unresolved observations
{{LIMITATIONS_OR_NONE}}

## 9. Semantic warning

This checkpoint proves only package-local Coding evidence.
It does not establish Fixed Trial Candidate or Gate PASS.
