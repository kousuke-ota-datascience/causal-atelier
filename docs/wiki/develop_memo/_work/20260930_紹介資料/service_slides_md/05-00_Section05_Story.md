# Section 05 Story｜因果推論PoC

## Polaris

**因果推論は、観測された関連ではなくTreatmentを変えたときのOutcome変化をEstimandとして定義し、因果構造と仮定に基づくIdentificationを成立させたうえでEstimationを行う。PoCではEffect Estimate単体ではなく、不確実性・Diagnostics・Refutation・Sensitivityを含むEvidence Stackから、どの前提のもとでどこまで効果を主張し、どの施策Decisionへ使えるかを判断する。**

## このセクションの役割

- Section 04で示した「何が起こりそうか」を扱うPredictiveから、「何をするとどう変わるか」を扱うCausalへ問いを切り替える。
- Predictiveでは答えられない介入の問いを、CounterfactualとTreatment Effectの意味論から定義する。
- 因果推論に適する業務課題を、明確なTreatment / Outcome / Population / Comparisonを持つDecisionとして整理する。
- Estimatorや手法名より先に、Causal Question、Estimand、Causal Structure / Assumptions、Identificationを設計する必要性を示す。
- Effect Estimateだけでなく、Diagnostics / Refutation / Sensitivityを含むEvidence StackをPoC成果として、施策判断とNext Phaseへ接続する。

## Section Entry｜Section 04からの接続

Section 04では、Prediction Question、未知データでのPerformance、Failure / Utility、利用条件、未検証事項をEvidence Packageとして統合し、Predictive PoCのNext Phaseを判断した。

そのうえで、業務上の問いが「誰が解約しそうか」「どの設備が故障しそうか」のようなOutcome Predictionではなく、**「Retention施策を行うと解約はどれだけ減るか」「保全施策を変えると故障はどれだけ減るか」**である場合、Predictionだけでは直接答えられない。

Section 05では、Treatmentを変えた場合のCounterfactual Outcome差を対象とするCausal PoCへ進む。

## Storyline

1. **因果推論が扱うのはObservationではなくIntervention / Counterfactualである。**
   - 観測データでTreatmentが異なる群のOutcomeが違うことは「関連」を示すが、その差がTreatmentによる変化とは限らない。
   - 因果効果は、同じ対象または同じ対象PopulationについてTreatment状態を変えた場合にOutcomeがどう変わるか、という反実仮想の比較を対象とする。
   - 同じUnitについて複数Treatment状態のPotential Outcomeを同時には観測できないため、妥当なCounterfactualを構成するDesign / Assumptionが必要になる。

2. **Prediction RiskとTreatment Effectは別物である。**
   - 「結果が悪くなりそうな対象」と「施策によって結果を改善できる対象」は一致しない。
   - 代表例としてCustomer Retentionでは、`解約しそうな顧客` と `Retention施策によって解約が減る顧客` を区別する。
   - High RiskでもTreatment Effectが小さい対象は施策優先度が低い場合があり、Baseline Riskが低くてもEffectが大きい対象は改善余地がある。
   - 「誰が起こすか」ではなく「誰に何をすべきか」を判断する場合、Incremental Effectを扱うCausal Questionが必要になる。

3. **因果推論が適するのは、比較したい介入選択肢が明確な業務である。**
   - 施策を実施する / しない、Process Ruleを変更する / 維持する、工程条件を変える / 維持する等のChoiceを比較する。
   - Treatment、Outcome、対象Population、Comparisonを定義できることが入口となる。
   - 「原因を知りたい」という曖昧な問いをそのまま扱わず、実際のDecisionに対応する介入問いへ具体化する。
   - RCT / A-B Testが可能なら有力な選択肢となるが、安全・Cost・倫理・時間・制度等により観測データでのCausal Inferenceが必要になる場合がある。
   - 代表例はCustomer Retention、Product / Feature Change、Operational Process Change、Manufacturing Quality等とし、特定DomainをサービスScopeそのものとして見せない。

