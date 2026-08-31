# 01-05 wk09｜当チームの強みとWhy Us仮説

## 1. 目的

本書は、`wk01`〜`wk08`までの競合差別化検討を踏まえ、現時点で考え得る**当チームの強みとWhy Usを、一度仮説として明示する**ことを目的とする。

ここで重要なのは、以下を分けることである。

- **Strength / Capability**：当チームが持つ能力・Asset・Operating Model
- **Comparative Advantage**：特定のDeal Profileにおいて、他の選択肢よりその強みの価値が高まる状態
- **Why Us**：顧客から見て「この商談では当チームを選ぶ合理性がある」と説明できる理由

したがって、本書では、

> 「当チームにしかできないことは何か」

を無理に探さない。

代わりに、

> **どのような商談特性の組み合わせで、当チームのCapabilityの組み合わせが相対的に効きやすいか**

を考える。

なお、本書は**仮説整理**である。案件実績、人材構成、価格、生産性、顧客評価等について、現時点で確認できていない事項は競争優位として断定しない。

---

# 2. ここまでに確認できている当チームの事実

本資料および関連資料から、少なくとも以下は確認できている。

1. **SIerのデータ分析部門である。**
2. **Predictive AnalysisとCausal InferenceのPoCを提供する。**
3. 分析実装は**データサイエンティストによるスクラッチ開発を基本**とする。
4. 必要に応じて成熟したOSS / Libraryを利用する。
5. 特定AI Productの導入をサービス提供の必須前提としていない。
6. PredictiveとCausalを、単なるAlgorithm差ではなく、**問い・推論対象・前提・評価基準の異なるAnalysis Family**として扱う。
7. Causalでは、必要に応じてCausal Question / Estimand / Assumptions / Identification / Estimation / Diagnostics / Sensitivityを分離して考える。
8. Predictiveでは、未知データ性能、Calibration、Error Pattern、業務上の誤判定等を含め、単一Accuracyだけで評価しない設計思想を持つ。
9. Ariadneは必須Productではなく、問い・条件・実行・結果・判断理由等のTraceability / Reproducibilityを補助する選択肢として位置づけている。
10. PoCをAnalysis Outputだけで終わらせず、Business Question / Decision / Actionとの接続を重視する。

ただし、10は高品質な競合も実施するため、**それ自体を差別化要因とはみなさない**。

---

# 3. 最有力仮説｜「専門ブティック的な分析深度 × SIer基盤」

現時点で最も有力な強み仮説は、単一Capabilityではなく以下の**組み合わせ**である。

> **高度・非定型な分析をスクラッチで設計できる専門性と、Enterprise Systemを前提としたSIerのDelivery基盤を同時に利用できる。**

より短く言えば、

> **Specialist Analytics × Enterprise Base**

である。

これは、

- 「因果推論ができる」
- 「SIerなので本番化できる」
- 「業務課題から考える」

という個別主張とは異なる。

いずれも他社に実行可能である。

仮説として重要なのは、**これらの組合せが特定のDeal Profileで顧客価値を持つ**ことである。

---

# 4. 当チームの比較優位が高まりやすいDeal Profile仮説

`wk08`では、Dealを以下の6軸の連続Profileとして整理した。

1. Decision Altitude
2. Problem Novelty
3. Analytical Complexity
4. Solution Standardizability
5. Implementation Coupling
6. Criticality / Governance

当チームの比較優位が最も出やすい領域を、現時点では以下のように仮説化する。

| Deal Profile軸 | 比較優位が出やすい方向の仮説 | 理由 |
|---|---|---|
| Decision Altitude | **Operational〜Business / Management** | 純粋な全社戦略より、具体的な意思決定と分析を接続する商談との適合が高いと考えられる |
| Problem Novelty | **Medium〜High** | 解き方が完全に定型化されていないほど、スクラッチ分析・問題設定能力の価値が上がる |
| Analytical Complexity | **Medium〜High** | Predictive / Causalを使い分け、前提・評価まで設計する能力が価値化しやすい |
| Solution Standardizability | **Low〜Medium** | 既製Productだけでは解きにくい問題ほど、Technology-neutralなスクラッチ設計が効く |
| Implementation Coupling | **Medium〜High** | 分析単体より、将来の業務・システム利用条件を考慮する必要があるほどSIer基盤が効く |
| Criticality / Governance | **Medium〜High** | Enterprise顧客でSecurity / Governance / Organizational Acceptabilityが必要になるほどSIerとしての基盤が補完要素になる |

概念的には以下である。

```text
比較優位が出やすい仮説領域

Problem Novelty            Medium ───────── High
Analytical Complexity      Medium ───────── High
Standardizability          Low    ─────── Medium
Implementation Coupling    Medium ───────── High
Criticality / Governance   Medium ───────── High

            ↓

「定型Solutionでは解きにくいが、
 分析だけの研究でもなく、
 将来の業務・システム利用まで考える必要がある問題」
```

