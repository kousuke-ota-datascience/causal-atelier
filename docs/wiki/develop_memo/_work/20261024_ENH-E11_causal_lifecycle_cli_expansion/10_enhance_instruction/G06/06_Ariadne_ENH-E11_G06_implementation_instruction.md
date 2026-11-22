# Ariadne ENH-E11 / G06 — 06 実装指示書

**DEC-PREPCODE-01=B（Owner 2026-11-22採用）：Gate別S09→S10→S11。** G06の独立S09監査は、先行Gate（G01）と共通E11 Wire/Port/Privacy/JCS/Publisher/Reader/Protected v2の変更影響閉包、およびG06自身の06/P00/Pxx/07/Method Profile/Backend/Scienceを対象とする。対象外Gateは全体SHA inventoryに保持し`NOT_REVIEWED`、未決の後続MethodはG06のCoding前無条件停止条件にしない。G06固有の独立S09 verdict→Owner G06-S10 Freeze→Owner G06-S11 Coding Authorizationを別々に取得する。**S11実行前にはG01_999の実PASSが必須**だが、S09文書監査の準備は先行Gateの実装中にも可能。実Adapter/FS/数値T2/T3/RegressionはG06の独立07/999で検証し、文書修正だけでPASSを付けない。現時点は`S09_NOT_RUN/S10_NOT_FROZEN/S11_NOT_AUTHORIZED`。

**Document class:** Gate Coding Contract — Reviewer DRAFT  
**Gate:** G06 — 正式Enhance Workflow Gate  
**Contract status:** DRAFT / NOT_FROZEN / CODING_NOT_AUTHORIZED  
**Depends on:** G01 PASS （Owner一括レビュー承認済み・未Freeze）  
**Execution mode:** WORK_PACKAGE （Owner一括レビュー承認済み・未Freeze）  
**Required packages:** P01,P02,P03 （Owner一括レビュー承認済み・未Freeze）  
**Trial:** NOT_STARTED  
**Gate07:** [07独立テスト指示書案](07_Ariadne_ENH-E11_G06_test_instruction.md) — DRAFT / NOT_FROZEN / TESTS_NOT_RUN（Owner一括レビュー承認済み・ただしOpen Decision残存、未Freeze）。  
**Baseline SHA:** 未固定（Coding Authorization時に取得）。  
**Authority/reference:** [Gate decomposition](../../40_operator_workflows/architecture_review/03_gate_decomposition.md)／[PREP-02 freeze](../../00_enhance_background/Revised_requirements_definition_documents/combined_review/117_20261117_prep02_common_contract_baseline_freeze.md)／[RD 10_32](../../00_enhance_background/Revised_requirements_definition_documents/10_requirements_definition/10_32_scientific_method_scope.md)／[DD 30_61](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_61_causal_domain_ports.md)／[DD 30_62](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_62_local_execution_publication.md)／[DD 30_63](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_63_causal_method_adapters.md)／[IF 23_41](../../00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design/23_41_cli_scientific_ports.md)／[IF 23_42](../../00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design/23_42_local_result_manifest_artifact.md)

**Owner review record:** 2026-11-18 JST、PREP-03 Final Auditの静的レビュー、G06のGate DAG・WORK_PACKAGE mode・Required packagesをOwner承認。06/07/Pxxの実装・科学的未決を補完して承認したものではない。NOT_FROZEN / CODING_NOT_AUTHORIZED / TESTS_NOT_RUNを維持。参照：[`PREP03_final_audit.md`](../PREP03_final_audit.md) §6。

## 0. Contract Boundary and PREP-03 Status

Gateの06は実装WHAT、07は独立Verification WHAT、40 Operatorは物理Test配置・実行HOW、999は唯一の正式Gate Verdict。P00はPlan、Pxxはbounded Coding Unitであり、Pxx/06の作成はGate PASS、Coding Authorization、Method Science PASS、07 Freezeを意味しない。

PREP-02のCommon Design BaselineはFreeze済み。**Gate Dependency/WORK_PACKAGE/Required Packagesの構成はOwner一括レビュー承認済み。ただし本Gate固有の未決Method config、実効Backend、独立Science Oracle、06/07/Pxxは引き続きDRAFT・NOT_FROZENで、実装開始不可。** 本文内の`Gxx PASS`は現在達成された状態ではない。

## 1. Gate Acceptance Claim and Scope

**受入命題:** Temporal Graphのlag/endpoint不確実性を保持しPCMCI系をMethod別に実行する。

