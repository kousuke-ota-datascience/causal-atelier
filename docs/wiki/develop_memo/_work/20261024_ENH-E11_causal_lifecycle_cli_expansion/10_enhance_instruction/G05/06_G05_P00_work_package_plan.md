# ENH-E11 G05 P00 — Work Package Plan (DRAFT)

**Gate:** G05 / Official Enhance Workflow Gate  
**Class:** Planning/Operator Artifact, not Coding Agent's normative package  
**Plan status:** OWNER_REVIEW_APPROVED / NOT_FROZEN / CODING_NOT_AUTHORIZED  
**Gate06:** [Implementation Contract](06_Ariadne_ENH-E11_G05_implementation_instruction.md)  
**Gate07:** [Independent Verification Draft](07_Ariadne_ENH-E11_G05_test_instruction.md) / DRAFT / NOT_FROZEN / TESTS_NOT_RUN  
**Owner-approved execution mode:** WORK_PACKAGE / P01,P02,P03,P04  
**Owner-approved upstream dependency:** G04 PASS。2026-11-18 JST Owner一括レビューで承認。各上流canonical 999 PASSは未成立、Runtimeで別途検証する。

**Owner review:** PREP-03 Final AuditのOD-04（G05 Gate Dependency / Required Packages / Package DAG）を承認。Planの承認はGate06/07 Freeze、Owner Coding Authorization、Agent実行を許可しない。科学Method Profiles・実効Approver/鍵配備・Parquet/Security Evidenceの未了事項を維持する。参照：[`PREP03_final_audit.md`](../PREP03_final_audit.md) §6。

## 1. Gate semantic acceptance

CATE support/calibration/uncertaintyと独立事前承認に基づく個票成果物発行を検証する。

**主要不確実性:** Ed25519＋admin-only trusted signing issuer registry/失効Policyと独立Verifier、認可後だけの`RowEffectsParquetWriter`/FactoryのClass/MethodはOwner採用済み。**実際の独立Approverとadminキー管理者・鍵/失効情報配備・実効TrustedRoot/OS/Parquetの検証は未完了で個票はBLOCKED**。

## 2. Package ownership map

| Package | Scope | Required Pxx deps | Method | Package obligations |
|---|---|---|---|---|
| P01 | hte_diagnostics | NONE | — | G04推定器を再実装せずMethod別support/calibration/uncertaintyを型付き診断。算法/Result owner不足ならDESIGN_GAP。 |
| P02 | row_authorization | NONE | — | Study要求∧CLI flag∧独立事前承認∧OS root/UID/ACL/mount∧列行上限のAND。署名方式Ed25519＋admin-only Trust StoreはOwner採用済み。実体の独立承認者/鍵管理者と失効運用・実効検証はFreeze前に必要。 |
| P03 | parquet_bundle | P01,P02 | — | Owner採用済み`RowEffectsParquetWriter.write`/Factoryと遅延許可・bound/bytes検証を本文へ埋込。Writer/Reader両側でcolumn/row bound検査。 |
| P04 | privacy_e2e | P01,P02,P03 | — | Denied時row bytes 0 / COMMITTED marker無し、shared mounts、root UID差、stdout/log leak負例。 |


**Owner OD-02/03採用によるG05実装規範：**

