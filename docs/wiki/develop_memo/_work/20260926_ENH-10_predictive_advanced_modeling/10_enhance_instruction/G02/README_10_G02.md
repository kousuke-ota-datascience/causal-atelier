# G02 Gate-local Instruction Set — Predictive Explanation Backend Contract

- Enhancement: ENH-E10
- Gate: G02
- Status: `MATERIALIZED_DRAFT`
- Dependency: G01 PASS
- Execution: **NOT ALLOWED until G02 06/07 become FROZEN**

## Required artifacts

- `06_Ariadne_ENH-E10_G02_implementation_instruction.md`
- `07_Ariadne_ENH-E10_G02_test_instruction.md`

## Gate claim

existing linear coefficient explanationを保護し、SHAP/LIMEをmodel capabilityに基づいて選択できるPredictive Explanation contractを成立させる。global/local差、output scale、background/reference、sampling、reproducibility、provenance、optional dependency failureをmethod-specificに固定する。

## Freeze prerequisites

Architecture Reviewでmodel × method compatibility、SHAP scale/background、LIME local/global policy、method parameters、dependency/version bounds、canonical explanation schema、failure taxonomyを確定する。

## Conditional artifacts

P00/PxxはExecution Mode freeze後。08はformal FAIL後のみ。09はoriginal Gate contract/ACのHuman-approved amendment時のみ。

## Authority rule

FROZEN後は06がimplementation authority、07がacceptance authority、999 Gate Decisionがfinal decision authority。draftを実行promptとして使用しない。