**候補依存:** `G01`のlatest canonical 999 PASS。この依存DAGはOwner一括レビューで承認済み。各上流Gateのlatest canonical 999 PASSは実行時に別途検証する。Issue追跡は999の代替でない。

**科学的失敗モードと未決事項:** time index/lag sign、contemporaneous/latentと独立Graph oracle必須。PAGをDAGへ勝手に変換しない。

**対象外:** 既存Product科学ABIの変更、Web/API/DB/Worker新規統合、G01のPublisherやGraphVersionを別実装すること、他Gate MethodをScopeなしに追加すること、顧客配布許可、現時点での正本文書昇格。

## 2. Class/Module Ownership and Canonical Signatures

既存Classと新規Design Classの区別は現物Sourceで確認すること。`30_61/62/63`のClass placement、Constructor fields、Method signatureがAuthority。明記のないConcrete引数型を創作せず、設計欠落ならFreeze前に解決する。

| Class / Port | Designed module | Method signature / source | Reuse |
|---|---|---|---|
| `GraphEvidence` | `ariadne.causal.discovery.graph_evidence.GraphEvidence` | from_canonical_json(raw:bytes) / canonical_payload() | 既存/新規の共通Value・Port・Facade参照。重複実装しない |
| `DiscoveryPort` | `ariadne.scientific.ports.causal.DiscoveryPort` | discover(self, request:ValidatedDiscoveryRequest, *, sink:StagingArtifactSink) -> DiscoveryGraphOutcome | 既存/新規の共通Value・Port・Facade参照。重複実装しない |
| `MethodCapabilityRegistry` | `ariadne.capabilities.causal.method_registry.MethodCapabilityRegistry` | describe(method_id) / resolve(method_id,backend_id,profile) / load_adapter(capability) | 既存/新規の共通Value・Port・Facade参照。重複実装しない |
| `TigramiteTemporalAdapter` | `ariadne.scientific.causal_methods.temporal.TigramiteTemporalAdapter` | `preflight(self, request: ValidatedMethodRequest)` → `EligibilityOutcome`; `execute(self, request: ValidatedMethodRequest, *, sink: StagingArtifactSink)` → `TypedScientificOutcome` | 既存Scientific Kernel再利用／追加Adapterの責務 |
| `LocalCausalUseCase` | `ariadne.capabilities.causal.local_execution.LocalCausalUseCase` | preflight(self,spec:ValidatedStudy,context:LocalRunContext)->PreflightReport / run(self,spec:ValidatedStudy,context:LocalRunContext)->LocalRunOutcome | 既存/新規の共通Value・Port・Facade参照。重複実装しない |
| `LocalManifestReader` | `ariadne.interfaces.cli.local_causal.manifest_reader.LocalManifestReader` | read_run(trusted_root:TrustedLocalRoot,run_id:RunId) | 既存/新規の共通Value・Port・Facade参照。重複実装しない |

**Port dependency:** Local CLI Composition Root → ValidatedStudy/ContentRef → `LocalCausalUseCase` → MethodCapabilityPort/Scientific Ports/Privacy/Publication → Method Adapter → shared `ariadne.causal.*` / `ariadne.scientific.*` Kernel。DomainからCLI ConcreteやWeb/DBへ逆依存しない。既存Product `ScientificCorePort`はBridge経由で同じ科学Kernelに接続する。

## 3. Bounded Work Packages and DAG

| Package | Responsibility | Primary Classes / Ports | Methods | Depends on Pxx |
|---|---|---|---|---|
| P01 | temporal graph | — / GraphEvidence,DiscoveryPort,MethodCapabilityRegistry | cross-cutting | NONE |
| P02 | pcmci adapters | TigramiteTemporalAdapter / DiscoveryPort | P3-M01,P3-M02,P3-M03 | P01 |
| P03 | temporal bundle | — / LocalCausalUseCase,GraphEvidence,LocalManifestReader | cross-cutting | P01,P02 |

全PxxのScopeとClass/Method ownershipは別文書`06_G06_Pxx_*.md`に自己完結記述。上流Packageからの利用はPort/Value/Bridgeであり、別Packageが所有するMethodを複製しない。Package setはOwnerが変更し得るため**DRAFT**。

## 4. Method Requirements, Eligibility, Positive/Negative Science

