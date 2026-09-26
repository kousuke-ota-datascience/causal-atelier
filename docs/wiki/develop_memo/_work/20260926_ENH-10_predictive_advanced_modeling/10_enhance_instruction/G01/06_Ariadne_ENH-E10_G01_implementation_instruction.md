# Ariadne ENH-E10 G01 実装指示書 — Predictive Model Backend Contract

**Document class:** Primary Execution Contract
**Contract status:** `FROZEN`
**Execution mode:** `WORK_PACKAGE`
**Required packages:** `NOT_MATERIALIZED`
**First executable package:** `NONE`
**Depends on:** `ENH-E9 final PASS / accepted pre-E10 baseline`
**Self-containment:** MUST — this frozen contract is the Gate implementation authority
**Execution eligibility:** **BLOCKED_PACKAGE_MATERIALIZATION** — contract is FROZEN; coding starts only after required Pxx execution contracts are materialized.

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

## 3. Frozen execution-precondition decisions — MUST resolve by explicit amendment before coding

本書は `FROZEN` である。以下はCoding Agentへ委譲しないexecution-precondition decisionとして固定し、Pxx materialization前にapproved amendmentで一意に確定する。

1. model capability interfaceとregistry entry schema
2. LightGBM model ID / version naming
3. optional dependency group名とpackage version bounds
4. dependency availability / version capability metadata
5. LightGBM parameter schema / defaults / invalid parameter taxonomy
6. categorical feature handlingをE10 scopeへ含めるか
7. missing value responsibilityをpreprocessing側に残すかLightGBM native handlingを許可するか
8. early stoppingをE10 scopeへ含めるか
9. deterministic seed / LightGBM deterministic settings
10. fitted-model artifact schema/version、serialization format、load adapter interface
11. feature order/name preservationとmismatch rejection
12. package/runtime provenance fields
13. failure taxonomyとHTTP/application error mapping
14. `predictive-analysis-spec/1` を維持するかversion revisionするか

本freeze以降、以下のpreconditionを具体化する変更はexplicit amendmentとして扱う。Gate execution開始後は06/07をsilent rewriteしない。

## 4. Expected execution-mode decomposition

`WORK_PACKAGE` をexecution modeとしてfreezeする。Required Pxxは未materializeであり、想定implementation boundaryは以下。

- model capability/registry + optional dependency availability
- LightGBM binary/regression adapter + parameter validation
- fitted-model serialization/load + prediction parity + provenance
- protected linear-model regression / integration assembly

P00/PxxはArchitecture Review後に作成し、06のsemantic contractを分割・変更しない。

## 5. Required implementation semantics

G01実装は最低限以下を満たすこと。

1. **Registry / capability**
   - model entryはtask compatibility、parameter schema、dependency requirement、availability/version、determinism capabilityを機械可読に表現する。
   - unsupported task/model combinationを明示的に拒否する。
   - unavailable optional dependencyをregistryから既存linear modelへsilent fallbackしない。

2. **Optional dependency**
   - LightGBMをcore mandatory dependencyへ追加しない。
   - LightGBM未導入でもAriadne core import/start、既存linear predictive flow、non-predictive flowを壊さない。
   - LightGBMを要求した時点でstable capability errorと必要package情報を返す。

3. **Model adapters**
   - Binary ClassificationとRegressionのLightGBM adapterをtask-specificに解決する。
   - prediction output contractはBinary Classificationではpositive-class probability、Regressionではnumeric predictionを維持する。
   - train/validation/test responsibilityを既存Predictive workflowから逸脱させない。

4. **Artifact / load**
   - fitted modelをdurable artifactとしてserializeし、fresh process相当のload pathからprediction可能にする。
   - serialize前後のprediction parityをdeterministic fixtureで検証可能にする。
   - feature order/name、preprocessor identity、model/task identityをartifactに結び付け、mismatchを拒否する。

5. **Reproducibility / provenance**
   - effective seedとdeterministic settingsを記録する。
   - model library名/version、Ariadne model ID/version、parameters、feature order、preprocessor hash、runtime metadataを再構成可能にする。
   - reproducibility保証範囲を過大に主張しない。

