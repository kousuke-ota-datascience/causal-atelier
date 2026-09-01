Document title: 高Novelty × Analytical PoC の競争ポジション

# A01-04f. Appendix｜高Novelty × Analytical PoC

## A01-04f.1. Message

**新規性が高いPoCでは、方法論だけでなく「何を検証できるか」の設計力が重要になる。**

## A01-04f.2. Chart

**チャートタイトル:** Deal Profile別Positioning｜高Novelty × Analytical PoC

### A01-04f.2.1. Chart Structure

```text
Deal Profile
────────────────────
Problem Novelty            High
Analytical Complexity      High
Implementation Coupling    Low〜Medium
Solution Standardizability Low
Criticality / Governance   Medium
Decision Altitude          Operational〜Business
          ↓
Customer Selection Criteria
────────────────────
Deal-specific Fit          ↑↑
Capability / Quality       ↑↑
Evidence / Credibility     ↑↑
Relational / Governance    ↑
Economic Value             ↑
          ↓
Provider Position 仮説
────────────────────
DS Specialist              Strong Candidate
当チーム                  Core Candidate
Consulting Analytics       Strong Candidate
SIer Analytics             組織次第
AI / Platform Vendor       Relative Weak候補
```

### A01-04f.2.2. Chart内の最小表示テキスト

- High Problem Novelty
- High Analytical Complexity
- Fit / Capability / Evidence重視
- **当チーム：Core Candidate**
- **DS Specialist / Consulting：Strong Candidate**

## A01-04f.3. Supporting Logic

### A01-04f.3.1. このProfileの特徴

このProfileでは「既知の手法を適用できるか」より前に、

- 何をOutcomeとするか
- PredictionかCausalか
- 何をEstimandとするか
- どのAssumptionが必要か
- 今のDataでIdentification可能か
- 何をSuccess Criteriaとするか
- 何が分からなければ次に何を集めるか

を設計する必要がある。

つまりPoCの主要成果はModelそのものだけでなく、**問いのAnswerabilityと検証設計を明らかにすること**になる。

BUYGRIDのNew Taskは、購買側の新規性・情報要求が高い状況を示す代表的Anchorである。[T8] 2023年のB2B Customer Journey研究でも、purchase taskの複雑性・不確実性によりBuying Processが変化すると整理される。[T3]

このため、高Novelty案件では既製Solutionの比較だけでなく、Providerと顧客がProblem Definition自体を共同で詰める必要性が高まる、というのが本資料の仮説である。

### A01-04f.3.2. Deal-specific Fitが強く効く理由

PattersonのManagement Consultancy選定研究ではclient-industry experienceが上位基準であり、Pemer & SkjølsvikもProfessional Service購入時にResource Quality等のSignalsが使われることを示す。[T4][T5]

新規性が高い案件では、一般的な「AI Capability」より、

- 類似する問題を扱った経験
- 該当方法論のSpecialist
- 不確実性を説明できる能力
- 無理にAnswerを出さず、Answerabilityを判断できる能力

がProvider Fitとして評価される可能性が高い。

### A01-04f.3.3. DS SpecialistをStrong Candidateとする根拠

BrainPadのようなAnalytics専門会社は、専門人材によるData Analysis / Consultingを中核Offeringとしている。[P1]

Problem Novelty / Analytical Complexityが高いほど、Specialist Talent / Methodological Depth / Flexible Analysisが直接価値化しやすい。このためStrong Candidateとする。

ただし、個別DS SpecialistのCausal Capability、業界実績、Enterprise Deliveryは各社で異なるため、一律の優位を意味しない。

### A01-04f.3.4. Consulting AnalyticsをStrong Candidateとする根拠

Deloitte / AccentureはAI / Data Strategyだけでなく、Analytics / Engineering / Buildまでを公式Offeringとして持つ。[P2][P3]

高Novelty案件ではProblem Framing、Stakeholder Alignment、Business Value Definitionも不確実であるため、Business / Strategy側から問いを構造化できるConsulting Analyticsは有力になり得る。

一方、PoCが非常にHands-onで、Methodological Detailが中心なら、担当Teamの専門性・Delivery Modelが勝敗を左右する。

### A01-04f.3.5. SIer Analyticsを「組織次第」とする理由

NTT DATAのようにAI Consulting / Data Science / PoCまで公式に持つSIerは十分有力である。[P4]

しかしSIerというCategory自体から、非定型Methodological Capabilityの強弱は決められない。組織ごとの専門人材・案件実績を見る必要がある。

従ってCategoryとして固定Scoreを付けず「組織次第」とする。

