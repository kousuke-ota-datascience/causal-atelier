# Ariadne ENH-E11 / G05 — 06 実装指示書

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

**受入命題:** CATE support/calibration/uncertaintyと独立事前承認に基づく個票成果物発行を検証する。

**候補依存:** `G04`のlatest canonical 999 PASS。この依存DAGはOwner一括レビューで承認済み。各上流Gateのlatest canonical 999 PASSは実行時に別途検証する。Issue追跡は999の代替でない。

**科学的失敗モードと未決事項:** Ed25519＋admin-only trusted signing issuer registry/失効Policyと独立Verifier、認可後だけの`RowEffectsParquetWriter`/FactoryのClass/MethodはOwner採用済み。**実際の独立Approverとadminキー管理者・鍵/失効情報配備・実効TrustedRoot/OS/Parquetの検証は未完了で個票はBLOCKED**。

**対象外:** 既存Product科学ABIの変更、Web/API/DB/Worker新規統合、G01のPublisherやGraphVersionを別実装すること、他Gate MethodをScopeなしに追加すること、顧客配布許可、現時点での正本文書昇格。

## 2. Class/Module Ownership and Canonical Signatures

既存Classと新規Design Classの区別は現物Sourceで確認すること。`30_61/62/63`のClass placement、Constructor fields、Method signatureがAuthority。明記のないConcrete引数型を創作せず、設計欠落ならFreeze前に解決する。

| Class / Port | Designed module | Method signature / source | Reuse |
|---|---|---|---|
| `EffectOutcome` | `ariadne.causal.inference.contracts.EffectOutcome` | validate_consistency() / to_result_payload() | 既存/新規の共通Value・Port・Facade参照。重複実装しない |
| `InferenceEvidence` | `ariadne.causal.inference.contracts.InferenceEvidence` | validate_for(mode,method) | 既存/新規の共通Value・Port・Facade参照。重複実装しない |
| `DiagnosticPort` | `ariadne.scientific.ports.causal.DiagnosticPort` | run(self, request:ValidatedDiagnosticRequest, *, sink:StagingArtifactSink) -> DiagnosticOutcome | 既存/新規の共通Value・Port・Facade参照。重複実装しない |
| `LocalPrivacyPolicy` | `ariadne.interfaces.cli.local_causal.privacy.LocalPrivacyPolicy` | authorize(self, *, study:ValidatedStudy, cli_row_flag:bool, root:TrustedLocalRoot, principal:LocalPrincipal, policy:VerifiedStudyPolicyEvidence|None, output_shape:OutputShape)->PrivacyDecision / filter_export_columns(self,frame_schema:ColumnSchema,*,decision:PrivacyDecision)->ColumnSelection | 既存/新規の共通Value・Port・Facade参照。重複実装しない |
| `LocalCausalUseCase` | `ariadne.capabilities.causal.local_execution.LocalCausalUseCase` | preflight(self,spec:ValidatedStudy,context:LocalRunContext)->PreflightReport / run(self,spec:ValidatedStudy,context:LocalRunContext)->LocalRunOutcome | 既存/新規の共通Value・Port・Facade参照。重複実装しない |
| `LocalArtifactPublisher` | `ariadne.interfaces.cli.local_causal.publication.LocalArtifactPublisher` | begin(self)->StagingArtifactSink; stage_bytes(self,key:RelativeArtifactKey,data:bytes,media_type:str,classification:PrivacyClass)->ArtifactDescriptor; validate(self,manifest:LocalRunManifest)->ValidatedBundle; commit(self,validated:ValidatedBundle)->CommittedRunRef; abort(self,reason:str)->None | 既存/新規の共通Value・Port・Facade参照。重複実装しない |
| `LocalRunManifest` | `ariadne.interfaces.cli.local_causal.manifest.LocalRunManifest` | to_canonical_bytes() | 既存/新規の共通Value・Port・Facade参照。重複実装しない |
| `LocalManifestReader` | `ariadne.interfaces.cli.local_causal.manifest_reader.LocalManifestReader` | read_run(trusted_root:TrustedLocalRoot,run_id:RunId) | 既存/新規の共通Value・Port・Facade参照。重複実装しない |

