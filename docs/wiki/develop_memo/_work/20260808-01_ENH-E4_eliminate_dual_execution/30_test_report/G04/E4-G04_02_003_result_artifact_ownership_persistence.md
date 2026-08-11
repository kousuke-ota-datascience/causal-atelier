# E4-G04 Trial 02 Test 003 — Canonical Result / Artifact Ownership Persistence

- Project: Ariadne / causal-atelier
- Enhancement: ENH-E4 eliminate dual execution
- Gate: E4-G04
- Trial: 02
- Test Item ID (3-digit): 003
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
Verify canonical Result/Artifact persistence remains intact after the remediation.

## 2. Acceptance Criteria
E4-G04-AC-001 and E4-G04-AC-002.

## 3. Preconditions / Environment
### Runtime
Python 3.12.13; PostgreSQL 17-alpine.
### External Services
Repository-managed `database_test`.
### Environment Variables
`ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-audit-evidence`.

## 4. Commands Executed
`ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-audit-evidence scripts/test/run_product_postgres_tests.sh tests/product/test_enh_e4_g04_result_artifact_postgres.py`

## 5. Exact Result
- passed: 3
- failed: 0
- skipped: 0
- warnings: 0
- exit code: 0

## 6. Log / Evidence
### stdout / stderr
The canonical PostgreSQL round-trip and ownership-negative tests passed.
### Failure traceback / assertion
N/A.
### Artifact paths
/tmp/ariadne-audit-evidence/run-20260809T054642Z.txt

/tmp/ariadne-audit-evidence/run-20260809T054642Z.metadata.txt

## 7. Findings
Result and Artifact execution/stage/result associations survive fresh-session reload; foreign ownership remains rejected.

## 8. Required Correction
N/A.

## 9. Reproduction Procedure
Run the command in section 4.

## 10. Expected Result
All canonical ownership persistence tests pass on real PostgreSQL.

## 11. Decision Rationale
The test passed.

## 12. Source Modification by Test Agent
NONE.

## 13. Supplemental Execution Context
The remediation changed typed reuse and failure-test coverage only; migration/schema remained unchanged.
