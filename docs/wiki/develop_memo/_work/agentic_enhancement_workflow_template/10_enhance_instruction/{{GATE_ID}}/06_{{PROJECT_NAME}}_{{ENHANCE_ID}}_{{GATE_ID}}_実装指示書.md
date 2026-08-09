# {{PROJECT_NAME}} {{ENHANCE_ID}} {{GATE_ID}} 実装指示書

- Project: {{PROJECT_NAME}}
- Enhancement: {{ENHANCE_ID}}
- Branch: {{BRANCH}}
- Baseline commit: {{BASELINE_COMMIT_FULL_SHA}}
- Active Gate: {{GATE_ID}}
- Initial Trial: {{TRIAL_ID}}
- Migration head: {{MIGRATION_HEAD_OR_NA}}
- Current State Control Sheet: {{CONTROL_SHEET_PATH}}

## 1. Source of Truth and precedence

1. 本書 = Active Gate Coding Contract。
2. applicable 08 = current Trialのcorrection deltaのみ。
3. final PASS previous Gate Decision = established previous contract evidence。
4. Current State Control Sheet = verified-state index。
5. current source/test/migration = observable implementation facts。

本書の意味論と上位承認contractに矛盾がある場合、推測で解決せず停止する。

## 2. Coding Agent role

- Active Gateのproduction codeを実装する。
- Active Gateに必要なautomated test codeを作成・修正する。
- 必要なmigrationを作成する。
- implementation commitを作成する。
- completion report / Gate-local detailを作成・更新する。
- `READY_FOR_TEST`で停止する。

## 3. Prohibited work

- Gate判定
- Acceptance Criteria変更
- independent auditの代替
- PASS済みGateの無断再設計
- next Gateへの先行着手
- scope外refactor
- assertion緩和 / failing test削除 / skip / xfail追加だけによる回避
- destructive environment operation（明示runbookがない限り）
- `git add .` 等で無関係変更を混入

## 4. Verified current state

{{VERIFIED_CURRENT_STATE_SUMMARY}}

## 5. Protected passed-Gate contracts

| Gate | Protected semantic / invariant | Evidence | Mandatory regression |
|---|---|---|---|
| {{PREVIOUS_GATE_OR_NONE}} | {{PROTECTED_SEMANTIC}} | {{DECISION_PATH}} | {{REGRESSION_REQUIREMENT}} |

If none: `NONE`.

## 6. Active Gate objective

{{GATE_OBJECTIVE}}

## 7. Implementation scope

### 7.1 In scope
{{IN_SCOPE}}

### 7.2 Out of scope
{{OUT_OF_SCOPE}}

### 7.3 Allowed change boundary
{{ALLOWED_PATHS_OR_COMPONENTS}}

### 7.4 Prohibited change boundary
{{PROHIBITED_PATHS_OR_COMPONENTS}}

## 8. Gate implementation contract

{{IMPLEMENTATION_CONTRACT}}

MUST express observable semantics, ownership/authority, schema/API/runtime invariants as applicable.

## 9. Transition Debt

| ID | Action this Gate | Temporary authority / exception | Scope guard | Exit Gate / criterion |
|---|---|---|---|---|
| {{TD_ID_OR_NONE}} | introduce / preserve / close / NONE | {{DETAIL}} | {{SCOPE_GUARD}} | {{EXIT}} |

## 10. Required self-checks

Coding Agent self-checkはimplementation confidenceのためでありGate PASS evidenceではない。

{{REQUIRED_SELF_CHECKS}}

## 11. Required outputs

- Implementation commit full SHA
- `20_implementation_reports/{{GATE_ID}}/{{ENHANCE_ID}}_{{GATE_ID}}_{{TRIAL_ID}}_implementation_completion_report.md`
- `20_implementation_reports/{{GATE_ID}}/{{ENHANCE_ID}}_{{GATE_ID}}_implementation_report_detail.md`
- changed file list
- migration/schema impact if applicable
- Transition Debt impact

## 12. Completion condition

{{COMPLETION_CONDITION}}

## 13. Stop condition

以下のいずれかで停止する。

- `READY_FOR_TEST`
- `BLOCKED_CONTRACT_AMBIGUITY`
- `BLOCKED_PREREQUISITE`
- `BLOCKED_UNSAFE_OPERATION`

Coding AgentはGate PASSを宣言しない。
