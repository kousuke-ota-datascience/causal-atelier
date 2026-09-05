# {{ENHANCE_ID}} {{GATE_ID}} Preflight Result

> **Document class:** Evidence / Operator Result  
> **Self-containment:** MUST for observed prerequisite state — status / facts / eligibility rationaleを本文内に記載し、external logsはevidence参照として利用してよい。


- Status: PASS / FAIL / BLOCKED
- Timestamp: {{TIMESTAMP}}
- Branch/commit observed: {{OBSERVED_BASELINE}}

| Check ID | Command / Method | Exit | Observed fact | Result |
|---|---|---:|---|---|
| PF-001 | `{{COMMAND}}` | {{EXIT}} | {{FACT}} | PASS / FAIL / BLOCKED |

## Environment mutations
{{MUTATIONS_OR_NONE}}

## Conclusion
{{CONCLUSION}}

## Gate execution eligibility
- Eligible to proceed: YES / NO
- Reason: {{REASON}}
