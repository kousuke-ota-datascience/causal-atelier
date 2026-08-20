# 40 — ENH-E8 Operator Workflow

Human/operatorはidentity、contract freeze、preflight、Agent routing、Candidate Assembly、Independent Verification、FAIL/BLOCKED後のroutingを管理する。

Routing:

- G01 normal Coding -> `agent_entry_prompts/10_normal_execution_01_single_execution_coding_agent_prompt.md`
- G02 package Coding -> `agent_entry_prompts/10_normal_execution_02_work_package_coding_agent_prompt.md`
- G02 Candidate Assembly -> `agent_entry_prompts/20_candidate_assembly_01_work_package_candidate_assembly_agent_prompt.md`
- G01/G02 Test -> `agent_entry_prompts/30_independent_verification_01_test_agent_prompt.md`
- formal FAILのみ -> `agent_entry_prompts/40_fail_remediation_01_fail_rework_coding_agent_prompt.md`

現在のE8 scopeではauthority/persistence/runtime/destructive changeを予定しないためArchitecture Review / Controlled Runbookは`N/A`としている。

その種の変更が必要と判明した場合、implicit scope expansionせずcontract escalationする。
