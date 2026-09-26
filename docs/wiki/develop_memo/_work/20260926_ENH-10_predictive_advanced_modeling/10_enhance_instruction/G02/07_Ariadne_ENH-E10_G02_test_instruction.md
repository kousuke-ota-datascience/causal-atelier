# Ariadne ENH-E10 G02 テスト指示書 — Predictive Explanation Backend Contract

**Document class:** Primary Execution Contract
**Verification contract status:** `MATERIALIZED_DRAFT / NOT_EXECUTABLE`
**Depends on:** `G01 PASS`
**Self-containment:** MUST when FROZEN; current artifact is a materialized authoring draft
**Execution eligibility:** **NOT EXECUTABLE** until §5 architecture decisions are resolved, G01 PASS exists, and 06/07/P01-P03 are explicitly FROZEN.

- Project: Ariadne
- Enhancement: ENH-E10
- Active Gate: G02
- Accepted pre-E10 code baseline: `c56a8809dea688380b113210bef12c30b50ca7f6`

## 1. Acceptance authority

FROZEN後は本書がG02 Acceptance Criteria authority。implementation reportやlibraryの「正常終了」をexplanation correctnessへ読み替えない。

## 2. Gate objective / acceptance claim

model capabilityに整合したSHAP/LIME/linear coefficient explanationを、method固有のglobal/local semantics、reproducibility、provenance、failure boundaryを保持して生成できることを検証する。

PASS後G03は、method compatibilityとcanonical explanation outputsをUI/product integrationから利用できる。

## 3. Effective verification context

- baseline methodは `LINEAR_COEFFICIENT_CONTRIBUTION` のみ。
- unsupported methodはbaselineでもsilent fallbackしない。
- feature order mismatchはexplicit reject。
- explanation datasetはTEST由来・explanation-only。
- binary coefficient explanationはLOG_ODDS scale、predictionはPROBABILITY。
- G02はSHAP/LIMEをPredictive Explanationとして扱い、causal explanationとは明確に区別する。
- SHAP/LIMEのlibrary-specific numeric semanticsをBrowser E2Eで一次検証しない。

## 4. Required verification inputs

- FROZEN G01 999 Gate Decision
- FROZEN G02 06/07
- G02 Completion Report + Fixed Candidate SHA
- current dependency/runtime versions
- frozen compatibility matrix / output-scale / sampling/background contract
- current source/artifact/result state

## 5. Architecture Review values to verify

Before FROZEN, 07 and P01-P03 must embody the following:

- methods: `LINEAR_COEFFICIENT_CONTRIBUTION`, `SHAP_TREE`, `LIME_TABULAR`
- compatibility matrix exactly as G02 06 §3
- SHAP LightGBM-only / tree_path_dependent / raw LOG_ODDS or PREDICTION
- SHAP global mean-absolute + signed mean over immutable TEST; local FIRST_N
- SHAP additivity tolerance `atol=1e-6, rtol=1e-5`
- LIME local-only on preprocessed feature space
- LIME defaults: 2000 samples, min(10,n_features), no continuous discretization, euclidean, 0.75*sqrt(n_features), no sample-around-instance
- deterministic TRAIN-derived `predictive-explanation-reference/1`, max 500 rows
- explanation result/artifact/model-card remain schema v1 with additive method-specific fields
- explicit dependency/scope/applicability/computation failure codes
- predictive-not-causal limitation retained

Architecture decisions are technically resolved; Human approval remains the freeze authorization.

## 6. Acceptance Criteria

| AC ID | Criterion | Required evidence | Severity |
|---|---|---|---|
| AC-01 | Existing linear coefficient global/local explanation remains available for compatible existing linear models with prior scale/feature-order semantics preserved. | protected unit/integration regression | MUST |
| AC-02 | Explanation method availability is resolved through a compatibility/capability contract; unsupported model-method combinations are rejected explicitly without fallback. | compatibility matrix contract tests | MUST |
| AC-03 | SHAP Binary Classification produces global/local canonical values on raw LOG_ODDS scale with base value, feature mapping, TEST sample identity and tree-path-dependent reference semantics. | deterministic SHAP integration evidence | MUST |
| AC-04 | SHAP Regression produces the analogous raw PREDICTION-scale canonical representation and provenance contract. | deterministic SHAP integration evidence | MUST |
| AC-05 | LIME Binary Classification local explanation operates on preprocessed features, explains positive-class probability, records instance/reference identity and per-row effective seed/parameters, and is reproducible within the runtime-scoped guarantee. | deterministic LIME integration evidence | MUST |
| AC-06 | LIME Regression local explanation satisfies the same local/provenance contract. | deterministic LIME integration evidence | MUST |
| AC-07 | Global LIME is unsupported: requesting it is explicitly rejected with `EXPLANATION_SCOPE_NOT_SUPPORTED`; no pseudo-global fallback is emitted. | negative capability test | MUST |
| AC-08 | Missing SHAP/LIME dependency does not break core/model flow; selecting unavailable method returns explicit capability error with package availability/version evidence. | dependency-absence tests | MUST |
| AC-09 | Explanation result/artifact/model-card preserve model identity, method identity/version, feature/sample identity, background/reference, output scale, seed and package/runtime provenance required by the frozen contract. | artifact/result/model-card audit | MUST |
| AC-10 | Explanation uses isolated explanation data and does not alter model selection/training or violate TEST isolation. | lineage/isolation audit | MUST |
| AC-11 | User-visible/result terminology never represents SHAP/LIME/coefficient explanation as causal explanation, treatment effect or causal feature importance. | contract/content assertions | MUST |
| AC-12 | G01 model artifact/load/prediction contract remains intact under explanation integration. | G01 protected regression | MUST |

