# 23 API・インターフェース設計 — 初期価値検証版

- 文書状態: 初版
- 更新日: 2026-08-05
- 上位文書:
  - `10_要件定義.md`
  - `21_論理データ設計.md`
  - `22_プロダクト基本設計.md`
- 下位文書:
  - `30_詳細設計.md`
- 目的: Web App、Web API、Worker、Scientific CoreおよびCLIの間で交換する契約を定義する

## 1. 適用範囲

本書は次を定義する。

- Web API Endpoint
- Request / Response DTO
- Navigation Context
- Scientific Coreの入出力契約
- CLI Manifest schema
- validationとerror model
- 契約のversioning方針

DB Entityやclass内部構造は定義しない。

## 2. 共通規約

### 2.1 表記

- IDはUUID文字列で表現する
- 日時はUTCのRFC 3339文字列で表現する
- enumは大文字snake caseとする
- JSON objectの未知fieldは、初期版では原則rejectする
- Request内でEntity全体を複製せず、正本EntityのIDを参照する

### 2.2 Response envelope

成功Responseは、単一ResourceではResource本体を返す。List Responseは次の共通構造とする。

```json
{
  "items": [],
  "next_cursor": null
}
```

初期版の一覧はcursor paginationを基本とする。小規模な固定候補一覧はpaginationを省略してよい。

### 2.3 Idempotency

作成系Commandのうち、ネットワーク再送で重複作成が問題となるものは`Idempotency-Key` headerを受け付ける。

対象:

- Dataset Version登録開始
- Execution Batch受付
- Graph Version作成
- Result export

同一Project、同一Key、同一Request bodyの場合は同一結果を返す。bodyが異なる場合は`409 IDEMPOTENCY_CONFLICT`を返す。

## 3. Navigation Context

Navigation ContextはWeb App内の遷移用であり、正本データではない。URL path、query parameterまたはclient-side route stateで保持する。

### 3.1 Discovery開始Context

| Field | Type | Required | 説明 |
|---|---|---:|---|
| `project_id` | UUID | 1 | Project |
| `dataset_version_id` | UUID | 1 | 初期選択Dataset Version |
| `source_execution_id` | UUID |  | 再実行元Execution |

### 3.2 Inference開始Context

| Field | Type | Required | 説明 |
|---|---|---:|---|
| `project_id` | UUID | 1 | Project |
| `dataset_version_id` | UUID | 1 | 推論入力Dataset Version |
| `graph_version_id` | UUID | 1 | 推論入力Graph Version |
| `source_discovery_result_id` | UUID |  | 表示用source Result。正本はGraph Versionから取得する |

### 3.3 Result選択Context

| Field | Type | Required | 制約 |
|---|---|---:|---|
| `project_id` | UUID | 1 |  |
| `result_ids` | UUID[] | 1 | 2〜20件 |
| `comparison_mode` | enum | 1 | `DISCOVERY` / `ESTIMATION` |
| `return_workspace` | enum |  | `DISCOVERY` / `INFERENCE` / `RESULTS` |

### 3.4 再実行Context

| Field | Type | Required | 説明 |
|---|---|---:|---|
| `project_id` | UUID | 1 | Project |
| `source_execution_id` | UUID | 1 | 初期値取得元 |
| `target_workspace` | enum | 1 | `DISCOVERY` / `INFERENCE` |

分析条件はContextへ複製せず、source Executionのprefill APIから取得する。

## 4. Web API Endpoint

### 4.1 Project

| Method | Path | 用途 |
|---|---|---|
| POST | `/projects` | Project作成 |
| GET | `/projects/{project_id}` | Project取得 |
| PATCH | `/projects/{project_id}` | Project更新 |

### 4.2 Dataset Version

| Method | Path | 用途 |
|---|---|---|
| POST | `/projects/{project_id}/dataset-versions` | Dataset Version登録 |
| GET | `/projects/{project_id}/dataset-versions` | Project内一覧 |
| GET | `/dataset-versions/{dataset_version_id}` | metadata取得 |
| GET | `/dataset-versions/{dataset_version_id}/preview` | preview取得 |

### 4.3 Execution

| Method | Path | 用途 |
|---|---|---|
| POST | `/projects/{project_id}/execution-batches` | 複数Execution受付 |
| GET | `/projects/{project_id}/executions` | Execution一覧 |
| GET | `/executions/{execution_id}` | Execution取得 |
| GET | `/executions/{execution_id}/prefill` | 再実行用初期値取得 |
| POST | `/executions/{execution_id}/cancel` | cancel要求 |
| POST | `/executions/{execution_id}/retry` | 技術的retry要求 |

`execution-batches`はCommand endpointであり、Batchを正本Resourceとして作成しない。

### 4.4 Result・Comparison・Lineage

