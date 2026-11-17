# 23_14_api_causal — Graph Version / Graph Candidate Web API仕様

## 1. API概要

- 対象: Graph Version / Graph Candidate のHTTP契約。
- Base path: `/api/v1`。
- 本改訂はOwner採用の**Operation単位Request/Response/Errors定義**を対象とする。実行時PASSや要件変更を含まない。
- Source snapshot: `89d4f135d8c680805731934e715b079ea0f72f2b`。Currentに対する未検証事項を明示する。

## 2. エンドポイント一覧

| No. | HTTP | Path | Handler | HTTP Success |
|---:|---|---|---|---|
| 1 | `POST` | `/api/v1/projects/{project_id}/graph-versions` | `create_graph_version` | `201` |
| 2 | `POST` | `/api/v1/projects/{project_id}/graph-edit-drafts` | `create_graph_edit_draft` | `201` |
| 3 | `GET` | `/api/v1/projects/{project_id}/graph-versions` | `list_graph_versions` | `200` |
| 4 | `GET` | `/api/v1/graph-versions/{graph_version_id}` | `get_graph_version` | `200` |
| 5 | `GET` | `/api/v1/projects/{project_id}/graph-versions/{graph_version_id}` | `get_project_graph_version` | `200` |
| 6 | `PATCH` | `/api/v1/graph-versions/{graph_version_id}` | `update_graph_version` | `200` |
| 7 | `PATCH` | `/api/v1/projects/{project_id}/graph-versions/{graph_version_id}` | `update_project_graph_version` | `200` |
| 8 | `POST` | `/api/v1/graph-versions/{graph_version_id}/fix` | `fix_graph_version` | `200` |
| 9 | `POST` | `/api/v1/projects/{project_id}/graph-versions/{graph_version_id}/fix` | `fix_project_graph_version` | `200` |
| 10 | `GET` | `/api/v1/projects/{project_id}/graph-candidates` | `list_graph_candidates` | `200` |
| 11 | `GET` | `/api/v1/projects/{project_id}/graph-candidates/{candidate_kind}/{candidate_id}` | `get_graph_candidate` | `200` |
| 12 | `POST` | `/api/v1/projects/{project_id}/graph-candidate-comparisons/query` | `compare_graph_candidates` | `200` |

## 3. 共通Error Response形式

CURRENTのDomainError/RequestValidationError Handlerは`application/problem+json`ではなく、以下のJSON envelope。

```json
{"error":{"code":"INVALID_REQUEST","message":"Request validation failed.","details":{},"request_id":"{request_id}"}}
```

共通Handlerに定義されたErrorがすべてのOperationから発生するとは限らない。下表の条件付きErrorはテストPASS済みという意味ではない。

## 4. エンドポイント詳細

### 4.1 `POST /api/v1/projects/{project_id}/graph-versions`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-14-01` |
| Method / Path | `POST /api/v1/projects/{project_id}/graph-versions` |
| Handler | `graph_versions.py::create_graph_version` |
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
| `Idempotency-Key` | 該当IdempotencyServiceの再送契約に依存 |
| `X-User-Id` | Routerから参照。認証方式の確証ではない |

**Request Body / Field定義**

Content-Type: `application/json`、型 `GraphVersionCreate`

| 項目（wire） | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `source_result_id` | `str \| None` | 任意 | 許可 | None |
| `parent_graph_version_id` | `str \| None` | 任意 | 許可 | None |
| `graph_origin` | `Literal["DISCOVERED", "CONSTRAINT_ADJUSTED", "USER_DEFINED", "IMPORTED", "USER_EDITED"]` | 必須 | 不可 | — |
| `name` | `str` | 必須 | 不可 | min_length=1, max_length=200 |
| `graph_type` | `Literal["DAG", "CPDAG", "PAG"]` | 必須 | 不可 | — |
| `graph` | `dict[str, Any]` | 必須 | 不可 | — |
| `provenance` | `dict[str, Any]` | 必須 | 不可 | — |
| `designated_outcome_node` | `str \| None` | 任意 | 許可 | lt=None, min_length=1, max_length=200 |
| `edit_rationale` | `str \| None` | 任意 | 許可 | None |
| `fix_immediately` | `bool` | 任意 | 不可 | False |

**Request JSON例（schema由来の説明用）**

```json
{
  "graph_origin": "DISCOVERED",
  "name": "string",
  "graph_type": "DAG",
  "graph": {},
  "provenance": {}
}
```

#### Response

- HTTP **201**。Body schema: `GraphVersionResponse`。

| 項目（wire） | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `graph_version_id` | `str` | 必須 | 不可 | — |
| `project_id` | `str` | 必須 | 不可 | — |
| `source_result_id` | `str \| None` | 必須 | 許可 | — |
| `parent_graph_version_id` | `str \| None` | 必須 | 許可 | — |
| `name` | `str` | 必須 | 不可 | — |
| `graph_type` | `str` | 必須 | 不可 | — |
| `graph` | `dict[str, Any]` | 必須 | 不可 | — |
| `graph_origin` | `str` | 必須 | 不可 | — |
| `provenance` | `dict[str, Any]` | 必須 | 不可 | — |
| `designated_outcome_node` | `str \| None` | 必須 | 許可 | — |
| `content_hash` | `str` | 必須 | 不可 | — |
| `edit_rationale` | `str \| None` | 必須 | 許可 | — |
| `status` | `str` | 必須 | 不可 | — |
| `created_by` | `str` | 必須 | 不可 | — |
| `created_at` | `datetime \| None` | 必須 | 許可 | — |
| `allowed_actions` | `dict[str, Any]` | 任意 | 不可 | Field(default_factory=dict) |

