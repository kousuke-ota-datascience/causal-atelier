# E4-G04 Trial 02 Test 005 — ArtifactStore Compensation / Reconciliation

- Project: Ariadne / causal-atelier
- Enhancement: ENH-E4 eliminate dual execution
- Gate: E4-G04
- Trial: 02
- Test Item ID (3-digit): 005
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
Verify real PostgreSQL rollback after physical store success and cleanup/reconciliation behavior.

## 2. Acceptance Criteria
E4-G04-AC-003 and INV-010.

## 3. Preconditions / Environment
### Runtime
Python 3.12.13; PostgreSQL 17-alpine; deterministic physical-store failure injection.
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
Both parametrized PostgreSQL commit-failure cases passed: cleanup succeeds and cleanup requires reconciliation.
### Failure traceback / assertion
N/A.
### Artifact paths
/tmp/ariadne-audit-evidence/run-20260809T054642Z.txt

/tmp/ariadne-audit-evidence/run-20260809T054642Z.metadata.txt

## 7. Findings
The test flushes metadata to real PostgreSQL, injects failure, rolls back, opens a fresh session, verifies no Result/Artifact metadata remains, verifies physical deletion, and verifies `OutputCompensationError.reconciliation` when deletion fails.

## 8. Required Correction
N/A.

## 9. Reproduction Procedure
Run the command in section 4 and inspect the two parametrized AC-003 nodes.

## 10. Expected Result
No false durable metadata; known physical objects are compensated; cleanup failure is observable.

## 11. Decision Rationale
The missing real-PostgreSQL evidence from Trial 01 is now present and passed.

## 12. Source Modification by Test Agent
NONE.

## 13. Supplemental Execution Context
The failure injector is test instrumentation around a real SQLAlchemy/PostgreSQL transaction, as required by the handoff report.
