# G6 Trial 002 Test 003 — result_summary_and_comparison

- Gate: G6
- Trial: 002
- Test item: 003
- Status: PASS
- Tested implementation commit: `79d16f1b000a0e8e4771bfdcfd72cdf12b0e838c`
- Handoff report commit / path: `195983d7c0ae120e5bd4537a265eb80cd1266e87` / `docs/wiki/develop_memo/_work/20260807-01_ENH-E3_enhance_plan_approved/20_implementation_reports/G6_002_implementation_completion_report.md`
- Branch: `prototype/ariadne_mvp_e3`
- Migration head: `20260807_product_0006`
- Started at: 2026-08-07T21:41:38Z
- Finished at: 2026-08-07T21:41:52Z

## Purpose

Unified Results summary/comparisonの意味論とstored Result不変性を検証する。

## Acceptance Criteria

compatible comparison、invariant/changed conditions、warning difference、cross-family summary、no cross-family ranking、immutable stored Result。

## Commands Executed

```bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 \
uv run pytest -q tests/product/test_cross_analysis_lineage_e3.py \
  tests/product/test_results_lineage_export_e3.py
```

## Exact Result

- exit code: 1（G6-007 strict-contract testの失敗を含む）
- G6-003 test: 1 passed, 0 failed
- duration: pytest 8.44s（command elapsed 14.39s）

## Log / Evidence

`common_summary`、metric differences、common/changed warnings、`ranking: null`、cross-family incompatibility、ORM snapshot一致をassertしてPASS。

## Findings

- product defect: none observed
- test infrastructure issue: none
- regression: none within this item
- deviation: none

## Decision Rationale

G6-003のcomparison testはPASS。別itemのstrict-contract assertionは本項目の判定を変更しない。

## Source Modification by Test Agent

NONE
