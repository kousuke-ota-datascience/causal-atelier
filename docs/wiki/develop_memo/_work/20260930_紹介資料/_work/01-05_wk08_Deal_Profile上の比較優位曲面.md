# 01-05 wk08｜Deal Profile上の比較優位曲面

## 1. 目的

`01-05_wk07_商談文脈を加味した競争構造マッピング.md` では、Vendor類型を固定的に評価するのではなく、**Deal Contextを先に定義し、その条件下でSelection CriteriaとVendorの比較優位を評価する**モデルへ修正した。

しかし、`wk07` にもなお離散化が強すぎる問題が残る。

例えば、

- Strategy / Advisory
- Analytical PoC
- System Design
- Build / Operate

といったDeal Archetypeは、実務上の商談を理解するための代表例としては有用である一方、現実の商談はそのどれか一つへ完全に分類できるとは限らない。

同じAnalytical PoCでも、

- 新規性が低い / 高い
- 分析難易度が低い / 高い
- 既製Solutionへ載せやすい / 個別設計が必要
- 分析単体 / 本番システムと強く結合
- 小規模 / Mission Critical

という連続的な差がある。

また、当チームにも得意領域・不得意領域はあるが、

> 「このDeal Typeだけ実施する / このDeal Typeは実施しない」

という排他的な境界が存在するわけではない。

したがって本書では、Dealを離散的なTypeとして分類するのではなく、**複数の連続軸上の位置＝Deal Profileとして捉え、そのProfileに応じて各Providerの比較優位が滑らかに変化する**モデルへ更新する。

本書の中心命題は以下である。

> **競争優位はDeal TypeごとにON / OFFで発生するのではなく、Deal ProfileとのFitに応じて連続的に変化する。**

---

# 2. 理論的背景

## 2.1. BUYGRIDは排他的なVendor選択ルールではない

Robinson, Faris & WindによるBUYGRID frameworkは、industrial buyingのBuying Situationを以下の3類型に整理する。

- New Task
- Modified Rebuy
- Straight Rebuy

これは購買課題の新規性、必要情報量、検討プロセス等を理解するうえで有用である。

一方で、BUYGRIDは、

> New TaskならVendor A、Straight RebuyならVendor B

というProvider選択の排他的ルールを与えるものではない。

本検討ではBUYGRIDを、商談を3つの箱へ固定分類するためではなく、**Problem Novelty / Buying Uncertainty軸を理解するための代表的なAnchor**として利用する。

概念的には以下である。

```text
Problem Novelty / Buying Uncertainty

Low                                                High
│---------------------------------------------------│
Straight Rebuy       Modified Rebuy            New Task
```

**出典:**

- Robinson, P. J., Faris, C. W., & Wind, Y. (1967). *Industrial Buying and Creative Marketing*. Allyn & Bacon.

---

## 2.2. Contingency Logic｜「唯一最善」ではなくContextとのFitを見る

Contingency Theoryでは、組織や管理方式について「常に唯一最善の形」が存在するのではなく、environment、technology、strategy、size等とのfitによってperformanceが変わるという考え方を採る。

本検討では、この考え方をProvider selectionへ直接理論移植するのではなく、以下の**分析原理**として利用する。

> **ProviderのCapabilityを固定的に順位づけするのではなく、Deal ContextとのFitによって相対優位が変化すると考える。**

例えば、同じProviderでも、

- 非定型・高難度分析では強い
- 定型Product導入では相対優位が薄い
- 本番統合が極めて重要なら再び強みが出る

ということがあり得る。

**参考文献:**

- Tosi, H. L., & Slocum, J. W. Jr. (1984). *Contingency Theory: Some Suggested Directions*. Journal of Management, 10(1), 9–26.  
  https://doi.org/10.1177/014920638401000103

※本書のDeal Profileモデル自体は既存のContingency Theoryの標準モデルではない。Context-dependent fitという考え方を競争分析へ応用した実務フレームである。

---

# 3. Deal TypeからDeal Profileへ

## 3.1. Deal Typeによる離散分類

`wk07` では、説明用に以下のようなDeal Archetypeを置いた。

