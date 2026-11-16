# 10_10_fr_project_context_data

**Status:** `RD03_FORMAL_E11_ISSUED / OWNER_SHA_REVIEW_PENDING`; original ID, level and state retained.  
**Source blob:** `40b83f29c67b4a39f6db5393be7534c5e892d656`.

---

## FR original requirement rows

| ID | Area | Requirement | Level | Requirement Status | Implementation Status | Delivery |
| --- | --- | --- | --- | --- | --- | --- |
| FR-001 | Project / Context | ProjectをResearch Topicの権限・来歴境界として作成、更新、archiveできる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-002 | Project / Context | Projectはtopic、objective、memoを保持し、decision contextはversioned `ResearchContextVersion`の責務として保持する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-003 | Project / Context | Research Contextをversioned resourceとして作成し、過去Versionを上書きしない | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-004 | Project / Context | Research Contextに複数のResearch QuestionとHypothesisを保持できる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-005 | Project / Context | Context間にREFINES、DERIVED_FROM、SUPERSEDES、RELATED_TO relationを設定できる | SHOULD | ACTIVE | IMPLEMENTED | BASELINE |
| FR-006 | Project / Context | Analysis Specificationは一つのResearch Context Versionを参照する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-007 | Project / Context | Executionは参照ResearchContextVersionを固定し、受付時のobjective/rationale等の再現に必要なsnapshot metadata/hashを保持する。ResearchContext全体の重複保存を必須化しない | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-008 | Project / Context | ResearchContextVersionから利用AnalysisSpecification、Execution、Resultへcanonical lineage/read modelで遡及・追跡できる | MUST | ACTIVE | PARTIAL | ENH-E5 |
| FR-009 | Project / Context | ARCHIVED Projectでは新規Executionを受け付けず、既存Resultを保持する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-010 | Data / View | CSVまたはParquetをDataset Versionとして不変登録する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-011 | Data / View | DatasetVersionにcontent hash、schema、row count、column countおよびcurrent profile summaryを保持する。登録時の独立full profile生成を必須化しない | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-012 | Data / View | Dataset previewとcolumn metadataを権限内で取得できる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-013 | Data / View | 同一Dataset系列に複数Versionを登録し、Executionが参照Versionを固定する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-014 | Data / View | Analysis Viewにrow filter、column selection、derived column、missing policy、time cutoffを定義する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-015 | Data / View | AnalysisViewのsource Dataset logical type × operator × value compatibilityをdomain/application validationで検証し、type mismatchを`FILTER_TYPE_MISMATCH`として返す | MUST | ACTIVE | IMPLEMENTED | ENH-E5 |
| FR-016 | Data / View | 固定済みAnalysis Viewを上書きせず、変更時は新Versionを作成する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-017 | Data / View | Analysis Viewからsource Dataset Versionと生成条件へ遡れる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-018 | Data / View | 同じAnalysis Viewを複数Analysis Familyから参照できる | SHOULD | ACTIVE | IMPLEMENTED | BASELINE |
| FR-019 | Data / View | Dataset columnにグローバルなTreatment、Outcome、Target等の役割を固定しない | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-020 | Data / View | Explore stateのdata-selection semantics（row_filter、selected_columns、derived_columns、missing_value_policy、time_cutoff、sampling）からAnalysisView DRAFTを作成できる。presentation-only chart stateはAnalysisViewへ保存しない | SHOULD | ACTIVE | NOT_IMPLEMENTED | ENH-E5 |
| FR-021 | Data / View | 機微列、利用制限および説明をcolumn metadataへ付与し、configurable sensitive-column policyに利用できる | SHOULD | DEFERRED | NOT_IMPLEMENTED | FUTURE |
| FR-022 | Data / View | Analysis View生成時に不正列、空母集団、非決定的式を拒否する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-166 | Project Management | selected Projectのlocal navigationはOverview / Research Context / Data / Resultsを提供する | MUST | ACTIVE | IMPLEMENTED | ENH-E7 |
| FR-167 | Project Management | OverviewはProject metadata / identity / status / archiveを所有し、Project Archiveをselected Project lifecycle operationとして提供する | MUST | ACTIVE | IMPLEMENTED | ENH-E7 |
| FR-168 | Project Management | DataはDataset / Dataset Version / Schema / Preview / Analysis View lifecycleを所有し、Analysis ViewをFamily横断analysis inputとして管理する | MUST | ACTIVE | IMPLEMENTED | ENH-E7 |
| FR-185 | Local Scientific Identity | ローカル因果分析の問い・デザイン・グラフ・データと参照版を識別し、上流条件が異なる結果の暗黙の再利用を拒否できる | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
