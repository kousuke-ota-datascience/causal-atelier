# E4-G05 Trial 01 Test 005 — Predictive Canonical Golden Path

- Project: Ariadne / causal-atelier
- Enhancement: ENH-E4 eliminate dual execution
- Gate: E4-G05
- Trial: 01
- Test Item ID (3-digit): 005
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
Prove Predictive canonical lifecycle/claim behavior with persistent stages and unchanged old-family rows.

## 2. Acceptance Criteria
AC-003, AC-004, and AC-005.

## 3. Preconditions / Environment
### Runtime
Python 3.12.13, pytest 9.0.3, PostgreSQL 17-alpine in repository-managed Docker test infrastructure.
### External Services
`database_test` was healthy; reset and migration completed.
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
Migration applied successfully and `20260809_product_0010 (head)` was reported.
### Failure traceback / assertion
`test_g05_phase_c_predictive_retry_is_canonical_and_append_preserving` failed at `tests/product/test_enh_e4_g05_phase_c_retry_postgres.py:236`: after `service.retry(ids["project"], ids["execution"])`, `SqlExecutionRepository.claim_next(...)` returned execution `217d355e-a138-42e8-9c6c-a57bc22700fe`, not expected retried execution `b4330c15-6149-492e-9f8f-44b56c0b0af6`.
### Artifact paths
/tmp/ariadne-g05-audit-isolated-retry/run-20260809T105931Z.txt

## 7. Findings
Facts: the failure reproduces with a fresh runner reset; it is not solely cross-file database residue.

Interpretation: the required canonical retry-to-claim path is not proven and the test contract fails.

## 8. Required Correction
Same-Gate remediation must make the Predictive retry claim contract pass (or correct the test only if its contract is demonstrably invalid, under a new fixed implementation target).

## 9. Reproduction Procedure
Run the command in §4. Do not manually reset or patch the database.

## 10. Expected Result
The retried Predictive execution is returned by canonical `claim_next`, then progresses via persistent StageExecution without family-row changes.

## 11. Decision Rationale
A required real-PostgreSQL Predictive lifecycle assertion failed on an isolated database.

## 12. Source Modification by Test Agent
NONE. Only G05 test-report documents were created.

## 13. Supplemental Execution Context
The initial combined run also failed this same node.
