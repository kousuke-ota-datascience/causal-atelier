# 23_50_error_contract

**Status:** `RD02_STRUCTURAL_WORKING_COPY / E11_NOT_PUBLISHED`. Original source section numbering retained; document numbering is by interface responsibility.  
**Source blob:** `131467f02222f105a49e6dfdbcec0f49cadb0f41`.

---

## 8. Cross-cutting Contract Policy

### 8.1 Error Model

Current error envelope:

```json
{
  "error": {
    "code": "INVALID_ANALYSIS_SPEC",
    "message": "human-readable message",
    "details": {},
    "request_id": "uuid-or-request-X-Request-Id"
  }
}
```

`details`はobjectである。Request validation errorでは`{"errors": [...]}`、Predictive validation errorでは`{"path": "..."}`等を格納する。

現行実装で明示されている主なmapping:

| HTTP | code例 | 意味 |
| --- | --- | --- |
| 404 | `ENTITY_NOT_FOUND` | Resource not found |
| 403 | `PROJECT_ACCESS_DENIED` | Project access denied |
| 409 | `PROJECT_ARCHIVED`, `IDEMPOTENCY_CONFLICT`, `RESOURCE_IMMUTABLE`, lifecycle conflict | state/conflict |
| 422 | `PROJECT_BOUNDARY_VIOLATION`, `INVALID_SCHEMA`, `INVALID_ANALYSIS_SPEC`, predictive validation code等 | semantic/domain validation |
| 400 | `INVALID_REQUEST`, fallback `DOMAIN_ERROR` | request validation / generic domain error |
| 500 | `ARTIFACT_HASH_MISMATCH` | persisted metadataとartifact contentのintegrity mismatch |

`401 / 413 / 429`は現行実装のcommon error handlerで一般contractとして定義されていないため、既存contractとして列挙しない。

Navigation catalog/route validation failureをruntime Execution failureへ変換しない。

Error contractに関する追加原則:

- 科学的負結果をtechnical HTTP errorへ変換しない。Result/response内のscientific status / warningとして表現する。
- Navigation catalog/route validation failureをruntime Execution failureへ変換しない。
- Project境界を越えるresource existenceをerror detailで漏洩しない。


## 98. RD-04：IF契約の要求起源・Trace

**Status:** `RD04_INTERFACE_CONSTRAINT_MIGRATED / OWNER_CONTENT_REVIEW_PENDING`。抽象化前のAPI／CLI／Navigationのwire・resource・state契約を失わないための移管記録。現在の実効Implementationを確認したことを意味しない。

### 98.1. FR-115（SPLIT）

- 旧要件に含まれるIF固有情報：validation、conflict、not found、forbidden、execution failureをcanonical errorで返す
- RDの要求核／Legacy Trace：利用側が入力不正・競合・不在・権限不足・処理失敗を判別できる
- `FR-115`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[RD-04逐条レビュー](../95_rd04_fr_application_review.md)

### 98.2. NFR-028（SPLIT）

- 旧要件に含まれるIF固有情報：optional analytical engineのimport/availability failureをcore process startup failureへ伝播させず、capability discovery/selection時に局所化してstable unavailable state/errorとして報告する
- RDの要求核／Legacy Trace：任意の分析エンジンが利用不能でも基本機能を継続でき、利用不能理由を識別できる
- `NFR-028`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[RD-04逐条レビュー](../96_rd04_nfr_ar_application_review.md)

### 98.3. AR-008（SPLIT）

- 旧要件に含まれるIF固有情報：Eligibilityの型はBINARY、CONTINUOUS、UNSUPPORTED等の正規値で保存する
- RDの要求核／Legacy Trace：推定に必要な変数型が適格かを識別できなければならない
- `AR-008`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[RD-04逐条レビュー](../96_rd04_nfr_ar_application_review.md)
