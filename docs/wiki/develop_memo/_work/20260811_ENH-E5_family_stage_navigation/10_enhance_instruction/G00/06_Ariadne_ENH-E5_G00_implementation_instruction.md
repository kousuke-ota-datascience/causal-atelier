# Ariadne ENH-E5 G00 実装指示書 — Gate Coding Contract（Gate実装契約）

文書区分: Primary Execution Contract（主要実行契約）
自己完結性: MUST（必須）

- プロジェクト: Ariadne
- Enhancement: ENH-E5
- Active Gate: G00
- Gate title: Family / Navigation Stage Domain Contract（Family / Navigation Stageドメイン契約）
- Branch: `feature/ariadne_mvp_e5`
- Baseline SHA: `46122c68333df03680b97c253a7b5d32bf9393e7`
- 契約状態: **DRAFT_FOR_REVIEW**（レビュー前ドラフト）
- Execution Mode: `SINGLE_EXECUTION`


## 0. 実装時の参照ポリシー — 本06のみをnormative sourceとする

本Gateは`SINGLE_EXECUTION`で実行する。Coding Agentに対する**唯一のnormative implementation contractは本06文書のみ**である。

Coding Agentは`WHAT / WHY / scope / responsibility / prohibited change / required outcome`を本06だけから判断しなければならない（MUST）。仕様を補完する目的で、00〜30、ADR、Gate decomposition、07、他Gate文書、過去Enhancement、issue、commit message、外部Webその他の資料を参照してはならない（MUST NOT）。

current repositoryのproduction code、existing tests、schema/type/interface、configuration、route/API implementation、repository structureは、current implementation factを確認し実装方法を決めるために参照してよい。ただしrepositoryは仕様authorityではない。

> **Repositoryから実装方法を発見してよいが、仕様を発見してはならない。**

current codeが本06と異なることを理由に、本06の要求を追加・削除・緩和・変更してはならない。

本06だけではrequired behavior、ownership、scope、compatibility、migration、architecture choiceを一意に決定できない場合、他資料を探索して補完せず`BLOCKED_CONTRACT_AMBIGUITY`で停止する（MUST）。

本06の外部にnormative decisionが残っている場合、本06を`FROZEN`にしてはならない。

## 1. Gate定義 / acceptance claim

### 目的
FamilyとNavigation Stageのapplication contractをExecution Stageから独立して成立させ、capability-owned canonical stage catalogとread APIを提供する。

### PASS後に後続Gateが利用できる成果
G01以降が、stable Family ID / stage ID / order / default Stage / catalog APIへ依存できる。

### この単位を1つのGateとする理由
この境界は、独立してaccept/protectできる1つのsemantic claimである。実装量が大きい場合は、Execution Modeが`WORK_PACKAGE`のときにWork Packageで分割する。

## 2. 実装時に有効な前提

- Familyはanalytical capabilityのcontextである。
- Navigation StageはUI/application上の作業・閲覧contextである。
- `Navigation Stage != Execution Stage` を維持する。
- Stageの名称・数はFamilyごとに異なってよい。
- Stage navigationを必須のsequential workflowとはみなさない。
- このGateで明示的に変更しない限り、既存のanalysis execution/persistence semanticsを保護する。
- 外部analytical engineの追加はENH-E5のscope外である。

### 2.1 FROZEN前に確定するcanonical navigation catalog

以下は本DRAFTでのtarget値である。**Human Architecture Reviewで承認または明示変更し、FROZEN版06ではDRAFT/未確定表現を除去して一意の値にすること。** Coding Agentへ判断を委ねない。

Family order / identity / slug / proposed default:

| order | AnalysisFamily | label | slug | proposed default Stage |
| ---: | --- | --- | --- | --- |
| 0 | `EXPLORATORY` | `Exploratory` | `exploratory` | `profile` |
| 1 | `PREDICTIVE` | `Predictive` | `predictive` | `setup` |
| 2 | `CAUSAL` | `Causal` | `causal` | `setup` |

Navigation Stage catalog:

| Family | order | Stage ID / slug | label |
| --- | ---: | --- | --- |
| EXPLORATORY | 0 | `profile` | `Profile` |
| EXPLORATORY | 1 | `data-quality` | `Data Quality` |
| EXPLORATORY | 2 | `distribution` | `Distribution` |
| EXPLORATORY | 3 | `relationships` | `Relationships` |
| EXPLORATORY | 4 | `comparison` | `Comparison` |
| EXPLORATORY | 5 | `findings` | `Findings` |
| PREDICTIVE | 0 | `setup` | `Setup` |
| PREDICTIVE | 1 | `train` | `Train` |
| PREDICTIVE | 2 | `predict` | `Predict` |
| PREDICTIVE | 3 | `metrics` | `Metrics` |
| PREDICTIVE | 4 | `explainability` | `Explainability` |
| PREDICTIVE | 5 | `model-management` | `Model Management` |
| CAUSAL | 0 | `setup` | `Setup` |
| CAUSAL | 1 | `discovery` | `Discovery` |
| CAUSAL | 2 | `identification` | `Identification` |
| CAUSAL | 3 | `estimation` | `Estimation` |
| CAUSAL | 4 | `effects` | `Effects` |
| CAUSAL | 5 | `diagnostics` | `Diagnostics` |
| CAUSAL | 6 | `sensitivity` | `Sensitivity` |

