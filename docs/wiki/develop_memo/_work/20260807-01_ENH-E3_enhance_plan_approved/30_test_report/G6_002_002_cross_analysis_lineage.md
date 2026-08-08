# G6 Trial 002 Test 002 — cross_analysis_lineage

- Gate: G6
- Trial: 002
- Test item: 002
- Status: PASS
- Tested implementation commit: `79d16f1b000a0e8e4771bfdcfd72cdf12b0e838c`
- Handoff report commit / path: `195983d7c0ae120e5bd4537a265eb80cd1266e87` / `docs/wiki/develop_memo/_work/20260807-01_ENH-E3_enhance_plan_approved/20_implementation_reports/G6_002_implementation_completion_report.md`
- Branch: `prototype/ariadne_mvp_e3`
- Migration head: `20260807_product_0006`
- Started at: 2026-08-07T21:41:38Z
- Finished at: 2026-08-07T21:41:52Z

## Purpose

Cross-analysis lineageとsame-project restrictionを検証する。

## Acceptance Criteria

Context→Dataset、Dataset→View、Explore→Causal/Predictive draft、Execution→Result→Artifact、Result→Annotation、RERUN/REVISED、same-project restriction。

## Commands Executed

```bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 \
uv run pytest -q tests/product/test_cross_analysis_lineage_e3.py \
  tests/product/test_results_lineage_export_e3.py
```

## Exact Result

- exit code: 1（同一command内のG6-007 strict-contract testのみ失敗）
- G6-002 tests: 2 passed, 0 failed
- duration: pytest 8.44s（command elapsed 14.39s）

## Log / Evidence

- Context→Dataset、Dataset→Analysis View、Explore→Causal/Predictive draft、Execution→Result→Artifact、Result→Annotationを直接assert。
- RERUN/REVISEDのrevision kind/evidence、cross-project rejectionもPASS。
- 同一commandの別item test failureはG6_002_007へ記録。

## Findings

- product defect: none observed
- test infrastructure issue: none
- regression: none within this item
- deviation: none

## Decision Rationale

G6 canonical lineage 2 testsが全PASSし、G6-002 Acceptance Criteriaを満たした。

## Source Modification by Test Agent

NONE