この領域を現時点での**Core Zone仮説**とする。

---

# 5. Strength Hypothesis 1｜非定型問題に対するAnalytical Design能力

## 仮説

> **既製Solutionや単一Algorithmへ課題を当てはめず、問いに応じて分析問題そのものを設計できる。**

当チームはPredictive / Causalを別の問いとして扱い、必要な前提・評価を分ける設計思想を持つ。

したがって、

- 何を予測すべきか
- 何を介入効果として知りたいか
- そもそもPredictionとCausalのどちらが必要か
- 既存データで何が検証可能か
- どの評価基準を使うべきか

が最初から確定していない商談において、価値が高まりやすい。

## 強みが出にくい領域

- 既製Productで十分解ける
- 手法・評価方法が完全に定型化されている
- 単純な追加導入 / Straight Rebuyに近い

この場合はProduct Vendorや定型DeliveryのEconomics / Speedが優位になり得る。

## 差別化強度

**Medium〜High仮説**

単独ではDS専門会社やコンサルAnalyticsにも可能であるため、後述するSIer基盤との組合せが重要。

---

# 6. Strength Hypothesis 2｜PredictiveとCausalを「Decision Problemの選択肢」として持つ

## 仮説

> **「AI / MLを使う」ことを前提にせず、何を知りたいかに応じてPredictionとCausal Effectを区別して設計できる。**

具体的には、

```text
何が起こりそうか？
    ↓
Predictive

何をするとどう変わるか？
    ↓
Causal
```

を明示的に分ける。

これは、

- 離脱しそうな顧客を知る
- 誰に施策を打てば離脱を減らせるか知る

を混同しない、という実務価値を持つ。

## 差別化強度

**Medium仮説**

因果推論を扱う競合は多数存在するため、単に「因果推論ができます」では弱い。

強みになる可能性があるのは、

> **Prediction / Causalのどちらかを売るのではなく、Decision Problemに対して必要なEvidenceの種類を選べること**

である。

ただし、これも高品質な競合は実施可能であり、Primary Why UsよりSupporting Capabilityに近い。

---

# 7. Strength Hypothesis 3｜Technology / Product非固定のスクラッチ分析

## 仮説

> **Product capabilityに課題を合わせるのではなく、課題に必要な分析をスクラッチ＋成熟OSSで構成できる。**

これは特に、Solution Standardizabilityが低いDealで価値が上がる。

顧客価値としては、

- 特殊なOutcome
- 複雑なTreatment
- 顧客固有の評価指標
- 特殊なデータ構造
- 業務Costを考慮したOptimization

等に対応しやすい。

## 差別化強度

**Medium仮説**

DS専門会社やコンサルAnalyticsも同様の提供が可能であるため単独差別化には弱い。

一方、AI Product Vendorとの比較では、非定型問題で明確なPositioning差になり得る。

---

# 8. Strength Hypothesis 4｜SIer基盤によるEnterprise Fit

## 仮説

> **分析だけで閉じず、Enterprise顧客のデータ・Security・System・Governance・本番利用を意識したPoC設計が可能である。**

これはSIerのデータ分析部門であることから生じ得る強みである。

顧客Selection Criteriaで言えば、

- Delivery Feasibility
- Risk
- Organizational Acceptability

を補強する可能性がある。

## 差別化強度

**Low as standalone / High as combination仮説**

他のSIer Analyticsに対しては全く差別化にならない可能性が高い。

一方、

> **Specialist Analytics × Enterprise Base**

としてDS専門会社・小規模専門Boutiqueと比較する場合には価値を持つ可能性がある。

---

# 9. Strength Hypothesis 5｜「分析品質」と「Enterprise Fit」を同じPoC内で両立する

ここまでのStrength 1〜4をまとめると、本質的な強み仮説は以下となる。

> **分析専門性だけでも、SIerの実装力だけでもなく、その中間で両方を必要とする商談に強い。**

これはCapabilityの足し算ではなく、Deal ProfileとのInteractionとして考える。

```text
                 Analytical Complexity
                        High
                         ▲
                         │
      DS Specialist     │   ★ 当チーム仮説Core Zone
                         │     Specialist Analytics
                         │          ×
                         │     Enterprise Fit
                         │
─────────────────────────┼──────────────▶ Implementation Coupling
                         │                 High
                         │
       Commodity /       │          SIer Build / Production
       Standard Tool     │
                         │
                        Low
```

※図は概念図であり、各競合を固定的に配置するものではない。

### 比較優位の仮説

- **分析難易度が高いが、Enterprise実装との接続が弱い** → DS専門会社・Research Boutiqueも強い
- **分析難易度は低いが、System Integrationが重い** → 一般SIer Deliveryが強い
- **分析難易度とImplementation Couplingの両方が高い** → 当チームの組合せ価値が出やすい可能性

