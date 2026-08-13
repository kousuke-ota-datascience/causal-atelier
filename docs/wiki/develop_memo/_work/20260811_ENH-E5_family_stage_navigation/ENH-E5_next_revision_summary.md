# ENH-E5 次版改訂サマリ

## 1. 改訂の結論

本版は、レビューで指摘された「文書構造の抽象度不整合」「ENH-E5差分資料化」「ENH-E4設計体系からの逸脱」「Execution Agentへの不要な仕様探索余地」を是正した次版ドラフトである。

主要な方針は次のとおり。

1. Revised requirements/design documentsは、ENH-E4までの章構成・記載粒度をcanonical baselineとして再構成する。
2. ENH-E5固有概念を文書のトップレベルへ突出させず、既存責務体系の適切なsectionへ配置する。
3. Product Concept本文は現在のプロダクト像から開始し、Enhancement履歴は後段へ分離する。
4. `Navigation Stage != Execution Stage`を、具体的な問題シチュエーションと依存方向まで含めて要件・基本設計・詳細設計・Gate ACへ落とす。
5. G00〜G05のExecution Agentは単一normative contractだけを使用する。

## 2. 文書構造の改訂

### 2.1 Product Concept

- 冒頭を`ENH-E5は...`で開始しない。
- Familyタブの表示方法やNavigation/Executionの具体的問題例をmajor chapterへ置かない。
- `Analytical Families`の下にExploratory / Causal / Predictiveを束ねる。
- external analytical engineは「今後の拡張予定」配下へ置く。
- Change scope / historyは本文後段またはCHANGE LOGへ分離する。

### 2.2 Requirements

ENH-E4までの構成を踏襲し、ENH-E4時点のFR-001〜FR-128 / NFR-001〜NFR-020 / AR-001〜AR-020を削らずcurrent effective requirementsとして保持した。その上でENH-E5要件をFR-129〜FR-162 / NFR-021〜NFR-027 / AR-021〜AR-026として追加・整理する。

構成:

```text
0 INTRODUCTION
1 適用範囲
2 Actor
3 業務Capability
4 E2Eシナリオ
5 機能要件
6 非機能要件
7 科学・統計・分析上の要件
8 状態要件
9 権限要件
10 データ保持・監査要件
11 対象外要件
12 総合完了条件
13 CHANGE LOG
```

`Requirement levels`はLegends配下へ置く。

### 2.3 Logical Data Design

```text
1 設計目的
2 基本原則
3 論理モデルの構成要素
  3.1 Domain Resource
  3.2 Domain Resource外の論理概念
  3.3 論理概念の分類原則
4 Domain Resource関係モデル
5 Domain Resource定義
6 Canonicalization
7 Index / Unique Constraint
8 Schema Reader Contract
20 CHANGE LOG
```

current sourceとの照合により、`AnalysisSpecification.analysis_family`が既に存在することを確認した。duplicate Family discriminatorは追加しない。Navigation StageはAnalysisSpecification / ExecutionPlan / Execution / StageExecutionへ保存しない。

### 2.4 Product Basic Design

ENH-E4の全体設計taxonomyへ戻した。

- System Context
- Architecture Principle
- Project Workspace Information Architecture
- Generic Workflow Core
- Family別Workflow / Capability
- Validation Architecture
- Result / Artifact / Lineage
- Comparison
- Frontend State
- Security / Deployment / Failure / Schema Boundary / Test

Family tab / Stage sidebarはWorkspace IAのsubsection、Navigation/Execution分離はGeneric Workflow Coreのsubsectionとして記載する。

### 2.5 API / Interface Design

ENH-E4のresource/interface taxonomyを維持し、Navigation metadataは`Frontend Support API`配下へ配置した。

`GET /api/v1/navigation/analysis`はtarget candidateであり、Human Architecture Review前の確定事項ではない。

Analysis Specification / Execution / Worker / CLI APIへNavigation Stageを必須入力として追加しない。

### 2.6 Detailed Design

ENH-E4のPackage / Value Object / Schema / Planner / Executor / Capability / Result / Frontend / Persistence / Test構造をbaselineとし、Navigation descriptor/catalog/route/UI実装を適切な既存sectionへ統合した。

