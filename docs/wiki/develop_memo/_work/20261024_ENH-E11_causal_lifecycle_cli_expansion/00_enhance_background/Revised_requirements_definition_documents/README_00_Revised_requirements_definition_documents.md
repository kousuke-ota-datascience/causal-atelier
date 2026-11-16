# ENH-E11 — Revised Requirements & Design Documents

**Status (2026-11-16):** `RD02_REORGANIZED / RD03_FORMAL_CLAUSES_ISSUED_IN_REVISED_COPY / OWNER_SHA_FINAL_REVIEW_PENDING / SCIENCE_AND_GATE_NOT_RUN`.

**Source authority:** 原正本 `docs/wiki/requirement_definition/` を変更せず、元の5文書を `_source_snapshots/` に固定blobのまま保管。Owner DEC09は実装Scopeと要件意味・Architecture方針を承認。今回のE11新FR/NFR/Scientific ARは**改訂版working-copyで条文・Status・Traceを発行**したものであり、元正本へのpromote、Coding、Science/Gate/Legalの承認ではない。

## 1. Current document index（全105 numbered files）

### 10_requirements_definition

- [10_00_overall_RD.md](10_requirements_definition/10_00_overall_RD.md)
- [10_01_business_capabilities.md](10_requirements_definition/10_01_business_capabilities.md)
- [10_02_use_cases_e2e.md](10_requirements_definition/10_02_use_cases_e2e.md)
- [10_10_fr_project_context_data.md](10_requirements_definition/10_10_fr_project_context_data.md)
- [10_11_fr_exploratory.md](10_requirements_definition/10_11_fr_exploratory.md)
- [10_12_fr_predictive.md](10_requirements_definition/10_12_fr_predictive.md)
- [10_13_fr_causal.md](10_requirements_definition/10_13_fr_causal.md)
- [10_14_fr_workflow_execution.md](10_requirements_definition/10_14_fr_workflow_execution.md)
- [10_15_fr_results_lineage.md](10_requirements_definition/10_15_fr_results_lineage.md)
- [10_16_fr_navigation_ui.md](10_requirements_definition/10_16_fr_navigation_ui.md)
- [10_17_fr_api_cli.md](10_requirements_definition/10_17_fr_api_cli.md)
- [10_18_fr_security_operations.md](10_requirements_definition/10_18_fr_security_operations.md)
- [10_20_nfr_reproducibility.md](10_requirements_definition/10_20_nfr_reproducibility.md)
- [10_21_nfr_reliability_performance.md](10_requirements_definition/10_21_nfr_reliability_performance.md)
- [10_22_nfr_security_compatibility.md](10_requirements_definition/10_22_nfr_security_compatibility.md)
- [10_30_ar_scientific_integrity.md](10_requirements_definition/10_30_ar_scientific_integrity.md)
- [10_31_ar_estimand_inference.md](10_requirements_definition/10_31_ar_estimand_inference.md)
- [10_32_scientific_method_scope.md](10_requirements_definition/10_32_scientific_method_scope.md)
- [10_40_state_lifecycle.md](10_requirements_definition/10_40_state_lifecycle.md)
- [10_50_authorization_retention.md](10_requirements_definition/10_50_authorization_retention.md)
- [10_90_scope_exclusions.md](10_requirements_definition/10_90_scope_exclusions.md)
- [10_91_acceptance_conditions.md](10_requirements_definition/10_91_acceptance_conditions.md)
- [10_99_change_log.md](10_requirements_definition/10_99_change_log.md)

### 21_logical_data_design

- [21_00_overall_LDD.md](21_logical_data_design/21_00_overall_LDD.md)
- [21_01_entity_relationships.md](21_logical_data_design/21_01_entity_relationships.md)
- [21_10_entity_project_context.md](21_logical_data_design/21_10_entity_project_context.md)
- [21_11_entity_dataset_view.md](21_logical_data_design/21_11_entity_dataset_view.md)
- [21_12_entity_specification_graph.md](21_logical_data_design/21_12_entity_specification_graph.md)
- [21_13_entity_execution.md](21_logical_data_design/21_13_entity_execution.md)
- [21_14_entity_result_artifact_lineage.md](21_logical_data_design/21_14_entity_result_artifact_lineage.md)
- [21_15_entity_membership_workspace.md](21_logical_data_design/21_15_entity_membership_workspace.md)
- [21_20_value_domain_identifiers.md](21_logical_data_design/21_20_value_domain_identifiers.md)
- [21_21_value_navigation_context.md](21_logical_data_design/21_21_value_navigation_context.md)
- [21_22_value_analysis_specifications.md](21_logical_data_design/21_22_value_analysis_specifications.md)
- [21_23_value_execution_snapshot.md](21_logical_data_design/21_23_value_execution_snapshot.md)
- [21_24_value_comparison_lineage.md](21_logical_data_design/21_24_value_comparison_lineage.md)
- [21_25_value_canonicalization.md](21_logical_data_design/21_25_value_canonicalization.md)
- [21_30_state_models.md](21_logical_data_design/21_30_state_models.md)
- [21_40_integrity_constraints.md](21_logical_data_design/21_40_integrity_constraints.md)
- [21_41_scientific_data_constraints.md](21_logical_data_design/21_41_scientific_data_constraints.md)
- [21_99_change_log.md](21_logical_data_design/21_99_change_log.md)