この「交差領域」が最も有望な差別化仮説である。

---

# 10. Why Us仮説｜顧客から見た選択理由

Strengthは内部Capabilityであり、そのままWhy Usではない。

顧客向けには、以下のように翻訳する必要がある。

## Why Us仮説A｜第一候補

> **定型解のない分析課題に、専門的な分析設計とEnterpriseの実装視点を一つのPoCで持ち込む。**

### 伝えたいこと

- 高度分析だけの会社ではない。
- System Integrationだけの会社でもない。
- 両方が必要になる商談で価値を出す。

### 評価

**現時点の第一候補。**

ただし「専門的」がEvidenceで裏付けられる必要がある。

---

## Why Us仮説B｜顧客ベネフィット寄り

> **既製AIでは解きにくい業務課題を、予測・因果の分析から本番利用条件まで一貫して検証する。**

### 長所

- 何が違うかが比較的具体的。
- Predictive / Causalというサービス内容が見える。
- SIerであることを「本番利用条件」へ翻訳している。

### 留保

「一貫して」が競合も使う一般表現であるため、Supporting Evidenceが必要。

---

## Why Us仮説C｜Positioningを明確にする案

> **分析専門会社の深さと、SIerの実装現実性を一つのPoCで両立する。**

### 長所

- 競争ポジションが非常に明確。
- `Specialist Analytics × Enterprise Base`を最も直接表現する。

### 留保

- 「分析専門会社の深さ」が実績・人材で証明できない場合は過剰主張になる。
- 顧客向けスライドで競合類型を直接意識させる表現が適切かは別途検討が必要。

内部Positioning Statementとしては有力。

---

## Why Us仮説D｜Scientific / Business寄り

> **分析手法を適用するだけでなく、業務判断に必要なEvidenceと本番で成立する条件を同時に検証する。**

### 長所

- 現行Slide 5との連続性が高い。
- 科学的妥当性とEnterprise Fitの両方を表現できる。

### 留保

- コンサル / SIer Analyticsも主張可能。
- Primary DifferentiatorというよりService Philosophyに近い。

---

# 11. 現時点でのWhy Us推奨構造

Slide 5を今後修正する場合、現時点では「3つの独立した強み」を横並びにするより、以下の構造がよいと考える。

```text
               Core Positioning

     非定型・高難度の分析課題
                  ×
      Enterpriseで使う現実性
                  │
                  ▼
       ┌──────────────────┐
       │ 当チームのSweet Spot │
       └──────────────────┘
                  │
       ┌──────────┼──────────┐
       ▼          ▼          ▼
  Predictive /   Scratch /   SIer Base
    Causal          OSS      / Delivery
  Methodology     Flexibility  Context
```

つまり、

- Predictive / Causal
- Scientific rigor
- Scratch / OSS
- Enterprise system understanding

をそれぞれ差別化要素として売るのではなく、**Core Positioningを成立させるSupporting Capability**として配置する。

---

# 12. 当チームが相対的に選ばれにくい可能性があるDeal Profile

Why Usを明確にするには、強みだけでなく、相対優位が薄くなる領域も認識する必要がある。

## 12.1. Corporate Strategy極端側

```text
Decision Altitude       Very High
Analytical Complexity   Low〜Medium
```

- 全社Strategy
- Operating Model
- M&A / Portfolio
- 大規模Transformation構想

等が主論点なら、総合コンサルの比較優位が高い可能性がある。

## 12.2. Standardized / Commodity側

```text
Problem Novelty         Low
Standardizability       Very High
```

既製AI Productで十分な場合、Product VendorのSpeed / Economicsが優位になり得る。

## 12.3. Pure System Integration側

```text
Analytical Complexity   Low
Implementation Coupling Very High
```

分析の不確実性が低く、主課題が本番構築・移行・運用である場合、通常のSIer Delivery部門の方が適切な場合がある。

## 12.4. Pure Research側

```text
Analytical Complexity   Extreme
Implementation Coupling Low
```

理論研究や新規Method開発自体が目的なら、大学・研究機関・特化Research Boutiqueが適する場合がある。

これは「対応しない」という意味ではない。

> **Service CoverageとComparative Advantageは異なる。**

という`wk08`の整理に従う。

---

# 13. Evidence Gap｜Why Usを事実へ昇格させるために必要な確認

現時点で最も不足しているのは、Capabilityの説明ではなく**Signals of Excellence**である。

`wk04`で参照したprofessional servicesのex ante quality研究では、顧客は購入前に品質を直接観察できないため、Quality Signalを用いてProviderをScreeningする。Pemer & Skjølsvik (2019)はQualifying SignalsとSignals of Excellenceを区別している。

Why Usを仮説から顧客向け主張へ昇格させるには、少なくとも以下を確認する必要がある。

