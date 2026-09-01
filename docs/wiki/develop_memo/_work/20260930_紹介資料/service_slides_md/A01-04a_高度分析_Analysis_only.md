Document title: 高度分析 × Analysis-only の競争ポジション

# A01-04a. Appendix｜高度分析 × Analysis-only

## A01-04a.1. Message

**分析難易度が高く実装接続が弱い案件では、Capability・Fit・Evidenceが競争を決めやすい。**

## A01-04a.2. Chart

**チャートタイトル:** Deal Profile別Positioning｜高度分析 × Analysis-only

### A01-04a.2.1. Chart Structure

```text
① Deal Profile｜6軸
────────────────────────
Decision Altitude          Operational〜Business
Problem Novelty            Medium〜High
Analytical Complexity      High
Solution Standardizability Low〜Medium
Implementation Coupling    Low
Criticality / Governance   Low〜Medium
              ↓
② Customer Selection Criteria｜Weight仮説
────────────────────────
Deal-specific Fit          H
Capability / Quality       H
Delivery Feasibility       L
Economic Value             M
Risk                       L〜M
Evidence / Credibility     H
Relational / Governance    M
Organizational Acceptability L
              ↓
③ Provider Competition｜Position仮説
────────────────────────
DS Specialist              Strong candidate
Consulting Analytics       Competitive
当チーム                   Competitive
SIer Analytics             Competitive / 条件次第
AI / Platform Vendor       Product Fit依存
              ↓
④ Our Position
────────────────────────
**Competitive**
Enterprise Baseの追加価値は小さく、
Relative Advantageは専門性・実績・Economics次第
```

### A01-04a.2.2. Chart内の最小表示テキスト

- 6軸Profileを全表示
- Capability / Fit / Evidence：High Weight
- Delivery / Org. Acceptability：Low Weight
- **DS Specialist：Strong candidate**
- **当チーム：Competitive**

## A01-04a.3. Supporting Logic

### A01-04a.3.1. なぜこの6軸Profileなのか

この類型は、具体的な業務・事業判断に使う高度分析ではあるが、PoC成果を直ちにEnterprise Systemへ組み込むことが主目的ではない案件を表す。

Decision AltitudeはOperational〜Businessとする。純粋なCorporate Transformationではなく、需要予測、リスク推定、因果効果推定、Target Definition等の具体的なDecision Problemを主対象とするためである。

Problem NoveltyとAnalytical ComplexityはMedium〜High / Highとする。既存テンプレートを適用するだけでなく、Outcome、Treatment、Estimand、Assumption、Evaluation等を個別設計する余地が大きい。

一方、Implementation CouplingはLowであり、System Integration、Security Architecture、Production Operation等は案件価値の中心ではない。

### A01-04a.3.2. なぜこのSelection Weightになるのか

B2B購買ではBuying Situation、関係Stakeholder、Perceived Risk等によって評価基準が変化する。[T1][T2][T3]

本Profileでは分析品質そのものが主要成果物であるため、Deal-specific Fit / Capability / EvidenceをHighと置く。Professional Serviceは購入前に品質を直接観察しにくく、専門家・実績・評判等のSignalが重要になるという研究とも整合する。[T4][T5]

Implementation Couplingが低いためDelivery FeasibilityとOrganizational Acceptabilityは相対的に低く置く。ただし顧客環境でのData access等は必要なためゼロではない。

### A01-04a.3.3. Consulting AnalyticsのPosition

Consulting Analyticsも高度なAI / Data / MLのBuildやAnalyticsを提供しており、「ConsultingはStrategyだけ」という前提は置かない。[P2][P3]

一方、Transformation / Stakeholder Alignmentが主要評価軸でないDealでは、それらのCapabilityが追加Scoreにならないため、本ProfileではCompetitiveと置く。

### A01-04a.3.4. SIer AnalyticsのPosition

SIer Analyticsも高度なData Science / AI Consulting / PoCを提供し得る。[P4]

ただしImplementation Couplingが低い本Profileでは、Integration / Security / Production等のEnterprise CapabilityのWeightが下がる。従って勝敗はAnalytical CapabilityとRelevant Evidenceへ寄りやすい。

### A01-04a.3.5. DS SpecialistのPosition

専門Analytics会社はData Scientist等の専門人材と個別分析Projectを主要Offeringとして持つ場合があり、高度分析そのものが成果物となるDealとBusiness Model上のFitが高い。[P1]

