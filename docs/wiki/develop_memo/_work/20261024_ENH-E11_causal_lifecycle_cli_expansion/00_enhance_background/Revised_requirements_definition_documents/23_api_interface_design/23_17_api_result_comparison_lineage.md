# 23_17_api_result_comparison_lineage — Result / Comparison / Lineage Web API仕様

## 1. API概要

- 対象: Result / Comparison / Lineage のHTTP契約。
- Base path: `/api/v1`。
- 本改訂はOwner採用の**Operation単位Request/Response/Errors定義**を対象とする。実行時PASSや要件変更を含まない。
- Source snapshot: `2068b3b2f8c096d581a0f2d56047c4185c5ac7cc`。CURRENTと未検証事項を分離する。

## 2. エンドポイント一覧

| No. | HTTP | Path | Handler | HTTP Success |
|---:|---|---|---|---|
| 1 | `GET` | `/api/v1/executions/{execution_id}/results` | `list_results_by_execution` | `200` |
| 2 | `GET` | `/api/v1/results/{result_id}` | `get_result` | `200` |
| 3 | `POST` | `/api/v1/comparisons/query` | `query_comparison` | `200` |
| 4 | `GET` | `/api/v1/results/{result_id}/lineage` | `get_lineage` | `200` |
| 5 | `POST` | `/api/v1/results/{result_id}/export` | `export_result` | `200` |
| 6 | `GET` | `/api/v1/projects/{project_id}/results` | `list_results` | `200` |
| 7 | `GET` | `/api/v1/projects/{project_id}/results/summary` | `results_summary` | `200` |
| 8 | `GET` | `/api/v1/projects/{project_id}/results/{result_id}` | `result_detail` | `200` |
| 9 | `POST` | `/api/v1/projects/{project_id}/comparisons` | `create_comparison` | `201` |
| 10 | `GET` | `/api/v1/projects/{project_id}/results/{result_id}/lineage` | `result_lineage` | `200` |
| 11 | `GET` | `/api/v1/projects/{project_id}/lineage` | `project_lineage` | `200` |
| 12 | `POST` | `/api/v1/projects/{project_id}/lineage-links` | `create_lineage_link` | `201` |

## 3. 共通Error Response形式

CURRENTのDomainError/RequestValidationError Handlerは`application/problem+json`ではなく、以下のJSON envelope。

```json
{"error":{"code":"INVALID_REQUEST","message":"Request validation failed.","details":{},"request_id":"{request_id}"}}
```

共通Handlerに定義されたErrorがすべてのOperationから発生するとは限らない。下表の条件付きErrorはテストPASS済みという意味ではない。

## 4. エンドポイント詳細

### 4.1 `GET /api/v1/executions/{execution_id}/results`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-17-01` |
| Method / Path | `GET /api/v1/executions/{execution_id}/results` |
| Handler | `results.py::list_results_by_execution` |
| Success Status | HTTP 200 |

#### Request

**Path parameters**

| 項目 | 型 | 必須 |
|---|---|---|
| `execution_id` | string | 必須 |

**Query parameters**

なし

**Headers**

Router固有の必須Header宣言なし

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
| 500 | ARTIFACT_HASH_MISMATCH | Artifact download/読み取りでHash不一致が伝播する場合 | 該当Output経路のみ |

#### 根拠・未検証事項

