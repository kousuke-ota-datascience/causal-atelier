# G4 Trial 002 Test 002 — predictive_plan_and_runner_registration

- Gate: G4
- Trial: 002
- Test item: 002
- Status: FAIL
- Tested implementation commit: `38f8b16f1a46d6c90fc780c446eb996417843841`
- Handoff report commit / path: `48256021903d8566d7bf6f2341304ed5a2bf46ea` / `20_implementation_reports/G4_002_implementation_completion_report.md`
- Branch: `prototype/ariadne_mvp_e3`
- Migration head: `20260807_product_0005`
- Started at: `2026-08-07T09:22:08Z`
- Finished at: `2026-08-07T09:22:18Z`

## Purpose

Predictive Plan determinism、DAG/binding、runner registrationを監査する。

## Acceptance Criteria

同一inputから生成したPlanのdeterministic identityを含む、G4-002全contract。

## Preconditions / Environment

Current automated test codeをread-only監査。

## Commands Executed

```bash
uv run pytest --collect-only -q tests/product/test_predictive_training_e3.py \
  tests/product/test_predictive_api_worker_e2e_e3.py
rg -n 'first_plan|second_plan|plan_one|plan_two|canonical_hash\(plan' \
  tests/product/test_predictive_training_e3.py \
  tests/product/test_predictive_api_worker_e2e_e3.py
```

## Exact Result

- coverage audit exit code: 0
- runtime pytest: NOT_RUN
- passed: 0
- failed: 0
- skipped: 0
- duration: 10s shared coverage audit
- planner identity comparison assertions: 0

## Log / Evidence

Stage order、Plan validation、successful execution assertionsは存在する。2つのgenerated Plan value/hashを直接比較するassertionは存在しない。Fitted model equalityはPlan identityの変化を検出できない。

## Findings

- product defect: none established
- test infrastructure issue: none
- regression: not evaluated
- deviation: `REQUIRED_TEST_COVERAGE_MISSING`
- none: false

```text
Failure category: REQUIRED_TEST_COVERAGE_MISSING
Missing contract: Planner deterministic identity
Expected test scope: predictive plan unit/contract test
Observed existing coverage: stage order/validation/execution and model reproducibility only
```

## Required Correction

同一inputsから生成されるPredictive Planのidentity/canonical contentが一致することを直接検証するautomated coverageが必要。

## Decision Rationale

Planner determinismはG4-002明示要件であり、直接assertionがないため§17によりFAIL。

## Source Modification by Test Agent

NONE
