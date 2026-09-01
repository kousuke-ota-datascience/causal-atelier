Document title: 競合比較から見た当チームのPositioning

# A01-04. Appendix｜競合比較から見た当チームのPositioning

## A01-04.1. Message

**当チームは、専門的な分析設計とEnterprise対応が同時に求められる領域を主戦場とする。**

## A01-04.2. Chart

**チャートタイトル:** Deal Profile上のPositioning｜Specialist Analytics × Enterprise Base

### A01-04.2.1. Chart Structure

A01-03で示した2軸上に、各Provider類型の「強みが出やすい領域」を重なりのある楕円で配置する。

- 縦軸：Analytical Complexity
- 横軸：Implementation Coupling

```text
                 Analytical Complexity
                        High
                         ▲
                         │
      DS Specialist     │       Consulting Analytics
        ╭──────╮         │          ╭────────╮
       ╱ 高度分析 ╲──────┼────────╱ 高度分析＋変革 ╲
       ╲ 柔軟性  ╱       │        ╲ Stakeholder  ╱
        ╰──────╯         │          ╰────────╯
                         │
                         │        ╭══════════════╮
                         │       ║ **当チーム**   ║
                         │       ║ Specialist   ║
                         │       ║ Analytics    ║
                         │       ║ × Enterprise ║
                         │        ╰══════════════╯
─────────────────────────┼────────────────────────▶
                         │              Implementation Coupling
       AI / Platform     │           SIer Analytics
        ╭──────╮         │          ╭────────╮
       ╱標準化・Scale╲    │         ╱Integration╲
       ╲ Speed      ╱     │         ╲Production ╱
        ╰──────╯         │          ╰────────╯
                         │
                        Low
```

**重要:** 実際のPowerPointでは各Providerを一点ではなく、互いに重なる半透明の楕円で描く。当チーム領域も他社領域と重ねる。

当チーム領域の横に、01-05と同じ3要素を置く。

```text
Predictive / Causal
        ×
Scratch / OSS
        ×
Enterprise Context
```

下部に顧客向けの結論を置く。

> **定型Solutionでは解きにくく、分析だけでも終わらない課題に。**

### A01-04.2.2. Chart内の最小表示テキスト

- DS Specialist：高度分析 / 柔軟性
- Consulting Analytics：高度分析 / Transformation
- SIer Analytics：Integration / Production
- AI Vendor：Standardization / Scale
- **当チーム：Specialist Analytics × Enterprise Base**
- **定型Solutionでは解きにくく、分析だけでも終わらない課題に**

## A01-04.3. Supporting Logic

### A01-04.3.1. このMapが答える顧客の疑問

01-05を見た顧客から、

> 「予測・因果、柔軟な分析、Enterprise利用まで考えるというが、他社も同じことができるのでは？」

という反論が想定される。

回答は、

> **はい、対応Capabilityは重なる。ただし、各Providerが最も強みを出しやすいDeal Profileは同じではない。**

である。

本Mapは「他社にはできない」ことを示すものではなく、**当チームがどの競争領域を主戦場としているか**を示す。

### A01-04.3.2. DS Specialistとの違い

DS Specialist / Research Boutiqueは、Analytical Complexityが高く、Analysis単体でも価値が成立する案件で強みを持ちやすい。

当チームもAnalytical Designを重視する一方、SIer内の分析組織として、Data / System / Security / Operation等のEnterprise条件をPoC段階から考慮できることをPositioning上の違いとする。

従って、Implementation Couplingが高まるほど、当チームのEnterprise Baseが追加価値になり得る。

### A01-04.3.3. SIer Analyticsとの違い

一般的なSIer Analyticsは、Enterprise Integration、Production、Security、Operationとの接続に強みを持ちやすい。

当チームはそこに加えて、Predictive / Causalを問いから使い分け、スクラッチ中心で非定型なAnalysis Designを行う専門組織としてPositioningする。

従って、Analytical Complexity / Problem Noveltyが高まるほど、Specialist Analytics側のCapabilityが追加価値になり得る。

ただし、他SIerにも同等の専門組織は存在し得るため、実案件ではRelevant Competitorの実績・人材との比較が必要である。

