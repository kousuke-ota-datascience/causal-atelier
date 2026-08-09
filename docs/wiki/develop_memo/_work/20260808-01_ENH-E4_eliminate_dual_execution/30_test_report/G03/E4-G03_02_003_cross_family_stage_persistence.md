# E4-G03 Trial 02 Test 003 — Cross-Family Canonical Stage Persistence

- Project: Ariadne / causal-atelier
- Enhancement: ENH-E4 eliminate dual execution
- Gate: E4-G03
- Trial: 02
- Test Item ID (3-digit): 003
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

Verify durable canonical StageExecution children for all analysis families.

## 2. Acceptance Criteria

E4-G03-AC-001, AC-004.

## 3. Preconditions / Environment

### Runtime

Repository-managed Python 3.12 test runner.

### External Services

Real PostgreSQL `database_test` service.

### Environment Variables

`ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-g03-trial02-evidence`.

## 4. Commands Executed

The standard runner command in Test 002, including `tests/product/test_enh_e4_g03_acceptance_postgres.py`.

## 5. Exact Result

- passed: 3 parameterized family cases (within 22 total)
- failed: 0
- skipped: 0
- warnings: 0
- exit code: 0

## 6. Log / Evidence

### stdout / stderr

`test_g03_ac001_canonical_application_path_persists_and_reloads_each_family` passed for EXPLORATORY, CAUSAL, and PREDICTIVE.

### Failure traceback / assertion

None.

### Artifact paths

`/tmp/ariadne-g03-trial02-evidence/run-20260809T044740Z.txt`

## 7. Findings

Each family submitted through `ExecutionService`, persisted two children, and reloaded them in a new session with the same execution ID and ordered keys `prepare`, `analyze`.

## 8. Required Correction

None.

## 9. Reproduction Procedure

Run Test 002's standard runner command.

## 10. Expected Result

Every canonical family has at least one persistent child owned by its canonical Execution.

## 11. Decision Rationale

The real PostgreSQL parameterized acceptance test directly establishes the required family matrix.

## 12. Source Modification by Test Agent

No source modification; only this report was created.

## 13. Supplemental Execution Context

The test reloads through `SqlStageExecutionRepository`, not runner-local state.
