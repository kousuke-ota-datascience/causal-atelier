Document title: 予測分析PoCの成果物とGo / No-Go

# 17. Slide 17｜予測分析PoCの成果物とGo / No-Go

## 17.1. Message

**予測PoCの成果は、成立条件・失敗条件・未検証事項を含むEvidence Packageであり、それを基に次フェーズを選ぶ。**

## 17.2. Chart

**チャートタイトル:** Evidence Packageから、次フェーズの選択肢を判断する

Slide 14〜16で得た検証結果をModel単体で返すのではなく、**Question / Data、Performance、Failure / Utility、利用条件、未検証事項をEvidence Packageとして統合し、GO / ADDITIONAL VALIDATION / NO-GOの判断へ接続する**構造を主チャートとして示す。

### 17.2.1. Chart Structure

```text
Predictive PoC Evidence Package

┌──────────────────────┐
│ ① Question / Data     │
│ Prediction Question   │
│ Data / Split Assessment│
└──────────────────────┘
┌──────────────────────┐
│ ② Performance         │
│ Baseline vs Model     │
│ Holdout / Calibration │
└──────────────────────┘
┌──────────────────────┐
│ ③ Failure / Utility   │
│ Error Pattern         │
│ Decision Utility      │
└──────────────────────┘
┌──────────────────────┐
│ ④ Usage Conditions    │
│ 対象範囲 / Timing / Rule│
│ Human Review / 制約    │
└──────────────────────┘
┌──────────────────────┐
│ ⑤ Residual Uncertainty│
│ 未検証事項 / Drift     │
│ Production検証事項     │
└──────────────────────┘
            ↓
Decision Gate
Feasibility / Generalization / Utility / Operating Fit / Residual Risk
            ↓
┌──────────────────┬──────────────────────┬──────────────────┐
│ GO               │ ADDITIONAL VALIDATION│ NO-GO            │
│ 次フェーズへ進む │ 不確実性を追加検証   │ 中止 / 再設計      │
├──────────────────┼──────────────────────┼──────────────────┤
│ 実装設計         │ Data追加             │ Question見直し    │
│ Production検証   │ 期間 / 対象拡張      │ Data / Action見直し│
│ Monitoring設計   │ 外部 / 運用検証      │ 別アプローチ検討  │
└──────────────────┴──────────────────────┴──────────────────┘

※ GOはBusiness Outcome改善の確定ではなく、次フェーズへ進む根拠が得られた状態
```

**PowerPoint上の配置・強調**

- 上段にEvidence Packageの5要素をカードとしてまとめる。Model fileを独立した主成果物として置かない。
- 中央のDecision Gateでは、単一Metricではなく `Feasibility / Generalization / Utility / Operating Fit / Residual Risk` を横並びで示す。
- 下段は `GO / ADDITIONAL VALIDATION / NO-GO` を同じウェイトで並べ、Additional ValidationとNo-GoもEvidenceに基づく正当な判断であることを示す。
- GOの直下は「本番化」だけにせず、`実装設計 / Production検証 / Monitoring設計` とし、PoCから即時の全面本番化を保証する表現を避ける。
- 最下部に `GOはBusiness Outcome改善の確定ではない` という留保を置く。

### 17.2.2. Chart内の最小表示テキスト

- **Predictive PoC Evidence Package**
- Question / Data
- Baseline vs Model
- Holdout / Calibration
- Error Pattern / Decision Utility
- Usage Conditions
- Residual Uncertainty
- **Decision Gate**
- Feasibility / Generalization / Utility / Operating Fit / Residual Risk
- **GO**｜次フェーズへ進む
- **ADDITIONAL VALIDATION**｜不確実性を追加検証
- **NO-GO**｜中止 / 再設計
- 実装設計 / Production検証 / Monitoring設計
- Data追加 / 期間・対象拡張 / 外部・運用検証
- Question / Data / Action見直し
- **GO ≠ Business Outcome改善の確定**

## 17.3. Supporting Logic

### 17.3.1. Slide 17の役割

