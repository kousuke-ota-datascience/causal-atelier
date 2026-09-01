Document title: Deal Profileと比較優位曲面

# A01-03. Appendix｜Deal Profileと比較優位曲面

## A01-03.1. Message

**商談は箱ではなく連続Profileとして捉え、比較優位もグラデーションで見る。**

## A01-03.2. Chart

**チャートタイトル:** Deal TypeからDeal Profileへ

### A01-03.2.1. Chart Structure

左側に「離散分類」、右側に「連続Profile」の対比を置く。

```text
Before｜Deal Type
────────────────
Strategy
Analytical PoC
Production
Product Adoption

        ↓

After｜Deal Profile
────────────────
Decision Altitude
Problem Novelty
Analytical Complexity
Solution Standardizability
Implementation Coupling
Criticality / Governance
```

右下に、比較優位が固定ラベルではなく曲面として変わる概念図を置く。

```text
Comparative Advantage
High                 ▲
                     │        ● Core Zone
                     │      ●●●●
                     │    ●●●●●
                     │  ●●●
                     │ ●
Low  ────────────────┴────────────────▶ Deal Profile
```

下部に3ゾーンを置く。

- Core Zone：比較優位が最も出やすい
- Adjacent Zone：十分競争可能
- Commodity / Disadvantaged Zone：対応可能だが他選択肢が合理的な場合もある

### A01-03.2.2. Chart内の最小表示テキスト

- **Deal Type → Deal Profile**
- 6つの連続軸
- **Service Coverage ≠ Comparative Advantage**
- Core / Adjacent / Commodity Zone

## A01-03.3. Supporting Logic

### A01-03.3.1. Deal Typeの限界

Strategy / PoC / Production等のDeal Typeは説明上は有用だが、同じPoCでも実際には以下が連続的に異なる。

- 新規性が低い / 高い
- 分析難易度が低い / 高い
- 既製Solutionへ載せやすい / 個別設計が必要
- 分析単体 / 業務・Systemと強く結合
- 小規模 / Mission Critical

したがって、商談を排他的なBoxへ分類すると、同一Type内の競争条件の違いを見落とす。

### A01-03.3.2. Deal Profileの6軸

本資料では、分析PoCサービスの競争構造を見るための操作的な仮説として、以下の6軸を使う。

1. **Decision Altitude**：Operational ↔ Corporate / Strategic
2. **Problem Novelty**：Established ↔ Novel / Uncertain
3. **Analytical Complexity**：Standard ↔ Complex Predictive / Causal / Experimental
4. **Solution Standardizability**：Standard Product適合 ↔ Individual Design
5. **Implementation Coupling**：Analysis-only ↔ Enterprise System / Workflow統合
6. **Criticality / Governance**：Low-risk / Reversible ↔ Mission Critical / High Governance

これは既存理論の標準6分類ではない。BUYGRID、Organizational Buying、Contingency Logic等を踏まえた競争分析用の実務フレームである。

### A01-03.3.3. BUYGRIDの位置づけ

New Task / Modified Rebuy / Straight Rebuyは、Vendorを排他的に選ぶルールではない。

本検討では、Problem Novelty / Buying Uncertainty軸を理解する代表的なAnchorとして利用する。

```text
Low                                           High
Straight Rebuy ─── Modified Rebuy ─── New Task
```

### A01-03.3.4. Selection CriteriaもProfileから変化する

Deal Profileが変われば、顧客が重視するSelection CriteriaのWeightも変化する。

例：

- Analytical Complexity ↑ → Capability / Evidenceの重要度が上がりやすい
- Implementation Coupling ↑ → Delivery / Risk / Organizational Acceptabilityが上がりやすい
- Criticality ↑ → Evidence / Governance / Riskが上がりやすい
- Problem Novelty ↑ → Deal-specific Fit / Capability / Relational Fitが上がりやすい

これらは実証済み係数ではなく、Organizational Buying / Contingency logicに基づく仮説である。

### A01-03.3.5. 比較優位は曲面として考える

VendorのCapabilityを固定Scoreとして扱わない。

概念的には、Deal Profileを `x(D)` とすると、

```text
Selection Weight_j = f_j(x(D))
Vendor Fit_j       = g_j(V, x(D))
```

となり、最終的な比較優位はProfileとのInteractionで変化する。

重要なのは、

> **ある領域で最も強いからといって、他領域を対応しないわけではない。**

という点である。

### A01-03.3.6. Focused Positioningの再定義

Focused Positioningは「この案件しかやらない」という意味ではない。

> **比較優位が最大になるDeal Profileを明確にし、そこを主戦場として顧客に想起してもらう。**

という意味である。

従って、Service CoverageとMarketing Positioningは一致しなくてよい。

## A01-03.4. Speaker Note

商談をStrategy、PoC、Productionのようなカテゴリーで分類するだけでは、まだ粗すぎます。同じPoCでも、定型的な需要予測と、前提や評価方法から設計する因果推論では競争条件が違います。

そこで商談を、Decision Altitude、新規性、分析難易度、標準化可能性、Systemとの結合度、Criticalityという複数の連続軸で捉えます。

こうすると、当チームにも競合にも「ここから先はできない」という硬い境界を置く必要がありません。対応可能な範囲は広くても、比較優位が最も出やすいCore Zone、その周辺のAdjacent Zone、他のProviderの方が合理的な場合も多い領域が連続的に存在すると考えます。

## A01-03.5. Appendix A01-03からA01-04への接続

> このDeal Profile上で当チームのCapabilityがどこで最も価値化しやすいかを置くと、Why Usの仮説を具体化できる。