# ENH-E10 設計書改定 — Predictive Advanced Modeling / XAI

> **Document class:** Planning / Decision Artifact  
> **Status:** `MATERIALIZED / ARCHITECTURE_REVIEW_DRAFT / NOT_FROZEN`  
> **Self-containment:** MUST for own subject

- Enhancement: `ENH-E10`
- Accepted pre-E10 code baseline: `c56a8809dea688380b113210bef12c30b50ca7f6`
- Source design documents:
  - `docs/wiki/requirement_definition/22_product_basic_design.md`
  - `docs/wiki/requirement_definition/23_api_interface_design.md`
  - `docs/wiki/requirement_definition/30_detailed_design.md`
- Requirement delta: `00_enhance_background/03_requirements_revision.md`
- Freeze state: **NOT FROZEN**

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

## 9. Architecture decisions still open

The following are **blocking before FROZEN 06/07**:

1. optional dependency group name/version bounds
2. exact LightGBM model IDs
3. LightGBM parameter/default subset
4. categorical feature scope
5. native missing-value handling
6. early stopping
7. fitted-model artifact version/format
8. SHAP output scale/background/additivity
9. LIME local-only decision and defaults
10. predictive spec schema version
11. capabilities API schema/version
12. Browser E2E canonical command/environment

本書はArchitecture Review入力であり、これらをCoding Agentへ暗黙決定させない。