### A01-04.3.4. Consulting Analyticsとの違い

Consulting Analyticsは、Decision Altitudeが高く、Strategy / Transformation / Stakeholder Alignmentを含む案件で強みを持ちやすい。

当チームは、全社変革構想そのものより、具体的なPredictive / Causal Questionをデータで検証し、将来利用へ接続するAnalytical PoCを中心にPositioningする。

特に、実際のDataを用いたHands-onなAnalysis Designの比重が高い商談を主戦場とする。

### A01-04.3.5. AI / Platform Vendorとの違い

AI / Platform Vendorは、ProblemがProduct Capabilityへ高くFitし、Standardizabilityが高い場合にSpeed / Reuse / Scaleで強みを持ちやすい。

当チームは、既製Solutionへ問題を合わせにくく、Outcome / Treatment / Evaluation / Data Structure等を個別に設計する必要がある案件を中心にPositioningする。

### A01-04.3.6. 当チームの主戦場

以上から、当チームが強みを訴求するDeal Profileを以下とする。

```text
Problem Novelty           Medium〜High
Analytical Complexity     Medium〜High
Solution Standardizability Low〜Medium
Implementation Coupling   Medium〜High
Criticality / Governance  Medium〜High
```

一言で表すと、

> **定型Solutionでは解きにくく、分析だけでも終わらない課題**

である。

ここでは、

- Specialist Analyticsとしての問い・前提・評価の設計
- Scratch / OSSによる柔軟な分析
- SIerとしてのEnterprise Context

が同時に価値を持ちやすい。

### A01-04.3.7. 01-05との対応

01-05の3つの顧客価値と、本Mapは以下のように対応する。

| 01-05の価値 | Positioning上の意味 |
|---|---|
| 問いに合う分析を選ぶ | Analytical Complexity / Problem Noveltyが高い案件へのFit |
| 非定型課題にも合わせる | Standardizabilityが低い案件へのFit |
| 利用段階まで見据える | Implementation Coupling / Criticalityが高い案件へのFit |

従って、01-05は単なるCapability列挙ではなく、このDeal Profile上のPositioningを顧客向けに圧縮したものとして扱う。

### A01-04.3.8. 主張範囲

- 各Providerの楕円は市場シェアや実測Scoreを示すものではない。
- Provider類型ごとの一般的なBusiness Model / Capability傾向をもとにしたPositioning仮説である。
- 個別競合企業には例外があり、当チームより高いFitを持つ企業も当然存在する。
- したがって営業現場では「他社にはできない」とは言わず、**「当チームはこの組み合わせを主戦場としている」**と説明する。
- 最終的な競争優位の強さは、人材・案件実績・顧客評価等のEvidenceで補強する。

## A01-04.4. Speaker Note

ここまでを一枚にまとめると、このPositioningになります。

確かに各社のCapabilityには重なりがあります。データサイエンス専門会社でもシステム支援はできますし、SIerやコンサルにも高度なデータサイエンティストはいます。ですから、境界線で「ここは当社だけ」とは説明しません。

違いは主戦場です。データサイエンス専門会社は高度分析と柔軟性、SIerはIntegrationやProduction、AI Vendorは標準化とScale、コンサルはTransformationまで含む上位課題に、それぞれ強みを作りやすい構造があります。

当チームが主戦場とするのは、その中でも分析方法自体を設計する必要がありながら、分析だけで完結せず、将来のEnterprise利用も考えなければならない領域です。Predictive / Causalを問いから使い分け、Scratch / OSSで個別に設計し、SIerのEnterprise Contextを同じPoCへ持ち込む。この組み合わせが01-05でお伝えしている強みです。

したがって、「どこも同じでは」という問いに対する回答は、「できることには重なりがあります。ただし、私たちは定型Solutionでは解きにくく、分析だけでも終わらない課題を主戦場として、そこに必要なCapabilityを組み合わせています」となります。

## A01-04.5. Appendix A01-04から本編への接続

> このPositioningを顧客向けに一枚へ圧縮したものが01-05である。予測・因果の専門分析、非定型課題への柔軟な設計、Enterprise利用まで見据えることを一つのPoCで提供する。