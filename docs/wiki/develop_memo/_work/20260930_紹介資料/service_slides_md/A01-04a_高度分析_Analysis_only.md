Document title: 高度分析 × Analysis-only の競争ポジション

# A01-04a. Appendix｜高度分析 × Analysis-only

## A01-04a.1. Message

**分析難易度が高く実装接続が弱い案件では、専門Analytics組織が有力になりやすい。**

## A01-04a.2. Chart

**チャートタイトル:** Deal Profile別Positioning｜高度分析 × Analysis-only

### A01-04a.2.1. Chart Structure

左にDeal Profile、中央にこのProfileで重くなりやすいCustomer Selection Criteria、右にProvider Positionを置く。

```text
Deal Profile
────────────────────
Analytical Complexity      High
Implementation Coupling    Low
Problem Novelty            Medium〜High
Solution Standardizability Low〜Medium
Criticality / Governance   Low〜Medium
          ↓
Customer Selection Criteria
────────────────────
Capability / Quality       ↑↑
Deal-specific Fit          ↑↑
Evidence / Credibility     ↑↑
Economic Value             ↑
Delivery / Integration     →
          ↓
Provider Position 仮説
────────────────────
DS Specialist             Strong candidate
Consulting Analytics      Competitive
当チーム                  Competitive
SIer Analytics            Competitive / 条件次第
AI / Platform Vendor      Product Fit依存
```

右下に小さく以下を付す。

> **この順位は市場実測ではなく、Deal Profile × Providerの事業特性から導くPositioning仮説。**

### A01-04a.2.2. Chart内の最小表示テキスト

- 高Analytical Complexity
- 低Implementation Coupling
- Capability / Fit / Evidence重視
- **DS Specialist：Strong candidate**
- **当チーム：Competitive**
- **Enterprise Baseは差になりにくい**

## A01-04a.3. Supporting Logic

### A01-04a.3.1. このProfileを独立類型として扱う理由

このProfileでは、顧客が購入しているものの中心が「Enterprise Systemそのもの」ではなく、**分析によって未知の問いへ答える専門サービス**になる。

典型例は以下である。

- 高度な需要予測・リスク推定の成立性検証
- 因果効果推定のFeasibility Study
- 新しい評価指標・Target Definitionの設計
- 既存データで何が識別・推定できるかの検討
- 特殊なData Generating Processを持つ分析

この場合、Implementation Couplingが低いため、System Integration、Security Architecture、24/365 Operation等は選定上の中心課題になりにくい。一方、Problem Novelty / Analytical Complexityが高いため、分析担当者の専門性、方法論、関連実績、顧客固有条件への適合性が相対的に重要になると考える。

ここでの「重要になる」は、当資料の恣意的な主張だけではない。Organizational Buying研究では、購買条件・購買関係者・期待が購買状況によって異なることが示されている。2023年のB2B Customer Journey研究も、purchase taskがroutine / low-priorityからstrategic / complexまで変化し、buying approachやBuying Centerの構成が状況依存で変わると整理している。[T1][T2][T3]

### A01-04a.3.2. なぜCapability / Fit / Evidenceの比重が上がるのか

Professional Serviceは購入前に完成品質を直接観測しにくい。

Pemer & Skjølsvik (2019)は51名のProfessional Service顧客へのInterviewをもとに、顧客がex anteでProvider Qualityを判断する際、Resource Quality / Delivery Quality / Relational Qualityと、それを示すSignalsを利用すると整理した。また、候補に残るための`qualifying signals`と、最終選択に寄与し得る`signals of excellence`を区別している。[T4]

Patterson (1995)の142組織を対象としたManagement Consultancy選定調査では、最終選択基準としてConsultancyのreputation、client industry experience、feesが上位だった。[T5]

したがって、高度なAnalysis-only案件で、

- 「高度分析ができます」というCapability自己申告

だけでは弱く、

- 関連する専門人材
- 類似する分析問題の実績
- 方法論的な説明力
- 顧客Data / Assumptionへの適合性
- 費用対価値

がSupplier Selectionに効く、という解釈には一定の根拠がある。

### A01-04a.3.3. DS SpecialistをStrong Candidateと置く根拠

これは「DS Specialistなら必ず強い」という普遍命題ではない。

代表例としてBrainPadは、公式サービス説明で「専門人材によるデータ分析」とProduct Serviceの両面を掲げており、Professional Serviceを主要なOfferingとしている。[P1]

このように、専門Analytics会社はBusiness Modelとして、

- Data Scientist / Analyst等の専門人材
- 個別分析Project
- Data活用Consulting

