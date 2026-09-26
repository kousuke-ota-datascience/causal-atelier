# Ariadne ENH-E10 G03 テスト指示書 — Predictive Product Integration Contract

**Document class:** Primary Execution Contract
**Verification contract status:** `FROZEN`
**Depends on:** `G01 PASS + G02 PASS`
**Self-containment:** MUST — this frozen document is the Gate verification authority
**Execution eligibility:** Independent Verification requires G01/G02 PASS and a G03 Fixed Trial Candidate.

- Project: Ariadne
- Enhancement: ENH-E10
- Active Gate: G03
- Accepted pre-E10 code baseline: `c56a8809dea688380b113210bef12c30b50ca7f6`

## 1. Acceptance authority

FROZEN後は本書がG03 Acceptance Criteria authority。Browser runner pathやhistorical E2E implementation自体をAcceptance authorityとしない。

## 2. Gate objective / acceptance claim

advanced predictive model/explanation capabilitiesが、existing Predictive Navigation Stage責務を維持したままTrain / Predict / Metrics / Explainability / Model Managementから選択・実行・確認できることを検証する。

## 3. Effective verification context

- current frontendはcapabilities APIからmodel registry / explanation methodsを取得する。
- current parameter construction/task switchにはlogistic/linear model ID hard-codeがあり、advanced backend追加時はcapability-drivenに解消する必要がある。
- Setupがfeature selection authorityで、Train/Predictはfeature context read-only。
- Browser E2Eはcritical cross-layer connectivity proofであり、detailed scientific correctnessのprimary proofではない。
- test-side failureはproduct failureから分離し、product correctnessを判定できない場合はBLOCKEDとする。

## 4. Required verification inputs

- G01/G02 final PASS Gate Decisions
- FROZEN G03 06/07
- G03 Completion Report / Fixed Candidate SHA
- current capability response/schema
- Browser E2E frozen command/environment/fixture
- current frontend/API/backend source
- current test estate discovered from repository

## 5. Frozen verification preconditions

- capabilities API fields/schema
- parameter rendering contract
- unavailable capability presentation
- default model selection
- compatibility validation boundary
- Model Management provenance set
- Browser command/environment/fixture/routes/synchronization/assertions
- accessibility/error semantics

未解決なら `BLOCKED_PREREQUISITE`。

## 6. Acceptance Criteria

| AC ID | Criterion | Required evidence | Severity |
|---|---|---|---|
| AC-01 | Train model selector is capability-driven and only presents/accepts models compatible with the selected task; existing logistic/linear and new LightGBM options remain usable as applicable. | frontend contract + API integration | MUST |
| AC-02 | Model-specific parameters are serialized from the frozen capability/parameter contract; current logistic-vs-else hard-coded payload assumption is removed without breaking existing models. | frontend contract + request evidence | MUST |
| AC-03 | Setup remains the only Predictive feature-editing stage; Train and Predict show feature context read-only and preserve dataset-schema-backed feature semantics. | frontend/navigation regression | MUST |
| AC-04 | Explainability presents only compatible methods/global-local capabilities for the selected model and makes unavailable dependency/incompatibility explicit with no fallback. | frontend/API contract tests | MUST |
| AC-05 | Predict/Metrics continue to consume canonical backend outputs without introducing a new mandatory standalone scoring engine or client-side numeric authority. | integration + frontend contract | MUST |
| AC-06 | Model Management remains read-oriented and exposes the frozen model/artifact/model-card/lineage/provenance fields sufficient to identify model/backend/runtime. | frontend contract + API evidence | MUST |
| AC-07 | Explainability presentation exposes method, global/local scope, output scale, sample/background provenance and limitations without causal terminology. | frontend/result presentation test | MUST |
| AC-08 | Application startup/navigation remains usable when LightGBM/SHAP/LIME are absent; unavailable capability state is explicit and existing supported paths remain operable. | optional-dependency environment integration | MUST |
| AC-09 | Browser critical journey for Binary Classification + LightGBM + SHAP crosses UI → API → execution/worker → Result/Artifact → Explainability/Model Management and reaches the frozen observable assertions. | Browser E2E trace/evidence | MUST |
| AC-10 | Browser critical journey for Regression + LightGBM + LIME crosses the same system boundaries and reaches the frozen observable assertions. | Browser E2E trace/evidence | MUST |
| AC-11 | G01 model contract and G02 explanation contract remain valid under product integration. | protected regression | MUST |
| AC-12 | ENH-E8 Predictive stage structure and ENH-E9 non-predictive stabilized surfaces have no candidate-caused semantic regression. | targeted regression / navigation evidence | MUST |

## 7. Test Item plan

