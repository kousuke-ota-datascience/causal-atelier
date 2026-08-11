# E4-G03 Trial 02 Test 006 — Failure, Retry, Cancel, and Lease Consistency

- Project: Ariadne / causal-atelier
- Enhancement: ENH-E4 eliminate dual execution
- Gate: E4-G03
- Trial: 02
- Test Item ID (3-digit): 006
- Status: PASS
- Tested implementation commit: `bac1814bb713f32b859fbe7e2b445fa6cd557f2b`
- Handoff report path: `docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/20_implementation_reports/G03/E4-G03_02_implementation_completion_report.md`
- Branch: `refactor/ariadne_mvp_e4`
- Migration head: `20260809_product_0008`
- Working directory: `/loc0/bigbrother/repositories/causal-atelier`
- Started at: 2026-08-09T04:47:40Z
- Finished at: 2026-08-09T04:48:01Z
- Duration: 21 seconds

## 1. Purpose

Verify persisted lifecycle consistency between Execution, StageExecution, attempts, cancellation, and lease owner.

## 2. Acceptance Criteria

E4-G03-AC-002, AC-005.

## 3. Preconditions / Environment

### Runtime

Repository-managed Python 3.12 test runner.

### External Services

Real PostgreSQL `database_test`.

### Environment Variables

`ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-g03-trial02-evidence`.

## 4. Commands Executed

The standard runner command in Test 002, including `tests/product/test_enh_e4_g03_acceptance_postgres.py`.

## 5. Exact Result

- passed: 1 dedicated acceptance case (within 22 total)
- failed: 0
- skipped: 0
- warnings: 0
- exit code: 0

## 6. Log / Evidence

### stdout / stderr

`test_g03_ac005_persistent_failure_retry_cancellation_owner_and_invalid_success` passed.

### Failure traceback / assertion

None.

### Artifact paths

`/tmp/ariadne-g03-trial02-evidence/run-20260809T044740Z.txt`

## 7. Findings

The test persists failure, retries with stable IDs and attempts `[1,2]`, cancels terminal/nonterminal stages correctly, rejects wrong and expired owner updates, and rejects invalid parent success.

## 8. Required Correction

None.

## 9. Reproduction Procedure

Run Test 002's standard runner command.

## 10. Expected Result

No durable parent-stage lifecycle contradiction or stale-owner mutation occurs.

## 11. Decision Rationale

All mandatory persisted lifecycle scenarios pass.

## 12. Source Modification by Test Agent

No source modification; only this report was created.

## 13. Supplemental Execution Context

The acceptance test uses the canonical repository/application path and real PostgreSQL.
