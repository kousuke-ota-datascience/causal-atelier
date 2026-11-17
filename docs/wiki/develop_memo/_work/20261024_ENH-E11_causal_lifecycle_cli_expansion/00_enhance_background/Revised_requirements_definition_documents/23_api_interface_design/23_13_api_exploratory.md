# 23_13_api_exploratory — Exploratory / Analysis View Web API仕様

## 1. API概要

- 対象: Exploratory / Analysis View のHTTP契約。
- Base path: `/api/v1`。
- 本改訂はOwner採用の**Operation単位Request/Response/Errors定義**を対象とする。実行時PASSや要件変更を含まない。
- Source snapshot: `89d4f135d8c680805731934e715b079ea0f72f2b`。Currentに対する未検証事項を明示する。

## 2. エンドポイント一覧

| No. | HTTP | Path | Handler | HTTP Success |
|---:|---|---|---|---|
| 1 | `POST` | `/api/v1/projects/{project_id}/analysis-views` | `create_analysis_view` | `201` |
| 2 | `GET` | `/api/v1/projects/{project_id}/analysis-views` | `list_analysis_views` | `200` |
| 3 | `GET` | `/api/v1/projects/{project_id}/analysis-views/{analysis_view_id}` | `get_analysis_view` | `200` |
| 4 | `PATCH` | `/api/v1/projects/{project_id}/analysis-views/{analysis_view_id}` | `update_analysis_view` | `200` |
| 5 | `POST` | `/api/v1/projects/{project_id}/analysis-views/{analysis_view_id}/validate` | `validate_analysis_view` | `200` |
| 6 | `POST` | `/api/v1/projects/{project_id}/analysis-views/{analysis_view_id}/fix` | `fix_analysis_view` | `200` |
| 7 | `POST` | `/api/v1/projects/{project_id}/exploration/preview` | `preview_exploration` | `200` |
| 8 | `POST` | `/api/v1/projects/{project_id}/exploration/executions` | `submit_exploration` | `202` |
| 9 | `GET` | `/api/v1/projects/{project_id}/exploration/executions` | `list_exploration_executions` | `200` |
| 10 | `GET` | `/api/v1/projects/{project_id}/exploration/executions/{execution_id}` | `get_exploration_execution` | `200` |
| 11 | `GET` | `/api/v1/projects/{project_id}/exploration/results` | `list_exploration_results` | `200` |
| 12 | `GET` | `/api/v1/projects/{project_id}/exploration/results/{result_id}` | `get_exploration_result` | `200` |
| 13 | `POST` | `/api/v1/projects/{project_id}/exploration/results/{result_id}/create-analysis-draft` | `create_analysis_draft` | `201` |
| 14 | `GET` | `/api/v1/projects/{project_id}/exploration/capabilities` | `exploration_capabilities` | `200` |

## 3. 共通Error Response形式

CURRENTのDomainError/RequestValidationError Handlerは`application/problem+json`ではなく、以下のJSON envelope。

```json
{"error":{"code":"INVALID_REQUEST","message":"Request validation failed.","details":{},"request_id":"{request_id}"}}
```

共通Handlerに定義されたErrorがすべてのOperationから発生するとは限らない。下表の条件付きErrorはテストPASS済みという意味ではない。

## 4. エンドポイント詳細

### 4.1 `POST /api/v1/projects/{project_id}/analysis-views`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-13-01` |
| Method / Path | `POST /api/v1/projects/{project_id}/analysis-views` |
| Handler | `exploration.py::create_analysis_view` |
| Success Status | HTTP 201 |

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

Content-Type: `application/json`、型 `AnalysisViewCreate`

| 項目（wire） | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `view_key` | `str` | 必須 | 不可 | min_length=1, max_length=100 |
| `name` | `str` | 必須 | 不可 | min_length=1, max_length=200 |
| `spec` | `dict[str, Any]` | 必須 | 不可 | — |

**Request JSON例（schema由来の説明用）**

```json
{
  "view_key": "string",
  "name": "string",
  "spec": {}
}
```

#### Response

- HTTP **201**。Body schema: `AnalysisViewResponse`。

| 項目（wire） | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `analysis_view_id` | `str` | 必須 | 不可 | — |
| `project_id` | `str` | 必須 | 不可 | — |
| `source_dataset_version_id` | `str` | 必須 | 不可 | — |
| `view_key` | `str` | 必須 | 不可 | — |
| `version_number` | `int` | 必須 | 不可 | — |
| `name` | `str` | 必須 | 不可 | — |
| `status` | `str` | 必須 | 不可 | — |
| `schema_version` | `str` | 必須 | 不可 | — |
| `spec` | `dict[str, Any]` | 必須 | 不可 | — |
| `content_hash` | `str \| None` | 必須 | 許可 | — |
| `manifest` | `dict[str, Any]` | 必須 | 不可 | — |
| `created_by` | `str` | 必須 | 不可 | — |
| `created_at` | `datetime \| None` | 必須 | 許可 | — |
| `fixed_at` | `datetime \| None` | 必須 | 許可 | — |

