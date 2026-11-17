# ENH-E11 G10 P00 — Work Package Plan (DRAFT)

**Gate:** G10 / Official Enhance Workflow Gate  
**Class:** Planning/Operator Artifact, not Coding Agent's normative package  
**Plan status:** DRAFT / NOT_FROZEN / CODING_NOT_AUTHORIZED  
**Gate06:** [Implementation Contract](06_Ariadne_ENH-E11_G10_implementation_instruction.md)  
**Gate07:** NOT_CREATED / NOT_FROZEN  
**Execution mode proposal:** WORK_PACKAGE / P01,P02,P03,P04,P05  
**Upstream dependency proposal:** G01 PASS, G02 PASS, G03 PASS, G04 PASS, G05 PASS, G06 PASS, G07 PASS, G08 PASS, G09 PASS。未承認のEdgeとしてまとめReviewする。

## 1. Gate semantic acceptance

41 Method/10 UCの再実行・Manifest/依存・科学証拠・旧v2互換を統合する。

**主要不確実性:** 各GateのScience999を省略しない。GPLの顧客個別License判断は別。

## 2. Package ownership map

| Package | Scope | Required Pxx deps | Method | Package obligations |
|---|---|---|---|---|
| P01 | registry_lock | NONE | — | 41 Method registryと5 Environment profile、uv.lock/effective API/optional extras/SBOMと配布制約を検査。 |
| P02 | operation_matrix | P01 | — | DISCOVER/IDENTIFY/ESTIMATE/REFUTE/SENSITIVITY/DIAGNOSEのMethod×Estimand×Backend×CI。 |
| P03 | replay_manifest | P01,P02 | — | JCS semantic hash/Graph self hash/ContentRef bytes/Manifest marker bytes別値、readback/atomic no-clobber。 |
| P04 | science_benchmarks | P02,P03 | — | 全41のDGP/NEG/REF、FWER=.05、独立K/R/Compute/coverage/MC-SE。未測定をPASSにしない。 |
| P05 | compatibility_evidence | P03,P04 | — | 旧causal-analysis-spec/2/CLI/Web/API/Worker/DB非破壊、privacy/license evidence・顧客Legal非認定。 |

## 3. Execution DAG and handoff

- `P01` <- NONE
- `P02` <- P01
- `P03` <- P01,P02
- `P04` <- P02,P03
- `P05` <- P03,P04

Each Pxx→focused verification→20 Package Report→Checkpoint SHA。全required Package完了→Candidate Assembly→Gate-wide self-verification→single fixed candidate SHA→Independent 07→canonical 999。Package Completed≠ReadyForTest≠PASS。

## 4. Governance / Coding Authorization

P00は独立受入条件でも実装許可でもない。06/07 Freeze、Owner採用のPackage list/dependency、上流Gate canonical 999、実基準SHAとenvironment preflightが揃うまでPxxは実行禁止。Issue、Package結果、P00の状態を999代用にしない。