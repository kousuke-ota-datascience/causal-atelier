> **Historical structural snapshot（RD-02完了時点）:** 本書の文字数・原文章節再配置チェックはRD-02時点の構造検証である。RD-04で要件本文を変更した後の最新照合は[98_rd04_consistency_verification.md](../rd04_review/98_rd04_consistency_verification.md)に記録。ここでの原文文字数一致を現行全ファイルが原文と逐語一致する意味に解釈しない。

# RD-02 — 全5文書群の番号帯再編・元文書保全監査

**2026-11-16 / Status:** `STRUCTURE_REORGANIZED / ORIGINAL_CANONICAL_UNCHANGED / E11_DRAFTS_ISOLATED`。

## 1. Structural verification summary

| Family | Original source blob SHA | Source-derived section characters | Matched assigned characters | Current numbered files |
|---|---|---:|---:|---:|
| 10_requirements_definition | `40b83f29c67b4a39f6db5393be7534c5e892d656` | 64366 | 64366 | 23 |
| 21_logical_data_design | `72903b9ad48b5b7edabaa7bb1c2cace42aa46ce7` | 65639 | 65639 | 18 |
| 22_product_basic_design | `87196f2f03a7f3367724bc05fb254d1a4d98109e` | 56778 | 56778 | 19 |
| 23_api_interface_design | `131467f02222f105a49e6dfdbcec0f49cadb0f41` | 59300 | 59300 | 20 |
| 30_detailed_design | `04d83541e55ab0364500afb4b92ef55c10785a0c` | 65021 | 65021 | 25 |
| **Total** | | | | **105** |

- 出典：`docs/wiki/requirement_definition/`の5原正本。各`##`節と必要な`###`節を責務別に移管した際の原文由来文字数保全を検証。計算上の再編見出しやWrapperは検証外。
- 10系の旧FR195／NFR36／Scientific AR27は原文行・ID・既存Statusの一致をRD-02段階で確認。RD-03でFR19／NFR8／AR17を追加し、別途原文一致再検証PASS。
- 旧`_source_snapshots/`、原正本、既存Product Schema/Source Code、uv.lockを変更していない。
- 旧ファイル名はGit commit履歴で追跡可能。新`XX_YY`はカテゴリと責務を表し、原文の章番号・ID範囲をファイル名に利用しない。
- E11の正式化前草案は各`_drafts/`へ隔離し、Class Gap Registerは`30_detailed_design/_review/`に分離。DD全Classの物理仕様完備を意味しない。

## 2. Legacy split file → new responsibility file migration（57 entries）

*左列はRD-02直前のworking-copy旧ファイル。右列に分割後の主な継承先を示す。全ての原文は`_source_snapshots/`の固定blobから復元可能。*