1. Policy Envelope v1はstrict `{payload,signature_ed25519}`、signed bytes=`ASCII("ARIADNE-E11-ROW-POLICY-v1")+0x00+RFC8785_JCS(payload)`、Ed25519 detached署名。信頼できる鍵はStudy/CLIでなくEUIDが変更できないadmin trust registryから取得。`subject_study_approval_digest`はStudyの`privacy.policy_ref=null` JCS hash、`request_hash`はpolicy_ref込みで別Hash。Issuer/key role、run_id、Study/Method/content、Scope、列/行/byte cap、期限と失効epochまで照合。
2. G05/P02の`Ed25519LocalPolicyVerifier`は既存`LocalPolicyVerifierPort.verify`へ適合する。`LocalPrivacyPolicy.authorize`はStudy request∧CLI flag∧独立署名済み事前Policy∧private TrustedRoot/OS Principal∧列行上限のAND。事前DENYならrow sourceを反復せずrow bytes 0、exit3、aggregateへの勝手な切替禁止。
3. G05/P03の`RowEffectsParquetWriter.write`は認可済みStudy/Run/Policyと同一Sinkを確認後のみSourceを遅延反復、`max_rows+1`検出/strict列・型/メモリ/byte上限を検証し`row_effects.parquet`を`RESTRICTED_ROW_LEVEL`としてG01 StagingSinkへ書く。G01 `LocalArtifactPublisher`/Reader以外がコミット/公開をしない。
4. G05/P04は署名偽造、self-signed、issuer/role、鍵/Policy失効・期限、別Study/run、root/UID/ACL/mount不正、row/byte cap超過、Row source事前反復0回、staging後失効で公開無し、ログ流出無しを実環境で独立検証。Test keyの正例は**本番の独立Approval Authorityが配備済み**の証拠にならない。
5. **残るDeployment/Verification blocker:** 現実の独立Approver・admin trust store Ownerの指名、鍵Provision/Rotation、revocation freshness/clock、対象Linux mount ACL、Method別ApprovedRowSchema、Parquet実効APIと独立E2E Test。署名/Writer方式のOwner判断自体はCLOSED。G05全GateはNOT_FROZEN/CODING_NOT_AUTHORIZEDを維持。

## 3. Execution DAG and handoff

- `P01` <- NONE
- `P02` <- NONE
- `P03` <- P01,P02
- `P04` <- P01,P02,P03

Each Pxx→focused verification→20 Package Report→Checkpoint SHA。全required Package完了→Candidate Assembly→Gate-wide self-verification→single fixed candidate SHA→Independent 07→canonical 999。Package Completed≠ReadyForTest≠PASS。

## 4. Governance / Coding Authorization

P00は独立受入条件でも実装許可でもない。06/07 Freeze、Owner採用のPackage list/dependency、上流Gate canonical 999、実基準SHAとenvironment preflightが揃うまでPxxは実行禁止。Issue、Package結果、P00の状態を999代用にしない。

## PREP-04.2 / G05 operational closure checkpoint (DRAFT / NOT_FROZEN)

**Already Owner-adopted — no redesign:** OD-02 Ed25519 detached domain-separated RFC8785-JCS + admin-owned non-EUID-writable Trust Anchor; OD-03 exact `Ed25519LocalPolicyVerifier`, `RowEffectsParquetWriter`/`Factory` and `DeferredRowEffectsSource`/`ValidatedParquetSerializer` signatures; G01 alone owns staging/publication/readback. P02 is independent verification (not signing), P03 serializes only after independent authorization; P04 independently verifies the full release boundary. No new G05 Method ID or Product API/DB.

**BLOCKED deployment inputs:** real independent Approver and Trust Store admin principal unassigned; key custody/provisioning/rotation and authentic policy/key revocation source not deployed; approved revocation-snapshot freshness and trusted UTC clock operating bounds unspecified; actual EUID/ACL/mount/FS not verified; Method-specific `ApprovedRowSchema` exact ordered column/dtype/row identity not finalized; effective Parquet and Ed25519 versions/APIs not probed. Freeze can't be declared by a test key or these documentation drafts. See independent operational mapping `combined_review/128_20261121_prep04_2_g05_operational_authority_contract.md`.

**Acceptance invariant:** initial missing/invalid approval ⇒ exit3, zero `DeferredRowEffectsSource.read_rows` and zero new row bytes. Valid approval⇒ bounded ordered allowed rows only→G01 staging; recheck revocation/clock/root pre-stage/seal/publish. After authorized private staging revocation ⇒ no publish, but do not assert historical staged bytes were zero. `row_effects.parquet` restricted, no values in Result/Manifest/stdout/stderr/log; own G01 Reader required. 

**Work boundary:** no numerical timeouts/thresholds, guessed Method columns/dtypes, substituted backend libraries, new signer/Publisher or new scientific target; unresolved values remain explicit Owner/operations blockers. G05 999, Freeze and Coding Authorization NOT_PERFORMED.

**Package-specific PREP-04.2 note:** P00: accepted P01/P02/P03/P04 DAG is immutable. Separately track contract-authoring, deployment evidence, scientific evidence; P02/03 blocked release does not justify changing DAG, simplifying signing, or suppressing aggregate-only diagnostics.
