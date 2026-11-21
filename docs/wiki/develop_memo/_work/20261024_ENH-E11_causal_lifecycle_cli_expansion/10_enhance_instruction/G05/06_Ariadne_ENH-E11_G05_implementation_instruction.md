# Ariadne ENH-E11 / G05 — 06 実装指示書

### 現行G05個票出力契約 — Owner 2026-11-21

- **要件:** FR-195／NFR-031／P2-15。一般ユーザーによるローカル分析中間Artifact。第三者Approver、署名、鍵、失効、issuer registryの承認プロセスを要求しない。「独立承認」ではなく「実行者の明示的opt-in」と定義する。
- **対象環境:** Linux非root実効UID・ext4/XFS local filesystem。UID=root owner、root/staging 0700・Parquet 0600、ACL/mount/namespace/symlink/dirfd・same-FSを検証。管理者・同一UID processは本Threat Modelで隔離できない。
- **許可AND:** `Study.privacy.row_export_requested=true` ∧ CLI `--allow-row-level-export` ∧ `RESTRICTED_ROW_LEVEL` ∧ 対象Methodの`ApprovedRowSchema`/ordered allowlist/row ID・row/byte/memory上限 ∧ private EUID-owned TrustedRoot ∧ same-run G01 StagingSink。未認可ならexit3、RowSource反復0・row bytes0、暗黙aggregate fallback無し。
- **既決APIの限定変更:** `LocalRunContext(root,principal,cli_row_flag)`、`LocalPrivacyPolicyPort.authorize(*,study,cli_row_flag,root,principal,output_shape)->PrivacyDecision`、`LocalCausalUseCase.__init__`から署名Verifier依存を除く。`e11-local-study/1`は維持し任意`privacy.policy_ref`は現行unsigned modeではnullのみ。
- **維持するClass:** `RowEffectsParquetWriter.__init__(*,serializer,max_memory_bytes)`、`write(*,source,study,decision,selection,sink)->ArtifactDescriptor`、`RowEffectsWriterFactory.create(*,serializer,max_memory_bytes)`、`DeferredRowEffectsSource.schema/read_rows`、`ValidatedParquetSerializer.encode(*,rows,schema)->bytes`。Sourceは全許可成立後だけ反復。WriterはG01公開責務を複製しない。
- **出力:** `row_effects.parquet`／`application/vnd.apache.parquet`／`RESTRICTED_ROW_LEVEL`。G01のみstaging/atomic no-clobber/Manifest/Marker/Reader。Stage/Seal/Publish前にroot/UID/ACL/mount/runを再検査。後段異常でprivate stagingの過去bytes0を主張せず、公開成功にもしない。Result/Manifest/stdout/stderr/logに行値なし。
- **未完了:** Method別RowSchema/制約数値、実ext4/XFS/ACL/mount、Parquet ABI、科学Reference、独立07実測。Freeze・Coding Authorization・999は未実施。変更のAuthorityは`combined_review/129_20261121_dec_g05_local_row_export_simplification.md`、過去PREP-02/03/04.2は履歴として保持。


**Document class:** Gate Coding Contract — Reviewer DRAFT  
**Gate:** G05 — 正式Enhance Workflow Gate  
**Contract status:** DRAFT / NOT_FROZEN / CODING_NOT_AUTHORIZED  
**Depends on:** G04 PASS （Owner一括レビュー承認済み・未Freeze）  
**Execution mode:** WORK_PACKAGE （Owner一括レビュー承認済み・未Freeze）  
**Required packages:** P01,P02,P03,P04 （Owner一括レビュー承認済み・未Freeze）  
**Trial:** NOT_STARTED  
**Gate07:** [07独立テスト指示書案](07_Ariadne_ENH-E11_G05_test_instruction.md) — DRAFT / NOT_FROZEN / TESTS_NOT_RUN（Owner一括レビュー承認済み・ただしOpen Decision残存、未Freeze）。  
**Baseline SHA:** 未固定（Coding Authorization時に取得）。  
**Authority/reference:** [Gate decomposition](../../40_operator_workflows/architecture_review/03_gate_decomposition.md)／[PREP-02 freeze](../../00_enhance_background/Revised_requirements_definition_documents/combined_review/117_20261117_prep02_common_contract_baseline_freeze.md)／[RD 10_32](../../00_enhance_background/Revised_requirements_definition_documents/10_requirements_definition/10_32_scientific_method_scope.md)／[DD 30_61](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_61_causal_domain_ports.md)／[DD 30_62](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_62_local_execution_publication.md)／[DD 30_63](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_63_causal_method_adapters.md)／[IF 23_41](../../00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design/23_41_cli_scientific_ports.md)／[IF 23_42](../../00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design/23_42_local_result_manifest_artifact.md)

