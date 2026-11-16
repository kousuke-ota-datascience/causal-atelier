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
