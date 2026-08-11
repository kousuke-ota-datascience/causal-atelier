# E4-G05 Trial 01 Test 007 — Old-Write Shutdown Negative Audit

- Project: Ariadne / causal-atelier
- Enhancement: ENH-E4 eliminate dual execution
- Gate: E4-G05
- Trial: 01
- Test Item ID (3-digit): 007
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
Verify old family new-write shutdown, row-count negative, and no fallback.

## 2. Acceptance Criteria
AC-005; TD-001, TD-002, and TD-003 closure support.

## 3. Preconditions / Environment
### Runtime
NOT_RUN after decisive failures.
### External Services
N/A.
### Environment Variables
N/A.

## 4. Commands Executed
`UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run pytest -q tests/product/test_enh_e4_g05_submission_convergence.py tests/product/test_enh_e4_g05_phase_d_d2_legacy_lifecycle_shutdown.py tests/product/test_enh_e4_g05_phase_d_d3_global_authority_audit.py`

## 5. Exact Result
- passed: 7
- failed: 0
- skipped: 0
- warnings: 0
- exit code: 0

## 6. Log / Evidence
### stdout / stderr
Static G05 boundary tests passed in 4.47 seconds.
### Failure traceback / assertion
NONE.
### Artifact paths
NONE.

## 7. Findings
Facts: partial static negative tests passed.

Interpretation: the full required static reachable-write audit plus runtime Causal/Exploratory/Predictive before/after count matrix was not completed, so this item is NOT_RUN rather than PASS.

## 8. Required Correction
After remediation, perform the complete static and runtime matrix required by G05 §10 item 007.

## 9. Reproduction Procedure
Run the command in §4, then run the specified real-PostgreSQL family count tests with fresh runner resets.

## 10. Expected Result
No Product new path writes old family execution/stage/result/artifact tables and no canonical-failure fallback occurs.

## 11. Decision Rationale
Partial static coverage is not sufficient evidence for the runtime-negative contract.

## 12. Source Modification by Test Agent
NONE. Only G05 test-report documents were created.

## 13. Supplemental Execution Context
The initial `uv run` without `UV_CACHE_DIR` failed before test start because its default cache was read-only; the recorded command is the successful rerun.