- Router Source: `results.py`（blob `e565edb21051133b84fb77fd7c1eafcd2d7257ea`）。Request DTO: `none`、Response Model: `ResultListResponse`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.2 `GET /api/v1/results/{result_id}`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-17-02` |
| Method / Path | `GET /api/v1/results/{result_id}` |
| Handler | `results.py::get_result` |
| Success Status | HTTP 200 |

#### Request

**Path parameters**

| 項目 | 型 | 必須 |
|---|---|---|
| `result_id` | string | 必須 |

**Query parameters**

なし

**Headers**

Router固有の必須Header宣言なし

**Request Body / Field定義**

Request JSON Bodyなし（Router未定義）。

#### Response

- HTTP **200**。Body schema: `ResultResponse`。

| 項目 | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `result_id` | `str` | 必須 | 不可 | — |
| `execution_id` | `str` | 必須 | 不可 | — |
| `result_type` | `str` | 必須 | 不可 | — |
| `scientific_status` | `str` | 必須 | 不可 | — |
| `summary` | `dict[str, Any]` | 必須 | 不可 | — |
| `payload` | `dict[str, Any]` | 必須 | 不可 | — |
| `diagnostics` | `dict[str, Any]` | 必須 | 不可 | — |
| `warnings` | `list[Any]` | 必須 | 不可 | — |
| `artifact_ids` | `list[str]` | 任意 | 不可 | Field(default_factory=list) |
| `created_at` | `datetime \| None` | 必須 | 許可 | — |

**Response JSON構造例（説明用）**

```json
{
  "result_id": "{result_id}",
  "execution_id": "{execution_id}",
  "result_type": "string",
  "scientific_status": "string",
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
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 対象がなく、ServiceがEntityNotFoundを送出する場合 | 共通Handler。Operationごとの到達は要確認 |
| 500 | ARTIFACT_HASH_MISMATCH | Artifact download/読み取りでHash不一致が伝播する場合 | 該当Output経路のみ |

#### 根拠・未検証事項

- Router Source: `results.py`（blob `e565edb21051133b84fb77fd7c1eafcd2d7257ea`）。Request DTO: `none`、Response Model: `ResultResponse`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.3 `POST /api/v1/comparisons/query`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-17-03` |
| Method / Path | `POST /api/v1/comparisons/query` |
| Handler | `results.py::query_comparison` |
| Success Status | HTTP 200 |

#### Request

**Path parameters**

なし

**Query parameters**

なし

**Headers**

Router固有の必須Header宣言なし

**Request Body / Field定義**

Content-Type: `application/json`、型 `ComparisonQueryRequest`

| 項目 | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `project_id` | `str` | 必須 | 不可 | — |
| `result_ids` | `list[str]` | 必須 | 不可 | min_length=2, max_length=20 |

**Request JSON例（説明用）**

```json
{
  "project_id": "{project_id}",
  "result_ids": []
}
```

#### Response

- HTTP **200**。Body schema: `ComparisonResponse`。

| 項目 | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `operation` | `str` | 必須 | 不可 | — |
| `common_conditions` | `dict[str, Any]` | 必須 | 不可 | — |
| `changed_conditions` | `list[dict[str, Any]]` | 必須 | 不可 | — |
| `result_differences` | `list[dict[str, Any]]` | 必須 | 不可 | — |
| `warnings` | `list[str]` | 必須 | 不可 | — |
| `lineage_summary` | `dict[str, Any]` | 必須 | 不可 | — |

**Response JSON構造例（説明用）**

```json
{
  "operation": "string",
  "common_conditions": {},
  "changed_conditions": [],
  "result_differences": [],
  "warnings": [],
  "lineage_summary": {}
}
```

#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗 | 共通Handler |
| 409 | PROJECT_ARCHIVED / RESOURCE_IMMUTABLE / EXECUTION_STATE_CONFLICT | 対象がARCHIVED/FIXEDまたは遷移不適格で該当DomainErrorを送出する場合 | 適用可能なOperationのみ、到達は要確認 |
| 500 | ARTIFACT_HASH_MISMATCH | Artifact download/読み取りでHash不一致が伝播する場合 | 該当Output経路のみ |

#### 根拠・未検証事項

- Router Source: `results.py`（blob `e565edb21051133b84fb77fd7c1eafcd2d7257ea`）。Request DTO: `ComparisonQueryRequest`、Response Model: `ComparisonResponse`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.4 `GET /api/v1/results/{result_id}/lineage`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-17-04` |
| Method / Path | `GET /api/v1/results/{result_id}/lineage` |
| Handler | `results.py::get_lineage` |
| Success Status | HTTP 200 |

#### Request

**Path parameters**

| 項目 | 型 | 必須 |
|---|---|---|
| `result_id` | string | 必須 |

**Query parameters**

なし

**Headers**

Router固有の必須Header宣言なし

**Request Body / Field定義**

Request JSON Bodyなし（Router未定義）。

#### Response

- HTTP **200**。Body schema: `LineageResponse`。

| 項目 | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `root_result_id` | `str` | 必須 | 不可 | — |
| `nodes` | `list[LineageNodeResponse]` | 必須 | 不可 | — |
| `edges` | `list[LineageEdgeResponse]` | 必須 | 不可 | — |

**Response JSON構造例（説明用）**

```json
{
  "root_result_id": "{root_result_id}",
  "nodes": [],
  "edges": []
}
```

#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 対象がなく、ServiceがEntityNotFoundを送出する場合 | 共通Handler。Operationごとの到達は要確認 |
| 500 | ARTIFACT_HASH_MISMATCH | Artifact download/読み取りでHash不一致が伝播する場合 | 該当Output経路のみ |

#### 根拠・未検証事項

- Router Source: `results.py`（blob `e565edb21051133b84fb77fd7c1eafcd2d7257ea`）。Request DTO: `none`、Response Model: `LineageResponse`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.5 `POST /api/v1/results/{result_id}/export`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-17-05` |
| Method / Path | `POST /api/v1/results/{result_id}/export` |
| Handler | `results.py::export_result` |
| Success Status | HTTP 200 |

#### Request

**Path parameters**

| 項目 | 型 | 必須 |
|---|---|---|
| `result_id` | string | 必須 |

**Query parameters**

なし

**Headers**

| Header | 仕様 |
|---|---|
| `Idempotency-Key` | IdempotencyService適用Commandなら非空必須 |

**Request Body / Field定義**

Request JSON Bodyなし（Router未定義）。

#### Response

- HTTP **200**。Body schema: Service output（response_model未宣言）。

Routerは`dict`を返すがPydantic response_model未宣言。Response Fieldの完全な型/キーは**未確定**。Service return値の追加照合が必要。


#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗 | 共通Handler |
| 400/409 | IDEMPOTENCY_KEY_REQUIRED / IDEMPOTENCY_CONFLICT | Key欠落・異なる内容の同一Key再利用 | IdempotencyService |
| 404 | ENTITY_NOT_FOUND | 対象がなく、ServiceがEntityNotFoundを送出する場合 | 共通Handler。Operationごとの到達は要確認 |
| 409 | PROJECT_ARCHIVED / RESOURCE_IMMUTABLE / EXECUTION_STATE_CONFLICT | 対象がARCHIVED/FIXEDまたは遷移不適格で該当DomainErrorを送出する場合 | 適用可能なOperationのみ、到達は要確認 |
| 500 | ARTIFACT_HASH_MISMATCH | Artifact download/読み取りでHash不一致が伝播する場合 | 該当Output経路のみ |

#### 根拠・未検証事項

- Router Source: `results.py`（blob `e565edb21051133b84fb77fd7c1eafcd2d7257ea`）。Request DTO: `none`、Response Model: `未宣言`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.6 `GET /api/v1/projects/{project_id}/results`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-17-06` |
| Method / Path | `GET /api/v1/projects/{project_id}/results` |
| Handler | `product_closure.py::list_results` |
| Success Status | HTTP 200 |

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

### 4.7 `GET /api/v1/projects/{project_id}/results/summary`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-17-07` |
| Method / Path | `GET /api/v1/projects/{project_id}/results/summary` |
| Handler | `product_closure.py::results_summary` |
| Success Status | HTTP 200 |

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

Request JSON Bodyなし（Router未定義）。

#### Response

- HTTP **200**。Body schema: JSON object（Router/Serviceのdict）。

| 項目 | 意味・型 |
|---|---|
| `schema_version` | Source返却キー（値の詳細型はService/Schema依存） |
| `project_id` | Source返却キー（値の詳細型はService/Schema依存） |
| `result_count` | Source返却キー（値の詳細型はService/Schema依存） |
| `by_family` | Source返却キー（値の詳細型はService/Schema依存） |
| `by_analytical_status` | Source返却キー（値の詳細型はService/Schema依存） |
| `by_result_type` | Source返却キー（値の詳細型はService/Schema依存） |
| `ranking` | Source返却キー（値の詳細型はService/Schema依存） |
| `warning` | Source返却キー（値の詳細型はService/Schema依存） |


#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 対象がなく、ServiceがEntityNotFoundを送出する場合 | 共通Handler。Operationごとの到達は要確認 |
| 403 | PROJECT_ACCESS_DENIED | Project membership/role不足のためClosure Serviceが拒否 | 共通Handler; gateway認証の保証ではない |

#### 根拠・未検証事項

- Router Source: `product_closure.py`（blob `7cae6a3df8725c3f5263ede17167225175f5968e`）。Request DTO: `none`、Response Model: `未宣言`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.8 `GET /api/v1/projects/{project_id}/results/{result_id}`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-17-08` |
| Method / Path | `GET /api/v1/projects/{project_id}/results/{result_id}` |
| Handler | `product_closure.py::result_detail` |
| Success Status | HTTP 200 |

#### Request

**Path parameters**

| 項目 | 型 | 必須 |
|---|---|---|
| `project_id` | string | 必須 |
| `result_id` | string | 必須 |

**Query parameters**

| 項目 | 型 | default |
|---|---|---|
| `include_sensitive` | `bool` | `Query(default=False)` |

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

### 4.9 `POST /api/v1/projects/{project_id}/comparisons`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-17-09` |
| Method / Path | `POST /api/v1/projects/{project_id}/comparisons` |
| Handler | `product_closure.py::create_comparison` |
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

Content-Type: `application/json`、型 `ComparisonCreate`

| 項目 | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `result_ids` | `list[str]` | 必須 | 不可 | min_length=2, max_length=20 |

**Request JSON例（説明用）**

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
| 404 | ENTITY_NOT_FOUND | 対象がなく、ServiceがEntityNotFoundを送出する場合 | 共通Handler。Operationごとの到達は要確認 |
| 409 | PROJECT_ARCHIVED / RESOURCE_IMMUTABLE / EXECUTION_STATE_CONFLICT | 対象がARCHIVED/FIXEDまたは遷移不適格で該当DomainErrorを送出する場合 | 適用可能なOperationのみ、到達は要確認 |
| 403 | PROJECT_ACCESS_DENIED | Project membership/role不足のためClosure Serviceが拒否 | 共通Handler; gateway認証の保証ではない |

#### 根拠・未検証事項

- Router Source: `product_closure.py`（blob `7cae6a3df8725c3f5263ede17167225175f5968e`）。Request DTO: `ComparisonCreate`、Response Model: `未宣言`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.10 `GET /api/v1/projects/{project_id}/results/{result_id}/lineage`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-17-10` |
| Method / Path | `GET /api/v1/projects/{project_id}/results/{result_id}/lineage` |
| Handler | `product_closure.py::result_lineage` |
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

| Header | 仕様 |
|---|---|
| `X-User-Id` | Sourceで参照。認証確立の証拠ではない |

**Request Body / Field定義**

Request JSON Bodyなし（Router未定義）。

#### Response

- HTTP **200**。Body schema: JSON object（Router/Serviceのdict）。

| 項目 | 意味・型 |
|---|---|
| `root_result_id` | Source返却キー（値の詳細型はService/Schema依存） |
| `nodes` | Source返却キー（値の詳細型はService/Schema依存） |
| `edges` | Source返却キー（値の詳細型はService/Schema依存） |


#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 対象がなく、ServiceがEntityNotFoundを送出する場合 | 共通Handler。Operationごとの到達は要確認 |
| 403 | PROJECT_ACCESS_DENIED | Project membership/role不足のためClosure Serviceが拒否 | 共通Handler; gateway認証の保証ではない |

#### 根拠・未検証事項

- Router Source: `product_closure.py`（blob `7cae6a3df8725c3f5263ede17167225175f5968e`）。Request DTO: `none`、Response Model: `未宣言`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.11 `GET /api/v1/projects/{project_id}/lineage`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-17-11` |
| Method / Path | `GET /api/v1/projects/{project_id}/lineage` |
| Handler | `product_closure.py::project_lineage` |
| Success Status | HTTP 200 |

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

Request JSON Bodyなし（Router未定義）。

#### Response

- HTTP **200**。Body schema: JSON object（Router/Serviceのdict）。

| 項目 | 意味・型 |
|---|---|
| `schema_version` | Source返却キー（値の詳細型はService/Schema依存） |
| `project_id` | Source返却キー（値の詳細型はService/Schema依存） |
| `nodes` | Source返却キー（値の詳細型はService/Schema依存） |
| `edges` | Source返却キー（値の詳細型はService/Schema依存） |


#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 対象がなく、ServiceがEntityNotFoundを送出する場合 | 共通Handler。Operationごとの到達は要確認 |
| 403 | PROJECT_ACCESS_DENIED | Project membership/role不足のためClosure Serviceが拒否 | 共通Handler; gateway認証の保証ではない |

#### 根拠・未検証事項

- Router Source: `product_closure.py`（blob `7cae6a3df8725c3f5263ede17167225175f5968e`）。Request DTO: `none`、Response Model: `未宣言`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.12 `POST /api/v1/projects/{project_id}/lineage-links`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-17-12` |
| Method / Path | `POST /api/v1/projects/{project_id}/lineage-links` |
| Handler | `product_closure.py::create_lineage_link` |
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

Content-Type: `application/json`、型 `LineageLinkCreate`

| 項目 | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `source_type` | `str` | 必須 | 不可 | min_length=1, max_length=100 |
| `source_id` | `str` | 必須 | 不可 | min_length=1, max_length=100 |
| `relation_type` | `Literal[` | 必須 | 不可 | — |
| `target_type` | `str` | 必須 | 不可 | min_length=1, max_length=100 |
| `target_id` | `str` | 必須 | 不可 | min_length=1, max_length=100 |
| `evidence` | `dict[str, Any]` | 任意 | 不可 | Field(default_factory=dict) |

**Request JSON例（説明用）**

```json
{
  "source_type": "string",
  "source_id": "{source_id}",
  "relation_type": "ENUM",
  "target_type": "string",
  "target_id": "{target_id}"
}
```

#### Response

- HTTP **201**。Body schema: Service output（response_model未宣言）。

Routerは`dict`を返すがPydantic response_model未宣言。Response Fieldの完全な型/キーは**未確定**。Service return値の追加照合が必要。


#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 対象がなく、ServiceがEntityNotFoundを送出する場合 | 共通Handler。Operationごとの到達は要確認 |
| 409 | PROJECT_ARCHIVED / RESOURCE_IMMUTABLE / EXECUTION_STATE_CONFLICT | 対象がARCHIVED/FIXEDまたは遷移不適格で該当DomainErrorを送出する場合 | 適用可能なOperationのみ、到達は要確認 |
| 403 | PROJECT_ACCESS_DENIED | Project membership/role不足のためClosure Serviceが拒否 | 共通Handler; gateway認証の保証ではない |

#### 根拠・未検証事項

- Router Source: `product_closure.py`（blob `7cae6a3df8725c3f5263ede17167225175f5968e`）。Request DTO: `LineageLinkCreate`、Response Model: `未宣言`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

## 5. 検証状況

- Route/Method/Path: 12 件 Source確認。
- Request: Router/Pydanticモデルの静的制約を反映。Response: 型付きモデルは全Fieldを表記。Service無型応答は一部未確定。
- HTTP Contract Test: NOT_RUN。Endpoint詳細の完全性・認可・実行時エラー網羅は未検証。
- 元の`docs/wiki/requirement_definition/`への昇格: NOT_DONE。

## 6. 既存Domain・設計制約（旧仕様本文から保持）

以下は既存のDomain規範・補足情報を保持したもの。重複する旧Route一覧より§2（Source基準）を優先する。改訂前の原本文はGit Blob `88e30c42c750a6bd0f6def2e7fc3470826af20a8`で追跡可能。

### Result / Comparison / Lineage API

#### Canonical Result API

Current canonical routes:

| Method | Path | 用途 |
| --- | --- | --- |
| GET | `/executions/{execution_id}/results` | canonical Result一覧 |
| GET | `/results/{result_id}` | canonical Result取得 |
| POST | `/comparisons/query` | canonical Result比較 |
| GET | `/results/{result_id}/lineage` | Result起点lineage projection |
| POST | `/results/{result_id}/export` | Result export projection |

Canonical Result response:

```text
result_id
execution_id
result_type
scientific_status
summary
payload
diagnostics
warnings
artifact_ids
created_at
```

Canonical responseには`project_id / analysis_family / schema_version / analytical_status`を直接持たない。

#### Project-scoped Product Closure

Current Project Closure routes:

| Method | Path | 用途 |
| --- | --- | --- |
| GET | `/projects/{project_id}/results` | Project result list |
| GET | `/projects/{project_id}/results/summary` | Project result summary |
| GET | `/projects/{project_id}/results/{result_id}` | Project boundary / membership付きresult detail |
| POST | `/projects/{project_id}/comparisons` | Project-scoped comparison |
| GET | `/projects/{project_id}/results/{result_id}/lineage` | Project-scoped result lineage |
| GET | `/projects/{project_id}/lineage` | Project lineage |
| POST | `/projects/{project_id}/lineage-links` | manual generic lineage link |
| POST | `/projects/{project_id}/exports` | Result集合export |
| GET | `/projects/{project_id}/exports/{export_id}` | Export metadata |
| GET | `/projects/{project_id}/exports/{export_id}/download` | Export download |

`POST /results/{result_id}/export`とProject-scoped`/exports`はcurrent branchで併存する別interfaceである。

#### Comparison semantics

Canonical `POST /comparisons/query`は最低2 Resultを受ける。Different Project、different Family/Result category等request shape自体が無効な場合はvalidation errorとする。意味上の比較可能性は`semantic_compatible`と`direct_metric_comparable`の二段階で返す。返却projection:

```text
operation
common_conditions
changed_conditions
result_differences
warnings
lineage_summary
```

Cross-familyで意味の異なるResultを単一`score`へ平坦化しない。

Current comparability responseには最低限次を追加する。

```json
{
  "semantic_compatible": true,
  "direct_metric_comparable": false,
  "compatibility_reasons": [],
  "direct_comparison_blockers": ["TEST_ROW_IDENTITY_MISMATCH"]
}
```

Predictive semantic keyは`task_type / target(outcome) / prediction_unit / prediction_time / horizon / deployment/evaluation population semantics`。Direct metric comparisonはさらにsame `dataset_version_id`、same TEST-row identity/hash、same metric definitionを要求する。

Causal semantic keyは`treatment/exposure / outcome / estimand / target population`。Direct comparisonはsame data/view/analysis populationを要求する。

semantic mismatchではHTTP successのまま`semantic_compatible=false`とreasonを返し、quantitative delta/rankを生成しない。

#### Lineage relationの二層

Result lineage projectionはtyped relationを表示用に次のような名称へmappingする。

```text
Project -> Execution: CONTEXT_FOR
Artifact -> DatasetVersion: SOURCE_OF
DatasetVersion -> Execution: INPUT_TO
Execution -> Result: GENERATED
Result -> GraphVersion: SOURCE_OF
GraphVersion -> Execution: INPUT_TO
Result -> Artifact: HAS_ARTIFACT
Result -> Annotation: HAS_ANNOTATION
GraphVersion -> Annotation: HAS_ANNOTATION
Execution -> Execution: REVISED_FROM
fallback: RELATED_TO
```

一方、manual generic lineage link APIが受け付けるrelationは次のsubsetである。

```text
USED_INPUT
GENERATED
DERIVED_FROM
REVISED_FROM
SUPPORTED_BY
MOTIVATED
SELECTED
REJECTED
```

projection relation名とgeneric authoritative write relationを混同しない。Navigation Stageをいずれのlineage identityにも追加しない。

Current canonical lineage read responseは`ResearchContextVersion -> AnalysisSpecification -> ExecutionPlan -> Execution -> StageExecution -> Result -> Artifact`を再構成し、DatasetVersion / AnalysisView / GraphVersion / input Result / base Executionを含める。deterministic structural relationをmanual/generic LineageEdgeとして二重writeしない。

**当該Interfaceの追加契約（関連Requirement）**

- **`FR-090`**：canonical Resultはexecution/stage relation、result type、scientific status、summary/payload/diagnostics/warningsを保持する。family/generic schema_versionをResult direct fieldへ重複保持しない
- **`FR-091`**：Result payloadはFamily・Type別Schemaで検証する
- **`FR-092`**：canonical Artifactはproject/execution/stage/result relation、artifact type/scope、object_key、media type、hash、size、metadataを保持する。family/generic schema_versionをdirect fieldへ重複保持しない
- **`FR-099`**：Manifest、Result summary、Specification、Artifact参照をexportできる

## 7. 改訂記録

- 2026-11-17: 全23_10〜23_19共通フォーマットへ再構成。Request/Response/ErrorsをOperation別に記載し、Source確認と未検証を分離。
