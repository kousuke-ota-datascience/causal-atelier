# Audit / Retention

> **Non-normative preflight finding.** 実装・検証仕様は正本文書および06/Pxx/07へ収束させる。

## 1. Scope

general AuditLogとconfigurable retention/deletion policyがcurrent implementationに存在しないCase Bを整理する。

## 2. Audit facts

| ID | Alignment | Statement | Audit finding | Source evidence |
|---|---|---|---|---|
| FR-122 | MISMATCH | 作成、更新、archive、execution、cancel、retry、exportをaudit logへ記録する | No general AuditLog domain/persistence resource implementing the listed action audit contract was found. | interfaces/web_api/app.py; routers; product_closure_service.py; dependencies.py; adapters |
| FR-126 | MISMATCH | Metadata、Artifact、logの保持期間と削除policyを設定できる | No configurable metadata/artifact/log retention and deletion policy implementation was found. | interfaces/web_api/app.py; routers; product_closure_service.py; dependencies.py; adapters |
| D10-006 | MISMATCH | artifact deletion audit + general audit fields + retention contract are implemented | Annotation revision history exists, but no general AuditLog resource and no configurable retention/deletion audit contract exists; LocalArtifactStore.delete removes file directly. | persistence/orm_models.py; adapters/local_artifact_store.py; web/application services |

## 3. Confirmed remediation

D3。AuditとRetentionを別technical debtとして将来planning ledgerへ送る。

| Decision Item | Decision | Substatement | Delivery | TD Ref |
|---|---|---|---|---|
| FR-122 | **D3** | General operational audit trail | FUTURE | TD-001 |
| FR-126 | **D3** | Configurable retention/deletion policy | FUTURE | TD-002 |
| D10-006a | **D3** | General Audit contract | FUTURE | TD-001 |
| D10-006b | **D3** | Retention/deletion contract | FUTURE | TD-002 |

## 4. Downstream impact

- D1: current contract記述を10/21/22/23/30へ反映する。
- D2: ENH-E5 targetとして必要なdesign/validation/API/UI/test seamを正本文書へ具体化し、NFR-019 PASS後に06/Pxx・07へ収束する。
- D3: current targetから分離し、`90_technical_debt_and_future_enhancements.md`へtraceする。
