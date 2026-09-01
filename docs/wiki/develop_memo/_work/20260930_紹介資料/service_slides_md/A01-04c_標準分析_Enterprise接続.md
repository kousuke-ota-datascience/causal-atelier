Document title: 標準分析 × Enterprise接続 の競争ポジション

# A01-04c. Appendix｜標準分析 × Enterprise接続

## A01-04c.1. Message

**分析が標準化し実装比重が高い案件では、SIer型Deliveryの重要性が高まる。**

## A01-04c.2. Chart

**チャートタイトル:** Deal Profile別Positioning｜標準分析 × Enterprise接続

### A01-04c.2.1. Chart Structure

```text
Deal Profile
────────────────────
Analytical Complexity      Low〜Medium
Implementation Coupling    High
Problem Novelty            Low〜Medium
Solution Standardizability Medium〜High
Criticality / Governance   Medium〜High
          ↓
Customer Selection Criteria
────────────────────
Delivery Feasibility       ↑↑
Risk                       ↑↑
Org. Acceptability         ↑↑
Economic Value             ↑
Capability / Quality       ↑
          ↓
Provider Position 仮説
────────────────────
SIer Analytics             Strong Candidate
当チーム                  Competitive
Consulting Analytics       Competitive / 条件次第
AI / Platform Vendor       Product Fit依存
DS Specialist              Competitive / Fit低下可能性
```

### A01-04c.2.2. Chart内の最小表示テキスト

- 低〜中Analytical Complexity
- 高Implementation Coupling
- Delivery / Risk / Org. Acceptability重視
- **SIer Analytics：Strong Candidate**
- **当チーム：Competitive**

## A01-04c.3. Supporting Logic

### A01-04c.3.1. このProfileの特徴

典型的には、分析手法そのものは既知であり、案件難易度の中心が以下へ移っている。

- Data Pipeline / Data Quality
- API / Batch / Workflow Integration
- Security / Access Control
- Production Reliability
- Monitoring / Operation
- Release / Change Management
- Governance / Auditability

この場合、顧客が購入している価値は「新しい分析方法」よりも、**既知の分析をEnterprise環境で安全・安定的に成立させるDelivery**へ近づく。

Webster & Wind / ShethのOrganizational Buying研究では、購買意思決定が複数StakeholderのExpectationによって構成される。[T1][T2] Implementation Couplingが高い場合、Business / Data-AIに加えIT / Security / Operation / ProcurementがBuying Centerへ入りやすいため、Delivery / Risk / Organizational AcceptabilityのWeightが高まる、というのが本資料の仮説である。

### A01-04c.3.2. Delivery / RiskのWeightが上がる理論的背景

TCEではAsset Specificity / Uncertainty等がGovernance設計上の主要属性として扱われる。[T6][T7]

Enterprise Systemへ組み込むほど、Vendor変更、データ連携、運用移管等にSwitching Costが生じやすく、顧客は単なるModel Quality以外に、

- 継続Delivery能力
- 契約・責任分界
- Security / Compliance
- Operation support
- Vendor dependency

を評価する必要がある。

従って、本ProfileでDelivery / Riskが重くなることには一定の理論的裏付けがある。

### A01-04c.3.3. SIer AnalyticsをStrong Candidateとする根拠

NTT DATAのAI ConsultingはPoC / Model TrainingだけでなくApplication Integrationまでを一連のOfferingとして明示している。[P4]

SIer型Providerは一般に、Analytics部門の外側にも、

- Cloud / Infrastructure
- Enterprise Architecture
- Security
- Application Development
- Managed Service

等のCapabilityを企業内に持つ場合がある。

このため、本Profileでは「分析専門性が圧倒的に高いか」より、**分析をEnterprise Deliveryへ接続できる組織能力**が価値になりやすい。

ただし「SIerなら常に勝つ」とはしない。既存ProductやPlatformで十分な場合はAI Vendorが合理的であり、Transformation全体が主課題ならConsultingが強い場合もある。

### A01-04c.3.4. AI / Platform VendorがProduct Fit次第で強くなる理由

PalantirのようなPlatform ProviderはOperational Application / Ontology等を通じ、Data・Model・Workflow・Actionを統合する。[P5]

