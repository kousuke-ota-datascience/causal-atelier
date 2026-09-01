Document title: 高度分析 × Enterprise接続 の競争ポジション

# A01-04b. Appendix｜高度分析 × Enterprise接続

## A01-04b.1. Message

**高度分析とEnterprise接続が同時に重要な案件は、当チームの重点Positioning候補である。**

## A01-04b.2. Chart

**チャートタイトル:** Deal Profile別Positioning｜高度分析 × Enterprise接続

### A01-04b.2.1. Chart Structure

```text
Deal Profile
────────────────────
Analytical Complexity      High
Implementation Coupling    High
Problem Novelty            Medium〜High
Solution Standardizability Low〜Medium
Criticality / Governance   Medium〜High
          ↓
Customer Selection Criteria
────────────────────
Capability / Quality       ↑↑
Deal-specific Fit          ↑↑
Delivery Feasibility       ↑↑
Risk                       ↑↑
Evidence / Credibility     ↑↑
Org. Acceptability         ↑
          ↓
Provider Position 仮説
────────────────────
当チーム                  Core Candidate
SIer Analytics             Strong Candidate
Consulting Analytics       Strong Candidate
DS Specialist              Competitive
AI / Platform Vendor       Product Fit依存
```

注記：`Core Candidate`は「相対優位が実証済み」の意味ではなく、**当チームのCapability Bundle全体が価値化しやすく、Competitive Gapを優先検証すべき領域**を意味する。

### A01-04b.2.2. Chart内の最小表示テキスト

- 高Analytical Complexity
- 高Implementation Coupling
- Capability / Delivery / Riskを同時評価
- **当チーム：Core Candidate**
- **SIer / Consulting：Strong Candidate**
- **空白地帯ではない**

## A01-04b.3. Supporting Logic

### A01-04b.3.1. このProfileを重要視する理由

このProfileでは、分析PoCに二つの異なる要求が同時に存在する。

1. **分析そのものが難しい**
   - Prediction / Causalの選択
   - Estimand / Assumption / Identification
   - 未知データ性能 / Calibration / Error Pattern
   - 顧客固有Data Structureへの対応
2. **分析だけで完結しない**
   - Data acquisition / Data pipeline
   - Enterprise SystemとのIntegration
   - Security / Access control
   - Operation / Monitoring
   - Governance / Accountability

この二つが同時に重い場合、単一Capabilityでなく、**Analytical CapabilityとDelivery / Governance Capabilityの組合せ**が評価対象になる。

Webster & Wind、ShethのOrganizational Buying研究は、B2B購買が複数Stakeholder・複数Expectationで構成されることを示している。[T1][T2] 2023年のB2B Customer Journey研究も、purchase complexityが高まるほどBuying Centerや購買プロセスが複雑化し得ることを整理している。[T3]

したがってこのProfileでは、Business / Data-AIだけでなく、IT / Security / Procurement / Operation等がBuying Centerへ入り、CapabilityだけでなくDelivery / Risk / Organizational AcceptabilityのWeightも高まりやすい、という仮説を置く。

### A01-04b.3.2. Risk / Governanceが選定軸として強くなる根拠

Transaction Cost Economicsでは、WilliamsonがAsset Specificity / Uncertainty / Frequencyをtransaction governanceを考える主要属性として扱う。[T6]

分析PoCをEnterprise利用へ接続する場合、顧客は単発分析だけでなく、

- 特定Vendor / Platformへの依存
- System Integration後のSwitching Cost
- Security / Compliance上の責任
- 運用変更へのAdaptation
- 後続Phaseへの引継ぎ

を考える必要が生じる。

TCEはVendor Selectionの全てを決める法則ではないが、Implementation Couplingが上がるほど「分析精度以外の取引・依存リスク」が選定に入る理論的レンズになる。[T6][T7]

### A01-04b.3.3. SIer AnalyticsがStrong Candidateとなる根拠

大手SIerは、AI / AnalyticsだけでなくEnterprise Systemとの接続をOfferingとして明示している。

NTT DATAのAI Consultingは、Strategy / Use Case prioritization / PoC / Model TrainingからApplication Integrationまでを一連のServiceとして掲げる。[P4]

この事業構造では、

- Enterprise Architecture
- Security
- Integration
- Production Delivery
- Operation

がCapability Portfolioの中核に含まれやすい。

したがってImplementation Couplingが高い本Profileでは、SIer Analyticsは構造的に有力なCandidateになる。

ただし、Analytical Complexityが高い場合の勝敗は別問題である。Predictive / Causalの専門人材、非定型問題への方法論、Relevant Evidenceが弱ければ、Enterprise Deliveryが強くても総合評価で勝つとは限らない。

