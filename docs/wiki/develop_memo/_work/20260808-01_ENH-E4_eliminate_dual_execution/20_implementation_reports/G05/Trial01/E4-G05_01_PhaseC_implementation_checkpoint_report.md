# E4-G05 Trial 01 Phase C Implementation Checkpoint Report

- Project: causal-atelier
- Enhancement: ENH-E4 eliminate dual execution
- Gate: G05
- Trial: 01
- Phase: C
- Phase Status: PHASE_C_COMPLETE
- Branch: `refactor/ariadne_mvp_e4`
- Phase baseline checkpoint: `7695834fe2eabc573cd68641c74a76f565334ca1`
- C1 checkpoint: `7695834fe2eabc573cd68641c74a76f565334ca1`
- C2 checkpoint: `3cea6711803904e0009fc55a013c2e8003b45f13`
- C3a checkpoint: `daedd9244bf73f586b77ff6da11a1c4de91db55c`
- C3b checkpoint: `7870329192986bcd070935bf48fe814dda444a77`
- Phase C final implementation checkpoint: `9c58bffd5c5fb6be8565a1256222e678fb86c52a`
- Report commit: PENDING
- Migration head: `20260809_product_0010`
- Started at: UNKNOWN
- Finished at: 2026-08-09 UTC

## 1. Input

06i13 C4 instruction、C1〜C3b checkpoint、actual branch sourceを入力とした。

## 2. Phase C Scope Summary

Predictive の Product-facing submit、read projection、worker、cancel/retry/rerun/revise を canonical Product aggregateへ収束させた。Phase Dの旧family lifecycle全面shutdown、Phase EのGate-level completionは対象外である。

## 3. Internal Checkpoint Ledger

### C1

Canonical Predictive Golden Path。canonical claim、StageExecution、typed Result/Artifact、provenance を確認。

### C2

Same Execution retry、append-only attempt history、old Family write-negativeを確認。

### C3a

New canonical Execution、base relation、RERUN、new StageExecution identitiesを確認。

### C3b

Changed condition revise、explicit reason、REVISED、same-condition RERUN comparisonを確認。

### C4

Cross-surface authority audit、retry worker re-execution修正、old E3 legacy-authority testのcanonical置換、final regressionを実施。

## 4. Final Authority Matrix

| Surface | Entry point | Canonical authority | Remaining legacy code | New Product flow |
|---|---|---|---|---|
| submit | `PredictiveWorkflowService.submit_execution` | `ExecutionService.create_family_execution` | legacy branch exists | unreachable in injected canonical mode |
| execution read/list | `get_execution` / `list_executions` | `ExecutionOrm` / `ExecutionService` | legacy branch exists | unreachable |
| stage read | `get_stages` | `StageExecutionOrm` / `StageAttemptOrm` | legacy branch exists | unreachable |
| result/artifact read | `list_results` / `list_artifacts` | `ResultOrm` / `ArtifactOrm` | legacy branch exists | unreachable |
| lineage/prefill | `list_lineage` / `prefill` | canonical owned IDs / Execution snapshot | legacy branch exists | unreachable |
| cancel/retry | `cancel` / `retry` | `ExecutionService` + persistent StageExecution | legacy mutation branch exists | unreachable |
| rerun/revise | `rerun` / `revise` | canonical base Execution + `ExecutionService` | legacy mutation branch exists | unreachable |
| worker | canonical claim + `ExecutionProcessor` | `ExecutionOrm`, StageExecution, Result, Artifact | legacy worker source remains | C1 canonical path |

## 5. Files Changed

### Added

- `tests/product/test_enh_e4_g05_phase_c_authority_audit_postgres.py`

### Modified

- `src/ariadne/product/application/execution_service.py`
- `src/ariadne/product/domain/stage_execution.py`
- `tests/product/test_enh_e4_g05_phase_c_retry_postgres.py`
- `tests/product/test_predictive_api_worker_e2e_e3.py`

### Deleted

NONE

## 6. Implementation Details

`StageExecution.prepare_retry()` は FAILED stage を identity / attempts / bindingsを保持したまま PENDINGへ遷移する。`ExecutionService.retry_execution()` がこれを呼び、canonical worker が READY→RUNNING→新 attempt を実行できるようにした。

