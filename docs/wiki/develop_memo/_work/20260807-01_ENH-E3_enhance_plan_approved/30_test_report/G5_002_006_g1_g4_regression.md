# G5 Trial 002 Test 006 — g1_g4_regression

- Gate: G5
- Trial: 002
- Test item: 006
- Status: PASS
- Tested implementation commit: 4a83bb6860c895f00e4dfd7c9e7880105387373e
- Handoff report commit / path: 4ccbfbb196ba384aa362450666c00b4c936c58d7 / docs/wiki/develop_memo/_work/20260807-01_ENH-E3_enhance_plan_approved/20_implementation_reports/G5_002_implementation_completion_report.md
- Branch: prototype/ariadne_mvp_e3
- Migration head: 20260807_product_0005
- Started at: 2026-08-07T11:32:35Z
- Finished at: 2026-08-07T11:32:57Z

## Purpose

G5 changesがG1〜G4の必須contractを破壊していないことを検証する。

## Acceptance Criteria

G1/G2 workflow・analysis view・exploratory、G3 predictive specification/split、G4 context/training/evaluation/API worker targeted suite。

## Preconditions / Environment

- G4 Trial 003: PASS
- Current handoff HEAD: 4ccbfbb196ba384aa362450666c00b4c936c58d7
- Project `.venv` via `uv run`; Test Agent source/test/migration modification: NONE

## Commands Executed

~~~bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run pytest -q \
  tests/product/test_analysis_view_e3.py tests/product/test_exploratory_contract_e3.py \
  tests/product/test_exploratory_api_worker_e2e_e3.py tests/product/test_exploratory_frontend_contract_e3.py \
  tests/product/test_enh_e3_workflow_core.py tests/product/test_enh_e3_causal_workflow_regression.py \
  tests/product/test_architecture.py tests/product/test_predictive_spec_e3.py \
  tests/product/test_predictive_leakage_e3.py tests/product/test_predictive_split_e3.py \
  tests/product/test_predictive_split_api_e3.py tests/product/test_research_context_e3.py \
  tests/product/test_analysis_specification_e3.py tests/product/test_predictive_training_e3.py \
  tests/product/test_predictive_evaluation_e3.py tests/product/test_predictive_api_worker_e2e_e3.py
~~~

## Exact Result

- exit code: 0
- passed: 57
- failed: 0
- skipped: 0
- duration: 22s wall clock (pytest 16.14s)

## Log / Evidence

- `/tmp/g5_002_006_g1_g4_regression.log`

## Findings

- product defect: none
- test infrastructure issue: none
- regression: none
- deviation: none

## Decision Rationale

All 57 G1〜G4 targeted regression tests passed.

## Source Modification by Test Agent

NONE

