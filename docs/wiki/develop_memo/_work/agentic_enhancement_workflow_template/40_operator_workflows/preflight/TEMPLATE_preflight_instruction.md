# {{ENHANCE_ID}} {{GATE_ID}} Preflight Instruction

- Purpose: {{PURPOSE}}
- Target Gate: {{GATE_ID}}
- Expected branch/commit: {{EXPECTED_BASELINE}}
- Destructive operations allowed: YES / NO

## Checks

| Check ID | Check | Exact command / method | Expected |
|---|---|---|---|
| PF-001 | {{CHECK}} | `{{COMMAND}}` | {{EXPECTED}} |

## Abort conditions
{{ABORT_CONDITIONS}}

## Output
Create a preflight result using `TEMPLATE_preflight_result.md` and stop.
Do not implement product code.