| `LocalPolicyVerifierPort` | `ariadne.capabilities.causal.ports.local_policy.LocalPolicyVerifierPort` | `verify(self, *, policy_ref:ContentRef,study:ValidatedStudy,root:TrustedLocalRoot,anchor:TrustedPolicyAnchor)->VerifiedStudyPolicyEvidence` | P02が既存Portを使い、実効AuthorityをG05で検証 |
| `Ed25519LocalPolicyVerifier` | `ariadne.interfaces.cli.local_causal.policy_verifier.Ed25519LocalPolicyVerifier` | `__init__(self, *,codec:StrictJcsCodec,clock:TrustedUtcClock)`; `verify(self, *,policy_ref:ContentRef,study:ValidatedStudy,root:TrustedLocalRoot,anchor:TrustedPolicyAnchor)->VerifiedStudyPolicyEvidence` | P02具体実装。Signing authorityではない |
| `TrustedPolicyAnchor` | `ariadne.interfaces.cli.local_causal.policy_trust.TrustedPolicyAnchor` | admin-only OS-backed immutable trust registry handle + issuer/key grants/revocation metadata | P02配備前提。EUIDが改変できないこと |
| `RowEffectsParquetWriter` | `ariadne.interfaces.cli.local_causal.row_effects_parquet.RowEffectsParquetWriter` | `__init__(self, *,serializer:ValidatedParquetSerializer,max_memory_bytes:int)`; `write(self, *,source:DeferredRowEffectsSource,study:ValidatedStudy,decision:PrivacyDecision,selection:ColumnSelection,sink:StagingArtifactSink)->ArtifactDescriptor` | P03。G01 Publisher/Readerを再実装しない |
| `RowEffectsWriterFactory` | `ariadne.interfaces.cli.local_causal.row_effects_parquet.RowEffectsWriterFactory` | `create(self, *,serializer:ValidatedParquetSerializer,max_memory_bytes:int)->RowEffectsParquetWriter` | P03 factoryは承認authorityではない |

**Port dependency:** Local CLI Composition Root → ValidatedStudy/ContentRef → `LocalCausalUseCase` → MethodCapabilityPort/Scientific Ports/Privacy/Publication → Method Adapter → shared `ariadne.causal.*` / `ariadne.scientific.*` Kernel。DomainからCLI ConcreteやWeb/DBへ逆依存しない。既存Product `ScientificCorePort`はBridge経由で同じ科学Kernelに接続する。

## 3. Bounded Work Packages and DAG

| Package | Responsibility | Primary Classes / Ports | Methods | Depends on Pxx |
|---|---|---|---|---|
| P01 | hte diagnostics | — / EffectOutcome,InferenceEvidence,DiagnosticPort | cross-cutting | NONE |
| P02 | row authorization | Ed25519LocalPolicyVerifier / LocalPolicyVerifierPort,TrustedPolicyAnchor,LocalPrivacyPolicy,LocalCausalUseCase | cross-cutting | NONE |
| P03 | parquet bundle | RowEffectsParquetWriter,RowEffectsWriterFactory / LocalArtifactPublisher,LocalRunManifest,LocalManifestReader | cross-cutting | P01,P02 |
| P04 | privacy e2e | — / LocalCausalUseCase,LocalPrivacyPolicy,LocalManifestReader | cross-cutting | P01,P02,P03 |

全PxxのScopeとClass/Method ownershipは別文書`06_G05_Pxx_*.md`に自己完結記述。上流Packageからの利用はPort/Value/Bridgeであり、別Packageが所有するMethodを複製しない。Package setはOwnerが変更し得るため**DRAFT**。

## 4. Method Requirements, Eligibility, Positive/Negative Science

**G05は新Method IDを追加しない。** G04のCATE/HTE Resultに対するSupport/Calibration/Inference/個票Policyの追加受入境界。

**Reference rule:** MethodごとのDGP/NEG/REF/ACを必須とする。Backend自身の結果は独立Referenceではない。当該GateのRD 10_32でBLOCKEDまたはPENDINGのMethodがある場合開発都合でMethodを削除せず、識別対象/実装方法/独立Science TestをOwner決定へ戻す。科学的定量判定はOwner採用FWER=.05とMethod別PilotからのK/R/MC-SE/Resource/coverageを07に具体化してから実測する。


**Owner OD-02/03採用によるG05実装規範：**

1. Policy Envelope v1はstrict `{payload,signature_ed25519}`、signed bytes=`ASCII("ARIADNE-E11-ROW-POLICY-v1")+0x00+RFC8785_JCS(payload)`、Ed25519 detached署名。信頼できる鍵はStudy/CLIでなくEUIDが変更できないadmin trust registryから取得。`subject_study_approval_digest`はStudyの`privacy.policy_ref=null` JCS hash、`request_hash`はpolicy_ref込みで別Hash。Issuer/key role、run_id、Study/Method/content、Scope、列/行/byte cap、期限と失効epochまで照合。
2. G05/P02の`Ed25519LocalPolicyVerifier`は既存`LocalPolicyVerifierPort.verify`へ適合する。`LocalPrivacyPolicy.authorize`はStudy request∧CLI flag∧独立署名済み事前Policy∧private TrustedRoot/OS Principal∧列行上限のAND。事前DENYならrow sourceを反復せずrow bytes 0、exit3、aggregateへの勝手な切替禁止。
3. G05/P03の`RowEffectsParquetWriter.write`は認可済みStudy/Run/Policyと同一Sinkを確認後のみSourceを遅延反復、`max_rows+1`検出/strict列・型/メモリ/byte上限を検証し`row_effects.parquet`を`RESTRICTED_ROW_LEVEL`としてG01 StagingSinkへ書く。G01 `LocalArtifactPublisher`/Reader以外がコミット/公開をしない。
4. G05/P04は署名偽造、self-signed、issuer/role、鍵/Policy失効・期限、別Study/run、root/UID/ACL/mount不正、row/byte cap超過、Row source事前反復0回、staging後失効で公開無し、ログ流出無しを実環境で独立検証。Test keyの正例は**本番の独立Approval Authorityが配備済み**の証拠にならない。
5. **残るDeployment/Verification blocker:** 現実の独立Approver・admin trust store Ownerの指名、鍵Provision/Rotation、revocation freshness/clock、対象Linux mount ACL、Method別ApprovedRowSchema、Parquet実効APIと独立E2E Test。署名/Writer方式のOwner判断自体はCLOSED。G05全GateはNOT_FROZEN/CODING_NOT_AUTHORIZEDを維持。

