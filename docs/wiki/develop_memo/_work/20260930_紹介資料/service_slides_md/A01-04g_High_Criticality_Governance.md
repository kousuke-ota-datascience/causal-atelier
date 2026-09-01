Document title: High Criticality / Governance の競争ポジション

# A01-04g. Appendix｜High Criticality / Governance

## A01-04g.1. Message

**重要度・規制・運用責任が高い案件では、Risk・Evidence・Delivery・Governanceが競争を決めやすい。**

## A01-04g.2. Chart

**チャートタイトル:** Deal Profile別Positioning｜High Criticality / Governance

### A01-04g.2.1. Chart Structure

```text
① Deal Profile｜6軸
────────────────────────
Decision Altitude          Business〜Corporate
Problem Novelty            Medium
Analytical Complexity      Medium〜High
Solution Standardizability Low〜Medium
Implementation Coupling    Medium〜High
Criticality / Governance   High
              ↓
② Customer Selection Criteria｜Weight仮説
────────────────────────
Deal-specific Fit          M〜H
Capability / Quality       H
Delivery Feasibility       H
Economic Value             M
Risk                       H
Evidence / Credibility     H
Relational / Governance    H
Organizational Acceptability H
              ↓
③ Provider Competition｜Position仮説
────────────────────────
SIer Analytics             Strong Candidate
Consulting Analytics       Strong Candidate
当チーム                   Competitive〜Conditional Core
DS Specialist              条件次第
AI / Platform Vendor       Product / Compliance Fit依存
              ↓
④ Our Position
────────────────────────
**Competitive〜Conditional Core**
High Criticality単独では差にならず、
Analytical Complexityも高い場合にPosition上昇
```

### A01-04g.2.2. Chart内の最小表示テキスト

- 6軸Profileを全表示
- Risk / Evidence / Delivery / Governance / Org. Acceptability：High Weight
- **SIer / Consulting：Strong Candidate**
- **当チーム：Analytical Complexityが高いほどPosition上昇**

## A01-04g.3. Supporting Logic

### A01-04g.3.1. なぜこの6軸Profileなのか

この類型は、Business〜CorporateレベルのDecisionで、失敗時の影響・規制・運用責任が大きい案件を表す。

Criticality / GovernanceはHigh、Implementation CouplingはMedium〜High。Analytical ComplexityはMedium〜Highで、標準分析から高度なCausal / Predictiveまで含む。Problem NoveltyはMedium、StandardizabilityはLow〜Mediumとする。

### A01-04g.3.2. なぜこのSelection Weightになるのか

Shethはindustrial buyingでPerceived Riskやpurchase typeをJoint Decisionに関係する要因として扱い、Webster & Windも複数Stakeholderを含む組織的意思決定をモデル化した。[T1][T2]

High Criticalityになるほど、Business / Data-AIだけでなくIT / Security / Legal / Procurement / Management等が関与しやすいと考え、Risk、Evidence、Delivery、Relational / Governance、Organizational AcceptabilityをHighと置く。

TCEはVendor dependency、Switching Cost、Contract adaptation等を考える理論的レンズになる。[T6][T7]

### A01-04g.3.3. Consulting AnalyticsのPosition

Deloitte / Accenture等はAI / Dataに加えてRisk / Governance / Transformationを含むEnterprise-wide Serviceを提供する。[P2][P3]

Policy design、Executive / Risk Committee alignment、Organization-wide controlsが重要ならStrong Candidateとなる。

### A01-04g.3.4. SIer AnalyticsのPosition

NTT DATA等はAI ConsultingからApplication IntegrationまでをOfferingとして持つ。[P4]

Security、Enterprise Architecture、System Delivery、Operation、Governance processがRisk低減へ直結しやすいためStrong Candidateとする。

### A01-04g.3.5. DS SpecialistのPosition

DS SpecialistはMethodologyでは強い可能性があるが、High CriticalityではEnterprise Security、Audit / Governance、Operational Responsibility、Organizational Acceptanceまで必要になる。[P1]

それらを自社またはPartnerでどこまで提供できるかによってFitが変わるため条件次第とする。

### A01-04g.3.6. AI / Platform VendorのPosition

PlatformとしてSecurity / Audit / Governance Capabilityが整備され、顧客要件へFitする場合は強い。[P5]

