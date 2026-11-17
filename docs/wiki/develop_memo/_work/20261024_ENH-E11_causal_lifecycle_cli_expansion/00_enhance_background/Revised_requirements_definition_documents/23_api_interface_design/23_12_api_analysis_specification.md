# 23_12_api_analysis_specification — Analysis Specification Web API仕様

## 1. API概要

- 対象: Analysis Specification のHTTP契約。
- Base path: `/api/v1`。
- 本改訂はOwner採用の**Operation単位Request/Response/Errors定義**を対象とする。実行時PASSや要件変更を含まない。
- Source snapshot: `89d4f135d8c680805731934e715b079ea0f72f2b`。Currentに対する未検証事項を明示する。

## 2. エンドポイント一覧

| No. | HTTP | Path | Handler | HTTP Success |
|---:|---|---|---|---|
| 1 | `POST` | `/api/v1/projects/{project_id}/analysis-specifications` | `create_analysis_specification` | `201` |
| 2 | `GET` | `/api/v1/projects/{project_id}/analysis-specifications` | `list_analysis_specifications` | `200` |
| 3 | `GET` | `/api/v1/projects/{project_id}/analysis-specifications/{spec_id}` | `get_analysis_specification` | `200` |
| 4 | `PATCH` | `/api/v1/projects/{project_id}/analysis-specifications/{spec_id}` | `patch_analysis_specification` | `200` |
| 5 | `POST` | `/api/v1/projects/{project_id}/analysis-specifications/{spec_id}/validate` | `validate_analysis_specification` | `200` |
| 6 | `POST` | `/api/v1/projects/{project_id}/analysis-specifications/{spec_id}/fix` | `fix_analysis_specification` | `200` |
| 7 | `POST` | `/api/v1/projects/{project_id}/analysis-specifications/{spec_id}/revise` | `revise_analysis_specification` | `201` |

## 3. 共通Error Response形式

CURRENTのDomainError/RequestValidationError Handlerは`application/problem+json`ではなく、以下のJSON envelope。

```json
{"error":{"code":"INVALID_REQUEST","message":"Request validation failed.","details":{},"request_id":"{request_id}"}}
```

共通Handlerに定義されたErrorがすべてのOperationから発生するとは限らない。下表の条件付きErrorはテストPASS済みという意味ではない。

## 4. エンドポイント詳細

### 4.1 `POST /api/v1/projects/{project_id}/analysis-specifications`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-12-01` |
| Method / Path | `POST /api/v1/projects/{project_id}/analysis-specifications` |
| Handler | `workspace_lifecycle.py::create_analysis_specification` |
| Success Status | HTTP 201 |

#### Request

**Path parameters**

| 項目 | 型 | 必須 |
|---|---|---|
| `project_id` | string | 必須 |

**Query parameters**

なし

**Headers**

| Header | 仕様 |
|---|---|
| `X-User-Id` | Routerから参照。認証方式の確証ではない |

**Request Body / Field定義**

Content-Type: `application/json`、型 `AnalysisSpecificationCreate`

| 項目（wire） | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `schema_version` | `Literal["analysis-specification/1"]` | 必須 | 不可 | — |
| `specification_key` | `str` | 必須 | 不可 | — |
| `analysis_family` | `Literal["EXPLORATORY", "CAUSAL", "PREDICTIVE"]` | 必須 | 不可 | — |
| `research_context_version_id` | `str` | 必須 | 不可 | — |
| `dataset_version_id` | `str` | 必須 | 不可 | — |
| `analysis_view_id` | `str \| None` | 任意 | 許可 | None |
| `analysis_mode` | `Literal["EXPLORATORY", "CONFIRMATORY"]` | 必須 | 不可 | — |
| `family_spec_schema_version` | `str` | 必須 | 不可 | — |
| `family_spec` | `dict[str, Any]` | 必須 | 不可 | — |
| `revision_context` | `dict[str, Any] \| None` | 任意 | 許可 | None |
| `warnings` | `list[dict[str, Any]]` | 任意 | 不可 | Field(default_factory=list) |

