# ENH-E11 G09 P00 — Work Package Plan (DRAFT)

**Gate:** G09 / Official Enhance Workflow Gate  
**Class:** Planning/Operator Artifact, not Coding Agent's normative package  
**Plan status:** DRAFT / NOT_FROZEN / CODING_NOT_AUTHORIZED  
**Gate06:** [Implementation Contract](06_Ariadne_ENH-E11_G09_implementation_instruction.md)  
**Gate07:** NOT_CREATED / NOT_FROZEN  
**Execution mode proposal:** WORK_PACKAGE / P01,P02,P03  
**Upstream dependency proposal:** G01 PASS。未承認のEdgeとしてまとめReviewする。

## 1. Gate semantic acceptance

Donor Designに基づきSCM point-onlyとSDID point/inferenceを区別する。

**主要不確実性:** Donor汚染・pre-fit・time support負例必須。SCMに未検証CIを付けない。

## 2. Package ownership map

| Package | Scope | Required Pxx deps | Method | Package obligations |
|---|---|---|---|---|
| P01 | scm_point | NONE | P3-M12 | Donor weights/pre-treatment RMSPE/fit・counterfactual gap。SCMは初期point-only。 |
| P02 | sdid_estimator | P01 | P3-M13 | unit/time weights、panel support、Method固有Variance/SE、SCMとの区別。 |
| P03 | synthetic_bundle | P01,P02 | — | donor contamination/pretreatment diagnostics・placeboとResult Bundle/Reader/old v2。 |

## 3. Execution DAG and handoff

- `P01` <- NONE
- `P02` <- P01
- `P03` <- P01,P02

Each Pxx→focused verification→20 Package Report→Checkpoint SHA。全required Package完了→Candidate Assembly→Gate-wide self-verification→single fixed candidate SHA→Independent 07→canonical 999。Package Completed≠ReadyForTest≠PASS。

## 4. Governance / Coding Authorization

P00は独立受入条件でも実装許可でもない。06/07 Freeze、Owner採用のPackage list/dependency、上流Gate canonical 999、実基準SHAとenvironment preflightが揃うまでPxxは実行禁止。Issue、Package結果、P00の状態を999代用にしない。