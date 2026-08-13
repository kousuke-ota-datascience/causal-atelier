# ENH-E7 Agent Entry Prompts

These prompts are Enhancement-specific. The shared template prompt directory must not be used directly.

## Routing

| Human goal | Prompt |
|---|---|
| one Work Package Coding execution | `10_normal_execution_02_work_package_coding_agent_prompt.md` |
| assemble Trial candidate after all Pxx | `20_candidate_assembly_01_work_package_candidate_assembly_agent_prompt.md` |
| independent Gate verification | `30_independent_verification_01_test_agent_prompt.md` |
| formal FAIL remediation | `40_fail_remediation_01_fail_rework_coding_agent_prompt.md` |
| Gate-level package orchestration | `50_orchestration_01_gate_orchestrator_prompt.md` |
| single-execution coding | disabled for ENH-E7; see `10_normal_execution_01_single_execution_coding_agent_prompt.md` |

## Quick entry example

```text
Read and execute:
docs/wiki/develop_memo/_work/20260813_ENH-E7_project_analysis_workspace_separation/40_operator_workflows/agent_entry_prompts/10_normal_execution_02_work_package_coding_agent_prompt.md

Runtime:
GATE_ID=G01
PACKAGE_ID=P01
TRIAL_NO=01
```

Human supplies runtime identity only. Enhancement identity is fixed in these prompts.
