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
| FR-059 | Predictive | target leakage、future leakage、group leakage、split overlapをBackendで拒否する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-060 | Predictive | imputation、encoding、scaling等のfitをtraining partitionのみに限定する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-061 | Predictive | Algorithm Registryはtask compatibilityに加えてmodel capability、parameter schema/default、provider/optional dependency availability/versionを表現し、利用可能なtask-compatible modelをbackend authorityで選択できる | MUST | ACTIVE | IMPLEMENTED | ENH-E10 |
| FR-062 | Predictive | validation partitionまたはcross-validationによるautomated hyperparameter selectionを提供する | SHOULD | DEFERRED | NOT_IMPLEMENTED | FUTURE |
| FR-063 | Predictive | 固定済みspecとsplitからmodelをtrainingできる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-064 | Predictive | test partitionをmodel selectionに使用せず、最終評価まで隔離する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-065 | Predictive | classificationとregressionでtask対応metricを生成する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-066 | Predictive | classificationでclass balance、threshold、calibrationを確認できる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-067 | Predictive | untouched TEST population上で指定subgroup columnごとのmetric、`sample_count`、計算可能な場合のbootstrap uncertaintyを確認できる | SHOULD | ACTIVE | IMPLEMENTED | ENH-E5 |
| FR-068 | Predictive | fitted model、fitted preprocessor、prediction等のdurable outputをArtifactとして保存し、provider-specific fitted modelはartifact schema/provider/payload identityから対応loaderを一意に解決してfresh-process相当で再読込・predictionできる | MUST | ACTIVE | IMPLEMENTED | ENH-E10 |
| FR-069 | Predictive | explanation method capabilityが宣言するsupported scopeに従いglobal / local Predictive Explanationを生成でき、unsupported scopeを擬似出力で補完しない | SHOULD | ACTIVE | IMPLEMENTED | ENH-E10 |
| FR-070 | Predictive | Predictive Explanationを因果説明と区別して表示・exportする | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-071 | Predictive | intended use、training data、metric、limitationsに加え、model/provider/version、effective parameters、seed/deterministic settings、feature/preprocessor identity、explanation method等の再現性provenanceをModel Cardへ記録する | SHOULD | ACTIVE | IMPLEMENTED | ENH-E10 |
| FR-072 | Predictive | Result比較はまずsemantic compatibilityを検証し、direct metric comparisonではさらに同一DatasetVersion、同一TEST-row identity/hash、同一定義metricを要求する | MUST | ACTIVE | PARTIAL | ENH-E5 |
| FR-073 | Predictive | Prediction Taskからsource Context、Dataset、Analysis Viewへ遡れる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-149 | Predictive | Predictiveは`setup / train / predict / metrics / explainability / model-management`をFamily-local Navigation Stageとして提供する | MUST | ACTIVE | IMPLEMENTED | ENH-E5 |
| FR-150 | Predictive | 既存Predictive UIの設定項目、validation、generated `predictive-analysis-spec/1` semanticsを全量保持する | MUST | ACTIVE | IMPLEMENTED | ENH-E5 |
| FR-151 | Predictive | MetricsとExplainabilityを異なる目的のNavigation Stageとして扱い、Predict Stage導入を理由に新規standalone scoring engineを必須化しない | MUST | ACTIVE | IMPLEMENTED | ENH-E5 |
| FR-152 | Predictive | Model Managementは現行scopeではfitted model、model card、artifact、lineageのread-oriented確認を中心とする | MUST | ACTIVE | IMPLEMENTED | ENH-E5 |
| FR-161 | Scope | LightGBM / SHAP / LIME等のexternal analytical engineはoptional capabilityとして導入し、未導入でもcore startupと既存supported flowを壊さず、unavailable capabilityから別model/methodへsilent fallbackしない | MUST | ACTIVE | IMPLEMENTED | ENH-E10 |
| FR-176 | Predictive Surface | Predictive Navigation Stageを新しいbackend Execution modelまたは1:1 runtime Stageとして扱わず、既存Prediction Task → Split → Training → Evaluation → Explanation → Model Card semanticsを保持する | MUST NOT | ACTIVE | IMPLEMENTED | ENH-E7 |
| FR-178 | Predictive | Binary Classification / RegressionでLightGBM backend（`lightgbm_classifier.v1` / `lightgbm_regressor.v1`）をtask-compatible modelとして選択できる | MUST | ACTIVE | IMPLEMENTED | ENH-E10 |
| FR-179 | Predictive | optional model dependencyが利用不可の場合は明示的capability-unavailable state/errorを返し、別modelへsilent fallbackしない | MUST | ACTIVE | IMPLEMENTED | ENH-E10 |
| FR-180 | Predictive | fitted modelはserialize/load round-trip後もmodel/task/feature/preprocessor identityを保持し、同一runtime/config fixtureでprediction contractを満たす | MUST | ACTIVE | IMPLEMENTED | ENH-E10 |
| FR-181 | Predictive | Predictive Explanationはmodel-method compatibilityをbackend authorityで検証し、`LINEAR_COEFFICIENT_CONTRIBUTION` / `SHAP_TREE` / `LIME_TABULAR`を明示methodとして解決する | MUST | ACTIVE | IMPLEMENTED | ENH-E10 |
| FR-182 | Predictive | `SHAP_TREE`はapproved compatibility範囲でglobal/localを提供し、`LIME_TABULAR`はlocal-onlyを提供する。unsupported capabilityを別methodまたは擬似global出力で補完しない | MUST | ACTIVE | IMPLEMENTED | ENH-E10 |
| FR-183 | Predictive | explanation Result/Artifactはmethod/model/provider、feature/sample identity、model/prediction output scale、background/reference、effective seed/parameters、library version等のprovenanceを保持する | MUST | ACTIVE | IMPLEMENTED | ENH-E10 |
| FR-184 | Predictive / UI | Train / Explainability / Model Managementはbackend capability metadataからcompatible option、availability/reason、parameter definition、provenanceを表示し、Frontendを独立したmodel-method compatibility authorityにしない | MUST | ACTIVE | IMPLEMENTED | ENH-E10 |