**Response JSON構造例（schema由来の説明用）**

```json
{
  "analysis_view_id": "{analysis_view_id}",
  "project_id": "{project_id}",
  "source_dataset_version_id": "{source_dataset_version_id}",
  "view_key": "string",
  "version_number": 0,
  "name": "string",
  "status": "string",
  "schema_version": "string",
  "spec": {},
  "content_hash": "string",
  "manifest": {},
  "created_by": "string",
  "created_at": "2026-11-17T00:00:00Z",
  "fixed_at": "2026-11-17T00:00:00Z"
}
```

#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗した場合 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 指定Resourceがない・別Projectである等、ServiceがEntityNotFoundを送出 | Handlerで確定、実到達は要確認 |
| 409 | PROJECT_ARCHIVED / RESOURCE_IMMUTABLE | ARCHIVEDまたはFIXEDに対する不適格変更の際、該当例外を送出した場合 | Handlerで確定、Operationごとの到達は要確認 |
| 422 | FILTER_TYPE_MISMATCH | Data logical type × filter operator不整合（Serviceが該当例外を送出した場合） | 共通Handler;実到達は要検証 |

#### 根拠・未検証事項

- Router Source: `exploration.py`（blob `8c068c77357cd628cd278e3668cdf23ff5a6046c`）。Request DTO: `AnalysisViewCreate`、Response Model: `AnalysisViewResponse`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.2 `GET /api/v1/projects/{project_id}/analysis-views`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-13-02` |
| Method / Path | `GET /api/v1/projects/{project_id}/analysis-views` |
| Handler | `exploration.py::list_analysis_views` |
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

- HTTP **200**。Body schema: `AnalysisViewListResponse`。

| 項目（wire） | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `items` | `list[AnalysisViewResponse]` | 必須 | 不可 | — |
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
| 422 | FILTER_TYPE_MISMATCH | Data logical type × filter operator不整合（Serviceが該当例外を送出した場合） | 共通Handler;実到達は要検証 |

#### 根拠・未検証事項

- Router Source: `exploration.py`（blob `8c068c77357cd628cd278e3668cdf23ff5a6046c`）。Request DTO: `none`、Response Model: `AnalysisViewListResponse`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.3 `GET /api/v1/projects/{project_id}/analysis-views/{analysis_view_id}`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-13-03` |
| Method / Path | `GET /api/v1/projects/{project_id}/analysis-views/{analysis_view_id}` |
| Handler | `exploration.py::get_analysis_view` |
| Success Status | HTTP 200 |

#### Request

**Path parameters**

| 項目 | 型 | 必須 |
|---|---|---|
| `project_id` | string | 必須 |
| `analysis_view_id` | string | 必須 |

**Query parameters**

なし

**Headers**

Router固有の必須Header宣言なし

**Request Body / Field定義**

Request JSON Bodyなし（Router未定義）。

#### Response

- HTTP **200**。Body schema: `AnalysisViewResponse`。

| 項目（wire） | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `analysis_view_id` | `str` | 必須 | 不可 | — |
| `project_id` | `str` | 必須 | 不可 | — |
| `source_dataset_version_id` | `str` | 必須 | 不可 | — |
| `view_key` | `str` | 必須 | 不可 | — |
| `version_number` | `int` | 必須 | 不可 | — |
| `name` | `str` | 必須 | 不可 | — |
| `status` | `str` | 必須 | 不可 | — |
| `schema_version` | `str` | 必須 | 不可 | — |
| `spec` | `dict[str, Any]` | 必須 | 不可 | — |
| `content_hash` | `str \| None` | 必須 | 許可 | — |
| `manifest` | `dict[str, Any]` | 必須 | 不可 | — |
| `created_by` | `str` | 必須 | 不可 | — |
| `created_at` | `datetime \| None` | 必須 | 許可 | — |
| `fixed_at` | `datetime \| None` | 必須 | 許可 | — |

**Response JSON構造例（schema由来の説明用）**

```json
{
  "analysis_view_id": "{analysis_view_id}",
  "project_id": "{project_id}",
  "source_dataset_version_id": "{source_dataset_version_id}",
  "view_key": "string",
  "version_number": 0,
  "name": "string",
  "status": "string",
  "schema_version": "string",
  "spec": {},
  "content_hash": "string",
  "manifest": {},
  "created_by": "string",
  "created_at": "2026-11-17T00:00:00Z",
  "fixed_at": "2026-11-17T00:00:00Z"
}
```

