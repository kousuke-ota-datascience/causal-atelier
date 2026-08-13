# Worker Reliability / Consistency / Observability

> **Non-normative preflight finding.** 実装・検証仕様は正本文書および06/Pxx/07へ収束させる。

## 1. Scope

current lease/claim/process/loggingと、artifact commit idempotency、cross-store compensation、restart semantics、observability拡張を分離する。

## 2. Audit facts

| ID | Alignment | Statement | Audit finding | Source evidence |
|---|---|---|---|---|
| NFR-006 | PARTIAL_MATCH | Worker再起動時もclaim、retry、artifact commitの二重実行を防ぐ | Lease/claim/retry mechanisms exist; exactly-once artifact commit across worker restart was not fully established. | cross-cutting source/tests: domain/workflow/persistence/web API/worker/frontend/adapters |
| NFR-007 | PARTIAL_MATCH | Metadata transactionとArtifact書込みの失敗補償を定義する | Metadata transactions and artifact storage exist, but a complete documented/implemented compensation protocol for cross-store failures was not established. | cross-cutting source/tests: domain/workflow/persistence/web API/worker/frontend/adapters |
| NFR-010 | PARTIAL_MATCH | APIとWorkerの障害を分離し、実行中断と再開可否を明示する | API and Worker are separate processes/contracts, but explicit restart/resume semantics are partial. | cross-cutting source/tests: domain/workflow/persistence/web API/worker/frontend/adapters |
| NFR-011 | PARTIAL_MATCH | structured log、correlation id、execution id、stage id、metricを出力する | Request/execution/stage identifiers exist, but comprehensive structured logs and metrics are not uniformly implemented. | cross-cutting source/tests: domain/workflow/persistence/web API/worker/frontend/adapters |

## 3. Confirmed remediation

current mechanics D1、artifact commit idempotency D2、compensation/restart/observability overhaulはD3。

| Decision Item | Decision | Substatement | Delivery | TD Ref |
|---|---|---|---|---|
| NFR-006a | **D1** | Current lease/claim/retry mechanics | BASELINE |  |
| NFR-006b | **D2** | Idempotent Artifact commit across retry/restart | ENH-E5 |  |
| NFR-007 | **D3** | Metadata/Artifact cross-store failure compensation | FUTURE | TD-014 |
| NFR-010a | **D1** | API/Worker process separation | BASELINE |  |
| NFR-010b | **D3** | Explicit restart/resume semantics | FUTURE | TD-017 |
| NFR-011a | **D1** | Existing request/execution/stage logging identifiers | BASELINE |  |
| NFR-011b | **D3** | Comprehensive structured logging + metrics | FUTURE | TD-018 |

## 4. Downstream impact

- D1: current contract記述を10/21/22/23/30へ反映する。
- D2: ENH-E5 targetとして必要なdesign/validation/API/UI/test seamを正本文書へ具体化し、NFR-019 PASS後に06/Pxx・07へ収束する。
- D3: current targetから分離し、`90_technical_debt_and_future_enhancements.md`へtraceする。
