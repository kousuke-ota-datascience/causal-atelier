# FAIL Rework Coding Agent Entry Prompt

同一Gateのretry Trialを実施してください。

- Immutable 06 Gate Coding Contract: `{{PATH_06}}`
- Immutable 07 Gate Verification Contract: `{{PATH_07}}`
- Failed Gate Decision: `{{FAILED_GATE_DECISION_PATH}}`
- Current Trial Remediation 08: `{{PATH_08}}`
- Current State Control Sheet: `{{CONTROL_SHEET_PATH}}`

08はFAIL evidenceに対するdelta remediationです。06/07の意味論、Acceptance Criteria、protected passed-Gate contractを変更しないでください。

修正後、新しいimplementation commitと新Trialのcompletion reportを作成し、Gate-local implementation detailへTrial履歴を追記してください。

Gate判定せず`READY_FOR_TEST`で停止してください。
