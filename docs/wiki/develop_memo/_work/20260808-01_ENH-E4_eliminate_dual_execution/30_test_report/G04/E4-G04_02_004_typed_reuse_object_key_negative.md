# E4-G04 Trial 02 Test 004 — Artifact Semantic ID / Typed Downstream Reuse

- Project: Ariadne / causal-atelier
- Enhancement: ENH-E4 eliminate dual execution
- Gate: E4-G04
- Trial: 02
- Test Item ID (3-digit): 004
- Status: PASS
- Tested implementation commit: 9c9db4454e0f08c4d46cb002f723ca6827917564
- Handoff report path: docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/20_implementation_reports/G04/E4-G04_02_implementation_completion_report.md
- Branch: refactor/ariadne_mvp_e4
- Migration head: 20260809_product_0009
- Working directory: /loc0/bigbrother/repositories/causal-atelier
- Started at: 2026-08-09T05:46:00Z
- Finished at: 2026-08-09T05:48:32Z
- Duration: 2 minutes 32 seconds

## 1. Purpose
Verify the Trial 01 AC-004 remediation: typed Result role and semantic-ID negatives.

## 2. Acceptance Criteria
E4-G04-AC-004 and typed-reuse portions of AC-002.

## 3. Preconditions / Environment
### Runtime
Python 3.12.13; repository-managed pytest and PostgreSQL runner.
### External Services
`database_test` for the shared regression command.
### Environment Variables
`UV_CACHE_DIR=/tmp/ariadne-uv-cache`; `PYTHONDONTWRITEBYTECODE=1`; `ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-audit-evidence`.

## 4. Commands Executed
`UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run pytest -q tests/product/test_enh_e4_g04_result_artifact_contract.py`

`ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-audit-evidence scripts/test/run_product_postgres_tests.sh tests/product/test_enh_e4_g04_result_artifact_postgres.py`

## 5. Exact Result
- passed: 6 unit tests; 3 PostgreSQL tests
- failed: 0
- skipped: 0
- warnings: 0
- exit code: 0

## 6. Log / Evidence
### stdout / stderr
Pure contract test: `6 passed in 1.22s`. PostgreSQL test: `3 passed in 0.69s`.
### Failure traceback / assertion
N/A.
### Artifact paths
/tmp/ariadne-audit-evidence/run-20260809T054642Z.txt

## 7. Findings
`ResultReuseRef` now requires `result_id` and typed `ResultReuseRole`. Raw strings, object_key-only, and content-hash-only references are rejected for Result and Artifact reuse.

## 8. Required Correction
N/A.

## 9. Reproduction Procedure
Run both commands in section 4.

## 10. Expected Result
Only typed semantic IDs satisfy downstream reuse; physical locators and hashes do not.

## 11. Decision Rationale
The Trial 01 AC-004 finding was remediated and all tests passed.

## 12. Source Modification by Test Agent
NONE.

## 13. Supplemental Execution Context
No migration change was needed for this remediation.
