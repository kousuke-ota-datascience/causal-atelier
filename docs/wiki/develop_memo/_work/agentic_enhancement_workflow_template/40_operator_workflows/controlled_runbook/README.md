# Controlled Runbook Workflow

## Purpose

Destructive / irreversible / infrastructure-sensitive operationをHuman-controlled sequential executionで行う。

## Pattern

```text
NN_step_prompt.md
  ↓ Agent executes exactly bounded action
NN_step_result.md
  ↓ Human reviews
next NN prompt or stop
...
99_completion_summary_decision_record.md
```

## Rules

- previous resultを確認してからnext stepを確定する。
- step promptにはexact command、precondition、expected result、abort conditionを固定する。
- Agentに「必要なら他も直す」等の広い裁量を与えない。
- step resultは実行事実を記録し、成功を推測しない。
- 最終summaryは実施範囲、残余risk、next allowed actionを固定する。
