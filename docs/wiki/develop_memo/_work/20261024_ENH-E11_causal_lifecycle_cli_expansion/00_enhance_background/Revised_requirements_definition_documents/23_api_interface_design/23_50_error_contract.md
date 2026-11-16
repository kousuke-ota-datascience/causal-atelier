# 23_50_error_contract


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

**当該Interfaceの追加契約（関連Requirement）**

- **`FR-115`**：validation、conflict、not found、forbidden、execution failureをcanonical errorで返す
- **`NFR-028`**：optional analytical engineのimport/availability failureをcore process startup failureへ伝播させず、capability discovery/selection時に局所化してstable unavailable state/errorとして報告する
- **`AR-008`**：Eligibilityの型はBINARY、CONTINUOUS、UNSUPPORTED等の正規値で保存する
