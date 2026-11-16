# 22_00_overall_BD

**Status:** `RD02_STRUCTURAL_WORKING_COPY / E11_NOT_PUBLISHED`. Original chapter and source provenance retained; DD physical coverage remains partial.  
**Source blob:** `87196f2f03a7f3367724bc05fb254d1a4d98109e`.

---

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

## 90. この文書種別の目的・責務・規範性

- **目的:** 上位Requirementを実現する論理component、責務境界、実行sequence、validation/authorization/exception policyを定める。
- **含む:** Domain・Application・Adapter・CLI・Product Authority、入力前提・主処理・状態変化・結果・失敗時挙動、配置先責任、deployment boundary。
- **含まない:** Class個別属性/メソッド、具体JSON field・endpoint signature、統計式の真偽を設計だけで保証すること。
- **E11境界:** Scientific Core + Local CLI + Local persistent artifactsに限定。既存Web/API/Worker/DB/migrationへの新手法統合はD。G01〜G10は暫定実装Workstreamで、受入プロセスGate06/07とは別。

**E11追加草案:** [22_08_enh_e11_causal_cli_basic_design_draft.md](22_08_enh_e11_causal_cli_basic_design_draft.md)
