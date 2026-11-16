# 10_16_fr_navigation_ui

**Status:** `RD02_STRUCTURAL_WORKING_COPY / E11_NOT_PUBLISHED`; original ID, level and state retained.  
**Source blob:** `40b83f29c67b4a39f6db5393be7534c5e892d656`.

---

## FR original requirement rows

| ID | Area | Requirement | Level | Requirement Status | Implementation Status | Delivery |
| --- | --- | --- | --- | --- | --- | --- |
| FR-104 | UI / Navigation | ApplicationはProject ManagementとAnalysis Workspaceを異なるnavigation scopeとして提供し、Project resource管理とFamily / Stage navigationを同一hierarchyへ混在させない | MUST | ACTIVE | IMPLEMENTED | ENH-E7 |
| FR-105 | UI / Navigation | Project Management routeとAnalysis routeはいずれも独立URL、direct link、reload、browser Back / Forwardでdeterministicに復元できる | MUST | ACTIVE | IMPLEMENTED | ENH-E7 |
| FR-106 | UI | Analysis WorkspaceはAnalysis ContextとしてCurrent Project、Active Research Context、Dataset Version、Analysis Viewを明示する | MUST | ACTIVE | IMPLEMENTED | ENH-E7 |
| FR-107 | UI | 操作可否をBackend authoritative state/authorizationから導出し、`allowed / reason_code / message`としてpresentationへ返す | MUST | ACTIVE | PARTIAL | ENH-E5 |
| FR-108 | UI | AnalysisSpecification、Execution、Result、GraphVersionへFamily/Navigation Stage contextを保持したdeep routeで直接遷移できる | MUST | ACTIVE | IMPLEMENTED | ENH-E5 |
| FR-109 | UI | 非同期presentation stateを`IDLE / LOADING / READY / EMPTY / PARTIAL / ERROR / CANCELLED`として区別する | MUST | ACTIVE | PARTIAL | ENH-E5 |
| FR-110a | UI | current result/list surfaceでfamily/type/status等の既存filterを提供する | SHOULD | ACTIVE | IMPLEMENTED | BASELINE |
| FR-110b | UI | 一覧・比較filterをdataset、context、date等へ拡張する | SHOULD | DEFERRED | NOT_IMPLEMENTED | FUTURE |
| FR-111 | UI | current surfaceでkeyboard、deterministic focus、accessible name、error association、non-color semanticsおよびcontrast要件を満たす | MUST | ACTIVE | PARTIAL | ENH-E5 |
| FR-112 | UI | Exploratory、Predictive、Causalの用語と警告を明示的に分離する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-129 | Navigation | Exploratory / Predictive / Causalをfirst-classなAnalysis Familyとして常時選択可能にする | MUST | ACTIVE | IMPLEMENTED | ENH-E5 |
| FR-130 | Navigation | Current Familyをactive stateとcanonical route `/projects/{project_id}/analysis/{family_slug}/{stage_slug}`の双方で一意に識別できる | MUST | ACTIVE | IMPLEMENTED | ENH-E5 |
| FR-131 | Navigation | Family-local navigationにはselected Familyが所有するNavigation Stageだけを表示する | MUST | ACTIVE | IMPLEMENTED | ENH-E5 |
| FR-132 | Navigation | Family切替時はCapability descriptorが宣言するdefault Navigation Stage（Exploratory=`profile`, Causal=`setup`, Predictive=`setup`）へ遷移する | MUST | ACTIVE | PARTIAL | ENH-E5 |
| FR-133 | Navigation | FamilyごとにCapability-owned immutable descriptorでStage ID、slug、label、order、default Stageを独立定義する | MUST | ACTIVE | PARTIAL | ENH-E5 |
| FR-134 | Navigation | Family間でStage数・名称を揃える目的のdummy/common Stageを導入しない | MUST NOT | ACTIVE | IMPLEMENTED | ENH-E5 |
| FR-135 | Navigation | Navigation Stageの表示順をwizard completion、runtime dependency、実行前提として強制しない | MUST NOT | ACTIVE | IMPLEMENTED | ENH-E5 |
| FR-136 | Navigation | canonical URL `/projects/{project_id}/analysis/{family_slug}/{stage_slug}`からProject、Family、Navigation Stageを復元できる | MUST | ACTIVE | IMPLEMENTED | ENH-E5 |
| FR-137 | Navigation | reload、browser back、browser forwardでFamily / Stage stateをdeterministicに復元できる | MUST | ACTIVE | IMPLEMENTED | ENH-E5 |
| FR-138 | Navigation | unknown Family / Stageをsilent fallbackで意味変換せず明示errorと有効な遷移先を提示する | MUST | ACTIVE | PARTIAL | ENH-E5 |
| FR-139 | Navigation | Overview / Research Context / Data / ResultsをProject Management local navigationとして扱い、Exploratory / Predictive / CausalのAnalytical Familyと同一taxonomyへ混在させない | MUST | ACTIVE | IMPLEMENTED | ENH-E7 |
| FR-140 | Navigation / Runtime | Navigation Stageをruntime `StageType` / `StageDefinition` / `StageExecution`として再利用・継承しない | MUST NOT | ACTIVE | IMPLEMENTED | ENH-E5 |
| FR-141 | Navigation / Runtime | Navigation StageとExecution Stageの1:1 mappingを要求するcontractを導入しない | MUST NOT | ACTIVE | IMPLEMENTED | ENH-E5 |
| FR-144 | Capability | concrete Navigation Stage catalogは各Family-specific Capabilityが所有し、application/interface aggregatorがread-only metadataとして集約する | MUST | ACTIVE | PARTIAL | ENH-E5 |
| FR-145 | Capability | generic application layerはFamily-specific Stage semanticsを集中所有しない | MUST NOT | ACTIVE | NOT_IMPLEMENTED | ENH-E5 |
| FR-157 | Domain / Compatibility | 既存`AnalysisSpecification.analysis_family`をFamily discriminatorとして再利用し、duplicate Family field/enumを追加しない | MUST | ACTIVE | IMPLEMENTED | ENH-E5 |
| FR-158 | Domain / Compatibility | AnalysisSpecification / ExecutionPlan / Execution / StageExecutionへNavigation Stage fieldを追加しない | MUST NOT | ACTIVE | IMPLEMENTED | ENH-E5 |
| FR-159 | Compatibility | supported legacy analytical entryはFamily Capability catalogで解決したcanonical Analysis routeへ一方向normalizeし、parallel navigation authorityとして維持しない | MUST | ACTIVE | IMPLEMENTED | ENH-E7 |
| FR-160 | Compatibility | Family / Navigation / application IAの変更だけを理由にDB schema migrationまたはnavigation-state persistenceを導入しない | MUST NOT | ACTIVE | IMPLEMENTED | ENH-E7 |
| FR-162 | Scope | Overview / FlagshipをAnalytical Family peerとして追加しない | MUST NOT | ACTIVE | IMPLEMENTED | ENH-E5 |
| FR-163 | Project Navigation | `/projects`をProject Listのcanonical surfaceとする | MUST | ACTIVE | IMPLEMENTED | ENH-E7 |
| FR-164 | Project Navigation | `/projects/new`をProject Registerのcanonical surfaceとし、作成成功後は`/projects/{new_project_id}/overview`へ遷移する | MUST | ACTIVE | IMPLEMENTED | ENH-E7 |
| FR-165 | Project Navigation | `/projects/{project_id}/overview`をselected Projectのdefault canonical surfaceとし、`/projects/{project_id}`はhistory-replaceでoverviewへnormalizeする | MUST | ACTIVE | IMPLEMENTED | ENH-E7 |
| FR-170 | Analysis Workspace | Analysis WorkspaceをProject Managementとは別surfaceとし、Family / Stage navigationはAnalysis Workspace内だけに表示する | MUST | ACTIVE | IMPLEMENTED | ENH-E7 |
| FR-171 | Analysis Context | Current Projectはcanonical Analysis URLの`project_id`をauthorityとしAnalysis Workspace内ではread-onlyとする。Project変更はProject Management経由で行う | MUST | ACTIVE | IMPLEMENTED | ENH-E7 |
| FR-172 | Analysis Context | Research Context / Dataset Version / Analysis ViewはCurrent Projectと整合するexisting resourceから選択し、復元不能時は架空default resourceを生成せずunselectedとする | MUST | ACTIVE | IMPLEMENTED | ENH-E7 |
| FR-173 | Analysis Context | Dataset Version変更時にselected Analysis Viewが互換でなければAnalysis View selectionを解除し、context変更または不足だけを理由にFamily / Stage routeを書き換えない | MUST | ACTIVE | IMPLEMENTED | ENH-E7 |
| FR-174 | Analysis Surface | existing Causal / Exploratory / Predictive capabilityを定義済みStage Contentsから操作可能にし、UI再配置だけを理由にanalysis execution semanticsを変更しない | MUST | ACTIVE | IMPLEMENTED | ENH-E7 |
| FR-177 | Architecture | UI / IA再編だけを理由に既存API contract、persistence schema、backend analysis/domain semanticsを変更しない | MUST NOT | ACTIVE | IMPLEMENTED | ENH-E7 |