一方、非定型MethodologyやVendor-neutralityが重要なら評価は変わるためProduct / Compliance Fit依存とする。

### A01-04g.3.7. 当チームのPosition

当チームはPredictive / Causalで問い・前提・評価を分け、CausalではEstimand / Assumption / Identification等、Predictiveではunknown-data performance / calibration / error pattern等を扱う。またSIer内Analytics組織としてEnterprise Contextを持つ。

High CriticalityかつAnalytical Complexityも高い場合、

> **Scientific / Methodological Validity × Enterprise Governance Context**

の双方が評価対象になりやすい。

従って、

> **Competitive〜Conditional Core。Criticality単独ではなくAnalytical Complexityとの掛け合わせが重要。**

とする。

### A01-04g.3.8. Relative Advantageの有無

High Governanceだけなら一般SIer / Consultingとの差別化にならない。High Criticality案件実績、Security / Governance連携、Validation、Auditability、OperationまでのDelivery Model等のEvidenceが必要である。

### A01-04g.3.9. 反証条件

- 顧客が求めるGovernanceが企業全体のRisk Framework中心でConsultingの方が高Fit
- 既存SIerがSystem / Security / OperationとAnalyticsを十分に持つ
- Platform VendorがCompliance要件を製品で満たしCustom Analysis価値が小さい
- 当チームにHigh Criticality案件のEvidenceがない

### A01-04g.3.10. Evidence / Inference区分

**Published Evidence:** Organizational Buying / Industrial Buyer Behavior、TCE。[T1][T2][T6][T7]

**Provider一次情報:** NTT DATA / Deloitte / Accenture / BrainPad / Palantir。[P1]〜[P5]

**当資料の分析仮説:** 本6軸Profile、8軸Weight、SIer / Consulting＝Strong Candidate、当チーム＝Conditional CoreというPositioning。

## A01-04g.4. Speaker Note

重要度の高い案件では、分析精度だけではVendorを選べません。失敗時の影響が大きいため、Security、Governance、責任分界、運用性、Evidenceまで判断材料になります。当チームが差を作れる可能性があるのは、Governanceだけでなく分析そのものも難しい場合です。

## A01-04g.5. A01-04への示唆

> A01-04gのうちAnalytical Complexityも高い領域は、A01-04無印の重点Positioningを補強する。High Governanceだけの案件はA01-04c寄りとなり、当チーム固有の差は弱まる。

## A01-04g.6. Sources

- [T1] Webster & Wind (1972): https://doi.org/10.1177/002224297203600204
- [T2] Sheth (1973): https://doi.org/10.1177/002224297303700408
- [T6] Williamson (2008): https://doi.org/10.1257/aer.100.3.673
- [T7] David & Han (2004): https://doi.org/10.1002/smj.359
- [P1] BrainPad: https://www.brainpad.co.jp/services/
- [P2] Deloitte AI & Data: https://www.deloitte.com/us/en/services/consulting/services/artificial-intelligence-and-data.html
- [P3] Accenture Data & AI: https://www.accenture.com/us-en/services/data-ai/cloud-data-ai
- [P4] NTT DATA AI Consulting: https://www.nttdata.com/global/en/services/ai/ai-consulting
- [P5] Palantir: https://www.palantir.com/docs/foundry/app-building/operational-apps

## A01-04g.7. Visualization Design Note｜2軸Projection

本Profileの競争Positionは6軸Deal Profileと8つのCustomer Selection Criteriaを用いて評価する。**2軸Mapは、この多次元分析を分かりやすく伝えるためのProjectionとして使用できる。**

説明用の主軸は以下を基本とする。

- 縦軸：**Analytical Complexity**
- 横軸：**Implementation Coupling**

一方、`Decision Altitude / Problem Novelty / Solution Standardizability / Criticality / Governance`は、同じ2軸位置でもSelection CriteriaのWeightとProvider Positionを変え得る**補正条件**として扱う。

従って、2軸MapだけからRelative Advantageを直接導出してはならない。正しい順序は、

> **6軸で競争構造を分析する → 8軸Weight / Provider Positionを評価する → その結果を2軸へ投影して説明する**

である。将来Visualizationを追加する場合、本Profileはこの2軸Map上の代表Anchorとして表示できる。