### A01-04b.3.4. Consulting AnalyticsがStrong Candidateとなる根拠

DeloitteはAI & Data Serviceで、Strategy / Data Modernizationだけでなく、bespoke AI solution、Data Engineering、Analytics、Intelligent Systemsまで扱う。[P2]

AccentureもData & AIにおいて、AI / MLのBuild・Scale、Cloud Data Foundation、Predictive Workflow等を統合的に提供する。[P3]

従って、Consulting Analyticsも「高度分析とEnterprise接続を両方できる」ため、本Profileの強い競合である。

特に、

- Decision Altitudeが高い
- Transformation Programが大きい
- Stakeholder Alignmentが重要
- Operating Model / Organization Changeを含む

場合にはConsulting側の追加Capabilityが強く効く可能性がある。

一方、具体的なAnalytical PoCを小さくHands-onで回すこと、Specialistが直接分析設計へ深く入ること、価格 / Lead Time等については個社・案件差が大きいため、一般化しない。

### A01-04b.3.5. DS SpecialistをCompetitiveと置く根拠

DS SpecialistはAnalytical Complexityが高い部分では強いCandidateである。[P1]

ただしImplementation Couplingが高まると、顧客の評価対象に、

- Security Review
- Data Access
- Enterprise Architecture
- System Integration
- Production Monitoring
- Governance

が加わる。

専門会社でもこれらを提供できる場合はあるが、Enterprise Deliveryをどこまで自社で持つか、Partnerへ依存するかでDelivery Feasibility / Riskの評価が変わる。

従って本資料では、「DS SpecialistはEnterpriseに弱い」と断定せず、**Analytical側では強いが、Enterprise条件を含めた総合Fitは個社差が大きい**として`Competitive`と置く。

### A01-04b.3.6. AI / Platform VendorをProduct Fit依存と置く根拠

PalantirのようなPlatform Vendorは、Data / Model / Ontology / Workflow / Operational Applicationを一体化し、Enterprise運用へ接続するAssetを持つ。[P5]

したがって、ProblemがPlatformの標準CapabilityへFitする場合、本Profileでも非常に強いCandidateになり得る。

一方、分析Question / Estimand / Evaluation / Data Structureが強く案件固有で、Platform導入そのものがValue Driverでない場合、標準Assetの優位が相対的に下がる可能性がある。

よって評価は`Product Fit依存`とする。

### A01-04b.3.7. 当チームのFit

当チームは、確認済みの範囲で、

- Predictive / Causal PoC
- Scratch + mature OSS
- Question / Assumption / Evaluationの分離
- 特定Product非必須
- SIer内のAnalytics組織

というCapability構成を持つ。

このProfileでは、`Specialist Analytics × Enterprise Base`の両側が同時にSelection Criteriaへ接続する。

具体的には、

| 当チームCapability | このProfileで効く選定軸 |
|---|---|
| Predictive / Causalを問いから使い分け | Deal-specific Fit / Capability |
| Scratch / OSS | Non-standard problemへのFit |
| Assumption / Evaluation設計 | Capability / Evidence |
| SIer context | Delivery / Risk / Org. Acceptability |
| Product非固定 | Dependency / Lock-in低減の可能性 |

このため、**当チームのCapability Bundleが最も全面的に価値化しやすいProfileの一つ**と評価する。

### A01-04b.3.8. それでも「相対優位」とは言えない理由

本Profileは競合の空白地帯ではない。

- 他SIer Analyticsも高度分析＋Enterprise Deliveryを持ち得る
- Consulting Analyticsも高度分析＋Transformation＋Engineeringを持ち得る
- DS SpecialistもEnterprise Capabilityを強化している場合がある
- Platform Vendorも高度なCustom Developmentを提供し得る

したがって、当チームのOwn Fitが高いことは確認できても、Relevant Competitorとの`Competitive Gap > 0`は未証明である。

### A01-04b.3.9. Competitive Gapを検証すべき項目

本ProfileでWhy Usを「競争優位」へ昇格させるには、以下を同一Deal条件で比較する必要がある。

**Analytical Side**
- Predictive / Causal専門人材の質・数
- 高難度案件実績
- Question / Assumption / Evaluation設計の深さ
- Specialist Direct Access

**Enterprise Side**
- Security / Data / System部門との連携
- 本番化・引継ぎ実績
- Delivery Governance

**Economics / Operating Model**
- PoC価格
- Lead Time
- Team Size
- Contract Flexibility
- Product / License依存

**Evidence**
- 顧客選定理由
- Competitive Win / Loss
- Repeat
- Production handoff事例

### A01-04b.3.10. 反証条件

