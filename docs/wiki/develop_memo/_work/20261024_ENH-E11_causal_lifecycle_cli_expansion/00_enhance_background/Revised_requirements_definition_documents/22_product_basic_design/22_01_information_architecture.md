<!-- ENH-E11 split working copy: not a formal approval. -->
# 22 — information architecture

**Status:** `STRUCTURAL_COPY_DRAFT` (existing baseline text, not E11 canonical publication)

**Source:** [22_product_basic_design.md](https://github.com/kousuke-ota-datascience/causal-atelier/blob/3ba5fe2465ec591f0da7f998c21a5241984b73dc/docs/wiki/requirement_definition/22_product_basic_design.md) · blob `87196f2f03a7f3367724bc05fb254d1a4d98109e`  
**Index:** [Revised document inventory](../README_00_Revised_requirements_definition_documents.md)

---

## 5. 利用者向けInformation Architecture

### 5.1. Top-level IA authorityと基本設計での詳細化

Top-level IAの**概念的な階層・意味**は`00_product_concept_memo.md > 3. Ariadne application model`をauthorityとし、本書では同じ概念説明を重複させない。

本書では、そのIAを実装可能な基本設計へ落とすため、surface responsibility、route authority、resource lifecycle ownership、UI state / operation boundaryを次のように具体化する。

| IA node | Basic-design responsibility | Navigation / state authority |
| --- | --- | --- |
| Project List | Project一覧・選択・Project Registerへの入口 | `/projects` |
| Project Register | Project新規作成 | `/projects/new` |
| Selected Project / Overview | Project identity / metadata / status / archive | Project route + Project status |
| Selected Project / Research Context | Research Context version lifecycle / history | Project-scoped ResearchContextVersion |
| Selected Project / Data | Dataset Version / schema / preview / Analysis View lifecycle | Project-scoped DatasetVersion / AnalysisView |
| Selected Project / Results / Lineage | persisted evidence / comparison / Artifact / Lineage / Annotation | Project-scoped canonical Results / references |
| Analysis Context | Current Project / Active Research Context / Dataset Version / Analysis Viewのcurrent selection | URL project_id + Project-scoped selection/resource |
| Analysis / Family | analytical paradigm選択 | canonical Analysis route + navigation catalog |
| Analysis / Stage | Family-local work/view context | canonical Analysis route + navigation catalog |
| Stage Contents | selected Family/Stageのexecution / presentation | renderer binding + backend operation availability |

### 5.2. Project Management surface decomposition

Project Managementは次のpresentation responsibilityへ分解する。

```text
Projects Surface
├─ Project List
└─ Project Register

Selected Project Shell
├─ Project Header
├─ Project Local Navigation
└─ Selected Project Contents
   ├─ Overview
   ├─ Research Context
   ├─ Data
   └─ Results / Lineage
```

Resource ownership:

| Surface | Responsibility |
| --- | --- |
| Overview | Project metadata / identity / status / archive |
| Research Context | Research Context lifecycle / DRAFT-FIXED / history / related analysis |
| Data | Dataset / Dataset Version / Schema / Preview / Analysis View lifecycle |
| Results / Lineage | persisted cross-analysis aggregation / comparison / Artifact / Lineage / Annotation |

Analysis ViewはFamily横断のversioned analysis inputであり、create / edit / version-management authorityをDataが持つ。

### 5.3. Analysis Workspace surface decomposition

```text
Analysis Workspace Shell
├─ Analysis Context
├─ Family navigation
├─ Family-local Stage navigation
└─ Stage Contents
```

- Family = analytical navigation
- Navigation Stage = selected Family内のwork/view navigation
- Stage Contents = selected Family/Stageのmain analytical presentation
- Family / Stage navigationはAnalysis Workspace内だけに表示する
- Current ProjectはAnalysis Workspace内ではread-onlyであり、Project変更はProject Management経由で行う

Analysis Context:

```text
Current Project
Active Research Context
Dataset Version
Analysis View
```

Research Context / Dataset Version / Analysis ViewはCurrent Projectと整合するexisting resource/stateから選択する。Dataset Version変更時にselected Analysis Viewが互換でなければAnalysis View selectionを解除する。有効selectionを復元できない場合は架空default resourceを生成しない。

### 5.4. Route / deep link / history authority

Application NavigationはProject NavigationとAnalysis Navigationを別authorityとして扱う。

```text
Project Navigation
├─ /projects
├─ /projects/new
├─ /projects/{project_id}/overview
├─ /projects/{project_id}/context
├─ /projects/{project_id}/data
└─ /projects/{project_id}/results

Analysis Navigation
└─ /projects/{project_id}/analysis/{family_slug}/{stage_slug}[/resource/...]
```

`/projects/{project_id}`はhistory replace semanticsで`/projects/{project_id}/overview`へnormalizeする。

Canonical Analysis route:

```text
/projects/{project_id}/analysis/{family_slug}/{stage_slug}
```

Resource deep route:

```text
/projects/{project_id}/analysis/{family_slug}/{stage_slug}/resource/{resource_type}/{resource_id}
```

Resource semanticとFamily/Stageが矛盾する場合はsilent correctionせずroute errorとする。Project/Analysis双方でdirect link、reload、browser Back、browser Forwardを成立させる。Supported legacy analytical entryはcanonical Analysis routeへ一方向normalizeし、parallel navigation authorityとして維持しない。

### 5.5. Analysis navigation catalog

Family切替時はbackend read-only navigation catalogの`default_stage_id`をauthorityとする。Frontendはfull catalogをduplicate ownershipしない。current read-only authorityは次であり、interface詳細は`23_api_interface_design.md`で定義する。

```text
GET /api/v1/navigation/analysis
schema = analysis-navigation/1
```

| Family | slug | default_stage_id | Navigation Stages |
| --- | --- | --- | --- |
| EXPLORATORY | `exploratory` | `profile` | Profile / Data Quality / Distribution / Relationships / Comparison / Findings |
| PREDICTIVE | `predictive` | `setup` | Setup / Train / Predict / Metrics / Explainability / Model Management |
| CAUSAL | `causal` | `setup` | Setup / Discovery / Identification / Estimation / Effects / Diagnostics / Sensitivity |

Family間でStage数を揃えるためのdummy Stageは作らない。Stage順はpresentation orderでありruntime dependency / required progressionではない。

### 5.6. Stage Contentsへのexisting capability配置

#### 5.6.1. Causal

| Stage | Primary responsibility |
| --- | --- |
| Setup | causal question / design preparation / Direct Graph Registration |
| Discovery | Discovery specification / PC-GES / Graph Candidates / comparison-edit-adopt-fix |
| Identification | Identification input / Data Eligibility / Gate |
| Estimation | estimator selection / override / execution / revision |
| Effects | Treatment Effect Results / result comparison |
| Diagnostics | diagnostics / scientific warnings |
| Sensitivity | Refutation / Sensitivity analysis |

Navigation Stage配置を理由にCausal execution semanticsを変更しない。

#### 5.6.2. Exploratory

| Stage | Existing operation / availability | Placement behavior |
| --- | --- | --- |
| Profile | `PROFILE` | operation controlとProfile result |
| Data Quality | dedicated operationなし | read-only availability。existing `PROFILE` resultを表示し、存在しなければ`NO_PROFILE_RESULT`とProfileへの導線を表示。新Execution/resource/backend stateを作らない |
| Distribution | `DISTRIBUTION` | operation controlとresult |
| Relationships | `ASSOCIATION` | operation controlとresult |
| Comparison | `GROUP_SUMMARY`, `TIME_TREND` | 両operationのcontrol/result。`TIME_TREND`はexisting grouping/aggregation semanticsを維持する |
| Findings | `CHART` + saved Exploratory Results | `CHART` control、Chart result/artifact、saved result |

`DATA_QUALITY` operationをtaxonomy充足のために新設しない。Stage placementを理由にExploratory planner、runner、Result type、Artifact type、API/persistenceを変更しない。

#### 5.6.3. Predictive

Existing semantics `Prediction Task -> Split -> Training -> Evaluation -> Explanation -> Model Card`を保持する。Navigation Stageはpresentation/navigation viewであり、新しいPredictive backend Execution modelではない。

| Stage | Primary presentation |
| --- | --- |
| Setup | Prediction Task / target-feature / Split configuration |
| Train | Training / status / result |
| Predict | existing prediction output presentationの範囲 |
| Metrics | Evaluation / metrics |
| Explainability | Explanation |
| Model Management | Model Card / existing model management surface |
