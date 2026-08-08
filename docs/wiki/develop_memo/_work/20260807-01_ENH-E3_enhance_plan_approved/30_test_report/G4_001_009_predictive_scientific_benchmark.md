# G4 Trial 001 Test 009 — predictive_scientific_benchmark

- Gate: G4
- Trial: 001
- Test item: 009
- Status: FAIL
- Tested implementation commit: `f16c0a7bb25fbe3378585ba78921398638d1ecea`
- Handoff report commit / path: `6c0f10a0eb3429d16f774d72d22a723626da5d03` / `20_implementation_reports/G4_001_implementation_completion_report.md`
- Branch: `prototype/ariadne_mvp_e3`
- Migration head: `20260807_product_0005`
- Started at: `2026-08-07T09:06:42Z`
- Finished at: `2026-08-07T09:06:49Z`

## Purpose

Predictive scientific benchmark が leakage prevention、reproducibility、classification/regression metric sanity を独立検証することを監査する。

## Acceptance Criteria

- train-only fit
- TEST isolation
- reproducibility
- classification metric sanity
- regression metric sanity
- deliberate leakage rejection

## Preconditions / Environment

- Canonical file: `tests/scientific_benchmarks/test_predictive_e3_benchmarks.py`
- Source/test code は変更せず、collect-only と static assertion audit を実施。

## Commands Executed

```bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 \
uv run pytest --collect-only -q \
  tests/scientific_benchmarks/test_predictive_e3_benchmarks.py

rg -n 'fit_partition|TRAIN_ONLY|train.only|TRAIN.*fit|fit.*TRAIN' \
  tests/scientific_benchmarks/test_predictive_e3_benchmarks.py
rg -n 'TEST_ISOLATION|selection_allowed|final_evaluation_only|TEST' \
  tests/scientific_benchmarks/test_predictive_e3_benchmarks.py
rg -n 'LEAK|leak|PredictiveValidationError|pytest\.raises' \
  tests/scientific_benchmarks/test_predictive_e3_benchmarks.py
```

## Exact Result

- coverage audit exit code: 0
- benchmark execution: NOT_RUN
- collected tests: 2
- passed: 0
- failed: 0
- skipped: 0
- duration: 7s
- train-only benchmark assertion matches: 0
- TEST isolation benchmark assertion matches: 0
- deliberate leakage rejection matches: 0
- reproducibility assertion matches: 1

## Log / Evidence

```text
test_logistic_registry_model_recovers_deterministic_separable_signal
test_linear_registry_model_recovers_exact_affine_signal
2 tests collected in 5.97s
TRAIN_ONLY_BENCHMARK_MATCHES=0
TEST_ISOLATION_BENCHMARK_MATCHES=0
DELIBERATE_LEAKAGE_REJECTION_MATCHES=0
REPRODUCIBILITY_ASSERTION_MATCHES=1
```

Existing coverage:

- classification: deterministic same-seed model equality、ROC-AUC、PR-AUC、log loss、Brier sanity
- regression: MAE、RMSE、R² sanity
- train-only fit: absent
- TEST isolation: absent
- deliberate leakage rejection: absent

## Findings

- product defect: none established; benchmark was not executed after coverage failure
- test infrastructure issue: none
- regression: not evaluated
- deviation: `REQUIRED_TEST_COVERAGE_MISSING`
- none: false

```text
Failure category: REQUIRED_TEST_COVERAGE_MISSING
Missing contract: train-only fit; TEST isolation; deliberate leakage rejection in Predictive scientific benchmark
Expected test scope: tests/scientific_benchmarks/test_predictive_e3_benchmarks.py
Observed existing coverage: two tests cover reproducibility and classification/regression metric sanity only
```

## Required Correction

Predictive scientific benchmark に train-only fit、TEST isolation、deliberate leakage rejection を直接検証する automated coverage が必要である。

## Decision Rationale

テスト指示書 G4-009 が最低限要求する6 contract のうち3 contract に automated benchmark assertion がない。§17 に従い、既存2 testsを実行して部分的 PASS を作らず FAIL とする。

## Source Modification by Test Agent

NONE
