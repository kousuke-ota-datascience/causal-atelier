# 01-04 wk04｜Analysis Apply Case

## 1. 目的

本書は、当チームが提供対象とする以下2系統の分析について、公開Competition、Open Data / Public Dataset、企業公開事例をもとに適用対象を再整理する。

- 予測分析 / Predictive Analytics
- 因果推論 / Causal Inference

目的は、単なるUse Case一覧を作ることではなく、サービス紹介資料で、

```text
Business Question
→ Analysis Target
→ Decision / Action
→ Business Outcome
```

まで説明できる代表例を選定することである。

---

# 2. 基本原則

## 2.1. Predictive

問い：

> **何が起こりそうか？**

対象：

- 将来・未知のOutcome
- Event Probability
- Continuous Value
- Time-to-event
- Future Trajectory
- Risk / Ranking

主なDecision / Action：

- Prioritize
- Allocate
- Schedule
- Plan
- Review / Escalate
- Control / Adjust

## 2.2. Causal

問い：

> **何をするとどう変わるか？**

対象：

- Treatment / InterventionによるOutcomeの変化
- ATE / ATT / CATE等のEstimand
- Intervention間の効果差
- Policy / Treatment Ruleの価値

主なDecision / Action：

- 施策を実施するか
- 施策を継続するか
- 施策A/Bのどちらを選ぶか
- どの対象へ施策を適用するか
- どこへ投資を配分するか

**重要**

Prediction RiskとTreatment Effectは同じではない。

```text
解約しそうな人
≠
Retention施策で解約が減る人
```

---

# 3. Predictive Analyticsの適用例

## 3.1. Customer / Commercial

|Business Question|Prediction Target|Action|Outcome候補|Evidence例|
|---|---|---|---|---|
|誰が解約しそうか|Churn probability|対応対象を優先|対応効率、継続機会|Kaggle Churn、企業Churn事例|
|誰が購入・成約しそうか|Purchase / Response propensity|Lead priority|営業効率|Bank Marketing、COIL 2000|
|誰が再購入しそうか|Repeat purchase|Follow-up / recommendation|継続購買|completejourney、Instacart、Online Retail|
|顧客価値はどの程度になりそうか|Future revenue / value|Resource allocation|高価値顧客管理|Google Analytics Revenue、completejourney|

**Open Data例**

- completejourney
- Olist
- Instacart
- Online Retail / II
- RetailRocket
- Bank Marketing
- COIL 2000

---

## 3.2. Operations / Logistics / Business Process

|Business Question|Prediction Target|Action|Outcome候補|Evidence例|
|---|---|---|---|---|
|どの配送が遅れそうか|Late delivery risk|High-risk shipmentを優先管理|遅延損失、対応工数|DataCo、E-Commerce Shipping、Olist|
|いつCaseが完了しそうか|Completion / Lead time|Escalation、Resource allocation|Lead time短縮|BPI Challenge 2019|
|次に何が起きそうか|Next activity|Process monitoring|Process効率|BPI Challenge 2019|
|どのCaseがDeviationしそうか|Deviation / Rework risk|Review priority|手戻り削減|BPI Challenge 2019|

**示唆**

Predictive Analyticsは顧客・設備だけでなく、企業内部のProcess Event Logにも適用できる。

---

## 3.3. Industrial / Maintenance

|Business Question|Prediction Target|Action|Outcome候補|Evidence例|
|---|---|---|---|---|
|どの設備が故障しそうか|Failure probability|点検優先順位|停止損失削減|AI4I、企業Predictive Maintenance事例|
|あとどの程度使えるか|RUL|保守/交換時期|過剰保全・停止削減|NASA C-MAPSS、IMS Bearings|
|どの設備が劣化しているか|Future health / condition|Maintenance schedule|稼働率改善|Hydraulic、Milling Wear|

---

## 3.4. Quality

|Business Question|Prediction Target|Action|Outcome候補|Evidence例|
|---|---|---|---|---|
|どの製品が不良になりそうか|Defect / Pass-Fail|重点検査|検査効率、不良流出削減|SECOM、Steel Plates Faults|
|品質指標はどの程度になるか|Quality metric|Process review|品質・歩留まり|企業Quality Inspection事例|

---

## 3.5. Risk / Finance

- Fraud Risk
- Default / Delinquency Risk
- Bankruptcy Risk
- Insurance Claim Risk
- Accident Risk

