# ENH-E10 設計書改定 — Predictive Advanced Modeling / XAI

> **Document class:** Planning / Decision Artifact  
> **Status:** `MATERIALIZED / ARCHITECTURE_APPROVED / NOT_FROZEN`  
> **Self-containment:** MUST for own subject

- Enhancement: `ENH-E10`
- Accepted pre-E10 code baseline: `c56a8809dea688380b113210bef12c30b50ca7f6`
- Source design documents:
  - `docs/wiki/requirement_definition/22_product_basic_design.md`
  - `docs/wiki/requirement_definition/23_api_interface_design.md`
  - `docs/wiki/requirement_definition/30_detailed_design.md`
- Requirement delta: `00_enhance_background/03_requirements_revision.md`
- Freeze state: **NOT FROZEN — Architecture Review approved; canonical application/final traceability/Gate freeze remain**

## 1. Current design constraints to preserve

Current design establishes:

- Predictive runtime uses `predictive-analysis-spec/1` and full plan `split -> prepare -> train -> evaluate -> optional explain`.
- Navigation `setup / train / predict / metrics / explainability / model-management` is not 1:1 with runtime Stage.
- Setup owns feature editing; Train/Predict consume feature identity read-only.
- `GET /projects/{project_id}/predictive/capabilities` already exists as Predictive capability metadata endpoint.
- Metrics may be a read surface over persisted `EVALUATION_RESULT`.
- Model Management may be a read surface over `TRAINING_RESULT`, `MODEL_CARD_RESULT`, `FITTED_MODEL`, `MODEL_CARD`.
- UI/navigation change alone must not alter backend scientific semantics.
- external analytical engine must not become mandatory core dependency.

## 2. Proposed design delta

### 2.1 Model Capability layer

Current small model registryをprovider-neutral capability registryへ拡張する。

Proposed descriptor responsibilities:

- `model_id`
- model contract version
- supported task types
- parameter schema/default metadata
- provider/library identity
- optional dependency requirement
- current availability + unavailable reason
- provider/library version when available
- deterministic/seed capability metadata
- serializer/loader identity
- explanation capability hooks or compatibility attributes

Model selection authorityはbackend capability layerに置く。frontend hard-coded model ID branchをauthorityにしない。

### 2.2 Model Backend adapter

model provider固有処理をrunnerから分離可能なadapter contractへ寄せる。

Conceptual operations:

- validate parameters
- fit
- predict
- serialize
- load
- describe provenance

Existing logistic/linear implementationは同一high-level contractを満たすlegacy-compatible backendとして保持する。

LightGBM classifier/regressorはtask-specific backendとして追加する。

### 2.3 Fitted-model Artifact

Existing linear `fitted-model/1` JSON contractを破壊的にprovider objectへ置換しない。

Architecture Reviewで次のどちらかをfreezeする。

**Option A — versioned provider-neutral artifact envelope**
- new fitted-model schema version
- metadata/envelopeはcanonical JSON
- provider model payloadはprovider-supported durable serialization
- loader identity/provider/versionをmetadataへ保持
- existing `fitted-model/1` read compatibilityを維持

**Option B — provider-specific artifact schema**
- linear v1を維持
- LightGBM用artifact schemaを明示追加
- common model descriptorからprovider-specific loaderへdispatch

Common invariant:

- Python pickleをportable/canonical contractとして暗黙採用しない。
- external model objectをJSON正本として保存しない。
- feature order/name、task、model ID、parameters、seed、preprocessor hashをartifact identityに結び付ける。
- fresh-process相当load後にpredict可能とする。

### 2.4 Optional dependency lifecycle

Proposed package topology:

```text
Ariadne core
  + optional predictive-advanced capability
      - LightGBM
      - SHAP
      - LIME
```

exact group name/version boundsはfreeze前に決定する。

Dependency resolver responsibilities:

- core import時にadvanced package import failureを発生させない
- capability discovery時にavailability/versionを報告
- selected unavailable model/methodをstable capability errorへ変換
- unavailable capabilityからexisting model/methodへsilent fallbackしない

### 2.5 Explanation Method Capability layer

Existing single constant/string branchをmethod capability registryへgeneralizeする。

Descriptor responsibilities:

- method ID/version
- global support
- local support
- required model/prediction interface
- compatible model/provider/task attributes
- dependency requirement/availability/version
- output-scale semantics
- background/reference requirement
- sampling/reproducibility parameters

Initial methods:

- existing Linear Coefficient Contribution
- SHAP
- LIME

exact canonical method IDsはfreeze decision。

### 2.6 SHAP adapter

Design intent:

