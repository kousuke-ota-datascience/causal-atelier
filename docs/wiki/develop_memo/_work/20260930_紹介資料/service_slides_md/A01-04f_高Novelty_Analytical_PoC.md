Document title: 高Novelty × Analytical PoC の競争ポジション

# A01-04f. Appendix｜高Novelty × Analytical PoC

## A01-04f.1. Message

**高Novelty PoCでは分析設計力が効き、Enterprise接続が加わるほど当チームのPositionが上がる。**

## A01-04f.2. Chart

**チャートタイトル:** Deal Profile別Positioning｜高Novelty × Analytical PoC

### A01-04f.2.1. Chart Structure

```text
① Deal Profile｜6軸
────────────────────────
Decision Altitude          Operational〜Business
Problem Novelty            High
Analytical Complexity      High
Solution Standardizability Low
Implementation Coupling    Low〜Medium
Criticality / Governance   Medium
              ↓
② Customer Selection Criteria｜Weight仮説
────────────────────────
Deal-specific Fit          H
Capability / Quality       H
Delivery Feasibility       M
Economic Value             M
Risk                       M〜H
Evidence / Credibility     H
Relational / Governance    H
Organizational Acceptability M
              ↓
③ Provider Competition｜Position仮説
────────────────────────
DS Specialist              Strong Candidate
Consulting Analytics       Strong Candidate
当チーム                   Competitive〜Conditional Core
SIer Analytics             組織次第
AI / Platform Vendor       Relative Weak候補
              ↓
④ Our Position
────────────────────────
**Competitive〜Conditional Core**
Implementation Coupling = Low
  → Analytical Capability中心でCompetitive
Implementation Coupling = Medium
  → Enterprise Contextも効き、Core Candidateへ近づく
```

### A01-04f.2.2. Chart内の最小表示テキスト

- 6軸Profileを全表示
- Fit / Capability / Evidence / Relational：High Weight
- **当チーム：Competitive〜Conditional Core**
- **Enterprise接続が増すほどPosition上昇**
- **DS Specialist / Consulting：Strong Candidate**

## A01-04f.3. Supporting Logic

### A01-04f.3.1. なぜこの6軸Profileなのか

この類型では、既知手法を適用する以前に、Outcome、PredictionかCausalか、Estimand、Assumption、Identification、Success Criteria、Data Sufficiency等を設計する必要がある。

Decision AltitudeはOperational〜Business。全社Strategyではなく具体的なDecision Problemを扱う。Problem Novelty / Analytical ComplexityはHigh、StandardizabilityはLow。Implementation CouplingはLow〜Mediumで、まずAnswerabilityを検証しつつ、案件によっては業務・Enterprise利用条件まで考慮する。CriticalityはMediumとする。

### A01-04f.3.2. なぜこのSelection Weightになるのか

BUYGRIDのNew Taskは購買側の新規性・情報要求が高い状況を示すAnchorであり、B2B Customer Journey研究もpurchase complexity / uncertaintyによるBuying Processの変化を整理している。[T8][T3]

高Novelty案件では一般的なAI Capabilityより、類似問題へのFit、専門人材、未知の条件を説明できる能力、共同でProblem Definitionを詰める関係性が重要になると考え、Fit / Capability / Evidence / RelationalをHighと置く。[T4][T5]

一方、Implementation CouplingがLow側ではDelivery / Organizational AcceptabilityのWeightはA01-04bほど高くならない。従って、本Profile単独では`Specialist Analytics × Enterprise Base`のCapability Bundle全体が常に価値化するとは置かない。

### A01-04f.3.3. Consulting AnalyticsのPosition

Deloitte / AccentureはProblem FramingからAI / Data Engineering / Buildまでを提供する。[P2][P3]

Business Problem自体が曖昧な場合はConsulting AnalyticsがStrong Candidateとなる。ただしHands-on Methodological Detailが中心なら担当Teamの専門性が勝敗を左右す。

### A01-04f.3.4. SIer AnalyticsのPosition

NTT DATA等のようにAI Consulting / Data Science / PoCまで持つSIerは有力になり得る。[P4]

ただしSIerというCategoryだけでは非定型Methodological Capabilityの強弱を決められないため「組織次第」とする。

### A01-04f.3.5. DS SpecialistのPosition

専門Analytics会社はSpecialist Talent / Flexible Analysisを中核Offeringとする場合があり、高Novelty / High Complexityで直接価値化しやすい。[P1]

