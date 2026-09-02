# Section 04 Story｜予測分析PoC

## Polaris

**予測分析は、Decision時点で利用可能な情報から未知・将来のOutcomeを予測し、その不確実性を含むPredictionをDecision Ruleへ組み込んでOutcome確定前のActionを改善する。当チームの重点テーマである故障予測・異常検知では、現在の状態変化を捉えるDetectionと将来の故障・劣化を見通すPredictionを区別し、設備Dataの観測可能性と保全Decisionから分析課題を定義する。PoCでは、Prediction QuestionとSplit / Validation設計をモデル選定より先に固定し、未知データでの再現性、Calibration、Error Pattern、Business Utilityを評価し、モデルだけでなく利用条件・制約をEvidence Packageとして次フェーズ判断へ渡す。**

## このセクションの役割

- Section 01〜03で定義したPredictiveの意味とDecision起点のPoC設計を、予測分析固有のWorkflowへ具体化する。
- 予測分析が価値を持つ業務条件を、業界ではなくDecision / Actionの構造として整理する。
- Prediction Errorを前提に、PredictionをDecision Ruleと反復Actionへ組み込むことでKPIの期待値を改善する価値発現メカニズムを示す。
- **当チームの重点テーマとして、設備の故障予測・異常検知を3枚で具体化し、「何を捉えるか」「どの業務に適するか」「どの保全Decisionへ価値を出すか」を示す。**
- Prediction Question、Validation、Model Selection、Evaluation、成果物とNext Phase判断までを一貫したストーリーとして接続する。

## Storyline

1. **予測分析は、Outcomeが分かる前のDecisionを支える。**
   - `Decision時点の観測情報 → Predictive Model → Prediction → Decision / Action` が基本構造である。
   - Featureは、実際にDecisionを行う時点で利用可能な情報に限定する。Outcome確定後の情報や未来情報を含めない。
   - PredictionはRisk / Probability / Forecast等の判断材料であり、Actionそのものではない。ActionはDecision Ruleと業務制約を介して決まる。

2. **Predictive PoC候補は、Predictionを先回りしたActionへ変換できる業務である。**
   - **BEFORE**：Outcomeが分かる前にDecisionがある。
   - **CHANGE**：Predictionに応じてActionを変えられる。
   - **DIFFERENTIATE**：対象・案件・時点によって判断を変える余地がある。
   - **REPEAT / ACCUMULATE**：類似Decisionを多数回行い、Baselineより良い判断の差分を累積できる。
   - **TOLERATE**：個々の誤予測を許容、またはHuman Review / Abstention / Safety Rule等で緩和できる。
   - **OBSERVE**：Outcome / KPIを事後観測し、性能やDecision Ruleを評価できる。
   - 代表ActionはPrioritize、Review / Escalate、Schedule、Allocate / Planである。

3. **Predictiveの価値は、一件を必ず当てることではなくDecision全体の期待値改善にある。**
   - `Prediction + Uncertainty → Decision Rule → 多数のDecision / Action → Operational Effect → KPI / Business Outcome` と接続する。
   - 個々のFalse Positive / False Negative / Forecast Errorは残り得る。
   - それでもBaselineより平均的に良い対象・時期・量を選べれば、見逃し・不要対応・時期Mismatch・Resource配分Mismatch等を減らし、KPI差分を累積できる。
   - Prediction性能だけではBusiness Outcome改善を証明しない。実際のOutcome改善にはProduction比較、実験、因果評価等が追加で必要になる場合がある。

4. **重点テーマでは、異常検知と故障予測を同義にしない。**
   - 異常検知は主に「現在の設備状態が通常状態から外れているか」を捉え、Anomaly Score / Flag等を返す。
   - 故障予測は「将来一定期間内に故障するか」「あとどの程度稼働できるか」を扱い、Failure Probability、Time-to-Failure、RUL等を返す。
   - `Anomaly Score ≠ Failure Probability` を明示し、異常であることから将来故障することを自動的に結論しない。
   - 実務上は `状態監視 → 異常・変化把握 → 故障Risk / 劣化 / RUL → 保全Decision` と連携し得るが、案件ごとに必要な問いだけを選ぶ。

