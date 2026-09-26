# ENH-E10 Target Architecture Decision Record — Predictive Advanced Modeling / XAI

> **Document class:** Architecture Review / Target Decision Record  
> **Status:** `APPROVED` — technical review complete and Human-approved  
> **Enhancement:** `ENH-E10`  
> **Decision date:** `2026-09-26`

## 1. Context

ENH-E10 adds LightGBM Binary Classification / Regression and Predictive XAI (SHAP/LIME) without making external analytical engines mandatory and without changing Predictive stage responsibility, TEST isolation, TRAIN-only preprocessing, or predictive-not-causal semantics.

The target design must be implementable on the current generic Product Execution / Result / Artifact architecture.

## 2. Current architecture facts

Current-state facts are recorded in `01_architecture_discovery.md`. The key constraints are:

- `predictive-analysis-spec/1` already carries extensible model/method IDs and parameters.
- preprocessing emits a finite numeric transformed feature matrix.
- `fitted-model/1` is coefficient-specific.
- canonical Artifact persistence accepts arbitrary bytes and metadata.
- `predictive-capabilities/1` already exists.
- existing explanation result/artifact/model-card schemas are extensible.
- frontend must consume backend capability authority rather than recreate it.

## 3. Decision

### ADR-E10-01 — Optional dependency topology

Create PEP 621 optional extra:

```toml
[project.optional-dependencies]
predictive-advanced = [
  "lightgbm>=4.7.0,<4.8",
  "shap>=0.52.0,<0.53",
  "lime==0.2.0.1",
]
```

Core install remains unchanged.

Dependency availability/version is resolved lazily with `importlib.util.find_spec` / `importlib.metadata.version`; advanced packages MUST NOT be imported at Ariadne core module import time.

### ADR-E10-02 — Model IDs and capability descriptor

Add:

- `lightgbm_classifier.v1` — `BINARY_CLASSIFICATION`
- `lightgbm_regressor.v1` — `REGRESSION`

Existing IDs remain unchanged.

Each model capability exposes:

- `model_id`
- `contract_version = "1"`
- `supported_tasks`
- legacy `parameter_schema` compatibility projection
- structured `parameters` definitions
- `provider`
- `dependency`
- `available`
- `unavailable_reason`
- `provider_version`
- `determinism`
- `serializer_id`
- `loader_id`
- `default_for_tasks`

Existing logistic/linear remain the defaults for their tasks.

### ADR-E10-03 — LightGBM parameter contract

E10 exposes only:

| Parameter | Type / range | Default |
|---|---|---|
| `num_boost_round` | integer `[1,2000]` | `100` |
| `learning_rate` | number `(0,1]` | `0.1` |
| `num_leaves` | integer `[2,256]` | `31` |
| `max_depth` | `-1` or integer `[1,64]` | `-1` |
| `min_data_in_leaf` | integer `[1,10000]` | `20` |
| `lambda_l2` | finite number `[0,+inf)` | `0.0` |

Internal fixed parameters:

- binary objective: `binary`
- regression objective: `regression`
- `metric = None`
- `device_type = cpu`
- `deterministic = true`
- `force_col_wise = true`
- `num_threads = 1`
- `seed = immutable execution/spec seed`
- `verbosity = -1`
- `use_missing = false`

Use the low-level `lightgbm.train` / `Booster` contract rather than sklearn wrapper as the backend serialization authority.

### ADR-E10-04 — Categorical, missing, early stopping

- E10 does **not** use LightGBM native categorical features.
- E10 does **not** use LightGBM native missing-value handling.
- Existing TRAIN-fitted mean imputation + one-hot preprocessing remains authoritative.
- early stopping is **out of scope**.
- validation data remains evaluation evidence and is not used to change the trained model through early stopping.

### ADR-E10-05 — Reproducibility

Required reproducibility claim is **same-runtime/config stability**, not cross-platform bitwise identity.

Record:

- effective seed
- deterministic=true
- force_col_wise=true
- num_threads=1
- LightGBM version
- Python version
- Ariadne code version
- feature/preprocessor identity

