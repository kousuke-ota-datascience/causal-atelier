# ENH-E7 Handoff — Project Management / Analysis Workspace IA Redesign

## 1. 対象

- Enhancement: **ENH-E7**
- Branch: `feature/ariadne_mvp_e7`
- Repository:
  `https://github.com/kousuke-ota-datascience/causal-atelier/tree/feature/ariadne_mvp_e7`
- 次スレッドの目的:
  1. 画面構成・UI挙動の詳細化
  2. ENH-E7 Enhancement計画の策定
  3. Acceptance Criteria / Gate / Test計画への展開

---

## 2. 背景

ENH-E6でAnalysis Family / Stage navigationを導入したが、実際に画面を操作すると、現行UIでは以下が同時に存在し、navigation hierarchyが重複している。

- Global sidebar
  - Explore & Visualize
  - Causal Discovery
  - Causal Inference
  - Predictive
- Analysis Family tabs
  - Exploratory
  - Causal
  - Predictive
- Analysis Stage tabs

結果として、Project管理機能とAnalysis Family / Stageが同じnavigation hierarchy上に混在している。

ENH-E7では、この問題をCSS調整ではなく、**Top-level Information Architectureの再編**として扱う。

---

## 3. ENH-E6からの既知事項

ENH-E6のFamily/Stage navigation自体は実装済み。

Canonical analysis route:

```text
/projects/{project_id}/analysis/{family}/{stage}
```

Family:

```text
Exploratory
Causal
Predictive
```

Stage catalog:

```text
Exploratory
├─ Profile
├─ Data Quality
├─ Distribution
├─ Relationships
├─ Comparison
└─ Findings

Causal
├─ Setup
├─ Discovery
├─ Identification
├─ Estimation
├─ Effects
├─ Diagnostics
└─ Sensitivity

Predictive
├─ Setup
├─ Train
├─ Predict
├─ Metrics
├─ Explainability
└─ Model Management
```

ENH-E6後の手動確認でFamily tabsが表示されなかった問題については、frontend bugではなくdefault runtimeのAPI build不整合が原因と判明した。

```text
main stack:
  /api/v1/navigation/analysis → 404

E2E stack:
  /api/v1/navigation/analysis → 200
```

main API rebuild/recreate後は3 Family catalogを正常取得できている。

したがって、このruntime version skew問題とENH-E7のIA redesignは別問題として扱う。

---

## 4. 採用するTop-level IA

Ariadneを大きく2つのworkspaceへ分離する。

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

設計原則:

> Project ManagementではProject resourceを管理する。  
> Analysis Workspaceでは、選択されたProject / Research Context / Dataset / Analysis Viewを入力contextとして分析を実行する。

---

## 5. Project Management

### 5.1 階層

採用済みの構造:

```text
Projects
│
├─ Project List
│    │
│    └─ Projectを選択
│
└─ Selected Project: SALES dataset
     │
     ├─ Overview / Project Info
     ├─ Research Context
     ├─ Data
     └─ Results / Lineage
```

`Project List` は全Project scope。

`Overview / Research Context / Data / Results` はselected Project scope。

両者を同一階層として扱わない。

---

### 5.2 暫定URL

```text
/projects
    Project List

/projects/new
    New Project

/projects/{project_id}
    Overview / Project Info

/projects/{project_id}/context
    Research Context

/projects/{project_id}/data
    Data

/projects/{project_id}/results
    Results / Lineage
```

SPAのままrouteを分離する想定。物理的なHTML分割は現時点では要求しない。

---

### 5.3 既存機能の移設先

```text
Project List
    → /projects

Project Register
    → /projects/new

Project metadata edit
Project archive
    → /projects/{id}

Research Context
Context DRAFT / FIXED
Context history
Related Analysis
    → /projects/{id}/context

Dataset Register
Registered Dataset
Schema / Preview
Analysis View management
    → /projects/{id}/data

Cross-analysis Results
Result filter
Result comparison
Artifacts
Lineage
Annotation
    → /projects/{id}/results
```

