# {{PROJECT_NAME}} {{ENHANCE_ID}} {{GATE_ID}} テスト指示書

- Project: {{PROJECT_NAME}}
- Enhancement: {{ENHANCE_ID}}
- Active Gate: {{GATE_ID}}
- Verification contract status: FROZEN
- Current State Control Sheet: {{CONTROL_SHEET_PATH}}

## 1. Test Agent authority and precedence

1. **本書 07 = Acceptance Criteria authority**。
2. 06 = implementation intent / allowed scope reference。07をoverrideできない。
3. applicable 08 = retry failure correction context。Acceptance Criteriaをoverrideできない。
4. final PASS previous Gate Decision = established previous contract evidence。
5. Current State Control Sheet = verified-state index。上位contractをoverrideできない。
6. implementation completion report = tested implementation commit authority。
7. current source/test/migration = observable facts。

矛盾がGate判定に影響する場合は`BLOCKED`とし、勝手にcriteriaを再解釈しない。

## 2. Required verification input

- Implementation completion report: {{COMPLETION_REPORT_PATH_TO_BE_SPECIFIED_AT_EXECUTION}}
- Tested implementation commit: report内full SHAを使用し、checkout stateを確認する。
- Applicable remediation: {{REMEDIATION_PATH_OR_NONE}}

## 3. Test Agent prohibited work

- production code modification
- automated test code modification
- migration modification
- dependency modification
- Acceptance Criteria modification
- implementation repair

Test Agentが対象sourceを変更した場合、そのtrialを通常PASS evidenceとして扱わない。

## 4. Gate objective

{{GATE_OBJECTIVE}}

## 5. Acceptance Criteria

| AC ID | Criterion | Required evidence | Severity |
|---|---|---|---|
| AC-{{N}} | {{CRITERION}} | {{EVIDENCE}} | MUST / SHOULD |

## 6. Test item plan

| Test Item ID | Name | Covers AC | Method |
|---|---|---|---|
| 001 | {{NAME}} | {{AC_IDS}} | {{METHOD}} |

Test Item IDs: `001-998`; `999` is Gate Decision reserved.

## 7. Protected passed-Gate regression

| Previous Gate | Protected semantic | Regression Test Item | Required result |
|---|---|---|---|
| {{GATE_OR_NONE}} | {{SEMANTIC}} | {{ITEM_ID}} | PASS |

## 8. Transition Debt audit

| TD ID | Expected state after this Gate | Scope/exit criterion to verify | Test Item |
|---|---|---|---|
| {{TD_ID_OR_NONE}} | OPEN / CLOSED / NONE | {{CRITERION}} | {{ITEM_ID_OR_NA}} |

## 9. Environment / prerequisite handling

- prerequisiteが未成立でtest不能 -> 原則`BLOCKED`。
- product implementation defect -> `FAIL`。
- Test Agentは環境を勝手に破壊的再初期化しない。
- 必要なら`40_operator_workflows/preflight`または`controlled_runbook`へ戻す。

## 10. Evidence requirements

各Test Item Reportに最低限以下を記録する。

- tested commit full SHA
- exact command
- exit code
- relevant raw output
- observed facts
- interpretation separately
- AC mapping
- protected Gate / TD relation
- reproduction steps

## 11. Gate decision semantics

### PASS
全MUST ACが必要evidence付きで成立し、required regressionがPASSし、blocking TD violationがない。

### FAIL
test実行可能であり、product / implementationがMUST ACまたはprotected contractを満たさない。

### BLOCKED
environment / prerequisite / contract ambiguity等で妥当なproduct判定ができない。

## 12. Required outputs

- `30_test_report/{{GATE_ID}}/{{ENHANCE_ID}}_{{GATE_ID}}_{{TRIAL_ID}}_{{ITEM_ID}}_*.md`
- `30_test_report/{{GATE_ID}}/{{ENHANCE_ID}}_{{GATE_ID}}_{{TRIAL_ID}}_999_gate_decision.md`
- PASS / FAIL / BLOCKED後に停止
