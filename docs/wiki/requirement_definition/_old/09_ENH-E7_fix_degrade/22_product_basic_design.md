# 22 プロダクト基本設計

- 文書状態: `APPROVED`
- 文書種別: 現行プロダクト基本設計のeffective snapshot
- 上位文書: `00_product_concept_memo.md`, `10_requirements_definition.md`, `21_logical_data_design.md`
- 下位文書: `23_api_interface_design.md`, `30_detailed_design.md`

> 基本設計は画面項目の一覧ではない。利用者の操作、前提状態、正本Resourceへの論理的効果、状態遷移、画面間のcontext引渡し、およびUI Gateを、実装詳細へ踏み込みすぎない粒度で定義する。

## 1. 文書の設計粒度

### 1.1. 本書で確定する事項

本書は、AriadneのProduct Architectureと、利用者操作が正本Resource / stateへ与える論理的効果を基本設計として確定する。最低限、次を本書の責務とする。

- 利用者向けsurface / workspace / page / sectionの責務と境界
- page / sectionの目的
- 利用者が実行できる主要操作
- 操作の前提となるResource / state / permission / operation availability
- 操作時に読み取る正本Resource / logical state
- 新規生成するResource
- 更新するResourceと更新可能な意味内容
- 操作後のResource / state
- UIの`enabled / disabled / read-only / hidden`
- 操作拒否時に利用者へ示す理由
- surface / page / stage間で引き渡すlogical context
- direct link / reload / Back / Forward時の復元責務
- Product Domain / Application / Worker / Scientific Core / CLIの責務境界

特に、Family / Navigation Stageのようなpresentation taxonomyを導入・変更しても、runtime execution lifecycleをpresentation taxonomyへ従属させない。

### 1.2. 下位文書へ委譲する事項

次は本書で意味上のcontractだけを定義し、物理詳細は下位文書へ委譲する。

- DTO / request / response classの正確なfield構成
- Endpointの正確なpath・HTTP method・serialization。ただしbrowser route authorityは本書で定義する
- JSON Schema / OpenAPIの物理表現
- package / module / class / repositoryの物理構成
- transaction boundary、lock、例外補償の実装詳細
- ORM mapping、DDL、indexの物理実装
- DOM構造、CSS値、描画library、component class名
- scientific algorithmの数式・実装手順

### 1.3. 上位・下位文書との責務分離

- Product concept、Top-level IAの概念的意味は`00_product_concept_memo.md`をauthorityとする。
- Product requirement / NFR / analytical requirementは`10_requirements_definition.md`をauthorityとする。
- Resource、Entity、Value、state model、整合性制約は`21_logical_data_design.md`をauthorityとする。
- API / browser / internal interfaceの具体contractは`23_api_interface_design.md`へ詳細化する。
- module / component / state transition / algorithmic orchestrationは`30_detailed_design.md`へ詳細化する。

本書はこれらの中間に位置し、**要件をsurface・操作・状態・責務・主要flowへ割り付ける**。

## 2. システム境界

### 2.1. 対象コンポーネント

| コンポーネント | 主な責務 | 本書での境界 |
| --- | --- | --- |
| Web Frontend | Project Management、Analysis Workspace、入力支援、状態表示、操作要求、結果表示、比較、Lineage | browser route / surface responsibility / UI Gateを保持し、Domain invariantを独自実装しない |
| Versioned Web API | 認可、validation、Resource操作、状態Gate、Query Projection、navigation metadata | Frontendの操作可否と同じDomain/Application ruleを強制する |
| Product Domain | Resource、Value、state、invariant | Web Framework、ORM、browser route、plot/ML libraryへ依存しない |
| Application / Query Services | use case、transaction coordination、planner/executor control、Query Projection、navigation coordination | Domain invariantを利用し、presentation taxonomyとruntimeを混同しない |
| Execution Worker | 非同期scientific execution、Result / Artifact保存、Execution状態遷移 | request lifecycleから長時間科学計算を分離する |
| Metadata DB | `21_logical_data_design.md`で定義するcanonical Domain Resource / stateの永続化 | Query/presentation-only stateを無目的に正本化しない |
| Artifact Store | Dataset source / execution output / export等の物理保存 | Artifact metadataとの整合を保持する |
| Scientific Core | Exploratory / Causal / Predictiveのscientific computation | browser route、Family tab、Navigation Stageをrequired inputとしない |
| Local CLI | Scientific Coreの独立headless interface | Web固有のProject Management / browser navigationを要求しない |

### 2.2. 正本Resourceと非正本概念