**Request JSON例（schema由来の説明用）**

```json
{
  "schema_version": "analysis-specification/1",
  "specification_key": "string",
  "analysis_family": "EXPLORATORY",
  "research_context_version_id": "{research_context_version_id}",
  "dataset_version_id": "{dataset_version_id}",
  "analysis_mode": "EXPLORATORY",
  "family_spec_schema_version": "string",
  "family_spec": {}
}
```

#### Response

- HTTP **201**。Body schema: AnalysisSpecification JSON。

| 項目 | 型 | 出所 |
|---|---|---|
| `analysis_specification_id` | `string` | `WorkspaceLifecycleService._specification_response` |
| `project_id` | `string` | `WorkspaceLifecycleService._specification_response` |
| `specification_key` | `string` | `WorkspaceLifecycleService._specification_response` |
| `version_number` | `integer` | `WorkspaceLifecycleService._specification_response` |
| `status` | `string` | `WorkspaceLifecycleService._specification_response` |
| `schema_version` | `string` | `WorkspaceLifecycleService._specification_response` |
| `analysis_family` | `string` | `WorkspaceLifecycleService._specification_response` |
| `research_context_version_id` | `string` | `WorkspaceLifecycleService._specification_response` |
| `dataset_version_id` | `string` | `WorkspaceLifecycleService._specification_response` |
| `analysis_view_id` | `string|null` | `WorkspaceLifecycleService._specification_response` |
| `analysis_mode` | `string` | `WorkspaceLifecycleService._specification_response` |
| `family_spec_schema_version` | `string` | `WorkspaceLifecycleService._specification_response` |
| `family_spec` | `object` | `WorkspaceLifecycleService._specification_response` |
| `revision_context` | `object|null` | `WorkspaceLifecycleService._specification_response` |
| `warnings` | `array[object]` | `WorkspaceLifecycleService._specification_response` |
| `canonical_hash` | `string|null` | `WorkspaceLifecycleService._specification_response` |
| `created_by` | `string` | `WorkspaceLifecycleService._specification_response` |
| `created_at` | `datetime` | `WorkspaceLifecycleService._specification_response` |
| `fixed_at` | `datetime|null` | `WorkspaceLifecycleService._specification_response` |

**Response JSON構造例（説明用）**

```json
{
  "analysis_specification_id": "{spec_id}",
  "project_id": "{project_id}",
  "specification_key": "string",
  "version_number": 1,
  "status": "DRAFT",
  "schema_version": "analysis-specification/1",
  "analysis_family": "EXPLORATORY",
  "research_context_version_id": "{context_id}",
  "dataset_version_id": "{dataset_id}",
  "analysis_view_id": null,
  "analysis_mode": "EXPLORATORY",
  "family_spec_schema_version": "exploratory-analysis-spec/1",
  "family_spec": {},
  "revision_context": null,
  "warnings": [],
  "canonical_hash": null,
  "created_by": "string",
  "created_at": "2026-11-17T00:00:00Z",
  "fixed_at": null
}
```

#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗した場合 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 指定Resourceがない・別Projectである等、ServiceがEntityNotFoundを送出 | Handlerで確定、実到達は要確認 |
| 409 | PROJECT_ARCHIVED / RESOURCE_IMMUTABLE | ARCHIVEDまたはFIXEDに対する不適格変更の際、該当例外を送出した場合 | Handlerで確定、Operationごとの到達は要確認 |
| 422 | INVALID_SCHEMA | Study/Family/Referencesの整合性、FIXED Context/Analysis View要件、revision前提等でServiceのInvalidSchemaが発生 | Service/Domainで具体化 |

#### 根拠・未検証事項

