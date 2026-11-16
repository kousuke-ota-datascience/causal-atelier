# 30_00_overall_DD


---

## 1. 実装原則

1. DomainはFramework / ORM / external analytical object / browser navigationへ依存しない。
2. Application ServiceはUnit of WorkとPortを通じてpersistence / external capabilityを利用する。
3. Scientific / ML library objectはAdapter境界の外へ持ち出さず、persistent payloadへ直接保存しない。
4. persistent snapshotはstrict schema validation、canonical JSON、content hashを持つ。
5. Runnerはruntime Stage input/output contractを受け取り、DB transactionやbrowser stateを直接操作しない。
6. Execution lifecycle authorityは`Execution`、runtime Stage lifecycle authorityは`StageExecution`に集約する。
7. `AnalysisFamily`は`EXPLORATORY / CAUSAL / PREDICTIVE`の3値を持つdomain enumをcanonical discriminatorとする。
8. Navigation Stageはapplication/presentation metadataであり、`AnalysisSpecification`、`ExecutionPlan`、`Execution`、`StageExecution`へ保存しない。
9. Navigation taxonomyの変更だけを理由にruntime `StageType`、stage dependency、retry/lease lifecycleを変更しない。
10. CLI / Python library / backend use caseはNavigation Stageを設定せずanalysis executionを開始できる。
11. UI上のNavigation Stageとruntime Stageに1:1 cardinalityを要求しない。
12. Project ManagementとAnalysis Workspaceは別navigation scopeとし、route/state authorityを混在させない。
13. Analysis Contextは新しいpersistent aggregateや専用backend APIではなく、既存resource/selectionのapplication-level projectionとして扱う。
14. UI / IA再編だけを理由に既存API contract、persistence schema、backend analysis/domain semanticsを変更しない。
15. Family-specific scientific semanticsをpresentation都合でgeneric score/statusへ平坦化しない。
16. Project境界をauthorization、resource ownership、lineage traversalの共通boundaryとする。
17. Stage Contentsのprimary identityはcurrent canonical Navigation Stageとし、legacy workspace groupingをcurrent Stage identityとして表示しない。
18. Stage固有のmain operation/result/explanationは、その責務を持つNavigation Stageが所有する。cross-stage情報はcompactなprerequisite/referenceに限定する。
19. 主要semantic sectionは縦方向reading flowを基本とし、独立sectionの横並びを理由にpage-level horizontal scrollを要求しない。
20. Predictive feature-column編集はSetupが所有し、Dataset Version schemaをcandidate authorityとする。Train/Predictは該当feature setをread-only表示する。

---

## 2. Software responsibility boundary

### 2.1 Layer responsibility

```text
Frontend / Browser
├─ Application Router
├─ Project Management UI
└─ Analysis Workspace UI
        │
        ▼
Interface / API
├─ Project / Context / Dataset / View API
├─ Analysis Specification / Execution / Result API
├─ Navigation metadata API
└─ Operation Availability API
        │
        ▼
Application
├─ Project / Context / Dataset / View use cases
├─ Analysis workflow use cases
├─ Navigation catalog aggregator
└─ authorization / Unit of Work orchestration
        │
        ▼
Domain / Capability / Runtime
├─ Product Domain
├─ Exploratory Capability
├─ Causal Capability
├─ Predictive Capability
├─ Planner / PlanValidator
├─ Runner Registry
└─ Generic Executor
        │
        ▼
Persistence / Artifact / External scientific adapters
```

### 2.2 Navigation metadataとruntimeの境界

| Concern | Owner | Navigationを参照 | Persistent |
| --- | --- | --- | --- |
| Family / Navigation Stage catalog | Capability + application/interface aggregator | する | しない |
| Browser route / current Family / current Stage | Frontend/application navigation | する | しない |
| Analysis Context selection | Frontend/application workspace state | route/resourceを参照 | 既存selection/resourceのみ |
| AnalysisSpecification | Product Domain | しない | する |
| ExecutionPlan / StageDefinition | workflow/domain | しない | snapshotとして保持し得る |
| Execution / StageExecution | runtime/domain | しない | する |
| Result / Artifact / Lineage | product/domain | しない | する |

新しいpersistent `navigation` aggregate/table、`AnalysisContext` table、`CurrentFamily` field、`CurrentNavigationStage` fieldを作らない。

### 2.3 Runtime packageへの禁止依存

次の責務からbrowser route / Navigation descriptor / Project Management componentをimportしない。

