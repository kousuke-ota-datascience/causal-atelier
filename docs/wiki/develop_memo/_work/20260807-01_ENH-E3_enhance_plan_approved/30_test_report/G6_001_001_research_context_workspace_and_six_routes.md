# G6 Trial 001 Test 001 — research_context_workspace_and_six_routes

- Gate: G6
- Trial: 001
- Test item: 001
- Status: NOT_RUN
- Tested implementation commit: `265b69a3317a0b9747cacee457e72b36a62daa7e`
- Handoff report commit / path: `963f1f2` / `docs/wiki/develop_memo/_work/20260807-01_ENH-E3_enhance_plan_approved/20_implementation_reports/G6_001_implementation_completion_report.md`
- Branch: `prototype/ariadne_mvp_e3`
- Migration head: `20260807_product_0006`
- Started at: NOT_RUN
- Finished at: NOT_RUN

## Purpose

Research Context、workspace state、6 route、履歴操作、FIXED resourceの不変性、analysis-familyに依存しないroleを検証する。

## Acceptance Criteria

Context CRUD/FIX/history/usage、6つの独立URL、共通header/selectors、deep link/reload/back、FIXED resource immutability、global Treatment/Outcome/Target roleがないこと。

## Preconditions / Environment

- G5 Trial 003 Gate Decision: PASS
- implementation/handoff差分はreport文書のみで、source/test/migration差分なし。
- 関連5 testはcollect可能。

## Commands Executed

```bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 \
uv run pytest -q --collect-only \
  tests/product/test_research_context_e3.py \
  tests/product/test_analysis_view_e3.py \
  tests/product/test_cross_analysis_lineage_e3.py \
  tests/product/test_results_lineage_export_e3.py \
  tests/product/test_enh_e3_api_worker_e2e.py
```

## Exact Result

- collection exit code: 0
- collected: 12（うち本項目に直接関連するContext/View testは5）
- executed: 0
- passed: 0
- failed: 0
- skipped: 0
- collection duration: 3.80s（command elapsed 10.33s）

## Log / Evidence

- `test_research_context_e3.py`の2件、`test_analysis_view_e3.py`の3件をcollect。
- G6-002/003/004/006/013のrequired coverage failure確定後は実行していない。

## Findings

- product defect: not evaluated
- test infrastructure issue: none
- regression: not evaluated
- deviation: NOT_RUN_DUE_TO_PRIOR_FAILURE

## Decision Rationale

同じ初期監査でGateをFAILにするrequired coverage欠落が確定したため、07b §14のfail-fastに従い実行を停止した。

## Source Modification by Test Agent

NONE
