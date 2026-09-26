# ENH-E10 G01 P01 — Model Capability / Optional Dependency

**Document class:** Work Package Execution Contract  
**Status:** `FROZEN`  
**Gate:** `G01`  
**Package:** `P01`  
**Depends on:** `NONE`  
**Self-containment:** `MUST`  
**Information isolation:** `MUST`  
**Execution eligibility:** `SUBJECT_TO_AGENT_EXECUTION_READINESS`
**Status at issuance:** `FROZEN`

## 0. Frozen authority

This P01 is the assigned-Pxx implementation authority after Agent Execution Readiness returns READY. The accepted pre-E10 baseline is protected context, not a runtime package dependency. Canonical requirement/design snapshot: `3e22d09e7e68e65aceb54d1a3a32cab697d7b480`.

## 1. Package objective

model capability registry、task compatibility、parameter metadata、optional dependency availability/version/error taxonomyをbounded execution unitとして成立させ、P02へ引き渡せるcheckpointを作る。

## 2. Effective architecture values

- Model IDs: `lightgbm_classifier.v1`, `lightgbm_regressor.v1`.
- Existing logistic/linear remain task defaults.
- Optional extra: `predictive-advanced`.
- LightGBM bound: `>=4.7.0,<4.8`.
- Capability descriptor includes structured parameters, provider/dependency availability/version/reason, determinism, serializer/loader IDs, task default.
- Dependency discovery/import is lazy and MUST NOT break core import/start.
- Error codes owned by this package: `MODEL_NOT_REGISTERED`, `MODEL_TASK_MISMATCH`, `MODEL_PARAMETER_INVALID`, `MODEL_DEPENDENCY_UNAVAILABLE`.
- `predictive-analysis-spec/1` remains unchanged.

## 3. Required behavior

- provider-neutral model capability descriptorを定義し、task compatibility、parameter schema/default metadata、dependency requirement、availability/version、determinism metadataを機械可読にする。
- existing logistic/linear registry behaviorを保護する。
- LightGBM optional dependencyのavailability discoveryをcore import/startから分離する。
- unavailable model selection、task mismatch、invalid parameterを区別可能なerror taxonomyへ接続する。
- silent fallbackは禁止する。

## 4. Focused verification

- existing logistic/linear registry regression
- task compatibility matrix
- optional dependency absent/import isolation
- parameter validation/error taxonomy

## 5. Protected invariants

- Gate 06/07のsemantic claim / Acceptance Criteriaを変更しない。
- TEST isolation / TRAIN-only preprocessing fitを変更しない。
- unrelated workflowへ変更を広げない。
- test expectationを弱めない。

## 6. Completion boundary

scope内implementation complete、focused verification PASS、package-local blocker NONE、package report作成、exact `PACKAGE_CHECKPOINT_SHA` 固定。terminal stateは `PACKAGE_READY` または明示的 `BLOCKED_*`。PACKAGE_READYはGate PASSではない。
