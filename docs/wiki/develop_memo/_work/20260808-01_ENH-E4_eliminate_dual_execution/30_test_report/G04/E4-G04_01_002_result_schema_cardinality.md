# E4-G04 Trial 01 Test 002 — Product Migration / Result Level / Cardinality Audit

- Project: Ariadne / causal-atelier
- Enhancement: ENH-E4 eliminate dual execution
- Gate: E4-G04
- Trial: 01
- Test Item ID (3-digit): 002
- Status: PASS
- Tested implementation commit: 3d88781c1b69ba03bb06c0b8f143612b81feb4bf
- Handoff report path: docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/20_implementation_reports/G04/E4-G04_01_implementation_completion_report.md
- Branch: refactor/ariadne_mvp_e4
- Migration head: 20260809_product_0009
- Working directory: /loc0/bigbrother/repositories/causal-atelier
- Started at: 2026-08-09T05:35:49Z
- Finished at: 2026-08-09T05:39:35Z
- Duration: 3 minutes 46 seconds

## 1. Purpose
Verify the G04 Product migration and explicit Result level/cardinality ownership contract.

## 2. Acceptance Criteria
E4-G04-AC-001, E4-G04-AC-002, and Product migration.

## 3. Preconditions / Environment
### Runtime
Python 3.12.13 in the repository-managed test container; PostgreSQL 17-alpine.
### External Services
Repository-managed Compose service `database_test`, database `ariadne_test`.
### Environment Variables
`ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-g04-trial01-evidence`.

## 4. Commands Executed
`sed -n '1,260p' product_migrations/versions/20260809_product_0009_enh_e4_g04_result_artifact_ownership.py`

`ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-g04-trial01-evidence scripts/test/run_product_postgres_tests.sh tests/product/test_enh_e4_g04_result_artifact_contract.py tests/product/test_enh_e4_g04_result_artifact_postgres.py tests/product/test_enh_e4_g02_canonical_execution.py tests/product/test_enh_e4_g03_generic_executor_boundary.py tests/product/test_enh_e4_g03_persistent_stage_execution.py tests/product/test_enh_e4_g03_acceptance_postgres.py tests/product/test_postgres_contract.py`

## 5. Exact Result
- passed: 29
- failed: 0
- skipped: 0
- warnings: 0
- exit code: 0

## 6. Log / Evidence
### stdout / stderr
The standardized runner reset `ariadne_test`, upgraded through `20260809_product_0009`, confirmed `20260809_product_0009 (head)`, and reported `29 passed in 2.62s`.
### Failure traceback / assertion
N/A.
### Artifact paths
/tmp/ariadne-g04-trial01-evidence/run-20260809T053910Z.txt

/tmp/ariadne-g04-trial01-evidence/run-20260809T053910Z.metadata.txt

## 7. Findings
Migration `0009` is a direct child of `0008`; it persists `result_level` and `stage_execution_id`, has allowed-level and level/stage checks, and applies composite ownership FKs. G04 tests reject ExecutionResult-with-stage, StageResult-without-stage, foreign execution ownership, and cardinality violations at the domain/service boundary. `result_type` remains independent of `result_level`.

## 8. Required Correction
N/A.

## 9. Reproduction Procedure
Run the standardized runner command in section 4; inspect its migration head and pytest output.

## 10. Expected Result
Clean Product migration reaches `20260809_product_0009` and Result level/stage ownership constraints are enforced.

## 11. Decision Rationale
The real PostgreSQL migration and relevant ownership/cardinality tests passed.

## 12. Source Modification by Test Agent
NONE. Only test evidence documents were created.

## 13. Supplemental Execution Context
The runner records HEAD `180c3e3…`; item 001 proves it is a report-only descendant of the fixed implementation SHA.
