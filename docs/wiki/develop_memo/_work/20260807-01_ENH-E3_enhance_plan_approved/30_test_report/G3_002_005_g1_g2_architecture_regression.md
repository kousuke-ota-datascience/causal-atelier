# G3 Trial 002 Test 005 — g1_g2_architecture_regression

- Gate: G3
- Trial: 002
- Test item: 005
- Status: PASS
- Tested implementation commit: `fd4e332939f93cc35adbf4a03929818e47c04b7e`
- Handoff report commit / path: `908ce954e4f155560861c91fae169cbe35f63866` / `20_implementation_reports/G3_002_implementation_completion_report.md`
- Branch: `prototype/ariadne_mvp_e3`
- Migration head: `20260807_product_0004`
- Started at: `2026-08-07T08:17:04Z`
- Finished at: `2026-08-07T08:17:15Z`

## Purpose

G1/G2、Generic Workflow Core、Causal workflow、Exploratory API/frontend、architecture の regression を検証する。

## Acceptance Criteria

テスト指示書 G3-005 の canonical 7-file suite が全て PASS する。

## Preconditions / Environment

- `UV_CACHE_DIR=/tmp/ariadne-uv-cache`
- `PYTHONDONTWRITEBYTECODE=1`

## Commands Executed

```bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 \
uv run pytest -q \
  tests/product/test_analysis_view_e3.py \
  tests/product/test_exploratory_contract_e3.py \
  tests/product/test_exploratory_api_worker_e2e_e3.py \
  tests/product/test_exploratory_frontend_contract_e3.py \
  tests/product/test_enh_e3_workflow_core.py \
  tests/product/test_enh_e3_causal_workflow_regression.py \
  tests/product/test_architecture.py
```

## Exact Result

- exit code: 0
- passed: 27
- failed: 0
- skipped: 0
- pytest duration: 4.73s
- command duration: 11s

## Log / Evidence

```text
...........................                                              [100%]
27 passed in 4.73s
```

## Findings

- product defect: none
- test infrastructure issue: none
- regression: 0
- deviation: none
- none: true

## Decision Rationale

指定された G1/G2 targeted regression と architecture tests が全て成功したため PASS。

## Source Modification by Test Agent

NONE
