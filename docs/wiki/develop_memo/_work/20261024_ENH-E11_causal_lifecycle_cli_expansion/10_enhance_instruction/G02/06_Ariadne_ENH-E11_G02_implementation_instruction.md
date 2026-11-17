# Ariadne ENH-E11 / G02 — 06 実装指示書

**Document class:** Gate Coding Contract — Reviewer DRAFT  
**Gate:** G02 — 正式Enhance Workflow Gate  
**Contract status:** DRAFT / NOT_FROZEN / CODING_NOT_AUTHORIZED  
**Depends on:** G01 PASS （Owner一括レビュー承認済み・未Freeze）  
**Execution mode:** WORK_PACKAGE （Owner一括レビュー承認済み・未Freeze）  
**Required packages:** P01,P02,P03,P04 （Owner一括レビュー承認済み・未Freeze）  
**Trial:** NOT_STARTED  
**Gate07:** [07独立テスト指示書案](07_Ariadne_ENH-E11_G02_test_instruction.md) — DRAFT / NOT_FROZEN / TESTS_NOT_RUN（Owner一括レビュー承認済み・ただしOpen Decision残存、未Freeze）。  
**Baseline SHA:** 未固定（Coding Authorization時に取得）。  
**Authority/reference:** [Gate decomposition](../../40_operator_workflows/architecture_review/03_gate_decomposition.md)／[PREP-02 freeze](../../00_enhance_background/Revised_requirements_definition_documents/combined_review/117_20261117_prep02_common_contract_baseline_freeze.md)／[RD 10_32](../../00_enhance_background/Revised_requirements_definition_documents/10_requirements_definition/10_32_scientific_method_scope.md)／[DD 30_61](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_61_causal_domain_ports.md)／[DD 30_62](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_62_local_execution_publication.md)／[DD 30_63](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_63_causal_method_adapters.md)／[IF 23_41](../../00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design/23_41_cli_scientific_ports.md)／[IF 23_42](../../00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design/23_42_local_result_manifest_artifact.md)

**Owner review record:** 2026-11-18 JST、PREP-03 Final Auditの静的レビュー、G02のGate DAG・WORK_PACKAGE mode・Required packagesをOwner承認。06/07/Pxxの実装・科学的未決を補完して承認したものではない。NOT_FROZEN / CODING_NOT_AUTHORIZED / TESTS_NOT_RUNを維持。参照：[`PREP03_final_audit.md`](../PREP03_final_audit.md) §6。

## 0. Contract Boundary and PREP-03 Status

Gateの06は実装WHAT、07は独立Verification WHAT、40 Operatorは物理Test配置・実行HOW、999は唯一の正式Gate Verdict。P00はPlan、Pxxはbounded Coding Unitであり、Pxx/06の作成はGate PASS、Coding Authorization、Method Science PASS、07 Freezeを意味しない。

PREP-02のCommon Design BaselineはFreeze済み。**Gate Dependency/WORK_PACKAGE/Required Packagesの構成はOwner一括レビュー承認済み。ただし本Gate固有の未決Method config、実効Backend、独立Science Oracle、06/07/Pxxは引き続きDRAFT・NOT_FROZENで、実装開始不可。** 本文内の`Gxx PASS`は現在達成された状態ではない。

## 1. Gate Acceptance Claim and Scope

**受入命題:** Native/DoWhy識別、推定適格性、FD-A限定線形効果を安全に区別する。

**候補依存:** `G01`のlatest canonical 999 PASS。この依存DAGはOwner一括レビューで承認済み。各上流Gateのlatest canonical 999 PASSは実行時に別途検証する。Issue追跡は999の代替でない。

**科学的失敗モードと未決事項:** P1-M05のIV識別対象は未確定。FD-A識別成立と数値推定成立は別。

**対象外:** 既存Product科学ABIの変更、Web/API/DB/Worker新規統合、G01のPublisherやGraphVersionを別実装すること、他Gate MethodをScopeなしに追加すること、顧客配布許可、現時点での正本文書昇格。

## 2. Class/Module Ownership and Canonical Signatures

既存Classと新規Design Classの区別は現物Sourceで確認すること。`30_61/62/63`のClass placement、Constructor fields、Method signatureがAuthority。明記のないConcrete引数型を創作せず、設計欠落ならFreeze前に解決する。

