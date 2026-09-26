# Ariadne ENH-E10 G01 テスト指示書 — Predictive Model Backend Contract

**Document class:** Primary Execution Contract
**Verification contract status:** `MATERIALIZED_DRAFT / NOT_EXECUTABLE`
**Depends on:** `ENH-E9 final PASS / accepted pre-E10 baseline`
**Self-containment:** MUST when FROZEN; current artifact is a materialized authoring draft
**Execution eligibility:** **NOT EXECUTABLE** until Human approval is recorded, G01 implementation produces a Fixed Trial Candidate, and 06/07/P01-P03 are FROZEN.

- Project: Ariadne
- Enhancement: ENH-E10
- Active Gate: G01
- Accepted pre-E10 code baseline: `c56a8809dea688380b113210bef12c30b50ca7f6`

## 1. Acceptance authority

FROZEN後は本書07がG01 original Acceptance Criteria authorityとなる。Coding self-check、Package completion、Completion Reportの `READY_FOR_TEST` をGate acceptanceへ読み替えない。

現時点はmaterialized authoring draftでありIndependent Verificationへ使用しない。§5を06/Pxxと整合させた上でFROZENへ変更し、Fixed Trial Candidate成立後にIndependent Verificationを開始する。

## 2. Gate objective / acceptance claim

既存linear modelを保護しながら、Binary Classification / Regression用LightGBMをregistry-selected optional backendとして利用し、train → durable artifact → load → predict → provenance確認を一貫して実行できることを検証する。

PASS後、G02/G03はLightGBM model capability、artifact/load/prediction contract、optional dependency behavior、provenance contractへ依存してよい。

## 3. Effective verification context

baseline facts:

- current registryは `logistic_regression.v1` / `linear_regression.v1`。
- current fitted artifactはJSON `fitted-model/1`。
- existing predictive flowはTRAIN-fitted preprocessor、feature order、preprocessor hash、TEST final-evaluation isolationを持つ。
- LightGBMはbaseline dependencyに存在しない。
- `FR-161` によりexternal analytical engineのmandatory dependency化は禁止。
- G01のscientific/numeric correctnessはlower deterministic layerをprimary proofとし、Browser E2Eへ委譲しない。

## 4. Required verification inputs

- FROZEN G01 06/07
- Implementation Completion Report
- Fixed Trial Candidate SHA
- actual Tested Repository State full SHA
- current source/dependency/runtime state
- ENH-E9 accepted baseline/protected regression evidence
- Architecture Reviewでfreezeされたmodel/artifact/dependency contract

## 5. Architecture Review values to verify

Before FROZEN, this 07 and P01-P03 must contain the same effective values:

- model IDs: `lightgbm_classifier.v1`, `lightgbm_regressor.v1`
- optional extra: `predictive-advanced` with LightGBM `>=4.7.0,<4.8`
- exposed LightGBM parameter subset/defaults defined in G01 06 §3
- existing preprocessing remains authoritative; no native categorical/missing and no early stopping
- deterministic CPU settings: deterministic=true, force_col_wise=true, num_threads=1
- new-write artifact: `fitted-model/2`; old `fitted-model/1` remains readable
- LightGBM payload: `lightgbm-model-string/1`; linear payload: `ariadne-linear-json/1`
- same-runtime/config reproducibility only
- explicit model dependency/task/parameter/artifact/load/feature mismatch taxonomy
- `predictive-analysis-spec/1` retained and no DB migration required

Architecture decisions are technically resolved; Human approval is the remaining freeze authorization.

## 6. Acceptance Criteria

| AC ID | Criterion | Required evidence | Severity |
|---|---|---|---|
| AC-01 | Existing `logistic_regression.v1` / `linear_regression.v1` remain task-compatible and behaviorally usable under the new registry contract. | protected unit/contract/integration regression | MUST |
| AC-02 | LightGBM classifier is registry-selectable only for Binary Classification and LightGBM regressor only for Regression; incompatible task/model combinations fail explicitly. | registry + validation tests | MUST |
| AC-03 | LightGBM absent environment still imports/starts Ariadne core and preserves existing flows; selecting LightGBM returns explicit capability-unavailable error with no silent fallback. | isolated dependency-absence test | MUST |
| AC-04 | Binary LightGBM train → `fitted-model/2` serialize → fresh load → predict preserves model/task/feature/preprocessor identity and prediction parity on deterministic fixture. | integration + artifact round-trip evidence | MUST |
| AC-05 | Regression LightGBM train → `fitted-model/2` serialize → fresh load → predict preserves the same identity/parity guarantees. | integration + artifact round-trip evidence | MUST |
| AC-06 | Invalid parameters, feature order/name mismatch, preprocessor mismatch and unsupported model/task requests are rejected with distinguishable failure semantics. | negative contract tests | MUST |
| AC-07 | Artifact/Model Card/runtime evidence records the frozen provenance set: Ariadne model identity, task, effective parameters, seed/determinism, feature identity, preprocessor identity and analytical package availability/version. | artifact/result inspection | MUST |
| AC-08 | TEST isolation and TRAIN-only preprocessing fit remain intact; LightGBM integration does not use TEST for selection/fitting. | leakage/isolation regression | MUST |
| AC-09 | Repeated fixed-seed runs satisfy the reproducibility guarantee defined by the frozen architecture without overstating cross-platform determinism. | deterministic scientific/contract evidence | MUST |

