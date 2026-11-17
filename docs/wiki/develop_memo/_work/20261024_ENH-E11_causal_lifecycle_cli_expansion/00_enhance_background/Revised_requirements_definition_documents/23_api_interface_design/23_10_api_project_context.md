# 23_10_api_project_context — Project / Research Context Web API仕様

## 1. API概要

- 対象: Project / Research Context のHTTP契約。
- Base path: `/api/v1`。
- 本改訂はOwner採用の**Operation単位Request/Response/Errors定義**を対象とする。実行時PASSや要件変更を含まない。
- Source snapshot: `89d4f135d8c680805731934e715b079ea0f72f2b`。Currentに対する未検証事項を明示する。

## 2. エンドポイント一覧

| No. | HTTP | Path | Handler | HTTP Success |
|---:|---|---|---|---|
| 1 | `POST` | `/api/v1/projects` | `create_project` | `201` |
| 2 | `GET` | `/api/v1/projects` | `list_projects` | `200` |
| 3 | `GET` | `/api/v1/projects/{project_id}` | `get_project` | `200` |
| 4 | `PATCH` | `/api/v1/projects/{project_id}` | `update_project` | `200` |
| 5 | `DELETE` | `/api/v1/projects/{project_id}` | `archive_project` | `204` |
| 6 | `POST` | `/api/v1/projects/{project_id}/research-contexts` | `create_research_context` | `201` |
| 7 | `GET` | `/api/v1/projects/{project_id}/research-contexts` | `list_research_contexts` | `200` |
| 8 | `GET` | `/api/v1/projects/{project_id}/research-contexts/{context_id}` | `get_research_context` | `200` |
| 9 | `PATCH` | `/api/v1/projects/{project_id}/research-contexts/{context_id}` | `patch_research_context` | `200` |
| 10 | `POST` | `/api/v1/projects/{project_id}/research-contexts/{context_id}/fix` | `fix_research_context` | `200` |
| 11 | `GET` | `/api/v1/projects/{project_id}/research-contexts/{context_id}/usage` | `research_context_usage` | `200` |

## 3. 共通Error Response形式

CURRENTのDomainError/RequestValidationError Handlerは`application/problem+json`ではなく、以下のJSON envelope。

```json
{"error":{"code":"INVALID_REQUEST","message":"Request validation failed.","details":{},"request_id":"{request_id}"}}
```

共通Handlerに定義されたErrorがすべてのOperationから発生するとは限らない。下表の条件付きErrorはテストPASS済みという意味ではない。

## 4. エンドポイント詳細

### 4.1 `POST /api/v1/projects`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-10-01` |
| Method / Path | `POST /api/v1/projects` |
| Handler | `projects.py::create_project` |
| Success Status | HTTP 201 |

#### Request

**Path parameters**

なし

**Query parameters**

なし

**Headers**

| Header | 仕様 |
|---|---|
| `X-User-Id` | Routerから参照。認証方式の確証ではない |

**Request Body / Field定義**

Content-Type: `application/json`、型 `ProjectCreate`

| 項目 | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `name` | `str` | 必須 | 不可 | min_length=1, max_length=200 |
| `topic` | `str \| None` | 任意 | 許可 | lt=None, max_length=4000 |
| `objective` | `str \| None` | 任意 | 許可 | lt=None, max_length=4000 |
| `memo` | `str \| None` | 任意 | 許可 | lt=None, max_length=8000 |

**Request JSON例（説明用）**

```json
{
  "name": "string"
}
```

#### Response

- HTTP **201**。Body schema: `ProjectResponse`。

| 項目 | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `project_id` | `str` | 必須 | 不可 | — |
| `name` | `str` | 必須 | 不可 | — |
| `topic` | `str \| None` | 必須 | 許可 | — |
| `objective` | `str \| None` | 必須 | 許可 | — |
| `memo` | `str \| None` | 必須 | 許可 | — |
| `status` | `str` | 必須 | 不可 | — |
| `created_at` | `datetime \| None` | 必須 | 許可 | — |
| `updated_at` | `datetime \| None` | 必須 | 許可 | — |

**Response JSON構造例（説明用）**

```json
{
  "project_id": "{project_id}",
  "name": "string",
  "topic": "string",
  "objective": "string",
  "memo": "string",
  "status": "string",
  "created_at": "2026-11-17T00:00:00Z",
  "updated_at": "2026-11-17T00:00:00Z"
}
```

