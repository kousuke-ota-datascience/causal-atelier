# ENH-E11 G05 P00 — Work Package Plan (DRAFT)

### G05現行個票出力契約 — Owner 2026-11-21改訂

- **機能/範囲:** FR-195、NFR-031、P2-15。一般ユーザーがlocal Linux ext4/XFSで個票中間データを出力する場合、実行者がversioned Studyの`privacy.row_export_requested=true`で単独明示opt-inする。独立した人的承認者・暗号署名・鍵管理・承認失効はこの範囲に要求しない。
- **Privacy/OS:** EUIDが所有するprivate TrustedRoot、root/staging 0700、row file 0600、owner/mode/local ext4-XFS/symlink/dirfdとsame-FSを検査。rootと同一UIDのプロセスは隔離できない。個票は`RESTRICTED_ROW_LEVEL`に分類。
- **Eligibility:** `Study.privacy.row_export_requested=true` ∧ private verified root/UID ∧ Method別`ApprovedRowSchema`/許可列・行ID・row/byte/memory上限 ∧ 同一runのG01 staging。初期denyはPrivacy exit3、Source反復0・row bytes0、暗黙aggregate fallback無し。通常集計は個票権限と独立。
- **内部Port:** `LocalRunContext(root,principal)`、`LocalPrivacyPolicyPort.authorize(*,study,root,principal,output_shape)->PrivacyDecision`、`LocalCausalUseCase`に署名Verifier依存無し。`e11-local-study/1`には`privacy.policy_ref`を設けない（未知キーはstrict reject）。
- **Writer:** 既決`RowEffectsParquetWriter.__init__(*,serializer,max_memory_bytes)`、`write(*,source,study,decision,selection,sink)->ArtifactDescriptor`、`RowEffectsWriterFactory.create(*,serializer,max_memory_bytes)`、`DeferredRowEffectsSource.schema/read_rows`、`ValidatedParquetSerializer.encode(*,rows,schema)->bytes`を維持。実行条件成立後だけread_rows、G01 Sink以外へ書かない。
- **Publication/test:** `row_effects.parquet`／`application/vnd.apache.parquet`のみG01 Publisher/Readerが原子的にpublish・readback。Stage/Seal/Publish前にroot/UID/mode/FS/runを再検査、障害後にCOMMITTEDを偽装しない。個票値はaggregate Result/Manifest/CLI/logsへ出さない。未検証事項：Method RowSchema、実FS/Parquet、07独立Science/Privacy Test、Freeze、Coding Authorization。


**Gate:** G05 / Official Enhance Workflow Gate  
**Class:** Planning/Operator Artifact, not Coding Agent's normative package  
**Plan status:** OWNER_REVIEW_APPROVED / NOT_FROZEN / CODING_NOT_AUTHORIZED  
**Gate06:** [Implementation Contract](06_Ariadne_ENH-E11_G05_implementation_instruction.md)  
**Gate07:** [Independent Verification Draft](07_Ariadne_ENH-E11_G05_test_instruction.md) / DRAFT / NOT_FROZEN / TESTS_NOT_RUN  
**Owner-approved execution mode:** WORK_PACKAGE / P01,P02,P03,P04  
**Owner-approved upstream dependency:** G04 PASS。2026-11-18 JST Owner一括レビューで承認。各上流canonical 999 PASSは未成立、Runtimeで別途検証する。

**Boundary:** Gate06とGate07はimplementation claimと独立test claimを分離し、P02はlocal permission evaluator、P03はbounded row Serializer、P04はreal OS/FS E2Eを担当する。P00/Package CompleteはGate999を代替しない。

## 1. Gate semantic acceptance

**Scope:** Local intermediate row artifact only. Science CATE/DRIVの対象は変更せず、行出力はStudyの`privacy.row_export_requested=true`という単独opt-inとnonroot private rootを満たす場合だけ。


## 2. Package ownership map

| Package | Scope | Required Pxx deps | Method | Package obligations |
|---|---|---|---|---|
| P01 | hte_diagnostics | NONE | — | G04推定器を再実装せずMethod別support/calibration/uncertaintyを型付き診断。算法/Result owner不足ならDESIGN_GAP。 |
| P02 | row authorization | LocalPrivacyPolicy,LocalCausalUseCase,TrustedLocalRoot | cross-cutting | NONE |
| P03 | parquet_bundle | P01,P02 | — | Owner採用済み`RowEffectsParquetWriter.write`/Factoryと遅延許可・bound/bytes検証を本文へ埋込。Writer/Reader両側でcolumn/row bound検査。 |
| P04 | privacy_e2e | P01,P02,P03 | — | Denied時row bytes 0 / COMMITTED marker無し、shared mounts、root UID差、stdout/log leak負例。 |