- Router Source: `workspace_lifecycle.py`（blob `eb90bd940fc7a35b84cda0e3fa58235a738cb0a1`）。Request DTO: `AnalysisSpecificationCreate`、Response Model: `未宣言`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.2 `GET /api/v1/projects/{project_id}/analysis-specifications`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-12-02` |
| Method / Path | `GET /api/v1/projects/{project_id}/analysis-specifications` |
| Handler | `workspace_lifecycle.py::list_analysis_specifications` |
| Success Status | HTTP 200 |

#### Request

**Path parameters**

| 項目 | 型 | 必須 |
|---|---|---|
| `project_id` | string | 必須 |

**Query parameters**

なし

**Headers**

Router固有の必須Header宣言なし

**Request Body / Field定義**

Request JSON Bodyなし（Router未定義）。

#### Response

- HTTP **200**。Body schema: Serviceの`AnalysisSpecification[]`。

| 項目 | 型 |
|---|---|
| `items` | array[AnalysisSpecification response] |

itemsの要素:

| 項目 | 型 | 出所 |
|---|---|---|
| `analysis_specification_id` | `string` | `WorkspaceLifecycleService._specification_response` |
| `project_id` | `string` | `WorkspaceLifecycleService._specification_response` |
| `specification_key` | `string` | `WorkspaceLifecycleService._specification_response` |
| `version_number` | `integer` | `WorkspaceLifecycleService._specification_response` |
| `status` | `string` | `WorkspaceLifecycleService._specification_response` |
| `schema_version` | `string` | `WorkspaceLifecycleService._specification_response` |
| `analysis_family` | `string` | `WorkspaceLifecycleService._specification_response` |
| `research_context_version_id` | `string` | `WorkspaceLifecycleService._specification_response` |
| `dataset_version_id` | `string` | `WorkspaceLifecycleService._specification_response` |
| `analysis_view_id` | `string|null` | `WorkspaceLifecycleService._specification_response` |
| `analysis_mode` | `string` | `WorkspaceLifecycleService._specification_response` |
| `family_spec_schema_version` | `string` | `WorkspaceLifecycleService._specification_response` |
| `family_spec` | `object` | `WorkspaceLifecycleService._specification_response` |
| `revision_context` | `object|null` | `WorkspaceLifecycleService._specification_response` |
| `warnings` | `array[object]` | `WorkspaceLifecycleService._specification_response` |
| `canonical_hash` | `string|null` | `WorkspaceLifecycleService._specification_response` |
| `created_by` | `string` | `WorkspaceLifecycleService._specification_response` |
| `created_at` | `datetime` | `WorkspaceLifecycleService._specification_response` |
| `fixed_at` | `datetime|null` | `WorkspaceLifecycleService._specification_response` |

**Response JSON構造例（説明用）**

```json
{"items":[]}
```

#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗した場合 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 指定Resourceがない・別Projectである等、ServiceがEntityNotFoundを送出 | Handlerで確定、実到達は要確認 |
| 422 | INVALID_SCHEMA | Study/Family/Referencesの整合性、FIXED Context/Analysis View要件、revision前提等でServiceのInvalidSchemaが発生 | Service/Domainで具体化 |

#### 根拠・未検証事項

- Router Source: `workspace_lifecycle.py`（blob `eb90bd940fc7a35b84cda0e3fa58235a738cb0a1`）。Request DTO: `none`、Response Model: `未宣言`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.3 `GET /api/v1/projects/{project_id}/analysis-specifications/{spec_id}`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-12-03` |
| Method / Path | `GET /api/v1/projects/{project_id}/analysis-specifications/{spec_id}` |
| Handler | `workspace_lifecycle.py::get_analysis_specification` |
| Success Status | HTTP 200 |

#### Request

**Path parameters**

| 項目 | 型 | 必須 |
|---|---|---|
| `project_id` | string | 必須 |
| `spec_id` | string | 必須 |

**Query parameters**

なし

**Headers**

Router固有の必須Header宣言なし

**Request Body / Field定義**

Request JSON Bodyなし（Router未定義）。

#### Response

- HTTP **200**。Body schema: AnalysisSpecification JSON。

