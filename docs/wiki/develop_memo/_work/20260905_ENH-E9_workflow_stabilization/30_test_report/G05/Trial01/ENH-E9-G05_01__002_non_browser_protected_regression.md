# ENH-E9 G05 Trial 01 Test Item 002 — Non-browser protected regression

> **Document class:** Evidence Artifact

- Status: PASS / UNIT, INTEGRATION, FRONTEND_CONTRACT
- Fixed Candidate: `2959afcf03261cba50edf13bf334038519b6c476`
- Tested state: `7c6a97953615c98c36d3bf1d5afa1af005771437`
- 07: `10_enhance_instruction/G05/07_Ariadne_ENH-E9_G05_test_instruction.md` (FROZEN)
- Timestamp: 2026-09-06T09:40:48Z

## Exact command

```bash
python3 -c "compile(run_critical_causal_journey_source, 'runner', 'exec')"
git diff --check
uv run pytest -q tests/enhancement/enh_e9/g01/frontend/test_analysis_view_context_clarity.py tests/enhancement/enh_e9/g02/frontend/test_discovery_copy_help_overflow.py tests/enhancement/enh_e9/g02/frontend/test_selection_comparison_clarity.py tests/enhancement/enh_e9/g02/frontend/test_adoption_feedback_export.py tests/enhancement/enh_e9/g03/frontend/test_identification_input_ergonomics.py tests/enhancement/enh_e9/g03/frontend/test_estimation_submission_regression.py tests/enhancement/enh_e9/g04/scientific/test_weighting_applicability_contract.py tests/enhancement/enh_e9/g04/scientific/test_ipw_weighting_persistence.py tests/enhancement/enh_e9/g04/scientific/test_balance_applicability.py tests/enhancement/enh_e9/g04/frontend/test_causal_result_presentation.py tests/enhancement/enh_e9/g04/frontend/test_structured_diagnostics_consumption.py tests/enhancement/enh_e9/g05/integration/test_critical_causal_journey_readiness.py tests/product/test_enh_e2_contract.py::test_graph_candidate_lifecycle_and_comparison_are_state_derived tests/product/test_enh_e2_contract.py::test_inference_rejects_missing_or_tampered_graph_outcome tests/product/test_enh_e5_g03_p02_identification_estimation_separation.py tests/product/test_enh_e5_g03_p03_causal_runtime_regression.py tests/product/test_enh_e8_g02_p02_causal_stage_surface_separation.py
docker compose -f compose.yaml -f compose.e1a.yaml --profile e2e config --quiet
```

Exit code: `0`.

```text
..................................................                       [100%]
50 passed in 5.64s
```

The suite passes G01 Context/View, G02 Discovery/adoption, G03 lineage, G04 structured effects/diagnostics, G05 runner readiness, and protected stage/navigation contracts. This covers AC1–AC9 non-browser primary/protected evidence. Test Agent production/migration/dependency changes: NONE.
