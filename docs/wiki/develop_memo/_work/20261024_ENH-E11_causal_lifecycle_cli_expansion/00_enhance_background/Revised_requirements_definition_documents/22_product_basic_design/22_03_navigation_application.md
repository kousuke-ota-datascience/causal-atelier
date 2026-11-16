# 22_03_navigation_application


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

**当該機能に適用する設計制約（関連Requirement）**

- **`FR-143`**：runtime layerはNavigation Stage ID、browser route、tab/sidebar stateへ依存しない
- **`FR-107`**：操作可否をBackend authoritative state/authorizationから導出し、`allowed / reason_code / message`としてpresentationへ返す
- **`FR-108`**：AnalysisSpecification、Execution、Result、GraphVersionへFamily/Navigation Stage contextを保持したdeep routeで直接遷移できる
- **`FR-109`**：非同期presentation stateを`IDLE / LOADING / READY / EMPTY / PARTIAL / ERROR / CANCELLED`として区別する
- **`FR-130`**：Current Familyをactive stateとcanonical route `/projects/{project_id}/analysis/{family_slug}/{stage_slug}`の双方で一意に識別できる
- **`FR-132`**：Family切替時はCapability descriptorが宣言するdefault Navigation Stage（Exploratory=`profile`, Causal=`setup`, Predictive=`setup`）へ遷移する
- **`FR-133`**：FamilyごとにCapability-owned immutable descriptorでStage ID、slug、label、order、default Stageを独立定義する
- **`FR-136`**：canonical URL `/projects/{project_id}/analysis/{family_slug}/{stage_slug}`からProject、Family、Navigation Stageを復元できる
- **`FR-140`**：Navigation Stageをruntime `StageType` / `StageDefinition` / `StageExecution`として再利用・継承しない
- **`FR-141`**：Navigation StageとExecution Stageの1:1 mappingを要求するcontractを導入しない
- **`FR-144`**：concrete Navigation Stage catalogは各Family-specific Capabilityが所有し、application/interface aggregatorがread-only metadataとして集約する
- **`FR-145`**：generic application layerはFamily-specific Stage semanticsを集中所有しない
- **`FR-157`**：既存`AnalysisSpecification.analysis_family`をFamily discriminatorとして再利用し、duplicate Family field/enumを追加しない
- **`FR-158`**：AnalysisSpecification / ExecutionPlan / Execution / StageExecutionへNavigation Stage fieldを追加しない
- **`FR-159`**：supported legacy analytical entryはFamily Capability catalogで解決したcanonical Analysis routeへ一方向normalizeし、parallel navigation authorityとして維持しない
- **`FR-160`**：Family / Navigation / application IAの変更だけを理由にDB schema migrationまたはnavigation-state persistenceを導入しない
- **`FR-171`**：Current Projectはcanonical Analysis URLの`project_id`をauthorityとしAnalysis Workspace内ではread-onlyとする。Project変更はProject Management経由で行う
- **`NFR-021`**：Navigation concernの変更がruntime execution lifecycleへ不要に伝播しない
- **`NFR-023`**：Family-specific Navigation Stage catalogをCapability ownershipで局所化する
- **`NFR-025`**：CLI / library executionがWeb UI route、tab/sidebar state、NavigationStageDescriptorへ依存しない
- **`AR-021`**：Navigation Stageの表示順を分析上必須の実行順序として解釈しない
- **`AR-022`**：Family間でStage数・名称を揃えることを科学的workflow要件としない
- **`AR-024`**：Causal Effectsは推定されたeffectの閲覧・利用を扱い、estimator configurationと混在させない
