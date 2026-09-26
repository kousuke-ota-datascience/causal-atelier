# Ariadne ENH-E10 G01 実装指示書 — Predictive Model Backend Contract

**Document class:** Primary Execution Contract
**Contract status:** `MATERIALIZED_DRAFT / NOT_EXECUTABLE`
**Execution mode:** `WORK_PACKAGE` — decision materialized; execution remains blocked until contract freeze
**Required packages:** `P01, P02, P03`
**First executable package:** `P01`
**Depends on:** `ENH-E9 final PASS / accepted pre-E10 baseline`
**Self-containment:** MUST when FROZEN; current artifact is a materialized authoring draft
**Execution eligibility:** **NOT EXECUTABLE** until §3 architecture decisions are resolved and 06/07/P01-P03 are explicitly FROZEN.

- Project: Ariadne
- Enhancement: ENH-E10
- Active Gate: G01
- Gate name: Predictive Model Backend Contract
- Branch: `feature/ariadne_mvp_e10`
- Accepted pre-E10 code baseline: `c56a8809dea688380b113210bef12c30b50ca7f6`
- Mutable Control Sheet: N/A — verified state is derived from canonical reports and Gate Decisions

## 1. Gate definition / acceptance claim

### Gate objective

既存のlinear predictive modelを壊さず、Binary Classification / RegressionについてLightGBM backendをAlgorithm Registryから明示的に選択でき、training、fitted-model artifact、load、prediction、provenance確認までを一貫したmodel capability contractとして成立させる。

### Contract claim established by PASS

G01がfinal PASSした後、後続Gateは次を成立済みcontractとして依存してよい。

- `logistic_regression.v1` と `linear_regression.v1` の既存behaviorが維持されている。
- Binary Classification用LightGBM classifierとRegression用LightGBM regressorがtask-compatible modelとしてregistryから解決できる。
- model固有parameter validation、deterministic seed policy、feature identity/order、preprocessing identity、artifact serialization/load、prediction semanticsが明示contractとして固定されている。
- LightGBM未導入環境でもAriadne coreはimport/start可能であり、LightGBM選択時だけ明示的capability errorになる。silent fallbackは発生しない。
- fitted-model / Model Card / runtime metadataからmodel ID、task、parameters、seed/determinism、feature identity、package availability/versionを追跡できる。

### Why this is one Gate

registry selection、fit、artifact、load、predict、provenanceは「model backendが実際に利用可能である」という同一acceptance claimを構成する。LightGBM classifier/regressorを別Gateへ分けるとartifact/load/prediction contractを重複させるため、G01では一つのsemantic acceptance boundaryとして扱う。

## 2. Effective current context

Accepted pre-E10 baseline `c56a8809...` では以下を確認済み。

- `src/ariadne/capabilities/predictive/modeling.py` のregistryは `logistic_regression.v1` と `linear_regression.v1` の2種。
- current fitted modelは `fitted-model/1` JSONで、係数・intercept等を直接保持する。
- `PredictiveTrainRunner` はTRAINでmodelをfitし、`preprocessor_hash`、`feature_order`、`seed`を付加して `FITTED_MODEL` artifactを生成する。
- `PredictiveEvaluateRunner` はfrozen modelとTRAIN-fitted preprocessorのidentity整合を検証し、TESTのみでfinal evaluationを行う。
- `pyproject.toml` にはLightGBM / SHAP / LIMEおよびpredictive-advanced optional dependency groupは存在しない。
- requirement `FR-161` はLightGBM等のexternal analytical engineをmandatory dependencyとして追加することを禁止している。
- `FR-061` はtask-compatible Algorithm Registry selectionを要求し、`FR-068` はfitted model等のdurable outputをArtifactとして保持する。

Historical handoffの仮説は上記baselineでは確認されたが、implementation時にはcurrent checkoutで再確認する。

## 3. Architecture Review decisions — effective values for freeze

Source decision record: `40_operator_workflows/architecture_review/02_target_architecture_decision_record.md`.

These values are no longer delegated to Coding Agents.

1. **Model capability**
   - existing: `logistic_regression.v1`, `linear_regression.v1`
   - new: `lightgbm_classifier.v1` / `BINARY_CLASSIFICATION`
   - new: `lightgbm_regressor.v1` / `REGRESSION`
   - existing logistic/linear remain task defaults.
2. **Optional dependency**
   - extra: `predictive-advanced`
   - `lightgbm>=4.7.0,<4.8`
   - `shap>=0.52.0,<0.53`
   - `lime==0.2.0.1`
   - advanced imports are lazy; core import/start MUST NOT require the extra.
3. **LightGBM exposed parameters**
   - `num_boost_round`: integer [1,2000], default 100
   - `learning_rate`: number (0,1], default 0.1
   - `num_leaves`: integer [2,256], default 31
   - `max_depth`: -1 or integer [1,64], default -1
   - `min_data_in_leaf`: integer [1,10000], default 20
   - `lambda_l2`: finite number >=0, default 0.0
4. **LightGBM fixed runtime**
   - objective = binary / regression by task
   - `metric=None`, `device_type=cpu`, `deterministic=true`, `force_col_wise=true`, `num_threads=1`, `verbosity=-1`, `use_missing=false`
   - seed = immutable execution/spec seed.
5. **Feature handling**
   - preserve existing TRAIN-fitted mean imputation + scaling + one-hot preprocessing.
   - no LightGBM native categorical handling.
   - no LightGBM native missing handling.
   - early stopping is out of scope.
6. **Model API**
   - provider backend uses low-level LightGBM `train` / `Booster`.
   - Binary prediction contract remains positive-class probability.
   - Regression prediction contract remains numeric prediction.
7. **Artifact**
   - all new training writes `fitted-model/2` provider-neutral envelope.
   - linear payload: `ariadne-linear-json/1`.
   - LightGBM payload: `lightgbm-model-string/1` from `Booster.model_to_string()`.
   - loader dispatch uses provider/payload format.
   - existing `fitted-model/1` remains readable; no in-place rewrite; no canonical pickle/joblib.
8. **Reproducibility/provenance**
   - guarantee = same-runtime/config stability, not cross-platform bitwise identity.
   - record effective seed, deterministic settings, provider/library version, Python/code version, feature order and preprocessor identity.
9. **Failure taxonomy**
   - `MODEL_NOT_REGISTERED`
   - `MODEL_TASK_MISMATCH`
   - `MODEL_PARAMETER_INVALID`
   - `MODEL_DEPENDENCY_UNAVAILABLE`
   - `MODEL_ARTIFACT_UNSUPPORTED`
   - `MODEL_ARTIFACT_LOAD_FAILED`
   - `MODEL_FEATURE_MISMATCH`
   - existing `PREPROCESSOR_MODEL_MISMATCH`
10. **Schema**
    - keep `predictive-analysis-spec/1`.
    - no DB migration required by G01 architecture.

Human approval of the Architecture Review remains required before changing this Gate set to FROZEN.


