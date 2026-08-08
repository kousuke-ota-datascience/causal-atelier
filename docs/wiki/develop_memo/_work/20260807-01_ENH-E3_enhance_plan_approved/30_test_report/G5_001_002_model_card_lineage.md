# G5 Trial 001 Test 002 — model_card_lineage

- Gate: G5
- Trial: 001
- Test item: 002
- Status: FAIL
- Tested implementation commit: cb0f45164fe5190af37df466af70057b89b8c8cb
- Handoff report commit / path: d7b1c1a9a97d8c9474d628baa42824fa959caeff / docs/wiki/develop_memo/_work/20260807-01_ENH-E3_enhance_plan_approved/20_implementation_reports/G5_001_implementation_completion_report.md
- Branch: prototype/ariadne_mvp_e3
- Migration head: 20260807_product_0005
- Started at: 2026-08-07T11:15:33Z
- Finished at: 2026-08-07T11:15:43Z

## Purpose

Model Cardの必須内容とSpecification/Dataset/Split/Model/Evaluation lineage coverageを監査する。

## Acceptance Criteria

intended use、deployment population、training data、features、split、model、validation/test metrics、limitations/warnings、runtime/code、およびSpec/Dataset/Split/Model/Evaluation lineage。

## Preconditions / Environment

- G4 Trial 003 Gate Decision: PASS
- Current handoff HEAD: d7b1c1a9a97d8c9474d628baa42824fa959caeff
- Test Agent source/test/migration modification: NONE

## Commands Executed

~~~bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run pytest -q --collect-only \
  tests/product/test_predictive_explanation_e3.py \
  tests/product/test_predictive_frontend_contract_e3.py \
  tests/product/test_predictive_api_worker_e2e_e3.py \
  tests/product/test_predictive_split_api_e3.py
sed -n '369,397p' tests/product/test_predictive_explanation_e3.py
~~~

## Exact Result

- coverage audit exit code: 1
- collected: 15 tests
- executed: 0
- failed acceptance coverage checks: Model Card lineage/value assertions
- duration: 10s

## Log / Evidence

- `/tmp/g5_001_required_coverage_audit.log`
- Existing lineage assertions cover Model Card→Specification, Model Card→Dataset, and Model Card→Evaluation only.
- The FITTED_MODEL assertion in the existing block targets the Explanation Result, not the Model Card.

## Findings

- Failure category: REQUIRED_TEST_COVERAGE_MISSING
- Missing contract: direct Model Card lineage assertions for Split/PARTITION_INDEX and FITTED_MODEL; no Model Card optional AnalysisView lineage assertion. FITTED_PREPROCESSOR coverage requested by the implementation handoff is also absent.
- Missing contract: direct value assertions for intended_use, deployment_population, feature_set, model_descriptor, and complete runtime metadata.
- Expected test scope: automated Model Card persistence/lineage contract.
- Observed existing coverage: payload key set plus selected training/split/metric/code values, and only Spec/Dataset/Evaluation lineage edges.
- product defect: not established

## Required Correction

Add automated coverage for the missing Model Card fields and lineage relationships. This is a coverage correction requirement, not a product implementation prescription.

## Decision Rationale

The test instruction requires critical automated coverage. Required Model Card contracts are not directly verified, so this item is FAIL without executing product tests.

## Source Modification by Test Agent

NONE

