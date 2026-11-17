# ENH-E11 — Revised Requirements & Design Documents

**Status (Owner 2026-11-16):** `DOC01_OWNER_APPROVED / IF01_DESIGN_ADOPTED / DD01_DESIGN_ADOPTED / INDEPENDENT_ARCH_AND_SCHEMA_FREEZE_PENDING / CODING_NOT_AUTHORIZED`.

**Source authority:** 原正本 `docs/wiki/requirement_definition/` を変更せず、元の5文書を `_source_snapshots/` に固定blobのまま保管。Owner DEC09は実装Scopeと要件意味・Architecture方針を承認。今回のE11新FR/NFR/Scientific ARは**改訂版working-copyで条文・Status・Traceを発行**したものであり、元正本へのpromote、Coding、Science/Gate/Legalの承認ではない。

## 1. Current document index（番号付き105ファイル：Stock候補（適合審査中））

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
- [22_17_stage_contents.md](22_product_basic_design/22_17_stage_contents.md)

### 23_api_interface_design

**章立ての読順:** 旧全文書の§1〜9を踏襲する箇所は、ファイル名順と一致しない。§4 Browser Navigationを§5 Web APIより先に置く。23_41/42の§1〜9は新Local Interfaceの**ファイル内採番**であり旧全体章番号と別。

- [23_00_overall_IF.md](23_api_interface_design/23_00_overall_IF.md)
- [23_01_common_conventions.md](23_api_interface_design/23_01_common_conventions.md)
- [23_20_browser_navigation.md](23_api_interface_design/23_20_browser_navigation.md)
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
- [23_30_worker_runtime.md](23_api_interface_design/23_30_worker_runtime.md)
- [23_40_cli_library.md](23_api_interface_design/23_40_cli_library.md)
- [23_41_cli_scientific_ports.md](23_api_interface_design/23_41_cli_scientific_ports.md)
- [23_42_local_result_manifest_artifact.md](23_api_interface_design/23_42_local_result_manifest_artifact.md)
- [23_50_error_contract.md](23_api_interface_design/23_50_error_contract.md)
- [23_51_idempotency_contract.md](23_api_interface_design/23_51_idempotency_contract.md)
- [23_52_versioning_compatibility.md](23_api_interface_design/23_52_versioning_compatibility.md)
- [23_90_interface_verification.md](23_api_interface_design/23_90_interface_verification.md)

### 30_detailed_design

**章立ての読順:** 旧詳細設計§3→§4/5（30_41）→§6を先に読む。30_41は§18 Routingも収録しており、先行のProduct Class節は§9.5/9.6（PlanValidator/Registry）、§10.5/10.6（ExecutionOutcome/GenericExecutor）、§3.7（GraphVersion）へ配置してグローバル§4/5衝突を縮小済み。30_41自体には§4/5と§18が同居するため、全番号・Anchorの完了判定はまだ行わない。

- [30_00_overall_DD.md](30_detailed_design/30_00_overall_DD.md)
- [30_01_class_design_template.md](30_detailed_design/30_01_class_design_template.md)
- [30_10_domain_resources.md](30_detailed_design/30_10_domain_resources.md)
- [30_41_navigation_routing.md](30_detailed_design/30_41_navigation_routing.md)
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
- [30_42_results_lineage.md](30_detailed_design/30_42_results_lineage.md)
- [30_43_operation_availability.md](30_detailed_design/30_43_operation_availability.md)
- [30_50_persistence_artifacts.md](30_detailed_design/30_50_persistence_artifacts.md)
- [30_51_security.md](30_detailed_design/30_51_security.md)
- [30_52_failure_handling.md](30_detailed_design/30_52_failure_handling.md)
- [30_60_cli_adapters.md](30_detailed_design/30_60_cli_adapters.md)
- [30_61_e11_local_domain_ports.md](30_detailed_design/30_61_e11_local_domain_ports.md)
- [30_62_local_execution_publication.md](30_detailed_design/30_62_local_execution_publication.md)
- [30_63_causal_method_adapters.md](30_detailed_design/30_63_causal_method_adapters.md)
- [30_90_verification_traceability.md](30_detailed_design/30_90_verification_traceability.md)

**構造監査上の注記:** 上記105件は移管後の5群番号付きファイル数であり、Stock適合PASS件数ではない。`10_99`、`21_99`、`22_99`、`23_99`、`30_99`のChange LogはFlowに分類される。Rootの`90〜98`監査記録もFlow。Root8件とChange Log5件は[移管台帳](doc01_review/93_20261117_flow_migration_manifest.md)に基づきFlowへ物理移管済み。Markdownファイルリンクは対象範囲で検査済みだが、全Anchor／非Markdown／Repo外のリンク監査は未完。[DOC-01横断監査](doc01_review/92_numbering_stockflow_and_class_template_audit.md)で残件を追跡する。

