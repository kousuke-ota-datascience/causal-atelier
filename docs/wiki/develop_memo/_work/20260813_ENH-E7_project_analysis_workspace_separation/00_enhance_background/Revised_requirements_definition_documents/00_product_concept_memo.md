# 00 プロダクトコンセプトメモ

- 文書状態: `APPROVED`
- 文書種別: 現行プロダクト構想のeffective snapshot
- 対象プロダクト: Ariadne
- 対象分析Family: Exploratory / Predictive / Causal
- 下位文書: `10_requirements_definition.md`, `21_logical_data_design.md`, `22_product_basic_design.md`, `23_api_interface_design.md`, `30_detailed_design.md`

> 本書は、過去Enhancementを知らない読者が、Ariadneをどのような分析プロダクトとして構成するかを理解できることを目的とする。変更履歴は後段へ分離し、本文は現在有効なプロダクト構想を記述する。

## 1. INTRODUCTION of Ariadne

### 1.1. プロダクトの一文定義

> **Ariadneは、Projectを問い・データ・分析・結果・判断の来歴境界とし、Project ManagementでResearch Contextおよびversioned analysis inputを管理し、Analysis WorkspaceでExploratory / Predictive / Causalの分析を行い、その条件、結果、判断理由および相互関係を追跡可能にする分析プロダクトである。**

短く表現すると、次のとおりである。

> **問い、データ、分析、結果、判断を切り離さずに残す。**

### 1.2. Ariadneのプロダクト像

Ariadneは単一の分析手法を実行する画面ではない。同一のResearch TopicとResearch Contextに対して、異なるAnalysis Familyの分析観点を往来しながら、versioned input、analysis specification、execution、result、artifact、annotation、lineageを一つのProject境界で扱うanalytical productである。

Top-level application responsibilityは、Project resourceを管理する`Project Management`と、明示されたProject contextの下で分析を行う`Analysis Workspace`へ分離する。全体のInformation Architectureは`3.0 Top-level Information Architecture (IA)`で定義する。

ProjectはResearch Topic、権限、分析資産、provenanceの境界である。Project Managementはそのresource lifecycleを扱い、Analysis Workspaceはcurrent analysis contextを消費してanalysis execution/presentationを行う。

Ariadneが目指すのは、Exploratory、Predictive、Causalを同一意味に平坦化することではない。それぞれが答える問いと成立条件を保持したまま、同一Projectの中で相互参照可能にすることである。

Ariadneが統合するのは分析活動のコンテキストと来歴であり、各Analysis Familyの意味論や成立条件ではない。

## 2. 分析プロダクトとして解く問題

### 2.1 分析観点と作業文脈を区別する

分析者は「どの分析観点で考えているか」と「その観点の中で何をしているか」を同時に扱う。

例えばPredictiveでは、モデル設定、学習、予測、性能評価、説明可能性、モデル資産確認は同じPredictiveという分析観点に属するが、作業・閲覧文脈は異なる。

Ariadneではこの2つを次のように分ける。

```text
Family = Analysis Workspace内のanalytical context
Stage  = Family-local work / view context
```

### 2.2 分析結果の意味論を守る

Exploratory association、Predictive performance、Causal effectは、いずれも意思決定に有用な情報になり得るが、科学的意味は異なる。

- Exploratory resultは仮説生成やデータ理解に用いる。
- Predictive resultは未知・将来の予測性能やモデル挙動を扱う。
- Causal resultは介入・反実仮想に関する仮定と識別条件のもとで扱う。

したがって、共通UIや共通envelopeを持たせる場合でも、Family-specific semanticsを失わせない。

### 2.3 UIの分類軸をruntime lifecycleへ漏らさない

ユーザーが画面上で認識する作業文脈と、backendが処理を分割・実行・retry・persistするruntime lifecycleは異なる責務である。

このため、画面上のStageをbackend executionのStageと同一視しない。詳細な問題シチュエーション、API・class境界、検証条件は要件定義・基本設計・詳細設計で定義する。

## 3. Ariadne application model

### 3.0 Top-level Information Architecture (IA)

AriadneのTop-level Information Architectureは、`Project Management`と`Analysis Workspace`の二つのworkspaceへ責務分離する。

