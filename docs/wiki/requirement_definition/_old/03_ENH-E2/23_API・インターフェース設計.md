# 23 API・インターフェース設計 — 初期価値検証版 ENH-E2統合改定

- 文書状態: ENH-E2統合改定版
- 更新日: 2026-08-06
- 上位文書:
  - `10_要件定義.md`
  - `21_論理データ設計.md`
  - `22_プロダクト基本設計.md`
- 下位文書:
  - `30_詳細設計.md`
- 目的: Web App、Web API、Worker、Scientific CoreおよびCLIの間で交換する契約を定義する

> **要件定義書は常にシステムの正本である。**
>
> **実装、既存コード、DBスキーマ、API、UIまたはテスト結果から、要件定義書を逆生成・事後更新してはならない。**

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
- 本章以降のPath表記には、共通prefix `/api/v1` を付与する

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

```json
{
  "project_id": "uuid",
  "dataset_version_id": "uuid",
  "graph_version_id": "uuid",
  "source_result_id": "uuid-or-null",
  "prefill_execution_id": "uuid-or-null"
}
```

Identification開始時は`graph_version_id`を必須とし、`source_result_id`は不要とする。

Estimation、Refutation、Sensitivity開始時は対応する`input_result_id`をExecution Commandへ渡す。
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
| GET | `/projects` | Project一覧。既定`status=ACTIVE`、管理用途でstatus filter可 |
| GET | `/projects/{project_id}` | Project取得 |
| PATCH | `/projects/{project_id}` | ACTIVE Project更新 |
| DELETE | `/projects/{project_id}` | Project論理削除。`ACTIVE → ARCHIVED` |

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
| POST | `/api/v1/projects/{project_id}/execution-batches` | Operation別Execution Batch作成 |
| GET | `/api/v1/projects/{project_id}/executions/{execution_id}` | Execution取得 |
| POST | `/api/v1/projects/{project_id}/executions/{execution_id}/cancel` | Cancel要求 |
| POST | `/api/v1/projects/{project_id}/executions/{execution_id}/retry` | 技術的Retry |
| GET | `/api/v1/projects/{project_id}/executions/{execution_id}/prefill` | 再実行用Prefill |

対応Operation:

```text
DISCOVERY
IDENTIFICATION
ESTIMATION
REFUTATION
SENSITIVITY
```
### 4.4 Result・Comparison・Lineage

| Method | Path | 用途 |
|---|---|---|
| GET | `/api/v1/projects/{project_id}/results/{result_id}` | Result詳細 |
| POST | `/api/v1/projects/{project_id}/comparisons/query` | Result比較Projection |
| GET | `/api/v1/projects/{project_id}/graph-candidates` | Discovery ResultとGraph Versionの統合一覧 |
| GET | `/api/v1/projects/{project_id}/graph-candidates/{candidate_kind}/{candidate_id}` | Graph Candidate詳細 |
| POST | `/api/v1/projects/{project_id}/graph-candidate-comparisons/query` | 2件以上のGraph Candidate比較 |
| GET | `/api/v1/projects/{project_id}/results/{result_id}/lineage` | Result Lineage |
| GET | `/api/v1/projects/{project_id}/scientific-capabilities` | 利用可能な科学機能 |

Comparisonは同一Result Type等の比較可能条件を検証する。
### 4.5 Graph Version

| Method | Path | 用途 |
|---|---|---|
| POST | `/api/v1/projects/{project_id}/graph-versions` | Graph Version作成 |
| POST | `/api/v1/projects/{project_id}/graph-edit-drafts` | ResultまたはFIXED Graphから編集用DRAFT作成 |
| GET | `/api/v1/projects/{project_id}/graph-versions/{graph_version_id}` | Graph取得 |
| PATCH | `/api/v1/projects/{project_id}/graph-versions/{graph_version_id}` | DRAFT更新 |
| POST | `/api/v1/projects/{project_id}/graph-versions/{graph_version_id}/fix` | FIXED化 |

