# ENH-E10 要件・設計整合性およびトレーサビリティ確認

> **Document class:** Planning / Decision Artifact  
> **Status:** `MATERIALIZED / APPROVED_ARCHITECTURE / NOT_READY_FOR_IMPLEMENTATION`  
> **Self-containment:** MUST for own subject

- Enhancement: `ENH-E10`
- Requirement proposal: `03_requirements_revision.md`
- Design proposal: `04_design_revision.md`
- Gate drafts: `10_enhance_instruction/G01..G03`
- Approval record: `02_enhancement_concept_approval_record.md`
- Current approval state: `APPROVED`

## 1. Traceability matrix

| Requirement / Invariant | Proposed design realization | Gate | Acceptance mapping |
|---|---|---|---|
| FR-061 revised — capability-aware model registry | Model Capability descriptor + backend resolver | G01 | registry/task compatibility / backward compatibility |
| FR-068 revised — durable model round-trip | provider-aware serializer/loader + fitted-model Artifact | G01 | binary/regression train→serialize→load→predict |
| FR-161 — no mandatory external engine | optional dependency resolver + availability state | G01/G02/G03 | core startup/existing flow without advanced packages; explicit unavailable state |
| FR-178 proposed — LightGBM classifier/regressor | LightGBM task-specific model backends | G01 | binary + regression LightGBM integration |
| FR-179 proposed — no fallback on unavailable dependency | explicit capability-unavailable taxonomy | G01 | dependency-absence negative test |
| FR-180 proposed — artifact/load identity | model descriptor + feature/preprocessor identity + loader | G01 | round-trip parity / mismatch rejection |
| NFR-001a/b — seed/library provenance | model descriptor, artifact metadata, Model Card/runtime metadata | G01/G02/G03 | provenance audit |
| AR-009 — external model object not JSON canonical | versioned artifact payload + canonical metadata; no implicit pickle/JSON object dump | G01 | artifact format audit |
| AR-011/012 — TRAIN-only preprocessing / TEST isolation | existing prepare/evaluate boundaries preserved | G01/G02 | leakage/isolation regression |
| FR-069 revised — method-aware global/local explanation | Explanation Method Capability registry + canonical explanation result | G02 | coefficient/SHAP/LIME capability tests |
| FR-181 proposed — model-method compatibility | compatibility resolver | G02/G03 | unsupported combination rejection / UI compatibility |
| FR-182 proposed — SHAP/LIME method-specific capability | SHAP global/local adapter; LIME local contract candidate | G02 | SHAP binary/regression, LIME local, unsupported global |
| FR-183 proposed — explanation provenance | normalized result/artifact metadata | G02/G03 | output scale/sample/background/provider audit |
| FR-070 / AR-003 / AR-025 / AR-027 proposed | predictive-not-causal limitation + UI/result language | G02/G03 | terminology/content assertions |
| FR-149–152 | existing six-stage navigation; Setup/Train/Predict responsibility; read-oriented Model Management | G03 | stage responsibility regression |
| FR-184 proposed — capability-driven product UI | capabilities API → Train/Explainability/Model Management consumers | G03 | frontend contract/API + Browser E2E |
| ENH-E8 protected contract | no feature-edit authority move; no navigation/runtime coupling | G03 | navigation/stage regression |
| ENH-E9 protected contract | no unrelated Project/Causal/Graph changes | G03 | targeted non-predictive smoke |

## 2. Consistency checks

### 2.1 Requirement vs design

**PROVISIONAL PASS**

理由:

- proposed requirementの各capabilityに対応するdesign responsibilityが存在する。
- FR-161 mandatory dependency prohibitionとoptional dependency designは整合する。
- AR-009とprovider artifact proposalは整合する。
- AR-003/025とSHAP/LIMEのpredictive-not-causal treatmentは整合する。
- leakage/TEST isolationをadvanced backend追加で変更していない。

ただしartifact schema、SHAP scale、LIME semantics等のopen decisionが残るためfinal PASSではない。

### 2.2 Design vs Gate decomposition

**PROVISIONAL PASS**

- G01 = model capability/artifact/predict/provenance
- G02 = explanation compatibility/method semantics/provenance
- G03 = product integration/browser connectivity

dependencyは `G01 -> G02 -> G03` で一方向。G03がG01/G02のscientific semanticsを再定義しない構造になっている。

