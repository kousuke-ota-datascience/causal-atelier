# ENH-E7 Enhance構想・要件改定計画

> 文書種別: Planning / Decision Artifact  
> Self-containment: MUST（当該文書の主題について本文内で完結） — 当該artifactの結論・effective contentを本文内に持つ。  
> Status: PLAN READY FOR 00-layer instantiation / IMPLEMENTATION NOT YET AUTHORIZED（実装未承認）  
> Enhancement: ENH-E7  
> Project: Ariadne  
> Branch: `feature/ariadne_mvp_e7`  
> 想定work root: `docs/wiki/develop_memo/_work/20260813_ENH-E7_project_analysis_workspace_separation/`

---

## 1. 問題定義

ENH-E7 は、現行 Ariadne UI において Project resource 管理と Analysis execution の navigation hierarchy が混在し、同一概念が複数の navigation surface に重複して現れている問題を、Top-level Information Architecture の再編として解消する Enhancement である。

現行 UI では概ね以下が同時に存在する。

- Global sidebar
  - Project Management
  - Research Context
  - Project / Data
  - Explore & Visualize
  - Causal Discovery
  - Causal Inference
  - Predictive
  - Results / Lineage
- Analysis Family navigation
  - Exploratory
  - Causal
  - Predictive
- Analysis Stage navigation

その結果、以下の異なる抽象レベルが同一 navigation hierarchy に混在している。

- Project lifecycle / resource management
- Analysis paradigm
- Analysis workflow / presentation stage
- Stage 内 operation

また、現行 `Project / Data` workspace では Project metadata と Dataset / Analysis View management が同一 surface に混在しており、Project resource の責務境界が曖昧である。

ENH-E7 では CSS 調整や sidebar の見た目変更として扱わず、次の責務分離を canonical design として成立させる。

```text
Project Management
    = Project resource を管理する場所

Analysis Workspace
    = Project context の下で分析する場所

Family
    = Analysis paradigm

Stage
    = Family 内部の workflow / presentation view

Operation
    = Stage 内で実行・表示する処理
```

異なる抽象レベルの概念を同一 navigation hierarchy に戻してはならない。

### 根拠・由来

- `ENH-E7 Handoff — Project Management / Analysis Workspace IA Redesign`
- ENH-E6 Family / Stage navigation implementation and PASS evidence
- current branch frontend source
- `docs/wiki/develop_memo/_work/agentic_enhancement_workflow_template/`

---

## 2. 今このEnhancementを行う理由

ENH-E6 により Analysis Family / Stage navigation 自体は導入済みであり、canonical analysis route も成立している。

```text
/projects/{project_id}/analysis/{family}/{stage}
```

しかし、実ブラウザで操作した結果、旧 Global sidebar の analytical navigation と新しい Family / Stage navigation が同時に表示され、navigation hierarchy が重複していることが明確になった。

この問題を放置すると、以下が継続する。

1. Project Management と Analysis execution の責務境界が UI 上で不明確。
2. 同じ Analysis concept が複数箇所の navigation に現れる。
3. 既存 surface を Family / Stage IA に適切に配置できない。
4. Project metadata / Dataset / Analysis View の ownership が曖昧なままになる。
5. 将来の UI enhancement が旧 navigation hierarchy と新 navigation hierarchy の双方に依存する。

したがって、ENH-E6 の Analysis navigation contract を保護したまま、その外側の application IA を ENH-E7 で整理する必要がある。

なお、ENH-E6 後に発生した `/api/v1/navigation/analysis` の runtime version skew は default runtime の API build 不整合であり、ENH-E7 の IA redesign とは別問題とする。ENH-E7 ではこの runtime deployment issue を product requirement に混在させない。

---

## 3. 現状の問題

### 3.1 Navigation scope の混在

現在は概念的に以下が同一 sidebar level に存在する。

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

一方 Analysis Workspace 側には既に以下が存在する。

```text
Family
├─ Exploratory
├─ Causal
└─ Predictive

Stage
└─ Family ごとの stage catalog
```

旧 analytical sidebar と新 Family / Stage navigation は責務が重複する。

### 3.2 Project metadata と Data management の混在

現行 `Project / Data` workspace は少なくとも以下を同一責務として扱っている。

```text
Project metadata
Dataset Register / Dataset management
```

ENH-E7 では次へ分割する必要がある。

```text
Overview / Project Info
    → Project metadata / lifecycle

Data
    → Dataset / Dataset Version / Schema / Analysis View
```

### 3.3 Analysis surface の配置未整理

ENH-E6 では Family / Stage navigation は成立したが、既存 Causal / Exploratory / Predictive surface のすべてが新 Stage Contents hierarchy に整理済みという意味ではない。

ENH-E7 では shell を作るだけでなく、既存機能を新 IA 上で実際に操作可能にする必要がある。

### 3.4 Workflow execution control の不足を再発させてはならない