- 全社AI / Data Transformation構想
- 未知テーマのPrediction / Causal PoC
- 既存予測モデルの本番化
- Productized AI導入

これは典型例を理解するには有用である。

しかし、実案件を、

```text
Deal A = Analytical PoC
Deal B = Production
```

と排他的に分類すると、同じカテゴリー内部の大きな差を見落とす。

---

## 3.2. Deal Profileによる連続表現

Dealを複数の連続軸上の位置として表現する。

概念的に、商談 `D` を以下のProfile vectorで表す。

```text
Deal Profile(D)
=
(
  Decision Altitude,
  Problem Novelty,
  Analytical Complexity,
  Solution Standardizability,
  Implementation Coupling,
  Criticality / Governance
)
```

実際に数値Scoreを付ける必要はない。

重要なのは、

> 「どのTypeか」

ではなく、

> **「各軸のどこに位置する商談か」**

を見ることである。

---

# 4. Deal Profileを構成する6軸

以下の6軸は既存理論の標準分類ではなく、分析PoCサービスの競争構造を考えるための操作的な仮説である。

## 4.1. ① Decision Altitude

**問い:** 商談の主な意思決定は、組織のどの高度に位置するか。

```text
Operational / Individual Action
                ↕
Business / Management
                ↕
Corporate / Strategic Decision
```

### Low側

- 誰に連絡するか
- 何件発注するか
- どの商品を推薦するか

### High側

- どの事業へ投資するか
- 全社AI戦略をどう設計するか
- どの市場へ参入するか

### 競争構造への示唆

Decision Altitudeが高くなるほど、

- Strategy
- Stakeholder Alignment
- Executive Communication
- Organizational Acceptability

等の重要度が上がる可能性がある。

一方、Altitudeが低いほど、

- Analytical specificity
- Operational feasibility
- Workflow integration

等が相対的に重要になる可能性がある。

---

## 4.2. ② Problem Novelty / Buying Uncertainty

**問い:** 顧客にとって、その問題・購買はどの程度未知か。

```text
Established / Repetitive
                ↕
Partially Known
                ↕
Novel / Uncertain
```

BUYGRIDのStraight Rebuy / Modified Rebuy / New Taskは、この連続軸を理解するAnchorとして扱う。

### Noveltyが低い例

- 毎年実施している需要予測モデル更新
- 定型レポーティング
- 既存Solutionの追加導入

### Noveltyが高い例

- 初めて解く施策効果問題
- 適切な分析方法自体が不明
- Data availability / answerabilityも不明

### 競争構造への示唆

Noveltyが高いほど、

- problem framing
- specialist capability
- joint problem solving
- evidence / credibility
- learning ability

等の重要度が高まる可能性がある。

---

## 4.3. ③ Analytical Complexity

**問い:** 問いへ答えるために、どの程度高度・非定型な分析設計が必要か。

```text
Descriptive / Standard Analysis
                ↕
Standard Predictive Modeling
                ↕
Complex Predictive / Causal / Experimental Design
```

Complexityを単純に「高度なAlgorithmを使うか」で測らない。

例えば以下を含む。

- Evaluation design complexity
- Identification difficulty
- Data limitations
- Rare event / small sample
- time-dependent structure
- multiple treatment / intervention
- heterogeneous effects
- Decision-specific loss / utility

### 競争構造への示唆

Analytical Complexityが高いほど、

- Methodological Capability
- Specialist Evidence
- Senior Expert involvement
- Flexible / scratch implementation

の重要度が高まる可能性がある。

---

## 4.4. ④ Solution Standardizability

**問い:** 課題を既存Product / Solution / Templateへどの程度そのまま載せられるか。

```text
Highly Standardizable
                ↕
Configurable
                ↕
Highly Bespoke
```

### Standardizabilityが高い例

- 一般的なOCR
- 定型Recommendation
- 標準的なForecasting SaaS
- 既存AI Platform capabilityと高Fit

### Standardizabilityが低い例