### 22_product_basic_design

- [22_00_overall_BD.md](22_product_basic_design/22_00_overall_BD.md)
- [22_01_information_architecture.md](22_product_basic_design/22_01_information_architecture.md)
- [22_02_web_operation.md](22_product_basic_design/22_02_web_operation.md)
- [22_03_navigation_application.md](22_product_basic_design/22_03_navigation_application.md)
- [22_04_workflow_core.md](22_product_basic_design/22_04_workflow_core.md)
- [22_05_family_exploratory.md](22_product_basic_design/22_05_family_exploratory.md)
- [22_06_family_causal.md](22_product_basic_design/22_06_family_causal.md)
- [22_07_family_predictive.md](22_product_basic_design/22_07_family_predictive.md)
- [22_08_validation_architecture.md](22_product_basic_design/22_08_validation_architecture.md)
- [22_09_results_artifacts_lineage.md](22_product_basic_design/22_09_results_artifacts_lineage.md)
- [22_10_comparison.md](22_product_basic_design/22_10_comparison.md)
- [22_11_frontend_state.md](22_product_basic_design/22_11_frontend_state.md)
- [22_12_security.md](22_product_basic_design/22_12_security.md)
- [22_13_deployment.md](22_product_basic_design/22_13_deployment.md)
- [22_14_failure_model.md](22_product_basic_design/22_14_failure_model.md)
- [22_15_schema_dependency.md](22_product_basic_design/22_15_schema_dependency.md)
- [22_16_test_architecture.md](22_product_basic_design/22_16_test_architecture.md)
- [22_17_stage_contents_e8_effective.md](22_product_basic_design/22_17_stage_contents_e8_effective.md)
- [22_99_change_log.md](22_product_basic_design/22_99_change_log.md)

### 23_api_interface_design

- [23_00_overall_IF.md](23_api_interface_design/23_00_overall_IF.md)
- [23_01_common_conventions.md](23_api_interface_design/23_01_common_conventions.md)
- [23_10_api_project_context.md](23_api_interface_design/23_10_api_project_context.md)
- [23_11_api_dataset_view.md](23_api_interface_design/23_11_api_dataset_view.md)
- [23_12_api_analysis_specification.md](23_api_interface_design/23_12_api_analysis_specification.md)
- [23_13_api_exploratory.md](23_api_interface_design/23_13_api_exploratory.md)
- [23_14_api_causal.md](23_api_interface_design/23_14_api_causal.md)
- [23_15_api_predictive.md](23_api_interface_design/23_15_api_predictive.md)
- [23_16_api_execution.md](23_api_interface_design/23_16_api_execution.md)
- [23_17_api_result_comparison_lineage.md](23_api_interface_design/23_17_api_result_comparison_lineage.md)
- [23_18_api_annotation_artifact.md](23_api_interface_design/23_18_api_annotation_artifact.md)
- [23_19_api_frontend_support.md](23_api_interface_design/23_19_api_frontend_support.md)
- [23_20_browser_navigation.md](23_api_interface_design/23_20_browser_navigation.md)
- [23_30_worker_runtime.md](23_api_interface_design/23_30_worker_runtime.md)
- [23_40_cli_library.md](23_api_interface_design/23_40_cli_library.md)
- [23_50_error_contract.md](23_api_interface_design/23_50_error_contract.md)
- [23_51_idempotency_contract.md](23_api_interface_design/23_51_idempotency_contract.md)
- [23_52_versioning_compatibility.md](23_api_interface_design/23_52_versioning_compatibility.md)
- [23_90_interface_verification.md](23_api_interface_design/23_90_interface_verification.md)
- [23_99_change_log.md](23_api_interface_design/23_99_change_log.md)

### 30_detailed_design

