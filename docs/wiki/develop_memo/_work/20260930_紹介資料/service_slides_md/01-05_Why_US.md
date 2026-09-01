Document title: Why US

# 5. Slide 5｜Why US

## 5.1. Message

**予測・因果の高度分析を、Enterprise利用まで見据えて柔軟に設計する。**

## 5.2. Chart

**チャートタイトル:** 分析専門性と実装現実性を、一つのPoCに

当チームの強みを、顧客が発注判断に使える3つの価値として示す。

```text
┌────────────────────┬────────────────────┬────────────────────┐
│ ① 問いに合う分析を選ぶ │ ② 非定型課題にも合わせる │ ③ 利用段階まで見据える   │
├────────────────────┼────────────────────┼────────────────────┤
│ Predictive / Causal │ Scratch + OSS      │ Enterprise Context │
│                     │                    │                    │
│ 何を知りたいかから   │ 製品や単一手法に     │ Data / System /     │
│ 分析を設計           │ 課題を合わせない     │ Security / Operation│
└──────────┬─────────┴──────────┬─────────┴──────────┬─────────┘
           │                    │                    │
           └────────────────────┼────────────────────┘
                                ▼
              **Specialist Analytics × Enterprise Base**
                                ▼
       **難しい分析課題を、実際に使えるPoCとして検証**
```

### 5.2.1. Chart Structure

PowerPoint上では、横3列のValue Propositionとして構成する。

1. **問いに合う分析を選ぶ**
   - Predictive / Causalを、使いたい技術ではなく顧客の問いから使い分ける。
2. **非定型課題にも合わせる**
   - スクラッチ開発と成熟OSSを用い、特定Productや単一Algorithmの制約に課題を合わせない。
3. **利用段階まで見据える**
   - SIerのデータ分析部門として、Data / System / Security / Operation等のEnterprise利用条件を早期から考慮する。

3つの下に `Specialist Analytics × Enterprise Base` を共通バーとして置き、その下に顧客便益として

> **難しい分析課題を、実際に使えるPoCとして検証**

を配置する。

**視覚上の強調**

- 3カードの中央見出しはCapability名ではなく、顧客が得る価値を動詞で表す。
- `Competitive Gap`、`Own Fit`、`Evidence Gap`等の内部検討用語は表示しない。
- Deal Profileの制約は図上の注釈として前面に出さず、Supporting Logic / Speaker Noteで「特に価値が出やすい条件」として説明する。
- 「対応可能範囲を限定する」印象は与えない。

### 5.2.2. Chart内の最小表示テキスト

**① 問いに合う分析を選ぶ**

- Predictive / Causal
- **何を知りたいかから設計**

**② 非定型課題にも合わせる**

- Scratch + OSS
- **課題に合わせて柔軟に構成**

**③ 利用段階まで見据える**

- Enterprise Context
- **Data / System / Securityまで考慮**

**共通**

- **Specialist Analytics × Enterprise Base**
- **難しい分析課題を、実際に使えるPoCとして検証**

## 5.3. Supporting Logic

### 5.3.1. Slide 5の役割

- Slide 1〜4では、Predictive / Causalがそれぞれどのような問いに答え、どのようなDecision / Actionへつながるかを説明した。
- Slide 5では、顧客に対して**当チームへ発注することで何が得られるか**を示す。
- 内部の競争分析では、Why UsはRelevant Competitorとの差分で成立するという前提を保持する。
- ただし顧客向けスライドでは、その検討プロセスを見せるのではなく、当チームが提供する具体的な価値を簡潔に提示する。

### 5.3.2. ① 問いに合う分析を選ぶ

- 当チームはPredictive AnalysisとCausal Inferenceの双方をPoC対象としている。
- 「AIを使いたい」「機械学習を使いたい」から始めるのではなく、顧客が何を知り、何を判断したいかからAnalysis Questionを定義する。
- 「何が起こりそうか」を知るPredictionと、「何をするとどう変わるか」を知るCausalを混同しない。
- Causalでは必要に応じてCausal Question / Estimand / Assumptions / Identification / Estimation / Diagnostics / Sensitivityを分けて検討する。
- Predictiveでは未知データ性能、Calibration、Error Pattern、業務上の誤判定コスト等を必要に応じて確認する。

