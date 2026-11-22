# Ariadne ENH-E11 / G05 — 06 実装指示書

### G05現行個票出力契約 — Owner 2026-11-21改訂

- **機能/範囲:** FR-195、NFR-031、P2-15。一般ユーザーがlocal Linux ext4/XFSで個票中間データを出力する場合、実行者がversioned Studyの`privacy.row_export_requested=true`で単独明示opt-inする。独立した人的承認者・暗号署名・鍵管理・承認失効はこの範囲に要求しない。
- **Privacy/OS:** EUIDが所有するprivate TrustedRoot、root/staging 0700、row file 0600、owner/mode/local ext4-XFS/symlink/dirfdとsame-FSを検査。rootと同一UIDのプロセスは隔離できない。個票は`RESTRICTED_ROW_LEVEL`に分類。
- **Eligibility:** `Study.privacy.row_export_requested=true` ∧ private verified root/UID ∧ Method別`ApprovedRowSchema`/許可列・行ID・row/byte/memory上限 ∧ 同一runのG01 staging。初期denyはPrivacy exit3、Source反復0・row bytes0、暗黙aggregate fallback無し。通常集計は個票権限と独立。
- **内部Port:** `LocalRunContext(root,principal)`、`LocalPrivacyPolicyPort.authorize(*,study,root,principal,output_shape)->PrivacyDecision`、`LocalCausalUseCase`に署名Verifier依存無し。`e11-local-study/1`には`privacy.policy_ref`を設けない（未知キーはstrict reject）。
- **Writer:** 既決`RowEffectsParquetWriter.__init__(*,serializer,max_memory_bytes)`、`write(*,source,study,decision,selection,sink)->ArtifactDescriptor`、`RowEffectsWriterFactory.create(*,serializer,max_memory_bytes)`、`DeferredRowEffectsSource.schema/read_rows`、`ValidatedParquetSerializer.encode(*,rows,schema)->bytes`を維持。実行条件成立後だけread_rows、G01 Sink以外へ書かない。
- **Publication/test:** `row_effects.parquet`／`application/vnd.apache.parquet`のみG01 Publisher/Readerが原子的にpublish・readback。Stage/Seal/Publish前にroot/UID/mode/FS/runを再検査、障害後にCOMMITTEDを偽装しない。個票値はaggregate Result/Manifest/CLI/logsへ出さない。未検証事項：Method RowSchema、実FS/Parquet、07独立Science/Privacy Test、Freeze、Coding Authorization。


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

**Scope:** Local intermediate row artifact only. Science CATE/DRIVの対象は変更せず、行出力はStudyの`privacy.row_export_requested=true`という単独opt-inとnonroot private rootを満たす場合だけ。

**候補依存:** `G04`のlatest canonical 999 PASS。この依存DAGはOwner一括レビューで承認済み。各上流Gateのlatest canonical 999 PASSは実行時に別途検証する。Issue追跡は999の代替でない。


**対象外:** 既存Product科学ABIの変更、Web/API/DB/Worker新規統合、G01のPublisherやGraphVersionを別実装すること、他Gate MethodをScopeなしに追加すること、顧客配布許可、現時点での正本文書昇格。

## 2. Class/Module Ownership and Canonical Signatures

既存Classと新規Design Classの区別は現物Sourceで確認すること。`30_61/62/63`のClass placement、Constructor fields、Method signatureがAuthority。明記のないConcrete引数型を創作せず、設計欠落ならFreeze前に解決する。

