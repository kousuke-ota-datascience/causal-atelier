# ENH-E7 Operator Workflows

**Purpose:** Human-controlled orchestration and Agent context isolation.

## Design priority

Workflowの目的はworkflow protocol自体の厳密性ではなく、Coding Agentが必要十分なcontextで迷わず実装し、Gate単位で意味のある品質確認を行えることにある。

このinstanceでは以下を優先する。

- Derived State over Declared State
- Semantic Validation over String Validation
- FAIL / WARN / INFO separation
- Work Packageはbounded implementation + focused self-check
- Gateが正式なquality assurance boundary
- non-essential metadata/status mismatchだけでは正常作業を停止しない

## Mandatory execution rule

Never direct an Agent to the shared repository template path.

Use only Enhancement-specific prompts under:

`docs/wiki/develop_memo/_work/20260813_ENH-E7_project_analysis_workspace_separation/40_operator_workflows/agent_entry_prompts/`

## Coding Agent context

```text
instantiated operator prompt
    +
assigned Pxx
    +
source/tests/config/migrations as implementation substrate
```

Gate 06/07/P00/other Pxx/00/20/30 are not normative Coding Agent read dependencies.

## Package execution eligibility

Preflightはexecution readinessを実状態から導出する。

Hard Fail対象は、誤対象・未依存・必須入力不足など、安全な実装開始を妨げるものに限定する。

`READY_TO_EXECUTE` 等のdeclared status、remote alias差異、説明用placeholder、optional metadata等は、それ単独ではHard Failにしない。

## Independent Test context

Test Agent receives the Gate verification contract, Fixed Trial Candidate identity and factual observation targets. It does not receive Coding Agent Pxx as acceptance authority.

## Preflight result semantics

- `FAIL`: 作業継続が誤実装・誤対象・未依存実行につながり得る。BLOCKED。
- `WARN`: 診断上確認価値はあるが、それ単独ではBLOCKしない。
- `INFO`: 追跡用情報。
