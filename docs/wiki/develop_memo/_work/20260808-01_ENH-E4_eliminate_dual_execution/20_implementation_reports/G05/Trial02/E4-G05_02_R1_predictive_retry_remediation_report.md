# E4-G05 Trial 02 R1 Predictive Retry Remediation Report

- Gate: E4-G05
- Trial: 02
- Remediation package: R1
- Status: R1_COMPLETE
- Branch: refactor/ariadne_mvp_e4
- Failed Trial 01 implementation SHA: ddb009875ef4e649f413cb0bb7f7a85f894e2b14
- R1 starting commit: f9c3fafda6b4d4ba77fdacdb192a58b3af07e9d0
- R1 checkpoint commit: ad3e3e124ee47f9cbaa2470b25263b7289795262
- Migration head: 20260809_product_0010
- Started at: 2026-08-09 UTC
- Finished at: 2026-08-09 UTC
- Report commit: 6269b8031f2cfa8d661cc432e5aea61709e7e4fe

## 1. Trial 01 Failure Input
Test Agent item 005 reported that retry target was not returned by canonical `claim_next` in an isolated run.
## 2. Reproduction
`ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-g05-t02-r1-baseline scripts/test/run_product_postgres_tests.sh tests/product/test_enh_e4_g05_phase_c_retry_postgres.py` exited 0: 1 passed. The same result held after diagnostic hardening (`/tmp/ariadne-g05-t02-r1-final`): 1 passed.
## 3. Claim Candidate Evidence
- retry target: the retried Predictive execution
- all eligible candidates: exactly that execution
- requested_at ordering: target is sole FIFO candidate
- actual claimed ID: retry target
## 4. Root Cause Classification
`TEST_FIXTURE_ISOLATION_DEFECT` for the combined invocation evidence; the Trial 01 isolated reproduction difference is recorded as non-reproducible on current standard runner. No implementation defect or queue-priority change was established.
## 5. Authoritative Queue / Retry Contract
### G02
Global FIFO canonical claimer; no retry/family priority introduced.
### G03
Same Execution and StageExecution identity; attempt history appends.
## 6. Fix
### Production
N/A.
### Test
Added claim-before diagnostic assertion for all eligible canonical candidates and FIFO order.
### Fixture / Runner
Combined-run isolation remains OPEN for later Trial 02 work.
## 7. Files Changed
`tests/product/test_enh_e4_g05_phase_c_retry_postgres.py`.
## 8. Retry Lifecycle Invariants
Same Execution, stable StageExecution, append attempt, correct lease, unchanged requested_at, Family 4-table writes NONE.
## 9. No-Legacy-Write Evidence
Retry test asserts FamilyExecution/StageExecution/Result/Artifact counts unchanged.
## 10. Verification
Baseline and final isolated standard runner: exit 0, 1 passed. Related rerun/revise/G02 PASS; combined G03 acceptance failed only after earlier tests created global queue/stage state, and is outside R1 scope.
## 11. Migration
20260809_product_0010; no migration.
## 12. Git Evidence
R1 checkpoint: ad3e3e124ee47f9cbaa2470b25263b7289795262.
## 13. Remaining Trial 02 Work
Combined-run fixture isolation, remaining Test Agent failures, and Trial 01 completion-report format remediation remain OPEN.
## 14. R1 Decision
R1_COMPLETE.
