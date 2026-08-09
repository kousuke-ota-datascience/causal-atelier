# {{ENHANCE_ID}} {{GATE_ID}} Gate Contract Amendment

- Gate: {{GATE_ID}}
- Amendment ID: {{AMENDMENT_ID}}
- Original 06: {{PATH_06}}
- Original 07: {{PATH_07}}
- Triggering evidence: {{EVIDENCE_PATH}}
- Decision authority: {{HUMAN_OR_ARCHITECTURE_OWNER}}
- Decision timestamp: {{TIMESTAMP_ISO8601_TZ}}

## 1. Why remediation is insufficient

{{WHY_CONTRACT_ITSELF_IS_WRONG}}

This section MUST demonstrate that the problem is in the Gate contract itself, not merely in the implementation.

## 2. Contract defect

{{CONTRACT_DEFECT}}

## 3. Approved amendment

### 3.1. 06 semantic amendment
{{CODING_CONTRACT_AMENDMENT_OR_NONE}}

### 3.2. 07 Acceptance / verification amendment
{{VERIFICATION_CONTRACT_AMENDMENT_OR_NONE}}

## 4. Impact analysis

- Previous Trials invalidated: {{TRIALS_OR_NONE}}
- Passed previous Gates affected: {{GATES_OR_NONE}}
- Requirement/design documents requiring revision: {{PATHS_OR_NONE}}
- Transition Debt impact: {{TD_IMPACT_OR_NONE}}

## 5. Regression obligations

{{REGRESSION_OBLIGATIONS}}

## 6. Re-baseline decision

- New contract effective from Trial: {{TRIAL_ID}}
- Required regenerated 06/07 paths: {{NEW_CONTRACT_PATHS}}
- Old 06/07 retained as historical evidence: YES

## 7. Approval

- Status: APPROVED / REJECTED / CONDITIONAL
- Rationale: {{RATIONALE}}

A rejected or unapproved amendment MUST NOT alter Acceptance Criteria.
