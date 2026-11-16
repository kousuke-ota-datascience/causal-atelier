# 10_01_business_capabilities


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
