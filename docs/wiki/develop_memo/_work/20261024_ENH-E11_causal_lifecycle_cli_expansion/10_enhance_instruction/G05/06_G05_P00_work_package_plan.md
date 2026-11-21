# ENH-E11 G05 P00 — Work Package Plan (DRAFT)

### 現行G05個票出力契約 — Owner 2026-11-21

- **要件:** FR-195／NFR-031／P2-15。一般ユーザーによるローカル分析中間Artifact。第三者Approver、署名、鍵、失効、issuer registryの承認プロセスを要求しない。「独立承認」ではなく「実行者の明示的opt-in」と定義する。
- **対象環境:** Linux非root実効UID・ext4/XFS local filesystem。UID=root owner、root/staging 0700・Parquet 0600、ACL/mount/namespace/symlink/dirfd・same-FSを検証。管理者・同一UID processは本Threat Modelで隔離できない。
- **許可AND:** `Study.privacy.row_export_requested=true` ∧ CLI `--allow-row-level-export` ∧ `RESTRICTED_ROW_LEVEL` ∧ 対象Methodの`ApprovedRowSchema`/ordered allowlist/row ID・row/byte/memory上限 ∧ private EUID-owned TrustedRoot ∧ same-run G01 StagingSink。未認可ならexit3、RowSource反復0・row bytes0、暗黙aggregate fallback無し。
- **既決APIの限定変更:** `LocalRunContext(root,principal,cli_row_flag)`、`LocalPrivacyPolicyPort.authorize(*,study,cli_row_flag,root,principal,output_shape)->PrivacyDecision`、`LocalCausalUseCase.__init__`から署名Verifier依存を除く。`e11-local-study/1`は維持し任意`privacy.policy_ref`は現行unsigned modeではnullのみ。
- **維持するClass:** `RowEffectsParquetWriter.__init__(*,serializer,max_memory_bytes)`、`write(*,source,study,decision,selection,sink)->ArtifactDescriptor`、`RowEffectsWriterFactory.create(*,serializer,max_memory_bytes)`、`DeferredRowEffectsSource.schema/read_rows`、`ValidatedParquetSerializer.encode(*,rows,schema)->bytes`。Sourceは全許可成立後だけ反復。WriterはG01公開責務を複製しない。
- **出力:** `row_effects.parquet`／`application/vnd.apache.parquet`／`RESTRICTED_ROW_LEVEL`。G01のみstaging/atomic no-clobber/Manifest/Marker/Reader。Stage/Seal/Publish前にroot/UID/ACL/mount/runを再検査。後段異常でprivate stagingの過去bytes0を主張せず、公開成功にもしない。Result/Manifest/stdout/stderr/logに行値なし。
- **未完了:** Method別RowSchema/制約数値、実ext4/XFS/ACL/mount、Parquet ABI、科学Reference、独立07実測。Freeze・Coding Authorization・999は未実施。変更のAuthorityは`combined_review/129_20261121_dec_g05_local_row_export_simplification.md`、過去PREP-02/03/04.2は履歴として保持。


**Gate:** G05 / Official Enhance Workflow Gate  
**Class:** Planning/Operator Artifact, not Coding Agent's normative package  
**Plan status:** OWNER_REVIEW_APPROVED / NOT_FROZEN / CODING_NOT_AUTHORIZED  
**Gate06:** [Implementation Contract](06_Ariadne_ENH-E11_G05_implementation_instruction.md)  
**Gate07:** [Independent Verification Draft](07_Ariadne_ENH-E11_G05_test_instruction.md) / DRAFT / NOT_FROZEN / TESTS_NOT_RUN  
**Owner-approved execution mode:** WORK_PACKAGE / P01,P02,P03,P04  
**Owner-approved upstream dependency:** G04 PASS。2026-11-18 JST Owner一括レビューで承認。各上流canonical 999 PASSは未成立、Runtimeで別途検証する。

**現行G05個票出力条件:** StudyとCLIの二重opt-in、実効一般Linux UID所有のprivate ext4/XFS rootとMethod別承認済みRowSchema/列・行・byte上限のAND。初期deny時にsource反復せずexit3。既存WriterとG01 Publisher/Readerのみを使用。

## 1. Gate semantic acceptance

**現行G05個票出力条件:** StudyとCLIの二重opt-in、実効一般Linux UID所有のprivate ext4/XFS rootとMethod別承認済みRowSchema/列・行・byte上限のAND。初期deny時にsource反復せずexit3。既存WriterとG01 Publisher/Readerのみを使用。

**現行G05個票出力条件:** StudyとCLIの二重opt-in、実効一般Linux UID所有のprivate ext4/XFS rootとMethod別承認済みRowSchema/列・行・byte上限のAND。初期deny時にsource反復せずexit3。既存WriterとG01 Publisher/Readerのみを使用。

## 2. Package ownership map

| Package | Scope | Required Pxx deps | Method | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
|---|---|---|---| Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| P01 | hte_diagnostics | NONE | — | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| P02 | row authorization | LocalPrivacyPolicy,LocalCausalUseCase,TrustedLocalRoot | cross-cutting | NONE |
| P03 | parquet_bundle | P01,P02 | — | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| P04 | privacy_e2e | P01,P02,P03 | — | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |


**Owner OD-02/03採用によるG05実装規範：**

1. Study＋CLI二重opt-in、実効Linux EUID所有のprivate ext4/XFS root、Method別行列byte上限とrun identityを検証。初期denyはexit3・RowSource反復0、成功時だけG01へstage。
2. Study＋CLI二重opt-in、実効Linux EUID所有のprivate ext4/XFS root、Method別行列byte上限とrun identityを検証。初期denyはexit3・RowSource反復0、成功時だけG01へstage。
3. G05/P03の`RowEffectsParquetWriter.write`は認可済みStudy/Run/Policyと同一Sinkを確認後のみSourceを遅延反復、`max_rows+1`検出/strict列・型/メモリ/byte上限を検証し`row_effects.parquet`を`RESTRICTED_ROW_LEVEL`としてG01 StagingSinkへ書く。G01 `LocalArtifactPublisher`/Reader以外がコミット/公開をしない。
4. Study＋CLI二重opt-in、実効Linux EUID所有のprivate ext4/XFS root、Method別行列byte上限とrun identityを検証。初期denyはexit3・RowSource反復0、成功時だけG01へstage。
5. Study＋CLI二重opt-in、実効Linux EUID所有のprivate ext4/XFS root、Method別行列byte上限とrun identityを検証。初期denyはexit3・RowSource反復0、成功時だけG01へstage。

## 3. Execution DAG and handoff

- `P01` <- NONE
- `P02` <- NONE
- `P03` <- P01,P02
- `P04` <- P01,P02,P03

Each Pxx→focused verification→20 Package Report→Checkpoint SHA。全required Package完了→Candidate Assembly→Gate-wide self-verification→single fixed candidate SHA→Independent 07→canonical 999。Package Completed≠ReadyForTest≠PASS。

## 4. Governance / Coding Authorization

P00は独立受入条件でも実装許可でもない。06/07 Freeze、Owner採用のPackage list/dependency、上流Gate canonical 999、実基準SHAとenvironment preflightが揃うまでPxxは実行禁止。Issue、Package結果、P00の状態を999代用にしない。