#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗した場合 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 指定Resourceがない・別Projectである等、ServiceがEntityNotFoundを送出 | Handlerで確定、実到達は要確認 |
| 422 | FILTER_TYPE_MISMATCH | Data logical type × filter operator不整合（Serviceが該当例外を送出した場合） | 共通Handler;実到達は要検証 |

#### 根拠・未検証事項

- Router Source: `exploration.py`（blob `8c068c77357cd628cd278e3668cdf23ff5a6046c`）。Request DTO: `none`、Response Model: `AnalysisViewResponse`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.4 `PATCH /api/v1/projects/{project_id}/analysis-views/{analysis_view_id}`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-13-04` |
| Method / Path | `PATCH /api/v1/projects/{project_id}/analysis-views/{analysis_view_id}` |
| Handler | `exploration.py::update_analysis_view` |
| Success Status | HTTP 200 |

#### Request

**Path parameters**

| 項目 | 型 | 必須 |
|---|---|---|
| `project_id` | string | 必須 |
| `analysis_view_id` | string | 必須 |

**Query parameters**

なし

**Headers**

Router固有の必須Header宣言なし

**Request Body / Field定義**

Content-Type: `application/json`、型 `AnalysisViewUpdate`

| 項目（wire） | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `name` | `str \| None` | 任意 | 許可 | lt=None, min_length=1, max_length=200 |
| `spec` | `dict[str, Any] \| None` | 任意 | 許可 | None |

**Request JSON例（schema由来の説明用）**

```json
{}
```

#### Response

- HTTP **200**。Body schema: `AnalysisViewResponse`。

| 項目（wire） | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `analysis_view_id` | `str` | 必須 | 不可 | — |
| `project_id` | `str` | 必須 | 不可 | — |
| `source_dataset_version_id` | `str` | 必須 | 不可 | — |
| `view_key` | `str` | 必須 | 不可 | — |
| `version_number` | `int` | 必須 | 不可 | — |
| `name` | `str` | 必須 | 不可 | — |
| `status` | `str` | 必須 | 不可 | — |
| `schema_version` | `str` | 必須 | 不可 | — |
| `spec` | `dict[str, Any]` | 必須 | 不可 | — |
| `content_hash` | `str \| None` | 必須 | 許可 | — |
| `manifest` | `dict[str, Any]` | 必須 | 不可 | — |
| `created_by` | `str` | 必須 | 不可 | — |
| `created_at` | `datetime \| None` | 必須 | 許可 | — |
| `fixed_at` | `datetime \| None` | 必須 | 許可 | — |

**Response JSON構造例（schema由来の説明用）**

```json
{
  "analysis_view_id": "{analysis_view_id}",
  "project_id": "{project_id}",
  "source_dataset_version_id": "{source_dataset_version_id}",
  "view_key": "string",
  "version_number": 0,
  "name": "string",
  "status": "string",
  "schema_version": "string",
  "spec": {},
  "content_hash": "string",
  "manifest": {},
  "created_by": "string",
  "created_at": "2026-11-17T00:00:00Z",
  "fixed_at": "2026-11-17T00:00:00Z"
}
```

#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗した場合 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 指定Resourceがない・別Projectである等、ServiceがEntityNotFoundを送出 | Handlerで確定、実到達は要確認 |
| 409 | PROJECT_ARCHIVED / RESOURCE_IMMUTABLE | ARCHIVEDまたはFIXEDに対する不適格変更の際、該当例外を送出した場合 | Handlerで確定、Operationごとの到達は要確認 |
| 422 | FILTER_TYPE_MISMATCH | Data logical type × filter operator不整合（Serviceが該当例外を送出した場合） | 共通Handler;実到達は要検証 |

#### 根拠・未検証事項

- Router Source: `exploration.py`（blob `8c068c77357cd628cd278e3668cdf23ff5a6046c`）。Request DTO: `AnalysisViewUpdate`、Response Model: `AnalysisViewResponse`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.5 `POST /api/v1/projects/{project_id}/analysis-views/{analysis_view_id}/validate`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-13-05` |
| Method / Path | `POST /api/v1/projects/{project_id}/analysis-views/{analysis_view_id}/validate` |
| Handler | `exploration.py::validate_analysis_view` |
| Success Status | HTTP 200 |

#### Request

**Path parameters**

| 項目 | 型 | 必須 |
|---|---|---|
| `project_id` | string | 必須 |
| `analysis_view_id` | string | 必須 |

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
| 422 | FILTER_TYPE_MISMATCH | Data logical type × filter operator不整合（Serviceが該当例外を送出した場合） | 共通Handler;実到達は要検証 |

