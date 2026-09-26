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

## 2. Architecture values required before freeze

capabilities API schema/version、model parameter UI schema、default model selection、unavailable/incompatible state semantics、client/server validation boundaryを06/07と一致させる。

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
