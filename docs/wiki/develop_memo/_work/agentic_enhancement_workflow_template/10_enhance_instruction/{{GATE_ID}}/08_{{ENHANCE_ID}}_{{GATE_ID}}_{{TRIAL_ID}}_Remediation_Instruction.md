# {{ENHANCE_ID}} {{GATE_ID}} Trial {{TRIAL_ID}} Remediation Instruction

- Gate: {{GATE_ID}}
- Retry Trial: {{TRIAL_ID}}
- Failed Trial: {{PREVIOUS_TRIAL_ID}}
- Failed Gate Decision: {{FAILED_GATE_DECISION_PATH}}
- Base 06 contract: {{PATH_06}}
- Base 07 contract: {{PATH_07}}

## 1. Contract invariant

06 / 07のsemantic contractとAcceptance Criteriaは変更しない。
本書はfailed evidenceに対する**delta remediation contract**である。

## 2. Failure facts

{{FAILURE_FACTS}}

観測事実と推論を分離する。

## 3. Required correction delta

{{REQUIRED_CORRECTION}}

## 4. Allowed change boundary for this remediation

{{ALLOWED_CHANGES}}

## 5. Explicit non-solutions

- AC緩和
- failing test削除
- skip / xfail追加だけによる回避
- assertion弱体化
- unrelated refactor
- next Gate先行実装
- architecture再定義（approved amendmentなし）

追加禁止事項:
{{PROJECT_SPECIFIC_NON_SOLUTIONS}}

## 6. Protected passed-Gate obligations

{{REGRESSION_OBLIGATIONS}}

## 7. Transition Debt constraints

{{TD_CONSTRAINTS_OR_NONE}}

## 8. Required self-check / handoff

{{REQUIRED_SELF_CHECK}}

Completion report must reference this remediation instruction.

## 9. Stop condition

- `READY_FOR_TEST`
- `BLOCKED_CONTRACT_AMBIGUITY`
- `BLOCKED_PREREQUISITE`