#### 根拠・未検証事項

- Router Source: `exploration.py`（blob `8c068c77357cd628cd278e3668cdf23ff5a6046c`）。Request DTO: `none`、Response Model: `未宣言`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.6 `POST /api/v1/projects/{project_id}/analysis-views/{analysis_view_id}/fix`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-13-06` |
| Method / Path | `POST /api/v1/projects/{project_id}/analysis-views/{analysis_view_id}/fix` |
| Handler | `exploration.py::fix_analysis_view` |
| Success Status | HTTP 200 |

#### Request

**Path parameters**

| 項目 | 型 | 必須 |
|---|---|---|
| `project_id` | string | 必須 |
| `analysis_view_id` | string | 必須 |

**Query parameters**

なし

**Headers**

Router固有の必須Header宣言なし

**Request Body / Field定義**

Request JSON Bodyなし（Router未定義）。

#### Response

- HTTP **200**。Body schema: `AnalysisViewResponse`。

| 項目（wire） | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `analysis_view_id` | `str` | 必須 | 不可 | — |
| `project_id` | `str` | 必須 | 不可 | — |
| `source_dataset_version_id` | `str` | 必須 | 不可 | — |
| `view_key` | `str` | 必須 | 不可 | — |
| `version_number` | `int` | 必須 | 不可 | — |
| `name` | `str` | 必須 | 不可 | — |
| `status` | `str` | 必須 | 不可 | — |
| `schema_version` | `str` | 必須 | 不可 | — |
| `spec` | `dict[str, Any]` | 必須 | 不可 | — |
| `content_hash` | `str \| None` | 必須 | 許可 | — |
| `manifest` | `dict[str, Any]` | 必須 | 不可 | — |
| `created_by` | `str` | 必須 | 不可 | — |
| `created_at` | `datetime \| None` | 必須 | 許可 | — |
| `fixed_at` | `datetime \| None` | 必須 | 許可 | — |

**Response JSON構造例（schema由来の説明用）**

```json
{
  "analysis_view_id": "{analysis_view_id}",
  "project_id": "{project_id}",
  "source_dataset_version_id": "{source_dataset_version_id}",
  "view_key": "string",
  "version_number": 0,
  "name": "string",
  "status": "string",
  "schema_version": "string",
  "spec": {},
  "content_hash": "string",
  "manifest": {},
  "created_by": "string",
  "created_at": "2026-11-17T00:00:00Z",
  "fixed_at": "2026-11-17T00:00:00Z"
}
```

#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗した場合 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 指定Resourceがない・別Projectである等、ServiceがEntityNotFoundを送出 | Handlerで確定、実到達は要確認 |
| 409 | PROJECT_ARCHIVED / RESOURCE_IMMUTABLE | ARCHIVEDまたはFIXEDに対する不適格変更の際、該当例外を送出した場合 | Handlerで確定、Operationごとの到達は要確認 |
| 422 | FILTER_TYPE_MISMATCH | Data logical type × filter operator不整合（Serviceが該当例外を送出した場合） | 共通Handler;実到達は要検証 |

#### 根拠・未検証事項

- Router Source: `exploration.py`（blob `8c068c77357cd628cd278e3668cdf23ff5a6046c`）。Request DTO: `none`、Response Model: `AnalysisViewResponse`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.7 `POST /api/v1/projects/{project_id}/exploration/preview`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-13-07` |
| Method / Path | `POST /api/v1/projects/{project_id}/exploration/preview` |
| Handler | `exploration.py::preview_exploration` |
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

Content-Type: `application/json`、型 `ExplorationRequest`

| 項目（wire） | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `dataset_version_id` | `str` | 必須 | 不可 | — |
| `analysis_view_id` | `str \| None` | 任意 | 許可 | None |
| `family_spec` | `dict[str, Any]` | 必須 | 不可 | — |

**Request JSON例（schema由来の説明用）**

```json
{
  "dataset_version_id": "{dataset_version_id}",
  "family_spec": {}
}
```

#### Response

- HTTP **200**。Body schema: `ExplorationPreviewResponse`。

| 項目（wire） | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `schema_version` | `str` | 必須 | 不可 | — |
| `analysis_family` | `Literal["EXPLORATORY"]` | 必須 | 不可 | — |
| `result_type` | `str` | 必須 | 不可 | — |
| `analytical_status` | `str` | 必須 | 不可 | — |
| `summary` | `dict[str, Any]` | 必須 | 不可 | — |
| `payload` | `dict[str, Any]` | 必須 | 不可 | — |
| `warnings` | `list[Any]` | 必須 | 不可 | — |
| `view_manifest` | `dict[str, Any]` | 必須 | 不可 | — |
| `saved` | `Literal[False]` | 必須 | 不可 | — |