特に、現行の `Project / Data` workspaceは分割する。

```text
Overview / Project Info
    → Project metadata

Data
    → Dataset + Analysis View
```

Analysis ViewはExploratory固有機能ではなく、Family横断で利用するversioned analysis inputとして扱う方向。

---

## 6. Analysis Workspace

### 6.1 基本レイアウト

目標イメージ:

```text
┌────────────────────────────────────────────────────────────────┐
│ Current Project │ Research Context │ Dataset │ Analysis View   │
│ SALES dataset   │ [ ▼ ]            │ [ ▼ ]   │ [ ▼ ]           │
│                                           [Project Management] │
├────────────────────────────────────────────────────────────────┤
│ [ Exploratory ] [ Causal ] [ Predictive ]                     │
├───────────────────┬────────────────────────────────────────────┤
│ [ Stage 1 ]       │                                            │
│ [ Stage 2 ]       │                                            │
│ [ Stage 3 ]       │              Stage Contents                │
│ [ Stage 4 ]       │                                            │
│ [ Stage 5 ]       │                                            │
└───────────────────┴────────────────────────────────────────────┘
```

Family:

- 上部横タブ

Stage:

- Family配下の左縦navigation

Stage Contents:

- 右側main area

---

### 6.2 Analysis Context

画面上部に以下を置く。

```text
Current Project
Active Research Context
Dataset Version
Analysis View
```

役割はnavigationではなく、**現在のanalysis input/context表示・選択**。

Current Projectについては、Analysis中に不用意にProjectを切り替えない設計も候補。

その場合:

```text
Current Project
    → read-only

Project変更
    → Project Management / Project List
```

としてもよい。

この詳細挙動はENH-E7設計時に確定する。

---

### 6.3 Analysis URL

ENH-E6のcanonical URLを維持する。

```text
/projects/{project_id}/analysis/{family}/{stage}
```

例:

```text
/projects/123/analysis/exploratory/profile
/projects/123/analysis/causal/discovery
/projects/123/analysis/causal/estimation
/projects/123/analysis/predictive/metrics
```

Family切替時はFamily default Stageへ遷移する現行semanticsを基本維持する。

---

## 7. 旧Global Sidebar

現行sidebar:

```text
Project Management
Research Context
Project / Data
Explore & Visualize
Causal Discovery
Causal Inference
Predictive
Results / Lineage
```

は抽象レベルが混在しているため、新IAでは廃止方向。

再配置:

```text
Project Management
Research Context
Project / Data
Results / Lineage
    → Project Management側

Explore & Visualize
    → Exploratory Family

Causal Discovery
Causal Inference
    → Causal Family / Stage

Predictive
    → Predictive Family
```

最終的には、各概念がnavigationに一度だけ現れる構造を目指す。

---

## 8. Legacy route compatibility

既存URLは即削除せず、canonical analysis URLへnormalizeする方向。

例:

```text
/projects/{id}/explore
    → /projects/{id}/analysis/exploratory/profile

/projects/{id}/causal
    → /projects/{id}/analysis/causal/discovery

/projects/{id}/predictive
    → /projects/{id}/analysis/predictive/setup
```

既存bookmark / deep link / compatibility entryを壊さないこと。

---

## 9. Stage Contentsの初期方針

ENH-E7初期実装では、全Stage contentを完全再設計しない。

まず以下を優先する。

```text
1. Project ManagementとAnalysis Workspaceを分離
2. 新しいtop-level routingを成立させる
3. Family横タブを配置
4. Stage縦navigationを配置
5. 既存workspace/surfaceをStage Contents領域へ移す
6. 実際に操作
7. 操作時の違和感を基にStage単位の再分割を行う
```

「実物を触らないと気づけない違和感」があることを前提に、初回実装では過剰に細部を固定しない。

---

## 10. 現時点のStage mapping案

### Causal