正本Resource / Entityの完全な定義は`21_logical_data_design.md`をauthorityとする。本書では次の境界だけを固定する。

- Project、Research Context、Dataset Version、Analysis View、Analysis Specification、Execution Plan、Execution、StageExecution、Result、Artifact、Graph Version、Annotation、Lineage等の再現性・来歴に関与する情報はcanonical Resourceとして扱う。
- Analysis Contextは専用persistent aggregateではなく、Current ProjectとProject-scoped selection/resourceから構成するlogical projectionである。
- Analysis Family、Navigation Stage、route representation、renderer binding、Graph Candidate、Comparison等は、それ自体を理由なくcanonical Domain Resourceへ昇格させない。
- UI表示用status、modal state、loading state等を新しいDomain Resourceへ複製しない。

### 2.3. Product ManagementとAnalysisの境界

- Project ManagementはProject resourceとversioned analysis inputのlifecycle ownerである。
- Analysis WorkspaceはProject Managementで管理されたResourceをanalysis input/contextとして利用し、analysis execution / presentationを担う。
- Current Projectの変更はProject Managementをauthorityとし、Analysis Workspace内部に独立したProject switch authorityを持たせない。
- persisted cross-analysis evidenceはProject Management / Results / Lineage、execution-local / stage-local presentationはAnalysis Workspaceが担う。

## 3. システム構成

```text
Analyst / Reviewer / Operator
            │
            ▼
        Web Frontend / CLI
            │
            ▼
        Versioned Web API
            │
   ┌────────┼───────────────┐
   ▼        ▼               ▼
Product   Query          Workflow
Domain    Services       Application
   │        │               │
   └────────┼───────────────┘
            ▼
Metadata DB / Artifact Store
            │
            ▼
     Execution Worker
            │
   ┌────────┼─────────────┐
   ▼        ▼             ▼
Explore   Causal       Predictive
Runners   Runners       Runners
            │
            ▼
      Scientific Core
```

Web APIとWorkerは同一codebaseを共有できるが、同期request処理と長時間scientific computationの責務を分離する。

現行scientific CLIはWeb/API Resource lifecycleの薄い別表現ではなく、local configを入力としてdomain validationと`ScientificCoreAdapter`を直接呼び出すheadless interfaceである。少なくとも`ariadne-discover`はWeb/APIのExecution IDを作成せず、`ariadne-identify` / `ariadne-refute` / `ariadne-sensitivity`もlocal scientific stageとして実行される。CLIへbrowser route、Current Family、Navigation Stageをrequired inputとして導入しない。

## 4. 横断設計原則

### 4.1. Layer boundary

- Domain: Resource、state、invariant、value object
- Application: use case、transaction、policy、planner、executor control、navigation coordination
- Port: repositories、artifact_store、clock、scientific_core、unit_of_work
- Adapter: SQL、Filesystem、Scientific library、ML library
- Object Storage adapterは`NFR-020b = DEFERRED / NOT_IMPLEMENTED / FUTURE`であり、current implementationの必須構成には含めない。
- Interface: Web API、Worker、CLI、Frontend

DomainはWeb Framework、ORM、plot library、ML library、browser routeおよびlegacy moduleへ依存しない。Object Storage adapterはcurrent implementationの必須境界ではない。

### 4.2. Capability分離

```text
Shared Product Core
├── Project / Context
├── Data / Analysis View
├── Workflow Core
├── Result / Artifact / Lineage
└── Security / Project Authorization

Analysis Capabilities
├── Exploratory
├── Causal
└── Predictive
```

各CapabilityはFamily Specification Schema、Planner、Stage Runner、Family Validation、Result Schema、analytical surface/binding、Navigation Stage catalog、Acceptance Testを所有する。Generic Product/Application codeは個別FamilyのStage literalや分析意味論を集中所有しない。

### 4.3. Family / Navigation Stage / Execution Stageを分離する

- `AnalysisFamily`: analytical capability discriminator
- `Navigation Stage`: Family内のuser work/view context
- `Execution Stage`: runtime plan/lifecycle上の処理単位

`Navigation Stage != Execution Stage`をinvariantとする。Navigation Stageの追加・名称変更・並び替えだけを理由にExecution Plan、Stage dependency、retry、attempt、statusを変更しない。

### 4.4. 正本とQuery / Presentation Modelを分離する

- Comparisonは必要に応じてcanonical Result等から導出する。
- Lineageはcanonical references / `LineageEdge`等から導出・構成する。
- Graph CandidateはResult / Graph Version等のcanonical resourceから投影する。
- UI表示用stateをcanonical Resourceへ複製しない。

### 4.5. 不変Versionを上書きしない

