# ENH-E10 G03 P01 — Capabilities / Train Integration

**Document class:** Work Package Execution Contract  
**Status:** `MATERIALIZED_DRAFT / NOT_EXECUTABLE`  
**Gate:** `G03`  
**Package:** `P01`  
**Depends on:** `G01 PASS + G02 PASS`  
**Self-containment:** MUST when FROZEN  
**Information isolation:** MUST  
**Execution eligibility:** `BLOCKED_CONTRACT_NOT_FROZEN`

## 1. Package objective

capabilities API consumer contract、task-compatible model selection、model-specific parameter rendering/serialization、unavailable state、stage responsibility regressionを成立させ、P02へ引き渡す。

## 2. Effective architecture values

`predictive-capabilities/1` remains the schema. Existing fields/types are retained; add:

- top-level `task_defaults`
- model `contract_version`, structured `parameters`, provider/dependency/availability/version/reason, determinism, serializer/loader IDs, default_for_tasks
- explanation dependency/availability/version/reason/default_for_models
- top-level `model_explanation_compatibility`

Retain legacy `parameter_schema`, `deterministic_seed`, `compatibility` and existing explanation fields as compatibility projections.

Task defaults remain logistic/linear. Task change retains a compatible current selection; otherwise selects backend task default. Unavailable advanced models are visible-disabled with reason. Parameter controls consume structured `parameters`; backend remains final validation authority.

## 3. Required behavior

- predictive capabilities API/domain outputをG01/G02 capability authorityから構成し、frontend独自compatibility authorityを持たせない。
- Train model selectorをtask-compatible capability-drivenにする。
- model-specific parameter controls/serializationをcapability parameter schemaから生成する。
- task change時のincompatible selection、unavailable optional backend、invalid parameterを明示する。
- Setup feature editing authority、Train/Predict read-only feature contextを維持する。

## 4. Focused verification

capabilities API/model schema contract、classification/regression task switch、model-specific parameter rendering/serialization、unavailable/incompatible state、stage responsibility regression。

## 5. Completion boundary

focused verification PASS、package report、exact checkpoint SHA、blocker NONE。terminal stateは `PACKAGE_READY` または `BLOCKED_*`。