従ってStrong Candidateとする。ただしEnterprise接続力や業界実績は個社差がある。

### A01-04f.3.6. AI / Platform VendorのPosition

Problem Noveltyが高い段階ではProduct CapabilityとのFit自体が未確立の場合がある。[P5]

Platform Fitが早期に確認できれば評価は上がるが、探索的Custom Analysisが中心なら標準Assetの価値が小さくなるためRelative Weak候補とする。

### A01-04f.3.7. 当チームのPosition

当チームのPredictive / Causalの使い分け、Causal Question / Estimand / Assumption / Identification、Scratch / OSS、特定Product非必須という特徴は本ProfileのAnalytical Design側と直接整合する。

ただし、`Specialist Analytics × Enterprise Base`というCapability Bundle全体が価値化するかはImplementation Couplingによって変わる。

```text
Implementation Coupling = Low
────────────────────────
問い / Answerability / Methodologyが中心
→ 当チームはCompetitive
→ DS Specialistとの競争が強い
→ Enterprise Baseは選定理由になりにくい

Implementation Coupling = Medium
────────────────────────
分析結果の業務利用、Data / System / Security等も考慮
→ Enterprise ContextのWeightが上がる
→ 当チームのCapability Bundleがより広く価値化
→ Core Candidateへ近づく
```

従って、本Profile全体を一律にCore Candidateとはせず、

> **Competitive〜Conditional Core。Implementation CouplingがMedium側へ上がるほど重点Positioningに近づく。**

とする。

### A01-04f.3.8. A01-04a / A01-04bとの連続性

A01-04fは独立した箱ではなく、Implementation Couplingの値によって隣接Profileへ連続する。

- Implementation CouplingがLowへ下がるほど、A01-04a「高度分析 × Analysis-only」に近づく。
- Implementation CouplingがMedium〜Highへ上がり、Criticalityも高まるほど、A01-04b「高度分析 × Enterprise接続」に近づく。

従って、High Noveltyそのものを当チームのWhy Usとはしない。

> **High Novelty / High Analytical Complexityに、Enterprise利用条件が加わるとき、01-05の3つのValue Propositionが同時に効きやすくなる。**

というのがA01-04全体との整合した解釈である。

### A01-04f.3.9. Relative Advantageの有無

DS Specialist / Consulting AnalyticsもStrong Candidateであるため相対優位は未証明。Causal / Predictive専門人材、新規テーマPoC実績、Answerability判断、Price / Lead Time、Enterprise接続までの継続Delivery等のEvidenceが必要である。

### A01-04f.3.10. 反証条件

- DS SpecialistがRelevant Evidence / Specialist Talentで明確に上回る
- Consulting AnalyticsがProblem FramingとHands-on Analysisをより高Valueで提供
- 顧客課題が既製Platformへ早期にFitする
- 当チームに高Novelty案件の実績Evidenceがない
- Implementation Couplingが低く、顧客がEnterprise Contextをほぼ評価しない

### A01-04f.3.11. Evidence / Inference区分

**Published Evidence:** BUYGRID / B2B Journey、Professional Service Signals。[T3][T4][T5][T8]

**Provider一次情報:** BrainPad / Deloitte / Accenture / NTT DATA / Palantir。[P1]〜[P5]

**当資料の分析仮説:** 本6軸Profile、8軸Weight、当チーム＝Competitive〜Conditional Core、DS Specialist / Consulting＝Strong CandidateというPositioning、およびImplementation Coupling上昇に伴う当チームPosition上昇。

## A01-04f.4. Speaker Note

新しいテーマのPoCでは、モデルを作る以前に「何を検証すれば意思決定できるか」を決める必要があります。当チームのPredictive / Causalの使い分けやEstimand / Assumption設計と相性がよい領域です。

ただし、分析単体に近い場合はDS Specialistも非常に自然な選択肢であり、当チームのEnterprise Baseは大きな差になりません。分析結果を業務・Systemで使う条件までPoCで考える必要が出てくるほど、当チームのもう一方のCapabilityが加わり、重点Positioningに近づきます。

したがってHigh Noveltyだから当チームがCoreなのではなく、**High Novelty / High Analytical ComplexityとEnterprise利用条件が重なること**が重要です。

## A01-04f.5. A01-04への示唆

> A01-04fは重点Positioningを支えるConditional Anchorである。Implementation CouplingがLowならA01-04a寄り、Medium以上ならA01-04b寄りとなり、後者で01-05の3つのValue Propositionが同時に価値化しやすい。

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