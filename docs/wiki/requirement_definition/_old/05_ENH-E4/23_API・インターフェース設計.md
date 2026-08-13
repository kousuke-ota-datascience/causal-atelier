# 23 API・インターフェース設計 — ENH-E4 approved target snapshot

- 文書状態: ENH-E4 approved target requirement/design snapshot
- Baseline: corresponding approved pre-ENH-E4 requirement/design document
- Precedence: baseline normative text that conflicts with an approved ENH-E4 ADR / requirement / invariant / constraint is superseded by the ENH-E4 target contract.
- Implementation status: this document describes the approved target contract; it does not assert production implementation completion.
- 承認日時: 2026-08-07 13:06 JST
- 更新日: 2026-08-07
- 上位文書:
  - `10_要件定義.md`
  - `21_論理データ設計.md`
  - `22_プロダクト基本設計.md`
- API base: `/api/v1`

## 1. API原則

1. Resource IDとProject境界を明示する
2. 作成・実行Commandはidempotencyに対応する
3. payloadはschema versionを持つ
4. validation errorはfield pathとcodeを返す
5. async operationは`202 Accepted`とExecution参照を返す
6. UI専用の推測値を正本APIへ混入しない
7. Result payloadとArtifact downloadを分離する
8. Family固有Schemaを共通Envelopeへ埋め込む

## 2. Authentication / Authorization

Request context:

- `Authorization: Bearer <token>`（production）
- `X-User-Subject`（development only）
- `X-Request-ID`
- `Idempotency-Key`（対象Command）

Project role:

- `VIEWER`
- `ANALYST`
- `OPERATOR`

認可はRouterだけでなくApplication Serviceでも検証する。

## 3. Common Response

### 3.1. Error

```json
{
  "error": {
    "code": "PREDICTIVE_LEAKAGE_DETECTED",
    "message": "Feature availability violates prediction time.",
    "details": [
      {"path":"feature_spec.feature_columns[3]","code":"FUTURE_FEATURE","value":"post_purchase_flag"}
    ],
    "request_id": "uuid"
  }
}
```

代表status:

- 400 schema / semantic validation
- 401 unauthenticated
- 403 unauthorized
- 404 not found or hidden
- 409 state / idempotency conflict
- 413 size limit
- 422 analytical command invalid
- 429 capacity limit
- 500 unexpected failure

### 3.2. Pagination

```text
?limit=50&cursor=<opaque>&sort=-created_at
```

Responseは`items`、`next_cursor`を返す。

## 4. Project / Research Context API

| Method | Path | 用途 |
| --- | --- | --- |
| POST | /projects | Project作成 |
| GET | /projects | Project一覧 |
| GET | /projects/{project_id} | Project取得 |
| PATCH | /projects/{project_id} | ACTIVE Project更新 |
| DELETE | /projects/{project_id} | Project archive |
| POST | /projects/{project_id}/research-contexts | Context DRAFT作成 |
| GET | /projects/{project_id}/research-contexts | Context一覧 |
| GET | /projects/{project_id}/research-contexts/{context_id} | Context取得 |
| PATCH | /projects/{project_id}/research-contexts/{context_id} | DRAFT更新 |
| POST | /projects/{project_id}/research-contexts/{context_id}/fix | FIXED化 |
| GET | /projects/{project_id}/research-contexts/{context_id}/usage | 利用Analysis / Result取得 |

Create Context example:

```json
{
  "schema_version": "research-context/1",
  "context_key": "coupon-sales",
  "problem_statement": "Coupon policy may increase sales but cost and selection bias are uncertain.",
  "research_questions": ["Which customers are likely to purchase?", "What is the effect of coupon delivery?"],
  "significance": "Supports targeting and budget allocation.",
  "hypotheses": ["Coupon effect differs by prior purchase frequency."],
  "decision_context": {"decision_owner":"marketing","decision":"coupon policy"},
  "relations": []
}
```

## 5. Dataset / Analysis View API

| Method | Path | 用途 |
| --- | --- | --- |
| POST | /projects/{project_id}/dataset-versions | Dataset登録 |
| GET | /projects/{project_id}/dataset-versions | Dataset一覧 |
| GET | /projects/{project_id}/dataset-versions/{dataset_version_id} | metadata取得 |
| GET | /projects/{project_id}/dataset-versions/{dataset_version_id}/preview | 制限付きpreview |
| GET | /projects/{project_id}/dataset-versions/{dataset_version_id}/profile | 保存済みprofile |
| POST | /projects/{project_id}/analysis-views | Analysis View DRAFT作成 |
| GET | /projects/{project_id}/analysis-views | View一覧 |
| GET | /projects/{project_id}/analysis-views/{analysis_view_id} | View取得 |
| PATCH | /projects/{project_id}/analysis-views/{analysis_view_id} | DRAFT更新 |
| POST | /projects/{project_id}/analysis-views/{analysis_view_id}/validate | View検証 |
| POST | /projects/{project_id}/analysis-views/{analysis_view_id}/fix | FIXED化 |

