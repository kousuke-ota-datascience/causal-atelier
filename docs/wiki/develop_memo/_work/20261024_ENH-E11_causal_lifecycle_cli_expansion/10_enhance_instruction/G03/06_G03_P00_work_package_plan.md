# ENH-E11 G03 P00 — Work Package Plan (DRAFT)

**Gate:** G03 / Official Enhance Workflow Gate  
**Class:** Planning/Operator Artifact, not Coding Agent's normative package  
**Plan status:** DRAFT / NOT_FROZEN / CODING_NOT_AUTHORIZED  
**Gate06:** [Implementation Contract](06_Ariadne_ENH-E11_G03_implementation_instruction.md)  
**Gate07:** [Independent Verification Draft](07_Ariadne_ENH-E11_G03_test_instruction.md) / DRAFT / NOT_FROZEN / TESTS_NOT_RUN  
**Execution mode proposal:** WORK_PACKAGE / P01,P02,P03,P04,P05,P06  
**Upstream dependency proposal:** G02 PASS。未承認のEdgeとしてまとめReviewする。

## 1. Gate semantic acceptance

Native推定と4 Refutation・2 Sensitivity・NCE/NCO/RVをEffect lineage付きで実行する。

**主要不確実性:** 非有意NCE/NCOは無交絡証明ではない。RVは古典OLS限定。P1-M11のScience未確定を黙認しない。

## 2. Package ownership map

| Package | Scope | Required Pxx deps | Method | Package obligations |
|---|---|---|---|---|
| P01 | native_effects | NONE | P1-M08,P1-M09 | 既存Treatment effect kernelのdiff-in-means/OLS再利用。割当/Target contrast/ATE-ATT区別。 |
| P02 | weighting_ipw_aipw | P01 | P1-M10,P1-M11 | 既存IPW/AIPWを共有しATE/ATT weight、ESS、balance、overlap、nuisance/seedを明示。 |
| P03 | refutation_methods | P01,P02 | P1-M12,P1-M13,P1-M14,P1-M15 | 既存run(input_,output_dir) API不変。M12/M13実装再利用、M14/M15不足Kernel追加、seedと元Effect hash必須。 |
| P04 | sensitivity_methods | P01,P02 | P1-M16,P1-M17 | 既存SensitivityAdapter.run公開ABI不変。Adjustment Set妥当性とPropensity Clippingによるtarget変化を保持。 |
| P05 | negative_controls_ols_rv | P01 | P1-M18,P1-M19,P1-M20 | 観測Z/W、事前帰無・opt-in・条件付き関連。OLS RV(q=1)は古典OLS coef/SE/df限定。 |
| P06 | diagnostics_pipeline | P03,P04,P05 | — | 13 MethodのREFUTE/SENSITIVITY/DIAGNOSE Bundleと旧Product v2回帰・Privacyを統合。 |

## 3. Execution DAG and handoff

- `P01` <- NONE
- `P02` <- P01
- `P03` <- P01,P02
- `P04` <- P01,P02
- `P05` <- P01
- `P06` <- P03,P04,P05

Each Pxx→focused verification→20 Package Report→Checkpoint SHA。全required Package完了→Candidate Assembly→Gate-wide self-verification→single fixed candidate SHA→Independent 07→canonical 999。Package Completed≠ReadyForTest≠PASS。

## 4. Governance / Coding Authorization

P00は独立受入条件でも実装許可でもない。06/07 Freeze、Owner採用のPackage list/dependency、上流Gate canonical 999、実基準SHAとenvironment preflightが揃うまでPxxは実行禁止。Issue、Package結果、P00の状態を999代用にしない。