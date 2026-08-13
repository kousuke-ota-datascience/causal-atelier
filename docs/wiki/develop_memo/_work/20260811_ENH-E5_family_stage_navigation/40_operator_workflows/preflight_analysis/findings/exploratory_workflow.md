# Exploratory / Dataset Workflow

> **Non-normative preflight finding.** 実装・検証仕様は正本文書および06/Pxx/07へ収束させる。

## 1. Scope

Exploratory workflow continuityと追加analytical surfaceを分離する。

## 2. Audit facts

| ID | Alignment | Statement | Audit finding | Source evidence |
|---|---|---|---|---|
| FR-020 | MISMATCH | Exploreのfilter・chart状態からAnalysis View draftを作成できる | No implemented Explore filter/chart-state -> AnalysisView draft conversion was found in the E4 frontend/application path. | product/domain/analysis_view.py; interfaces/web_api/routers/dataset_versions.py; exploratory/view compiler; frontend |
| FR-025 | PARTIAL_MATCH | 欠損パターンおよび列別missingnessを確認できる | Column missingness/profile exists; explicit missing-pattern analysis was not confirmed. | capabilities/exploratory/planner.py; capabilities/exploratory/runners.py; interfaces/web_api/routers/exploration.py |
| FR-026 | PARTIAL_MATCH | 二変量の散布、箱ひげ、クロス集計および関連指標を生成できる | Association operations exist, but the full requested scatter/box/crosstab surface set is not implemented as stated. | capabilities/exploratory/planner.py; capabilities/exploratory/runners.py; interfaces/web_api/routers/exploration.py |
| FR-028 | MISMATCH | correlation / association matrixを型に応じて生成できる | Exploratory operations do not include a correlation/association matrix operation. | capabilities/exploratory/planner.py; capabilities/exploratory/runners.py; interfaces/web_api/routers/exploration.py |
| FR-032 | MISMATCH | 探索ResultからCausalまたはPredictive Analysis Specificationのdraftを作成できる | No implemented Exploratory Result -> Causal/Predictive AnalysisSpecification draft conversion was confirmed. | capabilities/exploratory/planner.py; capabilities/exploratory/runners.py; interfaces/web_api/routers/exploration.py |
| FR-034 | PARTIAL_MATCH | 可視化の描画条件、集計条件、samplingおよびcode versionを保存する | Sampling/spec/code-version information exists across contracts, but complete rendering/aggregation-condition persistence as stated was not confirmed. | capabilities/exploratory/planner.py; capabilities/exploratory/runners.py; interfaces/web_api/routers/exploration.py |
| FR-011 | PARTIAL_MATCH | Dataset Versionにcontent hash、schema、row count、column count、基本profileを保存する | DatasetVersion stores profile_summary_json, but registration computes schema/row/column counts and does not compute the required basic profile. | product/domain/analysis_view.py; interfaces/web_api/routers/dataset_versions.py; exploratory/view compiler; frontend |

## 3. Confirmed remediation

AnalysisView draft/Family handoff/analysis-significant rendering parametersはD2。advanced missing/bivariate/matrix surfacesはD3。既存Dataset metadata/capabilityはD1。

| Decision Item | Decision | Substatement | Delivery | TD Ref |
|---|---|---|---|---|
| FR-020 | **D2** | Explore filter/chart state → AnalysisView draft handoff | ENH-E5 |  |
| FR-028 | **D3** | Correlation / association matrix operation | FUTURE | TD-007 |
| FR-032 | **D2** | Exploratory Result → Causal/Predictive AnalysisSpecification draft | ENH-E5 |  |
| FR-011 | **D1** | DatasetVersion registration metadata/profile semantics | BASELINE |  |
| FR-025a | **D1** | Column missingness | BASELINE |  |
| FR-025b | **D3** | Joint missing-pattern analysis | FUTURE | TD-007 |
| FR-026a | **D1** | Existing association/bivariate capability | BASELINE |  |
| FR-026b | **D3** | Full scatter/box/crosstab surface set | FUTURE | TD-007 |
| FR-034 | **D2** | Persist analysis-significant rendering/aggregation/sampling parameters | ENH-E5 |  |

## 4. Downstream impact

- D1: current contract記述を10/21/22/23/30へ反映する。
- D2: ENH-E5 targetとして必要なdesign/validation/API/UI/test seamを正本文書へ具体化し、NFR-019 PASS後に06/Pxx・07へ収束する。
- D3: current targetから分離し、`90_technical_debt_and_future_enhancements.md`へtraceする。
