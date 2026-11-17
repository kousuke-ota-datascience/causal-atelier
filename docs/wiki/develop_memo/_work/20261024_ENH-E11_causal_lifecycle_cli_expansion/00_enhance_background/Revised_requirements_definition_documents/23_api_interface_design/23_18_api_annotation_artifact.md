# 23_18_api_annotation_artifact — Annotation / Artifact / Export Web API仕様

## 1. API概要

- 対象: Annotation / Artifact / Export のHTTP契約。
- Base path: `/api/v1`。
- 本改訂はOwner採用の**Operation単位Request/Response/Errors定義**を対象とする。実行時PASSや要件変更を含まない。
- Source snapshot: `2068b3b2f8c096d581a0f2d56047c4185c5ac7cc`。CURRENTと未検証事項を分離する。

## 2. エンドポイント一覧

| No. | HTTP | Path | Handler | HTTP Success |
|---:|---|---|---|---|
| 1 | `GET` | `/api/v1/projects/{project_id}/workspace-annotations` | `list_workspace_annotations` | `200` |
| 2 | `POST` | `/api/v1/projects/{project_id}/workspace-annotations` | `create_workspace_annotation` | `201` |
| 3 | `PATCH` | `/api/v1/projects/{project_id}/workspace-annotations/{annotation_id}` | `update_workspace_annotation` | `200` |
| 4 | `GET` | `/api/v1/projects/{project_id}/artifacts/{artifact_id}` | `artifact_metadata` | `200` |
| 5 | `GET` | `/api/v1/projects/{project_id}/artifacts/{artifact_id}/download` | `download_artifact` | `200` |
| 6 | `POST` | `/api/v1/projects/{project_id}/exports` | `create_export` | `201` |
| 7 | `GET` | `/api/v1/projects/{project_id}/exports/{export_id}` | `get_export` | `200` |
| 8 | `GET` | `/api/v1/projects/{project_id}/exports/{export_id}/download` | `download_export` | `200` |
| 9 | `POST` | `/api/v1/projects/{project_id}/annotations` | `create_annotation` | `201` |
| 10 | `GET` | `/api/v1/annotations/{annotation_id}` | `get_annotation` | `200` |
| 11 | `PATCH` | `/api/v1/annotations/{annotation_id}` | `update_annotation` | `200` |
| 12 | `GET` | `/api/v1/artifacts/{artifact_id}` | `get_artifact` | `200` |
| 13 | `GET` | `/api/v1/artifacts/{artifact_id}/download` | `download_artifact` | `200` |

## 3. 共通Error Response形式

CURRENTのDomainError/RequestValidationError Handlerは`application/problem+json`ではなく、以下のJSON envelope。

```json
{"error":{"code":"INVALID_REQUEST","message":"Request validation failed.","details":{},"request_id":"{request_id}"}}
```

共通Handlerに定義されたErrorがすべてのOperationから発生するとは限らない。下表の条件付きErrorはテストPASS済みという意味ではない。

## 4. エンドポイント詳細

### 4.1 `GET /api/v1/projects/{project_id}/workspace-annotations`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-18-01` |
| Method / Path | `GET /api/v1/projects/{project_id}/workspace-annotations` |
| Handler | `product_closure.py::list_workspace_annotations` |
| Success Status | HTTP 200 |

#### Request

**Path parameters**

| 項目 | 型 | 必須 |
|---|---|---|
| `project_id` | string | 必須 |

**Query parameters**

| 項目 | 型 | default |
|---|---|---|
| `target_type` | `str \| None` | `Query(default=None)` |
| `target_id` | `str \| None` | `Query(default=None)` |

**Headers**

| Header | 仕様 |
|---|---|
| `X-User-Id` | Sourceで参照。認証確立の証拠ではない |

**Request Body / Field定義**

Request JSON Bodyなし（Router未定義）。

#### Response

- HTTP **200**。Body schema: JSON object。

| 項目 | 型 |
|---|---|
| `items` | array[Service resource] |

Service返却要素のField型は追加照合対象。

**Response JSON構造例（説明用）**

```json
{"items":[]}
```

#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 対象がなく、ServiceがEntityNotFoundを送出する場合 | 共通Handler。Operationごとの到達は要確認 |
| 403 | PROJECT_ACCESS_DENIED | Project membership/role不足のためClosure Serviceが拒否 | 共通Handler; gateway認証の保証ではない |