## 3. Architecture上の重要な照合結果

current codeでは次を確認した。

- `AnalysisFamily = EXPLORATORY | CAUSAL | PREDICTIVE`が存在する。
- `AnalysisSpecification.analysis_family`が存在する。
- `ExecutionPlan.analysis_family`および`Execution.analysis_family`が存在する。
- runtime側には`StageType / StageDefinition / StageExecution`があり、navigation viewとは別のlifecycle semanticsを持つ。

したがって、Navigation model導入で新しいFamily discriminatorやruntime Navigation Stage fieldを追加する必要はない。

## 4. Execution Agent isolation

Execution contractの参照範囲だけでなく、内容密度も見直した。G01〜G04のP01〜P03は、汎用template文ではなく、担当Package固有のrequired behavior / prohibited scope / focused verification / Package Acceptance Checklistを本文へ収束した。

- SINGLE_EXECUTION Coding Agent: 対象Gateの06のみ。
- WORK_PACKAGE Coding Agent: assigned Pxxのみ。
- Test / Audit Agent: 対象Gateの07のみ。
- P00はOperator / Planning用でありPackage Agentの入力ではない。
- repositoryはimplementation fact/evidenceを得るために読んでよいがspec authorityではない。
- ambiguityは`BLOCKED_CONTRACT_AMBIGUITY`で停止する。

> Repositoryから実装方法を発見してよい。Repositoryや上流資料から仕様を発見してはならない。

## 5. Review feedbackへの追加対応

- 全Revised documentでheading hierarchyを再点検し、個別UI論点を不適切なトップレベルchapterへ置かない。
- `AnalysisSpecification.analysis_family`をcurrent sourceと照合し、duplicate Family discriminatorを禁止した。
- Navigation StageをAnalysisSpecification / ExecutionPlan / Execution / StageExecutionへ保存しない。
- G00のsingle 06/07だけでcatalog実装・検証できるよう、DRAFT targetのFamily order / Stage ID / slug / default / descriptor / read-interface contractを本文へ明示した。これらはHuman approval後に一意のFROZEN値へ確定する。
- PxxからParent 06/P00の参照metadataを除き、assigned Pxx単体で実行する境界をさらに強めた。

## 6. 状態

本bundleは`DRAFT_FOR_REVIEW`である。Architecture Review、preflight、exact route/API decision、baseline testを完了するまではGate contractを`FROZEN`にしない。

## 7. 今回のレビュー追加反映（v4）

### 7.1 Detailed Designの実装解像度

`30_detailed_design.md`について、基本設計/API設計の要約を繰り返すのではなく、コードへ落とせる粒度へ増補した。

主な追加内容:

- `AnalysisFamily`の定義値、serialization、利用箇所
- `StageType / StageDefinition / StageBinding`のfieldとvalidation
- `ResourceRef`の全fieldとLineage上の責務
- `AnalysisSpecification` / `ExecutionPlan` schema field
- Worker claim / lease / completion contract
- `Execution` / `StageExecution` field・status transition・attempt lifecycle
- Predictive `predictive-analysis-spec/1`のfield、split/metric/leakage validation
- Predictive runtime `split -> prepare -> train -> evaluate -> optional explain` plan
- Result Type / Scientific Status一覧
- Lineage authority classification
- Family/Stage route parse/serialize、deep link、history、error handling
- Navigation persistence禁止field
- component単位のtest seam / negative test

### 7.2 API設計の外部依存除去

`23_api_interface_design.md`で、`既存Xを維持する`だけでは意味が確定しない箇所を具体contractへ展開した。

特に以下を訂正・明文化した。