| Class / Port | Designed module | Method signature / source | Reuse |
|---|---|---|---|
| `EffectOutcome` | `ariadne.causal.inference.contracts.EffectOutcome` | validate_consistency() / to_result_payload() | 既存/新規の共通Value・Port・Facade参照。重複実装しない |
| `InferenceEvidence` | `ariadne.causal.inference.contracts.InferenceEvidence` | validate_for(mode,method) | 既存/新規の共通Value・Port・Facade参照。重複実装しない |
| `DiagnosticPort` | `ariadne.scientific.ports.causal.DiagnosticPort` | run(self, request:ValidatedDiagnosticRequest, *, sink:StagingArtifactSink) -> DiagnosticOutcome | 既存/新規の共通Value・Port・Facade参照。重複実装しない |
| `LocalPrivacyPolicy` | `ariadne.interfaces.cli.local_causal.privacy.LocalPrivacyPolicy` | authorize(self, *, study:ValidatedStudy, root:TrustedLocalRoot, principal:LocalPrincipal, output_shape:OutputShape)->PrivacyDecision / filter_export_columns(self,frame_schema:ColumnSchema,*,decision:PrivacyDecision)->ColumnSelection | 既存/新規の共通Value・Port・Facade参照。重複実装しない |
| `LocalCausalUseCase` | `ariadne.capabilities.causal.local_execution.LocalCausalUseCase` | preflight(self,spec:ValidatedStudy,context:LocalRunContext)->PreflightReport / run(self,spec:ValidatedStudy,context:LocalRunContext)->LocalRunOutcome | 既存/新規の共通Value・Port・Facade参照。重複実装しない |
| `LocalArtifactPublisher` | `ariadne.interfaces.cli.local_causal.publication.LocalArtifactPublisher` | begin(self)->StagingArtifactSink; stage_bytes(self,key:RelativeArtifactKey,data:bytes,media_type:str,classification:PrivacyClass)->ArtifactDescriptor; validate(self,manifest:LocalRunManifest)->ValidatedBundle; commit(self,validated:ValidatedBundle)->CommittedRunRef; abort(self,reason:str)->None | 既存/新規の共通Value・Port・Facade参照。重複実装しない |
| `LocalRunManifest` | `ariadne.interfaces.cli.local_causal.manifest.LocalRunManifest` | to_canonical_bytes() | 既存/新規の共通Value・Port・Facade参照。重複実装しない |
| `LocalManifestReader` | `ariadne.interfaces.cli.local_causal.manifest_reader.LocalManifestReader` | read_run(trusted_root:TrustedLocalRoot,run_id:RunId) | 既存/新規の共通Value・Port・Facade参照。重複実装しない |

| `RowEffectsParquetWriter` | `ariadne.interfaces.cli.local_causal.row_effects_parquet.RowEffectsParquetWriter` | `__init__(self, *,serializer:ValidatedParquetSerializer,max_memory_bytes:int)`; `write(self, *,source:DeferredRowEffectsSource,study:ValidatedStudy,decision:PrivacyDecision,selection:ColumnSelection,sink:StagingArtifactSink)->ArtifactDescriptor` | P03。G01 Publisher/Readerを再実装しない |
| `RowEffectsWriterFactory` | `ariadne.interfaces.cli.local_causal.row_effects_parquet.RowEffectsWriterFactory` | `create(self, *,serializer:ValidatedParquetSerializer,max_memory_bytes:int)->RowEffectsParquetWriter` | P03 factoryは承認authorityではない |

**Port dependency:** Local CLI Composition Root → ValidatedStudy/ContentRef → `LocalCausalUseCase` → MethodCapabilityPort/Scientific Ports/Privacy/Publication → Method Adapter → shared `ariadne.causal.*` / `ariadne.scientific.*` Kernel。DomainからCLI ConcreteやWeb/DBへ逆依存しない。既存Product `ScientificCorePort`はBridge経由で同じ科学Kernelに接続する。

## 3. Bounded Work Packages and DAG

| Package | Responsibility | Primary Classes / Ports | Methods | Depends on Pxx |
|---|---|---|---|---|
| P01 | hte diagnostics | — / EffectOutcome,InferenceEvidence,DiagnosticPort | cross-cutting | NONE |
| P02 | row authorization | LocalPrivacyPolicy,LocalCausalUseCase,TrustedLocalRoot | cross-cutting | NONE |
| P03 | parquet bundle | RowEffectsParquetWriter,RowEffectsWriterFactory / LocalArtifactPublisher,LocalRunManifest,LocalManifestReader | cross-cutting | P01,P02 |
| P04 | privacy e2e | — / LocalCausalUseCase,LocalPrivacyPolicy,LocalManifestReader | cross-cutting | P01,P02,P03 |

全PxxのScopeとClass/Method ownershipは別文書`06_G05_Pxx_*.md`に自己完結記述。上流Packageからの利用はPort/Value/Bridgeであり、別Packageが所有するMethodを複製しない。Package setはOwnerが変更し得るため**DRAFT**。

