# G02 P03 — Predictive Stage Surface Separation / Feature Selector

- Status: `FROZEN`
**Assigned Coding Agent normative context: この文書のみ。**

## Objective

Predictive Setup / Train / Predict / Metrics / Explainability / Model Managementを、それぞれ異なるpresentation Stageとして成立させる。

existing Predictive analytical specification / backend execution semanticsを維持する。

追加で、Predictive feature-columnのcomma-delimited editingを、Dataset-schema-backed popup/dialog + checkbox multi-selectionへ置き換える。Causal Discoveryで既に確立しているinteraction modelと整合させる。

## Required Stage ownership

### Setup

- task/context/dataset/view
- prediction unit / target / features / timing / horizon
- split/specification-level input
- **feature-column editing owner**

### Train

- preprocessing/model/tuning
- execution/status
- current draft/spec feature setをcompact read-only execution contextとして表示

### Predict

- existing prediction output/result/artifact
- existing executionを選択する場合、そのexecution specificationに記録されたfeature setをread-only表示
- standalone scoring engineを追加しない
- editable feature selectionを提供しない

### Metrics

- Evaluation Result
- metrics
- subgroup/error analysis

existing spec構築に必要なconfig値はdraft stateとして保持してよいが、page purposeをTrainのcopyにしない。

### Explainability

- predictive explanation result/artifact
- predictive-not-causal semanticsを明確にする

### Model Management

- Model Card
- fitted model/preprocessor Artifact
- lineage/reference

## Predictive feature selector contract

### Candidate authority

selector optionは、frontendが既に保持している**currently selected Dataset Versionのschema**から取得する。

このselectorだけのためにnew Dataset schema APIを追加しない。

### User interaction

primary interaction:

```text
Setup / Feature columns
  -> 「列を選択」相当のcontrolをactivate
  -> dialogをopen
  -> Dataset schema columnをcheckbox表示
  -> pending selectionを変更
  -> Confirmでcommit
  -> Cancelは変更なし
```

必須事項:

1. Dataset Version/schemaがない場合、selector unavailableを明示しsynthetic optionを作らない。
2. dialog open時にcurrent confirmed feature selectionをchecked stateへ反映する。
3. checkbox変更はConfirmまでconfirmed draftを変更しない。
4. Confirmはchecked featureをDataset schemaのdeterministic orderでcommitする。
5. confirmed valueはexisting form/draft authorityへ入り、`predictive-analysis-spec/1 -> feature_spec.feature_columns` を生成する。
6. same feature setに2つの競合editable authorityを持たせない。comma-delimited free-textはprimary editable pathから除去するかnon-editable/internalにする。
7. Dataset Version変更時、新schemaに存在しないcolumnをsilentに保持しない。clearまたはvalid intersection保持を許可するが、破壊的reconcileは利用者へ示す。
8. target/excluded columns、feature availability、task、split、leakageのexisting validationを変更しない。
9. valid confirmed feature selectionはexisting Predictive draft-stateでStage切替後も保持する。
10. Trainはfeature setをeditableにしない。
11. Predictはfeature setをeditableにせず、existing execution resultではcurrent unrelated draftではなくexecution specificationをread-only sourceとする。

### Accessibility

- selector triggerにaccessible nameがある
- dialogにaccessible label/nameがある
- checkboxにlabelがある
- keyboardでopen / Confirm / Cancelできる
- hidden selector contentをfocus可能にしない
- close後に適切にfocusをinvokerへ戻す

### Causal Discovery selector reuse

baseline Causal Discoveryは既に以下を持つ。

- Dataset schema由来candidate
- modal/dialog
- checkbox
- deterministic schema ordering

shared helper/componentを抽出してよい。

shared code導入時は以下をprotected regressionとする。

- current selection restoration
- designated outcome synchronization
- Dataset Version change behavior
- unknown/duplicate column request validation
- modal open/Confirm behavior

Causal scientific semanticsは変更しない。

## Shared execution vs presentation

existing backendがTraining/Evaluation/Explanationを1pipelineで実行していてもよい。Navigationに合わせてruntime executionを分割しない。

## Draft/spec invariant

Stage切替で `predictive-analysis-spec/1` のvalid valueを失わない。

selectorはexisting feature-set fieldへの別input interactionであり、新しいspec field/versionではない。

## Layout

vertical semantic-section flowを使用する。

Train/Metrics/Explainability/Model Managementの唯一の意味としてgeneric `Predictive Result` cardだけを再利用しない。

selector dialog内のscrollable listは許可するが、page-level horizontal scrollを発生させない。

## Likely files

Primary:

- `frontend/index.html`
- `frontend/app.js`
- `frontend/styles.css`

Possible:

- shared column selector helper/module
- existing product/frontend tests

Protected:

- backend Predictive capability/domain/runtime semantics
- Causal Discovery scientific request semantics

## Forbidden

- API/DB/backend/runtime semantics変更
- LightGBM/LIME/SHAP実装
- UI selectorのためだけのnew Predictive spec version
- Navigationのためだけのnew prediction operation
- Train/Predictでeditable feature selectorを提供
- defaults/validation/spec serializationのsilent変更
- free-textとcheckboxを競合editable authorityとして併存
- code reuseのためにCausal Discovery validationを弱める

## Browser E2E script ownership

P03は、G02のPredictive critical journeyを検証する次のscriptをcandidateへ追加・維持する。

`tests/browser_e2e/run_enh_e8_g02_predictive_stage_content.py`

scriptはSetup feature selector、Train read-only feature context、Predict execution-recorded feature context、Metrics/Explainability/Model ManagementのStage identityとdraft continuityをreal Chromiumで検証し、evidenceを保存する。

## Required focused tests / self-check

1. Setup selector optionがselected Dataset schema columnと一致する。
2. Dataset/schemaなしでは明示的unavailable stateになる。
3. confirmed selectionがchecked stateへ復元される。
4. Cancelでconfirmed feature selectionが変わらない。
5. Confirmでchecked featureがdeterministic schema orderで反映される。
6. Dataset changeでnonexistent selected columnをsilent保持しない。
7. confirmed selectionがPredictive Stage切替で保持される。
8. 同じfeature listなら、baseline free-text入力と同一semanticsの `predictive-analysis-spec/1.feature_spec.feature_columns` を生成する。
9. existing feature availability / target / excluded-column / split validationが変わらない。
10. Trainはselected feature contextをread-only表示しeditable selectorを持たない。
11. Predictはrelevant execution feature contextをread-only表示しeditable selectorを持たない。
12. 6 Predictive Stageのpositive/negative surface testがPASSする。
13. selectorをshared/generalizeした場合、Causal Discovery protected regressionがPASSする。
14. route/catalog regressionがPASSする。

package checkpointのみ記録する。package completionはGate PASSではない。
