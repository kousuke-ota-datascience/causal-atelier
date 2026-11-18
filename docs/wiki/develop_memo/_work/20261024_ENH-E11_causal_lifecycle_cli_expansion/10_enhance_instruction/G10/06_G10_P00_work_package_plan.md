# ENH-E11 G10 P00 — Work Package Plan (DRAFT)

**Gate:** G10 / Official Enhance Workflow Gate  
**Class:** Planning/Operator Artifact, not Coding Agent's normative package  
**Plan status:** OWNER_REVIEW_APPROVED / NOT_FROZEN / CODING_NOT_AUTHORIZED  
**Gate06:** [Implementation Contract](06_Ariadne_ENH-E11_G10_implementation_instruction.md)  
**Gate07:** [Independent Verification Draft](07_Ariadne_ENH-E11_G10_test_instruction.md) / DRAFT / NOT_FROZEN / TESTS_NOT_RUN  
**Owner-approved execution mode:** WORK_PACKAGE / P01,P02,P03,P04,P05  
**Owner-approved upstream dependency:** G01 PASS, G02 PASS, G03 PASS, G04 PASS, G05 PASS, G06 PASS, G07 PASS, G08 PASS, G09 PASS。2026-11-18 JST Owner一括レビューで承認。各上流canonical 999 PASSは未成立、Runtimeで別途検証する。

**Owner review:** PREP-03 Final AuditのOD-04（G10 Gate Dependency / Required Packages / Package DAG）を承認。Planの承認はGate06/07 Freeze、Owner Coding Authorization、Agent実行を許可しない。科学Method・Privacy Authority・Row Writer等のOpen Decisionを維持する。参照：[`PREP03_final_audit.md`](../PREP03_final_audit.md) §6。

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


**OD-01/02/03/05（2026-11-19 Owner採用）との横断一致規範：**

- `P1-M05`はG02で`IDENTIFY`専用、明示的`B0_BINARY_IV` binary Z/A unadjusted `LATE_COMPLIER`条件付き識別。DoWhy IV internal label/`nonparametric-ate`だけでLATE証明とせず、宣言済みrelevance/exclusion/independence/monotonicity/consistency、Graph/Question/Design/Content hashとeffective APIを検証。`IDENTIFY`のEffect `result.json`は禁止。G08のB0数値推定/B1 slope/DRIVと混同しない。DGP-006、NEG-006/007、REF-I03/REF-G01は別科学Evidence。
- G05 restricted Row Parquetには独立admin-owned KeyStoreとEd25519 Policy Envelope、domain-separated JCS signature/run_id/Study approval digest/issuer role/expiry/revocation/column/row/byte limitsを全て検証した`VerifiedStudyPolicyEvidence`が必要。`RowEffectsParquetWriter`は`LocalPrivacyPolicy.authorize`の後でのみbounded row bytesをG01 StagingSinkへ作成し、G01 Publisher/Readerが唯一のpublication/readback Authority。実際の独立Approver／admin鍵Store管理者／失効・OS/Parquet検証が未配備ならRow ReleaseをBLOCKED、mock署名を本番許可としない。
- OD-05の40 Method専用Config/Question/Design/Output/Inference Profileは各Owner Gate（G02=6、G03=13、G04=8、G06=3、G07=3、G08=5、G09=2）で完成・登録されるまでは`METHOD_PROFILE_UNAVAILABLE`で該当Methodをfail-closed。P1-M06のG01 Draftを除く40件を`config={}`で一括許可しない。G10は全41 Methodの実Backend/Lock/独立DGP/NEG/REF/CI/Regressionを検証するのみ。
- 全決定は設計選択としてOwner採用済みであり、実Source/Test/uv.lock、実効Backend/独立Science、Contract Freeze、Coding Authorization、Customer LegalのPASSを意味しない。

## 3. Execution DAG and handoff

- `P01` <- NONE
- `P02` <- P01
- `P03` <- P01,P02
- `P04` <- P02,P03
- `P05` <- P03,P04

Each Pxx→focused verification→20 Package Report→Checkpoint SHA。全required Package完了→Candidate Assembly→Gate-wide self-verification→single fixed candidate SHA→Independent 07→canonical 999。Package Completed≠ReadyForTest≠PASS。

## 4. Governance / Coding Authorization

P00は独立受入条件でも実装許可でもない。06/07 Freeze、Owner採用のPackage list/dependency、上流Gate canonical 999、実基準SHAとenvironment preflightが揃うまでPxxは実行禁止。Issue、Package結果、P00の状態を999代用にしない。