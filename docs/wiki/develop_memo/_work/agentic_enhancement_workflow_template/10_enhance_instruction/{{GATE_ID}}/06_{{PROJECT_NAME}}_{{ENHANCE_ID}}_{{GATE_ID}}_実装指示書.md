# {{PROJECT_NAME}} {{ENHANCE_ID}} {{GATE_ID}} 実装指示書 — Gate Coding Contract

- Project: {{PROJECT_NAME}}
- Enhancement: {{ENHANCE_ID}}
- Active Gate: {{GATE_ID}}
- Branch: {{BRANCH}}
- Baseline: {{BASELINE_FULL_SHA}}
- Contract status: FROZEN
- Execution Mode: SINGLE_EXECUTION / WORK_PACKAGE
- Current State Control Sheet: {{CONTROL_SHEET_PATH}}

## 1. Gate definition / acceptance claim

### Gate objective

{{GATE_OBJECTIVE}}

### Contract claim established by PASS

このGateがfinal PASSしたとき、後続工程は以下を成立済みcontractとして依存してよい。

{{DOWNSTREAM_USABLE_RESULT_AFTER_PASS}}

### Why this is one Gate

{{WHY_THIS_IS_ONE_ACCEPTANCE_BOUNDARY}}

実装難易度やAgent execution sizeをGate境界理由として使用しない。

## 2. Execution Mode decision

- Selected: SINGLE_EXECUTION / WORK_PACKAGE
- Reason: {{EXECUTION_MODE_REASON}}
- P00 Plan: {{P00_PATH_OR_NA}}

Work Package ModeであってもGate semantic contractは分割されない。

## 3. Required implementation semantics

{{REQUIRED_IMPLEMENTATION_SEMANTICS}}

## 4. Allowed scope

{{ALLOWED_SCOPE}}

## 5. Explicitly prohibited scope

{{PROHIBITED_SCOPE}}

## 6. Protected passed-Gate contracts

| Gate | Protected semantic | Allowed interaction | Mandatory regression |
|---|---|---|---|
| {{PREVIOUS_GATE_OR_NONE}} | {{SEMANTIC}} | {{INTERACTION}} | {{REGRESSION}} |

## 7. Transition Debt

| TD ID | Required action in this Gate | Exit criterion / scope guard |
|---|---|---|
| {{TD_ID_OR_NONE}} | introduce / preserve / close / NONE | {{CRITERION}} |

## 8. Schema / migration / API / runtime policy

{{POLICY_OR_NA}}

## 9. Automated test obligations

{{TEST_OBLIGATIONS}}

## 10. Candidate Assembly requirement

Before READY_FOR_TEST:

- all required execution units complete
- integration / Gate-wide self-check complete
- protected passed-Gate coding-side regression complete
- unresolved candidate-affecting change = NONE
- Fixed Trial Candidate SHA fixed
- Implementation Completion Report created

Package checkpoint aloneをFixed Trial Candidateと扱わない。

## 11. Coding Agent prohibited work

- Gate Decision
- Acceptance Criteria変更
- 07変更によるtest回避
- passed-Gate semanticの無断変更
- next Gate先行実装
- package scope外の便乗変更

## 12. Required outputs

### SINGLE_EXECUTION

- implementation status report
- implementation completion report
- Gate-local implementation detail update

### WORK_PACKAGE

各package:

- package execution status report
- implementation checkpoint report
- checkpoint SHA

Trial completion時:

- Fixed Trial Candidate SHA
- implementation completion report
- Gate-local implementation detail update

## 13. Stop condition

Coding sideは`READY_FOR_TEST`または明示的`BLOCKED_*`で停止する。Gate PASSを宣言しない。
