# E4-G04 Trial 01 Test 006 — Artifact-Only Family Contract

- Project: Ariadne / causal-atelier
- Enhancement: ENH-E4 eliminate dual execution
- Gate: E4-G04
- Trial: 01
- Test Item ID (3-digit): 006
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
Verify explicit per-family Result cardinality and Artifact-only decisions.

## 2. Acceptance Criteria
E4-G04-AC-005 and E4-G04-AC-001.

## 3. Preconditions / Environment
### Runtime
Python 3.12.13 and the repository-managed PostgreSQL runner.
### External Services
`database_test` in Compose project `ariadne-test`.
### Environment Variables
`ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-g04-trial01-evidence`.

## 4. Commands Executed
`sed -n '1,220p' src/ariadne/product/workflow/output_contract.py`

`ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-g04-trial01-evidence scripts/test/run_product_postgres_tests.sh tests/product/test_enh_e4_g04_result_artifact_contract.py tests/product/test_enh_e4_g04_result_artifact_postgres.py tests/product/test_enh_e4_g02_canonical_execution.py tests/product/test_enh_e4_g03_generic_executor_boundary.py tests/product/test_enh_e4_g03_persistent_stage_execution.py tests/product/test_enh_e4_g03_acceptance_postgres.py tests/product/test_postgres_contract.py`

## 5. Exact Result
- passed: 29
- failed: 0
- skipped: 0
- warnings: 0
- exit code: 0

## 6. Log / Evidence
### stdout / stderr
The G04 contract test passed with the shared runner. CAUSAL and EXPLORATORY require one StageResult and reject artifact-only output. PREDICTIVE requires zero Results and explicitly allows artifact-only output.
### Failure traceback / assertion
N/A.
### Artifact paths
/tmp/ariadne-g04-trial01-evidence/run-20260809T053910Z.txt

/tmp/ariadne-g04-trial01-evidence/run-20260809T053910Z.metadata.txt

## 7. Findings
All three AnalysisFamily values have an explicit typed workflow contract. The tested Predictive case persists an Artifact without a synthetic Result; the Causal artifact-only attempt is rejected.

## 8. Required Correction
N/A.

## 9. Reproduction Procedure
Run the standardized runner command in section 4 and inspect `FAMILY_OUTPUT_CONTRACTS`.

## 10. Expected Result
Every family has an explicit allowed Result level/cardinality and artifact-only policy, including one allowed and one rejected behavior.

## 11. Decision Rationale
The explicit registry and both required behaviors passed.

## 12. Source Modification by Test Agent
NONE. Only test evidence documents were created.

## 13. Supplemental Execution Context
This item does not claim G05 route convergence; it verifies the G04 contract only.
