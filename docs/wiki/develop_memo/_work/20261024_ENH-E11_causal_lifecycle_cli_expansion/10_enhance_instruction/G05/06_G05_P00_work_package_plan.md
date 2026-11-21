# ENH-E11 G05 P00 — Work Package Plan (DRAFT)

### G05現行個票出力契約 — Owner 2026-11-21改訂

- **機能/範囲:** FR-195、NFR-031、P2-15。一般ユーザーがlocal Linux ext4/XFSで個票中間データを出力する場合、実行者がStudy requestとCLI flagで明示opt-inする。独立した人的承認者・暗号署名・鍵管理・承認失効はこの範囲に要求しない。
- **Privacy/OS:** EUIDが所有するprivate TrustedRoot、root/staging 0700、row file 0600、ACL/mount/namespace/symlink/dirfdとsame-FSを検査。rootと同一UIDのプロセスは隔離できない。個票は`RESTRICTED_ROW_LEVEL`に分類。
- **Eligibility:** `Study.privacy.row_export_requested=true` ∧ `--allow-row-level-export` ∧ private verified root/UID ∧ Method別`ApprovedRowSchema`/許可列・行ID・row/byte/memory上限 ∧ 同一runのG01 staging。初期denyはPrivacy exit3、Source反復0・row bytes0、暗黙aggregate fallback無し。通常集計は個票権限と独立。
- **内部Port:** `LocalRunContext(root,principal,cli_row_flag)`、`LocalPrivacyPolicyPort.authorize(*,study,cli_row_flag,root,principal,output_shape)->PrivacyDecision`、`LocalCausalUseCase`に署名Verifier依存無し。`e11-local-study/1`の任意`privacy.policy_ref`は現行unsigned modeではnullのみ。
- **Writer:** 既決`RowEffectsParquetWriter.__init__(*,serializer,max_memory_bytes)`、`write(*,source,study,decision,selection,sink)->ArtifactDescriptor`、`RowEffectsWriterFactory.create(*,serializer,max_memory_bytes)`、`DeferredRowEffectsSource.schema/read_rows`、`ValidatedParquetSerializer.encode(*,rows,schema)->bytes`を維持。実行条件成立後だけread_rows、G01 Sink以外へ書かない。
- **Publication/test:** `row_effects.parquet`／`application/vnd.apache.parquet`のみG01 Publisher/Readerが原子的にpublish・readback。Stage/Seal/Publish前にroot/UID/mount/runを再検査、障害後にCOMMITTEDを偽装しない。個票値はaggregate Result/Manifest/CLI/logsへ出さない。未検証事項：Method RowSchema、実FS/Parquet、07独立Science/Privacy Test、Freeze、Coding Authorization。


**Gate:** G05 / Official Enhance Workflow Gate  
**Class:** Planning/Operator Artifact, not Coding Agent's normative package  
**Plan status:** OWNER_REVIEW_APPROVED / NOT_FROZEN / CODING_NOT_AUTHORIZED  
**Gate06:** [Implementation Contract](06_Ariadne_ENH-E11_G05_implementation_instruction.md)  
**Gate07:** [Independent Verification Draft](07_Ariadne_ENH-E11_G05_test_instruction.md) / DRAFT / NOT_FROZEN / TESTS_NOT_RUN  
**Owner-approved execution mode:** WORK_PACKAGE / P01,P02,P03,P04  
**Owner-approved upstream dependency:** G04 PASS。2026-11-18 JST Owner一括レビューで承認。各上流canonical 999 PASSは未成立、Runtimeで別途検証する。

**G05 local eligibility:** Study＋CLI double opt-in・nonroot EUID/private ext4/XFS・Method row schema/row+byte boundをAND評価し、初期deny時RowSource反復0/bytes0、後段異常時public commit無し。G01 Publisher/Readerだけを使用する。

## 1. Gate semantic acceptance

**G05 local eligibility:** Study＋CLI double opt-in・nonroot EUID/private ext4/XFS・Method row schema/row+byte boundをAND評価し、初期deny時RowSource反復0/bytes0、後段異常時public commit無し。G01 Publisher/Readerだけを使用する。

**G05 local eligibility:** Study＋CLI double opt-in・nonroot EUID/private ext4/XFS・Method row schema/row+byte boundをAND評価し、初期deny時RowSource反復0/bytes0、後段異常時public commit無し。G01 Publisher/Readerだけを使用する。

## 2. Package ownership map

| Package | Scope | Required Pxx deps | Method | Package obligations |
|---|---|---|---|---|
| P01 | hte_diagnostics | NONE | — | G04推定器を再実装せずMethod別support/calibration/uncertaintyを型付き診断。算法/Result owner不足ならDESIGN_GAP。 |
| P02 | row authorization | LocalPrivacyPolicy,LocalCausalUseCase,TrustedLocalRoot | cross-cutting | NONE |
| P03 | parquet_bundle | P01,P02 | — | Owner採用済み`RowEffectsParquetWriter.write`/Factoryと遅延許可・bound/bytes検証を本文へ埋込。Writer/Reader両側でcolumn/row bound検査。 |
| P04 | privacy_e2e | P01,P02,P03 | — | Denied時row bytes 0 / COMMITTED marker無し、shared mounts、root UID差、stdout/log leak負例。 |


**Owner OD-02/03採用によるG05実装規範：**

1. Study＋CLI double opt-in、nonroot Linux EUIDが所有するprivate ext4/XFS rootとMethod approved row schema/列行byte上限を検証。失敗時に個票Sourceを反復せずexit3。
2. Study＋CLI double opt-in、nonroot Linux EUIDが所有するprivate ext4/XFS rootとMethod approved row schema/列行byte上限を検証。失敗時に個票Sourceを反復せずexit3。
3. G05/P03の`RowEffectsParquetWriter.write`は認可済みStudy/Run/Policyと同一Sinkを確認後のみSourceを遅延反復、`max_rows+1`検出/strict列・型/メモリ/byte上限を検証し`row_effects.parquet`を`RESTRICTED_ROW_LEVEL`としてG01 StagingSinkへ書く。G01 `LocalArtifactPublisher`/Reader以外がコミット/公開をしない。
4. Study＋CLI double opt-in、nonroot Linux EUIDが所有するprivate ext4/XFS rootとMethod approved row schema/列行byte上限を検証。失敗時に個票Sourceを反復せずexit3。
5. Study＋CLI double opt-in、nonroot Linux EUIDが所有するprivate ext4/XFS rootとMethod approved row schema/列行byte上限を検証。失敗時に個票Sourceを反復せずexit3。

## 3. Execution DAG and handoff

- `P01` <- NONE
- `P02` <- NONE
- `P03` <- P01,P02
- `P04` <- P01,P02,P03

Each Pxx→focused verification→20 Package Report→Checkpoint SHA。全required Package完了→Candidate Assembly→Gate-wide self-verification→single fixed candidate SHA→Independent 07→canonical 999。Package Completed≠ReadyForTest≠PASS。

## 4. Governance / Coding Authorization

P00は独立受入条件でも実装許可でもない。06/07 Freeze、Owner採用のPackage list/dependency、上流Gate canonical 999、実基準SHAとenvironment preflightが揃うまでPxxは実行禁止。Issue、Package結果、P00の状態を999代用にしない。