**Response JSON構造例（schema由来の説明用）**

```json
{
  "graph_version_id": "{graph_version_id}",
  "project_id": "{project_id}",
  "source_result_id": "{source_result_id}",
  "parent_graph_version_id": "{parent_graph_version_id}",
  "name": "string",
  "graph_type": "string",
  "graph": {},
  "graph_origin": "string",
  "provenance": {},
  "designated_outcome_node": "string",
  "content_hash": "string",
  "edit_rationale": "string",
  "status": "string",
  "created_by": "string",
  "created_at": "2026-11-17T00:00:00Z",
  "allowed_actions": {}
}
```

#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗した場合 | 共通Handler |
| 400 / 409 | IDEMPOTENCY_KEY_REQUIRED / IDEMPOTENCY_CONFLICT | Key欠落／同一Key・異なる要求内容 | IdempotencyService |
| 404 | ENTITY_NOT_FOUND | 指定Resourceがない・別Projectである等、ServiceがEntityNotFoundを送出 | Handlerで確定、実到達は要確認 |
| 409 | PROJECT_ARCHIVED / RESOURCE_IMMUTABLE | ARCHIVEDまたはFIXEDに対する不適格変更の際、該当例外を送出した場合 | Handlerで確定、Operationごとの到達は要確認 |
| 422/409 | INVALID_GRAPH_SEMANTICS / GRAPH_FIXED_IMMUTABLE | Graph意味論違反、FIXED Graph変更 | 共通Handler;詳細到達は要検証 |

#### 根拠・未検証事項

- Router Source: `graph_versions.py`（blob `ad6ba942ee8ecc95590175ec3de655d3bee9a155`）。Request DTO: `GraphVersionCreate`、Response Model: `GraphVersionResponse`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.2 `POST /api/v1/projects/{project_id}/graph-edit-drafts`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-14-02` |
| Method / Path | `POST /api/v1/projects/{project_id}/graph-edit-drafts` |
| Handler | `graph_versions.py::create_graph_edit_draft` |
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
| `Idempotency-Key` | 該当IdempotencyServiceの再送契約に依存 |
| `X-User-Id` | Routerから参照。認証方式の確証ではない |

**Request Body / Field定義**

Content-Type: `application/json`、型 `GraphEditDraftCreate`

| 項目（wire） | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `base_candidate_kind` | `Literal["DISCOVERY_RESULT", "GRAPH_VERSION"]` | 必須 | 不可 | — |
| `base_candidate_id` | `str` | 必須 | 不可 | — |
| `change_kind` | `Literal["USER_EDITED", "CONSTRAINT_ADJUSTED"]` | 必須 | 不可 | — |
| `name` | `str` | 必須 | 不可 | min_length=1, max_length=200 |
| `edit_rationale` | `str` | 必須 | 不可 | min_length=1, max_length=8000 |

**Request JSON例（schema由来の説明用）**

```json
{
  "base_candidate_kind": "DISCOVERY_RESULT",
  "base_candidate_id": "{base_candidate_id}",
  "change_kind": "USER_EDITED",
  "name": "string",
  "edit_rationale": "string"
}
```

#### Response

- HTTP **201**。Body schema: `GraphVersionResponse`。

| 項目（wire） | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `graph_version_id` | `str` | 必須 | 不可 | — |
| `project_id` | `str` | 必須 | 不可 | — |
| `source_result_id` | `str \| None` | 必須 | 許可 | — |
| `parent_graph_version_id` | `str \| None` | 必須 | 許可 | — |
| `name` | `str` | 必須 | 不可 | — |
| `graph_type` | `str` | 必須 | 不可 | — |
| `graph` | `dict[str, Any]` | 必須 | 不可 | — |
| `graph_origin` | `str` | 必須 | 不可 | — |
| `provenance` | `dict[str, Any]` | 必須 | 不可 | — |
| `designated_outcome_node` | `str \| None` | 必須 | 許可 | — |
| `content_hash` | `str` | 必須 | 不可 | — |
| `edit_rationale` | `str \| None` | 必須 | 許可 | — |
| `status` | `str` | 必須 | 不可 | — |
| `created_by` | `str` | 必須 | 不可 | — |
| `created_at` | `datetime \| None` | 必須 | 許可 | — |
| `allowed_actions` | `dict[str, Any]` | 任意 | 不可 | Field(default_factory=dict) |

**Response JSON構造例（schema由来の説明用）**

```json
{
  "graph_version_id": "{graph_version_id}",
  "project_id": "{project_id}",
  "source_result_id": "{source_result_id}",
  "parent_graph_version_id": "{parent_graph_version_id}",
  "name": "string",
  "graph_type": "string",
  "graph": {},
  "graph_origin": "string",
  "provenance": {},
  "designated_outcome_node": "string",
  "content_hash": "string",
  "edit_rationale": "string",
  "status": "string",
  "created_by": "string",
  "created_at": "2026-11-17T00:00:00Z",
  "allowed_actions": {}
}
```

#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗した場合 | 共通Handler |
| 400 / 409 | IDEMPOTENCY_KEY_REQUIRED / IDEMPOTENCY_CONFLICT | Key欠落／同一Key・異なる要求内容 | IdempotencyService |
| 404 | ENTITY_NOT_FOUND | 指定Resourceがない・別Projectである等、ServiceがEntityNotFoundを送出 | Handlerで確定、実到達は要確認 |
| 409 | PROJECT_ARCHIVED / RESOURCE_IMMUTABLE | ARCHIVEDまたはFIXEDに対する不適格変更の際、該当例外を送出した場合 | Handlerで確定、Operationごとの到達は要確認 |
| 422/409 | INVALID_GRAPH_SEMANTICS / GRAPH_FIXED_IMMUTABLE | Graph意味論違反、FIXED Graph変更 | 共通Handler;詳細到達は要検証 |

#### 根拠・未検証事項

- Router Source: `graph_versions.py`（blob `ad6ba942ee8ecc95590175ec3de655d3bee9a155`）。Request DTO: `GraphEditDraftCreate`、Response Model: `GraphVersionResponse`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.3 `GET /api/v1/projects/{project_id}/graph-versions`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-14-03` |
| Method / Path | `GET /api/v1/projects/{project_id}/graph-versions` |
| Handler | `graph_versions.py::list_graph_versions` |
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

