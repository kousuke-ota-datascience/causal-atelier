# ENH-E7 Independent Verification Test Agent Prompt

**Enhancement:** ENH-E7  
**Work root:** docs/wiki/develop_memo/_work/20260813_ENH-E7_project_analysis_workspace_separation

Human provides:

```text
GATE_ID=<G01|G02>
TRIAL_NO=<NN>
```

## Normative acceptance source

Read the exactly-one frozen Gate 07:

```text
docs/wiki/develop_memo/_work/20260813_ENH-E7_project_analysis_workspace_separation/10_enhance_instruction/<GATE_ID>/07_Ariadne_ENH-E7_<GATE_ID>_test_instruction.md
```

Do not use Coding Agent Pxx, P00 or Gate 06 to alter/complete Acceptance Criteria.

## Evidence inputs

- Implementation Completion Report for the Trial.
- Fixed Trial Candidate SHA from that report.
- actual checkout/runtime/source/test facts.
- previous PASS evidence identified by 07.

## Required flow

1. candidate identity audit first.
2. execute Test Items exactly according to frozen 07.
3. do not modify production/test/migration/dependency code.
4. create independent Test Item reports.
5. create 999 Gate Decision with PASS / FAIL / BLOCKED.
6. stop.

Coding-side `READY_FOR_TEST` is not acceptance evidence by itself.
