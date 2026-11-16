# 10_12_fr_predictive

**Status:** `RD02_STRUCTURAL_WORKING_COPY / E11_NOT_PUBLISHED`; original ID, level and state retained.  
**Source blob:** `40b83f29c67b4a39f6db5393be7534c5e892d656`.

---

## FR original requirement rows

| ID | Area | Requirement | Level | Requirement Status | Implementation Status | Delivery |
| --- | --- | --- | --- | --- | --- | --- |
| FR-055 | Predictive | 表形式Binary ClassificationとRegressionをPrediction Taskとして作成できる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-056 | Predictive | Prediction unit、target、prediction time、horizon、intended use、deployment populationを固定する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-057 | Predictive | feature setと各featureのavailability cutoffを固定する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-058 | Predictive | random、stratified、group、time-based splitを選択できる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-059 | Predictive | 目的変数・将来情報・同一GroupなどのLeakageを検出して不適切な評価を拒否する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-060 | Predictive | imputation、encoding、scaling等のfitをtraining partitionのみに限定する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-061 | Predictive | 対象Taskと実行環境に適合するモデルと設定候補を選択できる | MUST | ACTIVE | IMPLEMENTED | ENH-E10 |
| FR-062 | Predictive | validation partitionまたはcross-validationによるautomated hyperparameter selectionを提供する | SHOULD | DEFERRED | NOT_IMPLEMENTED | FUTURE |
| FR-063 | Predictive | 固定済みspecとsplitからmodelをtrainingできる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-064 | Predictive | test partitionをmodel selectionに使用せず、最終評価まで隔離する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-065 | Predictive | classificationとregressionでtask対応metricを生成する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-066 | Predictive | classificationでclass balance、threshold、calibrationを確認できる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-067 | Predictive | 指定Subgroupの評価指標・標本数と計算可能な不確実性を確認できる | SHOULD | ACTIVE | IMPLEMENTED | ENH-E5 |
| FR-068 | Predictive | 学習済みモデルと前処理を保存し、適合する環境で復元して再予測できる | MUST | ACTIVE | IMPLEMENTED | ENH-E10 |
| FR-069 | Predictive | 利用可能な範囲でモデル全体・個別予測の説明を生成でき、未対応の範囲を偽装しない | SHOULD | ACTIVE | IMPLEMENTED | ENH-E10 |
| FR-070 | Predictive | Predictive Explanationを因果説明と区別して表示・exportする | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-071 | Predictive | 学習・評価・説明の根拠、限界、再現性情報をModel Cardで確認できる | SHOULD | ACTIVE | IMPLEMENTED | ENH-E10 |
| FR-072 | Predictive | 意味的に比較可能なResultのみを比較する。直接数値差分は、同一DatasetVersion・同一TEST標本identity/hash・同一定義metricが一致する場合に限り算出できる | MUST | ACTIVE | PARTIAL | ENH-E5 |
| FR-073 | Predictive | Prediction Taskからsource Context、Dataset、Analysis Viewへ遡れる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-149 | Predictive | Predictiveは`setup / train / predict / metrics / explainability / model-management`をFamily-local Navigation Stageとして提供する | MUST | ACTIVE | IMPLEMENTED | ENH-E5 |
| FR-150 | Predictive | 既存の予測機能・入力検証・保存済み仕様の意味を維持する | MUST | ACTIVE | IMPLEMENTED | ENH-E5 |
| FR-151 | Predictive | 予測指標と予測説明の目的を区別して利用できる | MUST | ACTIVE | IMPLEMENTED | ENH-E5 |
| FR-152 | Predictive | Model Managementは現行scopeではfitted model、model card、artifact、lineageのread-oriented確認を中心とする | MUST | ACTIVE | IMPLEMENTED | ENH-E5 |
| FR-161 | Scope | 追加分析機能が未導入でも基本機能を使え、未対応手法へ勝手に切替えない | MUST | ACTIVE | IMPLEMENTED | ENH-E10 |
| FR-176 | Predictive Surface | 既存の予測タスク設定・データ分割・学習・評価・説明・Model Cardの意味を維持し、Navigation変更で分析実行契約を変更しない | MUST NOT | ACTIVE | IMPLEMENTED | ENH-E7 |
| FR-178 | Predictive | 表形式分類・回帰で承認済み追加学習方式を選択して学習・評価できる | MUST | ACTIVE | IMPLEMENTED | ENH-E10 |
| FR-179 | Predictive | optional model dependencyが利用不可の場合は明示的capability-unavailable state/errorを返し、別modelへsilent fallbackしない | MUST | ACTIVE | IMPLEMENTED | ENH-E10 |
| FR-180 | Predictive | 保存済み学習モデルを復元し、適合条件下で同等の予測を再実行できる | MUST | ACTIVE | IMPLEMENTED | ENH-E10 |
| FR-181 | Predictive | 利用可能なモデル説明方式を適合性に応じて選択し、予測への変数寄与を定量的に説明できる | MUST | ACTIVE | IMPLEMENTED | ENH-E10 |
| FR-182 | Predictive | 個別予測・モデル全体への説明の提供範囲を明示し、未対応の説明を擬似出力しない | MUST | ACTIVE | IMPLEMENTED | ENH-E10 |
| FR-183 | Predictive | 予測説明のモデル・入力・出力尺度・計算条件を追跡し再現できる | MUST | ACTIVE | IMPLEMENTED | ENH-E10 |
| FR-184 | Predictive / UI | 利用可能な学習・説明機能と不可理由、設定条件、由来を一貫して表示する | MUST | ACTIVE | IMPLEMENTED | ENH-E10 |
