# 22_02_web_operation

**Status:** `RD02_STRUCTURAL_WORKING_COPY / E11_NOT_PUBLISHED`. Original chapter and source provenance retained; DD physical coverage remains partial.  
**Source blob:** `87196f2f03a7f3367724bc05fb254d1a4d98109e`.

---

## 6. Web App情報設計と操作・状態境界

### 6.1. 共通操作表示

| 表示 | 意味 | Backend contractとの関係 |
| --- | --- | --- |
| `enabled` | 現在のResource/state/permissionで操作可能 | Backendでも同じ前提を満たす |
| `disabled` | 操作不可 | 理由を表示し、Backend拒否理由と矛盾させない |
| `read-only` | 参照可能だが更新不可 | canonical Resourceは変更しない |
| `hidden` | Actor / surface context上不要 | state制約や権限制御の代替にしない |

Frontend presentation stateは`IDLE / LOADING / READY / EMPTY / PARTIAL / ERROR / CANCELLED`を区別する。APIがstate inconsistencyやoperation unavailableを返した場合、単なる通信失敗ではなく対象状態と可能な次操作を表示する。

### 6.2. Project List / Project Register

#### 6.2.1. 目的と境界

Project ListはProjectの一覧・選択およびProject Registerへの入口を担う。Project RegisterはProject新規作成だけを担い、既存Project metadata編集やarchiveを所有しない。

#### 6.2.2. 主要操作・状態対応

| 操作 | 前提状態 | 読取 | 生成 | 更新 | 操作後 | UI挙動 |
| --- | --- | --- | --- | --- | --- | --- |
| Project一覧表示 | Project read permission | Project一覧 | なし | なし | 変更なし | loading / empty / readyを区別 |
| Project Registerへ移動 | create permission | なし | なし | なし | route=`/projects/new` | navigation enabled |
| Project登録 | create permission + valid input | なし | Project | なし | Project=`ACTIVE` | 成功後`/projects/{id}/overview`へ遷移 |
| Project選択 | Project read permission | Project | なし | なし | Current Project scope変更 | `/projects/{id}/overview`へ遷移 |

### 6.3. Selected Project / Overview

#### 6.3.1. 目的と境界

OverviewはProject identity、metadata、status、archiveを所有する。Dataset / Analysis View lifecycleをここへ混在させない。

#### 6.3.2. 主要操作・状態対応

| 操作 | 前提状態 | 読取 | 生成 | 更新 | 操作後 | UI挙動 |
| --- | --- | --- | --- | --- | --- | --- |
| Overview表示 | Project read permission | Project | なし | なし | 変更なし | ACTIVE/ARCHIVEDを明示 |
| Project metadata編集 | Project=`ACTIVE` + write permission | Project | なし | 許可metadata | `ACTIVE` | ARCHIVEDではread-only |
| Archive要求 | Project=`ACTIVE` + archive permission | Project | なし | なし | 未変更 | confirmationを表示 |
| Archive確定 | Project=`ACTIVE` + archive permission | Project | なし | `status` | `ARCHIVED` | write actionをread-only/disabled化し、既存Lineageは保持 |
| ARCHIVED Project write | Project=`ARCHIVED` | Project | なし | なし | `ARCHIVED` | disabled / read-only、理由表示 |

### 6.4. Selected Project / Research Context

#### 6.4.1. 目的と境界

Research ContextはResearch Context Versionの作成・改訂・固定・履歴確認を担う。Analysis Workspaceでは既存VersionをActive Research Contextとして選択・参照するが、lifecycle authorityを持たない。

#### 6.4.2. 主要操作・状態対応

