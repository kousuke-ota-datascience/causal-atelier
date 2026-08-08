# G4 Trial 002 Test 006 — metric_task_compatibility_and_diagnostics

- Gate: G4
- Trial: 002
- Test item: 006
- Status: FAIL
- Tested implementation commit: `38f8b16f1a46d6c90fc780c446eb996417843841`
- Handoff report commit / path: `48256021903d8566d7bf6f2341304ed5a2bf46ea` / `20_implementation_reports/G4_002_implementation_completion_report.md`
- Branch: `prototype/ariadne_mvp_e3`
- Migration head: `20260807_product_0005`
- Started at: `2026-08-07T09:22:08Z`
- Finished at: `2026-08-07T09:22:18Z`

## Purpose

Metric/diagnostic completenessを監査する。

## Acceptance Criteria

G4-006記載のclassification/regression metrics、sample count、population、status separation。

## Preconditions / Environment

Evaluation/API testsをread-only監査。

## Commands Executed

```bash
sed -n '68,100p' tests/product/test_predictive_evaluation_e3.py | rg 'sample_count'
```

## Exact Result

- coverage audit exit code: 0
- runtime pytest: NOT_RUN
- passed: 0
- failed: 0
- skipped: 0
- duration: 10s shared coverage audit
- classification sample-count assertions: 0

## Log / Evidence

Classification ROC-AUC/PR-AUC/log loss/Brier/threshold/class balance/calibrationはassertされる。Regression testは`sample_count`をassertするが、classification evaluationのsample countはassertされない。

## Findings

- product defect: none established
- test infrastructure issue: none
- regression: not evaluated
- deviation: `REQUIRED_TEST_COVERAGE_MISSING`
- none: false

```text
Failure category: REQUIRED_TEST_COVERAGE_MISSING
Missing contract: classification evaluation sample count
Expected test scope: tests/product/test_predictive_evaluation_e3.py
Observed existing coverage: regression sample_count only
```

## Required Correction

Classification evaluationのsample countを直接検証するautomated coverageが必要。

## Decision Rationale

G4-006のsample count contractがtask横断で検証されていないため§17のFAIL。

## Source Modification by Test Agent

NONE
