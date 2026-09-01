Document title: Standard / Commodity Analysis の競争ポジション

# A01-04h. Appendix｜Standard / Commodity Analysis

## A01-04h.1. Message

**標準的・低新規性の分析案件では、Economicsと基本Deliveryが競争を決めやすい。**

## A01-04h.2. Chart

**チャートタイトル:** Deal Profile別Positioning｜Standard / Commodity Analysis

### A01-04h.2.1. Chart Structure

```text
① Deal Profile｜6軸
────────────────────────
Decision Altitude          Operational
Problem Novelty            Low
Analytical Complexity      Low
Solution Standardizability High
Implementation Coupling    Low
Criticality / Governance   Low
              ↓
② Customer Selection Criteria｜Weight仮説
────────────────────────
Deal-specific Fit          L〜M
Capability / Quality       M
Delivery Feasibility       M
Economic Value             H
Risk                       M
Evidence / Credibility     L〜M
Relational / Governance    L
Organizational Acceptability M
              ↓
③ Provider Competition｜Position仮説
────────────────────────
AI / Product Vendor        Strong Candidate（Product Fit時）
Low-cost / General Provider Competitive
内製                       Strong Alternative
SIer Analytics             Competitive
DS Specialist              Competitive
Consulting Analytics       Relative Weak候補
当チーム                   Relative Weak〜Competitive
              ↓
④ Our Position
────────────────────────
**Relative Weak〜Competitive**
対応可能だが、Specialist Analytics / Enterprise Baseの
追加価値が小さい
```

### A01-04h.2.2. Chart内の最小表示テキスト

- 6軸Profileを全表示
- Economics：High Weight
- Standardizability：High
- **内製 / Product / Low-cost Providerが有力になり得る**
- **当チーム：Relative Weak〜Competitive**

## A01-04h.3. Supporting Logic

### A01-04h.3.1. なぜこの6軸Profileなのか

この類型は、Operationalレベルの定型的な分析を表す。

例として、既知のKPI集計・簡易予測、標準的な分類 / Regression、定型Featureを用いたModeling、既存TemplateやAutoMLで十分な分析、分析結果が単体で完結しEnterprise Integrationもほぼ不要な案件を想定する。

Problem Novelty、Analytical Complexity、Implementation Coupling、CriticalityはLow、Solution StandardizabilityはHighとする。

### A01-04h.3.2. なぜこのSelection Weightになるのか

BUYGRIDでは購買新規性が低いほど探索・情報要求が減る状況を扱う。[T8]

本Profileでは高度なMethodological ExpertiseやEnterprise Governanceを必要としないため、Economic ValueをHighと置く。Capability / Delivery / Riskは必要だが、一定水準を満たせばQualifying Signalになりやすく、卓越性としての差がつきにくいというProfessional ServiceのSignal論とも整合的である。[T4]

### A01-04h.3.3. Consulting AnalyticsのPosition

Corporate StrategyやTransformationのCapabilityは、本Profileではほぼ評価されない。高単価の上位CapabilityがEconomics上の不利になる可能性もあるためRelative Weak候補とする。

### A01-04h.3.4. SIer AnalyticsのPosition

SIer Analyticsは十分対応可能だが、Implementation CouplingがLowのためEnterprise Delivery力が大きな加点にならない。既存契約、顧客データへのAccess、既知System理解等があればCompetitiveになり得る。

### A01-04h.3.5. DS SpecialistのPosition

DS Specialistも十分対応できるが、高度な専門性が不要な場合、その希少CapabilityはSelection Criteriaに変換されにくい。価格、Lead Time、既存関係次第でCompetitiveとなる。

### A01-04h.3.6. AI / Product Vendor・内製のPosition

Problemが定型でStandardizabilityが高い場合、AutoML / BI / 既製AI機能等のProduct Fitが高くなりやすい。また低Criticality・低Complexityであれば顧客内製も合理的なAlternativeとなる。

従ってProduct Vendorや内製はStrong Alternativeになり得る。

### A01-04h.3.7. 当チームのPosition

当チームのPredictive / Causalの高度な使い分け、Scratch / OSSによる非定型設計、Enterprise Contextは、本Profileでは過剰Capabilityになり得る。

従って、

> **Relative Weak〜Competitive。対応可能だが、Why Usの中心に置くべきではない。**

とする。

### A01-04h.3.8. Relative Advantageの有無

当チームがこのProfileで選ばれるとすれば、既存取引、顧客Data理解、短Lead Time、低Price等の別要因が必要である。しかしそれらは現時点で確認済みの差別化Evidenceではないため、構造的Relative Advantageは主張しない。

### A01-04h.3.9. 反証条件

- 標準案件でも当チームが他Providerより明確に低Price / 短Lead Time
- 既存顧客環境へのAccessが圧倒的に容易
- Commodityに見える案件でも実際には高いCriticality / Governanceがあり、Enterprise Baseが効く

これらの場合はPositionを上げ得る。

### A01-04h.3.10. Evidence / Inference区分

**Published Evidence:** BUYGRID、Professional Service Signal。[T4][T8]

**Provider一次情報:** 各Providerが広いAnalytics Offeringを持つことはA01-04a〜gのSourcesを参照。

**当資料の分析仮説:** 本6軸Profile、8軸Weight、Product / 内製 / Low-cost Providerが相対的に合理的になりやすく、当チーム＝Relative Weak〜CompetitiveというPositioning。

## A01-04h.4. Speaker Note

このProfileは、当チームが対応できない領域ではありません。ただし高度な分析設計もEnterprise接続もほとんど必要ないなら、当チームの専門Capabilityを使う必然性が弱くなります。

その場合、Product、内製、より低コストなProviderが合理的な場合があります。こうした領域まで「当チームが強い」と主張しないことが、A01-04全体のPositioningの説得力につながります。

## A01-04h.5. A01-04への示唆

> A01-04hは、Problem Novelty / Analytical Complexity / Implementation Couplingが低い領域では当チームのCapability Bundleが価値化しにくいことを示す。A01-04無印の重点条件を高Novelty・高Complexity・一定以上のEnterprise接続へ絞る根拠となる。

## A01-04h.6. Sources

- [T8] Robinson, Faris & Wind (1967), *Industrial Buying and Creative Marketing*（BUYGRID）.
- [T4] Pemer, F. & Skjølsvik, T. (2019), “The cues that matter: Screening for quality signals in the ex ante phase of buying professional services,” *Journal of Business Research*, 98, 352–365. https://doi.org/10.1016/j.jbusres.2019.02.005

※Provider別の一次情報はA01-04a〜gの各Sourcesを参照。

## A01-04h.7. Visualization Design Note｜2軸Projection

本Profileの競争Positionは6軸Deal Profileと8つのCustomer Selection Criteriaを用いて評価する。**2軸Mapは、この多次元分析を分かりやすく伝えるためのProjectionとして使用できる。**

説明用の主軸は以下を基本とする。

- 縦軸：**Analytical Complexity**
- 横軸：**Implementation Coupling**

一方、`Decision Altitude / Problem Novelty / Solution Standardizability / Criticality / Governance`は、同じ2軸位置でもSelection CriteriaのWeightとProvider Positionを変え得る**補正条件**として扱う。

従って、2軸MapだけからRelative Advantageを直接導出してはならない。正しい順序は、

> **6軸で競争構造を分析する → 8軸Weight / Provider Positionを評価する → その結果を2軸へ投影して説明する**

である。将来Visualizationを追加する場合、本Profileはこの2軸Map上の代表Anchorとして表示できる。