# E4-G05 Trial 02 Test 008 — Mutation / Read Projection / CLI Boundary
- Project: Ariadne / causal-atelier
- Enhancement: ENH-E4 eliminate dual execution
- Gate: E4-G05
- Trial: 02
- Test Item ID (3-digit): 008
- Status: PASS
- Tested implementation commit: ad3e3e124ee47f9cbaa2470b25263b7289795262
- Handoff report path: docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/20_implementation_reports/G05/Trial02/E4-G05_02_implementation_completion_report.md
- Branch: refactor/ariadne_mvp_e4
- Migration head: 20260809_product_0010
- Working directory: /loc0/bigbrother/repositories/causal-atelier
- Started at: 2026-08-09T12:25:24+00:00
- Finished at: 2026-08-09T12:32:00+00:00
- Duration: PT6M36S
## 1. Purpose
Verify cancel/retry/rerun/revise/read/CLI authority boundaries.
## 2. Acceptance Criteria
AC-001..005 and G05 §10 item 008.
## 3. Preconditions / Environment
### Runtime
Python 3.12.13; pytest 9.0.3.
### External Services
Repository PostgreSQL runner.
### Environment Variables
`UV_CACHE_DIR=/tmp/ariadne-uv-cache`; PostgreSQL evidence dirs in §6.
## 4. Commands Executed
`UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run pytest -q tests/product/test_enh_e4_g05_submission_convergence.py tests/product/test_enh_e4_g05_phase_d_d2_legacy_lifecycle_shutdown.py tests/product/test_enh_e4_g05_phase_d_d3_global_authority_audit.py`

`ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-g05-t02-retry-independent scripts/test/run_product_postgres_tests.sh tests/product/test_enh_e4_g05_phase_c_retry_postgres.py`
## 5. Exact Result
- passed: 8
- failed: 0
- skipped: 0
- warnings: 0
- exit code: 0
## 6. Log / Evidence
### stdout / stderr
Static boundary tests 7 passed; independent Predictive retry 1 passed. Core partition passed rerun/revise and Exploratory projection.
### Failure traceback / assertion
NONE.
### Artifact paths
/tmp/ariadne-g05-t02-retry-independent; /tmp/ariadne-g05-t02-core
## 7. Findings
Facts: exposed mutation paths delegate/reject before legacy writes; worker CLI claims canonical execution only.

Interpretation: canonical mutation/read/CLI boundary is satisfied.
## 8. Required Correction
NONE.
## 9. Reproduction Procedure
Run §4 and item 006 core command.
## 10. Expected Result
Supported mutations and reads are canonical; no hidden old persistence.
## 11. Decision Rationale
PASS.
## 12. Source Modification by Test Agent
NONE. Only Trial 02 G05 test-report documents were created.
## 13. Supplemental Execution Context
No low-level Product persistence was observed in the static audit.
