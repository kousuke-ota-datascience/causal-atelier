# ENH-E11 G06 P00 — Work Package Plan (DRAFT)

**Gate:** G06 / Official Enhance Workflow Gate  
**Class:** Planning/Operator Artifact, not Coding Agent's normative package  
**Plan status:** OWNER_REVIEW_APPROVED / NOT_FROZEN / CODING_NOT_AUTHORIZED  
**Gate06:** [Implementation Contract](06_Ariadne_ENH-E11_G06_implementation_instruction.md)  
**Gate07:** [Independent Verification Draft](07_Ariadne_ENH-E11_G06_test_instruction.md) / DRAFT / NOT_FROZEN / TESTS_NOT_RUN  
**Owner-approved execution mode:** WORK_PACKAGE / P01,P02,P03  
**Owner-approved upstream dependency:** G01 PASS。2026-11-18 JST Owner一括レビューで承認。各上流canonical 999 PASSは未成立、Runtimeで別途検証する。

**Owner review:** PREP-03 Final AuditのOD-04（G06 Gate Dependency / Required Packages / Package DAG）を承認。Planの承認はGate06/07 Freeze、Owner Coding Authorization、Agent実行を許可しない。科学Method・Privacy Authority・Row Writer等のOpen Decisionを維持する。参照：[`PREP03_final_audit.md`](../PREP03_final_audit.md) §6。

## 1. Gate semantic acceptance

Temporal Graphのlag/endpoint不確実性を保持しPCMCI系をMethod別に実行する。

**主要不確実性:** time index/lag sign、contemporaneous/latentと独立Graph oracle必須。PAGをDAGへ勝手に変換しない。

## 2. Package ownership map

| Package | Scope | Required Pxx deps | Method | Package obligations |
|---|---|---|---|---|
| P01 | temporal_graph | NONE | — | G01 GraphValueを再利用しTemporalConvention/lag sign/time order/CI条件を検証。 |
| P02 | pcmci_adapters | P01 | P3-M01,P3-M02,P3-M03 | Tigramite lazy import、effective API、PCMCI+/LPCMCI endpoint/latent/lag、DGP oracle。 |
| P03 | temporal_bundle | P01,P02 | — | TIME_SERIES_GRAPH/Graph lossless hash/readbackとFCI旧Graphへの回帰。 |


**Owner採用 OD-05（2026-11-19）：** G06の3 Methodについて、既決Target/数理は変更せず、担当Pxxでそれぞれstrict versioned `Method Config / Question / Design / Output / Inference Profile`を独立に定義・登録する。Method固有の確認項目は「Tigramite CI test、lag sign/zero contemporaneous edge、time-index/order、PCMCI/PCMCI+/LPCMCI endpoint/latent/Graph proof」。条件付き必須Field、Backend effective API/version/optional extras、positive/invalid-config/wrong-target/unsupported-CI/negative-science fixtureとtyped reasonを固定する。未登録/未検証は`METHOD_PROFILE_UNAVAILABLE`等でfail-closed。単なる`config={}`、Backend default、未生成DGP/REF、K/R/MC-SE未実測をPASSとしない。これはProfile作成の**担当配分採用**であり、個々のSchema/Inference/科学Referenceの完成・Freeze・Coding Authorizationを意味しない。

## 3. Execution DAG and handoff

- `P01` <- NONE
- `P02` <- P01
- `P03` <- P01,P02

Each Pxx→focused verification→20 Package Report→Checkpoint SHA。全required Package完了→Candidate Assembly→Gate-wide self-verification→single fixed candidate SHA→Independent 07→canonical 999。Package Completed≠ReadyForTest≠PASS。

## 4. Governance / Coding Authorization

P00は独立受入条件でも実装許可でもない。06/07 Freeze、Owner採用のPackage list/dependency、上流Gate canonical 999、実基準SHAとenvironment preflightが揃うまでPxxは実行禁止。Issue、Package結果、P00の状態を999代用にしない。