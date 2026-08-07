# G3 Trial 001 Test 006 — postgres_predictive_split_contract

- Gate: G3
- Trial: 001
- Test item: 006
- Status: NOT_RUN
- Tested implementation commit: `73a92c1b5899bc0d072df0faf8621b5171b00e5a`
- Handoff report commit / path: `6540499bcf062b6af9dfe251b156e833a5142c06` / `20_implementation_reports/G3_001_implementation_completion_report.md`
- Branch: `prototype/ariadne_mvp_e3`
- Migration head: `20260807_product_0004` (`uv run alembic -c alembic_product.ini heads`, exit 0)
- Started at: NOT_RUN
- Finished at: NOT_RUN

## Purpose

PostgreSQL 上の predictive split API/persistence と migration head を検証する。

## Acceptance Criteria

テスト指示書 G3-006 記載の全項目。

## Preconditions / Environment

G3-001 が先に FAIL。Migration head の read-only static check のみ実施済み。

## Commands Executed

```bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache uv run alembic -c alembic_product.ini heads
```

PostgreSQL contract command は未実行。

## Exact Result

- migration heads command exit code: 0
- observed head: `20260807_product_0004 (head)`
- PostgreSQL test exit code: NOT_RUN
- passed: 0
- failed: 0
- skipped: 0
- duration: 0s for PostgreSQL test

## Log / Evidence

```text
20260807_product_0004 (head)
```

`NOT_RUN_DUE_TO_PRIOR_FAILURE`: G3-001 `REQUIRED_TEST_COVERAGE_MISSING`。

## Findings

- product defect: not evaluated
- test infrastructure issue: not evaluated
- regression: not evaluated
- deviation: prior mandatory item failed
- none: false

## Decision Rationale

Migration head は single head として確認したが、必須 PostgreSQL contract はテスト指示書 §14 の fail-fast 規則により未実行。したがって item は PASS ではない。

## Source Modification by Test Agent

NONE
