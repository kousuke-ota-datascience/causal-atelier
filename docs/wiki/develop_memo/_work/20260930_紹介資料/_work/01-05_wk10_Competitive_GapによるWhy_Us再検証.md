# 01-05 wk10｜Competitive GapによるWhy Us再検証

## 1. 目的

`wk09` では、当チームの有力なPositioning仮説として、

> **Specialist Analytics × Enterprise Base**

を置いた。

また、

> **高度・非定型な分析とEnterprise利用条件の両方が重要な商談で、当チームのCapability構成とのFitが高まりやすい**

という仮説を提示した。

しかし、この整理には重要な反論が残る。

> **当チームがその領域で最も高いFitを出せても、競合がそれ以上のFitを出すならWhy Usにはならない。**

例えば、

```text
当チーム  80
競合A     85
```

であれば、そのDealは当チームの「得意領域」ではあっても「競争優位領域」ではない。

本書では、この問題を解消するため、Why Usを**Own FitではなくCompetitive Gapで再定義**する。

---

# 2. 基本定義

## 2.1. Capability

当チームが持つ能力・Asset・Operating Model。

例：

- Predictive / Causal
- Scratch / OSS
- Scientific Validity
- Enterprise Fit

CapabilityはSupply-sideの事実・特徴である。

---

## 2.2. Own Fit

特定Deal Profileと当チームのCapabilityがどの程度適合するか。

概念的には、

```text
Own Fit = U(Our Team | Deal)
```

である。

Own Fitが高いことは、当チームがその案件に向いていることを意味する。

しかし競争優位を意味しない。

---

## 2.3. Competitor Fit

同じDealに参加するRelevant Competitorが、顧客Selection Criteriaに対してどの程度適合するか。

```text
Competitor Fit = U(Competitor | Deal)
```

Relevant CompetitorはDealごとに異なる。

例えば、

- Corporate Strategy寄り → Consulting Analytics
- Analytical PoC → Consulting Analytics / SIer Analytics / DS専門会社
- Productized AI → AI Vendor
- Production / Integration → SIer Analytics

等が中心になり得る。

---

## 2.4. Competitive Gap

当チームのWhy Usで最も重要なのは以下である。

```text
Competitive Gap(D)
  = U(Our Team | D)
    - max U(Relevant Competitor | D)
```

この式は実証済みの定量モデルではなく、競争分析の概念モデルである。

### 解釈

| Competitive Gap | 意味 |
|---|---|
| `> 0` | Right to Win候補 |
| `≈ 0` | 競争可能だが差別化弱い |
| `< 0` | 当チームが得意でもWhy Usにはならない |

---

# 3. Why Us探索の問いを変更する

## 3.1. 従来の問い

> 当チームはどのDeal Profileで最も強いか？

これはOwn Peakを探している。

```text
Own Fit
  ▲
  │        ★ Own Peak
  │       / \
  │      /   \
  └────────────────▶ Deal Profile
```

しかしOwn Peakが競合より高いとは限らない。

---

## 3.2. 修正後の問い

> **Relevant Competitorとの差が最も大きくなるDeal Profileはどこか？**

探すべきは、

> **Maximum Competitive Gap**

である。

```text
Competitive Gap
  ▲
  │             ★ Right-to-Win Zone
  │           /   \
  │──────────/─────\────────── 0
  │        /         \
  └───────────────────────────▶ Deal Profile
```

したがって、

> **Sweet Spot ≠ Right-to-Win Zone**

である。

---

# 4. `Specialist Analytics × Enterprise Base` 仮説を反証する

## 4.1. 仮説

当チームは、

- 高度・非定型な分析設計
- Predictive / Causal
- Product非固定のScratch / OSS
- Enterprise利用条件を考慮したPoC

を組み合わせられる。

そのため、

> **Analytical ComplexityとImplementation Couplingが共に高いDeal**

でCompetitive Gapが正になる可能性がある。

しかし、以下の競合反論を突破しなければならない。

---

# 5. 競合別の反証

## 5.1. Consulting Analyticsからの反論

### 反論

> 「高度分析もEnterprise Transformationも当社で提供できる。経営・業務・Technologyを一体で支援でき、実績・ブランド・Stakeholder Managementも強い。なぜ当チームを選ぶのか。」

### 当チーム側の仮説差分候補

以下が事実ならCompetitive Gapが生まれる可能性がある。

