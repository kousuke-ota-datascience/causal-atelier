Document title: Deal Profileで変わる比較優位

# A01-03. Appendix｜Deal Profileで変わる比較優位

## A01-03.1. Message

**同じ「分析PoC」でも、分析難易度と実装条件によって適したProviderは変わる。**

## A01-03.2. Chart

**チャートタイトル:** Providerの強みはDeal Profile上でグラデーションに変化する

### A01-03.2.1. Chart Structure

中央に、顧客が直感的に理解しやすい2軸を置く。

- 縦軸：Analytical Complexity
- 横軸：Implementation Coupling

```text
                 Analytical Complexity
                        High
                         ▲
                         │
   分析方法そのものを     │      高度分析とEnterprise条件を
   設計する必要が高い     │      同時に考える必要が高い
                         │
                         │
─────────────────────────┼────────────────────────▶
                         │              Implementation Coupling
                         │
   定型的・分析単体       │      System / Operationとの
                         │      接続が中心
                        Low
```

その周囲に補助軸として、Deal Profileの残りの特性を配置する。

```text
Problem Novelty            Established ───────── Novel
Solution Standardizability High ──────────────── Low
Criticality / Governance   Low ───────────────── High
Decision Altitude          Operational ───────── Strategic
```

図の下に、比較優位を「点」ではなく「領域」で示す原則を置く。

> **各Providerの対応範囲は重なる。違いは、Deal Profile上で強みが最も効く領域。**

### A01-03.2.2. Chart内の最小表示テキスト

- Analytical Complexity
- Implementation Coupling
- Problem Novelty
- Standardizability
- Criticality
- **対応範囲は重なる / 比較優位はグラデーション**

## A01-03.3. Supporting Logic

### A01-03.3.1. Deal Typeだけでは競争条件を説明できない

「分析PoC」という同じ名称でも、案件は大きく異なる。

例えば、

- 定型的な需要予測
- 特徴量・評価指標から設計するPrediction
- 観察データから施策効果を推定するCausal Inference
- 将来の本番System利用を前提とするPoC

では、必要な専門性・Delivery・Risk管理が異なる。

従って、Strategy / PoC / Productionのような箱だけではなく、商談特性を連続Profileとして捉える。

### A01-03.3.2. 本資料のDeal Profile

分析PoCサービスの競争条件を説明する実務フレームとして、以下6軸を用いる。

1. **Decision Altitude**：Operational ↔ Corporate / Strategic
2. **Problem Novelty**：Established ↔ Novel / Uncertain
3. **Analytical Complexity**：Standard ↔ Complex Predictive / Causal / Experimental
4. **Solution Standardizability**：Standard Product適合 ↔ Individual Design
5. **Implementation Coupling**：Analysis-only ↔ Enterprise System / Workflow統合
6. **Criticality / Governance**：Low-risk / Reversible ↔ Mission Critical / High Governance

これは既存研究の標準6分類ではなく、BUYGRID、Organizational Buying等を踏まえた本資料の操作的フレームである。

### A01-03.3.3. 顧客向けには2軸を主図にする

6軸すべてを一枚で可視化すると複雑になるため、01-05のPositioningと直接関係する、

- Analytical Complexity
- Implementation Coupling

を主軸にする。

残りの軸は、同じ2軸位置でも競争条件を変える補助条件として扱う。

### A01-03.3.4. なぜグラデーションなのか

各Providerに「ここから先は対応不能」という硬い境界があるわけではない。

例えば、

- Consulting Analyticsも高度分析を実行できる
- DS SpecialistもSystem Integrationを支援できる
- SIer AnalyticsもCausal / Advanced Analyticsを提供できる

場合がある。

それでも、組織の人材構成、Asset、Delivery Model、案件経験、Commercial Model等により、**どのDeal Profileで相対的に強みを発揮しやすいか**は変わる。

したがってPositioning MapではProviderを一点に固定せず、重なりを持つ領域・楕円として表現する。

### A01-03.3.5. 比較優位の考え方

内部分析上は、Deal Profile `x(D)` が変わることで、顧客のSelection CriteriaのWeightと各ProviderのFitが同時に変化すると考える。

```text
Selection Weight_j = f_j(x(D))
Provider Fit_j     = g_j(V, x(D))
```

これは実証済み係数ではなく、商談依存性を表現する概念モデルである。

顧客向けの結論はシンプルである。

> **どのProviderも広く対応できるが、案件条件によって「最も選ぶ理由が強くなるProvider」は変わる。**

### A01-03.3.6. 当チームへの接続

当チームの01-05で示した3つの価値、

- 問いに合うPredictive / Causalを選ぶ
- Scratch / OSSで非定型課題に合わせる
- Enterprise利用段階まで見据える

は、特にAnalytical ComplexityとImplementation Couplingが共に一定以上高い領域で同時に必要になりやすい。

次頁では、この2軸上に競合類型と当チームを同時に配置し、Positioningの違いを示す。

## A01-03.4. Speaker Note

同じ分析PoCでも、案件の中身によって必要なProviderは変わります。既存のモデルを適用すればよい案件もあれば、問いや評価方法から設計しなければならない案件もあります。また、分析単体で完結する案件もあれば、将来のSystemや業務運用まで考える必要がある案件もあります。

ここではその違いを、分析設計の難しさと、Enterprise Systemや業務との接続度という2軸で見ています。実際には新規性、標準化可能性、Criticality等も影響します。

重要なのは、各Providerの対応範囲にはかなり重なりがあることです。そのため境界線ではなくグラデーションで考えます。その上で、各社が最も強みを発揮しやすい領域を比較するのが次のPositioning Mapです。

## A01-03.5. Appendix A01-03からA01-04への接続

> このDeal Profile上に各Providerの強みが出やすい領域を重ねると、「どこも同じ」に見える市場の中で、当チームがどこを主戦場としているかを説明できる。