## 7. Test Item plan

| ID | Name | Covers AC | Primary layer | Blocking | Method |
|---|---|---|---|---|---|
| 001 | candidate_identity | META | META | YES | candidate/diff audit |
| 010 | coefficient_protected_regression | AC-01,11 | UNIT / INTEGRATION | YES | baseline compatible models |
| 020 | compatibility_registry | AC-02,07 | CONTRACT | YES | model × method matrix |
| 030 | shap_binary | AC-03,09,10,11 | INTEGRATION | YES | fixed synthetic fixture |
| 040 | shap_regression | AC-04,09,10,11 | INTEGRATION | YES | fixed synthetic fixture |
| 050 | lime_binary_local | AC-05,09,10,11 | INTEGRATION | YES | fixed seed/local instance |
| 060 | lime_regression_local | AC-06,09,10,11 | INTEGRATION | YES | fixed seed/local instance |
| 070 | optional_dependency_absence | AC-08 | CONTRACT / INTEGRATION | YES | SHAP/LIME independently unavailable |
| 080 | provenance_and_model_card | AC-09,11 | CONTRACT | YES | normalized result/artifact audit |
| 090 | g01_protected_regression | AC-12 | INTEGRATION | YES | model flow regression |
| 999 | gate_decision | ALL | META | YES | independent synthesis |

G02 Browser E2E: **0 blocking items**.

## 8. Method-specific verification principles

### SHAP

- raw library array shapeの存在だけでPASSしない。
- frozen output-scale contractとactual model output semanticsを照合する。
- base/expected value、feature contribution mapping、global aggregation/local instance identityを分離して確認する。
- additivity等をacceptanceへ含める場合はfrozen toleranceを明示し、未定toleranceをtest時に恣意的設定しない。

### LIME

- fixed seedだけでreproducibilityを過大評価しない。library/version/parameters/instance/background等を固定して比較する。
- local explanationのfeature representationがpreprocessed/original featureのどちらかをfrozen contractどおり判定する。
- global非対応なら「出力がない」ことをsilent successではなくcapability resultとして確認する。

## 9. Candidate identity / test architecture

candidate auditをMUST FIRSTとする。test discoveryは `tests/enhancement/enh_e10/g02/` を第一探索先とし、current repository stateをauthorityとする。

Browser/test harness側のdefectでproduct explanation correctnessを判断できない場合はBLOCKED。Independent Test Agentはtest-side repairを実装しない。

## 10. Protected regression

| Source | Semantic | Required |
|---|---|---|
| G01 | model registry/artifact/load/predict/provenance | PASS |
| baseline | coefficient explanation | PASS |
| baseline | feature-order mismatch rejection | PASS |
| baseline | TEST isolation | PASS |
| baseline | predictive-not-causal boundary | PASS |

## 11. Evidence requirements

- Fixed Candidate / Tested SHA
- exact command/environment
- LightGBM/SHAP/LIME versions or confirmed absence
- model/method identifiers
- fixture/sample/background identities
- seed/effective parameters
- output scale
- normalized explanation payload excerpts sufficient for AC
- raw provider evidence where needed
- Facts / Interpretation separation
- AC mapping / reproduction

## 12. Test Agent prohibited work

- product/test/dependency code modification
- method output reinterpretation to rescue failure
- tolerance invention
- unsupported method fallback
- AC modification
- candidate substitution
- causal meaning attribution

## 13. Decision semantics

**PASS:** all MUST AC + candidate identity + G01 regression pass.  
**FAIL:** executable test demonstrates Fixed Candidate violates frozen explanation contract.  
**BLOCKED:** contract/candidate/dependency/test infrastructure ambiguity prevents valid product judgment.

## 14. Required outputs

- `30_test_report/G02/TrialNN/...test_item...`
- `30_test_report/G02/TrialNN/ENH-E10_G02_NN_999_gate_decision.md`
- decision後停止
