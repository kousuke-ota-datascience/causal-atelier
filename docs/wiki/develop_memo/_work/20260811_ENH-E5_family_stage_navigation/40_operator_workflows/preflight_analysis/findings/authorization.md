# Authorization Model

> **Non-normative preflight finding.** 実装・検証仕様は正本文書および06/Pxx/07へ収束させる。

## 1. Scope

OWNER/EDITOR/VIEWERのcurrent role taxonomyとrouter coverage gap、system Operator targetを分離する。

## 2. Audit facts

| ID | Alignment | Statement | Audit finding | Source evidence |
|---|---|---|---|---|
| D10-005 | MISMATCH | read/write/execute/Operator permission taxonomy is the implemented authorization model | Persisted Project roles are OWNER/EDITOR/VIEWER; no distinct execute/Operator role model exists and authorization is not uniformly applied to all routers. | product/application/product_closure_service.py; web routers |
| FR-121 | PARTIAL_MATCH | Project単位でread、write、operate権限を検証する | Project Closure enforces OWNER/EDITOR/VIEWER roles, but not all routers uniformly pass through that authorization boundary. | interfaces/web_api/app.py; routers; product_closure_service.py; dependencies.py; adapters |
| FR-124 | PARTIAL_MATCH | Artifact downloadでProject権限とcontent dispositionを検証する | Project-scoped closure artifact download enforces project role and safe headers, but not every artifact route shares the same authorization boundary. | interfaces/web_api/app.py; routers; product_closure_service.py; dependencies.py; adapters |
| FR-123 | PARTIAL_MATCH | preview、artifact、prediction outputへの機微データ露出を権限と設定で制限する | Sensitive Result payload suppression exists, but uniform policy over preview/artifact/prediction output and configurable controls is not complete. | interfaces/web_api/app.py; routers; product_closure_service.py; dependencies.py; adapters |
| NFR-008 | PARTIAL_MATCH | 認証、認可、入力検証、path traversal防止、secret非露出を行う | Input validation/path safeguards exist in parts; authentication/authorization is not uniformly applied to all API routes. | cross-cutting source/tests: domain/workflow/persistence/web API/worker/frontend/adapters |

## 3. Confirmed remediation

D1+D2+D3。role taxonomy D1、Project-scoped authorization coverage D2、system Operator D3。

| Decision Item | Decision | Substatement | Delivery | TD Ref |
|---|---|---|---|---|
| D10-005a | **D1** | Project role taxonomy OWNER/EDITOR/VIEWER | BASELINE |  |
| D10-005b | **D2** | Uniform Project-scoped authorization across routers | ENH-E5 |  |
| D10-005c | **D3** | Distinct Operator / system-operate authorization | FUTURE | TD-003 |
| FR-121 | **D2** | Uniform Project-scoped authorization | ENH-E5 |  |
| FR-124a | **D1** | Existing project-scoped artifact download + safe content disposition | BASELINE |  |
| FR-124b | **D2** | Uniform artifact-route authorization coverage | ENH-E5 |  |

## 4. Downstream impact

- D1: current contract記述を10/21/22/23/30へ反映する。
- D2: ENH-E5 targetとして必要なdesign/validation/API/UI/test seamを正本文書へ具体化し、NFR-019 PASS後に06/Pxx・07へ収束する。
- D3: current targetから分離し、`90_technical_debt_and_future_enhancements.md`へtraceする。