- HTTP **200**。Body schema: `GraphVersionListResponse`。

| 項目（wire） | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `items` | `list[GraphVersionResponse]` | 必須 | 不可 | — |
| `next_cursor` | `str \| None` | 任意 | 許可 | None |

**Response JSON構造例（schema由来の説明用）**

```json
{
  "items": [],
  "next_cursor": "string"
}
```

#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗した場合 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 指定Resourceがない・別Projectである等、ServiceがEntityNotFoundを送出 | Handlerで確定、実到達は要確認 |
| 422/409 | INVALID_GRAPH_SEMANTICS / GRAPH_FIXED_IMMUTABLE | Graph意味論違反、FIXED Graph変更 | 共通Handler;詳細到達は要検証 |

#### 根拠・未検証事項

- Router Source: `graph_versions.py`（blob `ad6ba942ee8ecc95590175ec3de655d3bee9a155`）。Request DTO: `none`、Response Model: `GraphVersionListResponse`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.4 `GET /api/v1/graph-versions/{graph_version_id}`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-14-04` |
| Method / Path | `GET /api/v1/graph-versions/{graph_version_id}` |
| Handler | `graph_versions.py::get_graph_version` |
| Success Status | HTTP 200 |

#### Request

**Path parameters**

| 項目 | 型 | 必須 |
|---|---|---|
| `graph_version_id` | string | 必須 |

**Query parameters**

なし

**Headers**

Router固有の必須Header宣言なし

**Request Body / Field定義**

Request JSON Bodyなし（Router未定義）。

#### Response

- HTTP **200**。Body schema: `GraphVersionResponse`。

| 項目（wire） | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `graph_version_id` | `str` | 必須 | 不可 | — |
| `project_id` | `str` | 必須 | 不可 | — |
| `source_result_id` | `str \| None` | 必須 | 許可 | — |
| `parent_graph_version_id` | `str \| None` | 必須 | 許可 | — |
| `name` | `str` | 必須 | 不可 | — |
| `graph_type` | `str` | 必須 | 不可 | — |
| `graph` | `dict[str, Any]` | 必須 | 不可 | — |
| `graph_origin` | `str` | 必須 | 不可 | — |
| `provenance` | `dict[str, Any]` | 必須 | 不可 | — |
| `designated_outcome_node` | `str \| None` | 必須 | 許可 | — |
| `content_hash` | `str` | 必須 | 不可 | — |
| `edit_rationale` | `str \| None` | 必須 | 許可 | — |
| `status` | `str` | 必須 | 不可 | — |
| `created_by` | `str` | 必須 | 不可 | — |
| `created_at` | `datetime \| None` | 必須 | 許可 | — |
| `allowed_actions` | `dict[str, Any]` | 任意 | 不可 | Field(default_factory=dict) |

**Response JSON構造例（schema由来の説明用）**

```json
{
  "graph_version_id": "{graph_version_id}",
  "project_id": "{project_id}",
  "source_result_id": "{source_result_id}",
  "parent_graph_version_id": "{parent_graph_version_id}",
  "name": "string",
  "graph_type": "string",
  "graph": {},
  "graph_origin": "string",
  "provenance": {},
  "designated_outcome_node": "string",
  "content_hash": "string",
  "edit_rationale": "string",
  "status": "string",
  "created_by": "string",
  "created_at": "2026-11-17T00:00:00Z",
  "allowed_actions": {}
}
```

#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗した場合 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 指定Resourceがない・別Projectである等、ServiceがEntityNotFoundを送出 | Handlerで確定、実到達は要確認 |
| 422/409 | INVALID_GRAPH_SEMANTICS / GRAPH_FIXED_IMMUTABLE | Graph意味論違反、FIXED Graph変更 | 共通Handler;詳細到達は要検証 |

#### 根拠・未検証事項

- Router Source: `graph_versions.py`（blob `ad6ba942ee8ecc95590175ec3de655d3bee9a155`）。Request DTO: `none`、Response Model: `GraphVersionResponse`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.5 `GET /api/v1/projects/{project_id}/graph-versions/{graph_version_id}`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-14-05` |
| Method / Path | `GET /api/v1/projects/{project_id}/graph-versions/{graph_version_id}` |
| Handler | `graph_versions.py::get_project_graph_version` |
| Success Status | HTTP 200 |

