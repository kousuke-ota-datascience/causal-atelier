# ENH-E7 Work Package Candidate Assembly Agent Prompt

**Enhancement:** ENH-E7  
**Work root:** docs/wiki/develop_memo/_work/20260813_ENH-E7_project_analysis_workspace_separation

Human provides:

```text
GATE_ID=<G01|G02>
TRIAL_NO=<NN>
```

## Preconditions

- Gate 06/07 are FROZEN.
- required Pxx set is known from P00.
- all required package checkpoints are `PACKAGE_COMPLETE`.
- no package blocker remains.

## Responsibilities

1. audit package-chain completeness and checkpoint identity.
2. inspect source/diff for candidate-affecting uncommitted or report-only changes.
3. run Gate-wide integration self-check.
4. run Coding-side protected passed-Gate regression.
5. run applicable critical browser E2E self-check using repository harness.
6. fix a single Fixed Trial Candidate full SHA.
7. create Implementation Completion Report.
8. set candidate state to `READY_FOR_TEST`.

## Prohibited

- do not declare Gate PASS.
- do not rewrite 06/07.
- do not repair a missing package scope by ad hoc out-of-contract coding.
- if package chain is incomplete, return BLOCKED rather than assembling a partial candidate.
