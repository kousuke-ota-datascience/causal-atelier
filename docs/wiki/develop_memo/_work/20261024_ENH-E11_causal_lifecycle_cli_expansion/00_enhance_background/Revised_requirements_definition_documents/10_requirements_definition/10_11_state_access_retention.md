<!-- ENH-E11 split working copy: not a formal approval. -->
# 10 — state access retention

**Status:** `STRUCTURAL_COPY_DRAFT` (existing baseline text, not E11 canonical publication)

**Source:** [10_requirements_definition.md](https://github.com/kousuke-ota-datascience/causal-atelier/blob/3ba5fe2465ec591f0da7f998c21a5241984b73dc/docs/wiki/requirement_definition/10_requirements_definition.md) · blob `40b83f29c67b4a39f6db5393be7534c5e892d656`  
**Index:** [Revised document inventory](../README_00_Revised_requirements_definition_documents.md)

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

## 9. 権限要件

Project-scoped Resourceおよび操作の認可は、§7.1で定義するpersisted Project role `OWNER / EDITOR / VIEWER`をauthorityとする。

* Project-scoped Resourceへアクセスするには、対象Projectに対するmembershipと必要なProject権限を持たなければならない。
* `OWNER / EDITOR / VIEWER`はProjectをreadできる。
* Context、Analysis View、Analysis Specification、Annotationその他のProject ResourceのWRITE / MUTATEは`OWNER / EDITOR`のみ許可する。
* Executionのsubmit / cancel / retry / rerun / reviseは`OWNER / EDITOR`のみ許可する。
* Exportの作成は`OWNER / EDITOR`のみ許可する。
* Project membershipの管理は`OWNER`のみ許可する。
* prediction row / local explanation等のexplicit sensitive outputは`OWNER / EDITOR`のみ取得可能とし、`VIEWER`には返さない。
* 独立した`EXECUTE` Project roleは設けない。
* 認可失敗時は、権限を持たない利用者がResourceの存在を推測できない応答を選択できる。
* system-level Operator authorizationはcurrent Project authorization contractには含めず、`DEFERRED / FUTURE`として扱う。

## 10. データ保持要件とDeferred Audit / Retention Boundary

Current contractで有効なcurrent data-retention contractは次のとおりとする。

* Dataset Version、Result、Artifact metadataおよびExecution snapshotはappend-onlyを基本とする。
* Projectをarchiveしても、Projectに属する既存の分析Resourceをarchive操作だけを理由として物理削除しない。
* Annotationについて、current contractで保持されている変更履歴を維持する。

以下はRequirementとして維持するが、current delivery対象には含めない。

* general operational audit trail (`FR-122`): `DEFERRED / FUTURE`
* configurable retention/deletion policy (`FR-126`): `DEFERRED / FUTURE`

したがってCurrent contractでは、general Audit recordの共通field contract、configurable retention期間、Artifactの一般的な物理削除policyおよび削除audit contractを必須acceptanceとして要求しない。
