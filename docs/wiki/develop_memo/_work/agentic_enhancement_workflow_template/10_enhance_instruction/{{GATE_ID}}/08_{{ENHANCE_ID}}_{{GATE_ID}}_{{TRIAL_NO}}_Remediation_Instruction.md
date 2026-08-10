# {{ENHANCE_ID}} {{GATE_ID}} Trial {{TRIAL_NO}} Remediation Instruction

- Gate: {{GATE_ID}}
- New Trial: {{TRIAL_NO}}
- Failed Trial: {{FAILED_TRIAL_ID}}
- Failed Gate Decision: {{FAILED_GATE_DECISION_PATH}}
- Immutable 06: {{PATH_06}}
- Immutable 07: {{PATH_07}}
- Execution Mode: SINGLE_EXECUTION / WORK_PACKAGE

## 1. Failure facts

{{FAILURE_FACTS}}

## 2. Required correction delta

{{REQUIRED_CORRECTION}}

## 3. Explicitly forbidden workaround

{{FORBIDDEN_WORKAROUND}}

## 4. Acceptance Criteria invariance

- 07 changed: NO
- Acceptance Criteria relaxed: NO
- Gate semantic claim changed: NO

## 5. Remediation decomposition

- Remediation packages required: YES / NO
- If YES: use `R01-R99`, not original `Pxx` identities.
- Rxx plan / paths: {{REMEDIATION_PACKAGE_PATHS_OR_NA}}

## 6. Required re-verification

{{REVERIFICATION_REQUIREMENTS}}

## 7. Next Trial candidate rule

A new Fixed Trial Candidate SHA must be generated and independently verified. Failed candidate must not be overwritten as historical evidence.