ActionはReview / Escalation / Monitoring Priority等。

**留保**

Credit、Insurance等は規制・Fairness・Explainability論点が大きいため、Intro Slideの代表例としては優先度を下げる。

---

## 3.6. Energy / Environment / Mobility

- Electricity Consumption
- Emission / Air Quality
- Traffic Flow
- Travel Time
- Trajectory

主にPlanning / Control / Allocationへ接続する。

当チームのサービスScopeとの混同を避けるため、需要予測は代表例に用いない。

---

# 4. Causal Inferenceの適用例

## 4.1. Marketing / CRM施策効果

### Business Question

- Campaignを実施するとConversionはどの程度変わるか
- Couponを配布すると購買はどの程度増えるか
- Retention施策を行うと解約はどの程度減るか
- どの顧客Segmentで施策効果が大きいか

### Causal Target

- ATE / ATT
- CATE / HTE
- Uplift

### Decision / Action

- 施策実施 / 継続
- 施策対象の見直し
- Budget Allocation

### Open Data / Benchmark

**Criteo Uplift Prediction Dataset**

- Randomized incrementality tests由来
- Treatment indicator + Conversion / Visit label
- Uplift / Heterogeneous Treatment EffectのBenchmark

出所：
https://ailab.criteo.com/criteo-uplift-prediction-dataset/

**completejourney**

- Campaign / Coupon / Promotion関連Tableを持つため、施策効果分析のQuestion設定候補になる
- ただし観測Dataであり、Campaign exposureがあるだけで因果効果を識別できるわけではない

---

## 4.2. Product / Feature Change

### Business Question

- 新Featureを導入するとEngagementは変わるか
- UI変更でConversionは改善するか
- Algorithm変更がMarketplace指標へどのような影響を与えるか

### Design / Method候補

- A/B test
- A/B/N test
- CUPED等の実験精度改善
- Heterogeneous Treatment Effect

### 企業公開事例

UberはExperimentation PlatformをProduct Feature、App Design、Marketing Campaign、Promotion、ML Model等の効果評価に利用している。

また、平均効果だけでなくTreatment Effect HeterogeneityやQuantile Treatment Effect等も扱う事例を公開している。

出所：

- Uber, Under the Hood of Uber’s Experimentation Platform  
  https://www.uber.com/in/en/blog/xp/
- Uber, Using Causal Inference to Improve the Uber User Experience  
  https://www.uber.com/gb/en/blog/causal-inference-at-uber/
- Uber, Analyzing Experiment Outcomes: Beyond Average Treatment Effects  
  https://www.uber.com/us/en/blog/analyzing-experiment-outcomes/

---

## 4.3. Operational Intervention / Process Change

### Business Question

- Process Ruleを変更するとLead Timeは短縮するか
- Inspection Ruleを変えるとDefect / Costは変わるか
- 配送遅延が将来Engagementへ与える因果影響はどの程度か

### Method候補

- Randomized Experiment
- Difference-in-Differences
- Synthetic Control
- Matching / Weighting / Regression adjustment

### 企業公開事例

Uberは、Food Delivery Delayが将来のCustomer Engagementへ与える影響のように、倫理・顧客体験上ランダム化しにくい問題へObservational Causal Inferenceを利用する例を公開している。

出所：
https://www.uber.com/au/en/blog/causal-inference-at-uber/

---

## 4.4. Training / Policy / Program Evaluation

### Business Question

- Training Programで所得・成果はどの程度変化したか
- Policy /制度導入の効果はあったか

### Benchmark

**LaLonde / National Supported Work**

- Job Training ProgramのTreatment Effect推定で広く利用されるCausal Inference Benchmark
- Experimental treated/controlとnon-experimental comparisonを用いたMethod Evaluationにも利用される

出所：
https://users.nber.org/~rdehejia/nswdata.html

---

## 4.5. Causal Method Competition / Benchmark

### ACIC Data Challenge

ACIC Data ChallengeはCausal Effect EstimationのMethod比較を目的としたCompetitionである。

対象例：

- ATE
- CATE
- Subgroup Effect
- Multiple Treatments
- Counterfactual Outcome

2026 Challengeでは複数Treatment下でiCATE / sCATE / subgroup CATE / PATE等を評価対象としている。

出所：
https://acic2026datachallenge.github.io/

過去Challengeでもquasi-real-world Dataを用いたATE推定等が扱われている。

