# ENH-E10 Enhance構想・要件改定計画 — Predictive Advanced Modeling / XAI

> **Document class:** Planning / Decision Artifact  
> **Status:** `MATERIALIZED / PROPOSAL_READY_FOR_REVIEW`  
> **Self-containment:** MUST for own subject

- Enhancement: `ENH-E10`
- Working title: Predictive Advanced Modeling / XAI
- Branch: `feature/ariadne_mvp_e10`
- Accepted pre-E10 code baseline: `c56a8809dea688380b113210bef12c30b50ca7f6`
- Primary handoff: `00_enhance_background/_handoff/ENH-E10 Handoff — Predictive Advanced Modeling - XAI.md`
- Upstream protected enhancements: ENH-E8, ENH-E9
- Implementation status: **NOT STARTED / architecture freeze required**

## 1. Problem statement

AriadneのPredictive Analysisは、accepted pre-E10 baselineではBinary Classification / Regressionの基本workflow、TRAIN-only preprocessing、TEST isolation、Result / Artifact / Model Card、linear coefficient based explanationまでを持つ。一方、model backendは実質 `logistic_regression.v1` / `linear_regression.v1` に限定され、Predictive Explanationも `LINEAR_COEFFICIENT_CONTRIBUTION` が中心である。

ENH-E10では、既存のPredictive workflowとENH-E8/E9で安定化したnavigation / product semanticsを壊さず、advanced predictive model / explanation capabilityを追加する必要がある。

対象 capability:

- LightGBM Binary Classification
- LightGBM Regression
- SHAP
- LIME

本Enhancementは単なるfrontend option追加ではなく、model capability、artifact/load、prediction、explanation compatibility、optional dependency、reproducibility、provenanceまで含むanalytical capability enhancementである。

## 2. Why now

ENH-E8でPredictive Navigation Stage responsibilityが明確化され、ENH-E9でworkflow stabilizationが完了したため、advanced model / explanationを既存UI/Runtimeへ追加しても、navigation再設計やCausal workflow変更と混在させず独立scopeとして扱える状態になった。

historical handoffでadvanced modeling / XAIは後続Enhancementへ分離されており、ENH-E10がそのcurrent authorityとなる。

## 3. Current-state problem

accepted baselineで確認した主要制約:

1. `src/ariadne/capabilities/predictive/modeling.py`
   - model registryは `logistic_regression.v1`, `linear_regression.v1`。
   - fitted modelは係数/intercept中心のJSON `fitted-model/1`。
2. `src/ariadne/capabilities/predictive/explanation_runner.py`
   - explanation methodは `LINEAR_COEFFICIENT_CONTRIBUTION`。
   - unsupported methodはexplicit `NOT_APPLICABLE` でありsilent fallbackしない。
3. `pyproject.toml`
   - LightGBM / SHAP / LIME dependencyは存在しない。
4. frontend
   - capabilities APIからmodel/method listを取得する構造は存在する。
   - 一方、model parameter payloadとtask changeにはlogistic/linear model ID前提のhard-coded branchが残る。
5. canonical requirements
   - `FR-061` はAlgorithm Registryからtask-compatible modelを選択可能とする。
   - `FR-068` はdurable fitted model等をArtifactとして保存する。
   - `FR-069/070/071` はPredictive Explanation / predictive-not-causal / Model Cardを要求する。
   - `FR-161` はLightGBM等external analytical engineの**mandatory dependency化を禁止**する。
   - `NFR-001b` はactual scientific library versionとeffective seedのprovenanceを要求する。
   - `AR-003` はPredictive Explanationをcausal explanationと区別する。

## 4. Target outcome

ENH-E10完了時に、次を成立させる。

- LightGBM classifier/regressorをtask-compatible registryから選択できる。
- LightGBM modelをtrainし、durable artifactへserializeし、load後にpredictionできる。
- existing logistic/linear model behaviorを維持する。
- SHAP / LIME / existing coefficient explanationをmodel-method compatibilityに基づいて選択できる。
- global/local capabilityの差をmethod contractとして表現できる。
- unsupported/unavailable capabilityをexplicit error/stateとして扱い、silent fallbackしない。
- LightGBM / SHAP / LIME未導入でもAriadne coreとexisting supported flowsが利用できる。
- model / explanation artifactからmodel identity、parameters、feature identity、seed、library/version、method、sample/background等のprovenanceを再構成できる。
- Train / Explainability / Model Managementがcapability-drivenに追加backendを利用できる。
- ENH-E8のPredictive Stage responsibility、TEST isolation、predictive-vs-causal terminologyを維持する。

## 5. Scope

### In scope

- model capability / registry generalization
- LightGBM classifier / regressor
- model-specific parameter schema
- task compatibility validation
- fitted-model serialization / load / prediction adapter
- feature order/name and preprocessor identity validation
- optional dependency capability discovery
- reproducibility / package-runtime provenance
- explanation capability / method registry
- SHAP global/local explanation
- LIME local explanation
- model × explanation compatibility
- explanation result/artifact/model-card provenance
- Predictive capabilities API extension
- Train / Explainability / Model Management product integration
- ENH-E10 scoped tests and two final critical Browser E2E journeys