#### Request

**Path parameters**

| 項目 | 型 | 必須 |
|---|---|---|
| `project_id` | string | 必須 |
| `graph_version_id` | string | 必須 |

**Query parameters**

なし

**Headers**

Router固有の必須Header宣言なし

**Request Body / Field定義**

Request JSON Bodyなし（Router未定義）。

#### Response

- HTTP **200**。Body schema: `GraphVersionResponse`。

| 項目（wire） | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `graph_version_id` | `str` | 必須 | 不可 | — |
| `project_id` | `str` | 必須 | 不可 | — |
| `source_result_id` | `str \| None` | 必須 | 許可 | — |
| `parent_graph_version_id` | `str \| None` | 必須 | 許可 | — |
| `name` | `str` | 必須 | 不可 | — |
| `graph_type` | `str` | 必須 | 不可 | — |
| `graph` | `dict[str, Any]` | 必須 | 不可 | — |
| `graph_origin` | `str` | 必須 | 不可 | — |
| `provenance` | `dict[str, Any]` | 必須 | 不可 | — |
| `designated_outcome_node` | `str \| None` | 必須 | 許可 | — |
| `content_hash` | `str` | 必須 | 不可 | — |
| `edit_rationale` | `str \| None` | 必須 | 許可 | — |
| `status` | `str` | 必須 | 不可 | — |
| `created_by` | `str` | 必須 | 不可 | — |
| `created_at` | `datetime \| None` | 必須 | 許可 | — |
| `allowed_actions` | `dict[str, Any]` | 任意 | 不可 | Field(default_factory=dict) |

**Response JSON構造例（schema由来の説明用）**

```json
{
  "graph_version_id": "{graph_version_id}",
  "project_id": "{project_id}",
  "source_result_id": "{source_result_id}",
  "parent_graph_version_id": "{parent_graph_version_id}",
  "name": "string",
  "graph_type": "string",
  "graph": {},
  "graph_origin": "string",
  "provenance": {},
  "designated_outcome_node": "string",
  "content_hash": "string",
  "edit_rationale": "string",
  "status": "string",
  "created_by": "string",
  "created_at": "2026-11-17T00:00:00Z",
  "allowed_actions": {}
}
```

#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗した場合 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 指定Resourceがない・別Projectである等、ServiceがEntityNotFoundを送出 | Handlerで確定、実到達は要確認 |
| 422/409 | INVALID_GRAPH_SEMANTICS / GRAPH_FIXED_IMMUTABLE | Graph意味論違反、FIXED Graph変更 | 共通Handler;詳細到達は要検証 |

#### 根拠・未検証事項

- Router Source: `graph_versions.py`（blob `ad6ba942ee8ecc95590175ec3de655d3bee9a155`）。Request DTO: `none`、Response Model: `GraphVersionResponse`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.6 `PATCH /api/v1/graph-versions/{graph_version_id}`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-14-06` |
| Method / Path | `PATCH /api/v1/graph-versions/{graph_version_id}` |
| Handler | `graph_versions.py::update_graph_version` |
| Success Status | HTTP 200 |

#### Request

**Path parameters**

| 項目 | 型 | 必須 |
|---|---|---|
| `graph_version_id` | string | 必須 |

**Query parameters**

なし

**Headers**

Router固有の必須Header宣言なし

**Request Body / Field定義**

Content-Type: `application/json`、型 `GraphVersionUpdate`

| 項目（wire） | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `graph` | `dict[str, Any]` | 必須 | 不可 | — |
| `edit_rationale` | `str \| None` | 任意 | 許可 | None |
| `designated_outcome_node` | `str \| None` | 任意 | 許可 | lt=None, min_length=1, max_length=200 |
| `expected_content_hash` | `str \| None` | 任意 | 許可 | None |

**Request JSON例（schema由来の説明用）**

```json
{
  "graph": {}
}
```

#### Response

- HTTP **200**。Body schema: `GraphVersionResponse`。

| 項目（wire） | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `graph_version_id` | `str` | 必須 | 不可 | — |
| `project_id` | `str` | 必須 | 不可 | — |
| `source_result_id` | `str \| None` | 必須 | 許可 | — |
| `parent_graph_version_id` | `str \| None` | 必須 | 許可 | — |
| `name` | `str` | 必須 | 不可 | — |
| `graph_type` | `str` | 必須 | 不可 | — |
| `graph` | `dict[str, Any]` | 必須 | 不可 | — |
| `graph_origin` | `str` | 必須 | 不可 | — |
| `provenance` | `dict[str, Any]` | 必須 | 不可 | — |
| `designated_outcome_node` | `str \| None` | 必須 | 許可 | — |
| `content_hash` | `str` | 必須 | 不可 | — |
| `edit_rationale` | `str \| None` | 必須 | 許可 | — |
| `status` | `str` | 必須 | 不可 | — |
| `created_by` | `str` | 必須 | 不可 | — |
| `created_at` | `datetime \| None` | 必須 | 許可 | — |
| `allowed_actions` | `dict[str, Any]` | 任意 | 不可 | Field(default_factory=dict) |

**Response JSON構造例（schema由来の説明用）**

```json
{
  "graph_version_id": "{graph_version_id}",
  "project_id": "{project_id}",
  "source_result_id": "{source_result_id}",
  "parent_graph_version_id": "{parent_graph_version_id}",
  "name": "string",
  "graph_type": "string",
  "graph": {},
  "graph_origin": "string",
  "provenance": {},
  "designated_outcome_node": "string",
  "content_hash": "string",
  "edit_rationale": "string",
  "status": "string",
  "created_by": "string",
  "created_at": "2026-11-17T00:00:00Z",
  "allowed_actions": {}
}
```

#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗した場合 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 指定Resourceがない・別Projectである等、ServiceがEntityNotFoundを送出 | Handlerで確定、実到達は要確認 |
| 422/409 | INVALID_GRAPH_SEMANTICS / GRAPH_FIXED_IMMUTABLE | Graph意味論違反、FIXED Graph変更 | 共通Handler;詳細到達は要検証 |

#### 根拠・未検証事項

- Router Source: `graph_versions.py`（blob `ad6ba942ee8ecc95590175ec3de655d3bee9a155`）。Request DTO: `GraphVersionUpdate`、Response Model: `GraphVersionResponse`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.7 `PATCH /api/v1/projects/{project_id}/graph-versions/{graph_version_id}`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-14-07` |
| Method / Path | `PATCH /api/v1/projects/{project_id}/graph-versions/{graph_version_id}` |
| Handler | `graph_versions.py::update_project_graph_version` |
| Success Status | HTTP 200 |

