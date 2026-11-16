# 22_00_overall_BD


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
- ENH-E11作業版のProduct requirement / NFR / Scientific ARは[`10_requirements_definition/`](../10_requirements_definition/10_00_overall_RD.md)をauthorityとし、元正本は全件テストPASS後まで変更しない。
- Resource/Entity/Value/stateのE11作業版は[`21_logical_data_design/`](../21_logical_data_design/21_00_overall_LDD.md)を参照する。
- API/browser/Local CLI/Portの具体contractは[`23_api_interface_design/`](../23_api_interface_design/23_00_overall_IF.md)へ詳細化する。
- Module/Class/Method・例外・実行詳細は[`30_detailed_design/`](../30_detailed_design/30_00_overall_DD.md)へ詳細化する。

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

### 3.1. Existing Product（変更しない）

```text
Web Frontend → Versioned Web API → Product Application/Domain
                              ↓
                     Metadata DB / ArtifactStore
                              ↓
                     Execution Worker / Scientific Core
                              ↓
                     Product Result / Artifact / Lineage
```

### 3.2. Local Scientific CLI（Product実行系から独立）

```text
Local CLI / Explicit Versioned Config
                ↓
Local Application + Preflight + Scientific Domain
                ↓
Identification → Estimator Eligibility → Method Scientific Adapter
                ↓
Typed Scientific Outcome → Local Artifact Publisher → Local Manifest
```

**禁止:** E11 Local CLIがWeb API・Product DB・Worker lifecycleやNavigation Stageをrequired inputにすること。別契約間の自動同期・旧v2暗黙upgradeを禁止。共通化するScientific CoreはPort経由で再利用し、authorityを混同しない。

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


## 5. Local Scientific CLIの独立した実行境界

### 5.1. ProductとLocalの正本・依存の分離

```text
Existing Product lane (unchanged)                 ENH-E11 local lane (new, independent)
Web UI → Web API → Product Application             CLI / local config & data
          ↓                                                   ↓
       Product Domain                               Local Application / Preflight
          ↓                                                   ↓
Product DB / Worker / Execution lifecycle           Local Scientific Domain / Identification
          ↓                                                   ↓
      Product Scientific Adapter                       Method Scientific Port
          ↓                                                   ↓
  Canonical Product Result / Artifact                 Optional Scientific Adapter
                                                               ↓
                                                  Local Result + Local Artifact Publisher
                                                               ↓
                                                  JSON / Parquet / Manifest + readback

        Both may reuse scientific algorithms/interfaces only via compatible Ports.
        Neither lane silently writes or upgrades the other lane's canonical state.
```

- 左は既存Productの説明でありE11の改修対象外。旧`causal-analysis-spec/2`、Execution/StageExecution、Worker、Project DB、Navigation、Product Web APIの意味を維持する。
- 右は**Local CLI → Local Application → Scientific Domain/Ports → Method別Adapter → Local Artifact**。E11を追加するためにWeb APIを経由させず、Product Execution ID／Project Membership／DB connectionを必須入力にしない。
- 両レーンでアルゴリズムの共通化は許すが、**Productの永続正本をLocal Manifestで置換しない**。独立のauthorityとprovenanceを明記する。
- Web UIのFamily/Navigation Stage、既存Product Workflowのruntime Stageと、Local CLIの分析処理順序は**異なる概念**。Local CLIでpreflight→identification→estimationと処理することはProductのStageType増設を意味しない。

### 5.2. Layer別の責務と依存方向

