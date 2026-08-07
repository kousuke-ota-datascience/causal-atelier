# ENH-E3 G6 Trial 005 Implementation Completion Report

Gate: G6 Product Closure

Trial: 005

Status: READY_FOR_TEST

Implementation base commit: `518c559cb6b71b2a894cffc2a0d66beac7dc130c`

Implementation completed commit: `9505a4bf6e6738104412b1e45afaea9324cbdcea`

Handoff report commit: omitted because this report is contained by that commit

Migration head: `20260807_product_0006` (unchanged; migration execution not performed)

## Gate decision reviewed

- Gate decision: `G6_004_999_gate_decision.md`
- Failing item: G6-006 Browser E2E `E2E-06-regression`.
- Observed failure: `GET /projects/{project_id}/executions/{execution_id}/results` returned HTTP 404 after a predictive regression run.
- All other G6 items, full active pytest, scientific, PostgreSQL contract, and G1–G5 regression checks passed in Trial 004.

## Root cause

**Fact:** `POST /predictive/split-validations` persists a completed `FamilyExecutionOrm` with `analysis_family="PREDICTIVE"` but no `analysis_specification_id`. It is an internal validation execution used to preserve its partition artifact and lineage.

**Fact:** `GET /projects/{project_id}/executions` exposed that internal record. The predictive result endpoint deliberately rejects it, because its execution lookup requires a predictive analysis specification.

**Inference:** During E2E-06, the browser runner selected this newly created, completed split-validation record by family and status before selecting the subsequently completed predictive workflow. Its result request therefore returned the observed 404.

## Implemented correction

- Updated `PredictiveWorkflowService.list_family_executions` to exclude only `PREDICTIVE` family records without an `analysis_specification_id`.
- Retained other family executions, including exploratory executions without an analysis specification.
- Retained split-validation persistence, partition artifacts, and lineage; only the user-visible generic execution list is filtered.
- Added a regression assertion that an execution created by split validation is not returned by `GET /projects/{project_id}/executions`.

## Changed production files

- `src/ariadne/product/application/predictive_workflow_service.py`

## Changed test files

- `tests/product/test_predictive_split_api_e3.py`

## Added migration

- None. This is an API visibility correction with no schema change.

## Static verification

- Parsed both changed Python files with `ast.parse`: success.
- Confirmed the generic execution-list filter excludes only predictive rows lacking `analysis_specification_id`: success.
- Confirmed the regression assertion requests the public execution list and excludes the split-validation execution ID: success.
- `git diff --check`: clean before commit.

## Known limitations

- Coding Agent did not run pytest, Docker/Browser E2E, scientific benchmarks, PostgreSQL contract tests, or migrations, following the implementation instruction.
- G6 Gate Decision is not yet PASS. The new browser audit must confirm that E2E-06 selects a result-bearing predictive execution and completes successfully.

## Required Test Agent focus

1. Run G6-006 Browser E2E and confirm E2E-06 regression retrieves `EVALUATION_RESULT` with primary metric `RMSE` without HTTP 404.
2. Run the predictive split API regression test and confirm split validation artifacts and lineage remain available while its internal execution is absent from the generic execution list.
3. Re-run the G6 gate and required regression suites under 07b.

Test execution by Coding Agent: NOT PERFORMED
