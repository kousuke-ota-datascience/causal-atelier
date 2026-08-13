# Reproducibility / Execution Snapshot

> **Non-normative preflight finding.** 実装・検証仕様は正本文書および06/Pxx/07へ収束させる。

## 1. Scope

current snapshot metadataと不足するeffective seed/library environmentを分離する。

## 2. Audit facts

| ID | Alignment | Statement | Audit finding | Source evidence |
|---|---|---|---|---|
| FR-007 | PARTIAL_MATCH | Executionは受付時のResearch Context snapshotとhashを保持する | Execution persists analysis_spec_json/objective/rationale and snapshot hash, but a dedicated complete ResearchContext snapshot+hash contract was not confirmed. | product/domain/analysis_specification.py; product/persistence/orm_models.py; workspace lifecycle/query services |
| FR-086 | PARTIAL_MATCH | Stageごとのtimeout、resource limit、random seedを記録する | Random seed and some timeout/lifecycle data exist, but a universal per-stage timeout/resource-limit/random-seed persisted contract is not implemented. | product/workflow/*; domain/execution_plan.py; execution.py; stage_execution.py; worker |
| FR-087 | PARTIAL_MATCH | code、runtime、library、schema versionをExecution snapshotへ固定する | Execution stores code_version/runtime_version_json/schema snapshot, but universal explicit library-version capture was not established. | product/workflow/*; domain/execution_plan.py; execution.py; stage_execution.py; worker |
| NFR-001 | PARTIAL_MATCH | 同一snapshot、code version、seed、runtimeで再実行可能な情報を保持する | Reproducibility metadata is substantial, but complete snapshot/code/seed/runtime coverage for every execution path was not established. | cross-cutting source/tests: domain/workflow/persistence/web API/worker/frontend/adapters |

## 3. Confirmed remediation

current snapshot contractはD1、seed/library environment coverageはD2、resource-limit persistenceはD3。

| Decision Item | Decision | Substatement | Delivery | TD Ref |
|---|---|---|---|---|
| FR-007 | **D1** | Execution context snapshot semantics | BASELINE |  |
| FR-086a | **D2** | Effective random seed persistence for stochastic stages | ENH-E5 |  |
| FR-087a | **D1** | Code/runtime/schema snapshot metadata | BASELINE |  |
| FR-087b | **D2** | Effective library version capture | ENH-E5 |  |
| NFR-001a | **D1** | Current reproducibility snapshot/code/runtime metadata | BASELINE |  |
| NFR-001b | **D2** | Seed/library-environment reproducibility coverage | ENH-E5 |  |

## 4. Downstream impact

- D1: current contract記述を10/21/22/23/30へ反映する。
- D2: ENH-E5 targetとして必要なdesign/validation/API/UI/test seamを正本文書へ具体化し、NFR-019 PASS後に06/Pxx・07へ収束する。
- D3: current targetから分離し、`90_technical_debt_and_future_enhancements.md`へtraceする。
