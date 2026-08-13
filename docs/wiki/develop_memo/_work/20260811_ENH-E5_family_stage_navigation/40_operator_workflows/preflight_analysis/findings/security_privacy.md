# Security / Privacy

> **Non-normative preflight finding.** 実装・検証仕様は正本文書および06/Pxx/07へ収束させる。

## 1. Scope

Project authorization、row-level sensitive output、future sensitive metadata/configurable minimizationを分離する。

## 2. Audit facts

| ID | Alignment | Statement | Audit finding | Source evidence |
|---|---|---|---|---|
| FR-021 | MISMATCH | 機微列、利用制限および説明をcolumn metadataへ付与できる | Dataset column metadata is essentially logical type/schema; sensitive/use-restriction/description metadata was not implemented. | product/domain/analysis_view.py; interfaces/web_api/routers/dataset_versions.py; exploratory/view compiler; frontend |
| FR-123 | PARTIAL_MATCH | preview、artifact、prediction outputへの機微データ露出を権限と設定で制限する | Sensitive Result payload suppression exists, but uniform policy over preview/artifact/prediction output and configurable controls is not complete. | interfaces/web_api/app.py; routers; product_closure_service.py; dependencies.py; adapters |
| NFR-008 | PARTIAL_MATCH | 認証、認可、入力検証、path traversal防止、secret非露出を行う | Input validation/path safeguards exist in parts; authentication/authorization is not uniformly applied to all API routes. | cross-cutting source/tests: domain/workflow/persistence/web API/worker/frontend/adapters |
| NFR-009 | PARTIAL_MATCH | 機微列、prediction、local explanationの表示・exportを最小化できる | Sensitive output suppression exists for Result detail, but full configurable minimization across prediction/local explanations/exports is partial. | cross-cutting source/tests: domain/workflow/persistence/web API/worker/frontend/adapters |
| AR-020 | PARTIAL_MATCH | local explanationやprediction rowを機微情報として扱える | Sensitive Result handling exists, but row-level prediction/local-explanation handling as a uniform policy is partial. | family capability validation/runners; comparison/lineage/product closure services |

## 3. Confirmed remediation

authorization/row-level sensitive handlingはD2。current safeguardsはD1。metadata-driven configurable policy/auth hardeningはD3。

| Decision Item | Decision | Substatement | Delivery | TD Ref |
|---|---|---|---|---|
| FR-021 | **D3** | Sensitive/use-restriction/description column metadata | FUTURE | TD-006 |
| FR-123a | **D2** | Project authorization across preview/artifact/prediction output | ENH-E5 |  |
| FR-123b | **D3** | Configurable exposure policy based on sensitive metadata | FUTURE | TD-006 |
| NFR-008a | **D1** | Existing input validation/path safeguards | BASELINE |  |
| NFR-008b | **D2** | Project authorization coverage | ENH-E5 |  |
| NFR-008c | **D3** | Production-grade authentication/system security hardening | FUTURE | TD-015 |
| NFR-009a | **D1** | Existing sensitive Result suppression | BASELINE |  |
| NFR-009b | **D3** | Configurable prediction/local-explanation/export minimization | FUTURE | TD-006 |
| AR-020 | **D2** | Treat local explanation/prediction row as potentially sensitive output | ENH-E5 |  |

## 4. Downstream impact

- D1: current contract記述を10/21/22/23/30へ反映する。
- D2: ENH-E5 targetとして必要なdesign/validation/API/UI/test seamを正本文書へ具体化し、NFR-019 PASS後に06/Pxx・07へ収束する。
- D3: current targetから分離し、`90_technical_debt_and_future_enhancements.md`へtraceする。