- Smaller PoCをより機動的に開始できる
- Senior Data Scientistがhands-onで分析実装まで担当する
- Strategy / PMO overheadが小さい
- Predictive / Causalのmethodological depthが対象Dealで高い
- Product / Solution売上に引っ張られず分析方法を選択できる
- SIer内部のSystem組織へ直接接続できる

### 現時点の評価

**Competitive Gap：Unknown**

理由：

- 当チームのPrice / Lead Time / Staffing Model不明
- Consulting Analytics各社も高度なData Scientistを持つ
- 経営・Transformation寄りでは明確に不利になる可能性がある

したがって、Consulting Analyticsに対するRight to Winを現時点で断定できない。

---

## 5.2. 他SIer Analyticsからの反論

### 反論

> 「SIer基盤も高度分析部門も当社にある。Enterprise Delivery・Security・本番化もできる。御社固有の差は何か。」

### 当チーム側の仮説差分候補

- Causal Inferenceを明確なService Capabilityとして持つ
- Predictive / Causalを問い・前提・評価まで分離して扱う
- 特定Platformに寄らずScratch / OSS中心でPoCを設計する
- Methodological rigorをPoCの中心に置く
- PoC段階でSenior Analystが直接設計する
- Ariadne等によるAnalysis Context / Lineage / Rationaleの構造化

### 現時点の評価

**Competitive Gap：最も厳しい / Unknown〜Low仮説**

理由：

- SIer共通のEnterprise Fitは差別化にならない
- 高度Analytics / Causalを持つSIerも存在する
- 当チーム固有の実績・人材・Delivery Modelが確認できていない

ここを突破できなければ、`Specialist Analytics × Enterprise Base` は「自社類型の特徴」に留まり、Why Usにはならない。

---

## 5.3. Data Science専門会社からの反論

### 反論

> 「非定型分析・Scratch・Causal・専門人材は当社の本業である。分析深度ではむしろ専門会社の方が高いのではないか。」

### 当チーム側の仮説差分候補

- Enterprise System / Security / Governanceとの接続
- PoC後のSystemizationへ同一企業グループで接続可能
- 顧客の既存IT環境・Vendor管理との整合
- 大規模企業でのProcurement / Organizational Acceptability
- 分析から本番移行時のTransaction Cost低減

### 現時点の評価

**Competitive Gap：Medium候補だが未証明**

この比較では`Enterprise Base`が差分になり得る。

ただし、DS専門会社側もSystem Integration capabilityを持つケースがあり、一律には成立しない。

また、当チームのAnalytical Depthが同等以上であるEvidenceが必要。

---

## 5.4. AI Vendorからの反論

### 反論

> 「当社ProductがFitするなら、より速く・安く・安定的に導入できる。なぜScratch PoCが必要なのか。」

### 当チーム側の仮説差分候補

- ProblemがProduct capabilityに十分Fitしない
- Outcome / Treatment / evaluationが顧客固有
- 方法論自体を検証する必要がある
- Product選定前にAnswerabilityを確認したい
- Vendor Lock-inを避けたい

### 現時点の評価

**Competitive Gap：非定型Dealでは比較的説明しやすい**

ただし、Product Fitが高いDealではCompetitive Gapは負になる可能性が高い。

したがって、AI Vendorに対する比較優位はDeal Profile依存性が非常に大きい。

---

# 6. 現時点で最も可能性のあるCompetitive Gap構造

単独Capabilityで勝つより、**競合のTrade-offの間に入るConfiguration Advantage**の可能性を見る。

仮説例：

| Provider類型 | 強みが出やすい側 | Trade-off仮説 |
|---|---|---|
| Consulting Analytics | Strategy / Governance / Credibility | 小規模PoCのEconomics / hands-on比率が不利な可能性 |
| SIer Analytics | Enterprise Delivery / Risk | 非定型Methodologyへの集中度は部門差が大きい |
| DS専門会社 | Analytical Depth / Flexibility | Enterprise Delivery / Org Acceptabilityが相対的に弱い場合がある |
| AI Vendor | Product Fit / Speed / Scale | 非定型問題・Product外への柔軟性が低下 |
| 当チーム | Analytical Flexibility + Enterprise Base | 両者を高い水準で両立できるかが検証課題 |

重要なのは、上記Trade-offを一般論として断定しないこと。

Competitive Gapが成立するためには、当チームが実際に、

