Document title: 高Standardizability × Product Fit の競争ポジション

# A01-04d. Appendix｜高Standardizability × Product Fit

## A01-04d.1. Message

**既製Productへ高くFitする案件では、Economics・Delivery・再利用性が競争を決めやすい。**

## A01-04d.2. Chart

**チャートタイトル:** Deal Profile別Positioning｜高Standardizability × Product Fit

### A01-04d.2.1. Chart Structure

```text
① Deal Profile｜6軸
────────────────────────
Decision Altitude          Operational〜Business
Problem Novelty            Low
Analytical Complexity      Low〜Medium
Solution Standardizability High
Implementation Coupling    Medium
Criticality / Governance   Low〜Medium
              ↓
② Customer Selection Criteria｜Weight仮説
────────────────────────
Deal-specific Fit          H
Capability / Quality       M
Delivery Feasibility       H
Economic Value             H
Risk                       M
Evidence / Credibility     M
Relational / Governance    L〜M
Organizational Acceptability M
              ↓
③ Provider Competition｜Position仮説
────────────────────────
AI / Platform Vendor       Strong Candidate
SIer Analytics             Competitive
当チーム                   Relative Weak候補
Consulting Analytics       条件次第
DS Specialist              Relative Weak候補
              ↓
④ Our Position
────────────────────────
**Relative Weak候補**
標準解で十分ならScratch柔軟性は
主要Selection Criteriaに接続しにくい
```

### A01-04d.2.2. Chart内の最小表示テキスト

- 6軸Profileを全表示
- Fit / Delivery / Economics：High Weight
- **AI / Platform Vendor：Strong Candidate**
- **当チーム：Relative Weak候補**

## A01-04d.3. Supporting Logic

### A01-04d.3.1. なぜこの6軸Profileなのか

Operational〜Businessレベルの課題で、Problem Noveltyが低く、既存Product / PlatformのCapabilityへ高くFitする案件を表す。Analytical ComplexityはLow〜Medium、StandardizabilityはHighであり、個別のMethodological Designより既存Assetの再利用価値が高い。

Implementation CouplingはMediumとする。Product単体で完結せず一定のData / Workflow Integrationは必要だが、大規模なEnterprise Architecture変更までは前提としない代表Anchorである。

### A01-04d.3.2. なぜこのSelection Weightになるのか

BUYGRIDは購買の新規性・情報要求によってBuying Processが変わることを示す。[T8]

本Profileでは既知SolutionへのFitが高いため、Deal-specific Fit、Delivery Feasibility、Economic ValueをHighと置く。探索的な専門設計より、既存Capabilityをどれだけ短く・安定して利用できるかが価値になりやすいという当資料の仮説である。

### A01-04d.3.3. Consulting AnalyticsのPosition

Consulting AnalyticsはTransformationやProduct Selection全体では価値を持つが、単純なProduct Fit案件では上位Consulting Capabilityが追加Scoreにならない場合がある。[P2][P3]

### A01-04d.3.4. SIer AnalyticsのPosition

Product導入にLegacy Integration / Security / Data Pipelineが伴う場合、SIerのDelivery Capabilityが効く。[P4] そのためCompetitiveとする。

### A01-04d.3.5. DS SpecialistのPosition

Custom Analysisの必要性が低いほど、専門Analytics人材の希少性が選定理由になりにくい。[P1] 対応可能でも主戦場ではないためRelative Weak候補とする。

### A01-04d.3.6. AI / Platform VendorのPosition

Palantir等のProductized Assetは、Data / Model / Workflow / ActionをPlatform上で再利用可能な形で統合する。[P5]

問題が既存Capabilityへ高くFitする場合、Reuse / Deployment / Scale / Governanceの既存Assetが直接価値になるためStrong Candidateとする。

### A01-04d.3.7. 当チームのPosition

当チームのPredictive / Causal、Scratch / OSS、非定型設計は、顧客固有性が高いほど価値が増す。逆に標準Productで十分な場合、その柔軟性は主要Selection Criteriaに接続しにくい。

従って、

> **Relative Weak候補。対応不能ではなく、Why Usの中心に置く合理性が低い。**

とする。

### A01-04d.3.8. Relative Advantageの有無

Product License / Integration Costが高い、標準Capabilityで重要要件を満たせない、Vendor Lock-in回避が重要等の場合は当チームPositionが上がり得る。したがってProduct Fitが本当に高いかを先に評価すべきである。

### A01-04d.3.9. 反証条件

- Custom Buildの方がTCO / Lead Timeで有利
- ProductではBusiness Requirementを満たせない
- Security / Data residencyでProduct利用が困難
- Portability / Vendor independenceが重要

### A01-04d.3.10. Evidence / Inference区分

**Published Evidence:** BUYGRID、TCE。[T6][T7][T8]

**Provider一次情報:** Palantir / NTT DATA / Deloitte / Accenture / BrainPad。[P1]〜[P5]

**当資料の分析仮説:** 本6軸Profile、8軸Weight、Product Vendor＝Strong Candidate、当チーム＝Relative Weak候補というPositioning。

## A01-04d.4. Speaker Note

このProfileでは「柔軟に作れること」が必ずしも強みではありません。既製Productで十分なら、そのAssetを使う方が合理的な場合があります。当チームの価値は、標準解では足りないときに大きくなります。

## A01-04d.5. A01-04への示唆

> A01-04dは、Standardizabilityが高いほど当チームの非定型設計Capabilityの差別化寄与が下がることを示し、A01-04無印でStandardizability Low〜Mediumを重点条件とする根拠になる。

## A01-04d.6. Sources

- [T8] Robinson, Faris & Wind (1967), *Industrial Buying and Creative Marketing*（BUYGRID）.
- [T6] Williamson (2008), https://doi.org/10.1257/aer.100.3.673
- [T7] David & Han (2004), https://doi.org/10.1002/smj.359
- [P1] BrainPad: https://www.brainpad.co.jp/services/
- [P2] Deloitte AI & Data: https://www.deloitte.com/us/en/services/consulting/services/artificial-intelligence-and-data.html
- [P3] Accenture Data & AI: https://www.accenture.com/us-en/services/data-ai/cloud-data-ai
- [P4] NTT DATA AI Consulting: https://www.nttdata.com/global/en/services/ai/ai-consulting
- [P5] Palantir Operational Applications: https://www.palantir.com/docs/foundry/app-building/operational-apps

## A01-04d.7. Visualization Design Note｜2軸Projection

本Profileの競争Positionは6軸Deal Profileと8つのCustomer Selection Criteriaを用いて評価する。**2軸Mapは、この多次元分析を分かりやすく伝えるためのProjectionとして使用できる。**

説明用の主軸は以下を基本とする。

- 縦軸：**Analytical Complexity**
- 横軸：**Implementation Coupling**

一方、`Decision Altitude / Problem Novelty / Solution Standardizability / Criticality / Governance`は、同じ2軸位置でもSelection CriteriaのWeightとProvider Positionを変え得る**補正条件**として扱う。

従って、2軸MapだけからRelative Advantageを直接導出してはならない。正しい順序は、

> **6軸で競争構造を分析する → 8軸Weight / Provider Positionを評価する → その結果を2軸へ投影して説明する**

である。将来Visualizationを追加する場合、本Profileはこの2軸Map上の代表Anchorとして表示できる。