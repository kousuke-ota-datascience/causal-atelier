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

## 2. Architecture values required before freeze

SHAP supported model/task set、output scale、background/reference selection、base/expected value、additivity/tolerance、dependency versionを06/07と一致させる。

## 3. Required behavior

- frozen compatibility matrixに従いSHAP adapterを実装する。
- classification/regression provider output shapeをcanonical representationへnormalizeする。
- global/local semantics、model-output scale、base/expected value、feature mapping、sample identity、background/reference provenanceを保持する。
- unsupported shape/task/modelをcoerce/fallbackしない。

## 4. Focused verification

binary SHAP global/local、regression SHAP global/local、output-scale/base/background contract、feature mapping/sample identity、dependency unavailable。

## 5. Completion boundary

focused verification PASS、package report、exact checkpoint SHA、blocker NONE。terminal stateは `PACKAGE_READY` または `BLOCKED_*`。