| Method | Path | 用途 |
|---|---|---|
| GET | `/executions/{execution_id}/results` | ExecutionのResult一覧 |
| GET | `/results/{result_id}` | Result取得 |
| POST | `/comparisons/query` | Result比較を生成 |
| GET | `/results/{result_id}/lineage` | Result起点Lineageを生成 |
| POST | `/results/{result_id}/export` | portable package生成 |

### 4.5 Graph Version

| Method | Path | 用途 |
|---|---|---|
| POST | `/projects/{project_id}/graph-versions` | ResultからGraph Version作成 |
| GET | `/projects/{project_id}/graph-versions` | 一覧 |
| GET | `/graph-versions/{graph_version_id}` | 取得 |
| PATCH | `/graph-versions/{graph_version_id}` | DRAFT更新 |
| POST | `/graph-versions/{graph_version_id}/fix` | FIXEDへ遷移 |

### 4.6 Annotation・Artifact

| Method | Path | 用途 |
|---|---|---|
| POST | `/projects/{project_id}/annotations` | Annotation作成 |
| PATCH | `/annotations/{annotation_id}` | Annotation更新 |
| GET | `/artifacts/{artifact_id}` | Artifact metadata取得 |
| GET | `/artifacts/{artifact_id}/download` | file取得 |

## 5. 主要Command DTO

### 5.1 Create Project

```json
{
  "name": "Sales improvement analysis",
  "topic": "Coupon and sales",
  "objective": "Estimate the causal effect of coupon delivery",
  "memo": null
}
```

Validation:

- `name`: 1〜200文字
- `topic`, `objective`: 各0〜4,000文字

### 5.2 Register Dataset Version

`multipart/form-data`を使用する。

| Part | Type | Required | 制約 |
|---|---|---:|---|
| `file` | binary | 1 | CSVまたはParquet。上限は運用設定 |
| `dataset_key` | string | 1 | Project内でDataset系列を表す |
| `version_label` | string | 1 | 1〜100文字 |
| `name` | string | 1 | 1〜200文字 |
| `source_note` | string |  | 0〜4,000文字 |

ResponseはDataset Version metadataを返す。

### 5.3 Create Execution Batch Request

```json
{
  "operation": "DISCOVERY",
  "dataset_version_id": "uuid",
  "input_graph_version_id": null,
  "objective": "Find candidate causal structures",
  "rationale": "Compare algorithms before selecting an estimation graph",
  "analysis_spec": {},
  "variants": [
    {
      "algorithm_or_estimator": "PC",
      "parameters": {"alpha": 0.01},
      "random_seed": 42
    }
  ]
}
```

| Field | Type | Required | 制約 |
|---|---|---:|---|
| `operation` | enum | 1 | `DISCOVERY` / `ESTIMATION` |
| `dataset_version_id` | UUID | 1 | Project所属 |
| `input_graph_version_id` | UUID | 条件付 | ESTIMATIONで必須、DISCOVERYで禁止 |
| `objective` | string |  | 0〜4,000文字 |
| `rationale` | string |  | 0〜8,000文字 |
| `analysis_spec` | object | 1 | operation別schema |
| `variants` | object[] | 1 | 1〜20件 |

各variantが1 Executionとなる。

Response:

```json
{
  "batch_key": "uuid",
  "executions": [
    {"execution_id": "uuid", "status": "QUEUED"}
  ]
}
```

### 5.4 Create Graph Version Request

```json
{
  "source_result_id": "uuid",
  "parent_graph_version_id": null,
  "name": "Selected graph v1",
  "graph": {},
  "edit_rationale": "Removed an edge inconsistent with temporal ordering",
  "fix_immediately": false
}
```

Validation:

- source Resultは`DISCOVERY_GRAPH`である
- source ResultとProjectが一致する
- parent指定時は同一Projectである
- graph schemaがgraph typeと整合する

### 5.5 Upsert Annotation Request

```json
{
  "target_result_id": "uuid",
  "target_graph_version_id": null,
  "statement": "AIPW result is selected as the primary estimate.",
  "rationale": "Stable estimate and acceptable balance diagnostics.",
  "assumptions": ["No unmeasured confounding"],
  "limitations": ["Limited overlap for high-value customers"]
}
```

制約:

- target ResultまたはGraph Versionのどちらか一方のみを指定する
- targetは同一Projectに属する
- `statement`は必須、1〜8,000文字

## 6. 主要Query / Response DTO

### 6.1 Execution Response

主要field:

- `execution_id`
- `project_id`
- `batch_key`
- `operation`
- `status`
- `algorithm_or_estimator`
- `requested_at`, `started_at`, `finished_at`
- `retry_count`
- `last_error_summary`

詳細取得時はExecution Snapshotを含める。List Responseではsnapshot本体を省略する。

### 6.2 Result Response

主要field:

- `result_id`
- `execution_id`
- `result_type`
- `scientific_status`
- `summary`
- `diagnostics`
- `warnings`
- `artifact_ids`

大きなpayloadはArtifact参照へ分離できる。

### 6.3 Comparison Query

