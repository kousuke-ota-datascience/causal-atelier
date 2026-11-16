<!-- ENH-E11 split working copy: not a formal approval. -->
# 10 — science

**Status:** `STRUCTURAL_COPY_DRAFT` (existing baseline text, not E11 canonical publication)

**Source:** [10_requirements_definition.md](https://github.com/kousuke-ota-datascience/causal-atelier/blob/3ba5fe2465ec591f0da7f998c21a5241984b73dc/docs/wiki/requirement_definition/10_requirements_definition.md) · blob `40b83f29c67b4a39f6db5393be7534c5e892d656`  
**Index:** [Revised document inventory](../README_00_Revised_requirements_definition_documents.md)

---

## 7. 科学・統計・分析上の要件

| ID | Area | Requirement | Level | Requirement Status | Implementation Status | Delivery |
| --- | --- | --- | --- | --- | --- | --- |
| AR-001 | Scientific Integrity | 探索的可視化は仮説生成であり、因果結論または確認的検定へ自動変換しない | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-002 | Scientific Integrity | 予測性能は因果効果を示さない | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-003 | Scientific Integrity | Predictive Explanationはmodel behaviorの説明でありcausal explanationではない | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-004 | Scientific Integrity | 同一immutable `dataset_version_id`を探索とconfirmatory analysisで再利用した場合、`EXPLORATORY_REUSE_SAME_DATA` warningとlineage evidenceを保持する | — | ACTIVE | PARTIAL | ENH-E5 |
| AR-005 | Scientific Integrity | 因果推定はIdentification ResultとData Eligibility Resultを参照してgateする | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-006 | Scientific Integrity | Identification statusは全reasonを収集後に決定する | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-007 | Scientific Integrity | Collider判定はback-door path上のcolliderまたはその子孫を対象とする | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-008 | Scientific Integrity | Eligibilityの型はBINARY、CONTINUOUS、UNSUPPORTED等の正規値で保存する | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-009 | Scientific Integrity | 外部libraryのdtype objectまたはmodel objectをJSON正本へ保存しない | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-010 | Scientific Integrity | Estimation前提不成立時は数値を無理に返さず分析状態を保存する | — | ACTIVE | IMPLEMENTED | BASELINE |
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
| AR-023 | Scientific Integrity | Causal Identificationでは観測データと仮定からestimandが識別可能かをEstimationと分離して扱う | — | ACTIVE | IMPLEMENTED | ENH-E5 |
| AR-024 | Scientific Integrity | Causal Effectsは推定されたeffectの閲覧・利用を扱い、estimator configurationと混在させない | — | ACTIVE | IMPLEMENTED | ENH-E5 |
| AR-025 | Scientific Integrity | Predictive MetricsとPredictive Explainabilityを別目的として扱い、feature importance等をcausal effectへ読み替えない | — | ACTIVE | IMPLEMENTED | ENH-E5 |
| AR-026 | Scientific Integrity | Exploratory Findings / visualizationをcausal conclusionまたはconfirmatory resultへ自動昇格しない | — | ACTIVE | IMPLEMENTED | ENH-E5 |
| AR-027 | Scientific Integrity | coefficient contribution / SHAP / LIMEはmodel behavior explanationであり、feature causal importance、treatment effect、causal mechanismを意味しない | — | ACTIVE | IMPLEMENTED | ENH-E10 |



### 7.0.1. Predictive subgroup uncertainty contract

指定subgroup columnはuntouched TEST populationを各column独立にsliceする。automatic intersection/discovery/fairness frameworkはcurrent mandatory scope外。各recordは`sample_count`を必須とし、uncertaintyはnonparametric percentile bootstrap（confidence=0.95, resamples=1000, deterministic seed）とする。`n < 2`またはvalid resamples < 200ではCIを返さずwarningを返す。metricを計算できない場合はvalue/uncertaintyを`null`とし、値を捏造しない。

### 7.0.2. Scientific comparability contract

Comparisonは次の二段階で判定する。

1. `semantic_compatible`
2. `direct_metric_comparable`

Predictive semantic keyは`task_type / prediction target(outcome) / prediction unit / prediction time / horizon / deployment/evaluation population semantics`。Direct metric comparisonではさらに`same dataset_version_id / same TEST-row identity(hash) / same metric definition`を要求する。

Causal semantic keyは`treatment(exposure) / outcome / estimand / target population`。Direct comparisonではsame data/view/analysis populationも要求する。

semantic mismatchは比較request自体のtechnical failureにせず、compatible=falseとreasonを返し、quantitative delta/rankingを生成しない。AUC/RMSE/ATE等を単一scoreへ正規化しない。


## 7.1. Project Authorization / Sensitive Output Boundary

Persisted Project roleは次の3値のみとする。

- `OWNER`
- `EDITOR`
- `VIEWER`

| Action | OWNER | EDITOR | VIEWER |
| --- | --- | --- | --- |
| Project READ | allow | allow | allow |
| WRITE / MUTATE | allow | allow | deny |
| Execution submit/cancel/retry/rerun/revise | allow | allow | deny |
| Export create | allow | allow | deny |
| Membership administration | allow | deny | deny |
| Explicit sensitive output | allow | allow | deny |

独立`EXECUTE` roleは追加しない。prediction row / local explanationはpotentially sensitive outputとして扱う。configurable sensitive-column governanceは`DEFERRED`でありcurrent mandatory acceptanceへ含めない。



## 7.2. Canonical Lineage / Reproducibility / Retry Safety

Canonical lineage read modelは最低限次を接続する。

```text
ResearchContextVersion
  ↓
AnalysisSpecification
  ↓
ExecutionPlan
  ↓
Execution
  ↓
StageExecution
  ↓
Result
  ↓
Artifact
```

加えて`DatasetVersion / AnalysisView / GraphVersion / input Result / base Execution`を接続する。FK/snapshotからdeterministically導出できるstructural relationをgeneric `LineageEdge`へ重複persistしない。`MOTIVATED`等のsemantic relationだけをgeneric LineageEdgeで保持する。

Current contractでは`StageAttempt.effective_random_seed: int | null`を追加し、stochastic Stageのactual seedをattempt単位で保存する。同一logical Stageのretryは同じseedを再利用し、deterministic Stageは`null`とする。

`runtime_version_json`は最低限`ariadne_code_version / python_version / platform_system / platform_release / machine / libraries`を保持する。これはbit-for-bit numerical identity保証ではなくenvironment再構築情報である。

Idempotencyはduplicate durable side effectを生成し得るCommandに適用し、scopeを`(project_id, command_scope, idempotency_key)`とする。exactly-once executionは保証しないが、retryで同一successful Stage outputのdurable Artifactを重複materializeしてはならない。