- 十分なAnalytical Depth
- 十分なEnterprise Fit
- 過大でないCost / Lead Time

を同時に提供できる必要がある。

---

# 7. Configuration Advantage仮説

単一能力で最高点を取らなくても、顧客のCriterion Weightとの組合せで総合優位が生まれる可能性がある。

例：

| Provider | Analytical | Enterprise | Price | Speed |
|---|---:|---:|---:|---:|
| DS専門会社 | 95 | 55 | 75 | 80 |
| 大手SIer | 65 | 95 | 55 | 55 |
| Consulting | 85 | 80 | 45 | 60 |
| **当チーム** | **85** | **85** | **75** | **75** |

※数値は説明用の仮例であり実測値ではない。

Deal側で、

- Analytical Capability：High weight
- Enterprise Fit：High weight
- Price：Medium weight
- Speed：Medium weight

であれば、当チームが各軸で最高点でなくても、総合Utilityで勝つ可能性がある。

したがって、`Specialist Analytics × Enterprise Base`を成立させるには、

> **二つの能力を持っていること**

ではなく、

> **競合が同時に満たしにくいSelection Criteriaの組合せを、顧客にとって十分高い水準で同時に満たせること**

を示す必要がある。

---

# 8. Right-to-Win Zoneの暫定仮説

現時点で最も可能性があるのは、以下のDeal Profileである。

```text
Problem Novelty           Medium〜High
Analytical Complexity     Medium〜High
Solution Standardizability Low〜Medium
Implementation Coupling   Medium〜High
Criticality / Governance  Medium〜High
Decision Altitude         Operational〜Business
```

ただし、これをRight-to-Win Zoneと断定するには早い。

必要条件は、

1. 当チームのOwn Fitが高い
2. Relevant CompetitorのFitより高い
3. その差が顧客に重要なSelection Criteriaで生じている
4. Evidenceで証明できる

ことである。

---

# 9. 何をEvidenceとして確認すべきか

## 9.1. Competitive Win / Loss Evidence

最重要。

- 競合あり商談で勝った案件
- 競合あり商談で負けた案件
- 顧客が当チームを選んだ理由
- 顧客が他社を選んだ理由
- 比較対象Vendor

これによりCompetitive Gapを最も直接確認できる。

---

## 9.2. Capability Evidence

- Predictive / Causal案件実績
- 非定型問題の案件例
- Seniority
- Publication / Patent / OSS
- Methodological specialty

---

## 9.3. Delivery Configuration Evidence

- PoC team size
- Senior / Junior構成
- 誰がcodingするか
- 顧客との直接対話者
- SI / Security部門との連携方法
- AnalysisからProductionへの引継ぎ方法

---

## 9.4. Economic Evidence

- Price
- Lead Time
- PoC期間
- Change Request柔軟性
- Systemization時の追加Cost

---

## 9.5. Customer Signal

- Repeat
- Reference
- Recommendation
- 顧客評価
- 「なぜ選んだか」Interview

---

# 10. 01-05への反映方針

`01-05`では、従来の、

> **当チームが価値を出しやすいSweet Spot**

という表現を撤回する。

代わりに、

> **Why Usは、当チームのFitではなくRelevant Competitorとの差＝Competitive Gapで考える**

ことを主図とする。

`Specialist Analytics × Enterprise Base`は、

- Why Us

ではなく、

- **Why Usを生み得るCapability Configuration仮説**

として位置づける。

これにより、

> 「当チーム80点、競合85点では？」

という反論に対して、

> **その場合はWhy Usではない。競争優位仮説を棄却する。**

と明確に答えられる。

---

# 11. 暫定結論

現時点の最重要な修正は以下である。

```text
誤：
当チームのCapability
      ↓
Own Fitが高いDeal
      ↓
Why Us

正：
当チームのCapability
      ↓
Deal Profile
      ↓
Customer Selection Criteria
      ↓
Own Fit
      ↕ 比較
Relevant Competitor Fit
      ↓
Competitive Gap
      ↓
Evidence
      ↓
Why Us / Right to Win
```

したがって、現時点の`Specialist Analytics × Enterprise Base`は有望な仮説だが、競争優位としては未証明である。

今後のWhy Us確定では、

> **「どこで当チームが最も高得点か」ではなく、「どこで競合との差分が最大になるか」**

を探索する。

そして差分が存在しない場合には、仮説を維持するのではなく、Why Usを再探索する。