## 2. RD-03 formal requirement publication

- [正式要件全68 Scope・41 Method・10 UC Trace](doc01_review/rd03_review/96_rd03_formal_requirement_traceability.md)
- [41 Method scope catalog](10_requirements_definition/10_32_scientific_method_scope.md)
- [10_00 — Requirement semantics and issuance state](10_requirements_definition/10_00_overall_RD.md)
- [10_90 — E10 exclusion and E11 exceptions](10_requirements_definition/10_90_scope_exclusions.md)
- [10_91 — E11 acceptance obligation](10_requirements_definition/10_91_acceptance_conditions.md)

**発行結果:** 新規FR19（FR-185〜203）、NFR8（NFR-029〜036）、科学的AR17（AR-028〜044）を`MUST / ACTIVE / UNVERIFIED / ENH-E11`で登録。既存FR195／NFR36／AR27のStatusと正文は不変。Architecture候補E11-A-01〜07はScientific ARに混ぜず、22 BD／ADRへ移管。

## 3. Draft / Review material (not approved physical design)

- [BD-01 エンハンス固有のArchive/Reviews/Trace](bd01_review/README.md) — 正本候補22系と切り離して保管。
- [RD publication prior draft](doc01_review/prior_drafts/10_requirements_definition/enh_e11_formal_requirement_publication_draft.md)
- [LDD E11 local model draft](doc01_review/prior_drafts/21_logical_data_design/enh_e11_local_logical_model_draft.md)
- [BD E11 local architecture draft](doc01_review/prior_drafts/22_product_basic_design/enh_e11_causal_cli_basic_design_draft.md)
- [IF E11 local CLI/Port draft](doc01_review/prior_drafts/23_api_interface_design/enh_e11_cli_and_port_interface_draft.md)
- [DD proposed classes](doc01_review/prior_drafts/30_detailed_design/enh_e11_proposed_physical_class_design.md)
- [DD physical design gap register](doc01_review/reviews/physical_design_gap_register.md)

## 4. Audit reports

- [BD-01 Architecture consistency self-review and open findings](bd01_review/90_architecture_consistency_review.md) — 13 findings, 2 resolved in BD, 11 open; independent review pending.
- [BD-01 formal 44-requirement and ARC09 7-decision mapping](bd01_review/91_requirement_architecture_trace.md) — mapping coverage checked; science/implementation not verified.
- [RD-04 requirement consistency / design migration verification](doc01_review/rd04_review/98_rd04_consistency_verification.md) — current; structure and trace audit PASS, owner content review pending.
- [RD-04 FR195 clause review](doc01_review/rd04_review/95_rd04_fr_application_review.md)
- [RD-04 NFR36+Scientific AR27 review](doc01_review/rd04_review/96_rd04_nfr_ar_application_review.md)
- [RD-04 formal E11 44-clause semantic review](doc01_review/rd04_review/97_rd04_e11_requirement_review.md)
- [RD-02 current file numbering, preservation, and 57 legacy file migration](doc01_review/rd02_migration/92_rd02_restructure_verification.md)
- [RD-01 full 292-item Disposition review](rd01_review/91_rd01_requirement_granularity_review.md)
- [RD-01 existing FR 195 register](rd01_review/92_rd01_fr_disposition_register.md)
- [RD-01 NFR36 + AR27 register](rd01_review/93_rd01_nfr_ar_disposition_register.md)
- [RD-01 E11 provisional candidate register](rd01_review/94_rd01_e11_draft_disposition_register.md)
- [Prior structural split audit (historical)](doc01_review/structural_migration/90_structural_split_verification.md)

## 5. Authority and remaining work

- [DEC-SR04-09 Scope, Requirements, Architecture and Gate integrated Owner decisions](../../working_notes/20261116_sr04_dec09_scope_requirements_architecture_gate_integrated_owner_approval.md)
- `RD-01`のDispositionは`RD-04`で逐条再審査し、既存258件のうち122件を改訂・設計へ移管済み。136件は維持。個別条文の最終Ownerレビューは未完。
- 確定していない事項：Ownerによる新条文のSHA確認と元canonicalへの昇格、Method別実効Backend・CIの検証、ADR/Schema freeze、各Gateの06/07契約、Science T2/T3、顧客別Legal Gate、全Class物理詳細設計。
- `BD-01`でE11 Local Causal CLIの基本設計とDEC09 Authorityを具体化。自己レビューで原則整合と未確定事項を記録したが、独立Architectureレビュー・Schema/Port Freeze・Gate06/07は未完。
- `PLAN:G01〜G10`は実装Workstreamの名称。正式受入GateのPASSを意味しない。

