# G02 Gate-local Instruction Set — Predictive Explanation Backend Contract

- Enhancement: ENH-E10
- Gate: G02
- Status: `MATERIALIZED_DRAFT`
- Dependency: G01 PASS
- Execution: **NOT ALLOWED until G02 06/07 become FROZEN**

## Required artifacts

- `06_Ariadne_ENH-E10_G02_implementation_instruction.md`
- `07_Ariadne_ENH-E10_G02_test_instruction.md`
- `06_G02_P00_work_package_plan.md`
- `06_G02_P01_explanation_capability_and_canonical_contract.md`
- `06_G02_P02_shap_backend.md`
- `06_G02_P03_lime_backend_and_integration.md`

## Gate claim

existing linear coefficient explanationを保護し、SHAP/LIMEをmodel capabilityに基づいて選択できるPredictive Explanation contractを成立させる。global/local差、output scale、background/reference、sampling、reproducibility、provenance、optional dependency failureをmethod-specificに固定する。

## Freeze prerequisites

Architecture Reviewでmodel × method compatibility、SHAP scale/background、LIME local/global policy、method parameters、dependency/version bounds、canonical explanation schema、failure taxonomyを確定する。

## Work Package decision

Execution Modeは `WORK_PACKAGE` を採用する。Required packagesは `P01, P02, P03`、First executable packageは `P01`。P00/Pxxはmaterialized draftとして同時作成するが、Architecture Reviewのblocking decisionを06/07/Pxxへ反映し、同一freeze batchでFROZENにするまでは実行禁止。

08はformal FAIL後のみ。09はoriginal Gate contract/ACのHuman-approved amendment時のみ。

## Authority rule

FROZEN後は06がimplementation authority、07がacceptance authority、999 Gate Decisionがfinal decision authority。draftを実行promptとして使用しない。