Execution revisionの `revision_kind` / `change_reason` は `_build_revision_context()` の canonical comparison結果を使用する。従って同条件の revise は RERUN、条件変更ありだけが REVISEDとなる。

## 7. Automated Test Code Added / Changed

C4 authority audit testを追加した。旧E3 retry testを canonical ExecutionOrm / StageExecutionOrm / StageAttemptOrm 前提へ更新し、retry後のworker attempt 2まで検証する。

## 8. Migration

Phase C migration追加: NONE。Product migration headは `20260809_product_0010`。ORM/domain/schemaのPhase C追加不整合は観測されない。

## 9. No-Legacy-Write / No-Fallback Evidence

C1 submit/worker、C2 retry、C3a rerun、C3b revise、C4 read/cancel authority auditで `FamilyExecutionOrm`、`FamilyStageExecutionOrm`、`FamilyResultOrm`、`FamilyArtifactOrm` のbefore/after row count不変をassertした。unknown canonical IDは `EntityNotFound` で拒否され、Family fallbackは確認されなかった。

## 10. Passed-Gate Regression Impact

### G02

Canonical Execution identity/lifecycle/revision contract: PASS。

### G03

Persistent StageExecution、attempt history、retry-ready integration: PASS（独立 DB resetで6 passed）。

### G04

Result/Artifact ownership、typed persistence: PASS。

### Phase A

Typed Result/Artifact、schema/version、PostgreSQL constraint: PASS。

### Phase B

Exploratory canonical Result projection / draft / no shadow write: PASS。

## 11. Known Limitations / Remaining G05 Work

Phase D: global legacy claim/process hard shutdown、all-family legacy reachability shutdown、global failure fallback audit。Phase E: TD closure、G05 final Golden Paths、Gate completion report、READY_FOR_TEST。

## 12. Explicit Out-of-Scope Work

Phase D、Phase E、G06 lineage final consolidation。

## 13. Git Evidence

- Phase C implementation checkpoint: `9c58bffd5c5fb6be8565a1256222e678fb86c52a`
- Report commit: PENDING
- Working tree at implementation checkpoint: only untracked 06i13 instruction。

## 14. Phase Verification Evidence

- Command: `scripts/test/run_product_postgres_tests.sh tests/product/test_enh_e4_g03_acceptance_postgres.py`
  - Exit: 0; actual: 6 passed; expected: G03 persistent contract PASS; evidence: `test-results/postgres/run-20260809T092351Z.txt`。
- Command: `scripts/test/run_product_postgres_tests.sh tests/product/test_predictive_api_worker_e2e_e3.py::test_predictive_execution_plan_async_worker_results_artifacts_and_lineage tests/product/test_enh_e4_g05_phase_c_retry_postgres.py tests/product/test_enh_e4_g05_phase_c_rerun_postgres.py tests/product/test_enh_e4_g05_phase_c_revise_postgres.py tests/product/test_enh_e4_g05_phase_c_authority_audit_postgres.py tests/product/test_enh_e4_g05_phase_a_postgres.py tests/product/test_enh_e4_g05_phase_b_exploratory_postgres.py tests/product/test_enh_e4_g02_canonical_execution.py tests/product/test_enh_e4_g04_result_artifact_postgres.py`
  - Exit: 0; actual: 18 passed; expected: Phase C/A/B/G02/G04 PASS; evidence: `test-results/postgres/run-20260809T092414Z.txt`。
- Command: `.venv/bin/pytest -q tests/product/test_predictive_api_worker_e2e_e3.py`
  - Exit: 0; actual: 3 passed; expected: canonical API/worker retry regression PASS。
- Facts: one earlier combined runner had 21 passed / 3 failed because G03 assumes globally empty tables while preceding fixtures persist rows. G03 was rerun with the runner's independent DB reset and passed.
- Interpretation: the combined failure is fixture isolation, not a Product semantic failure.

## 15. Next-Phase Handoff

- Next phase: Phase D
- Ready for Phase D: YES
- Gate READY_FOR_TEST: NO

## 16. Design Block

NONE
