# ENH-E10 G03 P03 — Browser E2E / Product Regression

**Document class:** Work Package Execution Contract  
**Status:** `MATERIALIZED_DRAFT / NOT_EXECUTABLE`  
**Gate:** `G03`  
**Package:** `P03`  
**Depends on:** `G03 P02 canonical package report = PACKAGE_COMPLETE`  
**Self-containment:** MUST when FROZEN  
**Information isolation:** MUST  
**Execution eligibility:** `BLOCKED_CONTRACT_NOT_FROZEN`

## 1. Package objective

2 critical Browser journeys、hermetic orchestration、observable assertions、G01/G02 protected integration、Predictive/non-predictive navigation regressionを成立させ、Candidate Assembly可能なG03 stateへ到達する。

## 2. Effective architecture values

Canonical runner:

`tests/enhancement/enh_e10/g03/browser_e2e/run_predictive_advanced.py`

Compose stack:

`compose.yaml + compose.e1a.yaml + compose.enh_e10.yaml`, project `ariadne-enh-e10`.

API/worker advanced image:

`Dockerfile.predictive-advanced` with `.[predictive-advanced]`.

Blocking execution begins from `down -v --remove-orphans`, runs the browser service with `--build`, executes both scenarios, captures evidence under `test-results/browser_e2e/enh_e10/`, then tears down volumes/orphans.

Scenario 100 = Binary + `lightgbm_classifier.v1` + `SHAP_TREE`.
Scenario 110 = Regression + `lightgbm_regressor.v1` + explicit local `LIME_TABULAR`.

Primary synchronization is execution terminal state + required Result/Artifact availability + visible UI state; fixed sleep is not primary synchronization.

## 3. Required behavior

- Binary + LightGBM + SHAP と Regression + LightGBM + LIME の2 critical journeyをcurrent UI/API/worker/result/artifact flowへ接続するBrowser E2Eをmaterializeする。
- current-source/hermetic bootstrap、fixture ownership、semantic synchronization、observable assertions、evidence capture、teardownを07 contractと一致させる。
- Browser E2Eをnumeric/scientific correctnessのprimary proofにしない。
- G01/G02 protected integration、ENH-E8 Predictive stage responsibility、ENH-E9 non-predictive surfacesをtargeted regressionする。
- test implementation/orchestration/environment defectはproduct FAILへ短絡しない。

## 4. Focused verification

frontend/API integration suite、both Browser journeys coding-side smoke、stage/navigation protected regression、non-predictive targeted smoke、failure classification evidence。

## 5. Completion boundary

focused verification PASSまたは正当なBLOCKED evidence、G03-wide self-check可能、package report、exact checkpoint SHA。terminal stateは `PACKAGE_READY` または `BLOCKED_*`。P03 completion後はCandidate Assemblyへ進む。
