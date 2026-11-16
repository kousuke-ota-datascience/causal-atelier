<!-- ENH-E11 split working copy: not a formal approval. -->
# 23 — crosscut verification

**Status:** `STRUCTURAL_COPY_DRAFT` (existing baseline text, not E11 canonical publication)

**Source:** [23_api_interface_design.md](https://github.com/kousuke-ota-datascience/causal-atelier/blob/3ba5fe2465ec591f0da7f998c21a5241984b73dc/docs/wiki/requirement_definition/23_api_interface_design.md) · blob `131467f02222f105a49e6dfdbcec0f49cadb0f41`  
**Index:** [Revised document inventory](../README_00_Revised_requirements_definition_documents.md)

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

### 8.2 Idempotency

Idempotencyはretryでduplicate durable side effectを生成し得るCommandへ適用する。HTTP methodや「create」一般を判定基準にしない。

Scope:

```text
(project_id, command_scope, idempotency_key)
```

Required semantics:

- required key missing → `IDEMPOTENCY_KEY_REQUIRED`
- same key + same canonical semantic request → stored response replay、duplicate durable side effectなし
- same key + different request → HTTP 409 `IDEMPOTENCY_CONFLICT`
- request hashはpath上のsemantic resource identityを含む
- concurrent same-key requestはDB uniqueness/advisory lock等でsingle durable effectへ収束する
- idempotency replay recordは可能な限り対象metadata mutationと同一transactionでcommitする

Current contractでidempotency対象とするCommand:

- DatasetVersion create
- Execution batch create
- GraphVersion create
- GraphEditDraft create
- Result export create
- AnalysisView create
- Exploration execution submit
- Exploratory Result → AnalysisSpecification DRAFT create
- ResearchContext create
- AnalysisSpecification create / revise
- Predictive split-validation（durable Execution/Artifactを生成する場合）
- Predictive Execution submit / rerun / revise
- Annotation / WorkspaceAnnotation create
- Project Export create

対象外:

- pure GET/query/compare/preview/validate
- existing natural plan-hash idempotencyを持つExecutionPlan create
- uniquenessで重複を防ぐexplicit lineage link
- Project create
- cancel/fix/update等のstate-machine Command（別途自然なstate conflictで制御）

#### 8.2.1 Retry-safe Artifact materialization

exactly-once executionは保証しない。successful Stage outputのretry/restartでdurable Artifactを重複materializeしない。

- logical identity/object keyはExecution + Stage + output slot/ordinal + Artifact typeからdeterministically導出する。
- same logical output + same content hashは既存Artifactをreuseする。
- same logical output + different content hashはnondeterministic-output conflictとして失敗させる。
- Result/Artifact bindingはmetadata transactionでatomicに確定する。
- ArtifactStoreとmetadata DBのcross-store compensationはNFR-007に対応する`DEFERRED` scopeである。

### 8.3 Contract Versioning

Version axis:

- URL major: `/api/v1`
- Analysis Specification envelope: `analysis-specification/1`
- Family spec: `family_spec_schema_version`
- Execution Plan: `execution-plan/1`
- runtime Stage identity: `namespace / name / version`
- Navigation metadata: `analysis-navigation/1`

Navigation Stageのlabel/order変更をruntime `StageType.version`変更と連動させない。

破壊的persistent/scientific contract変更は新schema versionとして扱う。Presentation-only metadata変更とscientific snapshot versioningを同一version axisへ混在させない。

### 8.4 禁止interface

次のinterfaceを導入しない。

1. `AnalysisSpecification.current_family`
2. `AnalysisSpecification.navigation_stage`
3. `Execution.navigation_stage`
4. `StageExecution.navigation_stage`
5. Navigation Stage IDを`StageType`として流用するcontract
6. Navigation Stageごとの機械的なExecution endpoint増設
7. public `claim_token` resource/API
8. Family/Stage route changeをruntime lifecycle eventへ変換するevent contract
9. Findings / Model ManagementというUI名だけを理由とする重複Result/Artifact/Annotation resource
10. Navigation metadataをscientific generic `SchemaRegistry`へ登録するinterface
11. persisted `EXECUTE` role / system Operator roleをcurrent project authorizationへ無根拠に追加するinterface
12. Analysis Context専用backend resource/APIをUI都合だけで新設するinterface
13. Project route stateをAnalysis navigation stateへ混在させるinterface
14. UI Stage配置を理由にExploratory/Predictive/Causalのbackend operation/APIを増設するinterface

## 9. Interface verification観点

- `analysis_family`の値集合が`EXPLORATORY / CAUSAL / PREDICTIVE`で一意である。
- `AnalysisSpecification`にnavigation-only fieldが追加されていない。
- CLI/library/backend executionがNavigation metadata readなしで成立する。
- runtime `StageType`とNavigation Stage IDが別type/namespaceとして扱われる。
- Worker claimが`Execution.lease_owner / lease_expires_at`をauthorityとし、存在しないpublic claim resourceを前提にしない。
- Result / Annotation / Artifactのpublic pathとresponse fieldが本文contractと一致する。
- Findings / Model Managementのread surfaceが§11〜12で定義したResult / Annotation / Artifact / Lineage responsibilityを利用し、UI名だけの重複Resourceを作らない。
- Navigation route changeがExecution / StageExecution stateを変化させない。
- Project Management routeとAnalysis routeが別authorityとしてdirect-link / reload / Back / Forwardを復元できる。
- Analysis Contextは既存Project/Context/Dataset/Analysis View contractを再利用し、専用persistent/API resourceを要求しない。
- Dataset Version変更時のincompatible Analysis View deselectionをclient/application stateで扱い、Family/Stage routeを書き換えない。
- `GET /api/v1/navigation/analysis`が`analysis-navigation/1`のfrozen catalogを返す。
- AnalysisView type mismatchが`FILTER_TYPE_MISMATCH`を返す。
- required idempotency key missingが`IDEMPOTENCY_KEY_REQUIRED`、same key/different requestが409 `IDEMPOTENCY_CONFLICT`となる。
- VIEWERがexplicit sensitive prediction/local-explanation detailへアクセスできない。
- `StageAttempt.effective_random_seed`と`runtime_version_json`がreproducibility contractを満たす。
- `DEFERRED` interface（general AuditLog/retention/object-store等）をcurrent mandatory acceptanceへ混ぜない。
