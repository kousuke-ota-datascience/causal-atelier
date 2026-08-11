# Architecture / API Documentation Correction

> **Non-normative preflight finding.** 実装・検証仕様は正本文書および06/Pxx/07へ収束させる。

## 1. Scope

current sourceに存在しないOutbox/Portsや過剰なschema-example sync assertionを訂正する。

## 2. Audit facts

| ID | Alignment | Statement | Audit finding | Source evidence |
|---|---|---|---|---|
| D22-001 | MISMATCH | Metadata DB / Outbox / Artifact Store are current runtime components | No canonical Product Outbox resource/publisher is present in E4 completion implementation. | persistence/orm_models.py; product source tree |
| D22-002 | MISMATCH | implemented Port set includes repository, artifact store, runner, clock, auth, event | Current product ports are artifact_store, clock, repositories, scientific_core, unit_of_work; runner/auth/event ports are not present. | src/ariadne/product/ports directory |
| FR-120 | PARTIAL_MATCH | OpenAPIとSchema exampleを正本contractと同期する | FastAPI generates OpenAPI, but systematic synchronization of canonical schema examples was not established. | interfaces/web_api/app.py; routers; product_closure_service.py; dependencies.py; adapters |

## 3. Confirmed remediation

current architecture/OpenAPI generationはD1。systematic schema-example syncはD3。

| Decision Item | Decision | Substatement | Delivery | TD Ref |
|---|---|---|---|---|
| D22-001 | **D1** | Outbox as current runtime component | BASELINE |  |
| D22-002 | **D1** | Runner/Auth/Event Ports as current implemented Ports | BASELINE |  |
| FR-120a | **D1** | OpenAPI generated from runtime API schema | BASELINE |  |
| FR-120b | **D3** | Systematic canonical schema-example synchronization | FUTURE | TD-013 |

## 4. Downstream impact

- D1: current contract記述を10/21/22/23/30へ反映する。
- D2: ENH-E5 targetとして必要なdesign/validation/API/UI/test seamを正本文書へ具体化し、NFR-019 PASS後に06/Pxx・07へ収束する。
- D3: current targetから分離し、`90_technical_debt_and_future_enhancements.md`へtraceする。
