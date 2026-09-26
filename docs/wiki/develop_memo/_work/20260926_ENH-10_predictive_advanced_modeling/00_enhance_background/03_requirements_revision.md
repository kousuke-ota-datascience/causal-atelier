# ENH-E10 要件定義書改定 — Predictive Advanced Modeling / XAI

> **Document class:** Planning / Decision Artifact  
> **Status:** `MATERIALIZED / PROPOSED_REQUIREMENT_DELTA / NOT_APPLIED`  
> **Self-containment:** MUST for own subject

- Enhancement: `ENH-E10`
- Accepted pre-E10 code baseline: `c56a8809dea688380b113210bef12c30b50ca7f6`
- Canonical requirement source: `docs/wiki/requirement_definition/10_requirements_definition.md`
- Application state: **proposal only; canonical requirements have not yet been rewritten**
- Approval dependency: `02_enhancement_concept_approval_record.md`

## 1. Source requirements

Relevant current requirements:

- `FR-061` — Algorithm Registryからtask対応modelを選択できる
- `FR-063` — fixed spec/splitからtrainingできる
- `FR-064` — TESTをmodel selectionに使用しない
- `FR-068` — fitted model/preprocessor/prediction等をArtifactとして保存
- `FR-069` — global/local Predictive Explanation
- `FR-070` — Predictive Explanationとcausal explanationを区別
- `FR-071` — Model Card
- `FR-149–152` — Predictive navigation/stage responsibility
- `FR-161` — external analytical engineをmandatory dependencyとして追加しない
- `NFR-001a/b` — reproducibility metadata / scientific library version / effective seed
- `NFR-013` — schema evolution
- `NFR-015` — layer-separated testability
- `NFR-016` — scientific transparency
- `AR-003` — Predictive Explanationはcausal explanationではない
- `AR-009` — external model objectをJSON正本へ保存しない
- `AR-011` — preprocessingはTRAINのみでfit
- `AR-012` — TESTをselectionに使用しない
- `AR-019` — partition artifact等を保存
- `AR-020` — local explanationをpotentially sensitive outputとして扱う
- `AR-025` — MetricsとExplainabilityを分離しcausal effectへ読み替えない

## 2. Requirement delta

以下はcanonical requirement documentへ適用するための**proposed delta**である。新規IDはcurrent branch上の既存番号との衝突がないことをapply時に再確認する。

| Requirement ID | Before | Proposed After | Reason |
|---|---|---|---|
| FR-061 | task-compatible modelをAlgorithm Registryから選択 | registry entryはtask compatibilityに加えmodel capability、parameter schema、optional dependency availability/versionを表現し、利用可能なtask-compatible modelを選択できる | LightGBMをstatic branchではなくcapabilityとして追加するため |
| FR-068 | fitted model等をArtifactとして保存 | provider-specific fitted modelもdurable Artifactとして保存し、artifact identity/schemaから対応loaderを解決して再読込・predictionできる | train→artifact→load→predictをproduct contractにするため |
| FR-069 | global/local Predictive Explanationを生成 | explanation method capabilityに応じ、global/localのsupported scopeを保持してPredictive Explanationを生成する | SHAP/LIME/coefficientでcapabilityが異なるため |
| FR-071 | Model Cardへintended use/training data/metric/limitations | model/provider/version/effective parameters/seed/feature/preprocessor identity/explanation method等、再現性に必要なprovenanceをcurrent contractに従って記録する | advanced backendの再現性・監査性確保 |
| FR-161 | external analytical engineをmandatory dependencyとして追加しない | **維持**。LightGBM/SHAP/LIMEをoptional capabilityとして導入し、未導入でもcore startup/existing supported flowを壊さない | E10 scopeと既存constraintを両立 |
| FR-178 (NEW proposed) | N/A | Binary Classification / RegressionでLightGBM backendをtask-compatible modelとして選択できる | E10 named capability acceptance |
| FR-179 (NEW proposed) | N/A | optional model dependencyが利用不可の場合、明示的capability-unavailable error/stateを返し、別modelへsilent fallbackしない | optional dependency safety |
| FR-180 (NEW proposed) | N/A | fitted modelはserialize/load round-trip後もmodel/task/feature/preprocessor identityを保持し、同一fixtureでprediction contractを満たす | artifact/load correctness |
| FR-181 (NEW proposed) | N/A | Predictive Explanation methodはmodel-method compatibilityを検証し、coefficient / SHAP / LIMEを明示methodとして解決する | incompatible explanation防止 |
| FR-182 (NEW proposed) | N/A | SHAPはfrozen compatibility範囲でglobal/local、LIMEはfrozen contractでlocal capabilityを提供し、unsupported capabilityを擬似出力で補完しない | method semantics preservation |
| FR-183 (NEW proposed) | N/A | explanation Result/Artifactはmethod、model、feature/sample identity、output scale、background/reference、seed、package version等のprovenanceを保持する | XAI traceability |
| FR-184 (NEW proposed) | N/A | Train / Explainability / Model Managementはbackend capability metadataを利用してcompatible option、availability、provenanceを表示し、frontendを独立compatibility authorityにしない | product integration |
| NFR-028 (NEW proposed) | N/A | optional analytical engineのimport/availability failureをcore process startup failureへ伝播させず、capability選択時に局所化して報告する | optional dependency isolation |
| AR-027 (NEW proposed) | N/A | SHAP/LIME/coefficient contributionはmodel behavior explanationであり、feature causal importance、treatment effect、causal mechanismを意味しない | XAI scientific interpretation guard |

