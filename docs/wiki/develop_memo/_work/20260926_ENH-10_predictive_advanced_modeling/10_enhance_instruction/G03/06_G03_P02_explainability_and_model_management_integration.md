# ENH-E10 G03 P02 — Explainability / Model Management Integration

**Document class:** Work Package Execution Contract  
**Status:** `MATERIALIZED_DRAFT / NOT_EXECUTABLE`  
**Gate:** `G03`  
**Package:** `P02`  
**Depends on:** `G03 P01 canonical package report = PACKAGE_COMPLETE`  
**Self-containment:** MUST when FROZEN  
**Information isolation:** MUST  
**Execution eligibility:** `BLOCKED_CONTRACT_NOT_FROZEN`

## 1. Package objective

compatible method/global-local UI、explanation/result limitations、Model Management provenance/artifact/model-card presentationを成立させ、P03へ引き渡す。

## 2. Effective architecture values

- linear default explanation = `LINEAR_COEFFICIENT_CONTRIBUTION`.
- LightGBM default explanation = `SHAP_TREE`.
- `LIME_TABULAR` is an explicit local alternate on compatible models.
- unavailable methods are visible-disabled with reason; no fallback.
- scope controls derive from supports_global/supports_local.
- Model Management displays model/task/parameters, provider/library version, seed/determinism, feature/preprocessor identity, fitted-model artifact schema/ID, Model Card, explanation metadata, lineage/runtime provenance.
- Model Management remains read-only.
- predictive-not-causal wording remains mandatory.

## 3. Required behavior

- Explainability selectorをG02 compatibility/global-local capabilityから構成する。
- unavailable/incompatible methodを明示しsilent fallbackしない。
- method、scope、output scale、sample/background provenance、limitationsを表示する。
- Model Managementをread-orientedのままmodel/artifact/model-card/lineage/provider/runtime provenanceへ拡張する。
- Predictive Explanationをcausal explanationとして表示しない。

## 4. Focused verification

explainability capability UI/API contract、global/local/unavailable states、Model Management provenance/artifact/result rendering、predictive-not-causal wording、existing linear/coefficient product regression。

## 5. Completion boundary

focused verification PASS、package report、exact checkpoint SHA、blocker NONE。terminal stateは `PACKAGE_READY` または `BLOCKED_*`。