- `AnalysisFamily`は`EXPLORATORY / CAUSAL / PREDICTIVE`の3値であり、`AnalysisSpecification.analysis_family`がcanonical discriminatorである。
- Result public APIはExecution起点のlist、Result単体read、comparison、lineage、exportの具体pathを本文へ記載した。
- Annotation public APIはcreate/get/updateの具体path・response fieldを本文へ記載した。planning baselineで確認できないlist/history endpointは存在する前提で記載しない。
- Artifact public APIはmetadata/read verified downloadの具体path・response field・Digest contractを本文へ記載した。
- `Findings` / `Model Management`が利用するResult Type / Artifact Type / Annotation / Lineageを列挙し、UI名だけを理由とした重複Resource/APIを禁止した。
- Worker claimはpublic `claim_token` APIではなく、`Execution.lease_owner / lease_expires_at`とrepository-level `claim_next / renew_lease / complete`による内部ownership contractとして記載した。
- planning baselineに独立したExecution/Stage event publish interfaceが存在しないため、`existing event schemaを維持する`という旧記載を撤回した。Navigation route changeをruntime lifecycle eventへ変換しないことだけをtarget invariantとして残した。

### 7.3 自己完結性の横断基準

23/30では、以下の表現を設計説明の代替として用いない。

- `既存を利用する`
- `existing contractを維持する`
- `従来どおり`
- `current implementationに従う`

再利用・非変更方針を記載する場合も、対象type/schema/interfaceのfield/value/transitionを本文内に記述し、読者が外部文書またはsource codeを開かなければ設計内容を理解できない状態を作らない。
## 8. 既存実装・設計整合性監査（v5）

ENH-E5で変更しない既存contractをPlanning baseline sourceと突合し、設計記述に残っていた乖離を修正した。詳細は`00_enhance_background/06_existing_implementation_design_alignment_review.md`に記録する。

主な修正:

- canonical `Execution / StageExecution / StageAttempt / Result / Artifact / GraphVersion / Annotation`のfield・constraintをcurrent persistence/domainへ合わせた。
- Predictive/ExploratoryのResult status matrixをcurrent persistence constraintへ合わせた。
- generic canonicalizationとSchema Registryのcurrent contractを修正した。
- Bearer/OIDCや`ANALYST / OPERATOR`をcurrent contractとする誤記を除去し、`X-User-Id`と`OWNER / EDITOR / VIEWER`へ合わせた。
- Worker claimをpublic `claim_token`ではなくExecution lease ownershipとして記述した。
- Causal plannerを1 canonical Execution = 1 runtime Stageのcompatibility planとして修正した。
- Predictive runtime順序を`split -> prepare -> train -> evaluate -> optional explain`へ修正した。
- Exploratory plannerをoperationごとの1 runtime Stageとして明記した。
- `PlanValidator` / `StageRunnerRegistry`の責務・signatureをcurrent implementationへ合わせた。
- current CLI entry pointおよびheadless/local execution boundaryへ修正した。
- Lineage authorityをENH-E4 Phase記述ではなくcurrent `classify_lineage_authority`のexact tupleへ置換した。
- `30_detailed_design.md`のpackage mapに存在しないservice/module名が混在していたため、current package baselineへ置換した。ENH-E5新規Navigation module名はfreeze前に捏造しない。
- Research Context relation validationをcurrent sourceへ再照合し、同一Project target解決・自己参照禁止は維持する一方、未実装の一般cycle policyをcurrent contractから除去した。
- `GET /projects/{project_id}/analysis-specifications`はProject内全件一覧であり、Family / Context / Dataset query filterを受けるという誤記を修正した。
- Research Context usage APIはcanonical Execution / Result全体のusage indexではなく、AnalysisSpecification + historical Family read modelを使うcurrent projectionであることを明記した。


監査判定: `PASS_WITH_CORRECTIONS_APPLIED`。


### 8.1 最終整合確認

設計側の修正後、変更しないcurrent contractについて再確認した。Resource field表はPlanning baseline ORM/domainと一致し、API設計ではcurrent public routeとinternal Worker lease contractを区別した。`AnalysisSpecification` listはProject内全件一覧、Research Context usageはAnalysisSpecification + historical Family read model projectionとして記載し、未実装filter / generic cycle policy /架空event publisherをcurrent contractとして残していない。

なお、Family top tabs、Navigation Stage catalog、browser route、navigation metadata deliveryはENH-E5 targetであり、current implementationに存在しないこと自体は乖離と扱わない。