**Response JSON構造例（schema由来の説明用）**

```json
{
  "schema_version": "string",
  "analysis_family": "EXPLORATORY",
  "result_type": "string",
  "analytical_status": "string",
  "summary": {},
  "payload": {},
  "warnings": [],
  "view_manifest": {},
  "saved": null
}
```

#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗した場合 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 指定Resourceがない・別Projectである等、ServiceがEntityNotFoundを送出 | Handlerで確定、実到達は要確認 |
| 409 | PROJECT_ARCHIVED / RESOURCE_IMMUTABLE | ARCHIVEDまたはFIXEDに対する不適格変更の際、該当例外を送出した場合 | Handlerで確定、Operationごとの到達は要確認 |
| 422 | FILTER_TYPE_MISMATCH | Data logical type × filter operator不整合（Serviceが該当例外を送出した場合） | 共通Handler;実到達は要検証 |

#### 根拠・未検証事項

- Router Source: `exploration.py`（blob `8c068c77357cd628cd278e3668cdf23ff5a6046c`）。Request DTO: `ExplorationRequest`、Response Model: `ExplorationPreviewResponse`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.8 `POST /api/v1/projects/{project_id}/exploration/executions`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-13-08` |
| Method / Path | `POST /api/v1/projects/{project_id}/exploration/executions` |
| Handler | `exploration.py::submit_exploration` |
| Success Status | HTTP 202 |

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

Content-Type: `application/json`、型 `ExplorationRequest`

| 項目（wire） | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `dataset_version_id` | `str` | 必須 | 不可 | — |
| `analysis_view_id` | `str \| None` | 任意 | 許可 | None |
| `family_spec` | `dict[str, Any]` | 必須 | 不可 | — |

**Request JSON例（schema由来の説明用）**

```json
{
  "dataset_version_id": "{dataset_version_id}",
  "family_spec": {}
}
```

#### Response

- HTTP **202**。Body schema: `FamilyExecutionResponse`。

| 項目（wire） | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `execution_id` | `str` | 必須 | 不可 | — |
| `project_id` | `str` | 必須 | 不可 | — |
| `dataset_version_id` | `str` | 必須 | 不可 | — |
| `analysis_view_id` | `str \| None` | 必須 | 許可 | — |
| `execution_plan_id` | `str` | 必須 | 不可 | — |
| `analysis_family` | `str` | 必須 | 不可 | — |
| `specification_schema_version` | `str` | 必須 | 不可 | — |
| `snapshot_hash` | `str` | 必須 | 不可 | — |
| `status` | `str` | 必須 | 不可 | — |
| `requested_at` | `datetime \| None` | 必須 | 許可 | — |
| `started_at` | `datetime \| None` | 必須 | 許可 | — |
| `finished_at` | `datetime \| None` | 必須 | 許可 | — |
| `last_error` | `dict[str, Any] \| None` | 必須 | 許可 | — |

**Response JSON構造例（schema由来の説明用）**

```json
{
  "execution_id": "{execution_id}",
  "project_id": "{project_id}",
  "dataset_version_id": "{dataset_version_id}",
  "analysis_view_id": "{analysis_view_id}",
  "execution_plan_id": "{execution_plan_id}",
  "analysis_family": "string",
  "specification_schema_version": "string",
  "snapshot_hash": "string",
  "status": "string",
  "requested_at": "2026-11-17T00:00:00Z",
  "started_at": "2026-11-17T00:00:00Z",
  "finished_at": "2026-11-17T00:00:00Z",
  "last_error": {}
}
```

#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗した場合 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 指定Resourceがない・別Projectである等、ServiceがEntityNotFoundを送出 | Handlerで確定、実到達は要確認 |
| 409 | PROJECT_ARCHIVED / RESOURCE_IMMUTABLE | ARCHIVEDまたはFIXEDに対する不適格変更の際、該当例外を送出した場合 | Handlerで確定、Operationごとの到達は要確認 |
| 422 | FILTER_TYPE_MISMATCH | Data logical type × filter operator不整合（Serviceが該当例外を送出した場合） | 共通Handler;実到達は要検証 |

#### 根拠・未検証事項

- Router Source: `exploration.py`（blob `8c068c77357cd628cd278e3668cdf23ff5a6046c`）。Request DTO: `ExplorationRequest`、Response Model: `FamilyExecutionResponse`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.9 `GET /api/v1/projects/{project_id}/exploration/executions`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-13-09` |
| Method / Path | `GET /api/v1/projects/{project_id}/exploration/executions` |
| Handler | `exploration.py::list_exploration_executions` |
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

