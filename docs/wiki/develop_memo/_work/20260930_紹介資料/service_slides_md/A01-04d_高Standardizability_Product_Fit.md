Document title: 高Standardizability × Product Fit の競争ポジション

# A01-04d. Appendix｜高Standardizability × Product Fit

## A01-04d.1. Message

**既製Productへ高くFitする案件では、標準化・再利用・展開速度が主要な競争力になる。**

## A01-04d.2. Chart

**チャートタイトル:** Deal Profile別Positioning｜高Standardizability × Product Fit

### A01-04d.2.1. Chart Structure

```text
Deal Profile
────────────────────
Analytical Complexity      Low〜Medium
Implementation Coupling    Medium
Problem Novelty            Low
Solution Standardizability High
Criticality / Governance   Low〜Medium
          ↓
Customer Selection Criteria
────────────────────
Economic Value             ↑↑
Delivery Feasibility       ↑↑
Time-to-Value              ↑↑
Risk                       ↑
Capability / Quality       ↑
          ↓
Provider Position 仮説
────────────────────
AI / Platform Vendor       Strong Candidate
SIer Analytics             Competitive
当チーム                  Relative Weak候補
Consulting Analytics       条件次第
DS Specialist              Relative Weak候補
```

### A01-04d.2.2. Chart内の最小表示テキスト

- 高Standardizability / 高Product Fit
- Economics / Delivery / Time-to-Value重視
- **AI / Platform Vendor：Strong Candidate**
- **当チーム：Relative Weak候補**

## A01-04d.3. Supporting Logic

### A01-04d.3.1. このProfileの特徴

このProfileでは、顧客固有の分析方法を新規設計するより、既にProduct / Platformへ実装されたCapabilityを再利用する方が合理的である可能性が高い。

典型的には、

- 問題定義が比較的定型
- Input / Outputが既知
- Evaluation方法が標準化可能
- Product CapabilityとのGapが小さい
- 大規模展開・反復利用が想定される

という条件を持つ。

このとき顧客価値は「柔軟に何でも作れること」よりも、**既存Assetを使って速く・安定的に・反復可能な形で使えること**へ移る。

### A01-04d.3.2. 標準化が競争軸を変える理論的背景

BUYGRIDではStraight Rebuy / Modified Rebuy / New Taskのように、購買の新規性・情報要求によって購買プロセスが変わるとされる。[T8] 新規性が低くSolutionが既知に近づくほど、探索的な専門設計より、価格・Delivery・既存Supplier / Solutionの評価が相対的に重要になると考える余地がある。

またTCEの観点では、標準Assetの利用により取引固有投資を減らせる場合、個別開発よりGovernance Costを抑えられる可能性がある。[T6][T7]

ただし「標準化すれば必ずProduct Vendorが安い・速い」という実証済み法則ではない。ここから先はDeal条件に基づく当資料の推論である。

### A01-04d.3.3. AI / Platform VendorをStrong Candidateとする根拠

PalantirはOperational Application / Ontology / App Building等をPlatform Capabilityとして提供し、Data・Model・Workflow・Actionを再利用可能なPlatform上で統合する。[P5]

このようなProductized Assetは、問題が既存Capabilityへ高くFitする場合、

- Reuse
- Standardized deployment
- Shared governance
- Scale
- Operationalization

を通じて顧客価値を生み得る。

従って、本ProfileではAI / Platform VendorをStrong Candidateと置く。

### A01-04d.3.4. SIer AnalyticsがCompetitiveとなる理由

Product導入だけでなくLegacy System、Security、Data Pipeline等へのIntegrationが必要なら、SIerのDelivery Capabilityが効く。NTT DATAはAI ConsultingからApplication IntegrationまでをOfferingとして掲げる。[P4]

従って、Product Vendor単独ではなくSIerを含む構成が合理的な場合もある。

### A01-04d.3.5. 当チームのFitが下がる理由

当チームの特徴である、

- Predictive / Causalの問いからの使い分け
- Scratch / OSS
- 非定型Analytical Design

は、顧客固有性が高いほど価値を持つ。

逆に、既製Productで十分な場合、Scratchによる柔軟性は、

- 開発工数
- Test工数
- Maintenance
- Delivery Lead Time

を追加する可能性がある。

そのため本Profileでは、当チームが対応可能でも**Differentiating Capabilityが顧客の主要Selection Criteriaとずれやすい**と評価する。

### A01-04d.3.6. Consulting / DS Specialistの位置づけ

Deloitte / AccentureのようなConsulting AnalyticsはProduct選定を含むTransformation全体では価値を出し得る。[P2][P3] しかし単純なProduct Fit案件では上位Consulting Capabilityが追加価値にならない可能性がある。

DS SpecialistもCustom Analysisが不要なほど標準化された案件では、専門分析の希少性が選定理由になりにくい。[P1]

### A01-04d.3.7. 当チームのPosition

> **Relative Weak候補。対応不能ではなく、Why Usの中心に置く合理性が低い。**

この評価を覆すには、例えば、

- Scratch / OSSでもProductより短納期・低TCO
- Productでは満たせない重要な要件が存在
- 顧客がVendor Lock-in回避を強く評価

などのEvidenceが必要である。

### A01-04d.3.8. 反証条件

- Product License / Integration Costが大きく、Custom Buildの方がTCOで優位
- Productの標準CapabilityではBusiness Requirementを満たせない
- Data residency / Security等によりProduct利用が困難
- 顧客が将来のPortability / Vendor independenceを重視し、Scratch / OSSを選好

これらの場合、当チームPositionは上がり得る。

### A01-04d.3.9. Evidence / Inferenceの区分

**Published Evidence:** Buying Situationが購買行動に影響するBUYGRID、dependency / governanceを扱うTCE。[T6][T7][T8]

**Provider一次情報:** Palantir / NTT DATA / Deloitte / Accenture / BrainPadのOffering。[P1]〜[P5]

**当資料の分析仮説:** 高StandardizabilityではReuse / Economics / Time-to-ValueのWeightが高まり、Product VendorがStrong Candidateになりやすい。

## A01-04d.4. Speaker Note

このProfileでは「柔軟に作れること」が必ずしも強みではありません。既製Productが十分Fitするなら、既存Assetを使う方が速く、保守しやすく、展開しやすい可能性があります。

したがって当チームは、何でもScratchで作ることを売りにはしません。Productで十分ならProductを選ぶ方が合理的です。当チームの強みは、標準解では足りないときに初めて大きくなります。

## A01-04d.5. 次頁への接続

> 次に、技術Solutionより経営・事業変革そのものが購買対象になるProfileを見る。

## A01-04d.6. Sources

- [T8] Robinson, Faris & Wind (1967), *Industrial Buying and Creative Marketing*（BUYGRID）.
- [T6] Williamson (2008), https://doi.org/10.1257/aer.100.3.673
- [T7] David & Han (2004), https://doi.org/10.1002/smj.359
- [P1] BrainPad: https://www.brainpad.co.jp/services/
- [P2] Deloitte AI & Data: https://www.deloitte.com/us/en/services/consulting/services/artificial-intelligence-and-data.html
- [P3] Accenture Data & AI: https://www.accenture.com/us-en/services/data-ai/cloud-data-ai
- [P4] NTT DATA AI Consulting: https://www.nttdata.com/global/en/services/ai/ai-consulting
- [P5] Palantir Operational Applications: https://www.palantir.com/docs/foundry/app-building/operational-apps