| Class / Port | Designed module | Method signature / source | Reuse |
|---|---|---|---|
| `NativeIdentificationAdapter` | `ariadne.scientific.causal_methods.identification.NativeIdentificationAdapter` | `preflight(self, request: ValidatedMethodRequest)` → `EligibilityOutcome`; `execute(self, request: ValidatedMethodRequest, *, sink: StagingArtifactSink)` → `TypedScientificOutcome` | 既存Scientific Kernel再利用／追加Adapterの責務 |
| `IdentificationOutcome` | `ariadne.causal.identification.contracts.IdentificationOutcome` | from_evidence(evidence:ValidatedIdentificationEvidence) -> IdentificationOutcome | 既存/新規の共通Value・Port・Facade参照。重複実装しない |
| `IdentificationPort` | `ariadne.scientific.ports.causal.IdentificationPort` | identify(self, request:ValidatedIdentificationRequest) -> IdentificationOutcome | 既存/新規の共通Value・Port・Facade参照。重複実装しない |
| `DoWhyIdentificationAdapter` | `ariadne.scientific.causal_methods.identification.DoWhyIdentificationAdapter` | `preflight(self, request: ValidatedMethodRequest)` → `EligibilityOutcome`; `execute(self, request: ValidatedMethodRequest, *, sink: StagingArtifactSink)` → `TypedScientificOutcome` | 既存Scientific Kernel再利用／追加Adapterの責務 |
| `MethodCapabilityRegistry` | `ariadne.capabilities.causal.method_registry.MethodCapabilityRegistry` | describe(method_id) / resolve(method_id,backend_id,profile) / load_adapter(capability) | 既存/新規の共通Value・Port・Facade参照。重複実装しない |
| `FrontdoorLinearAdapter` | `ariadne.scientific.causal_methods.frontdoor.FrontdoorLinearAdapter` | `preflight(self, request: ValidatedMethodRequest)` → `EligibilityOutcome`; `execute(self, request: ValidatedMethodRequest, *, sink: StagingArtifactSink)` → `TypedScientificOutcome` | 既存Scientific Kernel再利用／追加Adapterの責務 |
| `EstimatorRequest` | `ariadne.causal.inference.contracts.EstimatorRequest` | validate_against(self, identification:IdentificationOutcome, design:CausalDesign, policy:EstimandEligibilityPolicy) -> ValidatedEstimatorRequest | 既存/新規の共通Value・Port・Facade参照。重複実装しない |
| `EstimatorPort` | `ariadne.scientific.ports.causal.EstimatorPort` | estimate(self, request:ValidatedEstimatorRequest, *, sink:StagingArtifactSink) -> EffectOutcome | 既存/新規の共通Value・Port・Facade参照。重複実装しない |
| `EffectOutcome` | `ariadne.causal.inference.contracts.EffectOutcome` | validate_consistency() / to_result_payload() | 既存/新規の共通Value・Port・Facade参照。重複実装しない |
| `LocalCausalUseCase` | `ariadne.capabilities.causal.local_execution.LocalCausalUseCase` | preflight(self,spec:ValidatedStudy,context:LocalRunContext)->PreflightReport / run(self,spec:ValidatedStudy,context:LocalRunContext)->LocalRunOutcome | 既存/新規の共通Value・Port・Facade参照。重複実装しない |
| `LocalRunManifest` | `ariadne.interfaces.cli.local_causal.manifest.LocalRunManifest` | to_canonical_bytes() | 既存/新規の共通Value・Port・Facade参照。重複実装しない |

**Port dependency:** Local CLI Composition Root → ValidatedStudy/ContentRef → `LocalCausalUseCase` → MethodCapabilityPort/Scientific Ports/Privacy/Publication → Method Adapter → shared `ariadne.causal.*` / `ariadne.scientific.*` Kernel。DomainからCLI ConcreteやWeb/DBへ逆依存しない。既存Product `ScientificCorePort`はBridge経由で同じ科学Kernelに接続する。

## 3. Bounded Work Packages and DAG

| Package | Responsibility | Primary Classes / Ports | Methods | Depends on Pxx |
|---|---|---|---|---|
| P01 | native identification | NativeIdentificationAdapter / IdentificationOutcome,IdentificationPort | P1-M01,P1-M02 | NONE |
| P02 | dowhy identification | DoWhyIdentificationAdapter / MethodCapabilityRegistry | P1-M03,P1-M04,P1-M05 | P01 |
| P03 | frontdoor fd a | FrontdoorLinearAdapter / EstimatorRequest,EstimatorPort,EffectOutcome | P1-M07 | P01,P02 |
| P04 | identification dispatch | — / LocalCausalUseCase,IdentificationPort,EstimatorPort,LocalRunManifest | cross-cutting | P01,P02,P03 |

全PxxのScopeとClass/Method ownershipは別文書`06_G02_Pxx_*.md`に自己完結記述。上流Packageからの利用はPort/Value/Bridgeであり、別Packageが所有するMethodを複製しない。Package setはOwnerが変更し得るため**DRAFT**。

## 4. Method Requirements, Eligibility, Positive/Negative Science