- 特殊なTreatment / Outcome定義
- 顧客固有のDecision Rule
- 複雑なData Generating Process
- 複数分析を組み合わせた非定型Decision Problem

### 競争構造への示唆

Standardizabilityが高いほど、Product Vendorの、

- Speed
- Economics
- Reuse
- Scale

が効きやすい。

Bespoke側へ寄るほど、

- Flexible design
- Specialist expertise
- scratch implementation

の価値が上がる可能性がある。

---

## 4.5. ⑤ Implementation Coupling

**問い:** 分析成果と業務・システム実装がどの程度不可分か。

```text
Analysis Standalone
                ↕
Decision / Workflow Integration
                ↕
Deep Enterprise System Integration
```

### Couplingが低い例

- 一度だけの効果検証
- 経営判断用分析
- 仮説検証PoC

### Couplingが高い例

- リアルタイム予測
- ERP / CRMへのModel組込み
- MLOps
- Security / SLAが必要な本番運用

### 競争構造への示唆

Implementation Couplingが高まるほど、

- Delivery Feasibility
- System Integration
- Security
- Governance
- Operation

のWeightが上がり、SIer系Providerの比較優位が強くなりやすい。

---

## 4.6. ⑥ Criticality / Governance Intensity

**問い:** 失敗時の影響や組織的な統制要求はどの程度大きいか。

```text
Low Stakes / Reversible
                ↕
Business Important
                ↕
Mission Critical / Regulated
```

評価要素：

- Investment size
- Operational impact
- Regulatory impact
- Security / Privacy
- Reversibility
- Reputation risk
- Business continuity

### 競争構造への示唆

Criticalityが高くなるほど、

- Risk
- Evidence
- Governance
- Organizational Acceptability
- Provider continuity

等の重要度が高まる可能性がある。

---

# 5. Deal ProfileとSelection Criteriaの関係

`wk04` で整理した8つのCustomer Selection Criteriaは維持する。

1. Deal-specific Fit
2. Capability / Quality
3. Delivery Feasibility
4. Economic Value
5. Risk
6. Evidence / Credibility
7. Relational / Governance Fit
8. Organizational Acceptability

ただし、それぞれの重要度は固定ではない。

**Deal Profileによって重みが変化する。**

例として以下のような関係を仮説化できる。

| Deal Profileの変化 | 重みが高まり得るSelection Criteria |
|---|---|
| Decision Altitude ↑ | Fit、Evidence、Relationship、Organizational Acceptability |
| Problem Novelty ↑ | Fit、Capability、Evidence、Relationship |
| Analytical Complexity ↑ | Capability、Evidence、Risk |
| Standardizability ↑ | Economic Value、Delivery、Evidence |
| Bespoke度 ↑ | Fit、Capability、Relationship |
| Implementation Coupling ↑ | Delivery、Risk、Organizational Acceptability |
| Criticality ↑ | Risk、Evidence、Governance、Organizational Acceptability |

この表は実証済み係数ではなく、組織購買論とProvider特性から導いた競争分析上の仮説である。

---

# 6. VendorのCapability Scoreも固定ではない

`wk05` のように、

```text
Consulting    Problem Fit = High
SIer          Delivery    = High
AI Vendor     Economics   = High
```

と固定評価するのは不十分である。

例えばSIerであっても、

- System integrationがほぼ不要な一度限りの高度分析

ではDelivery capabilityの相対価値は小さい。

一方、

- 本番システムへのReal-time integrationが必須

なら大きな競争優位となり得る。

したがってVendor評価も、

```text
Vendor Capability × Deal Profile
```

の相互作用として考える。

---

# 7. 比較優位曲面という考え方

## 7.1. 二次元で単純化した例

例えば、

- X軸 = Analytical Complexity
- Y軸 = Implementation Coupling

だけで考える。

```text
Implementation Coupling
High
 │
 │                     SIer / SIer Analytics
 │                        ●●●●●
 │                    ●●●●●
 │                ●●●●
 │
 │          当チームのSweet Spot ?
 │             ●●●●●
 │          ●●●●●●
 │       ●●●●●
 │
 │  DS Specialist
 │     ●●●●
 │
 └──────────────────────────────→
       Low       Analytical Complexity       High
```

