# 007 analysis_operation_regression

- Result: PASS
- Fixed Trial Candidate full SHA: `d2d5a9a7f6df352d787c8d561fce937012eef854`
- Tested Repository State full SHA: `9e85e4a6a2365869b48e5bc6c0b0ac6845698869`
- Exact command / method: `.venv/bin/python scripts/test/run_enh_e7_g04_trial02_cprs.py` (the versioned manifest explicitly includes the operation nodes listed below)
- Exit code: 0

## AC mapping

AC-G04-12, AC-G04-15.

## Direct assertion / predicate mapping

Direct nodes: `test_enh_e7_g04_p05_legacy_operation_resource_regression.py` (Data Quality read-only, Exploratory contracts, Causal/Predictive presentation-only navigation); `test_enh_e2_contract.py::test_project_delete_is_idempotent_archive_and_all_new_writes_are_guarded`; `test_enh_e2_contract.py::test_inference_rejects_missing_or_tampered_graph_outcome`; `test_enh_e3_api_worker_e2e.py::test_research_context_to_cross_family_results_lineage_annotation_and_export`; and `test_predictive_explanation_e3.py::test_api_worker_persists_explanation_model_card_artifacts_and_lineage`.

The latter four send required `Idempotency-Key` values before asserting archive, graph-outcome, Predictive execution, artifact, annotation/export, and lineage semantics.  This preserves FR-114 rather than bypassing it.

## Raw relevant evidence

The manifest regular bundle reports `89 passed in 10.61s`; all listed nodes are explicit members.  The PostgreSQL sub-bundle reports `4 passed in 0.72s` after migrations reached `20260813_product_0011 (head)`.

## Facts

Operation assertions passed after the documented API boundary.  Data Quality remains read-only, TIME_TREND/CHART are protected through their selected existing semantics, and no new operation architecture was introduced by the verification.

## Interpretation

AC-G04-12 operation semantics and the applicable protected API/persistence semantics pass.

## Protected contract relation

G02 operations; FR-114; current Project/domain/backend/API/persistence contract.

## Reproduction procedure

Run the command above.  The exact node list is versioned in `tests/product/manifests/enh_e7_g04_trial02_cprs.json`.

## Browser evidence

Browser operation-transition evidence is in Item 008; API and PostgreSQL evidence is recorded above.