| 項目 | 型 | 出所 |
|---|---|---|
| `analysis_specification_id` | `string` | `WorkspaceLifecycleService._specification_response` |
| `project_id` | `string` | `WorkspaceLifecycleService._specification_response` |
| `specification_key` | `string` | `WorkspaceLifecycleService._specification_response` |
| `version_number` | `integer` | `WorkspaceLifecycleService._specification_response` |
| `status` | `string` | `WorkspaceLifecycleService._specification_response` |
| `schema_version` | `string` | `WorkspaceLifecycleService._specification_response` |
| `analysis_family` | `string` | `WorkspaceLifecycleService._specification_response` |
| `research_context_version_id` | `string` | `WorkspaceLifecycleService._specification_response` |
| `dataset_version_id` | `string` | `WorkspaceLifecycleService._specification_response` |
| `analysis_view_id` | `string|null` | `WorkspaceLifecycleService._specification_response` |
| `analysis_mode` | `string` | `WorkspaceLifecycleService._specification_response` |
| `family_spec_schema_version` | `string` | `WorkspaceLifecycleService._specification_response` |
| `family_spec` | `object` | `WorkspaceLifecycleService._specification_response` |
| `revision_context` | `object|null` | `WorkspaceLifecycleService._specification_response` |
| `warnings` | `array[object]` | `WorkspaceLifecycleService._specification_response` |
| `canonical_hash` | `string|null` | `WorkspaceLifecycleService._specification_response` |
| `created_by` | `string` | `WorkspaceLifecycleService._specification_response` |
| `created_at` | `datetime` | `WorkspaceLifecycleService._specification_response` |
| `fixed_at` | `datetime|null` | `WorkspaceLifecycleService._specification_response` |

**Response JSON構造例（説明用）**

```json
{
  "analysis_specification_id": "{spec_id}",
  "project_id": "{project_id}",
  "specification_key": "string",
  "version_number": 1,
  "status": "DRAFT",
  "schema_version": "analysis-specification/1",
  "analysis_family": "EXPLORATORY",
  "research_context_version_id": "{context_id}",
  "dataset_version_id": "{dataset_id}",
  "analysis_view_id": null,
  "analysis_mode": "EXPLORATORY",
  "family_spec_schema_version": "exploratory-analysis-spec/1",
  "family_spec": {},
  "revision_context": null,
  "warnings": [],
  "canonical_hash": null,
  "created_by": "string",
  "created_at": "2026-11-17T00:00:00Z",
  "fixed_at": null
}
```

#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗した場合 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 指定Resourceがない・別Projectである等、ServiceがEntityNotFoundを送出 | Handlerで確定、実到達は要確認 |
| 422 | INVALID_SCHEMA | Study/Family/Referencesの整合性、FIXED Context/Analysis View要件、revision前提等でServiceのInvalidSchemaが発生 | Service/Domainで具体化 |

#### 根拠・未検証事項

