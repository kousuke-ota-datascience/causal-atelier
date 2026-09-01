Document title: Why US

# 5. Slide 5｜Why US

## 5.1. Message

**高度・非定型な分析と、Enterprise実装を見据えたPoCを一体で設計する。**

## 5.2. Chart

**チャートタイトル:** 当チームが価値を出しやすい領域｜分析の難しさ × 実装への接続

当チームのWhy Usを、個別Capabilityの羅列ではなく、**どのような商談条件で当チームのCapabilityの組合せが価値を持つか**として示す。

主図は、横軸を「業務・システムへの接続度」、縦軸を「分析設計の難易度」とする2軸マップとする。

当チームのSweet Spotを、**分析設計の難易度が一定以上高く、かつPoC後の業務・システム利用も見据える必要がある領域**として配置する。

### 5.2.1. Chart Structure

PowerPoint上では、中央に2軸マップを大きく配置し、右上寄りに当チームのSweet Spotを示す。

```text
                  分析設計の難易度
                        高
                         ▲
                         │
  高度分析・研究寄り     │      ★ 当チームのSweet Spot
                         │
  ・高度な方法論         │      ・Predictive / Causal
  ・非定型な検証         │      ・スクラッチ＋OSS
                         │      ・前提 / 評価まで設計
                         │      ・業務 / System利用を考慮
                         │
─────────────────────────┼────────────────────────▶
                         │            業務・Systemへの接続度
                         │
  定型分析・Tool活用      │      実装・Integration寄り
                         │
                        低
```

**PowerPoint上の読み順**

1. 縦軸で「分析自体の難しさ」を示す。
2. 横軸で「分析結果を業務・Systemへ接続する必要性」を示す。
3. 右上のSweet Spotを強調する。
4. Sweet Spotの下に、当チームの価値を支える4つのCapabilityを短く置く。

```text
         Specialist Analytics × Enterprise Base

Predictive / Causal ｜ Scratch / OSS ｜ Scientific Validity ｜ Enterprise Fit
```

**視覚上の留意点**

- 他社名を直接配置して「競合より優れている」と断定しない。
- 左上 / 右下等は「専門分析寄り」「実装寄り」の一般的な商談特性として示す。
- Sweet Spotは排他的な対応範囲ではなく、**比較優位が出やすい領域**として表現する。
- 「この領域以外は対応しない」という誤解を避けるため、領域境界は硬いBoxではなくグラデーションで表現する。

### 5.2.2. Chart内の最小表示テキスト

**軸**

- 分析設計の難易度
- 業務・Systemへの接続度

**Sweet Spot**

- **高度・非定型な分析 × Enterprise利用**

**Supporting Capability**

- Predictive / Causal
- Scratch / OSS
- 前提・評価まで設計
- Enterprise Fit

**Bottom Message**

- **Specialist Analytics × Enterprise Base**

## 5.3. Supporting Logic

### 5.3.1. Slide 5の役割

- Slide 1〜4では、当チームがPredictive / CausalのPoCを提供し、問いに応じて分析を使い分け、業務のDecision / Actionへつなげることを説明した。
- Slide 5では、そこから一段進み、**どのような商談で当チームを選ぶ合理性が高まりやすいか**を示す。
- 従来案の「Business-first」「Scientific rigor」「Flexible implementation」は重要だが、高品質なコンサル、SIer Analytics、Data Science専門会社等も実行可能であり、単独ではWhy Usになりにくい。
- そこで、個別能力ではなく**Capabilityの組合せとDeal ProfileとのFit**を差別化仮説の中心に置く。

### 5.3.2. 当チームの強み仮説｜Specialist Analytics × Enterprise Base

現時点で確認できている当チームの特徴は以下である。

