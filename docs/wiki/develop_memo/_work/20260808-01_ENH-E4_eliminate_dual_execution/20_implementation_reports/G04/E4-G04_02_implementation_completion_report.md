# E4-G04 Trial 02 Implementation Completion Report

- Project: Ariadne / causal-atelier
- Enhancement: ENH-E4 eliminate dual execution
- Gate: E4-G04
- Trial: 02
- Status: READY_FOR_TEST
- Branch: `refactor/ariadne_mvp_e4`
- Baseline commit: `14bc705938d0fda6ea0ab1b80c53ca677a19d794`
- Starting commit: `3aae1c8893e06f08caa11d7af9f48aba3cfde62f`
- Implementation commit: `9c9db4454e0f08c4d46cb002f723ca6827917564`
- Report commit: `a9a47ffa9b9053d024566c966e084c451a72acd5` (initial report commit; metadata correction follows)
- Migration head: `20260809_product_0009`
- Started at: `2026-08-09T05:41:00+00:00`
- Finished at: `2026-08-09T05:49:11+00:00`

Coding Agent handoff only. No Gate PASS/FAIL/BLOCKED decision is made here.

## 1. Input

- Implementation instruction: `docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/10_enhance_instruction/G04/06_Ariadne_ENH-E4_G04_実装指示書.md` (Trial 01 baseline; Trial 02 is limited remediation from independent-test evidence)
- Previous Gate Decision report: `docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/30_test_report/G04/E4-G04_01_999_gate_decision.md`

## 2. Scope Implemented

- Remediated AC-004 by requiring `ResultReuseRef` to carry both canonical `result_id` and typed `ResultReuseRole`.
- Added AC-004 object-key-only and content-hash-only negative cases for both Result and Artifact reuse boundaries.
- Remediated AC-003 evidence with real PostgreSQL commit-failure injection after ArtifactStore persistence and SQLAlchemy flush.
- Added fresh-Session assertions of absent Result/Artifact metadata and cleanup-failure reconciliation assertions.

No migration, route convergence, or G05 work was added.

## 3. Files Changed

### Added

- this completion report

### Modified

- `src/ariadne/product/domain/enums.py`
- `src/ariadne/product/application/output_ownership_service.py`
- `tests/product/test_enh_e4_g04_result_artifact_contract.py`
- `tests/product/test_enh_e4_g04_result_artifact_postgres.py`

### Deleted

`NONE`

The pre-existing unrelated `deploy/.nfs000000000076202f00000088` deletion was not staged or modified.

## 4. Implementation Details

### Typed Result reuse boundary

`ResultReuseRef` now requires `ResultReuseRole.UPSTREAM_INPUT`; a raw string is rejected at construction. Canonical lookup remains by `result_id`, so neither a physical `object_key` nor a content hash can be a semantic Result/Artifact reference.

### PostgreSQL transaction/physical-store compensation evidence

The test-only `_PostgresCommitFailureUow` flushes pending metadata to real PostgreSQL, rolls the transaction back, then raises an injected commit failure after bytes have been saved. A fresh SQLAlchemy Session confirms zero Result and Artifact rows. The test also proves physical deletion and, when deletion fails, that `OutputCompensationError.reconciliation` contains the artifact ID, physical object key, and cleanup error.

## 5. Automated Test Code Added / Changed

| AC | Exact pytest nodes | Evidence type |
|---|---|---|
| AC-003 | `test_g04_ac003_postgres_commit_failure_rolls_back_metadata_and_compensates_physical_store[cleanup_succeeds]`; `test_g04_ac003_postgres_commit_failure_rolls_back_metadata_and_compensates_physical_store[cleanup_requires_reconciliation]` | real PostgreSQL transaction failure after physical store |
| AC-004 | `test_g04_ac004_typed_reuse_requires_semantic_id_and_typed_role` | typed Result role plus physical-key/hash negatives |
| Regression | G02/G03/G04 selected Product test files | standardized PostgreSQL runner |

## 6. Migration

- Added migration: `NONE`
- Previous head: `20260809_product_0009`
- New head: `20260809_product_0009`
- Destructive change: `NONE`
- Data migration: `NONE`

## 7. Changes to Already-Passed Gates

G02/G03 production contracts and report artifacts are unchanged. Their dedicated tests ran with G04 under the standardized runner: `27 passed`.

## 8. Known Limitations / Unresolved Items

- Independent Test Agent verification of Trial 02 is still required.
- `E4-TD-001`, `E4-TD-002`, and `E4-TD-003` remain OPEN until G05; this remediation does not converge old output writers.
- Failure injection is deterministic test instrumentation around a real PostgreSQL transaction, not an in-memory UoW.

## 9. Out-of-Scope Work

G05 Product Execution convergence; G06 lineage authority consolidation; G07 legacy/CLI/migration retirement; G08 final bootstrap/audit; all user-facing/API/worker route changes; and a new migration.

## 10. Git Evidence

- `git rev-parse HEAD` after implementation commit: `9c9db4454e0f08c4d46cb002f723ca6827917564`
- `git status --short` after implementation commit: unrelated `.nfs` deletion and independent Test Agent report files only.
- Implementation diff stat: `4 files changed, 101 insertions(+), 6 deletions(-)`.
- `git diff --check`: exit `0` before implementation commit.

## 11. Handoff to Test Agent

- Test target implementation commit: `9c9db4454e0f08c4d46cb002f723ca6827917564`
- Active Gate: `E4-G04 Trial 02`
- Implementation report path: `docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/20_implementation_reports/G04/E4-G04_02_implementation_completion_report.md`
- Coding Agent test execution: pure contract test `6 passed`; standardized PostgreSQL G04 test `3 passed`; standardized G02/G03/G04 regression `27 passed`, all exit `0`.
- Ready for independent test: `YES`

## 12. Design Block

- Contradiction: `NONE`
- Observed facts: Trial 01 Gate Decision identified an absent typed Result role/context and an AC-003 test limited to an in-memory UoW.
- Impact: both acceptance items were FAIL despite remaining G04 items passing.
- Minimal choices: add a typed Result reuse role and real PostgreSQL failure evidence without changing the G04 ownership schema.
- Decision required: `NONE`

## 13. Supplemental Implementation Evidence

- Pure test: `UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run pytest -q tests/product/test_enh_e4_g04_result_artifact_contract.py` → `6 passed`.
- PostgreSQL G04 test: `ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-audit-evidence scripts/test/run_product_postgres_tests.sh tests/product/test_enh_e4_g04_result_artifact_postgres.py` → `3 passed`, migration head `20260809_product_0009`.
- PostgreSQL regression: `ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-audit-evidence scripts/test/run_product_postgres_tests.sh tests/product/test_enh_e4_g02_canonical_execution.py tests/product/test_enh_e4_g03_persistent_stage_execution.py tests/product/test_enh_e4_g03_generic_executor_boundary.py tests/product/test_enh_e4_g03_acceptance_postgres.py tests/product/test_enh_e4_g04_result_artifact_contract.py tests/product/test_enh_e4_g04_result_artifact_postgres.py` → `27 passed`, migration head `20260809_product_0009`.
- No dependency or migration was added.
