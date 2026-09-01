Document title: Causal QuestionとEstimandの定義

# 23. Slide 23｜Causal QuestionとEstimandの定義

## 23.1. Message

**因果分析の対象は「因果関係一般」ではなく、Treatment・Outcome・Population・Time・Contrastを明示したEstimandとして定義する。**

## 23.2. Chart

**チャートタイトル:** 「施策は有効か？」をDecisionに対応するEstimandへ具体化する

### 23.2.1. Chart Structure

Customer Retentionを例に、曖昧なBusiness Questionを5要素へ分解し、最後にEstimandへ集約する。

```text
Business Question
「Retention施策は有効か？」
        ↓
┌────────────────────────────┐
│ Treatment｜何を変えるか      │
│ 施策あり vs 施策なし          │
├────────────────────────────┤
│ Outcome｜何を評価するか        │
│ 解約                         │
├────────────────────────────┤
│ Population｜誰についてか       │
│ 対象顧客群                    │
├────────────────────────────┤
│ Time｜いつまでの効果か          │
│ 業務上意味のある評価期間         │
├────────────────────────────┤
│ Contrast｜何と何を比較するか     │
│ 施策あり − 施策なし             │
└────────────────────────────┘
        ↓
Estimand
「対象Populationにおける施策あり vs なしの
解約Outcome差」
例：ATE / ATT / CATE
```

**PowerPoint上の配置・強調**

- 左上に曖昧なBusiness Questionを置き、中央の5要素へ分解する。
- 5要素は同じウェイトで示し、Treatment / OutcomeだけでなくPopulation / Time / Contrastも必要であることを見せる。
- 下段にEstimandを置き、ATE / ATT / CATEは小さな例示として配置する。
- 数式一覧にはせず、「誰について、何と何を比べた効果か」が読める日本語を主表示にする。

### 23.2.2. Chart内の最小表示テキスト

- 「Retention施策は有効か？」
- Treatment｜施策あり vs なし
- Outcome｜解約
- Population｜対象顧客群
- Time｜評価期間
- Contrast｜施策あり − なし
- **Estimand｜誰について、何と何を比べた効果か**
- ATE / ATT / CATE（例）

## 23.3. Supporting Logic

- Treatmentの定義が曖昧だと、異なる施策内容・強度・タイミングが混在し、Effectの意味が不明確になる。
- OutcomeはBusiness KPIと対応させるだけでなく、測定方法と評価時点 / Windowを固定する必要がある。
- Populationは推定結果を誰へ適用するかを決める。対象範囲を変えるとEstimandも変わり得る。
- Contrastは、どのTreatment状態とどのTreatment状態を比較するかを明示する。多値TreatmentやDoseの場合は比較対象を特に明確にする。
- ATEは対象Population全体の平均効果、ATTは実際にTreatmentを受けたPopulationに対する平均効果、CATEはCovariate等で条件付けた効果を表す代表例であり、答えるDecisionが異なる。
- ATE / ATT / CATEはEstimator名ではない。Estimatorは、後段でIdentified Estimandを有限標本から推定するために選ぶ。
- Heterogeneous Effectを扱う場合も、どのSegment差がDecisionに必要かを先に定める。探索的な差を無制限に探すことを目的にしない。
- 「原因を特定したい」という依頼は、そのままEstimandにならない。介入可能なTreatmentとDecisionへ接続できる問いへ具体化する必要がある。

## 23.4. Speaker Note

「この施策は有効ですか」という問いは、そのままでは分析対象がまだ曖昧です。どの施策状態を比べるのか、何をOutcomeとするのか、誰について、どの期間の効果を見るのかを決める必要があります。

この5要素を固定すると、たとえば「対象顧客群についてRetention施策を行った場合と行わない場合の解約Outcome差」という形で、知りたい効果を明確にできます。ATEやATT、CATEは、この「誰についてどの効果を知るか」を表す対象量で、推定手法そのものではありません。

## 23.5. Slide 23からSlide 24への接続

> **Estimandを固定しただけでは、その効果を観測データから因果効果として取り出せるとは限らない。次に、Treatment前後の時間順序と変数の役割を整理し、必要なAssumptionとAdjustmentを設計する。**