出所：
https://sites.google.com/view/acic2019datachallenge/

---

## 4.6. Counterfactual Policy / Ranking

### Business Question

- Logged Interaction Dataから別Policyを採用した場合の成果を評価できるか
- Advertising / Recommendation Policyを変更するとUtilityはどう変わるか

### Dataset例

CriteoはCounterfactual Algorithm Evaluation用Datasetを公開している。

出所：
https://ailab.criteo.com/dataset-release-evaluation-counterfactual-algorithms/

**留保**

これは単純なATE推定よりPolicy Learning / Off-policy Evaluationに近く、Intro SlideではAdvanced Use Caseとして扱う。

---

# 5. Predictive / Causalを同じ業務課題で対にする

サービス紹介資料では、別々の業界例を置くより、同じBusiness Issueを2種類のQuestionへ分けると違いが明確になる。

## 5.1. Customer Retention

```text
業務課題
解約を減らしたい

Predictive
誰が解約しそうか？
→ 対応対象を優先

Causal
Retention施策で解約はどれだけ減るか？
→ 施策実施・対象を判断
```

**評価**：非常に強い。

- Question差が明確
- Customer Domainで理解しやすい
- Predictive / Causal双方に公開事例がある

---

## 5.2. Delivery / Logistics

```text
業務課題
配送品質を改善したい

Predictive
どの配送が遅れそうか？
→ High-risk shipmentを優先管理

Causal
配送Process変更で遅延はどれだけ減るか？
→ Process変更を判断
```

**評価**：強い。

- Operations Domainを表現できる
- Olist / DataCo等Open Dataが豊富
- Business Processへ接続しやすい

---

## 5.3. Manufacturing Quality

```text
業務課題
不良を減らしたい

Predictive
どの製品が不良になりそうか？
→ 重点検査

Causal
工程条件を変えると不良率はどう変わるか？
→ 工程変更を判断
```

**評価**：非常に強い。

- Industrial / Qualityを表現
- Prediction → Inspection
- Causal → Process Intervention

---

## 5.4. Equipment Maintenance

```text
業務課題
設備停止を減らしたい

Predictive
どの設備が停止しそうか？
→ 点検優先順位

Causal
保守施策で停止率はどれだけ下がるか？
→ 保守施策を判断
```

**評価**：強いがIndustrial Biasあり。

---

# 6. サービス紹介資料の代表例選定基準

以下を評価する。

1. Question Clarity
2. Actionability
3. Business Outcome Clarity
4. Predictive / Causal Contrast
5. Domain Neutrality
6. Scope Misunderstanding Risk
7. Data Intuitiveness
8. Ethical / Regulatory Burden
9. Business Process Proximity
10. Evidence Availability

---

# 7. 代表例の評価

5段階の設計仮説。

|候補|Question|Action|Outcome|P/C対称性|Domain Neutrality|Business Process proximity|総評|
|---|---:|---:|---:|---:|---:|---:|---|
|解約|5|5|4|5|3|5|Concept Anchorとして最有力|
|配送遅延|5|5|5|5|4|5|Operations代表として非常に強い|
|品質/不良|5|5|5|5|2|4|Industrial代表として非常に強い|
|故障/停止|5|5|5|4|2|4|Maintenance代表として強い|
|Fraud|5|5|5|2|2|5|Predictiveには強いがCausal対称性弱い|
|Credit|5|5|5|3|2|5|規制論点が重い|
|電力量|4|4|4|3|2|4|Forecasting幅を示す補助例|

---

# 8. 結論

## 8.1. 01-01〜01-04で「故障予測」を共通主例にする必要はない

故障予測は、

- Questionが明確
- Actionが明確
- Business Outcomeが明確

という点で優秀である。

しかしOpen Data / Competition / Enterprise Caseを広げると、**Customer、Operations、Qualityでも同等に強い例が存在する**。

そのため、故障予測をPredictive Service全体の代表とするより、Industrial Anchorの一つと位置付ける方が妥当である。

## 8.2. Concept Anchorには「解約」が最も使いやすい

01-01〜01-03でPredictive / Causalの違いを説明する場合、

```text
誰が解約しそうか？
vs.
どの施策で解約を減らせるか？
```

は同一OutcomeでQuestionのみを変えられるため、意味論の比較が最もcleanである。

## 8.3. 01-04は複数のValue Chainを見せる方がよい

