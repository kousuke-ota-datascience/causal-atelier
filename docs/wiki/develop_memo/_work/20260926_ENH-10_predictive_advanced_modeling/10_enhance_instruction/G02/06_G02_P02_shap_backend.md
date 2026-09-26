# ENH-E10 G02 P02 — SHAP Backend

**Document class:** Work Package Execution Contract  
**Status:** `MATERIALIZED_DRAFT / NOT_EXECUTABLE`  
**Gate:** `G02`  
**Package:** `P02`  
**Depends on:** `G02 P01 canonical package report = PACKAGE_COMPLETE`  
**Self-containment:** MUST when FROZEN  
**Information isolation:** MUST  
**Execution eligibility:** `BLOCKED_CONTRACT_NOT_FROZEN`

## 1. Package objective

SHAP global/local adapter、classification/regression normalization、output scale/base/background semanticsを成立させ、P03へ引き渡す。

## 2. Effective architecture values

- method = `SHAP_TREE`.
- supported models = `lightgbm_classifier.v1`, `lightgbm_regressor.v1`.
- `TreeExplainer(feature_perturbation="tree_path_dependent", model_output="raw")`.
- no explicit background matrix; reference semantics come from tree training path counts.
- classification model-output scale = `LOG_ODDS`; prediction scale = `PROBABILITY`.
- regression model-output/prediction scale = `PREDICTION`.
- global = mean absolute contribution + signed mean across all immutable TEST explanation rows.
- local = FIRST_N rows from current explanation sampling contract.
- mandatory additivity verification with `atol=1e-6, rtol=1e-5`.
- SHAP version bound = `>=0.52.0,<0.53`.

## 3. Required behavior

- frozen compatibility matrixに従いSHAP adapterを実装する。
- classification/regression provider output shapeをcanonical representationへnormalizeする。
- global/local semantics、model-output scale、base/expected value、feature mapping、sample identity、background/reference provenanceを保持する。
- unsupported shape/task/modelをcoerce/fallbackしない。

## 4. Focused verification

binary SHAP global/local、regression SHAP global/local、output-scale/base/background contract、feature mapping/sample identity、dependency unavailable。

## 5. Completion boundary

focused verification PASS、package report、exact checkpoint SHA、blocker NONE。terminal stateは `PACKAGE_READY` または `BLOCKED_*`。
