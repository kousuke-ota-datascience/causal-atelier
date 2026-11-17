# 23_12_api_analysis_specification


---

## 5. Web API Interface

### 5.3 Analysis Specification API

#### 5.3.1 Common envelope

Analysis Specificationのschema versionは`analysis-specification/1`であり、Family固有payloadを共通envelopeに保持する。

Canonical envelope field:

```json
{
  "schema_version": "analysis-specification/1",
  "analysis_family": "PREDICTIVE",
  "research_context_version_id": "uuid",
  "dataset_version_id": "uuid",
  "analysis_view_id": "uuid-or-null",
  "analysis_mode": "CONFIRMATORY",
  "family_spec_schema_version": "predictive-analysis-spec/1",
  "family_spec": {},
  "revision_context": null,
  "warnings": []
}
```

`analysis_family`は`AnalysisFamily` enumをserializationした値である。

| Enum value | API value | 意味 |
| --- | --- | --- |
| `AnalysisFamily.EXPLORATORY` | `EXPLORATORY` | 探索的分析Capability |
| `AnalysisFamily.CAUSAL` | `CAUSAL` | 因果分析Capability |
| `AnalysisFamily.PREDICTIVE` | `PREDICTIVE` | 予測分析Capability |

Family-specific schema mapping:

| analysis_family | family_spec_schema_version |
| --- | --- |
| `EXPLORATORY` | `exploratory-analysis-spec/1` |
| `CAUSAL` | `causal-analysis-spec/2` |
| `PREDICTIVE` | `predictive-analysis-spec/1` |

このdiscriminatorはAnalysis Specification自身の分析semanticを表す。browser上で現在選択されているtabを表す`current_family`とは意味が異なる。

#### 5.3.2 Analysis Specification resource operations

Current public resource operations:

| Method | Path | 用途 |
| --- | --- | --- |
| POST | `/projects/{project_id}/analysis-specifications` | Family Specification DRAFT作成 |
| GET | `/projects/{project_id}/analysis-specifications` | Project内Specification一覧。現行実装ではFamily / Context / Dataset query filterは受けない |
| GET | `/projects/{project_id}/analysis-specifications/{spec_id}` | Specification取得 |
| PATCH | `/projects/{project_id}/analysis-specifications/{spec_id}` | DRAFT更新 |
| POST | `/projects/{project_id}/analysis-specifications/{spec_id}/validate` | 共通 + Family validation |
| POST | `/projects/{project_id}/analysis-specifications/{spec_id}/fix` | FIXED化 |
| POST | `/projects/{project_id}/analysis-specifications/{spec_id}/revise` | child DRAFT作成 |

#### 5.3.3 Navigation Stageを保存しない

次のfieldはAnalysis Specification envelopeへ追加しない。

```json
{
  "current_family": "PREDICTIVE",
  "navigation_stage": "train",
  "current_stage": "train"
}
```

理由:

- `analysis_family`は分析Capabilityのsemantic discriminatorである。
- Current Family / Navigation StageはUI/application navigation stateである。
- 同じ`AnalysisSpecification`を`Train`、`Metrics`、`Explainability`等の複数Navigation Stageから参照し得る。
- Navigation Stageをspecへ保存すると、UI taxonomy変更がscientific/reproducibility contractへ波及する。

#### 5.3.4 Predictive specification contract

`predictive-analysis-spec/1`は次のtop-level fieldを持つ。

- `schema_version`
- `task_type`
- `prediction_question`
- `feature_spec`
- `split_spec`
- `preprocessing_spec`
- `model_spec`
- `tuning_spec`
- `evaluation_spec`
- `explanation_spec`

Task type:

- `BINARY_CLASSIFICATION`
- `REGRESSION`

Split strategy:

- `RANDOM`
- `STRATIFIED`
- `GROUP`
- `TIME_BASED`

Navigation Stage再配置を理由として、上記field、validation、default semanticsを削除・簡略化しない。

## PREP-01: Router operation source inventory

Evidence: workspace_lifecycle.py source blob eb90bd940fc7a35b84cda0e3fa58235a738cb0a1. Static decorator inventory only; /api/v1 is the app router prefix. 200* = default declared FastAPI code, not a runtime assertion.