```text
Setup
    causal question / design preparation
    Direct Graph Registration

Discovery
    Discovery specification
    PC / GES
    Graph Candidates
    Graph comparison/edit/adopt/fix

Identification
    Identification inputs
    Data Eligibility
    Gate

Estimation
    estimator selection
    override
    execution / revision

Effects
    Treatment Effect Results
    result comparison

Diagnostics
    diagnostics
    scientific warnings

Sensitivity
    Refutation
    Sensitivity analysis
```

Causalは既存Discovery / Inference surfaceをStage単位へ分解する方向。

---

### Predictive

```text
Setup
Train
Predict
Metrics
Explainability
Model Management
```

注意:

Predictive Stageは独立execution stepではなく、原則として**同一Predictive Executionのpresentation/navigation view**として扱う。

現行のPrediction Task → Split → Training → Evaluation → Explanation → Model CardというExecution semanticsを壊さない。

---

### Exploratory

```text
Profile
Data Quality
Distribution
Relationships
Comparison
Findings
```

現行operationとの暫定mapping:

```text
PROFILE
    → Profile

DISTRIBUTION
    → Distribution

ASSOCIATION
    → Relationships

GROUP_SUMMARY
    → Comparison

Saved Exploratory Results
    → Findings
```

`Data Quality`, `TIME_TREND`, `CHART`等の詳細配置はENH-E7設計時の残論点。

---

## 11. ENH-E7で避けること

初期段階では以下を一括で行わない。

- 全分析画面の全面的なUI再設計
- backend analysis semanticsの変更
- Predictive Execution modelの変更
- Family/Stage taxonomyそのものの大幅変更
- Results domain modelの再設計

ENH-E7の第一目的は、

> **navigation / workspace IAを正しい階層へ再配置し、既存機能をその構造上で操作可能にすること**

とする。

---

## 12. 次スレッドで決める事項

次スレッドでは最低限、以下を確定する。

### UI / UX

- Project Managementの具体的layout
- Project List → Selected Project遷移
- Analysis Workspace context bar
- Current Projectをread-onlyにするか
- Family tabのサイズ・配置
- Stage sidebarの幅・selected state
- Stage Contentsのscroll behavior
- Project Management ↔ Analysis Workspaceの遷移
- empty state / Project未選択時
- responsive behavior

### Routing

- `/projects/new` の扱い
- `/projects/{id}` default page
- Analysis Workspaceへのdefault entry
- legacy route normalization
- Back / Forward / reload semantics

### Functional migration

- 各existing DOM/form/result surfaceの移設先
- Stage間で共有するUI
- Analysis View管理の正式な移設先
- Result/LineageとAnalysis Workspaceの関係

### Enhancement Planning

- Goal / Non-goal
- Gate分割
- Acceptance Criteria
- Regression protection
- Browser E2E journeys
- migration order
- rollback / compatibility strategy

---

## 13. 実装分割の暫定案

詳細計画策定前のたたき台:

```text
G01
Top-level routing + Project Management separation

G02
Analysis Workspace shell
- Analysis Context bar
- Family tabs
- vertical Stage navigation

G03
Causal surface migration

G04
Exploratory / Predictive surface migration

G05
legacy navigation removal / compatibility / regression
```

このGate構成は未確定。次スレッドで変更可。

---

## 14. 設計上の中心原則

ENH-E7で常に維持する原則:

```text
Project Management
    = Project resourceを管理する場所

Analysis Workspace
    = Project contextの下で分析する場所

Family
    = Analysis paradigm

Stage
    = Family内部のworkflow/view

Operation
    = Stage内部で実行する処理
```

異なる抽象レベルの概念を同じnavigation hierarchyへ戻さないこと。

---

## 15. Starting Point

次スレッドでは、このhandoffを前提として、

> 「ENH-E7の画面詳細化とEnhancement計画を作成する」

ところから開始する。

IAの大枠については合意済みとして扱い、重大な矛盾が見つからない限り再議論から始めない。