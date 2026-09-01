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

- Identificationは、目的のCausal Estimandが、明示したAssumptionのもとでObserved Data Distributionの関数として表現可能かという問題である。
- Estimationは、Identificationされた対象量を有限標本から数値的に推定する問題である。
- したがって、必要なIdentification Assumptionが成立しない、または成立を合理的に支持できない場合、Estimatorを複雑化しても目的のCausal Effectを得られるわけではない。
- Backdoor Adjustment、Randomized Comparison、Difference-in-Differences、Regression Discontinuity、Instrumental Variable等は、異なるData Generating ProcessとAssumptionを利用して因果効果を識別する考え方である。
- 同じIdentification Strategyに対して複数のEstimatorを利用できる場合がある。たとえばBackdoor Adjustmentで識別された効果に対し、Outcome Regression / G-formula、Weighting、Matching、Doubly Robust Estimator等を検討できる。
- Estimation段階ではBias / Variance、Model Misspecification、Finite Sample Behavior、Overlap、Extreme Weight等を考慮する。
- 分析報告では「何を仮定して因果効果として識別したか」と「その量をどう推定したか」を分けて説明する。

## 25.4. Speaker Note

因果推論では、「どのEstimatorを使ったか」と「なぜその数値を因果効果と解釈できるか」は別の話です。先に確認するのはIdentificationで、業務上のTreatment割付や時間構造、必要な仮定を使って、知りたい効果を観測データから表現できるかを考えます。

ここが成立して初めて、その対象量をRegression、Weighting、Matchingなどでどう推定するかを選びます。Identificationが成立しない問題を、より高度な機械学習モデルへ置き換えて解決することはできません。その場合はDataやDesign、場合によっては問い自体を見直します。

## 25.5. Slide 25からSlide 26への接続

> **IdentificationとEstimationを分けると、手法選定の起点も変わる。次に、Estimator名ではなく、Treatmentの割付・時間・制度・交絡情報からIdentification Strategyを選ぶ。**
