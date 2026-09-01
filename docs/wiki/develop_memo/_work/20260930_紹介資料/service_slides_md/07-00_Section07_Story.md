# Section 07 Story｜Predictive / Causal PoC適用イメージ

## Polaris

**具体例では、PredictiveもCausalもBusiness Questionから始まりDecision / Actionで閉じることを対称に示す。Predictiveは将来Riskを予測して優先対象等を変える一方、Causalは介入の増分効果をIdentificationしDiagnostics / Sensitivityまで確認して施策継続・対象・配分を判断する。両者の問い・Evidence・評価を混同しない。**

## このセクションの役割

- Section 01〜06で説明した抽象的な設計原則を、Predictive / Causalそれぞれ一つのPoC Storyへ具体化する。
- 2つの例を同じレイアウト系統で見せ、共通する `Business Question → Analysis → Decision / Action` と、異なるAnalysis Question / Evidenceを比較可能にする。
- PredictiveのRisk PredictionとCausalのTreatment Effectを意図的に分け、両分析の補完関係を再確認する。
- 最後に、実案件ではこのStoryをInitial HearingとData確認から具体的なScopeへ落とすことをSection 08へつなぐ。

## Storyline

1. **Predictiveの適用例は、将来Riskを事前Actionへ接続する。**
   - Business Question：例として「解約を減らしたい」。
   - Prediction Question：Decision時点の情報から、所定期間内に誰が解約しそうかを予測する。
   - Data / Model：利用履歴、契約、問い合わせ等、予測時点で利用可能な情報からPredictionを作る。
   - Prediction：顧客別Churn Probability / Risk。
   - Decision / Action：対応可能件数、Threshold、誤判定Cost等を考慮して優先対象へFollow-upする。
   - PoC評価：Prediction Performanceだけでなく、CapacityやDecision Utilityまで確認する。

2. **Causalの適用例は、介入の増分効果を施策Decisionへ接続する。**
   - Business Question：例として「Campaign投資を最適化したい」。
   - Causal Question / Estimand：Campaignを実施したことによる購買等のIncremental Effectを定義する。
   - Causal Design：Treatment、Outcome、Population、Time、Confounder等を整理する。
   - Identification / Estimation：施策割付の仕組みと利用可能Dataから比較可能性を作り、Effectを推定する。
   - Diagnostics / Sensitivity：Assumptionへの整合性と結論の頑健性を確認する。
   - Decision / Action：施策継続・変更、対象選定、Budget / Resource配分を判断する。

3. **2つの例は、同じBusiness課題でも異なる問いへ分かれ得ることを再確認する。**
   - Predictiveが答えるのは「誰が起こしそうか」「何が起こりそうか」。
   - Causalが答えるのは「施策によってどれだけ変わるか」「誰に施策が効くか」。
   - **High Riskな対象 ≠ High Treatment Effectな対象**であるため、Risk Rankingをそのまま施策効果Targetingへ使わない。
   - 必要に応じてPredictiveでRiskを把握した後、Causalで候補施策のEffectを検討するなど補完的に利用できる。

4. **適用例でも、成立しない可能性をPoC成果として扱う。**
   - PredictiveではLeakageを除いたHoldout PerformanceやDecision Utilityが不十分な場合がある。
   - Causalでは利用可能な観測Dataから目的EstimandをIdentificationできない場合がある。
   - 「分析が成立しない / 追加検証が必要」という結論も、次フェーズ判断に必要なEvidenceである。

## Must Keep｜編集で崩してはいけない境界

- 解約・Campaignは説明用のConcept Anchorであり、サービスScopeをCRM / Marketingへ限定しない。
- 実績として確認されていない効果額、改善率、精度等の架空数値を置かない。
- Predictive例でRiskをTreatment Effectとして解釈しない。
- Causal例で単純な施策実施群 / 非実施群のOutcome差を、そのまま因果効果としない。
- Causal例ではIdentificationとDiagnostics / Sensitivityを省略しない。EstimatorだけのStoryへ縮退させない。
- どちらの例もAnalysis Resultで終わらず、Decision / Actionまで接続する。

## Slide Mapping

| Slide | Story上の役割 | Core Claim |
|---|---|---|
| 07-01 | Predictive適用例 | 将来Riskを予測し、対応対象の優先順位等のActionへ接続してPoC評価する |
| 07-02 | Causal適用例 | 施策のIncremental Effectを識別・検証し、施策継続・対象・配分へ接続する |

## 編集時の判断基準

- 2枚は可能な限り対称な構造で保ち、どこが共通でどこが異なるかを比較しやすくする。
- 共通部分はBusiness QuestionとDecision / Action、相違部分はAnalysis Question、成立条件、Evidence / Validationとして整理する。
- 別Use Caseへ差し替える場合も、Predictive側はOutcome前のPrediction利用、Causal側はTreatment EffectのIdentificationという核心を保持する。

## Section Transition

**具体的なPoC像を示した後は、実案件で何を確認すればこのScopeへ到達できるかを明確にする。Section 08では、Initial HearingからBusiness Question / Decision、Data Availability、Analysis Feasibility / Riskを確認し、Scope・成果物・Success Criteriaを合意してPoC開始へ進む。**
