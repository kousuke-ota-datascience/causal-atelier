# Ariadne ENH-E10 G02 実装指示書 — Predictive Explanation Backend Contract

**Document class:** Primary Execution Contract
**Contract status:** `MATERIALIZED_DRAFT / NOT_EXECUTABLE`
**Execution mode:** `WORK_PACKAGE` — decision materialized; execution remains blocked until contract freeze
**Required packages:** `P01, P02, P03`
**First executable package:** `P01`
**Depends on:** `G01 PASS`
**Self-containment:** MUST when FROZEN; current artifact is a materialized authoring draft
**Execution eligibility:** **NOT EXECUTABLE** until Human approval is recorded, G01 PASS exists, and 06/07/P01-P03 are explicitly FROZEN.

- Project: Ariadne
- Enhancement: ENH-E10
- Active Gate: G02
- Gate name: Predictive Explanation Backend Contract
- Branch: `feature/ariadne_mvp_e10`
- Accepted pre-E10 code baseline: `c56a8809dea688380b113210bef12c30b50ca7f6`
- Mutable Control Sheet: N/A

## 1. Gate definition / acceptance claim

### Gate objective

existing `LINEAR_COEFFICIENT_CONTRIBUTION` を保護したまま、model capabilityに基づいてSHAP / LIMEを明示的に選択できるPredictive Explanation backendを成立させる。global/local capability、model-method compatibility、output scale、background/reference data、sampling、reproducibility、provenanceをmethod-specific contractとして扱う。

### Contract claim established by PASS

G02 PASS後、G03は次へ依存してよい。

- explanation method registry/capabilityから、modelに適用可能なmethodを機械可読に解決できる。
- existing coefficient explanationは既存linear modelで引き続き利用できる。
- SHAPはfrozen contractで定義されたmodel/taskに対しglobal/local explanationを生成できる。
- LIMEはfrozen contractで定義されたmodel/taskに対しlocal explanationを生成でき、global非対応をcapabilityとして明示する。
- unsupported model-method combinationとoptional dependency absenceは明示errorとなり、coefficient/他methodへのsilent fallbackはない。
- explanation artifact/resultはmethod、model identity、feature identity、sample identity、output scale、background/reference、seed、library version等のprovenanceを再構成可能にする。
- Predictive Explanationをcausal explanation / treatment effectとして表現しない。

### Why this is one Gate

SHAP/LIMEの価値は個々のlibrary wrapperではなく、model-method compatibility、global/local capability、method-specific semantics、artifact/provenanceを共通Explanation contractの下で扱えることにあるため、一つのacceptance boundaryとする。

## 2. Effective current context

Accepted baselineでは以下を確認済み。

- `explanation_runner.py` は `SUPPORTED_EXPLANATION_METHOD = "LINEAR_COEFFICIENT_CONTRIBUTION"`。
- unsupported methodではapproximate fallbackせず `NOT_APPLICABLE` + `EXPLANATION_METHOD_NOT_APPLICABLE` を返す。
- explanation datasetとmodelの `feature_order` mismatchを拒否する。
- coefficient global explanationはcoefficient/absolute coefficient、local explanationはfeature value × coefficientを出力する。
- binary modelのcoefficient explanation `model_output_scale` は `LOG_ODDS`、prediction outputは `PROBABILITY`。
- Predictive Explanation result/artifactとModel Cardは既に存在し、predictive-not-causal diagnostics/limitationsを保持する。
- `explanation_dataset` はTEST partition由来で `explanation_only=True` として分離されている。
- SHAP/LIMEはbaseline dependencyに存在しない。

## 3. Architecture Review decisions — effective values for freeze

Source decision record: `40_operator_workflows/architecture_review/02_target_architecture_decision_record.md`.

1. **Method IDs**
   - existing `LINEAR_COEFFICIENT_CONTRIBUTION`
   - new `SHAP_TREE`
   - new `LIME_TABULAR`
2. **Compatibility**
   - logistic/linear: coefficient global+local; LIME local; SHAP unsupported.
   - LightGBM classifier/regressor: SHAP global+local; LIME local; coefficient unsupported.
   - no execution-time fallback.
3. **SHAP**
   - `shap.TreeExplainer`, LightGBM only.
   - `feature_perturbation="tree_path_dependent"`.
   - no explicit external background matrix.
   - binary model-output = raw `LOG_ODDS`; prediction output remains `PROBABILITY`.
   - regression model-output = raw `PREDICTION`.
   - global = mean absolute SHAP contribution over the entire immutable TEST explanation dataset, plus signed mean.
   - local = existing deterministic FIRST_N sampling.
   - additivity check is mandatory; Ariadne tolerance `atol=1e-6, rtol=1e-5`.
4. **LIME**
   - local-only; global request is explicitly unsupported.
   - representation = preprocessed model feature space.
   - binary target = positive-class probability; regression target = numeric prediction.
   - defaults: num_samples=2000, num_features=min(10,n_features), feature_selection=auto, discretize_continuous=false, distance_metric=euclidean, kernel_width=0.75*sqrt(n_features), sample_around_instance=false.
   - one-hot output columns are categorical binary LIME features; limitation must state that perturbation can form invalid original-category combinations.
   - each explained row gets an independently derived deterministic seed from sampling seed + row identity.
5. **Explanation reference**
   - PREPARE adds internal `predictive-explanation-reference/1` from transformed TRAIN features.
   - role = `EXPLANATION_REFERENCE_ONLY`.
   - deterministic sample without replacement, max 500 rows, seed = explanation sampling seed.
   - raw reference rows are runtime bindings only; persisted Result/Artifact records hash/count/seed/provenance, not raw rows.
6. **Optional dependency**
   - `predictive-advanced` extra uses SHAP `>=0.52.0,<0.53` and LIME `==0.2.0.1`.
   - availability is resolved per package; absence does not break core/G01.
7. **Schemas**
   - keep `predictive-explanation-result/1`, `predictive-explanation-artifact/1`, `predictive-model-card-result/1`, `predictive-model-card-artifact/1`; extend additively.
   - semantically unsupported fields are omitted/null by contract, not fabricated.
8. **Failure taxonomy**
   - `EXPLANATION_METHOD_NOT_REGISTERED`
   - `EXPLANATION_METHOD_NOT_APPLICABLE`
   - `EXPLANATION_DEPENDENCY_UNAVAILABLE`
   - `EXPLANATION_SCOPE_NOT_SUPPORTED`
   - `EXPLANATION_COMPUTATION_FAILED`
9. **Predictive-not-causal**
   - existing semantic limitation remains mandatory.

Human approval remains required before this Gate set is changed to FROZEN.