**Owner review record:** 2026-11-18 JST、PREP-03 Final Auditの静的レビュー、G05のGate DAG・WORK_PACKAGE mode・Required packagesをOwner承認。06/07/Pxxの実装・科学的未決を補完して承認したものではない。NOT_FROZEN / CODING_NOT_AUTHORIZED / TESTS_NOT_RUNを維持。参照：[`PREP03_final_audit.md`](../PREP03_final_audit.md) §6。

## 0. Contract Boundary and PREP-03 Status

Gateの06は実装WHAT、07は独立Verification WHAT、40 Operatorは物理Test配置・実行HOW、999は唯一の正式Gate Verdict。P00はPlan、Pxxはbounded Coding Unitであり、Pxx/06の作成はGate PASS、Coding Authorization、Method Science PASS、07 Freezeを意味しない。

PREP-02のCommon Design BaselineはFreeze済み。**Gate Dependency/WORK_PACKAGE/Required Packagesの構成はOwner一括レビュー承認済み。ただし本Gate固有の未決Method config、実効Backend、独立Science Oracle、06/07/Pxxは引き続きDRAFT・NOT_FROZENで、実装開始不可。** 本文内の`Gxx PASS`は現在達成された状態ではない。

## 1. Gate Acceptance Claim and Scope

**現行G05個票出力条件:** StudyとCLIの二重opt-in、実効一般Linux UID所有のprivate ext4/XFS rootとMethod別承認済みRowSchema/列・行・byte上限のAND。初期deny時にsource反復せずexit3。既存WriterとG01 Publisher/Readerのみを使用。

**候補依存:** `G04`のlatest canonical 999 PASS。この依存DAGはOwner一括レビューで承認済み。各上流Gateのlatest canonical 999 PASSは実行時に別途検証する。Issue追跡は999の代替でない。

**現行G05個票出力条件:** StudyとCLIの二重opt-in、実効一般Linux UID所有のprivate ext4/XFS rootとMethod別承認済みRowSchema/列・行・byte上限のAND。初期deny時にsource反復せずexit3。既存WriterとG01 Publisher/Readerのみを使用。

**対象外:** 既存Product科学ABIの変更、Web/API/DB/Worker新規統合、G01のPublisherやGraphVersionを別実装すること、他Gate MethodをScopeなしに追加すること、顧客配布許可、現時点での正本文書昇格。

## 2. Class/Module Ownership and Canonical Signatures

既存Classと新規Design Classの区別は現物Sourceで確認すること。`30_61/62/63`のClass placement、Constructor fields、Method signatureがAuthority。明記のないConcrete引数型を創作せず、設計欠落ならFreeze前に解決する。

| Class / Port | Designed module | Method signature / source | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
|---|---|---| Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| `EffectOutcome` | `ariadne.causal.inference.contracts.EffectOutcome` | validate_consistency() / to_result_payload() | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| `InferenceEvidence` | `ariadne.causal.inference.contracts.InferenceEvidence` | validate_for(mode,method) | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| `DiagnosticPort` | `ariadne.scientific.ports.causal.DiagnosticPort` | run(self, request:ValidatedDiagnosticRequest, *, sink:StagingArtifactSink) -> DiagnosticOutcome | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| `LocalPrivacyPolicy` | `ariadne.interfaces.cli.local_causal.privacy.LocalPrivacyPolicy` | authorize(self, *, study:ValidatedStudy, cli_row_flag:bool, root:TrustedLocalRoot, principal:LocalPrincipal, output_shape:OutputShape)->PrivacyDecision / filter_export_columns(self,frame_schema:ColumnSchema,*,decision:PrivacyDecision)->ColumnSelection | 既存/新規の共通Value・Port・Facade参照。重複実装しない |
| `LocalCausalUseCase` | `ariadne.capabilities.causal.local_execution.LocalCausalUseCase` | preflight(self,spec:ValidatedStudy,context:LocalRunContext)->PreflightReport / run(self,spec:ValidatedStudy,context:LocalRunContext)->LocalRunOutcome | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| `LocalArtifactPublisher` | `ariadne.interfaces.cli.local_causal.publication.LocalArtifactPublisher` | begin(self)->StagingArtifactSink; stage_bytes(self,key:RelativeArtifactKey,data:bytes,media_type:str,classification:PrivacyClass)->ArtifactDescriptor; validate(self,manifest:LocalRunManifest)->ValidatedBundle; commit(self,validated:ValidatedBundle)->CommittedRunRef; abort(self,reason:str)->None | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| `LocalRunManifest` | `ariadne.interfaces.cli.local_causal.manifest.LocalRunManifest` | to_canonical_bytes() | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| `LocalManifestReader` | `ariadne.interfaces.cli.local_causal.manifest_reader.LocalManifestReader` | read_run(trusted_root:TrustedLocalRoot,run_id:RunId) | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |




