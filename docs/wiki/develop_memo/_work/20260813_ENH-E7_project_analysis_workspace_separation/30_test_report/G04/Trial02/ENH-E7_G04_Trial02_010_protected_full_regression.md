# 010 protected_current_regression_bundle

- Result: PASS
- Fixed Trial Candidate full SHA: `d2d5a9a7f6df352d787c8d561fce937012eef854`
- Tested Repository State full SHA: `9e85e4a6a2365869b48e5bc6c0b0ac6845698869`
- Exact command / method: `.venv/bin/python scripts/test/run_enh_e7_g04_trial02_cprs.py`
- Exit code: 0

## AC mapping

AC-G04-13, AC-G04-15.

## Direct assertion / predicate mapping

For Trial02, Gate 07 Test Item 010 is applied through `09_ENH-E7_G04_Trial02_Gate_Contract_Amendment.md` section 7: AC-G04-15 and its MUST severity are unchanged; the method is the versioned Current Protected Regression Set (CPRS), not an unscoped repository-wide pytest interpretation.  `tests/product/manifests/enh_e7_g04_trial02_cprs.json` explicitly enumerates 89 regular pytest node IDs, 4 PostgreSQL node IDs, one exact browser command, KBE-01..09 replacement nodes, and their re-enable conditions.

## Raw relevant evidence

Regular CPRS: `89 passed in 10.61s`.  Browser command: PASS, five scenarios PASS and no console/page error.  PostgreSQL prerequisite: available; migrations reach `20260813_product_0011 (head)`; selected persistence suite: `4 passed in 0.72s`, `run_exit_code=0` in `test-results/postgres/run-20260815T051750Z.txt`.

## Known Baseline Exclusions

| KBE | Trial01 / G02 baseline evidence | Passing replacement node | Re-enable condition |
| --- | --- | --- | --- |
| KBE-01 | old fixed-20 status assertion failed on both Trial01 and `ba9fd56` | `test_scientific_status_is_exact_current_result_type_design_contract` | current ResultType/status assertion passes and rejects undocumented combinations. |
| KBE-02 | archive request lacked Idempotency-Key and returned 400 | `test_project_delete_is_idempotent_archive_and_all_new_writes_are_guarded` | header-valid archive idempotence and guarded writes pass. |
| KBE-03 | graph-outcome request lacked Idempotency-Key and returned 400 | `test_inference_rejects_missing_or_tampered_graph_outcome` | header-valid mismatch/required predicates pass. |
| KBE-04 | Predictive submit lacked Idempotency-Key and had no execution_id | `test_research_context_to_cross_family_results_lineage_annotation_and_export` | header-valid execution/results/annotation/export/lineage predicates pass. |
| KBE-05 | old six-route token assertion conflicted with canonical routing | `test_g6_frontend_closes_context_common_selectors_results_and_canonical_analysis_routes` | rewritten canonical-route/visible-state test passes; no token restoration. |
| KBE-06 | independent Explore workspace assertion conflicted with Family/Stage surface | `test_exploratory_family_is_a_canonical_non_causal_analysis_stage_surface` | mapped Exploratory route/history predicates pass. |
| KBE-07 | Predictive submit lacked Idempotency-Key and had no execution_id | `test_api_worker_persists_explanation_model_card_artifacts_and_lineage` | header-valid explanation/model-card/artifact/lineage predicates pass. |
| KBE-08 | independent Predictive workspace assertion was obsolete | `test_predictive_family_exposes_complete_g5_backend_vertical_slice_in_analysis_workspace` | mapped Predictive stage/capability/route predicates pass. |
| KBE-09 | old six-route deep-link assertion was obsolete | `test_project_shell_normalizes_legacy_routes_and_restores_predictive_canonical_deep_links` | canonical deep-link, normalization, reload, Back/Forward predicates pass. |

The complete baseline references, node IDs, and re-enable text are versioned in `tests/product/manifests/enh_e7_g04_trial02_cprs.json`.

## Facts

CPRS-01 G03 surface architecture, CPRS-02 G01 Project semantics, CPRS-03 G02 Analysis/cross-surface semantics, CPRS-04 ENH-E6 Family/Stage semantics, CPRS-05 current domain/API/persistence semantics, and CPRS-06 G04 reintegration all passed their explicit blocking members.  KBE-01..09 were not silently deselected: each maps to a passing replacement node in the manifest.  KBE-02/03/04/07 retain the required Idempotency-Key boundary; KBE-01 rejects invalid ResultType/status combinations; KBE-05/06/08/09 directly verify canonical Family/Stage routing rather than historical shell tokens.

## Interpretation

The amended method directly supports AC-G04-15's unchanged semantic claim: no protected semantic regression was observed in the current authoritative protected set.  This does not rewrite Trial01 evidence or assert that the historical broad-suite failures passed.

## Protected contract relation

Gate 07 section 8, as amended for Trial02+ only by Amendment 09 sections 3–7; G01/G02/G03/ENH-E6 and Project/domain/backend/API/persistence protected semantics.

## Reproduction procedure

Run the command above from repository root.  Do not replace it with a directory glob; inspect the committed manifest for every selected node and every KBE replacement/re-enable condition.

## Browser evidence

`test-results/browser_e2e/enh-e7-project-integration-evidence.json`; screenshots listed in Item 008.  PostgreSQL evidence is `test-results/postgres/run-20260815T051750Z.txt` and its metadata companion.
