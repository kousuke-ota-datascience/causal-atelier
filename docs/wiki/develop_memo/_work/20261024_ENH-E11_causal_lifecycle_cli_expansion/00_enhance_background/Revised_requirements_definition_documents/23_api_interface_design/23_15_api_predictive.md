# 23_15_api_predictive — Predictive Web API仕様

## 1. API概要

- 対象: Predictive のHTTP契約。
- Base path: `/api/v1`。
- 本改訂はOwner採用の**Operation単位Request/Response/Errors定義**を対象とする。実行時PASSや要件変更を含まない。
- Source snapshot: `2068b3b2f8c096d581a0f2d56047c4185c5ac7cc`。CURRENTと未検証事項を分離する。

## 2. エンドポイント一覧

| No. | HTTP | Path | Handler | HTTP Success |
|---:|---|---|---|---|
| 1 | `GET` | `/api/v1/projects/{project_id}/predictive/capabilities` | `predictive_capabilities` | `200` |
| 2 | `POST` | `/api/v1/projects/{project_id}/predictive/split-validations` | `validate_predictive_split` | `201` |
| 3 | `GET` | `/api/v1/projects/{project_id}/predictive/partition-artifacts/{artifact_id}` | `get_partition_artifact` | `200` |
| 4 | `POST` | `/api/v1/projects/{project_id}/execution-plans` | `create_execution_plan` | `201` |
| 5 | `GET` | `/api/v1/projects/{project_id}/execution-plans/{plan_id}` | `get_execution_plan` | `200` |
| 6 | `POST` | `/api/v1/projects/{project_id}/execution-plans/{plan_id}/validate` | `validate_execution_plan` | `200` |
| 7 | `POST` | `/api/v1/projects/{project_id}/executions` | `submit_predictive_execution` | `202` |
| 8 | `GET` | `/api/v1/projects/{project_id}/executions/{execution_id}` | `get_predictive_execution` | `200` |
| 9 | `GET` | `/api/v1/projects/{project_id}/executions/{execution_id}/stages` | `get_predictive_stages` | `200` |
| 10 | `GET` | `/api/v1/projects/{project_id}/executions/{execution_id}/results` | `get_predictive_results` | `200` |
| 11 | `GET` | `/api/v1/projects/{project_id}/executions/{execution_id}/artifacts` | `get_predictive_artifacts` | `200` |
| 12 | `GET` | `/api/v1/projects/{project_id}/executions/{execution_id}/lineage` | `get_predictive_lineage` | `200` |
| 13 | `POST` | `/api/v1/projects/{project_id}/executions/{execution_id}/cancel` | `cancel_predictive_execution` | `200` |
| 14 | `POST` | `/api/v1/projects/{project_id}/executions/{execution_id}/retry` | `retry_predictive_execution` | `200` |
| 15 | `POST` | `/api/v1/projects/{project_id}/executions/{execution_id}/rerun` | `rerun_predictive_execution` | `202` |
| 16 | `POST` | `/api/v1/projects/{project_id}/executions/{execution_id}/revise` | `revise_predictive_execution` | `202` |
| 17 | `GET` | `/api/v1/projects/{project_id}/executions/{execution_id}/prefill` | `get_predictive_prefill` | `200` |

## 3. 共通Error Response形式

CURRENTのDomainError/RequestValidationError Handlerは`application/problem+json`ではなく、以下のJSON envelope。

```json
{"error":{"code":"INVALID_REQUEST","message":"Request validation failed.","details":{},"request_id":"{request_id}"}}
```

共通Handlerに定義されたErrorがすべてのOperationから発生するとは限らない。下表の条件付きErrorはテストPASS済みという意味ではない。

## 4. エンドポイント詳細

### 4.1 `GET /api/v1/projects/{project_id}/predictive/capabilities`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-15-01` |
| Method / Path | `GET /api/v1/projects/{project_id}/predictive/capabilities` |
| Handler | `predictive.py::predictive_capabilities` |
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

- HTTP **200**。Response: Service/Router Sourceの返却Object。

| Field | Type | 根拠 |
|---|---|---|
| `schema_version` | `string` | Source上の返却Field |
| `gate` | `string` | Source上の返却Field |
| `task_types` | `array` | Source上の返却Field |
| `split_strategies` | `array` | Source上の返却Field |
| `preprocessing_steps` | `array` | Source上の返却Field |
| `task_defaults` | `object` | Source上の返却Field |
| `model_registry` | `array` | Source上の返却Field |
| `metrics` | `object` | Source上の返却Field |
| `compatibility` | `object` | Source上の返却Field |
| `model_explanation_compatibility` | `object` | Source上の返却Field |
| `explanation_methods` | `array` | Source上の返却Field |

**条件:** PredictiveWorkflowService.capabilities。schema_version=predictive-capabilities/1

#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 対象がなく、ServiceがEntityNotFoundを送出する場合 | 共通Handler。Operationごとの到達は要確認 |
| 422 | PredictiveValidationError.code / INVALID_SCHEMA | Predictive inputや実行契約不適合でDomainErrorを送出する場合 | Error codeはService/Backendの分岐による |

#### 根拠・未検証事項

