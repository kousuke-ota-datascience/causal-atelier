# 23_17_api_result_comparison_lineage


---

## 5. Web API Interface

### 5.8 Result / Comparison / Lineage API

#### 5.8.1 Canonical Result API

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

#### 5.8.2 Project-scoped Product Closure

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

#### 5.8.3 Comparison semantics

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

#### 5.8.4 Lineage relationの二層

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

## PREP-01: Router operation source inventory

Evidence: results.py@e565edb21051133b84fb77fd7c1eafcd2d7257ea, product_closure.py@7cae6a3df8725c3f5263ede17167225175f5968e. Source-declared routes only; the app.py API prefix is /api/v1. 200* is default decorator success, not a runtime validation.

| HTTP | Route | Handler | Declared status | Response model | Router |
| --- | --- | --- | --- | --- | --- |
| GET | `/api/v1/projects/{project_id}/graph-candidates` | `list_graph_candidates` | 200* | GraphCandidateListResponse | results |
| GET | `/api/v1/projects/{project_id}/graph-candidates/{candidate_kind}/{candidate_id}` | `get_graph_candidate` | 200* | GraphCandidateResponse | results |
| POST | `/api/v1/projects/{project_id}/graph-candidate-comparisons/query` | `compare_graph_candidates` | 200* | GraphCandidateComparisonResponse | results |
| GET | `/api/v1/executions/{execution_id}/results` | `list_results_by_execution` | 200* | ResultListResponse | results |
| GET | `/api/v1/results/{result_id}` | `get_result` | 200* | ResultResponse | results |
| POST | `/api/v1/comparisons/query` | `query_comparison` | 200* | ComparisonResponse | results |
| GET | `/api/v1/results/{result_id}/lineage` | `get_lineage` | 200* | LineageResponse | results |
| POST | `/api/v1/results/{result_id}/export` | `export_result` | 200* | untyped | results |
| GET | `/api/v1/projects/{project_id}/results` | `list_results` | 200* | untyped | product_closure |
| GET | `/api/v1/projects/{project_id}/results/summary` | `results_summary` | 200* | untyped | product_closure |
| GET | `/api/v1/projects/{project_id}/results/{result_id}` | `result_detail` | 200* | untyped | product_closure |
| POST | `/api/v1/projects/{project_id}/comparisons` | `create_comparison` | 201 | untyped | product_closure |
| GET | `/api/v1/projects/{project_id}/results/{result_id}/lineage` | `result_lineage` | 200* | untyped | product_closure |
| GET | `/api/v1/projects/{project_id}/lineage` | `project_lineage` | 200* | untyped | product_closure |
| POST | `/api/v1/projects/{project_id}/lineage-links` | `create_lineage_link` | 201 | untyped | product_closure |

Observed route count: 15. Identity/path = DEFINED by Router Source. Request DTO / constraints, authorization, lifecycle effects, error semantics, idempotency, version compatibility, FR/Negative Test trace are NOT_SPECIFIED pending DTO/Service/OpenAPI verification. Duplicate or shadowed route behavior, if any, is not established from this inventory. This annex is not Contract/Architecture PASS.
