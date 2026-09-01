Document title: Deal Profileの6軸

# A01-03. Appendix｜Deal Profileの6軸

## A01-03.1. Message

**案件条件を6軸でProfile化すると、どの選択基準が重くなり、誰が有力かを比較できる。**

## A01-03.2. Chart

**チャートタイトル:** Deal Profileを共通6軸で記述する

### A01-03.2.1. Chart Structure

6軸を同じ形式で並べる。

| Deal Profile軸 | Low側 | High側 | 競争条件への主な影響 |
|---|---|---|---|
| Decision Altitude | Operational | Corporate / Strategic | Stakeholder / Governance / Org. Acceptability |
| Problem Novelty | Established | Novel / Uncertain | Fit / Capability / Evidence |
| Analytical Complexity | Standard | Complex Predictive / Causal / Experimental | Capability / Specialist Evidence |
| Solution Standardizability | Standard Product適合 | Individual Design | Economics / Product Fit / Flexibility |
| Implementation Coupling | Analysis-only | Enterprise System / Workflow統合 | Delivery / Risk / Org. Acceptability |
| Criticality / Governance | Low-risk / Reversible | Mission Critical / High Governance | Risk / Evidence / Governance |

中央下に因果関係を置く。

```text
Deal Profile｜6軸
        ↓
8 Selection CriteriaのWeight
        ×
Provider Base Profile｜A01-02a
        ↓
Deal-level Provider Position
```

### A01-03.2.2. Chart内の最小表示テキスト

- Decision Altitude
- Problem Novelty
- Analytical Complexity
- Solution Standardizability
- Implementation Coupling
- Criticality / Governance
- **6軸 → 8軸Weight → Provider Position**

## A01-03.3. Supporting Logic

### A01-03.3.1. Deal Typeだけでは粗すぎる

同じ「分析PoC」でも、定型的な需要予測、因果推論のFeasibility、Production前提のModel検証では、必要な専門性・Delivery・Risk管理が異なる。

Strategy / PoC / Productionのような箱だけでは競争条件を十分に説明できないため、商談特性を連続Profileとして記述する。

### A01-03.3.2. 本資料の6軸

1. **Decision Altitude**：Operational ↔ Corporate / Strategic
2. **Problem Novelty**：Established ↔ Novel / Uncertain
3. **Analytical Complexity**：Standard ↔ Complex Predictive / Causal / Experimental
4. **Solution Standardizability**：Standard Product適合 ↔ Individual Design
5. **Implementation Coupling**：Analysis-only ↔ Enterprise System / Workflow統合
6. **Criticality / Governance**：Low-risk / Reversible ↔ Mission Critical / High Governance

これは既存研究の標準6分類ではない。BUYGRID、Organizational Buying、B2B Customer Journey、Contingency的な考え方を踏まえ、分析PoC競争を説明するために本資料で操作的に定義したフレームである。

### A01-03.3.3. 各軸がWeightをどう変えるか

#### Decision Altitude

高くなるほどExecutive / Business / IT等のStakeholderが増え、Evidence / Governance / Organizational AcceptabilityのWeightが上がりやすい。

#### Problem Novelty

高くなるほどSolutionが事前に確定せず、Deal-specific Fit / Capability / Evidenceが重要になりやすい。

#### Analytical Complexity

高くなるほどSpecialist Talent、Methodological Capability、Relevant Evidenceの重要性が上がる。

#### Solution Standardizability

高い場合はProduct / Reuse / Economicsが効きやすく、低い場合はIndividual Design / Flexibilityが重要になる。

#### Implementation Coupling

高くなるほどSystem / Workflow / Security / Operationとの接続が増え、Delivery / Risk / Organizational Acceptabilityが重要になる。

#### Criticality / Governance

高くなるほど失敗時Downside、Compliance、Auditability、責任分界が重要になり、Risk / Evidence / GovernanceのWeightが上がる。

これらはProfileからWeightへの**分析仮説**であり、実証済み係数ではない。

### A01-03.3.4. 6軸は排他的カテゴリではない

実案件はA / B / Cのどれかに完全分類されるわけではない。各Dealを6軸上の一点または範囲として記述し、代表Anchor Profileとの近さで読む。

```text
Actual Deal
    ↓
6軸でProfile化
    ↓
A01-04a〜hのAnchorを参照
    ↓
必要なら複数Anchorの中間として評価
```

### A01-03.3.5. A01-02a / 02bとの関係

- A01-02：Customer Selection Criteriaを8軸で固定
- A01-02a：Provider類型ごとのBase Strengthを整理
- A01-02b：Dealによって8軸のWeightが変わることを整理
- A01-03：そのDeal条件を6軸で共通記述

従って後続のProvider Positionは、概念的に以下で決まる。

```text
Provider Position
  ← Provider Base Strength
  × Deal Profileから導くSelection Weight
```

### A01-03.3.6. A01-04への接続

次頁A01-04では、A01-04a〜hの代表Anchor Profileを横断し、当チームのCapability BundleがどのProfileで最も価値化しやすいかを総合する。

## A01-03.4. Speaker Note

ここまでで比較の部品が揃います。顧客が見る8軸、Provider側のBase Strength、商談によって変わるWeightです。最後に必要なのが、今回の案件をどう記述するかです。

それをこの6軸で表します。分析難易度だけでなく、問題の新規性、標準Productへ載せられるか、Enterprise Systemとの接続、失敗時の影響、意思決定の高さまで含めます。

この6軸を使うことで、A01-04a〜hを同じ座標系で比較できます。次頁では、そのProfile別分析をまとめて当チームの重点Positioningを示します。

## A01-03.5. Appendix A01-03からA01-04への接続

> 比較軸、Provider Base Strength、Deal Weight、Deal Profileの定義が揃った。次に8つの代表Profileを横断して、当チームがどこで強みを出しやすいかを総合する。

## A01-03.6. Sources

- Webster, F. E. Jr. & Wind, Y. (1972), “A General Model for Understanding Organizational Buying Behavior,” *Journal of Marketing*. https://doi.org/10.1177/002224297203600204
- Sheth, J. N. (1973), “A Model of Industrial Buyer Behavior,” *Journal of Marketing*. https://doi.org/10.1177/002224297303700408
- Robinson, Faris & Wind (1967), *Industrial Buying and Creative Marketing*.
- “B2B customer journeys: Conceptualization and an integrative framework,” *Industrial Marketing Management*, 113 (2023), 74–87. https://doi.org/10.1016/j.indmarman.2023.05.020