| ID | Name | Covers AC | Primary layer | Blocking | Method |
|---|---|---|---|---|---|
| 001 | candidate_identity | META | META | YES | candidate/diff audit |
| 010 | capabilities_and_model_selector | AC-01,02,08 | FRONTEND_CONTRACT / API_INTEGRATION | YES | capability-driven rendering/request |
| 020 | stage_responsibility_regression | AC-03,05,12 | FRONTEND_CONTRACT | YES | Setup/Train/Predict/Nav invariants |
| 030 | explainability_capability_ui | AC-04,07,08 | FRONTEND_CONTRACT / API_INTEGRATION | YES | method/global-local/unavailable states |
| 040 | model_management_provenance | AC-06,07 | FRONTEND_CONTRACT / API_INTEGRATION | YES | Result/Artifact/Model Card/Lineage |
| 050 | g01_g02_protected_regression | AC-11 | INTEGRATION | YES | backend/explanation regression |
| 100 | browser_binary_lightgbm_shap | AC-09,03,04,06,07 | BROWSER_E2E | YES | critical journey |
| 110 | browser_regression_lightgbm_lime | AC-10,03,04,06,07 | BROWSER_E2E | YES | critical journey |
| 120 | non_predictive_smoke | AC-12 | FRONTEND / API smoke | YES | targeted Project/Causal/Graph surface checks |
| 999 | gate_decision | ALL | META | YES | independent synthesis |

## 8. Browser E2E frozen contract fields

FROZEN版ではTest Item 100/110ごとに次を具体化する。

- canonical command
- browser/runtime image and current-source build rule
- service prerequisites
- deterministic dataset/fixture
- starting route
- exact user actions
- semantic synchronization point
- expected Result/Artifact/Model Management observable state
- trace/screenshot/video/network/API/worker log evidence
- teardown
- failure classification

Browser command/environmentがapproved execution contractへ具体化されるまではBrowser E2Eを実行してGate判定してはならず、`BLOCKED_PREREQUISITE` とする。

## 9. Browser failure classification

少なくとも:

- `PRODUCT_DEFECT`
- `TEST_IMPLEMENTATION_DEFECT`
- `TEST_ORCHESTRATION_DEFECT`
- `TEST_ENVIRONMENT_DEFECT`
- `UNKNOWN`

`TEST_IMPLEMENTATION_DEFECT` / `TEST_ORCHESTRATION_DEFECT` / `TEST_ENVIRONMENT_DEFECT` / `UNKNOWN` によりproduct correctnessを判定できない場合、product `FAIL` ではなく原則 `BLOCKED`。

historical runnerのstale locator/obsolete routeを理由にACを弱めない。Independent Test Agentはtest-side repairを実装しない。

## 10. Candidate identity / test discovery

Fixed Candidate auditをMUST FIRSTとする。post-candidate diffは少なくとも:

- PRODUCT_SEMANTIC_CHANGE
- TEST_IMPLEMENTATION_CHANGE
- TEST_ORCHESTRATION_CHANGE
- TEST_INFRASTRUCTURE_CHANGE
- DOCUMENTATION_ONLY

へ分類する。

test implementationは `tests/enhancement/enh_e10/g03/` を第一探索先とし、必要に応じてtransition dirsをcurrent repositoryからdiscoverする。Completion Reportのhistorical pathをphysical authorityにしない。

## 11. Protected regression

| Source | Protected semantic | Result |
|---|---|---|
| G01 | model capability/artifact/load/predict/provenance | PASS |
| G02 | explanation compatibility/semantics/provenance | PASS |
| ENH-E8 | Predictive six-stage navigation and stage responsibility | PASS |
| ENH-E9 | stabilized non-predictive workflow | no candidate-caused regression |

## 12. Evidence requirements

全item:

- Fixed Candidate / Tested SHA
- exact command/method
- environment/package versions
- raw evidence and exit code
- Facts / Interpretation separation
- AC mapping
- reproduction

Browser items追加:

- trace/screenshot/video（利用可能な範囲）
- console/page errors
- relevant network request/response
- API/worker logs
- service/compose state
- failed synchronization point/assertion
- failure classification

HTTP status単体をroot causeとしない。

## 13. Test Agent prohibited work

- production/test/orchestration/dependency modification
- stale runner修正
- AC weakening
- numeric correctnessをBrowser表示だけで代替
- candidate substitution
- causal interpretation
- unsupported capability fallback

## 14. Decision semantics

**PASS:** all MUST AC、candidate identity、G01/G02 regressions、2 blocking browser journeysが成立。  
**FAIL:** executable verificationによりFixed Candidateのproduct/contract violationがverified。  
**BLOCKED:** contract/candidate/environment/test implementation/orchestration ambiguityでvalid product judgment不能。

## 15. Required outputs

- `30_test_report/G03/TrialNN/...test_item...`
- `30_test_report/G03/TrialNN/ENH-E10_G03_NN_999_gate_decision.md`
- decision後停止
