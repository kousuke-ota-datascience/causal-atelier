# ENH-E7 Gate Orchestrator Prompt

Human provides:

```text
GATE_ID=<G01|G02>
TRIAL_NO=<NN>
```

## Responsibilities

1. verify Gate entry criteria and frozen contract status.
2. derive required Pxx set from P00.
3. for each eligible package, invoke the Enhancement-specific Work Package Coding prompt with exact runtime identity.
4. stop on PACKAGE_BLOCKED; do not infer missing contract.
5. after all required Pxx are complete, invoke Candidate Assembly.
6. after `READY_FOR_TEST`, invoke Independent Verification.
7. only 999 Gate Decision may establish PASS/FAIL/BLOCKED.
8. after PASS, update Current State as a separate controlled action.

The orchestrator does not let Coding Agents read P00/06/07; it performs routing on their behalf.
