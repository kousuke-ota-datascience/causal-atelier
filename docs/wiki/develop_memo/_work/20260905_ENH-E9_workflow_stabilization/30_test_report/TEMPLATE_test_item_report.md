# {{ENHANCE_ID}} {{GATE_ID}} Trial {{TRIAL_NO}} Test Item {{TEST_ITEM_ID}} — {{TEST_NAME}}

> **Document class:** Evidence Artifact  
> **Self-containment:** MUST for own responsibility.


> **Evidence self-containment**: このartifactだけでtest/decisionの対象・observed facts・criterion evaluation・rationaleを理解できるよう記載する。external Test Item / log / source / report pathはevidence参照として利用してよい。


- Project: {{PROJECT_NAME}}
- Enhancement: {{ENHANCE_ID}}
- Gate: {{GATE_ID}}
- Trial: {{TRIAL_NO}}
- Test Item: {{TEST_ITEM_ID}}
- Status: PASS / FAIL / BLOCKED / NOT_RUN
- Primary test layer: META / UNIT_DOMAIN / API_INTEGRATION / FRONTEND_CONTRACT / BROWSER_E2E / OTHER
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

## 6A. Browser E2E diagnostic evidence — conditional

Complete when Primary test layer = `BROWSER_E2E`.

- Canonical Browser E2E command: {{COMMAND_OR_NA}}
- Environment bootstrap / teardown authority: {{DETAIL_OR_NA}}
- Compose / service state: {{EVIDENCE_OR_NA}}
- Current-source image / build identity: {{EVIDENCE_OR_NA}}
- Semantic synchronization point: {{DETAIL_OR_NA}}
- Failed assertion / observable state: {{DETAIL_OR_NA}}
- Playwright trace: {{PATH_OR_NA}}
- Screenshot: {{PATH_OR_NA}}
- Video: {{PATH_OR_NA}}
- Browser console / page errors: {{PATH_OR_SUMMARY_OR_NA}}
- Relevant network evidence: {{PATH_OR_SUMMARY_OR_NA}}
- API logs: {{PATH_OR_NA}}
- Worker logs: {{PATH_OR_NA}}
- Failure classification: PRODUCT_INTEGRATION_DEFECT / TEST_IMPLEMENTATION_DEFECT / TEST_ORCHESTRATION_DEFECT / TEST_ENVIRONMENT_DEFECT / UNKNOWN / N/A

Network evidenceにcredential / token / secret等を保存しない。HTTP status単体ではなくactual failing assertionとの関係を記録する。

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
