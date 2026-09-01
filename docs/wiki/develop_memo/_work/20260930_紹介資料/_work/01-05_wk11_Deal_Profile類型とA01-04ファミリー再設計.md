# A01-05 wk11｜Deal Profile類型とA01-04ファミリー再設計

## 1. 目的

本メモは、A01-04無印とA01-04a〜hの関係を整理し、Deal Profileの定義軸・Customer Selection Criteria・Provider競争ポジションを明確に分離するための設計方針を記録する。

結論は以下である。

> **A01-04無印は「なぜ当チームに依頼するのか」の総合結論、A01-04a〜hはその結論をDeal Profile類型ごとに分解して支えるロジックである。**

また、各Deal Profile類型は必ず同じ6軸で記述し、その6軸の値に応じて8つのCustomer Selection CriteriaのWeightが変化し、その結果としてProviderごとの相対Positionが変わる、という共通ロジックで統一する。

---

## 2. Deal Profileの共通6軸

Deal Profileを定義する共通座標系は以下の6軸である。

| Deal Profile軸 | Low側 | High側 |
|---|---|---|
| Decision Altitude | Operational | Corporate / Strategic |
| Problem Novelty | Established | Novel / Uncertain |
| Analytical Complexity | Standard | Complex Predictive / Causal / Experimental |
| Solution Standardizability | Standard Product適合 | Individual Design |
| Implementation Coupling | Analysis-only | Enterprise System / Workflow統合 |
| Criticality / Governance | Low-risk / Reversible | Mission Critical / High Governance |

重要なルールは以下である。

- A01-04a〜hでは、**6軸を必ず全て表示する**。
- 一部の軸がその類型の主題でなくても省略しない。
- 各類型は排他的なカテゴリではなく、連続空間上の代表的Anchor Profileとして扱う。
- 実案件はaかbかに完全分類される必要はなく、複数Anchorの中間として評価してよい。

概念的には以下である。

```text
Actual Deal
    ↓
6軸でProfile化
    ↓
最も近いAnchor Profileを参照
    ↓
必要に応じ複数Anchorの中間として評価
```

---

## 3. A01-04無印とA01-04a〜hの関係

A01-04ファミリーは以下の親子構造とする。

```text
A01-04
「なぜ当チームに依頼するのか？」
全Deal Profile類型を統合したPositioning結論
│
├─ A01-04a
│   高度分析 × Analysis-only
│   └ このProfileでの競争構造を詳細化
│
├─ A01-04b
│   高度分析 × Enterprise接続
│
├─ A01-04c
│   標準分析 × Enterprise接続
│
├─ A01-04d
│   Standard Product Fit
│
├─ A01-04e
│   Corporate / Transformation
│
├─ A01-04f
│   High Novelty Analytical PoC
│
├─ A01-04g
│   High Criticality / Governance
│
└─ A01-04h
    Standard / Commodity Analysis
```

A01-04hはSummaryではなく、他と同様の一つのAnchor Profileとする。

全Profileの横断Summaryは親であるA01-04無印が担う。

---

## 4. Deal ProfileとCustomer Selection Criteriaの関係

各Deal Profileの中で「新しい評価軸が発生する」と考えるのではなく、共通する8つのCustomer Selection Criteriaの**WeightがDeal Profileによって変化する**と整理する。

Customer Selection Criteriaは以下の8軸である。

1. Deal-specific Fit
2. Capability / Quality
3. Delivery Feasibility
4. Economic Value
5. Risk
6. Evidence / Credibility
7. Relational / Governance Fit
8. Organizational Acceptability

構造は以下である。

```text
6-dimensional Deal Profile
        ↓
今回のDealで
8 Selection CriteriaのWeightが決まる
        ↓
各Providerを同じWeightで評価
        ↓
ProviderごとのRelative Position
        ↓
当チームのPosition
```

ここで重要なのは、Providerごとに異なる評価軸を使うのではなく、**同一Dealでは全Providerを同一のCustomer Selection Criteria Weightで比較する**ことである。

