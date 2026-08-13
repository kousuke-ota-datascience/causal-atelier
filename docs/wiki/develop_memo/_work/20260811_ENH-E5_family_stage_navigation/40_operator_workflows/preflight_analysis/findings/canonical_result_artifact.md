# Canonical Result / Artifact / Schema Contract

> **Non-normative preflight finding.** 実装・検証仕様は正本文書および06/Pxx/07へ収束させる。

## 1. Scope

Result/Artifactへfamilyやgeneric schema_versionを一律に複製するE4 targetと、current canonical ownershipの差異を整理する。

## 2. Audit facts

| ID | Alignment | Statement | Audit finding | Source evidence |
|---|---|---|---|---|
| FR-090 | MISMATCH | 共通Result Envelopeにfamily、type、schema version、execution、stageを保持する | Canonical Result does not directly contain family or generic schema_version; execution result may have no stage_execution_id. | product/persistence/orm_models.py; product/application/product_closure_service.py; comparison/lineage services; results router |
| FR-092 | MISMATCH | Artifactにfamily、type、schema version、media type、hash、sizeを保持する | Canonical Artifact contains type/media/hash/size but not family or generic schema_version. | product/persistence/orm_models.py; product/application/product_closure_service.py; comparison/lineage services; results router |
| NFR-013 | MISMATCH | すべてのSpec、Plan、Result、Artifact descriptorにschema versionを持つ | Spec/Plan have schema versions, but canonical Result/Artifact descriptors do not each directly carry a generic schema_version. | cross-cutting source/tests: domain/workflow/persistence/web API/worker/frontend/adapters |
| FR-068 | PARTIAL_MATCH | prediction、residual / error、metric、model、preprocessorをArtifactとして保存する | Model/preprocessor/prediction artifacts exist, but metrics/errors are primarily Result payloads rather than all being Artifact resources as stated. | capabilities/predictive/validation.py; planner.py; metrics.py; training/explanation runners |

## 3. Confirmed remediation

D1中心。Result/Artifactのcurrent canonical responsibilityを正本として採用し、E5でschema migrationは行わない。

| Decision Item | Decision | Substatement | Delivery | TD Ref |
|---|---|---|---|---|
| FR-090 | **D1** | Canonical Result ownership/descriptor contract | BASELINE |  |
| FR-092 | **D1** | Canonical Artifact descriptor/ownership contract | BASELINE |  |
| NFR-013 | **D1** | Versioning at contract boundaries rather than generic field on every entity | BASELINE |  |
| FR-068 | **D1** | Result vs Artifact responsibility for predictive outputs | BASELINE |  |

## 4. Downstream impact

- D1: current contract記述を10/21/22/23/30へ反映する。
- D2: ENH-E5 targetとして必要なdesign/validation/API/UI/test seamを正本文書へ具体化し、NFR-019 PASS後に06/Pxx・07へ収束する。
- D3: current targetから分離し、`90_technical_debt_and_future_enhancements.md`へtraceする。
