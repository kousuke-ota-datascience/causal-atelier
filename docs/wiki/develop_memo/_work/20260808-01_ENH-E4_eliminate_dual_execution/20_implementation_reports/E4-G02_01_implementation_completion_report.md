# E4-G02 Trial 01 Implementation Completion Report

- Project: Ariadne / causal-atelier
- Enhancement: ENH-E4 eliminate dual execution
- Gate: E4-G02
- Trial: 01
- Status: READY_FOR_TEST
- Branch: refactor/ariadne_mvp_e4
- Baseline commit: e70c6f7f1f63ce2568c85482bc20a355da66b7cf
- Starting commit: e70c6f7f1f63ce2568c85482bc20a355da66b7cf
- Implementation commit: 166e90cd1c2d0e523fb863795a88343403d8cc44
- Report commit: PENDING_REPORT_COMMIT
- Migration head: 20260809_product_0007
- Started at: 2026-08-09T00:00:00Z
- Finished at: 2026-08-09T00:00:00Z

## 1. Input

- Implementation instruction: docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/10_enhance_instruction/G02/06_Ariadne_ENH-E4_実装指示書.md
- Previous Gate Decision report: N/A

## 2. Scope Implemented

G02のcanonical Product Execution aggregateを既存Product Execution modelへ拡張した。三family共通のanalysis_family discriminator、共通identity、canonical state domain、lease owner、retry/rerun/revise/cancel identity semantics、canonical repository claim boundaryを実装した。G03以降のStage/Result/Artifact/Lineage convergenceは実装していない。

## 3. Files Changed

### Added

- product_migrations/versions/20260809_product_0007_enh_e4_g02_canonical_execution.py
- tests/product/test_enh_e4_g02_canonical_execution.py

### Modified

- src/ariadne/product/domain/execution.py
- src/ariadne/product/application/execution_service.py
- src/ariadne/product/persistence/orm_models.py
- src/ariadne/product/persistence/repositories.py
- src/ariadne/product/ports/repositories.py
- src/ariadne/interfaces/worker/execution_processor.py
- src/ariadne/interfaces/worker/runner.py
- src/ariadne/interfaces/web_api/routers/executions.py
- src/ariadne/interfaces/web_api/schemas/__init__.py

### Deleted

NONE

## 4. Implementation Details

- ExecutionにCAUSAL/EXPLORATORY/PREDICTIVE discriminatorを追加し、Execution ID namespaceを共有した。
- Product execution tableへanalysis_family、base_execution_id、revision_kind、change_reason、lease_owner、lease_expires_atを追加した。
- SqlExecutionRepository.claim_nextをfamily-neutralなatomic row-lock claimへ拡張した。expired leaseは deterministic に再claimし、owner/expiryを永続化する。
- renew_lease、owner-checked update/completeを追加した。GenericExecutorは変更していないため、canonical claim/commit authorityではない。
- ExecutionServiceは同一familyのrerun/reviseのみ許可し、new Execution IDとtyped base relationを保存する。retryは既存ID/retry_countを維持する。
- workerの既存Causal processorはpersisted lease ownerをcompletion ownerとして利用し、既存直接processorテストとの互換性を維持した。
- Product migration chainのみを使用する0007 migrationを追加した。root legacy migrationは変更していない。

## 5. Automated Test Code Added / Changed

Added tests/product/test_enh_e4_g02_canonical_execution.py:

| AC | Test node | Coverage |
|---|---|---|
| E4-G02-AC-001 | g02_001 | all three family discriminators share Execution identity contract |
| E4-G02-AC-002 | g02_002 | common QUEUED→RUNNING→terminal state machine and invalid terminal transition |
| E4-G02-AC-003 | g02_003 / g02_004 | retry same ID; rerun/revise new ID with typed base |
| E4-G02-AC-004 | g02_005 and repository contract | lease is explicit; GenericExecutor unchanged |
| E4-G02-AC-005 | repository contract plus g02_002/g02_005 | atomic claim path, invalid transition and lease ownership contract |

Self-check results:
- PYTHONDONTWRITEBYTECODE=1 .venv/bin/pytest -q tests/product/test_enh_e4_g02_canonical_execution.py tests/product/test_domain_and_snapshot.py tests/product/test_enh_e1_contract.py: 29 passed
- PYTHONDONTWRITEBYTECODE=1 .venv/bin/pytest -q tests/product/test_api_worker_e2e.py tests/product/test_enh_e3_api_worker_e2e.py: 12 passed
- test collection for the G02 tests, domain tests, and PostgreSQL contract tests: 13 collected
- compileall: passed
- alembic -c alembic_product.ini heads: 20260809_product_0007 (head)
- git diff --check: passed

## 6. Migration

- Added migration: product_migrations/versions/20260809_product_0007_enh_e4_g02_canonical_execution.py
- Previous head: 20260807_product_0006
- New head: 20260809_product_0007
- Destructive change: NO
- Data migration: NONE; existing rows receive CAUSAL server default for analysis_family

## 7. Changes to Already-Passed Gates

NONE. G01 documentation/contract was not changed by the implementation.

## 8. Known Limitations / Unresolved Items

- Existing family workflow services still retain temporary family-specific lifecycle paths under E4-TD-001; G05 convergence is not attempted.
- G02 does not persist StageExecution attempts or consolidate Result/Artifact ownership.
- Real PostgreSQL concurrency and migration upgrade were not run because no isolated PostgreSQL environment was authorized/available in this trial; the existing PostgreSQL contract test was collected but not executed.
- The implementation uses the existing causal operation contract as the operation discriminator while analysis_family is the canonical family discriminator. Family-specific workflow operation expansion remains out of scope.

## 9. Out-of-Scope Work

G03 StageExecution, G04 Result/Artifact, G05 full runtime cutover, G06 lineage, G07 legacy/CLI/migration boundary, G08 final audit, scientific algorithms, frontend, legacy source deletion, root migrations, and unrelated working-tree changes were not modified.

## 10. Git Evidence

- git rev-parse HEAD: 166e90cd1c2d0e523fb863795a88343403d8cc44
- git status --short before report: existing deploy/.nfs000000000076202f00000088 deletion; pre-existing implementation-instruction README modification; G02 instruction directory untracked
- Diff stat for implementation commit: 11 files changed, 290 insertions, 18 deletions

## 11. Handoff to Test Agent

- Test target implementation commit: 166e90cd1c2d0e523fb863795a88343403d8cc44
- Active Gate: E4-G02
- Implementation report path: docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/20_implementation_reports/E4-G02_01_implementation_completion_report.md
- Coding Agent test execution: targeted and related regression self-checks listed in Section 5
- Ready for independent test: YES

## 12. Design Block

- Contradiction: NONE
- Observed facts: existing Product Execution model was Causal-oriented; Product migration head was 20260807_product_0006; family-specific services remained separate.
- Impact: G02 implementation was possible by adding the canonical family/lease/base contract without changing later Gate architecture.
- Minimal choices: reuse the Product Execution table as canonical persistence, add additive migration columns, preserve old family paths as E4-TD-001.
- Decision required: NONE

## 13. Supplemental Implementation Evidence

E4-TD-001 remains OPEN and exits at E4-G05. Coding Agent did not declare Gate PASS and stops at READY_FOR_TEST.