Stage IDはFamily-local stable identityである。表示labelからruntime時にIDを生成しない。Family間で同じStage ID（例: `setup`）を共有してよいが、identityは`(AnalysisFamily, stage_id)`で解決する。

### 2.2 Navigation descriptor contract

Navigation descriptorはExecution `StageType / StageDefinition / StageExecution`を継承・alias・field reuseせず、application metadata専用typeとして定義する。実装言語上の具体class名はrepository conventionへ合わせてよいが、最低限次を表現する。

`NavigationStageDescriptor`相当:

- `id`: Family-local stable Stage ID
- `label`: UI表示label
- `slug`: canonical route segment。現targetでは`id == slug`
- `order`: Family内表示順

`FamilyNavigationDescriptor`相当:

- `family`: existing `AnalysisFamily`
- `label`
- `slug`
- `order`
- `default_stage_id`
- `stages`

Generic aggregationは次をrejectする。

- duplicate Family
- 0件のStage
- Family内duplicate Stage ID/slug/order
- `default_stage_id`が`stages`に存在しない
- blank ID/slug/label
- unsupported/duplicate Family identity

### 2.3 Read API target contract

本DRAFTのtarget endpointは`GET /api/v1/navigation/analysis`、response schema versionは`analysis-navigation/1`とする。Architecture Reviewで代替interfaceを採用する場合は、本06/07をamendしてからFROZENにする。Coding Agentが別方式を選択してはならない。

Target response shape:

```json
{
  "schema": "analysis-navigation/1",
  "families": [
    {
      "family": "EXPLORATORY",
      "label": "Exploratory",
      "slug": "exploratory",
      "order": 0,
      "default_stage_id": "profile",
      "stages": [
        {"id": "profile", "label": "Profile", "slug": "profile", "order": 0}
      ]
    }
  ]
}
```

Responseは同一catalogに対してdeterministicなFamily/Stage orderを返す。Projectごとのcurrent navigation state、Execution status、runner、Resultは含めない。

このGateに対応するAcceptance target:
- AC-G00-001: Family identityとして既存AnalysisFamily値EXPLORATORY/CAUSAL/PREDICTIVEを用いる。
- AC-G00-002: Navigation descriptor typeは、execution StageType/StageDefinition/StageExecutionから構造上・semantics上独立している。
- AC-G00-003: 各capabilityが自身のStage ID、label、order、default Stageを正確に所有する。
- AC-G00-004: Generic aggregationはduplicate Family/Stage、空Stage list、不正default Stageをrejectする。
- AC-G00-005: `GET /api/v1/navigation/analysis`が3 Familyすべてについてdeterministicな`analysis-navigation/1` schemaを返す。
- AC-G00-006: DB migrationまたはnavigation-state persistenceを導入しない。
- AC-G00-007: 既存workflow/execution testがgreenを維持する。
- AC-G00-008: CLI/library/backend use case/runtime executionはNavigation Stageを必須inputとして要求しない。
- AC-G00-009: Navigation StageとExecution Stageの1:1 mappingを要求するcontract/dependencyを導入しない。
- AC-G00-010: 既存`AnalysisSpecification.analysis_family`をFamily discriminatorとして再利用し、duplicate Family enum/fieldを導入しない。
- AC-G00-011: AnalysisSpecification / ExecutionPlan / Execution / StageExecutionへNavigation Stage fieldを追加しない。

## 3. Execution Mode の決定

Mode: `SINGLE_EXECUTION`.

1つのbounded candidateとして実装し、candidate freeze前にGate-wide self-checkを実施する。

## 4. 必須の実装semantics

実装は、保護対象upstream contractの意味を変えずにGate目的を成立させなければならない（MUST）。このGateで明示的に必要としない限り、現在のanalysis spec、execution plan、result schema、algorithmを保持するadditive/refactoring変更を優先する。

## 5. 許可されるscope

- generic navigation descriptor types
- 3 Familyすべてのcapability-owned Stage catalog
- catalog aggregation/validation
- GET /api/v1/navigation/analysis
- unit/API tests
- direct execution regression tests where current CLI/library/application-service seam exists

## 6. 明示的な禁止scope

- Execution StageType/StageDefinition/StageExecutionの変更またはalias利用
- CLI/library/backend use case/runtime APIへのNavigation Stage必須argument追加
- Navigation Stage IDをrunner selection/dependency DAGのsource-of-truthとして使用
- frontend navigation shell implementation
- DB migration
- analytical engine changes