ENH-E6 の planning / Coding Agent 起動準備では、以下の workflow control 上の問題が確認された。

- template 側 operator prompt を直接 Agent に渡すと Enhancement identity が一意に解決できない。
- Coding Agent が Gate 06 / 07 / P00 / 他 Pxx など過剰な workflow context を仕様補完に利用しやすい。
- document compliance と Agent execution readiness が混同される。
- Enhancement-specific `agent_entry_prompts/` の instance 化が強制されていない。

ENH-E7 の計画では、これらを execution protocol に組み込み、Coding 開始条件として機械的に検査する。

---

## 4. 目標状態

### 4.1 Canonical Top-level IA

```text
Ariadne
│
├─ Project Management
│   │
│   ├─ Projects
│   │   ├─ Project List
│   │   └─ New Project
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

### 4.2 Canonical Project routes

```text
/projects
    Project List

/projects/new
    New Project

/projects/{project_id}/overview
    Overview / Project Info

/projects/{project_id}/context
    Research Context

/projects/{project_id}/data
    Data

/projects/{project_id}/results
    Results / Lineage
```

Short route:

```text
/projects/{project_id}
```

は canonical route:

```text
/projects/{project_id}/overview
```

へ history replace semantics で normalize する。

### 4.3 Canonical Analysis route

ENH-E6 の canonical route を維持する。

```text
/projects/{project_id}/analysis/{family}/{stage}
```

resource route が既存 contract として存在する場合も維持する。

Family 切替時は、existing analysis navigation catalog の `default_stage_id` を authority とする。Frontend 内に別の hard-coded default mapping を増やさない。

### 4.4 Project Managementの機能ownership

#### `/projects`

```text
Project List
Project selection
New Project entry
```

#### `/projects/new`

```text
Project Register
```

作成成功時:

```text
/projects/new
    ↓
/projects/{new_project_id}/overview
```

#### `/projects/{id}/overview`

```text
Project metadata
Project identity
Project status
Project archive
```

Project Archive は selected Project に対する lifecycle operation とし、Overview scope に所属させる。

#### `/projects/{id}/context`

```text
Research Context
Context DRAFT / FIXED
Context history
Related Analysis
```

既存 DRAFT / FIXED semantics は変更しない。

#### `/projects/{id}/data`

```text
Dataset Register
Registered Dataset
Dataset Version
Schema / Preview
Analysis View management
```

Analysis View は Exploratory 固有 object とせず、Family 横断の versioned analysis input として扱う。

```text
Project
  └─ Dataset Version
       └─ Analysis View
            ├─ Exploratory
            ├─ Causal
            └─ Predictive
```

Analysis View の管理 authority は Project Management / Data に置く。

#### `/projects/{id}/results`

```text
Cross-analysis Results
Result filter
Result comparison
Artifacts
Lineage
Annotation
```

責務境界:

```text
Analysis Workspace
    = execution-local / stage-local presentation

Results / Lineage
    = persisted cross-analysis aggregation
      + comparison
      + artifacts
      + lineage
      + annotation
```

### 4.5 Analysis Context

Analysis Workspace 上部には以下を置く。

```text
Current Project
Active Research Context
Dataset Version
Analysis View
```

これらは navigation item ではなく current analysis input/context とする。

依存関係は概念的に以下。

```text
Current Project
    ↓
Active Research Context
    ↓
Dataset Version
    ↓
Analysis View
```

#### Current Project

Current Project は read-only とする。

Project は canonical Analysis URL の `project_id` により決定する。

Analysis Workspace 内で別 Project へ直接切り替えない。Project を変更する場合は Projects / Project Management へ戻り、別 Project を選択する。

#### Active Research Context

Current Project に所属する既存 Research Context から選択する。

Research Context を変更しても Family / Stage route は維持する。

#### Dataset Version

Current Project に所属する Dataset Version から選択する。

Dataset Version を変更しても Family / Stage route は維持する。

選択済み Analysis View が新 Dataset Version と互換でない場合は Analysis View selection を解除する。

#### Analysis View

選択済み Dataset Version に所属する Analysis View を current analysis input として選択する。

Analysis Workspace では Analysis View の input selection を行い、create/edit/version-management authority は Project Management / Data に置く。

#### 復元方針

Project は URL から復元する。

Research Context / Dataset Version / Analysis View は existing persisted/workspace-state mechanism から対象 Project と整合する値だけを復元する。

有効な値を復元できない場合、ENH-E7 固有の架空 default resource は新設せず unselected とする。必要 input が不足する operation は execution unavailable state を表示する。

context selection 不足だけを理由に Family / Stage route を書き換えない。

### 4.6 Analysis Workspaceのlayout

```text
┌──────────────────────────────────────────────────────────────┐
│ Current Project | Research Context | Dataset | Analysis View │
│                                      [Project Management]    │
├──────────────────────────────────────────────────────────────┤
│ Exploratory | Causal | Predictive                            │
├──────────────────┬───────────────────────────────────────────┤
│ Stage navigation │ Stage Contents                            │
│                  │                                           │
└──────────────────┴───────────────────────────────────────────┘
```

- Family = 上部横 navigation
- Stage = 左縦 navigation
- Stage Contents = 右 main area
- active Family / Stage は selected state を持つ
- pixel-level styling は ENH-E7 Gate contract の主目的としない
- 実装後の実機操作で見つかる UI 違和感は、semantic contract を変えない範囲で follow-up 調整可能とする

### 4.7 既存Analysis surfaceの移設

G02 は Analysis shell が表示されるだけでは PASS としない。

既存 Causal / Exploratory / Predictive surface が、新しい Stage Contents 上から操作可能であることを要求する。

#### Causal

```text
Setup
    causal question / design preparation
    Direct Graph Registration

