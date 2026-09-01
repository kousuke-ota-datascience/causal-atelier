# Section 05 Story｜因果推論PoC

## Polaris

**因果推論は、観測された関連ではなくTreatmentを変えたときのOutcome変化をEstimandとして定義し、因果構造と仮定に基づくIdentificationを成立させたうえでEstimationを行う。PoCではEffect Estimate単体ではなく、不確実性・Diagnostics・Refutation・Sensitivityを含むEvidence Stackから、どの前提のもとでどこまで効果を主張し、どの施策Decisionへ使えるかを判断する。**

## このセクションの役割

- Predictiveでは答えられない「何をするとどう変わるか」という介入の問いを、CounterfactualとTreatment Effectの意味論から定義する。
- 因果推論に適する業務課題を、明確なTreatment / Outcome / Population / Comparisonを持つDecisionとして整理する。
- Estimatorや手法名より先に、Causal Question、Estimand、Causal Structure / Assumptions、Identificationを設計する必要性を示す。
- Effect Estimateだけでなく、Diagnostics / Refutation / Sensitivityを含むEvidence StackをPoC成果として、施策判断とNext Phaseへ接続する。

## Storyline

1. **因果推論が扱うのはObservationではなくIntervention / Counterfactualである。**
   - 観測データでTreatmentが異なる群のOutcomeが違うことは「関連」を示すが、その差がTreatmentによる変化とは限らない。
   - 因果効果は、同じ対象についてTreatmentを変えた場合にOutcomeがどう変わるか、という反実仮想の比較を対象とする。
   - 同じ対象の複数Treatment状態を同時には観測できないため、比較可能性を作るDesign / Assumptionが必要になる。

2. **Prediction RiskとTreatment Effectは別物である。**
   - 「結果が悪くなりそうな対象」と「施策によって結果を改善できる対象」は一致しない。
   - High RiskでもTreatment Effectが小さい対象は施策優先度が低い場合があり、Baseline Riskが低くてもEffectが大きい対象は改善余地がある。
   - 「誰が起こすか」ではなく「誰に何をすべきか」を判断する場合、Incremental Effectを扱うCausal Questionが必要になる。

3. **因果推論が適するのは、比較したい介入選択肢が明確な業務である。**
   - 施策を実施する / しない、価格を変える / 維持する、Process Ruleを変更する / 維持する等のChoiceを比較する。
   - Treatment、Outcome、対象Population、Comparisonを定義できることが入口となる。
   - 「原因を知りたい」という曖昧な問いをそのまま扱わず、実際のDecisionに対応する介入問いへ具体化する。
   - RCT / A-B Testが可能なら有力な選択肢となるが、安全・Cost・倫理・時間・制度等により観測データでのCausal Inferenceが必要になる場合がある。

4. **因果推論の価値は、介入の増分効果と不確実性を施策Decisionへ使うことにある。**
   - `施策候補 / 対象群 → 因果効果・異質性 → Effect + Uncertaintyの比較 → 施策選択・対象選択・投資配分` と接続する。
   - 平均効果だけでなく、Decision上必要で妥当な場合にはCATE / HTE等のEffect Heterogeneityを検討する。
   - 無効施策を抑制し、増分効果の高い介入や対象へResourceを集中する判断を支援する。
   - Effect Estimateが得られたことだけでROIやBusiness Outcomeを保証しない。

5. **因果PoCでは、Estimatorを選ぶ前の設計が分析の意味を決める。**
   - Workflowは `Causal Question → Treatment / Outcome / Population → Estimand → Causal Structure / Assumptions → Identification → Estimation → Diagnostics / Refutation → Sensitivity → Interpretation / Decision`。
   - 手法起点で「Propensity Scoreを使う」「Causal MLを使う」と始めず、何の効果をどの前提で推定するのかを先に固定する。

6. **Causal QuestionをEstimandまで具体化する。**
   - **Treatment**：何を変えるか。
   - **Outcome**：何を改善・評価するか。
   - **Population**：誰に対する効果か。
   - **Time**：どの時点・期間の効果か。
   - **Contrast**：どのTreatment状態同士を比較するか。
   - これらを踏まえてATE / ATT / CATE等、Decisionに対応するEstimandを定義する。

7. **因果構造とAssumptionを可視化し、調整変数を設計する。**
   - Confounder、Mediator、Collider、Temporal Ordering等の役割を整理する。
   - 「変数を多く入れるほど安全」ではなく、EstimandとCausal Structureに基づいてAdjustment Setを決める。
   - DAGは真実をデータから自動発見する装置ではなく、Domain KnowledgeとData Generating Processに関する仮定を明示する道具である。

