Document title: 当チームのWhy Us仮説

# A01-04. Appendix｜当チームのWhy Us仮説

## A01-04.1. Message

**非定型・高難度の分析とEnterprise利用の両方が重要な商談で強みが出やすい。**

## A01-04.2. Chart

**チャートタイトル:** 当チームのSweet Spot仮説｜Specialist Analytics × Enterprise Base

### A01-04.2.1. Chart Structure

中央に2軸マップを置く。

- 縦軸：Analytical Complexity
- 横軸：Implementation Coupling

```text
                 Analytical Complexity
                        High
                         ▲
                         │
  Specialist Analytics  │     ★ 当チームSweet Spot仮説
                         │
  ・高度分析             │     Specialist Analytics
  ・非定型検証           │             ×
                         │       Enterprise Base
                         │
─────────────────────────┼────────────────────────▶
                         │              Implementation Coupling
                         │
  Standard / Commodity   │     SI / Production-oriented
                         │
                        Low
```

Sweet Spotの右側にSupporting Capabilityを4つ置く。

1. Predictive / CausalをDecision Problemから使い分ける
2. Scratch / OSSによる非定型Analytical Design
3. 前提・評価・Limitationまで扱うScientific Validity
4. Enterprise Data / System / Governanceを考慮できるSIer context

下部にWhy Us候補を置く。

> **定型解のない分析課題に、専門的な分析設計とEnterpriseの実装視点を一つのPoCで持ち込む。**

### A01-04.2.2. Chart内の最小表示テキスト

- **Specialist Analytics × Enterprise Base**
- 高度・非定型な分析
- Enterprise利用条件
- Predictive / Causal
- Scratch / OSS
- Scientific Validity
- Enterprise Fit

## A01-04.3. Supporting Logic

### A01-04.3.1. 確認済みのチーム特徴

現時点で確認できているのは以下である。

- SIerのデータ分析部門
- Predictive / Causal PoCを提供
- データサイエンティストによるスクラッチ開発を基本とする
- 必要に応じ成熟OSS / Libraryを利用
- 特定Product導入を必須前提としない
- Predictive / Causalで問い・前提・評価を分けて扱う
- 分析結果をDecision / Actionへ接続することを重視する

ただし、これらの個別項目は優秀な競合にも実行可能であり、単独では強い差別化にならない。

### A01-04.3.2. 強み仮説1｜Analytical Design

Problem Novelty / Analytical Complexityが高いほど、以下の価値が上がると仮説化する。

- 何を予測すべきかを定義する
- PredictionとCausalを区別する
- Estimand / Assumption / Evaluationを設計する
- 既存データで何が答えられるかを見極める
- 顧客固有の評価条件へ対応する

既製Solutionへ課題を合わせるのではなく、問いへ必要な分析を構成する能力が効く。

### A01-04.3.3. 強み仮説2｜Technology非固定

Solution Standardizabilityが低い商談では、Scratch / OSSによる柔軟な実装が価値を持つ。

一方、既製Productに高くFitする課題では、AI Vendor等のSpeed / Economicsが優位になる可能性がある。

### A01-04.3.4. 強み仮説3｜Enterprise Base

Implementation Coupling / Criticalityが高まるほど、分析だけでなく、

- Enterprise Data
- Security
- System
- Governance
- 本番利用条件

等を考える必要性が増す。

これはSIer内の分析組織という位置づけが価値を持ち得る領域である。

ただし、他SIer Analyticsとの差別化にはならないため、単独のWhy Usにはしない。

### A01-04.3.5. 組合せとしての差別化仮説

個別Capabilityではなく、以下の交差領域を仮説上のSweet Spotとする。

```text
Problem Novelty           Medium〜High
Analytical Complexity     Medium〜High
Standardizability         Low〜Medium
Implementation Coupling   Medium〜High
Criticality / Governance  Medium〜High
```

つまり、

> **定型Solutionでは解きにくいが、分析だけのResearchでもなく、将来の業務・System利用を考慮する必要がある問題**

である。

### A01-04.3.6. 競合類型との相対関係

以下は固定的な強弱ではなく、Deal Profile上の仮説である。

| Deal Profile | 比較優位が出やすいProvider仮説 |
|---|---|
| Decision Altitudeが極めて高くStrategy比率が高い | 総合コンサルAnalytics |
| Analytical Complexityが高くImplementation Couplingが低い | DS専門会社 / Research Boutique |
| Analytical Complexityが低くImplementation Couplingが高い | 一般SIer / Production Delivery |
| Standardizabilityが極めて高い | AI / Product Vendor |
| Analytical ComplexityとImplementation Couplingが共に高い | **当チームのSweet Spot候補** |

他社にも同様のCapabilityを持つ組織は存在するため、この表は「他社にはできない」という主張ではない。

### A01-04.3.7. Evidence Gap

Why Us仮説を顧客向けの競争優位主張へ昇格させるためには、以下のEvidenceが必要である。

**人材**

- Predictive / Causal専門人材数
- Seniority
- 論文 / 学会 / 特許 / OSS

**案件**

- 高難度・非定型分析案件数
- Causal / Predictive案件数
- System / Productionまで接続した事例

**Delivery Model**

- Specialistが顧客との問い設計から実装までどこまで直接担当するか
- SI部門との連携方法

**Customer Evidence**

- 顧客が当チームを選んだ理由
- Repeat率
- 競合比較で勝った理由

現時点では、Speed / Cost / Accuracy等の競合優位はEvidence不足のため主張しない。

## A01-04.4. Speaker Note

ここまでの競争分析を当チームへ当てはめると、現時点で最も有力なのは「Specialist AnalyticsとEnterprise Baseの組み合わせ」です。

因果推論ができること自体や、SIerとして本番を考えられること自体は差別化ではありません。どちらも競合に存在します。

一方で、分析方法自体を設計しなければならない非定型・高難度の課題でありながら、分析だけで完結せず、将来の業務利用やシステム、Governanceも無視できない商談では、両方の能力が同時に必要になります。この交差領域が、当チームの比較優位が最も出やすいSweet Spotではないか、というのが現時点の仮説です。

ただし、これはまだPositioning仮説です。最終的にWhy Usとして外部へ主張するには、専門人材、案件実績、顧客評価などのEvidenceで裏付ける必要があります。

## A01-04.5. Appendix A01-04から本編への接続

> 本編Slide 5では、この詳細な競争分析を圧縮し、「高度・非定型な分析 × Enterprise利用」というSweet Spotを顧客向けのWhy Usとして提示する。