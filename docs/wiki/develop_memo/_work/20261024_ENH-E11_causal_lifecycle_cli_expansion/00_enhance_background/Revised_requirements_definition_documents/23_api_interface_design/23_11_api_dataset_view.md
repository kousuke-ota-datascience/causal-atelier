# 23_11_api_dataset_view — Dataset Version Web API仕様

## 1. API概要

- 対象: Dataset Version のHTTP契約。
- Base path: `/api/v1`。
- 本改訂はOwner採用の**Operation単位Request/Response/Errors定義**を対象とする。実行時PASSや要件変更を含まない。
- Source snapshot: `89d4f135d8c680805731934e715b079ea0f72f2b`。Currentに対する未検証事項を明示する。

## 2. エンドポイント一覧

| No. | HTTP | Path | Handler | HTTP Success |
|---:|---|---|---|---|
| 1 | `POST` | `/api/v1/projects/{project_id}/dataset-versions` | `register_dataset_version` | `201` |
| 2 | `GET` | `/api/v1/projects/{project_id}/dataset-versions` | `list_dataset_versions` | `200` |
| 3 | `GET` | `/api/v1/dataset-versions/{dataset_version_id}` | `get_dataset_version` | `200` |
| 4 | `GET` | `/api/v1/dataset-versions/{dataset_version_id}/preview` | `preview_dataset` | `200` |

## 3. 共通Error Response形式

CURRENTのDomainError/RequestValidationError Handlerは`application/problem+json`ではなく、以下のJSON envelope。

```json
{"error":{"code":"INVALID_REQUEST","message":"Request validation failed.","details":{},"request_id":"{request_id}"}}
```

共通Handlerに定義されたErrorがすべてのOperationから発生するとは限らない。下表の条件付きErrorはテストPASS済みという意味ではない。

## 4. エンドポイント詳細

### 4.1 `POST /api/v1/projects/{project_id}/dataset-versions`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-11-01` |
| Method / Path | `POST /api/v1/projects/{project_id}/dataset-versions` |
| Handler | `dataset_versions.py::register_dataset_version` |
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

**Request Body / Field定義**

Content-Type: `multipart/form-data`（JSONではない）

| Field | 型 | 必須 | 制約 |
|---|---|---|---|
| `dataset_key` | `str` | 必須 | Router Form定義 |
| `name` | `str` | 必須 | Router Form定義 |
| `version_label` | `str` | 必須 | Router Form定義 |
| `source_note` | `str | None` | 任意 | Router Form定義 |
| `file` | `UploadFile` | 必須 | CSV/Parquet拡張子・空ファイル禁止 |

#### Response

- HTTP **201**。Body schema: `DatasetVersionResponse`。

| 項目 | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `dataset_version_id` | `str` | 必須 | 不可 | — |
| `project_id` | `str` | 必須 | 不可 | — |
| `source_artifact_id` | `str` | 必須 | 不可 | — |
| `dataset_key` | `str` | 必須 | 不可 | — |
| `name` | `str` | 必須 | 不可 | — |
| `version_label` | `str` | 必須 | 不可 | — |
| `content_hash` | `str` | 必須 | 不可 | — |
| `column_schema` | `dict[str, Any]` | 必須 | 不可 | Field(alias="schema") |
| `profile_summary` | `dict[str, Any]` | 必須 | 不可 | — |
| `row_count` | `int` | 必須 | 不可 | — |
| `column_count` | `int` | 必須 | 不可 | — |
| `source_note` | `str \| None` | 必須 | 許可 | — |
| `created_at` | `datetime \| None` | 必須 | 許可 | — |

**Response JSON構造例（説明用）**

```json
{
  "dataset_version_id": "{dataset_version_id}",
  "project_id": "{project_id}",
  "source_artifact_id": "{source_artifact_id}",
  "dataset_key": "string",
  "name": "string",
  "version_label": "string",
  "content_hash": "string",
  "column_schema": {},
  "profile_summary": {},
  "row_count": 0,
  "column_count": 0,
  "source_note": "string",
  "created_at": "2026-11-17T00:00:00Z"
}
```

#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗した場合 | 共通Handler |
| 400 / 409 | IDEMPOTENCY_KEY_REQUIRED / IDEMPOTENCY_CONFLICT | Key欠落／同一Key・異なる要求内容 | IdempotencyService |
| 404 | ENTITY_NOT_FOUND | 指定Resourceがない・別Projectである等、ServiceがEntityNotFoundを送出 | Handlerで確定、実到達は要確認 |
| 409 | PROJECT_ARCHIVED / RESOURCE_IMMUTABLE | ARCHIVEDまたはFIXEDに対する不適格変更の際、該当例外を送出した場合 | Handlerで確定、Operationごとの到達は要確認 |
| 422 | INVALID_DATASET_FILE | CSV/Parquet拡張子違反、空ファイル、parse失敗、列名不正 | Router実装 |