- Dataset Versionは不変snapshotとして扱う。
- FIXED済みResearch Context / Analysis View / Analysis Specification / Graph Versionは意味内容を上書きしない。
- submitted execution input / planの再現性を破壊する更新を行わない。
- 条件変更は新Version / 新Execution / 新Resultとして表現する。

### 4.6. 技術状態と科学状態を分離する

`Execution.status = SUCCEEDED`とscientific negative resultは両立する。Frontendは文字列`FAIL`等だけでtechnical failureとscientific findingを混同しない。

### 4.7. Project archiveはLineageを破壊しない

Project利用停止は`ACTIVE -> ARCHIVED`で表現する。`ARCHIVED`はread-onlyとし、既存Resource / Result / Artifact / Lineageを保持する。hard deleteを通常の利用者操作として提供しない。

### 4.8. 操作・状態境界をBackendでも強制する

buttonをdisabledにするだけでは要件を満たさない。Domain / Application Service / APIは同一の前提状態・整合性・permissionを検証する。FrontendはBackendからの拒否を単なる通信失敗として扱わず、可能な範囲で理由と必要操作を表示する。

### 4.9. Provenance / Contextを一貫して継承する

Dataset Version、Research Context、Analysis View、Analysis Specification、Graph Version、upstream Result等、analysis inputとprovenanceをExecution / Result / Lineageまで追跡可能にする。presentationの都合でprovenance linkを切断しない。

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

## 9. Generic Workflow Core

### 9.1 Planner

`PlannerRegistry`はAnalysis FamilyとSpecification Schema VersionからPlannerを解決する。

```text
AnalysisSpecification
  ↓
PlannerRegistry.resolve(family, schema_version)
  ↓
Family Planner
  ↓
ExecutionPlan
```

PlannerはDomain上のruntime planを生成し、browser navigation stateを入力として要求しない。

### 9.2 Plan

Execution Planはruntime Stage DAGである。

- Stage keyはPlan内一意。
- Stage Typeはruntime operation identityを表す。
- Edgeはoutput / input bindingを表す。
- cycle禁止。
- required input未解決禁止。
- Runner未登録禁止。

Navigation Stageのsidebar orderをExecution Plan dependencyへ変換しない。

### 9.3 Executor

Generic Executorはcanonical lifecycle/application serviceが所有するworkflow execution context内で、Analysis内容を知らずにruntime Stageを実行する。

1. dependency解決
2. runtime Stage sequencing
3. Runner解決・invocation
4. workflow-level validation
5. temporary output binding

canonical Execution lifecycleはNavigation改修の対象外とし、current contractを維持する。基本設計上の境界は次のとおり。

- Execution technical statusは`QUEUED / RUNNING / SUCCEEDED / FAILED / CANCELLED`で管理する。
- Worker ownershipは`Execution.lease_owner / lease_expires_at`とrepository-level claim / renew / completeで管理し、Navigation stateをclaim条件へ追加しない。
- retry/rerun/reviseはcanonical Execution / revision semanticsとして扱い、Navigation Stage遷移へ変換しない。
- runtime Stageの進行は`StageExecution`とappend-only `StageAttempt`で表現する。
- Result / Artifactはcanonical Execution / StageExecution ownershipから生成・永続化し、browser routeやCurrent Navigation Stageをpersistent ownership fieldへ追加しない。
- transaction境界とpersistent lifecycle authorityはproduct application / persistence側に残し、Navigation componentへ移さない。

### 9.4 Runner Registry

runtime Runner Registryは`StageType`によりrunnerを解決する。

Navigation Stage IDを`StageType`として登録しない。巨大な`if navigation_stage == ...`をExecutorへ追加しない。

### 9.5 Navigation Stageとの境界

次を禁止する。

- `NavigationStageDescriptor`を`StageDefinition` / `StageExecution`のsubtypeにする。
- Navigation Stage IDをruntime `StageType`へ流用する。
- `AnalysisSpecification.navigation_stage`をexecution prerequisiteとして追加する。
- runtime moduleからbrowser route / Navigation Stage moduleへ依存する。

#### 9.5.1 Distribution

`Exploratory / Distribution`がDataset/profile/resultのreadだけで成立する場合、対応するruntime Execution Stageを作らない。

#### 9.5.2 Metrics

`Predictive / Metrics`は既存evaluation Resultを読むだけで成立してよい。Navigation taxonomyを理由に`METRICS` runtime Stageを新設しない。

#### 9.5.3 Explainability

1 Navigation Stageから複数read/compute use caseを呼び出してよい。Navigation StageとExecution Stageのcardinalityを1:1へ固定しない。

