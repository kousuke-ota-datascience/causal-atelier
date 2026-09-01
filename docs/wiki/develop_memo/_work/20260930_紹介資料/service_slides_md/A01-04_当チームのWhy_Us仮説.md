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
| **A01-04f High Novelty Analytical PoC** | **Competitive〜Conditional Core** | DS Specialist / Consulting Analytics | Analytical DesignはFitするが、Enterprise Baseが効くかはImplementation Coupling次第 |
| A01-04g High Criticality / Governance | Conditional Core | SIer Analytics / Consulting Analytics | Analytical Complexityも高い場合にScientific Validity × Enterprise Contextが効く |
| A01-04h Standard / Commodity Analysis | Relative Weak〜Competitive | AI Vendor / Low-cost Provider / 内製 | 専門分析・Enterprise Baseの追加価値が小さい |

下部に重点領域の導出を置く。

```text
A01-04b
高度分析 × Enterprise
       ＋
A01-04fの一部
High Novelty × High Analytical Complexity
× Implementation Coupling = Medium側
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

- 04b：**Core Candidate / Primary Core**
- 04f：**Conditional Core（Enterprise接続次第）**
- 04g：**Conditional Core（Analytical Complexity次第）**
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

### A01-04.3.4. 01-05の3 Value Propositionから8 Selection Criteriaへの橋

01-05で顧客向けに示す3つのValue Propositionは、A01-02で定義した8つのCustomer Selection Criteriaへ以下のように接続する。

| 01-05 Value Proposition | 当チームのCapability | 主に押し上げるSelection Criteria | 価値が高まりやすいDeal Profile条件 |
|---|---|---|---|
| **① 問いに合う分析を選ぶ** | Predictive / Causal、Question / Estimand / Assumption / Evaluation設計 | **Deal-specific Fit / Capability / Quality** | Problem Novelty ↑、Analytical Complexity ↑ |
| **② 非定型課題にも合わせる** | Scratch + OSS、特定Product非必須、個別設計 | **Deal-specific Fit / Capability / Quality**、一部Risk | Solution Standardizability ↓、Problem Novelty ↑ |
| **③ 利用段階まで見据える** | Enterprise Context、Data / System / Security / Operation / Governance考慮 | **Delivery Feasibility / Risk / Relational-Governance Fit / Organizational Acceptability** | Implementation Coupling ↑、Criticality / Governance ↑ |

この対応から重要な点は、3つのValue Propositionが**常に同じ強さで効くわけではない**ことである。

- Analysis-onlyなら①②は効くが③は相対的に効きにくい。
- 標準分析 × Enterpriseなら③は効くが①②の差別化寄与は小さい。
- 高NoveltyでもImplementation CouplingがLowなら、①②中心の競争になりDS Specialistとの差が縮む。
- 高度・非定型な分析にEnterprise接続が加わると、①②③が同時にSelection Criteriaへ効く。

従って、01-05の3つを一つのCapability Bundleとして最も強く説明できるAnchorはA01-04bである。

### A01-04.3.5. なぜ04bをPrimary Core、04f / 04gをConditional Coreとするか

当チームで確認済みのCapabilityは、

- Predictive / Causalを問いから使い分ける
- Scratch / OSSで非定型に設計する
- 前提 / 評価 / Limitationを必要に応じて扱う
- SIer内の分析組織としてEnterprise Contextを考慮する

である。

A01-04bでは、Analytical ComplexityとImplementation Couplingが共に高いため、

- ① 問いに合う分析を選ぶ
- ② 非定型課題にも合わせる
- ③ 利用段階まで見据える

の3つが同時に高WeightのSelection Criteriaへ接続する。従ってA01-04bを**Primary Core**とする。

A01-04fはProblem Novelty / Analytical Complexityが高く①②が強く効く一方、Implementation CouplingはLow〜Mediumである。このため、Low側ではCompetitive、Medium側へ上がるほど③も効いて**Conditional Core**となる。

A01-04gはCriticality / Governanceが高く③が強く効く一方、Analytical ComplexityがMedium側では一般SIer / Consultingとの差が出にくい。Analytical ComplexityがHigh側へ上がることで①②も同時に効き、**Conditional Core**となる。

### A01-04.3.6. 各Profileで当チームが常に優位とは限らない

- 高度分析 × Analysis-onlyではDS Specialistがより合理的な場合がある。
- 標準分析 × Enterpriseでは一般SIer AnalyticsがよりFitする場合がある。
- Standard Product FitではAI / Platform VendorがSpeed / Economicsで有利になり得る。
- Corporate TransformationではConsulting AnalyticsのStrategy / Stakeholder Alignmentが強く効く。
- Commodity Analysisでは低コストProviderや内製が合理的な場合もある。

従って、A01-04の目的は「全案件で当チームが最良」と示すことではなく、**どのDeal Profileで当チームのCapability Bundleが最も価値化しやすいかを明確にすること**である。

### A01-04.3.7. Relative Advantageとの区別

以下を区別する。

1. Capability：何ができるか
2. Deal Fit：そのProfileでCapabilityがどれだけ価値化するか
3. Relative Position：Relevant Competitorと比べたPositioning仮説
4. Relative Advantage / Competitive Gap：顧客Weightで競合を実際に上回るか

A01-04ファミリーで現時点に示すのは主に3までである。

`Core Candidate` / `Primary Core` / `Conditional Core`は、

> **当チームのCapability Bundleが価値化しやすく、Relevant Competitorとの差を優先的に検証すべき領域**

を意味する。

競争優位の実証には、競合勝敗、人材、案件実績、Price / Lead Time、顧客選定理由等のEvidenceが必要である。

### A01-04.3.8. 01-05との対応

01-05の顧客向けValue Proposition、

> **予測・因果の高度分析を、Enterprise利用まで見据えて柔軟に設計する。**

は、A01-04ファミリーの詳細分析を一枚に圧縮したものである。

圧縮の対応関係は以下である。

```text
A01-04ファミリー
────────────────────────
High Problem Novelty / Analytical Complexity
        ↓