- Router Source: `workspace_lifecycle.py`（blob `eb90bd940fc7a35b84cda0e3fa58235a738cb0a1`）。Request DTO: `none`、Response Model: `未宣言`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.4 `PATCH /api/v1/projects/{project_id}/analysis-specifications/{spec_id}`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-12-04` |
| Method / Path | `PATCH /api/v1/projects/{project_id}/analysis-specifications/{spec_id}` |
| Handler | `workspace_lifecycle.py::patch_analysis_specification` |
| Success Status | HTTP 200 |

#### Request

**Path parameters**

| 項目 | 型 | 必須 |
|---|---|---|
| `project_id` | string | 必須 |
| `spec_id` | string | 必須 |

**Query parameters**

なし

**Headers**

Router固有の必須Header宣言なし

**Request Body / Field定義**

Content-Type: `application/json`、型 `AnalysisSpecificationPatch`

| 項目（wire） | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `analysis_family` | `Literal["EXPLORATORY", "CAUSAL", "PREDICTIVE"] \| None` | 任意 | 許可 | None |
| `research_context_version_id` | `str \| None` | 任意 | 許可 | None |
| `dataset_version_id` | `str \| None` | 任意 | 許可 | None |
| `analysis_view_id` | `str \| None` | 任意 | 許可 | None |
| `analysis_mode` | `Literal["EXPLORATORY", "CONFIRMATORY"] \| None` | 任意 | 許可 | None |
| `family_spec_schema_version` | `str \| None` | 任意 | 許可 | None |
| `family_spec` | `dict[str, Any] \| None` | 任意 | 許可 | None |
| `revision_context` | `dict[str, Any] \| None` | 任意 | 許可 | None |
| `warnings` | `list[dict[str, Any]] \| None` | 任意 | 許可 | None |

**Request JSON例（schema由来の説明用）**

```json
{}
```

#### Response

- HTTP **200**。Body schema: AnalysisSpecification JSON。

| 項目 | 型 | 出所 |
|---|---|---|
| `analysis_specification_id` | `string` | `WorkspaceLifecycleService._specification_response` |
| `project_id` | `string` | `WorkspaceLifecycleService._specification_response` |
| `specification_key` | `string` | `WorkspaceLifecycleService._specification_response` |
| `version_number` | `integer` | `WorkspaceLifecycleService._specification_response` |
| `status` | `string` | `WorkspaceLifecycleService._specification_response` |
| `schema_version` | `string` | `WorkspaceLifecycleService._specification_response` |
| `analysis_family` | `string` | `WorkspaceLifecycleService._specification_response` |
| `research_context_version_id` | `string` | `WorkspaceLifecycleService._specification_response` |
| `dataset_version_id` | `string` | `WorkspaceLifecycleService._specification_response` |
| `analysis_view_id` | `string|null` | `WorkspaceLifecycleService._specification_response` |
| `analysis_mode` | `string` | `WorkspaceLifecycleService._specification_response` |
| `family_spec_schema_version` | `string` | `WorkspaceLifecycleService._specification_response` |
| `family_spec` | `object` | `WorkspaceLifecycleService._specification_response` |
| `revision_context` | `object|null` | `WorkspaceLifecycleService._specification_response` |
| `warnings` | `array[object]` | `WorkspaceLifecycleService._specification_response` |
| `canonical_hash` | `string|null` | `WorkspaceLifecycleService._specification_response` |
| `created_by` | `string` | `WorkspaceLifecycleService._specification_response` |
| `created_at` | `datetime` | `WorkspaceLifecycleService._specification_response` |
| `fixed_at` | `datetime|null` | `WorkspaceLifecycleService._specification_response` |

**Response JSON構造例（説明用）**

```json
{
  "analysis_specification_id": "{spec_id}",
  "project_id": "{project_id}",
  "specification_key": "string",
  "version_number": 1,
  "status": "DRAFT",
  "schema_version": "analysis-specification/1",
  "analysis_family": "EXPLORATORY",
  "research_context_version_id": "{context_id}",
  "dataset_version_id": "{dataset_id}",
  "analysis_view_id": null,
  "analysis_mode": "EXPLORATORY",
  "family_spec_schema_version": "exploratory-analysis-spec/1",
  "family_spec": {},
  "revision_context": null,
  "warnings": [],
  "canonical_hash": null,
  "created_by": "string",
  "created_at": "2026-11-17T00:00:00Z",
  "fixed_at": null
}
```

#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗した場合 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 指定Resourceがない・別Projectである等、ServiceがEntityNotFoundを送出 | Handlerで確定、実到達は要確認 |
| 409 | PROJECT_ARCHIVED / RESOURCE_IMMUTABLE | ARCHIVEDまたはFIXEDに対する不適格変更の際、該当例外を送出した場合 | Handlerで確定、Operationごとの到達は要確認 |
| 422 | INVALID_SCHEMA | Study/Family/Referencesの整合性、FIXED Context/Analysis View要件、revision前提等でServiceのInvalidSchemaが発生 | Service/Domainで具体化 |

#### 根拠・未検証事項

- Router Source: `workspace_lifecycle.py`（blob `eb90bd940fc7a35b84cda0e3fa58235a738cb0a1`）。Request DTO: `AnalysisSpecificationPatch`、Response Model: `未宣言`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.5 `POST /api/v1/projects/{project_id}/analysis-specifications/{spec_id}/validate`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-12-05` |
| Method / Path | `POST /api/v1/projects/{project_id}/analysis-specifications/{spec_id}/validate` |
| Handler | `workspace_lifecycle.py::validate_analysis_specification` |
| Success Status | HTTP 200 |