#### 根拠・未検証事項

- Router Source: `product_closure.py`（blob `7cae6a3df8725c3f5263ede17167225175f5968e`）。Request DTO: `none`、Response Model: `未宣言`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.2 `POST /api/v1/projects/{project_id}/workspace-annotations`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-18-02` |
| Method / Path | `POST /api/v1/projects/{project_id}/workspace-annotations` |
| Handler | `product_closure.py::create_workspace_annotation` |
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
| `Idempotency-Key` | IdempotencyService適用Commandなら非空必須 |
| `X-User-Id` | Sourceで参照。認証確立の証拠ではない |

**Request Body / Field定義**

Content-Type: `application/json`、型 `WorkspaceAnnotationCreate`

| 項目（wire） | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `target_type` | `Literal[ "Project", "ResearchContextVersion", "AnalysisView", "AnalysisSpecification", "Execution", "Result", "GraphVersion",` | 必須 | 不可 | — |
| `target_id` | `str` | 必須 | 不可 | min_length=1, max_length=100 |
| `statement` | `str` | 必須 | 不可 | min_length=1, max_length=8000 |
| `rationale` | `str \| None` | 任意 | 許可 | lt=None, max_length=8000 |
| `assumptions` | `list[Any]` | 任意 | 不可 | Field(default_factory=list) |
| `limitations` | `list[Any]` | 任意 | 不可 | Field(default_factory=list) |
| `decision` | `Literal["SELECTED", "REJECTED", "DEFERRED"] \| None` | 任意 | 許可 | None |
| `next_actions` | `list[Any]` | 任意 | 不可 | Field(default_factory=list) |

**Request JSON例（schema由来の説明用）**

```json
{
  "target_type": "Project",
  "target_id": "{target_id}",
  "statement": "string"
}
```

#### Response

- HTTP **201**。Body schema: Service output（response_model未宣言）。

Routerは`dict`を返すがPydantic response_model未宣言。Response Fieldの完全な型/キーは**未確定**。Service return値の追加照合が必要。


#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗 | 共通Handler |
| 400/409 | IDEMPOTENCY_KEY_REQUIRED / IDEMPOTENCY_CONFLICT | Key欠落・異なる内容の同一Key再利用 | IdempotencyService |
| 404 | ENTITY_NOT_FOUND | 対象がなく、ServiceがEntityNotFoundを送出する場合 | 共通Handler。Operationごとの到達は要確認 |
| 409 | PROJECT_ARCHIVED / RESOURCE_IMMUTABLE / EXECUTION_STATE_CONFLICT | 対象がARCHIVED/FIXEDまたは遷移不適格で該当DomainErrorを送出する場合 | 適用可能なOperationのみ、到達は要確認 |
| 403 | PROJECT_ACCESS_DENIED | Project membership/role不足のためClosure Serviceが拒否 | 共通Handler; gateway認証の保証ではない |

#### 根拠・未検証事項

- Router Source: `product_closure.py`（blob `7cae6a3df8725c3f5263ede17167225175f5968e`）。Request DTO: `WorkspaceAnnotationCreate`、Response Model: `未宣言`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.3 `PATCH /api/v1/projects/{project_id}/workspace-annotations/{annotation_id}`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-18-03` |
| Method / Path | `PATCH /api/v1/projects/{project_id}/workspace-annotations/{annotation_id}` |
| Handler | `product_closure.py::update_workspace_annotation` |
| Success Status | HTTP 200 |

#### Request

**Path parameters**

| 項目 | 型 | 必須 |
|---|---|---|
| `project_id` | string | 必須 |
| `annotation_id` | string | 必須 |

**Query parameters**

なし

**Headers**

| Header | 仕様 |
|---|---|
| `X-User-Id` | Sourceで参照。認証確立の証拠ではない |

**Request Body / Field定義**

Content-Type: `application/json`、型 `WorkspaceAnnotationUpdate`

| 項目（wire） | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `statement` | `str \| None` | 任意 | 許可 | lt=None, min_length=1, max_length=8000 |
| `rationale` | `str \| None` | 任意 | 許可 | lt=None, max_length=8000 |
| `assumptions` | `list[Any] \| None` | 任意 | 許可 | None |
| `limitations` | `list[Any] \| None` | 任意 | 許可 | None |
| `decision` | `Literal["SELECTED", "REJECTED", "DEFERRED"] \| None` | 任意 | 許可 | None |
| `next_actions` | `list[Any] \| None` | 任意 | 許可 | None |

**Request JSON例（schema由来の説明用）**

```json
{}
```

#### Response

- HTTP **200**。Body schema: Service output（response_model未宣言）。

Routerは`dict`を返すがPydantic response_model未宣言。Response Fieldの完全な型/キーは**未確定**。Service return値の追加照合が必要。


#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 対象がなく、ServiceがEntityNotFoundを送出する場合 | 共通Handler。Operationごとの到達は要確認 |
| 409 | PROJECT_ARCHIVED / RESOURCE_IMMUTABLE / EXECUTION_STATE_CONFLICT | 対象がARCHIVED/FIXEDまたは遷移不適格で該当DomainErrorを送出する場合 | 適用可能なOperationのみ、到達は要確認 |
| 403 | PROJECT_ACCESS_DENIED | Project membership/role不足のためClosure Serviceが拒否 | 共通Handler; gateway認証の保証ではない |

#### 根拠・未検証事項

- Router Source: `product_closure.py`（blob `7cae6a3df8725c3f5263ede17167225175f5968e`）。Request DTO: `WorkspaceAnnotationUpdate`、Response Model: `未宣言`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.4 `GET /api/v1/projects/{project_id}/artifacts/{artifact_id}`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-18-04` |
| Method / Path | `GET /api/v1/projects/{project_id}/artifacts/{artifact_id}` |
| Handler | `product_closure.py::artifact_metadata` |
| Success Status | HTTP 200 |

#### Request

**Path parameters**

| 項目 | 型 | 必須 |
|---|---|---|
| `project_id` | string | 必須 |
| `artifact_id` | string | 必須 |

**Query parameters**

なし

**Headers**

| Header | 仕様 |
|---|---|
| `X-User-Id` | Sourceで参照。認証確立の証拠ではない |

**Request Body / Field定義**

Request JSON Bodyなし（Router未定義）。

#### Response

- HTTP **200**。Body schema: Service output（response_model未宣言）。

Routerは`dict`を返すがPydantic response_model未宣言。Response Fieldの完全な型/キーは**未確定**。Service return値の追加照合が必要。


#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 対象がなく、ServiceがEntityNotFoundを送出する場合 | 共通Handler。Operationごとの到達は要確認 |
| 403 | PROJECT_ACCESS_DENIED | Project membership/role不足のためClosure Serviceが拒否 | 共通Handler; gateway認証の保証ではない |

#### 根拠・未検証事項

- Router Source: `product_closure.py`（blob `7cae6a3df8725c3f5263ede17167225175f5968e`）。Request DTO: `none`、Response Model: `未宣言`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.5 `GET /api/v1/projects/{project_id}/artifacts/{artifact_id}/download`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-18-05` |
| Method / Path | `GET /api/v1/projects/{project_id}/artifacts/{artifact_id}/download` |
| Handler | `product_closure.py::download_artifact` |
| Success Status | HTTP 200 |

#### Request

**Path parameters**

| 項目 | 型 | 必須 |
|---|---|---|
| `project_id` | string | 必須 |
| `artifact_id` | string | 必須 |

**Query parameters**

なし

**Headers**

| Header | 仕様 |
|---|---|
| `X-User-Id` | Sourceで参照。認証確立の証拠ではない |

**Request Body / Field定義**

Request JSON Bodyなし（Router未定義）。

#### Response

- HTTP **200**。Body schema: Binary（Download）。

HTTP Body: binary。Content-Type/Content-Disposition等はRouter内Response構築による。**JSON Bodyではない**。


#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 対象がなく、ServiceがEntityNotFoundを送出する場合 | 共通Handler。Operationごとの到達は要確認 |
| 403 | PROJECT_ACCESS_DENIED | Project membership/role不足のためClosure Serviceが拒否 | 共通Handler; gateway認証の保証ではない |

#### 根拠・未検証事項

- Router Source: `product_closure.py`（blob `7cae6a3df8725c3f5263ede17167225175f5968e`）。Request DTO: `none`、Response Model: `未宣言`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.6 `POST /api/v1/projects/{project_id}/exports`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-18-06` |
| Method / Path | `POST /api/v1/projects/{project_id}/exports` |
| Handler | `product_closure.py::create_export` |
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
| `Idempotency-Key` | IdempotencyService適用Commandなら非空必須 |
| `X-User-Id` | Sourceで参照。認証確立の証拠ではない |

**Request Body / Field定義**

Content-Type: `application/json`、型 `ExportCreate`

| 項目（wire） | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `result_ids` | `list[str]` | 必須 | 不可 | min_length=1, max_length=100 |

**Request JSON例（schema由来の説明用）**

```json
{
  "result_ids": []
}
```

#### Response

- HTTP **201**。Body schema: Service output（response_model未宣言）。

Routerは`dict`を返すがPydantic response_model未宣言。Response Fieldの完全な型/キーは**未確定**。Service return値の追加照合が必要。


#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗 | 共通Handler |
| 400/409 | IDEMPOTENCY_KEY_REQUIRED / IDEMPOTENCY_CONFLICT | Key欠落・異なる内容の同一Key再利用 | IdempotencyService |
| 404 | ENTITY_NOT_FOUND | 対象がなく、ServiceがEntityNotFoundを送出する場合 | 共通Handler。Operationごとの到達は要確認 |
| 409 | PROJECT_ARCHIVED / RESOURCE_IMMUTABLE / EXECUTION_STATE_CONFLICT | 対象がARCHIVED/FIXEDまたは遷移不適格で該当DomainErrorを送出する場合 | 適用可能なOperationのみ、到達は要確認 |
| 403 | PROJECT_ACCESS_DENIED | Project membership/role不足のためClosure Serviceが拒否 | 共通Handler; gateway認証の保証ではない |

#### 根拠・未検証事項

- Router Source: `product_closure.py`（blob `7cae6a3df8725c3f5263ede17167225175f5968e`）。Request DTO: `ExportCreate`、Response Model: `未宣言`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.7 `GET /api/v1/projects/{project_id}/exports/{export_id}`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-18-07` |
| Method / Path | `GET /api/v1/projects/{project_id}/exports/{export_id}` |
| Handler | `product_closure.py::get_export` |
| Success Status | HTTP 200 |

#### Request

**Path parameters**

| 項目 | 型 | 必須 |
|---|---|---|
| `project_id` | string | 必須 |
| `export_id` | string | 必須 |

**Query parameters**

なし

**Headers**

| Header | 仕様 |
|---|---|
| `X-User-Id` | Sourceで参照。認証確立の証拠ではない |

**Request Body / Field定義**

Request JSON Bodyなし（Router未定義）。

#### Response

- HTTP **200**。Body schema: Service output（response_model未宣言）。

Routerは`dict`を返すがPydantic response_model未宣言。Response Fieldの完全な型/キーは**未確定**。Service return値の追加照合が必要。


#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 対象がなく、ServiceがEntityNotFoundを送出する場合 | 共通Handler。Operationごとの到達は要確認 |
| 403 | PROJECT_ACCESS_DENIED | Project membership/role不足のためClosure Serviceが拒否 | 共通Handler; gateway認証の保証ではない |

#### 根拠・未検証事項

- Router Source: `product_closure.py`（blob `7cae6a3df8725c3f5263ede17167225175f5968e`）。Request DTO: `none`、Response Model: `未宣言`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.8 `GET /api/v1/projects/{project_id}/exports/{export_id}/download`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-18-08` |
| Method / Path | `GET /api/v1/projects/{project_id}/exports/{export_id}/download` |
| Handler | `product_closure.py::download_export` |
| Success Status | HTTP 200 |

#### Request

**Path parameters**

| 項目 | 型 | 必須 |
|---|---|---|
| `project_id` | string | 必須 |
| `export_id` | string | 必須 |

**Query parameters**

なし

**Headers**

| Header | 仕様 |
|---|---|
| `X-User-Id` | Sourceで参照。認証確立の証拠ではない |

**Request Body / Field定義**

Request JSON Bodyなし（Router未定義）。

#### Response

- HTTP **200**。Body schema: Binary（Download）。

HTTP Body: binary。Content-Type/Content-Disposition等はRouter内Response構築による。**JSON Bodyではない**。


#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 対象がなく、ServiceがEntityNotFoundを送出する場合 | 共通Handler。Operationごとの到達は要確認 |
| 403 | PROJECT_ACCESS_DENIED | Project membership/role不足のためClosure Serviceが拒否 | 共通Handler; gateway認証の保証ではない |

#### 根拠・未検証事項

- Router Source: `product_closure.py`（blob `7cae6a3df8725c3f5263ede17167225175f5968e`）。Request DTO: `none`、Response Model: `未宣言`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.9 `POST /api/v1/projects/{project_id}/annotations`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-18-09` |
| Method / Path | `POST /api/v1/projects/{project_id}/annotations` |
| Handler | `annotations.py::create_annotation` |
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
| `X-User-Id` | Sourceで参照。認証確立の証拠ではない |

**Request Body / Field定義**

Content-Type: `application/json`、型 `AnnotationCreate`

| 項目（wire） | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `target_result_id` | `str \| None` | 任意 | 許可 | None |
| `target_graph_version_id` | `str \| None` | 任意 | 許可 | None |
| `statement` | `str` | 必須 | 不可 | min_length=1, max_length=8000 |
| `rationale` | `str \| None` | 任意 | 許可 | None |
| `assumptions` | `list[Any]` | 任意 | 不可 | Field(default_factory=list) |
| `limitations` | `list[Any]` | 任意 | 不可 | Field(default_factory=list) |

**Request JSON例（schema由来の説明用）**

```json
{
  "statement": "string"
}
```

#### Response

- HTTP **201**。Body schema: `AnnotationResponse`。

| 項目（wire） | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `annotation_id` | `str` | 必須 | 不可 | — |
| `project_id` | `str` | 必須 | 不可 | — |
| `target_result_id` | `str \| None` | 必須 | 許可 | — |
| `target_graph_version_id` | `str \| None` | 必須 | 許可 | — |
| `statement` | `str` | 必須 | 不可 | — |
| `rationale` | `str \| None` | 必須 | 許可 | — |
| `assumptions` | `list[Any]` | 必須 | 不可 | — |
| `limitations` | `list[Any]` | 必須 | 不可 | — |
| `created_by` | `str` | 必須 | 不可 | — |
| `created_at` | `datetime \| None` | 必須 | 許可 | — |
| `updated_at` | `datetime \| None` | 必須 | 許可 | — |

**Response JSON構造例（schema由来の説明用）**

```json
{
  "annotation_id": "{annotation_id}",
  "project_id": "{project_id}",
  "target_result_id": "{target_result_id}",
  "target_graph_version_id": "{target_graph_version_id}",
  "statement": "string",
  "rationale": "string",
  "assumptions": [],
  "limitations": [],
  "created_by": "string",
  "created_at": "2026-11-17T00:00:00Z",
  "updated_at": "2026-11-17T00:00:00Z"
}
```

#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 対象がなく、ServiceがEntityNotFoundを送出する場合 | 共通Handler。Operationごとの到達は要確認 |
| 409 | PROJECT_ARCHIVED / RESOURCE_IMMUTABLE / EXECUTION_STATE_CONFLICT | 対象がARCHIVED/FIXEDまたは遷移不適格で該当DomainErrorを送出する場合 | 適用可能なOperationのみ、到達は要確認 |

#### 根拠・未検証事項

- Router Source: `annotations.py`（blob `93253262e3e4c99391280ffee7aedc4d022a6ed5`）。Request DTO: `AnnotationCreate`、Response Model: `AnnotationResponse`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.10 `GET /api/v1/annotations/{annotation_id}`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-18-10` |
| Method / Path | `GET /api/v1/annotations/{annotation_id}` |
| Handler | `annotations.py::get_annotation` |
| Success Status | HTTP 200 |

#### Request

**Path parameters**

| 項目 | 型 | 必須 |
|---|---|---|
| `annotation_id` | string | 必須 |

**Query parameters**

なし

**Headers**

Router固有の必須Header宣言なし

**Request Body / Field定義**

Request JSON Bodyなし（Router未定義）。

#### Response

- HTTP **200**。Body schema: `AnnotationResponse`。

| 項目（wire） | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `annotation_id` | `str` | 必須 | 不可 | — |
| `project_id` | `str` | 必須 | 不可 | — |
| `target_result_id` | `str \| None` | 必須 | 許可 | — |
| `target_graph_version_id` | `str \| None` | 必須 | 許可 | — |
| `statement` | `str` | 必須 | 不可 | — |
| `rationale` | `str \| None` | 必須 | 許可 | — |
| `assumptions` | `list[Any]` | 必須 | 不可 | — |
| `limitations` | `list[Any]` | 必須 | 不可 | — |
| `created_by` | `str` | 必須 | 不可 | — |
| `created_at` | `datetime \| None` | 必須 | 許可 | — |
| `updated_at` | `datetime \| None` | 必須 | 許可 | — |

**Response JSON構造例（schema由来の説明用）**

```json
{
  "annotation_id": "{annotation_id}",
  "project_id": "{project_id}",
  "target_result_id": "{target_result_id}",
  "target_graph_version_id": "{target_graph_version_id}",
  "statement": "string",
  "rationale": "string",
  "assumptions": [],
  "limitations": [],
  "created_by": "string",
  "created_at": "2026-11-17T00:00:00Z",
  "updated_at": "2026-11-17T00:00:00Z"
}
```

#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 対象がなく、ServiceがEntityNotFoundを送出する場合 | 共通Handler。Operationごとの到達は要確認 |

#### 根拠・未検証事項

- Router Source: `annotations.py`（blob `93253262e3e4c99391280ffee7aedc4d022a6ed5`）。Request DTO: `none`、Response Model: `AnnotationResponse`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.11 `PATCH /api/v1/annotations/{annotation_id}`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-18-11` |
| Method / Path | `PATCH /api/v1/annotations/{annotation_id}` |
| Handler | `annotations.py::update_annotation` |
| Success Status | HTTP 200 |

#### Request

**Path parameters**

| 項目 | 型 | 必須 |
|---|---|---|
| `annotation_id` | string | 必須 |

**Query parameters**

なし

**Headers**

Router固有の必須Header宣言なし

**Request Body / Field定義**

Content-Type: `application/json`、型 `AnnotationUpdate`

| 項目（wire） | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `statement` | `str \| None` | 任意 | 許可 | lt=None, min_length=1, max_length=8000 |
| `rationale` | `str \| None` | 任意 | 許可 | None |
| `assumptions` | `list[Any] \| None` | 任意 | 許可 | None |
| `limitations` | `list[Any] \| None` | 任意 | 許可 | None |

**Request JSON例（schema由来の説明用）**

```json
{}
```

#### Response

- HTTP **200**。Body schema: `AnnotationResponse`。

| 項目（wire） | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `annotation_id` | `str` | 必須 | 不可 | — |
| `project_id` | `str` | 必須 | 不可 | — |
| `target_result_id` | `str \| None` | 必須 | 許可 | — |
| `target_graph_version_id` | `str \| None` | 必須 | 許可 | — |
| `statement` | `str` | 必須 | 不可 | — |
| `rationale` | `str \| None` | 必須 | 許可 | — |
| `assumptions` | `list[Any]` | 必須 | 不可 | — |
| `limitations` | `list[Any]` | 必須 | 不可 | — |
| `created_by` | `str` | 必須 | 不可 | — |
| `created_at` | `datetime \| None` | 必須 | 許可 | — |
| `updated_at` | `datetime \| None` | 必須 | 許可 | — |

**Response JSON構造例（schema由来の説明用）**

```json
{
  "annotation_id": "{annotation_id}",
  "project_id": "{project_id}",
  "target_result_id": "{target_result_id}",
  "target_graph_version_id": "{target_graph_version_id}",
  "statement": "string",
  "rationale": "string",
  "assumptions": [],
  "limitations": [],
  "created_by": "string",
  "created_at": "2026-11-17T00:00:00Z",
  "updated_at": "2026-11-17T00:00:00Z"
}
```

#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 対象がなく、ServiceがEntityNotFoundを送出する場合 | 共通Handler。Operationごとの到達は要確認 |
| 409 | PROJECT_ARCHIVED / RESOURCE_IMMUTABLE / EXECUTION_STATE_CONFLICT | 対象がARCHIVED/FIXEDまたは遷移不適格で該当DomainErrorを送出する場合 | 適用可能なOperationのみ、到達は要確認 |

#### 根拠・未検証事項

- Router Source: `annotations.py`（blob `93253262e3e4c99391280ffee7aedc4d022a6ed5`）。Request DTO: `AnnotationUpdate`、Response Model: `AnnotationResponse`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.12 `GET /api/v1/artifacts/{artifact_id}`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-18-12` |
| Method / Path | `GET /api/v1/artifacts/{artifact_id}` |
| Handler | `artifacts.py::get_artifact` |
| Success Status | HTTP 200 |

#### Request

**Path parameters**

| 項目 | 型 | 必須 |
|---|---|---|
| `artifact_id` | string | 必須 |

**Query parameters**

なし

**Headers**

Router固有の必須Header宣言なし

**Request Body / Field定義**

Request JSON Bodyなし（Router未定義）。

#### Response

- HTTP **200**。Body schema: `ArtifactResponse`。

| 項目（wire） | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `artifact_id` | `str` | 必須 | 不可 | — |
| `project_id` | `str` | 必須 | 不可 | — |
| `execution_id` | `str \| None` | 必須 | 許可 | — |
| `result_id` | `str \| None` | 必須 | 許可 | — |
| `artifact_type` | `str` | 必須 | 不可 | — |
| `object_key` | `str` | 必須 | 不可 | — |
| `content_hash` | `str` | 必須 | 不可 | — |
| `media_type` | `str` | 必須 | 不可 | — |
| `size_bytes` | `int` | 必須 | 不可 | — |
| `metadata` | `dict[str, Any]` | 必須 | 不可 | — |
| `created_at` | `datetime \| None` | 必須 | 許可 | — |

**Response JSON構造例（schema由来の説明用）**

```json
{
  "artifact_id": "{artifact_id}",
  "project_id": "{project_id}",
  "execution_id": "{execution_id}",
  "result_id": "{result_id}",
  "artifact_type": "string",
  "object_key": "string",
  "content_hash": "string",
  "media_type": "string",
  "size_bytes": 0,
  "metadata": {},
  "created_at": "2026-11-17T00:00:00Z"
}
```

#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 対象がなく、ServiceがEntityNotFoundを送出する場合 | 共通Handler。Operationごとの到達は要確認 |
| 500 | ARTIFACT_HASH_MISMATCH | Artifact download/読み取りでHash不一致が伝播する場合 | 該当Output経路のみ |

#### 根拠・未検証事項

- Router Source: `artifacts.py`（blob `680b666cd484a08cdc3d764f7829d536cd0e496c`）。Request DTO: `none`、Response Model: `ArtifactResponse`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.13 `GET /api/v1/artifacts/{artifact_id}/download`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-18-13` |
| Method / Path | `GET /api/v1/artifacts/{artifact_id}/download` |
| Handler | `artifacts.py::download_artifact` |
| Success Status | HTTP 200 |

#### Request

**Path parameters**

| 項目 | 型 | 必須 |
|---|---|---|
| `artifact_id` | string | 必須 |

**Query parameters**

なし

**Headers**

Router固有の必須Header宣言なし

**Request Body / Field定義**

Request JSON Bodyなし（Router未定義）。

#### Response

- HTTP **200**。Body schema: Binary（Download）。

HTTP Body: binary。Content-Type/Content-Disposition等はRouter内Response構築による。**JSON Bodyではない**。


#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 対象がなく、ServiceがEntityNotFoundを送出する場合 | 共通Handler。Operationごとの到達は要確認 |
| 500 | ARTIFACT_HASH_MISMATCH | Artifact download/読み取りでHash不一致が伝播する場合 | 該当Output経路のみ |

#### 根拠・未検証事項

- Router Source: `artifacts.py`（blob `680b666cd484a08cdc3d764f7829d536cd0e496c`）。Request DTO: `none`、Response Model: `未宣言`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

## 5. 検証状況

- Route/Method/Path: 13 件 Source確認。
- Request: Router/Pydanticモデルの静的制約を反映。Response: 型付きモデルは全Fieldを表記。Service無型応答は一部未確定。
- HTTP Contract Test: NOT_RUN。Endpoint詳細の完全性・認可・実行時エラー網羅は未検証。
- 元の`docs/wiki/requirement_definition/`への昇格: NOT_DONE。

## 6. 既存Domain・設計制約（旧仕様本文から保持）

以下は既存のDomain規範・補足情報を保持したもの。重複する旧Route一覧より§2（Source基準）を優先する。改訂前の原本文はGit Blob `c4f50c46bc3025a9e94a724f5f23a1a9d6279e8d`で追跡可能。

### Annotation / Artifact API

#### Canonical/simple Annotation

Current routes:

| Method | Path | 用途 |
| --- | --- | --- |
| POST | `/projects/{project_id}/annotations` | ResultまたはGraphVersion向けAnnotation作成 |
| GET | `/annotations/{annotation_id}` | 取得 |
| PATCH | `/annotations/{annotation_id}` | 更新 |

Response field:

```text
annotation_id
project_id
target_result_id
target_graph_version_id
statement
rationale
assumptions
limitations
created_by
created_at
updated_at
```

exactly one target constraintを持つ。

#### WorkspaceAnnotation

Product Closureには別のProject-scoped annotation APIがある。

| Method | Path | 用途 |
| --- | --- | --- |
| GET | `/projects/{project_id}/workspace-annotations` | list/filter |
| POST | `/projects/{project_id}/workspace-annotations` | create |
| PATCH | `/projects/{project_id}/workspace-annotations/{annotation_id}` | update |

Allowed target:

```text
Project
ResearchContextVersion
AnalysisView
AnalysisSpecification
Execution
Result
GraphVersion
```

追加fieldとして`decision: SELECTED / REJECTED / DEFERRED / null`、`next_actions`を扱い、persistenceではrevision historyも保持する。

#### Canonical Artifact

Current unscoped-by-project routes:

| Method | Path | 用途 |
| --- | --- | --- |
| GET | `/artifacts/{artifact_id}` | metadata |
| GET | `/artifacts/{artifact_id}/download` | SHA-256検証済みdownload |

Metadata response:

```text
artifact_id
project_id
execution_id
result_id
artifact_type
object_key
content_hash
media_type
size_bytes
metadata
created_at
```

Canonical persistenceにはさらに`stage_execution_id / artifact_scope`が存在するが、current `ArtifactResponse`では公開していない。

Project Closureにも`GET /projects/{project_id}/artifacts/{artifact_id}`および`.../download`があり、membership / Project境界を付加して同じartifact contentを扱う。

Current contractではunscoped legacy routeもArtifactからProjectをresolveして同じmembership authorizationを適用する。Explicit sensitive Artifact/output detailはOWNER/EDITORのみ。

Canonical `ArtifactType`はfixed enumであり、Predictive関連では`PARTITION_INDEX / FITTED_PREPROCESSOR / FITTED_MODEL / PREDICTION / PREDICTIVE_EXPLANATION / MODEL_CARD`等を含む。

#### Findings / Model Management

`Findings`はcanonical Result、simple AnnotationまたはWorkspaceAnnotation、Artifact、Lineage projectionを組み合わせて構成する。decision/next actionが必要な場合はWorkspaceAnnotationの既存責務を利用する。

`Model Management`は`TRAINING_RESULT / EVALUATION_RESULT / MODEL_CARD_RESULT`と`FITTED_PREPROCESSOR / FITTED_MODEL / MODEL_CARD`等をreadするsurfaceとして構成できる。ENH-E10ではmodel/task/effective parameters、provider/library version、seed/determinism、feature/preprocessor identity、fitted-model schema/artifact identity、explanation method metadata、lineage/runtime provenanceを同じread surfaceから提示する。

これらのNavigation Stageのために重複Result/Annotation/Artifact Resourceを新設しない。

**当該Interfaceの追加契約（関連Requirement）**

- **`FR-124a`**：Artifact metadata/downloadでProject境界とsafe content dispositionを検証するcurrent contractを維持する
- **`FR-124b`**：legacy/generic routeを含むArtifact downloadでProjectMembership authorizationを一貫適用する
- **`AR-020`**：prediction row / local explanationをpotentially sensitive outputとして扱い、Project roleに応じてdetail exposureを制御する

## 7. 改訂記録

- 2026-11-17: 全23_10〜23_19共通フォーマットへ再構成。Request/Response/ErrorsをOperation別に記載し、Source確認と未検証を分離。
