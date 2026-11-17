# ENH-E11 G07 P00 — Work Package Plan (DRAFT)

**Gate:** G07 / Official Enhance Workflow Gate  
**Class:** Planning/Operator Artifact, not Coding Agent's normative package  
**Plan status:** DRAFT / NOT_FROZEN / CODING_NOT_AUTHORIZED  
**Gate06:** [Implementation Contract](06_Ariadne_ENH-E11_G07_implementation_instruction.md)  
**Gate07:** NOT_CREATED / NOT_FROZEN  
**Execution mode proposal:** WORK_PACKAGE / P01,P02,P03  
**Upstream dependency proposal:** G02 PASS。未承認のEdgeとしてまとめReviewする。

## 1. Gate semantic acceptance

DiD/Event/ITSをtiming・pretrend・cluster・serial correlation条件付きで実行する。

**主要不確実性:** 2x2とstaggered DiDを同一TWFE ATTへ還元せず、ITSにiid SEを無検証適用しない。

## 2. Package ownership map

| Package | Scope | Required Pxx deps | Method | Package obligations |
|---|---|---|---|---|
| P01 | did_event | NONE | P3-M04,P3-M05 | Cohort/adoption timing/parallel trend/pretrend、reference period、cluster covarianceを保持。 |
| P02 | interrupted_ts | NONE | P3-M06 | Intervention level/slope、seasonality、serial covariance/HACのmethod-specific evidence。 |
| P03 | quasi_integration | P01,P02 | — | Panel/time index/Design不適格のtyped negative、Local Effect/Manifestと旧v2を統合。 |

## 3. Execution DAG and handoff

- `P01` <- NONE
- `P02` <- NONE
- `P03` <- P01,P02

Each Pxx→focused verification→20 Package Report→Checkpoint SHA。全required Package完了→Candidate Assembly→Gate-wide self-verification→single fixed candidate SHA→Independent 07→canonical 999。Package Completed≠ReadyForTest≠PASS。

## 4. Governance / Coding Authorization

P00は独立受入条件でも実装許可でもない。06/07 Freeze、Owner採用のPackage list/dependency、上流Gate canonical 999、実基準SHAとenvironment preflightが揃うまでPxxは実行禁止。Issue、Package結果、P00の状態を999代用にしない。