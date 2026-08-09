# E4-G04 Trial 01 Test 007 — Canonical Ownership Service / GenericExecutor Boundary

- Project: Ariadne / causal-atelier
- Enhancement: ENH-E4 eliminate dual execution
- Gate: E4-G04
- Trial: 01
- Test Item ID (3-digit): 007
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
Verify the one canonical output metadata authority and retain GenericExecutor as a non-persistence boundary.

## 2. Acceptance Criteria
E4-G04-AC-002, E4-G04-AC-003, and the Gate architecture boundary.

## 3. Preconditions / Environment
### Runtime
Python 3.12.13; repository-managed test container.
### External Services
`database_test` in Compose project `ariadne-test`.
### Environment Variables
`UV_CACHE_DIR=/tmp/ariadne-uv-cache`; `PYTHONDONTWRITEBYTECODE=1`; `ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-g04-trial01-evidence`.

## 4. Commands Executed
`UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run pytest -q tests/product/test_enh_e4_g04_result_artifact_contract.py tests/product/test_enh_e4_g03_generic_executor_boundary.py`

`rg -n -C 3 'ResultReuseRef|ArtifactReuseRef|reuse_result|reuse_artifact|GenericExecutor|OutputOwnershipService|ArtifactStore|\.commit\(' src/ariadne/product/application/output_ownership_service.py src/ariadne/product/workflow/executor.py tests/product/test_enh_e4_g03_generic_executor_boundary.py`

`ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-g04-trial01-evidence scripts/test/run_product_postgres_tests.sh tests/product/test_enh_e4_g04_result_artifact_contract.py tests/product/test_enh_e4_g04_result_artifact_postgres.py tests/product/test_enh_e4_g02_canonical_execution.py tests/product/test_enh_e4_g03_generic_executor_boundary.py tests/product/test_enh_e4_g03_persistent_stage_execution.py tests/product/test_enh_e4_g03_acceptance_postgres.py tests/product/test_postgres_contract.py`

## 5. Exact Result
- passed: 12 unit tests; 29 shared-runner tests
- failed: 0
- skipped: 0
- warnings: 0
- exit code: 0

## 6. Log / Evidence
### stdout / stderr
Unit output was `12 passed in 1.42s`; shared runner output was `29 passed in 2.62s`. Static inspection locates metadata writes and ArtifactStore coordination in `OutputOwnershipService`; G03 boundary tests verify GenericExecutor has no UoW/commit/retry authority.
### Failure traceback / assertion
N/A.
### Artifact paths
/tmp/ariadne-g04-trial01-evidence/run-20260809T053910Z.txt

/tmp/ariadne-g04-trial01-evidence/run-20260809T053910Z.metadata.txt

## 7. Findings
`OutputOwnershipService` is the added canonical G04 metadata writer and coordinates physical store operations. GenericExecutor remains free of Result/Artifact persistence, ArtifactStore ownership, UoW commit, and ownership/cardinality decisions. No new family-specific canonical metadata writer was added in the G04 diff.

## 8. Required Correction
N/A.

## 9. Reproduction Procedure
Run the commands in section 4 from the repository root.

## 10. Expected Result
One canonical G04 output owner exists and GenericExecutor remains a detached workflow executor.

## 11. Decision Rationale
Static and behavioral boundary evidence passed.

## 12. Source Modification by Test Agent
NONE. Only test evidence documents were created.

## 13. Supplemental Execution Context
Old transitional writers remain under TD-003 and are not interpreted as a new canonical G04 authority.
