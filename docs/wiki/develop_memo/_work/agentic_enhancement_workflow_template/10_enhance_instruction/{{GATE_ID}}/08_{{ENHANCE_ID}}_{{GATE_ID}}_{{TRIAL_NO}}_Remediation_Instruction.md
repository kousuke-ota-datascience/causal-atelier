# {{ENHANCE_ID}} {{GATE_ID}} Trial {{TRIAL_NO}} Remediation Contract

**Document class:** Derived Contract  
**Self-containment:** CONDITIONAL — `DELTA` / `CONSOLIDATED`をFAIL evidence確定後に選択する。

- Gate: {{GATE_ID}}
- New Trial: {{TRIAL_NO}}
- Failed Trial: {{FAILED_TRIAL_ID}}
- Failed Gate Decision: {{FAILED_GATE_DECISION_PATH}}
- Original 06: {{PATH_06}}
- Original 07: {{PATH_07}}
- Remediation Mode: DELTA / CONSOLIDATED
- Execution Mode: SINGLE_EXECUTION / WORK_PACKAGE

## 1. Contract validity check / existence condition

- Original Gate semantic claim remains valid: YES / NO
- Original Acceptance Criteria remain valid: YES / NO
- If either is NO: STOP. This document must not silently redefine the Gate contract; create a Gate Contract Amendment instead.

## 2. Mode selection rationale

- Selected mode: DELTA / CONSOLIDATED
- Why this mode minimizes sufficient effective context: {{MODE_RATIONALE}}
- Required external contract context if DELTA: {{REQUIRED_PARENT_SECTIONS_OR_NA}}

## 3. Verified failure facts
{{FAILURE_FACTS}}

Factsとinterpretationを混同せず、failed 999 / Test Item evidenceへのpathを併記する。

## 4A. DELTA mode — fill only when selected

### Required parent contract references

| Contract | Required section / meaning | Why required |
|---|---|---|
| 06 | {{SECTION}} | {{REASON}} |
| 07 | {{SECTION}} | {{REASON}} |

### Required correction delta
{{REQUIRED_CORRECTION_DELTA}}

### Additional / changed re-verification procedure
{{REVERIFICATION_DELTA}}

DELTA modeでは、上記に列挙したparent contextと本書を合わせてnext Trialのeffective contextとする。必要以上のparent document全量を読ませない。

## 4B. CONSOLIDATED mode — fill only when selected

### Effective implementation semantics for next Trial
{{CONSOLIDATED_IMPLEMENTATION_CONTRACT}}

### Allowed / prohibited remediation scope
{{CONSOLIDATED_SCOPE_AND_PROHIBITIONS}}

### Protected passed-Gate / Transition Debt constraints
{{CONSOLIDATED_PROTECTED_AND_TD}}

### Effective verification requirements
{{CONSOLIDATED_VERIFICATION_REQUIREMENTS}}

### Completion / handoff condition
{{CONSOLIDATED_COMPLETION_CONDITION}}

CONSOLIDATED modeでは、next Trialを実行するためのnormative remediation contextを本書内へ統合する。Original 06 / 07 pathはhistorical traceabilityとして保持する。

## 5. Explicitly forbidden workaround
{{FORBIDDEN_WORKAROUND}}

## 6. Acceptance Criteria invariance

- 07 silently rewritten: NO
- Acceptance Criteria relaxed: NO
- Gate semantic claim changed by this 08: NO

## 7. Remediation decomposition

- Remediation packages required: YES / NO
- If YES: use `R01-R99`, not original `Pxx` identities.
- Rxx paths: {{REMEDIATION_PACKAGE_PATHS_OR_NA}}
- Each Rxx must be a self-contained Primary Execution Contract for its assigned package.

## 8. Next Trial candidate rule

A new Fixed Trial Candidate SHA must be generated and independently verified. Failed candidate / failed Test evidence must remain immutable historical evidence.