### 9.6 CLI / Library independence

CLI / Python library / backend use caseは、Analysis Specificationまたは既存use-case inputだけでexecutionを開始できる。

`Current Navigation Stage`、browser route、sidebar stateをrequired inputへ追加しない。


## 10. Family別Workflow / Capability

この章で扱う`Workflow`はruntime execution semanticsであり、5章のNavigation Stage一覧とは別概念である。

### 10.1 Exploratory

現行実装の`ExploratoryPlanner`は、`exploratory-analysis-spec/1`のoperationを次のruntime Stageへ写像し、**1 Execution Planにつき1 runtime Stage**を生成する。

| family_spec.operation | runtime stage_key | StageType |
| --- | --- | --- |
| `PROFILE` | `profile` | `exploratory.profile.v1` |
| `DISTRIBUTION` | `distribution` | `exploratory.distribution.v1` |
| `ASSOCIATION` | `association` | `exploratory.association.v1` |
| `GROUP_SUMMARY` | `aggregate` | `exploratory.aggregate.v1` |
| `TIME_TREND` | `time_trend` | `exploratory.time_trend.v1` |
| `CHART` | `chart` | `exploratory.chart.v1` |

Navigation Stage:

```text
Profile / Data Quality / Distribution / Relationships / Comparison / Findings
```

は上記runtime operationと同一taxonomyではない。例えば`Data Quality`や`Findings`に同名runtime Stageは存在しなくてよく、保存済みDataset/Result/Annotation/Artifactのreadで成立してよい。Navigation Stageを開いたことだけを理由にpersistent Executionを作らない。

### 10.2 Causal

現行実装の`CausalPlanner`は`causal-analysis-spec/2`向けcompatibility plannerである。canonical `Execution.operation`を次のruntime StageTypeへ写像し、**1 canonical Executionにつき1 runtime StageからなるExecution Plan**を生成する。

| ExecutionOperation | StageType |
| --- | --- |
| `DISCOVERY` | `causal.discovery.v1` |
| `IDENTIFICATION` | `causal.identification.v1` |
| `ESTIMATION` | `causal.estimation.v2` |
| `REFUTATION` | `causal.refutation.v1` |
| `SENSITIVITY` | `causal.sensitivity.v1` |

したがって、現行実装のruntimeを次のような単一Plan内のDAGとして扱わない。

```text
IDENTIFICATION -> ELIGIBILITY -> ESTIMATION -> ...
```

`IDENTIFICATION`処理から`DATA_ELIGIBILITY_RESULT`等が生成され得ることと、`ELIGIBILITY`というruntime Stageが存在することは別である。科学的な前提関係はcanonical Executionの`input_graph_version_id` / `input_result_id`等とResult lineageで表現される。

Navigation側の`Setup / Discovery / Identification / Estimation / Effects / Diagnostics / Sensitivity`はユーザーの作業・閲覧コンテキストであり、runtime StageTypeと1:1対応させない。Identification / Estimationの科学的責務分離はNavigation設計として維持するが、それを理由に既存Causal runtime planを多段化しない。

### 10.3 Predictive

現行実装のfull Predictive planは次のruntime Stageを生成する。

```text
SPLIT -> PREPARE -> TRAIN -> EVALUATE -> optional EXPLAIN
```

主なdependencyは次である。

- `split.partition_manifest -> prepare.partition_manifest`
- `prepare.training_bundle / fitted_preprocessor -> train`
- `prepare.evaluation_bundle / fitted_preprocessor`および`train.frozen_model -> evaluate`
- Explainが有効な場合はprepare/train/evaluateの必要outputをExplainへbindingする。

各runtime Stageの責務:

- SPLIT: immutable partition artifactを生成する。
- PREPARE: partition manifestを用いてtraining/evaluation bundle、fitted preprocessor、explanation向け入力を生成する。
- TRAIN: training bundleとfitted preprocessorからfrozen modelとtraining summaryを生成する。
- EVALUATE: frozen modelとevaluation bundleを用いてevaluation summaryを生成する。
- EXPLAIN: 有効なexplanation specificationに従ってexplanation summary / model card等を生成する。

Navigation側の`Setup / Train / Predict / Metrics / Explainability / Model Management`は、これらruntime stageと1:1対応させない。特にNavigation `Train`はruntime `train`単体実行を意味せず、`Metrics`は保存済みevaluation Resultのreadで成立し得る。

Predictiveの既存設定項目、default、validation、generated `predictive-analysis-spec/1` semanticsは全量保持する。

#### 10.3.1 Predictive subgroup evaluation