## 7. Test Item plan

| Test Item ID | Name | Covers AC | Primary layer | Gate blocking | Method |
|---|---|---|---|---|---|
| 001 | candidate_identity | META | META | YES | Fixed Candidate / checkout / post-candidate diff audit |
| 010 | registry_backward_compatibility | AC-01,02 | UNIT / CONTRACT | YES | registry and task matrix |
| 020 | optional_dependency_absence | AC-03 | CONTRACT / INTEGRATION | YES | execute without predictive-advanced package |
| 030 | lightgbm_binary_roundtrip | AC-04,07,09 | INTEGRATION | YES | deterministic synthetic binary fixture |
| 040 | lightgbm_regression_roundtrip | AC-05,07,09 | INTEGRATION | YES | deterministic synthetic regression fixture |
| 050 | negative_contracts | AC-02,06 | UNIT / CONTRACT | YES | mismatch / invalid param / feature identity cases |
| 060 | leakage_and_test_isolation | AC-08 | INTEGRATION | YES | TRAIN/VALIDATION/TEST lineage audit |
| 070 | linear_model_protected_regression | AC-01,08 | INTEGRATION | YES | existing logistic/linear behavior |
| 080 | provenance_audit | AC-07 | CONTRACT | YES | artifact/model-card/runtime metadata |
| 999 | gate_decision | ALL | META | YES | synthesize independent evidence |

G01 Browser E2E: **0 blocking items**. Product-level browser connectivity is G03 responsibility.

## 8. Candidate identity audit — MUST FIRST

1. Completion ReportからFixed Trial Candidate SHAを取得。
2. actual checkout/HEADを記録。
3. 差分があればFixed Candidate以降のdiffを分類。
4. `PRODUCT_SEMANTIC_CHANGE` の可能性を一意に否定できなければ本体test前にBLOCKED。
5. test/document-only changeは内容を確認し、candidate identityへの影響を明記。

## 9. Test architecture transition rule

current physical pathをAcceptance authorityにしない。第一探索先は `tests/enhancement/enh_e10/g01/` とし、必要ならtransition stateとして `tests/product/`, `tests/integration/`, `tests/scientific/`, `tests/browser_e2e/` をdiscoverする。

Test implementation/orchestration/environment defectでproduct correctnessを判定できない場合はproduct FAILへ短絡せずBLOCKEDとする。Independent Test Agent自身はtest-side repairを実装しない。

## 10. Protected upstream regression

| Source | Protected semantic | Required result |
|---|---|---|
| ENH-E8 | Predictive stage responsibility and Setup-owned feature editing | PASS |
| ENH-E9 | stabilized workflow / unrelated surfaces | no candidate-caused regression |
| Predictive baseline | logistic/linear model flow | PASS |
| Predictive baseline | TEST isolation / TRAIN-only preprocessing | PASS |

## 11. Evidence requirements

各Test Item Report:

- Fixed Trial Candidate SHA
- Tested Repository State full SHA
- exact command/method and environment
- dependency/package versions or confirmed absence
- exit code
- relevant raw evidence
- observed Facts / Interpretation separated
- AC mapping
- reproduction procedure

Artifact round-trip itemsはserialized artifact identity/hash/schema、load path、pre/post prediction comparison、feature/preprocessor identityを残す。

## 12. Test Agent prohibited work

- production code modification
- automated test code modification
- dependency modification
- artifact/migration modification
- Acceptance Criteria modification
- implementation repair
- candidate SHA substitution
- unavailable LightGBMをlinear modelへfallbackさせてPASSすること

## 13. Decision semantics

**PASS:** all MUST AC、candidate identity、protected regressionが成立。  
**FAIL:** test実行可能でFixed Candidateのproduct/model contract violationがverifiedされた。  
**BLOCKED:** contract未freeze、dependency/environment/prerequisite不備、candidate ambiguity、test implementation/orchestration/environment defect等によりproduct correctnessを妥当に判定できない。

## 14. Required outputs

FROZEN後のTrialごとに:

- `30_test_report/G01/TrialNN/ENH-E10_G01_NN_<ITEM>_*.md`
- `30_test_report/G01/TrialNN/ENH-E10_G01_NN_999_gate_decision.md`
- PASS / FAIL / BLOCKED後に停止
