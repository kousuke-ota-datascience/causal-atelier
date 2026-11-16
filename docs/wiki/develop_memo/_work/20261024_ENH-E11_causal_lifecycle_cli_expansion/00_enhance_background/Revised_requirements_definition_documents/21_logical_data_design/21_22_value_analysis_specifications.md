# 21_22_value_analysis_specifications


---

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

**適用する論理データ制約（関連Requirement）**

- **`FR-029`**：Chart Specificationを保存し、同じDataset Versionで再実行できる
- **`FR-032`**：Exploratory Resultからcanonical Causal/Predictive `AnalysisSpecification`をDRAFTとしてpersistし、source Resultとの`MOTIVATED` relationを保持できる。auto FIX / auto executionは行わない
- **`FR-034`**：Exploratory provenanceとしてdata-selection semantics、analysis-significant family_spec、sampling、Execution code/runtime metadataおよびResult/Artifact lineageを再構成できる
- **`FR-068`**：fitted model、fitted preprocessor、prediction等のdurable outputをArtifactとして保存し、provider-specific fitted modelはartifact schema/provider/payload identityから対応loaderを一意に解決してfresh-process相当で再読込・predictionできる
- **`FR-071`**：intended use、training data、metric、limitationsに加え、model/provider/version、effective parameters、seed/deterministic settings、feature/preprocessor identity、explanation method等の再現性provenanceをModel Cardへ記録する
- **`FR-183`**：explanation Result/Artifactはmethod/model/provider、feature/sample identity、model/prediction output scale、background/reference、effective seed/parameters、library version等のprovenanceを保持する
- **`FR-157`**：既存`AnalysisSpecification.analysis_family`をFamily discriminatorとして再利用し、duplicate Family field/enumを追加しない
- **`FR-158`**：AnalysisSpecification / ExecutionPlan / Execution / StageExecutionへNavigation Stage fieldを追加しない
- **`FR-160`**：Family / Navigation / application IAの変更だけを理由にDB schema migrationまたはnavigation-state persistenceを導入しない