- Router Source: `predictive.py`（blob `ca9f6e37796c38b6b0de22d78b08e5ed20042198`）。Request DTO: `none`、Response Model: `未宣言`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.2 `POST /api/v1/projects/{project_id}/predictive/split-validations`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-15-02` |
| Method / Path | `POST /api/v1/projects/{project_id}/predictive/split-validations` |
| Handler | `predictive.py::validate_predictive_split` |
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

Content-Type: `application/json`、型 `PredictiveSplitRequest`

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

- HTTP **201**。Body schema: `PredictiveSplitResponse`。

| 項目（wire） | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `schema_version` | `Literal["predictive-split-validation/1"]` | 必須 | 不可 | — |
| `status` | `Literal["VALID"]` | 必須 | 不可 | — |
| `execution_id` | `str` | 必須 | 不可 | — |
| `task_type` | `str` | 必須 | 不可 | — |
| `strategy` | `str` | 必須 | 不可 | — |
| `partition_counts` | `dict[str, int]` | 必須 | 不可 | — |
| `partition_artifact` | `PartitionArtifactResponse` | 必須 | 不可 | — |
| `source_snapshot` | `dict[str, Any]` | 必須 | 不可 | — |

**Response JSON構造例（schema由来の説明用）**

```json
{
  "schema_version": "predictive-split-validation/1",
  "status": "VALID",
  "execution_id": "{execution_id}",
  "task_type": "string",
  "strategy": "string",
  "partition_counts": {},
  "partition_artifact": {
    "artifact_id": "{artifact_id}",
    "schema_version": "partition-artifact/1",
    "content_hash": "string",
    "size_bytes": 0,
    "selection_contract": {}
  },
  "source_snapshot": {}
}
```

#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 対象がなく、ServiceがEntityNotFoundを送出する場合 | 共通Handler。Operationごとの到達は要確認 |
| 409 | PROJECT_ARCHIVED / RESOURCE_IMMUTABLE / EXECUTION_STATE_CONFLICT | 対象がARCHIVED/FIXEDまたは遷移不適格で該当DomainErrorを送出する場合 | 適用可能なOperationのみ、到達は要確認 |
| 422 | PredictiveValidationError.code / INVALID_SCHEMA | Predictive inputや実行契約不適合でDomainErrorを送出する場合 | Error codeはService/Backendの分岐による |

#### 根拠・未検証事項

- Router Source: `predictive.py`（blob `ca9f6e37796c38b6b0de22d78b08e5ed20042198`）。Request DTO: `PredictiveSplitRequest`、Response Model: `PredictiveSplitResponse`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.3 `GET /api/v1/projects/{project_id}/predictive/partition-artifacts/{artifact_id}`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-15-03` |
| Method / Path | `GET /api/v1/projects/{project_id}/predictive/partition-artifacts/{artifact_id}` |
| Handler | `predictive.py::get_partition_artifact` |
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

Router固有の必須Header宣言なし

**Request Body / Field定義**

Request JSON Bodyなし（Router未定義）。

#### Response

- HTTP **200**。Body schema: JSON object（Router/Serviceのdict）。

| 項目 | 意味・型 |
|---|---|
| `artifact_id` | Source返却キー（値の詳細型はService/Schema依存） |
| `execution_id` | Source返却キー（値の詳細型はService/Schema依存） |
| `artifact_type` | Source返却キー（値の詳細型はService/Schema依存） |
| `schema_version` | Source返却キー（値の詳細型はService/Schema依存） |
| `content_hash` | Source返却キー（値の詳細型はService/Schema依存） |
| `size_bytes` | Source返却キー（値の詳細型はService/Schema依存） |
| `metadata` | Source返却キー（値の詳細型はService/Schema依存） |


#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 対象がなく、ServiceがEntityNotFoundを送出する場合 | 共通Handler。Operationごとの到達は要確認 |
| 422 | PredictiveValidationError.code / INVALID_SCHEMA | Predictive inputや実行契約不適合でDomainErrorを送出する場合 | Error codeはService/Backendの分岐による |

#### 根拠・未検証事項

- Router Source: `predictive.py`（blob `ca9f6e37796c38b6b0de22d78b08e5ed20042198`）。Request DTO: `none`、Response Model: `未宣言`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.4 `POST /api/v1/projects/{project_id}/execution-plans`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-15-04` |
| Method / Path | `POST /api/v1/projects/{project_id}/execution-plans` |
| Handler | `predictive_workflow.py::create_execution_plan` |
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

Content-Type: `application/json`、型 `ExecutionPlanCreate`

| 項目 | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `analysis_specification_id` | `str` | 必須 | 不可 | — |

**Request JSON例（説明用）**

```json
{
  "analysis_specification_id": "{analysis_specification_id}"
}
```

#### Response

- HTTP **201**。Response: Service/Router Sourceの返却Object。

| Field | Type | 根拠 |
|---|---|---|
| `execution_plan_id` | `string` | Source上の返却Field |
| `project_id` | `string` | Source上の返却Field |
| `analysis_specification_id` | `string` | Source上の返却Field |
| `analysis_family` | `string` | Source上の返却Field |
| `plan_schema_version` | `string` | Source上の返却Field |
| `planner_id` | `string` | Source上の返却Field |
| `planner_version` | `string` | Source上の返却Field |
| `stages` | `array[object]` | Source上の返却Field |
| `dependencies` | `array[object]` | Source上の返却Field |
| `plan_hash` | `string` | Source上の返却Field |
| `created_at` | `datetime` | Source上の返却Field |

**条件:** PredictiveWorkflowService._plan_response

#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 対象がなく、ServiceがEntityNotFoundを送出する場合 | 共通Handler。Operationごとの到達は要確認 |
| 409 | PROJECT_ARCHIVED / RESOURCE_IMMUTABLE / EXECUTION_STATE_CONFLICT | 対象がARCHIVED/FIXEDまたは遷移不適格で該当DomainErrorを送出する場合 | 適用可能なOperationのみ、到達は要確認 |
| 422 | PredictiveValidationError.code / INVALID_SCHEMA | Predictive inputや実行契約不適合でDomainErrorを送出する場合 | Error codeはService/Backendの分岐による |

#### 根拠・未検証事項

- Router Source: `predictive_workflow.py`（blob `f6a2b04456d23f37baa4f17331241b2427ea5028`）。Request DTO: `ExecutionPlanCreate`、Response Model: `未宣言`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.5 `GET /api/v1/projects/{project_id}/execution-plans/{plan_id}`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-15-05` |
| Method / Path | `GET /api/v1/projects/{project_id}/execution-plans/{plan_id}` |
| Handler | `predictive_workflow.py::get_execution_plan` |
| Success Status | HTTP 200 |

