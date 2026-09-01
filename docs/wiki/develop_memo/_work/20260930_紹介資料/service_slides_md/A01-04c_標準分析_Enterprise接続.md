Document title: 標準分析 × Enterprise接続 の競争ポジション

# A01-04c. Appendix｜標準分析 × Enterprise接続

## A01-04c.1. Message

**分析が標準化し実装比重が高い案件では、Delivery・Risk・組織適合性が競争を決めやすい。**

## A01-04c.2. Chart

**チャートタイトル:** Deal Profile別Positioning｜標準分析 × Enterprise接続

### A01-04c.2.1. Chart Structure

```text
① Deal Profile｜6軸
────────────────────────
Decision Altitude          Operational〜Business
Problem Novelty            Low〜Medium
Analytical Complexity      Low〜Medium
Solution Standardizability Medium〜High
Implementation Coupling    High
Criticality / Governance   Medium〜High
              ↓
② Customer Selection Criteria｜Weight仮説
────────────────────────
Deal-specific Fit          M
Capability / Quality       M
Delivery Feasibility       H
Economic Value             M〜H
Risk                       H
Evidence / Credibility     M
Relational / Governance    M
Organizational Acceptability H
              ↓
③ Provider Competition｜Position仮説
────────────────────────
SIer Analytics             Strong Candidate
当チーム                   Competitive
Consulting Analytics       Competitive / 条件次第
AI / Platform Vendor       Product Fit依存
DS Specialist              Competitive / Fit低下可能性
              ↓
④ Our Position
────────────────────────
**Competitive**
Enterprise Baseは効くが、
Specialist Analytics側の差別化寄与は小さい
```

### A01-04c.2.2. Chart内の最小表示テキスト

- 6軸Profileを全表示
- Delivery / Risk / Org. Acceptability：High Weight
- **SIer Analytics：Strong Candidate**
- **当チーム：Competitive**

## A01-04c.3. Supporting Logic

### A01-04c.3.1. なぜこの6軸Profileなのか

この類型は、Operational〜Businessレベルの既知・比較的標準的な分析を、Enterprise System / Workflowへ高く結合させる案件を表す。

Decision AltitudeはOperational〜Business。Corporate Strategyではなく、既存業務の予測・分類・最適化等を実装・運用へ載せることが中心となる。

Problem NoveltyとAnalytical ComplexityはLow〜Medium、StandardizabilityはMedium〜High。分析方法自体よりData Pipeline、API / Batch、Security、Monitoring、Release、Operation等が難所になる。

Implementation CouplingとCriticalityはHigh / Medium〜Highであり、失敗時の業務影響や運用責任も無視できない。

### A01-04c.3.2. なぜこのSelection Weightになるのか

Organizational Buying研究では、複数Stakeholder・複数ExpectationがSupplier Selectionに影響する。[T1][T2]

Implementation Couplingが高い本ProfileではBusiness / Data-AIだけでなくIT / Security / Operation / ProcurementもBuying Centerへ入りやすいため、Delivery Feasibility / Risk / Organizational AcceptabilityをHighと置く。

TCEのAsset Specificity / Uncertaintyは、System結合、Switching Cost、責任分界、Vendor dependencyを考えるレンズとなる。[T6][T7]

### A01-04c.3.3. Consulting AnalyticsのPosition

Deloitte / AccentureはEngineering / Build / Scaleまで提供するため本Profileにも参入できる。[P2][P3]

ただしTransformationやStakeholder AlignmentのWeightが低いPure Delivery中心の案件では、その上位Capabilityが必ずしも追加ScoreにならないためCompetitive / 条件次第とする。

### A01-04c.3.4. SIer AnalyticsのPosition

NTT DATA等はPoC / Model TrainingからApplication IntegrationまでOfferingとして持つ。[P4]

本ProfileではEnterprise Architecture、Security、Application Development、Managed Service等が直接評価されるためStrong Candidateとする。

### A01-04c.3.5. DS SpecialistのPosition

DS Specialistも分析部分では対応可能だが、Enterprise Deliveryを自社でどこまで持つかは企業差が大きい。[P1]

Implementation Couplingが高いほどResponsibility Boundary / Integration Governance / Operation Continuityが追加評価となるため、CompetitiveだがFit低下可能性ありとする。

### A01-04c.3.6. AI / Platform VendorのPosition