- HTTP **200**。Body schema: `FamilyExecutionListResponse`。

| 項目（wire） | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `items` | `list[FamilyExecutionResponse]` | 必須 | 不可 | — |
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
| 422 | FILTER_TYPE_MISMATCH | Data logical type × filter operator不整合（Serviceが該当例外を送出した場合） | 共通Handler;実到達は要検証 |

#### 根拠・未検証事項

- Router Source: `exploration.py`（blob `8c068c77357cd628cd278e3668cdf23ff5a6046c`）。Request DTO: `none`、Response Model: `FamilyExecutionListResponse`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.10 `GET /api/v1/projects/{project_id}/exploration/executions/{execution_id}`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-13-10` |
| Method / Path | `GET /api/v1/projects/{project_id}/exploration/executions/{execution_id}` |
| Handler | `exploration.py::get_exploration_execution` |
| Success Status | HTTP 200 |

#### Request

**Path parameters**

| 項目 | 型 | 必須 |
|---|---|---|
| `project_id` | string | 必須 |
| `execution_id` | string | 必須 |

**Query parameters**

なし

**Headers**

Router固有の必須Header宣言なし

**Request Body / Field定義**

Request JSON Bodyなし（Router未定義）。

#### Response

- HTTP **200**。Body schema: `FamilyExecutionResponse`。

| 項目（wire） | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `execution_id` | `str` | 必須 | 不可 | — |
| `project_id` | `str` | 必須 | 不可 | — |
| `dataset_version_id` | `str` | 必須 | 不可 | — |
| `analysis_view_id` | `str \| None` | 必須 | 許可 | — |
| `execution_plan_id` | `str` | 必須 | 不可 | — |
| `analysis_family` | `str` | 必須 | 不可 | — |
| `specification_schema_version` | `str` | 必須 | 不可 | — |
| `snapshot_hash` | `str` | 必須 | 不可 | — |
| `status` | `str` | 必須 | 不可 | — |
| `requested_at` | `datetime \| None` | 必須 | 許可 | — |
| `started_at` | `datetime \| None` | 必須 | 許可 | — |
| `finished_at` | `datetime \| None` | 必須 | 許可 | — |
| `last_error` | `dict[str, Any] \| None` | 必須 | 許可 | — |

**Response JSON構造例（schema由来の説明用）**

```json
{
  "execution_id": "{execution_id}",
  "project_id": "{project_id}",
  "dataset_version_id": "{dataset_version_id}",
  "analysis_view_id": "{analysis_view_id}",
  "execution_plan_id": "{execution_plan_id}",
  "analysis_family": "string",
  "specification_schema_version": "string",
  "snapshot_hash": "string",
  "status": "string",
  "requested_at": "2026-11-17T00:00:00Z",
  "started_at": "2026-11-17T00:00:00Z",
  "finished_at": "2026-11-17T00:00:00Z",
  "last_error": {}
}
```

#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗した場合 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 指定Resourceがない・別Projectである等、ServiceがEntityNotFoundを送出 | Handlerで確定、実到達は要確認 |
| 422 | FILTER_TYPE_MISMATCH | Data logical type × filter operator不整合（Serviceが該当例外を送出した場合） | 共通Handler;実到達は要検証 |

#### 根拠・未検証事項

- Router Source: `exploration.py`（blob `8c068c77357cd628cd278e3668cdf23ff5a6046c`）。Request DTO: `none`、Response Model: `FamilyExecutionResponse`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.11 `GET /api/v1/projects/{project_id}/exploration/results`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-13-11` |
| Method / Path | `GET /api/v1/projects/{project_id}/exploration/results` |
| Handler | `exploration.py::list_exploration_results` |
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

- HTTP **200**。Body schema: `FamilyResultListResponse`。

| 項目（wire） | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `items` | `list[FamilyResultResponse]` | 必須 | 不可 | — |
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
| 422 | FILTER_TYPE_MISMATCH | Data logical type × filter operator不整合（Serviceが該当例外を送出した場合） | 共通Handler;実到達は要検証 |

#### 根拠・未検証事項