5. **故障予測・異常検知は、状態を観測でき、兆候に応じて保全Actionを変えられる業務に適する。**
   - **OBSERVE**：設備状態・運転条件を継続的に観測できる。
   - **BEFORE**：故障・停止・品質異常の前に兆候を捉える意味がある。
   - **CHANGE**：点検、交換、保全時期、監視強度等を変更できる。
   - **REPEAT**：設備・期間・部品等で類似判断が繰り返され、評価可能なDataが蓄積する。
   - **COST ASYMMETRY**：見逃し、誤報、突発停止、過剰保全等のCost差がありDecision Ruleを設計する意味がある。
   - 故障Labelと故障前履歴が十分ならFailure Prediction / RUL、故障Labelが少なく正常稼働Dataが豊富ならAnomaly Detection / State Monitoring等を検討する。

6. **故障予測・異常検知の価値は、設備Evidenceを保全Decisionへ変換することで発現する。**
   - `Anomaly Score / Failure Risk / RUL → Decision Rule → 点検優先順位 / 交換判断 / 保守Schedule / 人員・部品配置` と接続する。
   - Operational Effectとして、突発停止への先回り、不要・過剰な点検や交換の抑制、保全時期やResource配分のMismatch抑制を狙う。
   - False NegativeとFalse PositiveのCostは設備Criticality、安全条件、停止Cost、点検Cost等で異なるため、ThresholdやTop-Kは業務条件と合わせて設計する。
   - Detection / Prediction性能だけではDown Timeや保全Costの実改善を証明しない。
   - **高Failure Riskな設備 ≠ 特定保全施策で最も改善する設備**。保全施策のTreatment EffectはCausal Questionとして分ける。

7. **Predictive PoCでは、Modelより先にPrediction Questionと検証設計を固定する。**
   - Workflowは `Prediction Question → Target / Feature Definition → Split Design → Preprocessing / Baseline → Modeling → Holdout Evaluation → Error Analysis / Explainability → Business Decision`。
   - 誰について、いつ時点で、何を、どこまで先を予測するかを明確にする。
   - Random / Time / Group等のSplitはData Generating Processに合わせ、Holdoutを学習・Model Selectionから分離する。
   - 単純Ruleや現行判断をBaselineとして置き、複雑なModelの増分価値を確認する。

8. **モデル選定は「高度さ」ではなく、課題と運用条件へのFitで行う。**
   - Data Structure、非線形性、Sample Size、欠損、必要性能、説明性、推論時間、更新頻度等からModel Familyと複雑度を選ぶ。
   - Linear / Logistic、Tree、Random Forest、Gradient Boosting、Time-series等は候補であり、手法名自体を価値にしない。
   - Baselineより複雑にする増分価値、Calibration、安定性、解釈性、推論Costを合わせて判断する。

9. **モデル評価は、単一Accuracyではなく4層で行う。**
   - **Discrimination / Error**：AUROC、AUPRC、MAE、RMSE等を目的に応じて使う。
   - **Calibration**：Prediction Probabilityと実発生率の整合を確認する。
   - **Segment / Error Analysis**：重要Segment・期間・条件でどのように失敗するかを確認する。
   - **Business Utility**：Threshold、Ranking、誤判定Cost、Capacity、Action Value等を含め、Predictionを業務に使えるかを評価する。
   - ExplainabilityはModel挙動の理解に使うが、因果効果として解釈しない。

10. **Predictive PoCの成果は、モデルファイルではなく利用可否を判断できるEvidence Packageである。**
   - Prediction Question / Data Assessment。
   - Baseline / Candidate Models。
   - Holdout Performance / Calibration。
   - Error Analysis / Explainability。
   - 適用範囲・利用条件・制約。
   - これらをもとに `GO / ADDITIONAL VALIDATION / NO-GO` を判断し、本番化、データ追加、設計見直し、終了等へ接続する。

