# Section 08 Story｜PoC開始までの進め方

## Polaris

**PoC開始前は手法を先に決めず、Initial Hearingで背景・現行業務を把握し、Business Question / Decision、Data Availability、Analysis Feasibility / Riskの順に確認する。その結果をもとに対象・期間・成果物・除外事項・Success Criteria・次フェーズ判断を合意してScopeを確定し、PoCを開始する。**

## このセクションの役割

- 資料全体で説明したサービスを、顧客が実際に相談・発注する際の次のActionへ接続する。
- 分析手法を先に固定せず、業務課題・Decision・Dataを確認してからPredictive / Causalの適用可能性とScopeを判断する流れを示す。
- Section 03で示したStart Gateへ至る事前確認を、顧客向けの5ステップとして簡潔に整理する。
- 必要Dataが完全に揃っていなくてもInitial Hearingは開始できる一方、Analysis FeasibilityはData確認後に判断することを明確にする。

## Storyline

1. **Initial Hearing｜まず背景と現行業務を理解する。**
   - 業務背景、解決したい課題、現行Process、意思決定者、既存分析・Rule等を確認する。
   - 「AI / 特定手法を使いたい」をそのままScopeにせず、何を改善したいのかを確認する。

2. **Business Question / Decision｜何を知り、何を決めたいかを整理する。**
   - 誰が何を判断するのか、結果を受けてどのActionを変えたいのかを具体化する。
   - 「何が起こりそうか」を知る必要があるのか、「何をするとどう変わるか」を知る必要があるのかを整理する。
   - この段階でPredictive / Causalの候補を置くが、Dataと成立条件を確認する前に分析手法を確定しない。

3. **Data Availability｜分析に必要なDataが利用可能かを初期確認する。**
   - Data source、対象期間、観測粒度、履歴、主要変数、利用可否、既知の欠損・制約を確認する。
   - Predictiveでは、Prediction時点で利用できるFeatureとTargetを構成できる見込みがあるかを見る。
   - Causalでは、Treatment / Outcome / Populationおよび候補Comparisonを検討できるDataがあるかを見る。
   - ここで行うのは初期Feasibility確認であり、詳細なData AssessmentはPoC内で実施する。

4. **Analysis Feasibility / Risk｜問いに答えられる見込みと主要リスクを確認する。**
   - Predictiveでは、適切なSplit / HoldoutでValidation可能か、LeakageなくPrediction Questionを構成できるかを中心に確認する。
   - Causalでは、目的Estimandを識別するためのDesign / Assumptionを置けるか、Identification可能性を中心に確認する。
   - Data品質、Sample Size、期間、業務協力、Security / Operation等、PoC成立やDeliveryへ影響する主要リスクを整理する。
   - Feasibilityが低い場合は、Data Acquisition、事前調査、Question / Scope変更等を検討する。

5. **Scope・成果物・Success Criteria｜何を検証し、何で次を判断するかを合意する。**
   - 対象Population、期間、Analysis Question、成果物、除外事項等をScopeとして定義する。
   - 分析結果を利用するDecision / Actionと、必要に応じてWHO / WHEN / Decision Ruleを確認する。
   - Success Criteriaは分析成立性・業務利用性・次フェーズ判断の観点で合意する。
   - 本番化だけでなく、追加検証、Data Acquisition、Scope変更、中止等のNext Phaseを判断可能な形にする。
   - ここまで合意した状態をPoC Startとする。

## Must Keep｜編集で崩してはいけない境界

- 最初からModel / Estimator / Productを決めてからBusiness Questionを当てはめない。
- Dataが完全に揃っていないことをInitial Hearing開始不可の条件にしない。一方、Analysis FeasibilityをData未確認のまま断定しない。
- PredictiveのFeasibilityを単なる「MLが学習できるか」とせず、実運用時点に整合したValidation可能性として見る。
- CausalのFeasibilityを単なる「Treatment列とOutcome列があるか」とせず、目的EffectのIdentification可能性として見る。
- Success Criteriaを未検証の高精度・高効果の保証値として扱わない。
- 契約条件・価格等をこのStoryへ混在させず、PoC Scopeを科学的・業務的に合意する流れへ集中する。

## Slide Mapping

| Slide | Story上の役割 | Core Claim |
|---|---|---|
| 08-01 | PoC開始手順 | Hearing → Question / Decision → Data → Feasibility / Risk → Scope / Success Criteriaの順で合意してPoCを開始する |

## 編集時の判断基準

- 5ステップの順序を保持し、手法選定をData / Feasibility確認より前へ出さない。
- 顧客が「次に何を準備・相談すればよいか」が読後に分かる粒度を維持する。
- 詳細なPoC WorkflowはSection 03〜05と重複させず、ここではPoC開始前の合意形成に集中する。
- 新しい確認項目を追加する場合は、Question / Decision、Data、Feasibility / Risk、Scope / Success Criteriaのいずれに属するかを明確にする。

## Closing

**案件ごとのBusiness Questionと利用可能Dataを起点に、Predictive / Causalの適用可能性、検証すべき不確実性、成果物、Success Criteriaを具体化し、意思決定に使えるEvidenceを作るPoC Scopeへ落とし込む。**