Dataset uploadは`multipart/form-data`とし、`file`、`dataset_key`、`version_label`、`name`、`source_note`を受け取る。

## 6. Analysis Specification API

| Method | Path | 用途 |
| --- | --- | --- |
| POST | /projects/{project_id}/analysis-specifications | Family Specification DRAFT作成 |
| GET | /projects/{project_id}/analysis-specifications | Family / Context / Datasetで検索 |
| GET | /projects/{project_id}/analysis-specifications/{spec_id} | Specification取得 |
| PATCH | /projects/{project_id}/analysis-specifications/{spec_id} | DRAFT更新 |
| POST | /projects/{project_id}/analysis-specifications/{spec_id}/validate | 共通・Family検証 |
| POST | /projects/{project_id}/analysis-specifications/{spec_id}/fix | FIXED化 |
| POST | /projects/{project_id}/analysis-specifications/{spec_id}/revise | child DRAFT作成 |

Create common envelope:

```json
{
  "schema_version": "analysis-specification/1",
  "analysis_family": "PREDICTIVE",
  "research_context_version_id": "uuid",
  "dataset_version_id": "uuid",
  "analysis_view_id": "uuid-or-null",
  "analysis_mode": "CONFIRMATORY",
  "family_spec_schema_version": "predictive-analysis-spec/1",
  "family_spec": {}
}
```

## 7. Explore API

| Method | Path | 用途 |
| --- | --- | --- |
| POST | /projects/{project_id}/exploration/preview | 小規模同期集計 |
| POST | /projects/{project_id}/exploration/executions | 保存・非同期探索 |
| GET | /projects/{project_id}/exploration/capabilities | 利用可能chart / aggregation |
| POST | /projects/{project_id}/exploration/results/{result_id}/create-analysis-draft | Causal / Predictive draft作成 |

同期previewは保存済みResultではなく、row / time上限を設ける。保存または再現対象はExecutionを作成する。

## 8. Causal API

### 8.1. Graph

| Method | Path | 用途 |
| --- | --- | --- |
| POST | /projects/{project_id}/graph-versions | User-defined / Imported Graph作成 |
| GET | /projects/{project_id}/graph-candidates | Discovery ResultとGraph Versionの統合一覧 |
| POST | /projects/{project_id}/graph-candidate-comparisons | Graph比較 |
| POST | /projects/{project_id}/graph-versions/{graph_id}/create-child-draft | 編集DRAFT作成 |
| PATCH | /projects/{project_id}/graph-versions/{graph_id} | DRAFT編集 |
| POST | /projects/{project_id}/graph-versions/{graph_id}/fix | FIXED化 |

### 8.2. Scientific Capability

```text
GET /projects/{project_id}/causal/capabilities
```

algorithm、estimator、refutation method、sensitivity dimension、対応typeを返す。

因果実行は共通Execution APIを使用し、CAUSAL Specificationをsubmitする。

## 9. Predictive API

```text
GET /projects/{project_id}/predictive/capabilities
```

Response:

- task types
- split strategies
- preprocessing steps
- model registry entries
- metrics
- explanation methods
- compatibility matrix

予測実行も共通Execution APIを使用する。split previewは次を提供できる。

```text
POST /projects/{project_id}/predictive/split-validations
```

これは重いtrainingを行わず、partition overlap、class distribution、group / time boundaryを検証する。

## 10. Plan / Execution API

| Method | Path | 用途 |
| --- | --- | --- |
| POST | /projects/{project_id}/execution-plans | FIXED SpecificationからPlan生成 |
| GET | /projects/{project_id}/execution-plans/{plan_id} | Plan取得 |
| POST | /projects/{project_id}/execution-plans/{plan_id}/validate | DAG / Runner / contract検証 |
| POST | /projects/{project_id}/executions | Planをsubmit |
| GET | /projects/{project_id}/executions | Execution一覧 |
| GET | /projects/{project_id}/executions/{execution_id} | Execution詳細 |
| GET | /projects/{project_id}/executions/{execution_id}/stages | Stage一覧 |
| POST | /projects/{project_id}/executions/{execution_id}/cancel | cancel |
| POST | /projects/{project_id}/executions/{execution_id}/retry | technical retry |
| POST | /projects/{project_id}/executions/{execution_id}/rerun | 同一条件の新Execution |
| POST | /projects/{project_id}/executions/{execution_id}/revise | 変更条件prefill / child spec |
| GET | /projects/{project_id}/executions/{execution_id}/prefill | 再実行用snapshot |

Submit:

```json
{
  "execution_plan_id": "uuid",
  "requested_reason": "Compare baseline model",
  "client_context": {"route":"predictive"}
}
```

Response `202`:

