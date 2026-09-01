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

### 23.3.1. Slide 23の役割

- Slide 22では、Causal PoCの最初のPhaseとしてQuestion / EstimandをEstimatorより先に固定することを示した。
- **Slide 23では、曖昧なBusiness Questionを、分析可能かつDecisionに対応するEstimandへ落とす具体的な設計作業を示す。**
- このSlideで固定したEstimandが、後続のDAG、Identification Strategy、Estimator、Diagnostics、Claim Scopeの共通参照点になる。
- 次のSlide 24では、このEstimandに対してどの変数をAdjustmentすべきかをCausal Structureから設計する。

### 23.3.2. Treatment｜何を変えるか

- Treatmentは、比較したい施策・条件・Exposureを明確に定義する。
- 「施策あり」だけでは、施策内容、強度、Timing、Durationが複数混在する可能性があるため、業務上意味のあるIntervention Versionを固定する。
- Multi-valued TreatmentやDoseの場合は、どのLevel同士を比較するかをContrastと合わせて定義する。
- Treatment definitionが曖昧だとConsistencyの解釈が崩れ、Effectの意味が不明確になる。

### 23.3.3. Outcome / Time｜何を、いつ評価するか

- OutcomeはBusiness KPIと対応させるだけでなく、Measurement Ruleを固定する。
- 例：`解約` でも、30日以内の解約、契約更新時の解約、年間Churnでは異なるOutcomeになる。
- Treatment後すぐのOutcomeと長期OutcomeでEffectが異なる場合があるため、Time Horizonを明示する。
- Intermediate OutcomeをFinal Business Outcomeの代替として使う場合は、その関係を別途検討し、短期Effectを長期ROIへ直接読み替えない。

### 23.3.4. Population｜誰に対する効果か

- PopulationはEffectの適用範囲を規定する。
- 既存顧客全体、新規顧客、施策対象候補、実際に施策を受けた顧客等でEstimandは変わり得る。
- Analysis SampleとTarget Populationを同一視しない。Data availability上分析できるSampleが、Business Decisionの対象Populationを十分代表しているかを確認する。
- Generalization / Transportabilityが必要な場合は、PoCのClaim Scopeとして明示する。

### 23.3.5. Contrast｜何と何を比較するか

- Causal EffectはTreatment状態間のContrastで定義される。
- Binary Treatmentなら `施策あり vs なし` が典型だが、Business Decisionが `施策A vs B` ならそのContrastを直接対象にする。
- 現実に存在しない、実行不能なComparisonをEstimandにしてもDecisionには使えない。
- Policy変更前後を比較する場合も、何をCounterfactual Policyとするかを明確にする。

### 23.3.6. ATE / ATT / CATEは異なるDecisionに対応する

| Estimand例 | 概念 | Decision例 |
|---|---|---|
| ATE | Target Population全体の平均Effect | 全体導入するか |
| ATT | 実際にTreatmentを受けたPopulationの平均Effect | 既存施策対象でどの程度効いていたか |
| CATE | Covariate / Segmentで条件付けたEffect | 対象を選別するか |

- これらは代表例であり、案件によってPolicy Value、Quantile Effect等が適切な場合もある。
- EstimandはEstimatorではない。同じATEを複数Estimatorで推定できる。
- 「CATEを出せるからCausal MLを使う」のではなく、Targeting Decisionに異質効果が必要かを先に判断する。

### 23.3.7. 良いEstimandはDataとDecisionの両方へ接続する

良いEstimandは以下を満たす必要がある。

1. **Decision relevance**：結果によって施策・Targeting・配分が変わる。
2. **Well-defined intervention**：Treatment状態が業務上明確である。
3. **Observable outcome**：Outcomeと評価Windowを測定できる。
4. **Defined population**：誰について主張するかが明確である。
5. **Plausible identification**：利用可能Data / Designから識別可能性を検討できる。

- Business上重要でもDataから識別できないEstimandはあり得る。その場合はEstimandを都合よく変えるのではなく、Data / Design追加とTrade-offを明示する。
- 逆にDataから推定しやすくてもDecisionに関係しないEstimandはPoCの中心に置かない。

## 23.4. Speaker Note

「Retention施策は有効ですか」という問いは、一見明確に見えますが、因果分析としてはまだ曖昧です。どの施策状態を比較するのか、何をOutcomeとするのか、誰について、いつまでの効果を見るのかを決める必要があります。

例えばTreatmentを「Retention施策あり vs なし」、Outcomeを「30日以内の解約」、Populationを「更新対象となる既存顧客」と定義すれば、知りたい効果の範囲がかなり明確になります。ここで90日後を見るなら別のEstimandですし、実際に施策を受けた顧客だけの効果を見るならATTのように対象量も変わります。

ATE、ATT、CATEという言葉は手法の名前ではありません。「誰について、何と何を比較した効果を知るか」を表す対象量です。したがって、Estimatorを選ぶ前にBusiness Decisionに対応するEstimandを固定します。

また、分析しやすい量を選ぶことが目的ではありません。Business上は全顧客への導入判断をしたいのに、Data上扱いやすい一部顧客だけのEffectを出して、そのまま全体へ一般化することは避けます。分析Sampleと主張対象Populationの違いも成果物に残します。

このEstimandが決まると、次に「その効果を観測データから取り出すために何を調整し、どのAssumptionが必要か」を具体的に設計できます。

## 23.5. Slide 23からSlide 24への接続

> **Estimandを固定しただけでは、その効果を観測データから因果効果として取り出せるとは限らない。次に、Treatment前後の時間順序と変数の役割を整理し、必要なAssumptionとAdjustmentを設計する。**