| 操作 | 前提状態 | 読取 | 生成 | 更新 | 操作後 | UI挙動 |
| --- | --- | --- | --- | --- | --- | --- |
| Context一覧/履歴表示 | Project read permission | ResearchContextVersion群 | なし | なし | 変更なし | version/statusを表示 |
| Context新規作成 | Project=`ACTIVE` + write permission | Project | ResearchContextVersion | なし | `DRAFT` | 作成後DRAFT編集可能 |
| DRAFT編集 | Context=`DRAFT` + Project=`ACTIVE` | ResearchContextVersion | なし | DRAFT content | `DRAFT` | FIXEDでは編集不可 |
| Context固定 | Context=`DRAFT` + validation pass | ResearchContextVersion | なし | status/hash/fixed_at | `FIXED` | FIXED後はread-only |
| FIXED内容変更 | Context=`FIXED` | ResearchContextVersion | 新ResearchContextVersion | なし | 新Version=`DRAFT` | 既存FIXEDを上書きしない |
| Active Context選択 | same ProjectのContext | Context + WorkspaceSelection | なし | selection | selection更新 | Analysis Contextへ反映 |

### 6.5. Selected Project / Data

#### 6.5.1. 目的と境界

DataはDataset / Dataset Version / schema / preview / Analysis View lifecycleを所有する。Analysis ViewはFamily横断analysis inputであり、Analysis Workspaceはexisting Analysis Viewを選択・参照する。

#### 6.5.2. Dataset操作・状態対応

| 操作 | 前提状態 | 読取 | 生成 | 更新 | 操作後 | UI挙動 |
| --- | --- | --- | --- | --- | --- | --- |
| Dataset登録 | Project=`ACTIVE` + valid file/input | Project + file | DatasetVersion + source Artifact | なし | immutable Dataset Version | 登録後一覧更新 |
| Dataset Version一覧 | Project read permission | DatasetVersion群 | なし | なし | 変更なし | version/status/schema summary表示 |
| Dataset preview/schema表示 | DatasetVersion存在 | DatasetVersion + Artifact/schema | なし | なし | 変更なし | read-only |
| Dataset Version選択 | same ProjectのDatasetVersion | DatasetVersion + WorkspaceSelection | なし | selection | selection更新 | Analysis Contextへ反映 |
| Dataset Version切替 | same Project | DatasetVersion + current AnalysisView | なし | selection | 新Dataset selection | incompatible Analysis Viewならselection解除 |
| Dataset Version上書き | 任意 | 既存DatasetVersion | なし | なし | 変更なし | 操作を提供しない |

#### 6.5.3. Analysis View操作・状態対応

| 操作 | 前提状態 | 読取 | 生成 | 更新 | 操作後 | UI挙動 |
| --- | --- | --- | --- | --- | --- | --- |
| Analysis View新規作成 | Project=`ACTIVE` + DatasetVersion選択 | DatasetVersion | AnalysisView | なし | `DRAFT` | source DatasetVersionを固定 |
| Analysis View DRAFT編集 | AnalysisView=`DRAFT` | AnalysisView + Dataset schema | なし | view spec | `DRAFT` | invalid filter/columnは理由表示 |
| Analysis View固定 | AnalysisView=`DRAFT` + validation pass | AnalysisView | なし | status/hash/fixed_at | `FIXED` | FIXED後はread-only |
| FIXED内容変更 | AnalysisView=`FIXED` | AnalysisView | 新AnalysisView | なし | 新Version=`DRAFT` | 既存FIXEDを上書きしない |
| Analysis View選択 | selected DatasetVersionとcompatible | AnalysisView + WorkspaceSelection | なし | selection | selection更新 | Analysis Contextへ反映 |

### 6.6. Selected Project / Results / Lineage

#### 6.6.1. 目的と境界

Results / Lineageはpersisted cross-analysis evidenceをProject scopeで閲覧・比較・追跡する。Stage-local execution controlそのものはAnalysis Workspaceに残す。

#### 6.6.2. 主要操作・状態対応

| 操作 | 前提状態 | 読取 | 生成 | 更新 | 操作後 | UI挙動 |
| --- | --- | --- | --- | --- | --- | --- |
| Result一覧表示 | Project read permission | Result / Execution summary | なし | なし | 変更なし | technical/scientific statusを分離表示 |
| Result詳細表示 | Result存在 | Result + Execution + Artifact refs | なし | なし | 変更なし | Artifact欠損はResult failureと混同しない |
| Result比較 | comparison compatibilityを満たす候補 | Result群 | なし | なし | 変更なし | 非互換ならmetadata比較または理由表示 |
| Lineage表示 | canonical refs/Lineage存在 | Result / Execution / Dataset / Graph / Artifact等 | なし | なし | 変更なし | provenance chainを表示 |
| Annotation作成/更新 | Project=`ACTIVE` + write permission + valid target | target Resource | Annotation | Annotation content | Projectに追従 | ARCHIVEDではread-only |