#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗した場合 | 共通Handler |
| 409 | PROJECT_ARCHIVED / RESOURCE_IMMUTABLE | ARCHIVEDまたはFIXEDに対する不適格変更の際、該当例外を送出した場合 | Handlerで確定、Operationごとの到達は要確認 |

#### 根拠・未検証事項

- Router Source: `projects.py`（blob `6fc9aa297aba3f89d57613a1b1c203f4de071a8c`）。Request DTO: `ProjectCreate`、Response Model: `ProjectResponse`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.2 `GET /api/v1/projects`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-10-02` |
| Method / Path | `GET /api/v1/projects` |
| Handler | `projects.py::list_projects` |
| Success Status | HTTP 200 |

#### Request

**Path parameters**

なし

**Query parameters**

| 項目 | 型 | default |
|---|---|---|
| `status` | `ProjectStatus \| None` | `ProjectStatus.ACTIVE` |

**Headers**

Router固有の必須Header宣言なし

**Request Body / Field定義**

Request JSON Bodyなし（Router未定義）。

#### Response

- HTTP **200**。Body schema: `ProjectListResponse`。

| 項目 | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `items` | `list[ProjectResponse]` | 必須 | 不可 | — |
| `next_cursor` | `str \| None` | 任意 | 許可 | None |

**Response JSON構造例（説明用）**

```json
{
  "items": []
}
```

#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| — | 未確定 | Handlerで当該Operationに固有のError code未確認 | 追加Source照合要 |

#### 根拠・未検証事項

- Router Source: `projects.py`（blob `6fc9aa297aba3f89d57613a1b1c203f4de071a8c`）。Request DTO: `none`、Response Model: `ProjectListResponse`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.3 `GET /api/v1/projects/{project_id}`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-10-03` |
| Method / Path | `GET /api/v1/projects/{project_id}` |
| Handler | `projects.py::get_project` |
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

- HTTP **200**。Body schema: `ProjectResponse`。

| 項目 | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `project_id` | `str` | 必須 | 不可 | — |
| `name` | `str` | 必須 | 不可 | — |
| `topic` | `str \| None` | 必須 | 許可 | — |
| `objective` | `str \| None` | 必須 | 許可 | — |
| `memo` | `str \| None` | 必須 | 許可 | — |
| `status` | `str` | 必須 | 不可 | — |
| `created_at` | `datetime \| None` | 必須 | 許可 | — |
| `updated_at` | `datetime \| None` | 必須 | 許可 | — |

**Response JSON構造例（説明用）**

```json
{
  "project_id": "{project_id}",
  "name": "string",
  "topic": "string",
  "objective": "string",
  "memo": "string",
  "status": "string",
  "created_at": "2026-11-17T00:00:00Z",
  "updated_at": "2026-11-17T00:00:00Z"
}
```

#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗した場合 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 指定Resourceがない・別Projectである等、ServiceがEntityNotFoundを送出 | Handlerで確定、実到達は要確認 |

#### 根拠・未検証事項

- Router Source: `projects.py`（blob `6fc9aa297aba3f89d57613a1b1c203f4de071a8c`）。Request DTO: `none`、Response Model: `ProjectResponse`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.4 `PATCH /api/v1/projects/{project_id}`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-10-04` |
| Method / Path | `PATCH /api/v1/projects/{project_id}` |
| Handler | `projects.py::update_project` |
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

Content-Type: `application/json`、型 `ProjectUpdate`

| 項目 | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `name` | `str \| None` | 任意 | 許可 | lt=None, min_length=1, max_length=200 |
| `topic` | `str \| None` | 任意 | 許可 | lt=None, max_length=4000 |
| `objective` | `str \| None` | 任意 | 許可 | lt=None, max_length=4000 |
| `memo` | `str \| None` | 任意 | 許可 | lt=None, max_length=8000 |

**Request JSON例（説明用）**

```json
{}
```

#### Response

- HTTP **200**。Body schema: `ProjectResponse`。

| 項目 | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `project_id` | `str` | 必須 | 不可 | — |
| `name` | `str` | 必須 | 不可 | — |
| `topic` | `str \| None` | 必須 | 許可 | — |
| `objective` | `str \| None` | 必須 | 許可 | — |
| `memo` | `str \| None` | 必須 | 許可 | — |
| `status` | `str` | 必須 | 不可 | — |
| `created_at` | `datetime \| None` | 必須 | 許可 | — |
| `updated_at` | `datetime \| None` | 必須 | 許可 | — |

**Response JSON構造例（説明用）**

```json
{
  "project_id": "{project_id}",
  "name": "string",
  "topic": "string",
  "objective": "string",
  "memo": "string",
  "status": "string",
  "created_at": "2026-11-17T00:00:00Z",
  "updated_at": "2026-11-17T00:00:00Z"
}
```

#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗した場合 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 指定Resourceがない・別Projectである等、ServiceがEntityNotFoundを送出 | Handlerで確定、実到達は要確認 |
| 409 | PROJECT_ARCHIVED / RESOURCE_IMMUTABLE | ARCHIVEDまたはFIXEDに対する不適格変更の際、該当例外を送出した場合 | Handlerで確定、Operationごとの到達は要確認 |

#### 根拠・未検証事項

- Router Source: `projects.py`（blob `6fc9aa297aba3f89d57613a1b1c203f4de071a8c`）。Request DTO: `ProjectUpdate`、Response Model: `ProjectResponse`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.5 `DELETE /api/v1/projects/{project_id}`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-10-05` |
| Method / Path | `DELETE /api/v1/projects/{project_id}` |
| Handler | `projects.py::archive_project` |
| Success Status | HTTP 204 |

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