---

## 5. 代表Anchor Profile

現時点の代表Profileは以下の8類型とする。

| Profile | Decision Altitude | Novelty | Analytical Complexity | Standardizability | Implementation Coupling | Criticality |
|---|---|---|---|---|---|---|
| A01-04a 高度分析 × Analysis-only | Operational–Business | M–H | **H** | L–M | **L** | L–M |
| A01-04b 高度分析 × Enterprise | Operational–Business | M–H | **H** | L–M | **H** | M–H |
| A01-04c 標準分析 × Enterprise | Operational–Business | L–M | L–M | M–H | **H** | M–H |
| A01-04d Standard Product Fit | Operational–Business | **L** | L–M | **H** | M | L–M |
| A01-04e Corporate Transformation | **H** | H | M | L | M–H | **H** |
| A01-04f High Novelty Analytical PoC | Operational–Business | **H** | **H** | **L** | L–M | M |
| A01-04g High Criticality / Governance | Business–Corporate | M | M–H | L–M | M–H | **H** |
| A01-04h Standard / Commodity Analysis | Operational | **L** | **L** | **H** | **L** | **L** |

この8類型は市場に存在するDealを完全分類するtaxonomyではない。競争構造が変化する代表的なAnchor Profileとして用いる。

---

## 6. ProfileごとのCustomer Selection Criteria Weight仮説

各Profileで想定されるSelection Criteria Weightは概念的に以下とする。

| Profile | Fit | Capability | Delivery | Economics | Risk | Evidence | Relational / Gov | Org. Acceptability |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A01-04a 高度分析 × Analysis-only | **H** | **H** | L | M | L–M | **H** | M | L |
| A01-04b 高度分析 × Enterprise | **H** | **H** | **H** | M | **H** | **H** | M–H | **H** |
| A01-04c 標準分析 × Enterprise | M | M | **H** | M–H | **H** | M | M | **H** |
| A01-04d Product Fit | **H** | M | **H** | **H** | M | M | L–M | M |
| A01-04e Corporate Transformation | **H** | M–H | M–H | M | **H** | **H** | **H** | **H** |
| A01-04f High Novelty PoC | **H** | **H** | M | M | M–H | **H** | **H** | M |
| A01-04g High Criticality | M–H | H | **H** | M | **H** | **H** | **H** | **H** |
| A01-04h Commodity Analysis | L–M | M | M | **H** | M | L–M | L | M |

これは実証済み係数ではなく、Organizational Buying / BUYGRID / Professional Service Selection / Transaction Cost等の理論を踏まえた**当資料の分析仮説**である。

従って、各A01-04xでは「なぜこのWeightになるのか」をSupporting Logicで説明し、Published Evidenceと当資料のInferenceを分離する。

---

## 7. Profileごとの競争構造

### 7.1. A01-04a｜高度分析 × Analysis-only

Deal Profile例：

```text
Decision Altitude          Operational〜Business
Problem Novelty            Medium〜High
Analytical Complexity      High
Solution Standardizability Low〜Medium
Implementation Coupling    Low
Criticality / Governance   Low〜Medium
```

Implementation Couplingが低いため、Delivery Feasibility / Organizational Acceptability等のWeightは相対的に下がる。

一方、Analytical ComplexityとProblem Noveltyが高いため、Capability / Deal-specific Fit / Evidenceが強く効く。

競争構造仮説：

- DS Specialist：Analytical Depth / Specialist Evidenceが効きやすい
- Consulting Analytics：高度Analytics Capabilityがあれば競争可能
- 当チーム：Predictive / Causal / Scratchは効くがEnterprise Baseは加点されにくい
- SIer Analytics：Enterprise Deliveryの強みが加点されにくい
- AI Vendor：Product Fit次第

当チームPosition：**Competitive**。構造的Relative Advantageは未確認。

### 7.2. A01-04b｜高度分析 × Enterprise接続

6軸：