#### Request

**Path parameters**

| 項目 | 型 | 必須 |
|---|---|---|
| `project_id` | string | 必須 |
| `graph_version_id` | string | 必須 |

**Query parameters**

なし

**Headers**

Router固有の必須Header宣言なし

**Request Body / Field定義**

Content-Type: `application/json`、型 `GraphVersionUpdate`

| 項目（wire） | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `graph` | `dict[str, Any]` | 必須 | 不可 | — |
| `edit_rationale` | `str \| None` | 任意 | 許可 | None |
| `designated_outcome_node` | `str \| None` | 任意 | 許可 | lt=None, min_length=1, max_length=200 |
| `expected_content_hash` | `str \| None` | 任意 | 許可 | None |

**Request JSON例（schema由来の説明用）**

```json
{
  "graph": {}
}
```

#### Response

- HTTP **200**。Body schema: `GraphVersionResponse`。

| 項目（wire） | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `graph_version_id` | `str` | 必須 | 不可 | — |
| `project_id` | `str` | 必須 | 不可 | — |
| `source_result_id` | `str \| None` | 必須 | 許可 | — |
| `parent_graph_version_id` | `str \| None` | 必須 | 許可 | — |
| `name` | `str` | 必須 | 不可 | — |
| `graph_type` | `str` | 必須 | 不可 | — |
| `graph` | `dict[str, Any]` | 必須 | 不可 | — |
| `graph_origin` | `str` | 必須 | 不可 | — |
| `provenance` | `dict[str, Any]` | 必須 | 不可 | — |
| `designated_outcome_node` | `str \| None` | 必須 | 許可 | — |
| `content_hash` | `str` | 必須 | 不可 | — |
| `edit_rationale` | `str \| None` | 必須 | 許可 | — |
| `status` | `str` | 必須 | 不可 | — |
| `created_by` | `str` | 必須 | 不可 | — |
| `created_at` | `datetime \| None` | 必須 | 許可 | — |
| `allowed_actions` | `dict[str, Any]` | 任意 | 不可 | Field(default_factory=dict) |

**Response JSON構造例（schema由来の説明用）**

```json
{
  "graph_version_id": "{graph_version_id}",
  "project_id": "{project_id}",
  "source_result_id": "{source_result_id}",
  "parent_graph_version_id": "{parent_graph_version_id}",
  "name": "string",
  "graph_type": "string",
  "graph": {},
  "graph_origin": "string",
  "provenance": {},
  "designated_outcome_node": "string",
  "content_hash": "string",
  "edit_rationale": "string",
  "status": "string",
  "created_by": "string",
  "created_at": "2026-11-17T00:00:00Z",
  "allowed_actions": {}
}
```

#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗した場合 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 指定Resourceがない・別Projectである等、ServiceがEntityNotFoundを送出 | Handlerで確定、実到達は要確認 |
| 409 | PROJECT_ARCHIVED / RESOURCE_IMMUTABLE | ARCHIVEDまたはFIXEDに対する不適格変更の際、該当例外を送出した場合 | Handlerで確定、Operationごとの到達は要確認 |
| 422/409 | INVALID_GRAPH_SEMANTICS / GRAPH_FIXED_IMMUTABLE | Graph意味論違反、FIXED Graph変更 | 共通Handler;詳細到達は要検証 |

#### 根拠・未検証事項