## 3. New invariants / constraints

1. **Optional, not mandatory**
   - LightGBM / SHAP / LIMEをcore mandatory dependencyへ入れない。
   - unavailable capabilityをexplicitに表現する。
   - silent fallback禁止。

2. **Model compatibility**
   - classifier/regressor task mismatchをbackend execution前にreject可能にする。
   - frontend listだけでcompatibilityを保証せずbackend authorityを維持する。

3. **Artifact/load**
   - external Python object/pickleをJSON正本として保存しない。
   - artifact schema/metadataからloader/provider/versionを一意に解決可能にする。
   - serialize/load前後でfeature/preprocessor/model identityを失わない。

4. **Reproducibility**
   - effective seedだけでなくlibrary version、model parameters、deterministic settings、feature identityを記録する。
   - cross-platform bitwise determinism等、実証していない保証を要求しない。

5. **Explanation semantics**
   - all methodsへ同じglobal/local capabilityを強制しない。
   - SHAP/LIME raw provider outputをそのままcanonical public schemaにしない。
   - output scale / sample / background/referenceを明示する。
   - incompatible/unsupported methodを別methodへfallbackしない。

6. **Protected predictive workflow**
   - TRAIN-only preprocessing。
   - TEST isolation。
   - Setup feature editing authority。
   - Train/Predict read-only feature context。
   - MetricsとExplainabilityのseparation。
   - Model Managementはread-oriented。
   - Predictive Explanationはnot causal。

## 4. Removed / deprecated requirements

**NONE proposed.**

ENH-E10は既存Predictive requirementsを削除・緩和するEnhancementではない。

特に以下を削除/relaxしない。

- FR-064 TEST isolation
- FR-070 predictive-not-causal
- FR-149–152 Predictive stage responsibility
- FR-161 mandatory dependency prohibition
- AR-011/012 leakage protection
- AR-025 Metrics/Explainability separation

## 5. Acceptance implications

Requirement deltaをGate acceptanceへ割り当てる。

### G01

- FR-061 revised
- FR-068 revised
- FR-071 revised model provenance subset
- FR-161
- FR-178/179/180
- NFR-001a/b
- NFR-028
- AR-009/011/012/019

Primary proof: Unit / Contract / Integration. Browser E2Eはblockingにしない。

### G02

- FR-069 revised
- FR-070
- FR-071 explanation provenance subset
- FR-181/182/183
- NFR-001a/b
- AR-003/020/025/027

Primary proof: Unit / Contract / Integration. Browser E2Eはblockingにしない。

### G03

- FR-149–152
- FR-184
- FR-161 optional capability presentation
- AR-003/025/027
- G01/G02 protected contracts

Primary proof: Frontend Contract / API Integration + two critical Browser E2E journeys.

## 6. Architecture Review resolution / approval boundary

Architecture Review technical decisions are recorded in:

- `40_operator_workflows/architecture_review/02_target_architecture_decision_record.md`

The previously open technical requirement questions are resolved for the proposed delta:

1. LIME global capability = explicitly unsupported; LIME is local-only.
2. `predictive-analysis-spec/1` is retained.
3. categorical/native missing handling is not added; existing TRAIN-fitted one-hot + mean-imputation remains authoritative.
4. early stopping is out of scope.
5. reproducibility guarantee = same-runtime/config stability with effective seed/library/runtime/determinism provenance; no cross-platform bitwise claim.
6. model artifact evolution = provider-neutral `fitted-model/2` new-write envelope with `fitted-model/1` read compatibility.
7. optional external engines remain optional and unavailable capability never silently falls back.

The remaining requirement-level decision is governance rather than technical ambiguity: whether proposed new IDs FR-178–FR-184 / NFR-028 / AR-027 are applied as written or folded into existing canonical requirement IDs during approved canonical update. Requirement ID collision must be rechecked at apply time.

本書は引き続き `PROPOSED_REQUIREMENT_DELTA / NOT_APPLIED` であり、Human approval前にcanonical requirement sourceを書き換えない。
