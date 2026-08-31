Document title: Causal QuestionとEstimandの定義

# 22. Slide 22｜Causal QuestionとEstimandの定義

## 22.1. Message

**因果分析の対象は「因果関係一般」ではなく、Treatment・Outcome・Population・比較条件を明示したEstimandとして定義する。**

## 22.2. Chart

**チャートタイトル:** Business QuestionからEstimandへの具体化

Messageを説明・論証するための主たる視覚表現として、以下の構造を採用する。

### 22.2.1. Chart Structure

- 既存の論理フロー／概念図を主チャートとして用い、要素間の関係・順序が一目で追える構造にする。

```text
Business Question
「施策は有効か？」
        ↓
Treatment：何を変えるか
Outcome：何を改善するか
Population：誰を対象とするか
Time：いつまでの効果か
Contrast：何と何を比べるか
        ↓
Estimand
ATE / ATT / CATE ...
```

**PowerPoint上の配置・強調**

- Business Questionから5要素へ分解し、最後にEstimandへ集約する漏斗型とする。
- ATE等は例示に留め、数式は必要最小限にする。
- Treatment / Outcome / Populationを強調する。

### 22.2.2. Chart内の最小表示テキスト

実際のPowerPoint上では、以下のラベル・短文を中心に表示する。Supporting Logicの全文をスライド上へ掲載しない。

- Business Question
- 「施策は有効か？」
- Treatment：何を変えるか
- Outcome：何を改善するか
- Population：誰を対象とするか
- Time：いつまでの効果か
- Contrast：何と何を比べるか
- Estimand
- ATE / ATT / CATE ...

## 22.3. Supporting Logic

- Treatmentの定義が曖昧だと、異なる施策状態が混在し効果解釈が不明確になる。
- Outcomeは業務KPIと対応させ、測定時点・期間を固定する。
- Populationを定義しないと、推定結果の適用範囲が曖昧になる。
- ATEとATTでは答える意思決定が異なるため、Estimatorより先にEstimandを決める。
- Heterogeneous Effectを扱う場合も、どのSegment差がDecisionに必要かを先に定義する。

- 補足論点：**「何の効果か」をEstimandまで固定して初めて、必要データ・識別戦略・推定法を設計できる。**

## 22.4. Speaker Note

曖昧な「原因を特定したい」を、介入可能なTreatmentと結果Outcomeへ落とすところがDSの重要な設計作業となる。

## 22.5. Slide 22からSlide 23への接続

> **Estimandを定めた後、因果構造と仮定を整理し、どの変数を調整すべきかを設計する。**
