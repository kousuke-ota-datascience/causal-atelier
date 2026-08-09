# E4-G03 Trial 02 Test 002 — Product Migration and StageExecution Schema

- Project: Ariadne / causal-atelier
- Enhancement: ENH-E4 eliminate dual execution
- Gate: E4-G03
- Trial: 02
- Test Item ID (3-digit): 002
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

Verify the Product-only migration and persistent StageExecution schema from a clean PostgreSQL database.

## 2. Acceptance Criteria

E4-G03-AC-001, AC-002, AC-004.

## 3. Preconditions / Environment

### Runtime

Python 3.12 test-only container supplied by the repository-managed runner.

### External Services

Compose `database_test` service on `ariadne-test-network`; isolated `ariadne_test` database.

### Environment Variables

`ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-g03-trial02-evidence`.

## 4. Commands Executed

`ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-g03-trial02-evidence scripts/test/run_product_postgres_tests.sh tests/product/test_enh_e4_g03_generic_executor_boundary.py tests/product/test_enh_e4_g03_persistent_stage_execution.py tests/product/test_enh_e4_g03_acceptance_postgres.py tests/product/test_postgres_contract.py tests/product/test_enh_e4_g02_canonical_execution.py`

## 5. Exact Result

- passed: 22
- failed: 0
- skipped: 0
- warnings: 0
- exit code: 0

## 6. Log / Evidence

### stdout / stderr

Migration output: `20260809_product_0007 -> 20260809_product_0008`; current: `20260809_product_0008 (head)`.

### Failure traceback / assertion

None.

### Artifact paths

`/tmp/ariadne-g03-trial02-evidence/run-20260809T044740Z.txt`

`/tmp/ariadne-g03-trial02-evidence/run-20260809T044740Z.metadata.txt`

## 7. Findings

Migration `0008` has parent `0007`, canonical execution/stage FKs, required uniqueness constraints, attempt persistence, and explicit `CANCELLED` state.

## 8. Required Correction

None.

## 9. Reproduction Procedure

Run the command in section 4 from the repository root.

## 10. Expected Result

The runner resets `ariadne_test`, runs Product migrations only, reaches head, and exits 0.

## 11. Decision Rationale

Clean migration and schema requirements passed through the sole supported PostgreSQL route.

## 12. Source Modification by Test Agent

No source modification; only this report was created.

## 13. Supplemental Execution Context

The runner was cleaned up after execution with the documented Compose down command.
