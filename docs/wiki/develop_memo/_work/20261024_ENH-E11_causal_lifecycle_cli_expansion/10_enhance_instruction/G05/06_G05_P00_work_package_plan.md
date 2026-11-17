# ENH-E11 G05 P00 — Work Package Plan (DRAFT)

**Gate:** G05 / Official Enhance Workflow Gate  
**Class:** Planning/Operator Artifact, not Coding Agent's normative package  
**Plan status:** DRAFT / NOT_FROZEN / CODING_NOT_AUTHORIZED  
**Gate06:** [Implementation Contract](06_Ariadne_ENH-E11_G05_implementation_instruction.md)  
**Gate07:** [Independent Verification Draft](07_Ariadne_ENH-E11_G05_test_instruction.md) / DRAFT / NOT_FROZEN / TESTS_NOT_RUN  
**Execution mode proposal:** WORK_PACKAGE / P01,P02,P03,P04  
**Upstream dependency proposal:** G04 PASS。未承認のEdgeとしてまとめReviewする。

## 1. Gate semantic acceptance

CATE support/calibration/uncertaintyと独立事前承認に基づく個票成果物発行を検証する。

**主要不確実性:** 独立承認Authority、鍵・失効、Row WriterのClass/Method所有権に設計未確定がある。

## 2. Package ownership map

| Package | Scope | Required Pxx deps | Method | Package obligations |
|---|---|---|---|---|
| P01 | hte_diagnostics | NONE | — | G04推定器を再実装せずMethod別support/calibration/uncertaintyを型付き診断。算法/Result owner不足ならDESIGN_GAP。 |
| P02 | row_authorization | NONE | — | Study要求∧CLI flag∧独立事前承認∧OS root/UID/ACL/mount∧列行上限のAND。署名方式/鍵/失効はFreeze前決定。 |
| P03 | parquet_bundle | P01,P02 | — | 個票Parquet WriterのClass責務・正確署名未確定はDESIGN_GAPとして明記。Writer/Reader両側でcolumn/row bound検査。 |
| P04 | privacy_e2e | P01,P02,P03 | — | Denied時row bytes 0 / COMMITTED marker無し、shared mounts、root UID差、stdout/log leak負例。 |

## 3. Execution DAG and handoff

- `P01` <- NONE
- `P02` <- NONE
- `P03` <- P01,P02
- `P04` <- P01,P02,P03

Each Pxx→focused verification→20 Package Report→Checkpoint SHA。全required Package完了→Candidate Assembly→Gate-wide self-verification→single fixed candidate SHA→Independent 07→canonical 999。Package Completed≠ReadyForTest≠PASS。

## 4. Governance / Coding Authorization

P00は独立受入条件でも実装許可でもない。06/07 Freeze、Owner採用のPackage list/dependency、上流Gate canonical 999、実基準SHAとenvironment preflightが揃うまでPxxは実行禁止。Issue、Package結果、P00の状態を999代用にしない。