Graph Origin別にSource Result / Parent Graph制約を検証する。
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
  "operation": "IDENTIFICATION",
  "dataset_version_id": "uuid",
  "input_graph_version_id": "uuid",
  "input_result_id": null,
  "objective": "Identify the ATE",
  "rationale": "Campaign planning",
  "analysis_spec": {
    "schema_version": "causal-analysis-spec/2",
    "analysis_mode": "EXPLORATORY",
    "research_context": {},
    "causal_question": {},
    "causal_design": {},
    "operation_spec": {},
    "validation_override": null
  },
  "variants": [
    {
      "algorithm_or_estimator": "GRAPHICAL_BACKDOOR",
      "parameters": {},
      "random_seed": 42
    }
  ],
  "code_version": "git-sha",
  "runtime_versions": {}
}
```

**Operation別制約**

- DISCOVERY: Graph / Input Result禁止
- IDENTIFICATION: Dataset / Graph必須
- ESTIMATION: Identification Result必須
- REFUTATION / SENSITIVITY: Treatment Effect Result必須
### 5.4 Create Graph Version Request

```json
{
  "source_result_id": null,
  "parent_graph_version_id": null,
  "graph_origin": "USER_DEFINED",
  "name": "Domain graph v1",
  "designated_outcome_node": "sales",
  "graph": {},
  "provenance": {
    "source_note": "Defined from domain knowledge"
  },
  "edit_rationale": null,
  "fix_immediately": false
}
```

Graph Origin:

```text
DISCOVERED
CONSTRAINT_ADJUSTED
USER_DEFINED
IMPORTED
USER_EDITED
```
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

```json
{
  "result_id": "uuid",
  "execution_id": "uuid",
  "result_type": "IDENTIFICATION_RESULT",
  "scientific_status": "IDENTIFIED",
  "summary": {},
  "payload": {},
  "diagnostics": {},
  "warnings": [],
  "artifact_ids": []
}
```

一覧取得では`payload`を省略できる。

科学的負結果も通常のResult Responseとして返す。
### 6.3 Comparison Query

```json
{
  "result_ids": ["uuid-1", "uuid-2"]
}
```

Response:

```json
{
  "result_type": "TREATMENT_EFFECT_RESULT",
  "common_conditions": {},
  "changed_conditions": {},
  "result_differences": [],
  "warnings": [],
  "lineage_summary": []
}
```

比較可能条件を満たさない場合は`INCOMPARABLE` Warningを返す。
### 6.4 Lineage Response

```json
{
  "root_result_id": "uuid",
  "nodes": [],
  "edges": [],
  "warnings": []
}
```

Node Type:

- PROJECT
- DATASET_VERSION
- EXECUTION
- RESULT
- GRAPH_VERSION
- ARTIFACT
- ANNOTATION

`input_result_id`、Graph Source / Parentを再帰追跡し、Cycleを検出する。
## 7. Operation別Analysis Spec

### 7.1 共通構造

```json
{
  "schema_version": "causal-analysis-spec/2",
  "analysis_mode": "EXPLORATORY",
  "research_context": {},
  "causal_question": {},
  "causal_design": {},
  "operation_spec": {},
  "validation_override": null
}
```

未知FieldをRejectする。

### 7.2 Discovery Analysis Spec

- Feature Set
- Graph Constraint
- Algorithm Configuration
- Expected Graph Type
- Stability / Bootstrap Option

### 7.3 Identification Analysis Spec

```json
{
  "causal_design": {
    "identification_strategy": "BACKDOOR",
    "adjustment_set": ["x1", "x2"],
    "assumptions": []
  },
  "operation_spec": {
    "allow_partial_identification": false
  }
}
```

### 7.4 Estimation Analysis Spec

```json
{
  "operation_spec": {
    "estimator": "AIPW",
    "inference_options": {
      "confidence_level": 0.95
    }
  }
}
```

### 7.5 Refutation Analysis Spec

```json
{
  "operation_spec": {
    "method": "PLACEBO_TREATMENT",
    "repetitions": 100
  }
}
```

### 7.6 Sensitivity Analysis Spec

```json
{
  "operation_spec": {
    "dimension": "PROPENSITY_CLIPPING",
    "values": [0.01, 0.025, 0.05]
  }
}
```

### 7.7 Validation Override

```json
{
  "reason": "Scientific justification",
  "actor": "user-id",
  "warning_codes": ["LIMITED_OVERLAP"]
}
```
## 8. Scientific Core Interface

### 8.1 Product Port

```python
class ScientificCorePort(Protocol):
    def run_discovery(...) -> list[ScientificResultDescriptor]: ...
    def run_identification(...) -> list[ScientificResultDescriptor]: ...
    def run_estimation(...) -> list[ScientificResultDescriptor]: ...
    def run_refutation(...) -> list[ScientificResultDescriptor]: ...
    def run_sensitivity(...) -> list[ScientificResultDescriptor]: ...
