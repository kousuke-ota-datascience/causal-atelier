Document title: 高Novelty × Analytical PoC の競争ポジション

# A01-04f. Appendix｜高Novelty × Analytical PoC

## A01-04f.1. Message

**新規性が高いPoCでは、方法論だけでなく「何を検証できるか」の設計力が重要になる。**

## A01-04f.2. Chart

**チャートタイトル:** Deal Profile別Positioning｜高Novelty × Analytical PoC

### A01-04f.2.1. Chart Structure

```text
Deal Profile
────────────
Problem Novelty         High
Analytical Complexity   High
Implementation Coupling Low〜Medium
Standardizability       Low
Criticality             Medium
Decision Altitude       Operational〜Business
        ↓
重視されるSelection Criteria
────────────
Deal-specific Fit
Capability / Quality
Evidence / Credibility
Relational / Governance Fit
Economic Value
        ↓
Provider Position
────────────
DS Specialist          有力競合
当チーム               重点Positioning候補
Consulting Analytics   有力競合
SIer Analytics          組織次第
AI / Platform Vendor    Relative Weak候補
```

### A01-04f.2.2. Chart内の最小表示テキスト

- High Problem Novelty
- High Analytical Complexity
- **当チーム：Core Candidate**
- DS Specialist / Consultingも有力

## A01-04f.3. Supporting Logic

### A01-04f.3.1. このProfileの特徴

前例が少なく、既存データで何が答えられるかも含めてPoCの設計自体に不確実性がある案件。単なるModel Selectionより、Question / Estimand / Assumptions / Evaluation / Data sufficiency等の設計が重要になる。

### A01-04f.3.2. ProviderごとのFit仮説

- **DS Specialist**：高度なMethodological CapabilityやSpecialist Talentが直接価値になる。
- **当チーム**：Predictive / Causalを問いから使い分け、Scratch / OSSで非定型に設計できる点がFitする。Implementation CouplingがMedium以上ならEnterprise Contextも追加価値になり得る。
- **Consulting Analytics**：Business Problem framingやStakeholder Alignmentまで含める場合に有力。Hands-onな分析Deliveryの深さは個社差がある。
- **SIer Analytics**：高度分析専門組織を持つ場合は有力。一般的なIntegration中心組織では差が出る可能性がある。
- **AI / Platform Vendor**：ProblemがProduct Capabilityへ未確立の場合、標準化されたSolutionの適合度が下がりやすい。

### A01-04f.3.3. 当チームのPosition

> **重点Positioning候補。ただしDS Specialist / ConsultingとのCompetitive Gapは未証明。**

このProfileでは、当チームのAnalytical Design Capabilityが強く価値化しやすい。一方、Enterprise Baseが効く度合いはImplementation Coupling次第であり、Analysis-onlyに近いほどDS Specialistとの差が縮む。

## A01-04f.4. Speaker Note

新しいテーマのPoCでは、モデルを作れるかより、そもそも何を検証すべきか、今のデータで何が答えられるかを設計する力が重要です。この点は当チームのPredictive / Causalの使い分けや前提設計と相性があります。ただし、高度分析専門会社やConsulting Analyticsも有力なので、相対優位は実績やDelivery Modelで確認する必要があります。

## A01-04f.5. 次頁への接続

> 最後に、分析・実装に加えてRiskやGovernanceが強く効くHigh Criticality案件を見る。