Discovery
    Discovery specification
    PC / GES
    Graph Candidates
    Graph comparison / edit / adopt / fix

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

既存 Causal execution semantics は変更しない。

#### Exploratory

初期 mapping:

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

`Data Quality`, `TIME_TREND`, `CHART` の最終配置は Architecture / Design Revision で source を確認して freeze する。

この計画段階では以下を constraint とする。

- backend に存在しない operation を UI taxonomy を埋める目的で新設しない。
- `CHART` のような presentation mechanism を独立 execution semantics として扱わない。
- `TIME_TREND` の配置は existing operation semantics を確認して決定する。
- `Data Quality` に dedicated operation が存在しない場合、availability / empty state とすることを許容する。

#### Predictive

Stage:

```text
Setup
Train
Predict
Metrics
Explainability
Model Management
```

重要 invariant:

> Predictive Stage は独立 execution step ではなく、原則として同一 Predictive Execution の presentation/navigation view とする。

既存 execution semantics:

```text
Prediction Task
→ Split
→ Training
→ Evaluation
→ Explanation
→ Model Card
```

を変更しない。

初期 ownership:

```text
Setup
    Prediction Task
    target / feature configuration
    Split configuration

Train
    Training
    training status / result

Predict
    existing prediction output presentation
    ※ existing surface が存在する範囲

Metrics
    Evaluation / metrics

Explainability
    Explanation

Model Management
    Model Card
    existing model management surface
```

`Predict` 用に新しい backend execution semantics を ENH-E7 で作らない。

---

## 5. Scope

### 対象範囲

#### Product / IA

- Project Management と Analysis Workspace の top-level 分離
- Project List / New Project / Selected Project hierarchy の確立
- Project Management local navigation
  - Overview
  - Research Context
  - Data
  - Results / Lineage
- Project metadata と Dataset / Analysis View management の責務分離
- Analysis Context bar
  - Current Project
  - Active Research Context
  - Dataset Version
  - Analysis View
- Analysis Workspace layout
  - Family horizontal navigation
  - Stage vertical navigation
  - Stage Contents
- Project Management ↔ Analysis Workspace transition
- Analysis Workspace ↔ Results / Lineage transition
- Existing Causal / Exploratory / Predictive surface の Stage Contents への migration
- legacy analytical sidebar shortcut の除去
- legacy analysis URL compatibility
- direct link / reload / Back / Forward
- existing domain operation regression protection

#### Workflow / execution control

- Enhancement-specific `40_operator_workflows/agent_entry_prompts/` instance 化
- Enhancement-fixed variables と Runtime variables の分離
- template-side operator prompt の direct execution 禁止
- assigned Pxx only の Coding Agent normative-context rule
- Pxx self-contained contract
- Test Agent / Coding Agent information separation
- Agent Execution Readiness preflight
- Artifact completeness / Content completeness / Execution resolvability / Information isolation の独立 validation
- candidate / READY_FOR_TEST / PASS の evidence identity 分離

### 対象外

- 全 Analysis 画面の全面的 UI redesign
- Causal backend execution semantics の変更
- Predictive Execution model の変更
- Exploratory backend operation model の全面変更
- Family / Stage taxonomy の大幅変更
- Results domain model の再設計
- persistence schema の変更
- frontend framework migration
- design system 全面刷新
- ENH-E6 runtime API build/version skew の修正
- UI taxonomy を埋めるためだけの新 backend operation 作成

scope expansion が必要になった場合は silent expansion を禁止し、Requirement / Design Revision と Human approval を経て re-baseline する。

---

## 6. 想定するRequirement変更

以下の ENH-E7 local requirement を新設・改定候補とする。