#### Request

**Path parameters**

| 項目 | 型 | 必須 |
|---|---|---|
| `project_id` | string | 必須 |
| `plan_id` | string | 必須 |

**Query parameters**

なし

**Headers**

Router固有の必須Header宣言なし

**Request Body / Field定義**

Request JSON Bodyなし（Router未定義）。

#### Response

- HTTP **200**。Response: Service/Router Sourceの返却Object。

| Field | Type | 根拠 |
|---|---|---|
| `execution_plan_id` | `string` | Source上の返却Field |
| `project_id` | `string` | Source上の返却Field |
| `analysis_specification_id` | `string` | Source上の返却Field |
| `analysis_family` | `string` | Source上の返却Field |
| `plan_schema_version` | `string` | Source上の返却Field |
| `planner_id` | `string` | Source上の返却Field |
| `planner_version` | `string` | Source上の返却Field |
| `stages` | `array[object]` | Source上の返却Field |
| `dependencies` | `array[object]` | Source上の返却Field |
| `plan_hash` | `string` | Source上の返却Field |
| `created_at` | `datetime` | Source上の返却Field |

**条件:** PredictiveWorkflowService._plan_response

#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 対象がなく、ServiceがEntityNotFoundを送出する場合 | 共通Handler。Operationごとの到達は要確認 |
| 422 | PredictiveValidationError.code / INVALID_SCHEMA | Predictive inputや実行契約不適合でDomainErrorを送出する場合 | Error codeはService/Backendの分岐による |

#### 根拠・未検証事項

- Router Source: `predictive_workflow.py`（blob `f6a2b04456d23f37baa4f17331241b2427ea5028`）。Request DTO: `none`、Response Model: `未宣言`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.6 `POST /api/v1/projects/{project_id}/execution-plans/{plan_id}/validate`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-15-06` |
| Method / Path | `POST /api/v1/projects/{project_id}/execution-plans/{plan_id}/validate` |
| Handler | `predictive_workflow.py::validate_execution_plan` |
| Success Status | HTTP 200 |

#### Request

**Path parameters**

| 項目 | 型 | 必須 |
|---|---|---|
| `project_id` | string | 必須 |
| `plan_id` | string | 必須 |

**Query parameters**

なし

**Headers**

Router固有の必須Header宣言なし

**Request Body / Field定義**

Request JSON Bodyなし（Router未定義）。

#### Response

- HTTP **200**。Body schema: JSON object（Router/Serviceのdict）。

| 項目 | 意味・型 |
|---|---|
| `execution_plan_id` | Source返却キー（値の詳細型はService/Schema依存） |
| `valid` | Source返却キー（値の詳細型はService/Schema依存） |
| `plan_hash` | Source返却キー（値の詳細型はService/Schema依存） |
| `execution_order` | Source返却キー（値の詳細型はService/Schema依存） |


#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 対象がなく、ServiceがEntityNotFoundを送出する場合 | 共通Handler。Operationごとの到達は要確認 |
| 409 | PROJECT_ARCHIVED / RESOURCE_IMMUTABLE / EXECUTION_STATE_CONFLICT | 対象がARCHIVED/FIXEDまたは遷移不適格で該当DomainErrorを送出する場合 | 適用可能なOperationのみ、到達は要確認 |
| 422 | PredictiveValidationError.code / INVALID_SCHEMA | Predictive inputや実行契約不適合でDomainErrorを送出する場合 | Error codeはService/Backendの分岐による |

#### 根拠・未検証事項

- Router Source: `predictive_workflow.py`（blob `f6a2b04456d23f37baa4f17331241b2427ea5028`）。Request DTO: `none`、Response Model: `未宣言`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.7 `POST /api/v1/projects/{project_id}/executions`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-15-07` |
| Method / Path | `POST /api/v1/projects/{project_id}/executions` |
| Handler | `predictive_workflow.py::submit_predictive_execution` |
| Success Status | HTTP 202 |

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

Content-Type: `application/json`、型 `PredictiveExecutionSubmit`

| 項目 | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `analysis_specification_id` | `str` | 必須 | 不可 | — |
| `execution_plan_id` | `str` | 必須 | 不可 | — |
| `seed` | `int` | 必須 | 不可 | — |

**Request JSON例（説明用）**

```json
{
  "analysis_specification_id": "{analysis_specification_id}",
  "execution_plan_id": "{execution_plan_id}",
  "seed": 0
}
```

#### Response

- HTTP **202**。Response: Service/Router Sourceの返却Object。

| Field | Type | 根拠 |
|---|---|---|
| `execution_id` | `string` | Source上の返却Field |
| `project_id` | `string` | Source上の返却Field |
| `analysis_family` | `string` | Source上の返却Field |
| `dataset_version_id` | `string` | Source上の返却Field |
| `status` | `string` | Source上の返却Field |
| `retry_count` | `integer` | Source上の返却Field |
| `last_error` | `object\|null` | Source上の返却Field |
| `requested_by` | `string` | Source上の返却Field |
| `requested_at` | `datetime` | Source上の返却Field |
| `started_at` | `datetime\|null` | Source上の返却Field |
| `finished_at` | `datetime\|null` | Source上の返却Field |
| `analysis_specification_id` | `string` | Source上の返却Field |
| `execution_plan_id` | `string` | Source上の返却Field |
| `analysis_view_id` | `string\|null` | Source上の返却Field |
| `snapshot_hash` | `string` | Source上の返却Field |
| `snapshot` | `object` | Source上の返却Field |
| `specification_schema_version` | `string` | Source上の返却Field |
| `revision_kind` | `string\|null` | Source上の返却Field |

