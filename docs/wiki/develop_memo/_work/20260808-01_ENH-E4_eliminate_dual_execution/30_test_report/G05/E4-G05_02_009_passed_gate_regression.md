# E4-G05 Trial 02 Test 009 — Passed-Gate Regression
- Project: Ariadne / causal-atelier
- Enhancement: ENH-E4 eliminate dual execution
- Gate: E4-G05
- Trial: 02
- Test Item ID (3-digit): 009
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
Verify G02/G03/G04 and PostgreSQL contract regression using clean semantic partitions.
## 2. Acceptance Criteria
G05 §10 item 009.
## 3. Preconditions / Environment
### Runtime
Python 3.12.13; pytest 9.0.3.
### External Services
Every recorded invocation resets repository-managed PostgreSQL.
### Environment Variables
`ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-g05-t02-core`, `/tmp/ariadne-g05-t02-g03-independent`, and `/tmp/ariadne-g05-t02-contract-independent`.
## 4. Commands Executed
`ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-g05-t02-g03-independent scripts/test/run_product_postgres_tests.sh tests/product/test_enh_e4_g03_acceptance_postgres.py`

`ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-g05-t02-contract-independent scripts/test/run_product_postgres_tests.sh tests/product/test_postgres_contract.py`

`ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-g05-t02-core scripts/test/run_product_postgres_tests.sh tests/product/test_enh_e4_g05_phase_a_postgres.py tests/product/test_enh_e4_g05_phase_b_exploratory_postgres.py tests/product/test_enh_e4_g05_phase_c_authority_audit_postgres.py tests/product/test_enh_e4_g05_phase_c_rerun_postgres.py tests/product/test_enh_e4_g05_phase_c_revise_postgres.py tests/product/test_enh_e4_g05_phase_d_d2_legacy_lifecycle_shutdown_postgres.py tests/product/test_enh_e4_g05_phase_d_d3_global_authority_audit_postgres.py tests/product/test_enh_e4_g02_canonical_execution.py tests/product/test_enh_e4_g04_result_artifact_postgres.py tests/product/test_enh_e4_g04_result_artifact_contract.py`

`ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-g05-t02-g03-persistent-independent scripts/test/run_product_postgres_tests.sh tests/product/test_enh_e4_g03_persistent_stage_execution.py`

`UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run pytest -q tests/product/test_enh_e4_g03_generic_executor_boundary.py`
## 5. Exact Result
- passed: 41
- failed: 0
- skipped: 0
- warnings: 0
- exit code: 0
## 6. Log / Evidence
### stdout / stderr
Core: 24 passed; isolated G03 acceptance: 6 passed; isolated persistent StageExecution: 1 passed; GenericExecutor boundary: 6 passed; isolated contract: 4 passed.
### Failure traceback / assertion
NONE.
### Artifact paths
/tmp/ariadne-g05-t02-core; /tmp/ariadne-g05-t02-g03-independent; /tmp/ariadne-g05-t02-g03-persistent-independent; /tmp/ariadne-g05-t02-contract-independent
## 7. Findings
Facts: G02/G04 in core, all three G03 files in their valid runner modes, and atomic claim contract isolated all passed. An initial mixed pure invocation attempted the PostgreSQL-marked persistent-stage test and failed only because no repository-managed PostgreSQL runner was used; its proper runner rerun passed and is the acceptance evidence.

Interpretation: clean DB per semantic partition is required because the former all-in-one composition violates global queue/global-empty test assumptions; it is not an implementation failure.
## 8. Required Correction
NONE.
## 9. Reproduction Procedure
Run every command in §4.
## 10. Expected Result
All affected passed-Gate contracts pass with exit code 0.
## 11. Decision Rationale
PASS; required semantics passed under valid clean-database isolation boundaries.
## 12. Source Modification by Test Agent
NONE. Only Trial 02 G05 test-report documents were created.
## 13. Supplemental Execution Context
The obsolete single combined command remains unsuitable as a single test partition, not as a product acceptance condition.
