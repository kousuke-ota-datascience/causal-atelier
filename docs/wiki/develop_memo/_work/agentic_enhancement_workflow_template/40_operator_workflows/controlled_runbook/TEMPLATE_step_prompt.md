# {{RUNBOOK_ID}} Step {{STEP_ID}} Prompt — {{STEP_NAME}}

## Objective
{{OBJECTIVE}}

## Preconditions
{{PRECONDITIONS}}

## Allowed action
以下だけを実行する。

```bash
{{EXACT_COMMAND}}
```

## Prohibited actions
{{PROHIBITED_ACTIONS}}

## Expected result
{{EXPECTED_RESULT}}

## Abort conditions
{{ABORT_CONDITIONS}}

## Required output
`{{STEP_ID}}_{{STEP_NAME}}_result.md`へ実行事実を記録して停止する。
次stepを自律的に実行しない。