```json
{
  "project_id": "uuid",
  "result_ids": ["uuid", "uuid"]
}
```

Response:

```json
{
  "operation": "ESTIMATION",
  "common_conditions": {},
  "changed_conditions": {},
  "result_differences": {},
  "warnings": [],
  "lineage_summary": []
}
```

Validation:

- 2〜20 Result
- 全Resultが同一Project
- DISCOVERYとESTIMATIONを混在させない

### 6.4 Lineage Response

```json
{
  "root_result_id": "uuid",
  "nodes": [
    {
      "node_type": "RESULT",
      "entity_id": "uuid",
      "label": "AIPW result",
      "summary": {}
    }
  ],
  "edges": [
    {
      "relation_type": "GENERATED_BY",
      "from_id": "uuid",
      "to_id": "uuid"
    }
  ]
}
```

## 7. operation別Analysis Spec

### 7.1 Discovery Analysis Spec

```json
{
  "feature_columns": ["coupon", "visits", "sales"],
  "constraints": {
    "required_edges": [],
    "forbidden_edges": [],
    "temporal_tiers": []
  },
  "expected_graph_type": null
}
```

### 7.2 Estimation Analysis Spec

```json
{
  "treatment": "coupon",
  "outcome": "sales",
  "estimand": "ATE",
  "target_population": null,
  "adjustment_set": ["past_sales", "member_rank"],
  "assumptions": ["No unmeasured confounding"],
  "inference_options": {}
}
```

## 8. Scientific Core Interface

Scientific CoreのinterfaceはPython objectまたは同等の型付き構造を使用する。Web API schemaと完全に同一である必要はないが、意味を一致させる。

### 8.1 Discovery Input

- dataset reference
- algorithm identifier
- parameter map
- feature columns
- graph constraints
- random seed

### 8.2 Discovery Output

- graph type
- nodes
- edges and endpoint semantics
- diagnostics
- scientific warnings
- artifact payload descriptors

### 8.3 Estimation Input

- dataset reference
- graph reference
- causal design
- estimator identifier
- parameter map
- random seed

### 8.4 Estimation Output

- scientific status
- estimate nullable
- standard error / confidence interval nullable
- diagnostics
- warnings
- artifact payload descriptors

### 8.5 Scientific Status

- `VALID`
- `NOT_IDENTIFIED`
- `INSUFFICIENT_OVERLAP`
- `INSUFFICIENT_SAMPLE`
- `ESTIMATION_UNRELIABLE`

## 9. CLI Interface

### 9.1 Commands

```text
ariadne discovery run --config <path>
ariadne inference run --config <path>
ariadne config validate --config <path>
```

具体的なoption名は実装時に確定してよいが、configはWeb/APIのAnalysis Specと意味的に一致させる。

### 9.2 Manifest Schema

```json
{
  "manifest_version": "1.0",
  "operation": "DISCOVERY",
  "dataset": {"content_hash": "...", "location": "..."},
  "graph": null,
  "algorithm_or_estimator": "PC",
  "parameters": {},
  "analysis_spec": {},
  "random_seed": 42,
  "code_version": "...",
  "runtime_versions": {},
  "scientific_status": "VALID",
  "result_summary": {},
  "artifacts": []
}
```

## 10. Error Model

### 10.1 Error Response

```json
{
  "error": {
    "code": "INVALID_ANALYSIS_SPEC",
    "message": "The estimation analysis specification is invalid.",
    "details": {},
    "request_id": "uuid"
  }
}
```

### 10.2 HTTP status

| HTTP | 用途 |
|---:|---|
| 400 | Request構造または基本validation不正 |
| 401 | 未認証 |
| 403 | Projectへの権限なし |
| 404 | Resourceなし、または参照不可 |
| 409 | status競合、固定済みGraph更新、idempotency競合 |
| 413 | upload上限超過 |
| 422 | ドメイン上の入力条件不正 |
| 500 | 未分類の技術障害 |
| 503 | Worker / Artifact Store等の一時的利用不能 |

科学的負結果はHTTP errorにしない。正常Response内の`scientific_status`で表現する。

### 10.3 主要Error Code

- `INVALID_ANALYSIS_SPEC`
- `PROJECT_BOUNDARY_VIOLATION`
- `GRAPH_ALREADY_FIXED`
- `INVALID_GRAPH_SEMANTICS`
- `EXECUTION_STATE_CONFLICT`
- `IDEMPOTENCY_CONFLICT`
- `ARTIFACT_HASH_MISMATCH`
- `UNSUPPORTED_ALGORITHM`
- `UNSUPPORTED_ESTIMATOR`

## 11. Contract Versioning

- Web APIはURL major versionを使用する: `/api/v1/...`
- backward compatibleなfield追加はminor変更として扱う
- enum追加はclient影響を評価する
- CLI Manifestは`manifest_version`を持つ
- Scientific Core interfaceはapplication adapterでversion差を吸収する