実際には6次元Profileなので、このような単純な図にはならない。

重要なのは、各Providerに、

> **比較優位が最大になる領域と、そこから離れるにつれて優位が低下する領域がある**

という発想である。

---

## 7.2. 境界線ではなくGradient

Providerについて、

```text
このDealはできる
このDealはできない
```

という二値分類を置かない。

代わりに、

```text
Relative Advantage
High
 │                  ● Sweet Spot
 │              ●●●●●
 │           ●●●●●●
 │        ●●●●●
 │     ●●●
 │   ●●
 │ ●
 └──────────────────────────
           Deal Profile
```

と考える。

したがって、

- 得意領域外の案件も対応可能
- ただし他Providerと比較した選ばれやすさは低下する
- 得意領域の中心へ近づくほど相対優位が高まる

という連続的なモデルとなる。

---

# 8. Core / Adjacent / Disadvantaged Zone

Focused Positioningを「特定Dealしか受けない」と解釈しない。

代わりに、Deal Profile空間上で以下のZoneを考える。

## 8.1. Core Zone

> **当チームの比較優位が最も高くなる領域。**

特徴：

- 顧客Selection Criteriaと当チームの強みが高く整合
- 明確なSignal of Excellenceを提示可能
- 競合と比較して選択合理性を説明しやすい

マーケティング上、最も強く訴求する領域。

---

## 8.2. Adjacent Zone

> **十分競争可能だが、競合優位も存在する領域。**

特徴：

- 案件条件によって勝敗が変わる
- Existing relationship / price / specific capability等が重要
- 通常の営業対象にはなり得る

---

## 8.3. Disadvantaged / Commodity Zone

> **対応可能であっても、他Providerを選ぶ合理性が高い領域。**

例：

- 高度に標準化された安価なSaaSで十分
- 分析要素がほぼなく大規模System Integrationが中心
- Pure Strategyで経営Transformation capabilityが中心

ここでも「やらない」とは限らない。

重要なのは、マーケティング上のPrimary Positionから外れることである。

---

# 9. Focused Positioningの再定義

Focused Positioningを、

> 狭い対象しか対応しない

という意味にしない。

本検討では以下と定義する。

> **自社の比較優位が最大になるDeal Profileを明確にし、その領域で第一想起されるようValue PropositionとEvidenceを集中すること。**

したがって、

```text
Service Coverage
        ≠
Marketing Positioning
```

である。

例えば、

> 「高度な非定型分析PoCに強い」

とPositioningしても、定型予測案件を受けてはいけないことを意味しない。

**何を提供可能かではなく、何で選ばれたいかを決める。**

---

# 10. 当チームについての適用仮説

現時点で当チームについて確認済みの事実：

- SIerのデータ分析部門である。
- Predictive / Causal PoCを提供する。
- Data Scientistによるscratch developmentを基本とする。
- 必要に応じ成熟したOSSを利用する。
- Prediction / Causalで問い・推論対象・評価条件を分離して扱う。
- Ariadneは必須Productではない。

これらから、現時点で以下の方向に比較優位が強まる可能性を仮説化できる。

### 仮説1｜Problem Noveltyが高まるほど相対優位が上がる可能性

理由候補：

- 解法を固定せず分析設計できる
- Predictive / Causalの選択が可能
- scratch implementationが可能

ただし、コンサルAnalytics / DS専門会社も強いため、単独では差別化にならない。

---

### 仮説2｜Analytical Complexityが高まるほど相対優位が上がる可能性

理由候補：

- Predictive / Causal双方を扱う
- Methodological designを重視する

ただし、専門人材・案件実績のEvidenceが必要。

---

### 仮説3｜Implementation Couplingが一定以上ある領域でも競争力を維持できる可能性

DS Specialistに対し、SIer基盤により、

- System context
- Security
- production transition

等への接続が可能である可能性がある。

ここは「SIer Analyticsとして普通」で終わる可能性もあるため、他SIerとの差別化には追加Evidenceが必要。

---

