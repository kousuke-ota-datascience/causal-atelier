# Agent Execution Readiness Preflight Instruction

## Blocking checks

- PRE-01 enhancement-side agent_entry_prompts exists
- PRE-03 WORK_ROOT exists
- PRE-04 WORK_ROOT identity is correct
- PRE-05 assigned Pxx resolves to exactly one file
- PRE-06 Coding prompt preserves information isolation
- PRE-08 GATE_ID is valid
- PRE-09 PACKAGE_ID is valid
- PRE-10 TRIAL_NO is numeric and resolvable
- PRE-11 current branch matches the execution target
- PRE-13 Architecture record has no explicit blocking state
- PRE-14 Gate implementation / verification contracts have no explicit blocking state
- PRE-15 required dependencies are complete based on actual evidence

Any `FAIL` -> `BLOCKED_PRECHECK`.

## Diagnostic checks

The following do not block by themselves.

- PRE-02 template-like placeholder occurrences
- PRE-07 Pxx helper metadata
- PRE-12 remote alias availability
- PRE-16 package reporting destination resolvability
- DIAG-01 declared package status

Execution readiness is derived from actual prerequisites.  
Do not require exact `READY_TO_EXECUTE` status literals or package checkpoint SHA equality.
