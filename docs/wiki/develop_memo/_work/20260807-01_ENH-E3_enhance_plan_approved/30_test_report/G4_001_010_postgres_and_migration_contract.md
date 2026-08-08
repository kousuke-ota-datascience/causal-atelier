# G4 Trial 001 Test 010 — postgres_and_migration_contract

- Gate: G4
- Trial: 001
- Test item: 010
- Status: NOT_RUN
- Tested implementation commit: `f16c0a7bb25fbe3378585ba78921398638d1ecea`
- Handoff report commit / path: `6c0f10a0eb3429d16f774d72d22a723626da5d03` / `20_implementation_reports/G4_001_implementation_completion_report.md`
- Branch: `prototype/ariadne_mvp_e3`
- Migration head: `20260807_product_0005` (static single head only)
- Started at: NOT_RUN
- Finished at: NOT_RUN

## Purpose

PostgreSQL persistence と migration round trip を検証する。

## Acceptance Criteria

テスト指示書 G4-010 / §16 記載の clean upgrade、downgrade、re-upgrade、single head、PostgreSQL contract。

## Preconditions / Environment

Static `alembic heads` は成功したが、G4-009 coverage failure を先に検出。

## Commands Executed

```bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache uv run alembic -c alembic_product.ini heads
```

PostgreSQL migration executionは未実行。

## Exact Result

- static heads exit code: 0
- observed head: `20260807_product_0005 (head)`
- PostgreSQL test exit code: NOT_RUN
- passed: 0
- failed: 0
- skipped: 0
- duration: 0s for PostgreSQL execution

## Log / Evidence

`NOT_RUN_DUE_TO_PRIOR_FAILURE`: G4-009 `REQUIRED_TEST_COVERAGE_MISSING`。

## Findings

- product defect: not evaluated
- test infrastructure issue: not evaluated
- regression: not evaluated
- deviation: prior mandatory coverage failure
- none: false

## Decision Rationale

Single head の static factだけでは G4-010 を PASS にできない。§14 により高コスト PostgreSQL round trip は未実行。

## Source Modification by Test Agent

NONE
