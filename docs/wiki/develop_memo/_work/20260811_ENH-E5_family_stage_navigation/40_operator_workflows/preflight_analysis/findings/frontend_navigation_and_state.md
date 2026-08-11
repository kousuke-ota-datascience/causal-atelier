# Frontend Navigation / UI State / Accessibility

> **Non-normative preflight finding.** 実装・検証仕様は正本文書および06/Pxx/07へ収束させる。

## 1. Scope

ENH-E5 navigation改修に直接関係するdeep link/action state/async state/accessibilityと、future filter/CLIを分離する。

## 2. Audit facts

| ID | Alignment | Statement | Audit finding | Source evidence |
|---|---|---|---|---|
| FR-108 | MISMATCH | Result、Execution、Graph、Analysisへ直接遷移できる | Frontend routes are workspace surfaces; dedicated deep routes to Result/Execution/Graph/Analysis resources are not generally implemented. | product/persistence/orm_models.py; product/application/product_closure_service.py; comparison/lineage services; results router |
| FR-110 | MISMATCH | 一覧と比較でfamily、status、dataset、context、dateによるfilterを提供する | Results UI filters by a narrower set (e.g. family/type/status); dataset/context/date filtering is not fully implemented. | frontend/app.js; frontend/index.html; interfaces/web_api/app.py; routers |
| FR-107 | PARTIAL_MATCH | 操作可否をBackendの正本状態から導出し、拒否理由を表示する | Some APIs expose allowed_actions/backend-derived state, but this policy is not uniformly enforced across all controls. | product/persistence/orm_models.py; product/application/product_closure_service.py; comparison/lineage services; results router |
| FR-109 | PARTIAL_MATCH | 非同期処理のloading、empty、partial、error、cancel状態を区別する | Loading/empty/error states exist in places, but the full loading/empty/partial/error/cancel state taxonomy is not consistently implemented. | product/persistence/orm_models.py; product/application/product_closure_service.py; comparison/lineage services; results router |
| FR-111 | PARTIAL_MATCH | keyboard操作、focus、label、contrast等の基本accessibilityを満たす | Labels/ARIA/keyboard-related markup exists, but complete keyboard/focus/contrast conformance was not demonstrated. | frontend/app.js; frontend/index.html; interfaces/web_api/app.py; routers |
| NFR-012 | PARTIAL_MATCH | 主要操作をkeyboardで実行でき、状態を色だけで伝えない | Some accessibility support exists, but complete keyboard/non-color state conformance was not evidenced. | cross-cutting source/tests: domain/workflow/persistence/web API/worker/frontend/adapters |
| FR-118 | MISMATCH | CLIからFamily別Specificationをsubmitしstatus/resultを取得できる | Current scientific CLI runs local/headless scientific stages; it is not a generic Product CLI for submitting Family specifications and polling Product status/results. | frontend/app.js; frontend/index.html; interfaces/web_api/app.py; routers |

## 3. Confirmed remediation

deep navigation/state/accessibilityはD2。existing filtersはD1、追加filter/Product CLIはD3。

| Decision Item | Decision | Substatement | Delivery | TD Ref |
|---|---|---|---|---|
| FR-108 | **D2** | Direct/deep resource navigation | ENH-E5 |  |
| FR-110a | **D1** | Existing results filters (family/type/status等) | BASELINE |  |
| FR-110b | **D3** | Dataset/context/date filter expansion | FUTURE | TD-010 |
| FR-118 | **D3** | Product submit/poll CLI | FUTURE | TD-009 |
| FR-107 | **D2** | Backend-authoritative action availability / rejection reason | ENH-E5 |  |
| FR-109 | **D2** | Async UI state taxonomy loading/empty/partial/error/cancel | ENH-E5 |  |
| FR-111 | **D2** | Keyboard/focus/label/contrast accessibility | ENH-E5 |  |
| NFR-012 | **D2** | Keyboard + non-color state accessibility | ENH-E5 |  |

## 4. Downstream impact

- D1: current contract記述を10/21/22/23/30へ反映する。
- D2: ENH-E5 targetとして必要なdesign/validation/API/UI/test seamを正本文書へ具体化し、NFR-019 PASS後に06/Pxx・07へ収束する。
- D3: current targetから分離し、`90_technical_debt_and_future_enhancements.md`へtraceする。
