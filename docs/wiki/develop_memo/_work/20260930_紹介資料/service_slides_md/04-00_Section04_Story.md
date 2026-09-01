# Section 04 Story｜予測分析PoC

## Polaris

**予測分析は、Decision時点で利用可能な情報から未知・将来のOutcomeを予測し、その不確実性を含むPredictionをDecision Ruleへ組み込んでOutcome確定前のActionを改善する。PoCでは、Prediction QuestionとSplit / Validation設計をモデル選定より先に固定し、未知データでの再現性、Calibration、Error Pattern、Business Utilityを評価し、モデルだけでなく利用条件・制約をEvidence Packageとして次フェーズ判断へ渡す。**

## このセクションの役割

- Section 01〜03で定義したPredictiveの意味とDecision起点のPoC設計を、予測分析固有のWorkflowへ具体化する。
- 予測分析が価値を持つ業務条件を、業界ではなくDecision / Actionの構造として整理する。
- Prediction Errorを前提に、PredictionをDecision Ruleと反復Actionへ組み込むことでKPIの期待値を改善する価値発現メカニズムを示す。
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

4. **Predictive PoCでは、Modelより先にPrediction Questionと検証設計を固定する。**
   - Workflowは `Prediction Question → Target / Feature Definition → Split Design → Preprocessing / Baseline → Modeling → Holdout Evaluation → Error Analysis / Explainability → Business Decision`。
   - 誰について、いつ時点で、何を、どこまで先を予測するかを明確にする。
   - Random / Time / Group等のSplitはData Generating Processに合わせ、Holdoutを学習・Model Selectionから分離する。
   - 単純Ruleや現行判断をBaselineとして置き、複雑なModelの増分価値を確認する。

5. **モデル選定は「高度さ」ではなく、課題と運用条件へのFitで行う。**
   - Data Structure、非線形性、Sample Size、欠損、必要性能、説明性、推論時間、更新頻度等からModel Familyと複雑度を選ぶ。
   - Linear / Logistic、Tree、Random Forest、Gradient Boosting、Time-series等は候補であり、手法名自体を価値にしない。
   - Baselineより複雑にする増分価値、Calibration、安定性、解釈性、推論Costを合わせて判断する。

6. **モデル評価は、単一Accuracyではなく4層で行う。**
   - **Discrimination / Error**：AUROC、AUPRC、MAE、RMSE等を目的に応じて使う。
   - **Calibration**：Prediction Probabilityと実発生率の整合を確認する。
   - **Segment / Error Analysis**：重要Segment・期間・条件でどのように失敗するかを確認する。
   - **Business Utility**：Threshold、Ranking、誤判定Cost、Capacity、Action Value等を含め、Predictionを業務に使えるかを評価する。
   - ExplainabilityはModel挙動の理解に使うが、因果効果として解釈しない。

7. **Predictive PoCの成果は、モデルファイルではなく利用可否を判断できるEvidence Packageである。**
   - Prediction Question / Data Assessment。
   - Baseline / Candidate Models。
   - Holdout Performance / Calibration。
   - Error Analysis / Explainability。
   - 適用範囲・利用条件・制約。
   - これらをもとに `GO / ADDITIONAL VALIDATION / NO-GO` を判断し、本番化、データ追加、設計見直し、終了等へ接続する。

## Must Keep｜編集で崩してはいけない境界

- Predictiveで利用するFeatureとOutcomeの関係は、因果関係である必要はない。予測上の関連を介入効果へ読み替えない。
- **高Riskな対象 ≠ 特定施策で最も改善する対象**。施策効果によるTargetingはCausal Questionとして扱う。
- Business上の適用候補であることと、実際に十分なPrediction Performanceが得られることを分けて検証する。
- Future / Target Leakage、不適切なSplit、Holdoutの再利用により見かけの性能を過大評価しない。
- 「最も複雑なModel」「最高Accuracy」を自動的な最適解としない。
- SHAP等のExplainabilityを原因説明として扱わない。
- Prediction PerformanceとBusiness Outcome改善を同義にしない。
- No-GoやAdditional Validationを失敗扱いせず、Evidenceに基づくNext Phase判断として扱う。

## Slide Mapping

| Slide | Story上の役割 | Core Claim |
|---|---|---|
| 04-01 | Predictiveの定義 | Decision時点の情報から未知・将来Outcomeを予測し、事前判断へ使う |
| 04-02 | 適用条件 | ActionabilityとPrediction Errorを業務で扱える構造を持つ課題に適する |
| 04-03 | 価値発現 | 誤りを含むPredictionでも多数のDecision改善を累積してKPI価値へ接続する |
| 04-04 | PoC Workflow | Prediction QuestionとSplit / Holdout設計をModelより先に固定する |
| 04-05 | Model Selection | データ特性・性能・説明性・運用制約のバランスで選ぶ |
| 04-06 | Evaluation | 未知データ性能・Calibration・Error Pattern・Business Utilityで評価する |
| 04-07 | Output / Gate | 利用条件・制約まで含むEvidence PackageでNext Phaseを判断する |

## 編集時の判断基準

- Section全体は `定義 → 適用条件 → 価値発現 → 検証Workflow → Model Selection → Evaluation → Evidence Package` の順に進める。
- Algorithm名や指標一覧を増やす場合も、Prediction Question・Decision Utilityとの関係を説明できるものに限定する。
- 具体例はCustomer / Quality / Operations / Maintenance等へ展開可能だが、特定Use CaseをサービスScopeそのものとして見せない。
- 新しい評価項目は「未知データで再現するか」「誤り方を業務で許容できるか」「Decisionを改善できるか」のどこに寄与するかを明確にする。

## Section Transition

**PredictiveはOutcomeが分かる前の見通しを使ってDecisionを改善する。一方、「施策を実施したらOutcomeがどれだけ変わるか」を判断したい場合、Predictionだけでは答えられない。Section 05では、Treatmentの介入効果をEstimandとして定義し、Identificationから妥当性確認まで行うCausal PoCへ進む。**
