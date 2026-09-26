# ENH-E10 G01 P02 — LightGBM Model Adapters

**Document class:** Work Package Execution Contract  
**Status:** `MATERIALIZED_DRAFT / NOT_EXECUTABLE`  
**Gate:** `G01`  
**Package:** `P02`  
**Depends on:** `G01 P01 canonical package report = PACKAGE_COMPLETE`  
**Self-containment:** MUST when FROZEN  
**Information isolation:** MUST  
**Execution eligibility:** `BLOCKED_CONTRACT_NOT_FROZEN`

## 1. Package objective

Binary Classification / Regression用LightGBM adapter、parameter validation、seed/determinism、fit/predict semanticsを成立させ、P03へ引き渡す。

## 2. Architecture values required before freeze

LightGBM model IDs、supported parameter subset/defaults、categorical/missing/early-stopping policy、deterministic settingsを06/07と一致させる。

## 3. Required behavior

- P01 capability contractへBinary Classification用classifierとRegression用regressorを実装する。
- frozen parameter subset/defaultsのみ受理し、unsupported/invalid parameterを明示拒否する。
- Binary predictionはpositive-class probability、Regressionはnumeric predictionを維持する。
- TRAIN-only preprocessing、TEST isolationを変更しない。
- effective seed/deterministic settingsをruntime metadataへ伝播する。

## 4. Focused verification

- binary/regression deterministic synthetic fit/predict
- task mismatch and invalid parameter
- seed/effective parameter evidence
- TEST/preprocessing isolation regression

## 5. Protected invariants

existing logistic/linear behavior、P01 capability contract、no-silent-fallback、no TEST feedback、no unrelated refactor。

## 6. Completion boundary

focused verification PASS、package-local blocker NONE、package report + exact checkpoint SHA。terminal stateは `PACKAGE_READY` または `BLOCKED_*`。
