Document title: IdentificationとEstimationを分けて考える

# 25. Slide 25｜IdentificationとEstimationを分けて考える

## 25.1. Message

**Identificationは「因果効果をデータから表現できるか」、Estimationは「その量を有限標本からどう推定するか」であり、別の問題である。**

## 25.2. Chart

**チャートタイトル:** Identificationが成立して初めてEstimationへ進める

### 25.2.1. Chart Structure

Causal QuestionからEffect Estimateまでを、Identification Gateを境に明確に二分する。

```text
Causal Question / Estimand
        ↓
Assumptions / Data Generating Process
        ↓
┌────────────────────────────┐
│ IDENTIFICATION             │
│ 仮定のもとで、Estimandを     │
│ Observed Data Distribution │
│ から表現できるか？           │
└────────────────────────────┘
        ↓
   Identification Gate
   ├─ No → Question / Data / Designを見直す
   └─ Yes
        ↓
Identified Estimand / Functional
        ↓
┌────────────────────────────┐
│ ESTIMATION                 │
│ 有限標本から数値をどう推定するか│
│ Regression / G-formula     │
│ Weighting / Matching / DR  │
└────────────────────────────┘
        ↓
Effect Estimate + Uncertainty
```

**PowerPoint上の配置・強調**

- 上半分をIdentification、下半分をEstimationとして大きく分ける。
- 境界に `Identification Gate` を置き、Noの場合はEstimator側へ進まずQuestion / Data / Designへ戻る矢印を示す。
- Estimator名は下段の小さな例示とし、Identificationより視覚的に強くしない。
- `Identified Estimand / Functional` を両者の橋渡しとして中央に置く。

### 25.2.2. Chart内の最小表示テキスト

- Causal Question / Estimand
- Assumptions / Data Generating Process
- **IDENTIFICATION｜因果効果を観測データから表現できるか**
- **Gate｜識別できるか？**
- No → Question / Data / Design見直し
- Yes → Identified Estimand
- **ESTIMATION｜有限標本からどう推定するか**
- Regression / Weighting / Matching / DR（例）
- Effect Estimate + Uncertainty

## 25.3. Supporting Logic

### 25.3.1. Slide 25の役割

- Slide 23でEstimandを固定し、Slide 24でCausal StructureとAdjustmentに必要なAssumptionを整理した。
- **Slide 25では、「そのAssumptionのもとでEstimandをObserved Dataから表現できるか」というIdentificationと、「表現できた対象量を有限標本からどう推定するか」というEstimationを明確に分離する。**
- この区別はSection 05のScientific Boundaryの中核であり、後続Slide 26のStrategy Selectionを手法カタログにしないための前提となる。

### 25.3.2. Identificationが問うこと

- Identificationは、目的のCausal Estimandを、明示したAssumptionのもとでObserved Data Distributionの関数として表現できるかという問題である。
- 典型的には以下のような問いを扱う。
  - Randomizationにより群比較を因果比較として扱えるか。
  - 必要なConfounderを条件付ければBackdoor Pathを閉じられるか。
  - Policy導入前後とComparison GroupからDiDでCounterfactual Trendを構成できるか。
  - Threshold近傍のAssignment RuleをRDとして利用できるか。
  - Valid InstrumentからTreatmentの外生変動を取り出せるか。
- Identificationの答えは「どのEstimatorが高性能か」ではなく、「どのAssumptionで何が識別されるか」である。

### 25.3.3. Identified Estimand / Functionalが両者の境界になる

- Identificationが成立すると、Causal EstimandをObserved Data上の対象量として表現できる。
- 例えばConditional Exchangeability等のもとでATEをOutcome Regression / G-formulaで表現する、あるいはIPW形式で表現する等、同じCausal Targetに複数の表現があり得る。
- この「何をObserved Dataから計算すれば目的Effectになるか」が定まった後に、有限標本でその量をどう安定して推定するかを考える。
- 理論上のIdentificationと、実データで十分なPrecisionを得られることは別問題である。

