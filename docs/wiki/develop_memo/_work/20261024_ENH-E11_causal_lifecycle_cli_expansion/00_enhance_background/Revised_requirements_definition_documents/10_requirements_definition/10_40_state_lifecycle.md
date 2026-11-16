# 10_40_state_lifecycle


---

## 8. 状態要件

Ariadneのpersistent Resource、Execution lifecycleおよびNavigation stateは、それぞれ独立した状態体系として扱う。異なる状態体系を相互に読み替えない。

### 8.1. Project

Projectは次の状態遷移に従う。

```text
ACTIVE -> ARCHIVED
```

ARCHIVEDからACTIVEへの復元は、管理操作として別途定義するまで対象外とする。

### 8.2. Versioned Resource

DRAFT / FIXED lifecycleを持つVersioned Resourceは、次の状態遷移に従う。

```text
DRAFT -> FIXED
```

FIXED Resourceは上書きしない。変更時は新Versionまたはchild DRAFTを作成する。

### 8.3. Execution

Executionは次の状態遷移に従う。

```text
QUEUED -> RUNNING -> SUCCEEDED
                  -> FAILED -> QUEUED
QUEUED / RUNNING -> CANCELLED
```

`FAILED -> QUEUED`はtechnical retryによる再実行を表す。分析条件を変更する場合は同一Executionのretryではなく、新しいExecutionとして扱う。

### 8.4. Stage Execution

StageExecutionは次の状態遷移に従う。

```text
PENDING -> READY
READY -> RUNNING
RUNNING -> SUCCEEDED
RUNNING -> FAILED
FAILED -> PENDING
FAILED -> RUNNING
PENDING / READY -> SKIPPED_DUE_TO_PREREQUISITE
PENDING / READY / RUNNING -> CANCELLED
```

`FAILED -> PENDING`はretry準備、`FAILED -> RUNNING`はretry attempt開始時の遷移を表す。

StageExecutionの状態はruntime Execution Stageの実行状態であり、Navigation Stageの状態または完了状態として扱わない。

### 8.5. Analytical Status

Resultのanalytical statusはResult Typeごとに許可値を定義する。

ExecutionおよびStageExecutionのruntime statusと、Resultのanalytical statusを混在させない。technical failure、validation rejectionおよびanalytical negative resultは区別して扱う。

### 8.6. Navigation / Analysis Context State

Application navigation stateはProject route scopeとAnalysis route scopeを分離する。

Project Management route state:

```text
Project list / register
or
Project + Project section
```

Analysis navigation state:

```text
Current Project
+ Current Family
+ Current Navigation Stage
```

Analysis Context selection:

```text
Current Project       = URL project_id / read-only
Research Context      = Project-scoped selection
Dataset Version       = Project-scoped selection
Analysis View         = Dataset-Version-compatible selection
```

- Current FamilyおよびCurrent Navigation StageはURL / application navigation stateをauthorityとする。
- Current Projectはcanonical Analysis routeの`project_id`をauthorityとする。
- Research Context / Dataset Version / Analysis ViewはCurrent Projectと整合する値だけを復元する。
- Dataset Version変更でAnalysis Viewが互換でなくなった場合はAnalysis View selectionを解除する。
- contextがunselectedであっても、それだけを理由にFamily / Stage routeを書き換えない。
- 必要inputが不足するoperationはexecution unavailableとして表現する。
- Navigation stateをAnalysisSpecification、ExecutionPlan、ExecutionまたはStageExecutionへ保存しない。
- Navigation Stageの状態をExecutionまたはStageExecutionのruntime statusへ読み替えない。
