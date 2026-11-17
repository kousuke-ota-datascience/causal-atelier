# 23_16_api_execution — Execution Web API仕様

## 1. API概要

- 対象: Execution のHTTP契約。
- Base path: `/api/v1`。
- 本改訂はOwner採用の**Operation単位Request/Response/Errors定義**を対象とする。実行時PASSや要件変更を含まない。
- Source snapshot: `2068b3b2f8c096d581a0f2d56047c4185c5ac7cc`。CURRENTと未検証事項を分離する。

## 2. エンドポイント一覧

| No. | HTTP | Path | Handler | HTTP Success |
|---:|---|---|---|---|
| 1 | `POST` | `/api/v1/projects/{project_id}/execution-batches` | `create_execution_batch` | `202` |
| 2 | `GET` | `/api/v1/projects/{project_id}/executions` | `list_executions` | `200` |
| 3 | `GET` | `/api/v1/executions/{execution_id}` | `get_execution` | `200` |
| 4 | `GET` | `/api/v1/executions/{execution_id}/prefill` | `get_execution_prefill` | `200` |
| 5 | `POST` | `/api/v1/executions/{execution_id}/cancel` | `cancel_execution` | `204` |
| 6 | `POST` | `/api/v1/executions/{execution_id}/retry` | `retry_execution` | `204` |

## 3. 共通Error Response形式

CURRENTのDomainError/RequestValidationError Handlerは`application/problem+json`ではなく、以下のJSON envelope。

```json
{"error":{"code":"INVALID_REQUEST","message":"Request validation failed.","details":{},"request_id":"{request_id}"}}
```

共通Handlerに定義されたErrorがすべてのOperationから発生するとは限らない。下表の条件付きErrorはテストPASS済みという意味ではない。

## 4. エンドポイント詳細

### 4.1 `POST /api/v1/projects/{project_id}/execution-batches`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-16-01` |
| Method / Path | `POST /api/v1/projects/{project_id}/execution-batches` |
| Handler | `executions.py::create_execution_batch` |
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

Content-Type: `application/json`、型 `ExecutionBatchCreate`

| 項目（wire） | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `operation` | `Literal["DISCOVERY", "IDENTIFICATION", "ESTIMATION", "REFUTATION", "SENSITIVITY"]` | 必須 | 不可 | — |
| `analysis_family` | `Literal["CAUSAL", "EXPLORATORY", "PREDICTIVE"]` | 任意 | 不可 | "CAUSAL" |
| `dataset_version_id` | `str` | 必須 | 不可 | — |
| `input_graph_version_id` | `str \| None` | 任意 | 許可 | None |
| `input_result_id` | `str \| None` | 任意 | 許可 | None |
| `objective` | `str \| None` | 任意 | 許可 | lt=None, max_length=4000 |
| `rationale` | `str \| None` | 任意 | 許可 | lt=None, max_length=8000 |
| `analysis_spec` | `dict[str, Any]` | 必須 | 不可 | — |
| `variants` | `list[ExecutionVariantRequest]` | 必須 | 不可 | min_length=1, max_length=20 |
| `code_version` | `str` | 必須 | 不可 | min_length=1, max_length=200 |
| `runtime_versions` | `dict[str, Any]` | 必須 | 不可 | — |
| `base_execution_id` | `str \| None` | 任意 | 許可 | None |
| `change_reason` | `str \| None` | 任意 | 許可 | lt=None, max_length=8000 |

**Request JSON例（schema由来の説明用）**

```json
{
  "operation": "DISCOVERY",
  "dataset_version_id": "{dataset_version_id}",
  "analysis_spec": {},
  "variants": [],
  "code_version": "string",
  "runtime_versions": {}
}
```

#### Response

- HTTP **202**。Body schema: `ExecutionBatchResponse`。

| 項目（wire） | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `batch_key` | `str` | 必須 | 不可 | — |
| `executions` | `list[ExecutionAccepted]` | 必須 | 不可 | — |

**Response JSON構造例（schema由来の説明用）**

```json
{
  "batch_key": "string",
  "executions": []
}
```