| ID | Requirement |
|---|---|
| E7-REQ-001 | `/projects` を Project List の canonical surface とする |
| E7-REQ-002 | `/projects/new` を Project Register の canonical surface とする |
| E7-REQ-003 | `/projects/{id}/overview` を selected Project の default canonical surface とする |
| E7-REQ-004 | Overview / Context / Data / Results を Project Management local navigation とする |
| E7-REQ-005 | Project metadata と Dataset / Analysis View management を別 responsibility にする |
| E7-REQ-006 | Project Archive を selected Project lifecycle operation とする |
| E7-REQ-007 | Analysis View management を Data scope に置き、Family 横断 input とする |
| E7-REQ-008 | Analysis Workspace を Project Management と独立 surface とする |
| E7-REQ-009 | Analysis Context に Current Project / Research Context / Dataset Version / Analysis View を持つ |
| E7-REQ-010 | Current Project は Analysis Workspace 内で read-only とする |
| E7-REQ-011 | Family / Stage navigation は Analysis Workspace 内だけに存在する |
| E7-REQ-012 | `/projects/{id}/analysis/{family}/{stage}` の canonical semantics を維持する |
| E7-REQ-013 | Family change は existing catalog authority に従って default Stage へ遷移する |
| E7-REQ-014 | Existing Causal surface が定義 Stage Contents 上から操作可能である |
| E7-REQ-015 | Existing Exploratory surface が定義 Stage Contents 上から操作可能である |
| E7-REQ-016 | Existing Predictive surface が定義 Stage Contents 上から操作可能である |
| E7-REQ-017 | Predictive Stage navigation は既存 Predictive Execution semantics を変更しない |
| E7-REQ-018 | legacy analytical URL を canonical Analysis URL へ normalize する |
| E7-REQ-019 | direct link / reload / Back / Forward が Project と Analysis の双方で成立する |
| E7-REQ-020 | Results / Lineage は persisted cross-analysis aggregation responsibility を持つ |
| E7-REQ-021 | ENH-E7 の UI 再編だけを理由に backend domain semantics を変更しない |

### Workflow要件

| ID | Requirement |
|---|---|
| E7-WF-001 | Enhancement-specific Agent entry prompt を work root 配下へ instance 化する |
| E7-WF-002 | template-side Agent prompt を direct execution に使用しない |
| E7-WF-003 | Enhancement-fixed variables は instance 化時に concrete value へ解決する |
| E7-WF-004 | Runtime variable のみ Human operator が execution ごとに指定する |
| E7-WF-005 | Coding Agent の normative implementation workflow context は assigned Pxx のみに限定する |
| E7-WF-006 | Assigned Pxx は implementation scope / constraints / completion / stop condition を self-contained に持つ |
| E7-WF-007 | Coding Agent に Gate 07 を acceptance-answer key として露出させない |
| E7-WF-008 | Document compliance と Agent Execution Readiness を独立判定する |
| E7-WF-009 | Agent Execution Readiness は4軸 validation を持つ |
| E7-WF-010 | preflight 不成立時は Coding Agent を開始せず BLOCKED とする |

詳細な Before / After、removed requirement、new invariant、acceptance implication は `03_requirements_revision.md` で freeze する。

---

## 7. 想定するDesign変更

### 7.1 Navigation authority

Application navigation を論理的に以下へ分離する。

```text
Application Navigation
│
├─ Project Navigation
│   ├─ /projects
│   ├─ /projects/new
│   └─ /projects/{id}/{section}
│
└─ Analysis Navigation
    └─ /projects/{id}/analysis/{family}/{stage}[...]
```

Project route authority を Analysis-specific navigation state へ混在させない。

Existing `AnalysisNavigation` と Analysis transition authority は protected semantics とし、ENH-E7 の application IA 再編を理由に不要な一般化・再実装を行わない。

### 7.2 UI shellのownership

```text
Projects Surface
    Project List / New Project entry

Project Management Shell
    Project header
    Project-local vertical navigation
    Project section content

Analysis Workspace Shell
    Analysis Context
    Family tabs
    Stage sidebar
    Stage Contents
```

旧 global sidebar に Project Management item と Analysis Family shortcut を並置する構造を廃止する。

### 7.3 Data / Analysis Viewのownership

Analysis View の lifecycle management は Data に置く。

Analysis Workspace は input selection を行うだけとする。

### 7.4 Resultsのownership

Results / Lineage は cross-analysis persisted result aggregation とする。

Stage-local result display と Results / Lineage を同一 responsibility にしない。

### 7.5 Workflow operator topology

Canonical Coding Agent entry topology:

```text
Human operator
    │
    │ runtime identifiers only
    ▼
Enhancement-specific instantiated operator prompt
    │
    │ resolver + guardrail
    ▼
Assigned Pxx
    │
    │ self-contained implementation contract
    ▼
source / tests / config / migrations
```

Coding Agent operator prompt は workflow 全体の説明書にせず、resolver + guardrail とする。

### 7.6 Coding Agentのinformation isolation

Invariant:

```text
Normative workflow document reachable by
Work Package Coding Agent
=
assigned Pxx only
```