| Method / estimand | DD proof ID | Positive / Negative | Independent reference | AC | status from RD |
|---|---|---|---|---|---|
| `P1-M01` Native Randomized identification／A | `DD-E11-METH-P101` | DGP-001; NEG-001, NEG-027 | REF-G01, REF-I01 | AC-D01, AC-D02, AC-D07 | PLAN:G02 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P1-M02` Native Backdoor identification／ATE | `DD-E11-METH-P102` | DGP-002, DGP-021; NEG-002, NEG-003 | REF-G01, REF-I01 | AC-D01, AC-D02, AC-D07 | PLAN:G02 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P1-M03` DoWhy Backdoor identification／ATE候 | `DD-E11-METH-P103` | DGP-002, DGP-021; NEG-002, NEG-027 | REF-G01, REF-I01 | AC-D01, AC-D02, AC-D07 | PLAN:G02 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P1-M04` DoWhy Frontdoor identification／ATE | `DD-E11-METH-P104` | DGP-005; NEG-004 | REF-G01, REF-I02 | AC-D01, AC-D02, AC-D07 | PLAN:G02 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P1-M05` DoWhy IV identification／方法固有の対象は未確 | `DD-E11-METH-P105` | DGP-006; NEG-006, NEG-007 | REF-I03, REF-G01 | AC-D01, AC-D02, AC-D07 | PLAN:G02 / BLOCKED / NOT_GENERATED |
| `P1-M07` Frontdoor two-stage regression／ATE | `DD-E11-METH-P107` | DGP-005; NEG-004, NEG-005 | REF-I02, REF-E04 | AC-D03, AC-P01, AC-P03, AC-I01, AC-I02 | PLAN:G02 / OWNER_METHOD_ACCEPTED_TECH_AND_SCIENCE_BLOCKED / NOT_GENERATED |

**Reference rule:** MethodごとのDGP/NEG/REF/ACを必須とする。Backend自身の結果は独立Referenceではない。当該GateのRD 10_32でBLOCKEDまたはPENDINGのMethodがある場合開発都合でMethodを削除せず、識別対象/実装方法/独立Science TestをOwner決定へ戻す。科学的定量判定はOwner採用FWER=.05とMethod別PilotからのK/R/MC-SE/Resource/coverageを07に具体化してから実測する。

## 5. Global Scientific, I/O and Compatibility Constraints

- PREP-02の共通F03/F04/F05/F06/F07は適用基準。JCS RFC8785、Source/Graph/ContentRef/Manifestの異なるhash domain、atomic no-clobber、Trusted Root/independent privacy、typed scientific statusを損なわない。
- 旧Product `causal-analysis-spec/2`、`ScientificCorePort.run_*`、Web/API/Worker/DB、旧CLI、既存Refutation/Sensitivity `run`の公開ABIを変更しない。CLIだけの新Scientific Kernel、別MethodRegistry、別GraphVersion writer、別Publisherを作らない。
- Scientific `Identification/Point/Inference/ScienceAcceptance`とTechnical outcomeは別軸。不適格なMethod、無識別、Unsupported CI、missing optional Backendは型付き負結果またはTechnical error。未実行をPASS、point-onlyをCI有り、Backend自身の出力を独立Oracleにしない。
- `LocalCausalUseCase`はstrict ValidatedStudyから各Portへ委譲し、Fileはstaging→atomic Publisher→independent readback。G05のPolicy認可前は個票禁止。

**このGate固有の実装判断:** P1-M05のIV識別対象は未確定。FD-A識別成立と数値推定成立は別。各PxxのPositive/NegativeとBackend/Inference/Estimand/Statusを実行前にSchema/Registryで照合する。

## 6. Gate Coding-side Verification and Candidate Assembly

- 各PxxはMethod/DGP/NEG/REF/DD、Class.Method signature、typed Status、Backend effective API/optional Dependency、必要な実OS/CLI、既存Product invariantをFocused Testで確認。物理Path/Commandは40 Operatorがcurrent checkoutをdiscover/collectする。
- 新Testは原則`tests/enhancement/enh_e11/g02/<layer>/`、layer=unit/contract/integration（ENH-E11はCLI-only）。もし現行ProductのFrontend/Browser Regressionがaffectedならその既存Suiteも現物から検証する。科学的真偽をDir名やmockのみで推定しない。
- 全required PxxがCheckpoint SHAとStatus Reportを残してからCandidate Assembly。Gate-wide self-verification後に**1つのFixed Trial Candidate SHA**を確定、別途Freezeされた07による独立Test Item/999を実行する。
- Test-side defectはBLOCKEDとしIndependent Test Agentはtest/productionを修理しない。G10の最終統合は各Gateの独立999を置換しない。

## 7. Freeze前のReview/Stop条件

1. OwnerがGate依存・Acceptance Boundary・WORK_PACKAGE/Pxx順序を採否する。
2. `10_32`のMethod config、Estimand、DGP、NEG、Reference、実効Backend/API/Inferenceの適格性を検証する。特に本Gateの未決事項 P1-M05のIV識別対象は未確定。FD-A識別成立と数値推定成立は別。
3. 06/PxxのClass.Field/Constructor/Signature/Result authorityと既存Source、共有Port/Bridgeを整合させ、必要な設計欠落を閉じる。
4. **既存Gate07 DRAFTを本06/Pxxと照合・修正し**、Method別AC/独立科学閾値・負例・固定Fixture/Runtime・No PASS条件を確定して06/07をともにFreezeする。
5. Baseline full SHA、上流canonical 999、Runtime/Lock/License preflight、Ownerの明示Coding Authorizationが揃うまで`CODING_NOT_AUTHORIZED`。不足時は`BLOCKED_CONTRACT_AMBIGUITY`。

**本Commitには実装変更・試験実行・Owner Freeze・Coding Authorization・Gate 999判定を含めない。**