### Out of scope

- multiclass classification
- survival / forecasting / ranking / recommendation
- AutoML / automated hyperparameter search expansion
- deployment API / online inference / production monitoring
- production model registry platform
- causal explanation / causal interpretation of SHAP or LIME
- CATE / HTE / EconML
- Causal Lifecycle changes
- Project Management / Graph / Identification / Causal diagnostics changes
- repository-wide test architecture migration

## 6. Requirement changes expected

Existing requirements remain authoritative unless explicitly revised. ENH-E10 proposes:

- strengthen `FR-061` with capability/availability semantics rather than a static registry list;
- retain `FR-161` and concretize external engines as optional capabilities;
- add explicit requirements for optional dependency absence behavior and no silent fallback;
- add explicit fitted-model serialize/load/predict round-trip requirement;
- add explicit model/library/version/seed/feature/preprocessor provenance requirement;
- strengthen `FR-069` into method-capability-aware global/local Predictive Explanation;
- add explicit model × explanation compatibility requirement;
- add explanation output-scale/background/sample/method provenance requirement;
- add capability-driven Train / Explainability / Model Management UI requirement;
- retain `AR-003` / `AR-025` predictive-not-causal boundary.

Detailed proposed deltas are in `03_requirements_revision.md`.

## 7. Design changes expected

- provider-neutral Model Capability descriptor
- model backend adapter boundary for fit / serialize / load / predict
- optional dependency resolver and availability metadata
- provider-aware fitted-model Artifact envelope/loader
- Explanation Method Capability descriptor
- model × method compatibility resolution
- canonical normalized SHAP/LIME result representation
- package/runtime provenance propagation
- capabilities API extension consumable by frontend
- capability-driven model parameter and explanation controls
- read-oriented Model Management extension

Detailed proposed design is in `04_design_revision.md`.

## 8. Risk / migration / compatibility

Primary risks:

- existing `fitted-model/1` linear JSON contractとprovider-specific model artifactの混在
- external library version差によるserialization / numerical reproducibility drift
- SHAP binary-classification output shape/scale ambiguity
- LIME perturbation/discretizationによるreproducibility誤認
- UIがbackend capability authorityを重複実装すること
- optional dependency absenceをimport-time failureへ変えてしまうこと
- existing Predictive specを不必要にversion-upすること
- Browser E2Eをscientific correctnessのprimary proofにしてしまうこと

Compatibility invariants:

- existing linear model flowを壊さない。
- `predictive-analysis-spec/1` は明示的revision decisionがない限り維持する。
- TESTをselection/trainingへ使用しない。
- preprocessingはTRAIN partitionのみでfitする。
- Predictive Explanationをcausal explanationとして扱わない。
- external enginesをcore mandatory dependencyにしない。

## 9. Architecture-review applicability

- Required: **YES**
- Reason: model backend abstraction、artifact serialization/load、optional dependency lifecycle、explanation compatibility/output semantics、capabilities APIを変更するため。これらは実装詳細ではなくcross-layer contractであり、Coding Agentへ委譲してはならない。

Architecture Reviewで最低限freezeする:

1. model capability interface / registry semantics
2. LightGBM model ID/version and parameter schema
3. optional dependency group/version bounds
4. fitted-model artifact format/version and loader
5. deterministic seed policy
6. Explanation Method capability interface
7. model × explanation compatibility
8. SHAP output scale / background / global-local semantics
9. LIME local/global / perturbation / seed semantics
10. capability/error taxonomy
11. capabilities API contract
12. backward compatibility / schema-version strategy
13. Browser acceptance environment

## 10. Proposed Gate decomposition

### G01 — Predictive Model Backend Contract

PASS claim: existing linear modelsを保護しつつ、LightGBM Binary Classification / Regressionをregistryから選択し、train → artifact → load → predict → provenanceまで成立する。

### G02 — Predictive Explanation Backend Contract

Depends on G01 PASS.

PASS claim: model capabilityに応じてSHAP / LIME / coefficient explanationを選択でき、global/local差、output scale、sample/background、provenanceをmethod-specific contractとして保持する。

### G03 — Predictive Product Integration Contract

Depends on G01 + G02 PASS.

PASS claim: Train / Explainability / Model Managementがadvanced capabilitiesをcapability-drivenに利用し、existing Predictive navigation/workflowを壊さずcritical browser journeysが成立する。

## 11. Approval required before implementation

Coding開始前に必要:

- concept/scope approval
- requirement delta approval
- Architecture Review decision
- 03/04/05のreview completion
- G01/G02/G03 06/07の`FROZEN`化
- P00/Pxx materialization（WORK_PACKAGE採用時）

現時点では上記approval/freezeは完了していないため、materialized Gate instructionsは `NOT_EXECUTABLE` のままとする。