Request JSON Bodyなし（Router未定義）。

#### Response

- HTTP **204**。Body schema: なし（204 No Content）。

Response bodyなし。


#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗した場合 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 指定Resourceがない・別Projectである等、ServiceがEntityNotFoundを送出 | Handlerで確定、実到達は要確認 |
| 409 | PROJECT_ARCHIVED / RESOURCE_IMMUTABLE | ARCHIVEDまたはFIXEDに対する不適格変更の際、該当例外を送出した場合 | Handlerで確定、Operationごとの到達は要確認 |

#### 根拠・未検証事項

- Router Source: `projects.py`（blob `6fc9aa297aba3f89d57613a1b1c203f4de071a8c`）。Request DTO: `none`、Response Model: `未宣言`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.6 `POST /api/v1/projects/{project_id}/research-contexts`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-10-06` |
| Method / Path | `POST /api/v1/projects/{project_id}/research-contexts` |
| Handler | `workspace_lifecycle.py::create_research_context` |
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

Content-Type: `application/json`、型 `ResearchContextCreate`

| 項目 | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `context_key` | `str` | 必須 | 不可 | — |
| `problem_statement` | `str` | 任意 | 不可 | "" |
| `research_questions` | `list[str]` | 任意 | 不可 | Field(default_factory=list) |
| `significance` | `str \| None` | 任意 | 許可 | None |
| `hypotheses` | `list[str]` | 任意 | 不可 | Field(default_factory=list) |
| `decision_context` | `dict[str, Any]` | 任意 | 不可 | Field(default_factory=dict) |
| `relations` | `list[dict[str, str]]` | 任意 | 不可 | Field(default_factory=list) |

**Request JSON例（説明用）**

```json
{
  "context_key": "string"
}
```

#### Response

- HTTP **201**。Body schema: Service output（未型付け）。

**Routerにresponse_model未宣言。** Service返却項目は別途照合が必要。Type/keysが公開契約として確定したとはみなさない。


#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗した場合 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 指定Resourceがない・別Projectである等、ServiceがEntityNotFoundを送出 | Handlerで確定、実到達は要確認 |
| 409 | PROJECT_ARCHIVED / RESOURCE_IMMUTABLE | ARCHIVEDまたはFIXEDに対する不適格変更の際、該当例外を送出した場合 | Handlerで確定、Operationごとの到達は要確認 |
| 422 | INVALID_SCHEMA | Study/Family/Referencesの整合性、FIXED Context/Analysis View要件、revision前提等でServiceのInvalidSchemaが発生 | Service/Domainで具体化 |

#### 根拠・未検証事項

- Router Source: `workspace_lifecycle.py`（blob `eb90bd940fc7a35b84cda0e3fa58235a738cb0a1`）。Request DTO: `ResearchContextCreate`、Response Model: `未宣言`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.7 `GET /api/v1/projects/{project_id}/research-contexts`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-10-07` |
| Method / Path | `GET /api/v1/projects/{project_id}/research-contexts` |
| Handler | `workspace_lifecycle.py::list_research_contexts` |
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

- HTTP **200**。Body schema: JSON object。

| 項目 | 型 |
|---|---|
| `items` | array[Service resource] |