Coding Agent が execution 時に workflow specification として利用可能なのは原則以下。

1. Enhancement-specific instantiated Coding Agent prompt
2. assigned Pxx

implementation substrate として source / tests / config / migrations は調査可能とする。

以下を仕様補完目的で direct-read させない。

- Gate 06
- Gate 07
- P00
- other Pxx
- 00 planning artifacts
- 20 implementation evidence
- 30 test evidence
- previous Enhancement workflow documents
- ADR / issue / external Web

Human/auditor traceability と Coding Agent read dependency は別概念とする。

### 7.7 Pxxのself-containment

各 Pxx は最低限以下を本文内に持つ。

- Package objective
- Implementation scope
- Explicit non-scope
- Target responsibility / source discovery boundary
- Protected semantics
- Required behavior
- Constraints
- Focused verification
- Expected outputs / report location
- Completion criteria
- BLOCKED / stop condition

---

## 8. Risk / migration / compatibility

### 8.1 Product risk

#### R-E7-01 — navigation authorityの重複

Project route と Analysis route を複数箇所で解決すると URL と screen state が乖離する。

Mitigation:

- Project / Analysis の route authority を明示的に分離
- direct link / reload / Back / Forward contract test
- canonical normalization を一箇所へ集約

#### R-E7-02 — Analysis execution semanticsの意図しない変更

Stage UI へ surface を移す過程で execution model まで変更する危険がある。

Mitigation:

- Causal / Predictive / Exploratory existing domain semantics を protected contract 化
- Predictive Stage を presentation/navigation view と明示
- backend operation 不在時に架空 operation を作らない

#### R-E7-03 — Analysis Contextのstale selection

Dataset Version変更時に互換性のない Analysis View が残る可能性。

Mitigation:

- Dataset Version変更時に incompatible Analysis View selection を解除
- Project整合性のない persisted context を restore しない

#### R-E7-04 — Results ownershipの曖昧化

Stage-local result と persisted Results / Lineage の責務が再混在する可能性。

Mitigation:

- Results / Lineage responsibility を design revision で freeze
- Stage-local result presentation と cross-analysis aggregation を分離

### 8.2 Migration順序

```text
00 Background / Architecture Review / Requirement & Design freeze
    ↓
Enhancement-specific workflow instantiation
    ↓
G01 — Project Management Surface Contract
    ↓
G01 PASS / Current State promotion
    ↓
G02 — Analysis Workspace Contract
    ↓
G02 PASS / Current State promotion
```

G02 は G01 PASS 後に開始する。

### 8.3 Legacy compatibility

旧 UI analytical shortcut は ENH-E7 で除去する方向。

旧 URL は compatibility entry として維持し、canonical Analysis route へ normalize する。

例:

```text
/projects/{id}/explore
    → /projects/{id}/analysis/exploratory/{default-stage}

/projects/{id}/causal
    → /projects/{id}/analysis/causal/{compatible-default-stage}

/projects/{id}/predictive
    → /projects/{id}/analysis/predictive/{default-stage}
```

具体的 Stage は existing AnalysisNavigation compatibility semantics を source of truth とし、Planning document の例を authority にしない。

### 8.4 Persistence / API migration

Expected:

```text
Persistence migration: NONE
API contract change: NONE
Backend domain semantic change: NONE
```

Architecture Review / source inspection により不足が具体的に立証された場合のみ別途 requirement/design amendment を行う。

### 8.5 Rollback方針

Gate は semantic boundary 単位で rollback 可能にする。

#### G01 rollback

- Project Management route/shell changes を rollback
- Analysis protected route/navigation semantics を変更しない

#### G02 rollback

- Analysis Workspace shell / surface migration / legacy UI cutover を rollback
- G01 PASS contract は保護する
- ENH-E6 Analysis canonical route contract を保護する

rollback 時も persistence/backend domain semantics を変えないことを原則とする。

### 8.6 Workflow execution risk

#### R-WF-01 — Enhancement identityの曖昧性

Mitigation:

- Enhancement-specific prompts instance 化
- fixed/runtime variables 分離
- exactly-one resolution preflight

#### R-WF-02 — Coding Agentへの過剰context

Mitigation:

- assigned Pxx only invariant
- prompt direct-read rule の mechanical check
- Pxx self-containment check

#### R-WF-03 — Document complianceとexecution readinessの混同

Mitigation:

以下を独立判定する。

1. Artifact completeness
2. Content completeness
3. Execution resolvability
4. Information isolation

### 8.7 必須Agent Execution Readiness preflight

各 Coding Agent execution 前に少なくとも以下を検査する。

