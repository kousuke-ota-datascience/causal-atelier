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