**Owner OD-02/03採用によるG05実装規範：**

1. Study単独opt-in（`row_export_requested=true`）、nonroot Linux EUIDが所有するprivate ext4/XFS rootとMethod approved row schema/列行byte上限を検証。失敗時に個票Sourceを反復せずexit3。
2. Study単独opt-in（`row_export_requested=true`）、nonroot Linux EUIDが所有するprivate ext4/XFS rootとMethod approved row schema/列行byte上限を検証。失敗時に個票Sourceを反復せずexit3。
3. G05/P03の`RowEffectsParquetWriter.write`は認可済みStudy/Run/Policyと同一Sinkを確認後のみSourceを遅延反復、`max_rows+1`検出/strict列・型/メモリ/byte上限を検証し`row_effects.parquet`を`RESTRICTED_ROW_LEVEL`としてG01 StagingSinkへ書く。G01 `LocalArtifactPublisher`/Reader以外がコミット/公開をしない。
4. Study単独opt-in（`row_export_requested=true`）、nonroot Linux EUIDが所有するprivate ext4/XFS rootとMethod approved row schema/列行byte上限を検証。失敗時に個票Sourceを反復せずexit3。
5. Study単独opt-in（`row_export_requested=true`）、nonroot Linux EUIDが所有するprivate ext4/XFS rootとMethod approved row schema/列行byte上限を検証。失敗時に個票Sourceを反復せずexit3。

## 3. Execution DAG and handoff

- `P01` <- NONE
- `P02` <- NONE
- `P03` <- P01,P02
- `P04` <- P01,P02,P03

Each Pxx→focused verification→20 Package Report→Checkpoint SHA。全required Package完了→Candidate Assembly→Gate-wide self-verification→single fixed candidate SHA→Independent 07→canonical 999。Package Completed≠ReadyForTest≠PASS。

## 4. Governance / Coding Authorization

P00は独立受入条件でも実装許可でもない。06/07 Freeze、Owner採用のPackage list/dependency、上流Gate canonical 999、実基準SHAとenvironment preflightが揃うまでPxxは実行禁止。Issue、Package結果、P00の状態を999代用にしない。

### SIM-01 — local FS evidence requirements trimmed by Owner (2026-11-21)

This Gate's privacy threat boundary is a normal unprivileged Linux EUID and a local ext4/XFS filesystem. Enforce same-EUID ownership, private root/staging 0700, row file 0600, verified safe dirfd/O_NOFOLLOW/path and same-filesystem Publisher, Method-specific allowed schema/row/byte limits and both Study単独opt-in（`row_export_requested=true`） flags. **Remove as mandatory implementation/test features** independent POSIX ACL/xattr extraction/digest, statx mount-ID/namespace visibility attestation, CI/container heuristic/environment classification. This is not a guarantee against another process running with the same UID or a privileged OS administrator. Real ownership/modes/FS/path failures are still negative tests; no row source iteration before eligibility. G01 no-clobber Publisher/Reader and G05 independent science tests remain unchanged. Do not implement a key/Trust Store or signed prior approval. Reconciliation authority: combined_review/129 + /131. Independent Test NOT_RUN; Gate NOT_FROZEN.


## S02-01/02/05 現行契約の確認（2026-11-22、Owner採用）

本書が規範とする現行E11 Local個票出力の唯一の実行者opt-inは`ValidatedStudy.privacy.row_export_requested=true`である。CLI上の追加のrow-export許可flag、`LocalRunContext.cli_row_flag`、`privacy.policy_ref`、署名Verifier/鍵/独立Approverは実装しない。正規署名は`LocalRunContext(root:TrustedLocalRoot,principal:LocalPrincipal)`と`LocalPrivacyPolicyPort.authorize(*,study,root,principal,output_shape)->PrivacyDecision`。Study trueのみで個票を無条件許可するわけではない。必ずnonroot実効UID同一所有者・private ext4/XFS TrustedRoot・owner-only mode・安全なdirfd/relative path・Method別ApprovedRowSchemaとallowed ordered columns、row/byte/memory制限、同一run G01 stagingをAND検証する。未適格・false/省略はexit3、個票Source反復0・row bytes0、aggregateへ自動格下げせず、log/Manifestに個票値を流出させない。検証後もSeal/Publish/readbackまでRoot/lineage driftを拒否し、既存Product v2は変更しない。独立試験ではtrue/false/省略、未知`policy_ref`、廃止CLI flag、Wrong UID/Root、unapproved column/row/byte、WriterとReaderの正負例を検証する。本契約はS02-01/02/05の**実装指示本文**であり、科学的Test PASSやCoding Authorizationではない。