を中心資産として持つ場合がある。

この構造から、**Analytical Complexityが高く、Enterprise Integrationが主価値ではない案件では、専門人材の密度・関連実績・方法論のFitが直接競争力になりやすい**と推論する。

重要なのは、ここから「DS Specialistが当チームより常に優位」とは結論しないことである。実際の勝敗は、個別会社の人材、案件実績、価格、顧客業界経験等による。

### A01-04a.3.4. Consulting AnalyticsをCompetitiveと置く根拠

「ConsultingはStrategyだけ」という前提は事実に反する。

Deloitteは公式AI & Data Serviceで、AI Strategyだけでなく、bespoke AI-driven solutionのBuild、Data Engineering、Analytics、Intelligent Systemsまで扱うと説明している。[P2]

AccentureもData / AI Serviceで、AI / MLのBuild・ScaleやPredictive Workflowまで提供している。[P3]

したがって、高度なAnalysis-only案件でも、Consulting Analyticsが十分な専門人材を持つ場合は強い競合になり得る。

一方、このDealでStrategy Transformation / Organization Change / Enterprise-wide Program Managementが主な選定基準でない場合、それらのCapabilityが必ずしも追加Scoreにならない。このため本資料では`Strong`ではなく`Competitive`と置く。

これはProviderの能力不足ではなく、**今回のSelection WeightとのFit**の問題である。

### A01-04a.3.5. SIer Analyticsを「条件次第」と置く根拠

SIerも高度分析を提供し得る。例えばNTT DATAはAI Consultingにおいて、AI StrategyからUse Case prioritization、PoC、Model Training、Application IntegrationまでのRoadmapを掲げ、Data Science人材も明示している。[P4]

従って「SIerは分析が弱い」という一般化は行わない。

ただし、このProfileではImplementation Couplingが低いため、SIerが構造的に持ちやすい、

- System Integration
- Production Delivery
- Security / Governance
- Long-term Operation

等のCapabilityは、顧客の評価Weightが低い可能性がある。

そのため、SIer Analyticsの勝敗は、Enterprise Delivery力よりも**当該案件でのAnalytical Capability / Relevant Evidence**へ依存しやすいと考える。

### A01-04a.3.6. AI / Platform VendorをProduct Fit依存と置く根拠

AI / Platform Vendorの代表例としてPalantirは、Foundry / AIP上のOperational Application、Ontology、Application Building等を通じ、Data / Model / Workflow / ActionをPlatform上で統合する構造を提供している。[P5]

この種のProviderは、顧客問題がProduct Capabilityと高くFitする場合、既存Assetの再利用により強いValueを出し得る。

一方、Outcome定義、Treatment、Estimand、特殊なEvaluation、固有Data Structure等を案件ごとに設計する必要があり、かつPlatform導入価値が小さいAnalysis-only案件では、Product Assetの価値が相対的に下がる可能性がある。

ここも「AI Vendorは非定型分析ができない」という主張ではない。**Product Fitが選定Valueへどれだけ寄与するかがDeal依存**という整理である。

### A01-04a.3.7. 当チームのFit

当チームについて現時点で確認できているCapabilityは、以下である。

- Predictive / Causal PoCを提供する
- Data ScientistによるScratch開発を基本とする
- 必要に応じ成熟OSS / Libraryを利用する
- Predictive / Causalで問い・推論対象・Assumption・Evaluationを分ける
- 特定Product導入を必須前提としない

これらは本Profileと整合する。

特に、Problem Novelty / Analytical Complexityが高い案件では、

- Question Definition
- Predictive / Causalの選択
- Estimand / Assumption / Identification
- Unknown-data Performance / Calibration / Error Pattern

等を案件ごとに設計するCapabilityが価値になり得る。

一方、当チームのPositioning仮説のもう一方である`Enterprise Base`は、このProfileではSelection Weightが低い。

従って、

> **当チームは十分Fitするが、Capability Bundle全体が差別化として効くProfileではない。**

と評価する。

### A01-04a.3.8. 当チームのPosition

> **Competitive。ただし構造的なRelative Advantageは未確認。**

本Profileで「当チームが強い」と断定するには、少なくとも以下のEvidenceが必要である。

- Predictive / Causalの専門人材・Seniority
- 高難度案件の件数・具体例
- 関連Projectでの品質・顧客評価
- DS Specialist / Consulting Analyticsとの競合勝敗
- Price / Lead Time / Specialist Direct Access

これらが確認できない限り、DS Specialist等に対する`Competitive Gap > 0`は主張しない。

### A01-04a.3.9. 反証条件

