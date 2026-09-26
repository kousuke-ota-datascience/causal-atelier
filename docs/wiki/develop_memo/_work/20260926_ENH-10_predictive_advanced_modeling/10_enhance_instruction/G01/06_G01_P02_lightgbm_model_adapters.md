# ENH-E10 G01 P02 — LightGBM Model Adapters

**Document class:** Work Package Execution Contract  
**Status:** `FROZEN`  
**Gate:** `G01`  
**Package:** `P02`  
**Depends on:** `P01`  
**Self-containment:** `MUST`  
**Information isolation:** `MUST`  
**Execution eligibility:** `BLOCKED_PREREQUISITE_P01`
**Status at issuance:** `FROZEN`

## 0. Frozen authority

This P02 becomes executable only after the canonical P01 package report records `PACKAGE_COMPLETE` and Agent Execution Readiness for P02 returns READY. Canonical requirement/design snapshot: `3e22d09e7e68e65aceb54d1a3a32cab697d7b480`.

## 1. Package objective

Binary Classification / Regression用LightGBM adapter、parameter validation、seed/determinism、fit/predict semanticsを成立させ、P03へ引き渡す。

## 2. Effective architecture values

Exposed parameters:

- `num_boost_round`: integer [1,2000], default 100
- `learning_rate`: (0,1], default 0.1
- `num_leaves`: integer [2,256], default 31
- `max_depth`: -1 or integer [1,64], default -1
- `min_data_in_leaf`: integer [1,10000], default 20
- `lambda_l2`: finite >=0, default 0.0

Fixed runtime:

- objective by task; metric=None
- CPU, deterministic=true, force_col_wise=true, num_threads=1
- seed = immutable execution/spec seed
- verbosity=-1, use_missing=false
- existing mean-imputation/scaling/one-hot preprocessing remains authoritative
- no native categorical/missing and no early stopping
- use low-level LightGBM train/Booster interface

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
