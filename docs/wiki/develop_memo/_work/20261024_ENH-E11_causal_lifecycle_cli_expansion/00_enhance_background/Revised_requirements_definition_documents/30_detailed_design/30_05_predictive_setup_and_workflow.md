<!-- ENH-E11 split working copy: not a formal approval. -->
# 30 — predictive setup and workflow

**Status:** `STRUCTURAL_COPY_DRAFT` (existing baseline text, not E11 canonical publication)

**Source:** [30_detailed_design.md](https://github.com/kousuke-ota-datascience/causal-atelier/blob/3ba5fe2465ec591f0da7f998c21a5241984b73dc/docs/wiki/requirement_definition/30_detailed_design.md) · blob `04d83541e55ab0364500afb4b92ef55c10785a0c`  
**Index:** [Revised document inventory](../README_00_Revised_requirements_definition_documents.md)

---

## 15. Predictive Capability / Stage Contents

Predictive family schema versionは`predictive-analysis-spec/1`。

Top-level fields:

```text
schema_version
task_type
prediction_question
feature_spec
split_spec
preprocessing_spec
model_spec
tuning_spec
evaluation_spec
explanation_spec
```

Task typeは`BINARY_CLASSIFICATION / REGRESSION`。Split strategyは`RANDOM / STRATIFIED / GROUP / TIME_BASED`。

Key validation:

- targetをfeatureに含めない。
- feature availabilityは`feature_columns`全件をcoverする。
- prediction timeより後のfeatureを拒否する。
- split ratioは正数かつ合計1（TIME_BASEDを除く）。
- `GROUP`は`group_column`必須。
- `TIME_BASED`は`time_column / train_cutoff / validation_cutoff`必須でcutoff順序を保証する。
- stratified splitはbinary classificationに限定する。
- preprocessing fit partitionは`TRAIN`のみ。
- tuning selectionに`TEST`を使わない。

backend lifecycle:

```text
Prediction Task
  → Split
  → Training
  → Evaluation
  → Explanation
  → Model Card
```

Navigation presentation:

```text
Setup
Train
Predict
Metrics
Explainability
Model Management
```

両者を1:1 runtime Stage modelとして一致させない。

### 15.1 Setup

目的はprediction taskとanalysis specificationを定義することである。

primary surface:

- Analysis Context / selected Dataset Version / Analysis View
- task type
- prediction question
- target
- feature set
- prediction time / horizon where applicable
- split/specification-level configuration
- specification validation

feature-column editingはSetupのみが所有する。

### 15.2 Predictive feature-column selector

feature selectionのcandidate authorityはcurrently selected Dataset Versionのschemaである。

primary interaction:

```text
selected Dataset Version
  ↓
Dataset schema columns
  ↓
Feature selector dialog
  ├─ checkbox pending selection
  ├─ Confirm
  └─ Cancel
  ↓
feature_spec.feature_columns
```

Detailed contract:

1. primary editing interactionをcomma-delimited free textにしない。
2. Dataset Version/schemaがない場合、selector unavailableを明示し、架空column optionを生成しない。
3. dialog open時にcurrent confirmed feature selectionをchecked stateとして復元する。
4. checkbox toggleはpending stateのみを変更し、Confirm前にconfirmed draftを変更しない。
5. `Cancel`はconfirmed feature selectionを変更しない。
6. `Confirm`はchecked featureをdeterministic Dataset schema orderでcommitする。
7. committed valueは`predictive-analysis-spec/1 -> feature_spec.feature_columns`を生成する同一draft/form authorityへ反映する。
8. free-text入力とcheckboxを同時に競合editable authorityとして保持しない。
9. Dataset Version変更時、新schemaに存在しないselected columnをsilentに保持しない。全clearまたはvalid intersection保持を許可するが、破壊的reconcileは利用者へ示す。
10. target / excluded column、feature availability、split、leakage、task validationは上記current Predictive validationをauthorityとし、selector独自のscientific ruleを追加しない。
11. selector実現だけを理由にnew Dataset schema APIやnew Predictive specification versionを追加しない。

Accessibility:

- selector triggerにaccessible nameがある。
- dialogにaccessible nameがある。
- checkboxにlabelがある。
- keyboardでopen / Confirm / Cancelできる。
- closed/hidden dialog contentをfocus可能にしない。
- close後にfocusをinvoking controlへ戻す。

Causal Discovery等のschema-backed column selectorとimplementation helperを共通化してよいが、そのFamily固有のrequest validationやscientific semanticsを変更しない。

### 15.3 Train

目的はfixed/draft Predictive specificationに基づいてmodel trainingを実行・確認することである。

primary surface:

- selected draft/specification feature setのread-only context
- preprocessing configuration
- model configuration
- tuning configuration
- training execution/status
- fitted model/preprocessor artifact
- Training Result reference

Trainではfeature setをeditableにしない。feature setを変更する場合はSetupへ戻ってspecificationを改訂する。

### 15.4 Predict

目的はcurrent prediction/inference outputとそのprovenanceを確認することである。

- relevant saved execution specificationに記録されたfeature setをread-only表示する。
- prediction output/result/artifactを表示する。
- current unrelated draftのfeature setで既存execution結果を上書きして見せない。
- Navigation Stage名だけを理由にstandalone scoring engine/new runtime execution modelを作らない。
- feature selectorをeditable controlとして提供しない。

### 15.5 Metrics

目的はEvaluation Resultからpredictive performanceを評価することである。

primary surface:

- evaluation result
- primary/secondary metrics
- subgroup/error analysis where supported
- evaluation provenance/reference

Trainのconfig/execution UIをpage purposeとして複製しない。

### 15.6 Explainability

目的はPredictive Explanationを確認することである。

primary surface:

- `PREDICTIVE_EXPLANATION_RESULT`
- predictive explanation artifact
- relevant Model Card reference
- feature/model provenance

Predictive Explanationをcausal effect / causal explanationとして表現しない。Navigation requirementだけを理由に特定external explanation libraryを必須化しない。

### 15.7 Model Management

read-oriented model surfaceとしてResult / Artifact / Lineageを使用する。

対象:

- `TRAINING_RESULT`
- `EVALUATION_RESULT`
- `MODEL_CARD_RESULT`
- fitted preprocessor/model artifact
- Model Card artifact
- revised/rerun lineage

UI名だけを理由に別`ModelRegistry` persistent aggregateを追加しない。

### 15.8 Draft state preservation

Navigation Stage切替時に未保存DRAFT inputを意図せず初期化しない。

state authorityはroute-independent parent/application form store等へ一意化し、Stage child unmountだけで唯一のDRAFT stateを失う構造を避ける。

valid confirmed feature selectionも同じdraft-state contractで保持する。

### 15.9 Model Capability registry

Predictive model registryはdescriptor + backend adapter resolverとして構成する。

Required descriptor fields:

```text
model_id
contract_version
supported_tasks
parameters
provider
dependency
available
unavailable_reason
provider_version
determinism
serializer_id
loader_id
default_for_tasks
```

Current IDs:

- `logistic_regression.v1`
- `linear_regression.v1`
- `lightgbm_classifier.v1`
- `lightgbm_regressor.v1`

Existing logistic/linear are task defaults. Registry/capability response and execution resolver must use the same source of truth.

Optional dependency discovery uses lazy module/version inspection. Importing Ariadne core modules must not import LightGBM/SHAP/LIME eagerly.