そのためStrong candidateとする。ただし個別企業間の実績・価格・人材差まで含めた実測順位ではない。

### A01-04a.3.6. AI / Platform VendorのPosition

AI / Platform VendorはPlatform Assetや標準Capabilityが顧客問題へFitすれば強い。[P5]

ただし個別のOutcome / Treatment / Evaluation設計が中心でPlatform導入価値が小さい場合、標準Assetの寄与は低下するためProduct Fit依存とする。

### A01-04a.3.7. 当チームのPosition

当チームのPredictive / Causal、Scratch / OSS、前提・評価設計は本ProfileとFitする。一方、`Specialist Analytics × Enterprise Base`のうちEnterprise Baseが大きく加点されない。

従って、

> **Competitive。ただし構造的Relative Advantageは未確認。**

とする。

### A01-04a.3.8. Relative Advantageの有無

当チームがこのProfileで競合を上回るには、Methodological Expertise、Relevant Evidence、Specialist Direct Access、Price / Lead Time等で具体的なCompetitive Gapが必要である。

現時点でそれを裏付ける比較データは不足しているため「当チームが最も強い」とは主張しない。

### A01-04a.3.9. 反証条件

以下の場合はPositionを修正する。

- Relevant DS Specialistが当チームより高い専門実績・人材を持つ
- Consulting Analyticsが同等以上のHands-on Capabilityをより高いEconomic Valueで提供する
- 顧客が既存Vendor契約等を強く重視し、Implementation Couplingが低くてもOrganizational AcceptabilityのWeightが高い
- Product Vendorの既存Capabilityへ問題が高くFitする

### A01-04a.3.10. Evidence / Inference区分

**Published Evidence:** B2B購買の状況依存性、Professional ServiceのQuality Signal、Consulting選定におけるreputation / industry experience等。[T1]〜[T5]

**Provider一次情報:** BrainPad、Deloitte、Accenture、NTT DATA、PalantirのOffering。[P1]〜[P5]

**当資料の分析仮説:** 本6軸Profile、8軸Weight、Provider Positionの順位づけ。学術研究がこの順位を直接実証したものではない。

## A01-04a.4. Speaker Note

このProfileでは分析そのものが商品です。高度なPredictive / Causal、特殊な評価設計等が中心で、本番Systemとの接続はまだ重要ではありません。そのためCapability、案件Fit、関連実績が競争軸になります。

当チームは十分競争できますが、SIerとしてのEnterprise Baseが差になりにくいため、ここを最重要のWhy Us領域とは置きません。

## A01-04a.5. A01-04への示唆

> 高度分析だけでは当チーム固有のCapability Bundleは全面的に効かない。Implementation Couplingが高まったA01-04bで、Specialist AnalyticsとEnterprise Baseが同時に価値化するかを確認する。

## A01-04a.6. Sources

### Academic / Published
- [T1] Webster, F. E. Jr. & Wind, Y. (1972), “A General Model for Understanding Organizational Buying Behavior,” *Journal of Marketing*, 36(2), 12–19. https://doi.org/10.1177/002224297203600204
- [T2] Sheth, J. N. (1973), “A Model of Industrial Buyer Behavior,” *Journal of Marketing*, 37(4), 50–56. https://doi.org/10.1177/002224297303700408
- [T3] “B2B customer journeys: Conceptualization and an integrative framework,” *Industrial Marketing Management*, 113 (2023), 74–87. https://doi.org/10.1016/j.indmarman.2023.05.020
- [T4] Pemer, F. & Skjølsvik, T. (2019), “The cues that matter,” *Journal of Business Research*, 98, 352–365. https://doi.org/10.1016/j.jbusres.2019.02.005
- [T5] Patterson, P. G. (1995), “Choice Criteria in Final Selection of a Management Consultancy Service,” *Journal of Professional Services Marketing*, 11(2), 177–187. https://doi.org/10.1300/J090v11n02_13

### Provider primary sources
- [P1] BrainPad, Services: https://www.brainpad.co.jp/services/
- [P2] Deloitte, AI & Data: https://www.deloitte.com/us/en/services/consulting/services/artificial-intelligence-and-data.html
- [P3] Accenture, Data & AI: https://www.accenture.com/us-en/services/data-ai/cloud-data-ai
- [P4] NTT DATA, AI Consulting: https://www.nttdata.com/global/en/services/ai/ai-consulting
- [P5] Palantir, Operational Applications: https://www.palantir.com/docs/foundry/app-building/operational-apps