- Router Source: `graph_versions.py`（blob `ad6ba942ee8ecc95590175ec3de655d3bee9a155`）。Request DTO: `GraphVersionUpdate`、Response Model: `GraphVersionResponse`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.8 `POST /api/v1/graph-versions/{graph_version_id}/fix`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-14-08` |
| Method / Path | `POST /api/v1/graph-versions/{graph_version_id}/fix` |
| Handler | `graph_versions.py::fix_graph_version` |
| Success Status | HTTP 200 |

#### Request

**Path parameters**

| 項目 | 型 | 必須 |
|---|---|---|
| `graph_version_id` | string | 必須 |

**Query parameters**

なし

**Headers**

Router固有の必須Header宣言なし

**Request Body / Field定義**

Request JSON Bodyなし（Router未定義）。

#### Response

- HTTP **200**。Body schema: `GraphVersionResponse`。

| 項目（wire） | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `graph_version_id` | `str` | 必須 | 不可 | — |
| `project_id` | `str` | 必須 | 不可 | — |
| `source_result_id` | `str \| None` | 必須 | 許可 | — |
| `parent_graph_version_id` | `str \| None` | 必須 | 許可 | — |
| `name` | `str` | 必須 | 不可 | — |
| `graph_type` | `str` | 必須 | 不可 | — |
| `graph` | `dict[str, Any]` | 必須 | 不可 | — |
| `graph_origin` | `str` | 必須 | 不可 | — |
| `provenance` | `dict[str, Any]` | 必須 | 不可 | — |
| `designated_outcome_node` | `str \| None` | 必須 | 許可 | — |
| `content_hash` | `str` | 必須 | 不可 | — |
| `edit_rationale` | `str \| None` | 必須 | 許可 | — |
| `status` | `str` | 必須 | 不可 | — |
| `created_by` | `str` | 必須 | 不可 | — |
| `created_at` | `datetime \| None` | 必須 | 許可 | — |
| `allowed_actions` | `dict[str, Any]` | 任意 | 不可 | Field(default_factory=dict) |

**Response JSON構造例（schema由来の説明用）**

```json
{
  "graph_version_id": "{graph_version_id}",
  "project_id": "{project_id}",
  "source_result_id": "{source_result_id}",
  "parent_graph_version_id": "{parent_graph_version_id}",
  "name": "string",
  "graph_type": "string",
  "graph": {},
  "graph_origin": "string",
  "provenance": {},
  "designated_outcome_node": "string",
  "content_hash": "string",
  "edit_rationale": "string",
  "status": "string",
  "created_by": "string",
  "created_at": "2026-11-17T00:00:00Z",
  "allowed_actions": {}
}
```

#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗した場合 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 指定Resourceがない・別Projectである等、ServiceがEntityNotFoundを送出 | Handlerで確定、実到達は要確認 |
| 422/409 | INVALID_GRAPH_SEMANTICS / GRAPH_FIXED_IMMUTABLE | Graph意味論違反、FIXED Graph変更 | 共通Handler;詳細到達は要検証 |

#### 根拠・未検証事項

- Router Source: `graph_versions.py`（blob `ad6ba942ee8ecc95590175ec3de655d3bee9a155`）。Request DTO: `none`、Response Model: `GraphVersionResponse`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.9 `POST /api/v1/projects/{project_id}/graph-versions/{graph_version_id}/fix`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-14-09` |
| Method / Path | `POST /api/v1/projects/{project_id}/graph-versions/{graph_version_id}/fix` |
| Handler | `graph_versions.py::fix_project_graph_version` |
| Success Status | HTTP 200 |

#### Request

**Path parameters**

| 項目 | 型 | 必須 |
|---|---|---|
| `project_id` | string | 必須 |
| `graph_version_id` | string | 必須 |

**Query parameters**

なし

**Headers**

Router固有の必須Header宣言なし

**Request Body / Field定義**

Request JSON Bodyなし（Router未定義）。

#### Response

- HTTP **200**。Body schema: `GraphVersionResponse`。

| 項目（wire） | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `graph_version_id` | `str` | 必須 | 不可 | — |
| `project_id` | `str` | 必須 | 不可 | — |
| `source_result_id` | `str \| None` | 必須 | 許可 | — |
| `parent_graph_version_id` | `str \| None` | 必須 | 許可 | — |
| `name` | `str` | 必須 | 不可 | — |
| `graph_type` | `str` | 必須 | 不可 | — |
| `graph` | `dict[str, Any]` | 必須 | 不可 | — |
| `graph_origin` | `str` | 必須 | 不可 | — |
| `provenance` | `dict[str, Any]` | 必須 | 不可 | — |
| `designated_outcome_node` | `str \| None` | 必須 | 許可 | — |
| `content_hash` | `str` | 必須 | 不可 | — |
| `edit_rationale` | `str \| None` | 必須 | 許可 | — |
| `status` | `str` | 必須 | 不可 | — |
| `created_by` | `str` | 必須 | 不可 | — |
| `created_at` | `datetime \| None` | 必須 | 許可 | — |
| `allowed_actions` | `dict[str, Any]` | 任意 | 不可 | Field(default_factory=dict) |

**Response JSON構造例（schema由来の説明用）**

```json
{
  "graph_version_id": "{graph_version_id}",
  "project_id": "{project_id}",
  "source_result_id": "{source_result_id}",
  "parent_graph_version_id": "{parent_graph_version_id}",
  "name": "string",
  "graph_type": "string",
  "graph": {},
  "graph_origin": "string",
  "provenance": {},
  "designated_outcome_node": "string",
  "content_hash": "string",
  "edit_rationale": "string",
  "status": "string",
  "created_by": "string",
  "created_at": "2026-11-17T00:00:00Z",
  "allowed_actions": {}
}
```

