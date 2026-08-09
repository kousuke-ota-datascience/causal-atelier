# E4-G04 Trial 01 Test 008 — G02 / G03 / PostgreSQL Regression

- Project: Ariadne / causal-atelier
- Enhancement: ENH-E4 eliminate dual execution
- Gate: E4-G04
- Trial: 01
- Test Item ID (3-digit): 008
- Status: PASS
- Tested implementation commit: 3d88781c1b69ba03bb06c0b8f143612b81feb4bf
- Handoff report path: docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/20_implementation_reports/G04/E4-G04_01_implementation_completion_report.md
- Branch: refactor/ariadne_mvp_e4
- Migration head: 20260809_product_0009
- Working directory: /loc0/bigbrother/repositories/causal-atelier
- Started at: 2026-08-09T05:39:10Z
- Finished at: 2026-08-09T05:39:35Z
- Duration: 25 seconds

## 1. Purpose
Verify that G04 does not regress the passed G02 canonical Execution and G03 persistent StageExecution/GenericExecutor contracts.

## 2. Acceptance Criteria
G02/G03 regression preservation; E4-G04 architecture boundary.

## 3. Preconditions / Environment
### Runtime
Python 3.12.13 in the repository-managed test container; PostgreSQL 17-alpine.
### External Services
`database_test`, isolated database `ariadne_test`.
### Environment Variables
`ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-g04-trial01-evidence`.

## 4. Commands Executed
`ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-g04-trial01-evidence scripts/test/run_product_postgres_tests.sh tests/product/test_enh_e4_g04_result_artifact_contract.py tests/product/test_enh_e4_g04_result_artifact_postgres.py tests/product/test_enh_e4_g02_canonical_execution.py tests/product/test_enh_e4_g03_generic_executor_boundary.py tests/product/test_enh_e4_g03_persistent_stage_execution.py tests/product/test_enh_e4_g03_acceptance_postgres.py tests/product/test_postgres_contract.py`

## 5. Exact Result
- passed: 29
- failed: 0
- skipped: 0
- warnings: 0
- exit code: 0

## 6. Log / Evidence
### stdout / stderr
The runner applied migration `20260809_product_0009` and executed: G02 canonical execution (5), G03 GenericExecutor boundary (6), G03 persistent stage (1), G03 acceptance PostgreSQL (6), and PostgreSQL contract (4), all passing.
### Failure traceback / assertion
N/A.
### Artifact paths
/tmp/ariadne-g04-trial01-evidence/run-20260809T053910Z.txt

/tmp/ariadne-g04-trial01-evidence/run-20260809T053910Z.metadata.txt

## 7. Findings
Execution family/lifecycle/claim/lease, retry/rerun/revise/cancel, persistent StageExecution/attempt behavior, stage owner checks, zero-stage prevention, and GenericExecutor non-authority all remain passing. G03 `output_binding` was not treated as Result authority.

## 8. Required Correction
N/A.

## 9. Reproduction Procedure
Run the standardized runner command in section 4.

## 10. Expected Result
All affected G02/G03 and PostgreSQL regression tests pass after migration `0009`.

## 11. Decision Rationale
All required regression nodes passed on the fixed implementation’s report-only descendant.

## 12. Source Modification by Test Agent
NONE. Only test evidence documents were created.

## 13. Supplemental Execution Context
Evidence metadata records run exit code 0 and the exact start/end timestamps.