- Execution domain
- StageExecution domain
- Execution / StageExecution repository
- planner / plan validator
- runner registry
- generic executor
- worker claim / lease persistence
- scientific runner

architecture testで依存方向を検査可能にする。

---

## 24. Current design invariants

次はcurrent detailed designのMUST NOT invariantである。

1. Project ManagementとAnalysis Workspaceを1つのpeer-tab navigationへ再混在させない。
2. Project-global resource管理をAnalytical Familyとして扱わない。
3. Family/Navigation StageをExecution/StageExecution statusへ読み替えない。
4. current Navigation Stageをscientific reproducibility inputへ保存しない。
5. frontendにbackend catalogのduplicate full definitionを持たせない。
6. Analysis Contextをnew persistent aggregate/APIとして実装しない。
7. Analysis Workspace内でCurrent Projectを直接switchさせない。
8. missing contextをfake default resourceで補完しない。
9. Data Quality用backend operationをUI都合で新設しない。
10. TIME_TRENDへ新しい時系列scientific semanticsをUI都合で導入しない。
11. CHARTのpersistent operation semanticsを表示専用へ退化させない。
12. legacy analytical entryをparallel navigation authorityとして維持しない。
13. Project/Analysis route stateをruntime domainへ逆流させない。
14. UI IA変更だけを理由にDB/API/backend domain semanticsを変更しない。
15. Selected ProjectからProject Listへのparent actionを`history.back()`で実装しない。
16. legacy `Inference`等のworkspace groupingをcurrent canonical Stage identityとして表示しない。
17. Causal presentation groupingをroute/Navigation Stage/runtime Stage/persistent stateへ昇格させない。
18. Identification / Estimation / Effects / Diagnostics / Sensitivityのmain responsibilityを1つのgeneric surfaceへflattenしない。
19. Refutation/Sensitivity editable controlをSensitivity以外のStageへ配置しない。
20. Predictive Train/Predictでfeature setをad-hocに編集させない。
21. feature selectorのためだけにnew Predictive specification/API/backend operationを追加しない。
22. Predict Navigation Stageのためだけにstandalone scoring engineを新設しない。
23. UI/IA再編だけを理由にLightGBM / LIME / SHAP等のnew analytical capabilityを暗黙追加しない。
24. major semantic sectionの横並びを理由にpage-level horizontal scrollを必須化しない。

---

## 90. 詳細設計の目的・責務・必要粒度

**本種別は物理ソフトウェア設計である。** 上位のRD/LDD/BD/APIが定める契約を、module、class、関数、フィールド、メソッドシグネチャ、アルゴリズム、例外、テスト可能な不変条件へ落とす。参照例①（個別機能）・参考②（共通機能）の責務分割を踏襲する。

**各classで必須の記載:**

| 項目 | 定義すべき情報 |
|---|---|
| 識別 | Class/Protocol名、`module path`、現行/新規/候補の区分、参照source SHA |
| 目的・責務 | 単一責任、保持しない責務、依存可能/禁止層、lifecycleとowner |
| 属性 | field名、Python型、必須/default/null、immutableかmutableか、生成元・validation・機密分類 |
| 生成 | constructor/factoryの引数・型・戻り・precondition・postcondition |
| 公開method | 可視性、正確なsignature、戻り値、入力検証、計算/状態変更、副作用、例外 |
| 処理ロジック | 実行順、分岐、事前事後条件、algorithm/pseudocode、数値精度・seed、計算量上の制約 |
| collaboration | 呼出し先Port/Adapter/Library、呼出し方向、transaction/rollback/retry、I/O |
| serialization | 入出力Schema/Version、hash/canonicalization、atomic write、readback互換性 |
| 失敗・安全 | error code、fail-closed条件、partial write、path traversal、privacy、optional Backend unavailable |
| 検証 | unit/contract/negative/regression/benchmarkのTest IDと上位FR/NFR/AR・GateへのTrace |

**設計書の作成単位:** 共通の実行基盤はoverallで境界だけ宣言し、具体class群は同じ責務と依存方向を共有するpackage/module単位で分割する。手法固有の統計式は上位のScientific Contractを参照し、DDには呼出しと数値処理の詳細を書く。

**制約:** 現行物理コードから確認したclassはsource準拠として記載し、新E11実装前の候補classは`PROPOSED / ADR_REVIEW_REQUIRED`と区別する。既存Classの記述が存在しても、全Classの物理仕様が完了したことを意味しない。

- [30_20_planning_validation.md](30_20_planning_validation.md)

