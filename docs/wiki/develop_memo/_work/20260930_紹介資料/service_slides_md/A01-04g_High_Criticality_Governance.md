Document title: High Criticality / Governance の競争ポジション

# A01-04g. Appendix｜High Criticality / Governance

## A01-04g.1. Message

**重要度・規制・運用責任が高い案件では、RiskとGovernanceへの対応力が選定を左右する。**

## A01-04g.2. Chart

**チャートタイトル:** Deal Profile別Positioning｜High Criticality / Governance

### A01-04g.2.1. Chart Structure

```text
Deal Profile
────────────────────
Criticality / Governance   High
Implementation Coupling    Medium〜High
Analytical Complexity      Medium〜High
Problem Novelty            Medium
Solution Standardizability Low〜Medium
Decision Altitude          Business〜Corporate
          ↓
Customer Selection Criteria
────────────────────
Risk                       ↑↑
Evidence / Credibility     ↑↑
Delivery Feasibility       ↑↑
Org. Acceptability         ↑↑
Relational / Governance    ↑↑
Capability / Quality       ↑
          ↓
Provider Position 仮説
────────────────────
SIer Analytics             Strong Candidate
Consulting Analytics       Strong Candidate
当チーム                  Competitive〜Core Candidate
DS Specialist              条件次第
AI / Platform Vendor       Product / Compliance Fit依存
```

### A01-04g.2.2. Chart内の最小表示テキスト

- High Criticality / Governance
- Risk / Evidence / Delivery / Org. Acceptability重視
- **SIer / Consulting：Strong Candidate**
- **当チーム：Analytical Complexityが高いほどPosition上昇**

## A01-04g.3. Supporting Logic

### A01-04g.3.1. このProfileの特徴

High Criticality案件では、「分析できるか」だけでなく、**間違った場合に何が起きるか、そのRiskを誰がどう管理できるか**が購買判断に入る。

典型的には、

- Financial / Credit / Risk decision
- Safety-sensitive Operation
- Regulated business process
- Large investment / resource allocation
- Mission Critical workflow
- 顧客・従業員への重大な影響を持つDecision

等である。

この場合、顧客はModel AccuracyやEffect Estimateだけでなく、

- Security
- Compliance
- Auditability
- Explainability / Decision rationale
- Operational Control
- Responsibility boundary
- Incident / failure response
- Change / Model governance

まで含めてProviderを評価する必要がある。

### A01-04g.3.2. Perceived RiskがBuying Processを変える根拠

Sheth (1973)はindustrial buyingにおいて、perceived riskやpurchase type等がJoint Decision / Autonomous Decisionへ影響する要因として扱われている。[T2]

Webster & Windも、Organizational Buyingを複数Stakeholder・組織要因を含む意思決定として扱う。[T1]

High Criticalityになるほど、事業部門だけでなく、IT / Security / Legal / Procurement / Management等の関与が増える可能性がある。したがって、単純なAnalytical Capabilityよりも、Risk / Governance / Organizational AcceptabilityがSupplier Selectionへ強く入る、というのが本資料の仮説である。

### A01-04g.3.3. TCEから見たGovernance Risk

WilliamsonのTCEではAsset Specificity / Uncertainty / Frequencyがtransaction governanceの重要属性として扱われる。[T6]

High CriticalityなAI / Analyticsを業務Processへ組み込む場合、VendorやSystemへの依存度が上がり、

- Switching Cost
- Contract adaptation
- Data / Model ownership
- Long-term maintenance
- Supplier continuity

等が問題になる可能性がある。

David & Han (2004)が示すようにTCEの実証支持は一様ではないため、「High CriticalityならSIerが勝つ」といった単純な結論には使わない。[T7] あくまでRisk / Dependencyを考える理論的レンズとする。

### A01-04g.3.4. SIer AnalyticsをStrong Candidateとする根拠

NTT DATAはAI Consultingだけでなく、Application Integration等を一連のServiceとして掲げる。[P4]

SIer型Providerは企業として、

- Security
- Enterprise Architecture
- System Delivery
- Operation
- Governance process

へアクセスできる場合が多い。

High Criticalityではこれらが顧客のRisk低減へ直結しやすいため、Strong Candidateと置く。

ただし、Analytical Complexityが非常に高い場合、分析専門人材が不足すれば総合Fitは下がり得る。