以下が確認された場合、「当チームのCore Candidate」という評価を下げる。

- 他SIer Analyticsが同等以上のPredictive / Causal専門性を持ち、Delivery / Priceでも優位
- Consulting Analyticsが同等以上のHands-on分析を、より高いBusiness Fit / Governance力とともに提供
- DS SpecialistがEnterprise Integrationまで一貫して持ち、当チームより高いRelevant Evidenceを保有
- AI Platformが顧客課題へ高くFitし、Custom PoCより短期・低コストで業務利用まで到達

### A01-04b.3.11. Evidence / Inferenceの区分

**Published Evidence**
- B2B購買は複数Stakeholder / 複数基準で行われる。[T1][T2]
- Buying Process / Buying Centerはpurchase complexityやsituationで変化する。[T3]
- Professional ServiceではQuality Signal / Evidenceが重要。[T4][T5]
- Integration / dependencyが大きい取引ではTCEのAsset Specificity / Uncertaintyが有用な分析レンズになる。[T6][T7]

**Provider一次情報**
- Deloitte / Accenture / NTT DATA / BrainPad / Palantirが公式に示すCapability範囲。[P1]〜[P5]

**当資料の分析仮説**
- 高Analytical Complexity × 高Implementation CouplingではCapabilityとDelivery/Riskの両方のWeightが高い。
- 当チームをCore Candidate、SIer / ConsultingをStrong Candidateとする評価。
- 当チームのCapability BundleがこのProfileで全面的に価値化しやすいという解釈。

## A01-04b.4. Speaker Note

このProfileは、当チームが最も訴求しやすい候補の一つです。理由は、高度分析だけでなく、その分析をEnterprise環境へどうつなぐかまで同時に問われるからです。

ただし、ここは空白地帯ではありません。NTT DATAのようなSIerも、DeloitteやAccentureのようなConsulting Analyticsも、分析から実装まで広いCapabilityを公式に持っています。

したがって「当チームだけができる」とは言いません。言えるのは、Predictive / Causalの非定型分析とSIerのEnterprise Contextを同じPoCに持ち込めるため、このProfileでは当チームのCapability Bundle全体が評価対象になりやすい、ということです。

本当に競合より優位かは、人材、実績、価格、Lead Time、顧客が実際に選んだ理由まで比較して初めて言えます。ここはWhy Usの最有力仮説であると同時に、最優先でEvidenceを集めるべき領域です。

## A01-04b.5. 次頁への接続

> 分析難易度が下がり、Enterprise接続そのものが主要課題になると、同じSIer Baseを持つ競合との差がより出にくくなる。

## A01-04b.6. Sources

### Academic / Published
- [T1] Webster, F. E. Jr. & Wind, Y. (1972), “A General Model for Understanding Organizational Buying Behavior,” *Journal of Marketing*, 36(2), 12–19. https://doi.org/10.1177/002224297203600204
- [T2] Sheth, J. N. (1973), “A Model of Industrial Buyer Behavior,” *Journal of Marketing*, 37(4), 50–56. https://doi.org/10.1177/002224297303700408
- [T3] “B2B customer journeys: Conceptualization and an integrative framework,” *Industrial Marketing Management*, 113 (2023), 74–87. https://doi.org/10.1016/j.indmarman.2023.05.020
- [T4] Pemer, F. & Skjølsvik, T. (2019), *Journal of Business Research*, 98, 352–365. https://doi.org/10.1016/j.jbusres.2019.02.005
- [T5] Patterson, P. G. (1995), *Journal of Professional Services Marketing*, 11(2), 177–187. https://doi.org/10.1300/J090v11n02_13
- [T6] Williamson, O. E. (2008), “Transaction Cost Economics: The Natural Progression,” *American Economic Review*, 100(3), 673–690. https://doi.org/10.1257/aer.100.3.673
- [T7] David, R. J. & Han, S.-K. (2004), “A Systematic Assessment of the Empirical Support for Transaction Cost Economics,” *Strategic Management Journal*, 25(1), 39–58. https://doi.org/10.1002/smj.359

### Provider primary sources
- [P1] BrainPad, Services: https://www.brainpad.co.jp/services/
- [P2] Deloitte, AI & Data: https://www.deloitte.com/us/en/services/consulting/services/artificial-intelligence-and-data.html
- [P3] Accenture, Data & AI: https://www.accenture.com/us-en/services/data-ai/cloud-data-ai
- [P4] NTT DATA, AI Consulting: https://www.nttdata.com/global/en/services/ai/ai-consulting
- [P5] Palantir, Operational Applications: https://www.palantir.com/docs/foundry/app-building/operational-apps