#### Request

**Path parameters**

| 項目 | 型 | 必須 |
|---|---|---|
| `project_id` | string | 必須 |
| `spec_id` | string | 必須 |

**Query parameters**

なし

**Headers**

Router固有の必須Header宣言なし

**Request Body / Field定義**

Request JSON Bodyなし（Router未定義）。

#### Response

- HTTP **200**。Body schema: Validation object。

| 項目 | 型 | 意味 |
|---|---|---|
| `analysis_specification_id` | string | 対象ID |
| `valid` | bool | 成功時true |
| `canonical_hash` | string | Envelope hash |
| `warnings` | array[object] | 検証警告 |

**Response JSON構造例（説明用）**

```json
{"analysis_specification_id":"{spec_id}","valid":true,"canonical_hash":"{hash}","warnings":[]}
```

#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗した場合 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 指定Resourceがない・別Projectである等、ServiceがEntityNotFoundを送出 | Handlerで確定、実到達は要確認 |
| 409 | PROJECT_ARCHIVED / RESOURCE_IMMUTABLE | ARCHIVEDまたはFIXEDに対する不適格変更の際、該当例外を送出した場合 | Handlerで確定、Operationごとの到達は要確認 |
| 422 | INVALID_SCHEMA | Study/Family/Referencesの整合性、FIXED Context/Analysis View要件、revision前提等でServiceのInvalidSchemaが発生 | Service/Domainで具体化 |

#### 根拠・未検証事項

