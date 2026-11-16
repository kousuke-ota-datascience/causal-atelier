# 22_03_navigation_application

**Status:** `RD02_STRUCTURAL_WORKING_COPY / E11_NOT_PUBLISHED`. Original chapter and source provenance retained; DD physical coverage remains partial.  
**Source blob:** `87196f2f03a7f3367724bc05fb254d1a4d98109e`.

---

## 7. 画面遷移と論理引渡し

Browser stateへcanonical Resource全体を保持せず、遷移先はroute/resource identityと必要なselectionを用いてAPIから正本を再取得する。

| 遷移元 | 遷移先 | 前提 | 引渡し / authority | 遷移先での復元 |
| --- | --- | --- | --- | --- |
| Project List | Project Register | create action | route=`/projects/new` | registration formを初期化 |
| Project Register | Overview | Project create成功 | new `project_id` | Projectを再取得 |
| Project List | Overview | Project選択 | `project_id` | Project + local navigationを復元 |
| Overview / Context / Data / Results | Selected Project内別section | Project read permission | `project_id` + section route | section固有Resourceを再取得 |
| Project Management | Analysis Workspace | Project選択済み | `project_id` + target family/stage | Analysis Context + navigation catalogを復元 |
| Analysis Context Dataset変更 | current Family/Stage | same Project DatasetVersion | WorkspaceSelection更新 | route維持、Analysis View compatibilityを再検証 |
| Family A | Family B | valid catalog | family slug + B default stage | target Stage bindingを復元 |
| Stage A | Stage B | same Family valid Stage | stage slug | selected Stage contentsを復元 |
| Stage Contents | resource deep route | compatible Resource | resource type/id | Resourceを再取得しsemantic整合を検証 |
| Analysis Workspace | Results / Lineage | persisted Result等選択 | `project_id` + selected resource identity | Project-scoped evidenceを再取得 |
| Results / Lineage | Analysis Workspace | source execution/spec/contextが追跡可能 | project/family/stage/resource identity | canonical routeとcontextを復元 |

Project NavigationとAnalysis Navigationは別authorityであり、Project-local section変更でFamily/Stageを暗黙変更したり、Family/Stage変更でProject Management resource lifecycleを暗黙更新したりしない。

## 8. Application / Query Service責務

物理class名は下位文書へ委譲し、本書ではservice responsibilityを次のように分離する。

| Service responsibility | 主な責務 | 主な状態/Resource boundary |
| --- | --- | --- |
| Project Management Service | Project create/update/archive、ACTIVE guard | Project |
| Research Context Service | Context version create/edit/fix/history | ResearchContextVersion |
| Data / Analysis View Service | Dataset register/query、Analysis View lifecycle、compatibility validation | DatasetVersion / Artifact / AnalysisView |
| Workspace Selection Service | Active Context / Dataset / Analysis View selection整合 | WorkspaceSelection + Project-scoped Resource |
| Analysis Navigation Service | Family/Stage catalog、default Stage、route semantic | navigation metadata。persistent Domain Resource化しない |
| Analysis Specification / Planning Service | Family-specific spec validation、Execution Plan構築 | AnalysisSpecification / ExecutionPlan |
| Execution Service | submit、cancel/retry/revision等のexecution lifecycle coordination | Execution / StageExecution / StageAttempt |
| Result / Artifact Service | Result、Artifact metadata、保存・取得 | Result / Artifact |
| Graph Version Service | Graph作成、DRAFT編集、FIX、parent/outcome validation | GraphVersion |
| Comparison Query Service | compatible Result等の比較projection | canonical Resourceを更新しない |
| Lineage Query Service | Result / Execution / Graph / Dataset / Artifact等のprovenance reconstruction | canonical refs / LineageEdge |
| Annotation Service | Annotation writeとProject state guard | Annotation + target Resource |

Frontendはこれらのresponsibilityを単一巨大client-side state machineへ再実装しない。


## 98. RD-04：要件由来の基本設計制約

**Status:** `RD04_DESIGN_MIGRATED / OWNER_CONTENT_REVIEW_PENDING`。要件文の抽象化・設計移管で失われてはならない元の実現方式・責務境界を保持する。旧Requirement IDとStatusを維持する。コード検証やArchitecture GateのPASSを意味しない。

### 98.1. FR-143（MOVE_BD）