以下が確認された場合、本スライドのPositioningは修正すべきである。

- RelevantなDS SpecialistがEnterprise条件を必要とせず、当チームより高い専門実績・専門人材を保有している
- Consulting Analyticsが同等以上のHands-on Analytical Capabilityをより高いEconomic Valueで提供できる
- 顧客が実際にはEnterprise Vendorとしての既存取引・契約容易性を強く重視しており、Implementation Couplingが低くてもSIer Baseが大きく効く
- Product Vendorの既存Capabilityへ問題が高くFitし、個別分析よりPlatform利用が合理的である

### A01-04a.3.10. Evidence / Inferenceの区分

**Published Evidence**

- B2B購買はBuying Situation・Buying Center・複数評価基準に依存する。[T1][T2][T3]
- Professional Serviceはex ante Qualityを直接評価しにくく、Quality SignalsがProvider選定に使われる。[T4]
- Management Consultancy選定ではreputation / client-industry experience / feesが重要だったという実証研究がある。[T5]

**Provider一次情報**

- BrainPad、Deloitte、Accenture、NTT DATA、Palantirが実際に掲げるOffering / Capability。[P1]〜[P5]

**当資料の分析仮説**

- `高Analytical Complexity × 低Implementation Coupling`ではCapability / Fit / EvidenceのWeightが相対的に高い。
- DS SpecialistをStrong Candidate、当チームをCompetitiveとする評価。
- 当チームのEnterprise BaseはこのProfileでは差別化寄与が小さい、という解釈。

上記の分析仮説は、学術研究が直接Provider類型の順位を実証したものではない。

## A01-04a.4. Speaker Note

このProfileでは、分析そのものが商品です。高度な因果推論や予測、特殊なデータ構造など、方法論と専門人材の質が価値の中心になります。

そのため、専門Analytics会社は自然に強い候補になります。これは「SIerやConsultingには高度分析ができない」という意味ではありません。実際、DeloitteやNTT DATA等も高度なAI / Data Serviceを明確に提供しています。

差が出るのは、今回の案件で何にWeightが付くかです。System Integrationがほぼ不要なら、Enterprise Delivery力を持っていても大きな加点にならず、分析専門性や関連実績が前面に出ます。

当チームはPredictive / CausalやScratch分析で十分競争できますが、このProfileでは`Specialist Analytics × Enterprise Base`のうちEnterprise Baseが効きにくいため、主戦場候補とは置きません。ここで当チームが勝つには、方法論、人材、実績、価格等で個別競合を上回るEvidenceが必要です。

## A01-04a.5. 次頁への接続

> 高度分析だけでなく、PoC後のData / System / Security / Operationまで同時に重要になると、選択基準は変わる。次頁では当チームのCapability Bundleがより全面的に効くProfileを見る。

## A01-04a.6. Sources

### Academic / Published

- [T1] Webster, F. E. Jr. & Wind, Y. (1972), “A General Model for Understanding Organizational Buying Behavior,” *Journal of Marketing*, 36(2), 12–19. DOI: https://doi.org/10.1177/002224297203600204
- [T2] Sheth, J. N. (1973), “A Model of Industrial Buyer Behavior,” *Journal of Marketing*, 37(4), 50–56. DOI: https://doi.org/10.1177/002224297303700408
- [T3] “B2B customer journeys: Conceptualization and an integrative framework,” *Industrial Marketing Management*, 113 (2023), 74–87. DOI: https://doi.org/10.1016/j.indmarman.2023.05.020
- [T4] Pemer, F. & Skjølsvik, T. (2019), “The cues that matter: Screening for quality signals in the ex ante phase of buying professional services,” *Journal of Business Research*, 98, 352–365. DOI: https://doi.org/10.1016/j.jbusres.2019.02.005
- [T5] Patterson, P. G. (1995), “Choice Criteria in Final Selection of a Management Consultancy Service,” *Journal of Professional Services Marketing*, 11(2), 177–187. DOI: https://doi.org/10.1300/J090v11n02_13

### Provider primary sources

- [P1] BrainPad, Services: https://www.brainpad.co.jp/services/
- [P2] Deloitte, AI & Data: https://www.deloitte.com/us/en/services/consulting/services/artificial-intelligence-and-data.html
- [P3] Accenture, Data Services / AI and Data: https://www.accenture.com/us-en/services/data-ai/cloud-data-ai
- [P4] NTT DATA, AI Consulting: https://www.nttdata.com/global/en/services/ai/ai-consulting
- [P5] Palantir, Operational Applications / App Building: https://www.palantir.com/docs/foundry/app-building/operational-apps