### A01-04f.3.6. AI / Platform VendorのFitが下がり得る理由

Problem Noveltyが高い場合、そもそもProduct CapabilityとのFitが確立していない。

PalantirのようなPlatformは高度なCustom Application構築も可能だが、Platformを採用する価値がまだ明確でない探索的PoCでは、Product Assetの再利用メリットが小さい可能性がある。[P5]

従ってRelative Weak候補とするが、Platform Fitが早期に確認できれば評価は上がる。

### A01-04f.3.7. 当チームのFit

当チームの確認済み特徴である、

- Predictive / Causalを問いから区別する
- Causal Question / Estimand / Assumption / Identification等を分ける
- Scratch / OSSで個別設計する
- 特定Productを必須としない

は、高Novelty Profileと直接整合する。

さらにImplementation CouplingがMediumへ近づけば、SIer内組織としてEnterprise Contextも追加価値になり得る。

従って、

> **Core Candidate。ただし主にAnalytical Design側のFitによる。**

と評価する。

### A01-04f.3.8. A01-04aとの違い

A01-04aは「高度分析だが問題自体はある程度定義済み」の案件も含む。

本ProfileはさらにProblem Noveltyが高く、Question / Answerability / Data Sufficiencyそのものを設計する必要がある。

そのため当チームが重視する「問いから分析を選ぶ」Operating Modelは、A01-04aより強く価値化する可能性がある。

### A01-04f.3.9. Competitive Gapは未証明

このProfileは当チームにFitするが、DS Specialist / Consulting Analyticsも強い。

相対優位を主張するには、

- Causal / Predictive専門人材
- 新規テーマPoC実績
- No-Goを含むAnswerability判断実績
- Specialist Direct Access
- PoC価格 / Lead Time
- Enterprise接続まで必要になった際の継続Delivery

のEvidenceが必要である。

### A01-04f.3.10. 反証条件

- DS Specialistが当チームより強いRelevant Evidence / Specialist Talentを持つ
- Consulting AnalyticsがProblem FramingとHands-on Analysisを一体でより高いValueで提供
- 顧客課題が早期に既製PlatformへFitし、探索的Custom Analysisが不要
- 当チームに高Novelty案件の実績・人材Evidenceがない

### A01-04f.3.11. Evidence / Inferenceの区分

**Published Evidence**
- BUYGRID / B2B Journeyは新規性・複雑性によるBuying Process変化を支持する。[T3][T8]
- Professional ServiceではExperience / Resource Quality / Signalsが選択に使われる。[T4][T5]

**Provider一次情報**
- BrainPad / Deloitte / Accenture / NTT DATA / Palantirの公式Offering。[P1]〜[P5]

**当資料の分析仮説**
- 高Novelty × 高Analytical ComplexityではQuestion Design / Answerabilityが競争軸になる。
- 当チームをCore Candidateとする評価。

## A01-04f.4. Speaker Note

新しいテーマのPoCでは、モデルを作る以前に「何を検証すれば意思決定できるのか」を決める必要があります。ここは当チームのPredictive / Causalの使い分け、EstimandやAssumptionの設計と相性がよい領域です。

ただしDS SpecialistやConsulting Analyticsも強い領域です。したがって、当チームの主戦場候補とは言えても、競合より上とはまだ言えません。ここで勝つには、方法論人材、類似案件、顧客評価といったEvidenceが必要です。

## A01-04f.5. 次頁への接続

> Problem Noveltyだけでなく、失敗時の影響や規制・運用責任まで重くなると、Capability以外にRisk / Governanceが強い選定軸となる。

## A01-04f.6. Sources

- [T8] Robinson, Faris & Wind (1967), *Industrial Buying and Creative Marketing*.
- [T3] “B2B customer journeys: Conceptualization and an integrative framework,” *Industrial Marketing Management*, 113 (2023), 74–87. https://doi.org/10.1016/j.indmarman.2023.05.020
- [T4] Pemer & Skjølsvik (2019): https://doi.org/10.1016/j.jbusres.2019.02.005
- [T5] Patterson (1995): https://doi.org/10.1300/J090v11n02_13
- [P1] BrainPad: https://www.brainpad.co.jp/services/
- [P2] Deloitte AI & Data: https://www.deloitte.com/us/en/services/consulting/services/artificial-intelligence-and-data.html
- [P3] Accenture Data & AI: https://www.accenture.com/us-en/services/data-ai/cloud-data-ai
- [P4] NTT DATA AI Consulting: https://www.nttdata.com/global/en/services/ai/ai-consulting
- [P5] Palantir: https://www.palantir.com/docs/foundry/app-building/operational-apps