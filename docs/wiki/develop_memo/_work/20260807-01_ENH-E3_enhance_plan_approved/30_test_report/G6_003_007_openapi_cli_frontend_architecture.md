# G6 Trial 003 Test 007 — openapi_cli_frontend_architecture

- Gate: G6
- Trial: 003
- Test item: 007
- Status: FAIL
- Tested implementation commit: `a54c82f3648afad7cd9ec2bfacff2ceae7a59ac1`
- Handoff report commit / path: `fe700b0dfbfb4906dc599034a1cd0f11183a1dbf` / `docs/wiki/develop_memo/_work/20260807-01_ENH-E3_enhance_plan_approved/20_implementation_reports/G6_003_implementation_completion_report.md`
- Branch: `prototype/ariadne_mvp_e3`
- Migration head: `20260807_product_0006`
- Started at: 2026-08-07T21:52:23Z
- Finished at: 2026-08-07T21:52:45Z

## Purpose

OpenAPI/CLI/Frontend/architecture/operation availabilityと前段回帰を検証する。

## Acceptance Criteria

既存canonical contract testsが全PASSすること。

## Commands Executed

```bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 \
uv run pytest -q tests/product/test_frontend_contract.py \
  tests/product/test_architecture.py tests/product/test_cli_contract.py
```

## Exact Result

- item-related result: 1 failed, 6 passed in the combined targeted command
- failure: `test_four_workspace_frontend_uses_only_product_api_contract`
- missing current frontend contract token: `/export`
- command duration: targeted pytest elapsed 22.04s

## Log / Evidence

G5 Trial 002 full active pytest had 182 passed/4 skipped before G6 frontend closure. Current G6 frontend uses `/exports` project-scoped API; the existing canonical contract still requires `/export`. This is a current regression in a required existing contract.

## Findings

- Failure category: REGRESSION
- product defect: current frontend does not satisfy existing `test_frontend_contract.py` endpoint contract
- test infrastructure issue: none
- regression: confirmed relative to prior G5 full-suite evidence

## Required Correction

既存frontend contractに対する観測された契約違反を修正対象として報告する。設計案は提示しない。

## Decision Rationale

G6-007 canonical frontend contract failureは製品回帰であり、07b §4/§14によりFAIL。残りの高コスト試験を停止した。

## Source Modification by Test Agent

NONE