| Layer | Owner / Responsibility | Allowed input / dependency | Forbidden dependency |
|---|---|---|---|
| Local Scientific Domain | Question, Design, Estimand, Graph, assumptions, identification/eligibility state, result意味・不変条件 | versioned domain values / immutable refs | DoWhy/EconML/Tigramiteの生object、Product ORM、Web route |
| Scientific Port | Domain入力をMethod実行可能性と標準結果に接続 | versioned domain contract | backend独自のdtype／method objectを外部契約に露出 |
| Method Scientific Adapter | optional backend/APIのAvailability・版確認、入力翻訳、出力正規化 | declared Port, optional library | Domain上のEstimand再定義、silent fallback、Product DB直接更新 |
| Local Application | Preflight・Identification・Eligibility・Execution・Result validation・publish coordination | Domain, Port, local IO abstractions | Navigation Stage ID、Product Worker claim/lease、browser route |
| CLI Interface | 明示schema dispatch、config/args・ファイル検証、Method選択、exit class表示 | Local Application API | Product API必須化、旧v2の無断reinterpretation |
| Local Artifact Port/Adapter | canonical relative key、安全なstaging、checksum/readback、publish、failure cleanup | Root/policy, normalized data | 部分保存の成功宣言、制御外パスへの任意書込 |
| Product Domain / Application | 現行Product Resource・RBAC・persistent lifecycle authority | 既存契約 | E11を理由にしたDB migration・Product API/Worker拡張 |

**Dependency direction:** CLI→Local Application→Domain/Ports、External adapter→Port implementation。DomainからCLI/Framework/Adapterへ逆依存させない。既存のPortと重複する新Portを導入するかはDD-01で実物コード・Authorityを照合してから決定する。

### 5.3. Operational ownership matrix

| Operation / invariant | Domain | Local Application | Scientific Adapter | CLI | Local Artifact |
|---|---|---|---|---|---|
| Estimandの科学的意味、Graph不確実性、IV target区別 | R | C | C | — | — |
| Method/Estimand/Identification適格性 | R | R（順序・Gate） | C（実効Capability） | — | — |
| Backend実効API/version probe | C（許容契約） | C | R | C（表示） | — |
| config/version dispatch・入力Fileの検証 | C | C | — | R | C（Path） |
| Scientific Resultと各状態の正規化 | R | R（検査・公開可否） | R（raw変換） | C | C（保存） |
| Manifest・hash・staging・Readback/atomic publish | C | R（commit決定） | C（実効版） | C | R |
| 局所データ/個票出力のプライバシー方針適用 | R（分類） | R（Policy Gate） | — | R（opt-in受付） | R（権限/Path） |
| Product auth/Execution/DB/Worker | — | — | — | — | —（既存Productのowner） |

### 5.4. 相互運用上の禁止事項

- Phase1〜3は承認されたLocal Scientific CLI（41 Method内のR/Q/N）とLocal Artifactのみに限る。DEC09のD-only、Product統合、GAP-C01〜04の解消を「Local CLI実装」と同一視しない。
- Version dispatchは**旧`causal-analysis-spec/2`と新Local契約を別に扱う**。旧読取とREQUIRES_REVIEW/overrideは変更せず、E11新Methodを旧v2経由で無条件に実行しない。
- 正確なCLI command・config version・Port/class名・Backend pin・具体enumは**IF-01/DD-01/ADRでFreeze**。ここで仮名を既成事実化しない。

本節はLocal Causal解析機能の**現行予定設計**として継続的に保持する。

## 90. この文書種別の目的・責務・規範性

- **目的:** 上位Requirementを実現する論理component、責務境界、実行sequence、validation/authorization/exception policyを定める。
- **含む:** Domain・Application・Adapter・CLI・Product Authority、入力前提・主処理・状態変化・結果・失敗時挙動、配置先責任、deployment boundary。
- **含まない:** Class個別属性/メソッド、具体JSON field・endpoint signature、統計式の真偽を設計だけで保証すること。
- **E11境界:** Scientific Core + Local CLI + Local persistent artifactsに限定。既存Web/API/Worker/DB/migrationへの新手法統合はD。G01〜G10は暫定実装Workstreamで、受入プロセスGate06/07とは別。


**当該機能に適用する設計制約（関連Requirement）**

- **`NFR-018`**：Product DomainからWeb Framework、ORMおよびlegacy packageへ依存しない