#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗した場合 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 指定Resourceがない・別Projectである等、ServiceがEntityNotFoundを送出 | Handlerで確定、実到達は要確認 |
| 409 | PROJECT_ARCHIVED / RESOURCE_IMMUTABLE | ARCHIVEDまたはFIXEDに対する不適格変更の際、該当例外を送出した場合 | Handlerで確定、Operationごとの到達は要確認 |
| 422/409 | INVALID_GRAPH_SEMANTICS / GRAPH_FIXED_IMMUTABLE | Graph意味論違反、FIXED Graph変更 | 共通Handler;詳細到達は要検証 |

#### 根拠・未検証事項

- Router Source: `graph_versions.py`（blob `ad6ba942ee8ecc95590175ec3de655d3bee9a155`）。Request DTO: `none`、Response Model: `GraphVersionResponse`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.10 `GET /api/v1/projects/{project_id}/graph-candidates`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-14-10` |
| Method / Path | `GET /api/v1/projects/{project_id}/graph-candidates` |
| Handler | `results.py::list_graph_candidates` |
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

- HTTP **200**。Body schema: `GraphCandidateListResponse`。

| 項目（wire） | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `items` | `list[GraphCandidateResponse]` | 必須 | 不可 | — |
| `next_cursor` | `str \| None` | 任意 | 許可 | None |

**Response JSON構造例（schema由来の説明用）**

```json
{
  "items": [],
  "next_cursor": "string"
}
```

#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗した場合 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 指定Resourceがない・別Projectである等、ServiceがEntityNotFoundを送出 | Handlerで確定、実到達は要確認 |

#### 根拠・未検証事項

- Router Source: `results.py`（blob `e565edb21051133b84fb77fd7c1eafcd2d7257ea`）。Request DTO: `none`、Response Model: `GraphCandidateListResponse`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.11 `GET /api/v1/projects/{project_id}/graph-candidates/{candidate_kind}/{candidate_id}`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-14-11` |
| Method / Path | `GET /api/v1/projects/{project_id}/graph-candidates/{candidate_kind}/{candidate_id}` |
| Handler | `results.py::get_graph_candidate` |
| Success Status | HTTP 200 |

#### Request

**Path parameters**

| 項目 | 型 | 必須 |
|---|---|---|
| `project_id` | string | 必須 |
| `candidate_kind` | string | 必須 |
| `candidate_id` | string | 必須 |

**Query parameters**

なし

**Headers**

Router固有の必須Header宣言なし

**Request Body / Field定義**

Request JSON Bodyなし（Router未定義）。

#### Response

- HTTP **200**。Body schema: `GraphCandidateResponse`。

| 項目（wire） | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `candidate_kind` | `str` | 必須 | 不可 | — |
| `candidate_id` | `str` | 必須 | 不可 | — |
| `source_result_id` | `str \| None` | 必須 | 許可 | — |
| `graph_version_id` | `str \| None` | 必須 | 許可 | — |
| `parent_graph_version_id` | `str \| None` | 必須 | 許可 | — |
| `graph_type` | `str` | 必須 | 不可 | — |
| `graph_origin` | `str` | 必須 | 不可 | — |
| `version_status` | `str \| None` | 必須 | 許可 | — |
| `scientific_status` | `str \| None` | 必須 | 許可 | — |
| `fixed` | `bool` | 必須 | 不可 | — |
| `designated_outcome_node` | `str \| None` | 必須 | 許可 | — |
| `summary` | `dict[str, Any]` | 必須 | 不可 | — |
| `warnings` | `list[Any]` | 必須 | 不可 | — |
| `allowed_actions` | `dict[str, Any]` | 必須 | 不可 | — |
| `graph` | `dict[str, Any] \| None` | 任意 | 許可 | None |

**Response JSON構造例（schema由来の説明用）**

```json
{
  "candidate_kind": "string",
  "candidate_id": "{candidate_id}",
  "source_result_id": "{source_result_id}",
  "graph_version_id": "{graph_version_id}",
  "parent_graph_version_id": "{parent_graph_version_id}",
  "graph_type": "string",
  "graph_origin": "string",
  "version_status": "string",
  "scientific_status": "string",
  "fixed": false,
  "designated_outcome_node": "string",
  "summary": {},
  "warnings": [],
  "allowed_actions": {},
  "graph": {}
}
```

#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗した場合 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 指定Resourceがない・別Projectである等、ServiceがEntityNotFoundを送出 | Handlerで確定、実到達は要確認 |

#### 根拠・未検証事項