**条件:** Canonical/Family 2種のExecution Responseを統合したField一覧。各Fieldの存在は実行laneに依存

#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗 | 共通Handler |
| 400/409 | IDEMPOTENCY_KEY_REQUIRED / IDEMPOTENCY_CONFLICT | Key欠落・異なる内容の同一Key再利用 | IdempotencyService |
| 404 | ENTITY_NOT_FOUND | 対象がなく、ServiceがEntityNotFoundを送出する場合 | 共通Handler。Operationごとの到達は要確認 |
| 409 | PROJECT_ARCHIVED / RESOURCE_IMMUTABLE / EXECUTION_STATE_CONFLICT | 対象がARCHIVED/FIXEDまたは遷移不適格で該当DomainErrorを送出する場合 | 適用可能なOperationのみ、到達は要確認 |
| 422 | PredictiveValidationError.code / INVALID_SCHEMA | Predictive inputや実行契約不適合でDomainErrorを送出する場合 | Error codeはService/Backendの分岐による |

#### 根拠・未検証事項

- Router Source: `predictive_workflow.py`（blob `f6a2b04456d23f37baa4f17331241b2427ea5028`）。Request DTO: `PredictiveExecutionSubmit`、Response Model: `未宣言`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.8 `GET /api/v1/projects/{project_id}/executions/{execution_id}`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-15-08` |
| Method / Path | `GET /api/v1/projects/{project_id}/executions/{execution_id}` |
| Handler | `predictive_workflow.py::get_predictive_execution` |
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

- HTTP **200**。Response: Service/Router Sourceの返却Object。

| Field | Type | 根拠 |
|---|---|---|
| `execution_id` | `string` | Source上の返却Field |
| `project_id` | `string` | Source上の返却Field |
| `analysis_family` | `string` | Source上の返却Field |
| `dataset_version_id` | `string` | Source上の返却Field |
| `status` | `string` | Source上の返却Field |
| `retry_count` | `integer` | Source上の返却Field |
| `last_error` | `object\|null` | Source上の返却Field |
| `requested_by` | `string` | Source上の返却Field |
| `requested_at` | `datetime` | Source上の返却Field |
| `started_at` | `datetime\|null` | Source上の返却Field |
| `finished_at` | `datetime\|null` | Source上の返却Field |
| `analysis_specification_id` | `string` | Source上の返却Field |
| `execution_plan_id` | `string` | Source上の返却Field |
| `analysis_view_id` | `string\|null` | Source上の返却Field |
| `snapshot_hash` | `string` | Source上の返却Field |
| `snapshot` | `object` | Source上の返却Field |
| `specification_schema_version` | `string` | Source上の返却Field |
| `revision_kind` | `string\|null` | Source上の返却Field |

**条件:** Canonical/Family 2種のExecution Responseを統合したField一覧。各Fieldの存在は実行laneに依存

#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 対象がなく、ServiceがEntityNotFoundを送出する場合 | 共通Handler。Operationごとの到達は要確認 |
| 422 | PredictiveValidationError.code / INVALID_SCHEMA | Predictive inputや実行契約不適合でDomainErrorを送出する場合 | Error codeはService/Backendの分岐による |

#### 根拠・未検証事項

- Router Source: `predictive_workflow.py`（blob `f6a2b04456d23f37baa4f17331241b2427ea5028`）。Request DTO: `none`、Response Model: `未宣言`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.9 `GET /api/v1/projects/{project_id}/executions/{execution_id}/stages`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-15-09` |
| Method / Path | `GET /api/v1/projects/{project_id}/executions/{execution_id}/stages` |
| Handler | `predictive_workflow.py::get_predictive_stages` |
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
| 422 | PredictiveValidationError.code / INVALID_SCHEMA | Predictive inputや実行契約不適合でDomainErrorを送出する場合 | Error codeはService/Backendの分岐による |

#### 根拠・未検証事項

- Router Source: `predictive_workflow.py`（blob `f6a2b04456d23f37baa4f17331241b2427ea5028`）。Request DTO: `none`、Response Model: `未宣言`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.10 `GET /api/v1/projects/{project_id}/executions/{execution_id}/results`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-15-10` |
| Method / Path | `GET /api/v1/projects/{project_id}/executions/{execution_id}/results` |
| Handler | `predictive_workflow.py::get_predictive_results` |
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
| 422 | PredictiveValidationError.code / INVALID_SCHEMA | Predictive inputや実行契約不適合でDomainErrorを送出する場合 | Error codeはService/Backendの分岐による |

#### 根拠・未検証事項

- Router Source: `predictive_workflow.py`（blob `f6a2b04456d23f37baa4f17331241b2427ea5028`）。Request DTO: `none`、Response Model: `未宣言`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.11 `GET /api/v1/projects/{project_id}/executions/{execution_id}/artifacts`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-15-11` |
| Method / Path | `GET /api/v1/projects/{project_id}/executions/{execution_id}/artifacts` |
| Handler | `predictive_workflow.py::get_predictive_artifacts` |
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
| 422 | PredictiveValidationError.code / INVALID_SCHEMA | Predictive inputや実行契約不適合でDomainErrorを送出する場合 | Error codeはService/Backendの分岐による |