| `RowEffectsParquetWriter` | `ariadne.interfaces.cli.local_causal.row_effects_parquet.RowEffectsParquetWriter` | `__init__(self, *,serializer:ValidatedParquetSerializer,max_memory_bytes:int)`; `write(self, *,source:DeferredRowEffectsSource,study:ValidatedStudy,decision:PrivacyDecision,selection:ColumnSelection,sink:StagingArtifactSink)->ArtifactDescriptor` | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| `RowEffectsWriterFactory` | `ariadne.interfaces.cli.local_causal.row_effects_parquet.RowEffectsWriterFactory` | `create(self, *,serializer:ValidatedParquetSerializer,max_memory_bytes:int)->RowEffectsParquetWriter` | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |

**Port dependency:** Local CLI Composition Root → ValidatedStudy/ContentRef → `LocalCausalUseCase` → MethodCapabilityPort/Scientific Ports/Privacy/Publication → Method Adapter → shared `ariadne.causal.*` / `ariadne.scientific.*` Kernel。DomainからCLI ConcreteやWeb/DBへ逆依存しない。既存Product `ScientificCorePort`はBridge経由で同じ科学Kernelに接続する。

## 3. Bounded Work Packages and DAG

| Package | Responsibility | Primary Classes / Ports | Methods | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
|---|---|---|---| Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| P01 | hte diagnostics | — / EffectOutcome,InferenceEvidence,DiagnosticPort | cross-cutting | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| P02 | row authorization | LocalPrivacyPolicy,LocalCausalUseCase,TrustedLocalRoot | cross-cutting | NONE |
| P03 | parquet bundle | RowEffectsParquetWriter,RowEffectsWriterFactory / LocalArtifactPublisher,LocalRunManifest,LocalManifestReader | cross-cutting | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| P04 | privacy e2e | — / LocalCausalUseCase,LocalPrivacyPolicy,LocalManifestReader | cross-cutting | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |

全PxxのScopeとClass/Method ownershipは別文書`06_G05_Pxx_*.md`に自己完結記述。上流Packageからの利用はPort/Value/Bridgeであり、別Packageが所有するMethodを複製しない。Package setはOwnerが変更し得るため**DRAFT**。

## 4. Method Requirements, Eligibility, Positive/Negative Science

**G05は新Method IDを追加しない。** G04のCATE/HTE Resultに対するSupport/Calibration/Inference/個票Policyの追加受入境界。

**Reference rule:** MethodごとのDGP/NEG/REF/ACを必須とする。Backend自身の結果は独立Referenceではない。当該GateのRD 10_32でBLOCKEDまたはPENDINGのMethodがある場合開発都合でMethodを削除せず、識別対象/実装方法/独立Science TestをOwner決定へ戻す。科学的定量判定はOwner採用FWER=.05とMethod別PilotからのK/R/MC-SE/Resource/coverageを07に具体化してから実測する。


**Owner OD-02/03採用によるG05実装規範：**

