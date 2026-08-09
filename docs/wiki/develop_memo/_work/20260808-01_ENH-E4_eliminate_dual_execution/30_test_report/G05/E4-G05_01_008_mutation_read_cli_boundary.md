# E4-G05 Trial 01 Test 008 — Mutation / Read Projection / CLI Boundary

- Project: Ariadne / causal-atelier
- Enhancement: ENH-E4 eliminate dual execution
- Gate: E4-G05
- Trial: 01
- Test Item ID (3-digit): 008
- Status: FAIL
- Tested implementation commit: ddb009875ef4e649f413cb0bb7f7a85f894e2b14
- Handoff report path: docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/20_implementation_reports/G05/Trial01/E4-G05_01_implementation_completion_report.md
- Branch: refactor/ariadne_mvp_e4
- Migration head: 20260809_product_0010
- Working directory: /loc0/bigbrother/repositories/causal-atelier
- Started at: 2026-08-09T10:59:31+00:00
- Finished at: 2026-08-09T11:00:03+00:00
- Duration: PT32S

## 1. Purpose
Verify canonical mutation semantics and supported read/CLI boundaries.

## 2. Acceptance Criteria
AC-001 through AC-005; REQ-007 through REQ-010 and REQ-033/034.

## 3. Preconditions / Environment
### Runtime
Python 3.12.13, pytest 9.0.3, PostgreSQL 17-alpine.
### External Services
Repository-managed Docker PostgreSQL with successful reset/migration.
### Environment Variables
`ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-g05-audit-isolated-retry`.

## 4. Commands Executed
`ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-g05-audit-isolated-retry scripts/test/run_product_postgres_tests.sh tests/product/test_enh_e4_g05_phase_c_retry_postgres.py`

## 5. Exact Result
- passed: 0
- failed: 1
- skipped: 0
- warnings: 0
- exit code: 1

## 6. Log / Evidence
### stdout / stderr
The runner migrated to `20260809_product_0010` and executed one Predictive retry test.
### Failure traceback / assertion
After successful `service.retry`, canonical `claim_next` returned a different queued execution; assertion failed at `tests/product/test_enh_e4_g05_phase_c_retry_postgres.py:236`.
### Artifact paths
/tmp/ariadne-g05-audit-isolated-retry/run-20260809T105931Z.txt

## 7. Findings
Facts: the retry mutation/claim chain fails in a fresh real-PostgreSQL run.

Interpretation: canonical mutation semantics required by this item are not satisfied. Read and CLI inventory were not credited as substitutes.

## 8. Required Correction
Fix the Predictive retry-to-claim contract and execute the full mutation/read/CLI matrix on a new fixed SHA.

## 9. Reproduction Procedure
Run the command in §4.

## 10. Expected Result
Each exposed family mutation uses canonical semantics, its data is visible through the family read projection, and CLI has no hidden old persistence.

## 11. Decision Rationale
One required exposed mutation fails; PASS is impossible.

## 12. Source Modification by Test Agent
NONE. Only G05 test-report documents were created.

## 13. Supplemental Execution Context
Static CLI/legacy-boundary tests passed but do not negate the runtime mutation failure.