#### 根拠・未検証事項

- Router Source: `predictive_workflow.py`（blob `f6a2b04456d23f37baa4f17331241b2427ea5028`）。Request DTO: `none`、Response Model: `未宣言`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.12 `GET /api/v1/projects/{project_id}/executions/{execution_id}/lineage`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-15-12` |
| Method / Path | `GET /api/v1/projects/{project_id}/executions/{execution_id}/lineage` |
| Handler | `predictive_workflow.py::get_predictive_lineage` |
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
| 422 | PredictiveValidationError.code / INVALID_SCHEMA | Predictive inputや実行契約不適合でDomainErrorを送出する場合 | Error codeはService/Backendの分岐による |

#### 根拠・未検証事項

- Router Source: `predictive_workflow.py`（blob `f6a2b04456d23f37baa4f17331241b2427ea5028`）。Request DTO: `none`、Response Model: `未宣言`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.13 `POST /api/v1/projects/{project_id}/executions/{execution_id}/cancel`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-15-13` |
| Method / Path | `POST /api/v1/projects/{project_id}/executions/{execution_id}/cancel` |
| Handler | `predictive_workflow.py::cancel_predictive_execution` |
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

- HTTP **200**。Response: Service/Router Sourceの返却Object。

| Field | Type | 根拠 |
|---|---|---|
| `execution_id` | `string` | Source上の返却Field |
| `project_id` | `string` | Source上の返却Field |
| `analysis_family` | `string` | Source上の返却Field |
| `dataset_version_id` | `string` | Source上の返却Field |
| `status` | `string` | Source上の返却Field |
| `retry_count` | `integer` | Source上の返却Field |
| `last_error` | `object\|null` | Source上の返却Field |
| `requested_by` | `string` | Source上の返却Field |
| `requested_at` | `datetime` | Source上の返却Field |
| `started_at` | `datetime\|null` | Source上の返却Field |
| `finished_at` | `datetime\|null` | Source上の返却Field |

**条件:** Cancel後のExecution projection。詳細Fieldはcanonical/family laneで異なる

#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 対象がなく、ServiceがEntityNotFoundを送出する場合 | 共通Handler。Operationごとの到達は要確認 |
| 409 | PROJECT_ARCHIVED / RESOURCE_IMMUTABLE / EXECUTION_STATE_CONFLICT | 対象がARCHIVED/FIXEDまたは遷移不適格で該当DomainErrorを送出する場合 | 適用可能なOperationのみ、到達は要確認 |
| 422 | PredictiveValidationError.code / INVALID_SCHEMA | Predictive inputや実行契約不適合でDomainErrorを送出する場合 | Error codeはService/Backendの分岐による |

#### 根拠・未検証事項

- Router Source: `predictive_workflow.py`（blob `f6a2b04456d23f37baa4f17331241b2427ea5028`）。Request DTO: `none`、Response Model: `未宣言`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.14 `POST /api/v1/projects/{project_id}/executions/{execution_id}/retry`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-15-14` |
| Method / Path | `POST /api/v1/projects/{project_id}/executions/{execution_id}/retry` |
| Handler | `predictive_workflow.py::retry_predictive_execution` |
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

- HTTP **200**。Response: Service/Router Sourceの返却Object。

| Field | Type | 根拠 |
|---|---|---|
| `execution_id` | `string` | Source上の返却Field |
| `project_id` | `string` | Source上の返却Field |
| `analysis_family` | `string` | Source上の返却Field |
| `dataset_version_id` | `string` | Source上の返却Field |
| `status` | `string` | Source上の返却Field |
| `retry_count` | `integer` | Source上の返却Field |
| `last_error` | `object\|null` | Source上の返却Field |
| `requested_by` | `string` | Source上の返却Field |
| `requested_at` | `datetime` | Source上の返却Field |
| `started_at` | `datetime\|null` | Source上の返却Field |
| `finished_at` | `datetime\|null` | Source上の返却Field |

**条件:** Retry後のExecution projection。詳細Fieldはcanonical/family laneで異なる

#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 対象がなく、ServiceがEntityNotFoundを送出する場合 | 共通Handler。Operationごとの到達は要確認 |
| 409 | PROJECT_ARCHIVED / RESOURCE_IMMUTABLE / EXECUTION_STATE_CONFLICT | 対象がARCHIVED/FIXEDまたは遷移不適格で該当DomainErrorを送出する場合 | 適用可能なOperationのみ、到達は要確認 |
| 422 | PredictiveValidationError.code / INVALID_SCHEMA | Predictive inputや実行契約不適合でDomainErrorを送出する場合 | Error codeはService/Backendの分岐による |

#### 根拠・未検証事項

- Router Source: `predictive_workflow.py`（blob `f6a2b04456d23f37baa4f17331241b2427ea5028`）。Request DTO: `none`、Response Model: `未宣言`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.15 `POST /api/v1/projects/{project_id}/executions/{execution_id}/rerun`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-15-15` |
| Method / Path | `POST /api/v1/projects/{project_id}/executions/{execution_id}/rerun` |
| Handler | `predictive_workflow.py::rerun_predictive_execution` |
| Success Status | HTTP 202 |

#### Request

**Path parameters**

| 項目 | 型 | 必須 |
|---|---|---|
| `project_id` | string | 必須 |
| `execution_id` | string | 必須 |

**Query parameters**

なし

**Headers**

| Header | 仕様 |
|---|---|
| `X-User-Id` | Sourceで参照。認証確立の証拠ではない |

**Request Body / Field定義**

Request JSON Bodyなし（Router未定義）。

#### Response

- HTTP **202**。Response: Service/Router Sourceの返却Object。

