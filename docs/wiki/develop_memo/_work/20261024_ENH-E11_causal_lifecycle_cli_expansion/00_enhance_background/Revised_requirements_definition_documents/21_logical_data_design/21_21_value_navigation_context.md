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


## 98. RD-04：要求の論理データ制約の受入・Trace

**Status:** `DESIGN_CONSTRAINT_MIGRATION / OWNER_CONTENT_REVIEW_PENDING`。以下はRD-04で抽象化した元要件のうち、データ定義・同一性・来歴・正本性に関係する条項を論理設計側に残したもの。原文は出典保証目的で保持する。現行コードで検証済みと主張しない。

### 98.FR-148. FR-148（SPLIT）

- 元要件（設計上の拘束を含む）：Findingsは既存Result / Annotation / Lineageを利用可能とし、新規persistent Finding resourceを必須化しない
- RD改訂後の要求：探索上のFindingで既存の結果・注釈・来歴を利用できる
- Trace：`FR-148`; Status=`ACTIVE`; Implementation=`IMPLEMENTED`; [逐条レビュー](../95_rd04_fr_application_review.md)

### 98.FR-177. FR-177（SPLIT）

- 元要件（設計上の拘束を含む）：UI / IA再編だけを理由に既存API contract、persistence schema、backend analysis/domain semanticsを変更しない
- RD改訂後の要求：UI・IA再編によって既存API契約・永続化Schema・分析の意味を変更しない
- Trace：`FR-177`; Status=`ACTIVE`; Implementation=`IMPLEMENTED`; [逐条レビュー](../95_rd04_fr_application_review.md)