```text
Decision Altitude          Operational〜Business
Problem Novelty            Medium〜High
Analytical Complexity      High
Solution Standardizability Low〜Medium
Implementation Coupling    High
Criticality / Governance   Medium〜High
```

Analytical ComplexityとImplementation Couplingが同時に高いため、Capability / FitだけでなくDelivery / Risk / Organizational Acceptabilityも重くなる。

当チームの`Specialist Analytics × Enterprise Base`の双方が同時に価値化しやすい。

当チームPosition：**Core Candidate / Right-to-Win検証対象**。ただし他SIer AnalyticsやConsulting Analyticsも強いRelevant Competitorであり、Relative Advantageは未証明。

### 7.3. A01-04c｜標準分析 × Enterprise接続

6軸：

```text
Decision Altitude          Operational〜Business
Problem Novelty            Low〜Medium
Analytical Complexity      Low〜Medium
Solution Standardizability Medium〜High
Implementation Coupling    High
Criticality / Governance   Medium〜High
```

分析手法そのものよりIntegration / Production / Security / OperationのWeightが高まる。

当チームPosition：**Competitive**。SIer BaseはFitするが、Specialist Analytics側の差別化寄与は小さい。

### 7.4. A01-04d｜Standard Product Fit

6軸：

```text
Decision Altitude          Operational〜Business
Problem Novelty            Low
Analytical Complexity      Low〜Medium
Solution Standardizability High
Implementation Coupling    Medium
Criticality / Governance   Low〜Medium
```

Economic Value / Delivery / Time-to-Valueが強く効きやすく、AI / Platform VendorのProduct Assetが価値化しやすい。

当チームPosition：**Relative Weak候補**。Scratch柔軟性が過剰設計になる可能性がある。

### 7.5. A01-04e｜Corporate / Transformation

6軸：

```text
Decision Altitude          High
Problem Novelty            High
Analytical Complexity      Medium
Solution Standardizability Low
Implementation Coupling    Medium〜High
Criticality / Governance   High
```

Deal-specific Fit / Evidence / Relational-Governance / Organizational Acceptabilityが重くなり、Strategy / Stakeholder Alignmentが主要価値になる。

当チームPosition：**Relative Weak〜Competitive**。Analytical Workstreamでは有力でもPrime PositionのRelative Advantageは未確認。

### 7.6. A01-04f｜High Novelty Analytical PoC

6軸：

```text
Decision Altitude          Operational〜Business
Problem Novelty            High
Analytical Complexity      High
Solution Standardizability Low
Implementation Coupling    Low〜Medium
Criticality / Governance   Medium
```

既存手法を適用するだけでなく、Question / Estimand / Assumption / Evaluation / Data Sufficiency等の設計が必要になる。

当チームPosition：**Core Candidate**。ただしAnalysis-onlyに近いほどDS Specialistとの差が縮み、Consulting Analyticsも有力競合となる。

### 7.7. A01-04g｜High Criticality / Governance

6軸：

```text
Decision Altitude          Business〜Corporate
Problem Novelty            Medium
Analytical Complexity      Medium〜High
Solution Standardizability Low〜Medium
Implementation Coupling    Medium〜High
Criticality / Governance   High
```

Risk / Evidence / Delivery / Governance / Organizational Acceptabilityが強く効く。

当チームPosition：**Competitive〜Conditional Core Candidate**。High Governanceだけでは一般SIer / Consultingとの差別化にならないが、Analytical Complexityも高い場合は`Scientific Validity × Enterprise Context`が価値化しやすい。

### 7.8. A01-04h｜Standard / Commodity Analysis

6軸：

```text
Decision Altitude          Operational
Problem Novelty            Low
Analytical Complexity      Low
Solution Standardizability High
Implementation Coupling    Low
Criticality / Governance   Low
```

Economic Value、Speed、基本的なDeliveryが中心となり、専門的なAnalytical DesignやEnterprise Baseの追加価値は小さい。

当チームPosition：**Relative Weak〜Competitive**。対応可能だが、当チームのCapability Bundleを差別化として最も活かすProfileではない。

---