#### 根拠・未検証事項

- Router Source: `dataset_versions.py`（blob `1b0a202a4fb8b6f43248eaa7cf577c4d8c05676c`）。Request DTO: `none`、Response Model: `DatasetVersionResponse`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.2 `GET /api/v1/projects/{project_id}/dataset-versions`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-11-02` |
| Method / Path | `GET /api/v1/projects/{project_id}/dataset-versions` |
| Handler | `dataset_versions.py::list_dataset_versions` |
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

- HTTP **200**。Body schema: `DatasetVersionListResponse`。

| 項目 | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `items` | `list[DatasetVersionResponse]` | 必須 | 不可 | — |
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
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗した場合 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 指定Resourceがない・別Projectである等、ServiceがEntityNotFoundを送出 | Handlerで確定、実到達は要確認 |

#### 根拠・未検証事項

- Router Source: `dataset_versions.py`（blob `1b0a202a4fb8b6f43248eaa7cf577c4d8c05676c`）。Request DTO: `none`、Response Model: `DatasetVersionListResponse`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.3 `GET /api/v1/dataset-versions/{dataset_version_id}`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-11-03` |
| Method / Path | `GET /api/v1/dataset-versions/{dataset_version_id}` |
| Handler | `dataset_versions.py::get_dataset_version` |
| Success Status | HTTP 200 |

#### Request

**Path parameters**

| 項目 | 型 | 必須 |
|---|---|---|
| `dataset_version_id` | string | 必須 |

**Query parameters**

なし

**Headers**

Router固有の必須Header宣言なし

**Request Body / Field定義**

Request JSON Bodyなし（Router未定義）。

#### Response

- HTTP **200**。Body schema: `DatasetVersionResponse`。

| 項目 | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `dataset_version_id` | `str` | 必須 | 不可 | — |
| `project_id` | `str` | 必須 | 不可 | — |
| `source_artifact_id` | `str` | 必須 | 不可 | — |
| `dataset_key` | `str` | 必須 | 不可 | — |
| `name` | `str` | 必須 | 不可 | — |
| `version_label` | `str` | 必須 | 不可 | — |
| `content_hash` | `str` | 必須 | 不可 | — |
| `column_schema` | `dict[str, Any]` | 必須 | 不可 | Field(alias="schema") |
| `profile_summary` | `dict[str, Any]` | 必須 | 不可 | — |
| `row_count` | `int` | 必須 | 不可 | — |
| `column_count` | `int` | 必須 | 不可 | — |
| `source_note` | `str \| None` | 必須 | 許可 | — |
| `created_at` | `datetime \| None` | 必須 | 許可 | — |

**Response JSON構造例（説明用）**

```json
{
  "dataset_version_id": "{dataset_version_id}",
  "project_id": "{project_id}",
  "source_artifact_id": "{source_artifact_id}",
  "dataset_key": "string",
  "name": "string",
  "version_label": "string",
  "content_hash": "string",
  "column_schema": {},
  "profile_summary": {},
  "row_count": 0,
  "column_count": 0,
  "source_note": "string",
  "created_at": "2026-11-17T00:00:00Z"
}
```

#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗した場合 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 指定Resourceがない・別Projectである等、ServiceがEntityNotFoundを送出 | Handlerで確定、実到達は要確認 |

#### 根拠・未検証事項

