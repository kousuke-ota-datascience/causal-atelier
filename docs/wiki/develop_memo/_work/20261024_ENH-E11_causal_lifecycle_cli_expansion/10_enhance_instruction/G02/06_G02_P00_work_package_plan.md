# ENH-E11 G02 P00 — Work Package Plan (DRAFT)

**Gate:** G02 / Official Enhance Workflow Gate  
**Class:** Planning/Operator Artifact, not Coding Agent's normative package  
**Plan status:** DRAFT / NOT_FROZEN / CODING_NOT_AUTHORIZED  
**Gate06:** [Implementation Contract](06_Ariadne_ENH-E11_G02_implementation_instruction.md)  
**Gate07:** [Independent Verification Draft](07_Ariadne_ENH-E11_G02_test_instruction.md) / DRAFT / NOT_FROZEN / TESTS_NOT_RUN  
**Execution mode proposal:** WORK_PACKAGE / P01,P02,P03,P04  
**Upstream dependency proposal:** G01 PASS。未承認のEdgeとしてまとめReviewする。

## 1. Gate semantic acceptance

Native/DoWhy識別、推定適格性、FD-A限定線形効果を安全に区別する。

**主要不確実性:** P1-M05のIV識別対象は未確定。FD-A識別成立と数値推定成立は別。

## 2. Package ownership map

| Package | Scope | Required Pxx deps | Method | Package obligations |
|---|---|---|---|---|
| P01 | native_identification | NONE | P1-M01,P1-M02 | 既存randomized/backdoor識別・adjustment/Graph Validatorを再利用。非識別とProof/Upstream整合を厳格化。 |
| P02 | dowhy_identification | P01 | P1-M03,P1-M04,P1-M05 | DoWhy optional実効API/BackendとGraph/estimandを検証。IV内部labelをLATEへcastせず、P1-M05 target未確定ならBLOCKED。 |
| P03 | frontdoor_fd_a | P01,P02 | P1-M07 | 単一Mediator FD-Aの識別仮定と限定二段階線形数値を別契約で実装。一般Frontdoor Formulaへの拡張禁止。 |
| P04 | identification_dispatch | P01,P02,P03 | — | IDENTIFY/ESTIMATEのOperation別必須Bundleと未識別時Estimator未呼出、旧v2互換を実証。 |

## 3. Execution DAG and handoff

- `P01` <- NONE
- `P02` <- P01
- `P03` <- P01,P02
- `P04` <- P01,P02,P03

Each Pxx→focused verification→20 Package Report→Checkpoint SHA。全required Package完了→Candidate Assembly→Gate-wide self-verification→single fixed candidate SHA→Independent 07→canonical 999。Package Completed≠ReadyForTest≠PASS。

## 4. Governance / Coding Authorization

P00は独立受入条件でも実装許可でもない。06/07 Freeze、Owner採用のPackage list/dependency、上流Gate canonical 999、実基準SHAとenvironment preflightが揃うまでPxxは実行禁止。Issue、Package結果、P00の状態を999代用にしない。