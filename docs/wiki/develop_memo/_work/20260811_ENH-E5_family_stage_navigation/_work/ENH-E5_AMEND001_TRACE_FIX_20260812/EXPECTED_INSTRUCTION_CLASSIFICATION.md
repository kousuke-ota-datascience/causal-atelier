# AMEND-001 Instruction Classification

- Authority commit: `6e9c59515abb8c5c5981f96df5ad87782a7cdfc7`
- Total instruction Markdown documents changed by AMEND-001: **35**
- Normative semantic changes: **2**
- Metadata-only changes: **33**

## Normative semantic changes — 2

- `G01/06_G01_P02_navigation_shell_ui.md`
- `G01/07_Ariadne_ENH-E5_G01_test_instruction.md`

## Metadata-only changes — 33

- `README.md`
- `G00/06_Ariadne_ENH-E5_G00_implementation_instruction.md`
- `G00/07_Ariadne_ENH-E5_G00_test_instruction.md`
- `G00/README.md`
- `G01/06_Ariadne_ENH-E5_G01_implementation_instruction.md`
- `G01/06_G01_P00_work_package_plan.md`
- `G01/06_G01_P01_route_and_navigation_state.md`
- `G01/06_G01_P03_history_and_global_regression.md`
- `G01/README.md`
- `G02/06_Ariadne_ENH-E5_G02_implementation_instruction.md`
- `G02/06_G02_P00_work_package_plan.md`
- `G02/06_G02_P01_predictive_compatibility_inventory.md`
- `G02/06_G02_P02_predictive_stage_recomposition.md`
- `G02/06_G02_P03_predictive_regression_and_candidate.md`
- `G02/07_Ariadne_ENH-E5_G02_test_instruction.md`
- `G02/README.md`
- `G03/06_Ariadne_ENH-E5_G03_implementation_instruction.md`
- `G03/06_G03_P00_work_package_plan.md`
- `G03/06_G03_P01_causal_stage_mapping.md`
- `G03/06_G03_P02_identification_estimation_separation.md`
- `G03/06_G03_P03_causal_regression_and_candidate.md`
- `G03/07_Ariadne_ENH-E5_G03_test_instruction.md`
- `G03/README.md`
- `G04/06_Ariadne_ENH-E5_G04_implementation_instruction.md`
- `G04/06_G04_P00_work_package_plan.md`
- `G04/06_G04_P01_exploratory_stage_mapping.md`
- `G04/06_G04_P02_visualization_and_findings_integration.md`
- `G04/06_G04_P03_exploratory_regression_and_candidate.md`
- `G04/07_Ariadne_ENH-E5_G04_test_instruction.md`
- `G04/README.md`
- `G05/06_Ariadne_ENH-E5_G05_implementation_instruction.md`
- `G05/07_Ariadne_ENH-E5_G05_test_instruction.md`
- `G05/README.md`

## Fail-closed invariants

The script fails unless:

1. the authority commit is an ancestor of HEAD;
2. that commit changed exactly the audited 35 instruction Markdown files;
3. the current instruction Markdown set is exactly the same 35-file set;
4. the 2 semantic documents already have a valid semantic AMEND-001 trace;
5. the final state has exactly 35 local AMEND-001 traces = 2 semantic + 33 metadata-only;
6. the Ledger contains the appended `TRACE-FIX-001` correction record.
