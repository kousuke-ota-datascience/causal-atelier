# Operability / Health / Performance

> **Non-normative preflight finding.** 実装・検証仕様は正本文書および06/Pxx/07へ収束させる。

## 1. Scope

basic healthとcomponent readiness、general performance SLOを分離する。

## 2. Audit facts

| ID | Alignment | Statement | Audit finding | Source evidence |
|---|---|---|---|---|
| FR-127 | MISMATCH | API、DB、Worker、Artifact Storeのhealth / readinessを提供する | `/health/ready` returns only `{"status":"ok"}` and does not check API/DB/Worker/Artifact Store component readiness. | interfaces/web_api/app.py; routers; product_closure_service.py; dependencies.py; adapters |
| NFR-004 | MISMATCH | 通常一覧・詳細APIの95 percentileを2秒以内、重い集計は非同期化する | No evidence of a 95th-percentile <=2s acceptance/performance implementation or regression gate was found. | cross-cutting source/tests: domain/workflow/persistence/web API/worker/frontend/adapters |

## 3. Confirmed remediation

basic health D1。component readinessとgeneral p95 SLOはD3。

| Decision Item | Decision | Substatement | Delivery | TD Ref |
|---|---|---|---|---|
| FR-127a | **D1** | Existing basic health endpoint | BASELINE |  |
| FR-127b | **D3** | DB/Worker/Artifact Store component readiness | FUTURE | TD-011 |
| NFR-004 | **D3** | General p95 API SLO / performance regression gate | FUTURE | TD-012 |

## 4. Downstream impact

- D1: current contract記述を10/21/22/23/30へ反映する。
- D2: ENH-E5 targetとして必要なdesign/validation/API/UI/test seamを正本文書へ具体化し、NFR-019 PASS後に06/Pxx・07へ収束する。
- D3: current targetから分離し、`90_technical_debt_and_future_enhancements.md`へtraceする。