- Router Source: `dataset_versions.py`（blob `1b0a202a4fb8b6f43248eaa7cf577c4d8c05676c`）。Request DTO: `none`、Response Model: `DatasetVersionResponse`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.4 `GET /api/v1/dataset-versions/{dataset_version_id}/preview`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-11-04` |
| Method / Path | `GET /api/v1/dataset-versions/{dataset_version_id}/preview` |
| Handler | `dataset_versions.py::preview_dataset` |
| Success Status | HTTP 200 |

#### Request

**Path parameters**

| 項目 | 型 | 必須 |
|---|---|---|
| `dataset_version_id` | string | 必須 |

**Query parameters**

| 項目 | 型 | default |
|---|---|---|
| `limit` | `int` | `20` |

**Headers**

Router固有の必須Header宣言なし

**Request Body / Field定義**

Request JSON Bodyなし（Router未定義）。

#### Response

- HTTP **200**。Body schema: `DatasetPreviewResponse`。

| 項目 | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `dataset_version_id` | `str` | 必須 | 不可 | — |
| `columns` | `list[str]` | 必須 | 不可 | — |
| `rows` | `list[dict[str, Any]]` | 必須 | 不可 | — |
| `limit` | `int` | 必須 | 不可 | — |

**Response JSON構造例（説明用）**

```json
{
  "dataset_version_id": "{dataset_version_id}",
  "columns": [],
  "rows": [],
  "limit": 0
}
```

#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗した場合 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 指定Resourceがない・別Projectである等、ServiceがEntityNotFoundを送出 | Handlerで確定、実到達は要確認 |

#### 根拠・未検証事項

- Router Source: `dataset_versions.py`（blob `1b0a202a4fb8b6f43248eaa7cf577c4d8c05676c`）。Request DTO: `none`、Response Model: `DatasetPreviewResponse`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

## 5. 検証状況

- Route/Method/Path: 4 件 Source確認。
- Request: Router/Pydanticモデルの静的制約を反映。Response: 型付きモデルは全Fieldを表記。Service無型応答は一部未確定。
- HTTP Contract Test: NOT_RUN。Endpoint詳細の完全性・認可・実行時エラー網羅は未検証。
- 元の`docs/wiki/requirement_definition/`への昇格: NOT_DONE。

## 6. 既存Domain・設計制約（旧仕様本文から保持）

以下は既存のDomain規範・補足情報を保持したもの。重複する旧Route一覧より§2（Source基準）を優先する。改訂前の原本文はGit Blob `871af739f0a1d8ef78b004cb5cc1f81c9c87b7d8`で追跡可能。

### Dataset / Analysis View API

Dataset Version / Analysis ViewはFamily横断のProject-level analytical inputである。

#### DatasetVersion

Current public routes:

| Method | Path | 用途 |
| --- | --- | --- |
| POST | `/projects/{project_id}/dataset-versions` | CSV/Parquet Dataset登録 |
| GET | `/projects/{project_id}/dataset-versions` | Project内Dataset一覧 |
| GET | `/dataset-versions/{dataset_version_id}` | Dataset metadata取得 |
| GET | `/dataset-versions/{dataset_version_id}/preview` | preview取得。default limit 20 |

Dataset responseの主要field:

```text
dataset_version_id
project_id
source_artifact_id
dataset_key
name
version_label
content_hash
schema
profile_summary
row_count
column_count
source_note
created_at
```

現行実装に`/dataset-versions/{id}/profile`専用endpointはない。profile summaryはDataset metadata response内の`profile_summary`として取得する。

#### AnalysisView

Current public routes:

| Method | Path | 用途 |
| --- | --- | --- |
| POST | `/projects/{project_id}/analysis-views` | DRAFT作成 |
| GET | `/projects/{project_id}/analysis-views` | 一覧 |
| GET | `/projects/{project_id}/analysis-views/{analysis_view_id}` | 取得 |
| PATCH | `/projects/{project_id}/analysis-views/{analysis_view_id}` | DRAFT更新 |
| POST | `/projects/{project_id}/analysis-views/{analysis_view_id}/validate` | schema/semantic validation |
| POST | `/projects/{project_id}/analysis-views/{analysis_view_id}/fix` | FIXED化 |

AnalysisView responseは`analysis_view_id / project_id / source_dataset_version_id / view_key / version_number / name / status / schema_version / spec / content_hash / manifest / created_by / created_at / fixed_at`を返す。

Current contractでは`POST/PATCH/validate/fix`の全boundaryで同じtyped filter validatorを利用する。Mismatch responseのcanonical error codeは`FILTER_TYPE_MISMATCH`。

Compatibility summary:

| logical type | allowed operator |
| --- | --- |
| BOOLEAN | `EQ, NE, IN, NOT_IN, IS_NULL, NOT_NULL` |
| INTEGER / REAL / DATETIME | `EQ, NE, LT, LTE, GT, GTE, IN, NOT_IN, IS_NULL, NOT_NULL` |
| TEXT | `EQ, NE, IN, NOT_IN, IS_NULL, NOT_NULL` |
| OTHER | `IS_NULL, NOT_NULL` |

`IS_NULL/NOT_NULL`はvalueなし、`IN/NOT_IN`はnon-empty list。DATETIMEはISO-8601、INTEGERはbooleanを許容せず、REALはfinite numeric。`time_cutoff`はDATETIME + `LT/LTE`。

Family tab切替だけでDatasetVersionやAnalysisViewを複製しない。

**当該Interfaceの追加契約（関連Requirement）**

- **`FR-015`**：AnalysisViewのsource Dataset logical type × operator × value compatibilityをdomain/application validationで検証し、type mismatchを`FILTER_TYPE_MISMATCH`として返す

## 7. 改訂記録

- 2026-11-17: 全23_10〜23_19共通フォーマットへ再構成。Request/Response/ErrorsをOperation別に記載し、Source確認と未検証を分離。
