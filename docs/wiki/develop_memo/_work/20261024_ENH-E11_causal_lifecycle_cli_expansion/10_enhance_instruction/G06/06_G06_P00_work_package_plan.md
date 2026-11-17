# ENH-E11 G06 P00 — Work Package Plan (DRAFT)

**Gate:** G06 / Official Enhance Workflow Gate  
**Class:** Planning/Operator Artifact, not Coding Agent's normative package  
**Plan status:** DRAFT / NOT_FROZEN / CODING_NOT_AUTHORIZED  
**Gate06:** [Implementation Contract](06_Ariadne_ENH-E11_G06_implementation_instruction.md)  
**Gate07:** NOT_CREATED / NOT_FROZEN  
**Execution mode proposal:** WORK_PACKAGE / P01,P02,P03  
**Upstream dependency proposal:** G01 PASS。未承認のEdgeとしてまとめReviewする。

## 1. Gate semantic acceptance

Temporal Graphのlag/endpoint不確実性を保持しPCMCI系をMethod別に実行する。

**主要不確実性:** time index/lag sign、contemporaneous/latentと独立Graph oracle必須。PAGをDAGへ勝手に変換しない。

## 2. Package ownership map

| Package | Scope | Required Pxx deps | Method | Package obligations |
|---|---|---|---|---|
| P01 | temporal_graph | NONE | — | G01 GraphValueを再利用しTemporalConvention/lag sign/time order/CI条件を検証。 |
| P02 | pcmci_adapters | P01 | P3-M01,P3-M02,P3-M03 | Tigramite lazy import、effective API、PCMCI+/LPCMCI endpoint/latent/lag、DGP oracle。 |
| P03 | temporal_bundle | P01,P02 | — | TIME_SERIES_GRAPH/Graph lossless hash/readbackとFCI旧Graphへの回帰。 |

## 3. Execution DAG and handoff

- `P01` <- NONE
- `P02` <- P01
- `P03` <- P01,P02

Each Pxx→focused verification→20 Package Report→Checkpoint SHA。全required Package完了→Candidate Assembly→Gate-wide self-verification→single fixed candidate SHA→Independent 07→canonical 999。Package Completed≠ReadyForTest≠PASS。

## 4. Governance / Coding Authorization

P00は独立受入条件でも実装許可でもない。06/07 Freeze、Owner採用のPackage list/dependency、上流Gate canonical 999、実基準SHAとenvironment preflightが揃うまでPxxは実行禁止。Issue、Package結果、P00の状態を999代用にしない。