- Router Source: `exploration.py`（blob `8c068c77357cd628cd278e3668cdf23ff5a6046c`）。Request DTO: `none`、Response Model: `FamilyResultListResponse`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.12 `GET /api/v1/projects/{project_id}/exploration/results/{result_id}`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-13-12` |
| Method / Path | `GET /api/v1/projects/{project_id}/exploration/results/{result_id}` |
| Handler | `exploration.py::get_exploration_result` |
| Success Status | HTTP 200 |

#### Request

**Path parameters**

| 項目 | 型 | 必須 |
|---|---|---|
| `project_id` | string | 必須 |
| `result_id` | string | 必須 |

**Query parameters**

なし

**Headers**

Router固有の必須Header宣言なし

**Request Body / Field定義**

Request JSON Bodyなし（Router未定義）。

#### Response

- HTTP **200**。Body schema: `FamilyResultResponse`。

| 項目（wire） | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `result_id` | `str` | 必須 | 不可 | — |
| `project_id` | `str` | 必須 | 不可 | — |
| `execution_id` | `str` | 必須 | 不可 | — |
| `stage_execution_id` | `str` | 必須 | 不可 | — |
| `analysis_family` | `str` | 必須 | 不可 | — |
| `result_type` | `str` | 必須 | 不可 | — |
| `schema_version` | `str` | 必須 | 不可 | — |
| `analytical_status` | `str` | 必須 | 不可 | — |
| `summary` | `dict[str, Any]` | 必須 | 不可 | — |
| `payload` | `dict[str, Any]` | 必須 | 不可 | — |
| `diagnostics` | `dict[str, Any]` | 必須 | 不可 | — |
| `warnings` | `list[Any]` | 必須 | 不可 | — |
| `created_at` | `datetime \| None` | 必須 | 許可 | — |

**Response JSON構造例（schema由来の説明用）**

```json
{
  "result_id": "{result_id}",
  "project_id": "{project_id}",
  "execution_id": "{execution_id}",
  "stage_execution_id": "{stage_execution_id}",
  "analysis_family": "string",
  "result_type": "string",
  "schema_version": "string",
  "analytical_status": "string",
  "summary": {},
  "payload": {},
  "diagnostics": {},
  "warnings": [],
  "created_at": "2026-11-17T00:00:00Z"
}
```

#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗した場合 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 指定Resourceがない・別Projectである等、ServiceがEntityNotFoundを送出 | Handlerで確定、実到達は要確認 |
| 422 | FILTER_TYPE_MISMATCH | Data logical type × filter operator不整合（Serviceが該当例外を送出した場合） | 共通Handler;実到達は要検証 |

#### 根拠・未検証事項

- Router Source: `exploration.py`（blob `8c068c77357cd628cd278e3668cdf23ff5a6046c`）。Request DTO: `none`、Response Model: `FamilyResultResponse`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.13 `POST /api/v1/projects/{project_id}/exploration/results/{result_id}/create-analysis-draft`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-13-13` |
| Method / Path | `POST /api/v1/projects/{project_id}/exploration/results/{result_id}/create-analysis-draft` |
| Handler | `exploration.py::create_analysis_draft` |
| Success Status | HTTP 201 |

#### Request

**Path parameters**

| 項目 | 型 | 必須 |
|---|---|---|
| `project_id` | string | 必須 |
| `result_id` | string | 必須 |

**Query parameters**

なし

**Headers**

Router固有の必須Header宣言なし

**Request Body / Field定義**

Content-Type: `application/json`、型 `CreateDraftRequest`

| 項目（wire） | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `target_family` | `Literal["CAUSAL", "PREDICTIVE"]` | 必須 | 不可 | — |
| `analysis_mode` | `Literal["EXPLORATORY", "CONFIRMATORY"]` | 必須 | 不可 | — |
| `research_context_version_id` | `str \| None` | 任意 | 許可 | None |
| `family_spec_schema_version` | `str \| None` | 任意 | 許可 | None |
| `family_spec` | `dict[str, Any] \| None` | 任意 | 許可 | None |

**Request JSON例（schema由来の説明用）**

```json
{
  "target_family": "CAUSAL",
  "analysis_mode": "EXPLORATORY"
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
| 422 | FILTER_TYPE_MISMATCH | Data logical type × filter operator不整合（Serviceが該当例外を送出した場合） | 共通Handler;実到達は要検証 |

#### 根拠・未検証事項

- Router Source: `exploration.py`（blob `8c068c77357cd628cd278e3668cdf23ff5a6046c`）。Request DTO: `CreateDraftRequest`、Response Model: `未宣言`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.14 `GET /api/v1/projects/{project_id}/exploration/capabilities`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-13-14` |
| Method / Path | `GET /api/v1/projects/{project_id}/exploration/capabilities` |
| Handler | `exploration.py::exploration_capabilities` |
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

- HTTP **200**。Body schema: Service output（未型付け）。

**Routerにresponse_model未宣言。** Service返却項目は別途照合が必要。Type/keysが公開契約として確定したとはみなさない。


#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗した場合 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 指定Resourceがない・別Projectである等、ServiceがEntityNotFoundを送出 | Handlerで確定、実到達は要確認 |
| 422 | FILTER_TYPE_MISMATCH | Data logical type × filter operator不整合（Serviceが該当例外を送出した場合） | 共通Handler;実到達は要検証 |