- 既存要件の設計情報を含む原文：runtime layerはNavigation Stage ID、browser route、tab/sidebar stateへ依存しない
- RDに残る能力／Legacy Trace：【設計制約移管・Legacy Trace】NFR-025の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する
- Original Requirement：`FR-143`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.2. FR-107（SPLIT）

- 既存要件の設計情報を含む原文：操作可否をBackend authoritative state/authorizationから導出し、`allowed / reason_code / message`としてpresentationへ返す
- RDに残る能力／Legacy Trace：操作の可否と不可理由を一貫した権限・状態に基づいて表示できる
- Original Requirement：`FR-107`; Status：`ACTIVE`; Implementation：`PARTIAL`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.3. FR-108（SPLIT）

- 既存要件の設計情報を含む原文：AnalysisSpecification、Execution、Result、GraphVersionへFamily/Navigation Stage contextを保持したdeep routeで直接遷移できる
- RDに残る能力／Legacy Trace：分析仕様・実行・結果・Graphへ文脈を保持して直接移動できる
- Original Requirement：`FR-108`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.4. FR-109（SPLIT）

- 既存要件の設計情報を含む原文：非同期presentation stateを`IDLE / LOADING / READY / EMPTY / PARTIAL / ERROR / CANCELLED`として区別する
- RDに残る能力／Legacy Trace：読み込み中・空結果・部分結果・失敗・取消を適切に区別して表示できる
- Original Requirement：`FR-109`; Status：`ACTIVE`; Implementation：`PARTIAL`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.5. FR-130（SPLIT）

- 既存要件の設計情報を含む原文：Current Familyをactive stateとcanonical route `/projects/{project_id}/analysis/{family_slug}/{stage_slug}`の双方で一意に識別できる
- RDに残る能力／Legacy Trace：現在の分析Familyと画面位置を識別・復元できる
- Original Requirement：`FR-130`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.6. FR-132（SPLIT）

- 既存要件の設計情報を含む原文：Family切替時はCapability descriptorが宣言するdefault Navigation Stage（Exploratory=`profile`, Causal=`setup`, Predictive=`setup`）へ遷移する
- RDに残る能力／Legacy Trace：Family切替後は、そのFamilyの初期画面へ遷移できる
- Original Requirement：`FR-132`; Status：`ACTIVE`; Implementation：`PARTIAL`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.7. FR-133（MOVE_BD）

- 既存要件の設計情報を含む原文：FamilyごとにCapability-owned immutable descriptorでStage ID、slug、label、order、default Stageを独立定義する
- RDに残る能力／Legacy Trace：【設計制約移管・Legacy Trace】FR-131の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する
- Original Requirement：`FR-133`; Status：`ACTIVE`; Implementation：`PARTIAL`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.8. FR-136（SPLIT）

- 既存要件の設計情報を含む原文：canonical URL `/projects/{project_id}/analysis/{family_slug}/{stage_slug}`からProject、Family、Navigation Stageを復元できる
- RDに残る能力／Legacy Trace：分析ページのURLから対象Project・Family・画面位置を復元できる
- Original Requirement：`FR-136`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.9. FR-140（MOVE_BD）

- 既存要件の設計情報を含む原文：Navigation Stageをruntime `StageType` / `StageDefinition` / `StageExecution`として再利用・継承しない
- RDに残る能力／Legacy Trace：【設計制約移管・Legacy Trace】NFR-021の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する
- Original Requirement：`FR-140`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.10. FR-141（MOVE_BD）

- 既存要件の設計情報を含む原文：Navigation StageとExecution Stageの1:1 mappingを要求するcontractを導入しない
- RDに残る能力／Legacy Trace：【設計制約移管・Legacy Trace】NFR-021の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する
- Original Requirement：`FR-141`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.11. FR-144（MOVE_BD）

- 既存要件の設計情報を含む原文：concrete Navigation Stage catalogは各Family-specific Capabilityが所有し、application/interface aggregatorがread-only metadataとして集約する
- RDに残る能力／Legacy Trace：【設計制約移管・Legacy Trace】FR-131の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する
- Original Requirement：`FR-144`; Status：`ACTIVE`; Implementation：`PARTIAL`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.12. FR-145（MOVE_BD）

