# G6 Trial 003 Test 002 — cross_analysis_lineage

- Gate: G6
- Trial: 003
- Test item: 002
- Status: PASS
- Tested implementation commit: `a54c82f3648afad7cd9ec2bfacff2ceae7a59ac1`
- Handoff report commit / path: `fe700b0dfbfb4906dc599034a1cd0f11183a1dbf` / `docs/wiki/develop_memo/_work/20260807-01_ENH-E3_enhance_plan_approved/20_implementation_reports/G6_003_implementation_completion_report.md`
- Branch: `prototype/ariadne_mvp_e3`
- Migration head: `20260807_product_0006`
- Started at: 2026-08-07T21:52:23Z
- Finished at: 2026-08-07T21:52:45Z

## Purpose

Cross-analysis lineageとsame-project restrictionを検証する。

## Acceptance Criteria

Context→Dataset、Dataset→View、Explore→Causal/Predictive draft、Execution→Result→Artifact、Result→Annotation、RERUN/REVISED、same-project restriction。

## Commands Executed

```bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 \
uv run pytest -q tests/product/test_cross_analysis_lineage_e3.py \
  tests/product/test_results_lineage_export_e3.py \
  tests/product/test_enh_e3_api_worker_e2e.py
```

## Exact Result

- command exit code: 1（別itemのAPI/frontend failureを含む）
- G6-002 tests: 2 passed, 0 failed
- duration: targeted pytest elapsed 22.04s

## Findings

- product defect: none observed in this item
- regression: none within lineage tests
- deviation: none

## Decision Rationale

canonical lineage 2 testsがPASSしたためPASS。

## Source Modification by Test Agent

NONE
