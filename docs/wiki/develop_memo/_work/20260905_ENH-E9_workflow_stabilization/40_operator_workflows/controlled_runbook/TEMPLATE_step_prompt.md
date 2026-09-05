# {{RUNBOOK_ID}} Step {{STEP_ID}} Prompt — {{STEP_NAME}}

**Document class:** Operator Artifact / Execution Instruction  
**Self-containment:** MUST — Agentが本promptだけでbounded actionを実行し、result artifactを作成できること。

## Objective
{{OBJECTIVE}}

## Preconditions / required observed facts
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

## Required result file
`{{STEP_ID}}_{{STEP_NAME}}_result.md`

最低限以下を記載する。

- Status: PASS / FAIL / BLOCKED
- Timestamp
- exact command executed
- exit code
- raw relevant output
- observed facts
- deviations / additional mutations
- conclusion
- next-step recommendation

result作成後に停止する。次stepを自律実行しない。Result自体はnext stepをauthorizeしない。
