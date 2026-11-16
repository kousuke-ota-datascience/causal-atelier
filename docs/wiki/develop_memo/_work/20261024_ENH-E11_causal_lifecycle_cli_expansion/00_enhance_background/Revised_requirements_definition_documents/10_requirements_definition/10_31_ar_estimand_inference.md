# 10_31_ar_estimand_inference

**Status:** `RD02_STRUCTURAL_WORKING_COPY / E11_NOT_PUBLISHED`; original ID, level and state retained.  
**Source blob:** `40b83f29c67b4a39f6db5393be7534c5e892d656`.

---

## AR original requirement rows

| ID | Area | Requirement | Level | Requirement Status | Implementation Status | Delivery |
| --- | --- | --- | --- | --- | --- | --- |
| AR-005 | Scientific Integrity | 因果推定はIdentification ResultとData Eligibility Resultを参照してgateする | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-006 | Scientific Integrity | Identification statusは全reasonを収集後に決定する | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-007 | Scientific Integrity | Collider判定はback-door path上のcolliderまたはその子孫を対象とする | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-008 | Scientific Integrity | Eligibilityの型はBINARY、CONTINUOUS、UNSUPPORTED等の正規値で保存する | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-009 | Scientific Integrity | 外部libraryのdtype objectまたはmodel objectをJSON正本へ保存しない | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-010 | Scientific Integrity | Estimation前提不成立時は数値を無理に返さず分析状態を保存する | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-023 | Scientific Integrity | Causal Identificationでは観測データと仮定からestimandが識別可能かをEstimationと分離して扱う | — | ACTIVE | IMPLEMENTED | ENH-E5 |
| AR-024 | Scientific Integrity | Causal Effectsは推定されたeffectの閲覧・利用を扱い、estimator configurationと混在させない | — | ACTIVE | IMPLEMENTED | ENH-E5 |
### 7.0.2. Scientific comparability contract

Comparisonは次の二段階で判定する。

1. `semantic_compatible`
2. `direct_metric_comparable`

Predictive semantic keyは`task_type / prediction target(outcome) / prediction unit / prediction time / horizon / deployment/evaluation population semantics`。Direct metric comparisonではさらに`same dataset_version_id / same TEST-row identity(hash) / same metric definition`を要求する。

Causal semantic keyは`treatment(exposure) / outcome / estimand / target population`。Direct comparisonではsame data/view/analysis populationも要求する。

semantic mismatchは比較request自体のtechnical failureにせず、compatible=falseとreasonを返し、quantitative delta/rankingを生成しない。AUC/RMSE/ATE等を単一scoreへ正規化しない。