**顧客価値:**

> 問いに対して不適切な分析を適用するリスクを下げ、PoC終了時に「何が分かったか」を明確にしやすい。

### 5.3.3. ② 非定型課題にも合わせる

- 分析実装はデータサイエンティストによるスクラッチ開発を基本とし、必要に応じて成熟OSS / Libraryを組み合わせる。
- 特定Productや単一Algorithmへの適合を前提としない。
- Outcome、Treatment、評価指標、データ構造、業務制約等が案件固有であっても、PoCで検証すべき問いに合わせて分析を構成する。

**顧客価値:**

> 既製Solutionの対応範囲に合わせて問いを狭めるのではなく、顧客固有の課題を検証対象として扱いやすい。

### 5.3.4. ③ 利用段階まで見据える

- 当チームはSIerのデータ分析部門としてサービスを提供する。
- 分析精度やEffect Estimateだけでなく、将来的なData acquisition、System integration、Security、Operation、Governance等の制約を必要に応じてPoC段階から考慮する。
- PoCの時点で本番構築を約束するという意味ではなく、PoCの結果が次工程へ接続可能かを判断しやすい設計を目指す。

**顧客価値:**

> 分析上は成立しても実運用では使えない、という後工程の手戻りを減らし、本番化・追加検証・中止等の判断材料を得やすい。

### 5.3.5. 3つを組み合わせる意味

3つのCapabilityは、それぞれ単独では他社も持ち得る。

当チームのPositioning仮説は、それらを**一つのPoCの中で組み合わせること**にある。

```text
問いに合う分析選択
        ×
非定型課題への柔軟な設計
        ×
Enterprise利用条件の考慮
        ↓
難しい分析課題を、実際に使えるPoCとして検証
```

この組合せは、特に以下のDeal Profileで価値が高まりやすいと考える。

- Problem Noveltyが高い
- Analytical Complexityが高い
- Solution Standardizabilityが低い
- Implementation Couplingが一定以上ある
- Criticality / Governanceが一定以上ある

ただし、これはサービス提供範囲を限定するものではない。定型的なPrediction PoCや分析単体案件にも対応し得る。

### 5.3.6. 競争優位に関する内部留保

- `wk10`で整理した通り、当チームが得意であることとRelevant Competitorより優位であることは同義ではない。
- `Specialist Analytics × Enterprise Base` は現時点では有力なPositioning仮説であり、競争優位を確定するには案件実績、人材、顧客評価、Delivery Model等のEvidenceが必要である。
- ただし、この内部留保を顧客向けMessageの前面には出さない。顧客には、確認できているCapabilityとそこから得られる価値を明確に提示する。

## 5.4. Speaker Note

当チームの強みは、高度な分析だけを行うことでも、システム実装だけを行うことでもありません。予測分析と因果推論を使い分けながら、非定型な課題に合わせて分析を設計し、その結果を実際の業務やシステムで利用する条件まで見据えてPoCを進めることです。

一つ目は、問いに合う分析を選ぶことです。何が起こりそうかを知りたいのか、何かを変えたときの効果を知りたいのかによって、必要な分析は異なります。当チームではPredictiveとCausalを分けて扱い、問いに応じて前提や評価方法まで設計します。

二つ目は、非定型な課題への柔軟性です。特定の製品やアルゴリズムへ課題を合わせるのではなく、スクラッチ開発と成熟したOSS等を組み合わせ、顧客固有のデータや評価条件に合わせて分析を構成します。

三つ目は、利用段階まで見据えることです。SIerのデータ分析部門として、分析結果だけではなく、将来のデータ取得、システム連携、Security、運用条件まで必要に応じて考慮します。

特に、既製の分析をそのまま当てはめにくく、かつ分析結果を実際の業務やシステムで使うことまで考える必要がある案件では、この組み合わせが活きます。PoCを単なる分析結果で終わらせず、次の判断につながる形まで検証することが、当チームの提供価値です。

## 5.5. Slide 5からSlide 6への接続

> 当チームは、問いに合う分析設計とEnterprise利用の現実性を一つのPoCで検証する。では、そのPoCでは具体的に何を確認し、次の判断へつなげるのか。次にPoCの目的を整理する。