## Must Keep｜編集で崩してはいけない境界

- Predictiveで利用するFeatureとOutcomeの関係は、因果関係である必要はない。予測上の関連を介入効果へ読み替えない。
- **高Riskな対象 ≠ 特定施策で最も改善する対象**。施策効果によるTargetingはCausal Questionとして扱う。
- **Anomaly Score ≠ Failure Probability**。異常検知と将来故障予測を同じOutputとして扱わない。
- 異常検知は必ずしも未来Outcomeを直接予測する分析ではない。設備保全の重点テーマとして同じサブセクションで扱っても、分析上の意味論は区別する。
- Business上の適用候補であることと、実際に十分なPrediction / Detection Performanceが得られることを分けて検証する。
- Future / Target Leakage、不適切なSplit、Holdoutの再利用により見かけの性能を過大評価しない。
- 「最も複雑なModel」「最高Accuracy」を自動的な最適解としない。
- SHAP等のExplainabilityを原因説明として扱わない。
- Prediction / Detection PerformanceとBusiness Outcome改善を同義にしない。
- No-GoやAdditional Validationを失敗扱いせず、Evidenceに基づくNext Phase判断として扱う。

## Slide Mapping

| File | Deck Slide | Story上の役割 | Core Claim |
|---|---:|---|---|
| 04-01 | 11 | Predictiveの定義 | Decision時点の情報から未知・将来Outcomeを予測し、事前判断へ使う |
| 04-02 | 12 | 適用条件 | ActionabilityとPrediction Errorを業務で扱える構造を持つ課題に適する |
| 04-03 | 13 | 価値発現 | 誤りを含むPredictionでも多数のDecision改善を累積してKPI価値へ接続する |
| 04-04 | 14 | 重点テーマ：定義 | 異常検知は現在の状態変化、故障予測は将来の故障・劣化を捉える |
| 04-05 | 15 | 重点テーマ：適用課題 | 状態を観測でき、兆候に応じて保全Actionを変えられる業務に適する |
| 04-06 | 16 | 重点テーマ：期待効果 | 設備Evidenceを点検・交換・保守Decisionへ変換して価値を生む |
| 04-07 | 17 | PoC Workflow | Prediction QuestionとSplit / Holdout設計をModelより先に固定する |
| 04-08 | 18 | Model Selection | データ特性・性能・説明性・運用制約のバランスで選ぶ |
| 04-09 | 19 | Evaluation | 未知データ性能・Calibration・Error Pattern・Business Utilityで評価する |
| 04-10 | 20 | Output / Gate | 利用条件・制約まで含むEvidence PackageでNext Phaseを判断する |

## 編集時の判断基準

- Section全体は `定義 → 適用条件 → 価値発現 → 重点テーマ（定義 → 適用条件 → 期待効果） → 検証Workflow → Model Selection → Evaluation → Evidence Package` の順に進める。
- 04-01〜04-03ではPredictiveのサービスScopeを広く示し、04-04〜04-06は「当チームの重点テーマ」として設備保全を深掘る。重点テーマをPredictiveサービス全体のScopeと同一視しない。
- 04-04〜04-06ではアルゴリズムより、設備Data・分析Output・保全Decision・期待効果の接続を優先する。
- Algorithm名や指標一覧を増やす場合も、Prediction Question・Decision Utilityとの関係を説明できるものに限定する。
- 新しい評価項目は「未知データで再現するか」「誤り方を業務で許容できるか」「Decisionを改善できるか」のどこに寄与するかを明確にする。

## Section Transition

**PredictiveはOutcomeが分かる前の見通しや状態Evidenceを使ってDecisionを改善する。設備領域でも「どの設備が故障しそうか」「どの設備状態が通常と異なるか」には答えられる。一方、「保全施策を変えると故障・停止がどれだけ減るか」のようにTreatmentによるOutcome変化を判断したい場合、Prediction / Detectionだけでは答えられない。Section 05では、Treatmentの介入効果をEstimandとして定義し、Identificationから妥当性確認まで行うCausal PoCへ進む。**