- SIerのデータ分析部門である。
- Predictive Analysis / Causal InferenceのPoCを提供する。
- データサイエンティストによるスクラッチ開発を基本とし、必要に応じ成熟OSSを利用する。
- Predictive / Causalを問い・推論対象・前提・評価基準の異なるAnalysis Familyとして扱う。
- CausalではCausal Question / Estimand / Assumptions / Identification / Estimation / Diagnostics等を必要に応じて分けて検討する。
- Predictiveでは未知データ性能、Calibration、Error Pattern、業務上の誤判定等を必要に応じて評価する。
- 特定Product導入をサービスの必須前提としない。
- SIer組織内に位置するため、Enterpriseのデータ・System・Security・Governance・本番利用条件を考慮できる余地がある。

これらを単独で差別化要素とせず、**高度・非定型な分析設計とEnterprise利用条件の双方が重要になるDealで、組合せとして価値を持つ**という仮説を置く。

### 5.3.3. Sweet Spotは排他的なターゲットではない

- 当チームのサービスCoverageを、この2軸の右上だけに限定するものではない。
- 定型的なPrediction PoC、分析単体の案件、System連携が強い案件等にも対応し得る。
- ただし、競争優位はDealごとに一定ではなく、Problem Novelty、Analytical Complexity、Solution Standardizability、Implementation Coupling、Criticality等によって変化する。
- したがって本スライドでは「対応できる / できない」ではなく、**比較優位が相対的に高まりやすい領域**を示す。

### 5.3.4. 競合との差はCapabilityの有無ではなく、DealとのFitで考える

- 総合コンサルAnalyticsも高度分析や本番化支援を行う。
- 他SIer AnalyticsもEnterprise Systemと分析を接続できる。
- Data Science専門会社もスクラッチ分析やCausal Inferenceを提供し得る。
- AI VendorもProduct Fitした問題では、分析から業務Actionまで高い速度で実装し得る。

従って、

> 「他社にはできない」

ではなく、

> **「高度・非定型な分析とEnterprise利用条件の両方が重要な商談では、当チームのCapability構成とのFitが高まりやすい」**

と主張する方が反論耐性が高い。

### 5.3.5. 主張範囲 / Evidence Gap

本スライドは現時点ではPositioning仮説であり、以下は未確認のため断定しない。

- 競合より分析品質が高い
- 競合より価格が安い
- 競合より短納期
- 特定業界で圧倒的な実績がある
- Senior Scientistが常に直接担当する
- PoC本番化率・顧客Repeat率が高い

Why Usを最終確定するには、案件実績、人材、顧客評価、Delivery Model等のEvidenceによる裏付けが必要である。

## 5.4. Speaker Note

当チームの強みを、単に「因果推論ができます」「SIerなので本番化まで考えられます」と説明しても、十分な差別化にはなりません。優秀なコンサル、SIer、データサイエンス専門会社にも同様の能力があります。

そこで、私たちは個々のCapabilityの有無ではなく、どのような案件でその組み合わせが価値を持つかで考えています。

縦軸は分析設計の難易度です。既製の手法をそのまま適用できる案件から、予測・因果の使い分けや前提・評価方法そのものを設計する必要がある非定型案件まであります。

横軸は、分析結果を業務やシステムへどこまで接続する必要があるかです。分析単体で完結する案件もあれば、将来のデータ取得、運用、Security、システム連携まで考慮する案件もあります。

当チームの比較優位が出やすいと考えているのは、この二つが同時に一定以上高い領域です。Predictive / Causalの分析をスクラッチで設計しながら、SIerのデータ分析部門としてEnterpriseで利用する際の現実的な条件も視野に入れてPoCを進めます。

これは、この領域以外を扱わないという意味ではありません。商談にはグラデーションがあり、案件ごとに最適なProviderも変わります。その中で、高度な分析設計とEnterprise利用の双方が重要な課題では、当チームを選ぶ合理性が高まりやすい、というのが現時点でのWhy Us仮説です。

## 5.5. Slide 5からSlide 6への接続

> 当チームの強みは、モデルを作ること自体ではなく、高度な分析を実際の判断・利用へつなぐPoCを設計する点にある。では、そのPoCでは具体的に何を検証するのか。次にPoCの目的を整理する。