Business Outcome説明では、一つのDomainだけを示すより、

```text
Predictive
配送遅延 → 優先対応 → 遅延損失 / 対応工数
品質Risk → 重点検査 → 不良 / 検査Cost
解約Risk → 対応優先 → 対応Resource効率

Causal
Retention施策 → 継続率 / Incremental Revenue
Process変更 → Lead Time / Cost
Quality施策 → 不良率 / Quality Cost
```

のように、分析結果がActionを介してOutcomeへつながる複数例を短く示す方が適用範囲を誤解させにくい。

---

# 9. Slide別推奨

## 01-01

**解約をConcept AnchorとしてPredictive / Causalを対称にする。**

```text
Predictive
解約リスクを予測
→ 対応対象を決める

Causal
Retention施策の効果を推定
→ 施策実施を決める
```

補助的に「設備・品質・物流等にも適用」と記載する。

## 01-02

現行の解約例を維持する。

## 01-03

主図は抽象比較を維持し、Supporting Logicで、

- 解約Risk ≠ Retention Effect
- 不良Risk ≠ Process Change Effect

を補助例として入れる。

## 01-04

**故障一本から外し、Customer / Industrial / Operationsの複数Value Chainへ拡張する。**

Predictive側は、

- 解約Risk
- 品質Risk
- 配送遅延Risk

Causal側は、

- Retention施策
- Quality / Process Intervention
- Operational Process Change

を候補とする。

---

# 10. 主要出所

## Competition / Benchmark

- ACIC 2026 Data Challenge  
  https://acic2026datachallenge.github.io/
- ACIC 2019 Data Challenge  
  https://sites.google.com/view/acic2019datachallenge/
- Kaggle Predict Customer Churn  
  https://www.kaggle.com/competitions/playground-series-s6e3
- Kaggle Home Credit Default Risk  
  https://www.kaggle.com/competitions/home-credit-default-risk
- Kaggle IEEE-CIS Fraud Detection  
  https://www.kaggle.com/competitions/ieee-fraud-detection

## Open Data / Public Dataset

- Criteo Uplift Prediction Dataset  
  https://ailab.criteo.com/criteo-uplift-prediction-dataset/
- Criteo Counterfactual Evaluation Dataset  
  https://ailab.criteo.com/dataset-release-evaluation-counterfactual-algorithms/
- LaLonde / NSW Data  
  https://users.nber.org/~rdehejia/nswdata.html
- completejourney  
  https://github.com/bradleyboehmke/completejourney
- BPI Challenge 2019  
  https://research.tue.nl/en/datasets/bpi-challenge-2019/
- Olist  
  https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
- DataCo  
  https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis
- UCI SECOM  
  https://archive.ics.uci.edu/dataset/179/secom
- NASA C-MAPSS  
  https://data.nasa.gov/dataset/cmapss-jet-engine-simulated-data

## Enterprise Case

- Uber Experimentation Platform  
  https://www.uber.com/in/en/blog/xp/
- Uber Causal Inference  
  https://www.uber.com/gb/en/blog/causal-inference-at-uber/
- Uber Causal Inference with Observational Data  
  https://www.uber.com/au/en/blog/causal-inference-at-uber/
- Uber Quantile Treatment Effects  
  https://www.uber.com/us/en/blog/analyzing-experiment-outcomes/
- Google Cloud TOMRA  
  https://cloud.google.com/customers/tomra
- Google Cloud Talgo  
  https://cloud.google.com/customers/talgo
- Google Cloud Hitachi  
  https://cloud.google.com/customers/hitachi
- AWS Amazon Buyer Fraud  
  https://aws.amazon.com/solutions/case-studies/amazonbuyerfraud/

---

# 11. 留保

- Open DataにTreatment / Campaign / Process Eventが含まれていても、因果効果が自動的にIdentificationできるわけではない。
- Causal適用には、Causal Question / Estimand、Treatment Assignment、Temporal Ordering、Confounding、Positivity / Overlap、SUTVA等、Designに応じた前提確認が必要である。
- CATE / Upliftを用いたTargetingは、平均Treatment Effectを推定しただけでは正当化されない。
- Enterprise Caseで公開される成果は各社固有条件に依存し、当チームのPoCで同等効果を保証するものではない。
- Predictive側もAccuracyのみでBusiness Valueを保証しない。PredictionをDecision Rule / Actionへ接続する必要がある。