- evaluation populationはuntouched TEST。
- user-specified subgroup columnごとに独立sliceし、automatic intersection/discovery/fairness frameworkは追加しない。
- subgroup columnはfeatureである必要はなく、partition row identity/ordinalによりTEST rowへ対応付ける。
- nullはexplicit subgroupとして扱う。
- primary/secondary metricそれぞれに`sample_count`を必須で返す。
- uncertaintyはnonparametric percentile bootstrap、confidence=0.95、resamples=1000、deterministic seed。
- `n < 2`またはvalid resamples < 200ではCIを返さずwarningを返す。
- metricが計算不能なgroupではvalue/uncertaintyを`null`とし値を捏造しない。
- outputはgroup valueをmap keyに埋め込まずrecord listとする。


## 11. Validation Architecture

### 11.1 Generic Validation

Validation責務は、現行実装の`PlanValidator`が直接行う検証と、それ以外のapplication/domain validationを分離する。

#### 11.1.1 PlanValidatorが行う検証

`PlanValidator`は現在、次を検証する。

1. `plan_schema_version == execution-plan/1`。
2. `project_id`と`analysis_specification_id`が空でない。
3. `stage_key`が一意で、Planに少なくとも1 Stageが存在する。
4. enabled Stageの`StageType`にRunnerが登録済みである。
5. `resource_policy.timeout_seconds`が指定される場合、整数かつ1..86400以内である。
6. dependencyのsource/target Stageが存在する。
7. enabled Stageがdisabled Stageへ依存しない。
8. dependencyが参照するsource output / target input名が各contractに存在する。
9. source output schemaとtarget input schemaが一致する。
10. 同じtarget Stage inputへ複数upstream bindingを作らない。
11. topological sortが成立し、cycleがない。

`StageType.namespace/name/version`のsyntax validationは`StageType`生成時のdomain invariantであり、PlanValidatorの独立stepとして重複実装しない。

#### 11.1.2 PlanValidator外のvalidation

次は別のdomain/application boundaryで扱う。

- Project / Resource boundary・ownership
- Analysis Specification schema/lifecycle validation
- Family固有scientific validation
- supported endpointにおけるidempotency
- Dataset/Artifact size等、個別use caseのresource policy
- Navigation catalogのFamily/Stage ID、slug、order、default Stage、renderer binding整合性

Navigation catalog validationをruntime Plan dependency validationへ混入しない。

#### 11.1.3 AnalysisView typed filter validation

AnalysisView create/update/validate/fixは同じDataset logical-type compatibility validatorを利用する。

| Logical Type | Operator |
| --- | --- |
| BOOLEAN | `EQ, NE, IN, NOT_IN, IS_NULL, NOT_NULL` |
| INTEGER / REAL / DATETIME | `EQ, NE, LT, LTE, GT, GTE, IN, NOT_IN, IS_NULL, NOT_NULL` |
| TEXT | `EQ, NE, IN, NOT_IN, IS_NULL, NOT_NULL` |
| OTHER | `IS_NULL, NOT_NULL` |

`IS_NULL/NOT_NULL`はvalueなし、`IN/NOT_IN`はnon-empty list。DATETIME valueはISO-8601、REALはfinite numeric、INTEGERはbooleanを許容しない。`time_cutoff`はDATETIME + `LT/LTE`。logical type unknownをsuccess扱いしない。Mismatch codeは`FILTER_TYPE_MISMATCH`。

### 11.2 Exploratory Validation

- column typeとchart encoding
- aggregation compatibility
- empty population
- sampling disclosure
- exploratory findingをcausal claimへ変換しない

### 11.3 Causal Validation

- Graph semantics
- Causal Question completeness
- identification strategy
- adjustment set
- inferred type
- eligibility
- estimator compatibility
- post-discovery warning

### 11.4 Predictive Validation

- target existence / type
- feature availability
- target / future / group leakage
- split overlap
- preprocessing fit boundary
- metric / task compatibility
- test isolation
- existing setting/spec parity

### 11.5 Navigation Validation

- supported Familyのみ。
- Stage ID / slugはFamily内一意。
- default Stageはcatalog内に存在する。
- Family / Stage orderingはdeterministic。
- renderer binding欠落を検出する。
- Navigation descriptorにruntime input/output、status、retry semanticsを持たせない。


## 12. Result / Artifact / Lineage

### 12.1 Canonical Resultとcompatibility read model

現行のcanonical `Result` authorityは、`execution_id / result_level / stage_execution_id / result_type / scientific_status / summary / payload / diagnostics / warnings`を持つ。ProjectとAnalysis Familyは親Executionから解決する。