```text
Ariadne
│
├─ Project Management
│
│   ├─ Project List
│   │
│   └─ Selected Project
│       ├─ Overview / Project Info
│       ├─ Research Context
│       ├─ Data
│       └─ Results / Lineage
│
└─ Analysis Workspace
    │
    ├─ Analysis Context
    │   ├─ Current Project
    │   ├─ Active Research Context
    │   ├─ Dataset Version
    │   └─ Analysis View
    │
    └─ Analysis
        ├─ Exploratory
        │   └─ Stage
        ├─ Causal
        │   └─ Stage
        └─ Predictive
            └─ Stage
```

このIAの中心原則は次のとおりである。

- `Project Management`はProject resourceとversioned analysis inputのlifecycleを管理する。
- `Analysis Workspace`は選択されたProject / Research Context / Dataset Version / Analysis Viewをanalysis input/contextとして分析を実行・閲覧する。
- `Family`はAnalysis paradigm、`Stage`はFamily内部のwork/view contextである`Navigation Stage`を指し、異なる抽象レベルの概念を同一navigation hierarchyへ混在させない。
- Project Management側のresource lifecycleとAnalysis Workspace側のanalysis execution/presentationを別responsibilityとして扱う。

以下の各節は、このTop-level IAと同じ階層に沿って各responsibilityを展開する。

### 3.1. Project Management

Project Managementは、Project resourceおよびversioned analysis inputのlifecycleを管理するworkspaceである。

ProjectはResearch Topic、目的、意思決定文脈、権限、分析資産およびprovenanceの境界である。Project Managementは、Projectを選択する全Project scopeと、選択済みProjectのresourceを管理するselected Project scopeを区別する。

#### 3.1.1. Project List

Project Listは全Project scopeの入口であり、Projectの一覧、登録、選択を扱う。

Projectを選択すると、以後のProject Management操作はSelected Project scopeへ移る。Analysis Workspace内でCurrent Projectを不用意に切り替えるのではなく、Project変更はProject Management側のProject selectionをauthorityとする。

#### 3.1.2. Selected Project

Selected Projectは、単一Projectに属するresourceの管理scopeである。

```text
Selected Project
├─ Overview / Project Info
├─ Research Context
├─ Data
└─ Results / Lineage
```

Project metadata、Research Context、Dataset / Analysis View、persisted result / artifact / lineageを、それぞれ異なるresponsibilityへ分離する。

##### 3.1.2.1. Overview / Project Info

Overview / Project Infoは、Project identity、metadata、status、archive等、Project自体のlifecycleを扱う。

DatasetやAnalysis ViewのlifecycleをProject metadata responsibilityへ混在させない。

##### 3.1.2.2. Research Context

Research Contextは、問題、Research Question、Hypothesis、decision context等をversioned resourceとして保持し、分析結果が「何に答えるためのものか」を追跡可能にする。

Research Contextの作成・改訂・固定・履歴確認等のlifecycle authorityはProject Managementに置く。Analysis Workspaceでは、その中から現在の分析に用いるActive Research Contextをanalysis contextとして参照する。

##### 3.1.2.3. Data

Dataは、Dataset、Dataset Version、Schema / Preview、Analysis View等、versioned analysis inputのlifecycleを扱う。

Dataset Versionは分析入力の固定snapshotを表す。Analysis Viewはfilter、列選択、derived column、missing-value policy等、分析に使用する論理viewをversionedに表す。

Analysis ViewはExploratory固有objectではなく、Exploratory / Causal / Predictiveで共有可能なFamily横断analysis inputである。create / edit / version management authorityはProject Management / Dataに置く。

##### 3.1.2.4. Results / Lineage

Results / Lineageは、persisted cross-analysis result、comparison、Artifact、Lineage、Annotation等をProject scopeで横断的に扱う。

Analysis Workspaceがexecution-local / stage-local result presentationを担うのに対し、Results / Lineageは分析をまたいで保存・比較・追跡するevidence surfaceを担う。

Family横断統合のために共通表現を設ける場合も、Predictive metricとCausal effectを同じ`score`へ平坦化するような共通化は行わない。

### 3.2. Analysis Workspace

Analysis Workspaceは、Current Projectに属するanalysis contextの下で、Exploratory / Causal / Predictiveの分析を実行・閲覧するworkspaceである。

