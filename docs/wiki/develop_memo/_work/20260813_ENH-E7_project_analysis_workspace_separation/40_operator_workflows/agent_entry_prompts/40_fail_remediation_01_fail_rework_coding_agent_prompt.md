# ENH-E7 Formal FAIL Remediation Coding Agent Prompt

Use only after Independent Verification has issued a formal FAIL.

Human provides:

```text
GATE_ID=<Gxx>
TRIAL_NO=<next Trial>
REMEDIATION_PACKAGE_ID=<Rxx or N/A according to approved 08>
```

## Required inputs

- original frozen 06/07 remain immutable.
- formal FAIL evidence / 999 Gate Decision.
- concrete approved 08 remediation contract.

## Rules

- implement only the remediation contract.
- do not change Acceptance Criteria.
- do not reinterpret BLOCKED as product FAIL.
- if the Gate semantic claim itself is wrong, stop; a 09 amendment is required.
