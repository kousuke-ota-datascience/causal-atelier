# 00 プロダクトコンセプトメモ

- 文書状態: `DRAFT_FOR_REVIEW`
- 文書種別: 現行プロダクト構想のeffective snapshot
- 対象プロダクト: Ariadne
- 対象分析Family: Exploratory / Predictive / Causal
- 下位文書: `10_requirements_definition.md`, `21_logical_data_design.md`, `22_product_basic_design.md`, `23_api_interface_design.md`, `30_detailed_design.md`

> 本書は、過去Enhancementを知らない読者が、Ariadneをどのような分析プロダクトとして構成するかを理解できることを目的とする。変更履歴は後段へ分離し、本文は現在有効なプロダクト構想を記述する。

## 1. Ariadneのプロダクト像

Ariadneは、単一の分析手法を実行する画面ではなく、同一のResearch Topic / Decision Contextに対して、異なる分析観点を往来しながらエビデンスを形成するanalytical workspaceである。

中心となる利用単位はProjectである。Projectは、問い、入力データ、分析仕様、実行、結果、artifact、判断根拠を同一の来歴境界の中で扱う。

```text
Project / Research Topic
        │
        ├─ Research Context
        ├─ Dataset / Analysis View
        ├─ Analytical Families
        │    ├─ Exploratory
        │    ├─ Predictive
        │    └─ Causal
        └─ Result / Artifact / Lineage / Annotation
```

Ariadneが目指すのは、Exploratory、Predictive、Causalを同一意味に平坦化することではない。それぞれが答える問いと成立条件を保持したまま、同一Projectの中で相互参照可能にすることである。

## 2. 分析プロダクトとして解く問題

### 2.1 分析観点と作業文脈を区別する

分析者は「どの分析観点で考えているか」と「その観点の中で何をしているか」を同時に扱う。

例えばPredictiveでは、モデル設定、学習、予測、性能評価、説明可能性、モデル資産確認は同じPredictiveという分析観点に属するが、作業・閲覧文脈は異なる。

Ariadneではこの2つを次のように分ける。

```text
Family = global analytical context
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

## 3. Analytical Workspace model

### 3.1 Project / Research Context

ProjectはResearch Topic、目的、意思決定文脈、分析資産の権限・来歴境界である。

Research Contextは、問題、Research Question、Hypothesis、decision context等をversioned resourceとして保持し、分析結果が「何に答えるためのものか」を追跡可能にする。

### 3.2 Dataset / Analysis View

Dataset Versionは分析入力の固定snapshotを表す。Analysis Viewは、filter、列選択、derived column、missing-value policy等、分析に使用する論理viewをversionedに表す。

分析Familyを切り替えても、同一ProjectのDataset / Analysis Viewを共有できることを基本とする。

### 3.3 Family

Familyはanalytical capability contextを表すfirst-classなapplication conceptである。

現行の対象Familyは次の3つである。

- `Exploratory`
- `Predictive`
- `Causal`

Familyは単なるmenu groupではなく、「何を知ろうとしているか」というanalytical perspectiveを表す。

### 3.4 Navigation Stage

Navigation Stageは、選択中Familyの中でユーザーが現在行う・見る主要なwork/view contextを表す。

抽象modelは薄く保つ。

```text
Family
 └─ Navigation Stage*
```

抽象層は具体的な`Discovery`, `Train`, `Metrics`, `Estimation`, `Distribution`等の意味論を知らない。具体StageはFamilyに対応するCapabilityが所有する。

Navigation Stageはwizard stepではない。Stageの並び順は表示順であり、原則としてruntime dependencyや必須progressionを意味しない。

### 3.5 Result / Artifact / Lineage

分析結果はProject内のResult / Artifact / Lineage等の既存資産として追跡可能にする。

Family横断統合のために共通表現を設ける場合も、Predictive metricとCausal effectを同じ`score`へ平坦化するような共通化は行わない。

## 4. 基本設計原則

### 4.1 FamilyとNavigation Stageを別dimensionとして扱う

Familyはglobal analytical context、Navigation StageはFamily-local contextである。両者を同じ階層のmenu itemとして混在させない。

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

### 5.1 Global analytical context

ユーザーはProject内で現在のFamilyを認識し、別Familyへ横断移動できる。

Family選択はanalytical perspectiveの切替であり、Project、Research Context、Dataset等のglobal project contextを失わせない。

### 5.2 Family-local work/view context

選択中Familyに応じて、そのFamilyが所有するNavigation Stageを提示する。

Stage navigationは主として「設定する」「実行する」「結果を見る」「妥当性を確認する」等の作業・閲覧文脈を整理する。

### 5.3 Project-global surface

次のようなProject-wideなsurfaceはanalytical Familyとは異なるdimensionである。

- Project Management
- Research Context
- Data / Dataset
- Results / Lineage
- global evidence / workspace surface

これらをExploratory / Predictive / Causalと同じanalytical Familyとして扱わない。

## 6. Analytical Families

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

## 9. 現在のEnhancementで扱う変更範囲

現在のEnhancementでは、次を対象とする。

- `Family -> Navigation Stage*` application modelの明確化
- Exploratory / Predictive / CausalのFamily navigation
- selected Familyに応じたStage navigation
- Capability ownershipの明確化
- Navigation StageとExecution Stageの責務分離
- route / deep link / browser historyの整理
- 既存Exploratory / Predictive / Causal surfaceの再配置
- Predictive既存設定項目の完全保持

次は対象外とする。

- LightGBM / DoWhy / EconMLの導入
- runtime execution architectureの再構築
- Navigation stateのDB永続化
- Overview / Flagshipの本実装
- 新しいgeneral-purpose Finding/Evidence persistence model
- Family間のStage taxonomy統一

## 10. プロダクト成功条件

1. ユーザーが現在のanalytical FamilyとFamily内の作業文脈を別dimensionとして認識できる。
2. Familyを切り替えてもProject / Research Context / Dataset / Result lineageが同一workspaceで追跡できる。
3. Family-specific analytical semanticsが保たれる。
4. UI/navigation変更がCLI/library/runtime execution semanticsへ不要に波及しない。
5. Predictive既存機能・設定が欠落しない。
6. 将来engineやStageを追加してもapplication-levelのFamily / Stage abstractionを再設計せず拡張できる。

## 11. 用語

| 用語 | 意味 |
| --- | --- |
| Family | global analytical context / analytical capability context |
| Navigation Stage | Family-localな主要work/view context |
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