## 6. ENH-E11文書の格納・昇格方針（Owner決定 2026-11-16）

- **作業先:** この`Revised_requirements_definition_documents/`配下で全5文書群の編集・レビュー・検証を継続する。
- **昇格条件:** ENH-E11の対象テスト**全件PASSを確認した後**に限り、元の`docs/wiki/requirement_definition/`へ昇格する。未実施・FAIL・BLOCKEDのテストがある場合は昇格しない。
- **現状:** 元正本は未変更。`RD-03`新条文は本作業ディレクトリ内で発行済みだが、元正本への昇格ではない。
- **決定の詳細と判定規則:** [ENH-E11 Canonical昇格方針](combined_review/decisions/93_enh_e11_canonical_promotion_policy.md)。

## 7. BD-01 — 正本候補の常設設計とエンハンス固有レビューの分離（2026-11-16）

- ENH-E11と既存Productを**別の実行/永続authority**として扱い、[22_00のシステム構成](22_product_basic_design/22_00_overall_BD.md)、[Local execution boundary](22_product_basic_design/22_00_overall_BD.md)、[Scientific methods](22_product_basic_design/22_06_family_causal.md)、[Result/Artifact](22_product_basic_design/22_09_results_artifacts_lineage.md)、[Security](22_product_basic_design/22_12_security.md)・[Environment](22_product_basic_design/22_13_deployment.md)を改訂した。
- Owner承認済みDEC09 ARC09-01〜07は責務別BDに配置済み。新規FR/NFR/科学的AR44件とE11-A7件を[22_91 Trace](bd01_review/91_requirement_architecture_trace.md)へ対応付けた。
- [22_90内部Architecture整合レビュー](bd01_review/90_architecture_consistency_review.md)：Finding13件、基本設計上で修正2件、残る11件は未閉鎖。現行CLIのPort/Manifestと新E11のVersion・typed Result・Atomic Publish・Local Privacy等の実装差分はIF-01/DD-01・該当Gateの06実装契約に引き継ぐ。
- [BD-01整理方針・歴史的設計断片](bd01_review/README.md)に、旧22_20〜23設計断片と22_90〜91レビューの移動先・原Blobを記録する。これら6件は常設22系には置かない。
- **本工程は独立Architecture Review PASS、Port/Schema Freeze、Science/Legal Gate、Coding許可を意味しない。** 元正本はENH-E11全件テストPASS後にのみ昇格する。

> **DOC-01文書分類:** 10／21／22／23／30系のRD-04移管記録は[doc01_review/](doc01_review/README.md)へ隔離し、設計制約は責務別仕様へ保持。各群のStock適合性とリンク検証はDOC-01監査台帳を参照。

## 8. DOC-01／IF-01／DD-01 統合レビュー入口

- [DOC-01 Stock/Flow監査台帳](doc01_review/README.md)／[監査結果詳細](doc01_review/90_doc01_stock_flow_verification.md)
- [IF-01 Interface内部レビュー](if01_review/90_interface_contract_review.md) — 新Local CLI/Port、Effect/Graph/Manifest・Atomic Publishingの候補契約
- [DD-01 Physical Design内部レビュー](dd01_review/90_physical_design_review.md) — Domain/Port/Runner/Artifactと41 Methodの詳細設計案
- [三工程まとめてのOwner Review Pack](combined_review/90_doc01_if01_dd01_owner_review_pack.md)
- [2026-11-17 文書構成・API粒度・詳細設計7区分の再監査（要是正）](combined_review/92_20261117_document_architecture_audit.md)

**文書状態（2026-11-16）：** DOC-01をOwner承認、IF-01/DD-01設計案をOwner採用済み。独立Architecture/Science、Schema/Port Freeze、各Gateの06/07契約、Coding Authorization、canonical昇格は未完了。[統合Owner決定](combined_review/91_20261116_doc01_if01_dd01_owner_approval_record.md)。


## 9. 2026-11-17 横断再監査の追加Finding

DOC-01 Owner承認／IF-01・DD-01設計案採用の後、[横断監査](combined_review/92_20261117_document_architecture_audit.md)でRoot 90〜98番台8件のFlow混在、23/30章番号の非単調・重複、23系API契約粒度、30系のOwner採用7区分Classテンプレート不適合を確認した。**文書構造・Class仕様の修正が必要**。設計方針の承認を無断撤回するものではないが、文書品質・Source一致・Schema FreezeのPASSを意味しない。Stock文書自体は本監査で未改訂。

