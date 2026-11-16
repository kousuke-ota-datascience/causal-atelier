<!-- ENH-E11 split working copy: not a formal approval. -->
# 30 — predictive advanced xai

**Status:** `STRUCTURAL_COPY_DRAFT` (existing baseline text, not E11 canonical publication)

**Source:** [30_detailed_design.md](https://github.com/kousuke-ota-datascience/causal-atelier/blob/3ba5fe2465ec591f0da7f998c21a5241984b73dc/docs/wiki/requirement_definition/30_detailed_design.md) · blob `04d83541e55ab0364500afb4b92ef55c10785a0c`  
**Index:** [Revised document inventory](../README_00_Revised_requirements_definition_documents.md)

---

## 15. Predictive Capability（続き）

### 15.10 LightGBM backend / fitted-model/2

LightGBM backend uses low-level `lightgbm.train` / `Booster`.

Exposed parameter validation:

| Parameter | Contract |
|---|---|
| `num_boost_round` | integer 1..2000, default 100 |
| `learning_rate` | 0 < x <= 1, default 0.1 |
| `num_leaves` | integer 2..256, default 31 |
| `max_depth` | -1 or integer 1..64, default -1 |
| `min_data_in_leaf` | integer 1..10000, default 20 |
| `lambda_l2` | finite >= 0, default 0 |

Fixed runtime parameters include objective by task, CPU, `metric=None`, `deterministic=true`, `force_col_wise=true`, `num_threads=1`, immutable execution/spec seed, `verbosity=-1`, `use_missing=false`.

Existing PREPARE output remains authoritative. LightGBM receives the TRAIN-fitted transformed numeric matrix; native categorical/missing handling and early stopping are not part of ENH-E10.

New training writes use:

```text
schema_version = fitted-model/2
model_id
model_contract_version
task_type
parameters
seed
feature_order
preprocessor_hash
provider { id, library, library_version }
determinism { mode, deterministic, force_col_wise, num_threads, device_type }
payload { format, ... }
classes? 
```

Payload:

- linear: `ariadne-linear-json/1`
- LightGBM: `lightgbm-model-string/1` using provider-supported model string serialization

Loader dispatch is by provider/payload format. Existing `fitted-model/1` loader remains supported. Serialize→load→predict parity is required on deterministic fixtures.

Reproducibility claim is same-runtime/config stability. Cross-platform/compiler/library-version bitwise equality is not promised.

### 15.11 Explanation Method Capability registry

Methods:

- `LINEAR_COEFFICIENT_CONTRIBUTION`
- `SHAP_TREE`
- `LIME_TABULAR`

Compatibility:

| Model | Coefficient | SHAP_TREE | LIME_TABULAR |
|---|---|---|---|
| logistic_regression.v1 | global + local | unsupported | local |
| linear_regression.v1 | global + local | unsupported | local |
| lightgbm_classifier.v1 | unsupported | global + local | local |
| lightgbm_regressor.v1 | unsupported | global + local | local |

No method fallback is performed.

Canonical explanation Result/Artifact/Model Card schemas remain version 1 and receive additive method/provider/model/reference fields. Unsupported fields are not fabricated.

### 15.12 SHAP_TREE

Use `shap.TreeExplainer` for LightGBM.

- `feature_perturbation="tree_path_dependent"`
- no external background matrix
- binary `model_output="raw"` => model-output scale `LOG_ODDS`
- regression raw output => `PREDICTION`
- binary prediction output shown elsewhere remains `PROBABILITY`
- global importance = mean absolute SHAP value over the complete immutable TEST explanation dataset; signed mean is also recorded
- local rows follow deterministic FIRST_N sampling
- record TEST row identity/hash and tree-path reference semantics
- verify additivity with `atol=1e-6`, `rtol=1e-5`

Additivity failure is an explanation computation/scientific contract failure and is not silently disabled.

### 15.13 LIME_TABULAR / explanation reference

LIME is local-only.

Model representation is the same preprocessed feature space referenced by fitted model `feature_order`.

PREPARE produces internal `predictive-explanation-reference/1` from transformed TRAIN features:

- role = `EXPLANATION_REFERENCE_ONLY`
- seeded sample without replacement
- max rows = 500
- seed = explanation sampling seed
- raw reference rows are runtime binding only
- persisted explanation provenance contains hash/count/seed/reference role, not raw reference rows

LIME defaults:

- `num_samples=2000`
- `num_features=min(10, n_features)`
- `feature_selection="auto"`
- `discretize_continuous=false`
- `distance_metric="euclidean"`
- `kernel_width=0.75*sqrt(n_features)`
- `sample_around_instance=false`

One-hot transformed columns are supplied as categorical binary features. Limitation metadata must state that independent perturbation can form combinations that are not one valid original categorical row.

Binary local explanation targets positive-class probability. Regression targets numeric prediction. Per-row effective random seed is deterministically derived from explanation sampling seed + row identity.

A global LIME request, or a LIME request with local explanations disabled, returns `EXPLANATION_SCOPE_NOT_SUPPORTED`.

### 15.14 Capability-driven presentation

Train:

- obtains compatible models and structured parameter controls from `predictive-capabilities/1`
- retains current selection when task-compatible
- otherwise switches to backend-declared task default
- shows unavailable advanced option disabled with reason
- does not edit feature set

Explainability:

- derives valid methods/scope from model-method compatibility metadata
- linear default = coefficient
- LightGBM default = SHAP_TREE
- LIME is explicit local alternate
- unavailable/incompatible selection never silently falls back
- preserves Predictive-not-causal warning

Model Management remains read-only and renders persisted model/provider/artifact/model-card/explanation/lineage/runtime provenance.


---
