# G4 Trial 003 Test 011 — g1_g3_regression

- Gate: G4
- Trial: 003
- Test item: 011
- Status: PASS
- Tested implementation commit: a8b656b463b2f8251eff8006538d04ad5af83918
- Handoff report commit / path: 28c57400a2966568975698297eb7554ce51af80c / docs/wiki/develop_memo/_work/20260807-01_ENH-E3_enhance_plan_approved/20_implementation_reports/G4_003_implementation_completion_report.md
- Branch: prototype/ariadne_mvp_e3
- Migration head: 20260807_product_0005
- Started at: 2026-08-07T09:55:17Z
- Finished at: 2026-08-07T09:55:29Z

## Purpose

G4変更がG1〜G3重要契約を破壊していないことを検証する。

## Acceptance Criteria

G3 specification/leakage/split/API targeted testsとG1/G2 analysis view/exploratory/workflow/architecture重要回帰。

## Preconditions / Environment

- Current HEAD: 28c57400a2966568975698297eb7554ce51af80c
- Project .venv via uv run; Test Agentによるsource/test/migration変更なし。

## Commands Executed

~~~bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run pytest -q tests/product/test_predictive_spec_e3.py tests/product/test_predictive_leakage_e3.py tests/product/test_predictive_split_e3.py tests/product/test_predictive_split_api_e3.py tests/product/test_analysis_view_e3.py tests/product/test_exploratory_contract_e3.py tests/product/test_exploratory_api_worker_e2e_e3.py tests/product/test_exploratory_frontend_contract_e3.py tests/product/test_enh_e3_workflow_core.py tests/product/test_enh_e3_causal_workflow_regression.py tests/product/test_architecture.py
~~~

## Exact Result

- exit code 0; 45 passed; 0 failed; 0 skipped; 12s wall clock (pytest 6.36s).

## Log / Evidence

- /tmp/g4_003_011_g1_g3_regression.log

## Findings

- product defect: none; test infrastructure issue: none; regression: none; deviation: none.

## Decision Rationale

G3 targetedとG1/G2重要回帰45件が全成功したためPASS。

## User-directed Full Re-execution

- Execution HEAD before evidence update: `430f6411665bd72d3436b3a42cc7fd593e75a953`
- Technical status: PASS
- Started at: 2026-08-07T10:27:52Z
- Finished at: 2026-08-07T10:28:08Z

~~~bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run pytest -q tests/product/test_predictive_spec_e3.py tests/product/test_predictive_leakage_e3.py tests/product/test_predictive_split_e3.py tests/product/test_predictive_split_api_e3.py tests/product/test_analysis_view_e3.py tests/product/test_exploratory_contract_e3.py tests/product/test_exploratory_api_worker_e2e_e3.py tests/product/test_exploratory_frontend_contract_e3.py tests/product/test_enh_e3_workflow_core.py tests/product/test_enh_e3_causal_workflow_regression.py tests/product/test_architecture.py
~~~

- Exact result: exit code 0; 45 passed; 0 failed; 0 skipped; 16s wall clock (pytest 9.30s).
- Log / evidence: `/tmp/g4_003_full_rerun_011.log`
- Source/test/migration modification by Test Agent: NONE

## Source Modification by Test Agent

NONE
