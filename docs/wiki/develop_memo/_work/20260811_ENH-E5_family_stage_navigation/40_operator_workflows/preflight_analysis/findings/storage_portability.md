# Storage Portability

> **Non-normative preflight finding.** 実装・検証仕様は正本文書および06/Pxx/07へ収束させる。

## 1. Scope

ArtifactStore Portは存在するがLocalArtifactStoreのみでobject-storage adapterがない。

## 2. Audit facts

| ID | Alignment | Statement | Audit finding | Source evidence |
|---|---|---|---|---|
| NFR-020 | MISMATCH | Local filesystemとobject storageをPortで切り替えられる | ArtifactStore Port exists, but current adapter/wiring contains only LocalArtifactStore; no object-storage adapter is available to switch to. | cross-cutting source/tests: domain/workflow/persistence/web API/worker/frontend/adapters |
| D22-003 | PARTIAL_MATCH | SQL, Filesystem/Object Storage, scientific library, ML library are implemented Port/Adapter variants | LocalArtifactStore exists and scientific core has a port boundary, but there is no object-storage adapter and adapter taxonomy is not implemented as broadly as written. | src/ariadne/adapters; interfaces/web_api/dependencies.py; product/ports/scientific_core.py |

## 3. Confirmed remediation

Port abstractionはD1、object-storage adapter/broader variantsはD3。

| Decision Item | Decision | Substatement | Delivery | TD Ref |
|---|---|---|---|---|
| NFR-020a | **D1** | ArtifactStore Port abstraction | BASELINE |  |
| NFR-020b | **D3** | Object-storage adapter / switching | FUTURE | TD-005 |
| D22-003a | **D1** | Current implemented Port/Adapter boundary | BASELINE |  |
| D22-003b | **D3** | Object-storage / broader adapter variants | FUTURE | TD-005 |

## 4. Downstream impact

- D1: current contract記述を10/21/22/23/30へ反映する。
- D2: ENH-E5 targetとして必要なdesign/validation/API/UI/test seamを正本文書へ具体化し、NFR-019 PASS後に06/Pxx・07へ収束する。
- D3: current targetから分離し、`90_technical_debt_and_future_enhancements.md`へtraceする。
