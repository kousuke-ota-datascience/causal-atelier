# 21_22_value_analysis_specifications

**Status:** `RD02_STRUCTURAL_WORKING_COPY / E11_NOT_PUBLISHED`; original ID, level and state retained.  
**Source blob:** `72903b9ad48b5b7edabaa7bb1c2cace42aa46ce7`.

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


## 98. RD-04：要求の論理データ制約の受入・Trace

**Status:** `DESIGN_CONSTRAINT_MIGRATION / OWNER_CONTENT_REVIEW_PENDING`。以下はRD-04で抽象化した元要件のうち、データ定義・同一性・来歴・正本性に関係する条項を論理設計側に残したもの。原文は出典保証目的で保持する。現行コードで検証済みと主張しない。

### 98.1. FR-029（SPLIT）

- 元要件（設計上の拘束を含む）：Chart Specificationを保存し、同じDataset Versionで再実行できる
- RD改訂後の要求：可視化の条件を保存し同じデータ版で再実行できる
- Trace：`FR-029`; Status=`ACTIVE`; Implementation=`IMPLEMENTED`; [逐条レビュー](../95_rd04_fr_application_review.md)

### 98.2. FR-032（SPLIT）

- 元要件（設計上の拘束を含む）：Exploratory Resultからcanonical Causal/Predictive `AnalysisSpecification`をDRAFTとしてpersistし、source Resultとの`MOTIVATED` relationを保持できる。auto FIX / auto executionは行わない
- RD改訂後の要求：探索結果から因果・予測分析の草案を生成し由来を追跡できる。本人の確定・実行を必要とする
- Trace：`FR-032`; Status=`ACTIVE`; Implementation=`IMPLEMENTED`; [逐条レビュー](../95_rd04_fr_application_review.md)

### 98.3. FR-034（SPLIT）

- 元要件（設計上の拘束を含む）：Exploratory provenanceとしてdata-selection semantics、analysis-significant family_spec、sampling、Execution code/runtime metadataおよびResult/Artifact lineageを再構成できる
- RD改訂後の要求：探索に用いたデータ選択・分析設定・実行環境および成果物の由来を再構成できる
- Trace：`FR-034`; Status=`ACTIVE`; Implementation=`PARTIAL`; [逐条レビュー](../95_rd04_fr_application_review.md)

### 98.4. FR-068（SPLIT）

- 元要件（設計上の拘束を含む）：fitted model、fitted preprocessor、prediction等のdurable outputをArtifactとして保存し、provider-specific fitted modelはartifact schema/provider/payload identityから対応loaderを一意に解決してfresh-process相当で再読込・predictionできる
- RD改訂後の要求：学習済みモデルと前処理を保存し、適合する環境で復元して再予測できる
- Trace：`FR-068`; Status=`ACTIVE`; Implementation=`IMPLEMENTED`; [逐条レビュー](../95_rd04_fr_application_review.md)

### 98.5. FR-071（SPLIT）

- 元要件（設計上の拘束を含む）：intended use、training data、metric、limitationsに加え、model/provider/version、effective parameters、seed/deterministic settings、feature/preprocessor identity、explanation method等の再現性provenanceをModel Cardへ記録する
- RD改訂後の要求：学習・評価・説明の根拠、限界、再現性情報をModel Cardで確認できる
- Trace：`FR-071`; Status=`ACTIVE`; Implementation=`IMPLEMENTED`; [逐条レビュー](../95_rd04_fr_application_review.md)

### 98.6. FR-183（SPLIT）

- 元要件（設計上の拘束を含む）：explanation Result/Artifactはmethod/model/provider、feature/sample identity、model/prediction output scale、background/reference、effective seed/parameters、library version等のprovenanceを保持する
- RD改訂後の要求：予測説明のモデル・入力・出力尺度・計算条件を追跡し再現できる
- Trace：`FR-183`; Status=`ACTIVE`; Implementation=`IMPLEMENTED`; [逐条レビュー](../95_rd04_fr_application_review.md)

### 98.7. FR-157（MOVE_BD）

- 元要件（設計上の拘束を含む）：既存`AnalysisSpecification.analysis_family`をFamily discriminatorとして再利用し、duplicate Family field/enumを追加しない
- RD改訂後の要求：【設計制約移管・Legacy Trace】FR-074の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する
- Trace：`FR-157`; Status=`ACTIVE`; Implementation=`IMPLEMENTED`; [逐条レビュー](../95_rd04_fr_application_review.md)

### 98.8. FR-158（MOVE_BD）

- 元要件（設計上の拘束を含む）：AnalysisSpecification / ExecutionPlan / Execution / StageExecutionへNavigation Stage fieldを追加しない
- RD改訂後の要求：【設計制約移管・Legacy Trace】NFR-021の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する
- Trace：`FR-158`; Status=`ACTIVE`; Implementation=`IMPLEMENTED`; [逐条レビュー](../95_rd04_fr_application_review.md)

### 98.9. FR-160（MOVE_BD）

- 元要件（設計上の拘束を含む）：Family / Navigation / application IAの変更だけを理由にDB schema migrationまたはnavigation-state persistenceを導入しない
- RD改訂後の要求：【設計制約移管・Legacy Trace】NFR-021／FR-177の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する
- Trace：`FR-160`; Status=`ACTIVE`; Implementation=`IMPLEMENTED`; [逐条レビュー](../95_rd04_fr_application_review.md)
