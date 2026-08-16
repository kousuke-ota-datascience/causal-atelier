# ENH-E7 Local Workflow-Control Extensions

This instance applies additional execution-control rules derived from ENH-E6 findings:

1. enhancement-specific `agent_entry_prompts/` are mandatory.
2. template-side prompts are not direct execution entry points.
3. enhancement-fixed and runtime variables are separated.
4. Work Package Coding Agent normative workflow contract is assigned Pxx only.
5. Pxx must be self-contained.
6. Coding Agent and Test Agent information sources are intentionally isolated.
7. Agent Execution Readiness is independent from document compliance.
8. readiness has four axes: artifact completeness, content completeness, execution resolvability, information isolation.
9. mechanical preflight blocks execution when identity/resolution/isolation conditions fail.