| Field | Type | 根拠 |
|---|---|---|
| `execution_id` | `string` | Source上の返却Field |
| `project_id` | `string` | Source上の返却Field |
| `analysis_family` | `string` | Source上の返却Field |
| `dataset_version_id` | `string` | Source上の返却Field |
| `status` | `string` | Source上の返却Field |
| `retry_count` | `integer` | Source上の返却Field |
| `last_error` | `object\|null` | Source上の返却Field |
| `requested_by` | `string` | Source上の返却Field |
| `requested_at` | `datetime` | Source上の返却Field |
| `started_at` | `datetime\|null` | Source上の返却Field |
| `finished_at` | `datetime\|null` | Source上の返却Field |

**条件:** Rerunにより新たに作成したExecutionのprojection

#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 対象がなく、ServiceがEntityNotFoundを送出する場合 | 共通Handler。Operationごとの到達は要確認 |
| 409 | PROJECT_ARCHIVED / RESOURCE_IMMUTABLE / EXECUTION_STATE_CONFLICT | 対象がARCHIVED/FIXEDまたは遷移不適格で該当DomainErrorを送出する場合 | 適用可能なOperationのみ、到達は要確認 |
| 422 | PredictiveValidationError.code / INVALID_SCHEMA | Predictive inputや実行契約不適合でDomainErrorを送出する場合 | Error codeはService/Backendの分岐による |

#### 根拠・未検証事項

- Router Source: `predictive_workflow.py`（blob `f6a2b04456d23f37baa4f17331241b2427ea5028`）。Request DTO: `none`、Response Model: `未宣言`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.16 `POST /api/v1/projects/{project_id}/executions/{execution_id}/revise`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-15-16` |
| Method / Path | `POST /api/v1/projects/{project_id}/executions/{execution_id}/revise` |
| Handler | `predictive_workflow.py::revise_predictive_execution` |
| Success Status | HTTP 202 |

#### Request

**Path parameters**

| 項目 | 型 | 必須 |
|---|---|---|
| `project_id` | string | 必須 |
| `execution_id` | string | 必須 |

**Query parameters**

なし

**Headers**

| Header | 仕様 |
|---|---|
| `X-User-Id` | Sourceで参照。認証確立の証拠ではない |

**Request Body / Field定義**

Content-Type: `application/json`、型 `PredictiveExecutionRevise`

| 項目 | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `analysis_specification_id` | `str` | 必須 | 不可 | — |
| `seed` | `int` | 必須 | 不可 | — |
| `change_reason` | `str` | 必須 | 不可 | — |
| `project_id` | `str,` | 必須 | 不可 | — |
| `body` | `ExecutionPlanCreate,` | 必須 | 不可 | — |
| `svc` | `PredictiveWorkflowServiceDep,` | 必須 | 不可 | — |
| `project_id` | `str, plan_id: str, svc: PredictiveWorkflowServiceDep` | 必須 | 不可 | — |
| `project_id` | `str, plan_id: str, svc: PredictiveWorkflowServiceDep` | 必須 | 不可 | — |
| `project_id` | `str,` | 必須 | 不可 | — |
| `body` | `PredictiveExecutionSubmit,` | 必須 | 不可 | — |
| `request` | `Request,` | 必須 | 不可 | — |
| `svc` | `PredictiveWorkflowServiceDep,` | 必須 | 不可 | — |
| `idempotency` | `IdempotencyServiceDep,` | 必須 | 不可 | — |
| `idempotency_key` | `str \| None` | 任意 | 許可 | lt=None |
| `project_id` | `str, execution_id: str, svc: PredictiveWorkflowServiceDep` | 必須 | 不可 | — |
| `project_id` | `str, execution_id: str, svc: PredictiveWorkflowServiceDep` | 必須 | 不可 | — |
| `project_id` | `str, execution_id: str, svc: PredictiveWorkflowServiceDep` | 必須 | 不可 | — |
| `project_id` | `str, execution_id: str, svc: PredictiveWorkflowServiceDep` | 必須 | 不可 | — |
| `project_id` | `str, execution_id: str, svc: PredictiveWorkflowServiceDep` | 必須 | 不可 | — |
| `project_id` | `str, execution_id: str, svc: PredictiveWorkflowServiceDep` | 必須 | 不可 | — |
| `project_id` | `str, execution_id: str, svc: PredictiveWorkflowServiceDep` | 必須 | 不可 | — |
| `project_id` | `str,` | 必須 | 不可 | — |
| `execution_id` | `str,` | 必須 | 不可 | — |
| `request` | `Request,` | 必須 | 不可 | — |
| `svc` | `PredictiveWorkflowServiceDep,` | 必須 | 不可 | — |
| `project_id` | `str,` | 必須 | 不可 | — |
| `execution_id` | `str,` | 必須 | 不可 | — |
| `body` | `PredictiveExecutionRevise,` | 必須 | 不可 | — |
| `request` | `Request,` | 必須 | 不可 | — |
| `svc` | `PredictiveWorkflowServiceDep,` | 必須 | 不可 | — |
| `project_id` | `str, execution_id: str, svc: PredictiveWorkflowServiceDep` | 必須 | 不可 | — |

**Request JSON例（説明用）**

```json
{
  "analysis_specification_id": "{analysis_specification_id}",
  "seed": 0,
  "change_reason": "string",
  "project_id": "{project_id}",
  "body": "string",
  "svc": "string",
  "request": "string",
  "idempotency": "string",
  "execution_id": "{execution_id}"
}
```

#### Response

- HTTP **202**。Response: Service/Router Sourceの返却Object。

| Field | Type | 根拠 |
|---|---|---|
| `execution_id` | `string` | Source上の返却Field |
| `project_id` | `string` | Source上の返却Field |
| `analysis_family` | `string` | Source上の返却Field |
| `dataset_version_id` | `string` | Source上の返却Field |
| `status` | `string` | Source上の返却Field |
| `retry_count` | `integer` | Source上の返却Field |
| `last_error` | `object\|null` | Source上の返却Field |
| `requested_by` | `string` | Source上の返却Field |
| `requested_at` | `datetime` | Source上の返却Field |
| `started_at` | `datetime\|null` | Source上の返却Field |
| `finished_at` | `datetime\|null` | Source上の返却Field |

**条件:** Reviseにより新たに作成したExecutionのprojection

#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 対象がなく、ServiceがEntityNotFoundを送出する場合 | 共通Handler。Operationごとの到達は要確認 |
| 409 | PROJECT_ARCHIVED / RESOURCE_IMMUTABLE / EXECUTION_STATE_CONFLICT | 対象がARCHIVED/FIXEDまたは遷移不適格で該当DomainErrorを送出する場合 | 適用可能なOperationのみ、到達は要確認 |
| 422 | PredictiveValidationError.code / INVALID_SCHEMA | Predictive inputや実行契約不適合でDomainErrorを送出する場合 | Error codeはService/Backendの分岐による |

#### 根拠・未検証事項

- Router Source: `predictive_workflow.py`（blob `f6a2b04456d23f37baa4f17331241b2427ea5028`）。Request DTO: `PredictiveExecutionRevise`、Response Model: `未宣言`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.17 `GET /api/v1/projects/{project_id}/executions/{execution_id}/prefill`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-15-17` |
| Method / Path | `GET /api/v1/projects/{project_id}/executions/{execution_id}/prefill` |
| Handler | `predictive_workflow.py::get_predictive_prefill` |
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