| Old split file | New destination(s) |
|---|---|
| `10_requirements_definition/10_00_overall_RD.md` | `10_00_overall_RD.md` |
| `10_requirements_definition/10_01_capabilities_e2e.md` | `10_01_business_capabilities.md`、`10_02_use_cases_e2e.md` |
| `10_requirements_definition/10_02_fr_fr-001_to_fr-029.md` | `10_10_fr_project_context_data.md`、`10_11_fr_exploratory.md` |
| `10_requirements_definition/10_03_fr_fr-030_to_fr-060.md` | `10_11_fr_exploratory.md`、`10_12_fr_predictive.md`、`10_13_fr_causal.md` |
| `10_requirements_definition/10_04_fr_fr-061_to_fr-089.md` | `10_12_fr_predictive.md`、`10_14_fr_workflow_execution.md` |
| `10_requirements_definition/10_05_fr_fr-090_to_fr-118.md` | `10_15_fr_results_lineage.md`、`10_16_fr_navigation_ui.md`、`10_17_fr_api_cli.md` |
| `10_requirements_definition/10_06_fr_fr-119_to_fr-144.md` | `10_14_fr_workflow_execution.md`、`10_16_fr_navigation_ui.md`、`10_17_fr_api_cli.md`、`10_18_fr_security_operations.md` |
| `10_requirements_definition/10_07_fr_fr-145_to_fr-175.md` | `10_10_fr_project_context_data.md`、`10_11_fr_exploratory.md`、`10_12_fr_predictive.md`、`10_13_fr_causal.md`、`10_15_fr_results_lineage.md`、`10_16_fr_navigation_ui.md` |
| `10_requirements_definition/10_08_fr_fr-176_to_fr-184.md` | `10_12_fr_predictive.md`、`10_16_fr_navigation_ui.md` |
| `10_requirements_definition/10_09_nonfunctional.md` | `10_20_nfr_reproducibility.md`、`10_21_nfr_reliability_performance.md`、`10_22_nfr_security_compatibility.md` |
| `10_requirements_definition/10_10_science.md` | `10_20_nfr_reproducibility.md`、`10_30_ar_scientific_integrity.md`、`10_31_ar_estimand_inference.md`、`10_50_authorization_retention.md` |
| `10_requirements_definition/10_11_state_access_retention.md` | `10_40_state_lifecycle.md`、`10_50_authorization_retention.md` |
| `10_requirements_definition/10_12_scope_acceptance.md` | `10_90_scope_exclusions.md`、`10_91_acceptance_conditions.md` |
| `10_requirements_definition/10_13_change_history.md` | `10_99_change_log.md` |
| `10_requirements_definition/10_14_enh_e11_formal_requirement_publication_draft.md` | `_drafts/enh_e11_formal_requirement_publication_draft.md` |
| `21_logical_data_design/21_00_overall_LDD.md` | `21_00_overall_LDD.md` |
| `21_logical_data_design/21_01_relationships.md` | `21_01_entity_relationships.md` |
| `21_logical_data_design/21_02_entity_catalog_3_1_to_3_9.md` | `21_10_entity_project_context.md`、`21_11_entity_dataset_view.md`、`21_12_entity_specification_graph.md`、`21_13_entity_execution.md`、`21_14_entity_result_artifact_lineage.md` |
| `21_logical_data_design/21_03_entity_catalog_3_10_to_3_18.md` | `21_12_entity_specification_graph.md`、`21_13_entity_execution.md`、`21_14_entity_result_artifact_lineage.md`、`21_15_entity_membership_workspace.md` |
| `21_logical_data_design/21_04_value_catalog_4_1_to_4_8.md` | `21_20_value_domain_identifiers.md`、`21_21_value_navigation_context.md`、`21_22_value_analysis_specifications.md`、`21_23_value_execution_snapshot.md` |
| `21_logical_data_design/21_05_value_catalog_4_9_to_4_17.md` | `21_24_value_comparison_lineage.md`、`21_25_value_canonicalization.md` |
| `21_logical_data_design/21_06_state_model.md` | `21_30_state_models.md` |
| `21_logical_data_design/21_07_constraints.md` | `21_40_integrity_constraints.md`、`21_41_scientific_data_constraints.md` |
| `21_logical_data_design/21_08_history.md` | `21_99_change_log.md` |
| `21_logical_data_design/21_09_enh_e11_local_logical_model_draft.md` | `_drafts/enh_e11_local_logical_model_draft.md` |
| `22_product_basic_design/22_00_overall_BD.md` | `22_00_overall_BD.md` |
| `22_product_basic_design/22_01_information_architecture.md` | `22_01_information_architecture.md` |
| `22_product_basic_design/22_02_web_operation.md` | `22_02_web_operation.md` |
| `22_product_basic_design/22_03_navigation_application.md` | `22_03_navigation_application.md` |
| `22_product_basic_design/22_04_workflow_family_capabilities.md` | `22_04_workflow_core.md`、`22_05_family_exploratory.md`、`22_06_family_causal.md`、`22_07_family_predictive.md` |
| `22_product_basic_design/22_05_validation_results.md` | `22_08_validation_architecture.md`、`22_09_results_artifacts_lineage.md`、`22_10_comparison.md` |
| `22_product_basic_design/22_06_frontend_security_deploy.md` | `22_11_frontend_state.md`、`22_12_security.md`、`22_13_deployment.md`、`22_14_failure_model.md`、`22_15_schema_dependency.md`、`22_16_test_architecture.md` |
| `22_product_basic_design/22_07_history_e8.md` | `22_17_stage_contents_e8_effective.md`、`22_99_change_log.md` |
| `22_product_basic_design/22_08_enh_e11_causal_cli_basic_design_draft.md` | `_drafts/enh_e11_causal_cli_basic_design_draft.md` |
| `23_api_interface_design/23_00_overall_API.md` | `23_00_overall_IF.md` |
| `23_api_interface_design/23_01_browser_navigation.md` | `23_20_browser_navigation.md` |
| `23_api_interface_design/23_02_web_api_5_1_to_5_3.md` | `23_10_api_project_context.md`、`23_11_api_dataset_view.md`、`23_12_api_analysis_specification.md` |
| `23_api_interface_design/23_03_web_api_5_4_to_5_6.md` | `23_13_api_exploratory.md`、`23_14_api_causal.md`、`23_15_api_predictive.md` |
| `23_api_interface_design/23_04_web_api_5_7_to_5_9.md` | `23_16_api_execution.md`、`23_17_api_result_comparison_lineage.md`、`23_18_api_annotation_artifact.md` |
| `23_api_interface_design/23_05_web_api_5_10_to_5_10.md` | `23_19_api_frontend_support.md` |
| `23_api_interface_design/23_06_worker_cli.md` | `23_30_worker_runtime.md`、`23_40_cli_library.md` |
| `23_api_interface_design/23_07_crosscut_verification.md` | `23_50_error_contract.md`、`23_51_idempotency_contract.md`、`23_52_versioning_compatibility.md`、`23_90_interface_verification.md` |
| `23_api_interface_design/23_08_history.md` | `23_99_change_log.md` |
| `23_api_interface_design/23_09_enh_e11_cli_and_port_interface_draft.md` | `_drafts/enh_e11_cli_and_port_interface_draft.md` |
| `30_detailed_design/30_00_overall_DD.md` | `30_00_overall_DD.md` |
| `30_detailed_design/30_01_domain_context.md` | `30_10_domain_resources.md`、`30_11_schema_canonicalization.md`、`30_41_navigation_routing.md` |
| `30_detailed_design/30_02_planning_execution.md` | `30_12_context_analysis_view.md`、`30_20_planning_validation.md`、`30_21_execution_runtime.md` |
| `30_detailed_design/30_03_project_workspace.md` | `30_40_project_workspace.md` |
| `30_detailed_design/30_04_exploratory_causal.md` | `30_30_exploratory.md`、`30_31_causal_setup_discovery.md`、`30_32_causal_identification.md`、`30_33_causal_estimation_effects.md`、`30_34_causal_diagnostics_sensitivity.md` |
| `30_detailed_design/30_05_predictive_setup_and_workflow.md` | `30_35_predictive_training.md`、`30_36_predictive_explanation.md`、`30_37_predictive_model_management.md` |
| `30_detailed_design/30_06_predictive_advanced_xai.md` | `30_35_predictive_training.md`、`30_36_predictive_explanation.md` |
| `30_detailed_design/30_07_results_frontend.md` | `30_41_navigation_routing.md`、`30_42_results_lineage.md`、`30_43_operation_availability.md` |
| `30_detailed_design/30_08_persistence_security.md` | `30_50_persistence_artifacts.md`、`30_51_security.md`、`30_52_failure_handling.md` |
| `30_detailed_design/30_09_tests_history.md` | `30_90_verification_traceability.md`、`30_99_change_log.md` |
| `30_detailed_design/30_10_existing_classes_physical_design_verified.md` | `30_01_class_design_template.md`、`30_10_domain_resources.md`、`30_20_planning_validation.md`、`30_21_execution_runtime.md`、`30_50_persistence_artifacts.md`、`30_60_cli_adapters.md` |
| `30_detailed_design/30_11_enh_e11_proposed_physical_class_design.md` | `_drafts/enh_e11_proposed_physical_class_design.md` |
| `30_detailed_design/30_12_physical_design_gap_register.md` | `_review/physical_design_gap_register.md` |

## 3. Boundaries

- `90_structural_split_verification.md`は以前の分割構造の監査であり、本書を新番号体系の監査とする。
- 正式RD-03要件発行の境界・未充足Status・Scope/Method/UCは [RD-03 audit](../rd03_review/96_rd03_formal_requirement_traceability.md)で別管理する。
- 22/30のクラス詳細記述の再レビュー、RD-01逐条SPLIT/REWRITE候補の全文反映、設計へのMigration／章内Prefixの全面更新は未完。
