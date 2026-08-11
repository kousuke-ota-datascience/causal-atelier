# E4-G04 Trial 01 Test 003 — Canonical Result / Artifact Ownership Persistence

- Project: Ariadne / causal-atelier
- Enhancement: ENH-E4 eliminate dual execution
- Gate: E4-G04
- Trial: 01
- Test Item ID (3-digit): 003
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
Verify durable canonical Result/Artifact ownership after real PostgreSQL reload.

## 2. Acceptance Criteria
E4-G04-AC-001 and E4-G04-AC-002.

## 3. Preconditions / Environment
### Runtime
Python 3.12.13 and repository-managed PostgreSQL 17-alpine.
### External Services
`database_test` in Compose project `ariadne-test`.
### Environment Variables
`ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-g04-trial01-evidence`.

## 4. Commands Executed
`sed -n '1,260p' tests/product/test_enh_e4_g04_result_artifact_postgres.py`

`ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-g04-trial01-evidence scripts/test/run_product_postgres_tests.sh tests/product/test_enh_e4_g04_result_artifact_contract.py tests/product/test_enh_e4_g04_result_artifact_postgres.py tests/product/test_enh_e4_g02_canonical_execution.py tests/product/test_enh_e4_g03_generic_executor_boundary.py tests/product/test_enh_e4_g03_persistent_stage_execution.py tests/product/test_enh_e4_g03_acceptance_postgres.py tests/product/test_postgres_contract.py`

## 5. Exact Result
- passed: 29
- failed: 0
- skipped: 0
- warnings: 0
- exit code: 0

## 6. Log / Evidence
### stdout / stderr
`test_g04_ac001_ac002_postgres_round_trip_typed_result_and_artifact_ownership` passed. It reloads a persisted StageResult and Artifact from a new SQL connection and verifies shared execution, stage, result, scope, and distinct physical object key.
### Failure traceback / assertion
N/A.
### Artifact paths
/tmp/ariadne-g04-trial01-evidence/run-20260809T053910Z.txt

/tmp/ariadne-g04-trial01-evidence/run-20260809T053910Z.metadata.txt

## 7. Findings
The canonical path persists a StageResult and an execution-output Artifact linked to the same canonical Execution, StageExecution, and Result. The real PostgreSQL test rejects a foreign stage and a Result owned by another Execution. The family registry explicitly represents CAUSAL, EXPLORATORY, and PREDICTIVE without a family-specific canonical metadata repository.

## 8. Required Correction
N/A.

## 9. Reproduction Procedure
Run the standardized runner command in section 4 and inspect the named PostgreSQL test.

## 10. Expected Result
Canonical Result/Artifact links survive reload and mismatched ownership is rejected.

## 11. Decision Rationale
The real PostgreSQL round trip and ownership negatives passed.

## 12. Source Modification by Test Agent
NONE. Only test evidence documents were created.

## 13. Supplemental Execution Context
Artifact links are optional at schema level; the tested canonical Causal case exercises all three execution/stage/result associations.
