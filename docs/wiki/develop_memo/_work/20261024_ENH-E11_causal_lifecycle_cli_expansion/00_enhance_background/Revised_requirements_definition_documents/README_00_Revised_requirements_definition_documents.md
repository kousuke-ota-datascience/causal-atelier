# ENH-E11 — Revised Requirements & Design (Working Copy)

**State:** `STRUCTURAL_COPY_DRAFT / ENH_E11_FR_NFR_AR_PUBLICATION_PENDING`  
**Source:** `docs/wiki/requirement_definition/` at commit `3ba5fe2465ec591f0da7f998c21a5241984b73dc`  
**Policy:** Original canonical documents remain unchanged. The files here are a working copy, **not** formally published ENH-E11 FR/NFR/AR, ADR, Gate or implementation approval.

## 1. Scope and authority

- Lossless source files are under `_source_snapshots/` using the original blob SHA; the concept document is also present at the root.
- The five baseline documents are split into topic files. Sections and FR rows have been preserved from the originals; relative Markdown links in split text target the *pinned original source*.
- Every `XX_00_overall_*.md` holds baseline shared policy and has an index role. Enhancement deltas must be labeled as drafts until reviewed and approved at the canonical level.
- DEC-SR04-09 approves 68 Scope dispositions and semantic/architecture policy, **not** published requirement clauses, detailed ADR, Gate Freeze, scientific acceptance, or coding.

## 2. Document index

### 10 requirements_definition

Source: `_source_snapshots/10_requirements_definition.md` (blob `40b83f29c67b4a39f6db5393be7534c5e892d656`)

- [10_00_overall_RD.md](10_requirements_definition/10_00_overall_RD.md)
- [10_01_capabilities_e2e.md](10_requirements_definition/10_01_capabilities_e2e.md)
- [10_02_fr_fr-001_to_fr-029.md](10_requirements_definition/10_02_fr_fr-001_to_fr-029.md)
- [10_03_fr_fr-030_to_fr-060.md](10_requirements_definition/10_03_fr_fr-030_to_fr-060.md)
- [10_04_fr_fr-061_to_fr-089.md](10_requirements_definition/10_04_fr_fr-061_to_fr-089.md)
- [10_05_fr_fr-090_to_fr-118.md](10_requirements_definition/10_05_fr_fr-090_to_fr-118.md)
- [10_06_fr_fr-119_to_fr-144.md](10_requirements_definition/10_06_fr_fr-119_to_fr-144.md)
- [10_07_fr_fr-145_to_fr-175.md](10_requirements_definition/10_07_fr_fr-145_to_fr-175.md)
- [10_08_fr_fr-176_to_fr-184.md](10_requirements_definition/10_08_fr_fr-176_to_fr-184.md)
- [10_09_nonfunctional.md](10_requirements_definition/10_09_nonfunctional.md)
- [10_10_science.md](10_requirements_definition/10_10_science.md)
- [10_11_state_access_retention.md](10_requirements_definition/10_11_state_access_retention.md)
- [10_12_scope_acceptance.md](10_requirements_definition/10_12_scope_acceptance.md)
- [10_13_change_history.md](10_requirements_definition/10_13_change_history.md)

### 21 logical_data_design

Source: `_source_snapshots/21_logical_data_design.md` (blob `72903b9ad48b5b7edabaa7bb1c2cace42aa46ce7`)

- [21_00_overall_LDD.md](21_logical_data_design/21_00_overall_LDD.md)
- [21_01_relationships.md](21_logical_data_design/21_01_relationships.md)
- [21_02_entity_catalog_3_1_to_3_9.md](21_logical_data_design/21_02_entity_catalog_3_1_to_3_9.md)
- [21_03_entity_catalog_3_10_to_3_18.md](21_logical_data_design/21_03_entity_catalog_3_10_to_3_18.md)
- [21_04_value_catalog_4_1_to_4_8.md](21_logical_data_design/21_04_value_catalog_4_1_to_4_8.md)
- [21_05_value_catalog_4_9_to_4_17.md](21_logical_data_design/21_05_value_catalog_4_9_to_4_17.md)
- [21_06_state_model.md](21_logical_data_design/21_06_state_model.md)
- [21_07_constraints.md](21_logical_data_design/21_07_constraints.md)
- [21_08_history.md](21_logical_data_design/21_08_history.md)

### 22 product_basic_design

Source: `_source_snapshots/22_product_basic_design.md` (blob `87196f2f03a7f3367724bc05fb254d1a4d98109e`)

