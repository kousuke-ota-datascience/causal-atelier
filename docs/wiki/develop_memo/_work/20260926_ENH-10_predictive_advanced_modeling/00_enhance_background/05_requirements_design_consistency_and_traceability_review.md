# ENH-E10 要件・設計整合性およびトレーサビリティ確認

> **Document class:** Planning / Decision Artifact  
> **Status:** `MATERIALIZED / PROVISIONAL_REVIEW / NOT_READY_FOR_IMPLEMENTATION`  
> **Self-containment:** MUST for own subject

- Enhancement: `ENH-E10`
- Requirement proposal: `03_requirements_revision.md`
- Design proposal: `04_design_revision.md`
- Gate drafts: `10_enhance_instruction/G01..G03`
- Approval record: `02_enhancement_concept_approval_record.md`
- Current approval state: `PENDING`

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
- architecture decisions = NOT FROZEN
- Gate 06/07 = MATERIALIZED_DRAFT / NOT_EXECUTABLE
- P00/Pxx = NOT MATERIALIZED

従ってimplementation readinessは成立していない。

## 3. Unresolved issues

Blocking decisions:

1. named capability requirementsをcanonical FRへ直接入れるか、general FR + Gate acceptanceへ分けるか
2. optional dependency group name/composition/version bounds
3. final LightGBM model IDs
4. LightGBM parameter/default subset
5. categorical handling
6. missing-value responsibility
7. early stopping
8. fitted-model artifact schema/version/serialization
9. provider loader dispatch
10. SHAP supported model/task matrix
11. SHAP binary output scale
12. SHAP background/reference/global aggregation/additivity
13. LIME local-only decision
14. LIME perturbation/discretization/sample defaults
15. LIME feature representation
16. reproducibility guarantee strength
17. predictive spec schema revision
18. capabilities API schema/version
19. unavailable capability UI semantics
20. Browser E2E canonical environment/command/fixture/synchronization

Non-blocking/deferred by scope:

- multiclass
- AutoML
- online inference/deployment
- production monitoring/model registry
- causal explanation/CATE/HTE
- repository-wide test migration

## 4. Contradiction / risk review

### No detected contradiction

- `FR-161` prohibits **mandatory** external engines; it does not prohibit optional LightGBM/SHAP/LIME.
- `FR-150` protects current `predictive-analysis-spec/1` semantics; ENH-E10 can remain compatible if model/method extension is additive. A version bump requires explicit justification.
- `AR-009` does not prohibit durable external model artifacts; it prohibits external model object/dtype from becoming JSON canonical truth.
- `FR-069` requires global/local Predictive Explanation but does not require every method to implement both. G02 therefore must express method capability rather than fake unsupported output.

### Main architecture risk

The largest current ambiguity is fitted-model artifact evolution. LightGBM cannot be safely represented as the current coefficient-only `fitted-model/1` shape without semantic falsification. Architecture Review must choose a versioned provider-neutral or provider-specific artifact/load contract before G01 freeze.

The second major ambiguity is SHAP output semantics. Binary classification output scale/background/base value must be frozen before acceptance tolerances or result schema are written.

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

**PASS — provisional**

ENH-E10のproblem、requirement delta、proposed architecture、G01/G02/G03 semantic boundariesは相互に矛盾していない。

### Implementation readiness

**NOT READY / BLOCKED_BY_APPROVAL_AND_ARCHITECTURE_FREEZE**

次に必要なのはcodingではなく:

1. Human concept/scope approval
2. open requirement decisionsの確定
3. Architecture Reviewで04のblocking decisionsをfreeze
4. 03 requirement deltaをcanonical requirement documentsへapply
5. approved revised requirement/design snapshotを保存
6. 本05をfinal reviewへ更新
7. G01/G02/G03 06/07を`FROZEN`化
8. required P00/Pxxをmaterialize

この順序が完了するまで、ENH-E10 Gate executionを開始しない。