- Router Source: `workspace_lifecycle.py`（blob `eb90bd940fc7a35b84cda0e3fa58235a738cb0a1`）。Request DTO: `none`、Response Model: `未宣言`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.6 `POST /api/v1/projects/{project_id}/analysis-specifications/{spec_id}/fix`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-12-06` |
| Method / Path | `POST /api/v1/projects/{project_id}/analysis-specifications/{spec_id}/fix` |
| Handler | `workspace_lifecycle.py::fix_analysis_specification` |
| Success Status | HTTP 200 |

#### Request

**Path parameters**

| 項目 | 型 | 必須 |
|---|---|---|
| `project_id` | string | 必須 |
| `spec_id` | string | 必須 |

**Query parameters**

なし

**Headers**

Router固有の必須Header宣言なし

**Request Body / Field定義**

Request JSON Bodyなし（Router未定義）。

#### Response

- HTTP **200**。Body schema: AnalysisSpecification JSON。

| 項目 | 型 | 出所 |
|---|---|---|
| `analysis_specification_id` | `string` | `WorkspaceLifecycleService._specification_response` |
| `project_id` | `string` | `WorkspaceLifecycleService._specification_response` |
| `specification_key` | `string` | `WorkspaceLifecycleService._specification_response` |
| `version_number` | `integer` | `WorkspaceLifecycleService._specification_response` |
| `status` | `string` | `WorkspaceLifecycleService._specification_response` |
| `schema_version` | `string` | `WorkspaceLifecycleService._specification_response` |
| `analysis_family` | `string` | `WorkspaceLifecycleService._specification_response` |
| `research_context_version_id` | `string` | `WorkspaceLifecycleService._specification_response` |
| `dataset_version_id` | `string` | `WorkspaceLifecycleService._specification_response` |
| `analysis_view_id` | `string|null` | `WorkspaceLifecycleService._specification_response` |
| `analysis_mode` | `string` | `WorkspaceLifecycleService._specification_response` |
| `family_spec_schema_version` | `string` | `WorkspaceLifecycleService._specification_response` |
| `family_spec` | `object` | `WorkspaceLifecycleService._specification_response` |
| `revision_context` | `object|null` | `WorkspaceLifecycleService._specification_response` |
| `warnings` | `array[object]` | `WorkspaceLifecycleService._specification_response` |
| `canonical_hash` | `string|null` | `WorkspaceLifecycleService._specification_response` |
| `created_by` | `string` | `WorkspaceLifecycleService._specification_response` |
| `created_at` | `datetime` | `WorkspaceLifecycleService._specification_response` |
| `fixed_at` | `datetime|null` | `WorkspaceLifecycleService._specification_response` |

**Response JSON構造例（説明用）**

```json
{
  "analysis_specification_id": "{spec_id}",
  "project_id": "{project_id}",
  "specification_key": "string",
  "version_number": 1,
  "status": "DRAFT",
  "schema_version": "analysis-specification/1",
  "analysis_family": "EXPLORATORY",
  "research_context_version_id": "{context_id}",
  "dataset_version_id": "{dataset_id}",
  "analysis_view_id": null,
  "analysis_mode": "EXPLORATORY",
  "family_spec_schema_version": "exploratory-analysis-spec/1",
  "family_spec": {},
  "revision_context": null,
  "warnings": [],
  "canonical_hash": null,
  "created_by": "string",
  "created_at": "2026-11-17T00:00:00Z",
  "fixed_at": null
}
```

#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗した場合 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 指定Resourceがない・別Projectである等、ServiceがEntityNotFoundを送出 | Handlerで確定、実到達は要確認 |
| 409 | PROJECT_ARCHIVED / RESOURCE_IMMUTABLE | ARCHIVEDまたはFIXEDに対する不適格変更の際、該当例外を送出した場合 | Handlerで確定、Operationごとの到達は要確認 |
| 422 | INVALID_SCHEMA | Study/Family/Referencesの整合性、FIXED Context/Analysis View要件、revision前提等でServiceのInvalidSchemaが発生 | Service/Domainで具体化 |

#### 根拠・未検証事項

- Router Source: `workspace_lifecycle.py`（blob `eb90bd940fc7a35b84cda0e3fa58235a738cb0a1`）。Request DTO: `none`、Response Model: `未宣言`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.7 `POST /api/v1/projects/{project_id}/analysis-specifications/{spec_id}/revise`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-12-07` |
| Method / Path | `POST /api/v1/projects/{project_id}/analysis-specifications/{spec_id}/revise` |
| Handler | `workspace_lifecycle.py::revise_analysis_specification` |
| Success Status | HTTP 201 |

#### Request

**Path parameters**

| 項目 | 型 | 必須 |
|---|---|---|
| `project_id` | string | 必須 |
| `spec_id` | string | 必須 |

**Query parameters**

なし

**Headers**

| Header | 仕様 |
|---|---|
| `X-User-Id` | Routerから参照。認証方式の確証ではない |

**Request Body / Field定義**

Content-Type: `application/json`、型 `AnalysisSpecificationRevise`

| 項目（wire） | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `change_reason` | `str` | 必須 | 不可 | — |
| `changes` | `dict[str, Any]` | 任意 | 不可 | Field(default_factory=dict) |

**Request JSON例（schema由来の説明用）**

```json
{
  "change_reason": "string"
}
```

#### Response

- HTTP **201**。Body schema: AnalysisSpecification JSON。

