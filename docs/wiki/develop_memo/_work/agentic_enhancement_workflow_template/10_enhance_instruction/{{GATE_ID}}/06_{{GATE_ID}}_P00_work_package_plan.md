# {{ENHANCE_ID}} {{GATE_ID}} P00 Work Package Plan

- Gate: {{GATE_ID}}
- Trial applicability: {{TRIAL_SCOPE}}
- Parent 06: {{PATH_06}}
- Parent 07: {{PATH_07}}
- Plan status: FROZEN_FOR_TRIAL / SUPERSEDED
- P00 is an execution control document; **P00 is not an implementation Work Package**.

## 1. Why Work Package Mode is required

{{DECOMPOSITION_REASON}}

Gate scopeは保持し、Agent execution scopeだけを分割する。

## 2. Gate semantic boundary

- Gate acceptance claim: {{GATE_ACCEPTANCE_CLAIM}}
- Downstream usable result after PASS: {{DOWNSTREAM_RESULT}}

Work Package単位では上記contractを成立させない。

## 3. Package map

| Package | Purpose | Depends on | Entry criterion | Exit criterion | Focused verification |
|---|---|---|---|---|---|
| P01 | {{PURPOSE}} | NONE | {{ENTRY}} | {{EXIT}} | {{VERIFY}} |
| P02 | {{PURPOSE}} | P01 | {{ENTRY}} | {{EXIT}} | {{VERIFY}} |

## 4. Execution DAG

```text
{{PACKAGE_DAG}}
```

## 5. Package completion semantics

`PACKAGE_COMPLETE` means:

- assigned package scope implemented
- focused verification completed to package instruction requirement
- checkpoint SHA fixed
- checkpoint report written

It does **not** mean:

- Gate PASS
- verified state promotion
- downstream unlock
- Fixed Trial Candidate ready unless this package is explicitly Candidate Assembly and all prerequisites are complete

## 6. Interruption / restart rule

以下は同Trialのまま扱う。

- Agent interruption
- self-check failure
- package restart
- same-package implementation correction
- report correction

formal Trial FAILはIndependent Verificationの999 Gate Decisionによってのみ成立する。

## 7. Checkpoint policy

各packageは原則:

```text
focused implementation
  ↓
focused verification
  ↓
implementation checkpoint commit
  ↓
implementation checkpoint report
  ↓
report recording commit (if separate)
```

Implementation checkpoint SHAとreport-only commit SHAを混同しない。

## 8. Candidate Assembly

- Owner package / step: {{CANDIDATE_ASSEMBLY_PACKAGE_OR_STEP}}
- Required package set: {{REQUIRED_PACKAGE_SET}}
- Gate-wide regression: {{REGRESSION_PLAN}}
- Candidate completeness audit: {{COMPLETENESS_AUDIT}}
- Fixed Candidate rule: {{FIXED_CANDIDATE_RULE}}

## 9. Trial completion condition

All required packages complete + Candidate Assembly complete + Fixed Trial Candidate SHA fixed + Completion Report created -> `READY_FOR_TEST`.

## 10. Remediation rule

formal FAIL後のnext Trialではoriginal PxxをFAIL修正用identityとして再利用しない。必要なら`R01-R99` remediation packageを作る。
