# {{ENHANCE_ID}} {{GATE_ID}} Trial {{TRIAL_ID}} Test Item {{TEST_ITEM_ID}} — {{TEST_NAME}}

- Project: {{PROJECT_NAME}}
- Enhancement: {{ENHANCE_ID}}
- Gate: {{GATE_ID}}
- Trial: {{TRIAL_ID}}
- Test Item: {{TEST_ITEM_ID}}
- Status: PASS / FAIL / BLOCKED / NOT_RUN
- Tested commit: {{TESTED_COMMIT_FULL_SHA}}
- Completion report: {{COMPLETION_REPORT_PATH}}
- 07 Contract: {{PATH_07}}
- Applicable 08: {{PATH_OR_NONE}}
- Timestamp: {{TIMESTAMP_ISO8601_TZ}}

## 1. Purpose / Acceptance mapping

- Covers AC: {{AC_IDS}}
- Protected Gate regression: {{GATE_OR_NONE}}
- Transition Debt relation: {{TD_ID_OR_NONE}}

## 2. Preconditions

{{PRECONDITIONS}}

## 3. Exact command

```bash
{{EXACT_COMMAND}}
```

## 4. Exit code

`{{EXIT_CODE_OR_NA}}`

## 5. Raw relevant evidence

```text
{{RAW_RELEVANT_OUTPUT}}
```

## 6. Observed facts

{{FACTS}}

## 7. Interpretation

{{INTERPRETATION}}

## 8. Criterion evaluation

| Criterion | Expected | Observed | Result |
|---|---|---|---|
| {{CRITERION}} | {{EXPECTED}} | {{OBSERVED}} | PASS / FAIL / BLOCKED |

## 9. Source mutation audit

- Production code changed by Test Agent: NONE / {{PATH}}
- Automated test code changed by Test Agent: NONE / {{PATH}}
- Migration changed by Test Agent: NONE / {{PATH}}
- Dependency changed by Test Agent: NONE / {{DETAIL}}

Normal PASS requires all above `NONE` unless the verification contract explicitly defines a non-mutating generated artifact exception.

## 10. Reproduction procedure

{{REPRODUCTION_STEPS}}

## 11. Result rationale

{{RATIONALE}}
