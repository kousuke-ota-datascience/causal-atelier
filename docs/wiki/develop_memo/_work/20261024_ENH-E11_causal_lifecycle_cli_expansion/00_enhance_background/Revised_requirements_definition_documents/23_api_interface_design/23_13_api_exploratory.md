# 23_13_api_exploratory


---

## 5. Web API Interface

### 5.4 Exploratory Interface

Exploratory UIは`Profile / Data Quality / Distribution / Relationships / Comparison / Findings`をNavigation Stageとして持つが、各Navigation Stageに対応する新規Execution APIを1:1で要求しない。

現行実装で存在するExploratory / Analysis View interfaceは次である。

#### 5.4.1 Analysis View

| Method | Path | 用途 |
| --- | --- | --- |
| POST | `/projects/{project_id}/analysis-views` | Analysis View作成 |
| GET | `/projects/{project_id}/analysis-views` | Analysis View一覧 |
| GET | `/projects/{project_id}/analysis-views/{analysis_view_id}` | Analysis View取得 |
| PATCH | `/projects/{project_id}/analysis-views/{analysis_view_id}` | DRAFT更新 |
| POST | `/projects/{project_id}/analysis-views/{analysis_view_id}/validate` | validation |
| POST | `/projects/{project_id}/analysis-views/{analysis_view_id}/fix` | FIXED化 |

#### 5.4.2 Exploration

| Method | Path | 用途 |
| --- | --- | --- |
| POST | `/projects/{project_id}/exploration/preview` | 保存しない同期preview |
| POST | `/projects/{project_id}/exploration/executions` | persisted exploratory execution submit |
| GET | `/projects/{project_id}/exploration/executions` | exploratory execution一覧 |
| GET | `/projects/{project_id}/exploration/executions/{execution_id}` | exploratory execution取得 |
| GET | `/projects/{project_id}/exploration/results` | exploratory result一覧 |
| GET | `/projects/{project_id}/exploration/results/{result_id}` | exploratory result取得 |
| POST | `/projects/{project_id}/exploration/results/{result_id}/create-analysis-draft` | exploratory resultからCausal/Predictive analysis draft作成 |

`create-analysis-draft` request:

```json
{
  "target_family": "CAUSAL | PREDICTIVE",
  "analysis_mode": "EXPLORATORY | CONFIRMATORY",
  "research_context_version_id": "uuid-or-null",
  "family_spec_schema_version": "...",
  "family_spec": {}
}
```

Contract:

- `dataset_version_id / analysis_view_id`はsource Result lineageからderiveし、request overrideを受け付けない。
- research contextをsource lineageから一意に解決できない場合のみrequestで要求する。
- canonical `AnalysisSpecification`を`DRAFT`としてpersistする。
- source Resultからtarget AnalysisSpecificationへ`MOTIVATED` semantic lineageを保存する。
- auto FIX / auto Executionは行わない。
- same immutable `dataset_version_id` + `CONFIRMATORY`の場合、`EXPLORATORY_REUSE_SAME_DATA` warningとsource Result IDを返す。
| GET | `/projects/{project_id}/exploration/capabilities` | supported operation / chart mark metadata |

`ExplorationRequest`は`dataset_version_id / analysis_view_id? / family_spec`を受け取る。preview responseは`analysis_family = EXPLORATORY`、`result_type / analytical_status / summary / payload / warnings / view_manifest / saved=false`を返す。

Family-specific exploratory specのoperationは次である。

```text
PROFILE
DISTRIBUTION
ASSOCIATION
GROUP_SUMMARY
TIME_TREND
CHART
```

現行実装のExploratory plannerは各operationを1 runtime StageからなるExecution Planへ写像する。Navigation `Data Quality` / `Findings`等のために同名runtime endpointを追加せず、Dataset metadata、Result、Artifact、Annotation等のreadを組み合わせてよい。

## PREP-01: Router operation source inventory

Evidence: exploration.py source blob 8c068c77357cd628cd278e3668cdf23ff5a6046c. Static decorator inventory only; /api/v1 is the app router prefix. 200* = default declared FastAPI code, not a runtime assertion.

| HTTP | Route | Handler | Declared success | Response model |
| --- | --- | --- | --- | --- |
| POST | `/api/v1/projects/{project_id}/analysis-views` | `create_analysis_view` | 201 | AnalysisViewResponse |
| GET | `/api/v1/projects/{project_id}/analysis-views` | `list_analysis_views` | 200* | AnalysisViewListResponse |
| GET | `/api/v1/projects/{project_id}/analysis-views/{analysis_view_id}` | `get_analysis_view` | 200* | AnalysisViewResponse |
| PATCH | `/api/v1/projects/{project_id}/analysis-views/{analysis_view_id}` | `update_analysis_view` | 200* | AnalysisViewResponse |
| POST | `/api/v1/projects/{project_id}/analysis-views/{analysis_view_id}/validate` | `validate_analysis_view` | 200* | untyped |
| POST | `/api/v1/projects/{project_id}/analysis-views/{analysis_view_id}/fix` | `fix_analysis_view` | 200* | AnalysisViewResponse |
| POST | `/api/v1/projects/{project_id}/exploration/preview` | `preview_exploration` | 200* | ExplorationPreviewResponse |
| POST | `/api/v1/projects/{project_id}/exploration/executions` | `submit_exploration` | 202 | FamilyExecutionResponse |
| GET | `/api/v1/projects/{project_id}/exploration/executions` | `list_exploration_executions` | 200* | FamilyExecutionListResponse |
| GET | `/api/v1/projects/{project_id}/exploration/executions/{execution_id}` | `get_exploration_execution` | 200* | FamilyExecutionResponse |
| GET | `/api/v1/projects/{project_id}/exploration/results` | `list_exploration_results` | 200* | FamilyResultListResponse |
| GET | `/api/v1/projects/{project_id}/exploration/results/{result_id}` | `get_exploration_result` | 200* | FamilyResultResponse |
| POST | `/api/v1/projects/{project_id}/exploration/results/{result_id}/create-analysis-draft` | `create_analysis_draft` | 201 | untyped |
| GET | `/api/v1/projects/{project_id}/exploration/capabilities` | `exploration_capabilities` | 200* | untyped |

Observed 14 operations. Identity/path is DEFINED from the router; request DTO, auth, lifecycle, error mapping, idempotency, compatibility and operation-specific tests remain NOT_SPECIFIED until source/DTO/service/OpenAPI verification. This annex is not a complete Contract, nor an Independent Verification PASS.