| HTTP | Route | Handler | Declared success | Response model |
| --- | --- | --- | --- | --- |
| POST | `/api/v1/projects/{project_id}/analysis-specifications` | `create_analysis_specification` | 201 | untyped |
| GET | `/api/v1/projects/{project_id}/analysis-specifications` | `list_analysis_specifications` | 200* | untyped |
| GET | `/api/v1/projects/{project_id}/analysis-specifications/{spec_id}` | `get_analysis_specification` | 200* | untyped |
| PATCH | `/api/v1/projects/{project_id}/analysis-specifications/{spec_id}` | `patch_analysis_specification` | 200* | untyped |
| POST | `/api/v1/projects/{project_id}/analysis-specifications/{spec_id}/validate` | `validate_analysis_specification` | 200* | untyped |
| POST | `/api/v1/projects/{project_id}/analysis-specifications/{spec_id}/fix` | `fix_analysis_specification` | 200* | untyped |
| POST | `/api/v1/projects/{project_id}/analysis-specifications/{spec_id}/revise` | `revise_analysis_specification` | 201 | untyped |

Observed 7 operations. Identity/path is DEFINED from the router; request DTO, auth, lifecycle, error mapping, idempotency, compatibility and operation-specific tests remain NOT_SPECIFIED until source/DTO/service/OpenAPI verification. This annex is not a complete Contract, nor an Independent Verification PASS.

## PREP-01 — Analysis Specification 7 Operation Request / Response / Errors（2026-11-17）

**Source:** `routers/workspace_lifecycle.py` (blob `eb90bd940fc7a35b84cda0e3fa58235a738cb0a1`), `error_handlers.py`. All routes use `/api/v1` prefix. Source declares `dict[str,Any]` response for all seven operations; **there is no Pydantic response_model**, so no exact field list is asserted without Service return-path inspection. Success body shape is `{items: [...]}` for list; otherwise Service-returned dict with keys **UNVERIFIED**. HTTP errors handled as JSON `{"error":{"code","message","details","request_id"}}` for Domain/RequestValidationError, not application/problem+json. Request validation 400 `INVALID_REQUEST`; 404 `ENTITY_NOT_FOUND`, 409 `RESOURCE_IMMUTABLE`, 422 `INVALID_SCHEMA` possible based on raised DomainError, but *operation reachability not verified*. No invented OAuth contract.

### OP-SPEC-01 — `POST /api/v1/projects/{project_id}/analysis-specifications`

| Category | CURRENT Contract |
|---|---|
| Request path | required path project_id:string |
| Request body | JSON request body `AnalysisSpecificationCreate`; extra keys rejected by DTO. |
| Success | HTTP 201: Service-produced object (untyped keys, UNVERIFIED) |
| Errors | 400 `INVALID_REQUEST` on typed request failures; potential domain errors 404 `ENTITY_NOT_FOUND`, 409 `RESOURCE_IMMUTABLE`, 422 `INVALID_SCHEMA` (reachability **UNVERIFIED**) |

| JSON field | Type / required / constraints |
|---|---|
| `schema_version` | required, literal `analysis-specification/1` (removed before Service call) |
| `specification_key` | required string |
| `analysis_family` | required enum `EXPLORATORY/CAUSAL/PREDICTIVE` |
| `research_context_version_id`, `dataset_version_id` | required string |
| `analysis_view_id` | optional string|null |
| `analysis_mode` | required `EXPLORATORY/CONFIRMATORY` |
| `family_spec_schema_version` | required string |
| `family_spec` | required object |
| `revision_context` | optional object|null |
| `warnings` | optional array[object], default [] |
Router reads `X-User-Id` (default `anonymous`) for created_by; not evidence of authenticated identity.

### OP-SPEC-02 — `GET /api/v1/projects/{project_id}/analysis-specifications`

| Category | CURRENT Contract |
|---|---|
| Request path | required path project_id:string |
| Request body | No query or body declared by Router. |
| Success | HTTP 200: object with `items` list |
| Errors | 400 `INVALID_REQUEST` on typed request failures; potential domain errors 404 `ENTITY_NOT_FOUND`, 409 `RESOURCE_IMMUTABLE`, 422 `INVALID_SCHEMA` (reachability **UNVERIFIED**) |




