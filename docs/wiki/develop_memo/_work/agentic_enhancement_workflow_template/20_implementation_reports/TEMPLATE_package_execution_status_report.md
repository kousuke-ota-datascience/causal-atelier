# {{ENHANCE_ID}} {{GATE_ID}} Trial {{TRIAL_NO}} {{PACKAGE_ID}} Execution Status

- Gate: {{GATE_ID}}
- Trial: {{TRIAL_NO}}
- Package: {{PACKAGE_ID}}
- Execution status: PACKAGE_COMPLETE / PACKAGE_IN_PROGRESS / PACKAGE_BLOCKED / INTERRUPTED
- Instruction: {{INSTRUCTION_PATH}}
- Starting SHA: {{STARTING_SHA}}
- Latest implementation SHA: {{LATEST_IMPLEMENTATION_SHA_OR_NONE}}
- Timestamp: {{TIMESTAMP_ISO8601_TZ}}

## 1. Completed work
{{COMPLETED_WORK}}

## 2. Remaining work
{{REMAINING_WORK_OR_NONE}}

## 3. Observed failures / blockers
{{FAILURES_OR_NONE}}

## 4. Verification executed
| Command / method | Exit | Result |
|---|---:|---|
| {{COMMAND}} | {{EXIT_CODE}} | {{RESULT}} |

## 5. Relevant commits
{{COMMIT_LIST}}

## 6. Next required action
{{NEXT_ACTION}}

This report is operational status, not Gate acceptance evidence.