### A01-04g.3.5. Consulting AnalyticsをStrong Candidateとする根拠

Deloitte / Accenture等はAI / Dataに加え、Risk / Governance / Transformationを含むEnterprise-wide Serviceを提供する。[P2][P3]

High Criticalityで、

- Policy design
- Governance framework
- Executive / Risk Committee alignment
- Organization-wide controls

が重要なら、Consulting Analyticsは強いCandidateになる。

一方、案件の中心がHands-onなModel / Causal Designであれば、担当TeamのMethodological Capabilityを別途評価する必要がある。

### A01-04g.3.6. DS Specialistを条件付きとする理由

DS Specialistは高度Methodologyでは強いCandidateになり得る。[P1]

しかしHigh Criticalityでは、専門分析以外に、

- Enterprise Security
- Audit / Governance
- Operational responsibility
- Organizational acceptance

が必要になる。

これらを自社で持つか、Partnerと一体提供できるかによってFitが変わるため、Categoryとして固定評価しない。

### A01-04g.3.7. AI / Platform Vendorの位置づけ

PalantirのようなPlatformは、Data / Model / Application / Workflowを共通基盤で管理することで、OperationalizationやGovernanceを支援し得る。[P5]

製品としてSecurity / Audit / Governance Capabilityが十分整備され、顧客要件へFitする場合は強いCandidateになり得る。

一方、非定型MethodologyやVendor-neutralityが重要なら評価は変わる。

### A01-04g.3.8. 当チームのFit

当チームは、

- Predictive / Causalで問い・前提・評価を分ける
- CausalではEstimand / Assumption / Identification / Diagnostics等を必要に応じて扱う
- Predictiveではunknown-data performance / calibration / error pattern等を考慮する
- SIer内Analytics組織としてEnterprise Contextを持つ

という特徴がある。

High CriticalityかつAnalytical Complexityも高い場合、

> **Scientific / Methodological Validity × Enterprise Governance Context**

の両方が評価対象になりやすいため、当チームのPositionは上がる。

一方、High Governanceだが分析自体は標準的ならA01-04cに近づき、一般SIerとの差別化は弱くなる。

### A01-04g.3.9. 当チームのPosition

> **Competitive〜Core Candidate。Criticality単独ではなく、Analytical Complexityとの掛け合わせが重要。**

当チームが本当に優位かを確認するには、

- High Criticality案件実績
- Security / Governance連携実績
- Model / Causal validationの方法論
- Audit / Documentation / Traceability
- Incident / Operationを含むDelivery Model

のEvidenceが必要である。

### A01-04g.3.10. 反証条件

- 顧客が求めるGovernanceが企業全体のRisk Framework中心で、Consultingの方が高Fit
- 既存SIerがSystem / Security / Operationを既に担当し、Analyticsも十分なCapabilityを持つ
- Platform VendorがCompliance / Governance要件を製品で満たし、Custom Analysisの価値が小さい
- 当チームにHigh Criticality案件の実績・Governance Evidenceがない

### A01-04g.3.11. Evidence / Inferenceの区分

**Published Evidence**
- Organizational Buying / Industrial Buyer Behaviorでは複数Stakeholder、perceived risk等が購買に影響する。[T1][T2]
- TCEはdependency / governance riskを考える理論的レンズになるが、実証支持はmixed。[T6][T7]

**Provider一次情報**
- NTT DATA / Deloitte / Accenture / BrainPad / PalantirのOffering。[P1]〜[P5]

**当資料の分析仮説**
- High CriticalityではRisk / Evidence / Delivery / Org. AcceptabilityのWeightが上がる。
- Analytical Complexityも高い場合に当チームPositionが上がる。

## A01-04g.4. Speaker Note

重要度の高い案件では、分析精度だけではVendorを選べません。失敗したときの影響が大きいため、Security、Governance、責任分界、運用性、Evidenceまで含めた判断になります。

そのためSIerやConsultingは自然に強いCandidateです。当チームが差を作れる可能性があるのは、Governanceだけでなく分析そのものも難しい場合です。方法論上の妥当性とEnterprise側の制約を同時に扱えることが価値になります。

ただし、その優位を主張するにはHigh Criticality案件の実績やGovernance Evidenceが必要です。

## A01-04g.5. 次頁への接続

> ここまでのProfileを横断し、どこが当チームの重点候補で、どこでは他Providerの方が合理的かをSummaryする。

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