Fit / CapabilityのWeight上昇
        ↓
① 問いに合う分析を選ぶ
② 非定型課題にも合わせる

High Implementation Coupling / Criticality
        ↓
Delivery / Risk / Governance / Org. AcceptabilityのWeight上昇
        ↓
③ 利用段階まで見据える

両方が重なる
        ↓
A01-04bをPrimary Coreとする
        ↓
01-05
Specialist Analytics × Enterprise Base
```

顧客から「他社も同じでは？」と反論された場合、A01-04無印で総合Positionを示し、必要に応じa〜hでProfile別のCompetition Logicまで降りる。

## A01-04.4. Speaker Note

当チームの強みを一つの2軸Mapだけで説明すると、案件によって競争軸が変わることを捉えきれません。そこで商談を6つの共通軸でProfile化し、代表的な8パターンについて、顧客が何を重視し、どのProviderがFitしやすいかを分解しました。

01-05では「問いに合う分析」「非定型課題への柔軟性」「利用段階まで見る」の3つを示していますが、各Capabilityが効くSelection Criteriaは異なります。分析の新規性・難易度が高いほど前者2つが、Enterprise接続やCriticalityが高いほど後者が重要になります。

そのため、High Noveltyだけ、あるいはEnterprise接続だけで当チームがCoreになるとは考えていません。**高度・非定型な分析とEnterprise条件が同時に重いときに、3つのValue Propositionが一つのDealで同時に価値化する**というのが重点Positioningのロジックです。

この意味でA01-04bがPrimary Coreです。A01-04fとA01-04gは、もう一方の条件が高まった場合にCoreへ近づくConditional Anchorです。

ただし、ここで示すのはPositioning仮説です。競合より実際に優位かは、案件実績や競合勝敗等のEvidenceで確認します。

## A01-04.5. A01-04a〜hへの接続

> なぜこのProfileで当チームのPositionが変わるのか。A01-04a〜hでは、各Deal Profileを6軸で定義し、8つのCustomer Selection CriteriaのWeightとProvider競争構造を個別に展開する。

## A01-04.6. Sources / Design Note

本スライドはA01-04a〜hの集約であり、個別の理論・Provider一次情報は各サブスライドのSourcesを参照する。

Deal Profile 6軸およびProfile別Selection Weightは、BUYGRID、Webster & Wind、Sheth、Professional Service Selection、Transaction Cost / Contingency logic等を踏まえた当資料独自の分析フレームであり、既存研究に同名の標準6軸・8類型が存在するわけではない。