分析が標準化されており、その問題がPlatformの既存Capabilityへ高くFitするなら、個別SIよりもReuse / Deployment Speed / Platform Integrationが高いValueを持ち得る。

逆に、Product外のLegacy Integrationや特殊なEnterprise制約が大きい場合には、一般的なSI Capabilityの比重が高まる。

### A01-04c.3.5. Consulting Analyticsを条件付きCompetitiveとする理由

Deloitte / AccentureはAI StrategyだけでなくEngineering / Build / Scaleを公式に提供する。[P2][P3]

従って、Consulting Analyticsも本Profileへ参入できる。

ただし、案件価値の中心がPure System Delivery / Operationに寄り、Transformation / Business Design / Stakeholder AlignmentのWeightが低い場合、Consultingの上位Capabilityが必ずしも差別化Scoreにならない。

### A01-04c.3.6. DS SpecialistのFitが低下し得る理由

DS Specialistは分析部分で十分対応可能である。[P1]

一方、Enterprise Deliveryを自社Capabilityとしてどこまで持つかは企業差がある。Partner依存が大きい場合、顧客から見ると、

- Responsibility boundary
- Integration governance
- Operation continuity

が追加Riskになり得る。

従って本資料では「DS Specialistは弱い」ではなく、**Implementation Couplingが上がるほどAnalytics以外のCapabilityが評価に加わるため、相対Fitが低下する可能性がある**とする。

### A01-04c.3.7. 当チームのPosition

当チームはSIer内Analytics組織であるため、本ProfileのDelivery / Risk / Org. Acceptabilityと親和性がある。

しかし、01-05で差別化候補としている、

- Predictive / Causal
- Scratch / OSS
- 非定型Analytical Design

の価値は、Analytical Complexityが低〜中になるほど相対的に小さくなる。

したがって、

> **Competitive。ただしWhy Usの中心領域ではない。**

と評価する。

### A01-04c.3.8. 相対優位を主張しない理由

このProfileでは当チームより規模の大きいSIer Analytics、既存Systemの担当SIer、Platform Vendor等が構造的に有利な場合がある。

特に顧客が、

- 既存Vendorとの契約容易性
- Installed Base
- Production体制
- SLA
- Operation cost

を強く重視する場合、当チームの高度分析Capabilityは選定理由になりにくい。

### A01-04c.3.9. 反証条件 / Evidence Gap

以下を確認できれば評価を上げ得る。

- 当チームが分析からProduction handoffまで一貫して低コスト・短Lead Timeで提供した実績
- 他SIer Analyticsより少人数でPoC〜実装を接続できるDelivery Model
- 顧客から「分析専門性があるSIer部門だから選んだ」という明確なSelection Evidence

逆に、既存SIerやPlatform Vendorが同等品質をより低いTCOで提供できるなら、本Profileでの当チームPositionは下がる。

### A01-04c.3.10. Evidence / Inferenceの区分

**Published Evidence**
- Organizational Buyingでは複数Stakeholder / 複数基準が作用する。[T1][T2]
- TCEはSystem結合・依存・Switching Costを考える理論的レンズになる。[T6][T7]

**Provider一次情報**
- NTT DATA / Deloitte / Accenture / Palantir / BrainPadの公式Offering。[P1]〜[P5]

**当資料の分析仮説**
- 標準分析 × 高Implementation CouplingではDelivery / Risk / Org. AcceptabilityのWeightが高まる。
- SIer AnalyticsをStrong Candidate、当チームをCompetitiveとする評価。

## A01-04c.4. Speaker Note

このProfileでは、モデルよりも「Enterpriseで動かすこと」が難所になります。そのため、SIer型ProviderのDelivery capabilityが前面に出ます。

当チームもSIer内の分析組織なので十分競争できます。しかし、分析が標準的ならPredictive / CausalやScratch設計といった当チームの専門性は決定的な差になりません。

したがって、ここを当チームの主戦場とは置きません。勝てる可能性はありますが、勝因は当チーム固有のWhy Usというより、既存関係、Delivery体制、価格、System知識等に依存する可能性が高いと考えます。

## A01-04c.5. 次頁への接続

> さらにSolution Standardizabilityが高くなると、個別SIよりも既製Product / Platformの再利用性が競争軸になり得る。

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