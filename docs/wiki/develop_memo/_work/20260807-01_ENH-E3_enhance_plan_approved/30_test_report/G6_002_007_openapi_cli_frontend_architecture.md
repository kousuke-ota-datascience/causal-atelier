# G6 Trial 002 Test 007 — openapi_cli_frontend_architecture

- Gate: G6
- Trial: 002
- Test item: 007
- Status: BLOCKED
- Tested implementation commit: `79d16f1b000a0e8e4771bfdcfd72cdf12b0e838c`
- Handoff report commit / path: `195983d7c0ae120e5bd4537a265eb80cd1266e87` / `docs/wiki/develop_memo/_work/20260807-01_ENH-E3_enhance_plan_approved/20_implementation_reports/G6_002_implementation_completion_report.md`
- Branch: `prototype/ariadne_mvp_e3`
- Migration head: `20260807_product_0006`
- Started at: 2026-08-07T21:41:38Z
- Finished at: 2026-08-07T21:41:52Z

## Purpose

OpenAPI、CLI、Frontend、architecture、operation availabilityを検証する。

## Acceptance Criteria

既存canonical contract testsを全てPASSさせること。

## Commands Executed

```bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 \
uv run pytest -q tests/product/test_cross_analysis_lineage_e3.py \
  tests/product/test_results_lineage_export_e3.py
```

## Exact Result

- command exit code: 1
- passed: 5
- failed: 1
- failed test: `test_g6_request_contracts_reject_unknown_fields`
- duration: pytest 8.44s（command elapsed 14.39s）

## Log / Evidence

API responseは`400 INVALID_REQUEST`を返したが、assertionは`errors[0].loc == ["body", "unexpected"]`を要求。入力`result_ids=[]`はschemaの`min_length=1`にも違反するため、実際の先頭errorは`["body", "result_ids"]`だった。

## Findings

- Blocking category: TEST_ASSERTION_AMBIGUITY
- product defect: not established
- test infrastructure issue: none
- observed mismatch: error array ordering is not specified by 07b; test fixes an unspecified ordering and combines two validation failures.

## Required Correction

作業指示書の範囲内ではテストコードを変更しない。観測されたassertion/入力の不整合を次trialの判断対象とする。

## Decision Rationale

07b §18の「既存testが明らかに壊れている、またはassertionが指示書と矛盾する場合」に該当する可能性があり、製品FAILと断定できない。Test Agentはtestを変更せずBLOCKEDとした。

## Source Modification by Test Agent

NONE
