# E4-G05 Trial 01 Test 009 — Passed-Gate Regression

- Project: Ariadne / causal-atelier
- Enhancement: ENH-E4 eliminate dual execution
- Gate: E4-G05
- Trial: 01
- Test Item ID (3-digit): 009
- Status: FAIL
- Tested implementation commit: ddb009875ef4e649f413cb0bb7f7a85f894e2b14
- Handoff report path: docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/20_implementation_reports/G05/Trial01/E4-G05_01_implementation_completion_report.md
- Branch: refactor/ariadne_mvp_e4
- Migration head: 20260809_product_0010
- Working directory: /loc0/bigbrother/repositories/causal-atelier
- Started at: 2026-08-09T10:57:02+00:00
- Finished at: 2026-08-09T10:57:25+00:00
- Duration: PT23S

## 1. Purpose
Run required G02/G03/G04/PostgreSQL regression and G05 affected coverage.

## 2. Acceptance Criteria
G05 §10 item 009; preserve G02 identity/claim/lease/mutation, G03 StageExecution/attempt/GenericExecutor, and G04 Result/Artifact contracts.

## 3. Preconditions / Environment
### Runtime
Python 3.12.13, pytest 9.0.3.
### External Services
Repository-managed PostgreSQL 17-alpine; runner reset and migration succeeded.
### Environment Variables
`ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-g05-audit`.

## 4. Commands Executed
`ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-g05-audit scripts/test/run_product_postgres_tests.sh tests/product/test_enh_e4_g05_phase_a_postgres.py tests/product/test_enh_e4_g05_phase_b_exploratory_postgres.py tests/product/test_enh_e4_g05_phase_c_authority_audit_postgres.py tests/product/test_enh_e4_g05_phase_c_rerun_postgres.py tests/product/test_enh_e4_g05_phase_c_retry_postgres.py tests/product/test_enh_e4_g05_phase_c_revise_postgres.py tests/product/test_enh_e4_g05_phase_d_d1_legacy_claim_shutdown_postgres.py tests/product/test_enh_e4_g05_phase_d_d2_legacy_lifecycle_shutdown_postgres.py tests/product/test_enh_e4_g05_phase_d_d3_global_authority_audit_postgres.py tests/product/test_enh_e4_g02_canonical_execution.py tests/product/test_enh_e4_g03_acceptance_postgres.py tests/product/test_enh_e4_g03_persistent_stage_execution.py tests/product/test_enh_e4_g04_result_artifact_postgres.py tests/product/test_enh_e4_g04_result_artifact_contract.py tests/product/test_postgres_contract.py`

## 5. Exact Result
- passed: 32
- failed: 6
- skipped: 0
- warnings: 0
- exit code: 1

## 6. Log / Evidence
### stdout / stderr
38 tests collected; migration current was `20260809_product_0010 (head)`.
### Failure traceback / assertion
Failures: G05 Predictive retry; G05 D1 canonical claim; G03 acceptance AC002, AC005, and materialization count assertion; `test_postgres_contract.py::test_claim_next_is_atomic_across_concurrent_workers`.
### Artifact paths
/tmp/ariadne-g05-audit/run-20260809T105702Z.txt

## 7. Findings
Facts: required regression returned exit 1. An isolated rerun also reproduced the Predictive retry failure.

Interpretation: passed-Gate regression is FAIL. Some combined-run G03 failures are affected by persisted test state, but that does not remove the independent isolated G05 failure.

## 8. Required Correction
Repair the failing behavior and test isolation/order assumptions as applicable, then run the complete required scope on a new fixed SHA.

## 9. Reproduction Procedure
Run the command in §4. For the independent G05 reproduction, run item 005 §4.

## 10. Expected Result
All required affected tests pass with exit code 0.

## 11. Decision Rationale
The required regression command failed; G05 PASS requires it to pass.

## 12. Source Modification by Test Agent
NONE. Only G05 test-report documents were created.

## 13. Supplemental Execution Context
An initial unprivileged attempt failed before tests because Docker socket access was denied; the recorded command is the approved Docker-enabled run.
