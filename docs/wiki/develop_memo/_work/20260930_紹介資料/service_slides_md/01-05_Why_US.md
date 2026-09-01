Document title: Why US

# 5. Slide 5｜Why US

## 5.1. Message

**高度な分析とEnterprise利用の両方が重要なPoCで、選ばれる理由をつくる。**

## 5.2. Chart

**チャートタイトル:** Why Usは「得意領域」ではなく、競合との差が生まれる条件で考える

当チームのWhy Usを、単に「当チームが高い能力を発揮できる領域」ではなく、**同じ商談でRelevant Competitorと比較したときに、顧客にとって選択理由が成立する条件**として示す。

現時点では、`Specialist Analytics × Enterprise Base` を有力なCapability構成仮説とする。ただし、この組合せだけで競争優位を断定しない。

### 5.2.1. Chart Structure

PowerPoint上では、左から右へ3段階で示す。

```text
┌─────────────────────────┐
│ ① 当チームのCapability │
│                         │
│ ・Predictive / Causal   │
│ ・Scratch / OSS         │
│ ・前提 / 評価まで設計   │
│ ・Enterprise Fit        │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ ② Deal ProfileとのFit  │
│                         │
│ 高度・非定型な分析      │
│        ×                │
│ Enterprise利用条件      │
│                         │
│ ＝ 当チームのFitが高い  │
└────────────┬────────────┘
             │
             ▼
┌───────────────────────────────┐
│ ③ Relevant Competitorとの比較 │
│                               │
│ 当チームのFit                  │
│        −                      │
│ 最有力競合のFit                │
│        ↓                      │
│ **Competitive Gap**           │
└──────────────┬────────────────┘
               │
               ▼
      **選ばれる理由 / Why Us**
```

右端または下段に、小さく以下の補足を置く。

```text
高いFit ≠ 競争優位
Competitive Gap > 0 をEvidenceで確認する
```

**PowerPoint上の強調**

- `Specialist Analytics × Enterprise Base` は「競争優位」ではなく、**競争優位を生み得るCapability構成仮説**として表示する。
- 最も強く見せるのは `Competitive Gap`。
- 「Sweet Spot」という語は使わない。自社の得意領域と競争優位領域を混同させるため。
- 競合名を本編で直接並べず、詳細はAppendixへ送る。

### 5.2.2. Chart内の最小表示テキスト

**① Capability**

- Predictive / Causal
- Scratch / OSS
- 前提・評価まで設計
- Enterprise Fit

**② Deal Fit**

- 高度・非定型な分析
- Enterprise利用条件
- **当チームのFitが高い**

**③ Competitive Gap**

- 当チームのFit
- − 最有力競合のFit
- **選ばれる理由**

**注記**

- **高いFit ≠ 競争優位**

## 5.3. Supporting Logic

### 5.3.1. Slide 5の役割

- Slide 1〜4では、Predictive / Causalの役割と、分析結果を業務判断へつなげる考え方を説明した。
- Slide 5では「なぜ当チームへ依頼するのか」を扱う。
- ここで、当チームが能力を発揮しやすいDeal Profileと、競合より選ばれやすいDeal Profileを分ける。
- `wk08〜wk10`の検討から、Why UsはOwn Fitではなく、Relevant Competitorとの差分として考える必要がある。

### 5.3.2. 高いOwn FitだけではWhy Usにならない

例えば、あるDealに対して、

```text
当チーム   80
競合A      85
```

であれば、そのDealは当チームの得意領域であっても競争優位領域ではない。

従って、

> 「高度・非定型な分析とEnterprise利用の両方が重要な商談では、当チームのFitが高い」

だけではWhy Usとして不十分である。

必要なのは、

> **同じ商談でRelevant Competitorより高い顧客価値を提供できるか**

である。

### 5.3.3. Competitive Gapの概念

概念的には、Deal `D` に対するVendor `V` の顧客評価を `U(V|D)` とすると、当チームのCompetitive Gapを以下と考える。

```text
Competitive Gap(D)
  = U(Our Team | D)
    - max U(Relevant Competitor | D)
```

この式は実証済みの定量モデルではなく、Why Usを考えるための概念モデルである。

重要なのは、

- Competitive Gap > 0：Right to Win候補
- Competitive Gap ≈ 0：競争可能だが差別化弱い
- Competitive Gap < 0：得意でもWhy Usにはならない

という区別である。

### 5.3.4. `Specialist Analytics × Enterprise Base` の位置づけ

現時点で確認できる当チームのCapability構成から、

> **Specialist Analytics × Enterprise Base**

を有力な仮説とする。

ただしこれは、

> 「競合より優れている」

ことを意味しない。

例えば他SIer Analyticsが同等以上のAnalytical CapabilityとEnterprise Deliveryを持つ場合、Competitive Gapは生まれない。

総合コンサルAnalyticsが高度分析とEnterprise Transformationを同時に提供できる場合も同様である。

したがって、このCapability構成はWhy Usそのものではなく、**Competitive Gapを生み得る起点**として扱う。

### 5.3.5. Competitive Gapが生まれる可能性がある要因

今後確認すべき差分候補は以下である。

- 特定のPredictive / Causal問題への方法論的専門性
- Senior Data ScientistへのDirect Access
- 非定型PoCを小さく開始できるDelivery Model
- Product / Platform非固定での柔軟性
- SIer内部のSystem / Security / Production組織への接続
- 特定業界・課題でのRelevant Evidence
- PoC価格・Lead Time・契約柔軟性
- Analysisから次工程への引継ぎコスト

これらは現時点ではEvidence Gapを含むため、本スライドで競争優位として断定しない。

### 5.3.6. 本スライドで主張できる範囲

現時点で顧客向けに安全に主張できるのは、

> **高度な分析設計とEnterprise利用条件の双方を考慮できるCapability構成を持つこと**

までである。

「競合より選ばれる理由」を最終確定するには、`wk10`で整理するCompetitive Gap仮説を実案件・人材・実績・顧客評価等で検証する必要がある。

## 5.4. Speaker Note

当チームのWhy Usを考えるうえで、重要な区別があります。それは「私たちが得意な領域」と「競合より選ばれる領域」は同じではない、という点です。

例えば、ある高度な分析案件で当チームが十分高い品質を出せたとしても、同じ商談で競合がそれ以上の価値を出せるなら、その案件は当チームの得意領域ではあってもWhy Usにはなりません。

そのため、私たちはまず自分たちのCapabilityを整理し、次に案件とのFitを見ます。ただし、そこで止めずに、同じ商談に参加するRelevant Competitorとの比較まで行います。

当チームはPredictive / Causalの分析、スクラッチとOSSを使った柔軟な実装、分析前提や評価の設計、SIerとしてEnterprise利用を見据える視点を組み合わせています。この構成は、高度な分析とEnterprise利用の両方が重要なPoCで価値を持つ可能性があります。

ただし、それ自体が競争優位だとは考えていません。最終的なWhy Usは、競合との比較で顧客価値の差が生まれ、その差を実績や人材、Delivery Model等のEvidenceで説明できる場合に初めて成立します。

## 5.5. Slide 5からSlide 6への接続

> Why UsはCapabilityの自己評価ではなく、特定の商談で競合との差を生み出せるかで決まる。そのうえで、当チームが提供するPoC自体は何を検証するものなのか。次にPoCの目的を整理する。