- 既存要件の設計情報を含む原文：generic application layerはFamily-specific Stage semanticsを集中所有しない
- RDに残る能力／Legacy Trace：【設計制約移管・Legacy Trace】NFR-023の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する
- Original Requirement：`FR-145`; Status：`ACTIVE`; Implementation：`NOT_IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.13. FR-157（MOVE_BD）

- 既存要件の設計情報を含む原文：既存`AnalysisSpecification.analysis_family`をFamily discriminatorとして再利用し、duplicate Family field/enumを追加しない
- RDに残る能力／Legacy Trace：【設計制約移管・Legacy Trace】FR-074の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する
- Original Requirement：`FR-157`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.14. FR-158（MOVE_BD）

- 既存要件の設計情報を含む原文：AnalysisSpecification / ExecutionPlan / Execution / StageExecutionへNavigation Stage fieldを追加しない
- RDに残る能力／Legacy Trace：【設計制約移管・Legacy Trace】NFR-021の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する
- Original Requirement：`FR-158`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.15. FR-159（SPLIT）

- 既存要件の設計情報を含む原文：supported legacy analytical entryはFamily Capability catalogで解決したcanonical Analysis routeへ一方向normalizeし、parallel navigation authorityとして維持しない
- RDに残る能力／Legacy Trace：旧分析画面から正規の分析画面へ一意に遷移できる
- Original Requirement：`FR-159`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.16. FR-160（MOVE_BD）

- 既存要件の設計情報を含む原文：Family / Navigation / application IAの変更だけを理由にDB schema migrationまたはnavigation-state persistenceを導入しない
- RDに残る能力／Legacy Trace：【設計制約移管・Legacy Trace】NFR-021／FR-177の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する
- Original Requirement：`FR-160`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.17. FR-171（SPLIT）

- 既存要件の設計情報を含む原文：Current Projectはcanonical Analysis URLの`project_id`をauthorityとしAnalysis Workspace内ではread-onlyとする。Project変更はProject Management経由で行う
- RDに残る能力／Legacy Trace：分析画面で選択Projectを確認でき、Project変更は管理機能で実施できる
- Original Requirement：`FR-171`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.18. NFR-021（SPLIT）

- 既存要件の設計情報を含む原文：Navigation concernの変更がruntime execution lifecycleへ不要に伝播しない
- RDに残る能力／Legacy Trace：画面ナビゲーションの変更が分析実行ライフサイクルに影響しない
- Original Requirement：`NFR-021`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../96_rd04_nfr_ar_application_review.md)

### 98.19. NFR-023（SPLIT）

- 既存要件の設計情報を含む原文：Family-specific Navigation Stage catalogをCapability ownershipで局所化する
- RDに残る能力／Legacy Trace：Familyごとの画面構成を他Familyへの影響を抑えて変更できる
- Original Requirement：`NFR-023`; Status：`ACTIVE`; Implementation：`NOT_IMPLEMENTED`; [RD-04逐条台帳](../96_rd04_nfr_ar_application_review.md)

### 98.20. NFR-025（SPLIT）

- 既存要件の設計情報を含む原文：CLI / library executionがWeb UI route、tab/sidebar state、NavigationStageDescriptorへ依存しない
- RDに残る能力／Legacy Trace：CLIやライブラリ実行を画面状態なしで行える
- Original Requirement：`NFR-025`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../96_rd04_nfr_ar_application_review.md)

### 98.21. AR-021（SPLIT）

- 既存要件の設計情報を含む原文：Navigation Stageの表示順を分析上必須の実行順序として解釈しない
- RDに残る能力／Legacy Trace：Navigation Stageの表示順を、因果分析その他の科学的な実行順序や必須解析手順として解釈させない
- Original Requirement：`AR-021`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../96_rd04_nfr_ar_application_review.md)

### 98.22. AR-022（MOVE_BD）

- 既存要件の設計情報を含む原文：Family間でStage数・名称を揃えることを科学的workflow要件としない
- RDに残る能力／Legacy Trace：【設計制約移管・Legacy Trace】対応する既存上位要件に係る既存設計制約。具体的な実装契約は下位設計へ移し、元ID・Status・科学的制約の追跡を維持する
- Original Requirement：`AR-022`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../96_rd04_nfr_ar_application_review.md)

### 98.23. AR-024（SPLIT）

- 既存要件の設計情報を含む原文：Causal Effectsは推定されたeffectの閲覧・利用を扱い、estimator configurationと混在させない
- RDに残る能力／Legacy Trace：因果効果の結果閲覧・利用と推定器の設定操作を混同せず、区別して利用できる
- Original Requirement：`AR-024`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../96_rd04_nfr_ar_application_review.md)
