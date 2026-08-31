Document title: IdentificationとEstimationを分けて考える

# 24. Slide 24｜IdentificationとEstimationを分けて考える

## 24.1. Message

**Identificationは「因果効果をデータから表現できるか」、Estimationは「その量を有限標本からどう推定するか」であり、別の問題である。**

## 24.2. Chart

**チャートタイトル:** Identification → Estimationの二段階

Messageを説明・論証するための主たる視覚表現として、以下の構造を採用する。

### 24.2.1. Chart Structure

- 既存の論理フロー／概念図を主チャートとして用い、要素間の関係・順序が一目で追える構造にする。

```text
Causal Question / Estimand
        ↓
[ Identification ]
仮定のもとで観測分布から
因果効果を表現できるか
        ↓
Identified Estimand
        ↓
[ Estimation ]
回帰・Matching・Weighting・DR等で
有限標本から数値推定
        ↓
Effect Estimate + Uncertainty
```

**PowerPoint上の配置・強調**

- 上下二段の大きな箱でIdentification / Estimationを明確に分離する。
- 境界部分にIdentified Estimandを置く。
- Estimator名は下段の補助情報として扱う。

### 24.2.2. Chart内の最小表示テキスト

実際のPowerPoint上では、以下のラベル・短文を中心に表示する。Supporting Logicの全文をスライド上へ掲載しない。

- Causal Question / Estimand
- [ Identification ]
- 仮定のもとで観測分布から
- 因果効果を表現できるか
- Identified Estimand
- [ Estimation ]
- 回帰・Matching・Weighting・DR等で
- 有限標本から数値推定
- Effect Estimate + Uncertainty

## 24.3. Supporting Logic

- Identificationが成立しない場合、Estimatorを高度化しても目的の因果効果は得られない。
- Backdoor adjustment、DiD、IV、RDD等は異なる識別仮定に基づく。
- 同じIdentification Strategyに対して複数のEstimatorを比較できる場合がある。
- Estimator選択時にはbias-variance、overlap、model misspecification等を考慮する。
- 分析報告では識別仮定と推定方法を分けて説明する。

- 補足論点：**因果PoCの品質は「どのEstimatorを使ったか」より前に、「なぜそのEstimatorで因果効果を推定できるのか」を説明できるかで決まる。**

## 24.4. Speaker Note

因果推論の専門性を端的に示す重要スライド。営業資料でもここを落とすと単なる手法カタログになる。

## 24.5. Slide 24からSlide 25への接続

> **次に、データ生成過程に応じてどのIdentification Strategyを選ぶかを代表例で示す。**