要素FieldはService由来。Routerにresponse_model未宣言。

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

### 4.8 `GET /api/v1/projects/{project_id}/research-contexts/{context_id}`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-10-08` |
| Method / Path | `GET /api/v1/projects/{project_id}/research-contexts/{context_id}` |
| Handler | `workspace_lifecycle.py::get_research_context` |
| Success Status | HTTP 200 |

#### Request

**Path parameters**

| 項目 | 型 | 必須 |
|---|---|---|
| `project_id` | string | 必須 |
| `context_id` | string | 必須 |

**Query parameters**

なし

**Headers**

Router固有の必須Header宣言なし

**Request Body / Field定義**

Request JSON Bodyなし（Router未定義）。

#### Response

- HTTP **200**。Body schema: Service output（未型付け）。

**Routerにresponse_model未宣言。** Service返却項目は別途照合が必要。Type/keysが公開契約として確定したとはみなさない。


#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗した場合 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 指定Resourceがない・別Projectである等、ServiceがEntityNotFoundを送出 | Handlerで確定、実到達は要確認 |
| 422 | INVALID_SCHEMA | Study/Family/Referencesの整合性、FIXED Context/Analysis View要件、revision前提等でServiceのInvalidSchemaが発生 | Service/Domainで具体化 |

#### 根拠・未検証事項

- Router Source: `workspace_lifecycle.py`（blob `eb90bd940fc7a35b84cda0e3fa58235a738cb0a1`）。Request DTO: `none`、Response Model: `未宣言`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.9 `PATCH /api/v1/projects/{project_id}/research-contexts/{context_id}`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-10-09` |
| Method / Path | `PATCH /api/v1/projects/{project_id}/research-contexts/{context_id}` |
| Handler | `workspace_lifecycle.py::patch_research_context` |
| Success Status | HTTP 200 |

#### Request

**Path parameters**

| 項目 | 型 | 必須 |
|---|---|---|
| `project_id` | string | 必須 |
| `context_id` | string | 必須 |

**Query parameters**

なし

**Headers**

Router固有の必須Header宣言なし

**Request Body / Field定義**

Content-Type: `application/json`、型 `ResearchContextPatch`

| 項目 | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `problem_statement` | `str \| None` | 任意 | 許可 | None |
| `research_questions` | `list[str] \| None` | 任意 | 許可 | None |
| `significance` | `str \| None` | 任意 | 許可 | None |
| `hypotheses` | `list[str] \| None` | 任意 | 許可 | None |
| `decision_context` | `dict[str, Any] \| None` | 任意 | 許可 | None |
| `relations` | `list[dict[str, str]] \| None` | 任意 | 許可 | None |

**Request JSON例（説明用）**

```json
{}
```

#### Response

- HTTP **200**。Body schema: Service output（未型付け）。

**Routerにresponse_model未宣言。** Service返却項目は別途照合が必要。Type/keysが公開契約として確定したとはみなさない。


#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗した場合 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 指定Resourceがない・別Projectである等、ServiceがEntityNotFoundを送出 | Handlerで確定、実到達は要確認 |
| 409 | PROJECT_ARCHIVED / RESOURCE_IMMUTABLE | ARCHIVEDまたはFIXEDに対する不適格変更の際、該当例外を送出した場合 | Handlerで確定、Operationごとの到達は要確認 |
| 422 | INVALID_SCHEMA | Study/Family/Referencesの整合性、FIXED Context/Analysis View要件、revision前提等でServiceのInvalidSchemaが発生 | Service/Domainで具体化 |

#### 根拠・未検証事項

- Router Source: `workspace_lifecycle.py`（blob `eb90bd940fc7a35b84cda0e3fa58235a738cb0a1`）。Request DTO: `ResearchContextPatch`、Response Model: `未宣言`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.10 `POST /api/v1/projects/{project_id}/research-contexts/{context_id}/fix`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-10-10` |
| Method / Path | `POST /api/v1/projects/{project_id}/research-contexts/{context_id}/fix` |
| Handler | `workspace_lifecycle.py::fix_research_context` |
| Success Status | HTTP 200 |

#### Request

**Path parameters**

| 項目 | 型 | 必須 |
|---|---|---|
| `project_id` | string | 必須 |
| `context_id` | string | 必須 |

**Query parameters**

なし

**Headers**

Router固有の必須Header宣言なし

**Request Body / Field定義**