### 仮説4｜最も有望なのは複数軸の交差領域

単一軸では差別化しにくい。

例えば、

```text
Problem Novelty           High
Analytical Complexity     High
Standardizability         Low〜Medium
Implementation Coupling   Medium〜High
Criticality               Medium〜High
```

のような領域では、

- DS Specialistの分析専門性
- SIerのEnterprise Delivery capability

の双方が必要になるため、当チームのPositioning候補となり得る。

ただしこれは現時点では仮説である。

---

# 11. Selection Criteriaとの接続

Deal Profileから顧客Selection Criteriaの重みを考え、そこへ当チームのStrength / Evidenceを対応させる。

例えば、

```text
Problem Novelty ↑
Analytical Complexity ↑
        ↓
Capability / Evidenceの重要度 ↑
        ↓
当チームに実績・専門人材があれば
Relative Advantage ↑
```

一方、

```text
Standardizability ↑
Analytical Complexity ↓
        ↓
Economic Value / Speedの重要度 ↑
        ↓
Productized AI VendorのRelative Advantage ↑
```

また、

```text
Implementation Coupling ↑
Criticality ↑
        ↓
Delivery / Risk / Org. Acceptability ↑
        ↓
SIer系ProviderのRelative Advantage ↑
```

といった形で、**Deal Profile → Selection Criteria → Relative Advantage**をつなぐ。

---

# 12. 数理的な概念表現

## 12.1. Deal Profile

商談をProfile vector `x(D)` とする。

```text
x(D)
=
(
 Decision Altitude,
 Problem Novelty,
 Analytical Complexity,
 Solution Standardizability,
 Implementation Coupling,
 Criticality
)
```

## 12.2. 顧客Selection Criteriaの重み

Selection Criterion `j` のWeightは、Deal Profileの関数とする。

```text
w_j = f_j(x(D))
```

## 12.3. VendorのCriterion上の適合度

Vendor `V` のCriterion `j` における適合度も、Deal Profileに依存する。

```text
s_j = g_j(V, x(D))
```

## 12.4. Deal条件付きUtility

概念的には、

```text
U(V | D)
=
Σ_j f_j(x(D)) × g_j(V, x(D))
```

と表せる。

この式は実証モデルではなく、競争構造を考えるための概念表現である。

重要なのは、

> VendorのStrengthは固定Scoreではなく、Deal Profileとのinteractionによって発現する

という点である。

---

# 13. wk05 → wk07 → wk08の発展

## wk05｜Vendor固定評価

```text
Vendor Type
    ↓
8軸評価
    ↓
Competitive Advantage
```

問題：

- Vendor capabilityを固定値として扱いすぎる
- 同一顧客でも商談ごとに違うことを表現できない

---

## wk07｜Deal Context条件付き評価

```text
Deal Context
    ↓
Selection Criteria
    ↓
Vendor Comparison
    ↓
Why Us
```

改善：

- 商談ごとに評価が変わることを表現した

残課題：

- Deal Archetypeによる離散分類が残る
- 当チームの得意 / 不得意を境界的に捉えやすい

---

## wk08｜Deal Profile上の比較優位曲面

```text
Continuous Deal Profile
    ↓
Selection Criteria Weight
    ↓
Context-specific Vendor Fit
    ↓
Relative Advantage Surface
    ↓
Core / Adjacent / Disadvantaged Zone
    ↓
Focused Positioning
```

これにより、

- 同じDeal Type内部の差
- 同一顧客の商談間差
- Providerの得意 / 不得意のGradient
- 提供可能範囲とMarketing Positioningの分離

を同時に扱える。

---

# 14. Why Usへの意味

Why Usを、

> 当チームは何でも他社より優れている

という主張として作らない。

また、

> このDeal Typeだけを対象とする

という排他的Positioningにもする必要はない。

代わりに、

> **当チームの比較優位が最大になるDeal Profileはどこか。**

を特定し、その領域で顧客が重視するSelection Criteriaに対して、

- どのStrengthが効くか
- 何をEvidenceとして提示できるか

を明確にする。

したがってWhy Us導出は、以下となる。

