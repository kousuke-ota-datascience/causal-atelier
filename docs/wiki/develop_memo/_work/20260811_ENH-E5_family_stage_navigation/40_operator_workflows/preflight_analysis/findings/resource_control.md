# Resource Configuration / Resource Control

> **Non-normative preflight finding.** 実装・検証仕様は正本文書および06/Pxx/07へ収束させる。

## 1. Scope

registry-based capability managementとoperational limits/resource controlを分離する。

## 2. Audit facts

| ID | Alignment | Statement | Audit finding | Source evidence |
|---|---|---|---|---|
| FR-128 | MISMATCH | Algorithm、Runner、size limit、timeoutをconfigurationで管理する | Algorithm/runner/size/timeout configuration is not comprehensively externalized/configurable. | interfaces/web_api/app.py; routers; product_closure_service.py; dependencies.py; adapters |
| NFR-017 | MISMATCH | upload size、row count、column count、memory、timeoutに明示上限を持つ | No comprehensive explicit limits for upload size/rows/columns/memory/timeout were found. | cross-cutting source/tests: domain/workflow/persistence/web API/worker/frontend/adapters |
| FR-086 | PARTIAL_MATCH | Stageごとのtimeout、resource limit、random seedを記録する | Random seed and some timeout/lifecycle data exist, but a universal per-stage timeout/resource-limit/random-seed persisted contract is not implemented. | product/workflow/*; domain/execution_plan.py; execution.py; stage_execution.py; worker |

## 3. Confirmed remediation

Registry managementはD1。size/timeout/memory等の包括resource controlはD3。

| Decision Item | Decision | Substatement | Delivery | TD Ref |
|---|---|---|---|---|
| FR-128a | **D1** | Registry-based Algorithm / Runner management | BASELINE |  |
| FR-128b | **D3** | Operational size/timeout configuration | FUTURE | TD-004 |
| NFR-017 | **D3** | Explicit upload/row/column/memory/timeout hard limits | FUTURE | TD-004 |
| FR-086b | **D3** | Per-stage timeout/resource limit persistence | FUTURE | TD-004 |

## 4. Downstream impact

- D1: current contract記述を10/21/22/23/30へ反映する。
- D2: ENH-E5 targetとして必要なdesign/validation/API/UI/test seamを正本文書へ具体化し、NFR-019 PASS後に06/Pxx・07へ収束する。
- D3: current targetから分離し、`90_technical_debt_and_future_enhancements.md`へtraceする。