Request JSON Bodyなし（Router未定義）。

#### Response

- HTTP **200**。Body schema: Service output（未型付け）。

**Routerにresponse_model未宣言。** Service返却項目は別途照合が必要。Type/keysが公開契約として確定したとはみなさない。


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

### 4.11 `GET /api/v1/projects/{project_id}/research-contexts/{context_id}/usage`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-10-11` |
| Method / Path | `GET /api/v1/projects/{project_id}/research-contexts/{context_id}/usage` |
| Handler | `workspace_lifecycle.py::research_context_usage` |
| Success Status | HTTP 200 |

#### Request

**Path parameters**

| 項目 | 型 | 必須 |
|---|---|---|
| `project_id` | string | 必須 |
| `context_id` | string | 必須 |

**Query parameters**

なし

**Headers**

Router固有の必須Header宣言なし

**Request Body / Field定義**

Request JSON Bodyなし（Router未定義）。

#### Response

- HTTP **200**。Body schema: Service output（未型付け）。

**Routerにresponse_model未宣言。** Service返却項目は別途照合が必要。Type/keysが公開契約として確定したとはみなさない。


#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗した場合 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 指定Resourceがない・別Projectである等、ServiceがEntityNotFoundを送出 | Handlerで確定、実到達は要確認 |
| 422 | INVALID_SCHEMA | Study/Family/Referencesの整合性、FIXED Context/Analysis View要件、revision前提等でServiceのInvalidSchemaが発生 | Service/Domainで具体化 |

#### 根拠・未検証事項

- Router Source: `workspace_lifecycle.py`（blob `eb90bd940fc7a35b84cda0e3fa58235a738cb0a1`）。Request DTO: `none`、Response Model: `未宣言`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

## 5. 検証状況

- Route/Method/Path: 11 件 Source確認。
- Request: Router/Pydanticモデルの静的制約を反映。Response: 型付きモデルは全Fieldを表記。Service無型応答は一部未確定。
- HTTP Contract Test: NOT_RUN。Endpoint詳細の完全性・認可・実行時エラー網羅は未検証。
- 元の`docs/wiki/requirement_definition/`への昇格: NOT_DONE。

## 6. 既存Domain・設計制約（旧仕様本文から保持）

以下は既存のDomain規範・補足情報を保持したもの。重複する旧Route一覧より§2（Source基準）を優先する。改訂前の原本文はGit Blob `86589acb8ca6cd4873134dd7775ddcd0943b14ee`で追跡可能。

### Project / Research Context API

Project / Research ContextはFamily切替とは独立したProject-scoped resourceである。Project Managementがresource lifecycleを所有し、Family tab操作でresource identityを変更しない。

代表contract:

| Method | Path | 用途 |
| --- | --- | --- |
| POST | `/projects` | Project作成 |
| GET | `/projects` | Project一覧 |
| GET | `/projects/{project_id}` | Project取得 |
| PATCH | `/projects/{project_id}` | ACTIVE Project更新 |
| DELETE | `/projects/{project_id}` | Project archive |
| POST | `/projects/{project_id}/research-contexts` | Research Context DRAFT作成 |
| GET | `/projects/{project_id}/research-contexts` | Context一覧 |
| GET | `/projects/{project_id}/research-contexts/{context_id}` | Context取得 |
| PATCH | `/projects/{project_id}/research-contexts/{context_id}` | DRAFT更新 |
| POST | `/projects/{project_id}/research-contexts/{context_id}/fix` | FIXED化 |
| GET | `/projects/{project_id}/research-contexts/{context_id}/usage` | Analysis Specification利用状況とhistorical Family execution/result projectionを返す |

`research-contexts/{context_id}/usage`の現行実装実装は`AnalysisSpecificationOrm`に加え、historical/compatibility read modelである`FamilyExecutionOrm / FamilyResultOrm`を参照する。canonical `Execution / Result`全体の完全なusage indexではないため、そのように一般化しない。

Navigation routeはProject / Research Contextのidentity authorityではない。

**当該Interfaceの追加契約（関連Requirement）**

- **`FR-121`**：全project-scoped routeでpersisted ProjectMembership role（OWNER/EDITOR/VIEWER）に基づくauthorizationをservice action前に検証する

## 7. 改訂記録

- 2026-11-17: 全23_10〜23_19共通フォーマットへ再構成。Request/Response/ErrorsをOperation別に記載し、Source確認と未検証を分離。
