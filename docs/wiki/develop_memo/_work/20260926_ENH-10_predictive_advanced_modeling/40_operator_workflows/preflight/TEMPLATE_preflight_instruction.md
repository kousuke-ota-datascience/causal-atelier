# {{ENHANCE_ID}} {{GATE_ID}} Preflight Instruction

**Document class:** Operator Artifact / Execution Instruction  
**Self-containment:** MUST — Agentが本書だけでchecksを実行し、required result artifactを作成できること。

- Purpose: {{PURPOSE}}
- Target Gate: {{GATE_ID}}
- Expected branch/commit: {{EXPECTED_BASELINE}}
- Destructive operations allowed: YES / NO
- Result file: {{RESULT_FILE_PATH}}

## Checks

| Check ID | Check | Exact command / method | Expected |
|---|---|---|---|
| PF-001 | {{CHECK}} | `{{COMMAND}}` | {{EXPECTED}} |

## Abort conditions
{{ABORT_CONDITIONS}}

## Required result schema

Result fileへ最低限以下を記載する。

- Status: PASS / FAIL / BLOCKED
- Timestamp
- observed branch / commit
- checkごとの exact command / method
- exit code
- observed fact
- PASS / FAIL / BLOCKED result
- environment mutations
- conclusion
- Gate execution eligibility: YES / NO + reason

実行事実を記録して停止する。Product codeを実装しない。
