# 23_16_api_execution


---

## 5. Web API Interface

### 5.7 Execution Interface

現行branchには、canonical/common Execution APIとPredictive workflow向けProject-scoped APIが併存する。current snapshotはNavigation再構成を理由にこれらを暗黙統合・削除しない。

#### 5.7.1 Canonical/common Execution Web API

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

#### 5.7.2 Canonical Execution response

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

#### 5.7.3 Predictive workflow interface

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

#### 5.7.4 Execution Plan / runtime Stage

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