- [30_00_overall_DD.md](30_detailed_design/30_00_overall_DD.md)
- [30_01_class_design_template.md](30_detailed_design/30_01_class_design_template.md)
- [30_10_domain_resources.md](30_detailed_design/30_10_domain_resources.md)
- [30_11_schema_canonicalization.md](30_detailed_design/30_11_schema_canonicalization.md)
- [30_12_context_analysis_view.md](30_detailed_design/30_12_context_analysis_view.md)
- [30_20_planning_validation.md](30_detailed_design/30_20_planning_validation.md)
- [30_21_execution_runtime.md](30_detailed_design/30_21_execution_runtime.md)
- [30_30_exploratory.md](30_detailed_design/30_30_exploratory.md)
- [30_31_causal_setup_discovery.md](30_detailed_design/30_31_causal_setup_discovery.md)
- [30_32_causal_identification.md](30_detailed_design/30_32_causal_identification.md)
- [30_33_causal_estimation_effects.md](30_detailed_design/30_33_causal_estimation_effects.md)
- [30_34_causal_diagnostics_sensitivity.md](30_detailed_design/30_34_causal_diagnostics_sensitivity.md)
- [30_35_predictive_training.md](30_detailed_design/30_35_predictive_training.md)
- [30_36_predictive_explanation.md](30_detailed_design/30_36_predictive_explanation.md)
- [30_37_predictive_model_management.md](30_detailed_design/30_37_predictive_model_management.md)
- [30_40_project_workspace.md](30_detailed_design/30_40_project_workspace.md)
- [30_41_navigation_routing.md](30_detailed_design/30_41_navigation_routing.md)
- [30_42_results_lineage.md](30_detailed_design/30_42_results_lineage.md)
- [30_43_operation_availability.md](30_detailed_design/30_43_operation_availability.md)
- [30_50_persistence_artifacts.md](30_detailed_design/30_50_persistence_artifacts.md)
- [30_51_security.md](30_detailed_design/30_51_security.md)
- [30_52_failure_handling.md](30_detailed_design/30_52_failure_handling.md)
- [30_60_cli_adapters.md](30_detailed_design/30_60_cli_adapters.md)
- [30_90_verification_traceability.md](30_detailed_design/30_90_verification_traceability.md)
- [30_99_change_log.md](30_detailed_design/30_99_change_log.md)

## 2. RD-03 formal requirement publication

- [正式要件全68 Scope・41 Method・10 UC Trace](96_rd03_formal_requirement_traceability.md)
- [41 Method scope catalog](10_requirements_definition/10_32_scientific_method_scope.md)
- [10_00 — Requirement semantics and issuance state](10_requirements_definition/10_00_overall_RD.md)
- [10_90 — E10 exclusion and E11 exceptions](10_requirements_definition/10_90_scope_exclusions.md)
- [10_91 — E11 acceptance obligation](10_requirements_definition/10_91_acceptance_conditions.md)

**発行結果:** 新規FR19（FR-185〜203）、NFR8（NFR-029〜036）、科学的AR17（AR-028〜044）を`MUST / ACTIVE / UNVERIFIED / ENH-E11`で登録。既存FR195／NFR36／AR27のStatusと正文は不変。Architecture候補E11-A-01〜07はScientific ARに混ぜず、22 BD／ADRへ移管。

## 3. Draft / Review material (not approved physical design)

- [RD publication prior draft](10_requirements_definition/_drafts/enh_e11_formal_requirement_publication_draft.md)
- [LDD E11 local model draft](21_logical_data_design/_drafts/enh_e11_local_logical_model_draft.md)
- [BD E11 local architecture draft](22_product_basic_design/_drafts/enh_e11_causal_cli_basic_design_draft.md)
- [IF E11 local CLI/Port draft](23_api_interface_design/_drafts/enh_e11_cli_and_port_interface_draft.md)
- [DD proposed classes](30_detailed_design/_drafts/enh_e11_proposed_physical_class_design.md)
- [DD physical design gap register](30_detailed_design/_review/physical_design_gap_register.md)

## 4. Audit reports

- [RD-02 current file numbering, preservation, and 57 legacy file migration](92_rd02_restructure_verification.md)
- [RD-01 full 292-item Disposition review](rd01_review/91_rd01_requirement_granularity_review.md)
- [RD-01 existing FR 195 register](rd01_review/92_rd01_fr_disposition_register.md)
- [RD-01 NFR36 + AR27 register](rd01_review/93_rd01_nfr_ar_disposition_register.md)
- [RD-01 E11 provisional candidate register](rd01_review/94_rd01_e11_draft_disposition_register.md)
- [Prior structural split audit (historical)](90_structural_split_verification.md)

## 5. Authority and remaining work

- [DEC-SR04-09 Scope, Requirements, Architecture and Gate integrated Owner decisions](../../working_notes/20261116_sr04_dec09_scope_requirements_architecture_gate_integrated_owner_approval.md)
- `RD-01`分類Dispositionは独立承認前の編集候補であり、旧FR/NFR/ARの全面的な抽象化・移管本文反映は未完。RD-03の新E11条文発行とは別。
- 確定していない事項：Ownerによる新条文のSHA確認と元canonicalへの昇格、Method別実効Backend・CIの検証、ADR/Schema freeze、Gate06/07、Science T2/T3、顧客別Legal Gate、全Class物理詳細設計。
- `PLAN:G01〜G10`は実装Workstreamの名称。正式受入GateのPASSを意味しない。

## 6. ENH-E11文書の格納・昇格方針（Owner決定 2026-11-16）

- **作業先:** この`Revised_requirements_definition_documents/`配下で全5文書群の編集・レビュー・検証を継続する。
- **昇格条件:** ENH-E11の対象テスト**全件PASSを確認した後**に限り、元の`docs/wiki/requirement_definition/`へ昇格する。未実施・FAIL・BLOCKEDのテストがある場合は昇格しない。
- **現状:** 元正本は未変更。`RD-03`新条文は本作業ディレクトリ内で発行済みだが、元正本への昇格ではない。
- **決定の詳細と判定規則:** [ENH-E11 Canonical昇格方針](93_enh_e11_canonical_promotion_policy.md)。
