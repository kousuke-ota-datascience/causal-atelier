# Agent Execution Readiness Preflight Instruction

Check before Coding Agent execution:

- PRE-01 enhancement-side agent_entry_prompts exists
- PRE-02 enhancement-fixed double-curly placeholders == 0
- PRE-03 WORK_ROOT exists
- PRE-04 WORK_ROOT is exactly one enhancement root
- PRE-05 assigned Pxx resolves to exactly one file
- PRE-06 Coding prompt does not instruct direct-read of 06 / 07 / P00 / other Pxx
- PRE-07 assigned Pxx is self-contained and does not require those documents
- PRE-08 GATE_ID present
- PRE-09 PACKAGE_ID present
- PRE-10 TRIAL_NO present
- PRE-11 branch identity explicit and current branch matches
- PRE-12 remote alias explicit and locally verified
- PRE-13 Gate Architecture Review approved
- PRE-14 Gate 06/07 frozen
- PRE-15 assigned Pxx status READY_TO_EXECUTE

Any mandatory failure -> BLOCKED.