### 25.3.4. Estimationが問うこと

- Estimationでは、Identificationされた対象量を有限標本から数値化する。
- 検討事項には以下がある。
  - Model Misspecification。
  - Bias / Variance Trade-off。
  - Sample SizeとEffective Sample Size。
  - Positivity / Overlap不足によるExtreme Weight。
  - Flexible MLを使う場合のOverfitやCross-fitting。
  - Standard Error / Confidence Interval等のUncertainty Estimation。
- Regression、Weighting、Matching、Doubly Robust等は、このEstimation段階の選択肢として位置づける。

### 25.3.5. 高度なEstimatorはIdentification Failureを救わない

- 未観測Confoundingが重要で、Conditional Exchangeabilityを支持できない場合、Random ForestやNeural Networkへ置き換えてもCausal Effectが識別されるわけではない。
- Treatment / ControlのSupportが重ならない領域では、Flexible Modelで数値を出せても実質的にExtrapolationへ依存する。
- Valid Instrumentでない変数を使ってIV Estimationを高度化してもExclusion等の問題は残る。
- Causal MLはOutcome / Propensity ModelやHTE Estimationを柔軟にできるが、Identification Assumptionを不要にしない。
- 因果PoCでは「Estimatorを変えれば解決する問題」と「Data / Designを変えなければ解決しない問題」を分ける。

### 25.3.6. Identificationが成立してもEstimationが難しい場合がある

- 理論上識別可能でも、実データでは以下により推定が不安定になることがある。
  - Treatment群が極端に少ない。
  - Covariate SpaceでOverlapが弱い。
  - OutcomeがRareである。
  - Cluster / Time Dependenceが強い。
  - HTEを求めるにはSampleが不足する。
- この場合は対象Populationの限定、Trimming、Estimator変更、追加Data等を検討する。
- つまり `Identifiable ≠ Precise / Stable` であり、Identification Gate通過後にもEstimation Riskは残る。

### 25.3.7. 報告時にも両者を分ける

因果PoCの成果物では、少なくとも以下を別々に説明する。

1. **Estimand**：何のEffectか。
2. **Identification Strategy**：どの比較構造を使うか。
3. **Assumptions**：なぜ因果Effectとして解釈できるか。
4. **Estimator**：有限標本からどう推定したか。
5. **Uncertainty / Diagnostics**：推定の不確実性と設計上の問題。

- 「Propensity Score Matchingを使ったので因果推論できた」といった説明を避ける。
- Method名ではなく、Identification Logicを第三者が追跡できる状態を作る。

## 25.4. Speaker Note

因果推論で特に重要なのが、IdentificationとEstimationを分けて考えることです。

Identificationで問うのは、「このデータとこの前提から、そもそも知りたい因果効果を取り出せるか」です。例えば必要な交絡要因を観測できているのか、比較群のTrendをCounterfactualとして使えるのか、ThresholdやInstrumentが本当に外生的な比較を作っているのかを考えます。

この問題が解けて初めて、Estimationへ進みます。Estimationでは、識別された対象量をRegression、Weighting、Matching、Doubly Robustなどで有限標本からどう安定して推定するかを考えます。

ここを混同すると、Identificationに問題がある案件でEstimatorだけを高度化してしまいます。未観測Confoundingが残っているなら、Causal Forestへ変えてもその問題は消えません。逆にIdentificationは妥当でも、Overlapが弱い、Sampleが小さいといった理由で推定が不安定なこともあります。

そのため報告でも、「どのAssumptionで因果効果を識別したか」と「その量をどのEstimatorで推定したか」を分けます。因果PoCの品質はMethod名より、この論理を追跡できるかで判断します。

## 25.5. Slide 25からSlide 26への接続

> **IdentificationとEstimationを分けると、手法選定の起点も変わる。次に、Estimator名ではなく、Treatmentの割付・時間・制度・交絡情報からIdentification Strategyを選ぶ。**
