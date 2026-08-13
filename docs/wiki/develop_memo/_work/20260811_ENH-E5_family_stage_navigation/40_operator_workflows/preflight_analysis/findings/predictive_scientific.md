# Predictive / Causal Capability Boundaries

> **Non-normative preflight finding.** 実装・検証仕様は正本文書および06/Pxx/07へ収束させる。

## 1. Scope

Estimator capabilityに依存するCausal diagnosticsと、未実装のautomated hyperparameter selectionを、current contractとfuture capabilityへ分離する。

## 2. Audit facts

| ID | Alignment | Requirement | Audit finding | Source evidence |
|---|---|---|---|---|
| FR-048 | PARTIAL_MATCH | overlap、balance、weight、sample loss等をDiagnostics Resultとして分離保存する | Causal diagnostics exist and estimator capabilities declare several diagnostics, but the full overlap/balance/weight/sample-loss set is not uniformly produced. | product/application/scientific_validation_service.py; capabilities/causal/workflow.py; graph services/domain |
| FR-062 | MISMATCH | validation partitionまたはcross-validationでhyperparameter selectionを行える | Predictive validation explicitly rejects non-empty automated tuning candidates; automated hyperparameter selection is not supported. | capabilities/predictive/validation.py; planner.py; metrics.py; training/explanation runners |

## 3. Confirmed remediation

- `FR-048 → D1`: 全estimatorへoverlap/balance/weight/sample-lossを一律強制せず、estimator/analysis capabilityに適用可能なdiagnosticを明示的に生成・保存するcurrent modelを正本とする。
- `FR-062 → D3`: automated hyperparameter selectionは将来Predictive capability enhancementへ延期する。

## 4. Downstream impact

- FR-048のRequirement/Designをcapability-dependent diagnosticsへ訂正する。
- FR-062はRequirement Status=`DEFERRED`, Delivery=`FUTURE`とし、`90_technical_debt_and_future_enhancements.md`へtraceする。
- ENH-E5でsearch strategy/CV/tuning engineを新設しない。
