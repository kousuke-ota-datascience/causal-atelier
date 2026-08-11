# E4-G05 Trial 01 Test 004 — Exploratory Canonical Golden Path

- Project: Ariadne / causal-atelier
- Enhancement: ENH-E4 eliminate dual execution
- Gate: E4-G05
- Trial: 01
- Test Item ID (3-digit): 004
- Status: NOT_RUN
- Tested implementation commit: ddb009875ef4e649f413cb0bb7f7a85f894e2b14
- Handoff report path: docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/20_implementation_reports/G05/Trial01/E4-G05_01_implementation_completion_report.md
- Branch: refactor/ariadne_mvp_e4
- Migration head: 20260809_product_0010
- Working directory: /loc0/bigbrother/repositories/causal-atelier
- Started at: 2026-08-09T11:00:04+00:00
- Finished at: 2026-08-09T11:00:04+00:00
- Duration: PT0S

## 1. Purpose
Prove the real-PostgreSQL Exploratory Product submission Golden Path.

## 2. Acceptance Criteria
AC-002, AC-004, and AC-005.

## 3. Preconditions / Environment
### Runtime
PostgreSQL runner was operational; dedicated Golden Path completion was NOT_RUN.
### External Services
Repository-managed Docker PostgreSQL.
### Environment Variables
N/A.

## 4. Commands Executed
`ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-g05-audit scripts/test/run_product_postgres_tests.sh tests/product/test_enh_e4_g05_phase_a_postgres.py tests/product/test_enh_e4_g05_phase_b_exploratory_postgres.py tests/product/test_enh_e4_g05_phase_c_authority_audit_postgres.py tests/product/test_enh_e4_g05_phase_c_rerun_postgres.py tests/product/test_enh_e4_g05_phase_c_retry_postgres.py tests/product/test_enh_e4_g05_phase_c_revise_postgres.py tests/product/test_enh_e4_g05_phase_d_d1_legacy_claim_shutdown_postgres.py tests/product/test_enh_e4_g05_phase_d_d2_legacy_lifecycle_shutdown_postgres.py tests/product/test_enh_e4_g05_phase_d_d3_global_authority_audit_postgres.py tests/product/test_enh_e4_g02_canonical_execution.py tests/product/test_enh_e4_g03_acceptance_postgres.py tests/product/test_enh_e4_g03_persistent_stage_execution.py tests/product/test_enh_e4_g04_result_artifact_postgres.py tests/product/test_enh_e4_g04_result_artifact_contract.py tests/product/test_postgres_contract.py`

## 5. Exact Result
- passed: 2
- failed: 0
- skipped: 0
- warnings: 0
- exit code: 1

## 6. Log / Evidence
### stdout / stderr
`tests/product/test_enh_e4_g05_phase_b_exploratory_postgres.py` reported 2 passed within the combined run.
### Failure traceback / assertion
The combined required regression invocation failed elsewhere: 6 failed, 32 passed.
### Artifact paths
/tmp/ariadne-g05-audit/run-20260809T105702Z.txt

## 7. Findings
Facts: the Exploratory projection tests passed, but no completed dedicated user-visible submit-to-terminal Golden Path proof was produced.

Interpretation: this is insufficient for item 004 PASS.

## 8. Required Correction
Run the dedicated Exploratory Golden Path after resolving Gate failures.

## 9. Reproduction Procedure
Rerun the command in §4, then execute the dedicated Exploratory node with a fresh reset.

## 10. Expected Result
Returned ID is canonical, old family counts do not increase, and the family projection reads canonical outputs.

## 11. Decision Rationale
Partial positive projection evidence does not prove the entire required path.

## 12. Source Modification by Test Agent
NONE. Only G05 test-report documents were created.

## 13. Supplemental Execution Context
The runner applied migration `20260809_product_0010` successfully.