| 項目 | 型 | 出所 |
|---|---|---|
| `analysis_specification_id` | `string` | `WorkspaceLifecycleService._specification_response` |
| `project_id` | `string` | `WorkspaceLifecycleService._specification_response` |
| `specification_key` | `string` | `WorkspaceLifecycleService._specification_response` |
| `version_number` | `integer` | `WorkspaceLifecycleService._specification_response` |
| `status` | `string` | `WorkspaceLifecycleService._specification_response` |
| `schema_version` | `string` | `WorkspaceLifecycleService._specification_response` |
| `analysis_family` | `string` | `WorkspaceLifecycleService._specification_response` |
| `research_context_version_id` | `string` | `WorkspaceLifecycleService._specification_response` |
| `dataset_version_id` | `string` | `WorkspaceLifecycleService._specification_response` |
| `analysis_view_id` | `string|null` | `WorkspaceLifecycleService._specification_response` |
| `analysis_mode` | `string` | `WorkspaceLifecycleService._specification_response` |
| `family_spec_schema_version` | `string` | `WorkspaceLifecycleService._specification_response` |
| `family_spec` | `object` | `WorkspaceLifecycleService._specification_response` |
| `revision_context` | `object|null` | `WorkspaceLifecycleService._specification_response` |
| `warnings` | `array[object]` | `WorkspaceLifecycleService._specification_response` |
| `canonical_hash` | `string|null` | `WorkspaceLifecycleService._specification_response` |
| `created_by` | `string` | `WorkspaceLifecycleService._specification_response` |
| `created_at` | `datetime` | `WorkspaceLifecycleService._specification_response` |
| `fixed_at` | `datetime|null` | `WorkspaceLifecycleService._specification_response` |

**Response JSON構造例（説明用）**

```json
{
  "analysis_specification_id": "{spec_id}",
  "project_id": "{project_id}",
  "specification_key": "string",
  "version_number": 1,
  "status": "DRAFT",
  "schema_version": "analysis-specification/1",
  "analysis_family": "EXPLORATORY",
  "research_context_version_id": "{context_id}",
  "dataset_version_id": "{dataset_id}",
  "analysis_view_id": null,
  "analysis_mode": "EXPLORATORY",
  "family_spec_schema_version": "exploratory-analysis-spec/1",
  "family_spec": {},
  "revision_context": null,
  "warnings": [],
  "canonical_hash": null,
  "created_by": "string",
  "created_at": "2026-11-17T00:00:00Z",
  "fixed_at": null
}
```

#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗した場合 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 指定Resourceがない・別Projectである等、ServiceがEntityNotFoundを送出 | Handlerで確定、実到達は要確認 |
| 409 | PROJECT_ARCHIVED / RESOURCE_IMMUTABLE | ARCHIVEDまたはFIXEDに対する不適格変更の際、該当例外を送出した場合 | Handlerで確定、Operationごとの到達は要確認 |
| 422 | INVALID_SCHEMA | Study/Family/Referencesの整合性、FIXED Context/Analysis View要件、revision前提等でServiceのInvalidSchemaが発生 | Service/Domainで具体化 |

#### 根拠・未検証事項

- Router Source: `workspace_lifecycle.py`（blob `eb90bd940fc7a35b84cda0e3fa58235a738cb0a1`）。Request DTO: `AnalysisSpecificationRevise`、Response Model: `未宣言`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

## 5. 検証状況

- Route/Method/Path: 7 件 Source確認。
- Request: Router/Pydanticモデルの静的制約を反映。Response: 型付きモデルは全Fieldを表記。Service無型応答は一部未確定。
- HTTP Contract Test: NOT_RUN。Endpoint詳細の完全性・認可・実行時エラー網羅は未検証。
- 元の`docs/wiki/requirement_definition/`への昇格: NOT_DONE。

## 6. 既存Domain・設計制約（旧仕様本文から保持）

以下は既存のDomain規範・補足情報を保持したもの。重複する旧Route一覧より§2（Source基準）を優先する。改訂前の原本文はGit Blob `d8f2389e36be4029cdf2d0f1ea5ff5f4925e3477`で追跡可能。

### Analysis Specification API

#### Common envelope

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

#### Analysis Specification resource operations

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

#### Navigation Stageを保存しない

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

#### Predictive specification contract

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

## 7. 改訂記録

- 2026-11-17: 全23_10〜23_19共通フォーマットへ再構成。Request/Response/ErrorsをOperation別に記載し、Source確認と未検証を分離。
