# 10_30_ar_scientific_integrity

**Status:** `RD02_STRUCTURAL_WORKING_COPY / E11_NOT_PUBLISHED`; original ID, level and state retained.  
**Source blob:** `40b83f29c67b4a39f6db5393be7534c5e892d656`.

---

## AR original requirement rows

| ID | Area | Requirement | Level | Requirement Status | Implementation Status | Delivery |
| --- | --- | --- | --- | --- | --- | --- |
| AR-001 | Scientific Integrity | 探索的可視化は仮説生成であり、因果結論または確認的検定へ自動変換しない | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-002 | Scientific Integrity | 予測性能は因果効果を示さない | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-003 | Scientific Integrity | Predictive Explanationはmodel behaviorの説明でありcausal explanationではない | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-004 | Scientific Integrity | 同一immutable `dataset_version_id`を探索とconfirmatory analysisで再利用した場合、`EXPLORATORY_REUSE_SAME_DATA` warningとlineage evidenceを保持する | — | ACTIVE | PARTIAL | ENH-E5 |
| AR-011 | Scientific Integrity | Predictive preprocessingはtrain partitionのみでfitする | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-012 | Scientific Integrity | test partitionをfeature selection、model selection、threshold selectionに利用しない | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-013 | Scientific Integrity | 時系列Taskは未来観測がtrain featureへ混入しないsplitを使用する | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-014 | Scientific Integrity | 同一entityがtrainとtestへ跨る場合はgroup leakageを検査する | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-015 | Scientific Integrity | classification metricはclass imbalance、threshold、calibrationと併記する | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-016 | Scientific Integrity | subgroup metricは`sample_count`を必須とし、0.95 percentile bootstrap（1000 resamples、deterministic seed）で計算可能な場合にuncertaintyを併記し、計算不能値を捏造しない | — | ACTIVE | IMPLEMENTED | ENH-E5 |
| AR-017 | Scientific Integrity | Result比較はsemantic compatibilityとdirect metric comparabilityを分離して判定する | — | ACTIVE | IMPLEMENTED | ENH-E5 |
| AR-018 | Scientific Integrity | AUC、RMSE、ATE等を単一の優劣scoreへ変換しない | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-019 | Scientific Integrity | random seedだけでなくsplit indexまたはpartition artifactを保存する | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-020 | Scientific Integrity | prediction row / local explanationをpotentially sensitive outputとして扱い、Project roleに応じてdetail exposureを制御する | — | ACTIVE | PARTIAL | ENH-E5 |
| AR-021 | Scientific Integrity | Navigation Stageの表示順を分析上必須の実行順序として解釈しない | — | ACTIVE | IMPLEMENTED | ENH-E5 |
| AR-022 | Scientific Integrity | Family間でStage数・名称を揃えることを科学的workflow要件としない | — | ACTIVE | IMPLEMENTED | ENH-E5 |
| AR-025 | Scientific Integrity | Predictive MetricsとPredictive Explainabilityを別目的として扱い、feature importance等をcausal effectへ読み替えない | — | ACTIVE | IMPLEMENTED | ENH-E5 |
| AR-026 | Scientific Integrity | Exploratory Findings / visualizationをcausal conclusionまたはconfirmatory resultへ自動昇格しない | — | ACTIVE | IMPLEMENTED | ENH-E5 |
| AR-027 | Scientific Integrity | coefficient contribution / SHAP / LIMEはmodel behavior explanationであり、feature causal importance、treatment effect、causal mechanismを意味しない | — | ACTIVE | IMPLEMENTED | ENH-E10 |
### 7.0.1. Predictive subgroup uncertainty contract

指定subgroup columnはuntouched TEST populationを各column独立にsliceする。automatic intersection/discovery/fairness frameworkはcurrent mandatory scope外。各recordは`sample_count`を必須とし、uncertaintyはnonparametric percentile bootstrap（confidence=0.95, resamples=1000, deterministic seed）とする。`n < 2`またはvalid resamples < 200ではCIを返さずwarningを返す。metricを計算できない場合はvalue/uncertaintyを`null`とし、値を捏造しない。
