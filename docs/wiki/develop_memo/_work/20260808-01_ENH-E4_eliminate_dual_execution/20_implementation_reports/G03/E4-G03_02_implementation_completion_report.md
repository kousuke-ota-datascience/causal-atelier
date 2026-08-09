# E4-G03 Trial 02 Implementation Completion Report

## Status

`READY_FOR_TEST`

This is a Coding Agent handoff, not a Gate PASS/FAIL decision.

## Metadata

- Project: Ariadne / causal-atelier
- Enhancement: ENH-E4 eliminate dual execution
- Gate / Trial: E4-G03 / 02
- Branch: `refactor/ariadne_mvp_e4`
- Trial 02 starting SHA: `de4b120b452c019cf0863c6846b06261df6de8a4`
- Trial 01 implementation SHA: `f455354e3724b66360bed6d3cfd4646ca1463a89`
- Trial 01 FAIL/report SHA: `de4b120b452c019cf0863c6846b06261df6de8a4`
- Trial 02 implementation/test SHA: `bac1814bb713f32b859fbe7e2b445fa6cd557f2b`
- Product migration head: `20260809_product_0008`
- New Product migration: `NONE`

## Prior FAIL and remediation

Trial 01 was a required-evidence FAIL, not a production failure.  The missing
automated evidence was remediated as follows.

| Area | Trial 02 test evidence |
|---|---|
| R-01 cross-family persistence | CAUSAL, EXPLORATORY, and PREDICTIVE submit through `ExecutionService`, then reload persistent children in a new session. |
| R-02 query / round-trip | `list_for_execution`, `get`, dependencies, bindings, errors/timestamps, and retry attempts `[1,2]` are reloaded from PostgreSQL. |
| R-03 executor negative | A failing runner returns the in-memory failure outcome; no persistence/claim/retry/result/artifact/lineage authority is invoked. |
| R-04/R-05 lifecycle | durable failure, retry with stable IDs, cancellation, wrong/expired owner rejection, and invalid parent success are tested. |
| R-06/R-07 atomicity | invalid empty plan and injected stage-write failure roll back parent/stages; successful resubmission has exactly one child per key. |

## Changed files

### Test changes

- `tests/product/test_enh_e4_g03_acceptance_postgres.py`
- `tests/product/test_enh_e4_g03_generic_executor_boundary.py`

### Production changes

`NONE`

### Migration changes

`NONE`

### Documentation/report changes

- this report

## Acceptance-criteria mapping

| AC | Exact pytest node | Verification |
|---|---|---|
| AC-001 | `test_g03_ac001_canonical_application_path_persists_and_reloads_each_family[EXPLORATORY]`, `[CAUSAL]`, `[PREDICTIVE]` | real PostgreSQL canonical application submission, child persistence, new-session reload, same execution ID |
| AC-002 | `test_g03_ac002_persistent_round_trip_lists_bindings_timestamps_and_retry_history` | real PostgreSQL list/get, dependencies, input/output/error/timestamps, `[1,2]` attempts after reload |
| AC-003 | `test_g03_ac003_generic_executor_has_no_persistence_or_retry_authority`; `test_g03_ac003_runner_failure_has_no_persistence_claim_or_retry_side_effect` | static boundary and pure behavioral negative |
| AC-004 | `test_g03_ac004_ac007_materialization_failure_rolls_back_without_orphans_or_zero_stage_execution` | Causal zero-stage prevention, injected stage persistence rollback, no orphan/duplicate after resubmission |
| AC-005 | `test_g03_ac005_persistent_failure_retry_cancellation_owner_and_invalid_success` | persisted failure/retry/cancellation, wrong and expired owner rejection, invalid success rejection |

## Production defect findings

All added mandatory acceptance tests passed after correcting only test defects:

- PostgreSQL seed SQL reused one bind parameter across incompatible column types.
- The expired-lease fixture remained claimable by the subsequent invalid-success scenario.

No production defect was exposed by the added mandatory acceptance tests.

## Self-check

- `UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run pytest -q tests/product/test_enh_e4_g03_generic_executor_boundary.py` → exit `0`, `6 passed`.
- `scripts/test/run_product_postgres_tests.sh tests/product/test_enh_e4_g03_acceptance_postgres.py::test_g03_ac005_persistent_failure_retry_cancellation_owner_and_invalid_success` → exit `0`, `1 passed`; evidence `test-results/postgres/run-20260809T044238Z.metadata.txt`.
- `scripts/test/run_product_postgres_tests.sh tests/product/test_enh_e4_g03_generic_executor_boundary.py tests/product/test_enh_e4_g03_persistent_stage_execution.py tests/product/test_enh_e4_g03_acceptance_postgres.py tests/product/test_postgres_contract.py tests/product/test_enh_e4_g02_canonical_execution.py` → exit `0`, `22 passed`; migration current `20260809_product_0008 (head)`; evidence `test-results/postgres/run-20260809T044350Z.metadata.txt`.

The evidence metadata records the pre-commit SHA because verification preceded
the required implementation/test commit; the committed test content is the
content that was verified.

## Regression and scope

The final standard-runner command includes the G03 tests, PostgreSQL contract,
and G02 canonical execution regression: `22 passed`.

- `E4-TD-001`: `OPEN` until G05.
- `E4-TD-002`: `OPEN` until G05.
- G04 Result/Artifact consolidation and later gates remain unimplemented.

## Environment and working tree

The known standard-runner-external old DB configuration issue was not observed
in Trial 02 and was not modified. The unrelated deletion
`deploy/.nfs000000000076202f00000088` and untracked Trial 02 instruction file
were left untouched and excluded from both implementation/test commits.
