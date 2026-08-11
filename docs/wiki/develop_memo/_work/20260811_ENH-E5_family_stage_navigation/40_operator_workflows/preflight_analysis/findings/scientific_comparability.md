# Scientific Comparability / Exploratory-to-Confirmatory Guard

> **Non-normative preflight finding.** 実装・検証仕様は正本文書および06/Pxx/07へ収束させる。

## 1. Scope

comparison semantic guardと探索後推論warning/lineageを整理する。

## 2. Audit facts

| ID | Alignment | Statement | Audit finding | Source evidence |
|---|---|---|---|---|
| AR-017 | MISMATCH | Result比較は同一Task / Estimand / Outcome等の比較可能性を検証する | Result comparison validates same family/result type, not same Task/Estimand/Outcome semantic comparability. | family capability validation/runners; comparison/lineage/product closure services |
| FR-072 | PARTIAL_MATCH | 同一Taskのmodel、split、feature、metric差分を比較できる | Comparison enforces same family/result type; it does not fully validate same Task/split/feature/metric semantics. | capabilities/predictive/validation.py; planner.py; metrics.py; training/explanation runners |
| FR-051 | PARTIAL_MATCH | 同一Project・Datasetの先行Discoveryを確認し、確認的Estimationへ探索後推論警告を保存する | Cross-analysis scientific warning behavior exists in parts of the product, but the exact same-Project/same-Dataset prior-Discovery warning contract was not fully confirmed. | product/application/scientific_validation_service.py; capabilities/causal/workflow.py; graph services/domain |
| AR-004 | PARTIAL_MATCH | 同一データで探索後に確認的分析を行った事実を警告とLineageで保持する | Warnings/lineage support exists, but the exact same-data exploratory-then-confirmatory tracking contract was not fully established. | family capability validation/runners; comparison/lineage/product closure services |

## 3. Confirmed remediation

D2。Family別comparability keyとsame-data exploratory→confirmatory guardをfreezeする。

| Decision Item | Decision | Substatement | Delivery | TD Ref |
|---|---|---|---|---|
| AR-017 | **D2** | Semantic result comparability | ENH-E5 |  |
| FR-051 | **D2** | Prior exploratory use warning before confirmatory estimation | ENH-E5 |  |
| FR-072 | **D2** | Predictive comparison semantic guard | ENH-E5 |  |
| AR-004 | **D2** | Same-data exploratory→confirmatory warning + lineage | ENH-E5 |  |

## 4. Downstream impact

- D1: current contract記述を10/21/22/23/30へ反映する。
- D2: ENH-E5 targetとして必要なdesign/validation/API/UI/test seamを正本文書へ具体化し、NFR-019 PASS後に06/Pxx・07へ収束する。
- D3: current targetから分離し、`90_technical_debt_and_future_enhancements.md`へtraceする。