```text
Analysis Workspace
├─ Analysis Context
└─ Analysis
    ├─ Exploratory
    │   └─ Stage
    ├─ Causal
    │   └─ Stage
    └─ Predictive
        └─ Stage
```

Analysis WorkspaceはProject resourceのlifecycle ownerではない。Project Managementで管理されたresourceをanalysis input/contextとして利用し、analysis execution / presentationに責務を限定する。

#### 3.2.1. Analysis Context

Analysis Contextはnavigation itemではなく、現在のanalysis input/contextを明示する領域である。

```text
Analysis Context
├─ Current Project
├─ Active Research Context
├─ Dataset Version
└─ Analysis View
```

##### 3.2.1.1. Current Project

Current Projectはcanonical Analysis routeの`project_id`から決まるanalysis scopeであり、Analysis Workspace内ではread-onlyとする。

別Projectへ移る場合はProject Management / Project Listへ戻ってProjectを選択する。

##### 3.2.1.2. Active Research Context

Active Research ContextはCurrent Projectに属するResearch Contextのうち、現在の分析で参照するversioned contextである。

Research Context自体のlifecycleはProject Managementが所有し、Analysis Workspaceではanalysis input/contextとして選択・参照する。

##### 3.2.1.3. Dataset Version

Dataset VersionはCurrent Projectに属する固定analysis input snapshotである。

Dataset Version変更時は、現在選択中のAnalysis Viewが新しいDataset Versionと互換かを確認し、互換でなければAnalysis View selectionを解除する。

##### 3.2.1.4. Analysis View

Analysis ViewはDataset Version上の論理analysis viewであり、Family横断で利用するversioned analysis inputである。

Analysis Workspaceでは既存Analysis Viewをcurrent inputとして選択・参照する。Analysis Viewのcreate / edit / version managementはProject Management / Dataが所有する。

Analysis Contextの有効なselectionを復元できない場合、架空のdefault resourceを生成しない。必要inputが不足するoperationはunavailableとして表現し、context不足だけを理由にFamily / Stage routeを書き換えない。

#### 3.2.2. Analysis

Analysisは、Analysis Contextの下でanalytical perspectiveを選び、そのFamily内部のwork/view contextを通じて分析を実行・閲覧する領域である。

```text
Analysis
├─ Exploratory
│   └─ Stage
├─ Causal
│   └─ Stage
└─ Predictive
    └─ Stage
```

##### 3.2.2.1. Analysis Family

FamilyはAnalysis Workspace内のanalytical capability contextを表すfirst-classなapplication conceptである。

現行の対象Familyは次の3つである。

- `Exploratory`
- `Causal`
- `Predictive`

Familyは単なるmenu groupではなく、「何を知ろうとしているか」というanalytical perspectiveを表す。各Familyが扱う分析目的および具体Stageの意味は`6. Analysis Families`で定義する。

##### 3.2.2.2. Navigation Stage

Navigation Stageは、選択中Familyの中でユーザーが現在行う・見る主要なwork/view contextを表す。

具体的な`Profile`, `Discovery`, `Metrics`, `Estimation`等のStage taxonomy、label、order、default StageはFamilyに対応するCapabilityが所有する。

Navigation Stageはwizard stepではない。Stageの並び順は表示順であり、原則としてruntime dependencyや必須progressionを意味しない。また、Navigation Stageをbackend executionのStageと同一視しない。

###### 3.2.2.2.1. Stage Contents

Stage Contentsは、Current Family / Navigation Stageに対応するanalysis surfaceを表示し、analysis execution、操作、stage-local result presentationを行うmain areaである。

既存のExploratory / Causal / Predictive analytical capabilityは、Family / Stage structureの導入を理由に簡略化・削除せず、適切なStage Contentsへ配置する。

persisted cross-analysis result、comparison、Artifact、Lineage、Annotationの横断閲覧・管理はProject Management / Results / Lineageが担う。

## 4. 基本設計原則

### 4.1 FamilyとNavigation Stageを別dimensionとして扱う

FamilyはAnalysis Workspace内のanalytical context、Navigation StageはFamily-local contextである。両者を同じ階層のmenu itemとして混在させない。

### 4.2 concrete StageはCapabilityが所有する

Family-specificなStage taxonomy、Stage label、Stage order、default Stage、各Stageで提供する機能は、そのFamilyを担うCapability側で定義する。