4. **因果推論の価値は、介入の増分効果と不確実性を施策Decisionへ使うことにある。**
   - `施策候補 / 対象群 → 因果効果・異質性 → Effect + Uncertaintyの比較 → 施策選択・対象選択・投資配分` と接続する。
   - 平均効果だけでなく、Decision上必要で妥当な場合にはCATE / HTE等のEffect Heterogeneityを検討する。
   - 無効施策を抑制し、増分効果の高い介入や対象へResourceを集中する判断を支援する。
   - Effect Estimateが得られたことだけでROIやBusiness Outcomeを保証しない。実際のBusiness Outcomeは、施策実行、Cost、Capacity、運用条件等を介して決まる。

5. **因果PoCでは、Estimatorを選ぶ前の設計が分析の意味を決める。**
   - Workflowは `Causal Question → Treatment / Outcome / Population / Time / Contrast → Estimand → Causal Structure / Assumptions → Identification → Estimation → Diagnostics / Refutation → Sensitivity → Interpretation / Decision`。
   - 手法起点で「Propensity Scoreを使う」「Causal MLを使う」と始めず、何の効果をどの前提で推定するのかを先に固定する。
   - Identificationが成立しない場合は、Estimatorの高度化へ進むのではなく、Question / Data / Designの見直しや追加検証を選択する。

6. **Causal QuestionをEstimandまで具体化する。**
   - **Treatment**：何を変えるか。
   - **Outcome**：何を改善・評価するか。
   - **Population**：誰に対する効果か。
   - **Time**：どの時点・期間の効果か。
   - **Contrast**：どのTreatment状態同士を比較するか。
   - これらを踏まえてATE / ATT / CATE等、Decisionに対応するEstimandを定義する。
   - ATE / ATT / CATEはEstimator名ではなく、「誰について、何と何を比べた効果を知るか」を定める対象量である。

7. **因果構造とAssumptionを可視化し、調整変数を設計する。**
   - Confounder、Mediator、Collider、Temporal Ordering等の役割を分けて整理する。
   - 「変数を多く入れるほど安全」ではなく、EstimandとCausal Structureに基づいてAdjustment Setを決める。
   - Pre-treatment ConfounderはAdjustment候補となる一方、Mediatorの調整はTotal Effectとは異なるEstimandへ変える場合があり、ColliderへのConditioningはBiasを導入し得る。
   - DAGは真実をデータから自動発見する装置ではなく、Domain KnowledgeとData Generating Processに関する仮定を明示する道具である。

8. **IdentificationとEstimationを分離する。**
   - **Identification**：Assumptionのもとで目的のCausal EffectをObserved Data Distributionから表現できるか。
   - **Estimation**：Identified Estimandを有限標本からどのように数値推定するか。
   - Identificationが成立しない場合、Estimatorを高度化しても目的の因果効果は得られない。
   - 同じIdentification Strategyに対して、複数のEstimatorを比較できる場合がある。

9. **Identification StrategyはData Generating Processと成立条件から選ぶ。**
   - Randomized Assignmentが可能：Randomized Comparison / RCT / A-B Test。
   - 必要なPre-treatment Confounderを十分観測しBackdoor Adjustmentが妥当：Covariate Adjustment。その後のEstimationとしてRegression / G-formula、Weighting、Matching、Doubly Robust等を検討する。
   - 前後×比較群：Difference-in-Differences。
   - Threshold Assignment：Regression Discontinuity。
   - Valid Instrumentが存在：Instrumental Variable。
   - Single Treated Unit × Donor Pool × Time：Synthetic Control等。
   - 各Strategyには異なるAssumptionがあり、手法名だけで妥当性は決まらない。
   - Causal MLもIdentification Assumptionを不要にはしない。

10. **因果PoCの成果はEffect EstimateではなくEvidence Stackである。**
    - **Causal Question / Estimand**。
    - **Identification Strategy / Assumptions**。
    - **Effect Estimate + Uncertainty**。
    - **Diagnostics / Assumption-aligned Check**：Balance、Overlap / Positivity、Weight Distribution、Effective Sample Size、Pre-trend等をDesignに応じて確認する。
    - **Sensitivity / Refutation**：未観測交絡、Adjustment Set、Window、Trimming、Estimator等への依存性やPlaceboを確認する。
    - **Business Interpretation / Claim Scope**：どの前提のもとで、どこまで主張でき、どのDecisionに使えるかを整理する。
    - Diagnosticsは未観測交絡等の識別仮定を「証明」するものではない。検証可能な含意とデータ上の問題を確認し、残る仮定依存性はSensitivityとClaim Scopeへ明示する。
    - Go / Additional Validation / No-GoはEffect Sizeや統計的有意差だけでなくEvidence Stack全体から判断する。