- [22_00_overall_BD.md](22_product_basic_design/22_00_overall_BD.md)
- [22_01_information_architecture.md](22_product_basic_design/22_01_information_architecture.md)
- [22_02_web_operation.md](22_product_basic_design/22_02_web_operation.md)
- [22_03_navigation_application.md](22_product_basic_design/22_03_navigation_application.md)
- [22_04_workflow_family_capabilities.md](22_product_basic_design/22_04_workflow_family_capabilities.md)
- [22_05_validation_results.md](22_product_basic_design/22_05_validation_results.md)
- [22_06_frontend_security_deploy.md](22_product_basic_design/22_06_frontend_security_deploy.md)
- [22_07_history_e8.md](22_product_basic_design/22_07_history_e8.md)

### 23 api_interface_design

Source: `_source_snapshots/23_api_interface_design.md` (blob `131467f02222f105a49e6dfdbcec0f49cadb0f41`)

- [23_00_overall_API.md](23_api_interface_design/23_00_overall_API.md)
- [23_01_browser_navigation.md](23_api_interface_design/23_01_browser_navigation.md)
- [23_02_web_api_5_1_to_5_3.md](23_api_interface_design/23_02_web_api_5_1_to_5_3.md)
- [23_03_web_api_5_4_to_5_6.md](23_api_interface_design/23_03_web_api_5_4_to_5_6.md)
- [23_04_web_api_5_7_to_5_9.md](23_api_interface_design/23_04_web_api_5_7_to_5_9.md)
- [23_05_web_api_5_10_to_5_10.md](23_api_interface_design/23_05_web_api_5_10_to_5_10.md)
- [23_06_worker_cli.md](23_api_interface_design/23_06_worker_cli.md)
- [23_07_crosscut_verification.md](23_api_interface_design/23_07_crosscut_verification.md)
- [23_08_history.md](23_api_interface_design/23_08_history.md)

### 30 detailed_design

Source: `_source_snapshots/30_detailed_design.md` (blob `04d83541e55ab0364500afb4b92ef55c10785a0c`)

- [30_00_overall_DD.md](30_detailed_design/30_00_overall_DD.md)
- [30_01_domain_context.md](30_detailed_design/30_01_domain_context.md)
- [30_02_planning_execution.md](30_detailed_design/30_02_planning_execution.md)
- [30_03_project_workspace.md](30_detailed_design/30_03_project_workspace.md)
- [30_04_exploratory_causal.md](30_detailed_design/30_04_exploratory_causal.md)
- [30_05_predictive_setup_and_workflow.md](30_detailed_design/30_05_predictive_setup_and_workflow.md)
- [30_06_predictive_advanced_xai.md](30_detailed_design/30_06_predictive_advanced_xai.md)
- [30_07_results_frontend.md](30_detailed_design/30_07_results_frontend.md)
- [30_08_persistence_security.md](30_detailed_design/30_08_persistence_security.md)
- [30_09_tests_history.md](30_detailed_design/30_09_tests_history.md)

## 3. Approval / verification boundary

| Object | Status |
|---|---|
| Baseline original at `docs/wiki/requirement_definition` | Current approved source; not modified here |
| These split working copies | `STRUCTURAL_COPY_DRAFT` |
| DEC09 Scope & requirement meaning | `OWNER_APPROVED` |
| New canonical FR/NFR/AR / detailed ADR / schema | `PENDING` |
| Gate06/07 Freeze, Science T2/T3, License approval, Coding authorization | `NOT_COMPLETED` |

DEC09 authority: [Scope / Requirements / Architecture / Gate owner record](../../working_notes/20261116_sr04_dec09_scope_requirements_architecture_gate_integrated_owner_approval.md).

## 4. Source copy and historical note

The prior README in this folder was written for approved snapshots only. This revised index explicitly separates baseline copies from working drafts; presence in this folder does not imply approval. Retain the original effective-snapshot text and change logs as evidence, while using new E11 draft addenda for proposed semantics.

## 5. ENH-E11 revision candidates (not canonical)

- [10_14 — Candidate formal FR/NFR/AR and §11 diff](10_requirements_definition/10_14_enh_e11_formal_requirement_publication_draft.md)
- [21_09 — Local logical model](21_logical_data_design/21_09_enh_e11_local_logical_model_draft.md)
- [22_08 — Causal CLI basic architecture](22_product_basic_design/22_08_enh_e11_causal_cli_basic_design_draft.md)
- [23_09 — CLI/Scientific Port interface](23_api_interface_design/23_09_enh_e11_cli_and_port_interface_draft.md)
- [30_10 — Existing verified classes](30_detailed_design/30_10_existing_classes_physical_design_verified.md)
- [30_11 — Proposed E11 physical class contracts](30_detailed_design/30_11_enh_e11_proposed_physical_class_design.md)
- [30_12 — Physical specification template and gap register](30_detailed_design/30_12_physical_design_gap_register.md)

**Note:** structural copies have source-approved content, but formal new requirements/design remain pending; these E11 addenda carry a separate working-draft status.