product/application共通層は、Familyがあること、FamilyごとにStageがあること、現在Family/Stageがあることを扱うに留める。

### 4.3 Navigation StageとExecution Stageを別責務とする

Navigation Stageはapplication/navigation concernであり、Execution Stageはruntime concernである。

Navigation Stageの追加・名称変更・再配置だけを理由に、runner、dependency DAG、retry、attempt、execution status等のruntime semanticsを変更しない。

### 4.4 existing analytical capabilityを保持して再配置する

Family / Stage構造の導入を理由に、既存分析機能を簡略化・削除しない。特にPredictiveの既存設定項目は全量保持を前提とする。

### 4.5 Family間の意味論を無理に統一しない

FamilyごとにStage数・名称・内部構造が異なってよい。共通taxonomyへ揃えるためのdummy Stageを作らない。

## 5. Navigation concept

### 5.1 Top-level navigation scope

Ariadneは`Project Management`と`Analysis Workspace`を異なるnavigation scopeとして扱う。

```text
Application Navigation
├─ Project Navigation
└─ Analysis Navigation
```

Project resource lifecycleとanalysis paradigm / workflow presentationを同一navigation hierarchyへ戻さない。

### 5.2 Project Management navigation

Project Managementは次のfunctional destinationを持つ。

- Project List / New Project
- Overview
- Research Context
- Data
- Results / Lineage

Selected ProjectのProject-local navigationはOverview / Research Context / Data / Resultsを持つ。Project metadata / archiveはOverview、Dataset / Analysis View lifecycleはDataが所有する。

### 5.3 Analysis Workspace navigation

Analysis WorkspaceではFamilyとFamily-local Navigation Stageを別dimensionとして提示する。

```text
Analysis Context
      ↓
Family
      ↓
Navigation Stage
      ↓
Stage Contents
```

Family選択はanalytical perspectiveの切替であり、Project、Research Context、Dataset Version、Analysis View等のanalysis contextを不必要に失わせない。

Family切替時はFamily Capability catalogが宣言するdefault Stageへ遷移する。Frontendに別のhard-coded default mappingを持たせない。

### 5.4 Analysis Context selection

Current Projectはread-onlyであり、routeの`project_id`をauthorityとする。

Research Context、Dataset Version、Analysis Viewはcurrent Projectに整合する既存resourceから選択する。Dataset Version変更時に選択済みAnalysis Viewが互換でない場合はAnalysis View selectionを解除する。

context selectionが不足してもFamily / Stage route自体を書き換えない。必要inputが不足するoperationはunavailable stateとして表現する。

### 5.5 Browser navigation

Project navigationとAnalysis navigationはいずれもroute-backedとし、direct link / reload / Back / Forwardでdeterministicに復元できることを基本とする。

Supported legacy analytical entryはcanonical Analysis routeへ一方向normalizeし、parallel navigation authorityとして維持しない。

## 6. Analysis Families

本章は、`3.2.2 Analysis`で定義したIA上の配置を繰り返すための章ではなく、各Analysis Familyが**何を知るための分析観点であり、各Navigation Stageがどの分析責務を担うか**を定義する。Family / Stageのapplication上の所属・階層は`3.2.2 Analysis`をauthorityとする。

### 6.1 Exploratory Family

Exploratoryは、データの構造、品質、分布、関係、比較を理解し、後続の問いや仮説を形成するための分析観点である。

探索は線形workflowにならないため、Stageは実行順ではなく探索観点で構成する。

```text
Exploratory
├─ Profile
├─ Data Quality
├─ Distribution
├─ Relationships
├─ Comparison
└─ Findings
```

#### 6.1.1 Profile

Dataset全体のshape、schema、type、cardinality、summary statistics、metadataを把握する。

#### 6.1.2 Data Quality

missing、duplicate、outlier candidate、invalid value、unexpected category、coverage等を確認する。

#### 6.1.3 Distribution

主に単変量分布を扱う。histogram、density、quantile、category frequency等はDistributionを表現するvisualization techniqueである。

#### 6.1.4 Relationships

scatter、correlation、cross-tab、grouped distribution等を通じて変数間関係を探索する。関連を因果効果として解釈しない。

#### 6.1.5 Comparison

segment、group、cohort、region、before/after等の条件間比較を扱う。

#### 6.1.6 Findings