#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗 | 共通Handler |
| 400/409 | IDEMPOTENCY_KEY_REQUIRED / IDEMPOTENCY_CONFLICT | Key欠落・異なる内容の同一Key再利用 | IdempotencyService |
| 404 | ENTITY_NOT_FOUND | 対象がなく、ServiceがEntityNotFoundを送出する場合 | 共通Handler。Operationごとの到達は要確認 |
| 409 | PROJECT_ARCHIVED / RESOURCE_IMMUTABLE / EXECUTION_STATE_CONFLICT | 対象がARCHIVED/FIXEDまたは遷移不適格で該当DomainErrorを送出する場合 | 適用可能なOperationのみ、到達は要確認 |

#### 根拠・未検証事項

- Router Source: `executions.py`（blob `c073974ed1bbd91161b67035850070c78a46e7da`）。Request DTO: `ExecutionBatchCreate`、Response Model: `ExecutionBatchResponse`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.2 `GET /api/v1/projects/{project_id}/executions`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-16-02` |
| Method / Path | `GET /api/v1/projects/{project_id}/executions` |
| Handler | `executions.py::list_executions` |
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

#### 根拠・未検証事項

- Router Source: `executions.py`（blob `c073974ed1bbd91161b67035850070c78a46e7da`）。Request DTO: `none`、Response Model: `未宣言`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.3 `GET /api/v1/executions/{execution_id}`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-16-03` |
| Method / Path | `GET /api/v1/executions/{execution_id}` |
| Handler | `executions.py::get_execution` |
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

- HTTP **200**。Body schema: `ExecutionResponse`。

| 項目（wire） | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `execution_id` | `str` | 必須 | 不可 | — |
| `project_id` | `str` | 必須 | 不可 | — |
| `dataset_version_id` | `str` | 必須 | 不可 | — |
| `analysis_family` | `str` | 必須 | 不可 | — |
| `input_graph_version_id` | `str \| None` | 必須 | 許可 | — |
| `input_result_id` | `str \| None` | 必須 | 許可 | — |
| `snapshot_schema_version` | `str` | 必須 | 不可 | — |
| `batch_key` | `str` | 必須 | 不可 | — |
| `operation` | `str` | 必須 | 不可 | — |
| `algorithm_or_estimator` | `str` | 必須 | 不可 | — |
| `status` | `str` | 必須 | 不可 | — |
| `retry_count` | `int` | 必須 | 不可 | — |
| `requested_by` | `str` | 必須 | 不可 | — |
| `requested_at` | `datetime \| None` | 必須 | 許可 | — |
| `started_at` | `datetime \| None` | 必須 | 許可 | — |
| `finished_at` | `datetime \| None` | 必須 | 許可 | — |
| `last_error_summary` | `str \| None` | 必須 | 許可 | — |
| `analysis_mode` | `str \| None` | 任意 | 許可 | None |
| `scientific_warnings` | `list[dict[str, Any]]` | 任意 | 不可 | Field(default_factory=list) |
| `revision_context` | `dict[str, Any] \| None` | 任意 | 許可 | None |

**Response JSON構造例（schema由来の説明用）**

```json
{
  "execution_id": "{execution_id}",
  "project_id": "{project_id}",
  "dataset_version_id": "{dataset_version_id}",
  "analysis_family": "string",
  "input_graph_version_id": "{input_graph_version_id}",
  "input_result_id": "{input_result_id}",
  "snapshot_schema_version": "string",
  "batch_key": "string",
  "operation": "string",
  "algorithm_or_estimator": "string",
  "status": "string",
  "retry_count": 0,
  "requested_by": "string",
  "requested_at": "2026-11-17T00:00:00Z",
  "started_at": "2026-11-17T00:00:00Z",
  "finished_at": "2026-11-17T00:00:00Z",
  "last_error_summary": "string",
  "analysis_mode": "string",
  "scientific_warnings": [],
  "revision_context": {}
}
```

#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 対象がなく、ServiceがEntityNotFoundを送出する場合 | 共通Handler。Operationごとの到達は要確認 |

#### 根拠・未検証事項