Different LightGBM versions, compiler builds, OS/architecture may produce different results and MUST NOT be claimed deterministic across environments.

### ADR-E10-06 — Fitted model artifact

Adopt **provider-neutral `fitted-model/2` envelope** for all newly trained models.

Required common fields:

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
classes?  # classification only
```

Payload formats:

- Ariadne linear: `ariadne-linear-json/1` with coefficients/intercept/classes
- LightGBM: `lightgbm-model-string/1` containing provider-supported `Booster.model_to_string()`

Loader dispatch is by payload format/provider identity.

Existing persisted `fitted-model/1` remains readable; it is not rewritten in place. Python pickle is not canonical.

### ADR-E10-07 — Model failure taxonomy

Stable Predictive codes:

- `MODEL_NOT_REGISTERED`
- `MODEL_TASK_MISMATCH`
- `MODEL_PARAMETER_INVALID`
- `MODEL_DEPENDENCY_UNAVAILABLE`
- `MODEL_ARTIFACT_UNSUPPORTED`
- `MODEL_ARTIFACT_LOAD_FAILED`
- `MODEL_FEATURE_MISMATCH`
- existing `PREPROCESSOR_MODEL_MISMATCH`

Synchronous spec/capability errors map through `PredictiveValidationError` to HTTP 422. Provider runtime/load failures become structured Stage failure evidence and are not silently converted to another model.

### ADR-E10-08 — Explanation method IDs / compatibility

Methods:

- existing `LINEAR_COEFFICIENT_CONTRIBUTION`
- `SHAP_TREE`
- `LIME_TABULAR`

Compatibility:

| Model | Coefficient | SHAP_TREE | LIME_TABULAR |
|---|---:|---:|---:|
| logistic_regression.v1 | global + local | no | local |
| linear_regression.v1 | global + local | no | local |
| lightgbm_classifier.v1 | no | global + local | local |
| lightgbm_regressor.v1 | no | global + local | local |

No execution-time fallback between methods.

### ADR-E10-09 — SHAP semantics

Use `shap.TreeExplainer` for LightGBM only.

- `feature_perturbation = "tree_path_dependent"`
- no external background matrix is passed
- background/reference semantics = training leaf-path counts embedded in the fitted tree model
- Binary Classification `model_output = "raw"` => `LOG_ODDS`
- Regression `model_output = "raw"` => `PREDICTION`
- prediction output remains `PROBABILITY` for binary and `PREDICTION` for regression
- local base value + feature contributions are additive in model-output space
- global explanation = mean absolute SHAP contribution over the entire immutable TEST explanation dataset; also record signed mean
- local explanations use existing deterministic FIRST_N sampling
- record TEST row-ordinal identity/hash and background/reference role
- additivity check uses SHAP check plus Ariadne `allclose(atol=1e-6, rtol=1e-5)`; failure is a product/scientific contract failure, not silently disabled

### ADR-E10-10 — LIME semantics

LIME is **local-only** in E10. Global LIME is unsupported.

Feature representation is the model's **preprocessed feature space** to preserve alignment with `feature_order` and current coefficient explanation.

Add new internal `predictive-explanation-reference/1` produced from TRAIN transformed features:

- role = `EXPLANATION_REFERENCE_ONLY`
- deterministic seeded sample without replacement
- max rows = `500`
- seed = `explanation_spec.sampling.seed`
- persist only provenance/hash/count in explanation Result/Artifact; raw reference rows are not persisted as explanation output

LIME fixed defaults:

- `num_samples = 2000`
- `num_features = min(10, model feature count)`
- `feature_selection = "auto"`
- `discretize_continuous = false`
- `distance_metric = "euclidean"`
- `kernel_width = 0.75 * sqrt(feature_count)`
- `sample_around_instance = false`

One-hot output columns are supplied to LIME as categorical binary features. Limitation must state that independent perturbation can generate combinations that do not correspond to one valid original categorical row.

Binary classification explains the positive-class probability; regression explains numeric prediction.

For each local row, derive an independent deterministic random seed from `sampling.seed + row identity` rather than reusing one advancing RNG. Record the effective per-row seed, surrogate score, intercept, local prediction, model prediction, and weights.

If `LIME_TABULAR` is selected while `local_explanations=false`, reject explicitly with `EXPLANATION_SCOPE_NOT_SUPPORTED`.

### ADR-E10-11 — Explanation schemas

Keep:

- `predictive-explanation-result/1`
- `predictive-explanation-artifact/1`
- `predictive-model-card-result/1`
- `predictive-model-card-artifact/1`

Extend additively with method/provider/model provenance and method-specific fields.

Do not fill semantically unsupported fields with fake values.

Failure taxonomy:

- `EXPLANATION_METHOD_NOT_REGISTERED`
- `EXPLANATION_METHOD_NOT_APPLICABLE`
- `EXPLANATION_DEPENDENCY_UNAVAILABLE`
- `EXPLANATION_SCOPE_NOT_SUPPORTED`
- `EXPLANATION_COMPUTATION_FAILED`

Existing coefficient unsupported/no-approximation behavior remains protected.

### ADR-E10-12 — Predictive analysis spec and capabilities API

Keep `predictive-analysis-spec/1`; no schema version bump.

Keep `predictive-capabilities/1`; extend additively.

Capabilities must preserve existing fields/types and add:

- top-level `task_defaults`
- model `contract_version`
- structured model `parameters` definitions/defaults
- model provider/dependency availability/version/reason
- model determinism/serializer/loader/default-for-task metadata
- explanation dependency availability/version/reason/default-for-model metadata
- `model_explanation_compatibility`

Existing `parameter_schema`, `deterministic_seed`, `compatibility`, and explanation `method/supported_models/supports_global/supports_local/model_output_scales` remain compatibility projections.

Backend resolver remains final validation authority.

### ADR-E10-13 — Frontend behavior

- existing logistic/linear remain task defaults
- current compatible model selection is retained on task change; incompatible selection switches to the backend-declared task default
- unavailable advanced capabilities are **visible but disabled with reason**, not hidden
- selecting an unavailable capability never falls back silently
- model parameter controls are generated from capability `parameters` definitions
- linear model default explanation = coefficient
- LightGBM default explanation = SHAP_TREE
- if default method is unavailable, UI shows the unavailable state; another method requires explicit user selection
- Setup remains feature-edit authority
- Model Management remains read-only

### ADR-E10-14 — Browser E2E runtime

G03 owns two blocking Browser journeys.

Create ENH-E10-specific advanced runtime:

- `Dockerfile.predictive-advanced` installs `.[predictive-advanced]`
- `compose.enh_e10.yaml` overrides API/worker build to the advanced image
- core `Dockerfile` / normal compose remain core-only
- Browser container remains Playwright 1.62.0 and receives a new ENH-E10 runner copied into the image

Canonical G03 browser lifecycle:

1. `docker compose ... -p ariadne-enh-e10 down -v --remove-orphans`
2. build API/worker/frontend/browser from current source
3. start clean DB/migrate/API/worker/frontend
4. run ENH-E10 browser runner
5. capture trace/screenshot/network/API/worker evidence
6. teardown with `down -v --remove-orphans`

Canonical runner path is `tests/enhancement/enh_e10/g03/browser_e2e/run_predictive_advanced.py`.

The blocking compose stack is `compose.yaml + compose.e1a.yaml + compose.enh_e10.yaml`, project `ariadne-enh-e10`. The exact command sequence and evidence contract are materialized in G03 07/P03 before freeze.

## 4. Canonical authorities

| Concern | Canonical authority after completion |
|---|---|
| Model registration/availability/parameters | backend Model Capability registry |
| Model provider execution | Model Backend adapter |
| Model durable representation | `fitted-model/2` envelope + provider loader |
| Legacy model read | `fitted-model/1` compatibility loader |
| Explanation method compatibility | backend Explanation Method registry |
| SHAP semantics | SHAP_TREE adapter contract |
| LIME semantics | LIME_TABULAR adapter contract |
| Optional package state | lazy dependency resolver |
| Client option construction | `predictive-capabilities/1` generated from backend authorities |
| Predictive input | `predictive-analysis-spec/1` |
| Execution lifecycle | existing generic Product Execution |
| Feature editing | Setup |
| TEST final evaluation | existing Evaluate stage |

## 5. Invariants

| ID | Invariant | Verification implication |
|---|---|---|
| INV-01 | core import/start does not require advanced engines | isolated core-only environment test |
| INV-02 | unavailable capability never falls back | negative model/method tests + UI/API |
| INV-03 | TEST never participates in model selection/fitting | leakage/isolation regression |
| INV-04 | preprocessing fits on TRAIN only | preprocessor identity regression |
| INV-05 | artifact/load preserves identity and prediction | fresh-load parity |
| INV-06 | feature order/preprocessor mismatch is rejected | negative contract tests |
| INV-07 | explanation is model behavior, not causal effect | result/model-card/UI assertions |
| INV-08 | LIME global is unsupported, not synthesized | negative capability test |
| INV-09 | frontend does not become compatibility authority | capability/API contract tests |
| INV-10 | G03 Browser E2E proves connectivity, not numeric science | test-layer allocation audit |

## 6. Constraints

- Python `>=3.12,<3.13`
- no DB migration required by architecture
- no multiclass/forecasting/ranking/recommendation
- no early stopping/AutoML expansion
- no production serving/model registry
- no causal interpretation
- no repository-wide test migration

## 7. Explicitly removed / deprecated paths

- frontend logistic-vs-else parameter construction as model authority
- frontend task-to-model hard-coded compatibility as authority
- coefficient-only fitted model shape as the only new-write model artifact format

Existing `fitted-model/1` read support is retained.

## 8. Transition strategy and temporary debt

No Transition Debt is approved.

Versioned `fitted-model/1` read compatibility is a permanent backward-compatibility path for E10, not temporary debt.

Rollout order:

1. G01 model capability + v2 artifact
2. G02 explanation capability
3. G03 product integration

## 9. Alternatives considered

- Mandatory advanced dependencies — rejected by FR-161.
- Provider-specific LightGBM artifact without common envelope — rejected because it duplicates identity/provenance contract.
- Pickle/joblib canonical model artifact — rejected for portability/security/version opacity.
- LightGBM native categorical/missing semantics — rejected because current preprocessing is already authoritative.
- probability-space SHAP for binary — rejected because it requires interventional background data and complicates stable additivity; raw log-odds aligns with current coefficient scale.
- global LIME aggregation — rejected because it would create a pseudo-global semantic not supplied by LIME.
- predictive spec v2 — rejected because current spec already has the required extensibility.
- capabilities v2 — rejected because required additions are backward-compatible additive metadata.

## 10. Consequences / risks

- LIME 0.2.0.1 is old and must be treated as an optional adapter with strong contract tests.
- LIME transformed-space perturbation has interpretation limitations; these must be surfaced.
- LightGBM reproducibility is runtime-scoped, not cross-platform.
- v1/v2 fitted-model loader compatibility increases model backend test surface.
- SHAP provider output shape must be normalized and tested against LightGBM specifically.
- advanced Browser E2E needs a dedicated runtime image because core images intentionally omit optional engines.

## 11. External evidence

Reviewed on 2026-09-26:

- LightGBM PyPI: https://pypi.org/project/lightgbm/
- LightGBM parameters: https://lightgbm.readthedocs.io/en/latest/Parameters.html
- LightGBM Booster API: https://lightgbm.readthedocs.io/en/latest/pythonapi/lightgbm.Booster.html
- SHAP PyPI: https://pypi.org/project/shap/
- SHAP TreeExplainer: https://shap.readthedocs.io/en/latest/generated/shap.TreeExplainer.html
- LIME PyPI: https://pypi.org/project/lime/
- LIME tabular source/API: https://github.com/marcotcr/lime/blob/master/lime/lime_tabular.py

## 12. Approval

- Technical review: **COMPLETE**
- Status: **APPROVED**
- Human architecture approval: **APPROVED**
- Gate freeze authorization: **GRANTED AFTER canonical requirement/design application and final traceability review**
- Timestamp: `2026-09-26T14:58:00+09:00`