### OP-SPEC-03 — `GET /api/v1/projects/{project_id}/analysis-specifications/{spec_id}`

| Category | CURRENT Contract |
|---|---|
| Request path | required path project_id:string and spec_id:string |
| Request body | No query or body declared by Router. |
| Success | HTTP 200: Service-produced object (untyped keys, UNVERIFIED) |
| Errors | 400 `INVALID_REQUEST` on typed request failures; potential domain errors 404 `ENTITY_NOT_FOUND`, 409 `RESOURCE_IMMUTABLE`, 422 `INVALID_SCHEMA` (reachability **UNVERIFIED**) |




### OP-SPEC-04 — `PATCH /api/v1/projects/{project_id}/analysis-specifications/{spec_id}`

| Category | CURRENT Contract |
|---|---|
| Request path | required path project_id:string and spec_id:string |
| Request body | JSON request body `AnalysisSpecificationPatch`; extra keys rejected by DTO. |
| Success | HTTP 200: Service-produced object (untyped keys, UNVERIFIED) |
| Errors | 400 `INVALID_REQUEST` on typed request failures; potential domain errors 404 `ENTITY_NOT_FOUND`, 409 `RESOURCE_IMMUTABLE`, 422 `INVALID_SCHEMA` (reachability **UNVERIFIED**) |

| JSON field | Type / required |
|---|---|
| `analysis_family` | optional enum or null |
| `research_context_version_id`, `dataset_version_id`, `analysis_view_id` | optional string|null |
| `analysis_mode` | optional enum|null |
| `family_spec_schema_version` | optional string|null |
| `family_spec`, `revision_context` | optional object|null |
| `warnings` | optional array[object]|null |

Router uses `exclude_unset=True`. Omitted and explicit-null inputs are distinguishable; allowed transitions must be verified in Service.


### OP-SPEC-05 — `POST /api/v1/projects/{project_id}/analysis-specifications/{spec_id}/validate`

| Category | CURRENT Contract |
|---|---|
| Request path | required path project_id:string and spec_id:string |
| Request body | No query or body declared by Router. |
| Success | HTTP 200: Service-produced object (untyped keys, UNVERIFIED) |
| Errors | 400 `INVALID_REQUEST` on typed request failures; potential domain errors 404 `ENTITY_NOT_FOUND`, 409 `RESOURCE_IMMUTABLE`, 422 `INVALID_SCHEMA` (reachability **UNVERIFIED**) |




### OP-SPEC-06 — `POST /api/v1/projects/{project_id}/analysis-specifications/{spec_id}/fix`

| Category | CURRENT Contract |
|---|---|
| Request path | required path project_id:string and spec_id:string |
| Request body | No query or body declared by Router. |
| Success | HTTP 200: Service-produced object (untyped keys, UNVERIFIED) |
| Errors | 400 `INVALID_REQUEST` on typed request failures; potential domain errors 404 `ENTITY_NOT_FOUND`, 409 `RESOURCE_IMMUTABLE`, 422 `INVALID_SCHEMA` (reachability **UNVERIFIED**) |




### OP-SPEC-07 — `POST /api/v1/projects/{project_id}/analysis-specifications/{spec_id}/revise`

| Category | CURRENT Contract |
|---|---|
| Request path | required path project_id:string and spec_id:string |
| Request body | JSON request body `AnalysisSpecificationRevise`; extra keys rejected by DTO. |
| Success | HTTP 201: Service-produced object (untyped keys, UNVERIFIED) |
| Errors | 400 `INVALID_REQUEST` on typed request failures; potential domain errors 404 `ENTITY_NOT_FOUND`, 409 `RESOURCE_IMMUTABLE`, 422 `INVALID_SCHEMA` (reachability **UNVERIFIED**) |

| JSON field | Type / required |
|---|---|
| `change_reason` | string, required |
| `changes` | object, optional, default {} |
Router reads `X-User-Id` (default `anonymous`) for created_by.

**Coverage limit:** These 7 Endpoint contracts document every declared Router input and success code; Service result shape, domain-specific validation branches and real error reachability are still open. Existing §5.3 domain invariants remain required. No runtime tests were run.