- Router Source: `executions.py`（blob `c073974ed1bbd91161b67035850070c78a46e7da`）。Request DTO: `none`、Response Model: `ExecutionResponse`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.4 `GET /api/v1/executions/{execution_id}/prefill`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-16-04` |
| Method / Path | `GET /api/v1/executions/{execution_id}/prefill` |
| Handler | `executions.py::get_execution_prefill` |
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

- HTTP **200**。Body schema: `ExecutionPrefillResponse`。

| 項目（wire） | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `operation` | `str` | 必須 | 不可 | — |
| `dataset_version_id` | `str` | 必須 | 不可 | — |
| `input_graph_version_id` | `str \| None` | 必須 | 許可 | — |
| `input_result_id` | `str \| None` | 必須 | 許可 | — |
| `objective` | `str \| None` | 必須 | 許可 | — |
| `rationale` | `str \| None` | 必須 | 許可 | — |
| `analysis_spec` | `dict[str, Any]` | 必須 | 不可 | — |
| `algorithm_or_estimator` | `str` | 必須 | 不可 | — |
| `parameters` | `dict[str, Any]` | 必須 | 不可 | — |
| `random_seed` | `int \| None` | 必須 | 許可 | — |

**Response JSON構造例（schema由来の説明用）**

```json
{
  "operation": "string",
  "dataset_version_id": "{dataset_version_id}",
  "input_graph_version_id": "{input_graph_version_id}",
  "input_result_id": "{input_result_id}",
  "objective": "string",
  "rationale": "string",
  "analysis_spec": {},
  "algorithm_or_estimator": "string",
  "parameters": {},
  "random_seed": 0
}
```

#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 対象がなく、ServiceがEntityNotFoundを送出する場合 | 共通Handler。Operationごとの到達は要確認 |

#### 根拠・未検証事項

- Router Source: `executions.py`（blob `c073974ed1bbd91161b67035850070c78a46e7da`）。Request DTO: `none`、Response Model: `ExecutionPrefillResponse`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.5 `POST /api/v1/executions/{execution_id}/cancel`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-16-05` |
| Method / Path | `POST /api/v1/executions/{execution_id}/cancel` |
| Handler | `executions.py::cancel_execution` |
| Success Status | HTTP 204 |

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

- HTTP **204**。Body schema: なし（204 No Content）。

Response bodyなし。


#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 対象がなく、ServiceがEntityNotFoundを送出する場合 | 共通Handler。Operationごとの到達は要確認 |
| 409 | PROJECT_ARCHIVED / RESOURCE_IMMUTABLE / EXECUTION_STATE_CONFLICT | 対象がARCHIVED/FIXEDまたは遷移不適格で該当DomainErrorを送出する場合 | 適用可能なOperationのみ、到達は要確認 |

#### 根拠・未検証事項

