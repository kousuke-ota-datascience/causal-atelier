<!-- ENH-E11 split working copy: not a formal approval. -->
# 10 — capabilities e2e

**Status:** `STRUCTURAL_COPY_DRAFT` (existing baseline text, not E11 canonical publication)

**Source:** [10_requirements_definition.md](https://github.com/kousuke-ota-datascience/causal-atelier/blob/3ba5fe2465ec591f0da7f998c21a5241984b73dc/docs/wiki/requirement_definition/10_requirements_definition.md) · blob `40b83f29c67b4a39f6db5393be7534c5e892d656`  
**Index:** [Revised document inventory](../README_00_Revised_requirements_definition_documents.md)

---

## 3. 業務Capability

| Capability | 目的 | 正本Resource |
| --- | --- | --- |
| Project Management | Project lifecycleとProject-local resource管理のsurface責務を提供する | Project、ResearchContextVersion、DatasetVersion、AnalysisView、Result、Artifact、LineageEdge |
| Project / Research Context | 分析の意味、問い、意思決定を固定する | Project、ResearchContextVersion |
| Data / Analysis View | 入力データと分析対象条件を固定する | DatasetVersion、AnalysisView |
| Exploratory Analysis | データ品質・分布・関係・比較を探索し、Finding候補を蓄積する | AnalysisSpecification(EXPLORATORY)、Result、Artifact、Annotation |
| Causal Analysis | 介入効果を仮定・識別・診断とともに評価する | AnalysisSpecification(CAUSAL)、GraphVersion、Result |
| Predictive Analysis | 将来targetの予測可能性とmodel挙動を評価する | AnalysisSpecification(PREDICTIVE)、Result、Artifact |
| Workflow | Planner、Plan、Stage、Runner、Executorを制御する | ExecutionPlan、Execution、StageExecution |
| Results / Lineage | 結果比較、判断、来歴、Exportを提供する | Result、Artifact、Annotation、LineageEdge |
| Application Navigation | Project ManagementとAnalysis Workspaceを別navigation scopeとしてroute-backedに提示する | browser route / application state（non-persistent） |
| Analytical Navigation | Analysis Workspace内でAnalysis FamilyとFamily-local Navigation Stageを独立したnavigation dimensionとして提示する | AnalysisFamily、Navigation metadata/state（non-persistent） |

### 3.1. Analytical Navigation frozen catalog

Navigation catalogのauthorityはFamily Capability descriptorをaggregateするbackend read-only metadata interfaceとする。

```text
GET /api/v1/navigation/analysis
schema: analysis-navigation/1
```

| Family | family_slug | default_stage_id | Navigation Stages |
| --- | --- | --- | --- |
| EXPLORATORY | `exploratory` | `profile` | `profile`, `data-quality`, `distribution`, `relationships`, `comparison`, `findings` |
| PREDICTIVE | `predictive` | `setup` | `setup`, `train`, `predict`, `metrics`, `explainability`, `model-management` |
| CAUSAL | `causal` | `setup` | `setup`, `discovery`, `identification`, `estimation`, `effects`, `diagnostics`, `sensitivity` |

Canonical Project routes:

```text
/projects
/projects/new
/projects/{project_id}/overview
/projects/{project_id}/context
/projects/{project_id}/data
/projects/{project_id}/results
```

`/projects/{project_id}`は`/projects/{project_id}/overview`へhistory-replace semanticsでnormalizeする。

Canonical analytical route:

```text
/projects/{project_id}/analysis/{family_slug}/{stage_slug}
```

Resource deep route:

```text
/projects/{project_id}/analysis/{family_slug}/{stage_slug}/resource/{resource_type}/{resource_id}
```

Supported resource typeは`analysis-specification / execution / result / graph-version`とする。Supported legacy analytical entryは各Family default Stageへ一方向normalizeする。

`analysis-navigation/1`はpresentation/application metadata schemaであり、scientific generic `SchemaRegistry`へ登録しない。Frontendはfull catalogをduplicate ownershipしない。


## 4. E2Eシナリオ

| ID | シナリオ | 完了条件 |
| --- | --- | --- |
| E2E-01 | Research Workspaceを作成する | ProjectとResearch Contextを作成し、Dataset Versionを登録してProject-global surfaceと三つのAnalytical Familyへ遷移できる |
| E2E-02 | 探索・可視化を保存する | Datasetの品質・分布・関連を確認し、ChartとAnalysis Viewを保存できる |
| E2E-03 | 探索から分析draftを作る | 探索ResultからCausalまたはPredictive Specification draftを作成し、source relationを保持できる |
| E2E-04 | 因果効果を評価する | Graph、Question、Design、Identification、Eligibility、Estimation、Diagnostics、Refutation、Sensitivityを実行できる |
| E2E-05 | 分類モデルを評価する | Binary Classificationをsplit、train、evaluate、explainし、test isolationを確認できる |
| E2E-06 | 回帰モデルを評価する | Regressionをsplit、train、evaluate、error analysisし、複数modelを比較できる |
| E2E-07 | 条件変更を比較する | base ExecutionからRERUNまたはREVISEDを作成し、changed dimensionsと結果差分を確認できる |
| E2E-08 | 横断来歴を確認する | ReviewerがResearch ContextからExploratory、Causal、PredictiveのResultと判断理由へ遡れる |
| E2E-09 | Analysis Familyを横断する | Family tabでExploratory / Predictive / Causalを切り替え、selected FamilyのNavigation Stageだけを左navigationから選択できる |
| E2E-10 | UIを経由せずanalysisを実行する | CLI / Python library / backend use caseからCurrent Navigation Stageを指定せず既存analysis executionを開始できる |
| E2E-11 | Project resourceを管理する | Project List / RegisterからProjectを選択し、Overview / Research Context / Data / Resultsへroute-backedに遷移できる |
| E2E-12 | Analysis Workspaceでcontextを保持して分析する | Current Projectをread-onlyで確認し、Research Context / Dataset Version / Analysis Viewを選択してFamily / Stageを操作でき、context変更だけでFamily / Stage routeが失われない |

### 4.1. E2E共通受入条件

- Command受付時にProject権限、Resource状態、SchemaおよびFamily固有validationが実行される
- すべてのExecutionがResearch Context Version、Dataset VersionまたはAnalysis Viewを固定する
- ResultとArtifactがExecution / Stageへ紐付く
- UI表示とAPI payloadが同じ保存済み正本を参照する
- 失敗時にtechnical failure、validation rejection、analytical negative resultを区別する
- Navigation Stageの存在・順序をruntime Execution Stageやworkflow completionへ読み替えない