探索結果を後続分析や意思決定で参照できるfinding/evidenceとして整理するための接続点とする。ただし、専用persistent `Finding` resourceの新設を前提としない。

#### 6.1.7 Visualizationの位置づけ

Visualizationは分析観点ではなく表現手段であるため、独立Navigation Stageにはしない。

### 6.2 Causal Family

Causalは、介入した場合の変化を扱うため、仮定、識別、推定、診断、感度分析を明確に分ける。

```text
Causal
├─ Setup
├─ Discovery
├─ Identification
├─ Estimation
├─ Effects
├─ Diagnostics
└─ Sensitivity
```

#### 6.2.1 Setup

Dataset、treatment、outcome、covariates候補、population、time window、estimand等の分析条件を扱う。

#### 6.2.2 Discovery

DAG、candidate confounder、mediator、collider、temporal ordering、domain assumption等、構造・分析設計を検討する。

#### 6.2.3 Identification

観測データと仮定のもとで目的estimandが識別可能か、どのstrategy/adjustment setを用いるかを扱う。

#### 6.2.4 Estimation

識別されたestimandを有限標本からどのように推定するかを扱う。

#### 6.2.5 Effects

ATE、ATT、CATE、subgroup effects、interval等、推定されたcausal effectの閲覧・利用を扱う。

#### 6.2.6 Diagnostics

balance、overlap、positivity、effective sample size、weight distribution、pre-trend等、推定の妥当性を確認する。

#### 6.2.7 Sensitivity

unmeasured confounding、alternate adjustment set、estimator、window、trimming等への依存性を確認する。

IdentificationとEstimationは異なる科学的問いであり、同一Stageへ統合しない。

### 6.3 Predictive Family

Predictiveは、未知・将来の値やclassを予測するmodelの設定、学習、予測、評価、説明、資産確認を扱う。

```text
Predictive
├─ Setup
├─ Train
├─ Predict
├─ Metrics
├─ Explainability
└─ Model Management
```

#### 6.3.1 Setup

目的変数、feature/input、split、実行条件等の設定を扱う。既存Predictive UIで提供される設定項目は保持する。

#### 6.3.2 Train

model training / training runを扱う。

#### 6.3.3 Predict

学習済みmodelを用いたprediction contextを扱う。新しいstandalone scoring engineの導入を意味しない。

#### 6.3.4 Metrics

RMSE、MAE、AUROC、AUPRC、precision/recall、calibration等、predictive performanceを評価する。

#### 6.3.5 Explainability

feature importance、permutation importance、SHAP、PDP/ICE、local explanation等、モデル挙動の解釈を扱う。Predictive explanationをcausal effectとして扱わない。

#### 6.3.6 Model Management

現行scopeでは、fitted model、model card、artifact、lineage等の確認を中心とする。新しいmodel registry/lifecycle platformの導入は別途設計判断とする。

## 7. Evidence integration concept

### 7.1 Family横断の接続点

同一Research Topicについて、Exploratory finding、Predictive result、Causal effectを相互参照可能にし、意思決定時に根拠を辿れることを目指す。

```text
Research Question / Decision
        │
        ├─ Exploratory Findings
        ├─ Predictive Results
        └─ Causal Effects
                 ↓
          Evidence / Lineage
```

### 7.2 共通化の限界

共通化する場合は、lineage、analysis family、method、status、artifact等の共通envelopeと、Family-specific typed payloadを分ける方向を優先する。

Family-specific semanticsを失う共通`score`や単一result typeへの平坦化は行わない。

## 8. 今後の拡張予定

### 8.1 Flagship / 看板画面

将来的には、Research Question / Decision Contextを中心に各Familyのevidenceを横断表示するworkspaceを検討する。

これはExploratory / Predictive / Causalと同列のanalytical Familyではなく、Project-global surfaceとして扱う方向を優先する。

### 8.2 External analytical engine

LightGBM、DoWhy、EconML等のexternal analytical engineは、Family / Stage application modelとは独立して追加可能なadapterとして扱うことを目指す。

#### 8.2.1 現行scopeで導入しない理由

- application model / navigation / capability responsibilityの確立とengine追加を同時に行うと、責務と検証範囲が混線する。
- Family / Stage modelが安定した後にengineを追加する方が、architecture extensibilityを検証しやすい。
- engine追加を理由にFamily / Stage abstractionを再変更しない構造を先に成立させる。