- Router Source: `executions.py`（blob `c073974ed1bbd91161b67035850070c78a46e7da`）。Request DTO: `none`、Response Model: `未宣言`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.6 `POST /api/v1/executions/{execution_id}/retry`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-16-06` |
| Method / Path | `POST /api/v1/executions/{execution_id}/retry` |
| Handler | `executions.py::retry_execution` |
| Success Status | HTTP 204 |

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

- HTTP **204**。Body schema: なし（204 No Content）。

Response bodyなし。


#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 対象がなく、ServiceがEntityNotFoundを送出する場合 | 共通Handler。Operationごとの到達は要確認 |
| 409 | PROJECT_ARCHIVED / RESOURCE_IMMUTABLE / EXECUTION_STATE_CONFLICT | 対象がARCHIVED/FIXEDまたは遷移不適格で該当DomainErrorを送出する場合 | 適用可能なOperationのみ、到達は要確認 |

#### 根拠・未検証事項

- Router Source: `executions.py`（blob `c073974ed1bbd91161b67035850070c78a46e7da`）。Request DTO: `none`、Response Model: `未宣言`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

## 5. 検証状況

- Route/Method/Path: 6 件 Source確認。
- Request: Router/Pydanticモデルの静的制約を反映。Response: 型付きモデルは全Fieldを表記。Service無型応答は一部未確定。
- HTTP Contract Test: NOT_RUN。Endpoint詳細の完全性・認可・実行時エラー網羅は未検証。
- 元の`docs/wiki/requirement_definition/`への昇格: NOT_DONE。

## 6. 既存Domain・設計制約（旧仕様本文から保持）

以下は既存のDomain規範・補足情報を保持したもの。重複する旧Route一覧より§2（Source基準）を優先する。改訂前の原本文はGit Blob `2ee2b80400cd697ee0c9ea0d2ca22040c2fefece`で追跡可能。

### Execution Interface

現行branchには、canonical/common Execution APIとPredictive workflow向けProject-scoped APIが併存する。current snapshotはNavigation再構成を理由にこれらを暗黙統合・削除しない。

#### Canonical/common Execution Web API

| Method | Path | 用途 |
| --- | --- | --- |
| POST | `/projects/{project_id}/execution-batches` | canonical Execution batchを非同期submit |
| GET | `/projects/{project_id}/executions` | canonical + predictive family executionのproject list projection |
| GET | `/executions/{execution_id}` | canonical Execution詳細 |
| GET | `/executions/{execution_id}/prefill` | rerun/revision用prefill |
| POST | `/executions/{execution_id}/cancel` | cancel |
| POST | `/executions/{execution_id}/retry` | FAILEDをretry |

Batch submitの主要input:

```text
dataset_version_id
analysis_family
operation
analysis_spec
variants[].algorithm_or_estimator
variants[].parameters
variants[].random_seed
input_graph_version_id
input_result_id
code_version
runtime_versions
objective / rationale
base_execution_id / change_reason
```

Navigation Stageはrequired inputではない。

#### Canonical Execution response

Current response field:

```text
execution_id
project_id
dataset_version_id
analysis_family
input_graph_version_id
input_result_id
snapshot_schema_version
batch_key
operation
algorithm_or_estimator
status
retry_count
requested_by
requested_at
started_at
finished_at
last_error_summary
analysis_mode
scientific_warnings
revision_context
```

Status: `QUEUED / RUNNING / SUCCEEDED / FAILED / CANCELLED`。

#### Predictive workflow interface

Current Predictive workflowはExecutionPlanをfirst-class APIとして公開する。

| Method | Path | 用途 |
| --- | --- | --- |
| POST | `/projects/{project_id}/execution-plans` | `analysis_specification_id`からPlan作成 |
| GET | `/projects/{project_id}/execution-plans/{plan_id}` | Plan取得 |
| POST | `/projects/{project_id}/execution-plans/{plan_id}/validate` | Plan validation |
| POST | `/projects/{project_id}/executions` | `analysis_specification_id / execution_plan_id / seed`でpredictive Execution submit |
| GET | `/projects/{project_id}/executions/{execution_id}` | Predictive execution取得 |
| GET | `/projects/{project_id}/executions/{execution_id}/stages` | StageExecution一覧 |
| GET | `/projects/{project_id}/executions/{execution_id}/results` | Result一覧 |
| GET | `/projects/{project_id}/executions/{execution_id}/artifacts` | Artifact一覧 |
| GET | `/projects/{project_id}/executions/{execution_id}/lineage` | Lineage一覧 |
| POST | `/projects/{project_id}/executions/{execution_id}/cancel` | cancel |
| POST | `/projects/{project_id}/executions/{execution_id}/retry` | retry |
| POST | `/projects/{project_id}/executions/{execution_id}/rerun` | rerun |
| POST | `/projects/{project_id}/executions/{execution_id}/revise` | revised execution |
| GET | `/projects/{project_id}/executions/{execution_id}/prefill` | prefill |

#### Execution Plan / runtime Stage

`ExecutionPlan`は次を保持する。

```text
execution_plan_id
project_id
analysis_specification_id
analysis_family
plan_schema_version
planner_id / planner_version
stages
dependencies
plan_hash
created_at
```

`StageDefinition.stage_type`はruntime `StageType(namespace, name, version)`でありNavigation Stage IDではない。

Canonical `Execution`には`execution_plan_id`独立field/FKはない。Predictive/Exploratory current pathではexecution metadataとして`analysis_spec_json`内にplan/spec/view identityを保持し得る。この差を無視して、Navigation StageをExecutionPlanまたはExecutionの共通fieldとして追加しない。

**当該Interfaceの追加契約（関連Requirement）**

- **`FR-082`**：idempotency対象Commandでは`(project_id, command_scope, idempotency_key)`をauthorityとし、同一semantic requestをreplay、異なるrequestを`IDEMPOTENCY_CONFLICT`で拒否する
- **`FR-084`**：上流Artifactを下流Stage inputへ型付きでbindingする
- **`FR-085`**：未登録Runner、cycle、missing output、schema mismatchをPlan受付時に拒否する
- **`FR-087b`**：Execution `runtime_version_json`にAriadne code、Python、platform、machineおよび実際に利用したscientific library versionを保持する

## 7. 改訂記録

- 2026-11-17: 全23_10〜23_19共通フォーマットへ再構成。Request/Response/ErrorsをOperation別に記載し、Source確認と未検証を分離。
