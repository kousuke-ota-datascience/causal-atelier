# E4-G04 Trial 01 Test 005 — ArtifactStore Compensation / Reconciliation

- Project: Ariadne / causal-atelier
- Enhancement: ENH-E4 eliminate dual execution
- Gate: E4-G04
- Trial: 01
- Test Item ID (3-digit): 005
- Status: FAIL
- Tested implementation commit: 3d88781c1b69ba03bb06c0b8f143612b81feb4bf
- Handoff report path: docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/20_implementation_reports/G04/E4-G04_01_implementation_completion_report.md
- Branch: refactor/ariadne_mvp_e4
- Migration head: 20260809_product_0009
- Working directory: /loc0/bigbrother/repositories/causal-atelier
- Started at: 2026-08-09T05:35:49Z
- Finished at: 2026-08-09T05:40:17Z
- Duration: 4 minutes 28 seconds

## 1. Purpose
Verify compensation and reconciliation behavior, including real PostgreSQL metadata durability/rollback.

## 2. Acceptance Criteria
E4-G04-AC-003 and INV-010.

## 3. Preconditions / Environment
### Runtime
Python 3.12.13; repository-managed PostgreSQL 17-alpine for the shared runner; deterministic in-memory ArtifactStore/UoW doubles for the existing failure tests.
### External Services
`database_test` in Compose project `ariadne-test`.
### Environment Variables
`ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-g04-trial01-evidence`.

## 4. Commands Executed
`sed -n '1,300p' src/ariadne/product/application/output_ownership_service.py`

`sed -n '1,360p' tests/product/test_enh_e4_g04_result_artifact_contract.py`

`sed -n '1,260p' tests/product/test_enh_e4_g04_result_artifact_postgres.py`

`ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-g04-trial01-evidence scripts/test/run_product_postgres_tests.sh tests/product/test_enh_e4_g04_result_artifact_contract.py tests/product/test_enh_e4_g04_result_artifact_postgres.py tests/product/test_enh_e4_g02_canonical_execution.py tests/product/test_enh_e4_g03_generic_executor_boundary.py tests/product/test_enh_e4_g03_persistent_stage_execution.py tests/product/test_enh_e4_g03_acceptance_postgres.py tests/product/test_postgres_contract.py`

## 5. Exact Result
- passed: 29 shared-runner tests; unit doubles cover three injected failure scenarios
- failed: 1 audit finding
- skipped: 0
- warnings: 0
- exit code: 1

## 6. Log / Evidence
### stdout / stderr
Shared runner output is `29 passed in 2.62s`, but the only G04 PostgreSQL test is the successful ownership round-trip. The DB-commit failure test constructs `MemoryUow(commit_failure=True)`; its rollback is a no-op and it is not a PostgreSQL test.
### Failure traceback / assertion
Coverage failure: 07 item 005 and 06 §15.3 require real PostgreSQL for metadata durability/rollback assertions. No test injects a SQL commit/flush failure after physical store success and then reloads PostgreSQL to prove metadata was not committed.
### Artifact paths
/tmp/ariadne-g04-trial01-evidence/run-20260809T053910Z.txt

/tmp/ariadne-g04-trial01-evidence/run-20260809T053910Z.metadata.txt

## 7. Findings
Fact: deterministic tests cover store failure before metadata, partial multi-artifact failure, normal cleanup after a double’s commit failure, and cleanup-failure reconciliation visibility. Fact: their DB failure path uses `MemoryUow`, not real PostgreSQL. Conclusion: the mandatory real-PostgreSQL durability/rollback evidence is missing; passing shared-runner tests do not establish it.

## 8. Required Correction
Add a real PostgreSQL failure-injection test that fails metadata flush/commit after `ArtifactStorePort.store` succeeds, reloads with a new session, proves Result/Artifact metadata are absent, proves cleanup occurs, and asserts reconciliation context when cleanup fails.

## 9. Reproduction Procedure
Run the standardized runner command in section 4 and inspect the two G04 test files. Confirm that the PostgreSQL file contains only the successful ownership round-trip and the commit-failure test uses `MemoryUow`.

## 10. Expected Result
DB failure after physical storage leaves no durable false metadata in real PostgreSQL, cleans known physical objects, and surfaces cleanup failure as reconciliation data.

## 11. Decision Rationale
Mandatory AC-003 coverage is missing. This is a required automated-coverage defect and therefore FAIL.

## 12. Source Modification by Test Agent
NONE. Only test evidence documents were created.

## 13. Supplemental Execution Context
No manual PostgreSQL workaround was used; only the repository-managed runner was used.