## 4. Method Requirements, Eligibility, Positive/Negative Science

**G05は新Method IDを追加しない。** G04のCATE/HTE Resultに対するSupport/Calibration/Inference/個票Policyの追加受入境界。

**Reference rule:** MethodごとのDGP/NEG/REF/ACを必須とする。Backend自身の結果は独立Referenceではない。当該GateのRD 10_32でBLOCKEDまたはPENDINGのMethodがある場合開発都合でMethodを削除せず、識別対象/実装方法/独立Science TestをOwner決定へ戻す。科学的定量判定はOwner採用FWER=.05とMethod別PilotからのK/R/MC-SE/Resource/coverageを07に具体化してから実測する。


**Owner OD-02/03採用によるG05実装規範：**

1. Study単独opt-in（`row_export_requested=true`）、nonroot Linux EUIDが所有するprivate ext4/XFS rootとMethod approved row schema/列行byte上限を検証。失敗時に個票Sourceを反復せずexit3。
2. Study単独opt-in（`row_export_requested=true`）、nonroot Linux EUIDが所有するprivate ext4/XFS rootとMethod approved row schema/列行byte上限を検証。失敗時に個票Sourceを反復せずexit3。
3. G05/P03の`RowEffectsParquetWriter.write`は認可済みStudy/Run/Policyと同一Sinkを確認後のみSourceを遅延反復、`max_rows+1`検出/strict列・型/メモリ/byte上限を検証し`row_effects.parquet`を`RESTRICTED_ROW_LEVEL`としてG01 StagingSinkへ書く。G01 `LocalArtifactPublisher`/Reader以外がコミット/公開をしない。
4. Study単独opt-in（`row_export_requested=true`）、nonroot Linux EUIDが所有するprivate ext4/XFS rootとMethod approved row schema/列行byte上限を検証。失敗時に個票Sourceを反復せずexit3。
5. Study単独opt-in（`row_export_requested=true`）、nonroot Linux EUIDが所有するprivate ext4/XFS rootとMethod approved row schema/列行byte上限を検証。失敗時に個票Sourceを反復せずexit3。

## 5. Global Scientific, I/O and Compatibility Constraints

- PREP-02の共通F03/F04/F05/F06/F07は適用基準。JCS RFC8785、Source/Graph/ContentRef/Manifestの異なるhash domain、atomic no-clobber、Trusted Root/independent privacy、typed scientific statusを損なわない。
- 旧Product `causal-analysis-spec/2`、`ScientificCorePort.run_*`、Web/API/Worker/DB、旧CLI、既存Refutation/Sensitivity `run`の公開ABIを変更しない。CLIだけの新Scientific Kernel、別MethodRegistry、別GraphVersion writer、別Publisherを作らない。
- Scientific `Identification/Point/Inference/ScienceAcceptance`とTechnical outcomeは別軸。不適格なMethod、無識別、Unsupported CI、missing optional Backendは型付き負結果またはTechnical error。未実行をPASS、point-onlyをCI有り、Backend自身の出力を独立Oracleにしない。
- `LocalCausalUseCase`はstrict ValidatedStudyから各Portへ委譲し、Fileはstaging→atomic Publisher→independent readback。G05のPolicy認可前は個票禁止。

**Scientific boundary:** G04のCATE(x)／DRIV heterogeneous IV coefficientは異なるEstimand。HTE support/uncertainty、Method別oracleと推論の可用性を混同せず、個票Releaseの可否を科学Statusへ偽装しない。

## 6. Gate Coding-side Verification and Candidate Assembly

- 各PxxはMethod/DGP/NEG/REF/DD、Class.Method signature、typed Status、Backend effective API/optional Dependency、必要な実OS/CLI、既存Product invariantをFocused Testで確認。物理Path/Commandは40 Operatorがcurrent checkoutをdiscover/collectする。
- 新Testは原則`tests/enhancement/enh_e11/g05/<layer>/`、layer=unit/contract/integration（ENH-E11はCLI-only）。もし現行ProductのFrontend/Browser Regressionがaffectedならその既存Suiteも現物から検証する。科学的真偽をDir名やmockのみで推定しない。
- 全required PxxがCheckpoint SHAとStatus Reportを残してからCandidate Assembly。Gate-wide self-verification後に**1つのFixed Trial Candidate SHA**を確定、別途Freezeされた07による独立Test Item/999を実行する。
- Test-side defectはBLOCKEDとしIndependent Test Agentはtest/productionを修理しない。G10の最終統合は各Gateの独立999を置換しない。