| Method / estimand | DD proof ID | Positive / Negative | Independent reference | AC | status from RD |
|---|---|---|---|---|---|
| `P3-M01` PCMCI／time-lagged graph | `DD-E11-METH-P301` | DGP-009; NEG-021 | REF-G03 | AC-D01, AC-G01, AC-G02, AC-G03, AC-G05 | PLAN:G06 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P3-M02` PCMCI+／time-series CPDAG | `DD-E11-METH-P302` | DGP-009, DGP-010; NEG-021, NEG-028 | REF-G03, REF-G02 | AC-D01, AC-G01, AC-G02, AC-G03, AC-G04, AC-G06 | PLAN:G06 / OWNER_ORACLE_PRINCIPLE_ACCEPTED_ORACLE_BLOCKED / NOT_GENERATED |
| `P3-M03` LPCMCI／time-series PAG | `DD-E11-METH-P303` | DGP-011; NEG-021, NEG-028 | REF-G03, REF-G02 | AC-D01, AC-G01, AC-G02, AC-G03, AC-G04, AC-G06 | PLAN:G06 / OWNER_ORACLE_PRINCIPLE_ACCEPTED_ORACLE_BLOCKED / NOT_GENERATED |

**Reference rule:** MethodごとのDGP/NEG/REF/ACを必須とする。Backend自身の結果は独立Referenceではない。当該GateのRD 10_32でBLOCKEDまたはPENDINGのMethodがある場合開発都合でMethodを削除せず、識別対象/実装方法/独立Science TestをOwner決定へ戻す。科学的定量判定はOwner採用FWER=.05とMethod別PilotからのK/R/MC-SE/Resource/coverageを07に具体化してから実測する。


**Owner採用 OD-05（2026-11-19）：** G06の3 Methodについて、既決Target/数理は変更せず、担当Pxxでそれぞれstrict versioned `Method Config / Question / Design / Output / Inference Profile`を独立に定義・登録する。Method固有の確認項目は「Tigramite CI test、lag sign/zero contemporaneous edge、time-index/order、PCMCI/PCMCI+/LPCMCI endpoint/latent/Graph proof」。条件付き必須Field、Backend effective API/version/optional extras、positive/invalid-config/wrong-target/unsupported-CI/negative-science fixtureとtyped reasonを固定する。未登録/未検証は`METHOD_PROFILE_UNAVAILABLE`等でfail-closed。単なる`config={}`、Backend default、未生成DGP/REF、K/R/MC-SE未実測をPASSとしない。これはProfile作成の**担当配分採用**であり、個々のSchema/Inference/科学Referenceの完成・Freeze・Coding Authorizationを意味しない。

## 5. Global Scientific, I/O and Compatibility Constraints

- PREP-02の共通F03/F04/F05/F06/F07は適用基準。JCS RFC8785、Source/Graph/ContentRef/Manifestの異なるhash domain、atomic no-clobber、Trusted Root/independent privacy、typed scientific statusを損なわない。
- 旧Product `causal-analysis-spec/2`、`ScientificCorePort.run_*`、Web/API/Worker/DB、旧CLI、既存Refutation/Sensitivity `run`の公開ABIを変更しない。CLIだけの新Scientific Kernel、別MethodRegistry、別GraphVersion writer、別Publisherを作らない。
- Scientific `Identification/Point/Inference/ScienceAcceptance`とTechnical outcomeは別軸。不適格なMethod、無識別、Unsupported CI、missing optional Backendは型付き負結果またはTechnical error。未実行をPASS、point-onlyをCI有り、Backend自身の出力を独立Oracleにしない。
- `LocalCausalUseCase`はstrict ValidatedStudyから各Portへ委譲し、Fileはstaging→atomic Publisher→independent readback。G05のPolicy認可前は個票禁止。

**このGate固有の実装判断:** time index/lag sign、contemporaneous/latentと独立Graph oracle必須。PAGをDAGへ勝手に変換しない。各PxxのPositive/NegativeとBackend/Inference/Estimand/Statusを実行前にSchema/Registryで照合する。

## 6. Gate Coding-side Verification and Candidate Assembly

- 各PxxはMethod/DGP/NEG/REF/DD、Class.Method signature、typed Status、Backend effective API/optional Dependency、必要な実OS/CLI、既存Product invariantをFocused Testで確認。物理Path/Commandは40 Operatorがcurrent checkoutをdiscover/collectする。
- 新Testは原則`tests/enhancement/enh_e11/g06/<layer>/`、layer=unit/contract/integration（ENH-E11はCLI-only）。もし現行ProductのFrontend/Browser Regressionがaffectedならその既存Suiteも現物から検証する。科学的真偽をDir名やmockのみで推定しない。
- 全required PxxがCheckpoint SHAとStatus Reportを残してからCandidate Assembly。Gate-wide self-verification後に**1つのFixed Trial Candidate SHA**を確定、別途Freezeされた07による独立Test Item/999を実行する。
- Test-side defectはBLOCKEDとしIndependent Test Agentはtest/productionを修理しない。G10の最終統合は各Gateの独立999を置換しない。

## 7. Freeze前のReview/Stop条件

1. OwnerがGate依存・Acceptance Boundary・WORK_PACKAGE/Pxx順序を採否する。
2. `10_32`のMethod config、Estimand、DGP、NEG、Reference、実効Backend/API/Inferenceの適格性を検証する。特に本Gateの未決事項 time index/lag sign、contemporaneous/latentと独立Graph oracle必須。PAGをDAGへ勝手に変換しない。
3. 06/PxxのClass.Field/Constructor/Signature/Result authorityと既存Source、共有Port/Bridgeを整合させ、必要な設計欠落を閉じる。
4. **既存Gate07 DRAFTを本06/Pxxと照合・修正し**、Method別AC/独立科学閾値・負例・固定Fixture/Runtime・No PASS条件を確定して06/07をともにFreezeする。
5. Baseline full SHA、上流canonical 999、Runtime/Lock/License preflight、Ownerの明示Coding Authorizationが揃うまで`CODING_NOT_AUTHORIZED`。不足時は`BLOCKED_CONTRACT_AMBIGUITY`。

**本Commitには実装変更・試験実行・Owner Freeze・Coding Authorization・Gate 999判定を含めない。**


## PREP-04.1 Method ownership matrix (DRAFT)
- P3-M01 Pxx P02 DISCOVER/10_32 semantic target (not assigned canonical enum) Config(ci_test_spec_ref, tau_min, tau_max, alpha), Design(time_index, sampling_unit, observed_variables, temporal_ordering_ref, lag_convention_ref), DGP-009; NEG-021; REF-G03; Backend/Science BLOCKED.
- P3-M02 Pxx P02 DISCOVER/10_32 semantic target (not assigned canonical enum) Config(ci_test_spec_ref, tau_min, tau_max, alpha, contemporaneous_rules_ref), Design(time_index, sampling_unit, observed_variables, temporal_ordering_ref, lag_convention_ref, endpoint_convention_ref), DGP-009, DGP-010; NEG-021, NEG-028; REF-G03, REF-G02; Backend/Science BLOCKED.
- P3-M03 Pxx P02 DISCOVER/10_32 semantic target (not assigned canonical enum) Config(ci_test_spec_ref, tau_min, tau_max, alpha, latent_assumptions_ref), Design(time_index, sampling_unit, observed_variables, temporal_ordering_ref, lag_convention_ref, endpoint_convention_ref), DGP-011; NEG-021, NEG-028; REF-G03, REF-G02; Backend/Science BLOCKED.

## S02簡素化・G06 Temporal GraphとMethod Profileの規範

担当Methodは`P3-M01` PCMCI、`P3-M02` PCMCI+、`P3-M03` LPCMCIの3件。5 Profile kind（method_config/question_profile/design_profile/output_profile/inference_profile）は`23_api_interface_design/schema_drafts/method_profiles/factored/e11_<kind>_factored_v1.json`のshared core＋exact Method ID overlayから再構成し、Dispatch Registry/200 Schema標準Draft202012/正負例/parityの確認が不足すれば`METHOD_PROFILE_UNAVAILABLE`でfail-closed。科学的契約は各Methodで異なり、time-lag端点の向き/ラグ0、PAG/CPDAG同値類、潜在交絡・CIテストの意味を厳格保存し、グラフ方向を自動確定しない。ENV-TIGRAMITEの実効Python3.12 APIと独立時系列Graph Oracleの実測は後続検証事項。

新Local Graphは内容hashとsource/parent科学由来を保持するがProduct GraphVersion DBはlookup/edit/write/FIXしない。`version_id=parent_version_id=null`のみ提供し、non-null importは未対応として拒否。共通`LocalRunContext(root,principal)`、`LocalPrivacyPolicyPort.authorize(*,study,root,principal,output_shape)`を利用し、署名Verifier/Policy Anchorと追加CLI flagを作らない。G06は個票を直接公開せず、旧Product v2のABIと共通Kernelを保護する。独立Testは時系列順序・PAG/CPDAG同値類・Graph hash/Manifest/readback・wrong Method/unsupported CIの負例を確認する。未実測をScience PASSとしない。
