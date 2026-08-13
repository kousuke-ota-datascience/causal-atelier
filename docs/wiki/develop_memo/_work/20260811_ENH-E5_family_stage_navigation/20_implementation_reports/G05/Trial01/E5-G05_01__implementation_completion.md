# ENH-E5 G05 Trial 01 — Implementation Completion Report

- PROJECT_NAME: Ariadne
- ENHANCE_ID: ENH-E5
- GATE_ID: G05
- TRIAL_NO: 01
- Normative contract: `docs/wiki/develop_memo/_work/20260811_ENH-E5_family_stage_navigation/10_enhance_instruction/G05/06_Ariadne_ENH-E5_G05_implementation_instruction.md`
- START_SHA: `92afd1802e52db813b4fc4c7d6e1c7d2280b6a7b`
- Execution status: `READY_FOR_TEST`
- FIXED_TRIAL_CANDIDATE_SHA: `5cf0caf515b8e57fc114eabea0efd9acffe23e62`

## Implemented

- Comparison projections now return `semantic_compatible`,
  `direct_metric_comparable`, `compatibility_reasons`, and
  `direct_comparison_blockers`; semantic mismatch is represented in the
  response instead of as a request failure.
- Idempotency commands reject missing keys with
  `IDEMPOTENCY_KEY_REQUIRED`, include project/scope identity in the request
  hash, and cover project export, workspace annotation, lineage link, and
  predictive execution submission.
- `StageAttempt.effective_random_seed` was added to domain/ORM/repository,
  processor propagation, read response, and migration
  `20260813_product_0011`.
- Execution runtime metadata records the required environment fields and
  versions of actually installed scientific/runner dependencies without
  importing optional future libraries.

## Changed files

- `src/ariadne/interfaces/web_api/error_handlers.py`
- `src/ariadne/interfaces/web_api/idempotency.py`
- `src/ariadne/interfaces/web_api/routers/predictive_workflow.py`
- `src/ariadne/interfaces/web_api/routers/product_closure.py`
- `src/ariadne/interfaces/worker/execution_processor.py`
- `src/ariadne/product/application/execution_service.py`
- `src/ariadne/product/application/predictive_workflow_service.py`
- `src/ariadne/product/application/product_closure_service.py`
- `src/ariadne/product/domain/stage_execution.py`
- `src/ariadne/product/persistence/orm_models.py`
- `src/ariadne/product/persistence/repositories.py`
- `src/ariadne/product/workflow/executor.py`
- `product_migrations/versions/20260813_product_0011_enh_e5_reproducibility.py`

## Verification

| Command | Result |
| --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m compileall -q src product_migrations` | PASS |
| `PYTHONDONTWRITEBYTECODE=1 .venv/bin/pytest -q tests/product/test_enh_e5_g00_navigation.py tests/product/test_enh_e5_g01_navigation_state.py tests/product/test_enh_e5_g02_p01_predictive_compatibility.py tests/product/test_enh_e5_g03_p03_causal_runtime_regression.py tests/product/test_enh_e5_g04_p03_exploratory_boundary.py` | PASS (16 passed) |
| `PYTHONDONTWRITEBYTECODE=1 .venv/bin/pytest -q tests/product/test_results_lineage_export_e3.py tests/product/test_cross_analysis_lineage_e3.py tests/product/test_enh_e4_g03_persistent_stage_execution.py tests/product/test_predictive_api_worker_e2e_e3.py` | FAIL (6 failed, 3 passed, 1 skipped) |
| `git diff --check` | PASS |
| continuation focused regression: results/lineage/stage/predictive plus G00–G04 selection | PASS (25 passed, 1 skipped) |
| `PYTHONDONTWRITEBYTECODE=1 .venv/bin/pytest -q --maxfail=1` | PASS |

## Continuation failure classification

| Test | Failing request / assertion | Expected | Actual | G05 classification | Corrective action |
| --- | --- | --- | --- | --- | --- |
| `test_unified_results_summary_and_compatible_comparison_do_not_rank_metrics` | Cross-family `POST /comparisons` | old `422 INVALID_SCHEMA` | compatibility projection | comparison is query scope; semantic mismatch must not be request failure | assert `semantic_compatible=false`, `direct_metric_comparable=false`, no rank |
| `test_annotation_target_matrix_history_and_export_manifest_contracts` | `POST /workspace-annotations` | `201` | `400 IDEMPOTENCY_KEY_REQUIRED` | WorkspaceAnnotation create is required idempotency scope | add a unique `Idempotency-Key` to each caller; serialize replay response datetimes |
| `test_project_access_controlled_download_hash_and_sensitive_output_policy` | `POST /exports` | `201` | `400 IDEMPOTENCY_KEY_REQUIRED` | Project Export create is required idempotency scope | add `Idempotency-Key`; preserve the authorization assertion's purpose with a key on the forbidden annotation request |
| `test_project_lineage_combines_families_and_explicit_relations` | `POST /lineage-links` | `201` | `400 IDEMPOTENCY_KEY_REQUIRED` | explicit uniqueness-protected lineage link is excluded from idempotency scope | remove idempotency transport requirement from this route; do not alter caller |
| `test_explicit_lineage_link_rejects_cross_project_resources` | cross-project `POST /lineage-links` | `422 PROJECT_BOUNDARY_VIOLATION` | `400 IDEMPOTENCY_KEY_REQUIRED` before boundary check | same excluded command; implementation defect | remove the erroneous key gate so the boundary validation is reached |
| `test_predictive_execution_plan_async_worker_results_artifacts_and_lineage` | expected canonical input nodes/edges | context, specification and plan input projections | actual nodes were only `DatasetVersion`, `Execution`, `Result`, `Artifact` | implementation defect: canonical read projection omitted deterministic snapshot/FK inputs | project `ResearchContextVersion`, `AnalysisSpecification`, and `ExecutionPlan` as typed read edges; measured artifact ownership is `Result(TRAINING) → Artifact`, which replaces obsolete direct `Execution → Artifact` expectation |

No assertion was removed, weakened, skipped, or marked xfail. Transport-caller
changes were made only for G05 required idempotency scopes; the excluded lineage
link caller was deliberately left keyless.

## Remaining work

None. The candidate is ready for independent test execution; this report does
not make a Gate PASS/FAIL decision.