```text
PRE-01 Enhancement-side agent_entry_prompts directory exists
PRE-02 Enhancement-fixed placeholders == 0
PRE-03 WORK_ROOT exists
PRE-04 WORK_ROOT resolves to exactly one Enhancement root
PRE-05 Assigned Pxx resolves to exactly one file
PRE-06 Coding Agent prompt does not direct-read 06 / 07 / P00 / other Pxx
PRE-07 Assigned Pxx does not require 06 / 07 / P00 / other Pxx
PRE-08 GATE_ID exists
PRE-09 PACKAGE_ID exists
PRE-10 TRIAL_NO exists
PRE-11 BRANCH_NAME is explicit and current branch matches
PRE-12 REMOTE_NAME is explicit and repository identity matches
```

1件でも不成立の場合:

```text
Agent Execution Readiness = FAIL
Execution state = BLOCKED
Coding Agent MUST NOT START
```

`REMOTE_NAME` の実値は Enhancement-specific prompt instance 化時に repository で確認し、推測で補完しない。

---

## 9. Architecture Review適用判定

- Required: **YES**

### 理由

ENH-E7 は少なくとも以下を変更・整理する。

- application navigation authority
- ProjectNavigation ownership
- Project Management / Analysis Workspace shell ownership
- Analysis Context authority
- legacy analytical navigation surface
- legacy path normalization policy
- Project resource / Analysis input ownership
- Results / Lineage responsibility boundary

authority / ownership 変更および legacy path の統合を含むため、Gate implementation contract 作成前に Architecture Review が必要である。

### Architecture Reviewで必ず決定する事項

最低限以下を決定・記録する。

#### AR-E7-01
Application route authority と route restore order。

#### AR-E7-02
Project Navigation と existing AnalysisNavigation の responsibility boundary。

#### AR-E7-03
Project Management shell / Analysis Workspace shell / shared header の ownership。

#### AR-E7-04
Analysis Context の source-of-truth、restore、invalid-selection semantics。

#### AR-E7-05
Analysis View の Data ownership と Family 横断 input semantics。

#### AR-E7-06
Results / Lineage と Stage-local results の boundary。

#### AR-E7-07
Legacy analytical UI removal と legacy URL compatibility policy。

#### AR-E7-08
Existing Causal / Exploratory / Predictive surface の Stage mapping。

#### AR-E7-09
`Data Quality`, `TIME_TREND`, `CHART` の final placement または explicit deferred behavior。

#### AR-E7-10
Persistence/API change が不要であることの source-based confirmation。

Architecture Review 結果は `03_requirements_revision.md` / `04_design_revision.md` / `05_requirements_design_consistency_and_traceability_review.md` へ反映する。

---

## 10. Gate分割案

ENH-E7 は **2 Gate / WORK_PACKAGE mode** とする。

Gate は implementation phase やファイル数ではなく、PASS 後に downstream が依存可能な semantic contract で分割する。

---

### G01 — Project Management Surface Contract

#### Gate claim

> G01 PASS 後、Project の作成・選択・管理が独立した URL-authoritative Project Management surface として成立し、後続 Gate は Project route、Project section ownership、Analysis input resource ownership に安全に依存できる。

#### Entry criteria

- 00 background artifacts approved
- Architecture Review complete
- Requirements / Design / Traceability revision complete
- G01 06 / 07 APPROVED/FROZEN
- Enhancement-specific operator prompts instantiated
- G01 Pxx self-contained
- Agent Execution Readiness preflight PASS

#### Work Package

```text
G01
├─ P01 Project Navigation Authority
├─ P02 Projects / New Project Surface
├─ P03 Overview / Project Lifecycle
├─ P04 Research Context Surface
├─ P05 Data / Analysis View Surface
├─ P06 Results / Lineage Surface
└─ P07 Project Integration / Regression
```

##### P01 — Project Navigation Authority

- `/projects`
- `/projects/new`
- `/projects/{id}/overview`
- `/projects/{id}/context`
- `/projects/{id}/data`
- `/projects/{id}/results`
- parse / serialize / canonical normalization
- history behavior
- `/projects/{id}` → `/overview`

##### P02 — Projects / New Project Surface

- Project List
- Project selection
- New Project route
- Project Register

##### P03 — Overview / Project Lifecycle

- Project metadata
- Project identity / status
- Project archive

##### P04 — Research Context Surface

- Research Context
- DRAFT / FIXED
- Context history
- Related Analysis

##### P05 — Data / Analysis View Surface

- Dataset Register
- Registered Dataset
- Dataset Version
- Schema / Preview
- Analysis View lifecycle management

##### P06 — Results / Lineage Surface

- Cross-analysis Results
- Result filter
- Result comparison
- Artifacts
- Lineage
- Annotation

##### P07 — Project Integration / Regression

- direct link
- reload
- Back / Forward
- Project create/select/archive
- Context regression
- Dataset / Analysis View regression
- Results / Lineage regression
- protected Analysis regression

#### G01 Acceptance Criteria骨子