同時に、過去のFamily workflowを読むための`FamilyResult` compatibility read modelが残っており、こちらは`project_id / analysis_family / schema_version / analytical_status`を持つ。新規write authorityはcanonical Resultに寄せ、両者を同一entityとして扱わない。

Navigation StageをResult ownership keyとして必須化しない。

### 12.2 Artifact

Canonical Artifactは`SOURCE`または`EXECUTION_OUTPUT` scopeを持ち、`object_key / content_hash / media_type / size_bytes`でArtifactStore上のcontentを参照する。Artifact readでは保存済み`content_hash`と取得contentのSHA-256を照合する。

Predictive等のhistorical Family read modelとして`FamilyArtifact`が残るが、新規canonical Artifact ownershipと区別する。

### 12.3 Lineage

Lineageには2つの表現層がある。

1. canonical/generic authority: `LineageEdge(ResourceRef -> ResourceRef)`およびtyped structural relation。
2. Result起点read projection: Project / Dataset / Execution / Result / GraphVersion / Artifact / Annotationをtraverseし、表示用relation名へ変換する。

表示用`CONTEXT_FOR / SOURCE_OF / INPUT_TO / HAS_ARTIFACT / HAS_ANNOTATION`等と、generic authoritative relation typeを同一のwrite contractにしない。

Navigation Stageをpersistent lineage resourceとして追加しない。

Current lineage read modelは`ResearchContextVersion -> AnalysisSpecification -> ExecutionPlan -> Execution -> StageExecution -> Result -> Artifact`を最低chainとし、DatasetVersion / AnalysisView / GraphVersion / input Result / base Executionを接続する。FK/snapshotからdeterministically導出できるstructural relationをgeneric LineageEdgeへ二重persistせず、`MOTIVATED`等のsemantic relationだけをgeneric edgeとして保持する。

Exploratory ResultからAnalysisSpecification DRAFTへのhandoffは`Result --MOTIVATED--> AnalysisSpecification`を明示保存する。


## 13. Comparison Design

### 13.1 Canonical comparison query

現行`ComparisonQueryService`は2件以上のcanonical Resultを比較し、以下を要求する。

- 全Resultが同一Projectに属する。
- 全Resultの親Executionが同一`operation`である。
- 全Resultが同一`result_type`である。

比較projectionは次を返す。

- `operation`
- `common_conditions`
- `changed_conditions`
- `result_differences`
- `warnings`
- `lineage_summary`

Execution snapshot差分として、少なくとも`algorithm_or_estimator / parameter_json / random_seed / analysis_spec_json / dataset_version_id / input_graph_version_id`を比較する。

### 13.1.1 Scientific comparability gate

Comparisonは二段階で評価する。

1. `semantic_compatible`
2. `direct_metric_comparable`

Predictive semantic key:

```text
task_type
prediction target/outcome
prediction unit
prediction time
horizon
deployment/evaluation population semantics
```

Model/feature/hyperparameter/split method差分は比較対象だがsemantic keyそのものではない。Direct metric comparisonではさらに`same dataset_version_id / same TEST-row identity(hash) / same metric definition`を要求する。

Causal semantic keyは`treatment/exposure / outcome / estimand / target population`。Direct comparisonではsame data/view/analysis populationも要求する。

同一immutable `dataset_version_id`をExploratoryとconfirmatory analysisで再利用した場合はAnalysisViewが異なってもsame-dataと判定し、`EXPLORATORY_REUSE_SAME_DATA`をnon-blocking warningとして先行Exploratory Result IDとともに保持する。

semantic mismatchはHTTP-level failureにせず`compatible=false`とreasonを返し、quantitative delta/rankを生成しない。Different Family / incompatible Result Typeなどrequest shape自体が無効な場合はvalidation errorとする。

### 13.2 Project-scoped comparison

Project Closure APIにも`POST /projects/{project_id}/comparisons`が存在する。これはProject membership境界を通った比較surfaceであり、canonical Result比較の意味を変えない。

### 13.3 Cross-family summaryの将来境界

現行canonical comparisonはsame operation / same Result Typeを要求するため、異なるFamily semanticを直接同一comparisonへ入れる設計ではない。

将来Cross-family summaryを行う場合も、Predictive metricとCausal effectを単一scoreへ平坦化せず、Research Context / Dataset / Analysis View / evidence relation等を用いたpresentation summaryとして設計する。


## 14. Frontend State Design

Frontend stateは次の責務へ分離する。

