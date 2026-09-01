Document title: Deal Profile別に見た当チームのPositioning

# A01-04. Appendix｜Deal Profile別に見た当チームのPositioning

## A01-04.1. Message

**当チームの重点領域は、高度・非定型な分析とEnterprise条件が同時に重い案件に集中する。**

## A01-04.2. Chart

**チャートタイトル:** 8つの代表Deal Profileから見た当チームのPositioning

### A01-04.2.1. Chart Structure

A01-04a〜hの分析結果を集約したSummary Tableを中央に置く。

| Deal Profile | 当チームPosition | 主な有力競合 | Positionの理由 |
|---|---|---|---|
| A01-04a 高度分析 × Analysis-only | Competitive | DS Specialist | 分析CapabilityはFitするがEnterprise Baseが効きにくい |
| **A01-04b 高度分析 × Enterprise** | **Core Candidate** | SIer Analytics / Consulting Analytics | Specialist AnalyticsとEnterprise Baseが同時に価値化しやすい |
| A01-04c 標準分析 × Enterprise | Competitive | SIer Analytics | Enterprise側はFitするが分析専門性が差になりにくい |
| A01-04d Standard Product Fit | Relative Weak | AI / Platform Vendor | Scratch柔軟性よりStandardization / Speed / Economicsが効きやすい |
| A01-04e Corporate / Transformation | Relative Weak〜Competitive | Consulting Analytics | Strategy / Stakeholder Alignmentが主要競争軸になる |
| **A01-04f High Novelty Analytical PoC** | **Core Candidate** | DS Specialist / Consulting Analytics | 問い・前提・評価を含むAnalytical Designが価値化しやすい |
| A01-04g High Criticality / Governance | Conditional Core | SIer Analytics / Consulting Analytics | Analytical Complexityも高い場合にScientific Validity × Enterprise Contextが効く |
| A01-04h Standard / Commodity Analysis | Relative Weak〜Competitive | AI Vendor / Low-cost Provider / 内製 | 専門分析・Enterprise Baseの追加価値が小さい |

下部に共通Profileを抽出する。

```text
A01-04b
高度分析 × Enterprise
       ＋
A01-04f
High Novelty Analytical PoC
       ＋
A01-04gの一部
High Governance × High Analytical Complexity
       ↓
共通条件
────────────────────
Decision Altitude          Operational〜Business中心
Problem Novelty            Medium〜High
Analytical Complexity      High
Solution Standardizability Low〜Medium
Implementation Coupling    Medium〜High
Criticality / Governance   Medium〜High
       ↓
重点Positioning
**定型解では扱いにくい高度分析を、Enterprise利用まで見据えてPoCする領域**
```

### A01-04.2.2. Chart内の最小表示テキスト

- 04b：**Core Candidate**
- 04f：**Core Candidate**
- 04g：**Conditional Core**
- 04a / 04c：Competitive
- 04d / 04e / 04h：主戦場外寄り
- **Core Candidate ≠ Relative Advantage実証済み**

## A01-04.3. Supporting Logic

### A01-04.3.1. A01-04ファミリーの役割

A01-04無印は、A01-04a〜hを束ねる親スライドである。

```text
A01-04
「なぜ当チームに依頼するのか？」の総合結論
│
├─ A01-04a：高度分析 × Analysis-only
├─ A01-04b：高度分析 × Enterprise
├─ A01-04c：標準分析 × Enterprise
├─ A01-04d：Standard Product Fit
├─ A01-04e：Corporate / Transformation
├─ A01-04f：High Novelty Analytical PoC
├─ A01-04g：High Criticality / Governance
└─ A01-04h：Standard / Commodity Analysis
```

a〜hは排他的な市場分類ではなく、6次元Deal Profile空間上の代表Anchorである。実案件は複数Anchorの中間に位置し得る。

### A01-04.3.2. Deal Profileの共通6軸

全Profileを以下の同じ6軸で記述する。

1. Decision Altitude：Operational ↔ Corporate / Strategic
2. Problem Novelty：Established ↔ Novel / Uncertain
3. Analytical Complexity：Standard ↔ Complex Predictive / Causal / Experimental
4. Solution Standardizability：Standard Product適合 ↔ Individual Design
5. Implementation Coupling：Analysis-only ↔ Enterprise System / Workflow統合
6. Criticality / Governance：Low-risk / Reversible ↔ Mission Critical / High Governance

各サブスライドでは6軸を必ず全て表示する。

### A01-04.3.3. Deal Profileから競争構造へ至るロジック

各Dealで新しい評価軸を作るのではなく、共通する8つのCustomer Selection CriteriaのWeightがDeal Profileによって変化すると考える。

共通8軸は以下である。

1. Deal-specific Fit
2. Capability / Quality
3. Delivery Feasibility
4. Economic Value
5. Risk
6. Evidence / Credibility
7. Relational / Governance Fit
8. Organizational Acceptability