#### 8.2.2 拡張イメージ

```text
Predictive Capability
 └─ LightGBM adapter

Causal Capability
 ├─ DoWhy adapter
 └─ EconML estimator adapter
```

### 8.3 Analysis Result / Finding domainの拡張

Family横断のevidence利用が成熟した段階で、共通envelope、typed payload、Finding/Evidenceのdomain modelを再評価する。

## 9. 現行スコープ境界

Current product contractでは次を含む。

- Project Management / Analysis Workspaceのresponsibility separation
- Project routesとAnalysis routeのroute-backed navigation
- Analysis Contextの明示
- Exploratory / Predictive / CausalのFamily navigation
- selected Familyに応じたNavigation Stage navigation
- Capability ownershipの明確化
- Navigation StageとExecution Stageの責務分離
- existing analytical capabilityのStage Contentsへの配置
- Result / Artifact / Lineageを用いたcross-analysis evidence追跡

次はcurrent product concept上の必須scopeに含めない。

- LightGBM / DoWhy / EconML等の特定external analytical engineの必須導入
- Navigation taxonomyだけを理由とするruntime execution architecture再構築
- Navigation stateまたはAnalysis Context専用resourceのDB永続化
- 新しいgeneral-purpose Finding/Evidence persistent model
- Family間のStage taxonomy統一
- UI taxonomyを埋める目的だけのbackend operation新設

Project/Analysis IAの都合だけを理由に、既存API、persistence schema、backend analysis/domain semanticsを変更しない。

## 10. プロダクト成功条件

1. ユーザーがProject resource管理とanalysis execution/presentationを別responsibilityとして認識できる。
2. Project ManagementのOverview / Research Context / Data / Resultsのownershipが明確である。
3. Analysis WorkspaceでCurrent Project / Research Context / Dataset Version / Analysis Viewをanalysis contextとして確認できる。
4. ユーザーが現在のanalytical FamilyとFamily内の作業文脈を別dimensionとして認識できる。
5. Familyを切り替えてもProject / Research Context / Dataset / Result lineageが同一Project境界で追跡できる。
6. Family-specific analytical semanticsが保たれる。
7. UI/navigation変更がCLI/library/runtime execution semanticsへ不要に波及しない。
8. Project routeとAnalysis routeがdirect link / reload / Back / Forwardでdeterministicに復元できる。
9. 将来engineやStageを追加してもapplication-levelのFamily / Stage abstractionを再設計せず拡張できる。

## 11. 用語

| 用語 | 意味 |
| --- | --- |
| Project Management | Project resource / versioned analysis inputの作成・管理を担うapplication surface |
| Analysis Workspace | current Project contextの下でanalysis execution / presentationを行うapplication surface |
| Analysis Context | Current Project / Active Research Context / Dataset Version / Analysis Viewの組 |
| Family | Analysis Workspace内のanalytical context / analytical capability context |
| Navigation Stage | Family-localな主要work/view context |
| Stage Contents | selected Family / Navigation Stageに対応するanalysis operation/result presentation領域 |
| Execution Stage | backend runtimeが実行・依存・attempt/statusを管理する処理単位 |
| Capability | Family-specificな分析機能、Stage catalog、use caseを所有するsoftware responsibility |
| Project | Research Topicと分析資産の権限・来歴境界 |
| Result | analysis executionまたはstage executionから生成される分析結果 |
| Artifact | sourceまたはexecution/resultに紐づくfile/object asset |
| Lineage | Resource間の来歴・根拠関係 |

## 20. CHANGE LOG

### 20.4 ENH-E4 Canonical Execution Architecture

Execution authority、Execution Plan、Stage Execution、Result/Artifact/Lineage等のcanonical execution architectureを現行プロダクト構造として継承する。

### 20.5 ENH-E5 Family × Navigation Stage Application Architecture

analytical capabilityをExploratory / Predictive / CausalのFamilyとFamily-owned Navigation Stageで再構成し、application/navigation concernをruntime execution concernから分離する変更を追加する。


### 20.6 ENH-E7 Project Management / Analysis Workspace Responsibility Separation

Project resource managementとanalysis execution/presentationを別surface・別navigation scopeへ分離し、Analysis Context、Project route、surface ownershipをcurrent product conceptへ統合した。
