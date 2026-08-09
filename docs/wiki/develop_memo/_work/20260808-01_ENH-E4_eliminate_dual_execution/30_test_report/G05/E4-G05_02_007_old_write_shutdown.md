# E4-G05 Trial 02 Test 007 — Old-Write Shutdown Negative Audit
- Project: Ariadne / causal-atelier
- Enhancement: ENH-E4 eliminate dual execution
- Gate: E4-G05
- Trial: 02
- Test Item ID (3-digit): 007
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
Verify old family new-write shutdown and no fallback.
## 2. Acceptance Criteria
AC-005; TD-001/002/003 support.
## 3. Preconditions / Environment
### Runtime
Python 3.12.13; pytest 9.0.3.
### External Services
PostgreSQL runner for runtime checks.
### Environment Variables
`UV_CACHE_DIR=/tmp/ariadne-uv-cache`; PostgreSQL evidence dirs in items 005/009.
## 4. Commands Executed
`UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run pytest -q tests/product/test_enh_e4_g05_submission_convergence.py tests/product/test_enh_e4_g05_phase_d_d2_legacy_lifecycle_shutdown.py tests/product/test_enh_e4_g05_phase_d_d3_global_authority_audit.py`

`ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-g05-t02-d1-independent scripts/test/run_product_postgres_tests.sh tests/product/test_enh_e4_g05_phase_d_d1_legacy_claim_shutdown_postgres.py`
## 5. Exact Result
- passed: 9
- failed: 0
- skipped: 0
- warnings: 0
- exit code: 0
## 6. Log / Evidence
### stdout / stderr
Static: 7 passed. D1 runtime: 2 passed; D2/D3 runtime are included in core 24 passed.
### Failure traceback / assertion
NONE.
### Artifact paths
/tmp/ariadne-g05-t02-d1-independent; /tmp/ariadne-g05-t02-core
## 7. Findings
Facts: old family claim/process facades reject; static reachability audit and runtime four-table traps pass.

Interpretation: TD-001/002/003 old-write shutdown evidence is satisfied.
## 8. Required Correction
NONE.
## 9. Reproduction Procedure
Run both commands in §4 and core command in item 006.
## 10. Expected Result
New Product paths cannot write/fallback to Family tables.
## 11. Decision Rationale
PASS.
## 12. Source Modification by Test Agent
NONE. Only Trial 02 G05 test-report documents were created.
## 13. Supplemental Execution Context
Retained structural legacy code is unreachable for Product operations and deferred to G07 retirement.