## 5. Global Scientific, I/O and Compatibility Constraints

- PREP-02の共通F03/F04/F05/F06/F07は適用基準。JCS RFC8785、Source/Graph/ContentRef/Manifestの異なるhash domain、atomic no-clobber、Trusted Root/independent privacy、typed scientific statusを損なわない。
- 旧Product `causal-analysis-spec/2`、`ScientificCorePort.run_*`、Web/API/Worker/DB、旧CLI、既存Refutation/Sensitivity `run`の公開ABIを変更しない。CLIだけの新Scientific Kernel、別MethodRegistry、別GraphVersion writer、別Publisherを作らない。
- Scientific `Identification/Point/Inference/ScienceAcceptance`とTechnical outcomeは別軸。不適格なMethod、無識別、Unsupported CI、missing optional Backendは型付き負結果またはTechnical error。未実行をPASS、point-onlyをCI有り、Backend自身の出力を独立Oracleにしない。
- `LocalCausalUseCase`はstrict ValidatedStudyから各Portへ委譲し、Fileはstaging→atomic Publisher→independent readback。G05のPolicy認可前は個票禁止。

**このGate固有の実装判断:** Ed25519＋admin-only trusted signing issuer registry/失効Policyと独立Verifier、認可後だけの`RowEffectsParquetWriter`/FactoryのClass/MethodはOwner採用済み。**実際の独立Approverとadminキー管理者・鍵/失効情報配備・実効TrustedRoot/OS/Parquetの検証は未完了で個票はBLOCKED**。各PxxのPositive/NegativeとBackend/Inference/Estimand/Statusを実行前にSchema/Registryで照合する。

## 6. Gate Coding-side Verification and Candidate Assembly

- 各PxxはMethod/DGP/NEG/REF/DD、Class.Method signature、typed Status、Backend effective API/optional Dependency、必要な実OS/CLI、既存Product invariantをFocused Testで確認。物理Path/Commandは40 Operatorがcurrent checkoutをdiscover/collectする。
- 新Testは原則`tests/enhancement/enh_e11/g05/<layer>/`、layer=unit/contract/integration（ENH-E11はCLI-only）。もし現行ProductのFrontend/Browser Regressionがaffectedならその既存Suiteも現物から検証する。科学的真偽をDir名やmockのみで推定しない。
- 全required PxxがCheckpoint SHAとStatus Reportを残してからCandidate Assembly。Gate-wide self-verification後に**1つのFixed Trial Candidate SHA**を確定、別途Freezeされた07による独立Test Item/999を実行する。
- Test-side defectはBLOCKEDとしIndependent Test Agentはtest/productionを修理しない。G10の最終統合は各Gateの独立999を置換しない。

## 7. Freeze前のReview/Stop条件

1. Gate依存・WORK_PACKAGE/Pxx順序はOwner承認済み。Acceptance Boundaryの実配備・Science Profile/07検証はFreeze前に具体化する。
2. `10_32`のMethod config、Estimand、DGP、NEG、Reference、実効Backend/API/Inferenceの適格性を検証する。特に本Gateの未決事項 Ed25519＋admin-only trusted signing issuer registry/失効Policyと独立Verifier、認可後だけの`RowEffectsParquetWriter`/FactoryのClass/MethodはOwner採用済み。**実際の独立Approverとadminキー管理者・鍵/失効情報配備・実効TrustedRoot/OS/Parquetの検証は未完了で個票はBLOCKED**。
3. 06/PxxのClass.Field/Constructor/Signature/Result authorityと既存Source、共有Port/Bridgeを整合させ、必要な設計欠落を閉じる。
4. **既存Gate07 DRAFTを本06/Pxxと照合・修正し**、Method別AC/独立科学閾値・負例・固定Fixture/Runtime・No PASS条件を確定して06/07をともにFreezeする。
5. Baseline full SHA、上流canonical 999、Runtime/Lock/License preflight、Ownerの明示Coding Authorizationが揃うまで`CODING_NOT_AUTHORIZED`。不足時は`BLOCKED_CONTRACT_AMBIGUITY`。

**本Commitには実装変更・試験実行・Owner Freeze・Coding Authorization・Gate 999判定を含めない。**