```

### 8.2 Scientific Result Descriptor

```python
@dataclass(frozen=True)
class ScientificResultDescriptor:
    result_type: ResultType
    scientific_status: ScientificStatus
    summary: dict[str, Any]
    payload: dict[str, Any]
    diagnostics: dict[str, Any]
    warnings: list[dict[str, Any]]
    artifacts: list[ArtifactDescriptor]
```

### 8.3 Result Type / Status

Result TypeとScientific Statusの対応は`21_論理データ設計.md`に従う。

### 8.4 Boundary

- External Library型をProduct Domainへ返さない
- DB RepositoryをScientific Coreへ渡さない
- Scientific Negative OutcomeをTechnical Exceptionへ変換しない
- Backend名 / Version / WarningをResultまたはArtifact Metadataへ保存する
## 9. CLI Interface

### 9.1 Commands

```text
ariadne-discover --config <path>
ariadne-identify --config <path>
ariadne-estimate --config <path>
ariadne-refute --config <path>
ariadne-sensitivity --config <path>
```

### 9.2 Manifest Schema

- Manifest Schema Version
- Operation
- Analysis Mode
- Causal Question Hash
- Dataset / Graph Hash
- Graph Origin
- Upstream Result Reference
- Method / Parameter / Seed
- Code / Runtime / Backend Version
- Scientific Status
- Artifact List / Hash

CLIはWeb Execution IDを生成しない。
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

```text
ENTITY_NOT_FOUND
PROJECT_BOUNDARY_VIOLATION
INVALID_STATE_TRANSITION
INVALID_ANALYSIS_SPEC
GRAPH_ALREADY_FIXED
INVALID_GRAPH_SEMANTICS
UNSUPPORTED_ALGORITHM
UNSUPPORTED_ESTIMATOR
UPSTREAM_RESULT_REQUIRED
UPSTREAM_RESULT_INCOMPATIBLE
IDENTIFICATION_NOT_ACCEPTABLE
DATA_ELIGIBILITY_FAILED
OVERRIDE_REASON_REQUIRED
UNSUPPORTED_IDENTIFICATION_STRATEGY
UNSUPPORTED_REFUTATION_METHOD
UNSUPPORTED_SENSITIVITY_METHOD
SNAPSHOT_SCHEMA_UNSUPPORTED
GRAPH_ORIGIN_INVALID
INCOMPARABLE_RESULTS
```

科学的負結果をHTTP Errorにしない。

Input Contract、Project境界、State Conflictは`422`または`409`へ変換する。
## 11. Contract Versioning

### 11.1 Version対象

- Web API
- Analysis Spec
- Snapshot Canonicalization
- Artifact / Manifest Schema
- Scientific Backend Adapter

### 11.2 Contract Version

```text
API: v1
Analysis Spec: causal-analysis-spec/2
ENH-E2では両versionを維持する
```

### 11.3 互換方針

- 既存DISCOVERY / ESTIMATIONの意味を保持する
- 旧DTOまたは旧DB Schemaを要件へ昇格しない
- 未対応FieldをSilent Ignoreしない
- Breaking Changeが必要な場合、要件変更、設計更新、Contract Version更新の順で処理する
- 実装から要件定義書を更新しない


## 12. ENH-E2追加Contract

### 12.1. Project論理削除

```http
DELETE /api/v1/projects/{project_id}
```

意味:

- ACTIVEの場合、ARCHIVEDへ変更する
- 既にARCHIVEDの場合、idempotentに成功する
- Projectおよび下位Entityを物理削除しない
- Responseは`204 No Content`とする

ARCHIVED Projectへのwriteは`409 PROJECT_ARCHIVED`を返す。

### 12.2. Discovery Analysis Spec

```json
{
  "operation_spec": {
    "feature_columns": ["coupon", "visits", "sales"],
    "designated_outcome_node": "sales",
    "constraints": {
      "required_edges": [],
      "forbidden_edges": [],
      "temporal_tiers": []
    }
  }
}
```

Validation:

- FeatureはDataset schemaに存在する
- 重複しない
- OutcomeはDataset schemaとFeature columnsに存在する

### 12.3. Graph Version Response

追加field:

```json
{
  "designated_outcome_node": "sales",
  "allowed_actions": {
    "can_edit": false,
    "can_fix": false,
    "can_create_child": true,
    "can_use_for_inference": true,
    "disabled_reasons": []
  }
}
```

`allowed_actions`はQuery Responseへ含めてもよく、正本Entity属性として保存しない。

### 12.4. Create Graph Edit Draft

```http
POST /api/v1/projects/{project_id}/graph-edit-drafts
```

```json
{
  "base_candidate_kind": "GRAPH_VERSION",
  "base_candidate_id": "uuid",
  "change_kind": "USER_EDITED",
  "name": "Edited graph",
  "edit_rationale": "Remove implausible edge"
}
```

規則:

- baseがFIXED Graph Versionなら子DRAFTを作成する
- baseがDiscovery Resultなら同一内容のDISCOVERED rootを確保し、その子DRAFTを作成する
- Algorithm Outputを変更しない
- Parentは同一ProjectかつFIXED

### 12.5. Graph Candidate Response

```json
{
  "candidate_kind": "GRAPH_VERSION",
  "candidate_id": "uuid",
  "source_result_id": "uuid",
  "graph_version_id": "uuid",
  "parent_graph_version_id": null,
  "graph_type": "DAG",
  "graph_origin": "DISCOVERED",
  "version_status": "FIXED",
  "scientific_status": null,
  "fixed": true,
  "designated_outcome_node": "sales",
  "summary": {
    "node_count": 8,
    "edge_count": 11
  },
  "allowed_actions": {}
}
```

### 12.6. Graph Candidate Comparison Request

```json
{
  "candidate_refs": [
    {"candidate_kind": "DISCOVERY_RESULT", "candidate_id": "uuid-1"},
    {"candidate_kind": "GRAPH_VERSION", "candidate_id": "uuid-2"}
  ]
}
```

2件以上を必須とする。

Response:

- candidate tabs
- Graph Document
- compatibility
- common nodes
- added / removed / endpoint-changed edges
- non-comparable reasons

### 12.7. Inference Outcome Validation

Web AppはGraph Versionの`designated_outcome_node`をCausal Questionへ設定する。APIは次を検証する。

```text
analysis_spec.causal_question.outcome
= input_graph_version.designated_outcome_node
```

不一致は`409 GRAPH_OUTCOME_MISMATCH`、未指定は`422 GRAPH_OUTCOME_REQUIRED`とする。

### 12.8. 追加Error Code

| Code | HTTP | 意味 |
|---|---:|---|
| `PROJECT_ARCHIVED` | 409 | ARCHIVED Projectへのwrite |
| `GRAPH_PARENT_NOT_FIXED` | 409 | DRAFTをParentに指定 |
| `GRAPH_FIXED_IMMUTABLE` | 409 | FIXED Graph直接更新 |
| `GRAPH_OUTCOME_REQUIRED` | 422 | FIXED GraphのOutcome未指定 |
| `GRAPH_OUTCOME_MISMATCH` | 409 | Inference Outcome不一致 |
| `GRAPH_CANDIDATE_NOT_COMPARABLE` | 422 | 構造差分不能。個別表示は可能 |
| `INVALID_GRAPH_EDIT_BASE` | 409 | 編集元Candidateが不適格 |