### 2.3 Gate boundaries mutually coherent

**PASS at semantic-boundary level**

- G01とG02はlower deterministic proofをprimaryとする。
- G03だけがfinal product connectivityとしてblocking Browser E2Eを持つ。
- model artifact/load contractとexplanation contractをUI Gateへ混在させていない。
- Work Package sizeを理由にGateを分割していない。

### 2.4 Transition Debt exits defined

**N/A — no Transition Debt approved**

04にpotential candidatesは記載したが、現時点でTDとして採用していない。採用時はID/owner/exit criterionをGate freeze前に追加する。

### 2.5 Approval / freeze readiness

**FAIL / BLOCKING**

- 02 concept approval = PENDING
- requirement delta = NOT APPLIED
- architecture technical decisions = COMPLETE / Human approval APPROVED
- Gate 06/07 = MATERIALIZED_DRAFT / NOT_EXECUTABLE
- P00/P01-P03 = MATERIALIZED_DRAFT / NOT_EXECUTABLE

従ってimplementation readinessは成立していない。

## 3. Post-Architecture-Review state

The technical issues previously listed as blocking decisions are resolved by:

- `40_operator_workflows/architecture_review/01_architecture_discovery.md`
- `40_operator_workflows/architecture_review/02_target_architecture_decision_record.md`
- `40_operator_workflows/architecture_review/03_gate_decomposition.md`

Resolved technical decisions include optional dependency versions, LightGBM model/parameter contract, preprocessing boundary, determinism, fitted-model/2, SHAP semantics, LIME semantics, explanation compatibility/provenance, predictive spec version, capabilities API version, unavailable-state UX, and G03 Browser E2E runtime design.

Remaining blocking items are governance/materialization steps rather than unresolved technical architecture:

1. Approved requirement delta remains `NOT_APPLIED` to canonical requirement/design documents.
2. Approved revised requirement/design snapshot has not yet been recorded.
3. Gate 06/07/P01-P03 remain `MATERIALIZED_DRAFT / NOT_EXECUTABLE`.
4. Agent Execution Readiness therefore MUST remain not-ready.

## 4. Contradiction / risk review

### No detected contradiction

- `FR-161` prohibits **mandatory** external engines; it does not prohibit optional LightGBM/SHAP/LIME.
- `FR-150` protects current `predictive-analysis-spec/1` semantics; ENH-E10 can remain compatible if model/method extension is additive. A version bump requires explicit justification.
- `AR-009` does not prohibit durable external model artifacts; it prohibits external model object/dtype from becoming JSON canonical truth.
- `FR-069` requires global/local Predictive Explanation but does not require every method to implement both. G02 therefore must express method capability rather than fake unsupported output.

### Main architecture risk

The fitted-model and SHAP ambiguities identified in the provisional review are resolved. The selected architecture is provider-neutral `fitted-model/2` with v1 read compatibility, and SHAP TreeExplainer on raw model output (`LOG_ODDS` for binary, `PREDICTION` for regression). The remaining risk is implementation fidelity to these frozen-intent contracts, not an unresolved architecture choice.

## 5. Test architecture consistency

ENH-E10 test handoff is consistent with proposed Gate structure.

- new/materially rebuilt tests: `tests/enhancement/enh_e10/<gate>/<layer>/`
- G01/G02 detailed correctness: unit/contract/integration
- G03 browser: cross-layer connectivity only
- test implementation/orchestration/environment defect that prevents product judgment => BLOCKED, not product FAIL
- Independent Test Agent does not repair tests
- repository-wide test migration is not an E10 prerequisite

## 6. Conclusion

### Planning coherence

**PASS — technical Architecture Review complete**

Problem, requirement proposal, target architecture, Gate boundaries and Work Package decomposition are technically coherent.

### Implementation readiness

**NOT READY — BLOCKED_BY_REQUIREMENT_APPLICATION_AND_GATE_FREEZE**

Required sequence:

1. Apply the approved requirement/design delta to canonical requirement/design documents and save the approved snapshot.
2. Finalize this traceability review against that snapshot.
3. Freeze G01/G02/G03 06/07/P01-P03 consistently.
4. Run Agent Execution Readiness.
5. Start G01 P01 Coding Agent only after readiness reports READY.