```json
{
  "execution_id": "uuid",
  "status": "QUEUED",
  "status_url": "/api/v1/projects/.../executions/uuid"
}
```

## 11. Result / Comparison / Lineage API

| Method | Path | 用途 |
| --- | --- | --- |
| GET | /projects/{project_id}/results | Result一覧 |
| GET | /projects/{project_id}/results/{result_id} | Result詳細 |
| POST | /projects/{project_id}/comparisons | 同種Result比較 |
| GET | /projects/{project_id}/results/summary | Family横断summary |
| GET | /projects/{project_id}/results/{result_id}/lineage | Result起点Lineage |
| GET | /projects/{project_id}/lineage | Project Lineage query |
| POST | /projects/{project_id}/lineage-links | 明示relation作成 |
| POST | /projects/{project_id}/exports | Manifest / bundle生成 |

Comparison request:

```json
{
  "result_ids": ["uuid1", "uuid2"],
  "comparison_schema_version": "result-comparison/1",
  "requested_dimensions": ["conditions", "metrics", "warnings", "artifacts"]
}
```

APIは比較可能性を検証し、異種metricをrankしない。

## 12. Annotation / Artifact API

| Method | Path | 用途 |
| --- | --- | --- |
| POST | /projects/{project_id}/annotations | Annotation作成 |
| GET | /projects/{project_id}/annotations | targetで検索 |
| PATCH | /projects/{project_id}/annotations/{annotation_id} | Annotation更新 |
| GET | /projects/{project_id}/annotations/{annotation_id}/history | 変更履歴 |
| GET | /projects/{project_id}/artifacts/{artifact_id} | Artifact metadata |
| GET | /projects/{project_id}/artifacts/{artifact_id}/download | 権限付きdownload |

## 13. Operation Availability API

```text
GET /projects/{project_id}/operation-availability
```

Query:

- resource_type
- resource_id
- route

Response:

```json
{
  "operations": {
    "RUN": {"allowed": false, "reason_code": "SPEC_NOT_FIXED", "message": "Fix the specification first."},
    "EDIT": {"allowed": true},
    "EXPORT": {"allowed": true}
  }
}
```

Frontendはこの結果を表示補助に使用するが、Command時にもBackendが再検証する。

## 14. Worker Interface

### 14.1. Claim

WorkerはDB row lockまたはqueue messageでExecutionをclaimする。claim token、worker id、lease expiryを記録する。

### 14.2. Runner Contract

```python
class StageRunner(Protocol):
    stage_type: StageType
    def validate(self, context: StageContext) -> ValidationReport: ...
    def run(self, context: StageContext) -> StageRunResult: ...
```

`StageRunResult`:

- analytical results
- artifacts
- output bindings
- warnings
- metrics

### 14.3. Event

Outbox event example:

```json
{
  "event_type": "STAGE_SUCCEEDED",
  "event_version": "1",
  "project_id": "uuid",
  "execution_id": "uuid",
  "stage_execution_id": "uuid",
  "occurred_at": "datetime"
}
```

## 15. CLI

```text
ariadne project list
ariadne context create|fix|show
ariadne dataset register|show
ariadne view create|validate|fix
ariadne analysis create|validate|fix
ariadne plan create|show
ariadne execution submit|status|cancel|retry
ariadne result show|compare|export
```

CLI manifestはWeb APIと同じSchemaを使用する。CLI単独でhistory依存warningを生成しない。

## 16. Idempotency

対象:

- Project作成
- Dataset Version登録
- Context / View / Specification固定
- Plan生成
- Execution submit
- Graph Version作成
- Export生成

同一Project、同一Idempotency-Key、同一canonical bodyは同一responseを返す。bodyが異なる場合は`409 IDEMPOTENCY_CONFLICT`。

## 17. Contract Versioning

- URL major: `/api/v1`
- Resource payload: `schema_version`
- Family spec: `family_spec_schema_version`
- Result: `schema_version`
- Stage: namespace / name / version
- Event: `event_version`

破壊的変更は新versionを追加し、既存versionのreaderとmigration policyを定義する。


## ENH-E4 approved interface contract delta

- user-visible Product analysis submissionはcanonical Executionを作成する。
- family/typeは別lifecycle authorityを作らない。
- retryはidentityを保持し、rerun/reviseは承認済みtyped relationを伴うdistinct identityを作る。
- cancelはcanonical lifecycle contractに従い、prior successful outputをsilent rewriteしない。
- Result/Artifact referenceはcanonical semantic identityを使い、physical object keyを使わない。
- low-level standalone scientific CLIはpersistent audit APIではない。auditが必要なuser-visible CLI analysisはcanonical Executionへsubmitする。

既存endpoint pathのrenameは本snapshotでは決定しない。既存API compatibilityとtarget contractの具体的衝突は、compatibility evidenceを収集する後続Gateへ割り当てる。