## 7. Freeze前のReview/Stop条件

1. Gate依存・WORK_PACKAGE/Pxx順序はOwner承認済み。Acceptance Boundaryの実配備・Science Profile/07検証はFreeze前に具体化する。
2. Study単独opt-in（`row_export_requested=true`）、nonroot Linux EUIDが所有するprivate ext4/XFS rootとMethod approved row schema/列行byte上限を検証。失敗時に個票Sourceを反復せずexit3。
3. 06/PxxのClass.Field/Constructor/Signature/Result authorityと既存Source、共有Port/Bridgeを整合させ、必要な設計欠落を閉じる。
4. **既存Gate07 DRAFTを本06/Pxxと照合・修正し**、Method別AC/独立科学閾値・負例・固定Fixture/Runtime・No PASS条件を確定して06/07をともにFreezeする。
5. Baseline full SHA、上流canonical 999、Runtime/Lock/License preflight、Ownerの明示Coding Authorizationが揃うまで`CODING_NOT_AUTHORIZED`。不足時は`BLOCKED_CONTRACT_AMBIGUITY`。

**本Commitには実装変更・試験実行・Owner Freeze・Coding Authorization・Gate 999判定を含めない。**


### SIM-01 — local FS evidence requirements trimmed by Owner (2026-11-21)

This Gate's privacy threat boundary is a normal unprivileged Linux EUID and a local ext4/XFS filesystem. Enforce same-EUID ownership, private root/staging 0700, row file 0600, verified safe dirfd/O_NOFOLLOW/path and same-filesystem Publisher, Method-specific allowed schema/row/byte limits and both Study単独opt-in（`row_export_requested=true`） flags. **Remove as mandatory implementation/test features** independent POSIX ACL/xattr extraction/digest, statx mount-ID/namespace visibility attestation, CI/container heuristic/environment classification. This is not a guarantee against another process running with the same UID or a privileged OS administrator. Real ownership/modes/FS/path failures are still negative tests; no row source iteration before eligibility. G01 no-clobber Publisher/Reader and G05 independent science tests remain unchanged. Do not implement a key/Trust Store or signed prior approval. Reconciliation authority: combined_review/129 + /131. Independent Test NOT_RUN; Gate NOT_FROZEN.


## S02-01/02/05 現行契約の確認（2026-11-22、Owner採用）

本書が規範とする現行E11 Local個票出力の唯一の実行者opt-inは`ValidatedStudy.privacy.row_export_requested=true`である。CLI上の追加のrow-export許可flag、`LocalRunContext.cli_row_flag`、`privacy.policy_ref`、署名Verifier/鍵/独立Approverは実装しない。正規署名は`LocalRunContext(root:TrustedLocalRoot,principal:LocalPrincipal)`と`LocalPrivacyPolicyPort.authorize(*,study,root,principal,output_shape)->PrivacyDecision`。Study trueのみで個票を無条件許可するわけではない。必ずnonroot実効UID同一所有者・private ext4/XFS TrustedRoot・owner-only mode・安全なdirfd/relative path・Method別ApprovedRowSchemaとallowed ordered columns、row/byte/memory制限、同一run G01 stagingをAND検証する。未適格・false/省略はexit3、個票Source反復0・row bytes0、aggregateへ自動格下げせず、log/Manifestに個票値を流出させない。検証後もSeal/Publish/readbackまでRoot/lineage driftを拒否し、既存Product v2は変更しない。独立試験ではtrue/false/省略、未知`policy_ref`、廃止CLI flag、Wrong UID/Root、unapproved column/row/byte、WriterとReaderの正負例を検証する。本契約はS02-01/02/05の**実装指示本文**であり、科学的Test PASSやCoding Authorizationではない。