```text
当チームのAsset / Capability
          ＋
Deal Profile
          ↓
Selection CriteriaとのFit
          ↓
Relative Advantage
          ↓
Evidence
          ↓
Focused Positioning
          ↓
Why Us
```

---

# 15. 次に確認すべきこと

次段階では、Deal Profileの6軸それぞれについて、**当チームの比較優位がどちら側へ寄ると高まるのか**を事実ベースで確認する。

例えば以下を問う。

| Deal Profile軸 | 確認すべき問い |
|---|---|
| Decision Altitude | Executive / Strategy案件とOperational案件のどちらで実績・評価が強いか |
| Problem Novelty | 解法未定の案件をどの程度扱っているか |
| Analytical Complexity | 高難度Prediction / Causal等の実績・人材Evidenceがあるか |
| Standardizability | Standard Solutionとscratchのどちらで価値を出しているか |
| Implementation Coupling | 分析単体からProduction接続までどこで強いか |
| Criticality | 高Security / 高Business Impact案件で何を証拠化できるか |

そして、

> Core Zoneはどこか

を定める。

その際も境界線を固定せず、

- Core
- Adjacent
- Disadvantaged

のGradientとして扱う。

---

# 16. 暫定結論

競争構造を理解する分析単位は、Deal Typeではなく**Deal Profile**とする。

当チームにも競合にも、

> 「できる / できない」

ではなく、

> **「どの商談条件で相対的に選ばれやすくなるか」**

という比較優位のGradientがある。

従って、Focused Positioningとは提供範囲を狭く制限することではなく、

> **比較優位曲面のPeak＝Core Zoneを見つけ、その周辺で最も強いValue PropositionとEvidenceを提示すること**

と定義する。

この考え方により、

```text
全Dealに対応可能
        ≠
全Dealで同じ競争力
```

という現実を明示的に扱うことができる。

Why Usの最終検討では、「我々は何ができるか」ではなく、

> **どのDeal Profileで、なぜ当チームの比較優位が高まり、その優位を何で証明できるか**

を問う。

---

# 17. Evidence / Inferenceの区別

## 17.1. 既存理論・研究に依拠する部分

- BUYGRIDがNew Task / Modified Rebuy / Straight RebuyというBuying Situationを区別すること。
- Organizational buyingが購買状況・組織条件等に依存すること。
- Contingency Theoryが「唯一最善」ではなくContextとのfitを重視する理論群であること。

## 17.2. 本書独自の分析仮説

以下は既存研究の標準モデルではない。

- Deal Profileを6つの連続軸で表現すること。
- Deal ProfileからSelection Criteriaの重みが変化すると考えること。
- Vendorの比較優位をDeal Profile空間上のSurfaceとして捉えること。
- Core / Adjacent / Disadvantaged Zoneを設定すること。
- Focused Positioningを「比較優位曲面のPeakへのマーケティング集中」と定義すること。

これらはWhy Usの競争分析を行うための実務フレームであり、最終的な妥当性は当チームの案件実績・失注理由・顧客評価等によって検証する必要がある。

---

# 18. 参考文献

1. Robinson, P. J., Faris, C. W., & Wind, Y. (1967). *Industrial Buying and Creative Marketing*. Allyn & Bacon.

2. Webster, F. E. Jr., & Wind, Y. (1972). *A General Model for Understanding Organizational Buying Behavior*. Journal of Marketing, 36(2), 12–19.  
   https://doi.org/10.1177/002224297203600204

3. Sheth, J. N. (1973). *A Model of Industrial Buyer Behavior*. Journal of Marketing, 37(4), 50–56.  
   https://doi.org/10.1177/002224297303700408

4. Tosi, H. L., & Slocum, J. W. Jr. (1984). *Contingency Theory: Some Suggested Directions*. Journal of Management, 10(1), 9–26.  
   https://doi.org/10.1177/014920638401000103

5. *B2B customer journeys: Conceptualization and an integrative framework*. Industrial Marketing Management, 113, 74–87 (2023).  
   https://doi.org/10.1016/j.indmarman.2023.05.020
