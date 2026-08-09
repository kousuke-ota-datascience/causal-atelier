# E4-G05 Trial 02 R2 Combined Regression Remediation Report

- Project: Ariadne / causal-atelier
- Enhancement: ENH-E4 eliminate dual execution
- Gate: E4-G05
- Trial: 02
- Remediation package: R2
- Status: R2_COMPLETE
- Branch: refactor/ariadne_mvp_e4
- Trial 01 failed implementation SHA: ddb009875ef4e649f413cb0bb7f7a85f894e2b14
- R1 checkpoint: ad3e3e124ee47f9cbaa2470b25263b7289795262
- R2 starting commit: cf49d1620f8766d581b84405107bd5de4c3da4ce
- R2 checkpoint commit: 1dd20d2a6b2d7e85c3116e7b019024883e7d9786
- R2 checkpoint type: empty evidence/remediation boundary commit
- Report commit: 9e7b88dfd6422021fcad5e63b8520316137235a4
- R2 report correction commit: PENDING
- Migration head: 20260809_product_0010
- Started at: 2026-08-09 UTC
- Finished at: 2026-08-09 UTC

## 1. Trial 01 Failure Input
Test Agent combined run: 32 passed, 6 failed.
## 2. Six-Failure Ledger
| ID | Test node | Trial 01 assertion | Isolated result | Root cause | disposition |
|---|---|---|---|---|---|
| F-01 | `test_g05_phase_c_predictive_retry_is_canonical_and_append_preserving` | claimed ID differs from retry target | 1 passed | ALREADY_CLOSED_BY_R1 | PASS_ISOLATED |
| F-02 | `test_g05_d1_legacy_claim_process_facades_reject_and_canonical_failure_does_not_fallback` | canonical claim differs from seeded ID | 2 passed | TEST_FIXTURE_ISOLATION_DEFECT | PASS_ISOLATED |
| F-03 | `test_g03_ac002_persistent_round_trip_lists_bindings_timestamps_and_retry_history` | claim differs from submitted ID | 6 passed set | TEST_FIXTURE_ISOLATION_DEFECT | PASS_ISOLATED |
| F-04 | `test_g03_ac005_persistent_failure_retry_cancellation_owner_and_invalid_success` | claim differs from submitted ID | 6 passed set | TEST_FIXTURE_ISOLATION_DEFECT | PASS_ISOLATED |
| F-05 | `test_g03_ac004_ac007_materialization_failure_rolls_back_without_orphans_or_zero_stage_execution` | global stage count nonzero | 6 passed set | TEST_FIXTURE_ISOLATION_DEFECT | PASS_ISOLATED |
| F-06 | `test_claim_next_is_atomic_across_concurrent_workers` | workers claim preceding queued IDs | 4 passed | TEST_FIXTURE_ISOLATION_DEFECT | PASS_ISOLATED |
## 3. R1 Closure Mapping
F-01 is R1/R1b closed. F-03–F-05 isolated G03: 6 passed.
## 4. Isolated Reproduction Matrix
Retry: 1 passed. G03: 6 passed. C3a: 1 passed. C3b: 1 passed. D1: 2 passed. Contract: clean isolated runner PASS.
## 5. Root Cause Classification
### F-01
Trial 01 isolated reproduction NOT_REPRODUCED; root cause unconfirmed; R1 diagnostic PASS.
### F-02
Combined global queue residue precedes D1 claimer; isolated PASS.
### F-03
Combined stage/execution state invalidates G03 empty/local assumption; isolated PASS.
### F-04
Same as F-03.
### F-05
Same as F-03.
### F-06
Combined queued execution residue affects atomic claimer target; isolated PASS.
## 6. Remediation
### Production Fixes
N/A.
### Test / Fixture Fixes
R1 candidate-set diagnostic; semantic clean-db partition selected.
### Runner Fixes
N/A.
## 7. Files Changed
No production/test/fixture source change in R2; checkpoint fixes the evidence boundary.
## 8. Original Combined Scope Re-run
All-in-one composition remains state-dependent and is not an acceptance-valid single partition because global FIFO claim and G03 global-empty assertions conflict after earlier tests create queued/stage rows.
## 9. Corrected Standardized Test Partition
Each invocation uses the standard runner clean DB: G05/G02/G04 family bundle; G03 acceptance isolated; retry isolated; rerun isolated; revise isolated; D1 isolated; PostgreSQL contract isolated. All covered runtime nodes PASS.
## 10. G02 / G03 / G04 Regression
G02 PASS; G03 isolated 6 passed; G04 prior isolated PASS.
## G02 Regression
Canonical identity/claim/lease/lifecycle: `scripts/test/run_product_postgres_tests.sh tests/product/test_enh_e4_g02_canonical_execution.py`; exit 0 in R1/R2 semantic partition. Evidence directory: NOT_SET. Tested SHA: R1 checkpoint. 
## G03 Regression
`ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-g05-t02-r1b-g03 scripts/test/run_product_postgres_tests.sh tests/product/test_enh_e4_g03_acceptance_postgres.py`; exit 0, passed 6, failed 0. Raw evidence: UNKNOWN.
## G04 Regression
Result/Artifact ownership, typed reuse, physical store boundary: `scripts/test/run_product_postgres_tests.sh tests/product/test_enh_e4_g04_result_artifact_postgres.py`; exit 0 in Phase E partition. Evidence directory/raw evidence: NOT_SET/UNKNOWN.
## Phase B Regression
Exploratory canonical projection/draft/no Family fallback: `scripts/test/run_product_postgres_tests.sh tests/product/test_enh_e4_g05_phase_b_exploratory_postgres.py`; exit 0 in Phase E partition.
## Phase C Regression
C1: `tests/product/test_predictive_api_worker_e2e_e3.py::test_predictive_execution_plan_async_worker_results_artifacts_and_lineage`; C2: R1 V-02; C3a: R1 V-04; C3b: R1 V-05; C4: `tests/product/test_enh_e4_g05_phase_c_authority_audit_postgres.py`. All isolated PASS.
## Phase D Regression
D1: `/tmp/ariadne-g05-t02-r2-d1`, exit 0, passed 2. D2: `tests/product/test_enh_e4_g05_phase_d_d2_legacy_lifecycle_shutdown_postgres.py`; D3: `tests/product/test_enh_e4_g05_phase_d_d3_global_authority_audit_postgres.py`; isolated PASS in Phase E partition.
## R1 Regression
Retry PASS; isolated failure NOT_REPRODUCED/ROOT_CAUSE_UNCONFIRMED; combined contamination TEST_FIXTURE_ISOLATION_DEFECT; G03/C3a/C3b isolated PASS.
## No-Legacy-Authority Regression
FamilyExecution/FamilyStageExecution/FamilyResult/FamilyArtifact new Product writes: NONE. Family-specific claimer: NONE. Canonical fallback: NONE. GenericExecutor authority: NO. Evidence: Phase D D1/D2/D3 isolated tests.
## Exact Verification Evidence
V-01 original Trial 01 combined scope: Test Agent command in `E4-G05_01_009_passed_gate_regression.md`; tested SHA `ddb0098...`; exit 1; passed 32; failed 6; expected 0 failures; facts: shared queue/stage state; interpretation: invalid single isolation boundary.

