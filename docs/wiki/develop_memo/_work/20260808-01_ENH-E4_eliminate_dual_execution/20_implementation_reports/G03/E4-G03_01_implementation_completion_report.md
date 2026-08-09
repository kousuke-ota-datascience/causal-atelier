# E4-G03 Trial 01 Implementation Completion Report

## 1. Status

`READY_FOR_TEST`

This is a Coding Agent implementation handoff. It is not an E4-G03 Gate
PASS/FAIL decision.

## 2. Repository Metadata

- Branch: `refactor/ariadne_mvp_e4`
- Baseline: `cb28a18c07cad00cf12f01e9124651aa45aab16f`
- Starting commit: `cb28a18c07cad00cf12f01e9124651aa45aab16f`
- Implementation commit: `f455354` (`feat: persist canonical stage executions`)
- Previous Product migration head: `20260809_product_0007`
- New Product migration head: `20260809_product_0008`

The unrelated `deploy/.nfs000000000076202f00000088` deletion and existing G03
operator prompt files remain unstaged and were not modified.

## 3. Implemented Boundary

G03 adds canonical `product_stage_execution` and append-only
`product_stage_attempt` persistence. `Execution` remains the sole claim/lease
authority. `StageExecutionService`, `SqlStageExecutionRepository`, and the
Product Unit of Work provide the application/repository boundary.

`StagePlanMaterializer` validates family, non-empty plans, unique stage keys,
dependency references, and cycles, then assigns deterministic ordinals and
stable stage identities. `CanonicalPlanProvider` maps CAUSAL, EXPLORATORY, and
PREDICTIVE planners into this common materialization contract.

Canonical Causal `ExecutionService` submission materializes stages before the
single UoW commit. Plan failure occurs before persistence, so a valid canonical
Execution cannot be committed with zero stages. Existing FamilyExecution and
FamilyStageExecution paths remain transitional and are not deleted or promoted
to a second canonical StageExecution authority; E4-TD-002 remains open.

## 4. Schema

Migration `20260809_product_0008` creates:

- `product_stage_execution`: execution FK, stage key/type, ordinal,
  dependencies, state, JSON-safe input/output bindings, error and timestamps;
- `product_stage_attempt`: stage FK, stable attempt ID, monotonic attempt
  number, worker, timestamps, and error.

Uniqueness constraints enforce `(execution_id, stage_key)` and
`(stage_execution_id, attempt_number)`. `CANCELLED` is an explicit persistent
stage state.

## 5. Lifecycle and Ownership

- Stage retry preserves `execution_id` and `stage_execution_id` and appends an
  attempt; previous attempts are not deleted or renumbered.
- `RUNNING` requires a parent `Execution` in `RUNNING` state.
- Stage mutation checks the parent lease owner and rejects expired leases,
  including SQLite's naive timestamp representation.
- Cancellation uses explicit `CANCELLED`; successful stages remain successful.
- Execution completion rejects success if no canonical stages exist or any stage
  is nonterminal/failed.
- Result/Artifact semantics remain unchanged for G04.

## 6. GenericExecutor Boundary

`GenericExecutor` now performs plan validation, ordering, binding resolution,
runner invocation, and in-memory outcome production only. It has no UoW,
database, claim, commit, or canonical retry callback. It returns per-stage
`StageRunResult` values to the orchestration owner. Existing worker paths persist
stage outcomes outside the executor.

## 7. Changed Files

Production/migration:

- `src/ariadne/product/domain/{enums,stage_execution}.py`
- `src/ariadne/product/persistence/{orm_models,repositories,unit_of_work}.py`
- `src/ariadne/product/ports/{repositories,unit_of_work}.py`
- `src/ariadne/product/application/{execution_service,stage_execution_service}.py`
- `src/ariadne/product/workflow/{executor,stage_materialization,canonical_plan_provider}.py`
- `src/ariadne/interfaces/worker/execution_processor.py`
- `src/ariadne/product/application/predictive_workflow_service.py`
- `product_migrations/versions/20260809_product_0008_enh_e4_g03_stage_execution.py`

Tests:

- `tests/product/test_enh_e4_g03_generic_executor_boundary.py`
- `tests/product/test_enh_e4_g03_persistent_stage_execution.py`
- shared PostgreSQL fixture in `tests/product/conftest.py`
- updated GenericExecutor regression expectation in
  `tests/product/test_enh_e3_causal_workflow_regression.py`

## 8. AC Mapping

| AC | Direct automated coverage |
|---|---|
| AC-001 | `test_g03_ac001_materializes_persistent_shape_for_all_canonical_families`; `test_g03_ac001_ac002_persistent_stage_round_trip` |
| AC-002 | `test_g03_ac001_ac002_persistent_stage_round_trip` queries state, binding, error, timestamps, and attempt history through `SqlStageExecutionRepository` |
| AC-003 | `test_g03_ac003_generic_executor_has_no_persistence_or_retry_authority`; updated causal workflow regression |
| AC-004 | `test_g03_ac004_empty_or_mismatched_plan_is_rejected_before_persistence` |
| AC-005 | `test_g03_stage_identity_and_attempt_history_are_append_preserving`; `test_g03_ac005_cancellation_is_explicit_and_terminal`; owner checks in the PostgreSQL round-trip |

## 9. Self-checks

- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/pytest -q`: `198 passed, 5 skipped`
- G03 unit/boundary tests: passed
- Standard runner:
  `scripts/test/run_product_postgres_tests.sh tests/product/test_enh_e4_g03_persistent_stage_execution.py tests/product/test_postgres_contract.py tests/product/test_enh_e4_g02_canonical_execution.py`
  → `10 passed`, migration exit `0`, pytest exit `0`
- Observed migration current/head: `20260809_product_0008 (head)`
- Preflight infrastructure was used without modification.

## 10. Passed-Gate Regression

G02 files were changed only where needed to attach stage materialization and
persist stage outcomes. Canonical family discriminator, atomic claim, lease
owner/expiry, owner-checked mutation, and G02 identity semantics remain intact.
The PostgreSQL contract and G02 regression suite passed.

## 11. Transition Debt

- `E4-TD-001`: `OPEN`, introduced by G02, exit gate G05.
- `E4-TD-002`: `OPEN`, introduced by G03; old stage persistence/ephemeral
  behavior remains on transitional Family paths, exit gate G05.

G04 Result/Artifact consolidation, G05 convergence, G06 lineage, G07 legacy
retirement, and G08 final audit/bootstrap were not implemented.

## 12. Known Limitations

Docker daemon access and sufficient host disk are required for real PostgreSQL
self-checks. The standardized runner was available and the self-check passed.
The independent Test Agent must perform the Gate decision; this report does not
declare G03 PASS.
