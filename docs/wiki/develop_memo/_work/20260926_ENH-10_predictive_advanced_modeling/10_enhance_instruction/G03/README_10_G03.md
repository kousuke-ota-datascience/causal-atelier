# G03 Gate-local Instruction Set — Predictive Product Integration Contract

- Enhancement: ENH-E10
- Gate: G03
- Status: `MATERIALIZED_DRAFT`
- Dependency: G01 PASS + G02 PASS
- Execution: **NOT ALLOWED until G03 06/07 become FROZEN**

## Required artifacts

- `06_Ariadne_ENH-E10_G03_implementation_instruction.md`
- `07_Ariadne_ENH-E10_G03_test_instruction.md`

## Gate claim

G01 model capabilityとG02 explanation capabilityをTrain / Predict / Metrics / Explainability / Model Managementへ統合し、ENH-E8で確立したPredictive stage責務を保護したままreal product journeyを成立させる。

## Browser acceptance

G03のみBrowser E2EをGate-blockingとし、Binary + LightGBM + SHAP、Regression + LightGBM + LIMEの2 critical journeysを想定する。Browserはcross-layer connectivity proof、scientific/numeric correctnessはG01/G02 lower deterministic layersがprimary proof。

## Freeze prerequisites

capabilities API、parameter rendering、unavailable state、compatibility UX、Model Management provenance、Browser command/environment/fixture/synchronization/assertionをArchitecture Reviewで確定する。

## Conditional artifacts

P00/PxxはExecution Mode freeze後。08はformal FAIL後のみ。09はoriginal Gate contract/AC amendment時のみ。

## Authority rule

FROZEN後は06がimplementation authority、07がacceptance authority、999 Gate Decisionがfinal decision authority。draftをAgent executionへ直接渡さない。