- server state: API query cache
- Project route state: Project list/registerまたはProject / Project section
- Analysis route state: Project / Family / Navigation Stage / optional resource identity
- Analysis Context selection: Research Context / Dataset Version / Analysis View
- draft state: unsaved form
- authoritative resource state: backend Resource status
- async presentation state: `IDLE / LOADING / READY / EMPTY / PARTIAL / ERROR / CANCELLED`

Authority rule:

1. Analysis WorkspaceのCurrent ProjectはURL `project_id`をauthorityとしread-only。
2. Current Family / Navigation Stageはcanonical Analysis route / application navigation stateをauthorityとする。
3. Research Context / Dataset Version / Analysis Viewはcurrent Projectと整合するexisting resource/stateだけを復元する。
4. Dataset Version変更でAnalysis Viewが互換でなくなればAnalysis View selectionを解除する。
5. context selection不足だけを理由にFamily / Stage routeを書き換えない。
6. Family / Navigation StageをDB/workspace persistent stateへ昇格させない。
7. Predictive等のdraft inputをStage切替で不必要に破棄しない。
8. Button enablementはclient local stateだけで決定せず、backend validation / operation availabilityを利用する。

Backend action availabilityは最低限`{allowed, reason_code?, message?}`を返し、action visibilityとaction allowedを別conceptとして扱う。


## 15. Security Design

### 15.1 Current request identity

現行実装のWeb APIには共通Bearer/OIDC authentication middlewareは存在しない。request identityが必要なrouterでは`X-User-Id`を読み、未指定時は`anonymous`として扱う実装がある。

Request correlationは`X-Request-Id`をmiddlewareで受理し、未指定時はUUIDを生成してresponse headerへ返す。

したがってCurrent architectureでは、Navigation改修を理由に「production OIDCが既に成立している」と仮定しない。Authentication hardeningは別scopeである。

### 15.2 Project membership

Project Closure領域のProject roleは次の3値である。

- `OWNER`
- `EDITOR`
- `VIEWER`

`ProductClosureService`ではreadを`OWNER / EDITOR / VIEWER`、writeを`OWNER / EDITOR`へ許可する。Project作成時にはrequestの`X-User-Id`をownerとしてmembership登録する。

**全project-scoped route**はservice action前にProject membership authorizationを通す。routerごとの実装差異をauthorization bypassの理由にしてはならない。

Role/action matrix:

| Action | OWNER | EDITOR | VIEWER |
| --- | --- | --- | --- |
| READ | allow | allow | allow |
| WRITE / MUTATE | allow | allow | deny |
| Execution mutation | allow | allow | deny |
| Export create | allow | allow | deny |
| Membership admin | allow | deny | deny |
| Explicit sensitive output | allow | allow | deny |

独立`EXECUTE` roleは追加しない。system-level Operator authorizationは`DEFERRED` scopeである。

### 15.3 Artifact / sensitive output

Artifact downloadはcontent hashを検証して返す。Project-scoped closure downloadでは`Content-Disposition`、`Digest`、`X-Content-Type-Options: nosniff`、`Cache-Control: private, no-store`を付与する。

Prediction / local explanation等のsensitive output policyをNavigation Stage名称で緩和しない。

prediction row / local explanation row/detailはpotentially sensitive outputとして扱う。VIEWERにはaggregate/suppressed viewのみ許可し、explicit sensitive detailはOWNER/EDITORに限定する。configurable sensitive-column metadata/policyは`DEFERRED`でありcurrent mandatory designへ含めない。


### 15.4 Command Idempotency / Retry-safe Artifact Commit

Idempotency対象は「全POST/create」ではなく、retryでduplicate durable side effectを生成し得るCommandである。Scopeは`(project_id, command_scope, idempotency_key)`。

- required key missing: `IDEMPOTENCY_KEY_REQUIRED`
- same key + same canonical semantic request: stored response replay、duplicate side effectなし
- same key + different request: HTTP 409 `IDEMPOTENCY_CONFLICT`
- natural idempotency/uniquenessが成立するCommandへheaderを機械的に要求しない
- exactly-once executionは保証しない

Artifact materializationはlogical Execution/Stage/output slot/typeからdeterministic identity/object keyを導出し、same logical output + same content hashはreuse、different content hashはnondeterministic-output conflictとする。Result/Artifact bindingは可能な限りmetadata transaction内でcommitする。cross-store compensationは`DEFERRED` scopeである。



## 16. Deployment

現行実装ではFastAPI Web API、polling Worker、Product persistence DB、ArtifactStore Port（default LocalArtifactStore）が分離されている。Family / Navigation Stage導入のために別runtime execution serviceを新設しない。