- Router Source: `results.py`（blob `e565edb21051133b84fb77fd7c1eafcd2d7257ea`）。Request DTO: `none`、Response Model: `GraphCandidateResponse`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.12 `POST /api/v1/projects/{project_id}/graph-candidate-comparisons/query`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-14-12` |
| Method / Path | `POST /api/v1/projects/{project_id}/graph-candidate-comparisons/query` |
| Handler | `results.py::compare_graph_candidates` |
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

Content-Type: `application/json`、型 `GraphCandidateComparisonRequest`

| 項目（wire） | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `candidate_refs` | `list[CandidateRef]` | 必須 | 不可 | min_length=2, max_length=20 |

**Request JSON例（schema由来の説明用）**

```json
{
  "candidate_refs": []
}
```

#### Response

- HTTP **200**。Body schema: `GraphCandidateComparisonResponse`。

| 項目（wire） | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `candidates` | `list[GraphCandidateResponse]` | 必須 | 不可 | — |
| `compatibility` | `dict[str, Any]` | 必須 | 不可 | — |
| `differences` | `list[dict[str, Any]]` | 必須 | 不可 | — |
| `warnings` | `list[str]` | 必須 | 不可 | — |

**Response JSON構造例（schema由来の説明用）**

```json
{
  "candidates": [],
  "compatibility": {},
  "differences": [],
  "warnings": []
}
```

#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗した場合 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 指定Resourceがない・別Projectである等、ServiceがEntityNotFoundを送出 | Handlerで確定、実到達は要確認 |
| 409 | PROJECT_ARCHIVED / RESOURCE_IMMUTABLE | ARCHIVEDまたはFIXEDに対する不適格変更の際、該当例外を送出した場合 | Handlerで確定、Operationごとの到達は要確認 |

#### 根拠・未検証事項

- Router Source: `results.py`（blob `e565edb21051133b84fb77fd7c1eafcd2d7257ea`）。Request DTO: `GraphCandidateComparisonRequest`、Response Model: `GraphCandidateComparisonResponse`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

## 5. 検証状況

- Route/Method/Path: 12 件 Source確認。
- Request: Router/Pydanticモデルの静的制約を反映。Response: 型付きモデルは全Fieldを表記。Service無型応答は一部未確定。
- HTTP Contract Test: NOT_RUN。Endpoint詳細の完全性・認可・実行時エラー網羅は未検証。
- 元の`docs/wiki/requirement_definition/`への昇格: NOT_DONE。

## 6. 既存Domain・設計制約（旧仕様本文から保持）

以下は既存のDomain規範・補足情報を保持したもの。重複する旧Route一覧より§2（Source基準）を優先する。改訂前の原本文はGit Blob `f9d66bdd6cd82d09fb8fad4b75f77ccb5a918c5a`で追跡可能。

### Causal Interface

#### Graph

Causal analysisはGraph Version / candidate graphを扱う。現行実装のpublic interfaceは次である。

| Method | Path | 用途 |
| --- | --- | --- |
| POST | `/projects/{project_id}/graph-versions` | Graph Version作成。`Idempotency-Key`対応 |
| POST | `/projects/{project_id}/graph-edit-drafts` | candidateを基に編集DRAFT作成。`Idempotency-Key`対応 |
| GET | `/projects/{project_id}/graph-versions` | Project内Graph Version一覧 |
| GET | `/graph-versions/{graph_version_id}` | Graph Version取得 |
| GET | `/projects/{project_id}/graph-versions/{graph_version_id}` | Project境界を検証して取得 |
| PATCH | `/graph-versions/{graph_version_id}` | DRAFT更新 |
| PATCH | `/projects/{project_id}/graph-versions/{graph_version_id}` | Project-scoped DRAFT更新 |
| POST | `/graph-versions/{graph_version_id}/fix` | FIXED化 |
| POST | `/projects/{project_id}/graph-versions/{graph_version_id}/fix` | Project-scoped FIXED化 |
| GET | `/projects/{project_id}/graph-candidates` | Discovery ResultとGraph Versionのcandidate一覧 |
| GET | `/projects/{project_id}/graph-candidates/{candidate_kind}/{candidate_id}` | candidate取得 |
| POST | `/projects/{project_id}/graph-candidate-comparisons/query` | Graph candidate比較 |

Graph Version responseは少なくとも`graph_version_id / project_id / source_result_id / parent_graph_version_id / name / graph_type / graph_origin / provenance / designated_outcome_node / graph / content_hash / edit_rationale / status / created_by / created_at / allowed_actions`を返す。Navigation Stage IDをGraph Version identityへ追加しない。

#### Causal operation

Runtime causal operation discriminatorは次である。

- `DISCOVERY`
- `IDENTIFICATION`
- `ESTIMATION`
- `REFUTATION`
- `SENSITIVITY`

現行実装の`CausalPlanner`はcanonical `Execution.operation`から**1 runtime Stageだけを持つcompatibility plan**を生成する。

| ExecutionOperation | StageType |
| --- | --- |
| `DISCOVERY` | `causal.discovery.v1` |
| `IDENTIFICATION` | `causal.identification.v1` |
| `ESTIMATION` | `causal.estimation.v2` |
| `REFUTATION` | `causal.refutation.v1` |
| `SENSITIVITY` | `causal.sensitivity.v1` |

したがって、`Identification / Estimation / Effects / Diagnostics`等のNavigation Stageを理由にCausal API/runtimeを単一Plan内の多段Stageへ作り替えない。科学的な前提関係はcanonical Executionの`input_graph_version_id / input_result_id`とResult/Lineageで扱う。

**当該Interfaceの追加契約（関連Requirement）**

- **`FR-051`**：同一immutable `dataset_version_id`の先行Exploratory Resultを用いたconfirmatory分析では`EXPLORATORY_REUSE_SAME_DATA` warningとevidence Result IDを保持する
- **`AR-004`**：同一immutable `dataset_version_id`を探索とconfirmatory analysisで再利用した場合、`EXPLORATORY_REUSE_SAME_DATA` warningとlineage evidenceを保持する

## 7. 改訂記録

- 2026-11-17: 全23_10〜23_19共通フォーマットへ再構成。Request/Response/ErrorsをOperation別に記載し、Source確認と未検証を分離。