## Must Keep｜編集で崩してはいけない境界

- 因果推論を「AIが原因を自動発見する技術」と表現しない。
- 観測された群間差・Correlation・Predictive Importanceを、そのままTreatment Effectと解釈しない。
- RCTと観測研究を同じ前提で扱わない。観測データではIdentification Assumptionが必要である。
- EstimandをEstimatorより先に定義する。ATE / ATT / CATE等を単なる手法名の一覧にしない。
- DAGを真の因果構造の自動確定として扱わない。
- Confounder / Mediator / Colliderを「すべて調整すべき変数」として扱わない。
- Identification Failureを複雑なEstimatorで解消できると見せない。
- Causal MLを「仮定不要の因果推論」と表現しない。
- Diagnosticsで未観測の識別仮定が証明できると表現しない。
- Effect Estimate、`p < 0.05`、統計的有意差だけをPoC成功基準にしない。
- Causalの成果は「効果が出た / 出なかった」の二値ではなく、主張可能範囲・限界・残存リスクまで含める。

## Slide Mapping

| File | Deck Slide | Story上の役割 | Core Claim |
|---|---:|---|---|
| 05-01 | 18 | Causalの定義 | ObservationではなくTreatmentを変えたときのCounterfactual Effectを扱う |
| 05-02 | 19 | Predictiveとの境界 | High RiskとHigh Treatment Effectは一致しない |
| 05-03 | 20 | 適用課題 | 明確な介入・比較・Outcomeを持つDecisionに適する |
| 05-04 | 21 | 価値発現 | Incremental Effectと不確実性を施策・対象・投資判断へ使う |
| 05-05 | 22 | PoC Workflow | Estimatorより先にQuestion / Estimand / Structure / Identificationを設計する |
| 05-06 | 23 | Estimand | Treatment / Outcome / Population / Time / Contrastから効果対象を固定する |
| 05-07 | 24 | Causal Structure | 時間順序と変数役割からAdjustmentとAssumptionを設計する |
| 05-08 | 25 | Identification / Estimation | 識別可能性と有限標本推定を別問題として扱う |
| 05-09 | 26 | Strategy Selection | Data Generating ProcessとAssumptionからIdentification Strategyを選ぶ |
| 05-10 | 27 | Evidence / Output | Diagnostics / Sensitivityまで含むEvidence Stackで主張可能範囲を判断する |

## 編集時の判断基準

- Section全体は `反実仮想の定義 → Predictiveとの境界 → 適用条件 / 価値 → Causal Design → Estimand → Structure / Assumption → Identification → Estimation → Validation / Interpretation` の順序を保持する。
- 05-02の主例はCustomer Retentionとし、Prediction RiskとTreatment Effectの差を同じBusiness Issueで示す。
- 05-03ではCustomer / Product / Operations / Manufacturing等へ横展開し、特定Use CaseをサービスScopeそのものとして見せない。
- 手法一覧を追加するときは、必ず「どのData Generating ProcessとAssumptionでIdentificationが成立するか」と「その後にどのEstimatorを使うか」を混同しない。
- 因果の専門性はEstimator数ではなく、Question / Estimand / Identification / Diagnosticsを一貫して設計できることとして表現する。
- Business向け表現に簡略化しても、「どの前提のもとでEffectと解釈できるか」という論点は落とさない。

## Section Transition

**Predictive / Causalそれぞれの分析WorkflowとEvidence Package / Evidence Stackを定義した後は、それらを実際のPoCでどう実装・管理するかを示す。Section 06では、Data ScientistによるScratch + OSSを基本とする実装方針と、Ariadneが分析Context / Workflow / Result / Lineageの構造化・追跡を補助する位置づけを整理する。**
