# {{ENHANCE_ID}} {{GATE_ID}} Trial {{TRIAL_NO}} Test Item {{TEST_ITEM_ID}} — {{TEST_NAME}}

- Project: {{PROJECT_NAME}}
- Enhancement: {{ENHANCE_ID}}
- Gate: {{GATE_ID}}
- Trial: {{TRIAL_NO}}
- Test Item: {{TEST_ITEM_ID}}
- Status: PASS / FAIL / BLOCKED / NOT_RUN
- Fixed Trial Candidate SHA: {{FIXED_TRIAL_CANDIDATE_FULL_SHA}}
- Tested Repository State: {{TESTED_REPOSITORY_FULL_SHA}}
- Completion report: {{COMPLETION_REPORT_PATH}}
- 07 Contract: {{PATH_07}}
- Applicable 08: {{PATH_OR_NONE}}
- Timestamp: {{TIMESTAMP_ISO8601_TZ}}

## 1. Purpose / Acceptance mapping

- Covers AC: {{AC_IDS}}
- Candidate identity audit: YES / NO
- Protected Gate regression: {{GATE_OR_NONE}}
- Transition Debt relation: {{TD_ID_OR_NONE}}

## 2. Candidate identity evidence

- Fixed Candidate: {{FIXED_SHA}}
- Actual tested HEAD/state: {{TESTED_SHA}}
- Same SHA: YES / NO
- If NO, diff range: {{DIFF_RANGE}}
- Candidate-affecting post-change: NONE / {{DETAIL}}
- Identity conclusion: VALID / INVALID / BLOCKED

## 3. Preconditions
{{PRECONDITIONS}}

## 4. Exact command
```bash
{{EXACT_COMMAND}}
```

## 5. Exit code
`{{EXIT_CODE_OR_NA}}`

## 6. Raw relevant evidence
```text
{{RAW_RELEVANT_OUTPUT}}
```

## 7. Observed Facts
{{FACTS}}

## 8. Interpretation
{{INTERPRETATION}}

## 9. Criterion evaluation
| Criterion | Expected | Observed | Result |
|---|---|---|---|
| {{CRITERION}} | {{EXPECTED}} | {{OBSERVED}} | PASS / FAIL / BLOCKED |

## 10. Source mutation audit

- Production code changed by Test Agent: NONE / {{PATH}}
- Automated test code changed by Test Agent: NONE / {{PATH}}
- Migration changed by Test Agent: NONE / {{PATH}}
- Dependency changed by Test Agent: NONE / {{DETAIL}}

Normal PASS requires all above`NONE` unless07 explicitly defines a non-mutating generated artifact exception.

## 11. Reproduction procedure
{{REPRODUCTION_STEPS}}

## 12. Result rationale
{{RATIONALE}}