- LightGBMはTreeSHAPをprimary candidateとするが、final compatibilityはArchitecture Reviewでfreezeする。
- classification/regressionのprovider output shapeをcanonical resultへnormalizeする。
- global summaryとlocal sample explanationを別semanticとして保持する。
- output scaleを明示する。
- expected/base value、feature mapping、sample identity、background/reference provenanceを保持する。
- additivityをacceptanceに含める場合はscale/toleranceをfreezeする。

未決:
- binary classification SHAP scale
- background/reference dataset
- linear model SHAP support
- exact global aggregation
- additivity metadata/tolerance

### 2.7 LIME adapter

Design intent:

- E10ではlocal explanation primary。
- global非対応を正式capabilityとして表現する案を第一候補とする。
- instance identity、feature representation、seed、number of samples/features、kernel/discretization等をprovenanceへ保持する。
- unsupported global requestからpseudo-global aggregateを生成しない。

未決:
- perturbation/discretization defaults
- number of samples/features
- classification target semantics
- original vs preprocessed feature representation
- exact reproducibility guarantee

### 2.8 Canonical explanation result

provider raw objectをpublic Result schemaとして直接露出しない。

Canonical representationは少なくとも次を表現可能とする。

- method identity/version
- model identity
- global/local scope
- analytical status
- model output scale / prediction output scale
- feature identities/order
- local instance/sample identity
- background/reference identity
- contributions/importances in normalized form
- base/expected value where method supports it
- warnings/limitations
- seed/effective parameters
- provider/library version

methodで意味のないfieldをfake valueで埋めない。capability差はschema/capability metadataで明示する。

### 2.9 Capabilities API

Existing:
`GET /projects/{project_id}/predictive/capabilities`

をextension pointとして使用する。

Responseはfrontendが次を判断できる情報を提供する。

- task-compatible model options
- availability/unavailable reason
- model parameter schema/default metadata
- explanation methods
- model-method compatibility
- global/local support
- provider/library version availability

backend validationがfinal authorityであり、capabilities responseはclient convenience onlyにならないよう同一domain authorityから生成する。

response schema/versionを新設するかはfreeze decision。

### 2.10 Frontend integration

#### Train

- capability-driven model selector
- capability-driven model parameter controls
- task change時にincompatible modelを保持しない
- Setup-owned feature editを移管しない
- feature contextはread-only

#### Explainability

- current modelにcompatibleなmethodのみvalid selection
- global/local capabilityを明示
- unavailable reasonを表示
- predictive-not-causal limitationを維持
- raw provider object dumpだけをuser-facing contractにしない

#### Model Management

read-oriented scopeを維持し、少なくとも:

- model ID / task / parameters
- provider/library version
- seed/deterministic metadata
- feature/preprocessor identity
- fitted-model artifact
- Model Card
- explanation method metadata
- lineage/runtime provenance

を確認可能にする。

## 3. Authority / ownership changes

### Changes

- model compatibility/availability authority: backend Model Capability registry
- explanation compatibility authority: backend Explanation Method Capability + model capability resolution
- frontend option construction: backend capabilities metadataのconsumer
- provider serialization/load authority: model backend/loader layer

### Unchanged

- AnalysisSpecification remains analytical input authority.
- Planner/Execution/Stage lifecycle authority remains existing workflow architecture.
- Navigation Stage is not runtime execution authority.
- Setup remains feature editing authority.
- Predictive scientific validation remains backend authority.

## 4. Runtime / data-flow changes

Proposed flow:

```text
predictive-analysis-spec
  -> validation
  -> model capability resolution
  -> optional dependency availability check
  -> TRAIN preprocessing
  -> provider model fit
  -> fitted model artifact serialization
  -> load/predict adapter
  -> VALIDATION evaluation
  -> untouched TEST final evaluation
  -> explanation capability resolution
  -> SHAP/LIME/coefficient explanation
  -> Result / Artifact / Model Card / lineage
  -> capabilities-driven presentation
```

TEST explanation data must not feed model fitting/selection.

## 5. Persistence / migration changes

Current expectation:

- DB schema migration: **not assumed**
- new persistent entity: **not required**
- Artifact metadata/schema evolution: **likely**
- Result payload/schema evolution: **possible**
- `predictive-analysis-spec/1` revision: **undecided**

Prefer additive/versioned artifact/result evolution over DB schema change unless Architecture Review finds a hard requirement.

## 6. Compatibility / rollout strategy

1. preserve existing logistic/linear model IDs and behavior
2. preserve existing coefficient explanation for compatible linear models
3. advanced packages optional
4. unavailable advanced capability explicitly reported
5. no silent fallback
6. existing saved predictive specs remain readable
7. if spec/artifact schema version changes, old reader compatibility or explicit migration/read adapter must be defined
8. G01 backend contract before G02 explanation; G03 product integration only after both PASS

## 7. Transition Debt candidates

No Transition Debt is approved at this stage.

Potential temporary states that require explicit approval if introduced:

- dual fitted-model artifact versions
- compatibility adapter for `fitted-model/1`
- legacy frontend payload branch retained during staged migration

If accepted, each must receive explicit TD ID, owner Gate, exit criterion, and regression obligation before Gate freeze.

## 8. Gate implications

### G01

Freeze:
- model descriptors
- LightGBM IDs/tasks/parameters
- dependency behavior
- serializer/loader/artifact version
- seed/determinism
- model provenance/failure taxonomy

### G02

Freeze:
- method descriptors/IDs
- compatibility
- SHAP scale/background/global-local
- LIME local/global/perturbation/reproducibility
- canonical explanation schema
- method provenance/failure taxonomy

### G03

Freeze:
- capabilities API response
- parameter UI contract
- unavailable-state UX
- model-method selection UX
- Model Management provenance display
- two canonical Browser E2E journeys/environment

## 9. Architecture Review resolution

Technical Architecture Review is complete. The canonical review artifacts are:

- `40_operator_workflows/architecture_review/01_architecture_discovery.md`
- `40_operator_workflows/architecture_review/02_target_architecture_decision_record.md`
- `40_operator_workflows/architecture_review/03_gate_decomposition.md`

The former blocking design questions are technically resolved as follows.

| Concern | Architecture decision |
|---|---|
| Optional dependency | `predictive-advanced` extra; LightGBM `>=4.7.0,<4.8`, SHAP `>=0.52.0,<0.53`, LIME `==0.2.0.1`; lazy discovery/import |
| Model IDs | `lightgbm_classifier.v1`, `lightgbm_regressor.v1`; existing linear IDs remain defaults |
| LightGBM parameters | bounded E10 subset: num_boost_round, learning_rate, num_leaves, max_depth, min_data_in_leaf, lambda_l2 |
| Categorical / missing | keep existing TRAIN-fitted one-hot + mean-imputation; no LightGBM native categorical/missing semantics in E10 |
| Early stopping | out of scope |
| Determinism | CPU, deterministic=true, force_col_wise=true, num_threads=1; same-runtime/config stability only |
| Model Artifact | new provider-neutral `fitted-model/2` envelope; linear JSON payload and LightGBM model-string payload; `fitted-model/1` read compatibility |
| SHAP | `SHAP_TREE`; LightGBM only; tree_path_dependent; raw LOG_ODDS for binary / PREDICTION for regression; global mean-absolute contribution over TEST; local FIRST_N |
| LIME | `LIME_TABULAR`; local-only; preprocessed feature space; deterministic TRAIN reference sample; explicit global unsupported |
| Explanation schemas | keep v1 result/artifact/model-card schemas and extend additively |
| Predictive spec | keep `predictive-analysis-spec/1` |
| Capabilities API | keep `predictive-capabilities/1` and extend additively from backend capability authorities |
| UI unavailable state | visible + disabled + reason; no silent fallback |
| Browser E2E | G03 only; dedicated advanced API/worker image/compose override; 2 blocking critical journeys |

### 9.1 Model artifact decision

Architecture Review selects the provider-neutral envelope option.

New writes use `fitted-model/2` so provider identity, loader identity, feature/preprocessor identity, determinism and provenance share one canonical envelope. Existing `fitted-model/1` remains readable for backward compatibility. Python pickle/joblib is not the canonical portable representation.

### 9.2 SHAP decision

Binary LightGBM explanation is frozen on raw model output (`LOG_ODDS`), not probability-space SHAP. This preserves a stable additive contract without requiring interventional background data. Regression uses raw `PREDICTION` scale.

### 9.3 LIME decision

LIME is local-only. It operates on the same preprocessed feature space consumed by the model and uses a deterministic TRAIN-derived explanation reference sample. Global LIME is explicitly unsupported; no pseudo-global aggregation is generated.

### 9.4 Schema / persistence decision

No DB migration is required by ENH-E10 architecture. Existing Product Result/Artifact persistence is reused.

`predictive-analysis-spec/1` and `predictive-capabilities/1` remain version 1 because the required E10 additions are additive within the existing extensibility points.

### 9.5 Gate / Work Package decision

Semantic Gate decomposition remains:

```text
G01 Predictive Model Backend Contract
  -> G02 Predictive Explanation Backend Contract
  -> G03 Predictive Product Integration Contract
```

Each Gate uses three Work Packages for execution/failure localization only. Work Package completion is not a Gate acceptance boundary.

## 10. Remaining pre-freeze workflow

Architecture questions are no longer technically open. Remaining blockers before Gate freeze are governance/application steps:

1. apply the approved requirement delta to canonical requirement/design documents.
2. save the approved revised requirement/design snapshot.
3. finalize 05 traceability review against that canonical snapshot.
4. freeze G01–G03 06/07/Pxx in one internally consistent batch.

Until those steps complete, implementation remains NOT EXECUTABLE.
