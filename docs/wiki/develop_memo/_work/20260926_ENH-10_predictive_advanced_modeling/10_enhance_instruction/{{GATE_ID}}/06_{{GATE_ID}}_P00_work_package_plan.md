# {{ENHANCE_ID}} {{GATE_ID}} P00 Work Package Plan

**Document class:** Planning / Operator Artifact  
**Self-containment:** MUST for orchestration — package分解・dependency・checkpoint・Candidate Assemblyの規則を本書内に保持する。

- Gate: {{GATE_ID}}
- Trial applicability: {{TRIAL_SCOPE}}
- Parent 06 (traceability): {{PATH_06}}
- Parent 07 (traceability): {{PATH_07}}
- Plan status: FROZEN_FOR_TRIAL / SUPERSEDED
- P00 is an execution control document; **P00 is not an implementation Work Package**.

## 1. Why Work Package Mode is required
{{DECOMPOSITION_REASON}}

Gate scopeは保持し、Agent execution scopeだけを分割する。

## 2. Effective Gate semantic boundary for decomposition

- Gate acceptance claim: {{GATE_ACCEPTANCE_CLAIM}}
- Downstream usable result after PASS: {{DOWNSTREAM_RESULT}}
- Constraints that all packages must preserve: {{GATE_WIDE_CONSTRAINTS}}

P00を理解するためにParent 06 / 07の本文を必須参照させない。Parent pathsはtraceabilityである。

## 3. Package map

| Package | Purpose | Depends on | Entry criterion | Exit criterion | Focused verification |
|---|---|---|---|---|---|
| P01 | {{PURPOSE}} | NONE | {{ENTRY}} | {{EXIT}} | {{VERIFY}} |
| P02 | {{PURPOSE}} | P01 | {{ENTRY}} | {{EXIT}} | {{VERIFY}} |

## 4. Execution DAG
```text
{{PACKAGE_DAG}}
```

## 5. Shared package rules

すべてのPxxは次を守る。

- assigned package scope外へ拡張しない。
- protected Gate / Transition Debt scope guardを破らない。
- package completionをGate PASSと表現しない。
- dependency未成立なら実装を推測で先行しない。
- Pxx instruction自体に、そのpackage実行に必要なeffective constraintsを再掲する。

## 6. Package completion semantics

`PACKAGE_COMPLETE` means:

- assigned scope implemented
- focused verification completed
- checkpoint SHA fixed
- checkpoint report written

It does **not** mean Gate PASS / verified state promotion / downstream unlock / Fixed Trial Candidate ready。

## 7. Interruption / restart rule

以下は同Trialのまま扱う。

- Agent interruption
- self-check failure
- package restart
- same-package correction
- report correction

formal Trial FAILはIndependent Verificationの999 Gate Decisionによって成立する。

## 8. Checkpoint policy

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

## 9. Candidate Assembly

- Owner package / step: {{CANDIDATE_ASSEMBLY_PACKAGE_OR_STEP}}
- Required package set: {{REQUIRED_PACKAGE_SET}}
- Gate-wide regression: {{REGRESSION_PLAN}}
- Candidate completeness audit: {{COMPLETENESS_AUDIT}}
- Fixed Candidate rule: {{FIXED_CANDIDATE_RULE}}

## 10. Trial completion condition

All required packages complete + Candidate Assembly complete + Fixed Trial Candidate SHA fixed + Completion Report created -> `READY_FOR_TEST`.

## 11. Remediation rule

formal FAIL後のnext Trialではoriginal PxxをFAIL修正用identityとして再利用しない。必要なら`R01-R99` remediation packageを作る。