- HTTP **200**。Body schema: JSON object（Router/Serviceのdict）。

| 項目 | 意味・型 |
|---|---|
| `base_execution_id` | Source返却キー（値の詳細型はService/Schema依存） |
| `analysis_specification_id` | Source返却キー（値の詳細型はService/Schema依存） |
| `execution_plan_id` | Source返却キー（値の詳細型はService/Schema依存） |
| `seed` | Source返却キー（値の詳細型はService/Schema依存） |
| `revision_context` | Source返却キー（値の詳細型はService/Schema依存） |


#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 対象がなく、ServiceがEntityNotFoundを送出する場合 | 共通Handler。Operationごとの到達は要確認 |
| 422 | PredictiveValidationError.code / INVALID_SCHEMA | Predictive inputや実行契約不適合でDomainErrorを送出する場合 | Error codeはService/Backendの分岐による |

#### 根拠・未検証事項

- Router Source: `predictive_workflow.py`（blob `f6a2b04456d23f37baa4f17331241b2427ea5028`）。Request DTO: `none`、Response Model: `未宣言`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

## 5. 検証状況

- Route/Method/Path: 17 件 Source確認。
- Request: Router/Pydanticモデルの静的制約を反映。Response: 型付きモデルは全Fieldを表記。Service無型応答は一部未確定。
- HTTP Contract Test: NOT_RUN。Endpoint詳細の完全性・認可・実行時エラー網羅は未検証。
- 元の`docs/wiki/requirement_definition/`への昇格: NOT_DONE。

## 6. 既存Domain・設計制約（旧仕様本文から保持）

以下は既存のDomain規範・補足情報を保持したもの。重複する旧Route一覧より§2（Source基準）を優先する。改訂前の原本文はGit Blob `9dc7ef62e0f1ec7d0c769556f98cfa3d593c8226`で追跡可能。

### Predictive Interface

Predictive analysisは`predictive-analysis-spec/1`を入力契約とする。現行実装のfull runtime planは`split -> prepare -> train -> evaluate -> optional explain`である。

Predictive Navigation Stage:

- Setup
- Train
- Predict
- Metrics
- Explainability
- Model Management

これらのStage名に合わせて独立execution APIを6本新設することは要件ではない。

現行実装で存在するPredictive support API:

| Method | Path | 用途 |
| --- | --- | --- |
| GET | `/projects/{project_id}/predictive/capabilities` | Predictive capability metadata |
| POST | `/projects/{project_id}/predictive/split-validations` | split validationを実行しpartition artifactを保存 |
| GET | `/projects/{project_id}/predictive/partition-artifacts/{artifact_id}` | partition artifact metadata取得 |

Split validation requestは`dataset_version_id / analysis_view_id? / family_spec`を受け取る。responseは`predictive-split-validation/1`で、`status=VALID / execution_id / task_type / strategy / partition_counts / partition_artifact / source_snapshot`を返す。

`Metrics`は保存済み`EVALUATION_RESULT`をreadして成立し得る。`Model Management`は`TRAINING_RESULT`、`MODEL_CARD_RESULT`、`FITTED_MODEL`、`MODEL_CARD`等のResult / Artifactをreadするsurfaceとして成立し得る。Navigation再配置を理由にPredictive spec/validation/defaultを変更しない。


#### Predictive subgroup evaluation response contract

Predictive evaluation outputは指定subgroupごとにrecord listを返す。group valueをJSON object keyへ埋め込まない。

```json
{
  "subgroup_metrics": [
    {
      "subgroup_column": "segment",
      "subgroup_value": "A",
      "is_null_group": false,
      "metric": "roc_auc",
      "sample_count": 120,
      "value": 0.81,
      "uncertainty": {
        "method": "percentile_bootstrap",
        "confidence": 0.95,
        "lower": 0.76,
        "upper": 0.86,
        "requested_resamples": 1000,
        "valid_resamples": 1000
      },
      "status": "OK",
      "warnings": []
    }
  ]
}
```