#### 根拠・未検証事項

- Router Source: `exploration.py`（blob `8c068c77357cd628cd278e3668cdf23ff5a6046c`）。Request DTO: `none`、Response Model: `未宣言`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

## 5. 検証状況

- Route/Method/Path: 14 件 Source確認。
- Request: Router/Pydanticモデルの静的制約を反映。Response: 型付きモデルは全Fieldを表記。Service無型応答は一部未確定。
- HTTP Contract Test: NOT_RUN。Endpoint詳細の完全性・認可・実行時エラー網羅は未検証。
- 元の`docs/wiki/requirement_definition/`への昇格: NOT_DONE。

## 6. 既存Domain・設計制約（旧仕様本文から保持）

以下は既存のDomain規範・補足情報を保持したもの。重複する旧Route一覧より§2（Source基準）を優先する。改訂前の原本文はGit Blob `e7bf094d57a1957b77a18006e57f168bcdfd01b4`で追跡可能。

### Exploratory Interface

Exploratory UIは`Profile / Data Quality / Distribution / Relationships / Comparison / Findings`をNavigation Stageとして持つが、各Navigation Stageに対応する新規Execution APIを1:1で要求しない。

現行実装で存在するExploratory / Analysis View interfaceは次である。

#### Analysis View

| Method | Path | 用途 |
| --- | --- | --- |
| POST | `/projects/{project_id}/analysis-views` | Analysis View作成 |
| GET | `/projects/{project_id}/analysis-views` | Analysis View一覧 |
| GET | `/projects/{project_id}/analysis-views/{analysis_view_id}` | Analysis View取得 |
| PATCH | `/projects/{project_id}/analysis-views/{analysis_view_id}` | DRAFT更新 |
| POST | `/projects/{project_id}/analysis-views/{analysis_view_id}/validate` | validation |
| POST | `/projects/{project_id}/analysis-views/{analysis_view_id}/fix` | FIXED化 |

#### Exploration

| Method | Path | 用途 |
| --- | --- | --- |
| POST | `/projects/{project_id}/exploration/preview` | 保存しない同期preview |
| POST | `/projects/{project_id}/exploration/executions` | persisted exploratory execution submit |
| GET | `/projects/{project_id}/exploration/executions` | exploratory execution一覧 |
| GET | `/projects/{project_id}/exploration/executions/{execution_id}` | exploratory execution取得 |
| GET | `/projects/{project_id}/exploration/results` | exploratory result一覧 |
| GET | `/projects/{project_id}/exploration/results/{result_id}` | exploratory result取得 |
| POST | `/projects/{project_id}/exploration/results/{result_id}/create-analysis-draft` | exploratory resultからCausal/Predictive analysis draft作成 |

`create-analysis-draft` request:

```json
{
  "target_family": "CAUSAL | PREDICTIVE",
  "analysis_mode": "EXPLORATORY | CONFIRMATORY",
  "research_context_version_id": "uuid-or-null",
  "family_spec_schema_version": "...",
  "family_spec": {}
}
```

Contract:

- `dataset_version_id / analysis_view_id`はsource Result lineageからderiveし、request overrideを受け付けない。
- research contextをsource lineageから一意に解決できない場合のみrequestで要求する。
- canonical `AnalysisSpecification`を`DRAFT`としてpersistする。
- source Resultからtarget AnalysisSpecificationへ`MOTIVATED` semantic lineageを保存する。
- auto FIX / auto Executionは行わない。
- same immutable `dataset_version_id` + `CONFIRMATORY`の場合、`EXPLORATORY_REUSE_SAME_DATA` warningとsource Result IDを返す。
| GET | `/projects/{project_id}/exploration/capabilities` | supported operation / chart mark metadata |

`ExplorationRequest`は`dataset_version_id / analysis_view_id? / family_spec`を受け取る。preview responseは`analysis_family = EXPLORATORY`、`result_type / analytical_status / summary / payload / warnings / view_manifest / saved=false`を返す。

Family-specific exploratory specのoperationは次である。

```text
PROFILE
DISTRIBUTION
ASSOCIATION
GROUP_SUMMARY
TIME_TREND
CHART
```

現行実装のExploratory plannerは各operationを1 runtime StageからなるExecution Planへ写像する。Navigation `Data Quality` / `Findings`等のために同名runtime endpointを追加せず、Dataset metadata、Result、Artifact、Annotation等のreadを組み合わせてよい。

## 7. 改訂記録

- 2026-11-17: 全23_10〜23_19共通フォーマットへ再構成。Request/Response/ErrorsをOperation別に記載し、Source確認と未検証を分離。
