# {{ENHANCE_ID}} {{GATE_ID}} Trial {{TRIAL_ID}} Implementation Completion Report

- Project: {{PROJECT_NAME}}
- Enhancement: {{ENHANCE_ID}}
- Gate: {{GATE_ID}}
- Trial: {{TRIAL_ID}}
- Status: READY_FOR_TEST / BLOCKED
- Starting commit: {{STARTING_COMMIT_FULL_SHA}}
- Implementation commit: {{IMPLEMENTATION_COMMIT_FULL_SHA_OR_NONE}}
- Report commit: {{REPORT_COMMIT_FULL_SHA_OR_PENDING}}
- 06 Contract: {{PATH_06}}
- Applicable 08 Remediation: {{PATH_OR_NONE}}
- Timestamp: {{TIMESTAMP_ISO8601_TZ}}

## 1. Implementation summary

{{SUMMARY}}

## 2. Changed files

| Path | Change | Reason |
|---|---|---|
| {{PATH}} | add / modify / delete | {{REASON}} |

## 3. Observable implementation facts

{{FACTS}}

## 4. Schema / migration / API / runtime impact

{{IMPACT_OR_NA}}

## 5. Protected passed-Gate impact

| Passed Gate | Touched? | Preserved semantic | Self-check / evidence |
|---|---|---|---|
| {{GATE_OR_NONE}} | YES / NO | {{SEMANTIC}} | {{EVIDENCE}} |

## 6. Transition Debt impact

| TD ID | Action | Implementation fact |
|---|---|---|
| {{TD_ID_OR_NONE}} | introduced / preserved / closed / NONE | {{FACT}} |

## 7. Coding Agent self-checks

| Command | Exit code | Result summary |
|---|---:|---|
| `{{COMMAND}}` | {{EXIT_CODE}} | {{SUMMARY}} |

These are not Gate acceptance evidence.

## 8. Known limitations / unresolved observations

{{LIMITATIONS_OR_NONE}}

## 9. Handoff to Test Agent

- Tested candidate commit: {{IMPLEMENTATION_COMMIT_FULL_SHA}}
- Required completion report path: this file
- Expected next action: independent verification under 07

## 10. Fact / interpretation separation

### Facts
{{FACTS_RECAP}}

### Interpretation
{{INTERPRETATION_OR_NONE}}