全Gate共通の禁止事項:
- testをgreenにすることだけを目的としたassertion弱体化、test削除、skip、xfailは禁止;
- requirement/ACの無断変更は禁止;
- 後続Gateの作業をこのGateへ混入させない;
- 未承認のschema/dependency/engine拡張は禁止。

## 7. 保護対象となる既PASS Gate contract

NONE — first Gate.

本06をfreezeする担当者が、必要なprotected Gate identity / evidenceをfreeze前に本節へ具体値として転記する。Coding AgentへCurrent State Control Sheetの再探索を要求しない。

## 8. Transition Debt

計画上は`NONE`。後続へ延期したscopeはTransition Debtではない。

一時的な例外挙動が不可避になった場合は停止し、architecture/Humanの明示的判断を求める。文書化されていないdebtを勝手に作らない。

## 9. Schema / migration / API / runtime ポリシー

- DB schema migration: 明示的なamendmentがない限り`PROHIBITED`。
- AnalysisSpecification/ExecutionPlan/Execution/StageExecution/Result schema変更: このGateで明示しない限り`PROHIBITED`。
- 既存`AnalysisSpecification.analysis_family`と重複するFamily discriminator追加: `PROHIBITED`。
- `navigation_stage` / `current_navigation_stage`等のpersistent analysis/runtime field追加: `PROHIBITED`。
- Execution lifecycle: 既存semanticsを保持する。
- API変更: このGateで明示的に必要とするadditive変更だけを許可する。
- legacy analytical route: 保持または明示的にnormalizeし、無断削除しない。

## 10. 自動テスト義務

- AC-G00-001について自動テストevidenceを実装する: Family identityとして既存AnalysisFamily値EXPLORATORY/CAUSAL/PREDICTIVEを用いる。
- AC-G00-002について自動テストevidenceを実装する: Navigation descriptor typeは、execution StageType/StageDefinition/StageExecutionから構造上・semantics上独立している。
- AC-G00-003について自動テストevidenceを実装する: 各capabilityが自身のStage ID、label、order、default Stageを正確に所有する。
- AC-G00-004について自動テストevidenceを実装する: Generic aggregationはduplicate Family/Stage、空Stage list、不正default Stageをrejectする。
- AC-G00-005について自動テストevidenceを実装する: `GET /api/v1/navigation/analysis`が3 Familyすべてについてdeterministicな`analysis-navigation/1` schemaを返す。
- AC-G00-006について自動テストevidenceを実装する: DB migrationまたはnavigation-state persistenceを導入しない。
- AC-G00-007について自動テストevidenceを実装する: 既存workflow/execution testがgreenを維持する。
- AC-G00-008について自動テスト/構造evidenceを実装する: CLI/library/backend use case/runtime executionはNavigation Stageを必須inputとして要求しない。
- AC-G00-009について自動テスト/依存関係evidenceを実装する: Navigation StageとExecution Stageの1:1 mappingを要求するcontract/dependencyを導入しない。
- AC-G00-010について構造evidenceを実装する: 既存`AnalysisSpecification.analysis_family`をFamily discriminatorとして再利用し、duplicate Family field/enumを追加しない。
- AC-G00-011についてschema/code evidenceを実装する: AnalysisSpecification / ExecutionPlan / Execution / StageExecutionへNavigation Stage fieldを追加しない。

変更moduleに対するfocused existing testと、diffの影響を受けるすべての保護対象upstream contractを対象としたregression testも実行する。

## 11. Candidate Assembly（候補成果物の組み立て）

`READY_FOR_TEST`へ移行する前に:
1. 必須の実装scopeがすべて完了していること;
2. Packageがある場合、すべてに有効なcheckpoint reportがあること;
3. 未解決blockerが`NONE`であること;
4. focusedおよびGate-wide self-verificationが記録されていること;
5. production/test/migration/dependency diffがレビュー済みであること;
6. implementation completion reportにFixed Trial Candidate SHAが1つ記録されていること。

## 12. Coding Agent の禁止作業

Coding Agentは以下をしてはならない:
- Gate PASSを判定する;
- 07 Acceptance Criteriaを変更する;
- Package完了をpartial PASSとして扱う;
- amendmentなしに既PASS Gateのsemanticsを変更する;
- 対象外の後続featureを実装する。

## 13. 必須成果物

- Trial01（またはcurrent Trial）のimplementation completion report
- 必要に応じたGate-local implementation ledger/detail
- `WORK_PACKAGE`時のPackage checkpoint/status report
- 正確なFixed Trial Candidate SHA
- 実行commandとtest evidence
- 明示的なblocker status

## 14. 外部参照ポリシー

source code pathおよび観測したruntime/test outputはevidenceとして参照してよい。Coding Agentが実装判断に用いるnormative rulesは本06にすべて記載する。本06外の設計資料から仕様を補完してはならない。
