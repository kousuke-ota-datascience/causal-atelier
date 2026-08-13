# ENH-E5 G05 Trial 01 — Implementation Completion Report

- PROJECT_NAME: Ariadne
- ENHANCE_ID: ENH-E5
- GATE_ID: G05
- TRIAL_NO: 01
- Normative contract: `docs/wiki/develop_memo/_work/20260811_ENH-E5_family_stage_navigation/10_enhance_instruction/G05/06_Ariadne_ENH-E5_G05_implementation_instruction.md`
- START_SHA: `92afd1802e52db813b4fc4c7d6e1c7d2280b6a7b`
- Execution status: `BLOCKED_IMPLEMENTATION`
- FIXED_TRIAL_CANDIDATE_SHA: none

## Implemented (uncommitted; not a candidate)

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

## Changed files (uncommitted)

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

## Blocker / remaining work

The required gate-wide verification is not green. Five failures are old tests
that issue durable export/annotation/lineage mutations without the now-required
`Idempotency-Key`; their expectation conflicts with the frozen G05 contract.
One predictive lineage failure also requires investigation before candidate
creation. No test was weakened or changed to hide these failures.

During execution, unrelated untracked files appeared under
`docs/wiki/develop_memo/_work/20260811_ENH-E5_family_stage_navigation/_work/agentic_workflow_template_update_v3_1/`.
They were not modified or staged.