- Slide 14ではPrediction QuestionとValidation Designを固定した。
- Slide 15では同じValidation条件のもとでBaselineからFit-for-useなModelを選定した。
- Slide 16ではGeneralization、Reliability、Failure Mode、Business Utilityの4層で利用可否を評価した。
- **Slide 17では、それらを「何が成立し、どの条件なら使え、何がまだ未検証か」というEvidence Packageへ統合し、次フェーズ判断へ接続する。**
- したがって成果物はModel fileやAccuracy表だけではなく、**利用可否を第三者が追跡できる判断材料一式**である。

### 17.3.2. Evidence Packageに含める5要素

#### 1. Question / Data

- Prediction Question：Who / Prediction Time / Target / Horizon / Decision / Action。
- Target / Feature定義とPrediction TimeでのData availability。
- 対象Population、Data期間、Sample Size、Label availability、欠損等のData Assessment。
- Split / Validation / Holdout設計と、その設計が実運用をどこまで模擬しているか。
- Leakage防止条件、除外条件、既知のData limitation。

#### 2. Performance

- 現行Rule / Simple BaselineとSelected Modelの比較。
- Locked HoldoutでのTask-specific Performance。
- Probabilityを使う場合のCalibration。
- 期間・Segment等でのStability。
- ValidationとHoldoutの差、性能劣化の有無。

#### 3. Failure / Utility

- False Positive / False Negative、過大 / 過小予測等のError Pattern。
- 重要Segment・期間・条件でのFailure Mode。
- ExplainabilityによるModel挙動の確認。ただし因果効果として解釈しない。
- Ranking / Threshold / Capacity / Action Costを含むDecision Utility。
- 現行Decision Ruleとの比較結果。

#### 4. Usage Conditions

- どの対象Population / Segmentへ適用するか。
- いつPredictionを出し、誰が利用するか。
- Ranking / Threshold / Schedule等、どのDecision Ruleへ接続するか。
- Human Review、Abstention、Safety Rule等を必要とする条件。
- Predictionに必要なDataを実運用時に取得できるか。
- 適用外とするCaseや、Predictionを自動Actionへ使わない条件。

#### 5. Residual Uncertainty

- Data期間が短い、特定環境しか含まない、重要SegmentのSampleが少ない等の未検証事項。
- Distribution Shift / Driftへの耐性。
- 外部拠点・別期間・別PopulationへのGeneralization。
- Production上のLatency、Data Pipeline、Monitoring等の未検証事項。
- Predictionを使ったActionが実Business Outcomeを改善するかというProductionレベルの未検証事項。

- **未検証事項を隠さず成果物化すること自体が、PoCの重要な成果である。**

### 17.3.3. Decision Gateは単一Accuracyで決めない

Gateでは少なくとも以下の5観点を確認する。

| Gate観点 | 判断する問い |
|---|---|
| Feasibility | Prediction Timeで必要DataからTargetを予測できるか |
| Generalization | 実利用を模した未知データでBaselineを超えるか |
| Utility | PredictionをDecision Ruleへ変換すると現行判断より有用か |
| Operating Fit | Data availability、Latency、Human Review、Capacity等の運用条件を満たせるか |
| Residual Risk | 重要なFailure Modeや未検証事項を次フェーズで許容・検証できるか |

- GateのThresholdや必須条件は案件ごとに、Slide 10で合意した成功基準へ戻して判断する。
- 「Metricが最も高いModelがある」だけではGO条件にならない。
- 逆に、一部制約が残っていても、適用範囲の限定や追加検証で解消可能ならAdditional Validationまたは限定的な次フェーズへ進める場合がある。

### 17.3.4. GO｜次フェーズへ進む根拠が得られた

GOは、少なくとも以下の条件がEvidenceで支持される状態を想定する。

- Prediction Questionが業務Decisionへ接続している。
- Locked HoldoutでBaselineに対する有意義な増分が確認できる。
- 重要SegmentのFailure Modeが把握され、Downsideを許容・緩和できる。
- Decision Utilityがあり、Predictionを受けるAction / Ruleが実行可能である。
- 残る不確実性をProduction検証やMonitoringで管理できる見込みがある。

GO後の候補は以下であり、案件に応じて選ぶ。

