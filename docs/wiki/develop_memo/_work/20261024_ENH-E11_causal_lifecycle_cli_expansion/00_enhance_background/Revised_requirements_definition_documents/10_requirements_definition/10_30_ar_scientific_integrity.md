# 10_30_ar_scientific_integrity

**Status:** `RD03_FORMAL_E11_ISSUED / OWNER_SHA_REVIEW_PENDING`; original ID, level and state retained.  
**Source blob:** `40b83f29c67b4a39f6db5393be7534c5e892d656`.

---

## AR original requirement rows

| ID | Area | Requirement | Level | Requirement Status | Implementation Status | Delivery |
| --- | --- | --- | --- | --- | --- | --- |
| AR-001 | Scientific Integrity | 探索的可視化は仮説生成であり、因果結論または確認的検定へ自動変換しない | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-002 | Scientific Integrity | 予測性能は因果効果を示さない | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-003 | Scientific Integrity | Predictive Explanationはmodel behaviorの説明でありcausal explanationではない | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-004 | Scientific Integrity | 同一データを探索と確認的分析に再利用した場合、その事実を示し独立検証として扱わない | — | ACTIVE | PARTIAL | ENH-E5 |
| AR-011 | Scientific Integrity | Predictive preprocessingはtrain partitionのみでfitする | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-012 | Scientific Integrity | test partitionをfeature selection、model selection、threshold selectionに利用しない | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-013 | Scientific Integrity | 時系列Taskは未来観測がtrain featureへ混入しないsplitを使用する | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-014 | Scientific Integrity | 同一entityがtrainとtestへ跨る場合はgroup leakageを検査する | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-015 | Scientific Integrity | classification metricはclass imbalance、threshold、calibrationと併記する | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-016 | Scientific Integrity | 評価Subgroupの標本数と不確実性を明示し、標本条件・推論方法が不適切な場合は計算不能理由を示して未検証区間を生成しない | — | ACTIVE | IMPLEMENTED | ENH-E5 |
| AR-017 | Scientific Integrity | Result比較はsemantic compatibilityとdirect metric comparabilityを分離して判定する | — | ACTIVE | IMPLEMENTED | ENH-E5 |
| AR-018 | Scientific Integrity | AUC、RMSE、ATE等を単一の優劣scoreへ変換しない | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-019 | Scientific Integrity | 分析のデータ分割を再現可能な情報として保持しなければならない | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-020 | Scientific Integrity | 個票予測と局所説明は機微情報になり得るため、利用権限に応じ露出を制限する | — | ACTIVE | PARTIAL | ENH-E5 |
| AR-021 | Scientific Integrity | Navigation Stageの表示順を、因果分析その他の科学的な実行順序や必須解析手順として解釈させない | — | ACTIVE | IMPLEMENTED | ENH-E5 |
| AR-022 | Scientific Integrity | 【設計制約移管・Legacy Trace】対応する既存上位要件に係る既存設計制約。具体的な実装契約は下位設計へ移し、元ID・Status・科学的制約の追跡を維持する | — | ACTIVE | IMPLEMENTED | ENH-E5 |
| AR-025 | Scientific Integrity | Predictive MetricsとPredictive Explainabilityを別目的として扱い、feature importance等をcausal effectへ読み替えない | — | ACTIVE | IMPLEMENTED | ENH-E5 |
| AR-026 | Scientific Integrity | Exploratory Findings / visualizationをcausal conclusionまたはconfirmatory resultへ自動昇格しない | — | ACTIVE | IMPLEMENTED | ENH-E5 |
| AR-027 | Scientific Integrity | 予測モデルの説明値はモデルの挙動に関するものであり、変数の因果的重要性・介入効果・因果機構を示さない | — | ACTIVE | IMPLEMENTED | ENH-E10 |
| AR-031 | Negative Control Semantics | 観測NCE／NCOは研究者の明示opt-inとGraph／時間的適格性を要し、Null検査の非有意を未観測交絡がない証明と解釈してはならない | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| AR-032 | Sensitivity Scope | 初期の未観測交絡感度は古典OLS係数のpartial R²とpoint RV（q=1）に限り、HC3やIPW／AIPW／CATEへ無検証に一般化してはならない | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| AR-033 | Weight and Inference Validity | IPW／IPTW／AIPWの解析重み・正規化・Clipping／Trimmingとoverlap／balance／ESSを区別し、適格性に裏付けられない区間推論を生成してはならない | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| AR-035 | Exploratory and Confirmatory | 探索的点推定を確認的推論の成功と表してはならず、確認的区間推論には対象Method・構成に適合した推論根拠が必要である | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| AR-042 | Scientific Negative State | 非識別・適格性不足・Review要・推論未対応・Backend利用不能を技術失敗や数値ゼロに読み替えてはならない | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| AR-044 | Method-specific Scientific Validation | 採用MethodのEstimand・適格性・点推定・推論を個別の既知真値と負例で検証し、未対応の推論や点ごとの区間を同時信頼帯として報告してはならない | MUST | ACTIVE | UNVERIFIED | ENH-E11 |

### 7.0.1. Predictive subgroup uncertainty contract

指定subgroup columnはuntouched TEST populationを各column独立にsliceする。automatic intersection/discovery/fairness frameworkはcurrent mandatory scope外。各recordは`sample_count`を必須とし、uncertaintyはnonparametric percentile bootstrap（confidence=0.95, resamples=1000, deterministic seed）とする。`n < 2`またはvalid resamples < 200ではCIを返さずwarningを返す。metricを計算できない場合はvalue/uncertaintyを`null`とし、値を捏造しない。