## 10. PREP-01/02開始時のSource照合と用語規則（2026-11-17）

- [PREP-01/02 実行記録](../../working_notes/20261117_prep01_prep02_execution_evidence.md) はFlowであり、Stock契約の代替ではない。
- ENH-E11の対象は、承認済み68 Scope・41 Method・10 UCと改訂要件・設計全体である。初回Coding時点で全Methodの科学実測PASSを要求しないことと、全対象の品質是正義務を捨てることは別。
- Enhancement WorkflowでGateはsemantic Acceptance Contractの一義のみを持つ。G01〜G10は暫定計画Stageであり、正式なGateは受入境界と06/07 Contractで定義する。06は各GateのCoding Contract、07は各GateのIndependent Verification Contract、999は各GateのDecision。DEC09の「Gate06/07」を全体の工程として使う旧称は現在の標準語彙とは不整合で、独立のGate階層として再利用しない。Ownerが採用したScience・Environment・法務の受入条件は保持する。
- 工程ごとのStatusは[Notion control plane](https://app.notion.com/p/41ae5855be39805388acef85a77b2279)に集約し、Source・Reviewの証拠はGitHubに保存する。

## 11. PREP-01/02の部分是正（2026-11-17、未完）

- Product Web APIのProject/ResearchContextは、Router→Serviceの静的追跡でFR-121 Membership AuthorizationとFR-114 IdempotencyにSource契約Gapが存在する。23_10と22_12/23_51にCURRENT/REQUIREDとNegative Testを明記。Product gapのE11 CLI自動閉鎖は不可。
- 23_10〜23_19の10 Stockファイルに13 Router由来101件のOperation宣言を対応付け、共通9欄の必須Fieldを23_01で定義した。Service/Error/Authorization/Testの全セルはまだ未完。
- 30_62のE11 Local UseCase/MethodRegistry/Publisher/Manifest/Reader/Privacyについて、Owner指定7区分のPhysical Design記述へ部分修正。30_20のExisting PlanValidator/StageRunnerRegistry、30_21のExisting ExecutionOutcome/GenericExecutor、30_10のProduct GraphVersionをSourceと照合した7区分へ更新。**30系全Classの7区分完了ではない。**
- 23_42と22_15にはAtomic Manifest Publish、no-clobber、version/Schema/Port/PrivacyのFreeze確認事項を追加。実FS/Backend/Science/Independent Architecture Reviewは未実施。
- 既存WorkflowのGate用語を一意化するため、Stockの旧「Gate06/07」の全体段階としての表現を局所修正した。過去のOwner採択のScientfic/Architecture要件は維持。
- Root Flow8件・5 Change LogのFlow移管は完了。残る23/30の全番号・Anchor、全API/Class、改訂122条文とMethod41全セル、Backend5環境の実効証拠は未完。[本ページの進捗authorityはNotion](https://app.notion.com/p/41ae5855be39805388acef85a77b2279)。

## 12. 別保管する歴史記録・変更ログ（Flow）

Rootの監査・Owner判断8件と変更ログ5件は、2026-11-17の移管で以下のFlow領域へ配置し、旧Pathを削除した（Git `cd4e738`）。参照の静的検査は[移管台帳](doc01_review/93_20261117_flow_migration_manifest.md)に記録する。元canonicalへの昇格はENH-E11の全対象テストPASS後のみ。

- [90_structural_split_verification.md](doc01_review/structural_migration/90_structural_split_verification.md)
- [92_rd02_restructure_verification.md](doc01_review/rd02_migration/92_rd02_restructure_verification.md)
- [93_enh_e11_canonical_promotion_policy.md](combined_review/decisions/93_enh_e11_canonical_promotion_policy.md)
- [95_rd04_fr_application_review.md](doc01_review/rd04_review/95_rd04_fr_application_review.md)
- [96_rd03_formal_requirement_traceability.md](doc01_review/rd03_review/96_rd03_formal_requirement_traceability.md)
- [96_rd04_nfr_ar_application_review.md](doc01_review/rd04_review/96_rd04_nfr_ar_application_review.md)
- [97_rd04_e11_requirement_review.md](doc01_review/rd04_review/97_rd04_e11_requirement_review.md)
- [98_rd04_consistency_verification.md](doc01_review/rd04_review/98_rd04_consistency_verification.md)
- [10_99_change_log.md](doc01_review/history/10_99_change_log.md)
- [21_99_change_log.md](doc01_review/history/21_99_change_log.md)
- [22_99_change_log.md](doc01_review/history/22_99_change_log.md)
- [23_99_change_log.md](doc01_review/history/23_99_change_log.md)
- [30_99_change_log.md](doc01_review/history/30_99_change_log.md)
