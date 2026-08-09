# E4-G04 Trial 02 Test 008 — G02 / G03 / PostgreSQL Regression

- Project: Ariadne / causal-atelier
- Enhancement: ENH-E4 eliminate dual execution
- Gate: E4-G04
- Trial: 02
- Test Item ID (3-digit): 008
- Status: PASS
- Tested implementation commit: 9c9db4454e0f08c4d46cb002f723ca6827917564
- Handoff report path: docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/20_implementation_reports/G04/E4-G04_02_implementation_completion_report.md
- Branch: refactor/ariadne_mvp_e4
- Migration head: 20260809_product_0009
- Working directory: /loc0/bigbrother/repositories/causal-atelier
- Started at: 2026-08-09T05:47:13Z
- Finished at: 2026-08-09T05:47:15Z
- Duration: 2 seconds

## 1. Purpose
Verify G02/G03 contracts and G04 remediation together.

## 2. Acceptance Criteria
G02/G03 regression preservation.

## 3. Preconditions / Environment
### Runtime
Python 3.12.13; PostgreSQL 17-alpine.
### External Services
`database_test`.
### Environment Variables
`ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-audit-evidence`.

## 4. Commands Executed
`ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-audit-evidence scripts/test/run_product_postgres_tests.sh tests/product/test_enh_e4_g02_canonical_execution.py tests/product/test_enh_e4_g03_persistent_stage_execution.py tests/product/test_enh_e4_g03_generic_executor_boundary.py tests/product/test_enh_e4_g03_acceptance_postgres.py tests/product/test_enh_e4_g04_result_artifact_contract.py tests/product/test_enh_e4_g04_result_artifact_postgres.py`

## 5. Exact Result
- passed: 27
- failed: 0
- skipped: 0
- warnings: 0
- exit code: 0

## 6. Log / Evidence
### stdout / stderr
27 passed; migration current/head 0009.
### Failure traceback / assertion
N/A.
### Artifact paths
/tmp/ariadne-audit-evidence/run-20260909T055336Z.metadata.txt

## 7. Findings
Execution lifecycle, claim/lease, persistent StageExecution, attempts, and GenericExecutor boundary remain passing.

## 8. Required Correction
N/A.

## 9. Reproduction Procedure
Run section 4.

## 10. Expected Result
No passed G02/G03 contract regresses.

## 11. Decision Rationale
Passed.

## 12. Source Modification by Test Agent
NONE.

## 13. Supplemental Execution Context
No manual PostgreSQL flow used.
