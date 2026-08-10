# FAIL Rework Coding Agent 作業開始プロンプト

このpromptはIndependent Test / Auditのformal FAIL後のnext Trialにのみ使用する。

```text
PROJECT_NAME={{PROJECT_NAME}}
ENHANCE_ID={{ENHANCE_ID}}
ENHANCE_SHORT_ID={{ENHANCE_SHORT_ID}}
GATE_ID={{GATE_ID}}
FAILED_TRIAL_NO={{FAILED_TRIAL_NO}}
TRIAL_NO={{TRIAL_NO}}
WORK_DIR_NAME={{WORK_DIR_NAME}}
REMOTE_NAME={{REMOTE_NAME}}
BRANCH_NAME={{BRANCH_NAME}}
```

## Derived variables

```text
WORK_ROOT=docs/wiki/develop_memo/_work/{{WORK_DIR_NAME}}
GATE_INSTRUCTION_DIR={{WORK_ROOT}}/10_enhance_instruction/{{GATE_ID}}
PATH_06_PATTERN={{GATE_INSTRUCTION_DIR}}/06_*_{{GATE_ID}}_実装指示書.md
PATH_07_PATTERN={{GATE_INSTRUCTION_DIR}}/07_*_{{GATE_ID}}_テスト指示書.md
PATH_08_PATTERN={{GATE_INSTRUCTION_DIR}}/08_*_{{GATE_ID}}_{{TRIAL_NO}}_Remediation_Instruction.md
FAILED_GATE_DECISION={{WORK_ROOT}}/30_test_report/{{GATE_ID}}/Trial{{FAILED_TRIAL_NO}}/*_999_gate_decision.md
```

未解決placeholderがないことを確認せよ。

Inputs:

- immutable 06
- immutable 07
- failed 999 Gate Decision
- current Trial 08 Remediation
- Current State Control Sheet
- Rxx package instruction if Work Package remediation mode

08はFAIL evidenceに対するdeltaであり、06/07 Acceptance Criteriaを変更しない。

Work Package remediationの場合、original PxxをFAIL修正identityとして再利用せずR01-R99を実行する。

新しいTrial candidateを生成し、Fixed Trial Candidate SHAを新規固定する。failed candidate evidenceを上書きしない。

Gate判定せず`READY_FOR_TEST`で停止する。