## 17. Failure Model

| Failure | 扱い |
| --- | --- |
| Navigation descriptor invalid | startup/query validation error。runtime execution failureへ変換しない |
| Unknown Family / Stage route | explicit 4xx / unsupported state。silent fallbackしない |
| Renderer binding missing | presentation/configuration defectとして検出 |
| Validation rejection | Executionを作成せず4xxまたはREJECTED Command Result |
| Technical runtime stage failure | Stage FAILED、Execution FAILED、既存retry policy |
| Analytical prerequisite unmet | Result/operation availabilityとして表現。Navigation Stage存在自体とは分離 |
| Artifact read integrity failure | `ArtifactHashMismatch`として扱い、破損contentを正常として返さない |
| Client disconnect | server-side Execution継続。cancelは明示Command |


## 18. Schema / Dependency Boundary

- `analysis-specification/1`の既存`analysis_family`を再利用する。
- Navigation Stage fieldをAnalysisSpecificationへ追加しない。
- ExecutionPlan / Execution / StageExecutionへNavigation Stage fieldを追加しない。
- Product Domainはbrowser route/navigation implementationへ依存しない。
- Scientific / ML / visualization libraryはPort / Adapter背後へ隔離する。
- Capability固有Adapterはcanonical runtime lifecycleを制御しない。
- Navigation metadata/stateについてはDB migrationを行わない。
- Reproducibility contractとして`StageAttempt.effective_random_seed: int | null`を追加するDB migrationを行う。
- `Execution.runtime_version_json`へ`ariadne_code_version / python_version / platform_system / platform_release / machine / libraries`を保存する。


## 19. Test Architecture

Current design concernを次のtest layerへtraceする。

- domain invariant / typed filter / scientific guard → unit/domain test
- persistence / StageAttempt seed / concurrency / idempotency / authorization / lineage → integration test
- route/header/error/response/authorization → API contract test
- Navigation/deep link/history/async state/accessibility → frontend/browser test
- Navigation→runtime import prohibition / optional future dependency prohibition → architecture/static test
- Planner golden / Plan DAG / Runner contract / worker lifecycle → workflow regression
- CLI / library direct execution → headless regression
- Predictive existing setting/spec parity → compatibility regression
- Causal scientific benchmark / Predictive leakage/split/subgroup → scientific test
- Family横断browser E2E

`DEFERRED` concern（general AuditLog、retention、object storage、hard limits、production auth hardening、cross-store compensation等）のtest targetをcurrent mandatory acceptanceへ混ぜない。

## 20. CHANGE LOG

### 20.4 ENH-E4 Canonical Execution Architecture

canonical Product runtime Execution authority、generic workflow core、persistent StageExecution、Result / Artifact / Lineage authority等の設計を継承する。

### 20.5 ENH-E5 Family × Navigation Stage Application Architecture

Project Workspaceのanalytical navigationをFamily / Family-local Navigation Stageへ再構成する。Navigation taxonomyはPresentation / Application / Capabilityの責務として追加し、Generic Workflow Coreおよびruntime Execution Stageへ依存を逆流させない。

### 20.6 ENH-E5 Phase I Canonical Convergence

- Outbox/nonexistent Port overstatementをD1 current contractへ訂正した。
- Navigation metadata endpoint/schema/route/default Stageをfreezeした。
- typed filter、subgroup、comparability、authorization、idempotency、lineage、reproducibility、frontend accessibilityをD2 targetとして具体化した。
- `StageAttempt.effective_random_seed` migrationを明示し、D3 capabilityをE5 acceptanceから分離した。


### 20.7 ENH-E7 Project Management / Analysis Workspace Basic Architecture

Application IAをProject ManagementとAnalysis Workspaceへ分離し、Project route、Analysis Context、resource ownership、existing Causal/Exploratory/Predictive surface placementをcurrent basic designへ統合した。API/persistence/backend execution semanticsはUI再配置だけを理由に変更しない。

### 20.8 ENH-E7 Product Basic Design Structure Restoration

- ENH-E2で確立していた「文書の設計粒度」「screen/function boundary」「operation / prerequisite / Resource effect / post-state / UI Gate」「画面遷移とlogical context handoff」という基本設計の記載粒度を復元した。
- Top-level IAのconcept authorityは`00_product_concept_memo.md > 3. Ariadne application model`へ集約し、本書ではsurface responsibility、route authority、resource lifecycle ownership、operation/state boundaryを詳細化する責務分離とした。
- Project Management / Analysis Workspace分離、Analysis Context、Family/Navigation Stage、existing capability placement、runtime/capability semanticsは維持した。

