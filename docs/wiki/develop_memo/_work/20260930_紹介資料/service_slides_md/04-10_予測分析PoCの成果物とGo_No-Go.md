Document title: 予測分析PoCの成果物とGo / No-Go

# 20. Slide 20｜予測分析PoCの成果物とGo / No-Go

## 20.1. Message

**予測PoCの成果は、成立条件・失敗条件・未検証事項を含むEvidence Packageであり、それを基に次フェーズを選ぶ。**

## 20.2. Chart

**チャートタイトル:** Evidence Packageから、次フェーズの選択肢を判断する

### 20.2.1. Chart Structure

```text
Predictive PoC Evidence Package
┌──────────────────────┐
│ ① Question / Data     │
│ Question / Data / Split│
└──────────────────────┘
┌──────────────────────┐
│ ② Performance         │
│ Baseline / Holdout    │
│ Calibration / Stability│
└──────────────────────┘
┌──────────────────────┐
│ ③ Failure / Utility   │
│ Error Pattern         │
│ Decision Utility      │
└──────────────────────┘
┌──────────────────────┐
│ ④ Usage Conditions    │
│ Scope / Timing / Rule │
│ Human Review / Safety │
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
│ 次フェーズへ進む │ 不確実性を追加検証   │ 中止 / 再設計     │
└──────────────────┴──────────────────────┴──────────────────┘

※ GO ≠ Business Outcome改善の確定
```

### 20.2.2. Chart内の最小表示テキスト

- Predictive PoC Evidence Package
- Question / Data / Split
- Baseline / Holdout / Calibration
- Error Pattern / Decision Utility
- Usage Conditions
- Residual Uncertainty
- Decision Gate
- Feasibility / Generalization / Utility / Operating Fit / Residual Risk
- GO｜次フェーズへ進む
- ADDITIONAL VALIDATION｜不確実性を追加検証
- NO-GO｜中止 / 再設計
- **GO ≠ Business Outcome改善の確定**

## 20.3. Supporting Logic

### 20.3.1. Slide 20の役割

- Slide 17ではPrediction QuestionとValidation Designを固定した。
- Slide 18では同じ条件のもとでFit-for-useなModelを選定した。
- Slide 19ではGeneralization、Reliability、Failure Mode、Business Utilityを評価した。
- **Slide 20では、それらを成立条件・利用条件・未検証事項まで含むEvidence Packageへ統合し、次フェーズ判断へ接続する。**
- 成果物はModel fileやAccuracy表だけではなく、利用可否を第三者が追跡できる判断材料一式である。

### 20.3.2. Evidence Packageに含める5要素

1. **Question / Data**
   - Prediction / Detection Question、利用時点、対象、Horizon、Decision / Action。
   - Data期間、Label availability、Split / Validation / Holdout、Leakage防止条件。
   - 設備案件では設備・型式・拠点・期間のCoverageも明示する。
2. **Performance**
   - 現行Rule / Baselineとの比較。
   - Locked HoldoutでのTask-specific Performance。
   - Calibration / Stability、異常検知では必要に応じてAlert burdenやKnown Eventでの検証。
3. **Failure / Utility**
   - False Positive / False Negative、早すぎ / 遅すぎ検知、RUL誤差等。
   - 重要設備・Segment・期間でのFailure Mode。
   - Ranking / Threshold / Schedule / Capacity等のDecision Utility。
4. **Usage Conditions**
   - 適用対象、Prediction / Detection Timing、Decision Rule。
   - Human Review、Abstention、Safety Rule、Critical設備での利用制約。
   - 実運用時のData availability、Latency、更新条件。
5. **Residual Uncertainty**
   - Data期間・故障件数不足、別設備 / 拠点へのGeneralization、Drift。
   - Production Pipeline、Monitoring、Business Outcomeの未検証事項。

### 20.3.3. Decision Gateは単一Metricで決めない

| Gate観点 | 判断する問い |
|---|---|
| Feasibility | 利用時点のDataから必要Evidenceを作れるか |
| Generalization | 実利用を模した未知データでBaselineを超えるか |
| Utility | OutputをDecision Ruleへ変換すると現行判断より有用か |
| Operating Fit | Data、Latency、Human Review、Safety、Capacityを満たせるか |
| Residual Risk | Failure Modeや未検証事項を次フェーズで管理できるか |

- Slide 10で合意した成功基準へ戻してGateを判断する。
- 高いAccuracyや高いAnomaly SeparationだけでGOとはしない。

### 20.3.4. GO / ADDITIONAL VALIDATION / NO-GO

**GO**
- 利用時点のDataで有用なEvidenceが再現する。
- 重要なFailure Modeを把握し、Downsideを許容・緩和できる。
- Decision RuleとActionが実行可能である。
- 次フェーズではIntegration、Shadow mode、限定運用、Monitoring等を検討する。

**ADDITIONAL VALIDATION**
- 故障Event・Data期間を追加する。
- 別設備、別型式、別拠点、別期間でExternal / Prospective Validationする。
- Alert burden、Threshold、保全Capacity、Data Pipelineを実運用条件で追加確認する。
- 「何のResidual Uncertaintyを減らせばGate判断が変わるか」を明示する。

**NO-GO**
- Leakageを除くと性能が成立しない。
- 未知データでBaselineを安定して超えない。
- 故障Labelや正常状態定義が成立せず、対象Questionを評価できない。
- 重要な見逃し・誤報を業務で許容できない。
- Evidenceが得られても保全Actionを変更できない。
- 必要Data / Operation Costが期待価値に見合わない。

No-Goは失敗ではなく、Question / Data / Actionの再設計、追加Data取得、別アプローチへの切替を判断できた成果である。

### 20.3.5. Section 04で顧客へ伝える最終メッセージ

```text
Predictiveの一般原則
        ↓
重点テーマ：故障予測・異常検知
Data → Evidence → 保全Decision
        ↓
Prediction / Detection Question
        ↓
Validation Design
        ↓
Fit-for-use Model
        ↓
Generalization / Reliability / Failure / Utility
        ↓
Evidence Package
        ↓
Next Phase Decision
```

- Prediction / Detection Performanceは必要条件だが、それだけでBusiness Valueは決まらない。
- 特に設備領域では、Anomaly ScoreとFailure Probabilityを区別し、保全DecisionとSafety条件まで含めて利用可否を判断する。
- **高Failure Riskな設備と、特定保全施策によって最も改善する設備は同義ではない。**

## 20.4. Speaker Note

PoCの成果物をModelファイルだけにすると、どの条件なら使えるか、どこで外れるか、何がまだ分かっていないかを判断できません。そこで、QuestionとData、Holdout性能、Failure Mode、Decision Utility、利用条件、未検証事項をEvidence Packageとして返します。

設備案件では特に、どの設備・期間・型式まで検証したか、故障件数が十分か、Alert負荷や見逃しが許容できるか、Safety Ruleが必要かまで明示します。

GOはBusiness Outcome改善の確定ではありません。次フェーズへ進む根拠が得られた状態であり、必要に応じてProductionで追加検証します。

## 20.5. Slide 20からSlide 21への接続

> **Predictiveは「どの設備が故障しそうか」「どの状態が通常と異なるか」を判断材料にできる。一方、「保全施策を変えると故障・停止がどれだけ減るか」を知りたい場合、高RiskやAnomalyだけでは答えられない。次SectionではTreatmentによるOutcome変化を扱う因果推論へ進む。**
