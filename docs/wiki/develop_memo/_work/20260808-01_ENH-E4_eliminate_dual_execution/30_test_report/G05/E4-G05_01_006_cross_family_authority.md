# E4-G05 Trial 01 Test 006 — Cross-Family Authority Contract

- Project: Ariadne / causal-atelier
- Enhancement: ENH-E4 eliminate dual execution
- Gate: E4-G05
- Trial: 01
- Test Item ID (3-digit): 006
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
Prove one canonical claim/stage/result/artifact authority across Causal, Exploratory, and Predictive.

## 2. Acceptance Criteria
AC-004.

## 3. Preconditions / Environment
### Runtime
Python 3.12.13, pytest 9.0.3, repository-managed PostgreSQL.
### External Services
Docker PostgreSQL healthy; runner reset and migrated to `20260809_product_0010`.
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
The command collected 38 tests. Causal/Exploratory-related tests and several authority audits passed.
### Failure traceback / assertion
Predictive retry canonical claim failed; G03 claim regressions also returned pre-existing queued executions rather than the execution seeded by each test.
### Artifact paths
/tmp/ariadne-g05-audit/run-20260809T105702Z.txt

## 7. Findings
Facts: not all required family claim paths passed.

Interpretation: one shared authoritative claim contract across all three families is not proven.

## 8. Required Correction
Repair/re-baseline claim ordering and isolation semantics, then rerun the cross-family contract on a fixed SHA.

## 9. Reproduction Procedure
Run the command in §4, then run the isolated Predictive retry command from item 005.

## 10. Expected Result
Each family is handled by canonical Execution claim, persistent stages, canonical Results, and canonical Artifacts.

## 11. Decision Rationale
AC-004 requires all families; any failing required family path prevents PASS.

## 12. Source Modification by Test Agent
NONE. Only G05 test-report documents were created.

## 13. Supplemental Execution Context
The single invocation reset only at invocation start; isolated Predictive retry also failed, confirming a substantive unresolved failure.
