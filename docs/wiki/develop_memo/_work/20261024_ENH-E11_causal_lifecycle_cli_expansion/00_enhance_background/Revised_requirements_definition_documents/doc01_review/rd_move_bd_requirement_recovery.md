# DOC-01 — RD-04 MOVE_BDからの要件本文正本適合性回復

**Kind:** FLOW/CHANGE-REASON. **Source HEAD:** `af93ef0e9b25576f03fec928ad2045b622f872a1`. `MOVE_BD`19件に含まれていた`【設計制約移管・Legacy Trace】`は要件の受入条文ではなく作業メモだった。

## Decision and preservation

- **今回の処置:** 各IDのRequirement Status/Implementation Status/Delivery/Levelを変更せず、**もとの要件原文**を再掲する。強い抽象化や暗黙の廃止はOwnerの別途承認が必要である。
- 21/22/23/30系へ移管済みの同条文の具体的設計拘束は残す。新たな要件義務・Method範囲は追加しない。
- 正本候補のストック型RDから工程名・Legacy Traceのplaceholderを排除する。この処置はRD-04抽象度判定の最終Owner承認を意味しない。

## 19 record crosswalk

| ID | RD file | Restored normative text | Status | Replaced workflow placeholder |
|---|---|---|---|---|
| FR-045 | 10_requirements_definition/10_13_fr_causal.md | Treatment / Outcome inferred typeを正規化文字列で保存し、外部型objectを永続化しない | ACTIVE | 【設計制約移管・Legacy Trace】FR-044の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する |
| FR-075 | 10_requirements_definition/10_14_fr_workflow_execution.md | Family別PlannerをRegistryから解決する | ACTIVE | 【設計制約移管・Legacy Trace】NFR-005の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する |
| FR-077 | 10_requirements_definition/10_14_fr_workflow_execution.md | Stage Typeをnamespace、name、versionで識別する | ACTIVE | 【設計制約移管・Legacy Trace】FR-076の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する |
| FR-079 | 10_requirements_definition/10_14_fr_workflow_execution.md | Stage RunnerをRegistryから解決し、Executorへif/elif分岐を集約しない | ACTIVE | 【設計制約移管・Legacy Trace】NFR-005の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する |
| FR-080 | 10_requirements_definition/10_14_fr_workflow_execution.md | canonical lifecycle/application serviceがExecutionのclaim、state、cancel、retry、Result/Artifact metadata commitを所有し、Generic Executorはowned workflow context内で依存順、Stage sequencing、runner invocationを実行する | ACTIVE | 【設計制約移管・Legacy Trace】FR-081の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する |
| FR-089 | 10_requirements_definition/10_14_fr_workflow_execution.md | Generic validationとFamily-specific validationを分離して実行する | ACTIVE | 【設計制約移管・Legacy Trace】FR-085の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する |
| FR-143 | 10_requirements_definition/10_14_fr_workflow_execution.md | runtime layerはNavigation Stage ID、browser route、tab/sidebar stateへ依存しない | ACTIVE | 【設計制約移管・Legacy Trace】NFR-025の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する |
| FR-133 | 10_requirements_definition/10_16_fr_navigation_ui.md | FamilyごとにCapability-owned immutable descriptorでStage ID、slug、label、order、default Stageを独立定義する | ACTIVE | 【設計制約移管・Legacy Trace】FR-131の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する |
| FR-140 | 10_requirements_definition/10_16_fr_navigation_ui.md | Navigation Stageをruntime `StageType` / `StageDefinition` / `StageExecution`として再利用・継承しない | ACTIVE | 【設計制約移管・Legacy Trace】NFR-021の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する |
| FR-141 | 10_requirements_definition/10_16_fr_navigation_ui.md | Navigation StageとExecution Stageの1:1 mappingを要求するcontractを導入しない | ACTIVE | 【設計制約移管・Legacy Trace】NFR-021の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する |
| FR-144 | 10_requirements_definition/10_16_fr_navigation_ui.md | concrete Navigation Stage catalogは各Family-specific Capabilityが所有し、application/interface aggregatorがread-only metadataとして集約する | ACTIVE | 【設計制約移管・Legacy Trace】FR-131の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する |
| FR-145 | 10_requirements_definition/10_16_fr_navigation_ui.md | generic application layerはFamily-specific Stage semanticsを集中所有しない | ACTIVE | 【設計制約移管・Legacy Trace】NFR-023の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する |
| FR-157 | 10_requirements_definition/10_16_fr_navigation_ui.md | 既存`AnalysisSpecification.analysis_family`をFamily discriminatorとして再利用し、duplicate Family field/enumを追加しない | ACTIVE | 【設計制約移管・Legacy Trace】FR-074の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する |
| FR-158 | 10_requirements_definition/10_16_fr_navigation_ui.md | AnalysisSpecification / ExecutionPlan / Execution / StageExecutionへNavigation Stage fieldを追加しない | ACTIVE | 【設計制約移管・Legacy Trace】NFR-021の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する |
| FR-160 | 10_requirements_definition/10_16_fr_navigation_ui.md | Family / Navigation / application IAの変更だけを理由にDB schema migrationまたはnavigation-state persistenceを導入しない | ACTIVE | 【設計制約移管・Legacy Trace】NFR-021／FR-177の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する |
| FR-128a | 10_requirements_definition/10_18_fr_security_operations.md | Algorithm/Runnerをregistry/capabilityから解決・管理するcurrent contractを維持する | ACTIVE | 【設計制約移管・Legacy Trace】FR-035／NFR-005の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する |
| NFR-018 | 10_requirements_definition/10_22_nfr_security_compatibility.md | Product DomainからWeb Framework、ORMおよびlegacy packageへ依存しない | ACTIVE | 【設計制約移管・Legacy Trace】NFR-005に係る既存設計制約。具体的な実装契約は下位設計へ移し、元ID・Status・科学的制約の追跡を維持する |
| AR-022 | 10_requirements_definition/10_30_ar_scientific_integrity.md | Family間でStage数・名称を揃えることを科学的workflow要件としない | ACTIVE | 【設計制約移管・Legacy Trace】対応する既存上位要件に係る既存設計制約。具体的な実装契約は下位設計へ移し、元ID・Status・科学的制約の追跡を維持する |
| AR-009 | 10_requirements_definition/10_31_ar_estimand_inference.md | 外部libraryのdtype objectまたはmodel objectをJSON正本へ保存しない | ACTIVE | 【設計制約移管・Legacy Trace】対応する既存上位要件に係る既存設計制約。具体的な実装契約は下位設計へ移し、元ID・Status・科学的制約の追跡を維持する |