## 8. 各A01-04xの標準構造

A01-04a〜hは以下の構造へ統一する。

```text
A01-04x

1. Message
   このDeal Profileで何が競争を決めるか

2. Chart

   ① Deal Profile
      6軸すべてを表示

           ↓

   ② Customer Selection Criteria
      8軸のWeightをH/M/L表示

           ↓

   ③ Provider Competition
      Consulting
      SIer
      DS Specialist
      AI Vendor
      Our Team

           ↓

   ④ Our Position
      Core Candidate
      Competitive
      Relative Weak
      Evidence Insufficient

3. Supporting Logic

   3.1 なぜこの6軸Profileなのか
   3.2 なぜこのSelection Weightになるのか
   3.3 ConsultingのPosition
   3.4 SIerのPosition
   3.5 DS SpecialistのPosition
   3.6 AI VendorのPosition
   3.7 当チームのPosition
   3.8 Relative Advantageの有無
   3.9 反証条件
   3.10 Evidence / Inference区分

4. Speaker Note

5. A01-04への示唆

6. Sources
```

この構造により、全Profileを同じ物差しで横比較できる。

---

## 9. A01-04無印の役割

A01-04無印は、A01-04a〜hの結果を集約して「なぜ当チームに依頼するのか」を示す親スライドとする。

横断Summaryは概念的に以下となる。

```text
                   Our Position

04a  高度分析 × Analysis-only       Competitive
04b  高度分析 × Enterprise         ★ Core Candidate
04c  標準分析 × Enterprise         Competitive
04d  Product Fit                    Relative Weak
04e  Corporate Transformation       Relative Weak–Competitive
04f  High Novelty Analytical PoC    ★ Core Candidate
04g  High Criticality               Conditional Core
04h  Commodity Analysis             Relative Weak–Competitive
```

この結果から、当チームの重点Positioning候補を以下の共通条件として抽出する。

```text
04b
高度分析 × Enterprise

        ＋

04f
High Novelty Analytical PoC

        ＋

04gの一部
High Governance × High Analytical Complexity

        ↓

共通条件

Decision Altitude          Operational〜Business中心
Problem Novelty            Medium〜High
Analytical Complexity      High
Solution Standardizability Low〜Medium
Implementation Coupling    Medium〜High
Criticality / Governance   Medium〜High

        ↓

当チームの重点Positioning

「定型解では扱いにくい高度分析を、
 Enterprise利用まで見据えてPoCする領域」
```

従ってA01-04無印は、単なる2軸Mapではなく、**8つのAnchor Profile比較から導かれた総合Positioning結論**として再構成する。

---

## 10. 競争優位に関する主張範囲

以下を明確に区別する。

1. **Capability**：当チームが何をできるか
2. **Deal Fit**：当チームのCapabilityがそのProfileでどれだけ価値化しやすいか
3. **Relative Position**：Relevant Competitorと比較した場合のPositioning仮説
4. **Relative Advantage / Competitive Gap**：顧客Weightで競合を上回っているか

A01-04a〜hで現時点に示せるのは主に3までである。

`Core Candidate`は、

> **当チームのCapability Bundleが最も価値化しやすく、Relevant Competitorとの差を優先的に検証すべき領域**

を意味する。

`Core Candidate ≠ Relative Advantage実証済み`である。

相対優位を主張するには、競合勝敗、人材、案件実績、Price / Lead Time、顧客選定理由等のEvidenceが必要である。

---

## 11. 最終的な説明シーケンス

顧客向けには以下の順で説明する。

```text
A01-04
最初に総合結論を提示
「当チームはこのProfile群でCapability Bundleが最も活きる」
        ↓
顧客：「なぜ？」
        ↓
A01-04a〜h
Profileごとの6軸
        ↓
Selection Criteria Weight
        ↓
Provider Competition
        ↓
Our Position
        ↓
必要に応じSources / Evidenceまで降りる
```

したがってA01-04a〜hは単なる追加資料ではなく、**A01-04の結論を構成する分解証明**として位置づける。