```text
AC-G01-01 /projects is canonical Project List surface
AC-G01-02 /projects/new is canonical Project Register surface
AC-G01-03 creation transitions to /projects/{id}/overview
AC-G01-04 /projects/{id} normalizes to /overview
AC-G01-05 Overview / Context / Data / Results local navigation works
AC-G01-06 Project metadata and Data management are separated
AC-G01-07 Project Archive belongs to selected Project / Overview
AC-G01-08 Analysis View management belongs to Data
AC-G01-09 Analysis View is available as Family-crossing analysis input
AC-G01-10 Results / Lineage retains existing cross-analysis functions
AC-G01-11 direct link / reload / Back / Forward work
AC-G01-12 existing Project/domain semantics do not regress
```

---

### G02 — Analysis Workspace Contract

#### Gate claim

> G02 PASS 後、Analysis Workspace が Project Management と独立した analysis surface として成立し、Analysis Context、Family / Stage navigation、既存 Exploratory / Causal / Predictive surface の Stage Contents への配置、Project ↔ Analysis 遷移、legacy compatibility、browser history が一体として利用可能になる。

Analysis shell の表示だけでは G02 PASS としない。

#### Entry criteria

- G01 final PASS
- G01 Current State promotion complete
- G02 Architecture/Design decisions resolved
- G02 06 / 07 APPROVED/FROZEN
- G02 Pxx self-contained
- Agent Execution Readiness preflight PASS

#### Work Package

```text
G02
├─ P01 Analysis Shell / Analysis Context
├─ P02 Project ↔ Analysis Routing
├─ P03 Causal Stage Surface Migration
├─ P04 Exploratory Stage Surface Migration
├─ P05 Predictive Stage Surface Migration
└─ P06 Legacy Cutover / Integration / Regression
```

##### P01 — Analysis Shell / Analysis Context

- Analysis Context bar
- Current Project read-only
- Research Context selector
- Dataset Version selector
- Analysis View selector
- Family tabs
- Stage sidebar
- Stage Contents
- selected state
- context restore / invalid-selection behavior

##### P02 — Project ↔ Analysis Routing

- Open Analysis Workspace
- Project Management return
- Results / Lineage transition
- canonical Analysis route
- Family default Stage authority

##### P03 — Causal Stage Surface Migration

- Setup
- Discovery
- Identification
- Estimation
- Effects
- Diagnostics
- Sensitivity
- existing Causal execution semantics protection

##### P04 — Exploratory Stage Surface Migration

- Profile
- Data Quality
- Distribution
- Relationships
- Comparison
- Findings
- existing operation mapping
- explicit availability/deferred handling for unresolved operations

##### P05 — Predictive Stage Surface Migration

- Setup
- Train
- Predict
- Metrics
- Explainability
- Model Management
- existing Predictive Execution semantics protection

##### P06 — Legacy Cutover / Integration / Regression

- remove legacy analytical sidebar shortcuts
- preserve legacy URL compatibility
- canonical normalization
- Project → Analysis → Project
- Analysis → Results
- deep link / reload / Back / Forward
- resource route
- existing operation availability
- ENH-E6 protected regression

#### G02 Acceptance Criteria骨子

```text
AC-G02-01 Analysis Workspace is a separate surface
AC-G02-02 Analysis Context exposes all four context elements
AC-G02-03 Current Project is read-only
AC-G02-04 Project changes occur via Projects / Project Management
AC-G02-05 Research Context / Dataset Version / Analysis View can be selected as current input
AC-G02-06 Family navigation exists only in Analysis Workspace
AC-G02-07 Stage navigation is vertical under the active Family
AC-G02-08 existing Causal surfaces are operable from defined Stage Contents
AC-G02-09 existing Exploratory surfaces are operable from defined Stage Contents
AC-G02-10 existing Predictive surfaces are operable from defined Stage Contents
AC-G02-11 Predictive Execution semantics do not change
AC-G02-12 canonical Analysis URL semantics do not change
AC-G02-13 Family default-Stage semantics remain catalog-authoritative
AC-G02-14 legacy analytical URLs normalize to canonical Analysis routes
AC-G02-15 Project → Analysis → Project navigation works
AC-G02-16 Analysis → Results / Lineage navigation works
AC-G02-17 deep link / reload / Back / Forward work
AC-G02-18 resource route semantics are preserved
AC-G02-19 ENH-E6 protected Analysis navigation semantics do not regress
```

---

### Trial / Independent Verificationの意味論

Work Package completion does not mean Gate PASS.

```text
Package checkpoint
    != Fixed Trial Candidate
    != Gate PASS
```

Candidate Assembly 後は:

```text
READY_FOR_TEST
```

とする。

Gate 07 を Independent Verification authority とし、Coding Agent focused test は package completion evidence に限定する。

Coding Agent に Gate 07 を acceptance-answer key として読ませない。

final PASS authority は:

```text
999 Gate Decision
```

のみとする。

formal FAIL 後にのみ next Trial candidate transaction へ進む。

