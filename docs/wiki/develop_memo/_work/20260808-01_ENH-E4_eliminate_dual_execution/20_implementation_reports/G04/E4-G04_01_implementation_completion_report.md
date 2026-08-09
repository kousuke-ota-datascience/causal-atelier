# E4-G04 Trial 01 Implementation Completion Report

- Project: Ariadne / causal-atelier
- Enhancement: ENH-E4 eliminate dual execution
- Gate: E4-G04
- Trial: 01
- Status: READY_FOR_TEST
- Branch: `refactor/ariadne_mvp_e4`
- Baseline commit: `14bc705938d0fda6ea0ab1b80c53ca677a19d794`
- Starting commit: `c23ba9e144d6994a32816efa8e5257fa7c47fddc`
- Implementation commit: `3d88781c1b69ba03bb06c0b8f143612b81feb4bf`
- Report commit: `0c138086d3bedca49fb83c7c28cef059e0dde914` (initial report commit; metadata correction follows)
- Migration head: `20260809_product_0009`
- Started at: `2026-08-09T05:15:47+00:00`
- Finished at: `2026-08-09T05:24:26+00:00`

Coding Agent handoff only. No Gate PASS/FAIL/BLOCKED decision is made here.

## 1. Input

- Implementation instruction: `docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/10_enhance_instruction/G04/06_Ariadne_ENH-E4_G04_実装指示書.md`
- Previous Gate Decision report: `docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/30_test_report/G03/E4-G03_02_999_gate_decision.md`

## 2. Scope Implemented

- Added explicit `ResultLevel` values `EXECUTION_RESULT` and `STAGE_RESULT`.
- Added persistent Result level/stage ownership fields and Artifact execution-output scope/stage ownership fields.
- Added `OutputOwnershipService` as the canonical G04 Result/Artifact metadata writer.
- Added explicit family output cardinality and Artifact-only contracts for CAUSAL, EXPLORATORY, and PREDICTIVE.
- Kept `ArtifactStorePort` physical-only and implemented store/metadata compensation with reconciliation visibility.
- Added typed `ResultReuseRef` / `ArtifactReuseRef`; physical `object_key` is never a semantic ID.
- Added Product migration `20260809_product_0009` as a direct child of `20260809_product_0008`.

G05 route convergence, G06 lineage convergence, and old family writer retirement remain out of scope.

## 3. Files Changed

### Added

- `product_migrations/versions/20260809_product_0009_enh_e4_g04_result_artifact_ownership.py`
- `src/ariadne/product/application/output_ownership_service.py`
- `src/ariadne/product/workflow/output_contract.py`
- `tests/product/test_enh_e4_g04_result_artifact_contract.py`
- `tests/product/test_enh_e4_g04_result_artifact_postgres.py`
- this completion report

### Modified

- `src/ariadne/product/domain/artifact.py`
- `src/ariadne/product/domain/enums.py`
- `src/ariadne/product/domain/errors.py`
- `src/ariadne/product/domain/result.py`
- `src/ariadne/product/persistence/orm_models.py`
- `src/ariadne/product/persistence/repositories.py`

### Deleted

`NONE`

The known unrelated `deploy/.nfs000000000076202f00000088` deletion was not staged or modified.

## 4. Implementation Details

### Physical Result design

Existing canonical `product_result` is evolved with `result_level` and nullable
`stage_execution_id`. Database checks distinguish ExecutionResult from
StageResult; a composite StageExecution/Execution FK rejects wrong-stage
ownership. Existing scientific result type/status/payload fields are retained.

### Physical Artifact design

Existing canonical `product_artifact` is evolved with `artifact_scope` and
nullable `stage_execution_id`. `SOURCE` preserves pre-analysis dataset source
semantics; `EXECUTION_OUTPUT` requires an Execution. Composite FKs validate
optional StageExecution and Result links. `artifact_id` is the semantic ID;
`object_key` is only the physical locator.

### Ownership and compensation

`OutputOwnershipService` validates persisted canonical StageExecution ownership,
Result level/cardinality, and execution/stage consistency. It writes bytes via
`ArtifactStorePort`, persists Result and Artifact metadata through the Product
UoW, compensates already-written objects on store/DB failure, and exposes
`OutputCompensationError.reconciliation` when cleanup itself fails.

### Cardinality / Artifact-only rules

CAUSAL and EXPLORATORY explicitly require one StageResult and reject
Artifact-only output. PREDICTIVE explicitly permits zero Results with
Artifact-only output for the represented partition-style contract. These are
typed registry entries, not family-name inference.

### Transition debt

