# 23_11_api_dataset_view


---

## 5. Web API Interface

### 5.2 Dataset / Analysis View API

Dataset Version / Analysis ViewはFamily横断のProject-level analytical inputである。

#### 5.2.1 DatasetVersion

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

#### 5.2.2 AnalysisView

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

## PREP-01: Router operation source inventory

Evidence: dataset_versions.py source blob 1b0a202a4fb8b6f43248eaa7cf577c4d8c05676c. Static decorator inventory only; /api/v1 is the app router prefix. 200* = default declared FastAPI code, not a runtime assertion.

| HTTP | Route | Handler | Declared success | Response model |
| --- | --- | --- | --- | --- |
| POST | `/api/v1/projects/{project_id}/dataset-versions` | `register_dataset_version` | 201 | DatasetVersionResponse |
| GET | `/api/v1/projects/{project_id}/dataset-versions` | `list_dataset_versions` | 200* | DatasetVersionListResponse |
| GET | `/api/v1/dataset-versions/{dataset_version_id}` | `get_dataset_version` | 200* | DatasetVersionResponse |
| GET | `/api/v1/dataset-versions/{dataset_version_id}/preview` | `preview_dataset` | 200* | DatasetPreviewResponse |

Observed 4 operations. Identity/path is DEFINED from the router; request DTO, auth, lifecycle, error mapping, idempotency, compatibility and operation-specific tests remain NOT_SPECIFIED until source/DTO/service/OpenAPI verification. This annex is not a complete Contract, nor an Independent Verification PASS.

## PREP-01 — DatasetVersion全4 EndpointのRequest / Response / Errors（Owner採用 2026-11-17）

**Source:** `routers/dataset_versions.py`, `schemas/__init__.py`, `error_handlers.py`, `idempotency.py`。全Pathは `/api/v1` 以下。ここでは4 Router Operationを記載する。既存§5.2.2のAnalysisViewとRouter棚卸しの対象が異なるため、**AnalysisView 6 Operationsを本4件の実装済みRouterとは認定しない**。API契約のHTTP エラー形式は `{"error":{"code":string,"message":string,"details":object,"request_id":string}}` であり、Notionサンプルのproblem+jsonはCURRENTではない。

### OP-DATASET-01 — `POST /api/v1/projects/{project_id}/dataset-versions`

| 項目 | CURRENT 契約 |
|---|---|
| HTTP success | 201 + `DatasetVersionResponse` |
| Path | `project_id:string` (必須) |
| Content type | **multipart/form-data**、JSONではない |
| Header | `Idempotency-Key:string`（Router引数optionalだがServiceが非空必須） |
| Body | `dataset_key:string`、`name:string`、`version_label:string`はForm必須。 `source_note:string|null`はForm任意。 `file:UploadFile`は必須 |
| File constraints | 拡張子 `.csv` または `.parquet`、空ファイル不可、parseable、1列以上、非空・重複なしの列名 |
| Idempotency | same `(project_id, dataset-version, key)` + same semantic request hash → recorded response replay。別payload → conflict |

**Response fields:** `dataset_version_id:string`, `project_id:string`, `source_artifact_id:string`, `dataset_key:string`, `name:string`, `version_label:string`, `content_hash:string`, `schema:object`（Pydantic内部名`column_schema`のalias）、`profile_summary:object`, `row_count:int`, `column_count:int`, `source_note:string|null`, `created_at:datetime|null`。ここで `schema` はJSON property名であり `column_schema` ではない。

**Error mappings confirmed at shared handler:** 400 `INVALID_REQUEST`（Form/Pathのvalidation）、400 `IDEMPOTENCY_KEY_REQUIRED`（空/欠落key）、409 `IDEMPOTENCY_CONFLICT`（key再利用payload不一致）、409 `PROJECT_ARCHIVED`（archive Project）、422 `INVALID_DATASET_FILE`（拡張子/parse/列）、422 `INVALID_DATASET_METADATA`（domain metadataに該当した場合）。その他の実際の到達可能性、authは未検証。

### OP-DATASET-02 — `GET /api/v1/projects/{project_id}/dataset-versions`

| 項目 | CURRENT 契約 |
|---|---|
| Request | 必須path `project_id:string`。Query/Body無し（Router宣言） |
| Success | 200 `DatasetVersionListResponse` |
| Response | `items:DatasetVersionResponse[]`、`next_cursor:string|null`（model default null） |
| Errors | 404 `ENTITY_NOT_FOUND` / 409 `PROJECT_ARCHIVED`等はService送出次第。Operation別の実到達はUNVERIFIED |

### OP-DATASET-03 — `GET /api/v1/dataset-versions/{dataset_version_id}`

| 項目 | CURRENT 契約 |
|---|---|
| Request | 必須path `dataset_version_id:string`。Query/Body無し |
| Success | 200 `DatasetVersionResponse`（全FieldはOP-DATASET-01参照） |
| Errors | 404 `ENTITY_NOT_FOUND` if Service raises EntityNotFound。その他はUNVERIFIED |

### OP-DATASET-04 — `GET /api/v1/dataset-versions/{dataset_version_id}/preview`

| 項目 | CURRENT 契約 |
|---|---|
| Request | 必須path `dataset_version_id:string`、Query `limit:int`（任意、default **20**） |
| Success | 200 `DatasetPreviewResponse` |
| Response | `dataset_version_id:string`, `columns:string[]`, `rows:object[]`, `limit:int` |
| Error | Queryの型不正→400 `INVALID_REQUEST`。Limit範囲やService権限/NotFoundはUNVERIFIED |
| Privacy | rowsは実データを含む。認可・機微列制限の実効確認は未完了。安全性PASSではない |

**Verification boundary:** 上記はRouter+DTO+Handlerの静的Source contractであり、Runtime Contract TestとAuth/Service完全性は未実施。HTTP 200はFastAPI defaultで、実稼働呼び出し結果ではない。ExtensionやDTO制約を未確認の追加規格へ書き換えない。