- evaluation population = untouched TEST。
- specified subgroup columnごとに独立sliceし、自動intersection/discoveryをしない。
- `sample_count`は常に必須。
- bootstrapはnonparametric percentile、confidence=0.95、1000 resamples、deterministic seed。
- `n < 2`またはvalid resamples < 200では`uncertainty=null` + warning。
- metric計算不能は`value=null`、`uncertainty=null`、status/warningを返す。値を捏造しない。

#### Predictive advanced capabilities contract

`GET /projects/{project_id}/predictive/capabilities` remains the canonical Predictive capability metadata endpoint.

Response schema remains:

```text
predictive-capabilities/1
```

Existing fields/types remain backward-compatible. ENH-E10 adds the following metadata from the same backend model/explanation capability authorities.

```json
{
  "schema_version": "predictive-capabilities/1",
  "task_defaults": {
    "BINARY_CLASSIFICATION": {"model_id": "logistic_regression.v1"},
    "REGRESSION": {"model_id": "linear_regression.v1"}
  },
  "model_registry": [
    {
      "model_id": "lightgbm_classifier.v1",
      "contract_version": "1",
      "supported_tasks": ["BINARY_CLASSIFICATION"],
      "parameter_schema": ["num_boost_round", "learning_rate", "num_leaves", "max_depth", "min_data_in_leaf", "lambda_l2"],
      "parameters": {
        "num_boost_round": {"type": "integer", "minimum": 1, "maximum": 2000, "default": 100},
        "learning_rate": {"type": "number", "exclusive_minimum": 0, "maximum": 1, "default": 0.1}
      },
      "provider": "lightgbm",
      "dependency": "lightgbm",
      "available": true,
      "unavailable_reason": null,
      "provider_version": "4.7.x",
      "deterministic_seed": true,
      "determinism": {"mode": "same-runtime-config", "num_threads": 1, "device_type": "cpu"},
      "serializer_id": "lightgbm-model-string/1",
      "loader_id": "lightgbm-booster/1",
      "default_for_tasks": []
    }
  ],
  "explanation_methods": [
    {
      "method": "SHAP_TREE",
      "contract_version": "1",
      "supported_models": ["lightgbm_classifier.v1", "lightgbm_regressor.v1"],
      "supports_global": true,
      "supports_local": true,
      "model_output_scales": ["LOG_ODDS", "PREDICTION"],
      "dependency": "shap",
      "available": true,
      "unavailable_reason": null,
      "provider_version": "0.52.x",
      "default_for_models": ["lightgbm_classifier.v1", "lightgbm_regressor.v1"]
    }
  ],
  "model_explanation_compatibility": {}
}
```

The example is illustrative; exact ordering is not semantic. Existing `parameter_schema`, `deterministic_seed`, `compatibility`, and existing explanation fields remain compatibility projections. Structured model controls consume `parameters`.

Backend validation is final authority. A client-provided model/method that is unregistered, task-incompatible, dependency-unavailable, parameter-invalid or scope-incompatible must be rejected explicitly; the server does not substitute a different model/method.

Stable Predictive validation/failure codes include:

- `MODEL_NOT_REGISTERED`
- `MODEL_TASK_MISMATCH`
- `MODEL_PARAMETER_INVALID`
- `MODEL_DEPENDENCY_UNAVAILABLE`
- `MODEL_ARTIFACT_UNSUPPORTED`
- `MODEL_ARTIFACT_LOAD_FAILED`
- `MODEL_FEATURE_MISMATCH`
- `PREPROCESSOR_MODEL_MISMATCH`
- `EXPLANATION_METHOD_NOT_REGISTERED`
- `EXPLANATION_METHOD_NOT_APPLICABLE`
- `EXPLANATION_DEPENDENCY_UNAVAILABLE`
- `EXPLANATION_SCOPE_NOT_SUPPORTED`
- `EXPLANATION_COMPUTATION_FAILED`

Synchronous request/domain validation uses the canonical 422 validation envelope. Provider runtime failures are persisted as execution/stage failure evidence rather than silently converted to another capability.

Model artifacts continue to use existing Artifact resources. New model writes carry `fitted-model/2` in Artifact content/metadata; existing `fitted-model/1` remains readable. No new Model Registry API or persistence aggregate is introduced.

**当該Interfaceの追加契約（関連Requirement）**

- **`FR-061`**：Algorithm Registryはtask compatibilityに加えてmodel capability、parameter schema/default、provider/optional dependency availability/versionを表現し、利用可能なtask-compatible modelをbackend authorityで選択できる
- **`FR-071`**：intended use、training data、metric、limitationsに加え、model/provider/version、effective parameters、seed/deterministic settings、feature/preprocessor identity、explanation method等の再現性provenanceをModel Cardへ記録する
- **`FR-181`**：Predictive Explanationはmodel-method compatibilityをbackend authorityで検証し、`LINEAR_COEFFICIENT_CONTRIBUTION` / `SHAP_TREE` / `LIME_TABULAR`を明示methodとして解決する
- **`FR-183`**：explanation Result/Artifactはmethod/model/provider、feature/sample identity、model/prediction output scale、background/reference、effective seed/parameters、library version等のprovenanceを保持する
- **`FR-184`**：Train / Explainability / Model Managementはbackend capability metadataからcompatible option、availability/reason、parameter definition、provenanceを表示し、Frontendを独立したmodel-method compatibility authorityにしない

## 7. 改訂記録

- 2026-11-17: 全23_10〜23_19共通フォーマットへ再構成。Request/Response/ErrorsをOperation別に記載し、Source確認と未検証を分離。