`E4-TD-001` and `E4-TD-002` remain OPEN until G05. `E4-TD-003` is introduced
by G04 and remains OPEN until G05; old family Result/Artifact writers are not
cut over or treated as a second writer for the new canonical G04 service path.

## 5. Automated Test Code Added / Changed

| AC | Exact pytest nodes | Evidence type |
|---|---|---|
| AC-001 | `test_g04_ac001_result_levels_and_ownership_validation_are_explicit`; `test_g04_ac001_ac002_postgres_round_trip_typed_result_and_artifact_ownership` | domain/service + real PostgreSQL |
| AC-002 | `test_g04_ac001_ac002_postgres_round_trip_typed_result_and_artifact_ownership` | real PostgreSQL round-trip and wrong ownership negatives |
| AC-003 | `test_g04_ac003_store_failure_leaves_no_metadata_and_cleans_written_siblings`; `test_g04_ac003_db_failure_cleans_physical_object_and_cleanup_failure_is_reconcilable` | deterministic store/UoW failure injection |
| AC-004 | `test_g04_ac004_typed_reuse_rejects_object_key_and_requires_semantic_ids` | typed reuse negative |
| AC-005 | `test_g04_ac001_ac005_family_cardinality_contract_is_explicit`; `test_g04_ac005_artifact_only_is_explicitly_allowed_or_rejected` | explicit family registry and allow/reject behavior |

## 6. Migration

- Added migration: `product_migrations/versions/20260809_product_0009_enh_e4_g04_result_artifact_ownership.py`
- Previous head: `20260809_product_0008`
- New head: `20260809_product_0009`
- Destructive change: `NONE`
- Data migration: `NONE`; existing source artifacts receive `SOURCE` default and no historical output backfill is performed.

## 7. Changes to Already-Passed Gates

G02/G03 production contracts were preserved. The final standardized runner
included G02 canonical execution, G03 persistent StageExecution, G03 acceptance,
and PostgreSQL contract tests. No G02/G03 instruction or report artifact was
modified.

## 8. Known Limitations / Unresolved Items

- G05 is still required to converge all Product submission and old family output routes.
- Existing family Result/Artifact writers remain transitional and are tracked by `E4-TD-003`.
- Full UI/API/worker route cutover is intentionally not implemented.
- The evidence runner logs were produced before the implementation commit fixed the SHA; the tested working-tree source corresponds to the implementation commit content.

## 9. Out-of-Scope Work

G05 Product Execution convergence; G06 lineage authority consolidation; G07
legacy/CLI/migration retirement; G08 final bootstrap/audit; scientific payload
or algorithm redesign; dataset ingestion redesign; root legacy migration;
GenericExecutor persistence; and PostgreSQL infrastructure redesign.

## 10. Git Evidence

- `git rev-parse HEAD` after implementation commit: `3d88781c1b69ba03bb06c0b8f143612b81feb4bf`
- `git status --short` before implementation commit: unrelated `.nfs` deletion only.
- Implementation diff stat: `11 files changed, 653 insertions(+), 2 deletions(-)`.
- `git diff --check`: exit `0` before commit.

## 11. Handoff to Test Agent

- Test target implementation commit: `3d88781c1b69ba03bb06c0b8f143612b81feb4bf`
- Active Gate: `E4-G04 Trial 01`
- Implementation report path: `docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/20_implementation_reports/G04/E4-G04_01_implementation_completion_report.md`
- Coding Agent test execution: pure `17 passed, 1 skipped`; standardized PostgreSQL `17 passed`, exit `0`.
- Ready for independent test: `YES`

## 12. Design Block

- Contradiction: `NONE`
- Observed facts: existing source Artifact rows share `product_artifact` with execution outputs; explicit `artifact_scope` preserves source semantics while enforcing output ownership.
- Impact: `NONE`; this is resolved within the approved G04 contract.
- Minimal choices: `NONE`
- Decision required: `NONE`

## 13. Supplemental Implementation Evidence

- G04 PostgreSQL evidence: `test-results/postgres/run-20260809T052308Z.metadata.txt` (`1 passed`, migration head `20260809_product_0009`).
- Regression PostgreSQL evidence: `test-results/postgres/run-20260809T052335Z.metadata.txt` (`17 passed`, migration head `20260809_product_0009`).
- Pure evidence command: `UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run pytest -q tests/product/test_enh_e4_g04_result_artifact_contract.py tests/product/test_enh_e4_g03_generic_executor_boundary.py tests/product/test_enh_e4_g03_persistent_stage_execution.py tests/product/test_enh_e4_g02_canonical_execution.py` → exit `0`, `17 passed, 1 skipped`.
- No new dependency was added.
- GenericExecutor remains free of Result/Artifact persistence, UoW commit, claim/lease, retry, and lineage authority.