概念構造：

```text
6-dimensional Deal Profile
        ↓
8 Selection CriteriaのWeight
        ↓
同じWeightで各Providerを比較
        ↓
ProviderごとのRelative Position
        ↓
当チームのPosition
```

このWeight設定は実証済み係数ではなく、Organizational Buying、BUYGRID、Professional Service Selection、Transaction Cost等の既存研究を踏まえた当資料の分析仮説である。

### A01-04.3.4. なぜ04b / 04f / 04gの一部を重点候補とするか

当チームで確認済みのCapabilityは、

- Predictive / Causalを問いから使い分ける
- Scratch / OSSで非定型に設計する
- 前提 / 評価 / Limitationを必要に応じて扱う
- SIer内の分析組織としてEnterprise Contextを考慮する

である。

このCapability Bundleは、Analytical ComplexityやProblem Noveltyだけが高い場合より、**Implementation CouplingやCriticalityも一定以上ある場合に複数Capabilityが同時に価値化しやすい**。

そのため、04bを中心に、04fのうちEnterprise接続が一定以上ある領域、04gのうちAnalytical Complexityも高い領域を重点Positioning候補とする。

### A01-04.3.5. 各Profileで当チームが常に優位とは限らない

- 高度分析 × Analysis-onlyではDS Specialistがより合理的な場合がある。
- 標準分析 × Enterpriseでは一般SIer AnalyticsがよりFitする場合がある。
- Standard Product FitではAI / Platform VendorがSpeed / Economicsで有利になり得る。
- Corporate TransformationではConsulting AnalyticsのStrategy / Stakeholder Alignmentが強く効く。
- Commodity Analysisでは低コストProviderや内製が合理的な場合もある。

従って、A01-04の目的は「全案件で当チームが最良」と示すことではなく、**どのDeal Profileで当チームのCapability Bundleが最も価値化しやすいかを明確にすること**である。

### A01-04.3.6. Relative Advantageとの区別

以下を区別する。

1. Capability：何ができるか
2. Deal Fit：そのProfileでCapabilityがどれだけ価値化するか
3. Relative Position：Relevant Competitorと比べたPositioning仮説
4. Relative Advantage / Competitive Gap：顧客Weightで競合を実際に上回るか

A01-04ファミリーで現時点に示すのは主に3までである。

`Core Candidate`は、

> **当チームのCapability Bundleが最も価値化しやすく、Relevant Competitorとの差を優先的に検証すべき領域**

を意味する。

競争優位の実証には、競合勝敗、人材、案件実績、Price / Lead Time、顧客選定理由等のEvidenceが必要である。

### A01-04.3.7. 01-05との対応

01-05の顧客向けValue Proposition、

> **予測・因果の高度分析を、Enterprise利用まで見据えて柔軟に設計する。**

は、A01-04ファミリーの詳細分析を一枚に圧縮したものである。

顧客から「他社も同じでは？」と反論された場合、A01-04無印で総合Positionを示し、必要に応じa〜hでProfile別のCompetition Logicまで降りる。

## A01-04.4. Speaker Note

当チームの強みを一つの2軸Mapだけで説明すると、案件によって競争軸が変わることを捉えきれません。そこで商談を6つの共通軸でProfile化し、代表的な8パターンについて、顧客が何を重視し、どのProviderがFitしやすいかを分解しました。

その結果、当チームが常に有利という結論にはなりません。分析単体ならDS専門会社、標準Productで十分ならAI Vendor、全社TransformationならConsulting、標準的な本番化ならSIerが合理的な場合があります。

一方、高度で非定型な分析を設計しながら、その結果をEnterprise環境で使う条件まで考える必要がある案件では、当チームのPredictive / Causal、Scratch / OSS、分析前提の設計、SIerとしてのEnterprise Contextが同時に効きます。この領域を重点Positioning候補としています。

ただし、ここで示すのはPositioning仮説です。競合より実際に優位かは、案件実績や競合勝敗等のEvidenceで確認します。

## A01-04.5. A01-04a〜hへの接続

> なぜこのProfileで当チームのPositionが変わるのか。A01-04a〜hでは、各Deal Profileを6軸で定義し、8つのCustomer Selection CriteriaのWeightとProvider競争構造を個別に展開する。

## A01-04.6. Sources / Design Note

本スライドはA01-04a〜hの集約であり、個別の理論・Provider一次情報は各サブスライドのSourcesを参照する。

Deal Profile 6軸およびProfile別Selection Weightは、BUYGRID、Webster & Wind、Sheth、Professional Service Selection、Transaction Cost / Contingency logic等を踏まえた当資料独自の分析フレームであり、既存研究に同名の標準6軸・8類型が存在するわけではない。