8. **IdentificationとEstimationを分離する。**
   - **Identification**：Assumptionのもとで目的のCausal EffectをObserved Data Distributionから表現できるか。
   - **Estimation**：Identified Estimandを有限標本からどのように数値推定するか。
   - Identificationが成立しない場合、Estimatorを高度化しても目的の因果効果は得られない。

9. **Identification StrategyはData Generating Processと成立条件から選ぶ。**
   - Randomization可能：RCT / A-B Test。
   - 交絡を十分観測：Regression / Weighting / Doubly Robust等。
   - 前後×比較群：Difference-in-Differences。
   - Threshold assignment：Regression Discontinuity。
   - External instrument：Instrumental Variable。
   - Single treated unit × time：Synthetic Control等。
   - 各Approachには異なるAssumptionがあり、手法名だけで妥当性は決まらない。
   - Causal MLもIdentification Assumptionを不要にはしない。

10. **因果PoCの成果はEffect EstimateではなくEvidence Stackである。**
    - **Identification Strategy / Assumptions**。
    - **Effect Estimate + Uncertainty**。
    - **Diagnostics / Assumption Check**：Balance、Overlap / Positivity、Weight Distribution、Effective Sample Size、Pre-trend等をDesignに応じて確認。
    - **Sensitivity / Refutation**：未観測交絡、Adjustment Set、Window、Trimming、Estimator等への依存性やPlaceboを確認。
    - **Business Interpretation**：どの前提のもとで、どこまで主張でき、どのDecisionに使えるかを整理する。
    - Go / Additional Validation / No-GoはEffect Sizeや有意差だけでなくEvidence Stack全体から判断する。

## Must Keep｜編集で崩してはいけない境界

- 因果推論を「AIが原因を自動発見する技術」と表現しない。
- 観測された群間差・Correlation・Predictive Importanceを、そのままTreatment Effectと解釈しない。
- RCTと観測研究を同じ前提で扱わない。観測データではIdentification Assumptionが必要である。
- EstimandをEstimatorより先に定義する。ATE / ATT / CATE等を単なる手法名の一覧にしない。
- DAGを真の因果構造の自動確定として扱わない。
- Identification Failureを複雑なEstimatorで解消できると見せない。
- Causal MLを「仮定不要の因果推論」と表現しない。
- Effect Estimate、`p < 0.05`、統計的有意差だけをPoC成功基準にしない。
- Causalの成果は「効果が出た / 出なかった」の二値ではなく、主張可能範囲・限界・残存リスクまで含める。

## Slide Mapping

| Slide | Story上の役割 | Core Claim |
|---|---|---|
| 05-01 | Causalの定義 | ObservationではなくTreatmentを変えたときのCounterfactual Effectを扱う |
| 05-02 | Predictiveとの境界 | High RiskとHigh Treatment Effectは一致しない |
| 05-03 | 適用課題 | 明確な介入・比較・Outcomeを持つDecisionに適する |
| 05-04 | 価値発現 | Incremental Effectと不確実性を施策・対象・投資判断へ使う |
| 05-05 | PoC Workflow | Estimatorより先にQuestion / Estimand / Structure / Identificationを設計する |
| 05-06 | Estimand | Treatment / Outcome / Population / Time / Contrastから効果対象を固定する |
| 05-07 | Causal Structure | 時間順序と変数役割からAdjustmentとAssumptionを設計する |
| 05-08 | Identification / Estimation | 識別可能性と有限標本推定を別問題として扱う |
| 05-09 | Strategy Selection | Data Generating ProcessとAssumptionからIdentification Strategyを選ぶ |
| 05-10 | Evidence / Output | Diagnostics / Sensitivityまで含むEvidence Stackで主張可能範囲を判断する |

## 編集時の判断基準

- Section全体は `反実仮想の定義 → Predictiveとの境界 → 適用条件 / 価値 → Causal Design → Estimand → Structure / Assumption → Identification → Estimation → Validation / Interpretation` の順序を保持する。
- 手法一覧を追加するときは、必ず「どのData Generating ProcessとAssumptionで成立するか」を併記できるものにする。
- 因果の専門性はEstimator数ではなく、Question / Estimand / Identification / Diagnosticsを一貫して設計できることとして表現する。
- Business向け表現に簡略化しても、「どの前提のもとでEffectと解釈できるか」という論点は落とさない。

## Section Transition

**Predictive / Causalそれぞれの分析Workflowを定義した後は、それらを実際のPoCでどう実装・管理するかを示す。Section 06では、Data ScientistによるScratch + OSSを基本とする実装方針と、Ariadneが分析Context / Workflow / Result / Lineageの構造化・追跡を補助する位置づけを整理する。**