Palantir等はData・Model・Workflow・Actionの統合Assetを持つ。[P5]

問題がPlatform Capabilityへ高くFitする場合は非常に強い。一方Legacy Integrationや特殊制約が大きければSIer型Capabilityがより効くためProduct Fit依存とする。

### A01-04c.3.7. 当チームのPosition

当チームはSIer内Analytics組織としてDelivery / Risk / Organizational Acceptabilityと親和性がある。

一方、Predictive / Causal、Scratch / OSS、非定型Analytical Designの価値は、Analytical Complexityが低〜中になるほど小さくなる。

従って、

> **Competitive。ただしWhy Usの中心領域ではない。**

とする。

### A01-04c.3.8. Relative Advantageの有無

既存SIer、Installed Baseを持つProvider、Platform Vendor等がより合理的な場合がある。特にSLA、Operation Cost、既存契約、System Knowledgeが重い場合は当チームの分析専門性が選定理由になりにくい。

### A01-04c.3.9. 反証条件

- 当チームがPoC〜Production handoffを他SIerより低コスト・短Lead Timeで提供した実績がある
- 顧客から「分析専門性を持つSIerだから選んだ」という明確なSelection Evidenceがある
- 逆に既存SIer / Platform Vendorが同等品質をより低TCOで提供できる場合はPositionを下げる

### A01-04c.3.10. Evidence / Inference区分

**Published Evidence:** Organizational Buying、TCE。[T1][T2][T6][T7]

**Provider一次情報:** NTT DATA、Deloitte、Accenture、Palantir、BrainPad。[P1]〜[P5]

**当資料の分析仮説:** 本6軸Profile、8軸Weight、SIer Analytics＝Strong Candidate、当チーム＝CompetitiveというPositioning。

## A01-04c.4. Speaker Note

このProfileではモデルより「Enterpriseで動かすこと」が難所です。そのためSIer型Deliveryが前面に出ます。当チームも競争できますが、高度分析の専門性が決定的な差になりにくいため、主戦場とは置きません。

## A01-04c.5. A01-04への示唆

> A01-04cは、Enterprise Baseだけが効くProfileでは当チーム固有のWhy Usが弱まることを示す。A01-04無印で重点とするにはAnalytical Complexity / Noveltyも同時に高い必要がある。

## A01-04c.6. Sources

- [T1] Webster & Wind (1972), *Journal of Marketing*. https://doi.org/10.1177/002224297203600204
- [T2] Sheth (1973), *Journal of Marketing*. https://doi.org/10.1177/002224297303700408
- [T6] Williamson (2008), “Transaction Cost Economics: The Natural Progression.” https://doi.org/10.1257/aer.100.3.673
- [T7] David & Han (2004), “A Systematic Assessment of the Empirical Support for Transaction Cost Economics.” https://doi.org/10.1002/smj.359
- [P1] BrainPad: https://www.brainpad.co.jp/services/
- [P2] Deloitte AI & Data: https://www.deloitte.com/us/en/services/consulting/services/artificial-intelligence-and-data.html
- [P3] Accenture Data & AI: https://www.accenture.com/us-en/services/data-ai/cloud-data-ai
- [P4] NTT DATA AI Consulting: https://www.nttdata.com/global/en/services/ai/ai-consulting
- [P5] Palantir Operational Applications: https://www.palantir.com/docs/foundry/app-building/operational-apps

## A01-04c.7. Visualization Design Note｜2軸Projection

本Profileの競争Positionは6軸Deal Profileと8つのCustomer Selection Criteriaを用いて評価する。**2軸Mapは、この多次元分析を分かりやすく伝えるためのProjectionとして使用できる。**

説明用の主軸は以下を基本とする。

- 縦軸：**Analytical Complexity**
- 横軸：**Implementation Coupling**

一方、`Decision Altitude / Problem Novelty / Solution Standardizability / Criticality / Governance`は、同じ2軸位置でもSelection CriteriaのWeightとProvider Positionを変え得る**補正条件**として扱う。

従って、2軸MapだけからRelative Advantageを直接導出してはならない。正しい順序は、

> **6軸で競争構造を分析する → 8軸Weight / Provider Positionを評価する → その結果を2軸へ投影して説明する**

である。将来Visualizationを追加する場合、本Profileはこの2軸Map上の代表Anchorとして表示できる。