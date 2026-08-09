# E4-G05 Trial 02 Test 006 — Cross-Family Authority Contract
- Project: Ariadne / causal-atelier
- Enhancement: ENH-E4 eliminate dual execution
- Gate: E4-G05
- Trial: 02
- Test Item ID (3-digit): 006
- Status: PASS
- Tested implementation commit: ad3e3e124ee47f9cbaa2470b25263b7289795262
- Handoff report path: docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/20_implementation_reports/G05/Trial02/E4-G05_02_implementation_completion_report.md
- Branch: refactor/ariadne_mvp_e4
- Migration head: 20260809_product_0010
- Working directory: /loc0/bigbrother/repositories/causal-atelier
- Started at: 2026-08-09T12:28:19+00:00
- Finished at: 2026-08-09T12:32:00+00:00
- Duration: PT3M41S
## 1. Purpose
Verify common canonical authority across all families.
## 2. Acceptance Criteria
AC-004.
## 3. Preconditions / Environment
### Runtime
Python 3.12.13; pytest 9.0.3.
### External Services
Repository-managed PostgreSQL.
### Environment Variables
`ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-g05-t02-core`.
## 4. Commands Executed
`ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-g05-t02-core scripts/test/run_product_postgres_tests.sh tests/product/test_enh_e4_g05_phase_a_postgres.py tests/product/test_enh_e4_g05_phase_b_exploratory_postgres.py tests/product/test_enh_e4_g05_phase_c_authority_audit_postgres.py tests/product/test_enh_e4_g05_phase_c_rerun_postgres.py tests/product/test_enh_e4_g05_phase_c_revise_postgres.py tests/product/test_enh_e4_g05_phase_d_d2_legacy_lifecycle_shutdown_postgres.py tests/product/test_enh_e4_g05_phase_d_d3_global_authority_audit_postgres.py tests/product/test_enh_e4_g02_canonical_execution.py tests/product/test_enh_e4_g04_result_artifact_postgres.py tests/product/test_enh_e4_g04_result_artifact_contract.py`
## 5. Exact Result
- passed: 24
- failed: 0
- skipped: 0
- warnings: 0
- exit code: 0
## 6. Log / Evidence
### stdout / stderr
Causal/Exploratory/Predictive authority audits and G02/G04 contracts passed.
### Failure traceback / assertion
NONE.
### Artifact paths
/tmp/ariadne-g05-t02-core
## 7. Findings
Facts: canonical claim/stage/output tests pass; family lifecycle authority is rejected.

Interpretation: AC-004 is satisfied.
## 8. Required Correction
NONE.
## 9. Reproduction Procedure
Run §4 plus item 005 retry command.
## 10. Expected Result
All families use the same canonical claim, stage, Result, and Artifact owners.
## 11. Decision Rationale
PASS.
## 12. Source Modification by Test Agent
NONE. Only Trial 02 G05 test-report documents were created.
## 13. Supplemental Execution Context
G03 isolated acceptance evidence is in item 009.