6. **Backward compatibility**
   - existing logistic/linear model selection、training、evaluation、artifact/result contractをE10の都合で削除しない。
   - existing preprocessing leakage prevention、TEST isolation、dataset-schema-backed feature semanticsを維持する。

## 6. Allowed scope

- predictive model capability / registry
- LightGBM classifier/regressor adapters
- model parameter validation
- optional dependency declaration / capability discovery
- fitted-model serialization/load/prediction adapter
- predictive artifact/result/model-card provenance fields
- G01に必要なAPI/domain contract
- G01の新規/ materially rebuilt automated tests

## 7. Explicitly prohibited scope

- SHAP/LIME implementation（G02）
- Train/Explainability/Model Managementのproduct-wide UI integration（G03）
- multiclass, survival, forecasting, ranking, recommendation
- AutoML / automated tuning expansion
- online inference / deployment API / production monitoring
- causal interpretation / CATE / HTE / EconML
- Project Management、Causal workflow、Graph workflow、Identification UX、Causal diagnosticsの変更
- repository-wide test migration
- mandatory LightGBM dependency
- unsupported caseのsilent fallback

## 8. Protected upstream contracts

| Source | Protected semantic | Mandatory regression |
|---|---|---|
| ENH-E8 | Predictive Navigation Stage responsibility separation; Setup owns feature editing; Train/Predict read-only | stage/navigation contract remains intact |
| ENH-E9 | stabilized workflow and non-predictive surfaces | no unrelated Project/Causal/Graph regressions |
| Predictive baseline | TEST isolation + TRAIN-only preprocessing fit | leakage/isolation tests |
| Predictive baseline | logistic/linear registry behavior | protected linear-model regression |

## 9. Schema / API / runtime policy

- `predictive-analysis-spec/1`、`fitted-model/1`、result/artifact schemaのrevision要否はexecution-precondition decisionであり、実装者が独断でversionを変更しない。
- model artifactを既存linear JSON形式へ偽装してLightGBMを格納しない。
- provider-specific serializationを採用する場合、artifact metadata/schemaからloaderを一意に解決可能にする。
- dependency unavailable / model task mismatch / invalid parameter / feature mismatchは区別可能なfailure taxonomyを持つ。

## 10. Automated test obligations

新規またはmaterially rebuilt testは原則 `tests/enhancement/enh_e10/g01/<layer>/` に置く。

最低限:

- binary synthetic fixture: LightGBM train → serialize → load → predict parity
- regression synthetic fixture: 同上
- fixed seedでのconfig-stable behavior
- task mismatch
- invalid parameter
- unavailable optional dependency
- feature order/name mismatch rejection
- preprocessor/model identity mismatch
- package/version provenance
- existing logistic/linear protected regression
- TEST partition isolation / preprocessing leakage prevention

numeric/scientific correctnessとserialization parityはUnit/Contract/Integrationをprimary proofとする。G01ではBrowser E2EをGate blocking requirementにしない。

既存testを移動する場合はpath/import/fixture/conftest/repository-root resolution/pytest marker/Docker/CI/evidence pathを同一batchで扱い、単なる移動でfrozen behaviorを変えない。

## 11. Candidate Assembly requirement

`READY_FOR_TEST` 前に:

- all required execution units complete
- G01-wide integration self-check complete
- protected linear-model regression complete
- optional-dependency absence scenario complete
- unresolved candidate-affecting change = NONE
- Fixed Trial Candidate SHA fixed
- Implementation Completion Report created

Package checkpoint単体をFixed Trial Candidateとしない。

## 12. Coding Agent prohibited work

- Gate Decision
- Acceptance Criteria変更
- test回避のための07変更
- passed/upstream semanticの無断変更
- G02/G03先行実装
- package scope外の便乗変更
- repository-wide test cleanup

## 13. Required outputs after execution

- package execution status / checkpoint reports（WORK_PACKAGE時）
- Fixed Trial Candidate SHA
- implementation completion report
- Gate-local implementation detail
- dependency/provenance evidence

## 14. Stop condition

本書は `FROZEN` である。ただしRequired Pxxが未materializeの間はcodingを開始せず `BLOCKED_PACKAGE_MATERIALIZATION` とする。Pxx materialization後のCoding sideは `READY_FOR_TEST` または明示的 `BLOCKED_*` で停止し、Gate PASSを宣言しない。
