# 21_21_value_navigation_context

**Status:** `RD02_STRUCTURAL_WORKING_COPY / E11_NOT_PUBLISHED`; original ID, level and state retained.  
**Source blob:** `72903b9ad48b5b7edabaa7bb1c2cace42aa46ce7`.

---

### 4.2 Analysis Context

Analysis Contextは新しいpersistent aggregateではなく、current routeとProject-scoped selection/resourceの論理projectionである。

```text
Analysis Context
├─ Current Project
│  └─ canonical Analysis route.project_id
├─ Active Research Context
│  └─ WorkspaceSelection.research_context_version_id
├─ Dataset Version
│  └─ WorkspaceSelection.dataset_version_id
└─ Analysis View
   └─ WorkspaceSelection.analysis_view_id
```

| Element | Authority | Persistence |
| --- | --- | --- |
| Current Project | canonical Analysis route `project_id` | 専用field/resourceを追加しない |
| Active Research Context | `ResearchContextVersion` + `WorkspaceSelection` | existing lifecycleを利用 |
| Dataset Version | `DatasetVersion` + `WorkspaceSelection` | existing lifecycleを利用 |
| Analysis View | `AnalysisView` + `WorkspaceSelection` | existing lifecycleを利用 |
| Current Family / Navigation Stage | browser URL / navigation state | DB永続化しない |

Selection rule:

1. Research Context / Dataset Version / Analysis ViewはCurrent Projectと整合する。
2. Analysis Viewはselected Dataset Versionと互換である。
3. Dataset Version変更時、Analysis Viewが互換でなければAnalysis View selectionを解除する。
4. 有効selectionを復元できない場合、架空default resourceを作らずunselectedとする。
5. Context不足だけを理由にFamily / Navigation Stage routeを書き換えない。

### 4.3 Navigation metadata model

Navigation StageはAnalysis Specificationやruntime Stageとは異なるapplication metadataである。

```text
AnalysisFamily
   │
   ▼
FamilyNavigationDescriptor
   │
   └─ NavigationStageDescriptor*
            │
            └─ renderer / use-case binding
```

主要value:

| Value | 内容 |
| --- | --- |
| `FamilyNavigationDescriptor` | Family、default Stage、Stage catalog |
| `NavigationStageDescriptor` | Stage ID、label、order、表示metadata |
| Current Family | browser navigation state |
| Current Navigation Stage | Family-local browser navigation state |
| route representation | `/projects/{project_id}/analysis/{family_slug}/{stage_slug}` |
| renderer binding | `(family, stage)`から既存surface/use caseへのbinding |

Navigation metadataを`AnalysisSpecification`、`ExecutionPlan`、`Execution`、`StageExecution`へ保存しない。

**適用する論理データ制約（関連Requirement）**

- **`FR-148`**：Findingsは既存Result / Annotation / Lineageを利用可能とし、新規persistent Finding resourceを必須化しない
- **`FR-177`**：UI / IA再編だけを理由に既存API contract、persistence schema、backend analysis/domain semanticsを変更しない
