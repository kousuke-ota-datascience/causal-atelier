# AnalysisView Typed Validation

> **Non-normative preflight finding.** 実装・検証仕様は正本文書および06/Pxx/07へ収束させる。

## 1. Scope

filter operator/valueとcolumn logical typeのcompatibility validation gapを確認する。

## 2. Audit facts

| ID | Alignment | Statement | Audit finding | Source evidence |
|---|---|---|---|---|
| FR-015 | MISMATCH | Analysis Viewの式と参照列を型付きSchemaで検証する | AnalysisView validates shape/known columns/deterministic compilation, but filter operator/value logical-type compatibility is not enforced by the domain validator. | product/domain/analysis_view.py; interfaces/web_api/routers/dataset_versions.py; exploratory/view compiler; frontend |
| D21-005 | MISMATCH | filter operator/value type are checked against column logical type | Domain validator checks envelope/array uniqueness/derived names but not filter operator/value logical-type compatibility. | analysis_view.py |

## 3. Confirmed remediation

D2。既存validatorへtyped compatibility validationを追加し、expression language全体の再設計へscopeを拡張しない。

| Decision Item | Decision | Substatement | Delivery | TD Ref |
|---|---|---|---|---|
| FR-015 | **D2** | AnalysisView filter operator/value × column logical type compatibility validation | ENH-E5 |  |
| D21-005 | **D2** | AnalysisView typed filter constraint | ENH-E5 |  |

## 4. Downstream impact

- D1: current contract記述を10/21/22/23/30へ反映する。
- D2: ENH-E5 targetとして必要なdesign/validation/API/UI/test seamを正本文書へ具体化し、NFR-019 PASS後に06/Pxx・07へ収束する。
- D3: current targetから分離し、`90_technical_debt_and_future_enhancements.md`へtraceする。