### 6.7. Analysis Workspace / Analysis Context

#### 6.7.1. 目的と境界

Analysis ContextはCurrent Project / Active Research Context / Dataset Version / Analysis Viewを、現在のanalysis inputとして明示する。専用Domain Resourceを生成しない。

#### 6.7.2. 主要操作・状態対応

| 操作 | 前提状態 | 読取 | 生成 | 更新 | 操作後 | UI挙動 |
| --- | --- | --- | --- | --- | --- | --- |
| Workspace表示 | valid project route | Project + selections/resources | なし | なし | Current Project確定 | Current Projectはread-only |
| Active Research Context選択 | same Project | ResearchContextVersion | なし | WorkspaceSelection | selection更新 | context表示更新 |
| Dataset Version選択 | same Project | DatasetVersion | なし | WorkspaceSelection | selection更新 | incompatible Analysis Viewをclear |
| Analysis View選択 | same Project + selected DatasetVersion compatible | AnalysisView | なし | WorkspaceSelection | selection更新 | incompatible viewは選択不可 |
| context不足 | required input不足 | current context | なし | なし | 不足状態維持 | 架空defaultを生成せずoperation unavailableを表示 |

### 6.8. Analysis Workspace / Family・Stage・Operation

| 操作 | 前提状態 | 読取 | 生成/更新 | 操作後 | UI Gate / navigation behavior |
| --- | --- | --- | --- | --- | --- |
| Family切替 | valid Family catalog | navigation catalog | route更新 | selected Family + default Stage | catalog `default_stage_id`へ遷移 |
| Stage切替 | selected Family内のvalid Stage | navigation catalog | route更新 | selected Stage | Stage順をruntime progressionとして強制しない |
| Stage Contents表示 | valid Family/Stage binding | context + relevant Resource | なし | presentation state | binding欠落はunsupported/error |
| operation実行 | backend operation availability + required context/resource | context/spec/input | Execution等 | async lifecycle開始 | unavailable reasonを表示 |
| resource deep link | route/resource semantic整合 | Resource | route state | resource context表示 | semantic矛盾はsilent correctionしない |
| context不足でStage閲覧 | valid Family/Stage route | current context | なし | route維持 | routeを書き換えず必要operationだけdisabled/unavailable |

### 6.9. Stage固有の重要な状態境界

- Exploratory / Data Qualityはdedicated operationを持たない。existing `PROFILE` resultがあればread-only表示し、なければ`NO_PROFILE_RESULT`とProfileへの導線を表示する。新Execution/Resourceを生成しない。
- Exploratory / TIME_TRENDはexisting grouping/aggregation semanticsを維持し、presentation配置だけを理由に新しいtime-series Domain modelを導入しない。
- Exploratory / Findingsの`CHART`はexisting persistent operation semanticsを維持する。
- CausalのDiscovery Result、DRAFT Graph Version、FIXED Graph Versionは同一編集可否として扱わない。FIXED Resourceを直接更新しない。
- Causalのscientific Gateが不成立の場合、Execution technical failureへ読み替えない。
- PredictiveのNavigation Stage切替を理由にdraft analytical inputを不必要に破棄しない。

### 6.10. Loading / Error / Accessibility

- navigation metadata loadingを明示する。
- unknown Family / Stageをsilent fallbackしない。
- renderer binding欠落はunsupported stateとして検出する。
- current main surfacesはkeyboard操作、deterministic focus、accessible name、error association、non-color semanticsを満たす。
- normal text contrastは4.5:1以上、large text / UI graphics / focus indicatorは3:1以上をtargetとする。
- small viewportでもProject scope / Family dimension / Stage dimensionを混同させない。