- 実装 / Integration設計。
- Shadow modeや限定運用によるProduction検証。
- Threshold / Capacity / Human Review ruleの確定。
- Monitoring、Drift検知、Retraining条件等の設計。
- 必要に応じたBusiness Outcomeの実地評価。

**GOは「PoCでBusiness Outcome改善まで証明済み」という意味ではない。**

### 17.3.5. ADDITIONAL VALIDATION｜不確実性を減らせば判断可能

Additional Validationは失敗ではなく、**追加Evidenceにより判断を更新できる合理的な選択肢**である。

例：

- Data期間が短い → 追加期間を取得してTime Split / Backtestを拡張する。
- 重要SegmentのSampleが少ない → 対象数を増やす。
- 一拠点だけで検証 → 別拠点 / 別PopulationでExternal Validationする。
- Thresholdの業務Costが不明 → Capacity / Action Costを入れたSimulationを行う。
- Data availabilityが不明 → 実運用PipelineでShadow testを行う。
- Drift懸念がある → 時間を置いたProspective Validationを行う。

- 追加検証は「とりあえずDataを増やす」のではなく、**どのResidual Uncertaintyを減らせばGate判断が変わるか**を明示して設計する。

### 17.3.6. NO-GO｜中止またはQuestion / Data / Actionを再設計する

No-GoもEvidenceに基づく成果である。代表例は以下。

- Leakageを除くとPrediction Performanceが成立しない。
- Locked HoldoutでBaselineを安定して超えない。
- 重要なFailure ModeのDownsideを業務で許容・緩和できない。
- Prediction Timeで必要Dataを取得できない。
- 予測できてもActionを変えられずDecision Utilityがない。
- 必要性能を得るためのData / Operation Costが期待価値に見合わない。

No-Go時の次アクションは「終了」だけではない。

- Prediction QuestionやPrediction Horizonを見直す。
- Target / Feature / Data収集を再設計する。
- Action / Decision Ruleを見直す。
- Exploratory Analysisへ戻りData生成過程を理解する。
- **本当に知りたい問いが「施策をするとどう変わるか」であれば、PredictiveではなくCausal Questionとして再定義する。**

### 17.3.7. Section 04で顧客へ伝える最終メッセージ

Section 04を通じて伝えるべきことは、Predictive PoCが単なるModel開発ではないという点である。

```text
業務Decision / Action
        ↓
Prediction Question
        ↓
Validation Design
        ↓
Fit-for-use Model Selection
        ↓
Generalization / Reliability / Failure / Utility
        ↓
Evidence Package
        ↓
Next Phase Decision
```

- Prediction Performanceは必要条件だが、それだけでBusiness Valueは決まらない。
- Prediction Errorを前提に、誰が・いつ・どのRuleで使うかまで設計し、利用条件と未検証事項を明示して次フェーズへ渡す。
- この境界を明確にすることで、Predictiveで主張できることを過大評価せず、必要な場合にCausal PoCへ正しく接続できる。

## 17.4. Speaker Note

PoCの成果物をModelファイルだけにすると、次の担当者は「どの条件なら使えるのか」「どこで外れるのか」「何がまだ分かっていないのか」を判断できません。そこで、Prediction Question、DataとValidation、Holdout性能、Failure Mode、Decision Utility、利用条件、未検証事項を一つのEvidence Packageとして返します。

そのEvidenceを、Feasibility、Generalization、Utility、Operating Fit、Residual Riskの観点で確認し、Go、Additional Validation、No-Goを判断します。Additional ValidationやNo-GoもPoCの失敗ではなく、投資や実装を進める前に不確実性を明らかにしたという意味で重要な結果です。

また、Goは「Business Outcome改善が確定した」という意味ではありません。Predictionを業務へ接続する根拠が得られた状態であり、必要に応じてProductionでの限定検証、Monitoring、実Business Outcomeの評価を次フェーズとして行います。

## 17.5. Slide 17からSlide 18への接続

> **Predictiveは「何が起こりそうか」を見通してDecisionを改善する。一方、次に知りたいことが「施策を実施するとOutcomeがどれだけ変わるか」であれば、高Risk予測だけでは答えられない。次SectionではTreatmentの介入効果を扱う因果推論へ進む。**