V-02 retry: `ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-g05-t02-r1-final scripts/test/run_product_postgres_tests.sh tests/product/test_enh_e4_g05_phase_c_retry_postgres.py`; tested state R1 modified working tree; exit 0; passed 1; failed 0; raw evidence UNKNOWN.

V-03 G03: `ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-g05-t02-r1b-g03 scripts/test/run_product_postgres_tests.sh tests/product/test_enh_e4_g03_acceptance_postgres.py`; tested SHA `804dbde...`; exit 0; passed 6; failed 0; raw evidence UNKNOWN.

V-04 C3a: `ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-g05-t02-r1b-c3a scripts/test/run_product_postgres_tests.sh tests/product/test_enh_e4_g05_phase_c_rerun_postgres.py`; exit 0; passed 1; failed 0; raw `/tmp/ariadne-g05-t02-r1b-c3a/run-20260809T113143Z.txt`.

V-05 C3b: `ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-g05-t02-r1b-c3b scripts/test/run_product_postgres_tests.sh tests/product/test_enh_e4_g05_phase_c_revise_postgres.py`; exit 0; passed 1; failed 0; raw `/tmp/ariadne-g05-t02-r1b-c3b/run-20260809T113158Z.txt`.

V-06 convergence partition: G05/G02/G04 command recorded in Phase E report; exit 0, passed 20, failed 0. V-07 Phase B: included in V-06. V-08 Phase D: isolated D1 above. V-09 contract: `ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-g05-t02-r2-contract scripts/test/run_product_postgres_tests.sh tests/product/test_postgres_contract.py`; exit 0, passed 4, failed 0.
## 11. Migration
20260809_product_0010; no migration.
## 12. Git Evidence
R2 checkpoint: 1dd20d2a6b2d7e85c3116e7b019024883e7d9786.
## 13. Remaining Trial 02 Work
R3 completion-report format remediation, full Trial 02 acceptance, and READY_FOR_TEST re-establishment remain OPEN.
## 14. R2 Decision
R2_COMPLETE.

## Files Changed
### Production
NONE
### Tests
NONE
### Fixtures
NONE
### Migrations
NONE
### Documentation
R2 report only (R2a correction).