1. Study＋CLI二重opt-in、実効Linux EUID所有のprivate ext4/XFS root、Method別行列byte上限とrun identityを検証。初期denyはexit3・RowSource反復0、成功時だけG01へstage。
2. Study＋CLI二重opt-in、実効Linux EUID所有のprivate ext4/XFS root、Method別行列byte上限とrun identityを検証。初期denyはexit3・RowSource反復0、成功時だけG01へstage。
3. G05/P03の`RowEffectsParquetWriter.write`は認可済みStudy/Run/Policyと同一Sinkを確認後のみSourceを遅延反復、`max_rows+1`検出/strict列・型/メモリ/byte上限を検証し`row_effects.parquet`を`RESTRICTED_ROW_LEVEL`としてG01 StagingSinkへ書く。G01 `LocalArtifactPublisher`/Reader以外がコミット/公開をしない。
4. Study＋CLI二重opt-in、実効Linux EUID所有のprivate ext4/XFS root、Method別行列byte上限とrun identityを検証。初期denyはexit3・RowSource反復0、成功時だけG01へstage。
5. Study＋CLI二重opt-in、実効Linux EUID所有のprivate ext4/XFS root、Method別行列byte上限とrun identityを検証。初期denyはexit3・RowSource反復0、成功時だけG01へstage。

## 5. Global Scientific, I/O and Compatibility Constraints

- PREP-02の共通F03/F04/F05/F06/F07は適用基準。JCS RFC8785、Source/Graph/ContentRef/Manifestの異なるhash domain、atomic no-clobber、Trusted Root/independent privacy、typed scientific statusを損なわない。
- 旧Product `causal-analysis-spec/2`、`ScientificCorePort.run_*`、Web/API/Worker/DB、旧CLI、既存Refutation/Sensitivity `run`の公開ABIを変更しない。CLIだけの新Scientific Kernel、別MethodRegistry、別GraphVersion writer、別Publisherを作らない。
- Scientific `Identification/Point/Inference/ScienceAcceptance`とTechnical outcomeは別軸。不適格なMethod、無識別、Unsupported CI、missing optional Backendは型付き負結果またはTechnical error。未実行をPASS、point-onlyをCI有り、Backend自身の出力を独立Oracleにしない。
- `LocalCausalUseCase`はstrict ValidatedStudyから各Portへ委譲し、Fileはstaging→atomic Publisher→independent readback。G05のPolicy認可前は個票禁止。

**現行G05個票出力条件:** StudyとCLIの二重opt-in、実効一般Linux UID所有のprivate ext4/XFS rootとMethod別承認済みRowSchema/列・行・byte上限のAND。初期deny時にsource反復せずexit3。既存WriterとG01 Publisher/Readerのみを使用。

## 6. Gate Coding-side Verification and Candidate Assembly

- 各PxxはMethod/DGP/NEG/REF/DD、Class.Method signature、typed Status、Backend effective API/optional Dependency、必要な実OS/CLI、既存Product invariantをFocused Testで確認。物理Path/Commandは40 Operatorがcurrent checkoutをdiscover/collectする。
- 新Testは原則`tests/enhancement/enh_e11/g05/<layer>/`、layer=unit/contract/integration（ENH-E11はCLI-only）。もし現行ProductのFrontend/Browser Regressionがaffectedならその既存Suiteも現物から検証する。科学的真偽をDir名やmockのみで推定しない。
- 全required PxxがCheckpoint SHAとStatus Reportを残してからCandidate Assembly。Gate-wide self-verification後に**1つのFixed Trial Candidate SHA**を確定、別途Freezeされた07による独立Test Item/999を実行する。
- Test-side defectはBLOCKEDとしIndependent Test Agentはtest/productionを修理しない。G10の最終統合は各Gateの独立999を置換しない。

## 7. Freeze前のReview/Stop条件

1. Gate依存・WORK_PACKAGE/Pxx順序はOwner承認済み。Acceptance Boundaryの実配備・Science Profile/07検証はFreeze前に具体化する。
2. Study＋CLI二重opt-in、実効Linux EUID所有のprivate ext4/XFS root、Method別行列byte上限とrun identityを検証。初期denyはexit3・RowSource反復0、成功時だけG01へstage。
3. 06/PxxのClass.Field/Constructor/Signature/Result authorityと既存Source、共有Port/Bridgeを整合させ、必要な設計欠落を閉じる。
4. **既存Gate07 DRAFTを本06/Pxxと照合・修正し**、Method別AC/独立科学閾値・負例・固定Fixture/Runtime・No PASS条件を確定して06/07をともにFreezeする。
5. Baseline full SHA、上流canonical 999、Runtime/Lock/License preflight、Ownerの明示Coding Authorizationが揃うまで`CODING_NOT_AUTHORIZED`。不足時は`BLOCKED_CONTRACT_AMBIGUITY`。

**本Commitには実装変更・試験実行・Owner Freeze・Coding Authorization・Gate 999判定を含めない。**

