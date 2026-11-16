# 10_16_fr_navigation_ui


---

## FR original requirement rows

| ID | Area | Requirement | Level | Requirement Status | Implementation Status | Delivery |
| --- | --- | --- | --- | --- | --- | --- |
| FR-104 | UI / Navigation | ApplicationはProject ManagementとAnalysis Workspaceを異なるnavigation scopeとして提供し、Project resource管理とFamily / Stage navigationを同一hierarchyへ混在させない | MUST | ACTIVE | IMPLEMENTED | ENH-E7 |
| FR-105 | UI / Navigation | Project Management routeとAnalysis routeはいずれも独立URL、direct link、reload、browser Back / Forwardでdeterministicに復元できる | MUST | ACTIVE | IMPLEMENTED | ENH-E7 |
| FR-106 | UI | Analysis WorkspaceはAnalysis ContextとしてCurrent Project、Active Research Context、Dataset Version、Analysis Viewを明示する | MUST | ACTIVE | IMPLEMENTED | ENH-E7 |
| FR-107 | UI | 操作の可否と不可理由を一貫した権限・状態に基づいて表示できる | MUST | ACTIVE | PARTIAL | ENH-E5 |
| FR-108 | UI | 分析仕様・実行・結果・Graphへ文脈を保持して直接移動できる | MUST | ACTIVE | IMPLEMENTED | ENH-E5 |
| FR-109 | UI | 読み込み中・空結果・部分結果・失敗・取消を適切に区別して表示できる | MUST | ACTIVE | PARTIAL | ENH-E5 |
| FR-110a | UI | current result/list surfaceでfamily/type/status等の既存filterを提供する | SHOULD | ACTIVE | IMPLEMENTED | BASELINE |
| FR-110b | UI | 一覧・比較filterをdataset、context、date等へ拡張する | SHOULD | DEFERRED | NOT_IMPLEMENTED | FUTURE |
| FR-111 | UI | current surfaceでkeyboard、deterministic focus、accessible name、error association、non-color semanticsおよびcontrast要件を満たす | MUST | ACTIVE | PARTIAL | ENH-E5 |
| FR-112 | UI | Exploratory、Predictive、Causalの用語と警告を明示的に分離する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-129 | Navigation | Exploratory / Predictive / Causalをfirst-classなAnalysis Familyとして常時選択可能にする | MUST | ACTIVE | IMPLEMENTED | ENH-E5 |
| FR-130 | Navigation | 現在の分析Familyと画面位置を識別・復元できる | MUST | ACTIVE | IMPLEMENTED | ENH-E5 |
| FR-131 | Navigation | Family-local navigationにはselected Familyが所有するNavigation Stageだけを表示する | MUST | ACTIVE | IMPLEMENTED | ENH-E5 |
| FR-132 | Navigation | Family切替後は、そのFamilyの初期画面へ遷移できる | MUST | ACTIVE | PARTIAL | ENH-E5 |
| FR-133 | Navigation | FamilyごとにCapability-owned immutable descriptorでStage ID、slug、label、order、default Stageを独立定義する | MUST | ACTIVE | PARTIAL | ENH-E5 |
| FR-134 | Navigation | Family間でStage数・名称を揃える目的のdummy/common Stageを導入しない | MUST NOT | ACTIVE | IMPLEMENTED | ENH-E5 |
| FR-135 | Navigation | Navigation Stageの表示順をwizard completion、runtime dependency、実行前提として強制しない | MUST NOT | ACTIVE | IMPLEMENTED | ENH-E5 |
| FR-136 | Navigation | 分析ページのURLから対象Project・Family・画面位置を復元できる | MUST | ACTIVE | IMPLEMENTED | ENH-E5 |
| FR-137 | Navigation | reload、browser back、browser forwardでFamily / Stage stateをdeterministicに復元できる | MUST | ACTIVE | IMPLEMENTED | ENH-E5 |
| FR-138 | Navigation | unknown Family / Stageをsilent fallbackで意味変換せず明示errorと有効な遷移先を提示する | MUST | ACTIVE | PARTIAL | ENH-E5 |
| FR-139 | Navigation | Overview / Research Context / Data / ResultsをProject Management local navigationとして扱い、Exploratory / Predictive / CausalのAnalytical Familyと同一taxonomyへ混在させない | MUST | ACTIVE | IMPLEMENTED | ENH-E7 |
| FR-140 | Navigation / Runtime | Navigation Stageをruntime `StageType` / `StageDefinition` / `StageExecution`として再利用・継承しない | MUST NOT | ACTIVE | IMPLEMENTED | ENH-E5 |
| FR-141 | Navigation / Runtime | Navigation StageとExecution Stageの1:1 mappingを要求するcontractを導入しない | MUST NOT | ACTIVE | IMPLEMENTED | ENH-E5 |
| FR-144 | Capability | concrete Navigation Stage catalogは各Family-specific Capabilityが所有し、application/interface aggregatorがread-only metadataとして集約する | MUST | ACTIVE | PARTIAL | ENH-E5 |
| FR-145 | Capability | generic application layerはFamily-specific Stage semanticsを集中所有しない | MUST NOT | ACTIVE | NOT_IMPLEMENTED | ENH-E5 |
| FR-157 | Domain / Compatibility | 既存`AnalysisSpecification.analysis_family`をFamily discriminatorとして再利用し、duplicate Family field/enumを追加しない | MUST | ACTIVE | IMPLEMENTED | ENH-E5 |
| FR-158 | Domain / Compatibility | AnalysisSpecification / ExecutionPlan / Execution / StageExecutionへNavigation Stage fieldを追加しない | MUST NOT | ACTIVE | IMPLEMENTED | ENH-E5 |
| FR-159 | Compatibility | 旧分析画面から正規の分析画面へ一意に遷移できる | MUST | ACTIVE | IMPLEMENTED | ENH-E7 |
| FR-160 | Compatibility | Family / Navigation / application IAの変更だけを理由にDB schema migrationまたはnavigation-state persistenceを導入しない | MUST NOT | ACTIVE | IMPLEMENTED | ENH-E7 |
| FR-162 | Scope | Overview / FlagshipをAnalytical Family peerとして追加しない | MUST NOT | ACTIVE | IMPLEMENTED | ENH-E5 |
| FR-163 | Project Navigation | Project一覧へ一意の正規画面からアクセスできる | MUST | ACTIVE | IMPLEMENTED | ENH-E7 |
| FR-164 | Project Navigation | Project作成後に対象Projectの概要画面へ遷移できる | MUST | ACTIVE | IMPLEMENTED | ENH-E7 |
| FR-165 | Project Navigation | 対象Projectの標準表示画面を一意に復元できる | MUST | ACTIVE | IMPLEMENTED | ENH-E7 |
| FR-170 | Analysis Workspace | Analysis WorkspaceをProject Managementとは別surfaceとし、Family / Stage navigationはAnalysis Workspace内だけに表示する | MUST | ACTIVE | IMPLEMENTED | ENH-E7 |
| FR-171 | Analysis Context | 分析画面で選択Projectを確認でき、Project変更は管理機能で実施できる | MUST | ACTIVE | IMPLEMENTED | ENH-E7 |
| FR-172 | Analysis Context | Research Context / Dataset Version / Analysis ViewはCurrent Projectと整合するexisting resourceから選択し、復元不能時は架空default resourceを生成せずunselectedとする | MUST | ACTIVE | IMPLEMENTED | ENH-E7 |
| FR-173 | Analysis Context | Dataset Version変更時にselected Analysis Viewが互換でなければAnalysis View selectionを解除し、context変更または不足だけを理由にFamily / Stage routeを書き換えない | MUST | ACTIVE | IMPLEMENTED | ENH-E7 |
| FR-174 | Analysis Surface | 既存の因果・探索・予測機能を整理後の画面から利用でき、分析の意味を維持する | MUST | ACTIVE | IMPLEMENTED | ENH-E7 |
| FR-177 | Architecture | UI・IA再編によって既存API契約・永続化Schema・分析の意味を変更しない | MUST NOT | ACTIVE | IMPLEMENTED | ENH-E7 |
