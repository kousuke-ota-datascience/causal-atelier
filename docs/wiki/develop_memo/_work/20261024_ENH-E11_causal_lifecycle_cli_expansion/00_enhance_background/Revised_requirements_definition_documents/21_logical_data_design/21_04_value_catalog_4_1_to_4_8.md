<!-- ENH-E11 split working copy: not a formal approval. -->
# 21 — value catalog 4 1 to 4 8

**Status:** `STRUCTURAL_COPY_DRAFT` (existing baseline text, not E11 canonical publication)

**Source:** [21_logical_data_design.md](https://github.com/kousuke-ota-datascience/causal-atelier/blob/3ba5fe2465ec591f0da7f998c21a5241984b73dc/docs/wiki/requirement_definition/21_logical_data_design.md) · blob `72903b9ad48b5b7edabaa7bb1c2cace42aa46ce7`  
**Index:** [Revised document inventory](../README_00_Revised_requirements_definition_documents.md)

---

## 4. 非Entityのデータモデル

本章は独立identity/lifecycleを持たないvalue object、projection、query model、navigation metadata、embedded schemaを定義する。これらをUI上に存在するという理由だけでpersistent Entityへ昇格させない。

### 4.1 AnalysisFamily

`AnalysisFamily`はEntityではなくdomain discriminatorであり、許容値は次の3つとする。

- `EXPLORATORY`
- `CAUSAL`
- `PREDICTIVE`

この値は`AnalysisSpecification.analysis_family`、`ExecutionPlan.analysis_family`、`Execution.analysis_family`で共通利用する。同義のduplicate enum/fieldを増設しない。

### 4.2 Analysis Context

Analysis Contextは新しいpersistent aggregateではなく、current routeとProject-scoped selection/resourceの論理projectionである。

```text
Analysis Context
├─ Current Project
│  └─ canonical Analysis route.project_id
├─ Active Research Context
│  └─ WorkspaceSelection.research_context_version_id
├─ Dataset Version
│  └─ WorkspaceSelection.dataset_version_id
└─ Analysis View
   └─ WorkspaceSelection.analysis_view_id
```

| Element | Authority | Persistence |
| --- | --- | --- |
| Current Project | canonical Analysis route `project_id` | 専用field/resourceを追加しない |
| Active Research Context | `ResearchContextVersion` + `WorkspaceSelection` | existing lifecycleを利用 |
| Dataset Version | `DatasetVersion` + `WorkspaceSelection` | existing lifecycleを利用 |
| Analysis View | `AnalysisView` + `WorkspaceSelection` | existing lifecycleを利用 |
| Current Family / Navigation Stage | browser URL / navigation state | DB永続化しない |

Selection rule:

1. Research Context / Dataset Version / Analysis ViewはCurrent Projectと整合する。
2. Analysis Viewはselected Dataset Versionと互換である。
3. Dataset Version変更時、Analysis Viewが互換でなければAnalysis View selectionを解除する。
4. 有効selectionを復元できない場合、架空default resourceを作らずunselectedとする。
5. Context不足だけを理由にFamily / Navigation Stage routeを書き換えない。

### 4.3 Navigation metadata model

Navigation StageはAnalysis Specificationやruntime Stageとは異なるapplication metadataである。

```text
AnalysisFamily
   │
   ▼
FamilyNavigationDescriptor
   │
   └─ NavigationStageDescriptor*
            │
            └─ renderer / use-case binding
```

主要value:

| Value | 内容 |
| --- | --- |
| `FamilyNavigationDescriptor` | Family、default Stage、Stage catalog |
| `NavigationStageDescriptor` | Stage ID、label、order、表示metadata |
| Current Family | browser navigation state |
| Current Navigation Stage | Family-local browser navigation state |
| route representation | `/projects/{project_id}/analysis/{family_slug}/{stage_slug}` |
| renderer binding | `(family, stage)`から既存surface/use caseへのbinding |

Navigation metadataを`AnalysisSpecification`、`ExecutionPlan`、`Execution`、`StageExecution`へ保存しない。

### 4.4 Runtime Stage value model

ExecutionPlan内のruntime Stageは次のvalue objectで表現する。

```json
{
  "stage_key": "train",
  "stage_type": {
    "namespace": "predictive",
    "name": "train",
    "version": "1"
  },
  "input_contract": {},
  "output_contract": {},
  "parameters": {},
  "resource_policy": {},
  "enabled": true
}
```

- `StageType`: namespace / name / versionでruntime Stage種別を識別
- `StageDefinition`: input/output/parameter/resource policy
- `StageBinding`: Stage間dependency / input-output binding

これらはNavigation Stageと同一型にしない。

### 4.5 AnalysisView specification

`AnalysisView.spec_json`のcanonical envelopeは次の概念を保持する。

```json
{
  "schema_version": "analysis-view/1",
  "source_dataset_version_id": "uuid",
  "row_filter": [],
  "selected_columns": [],
  "derived_columns": [],
  "missing_value_policy": {},
  "time_cutoff": null,
  "sampling": null
}
```

Typed filter compatibility:

| Logical Type | Allowed operators | Value contract |
| --- | --- | --- |
| BOOLEAN | `EQ, NE, IN, NOT_IN, IS_NULL, NOT_NULL` | boolean。`IN/NOT_IN`はboolean list |
| INTEGER | `EQ, NE, LT, LTE, GT, GTE, IN, NOT_IN, IS_NULL, NOT_NULL` | integer。booleanをintegerとして扱わない |
| REAL | `EQ, NE, LT, LTE, GT, GTE, IN, NOT_IN, IS_NULL, NOT_NULL` | finite int/float。booleanは禁止 |
| DATETIME | `EQ, NE, LT, LTE, GT, GTE, IN, NOT_IN, IS_NULL, NOT_NULL` | ISO-8601 string |
| TEXT | `EQ, NE, IN, NOT_IN, IS_NULL, NOT_NULL` | string |
| OTHER | `IS_NULL, NOT_NULL` | valueなし |

追加rule:

- `IS_NULL / NOT_NULL`はvalueを持たない。
- `IN / NOT_IN`はnon-empty listを要求する。
- `time_cutoff`はDATETIME columnと`LT / LTE` semanticsで扱う。
- type不整合をvalidation successとして扱わず、stable code `FILTER_TYPE_MISMATCH`で表現する。
- create / update / validate / fixで同一のcompatibility validatorを利用する。
- new expression language、derived expressionのfull static typing、Family-specific typingをこの契約から暗黙に追加しない。

### 4.6 AnalysisSpecification family payload

共通Envelope:

```json
{
  "schema_version": "analysis-specification/1",
  "analysis_family": "EXPLORATORY | CAUSAL | PREDICTIVE",
  "research_context_version_id": "uuid",
  "dataset_version_id": "uuid",
  "analysis_view_id": "uuid-or-null",
  "analysis_mode": "EXPLORATORY | CONFIRMATORY",
  "family_spec_schema_version": "...",
  "family_spec": {},
  "revision_context": null,
  "warnings": []
}
```

Family-specific schemaの主要scope:

- Exploratory: profile / distribution / association / group summary / time trend / chart等の分析仕様
- Causal: causal question / design / identification / estimation / refutation / sensitivity等
- Predictive: task / target / feature / split / preprocessing / model / tuning / evaluation / explanation等

Family-specific payloadを共通Entityへ無制限にflat展開しない。


#### 4.6.1 Exploratory handoff DRAFT contract

Exploratory ResultからCausal/Predictiveへhandoffする場合、canonical `AnalysisSpecification`をDRAFTとしてpersistする。

- target `analysis_family`: `CAUSAL`または`PREDICTIVE`
- `analysis_mode`: requestで`EXPLORATORY / CONFIRMATORY`を明示
- `dataset_version_id / analysis_view_id`: source Result lineageからderiveし、arbitrary overrideしない
- `research_context_version_id`: source lineageから一意にderiveできる場合は継承し、曖昧ならrequestで要求
- DRAFTではfamily_specの未完成を許容する
- source Resultからtarget AnalysisSpecificationへsemantic `MOTIVATED` relationを保存する
- auto FIX / auto Executionは行わない
- same immutable `dataset_version_id`をconfirmatory analysisへ再利用する場合はscientific warningを保持する

Explore stateからAnalysisView DRAFTへ持ち込むのは`row_filter / selected_columns / derived_columns / missing_value_policy / time_cutoff / sampling`であり、chart mark/encoding/panel layout等のpresentation-only stateをAnalysisViewへ混入させない。

#### 4.6.2 Exploratory schema

`exploratory-analysis-spec/1`の主要構造:

- operation: `PROFILE / DISTRIBUTION / ASSOCIATION / GROUP_SUMMARY / TIME_TREND / CHART`
- columns
- grouping
- aggregation
- chart encoding
- filter / sampling reference
- expected output type

#### 4.6.3 Causal schema

`causal-analysis-spec/2`の主要構造:

- analysis_mode
- research_context
- causal_question
- causal_design
- operation_spec
- validation_override
- optional revision_context
- optional scientific_warnings

Causal Operationは`DISCOVERY / IDENTIFICATION / ESTIMATION / REFUTATION / SENSITIVITY`である。未知fieldをsilent acceptanceしない。

#### 4.6.4 Predictive schema

`predictive-analysis-spec/1`の主要構造:

- task_type: `BINARY_CLASSIFICATION / REGRESSION`
- prediction_question
  - prediction_unit
  - target
  - prediction_time
  - horizon
  - intended_use
  - deployment_population
- feature_spec
  - feature_columns
  - availability_cutoff
  - excluded_columns
- split_spec
  - strategy
  - train / validation / test ratioまたはcutoff
  - group_column
  - stratify
  - seed
- preprocessing_spec
- model_spec
- tuning_spec
- evaluation_spec
- explanation_spec

### 4.7 Execution Snapshot

Execution Snapshotは独立Entityではなく、`Execution`へ固定保存する再現性payloadである。

```json
{
  "snapshot_schema_version": "...",
  "analysis_family": "...",
  "dataset_version_id": "...",
  "input_graph_version_id": null,
  "input_result_id": null,
  "analysis_spec": {},
  "algorithm_or_estimator": "...",
  "parameters": {},
  "random_seed": null,
  "code_version": "...",
  "runtime_versions": {}
}
```

canonical JSONを用いて`snapshot_hash`を計算する。Execution作成後にsnapshotを上書きしない。

### 4.8 Batch View

Batchは独立Entityではない。`Execution.batch_key`が同じExecution集合をquery projectionとして表示する。

```text
Batch View
├─ batch_key
├─ executions[]
├─ operation
├─ parameter differences
├─ scientific result summary
└─ technical status summary
```

`batch_key`はExecution identityでもLineage edgeでもない。