### 13.1. 人材Evidence

- Predictive / Causalの専門人材数
- Seniority
- 論文 / 学会 / 特許 / OSS
- 高難度分析の実務経験

### 13.2. 案件Evidence

- Predictive案件数
- Causal案件数
- 非定型分析案件数
- 本番化につながったPoC
- 分析結果によって施策 / 投資判断が変わった事例

### 13.3. Delivery Model Evidence

- 誰が顧客とBusiness Questionを議論するか
- その人物が実際の分析・Codingにも関与するか
- Analysis → System Designへの引継ぎ方法
- SIer内他部門との連携実績

### 13.4. Customer Evidence

- Repeat率
- 顧客評価
- 「なぜ当チームを選んだか」のVoice of Customer
- 競合比較で勝った理由

### 13.5. Economics Evidence

- PoC期間
- Price
- Lead time
- Productivity

現時点ではこれらが不明なため、Speed / Cost AdvantageはWhy Us候補に含めない。

---

# 14. 暫定Tier

## Tier S｜Why Usの核候補

### S1｜Specialist Analytics × Enterprise Base

> **非定型・高難度の分析とEnterprise利用条件の両方が重要な商談で、専門性とSIer基盤の組合せが価値になる。**

これは現時点で最も有力なPositioning仮説。

---

## Tier A｜S1を成立させるCapability

### A1｜Predictive / Causalを問いから使い分ける

### A2｜スクラッチ＋OSSによるTechnology-neutralなAnalytical Design

### A3｜分析の前提・評価・Limitationまで扱うScientific rigor

### A4｜Enterprise環境・本番利用を意識したDelivery context

これらは単独では差別化が弱いが、S1の裏付けとなる。

---

## Tier B｜Table Stakes / Service Philosophy

- Business-first
- Decision / Actionへの接続
- Go / No-Go
- DGPを理解する
- 「分析できた」で終わらない

高品質な競合も実施可能であり、Primary Why Usにはしない。

---

# 15. 暫定結論

現時点で当チームのWhy Usを一文で仮説化するなら、第一候補は以下である。

> **定型解のない分析課題に、専門的な分析設計とEnterpriseの実装視点を一つのPoCで持ち込む。**

これを競争戦略上の内部表現へ変換すると、

> **Specialist Analytics × Enterprise Base**

である。

このPositioningの意味は、

> 「他社には因果推論ができない」
>
> 「他社にはシステムが分からない」

ではない。

むしろ、

> **Problem Novelty / Analytical Complexity / Implementation Coupling / Criticalityが同時に一定以上高いDeal Profileで、当チームの複数Capabilityの組合せが相対的に価値化しやすい**

という仮説である。

したがってWhy Usは、Capabilitiesの羅列ではなく、

```text
どの商談特性で
        ↓
当チームのCapabilityの組合せが効き
        ↓
顧客のどのSelection Criteriaを満たし
        ↓
何のEvidenceでそれを証明するか
```

まで設計する必要がある。

次の検討では、S1仮説を崩すために、

- 総合コンサルAnalytics
- 他SIer Analytics
- Data Science専門会社

それぞれの立場から反論を当てるとともに、当チームの実績・人材・Delivery Modelを棚卸しし、**仮説を証明できるEvidenceが存在するか**を確認するのがよい。

---

# 16. 理論的背景 / 参考文献

本書の「Deal Profileによって比較優位が変わる」というモデル自体は既存理論の標準モデルではなく、`wk04`〜`wk08`で整理した理論を競争分析へ応用した実務仮説である。

主な理論的背景は以下。

1. Webster, F. E. Jr., & Wind, Y. (1972). *A General Model for Understanding Organizational Buying Behavior*. Journal of Marketing, 36(2), 12–19.  
   https://doi.org/10.1177/002224297203600204

2. Robinson, P. J., Faris, C. W., & Wind, Y. (1967). *Industrial Buying and Creative Marketing*. Allyn & Bacon.

3. Sheth, J. N. (1973). *A Model of Industrial Buyer Behavior*. Journal of Marketing, 37(4), 50–56.  
   https://doi.org/10.1177/002224297303700408

4. Pemer, F., & Skjølsvik, T. (2019). *The cues that matter: Screening for quality signals in the ex ante phase of buying professional services*. Journal of Business Research, 98.  
   https://doi.org/10.1016/j.jbusres.2019.02.005

5. Tosi, H. L., & Slocum, J. W. Jr. (1984). *Contingency Theory: Some Suggested Directions*. Journal of Management, 10(1), 9–26.  
   https://doi.org/10.1177/014920638401000103

※上記理論は「Specialist Analytics × Enterprise Base」が競争優位になることを直接証明するものではない。その結論は、本資料内のサービス事実とDeal Profile分析を組み合わせた**仮説**である。