---

## 11. 実装開始前に必要な承認

この Planning Artifact の作成だけでは Coding implementation を開始してはならない。

以下を implementation prerequisite とする。

### 11.1 Human / Architecture承認

- [ ] ENH-E7 scope / out-of-scope approved
- [ ] 2 Gate decomposition approved
- [ ] Architecture Review completed
- [ ] Current Project read-only policy approved
- [ ] `/projects/new` and `/projects/{id}/overview` routing approved
- [ ] Analysis View ownership approved
- [ ] Results / Lineage ownership approved
- [ ] Causal / Exploratory / Predictive Stage mapping approved or explicitly deferred where allowed
- [ ] legacy URL compatibility policy approved

### 11.2 00-layer完了条件

- [ ] `02_enhancement_concept_approval_record.md`
- [ ] `03_requirements_revision.md`
- [ ] `04_design_revision.md`
- [ ] `05_requirements_design_consistency_and_traceability_review.md`
- [ ] Revised requirements/design snapshot where applicable
- [ ] `80_contract_amendment_log.md` initialized

### 11.3 Workflow instance化

- [ ] Enhancement-specific `40_operator_workflows/agent_entry_prompts/` exists
- [ ] Enhancement-fixed variables resolved
- [ ] Runtime-variable convention documented
- [ ] template-side prompt direct execution prohibited
- [ ] Coding Agent prompt reduced to resolver + guardrail
- [ ] assigned Pxx only normative-context invariant present
- [ ] Test Agent information isolation present

### 11.4 Agent execution前に固定するEnhancement identity

The following must be concretely resolved before execution:

```text
PROJECT_NAME=Ariadne
ENHANCE_ID=ENH-E7
ENHANCE_SHORT_ID=E7
BRANCH_NAME=feature/ariadne_mvp_e7
WORK_ROOT=docs/wiki/develop_memo/_work/20260813_ENH-E7_project_analysis_workspace_separation
WORK_DIR_NAME=20260813_ENH-E7_project_analysis_workspace_separation
REMOTE_NAME=<must be verified from repository>
```

`REMOTE_NAME` must not be guessed.

### 11.5 Runtime identifier

Human operator supplies only execution-scoped values.

```text
GATE_ID
PACKAGE_ID
TRIAL_NO

when applicable:
REMEDIATION_PACKAGE_ID
AMENDMENT_ID
```

### 11.6 Agent Execution Readiness

Before every Coding Agent execution:

```text
Artifact completeness = PASS
Content completeness = PASS
Execution resolvability = PASS
Information isolation = PASS
```

and PRE-01 through PRE-12 must PASS.

If any item fails:

```text
BLOCKED
```

No Coding Agent implementation begins.

---

## 12. 初期traceability骨子

| Requirement group | Design responsibility | Gate / Package |
|---|---|---|
| Project List / New Project / Project route | Project Navigation / Projects Surface | G01 P01-P02 |
| Project lifecycle | Overview | G01 P03 |
| Research Context | Context Surface | G01 P04 |
| Dataset / Analysis View | Data Surface | G01 P05 |
| Results / Lineage | Results Surface | G01 P06 |
| Project browser semantics | Project Routing | G01 P07 |
| Analysis Context | Analysis Shell / Context authority | G02 P01 |
| Project ↔ Analysis | Application routing | G02 P02 |
| Causal Stage operability | Causal surface ownership | G02 P03 |
| Exploratory Stage operability | Exploratory surface ownership | G02 P04 |
| Predictive Stage operability | Predictive surface ownership | G02 P05 |
| legacy compatibility / cross-surface regression | Compatibility / integration | G02 P06 |
| Agent prompt instantiation | Operator workflow | pre-execution |
| Coding Agent isolation | Operator prompt + Pxx contract | every Pxx |
| Independent Verification isolation | Gate 07 / Test Agent | every Gate |
| Execution readiness | preflight / controlled runbook | every Pxx |

Final traceability in `05_requirements_design_consistency_and_traceability_review.md` must resolve:

```text
Requirement
    ↓
Design
    ↓
Gate
    ↓
Work Package
    ↓
Acceptance Criterion
    ↓
Test Item
    ↓
Evidence
    ↓
999 Gate Decision
```

---

## 13. Planning完了状態

This document establishes the ENH-E7 enhancement concept and revision plan.

Current status:

```text
Enhancement planning concept: READY
Implementation authorization: NOT YET
```

Remaining mandatory work before G01 Coding:

1. Human concept approval record
2. Architecture Review
3. Requirements revision
4. Design revision
5. Requirements/design/AC traceability review
6. Current State initialization
7. Enhancement-specific operator prompt instantiation
8. G01 06 / 07 freeze
9. G01 Pxx self-contained contract creation
10. Agent Execution Readiness preflight PASS

Only after those conditions are satisfied may G01 Coding Agent execution start.
