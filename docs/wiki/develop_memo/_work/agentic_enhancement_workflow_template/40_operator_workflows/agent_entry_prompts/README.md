# Agent Entry Prompts — v3

## Principle

Humanがidentity variablesを与え、derived variablesを再帰展開して実行対象path / filenameを決定する。

## Selection

| Situation | Prompt |
|---|---|
| Single-execution Gate Coding | `coding_agent_prompt.md` |
| Planned / remediation Work Package | `work_package_coding_agent_prompt.md` |
| formal FAIL after Independent Test | `fail_rework_coding_agent_prompt.md` |
| Independent Test / Audit | `test_agent_prompt.md` |

Trial番号はAgent起動回数ではない。Package interruptionやrestartだけでTrialを増やさない。

Canonical variable naming: `VARIABLE_CONVENTIONS.md`.
