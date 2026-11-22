# Ariadne ENH-E11 / G08 — 06 実装指示書

**Document class:** Gate Coding Contract — Reviewer DRAFT  
**Gate:** G08 — 正式Enhance Workflow Gate  
**Contract status:** DRAFT / NOT_FROZEN / CODING_NOT_AUTHORIZED  
**Depends on:** G01 PASS, G02 PASS （Owner一括レビュー承認済み・未Freeze）  
**Execution mode:** WORK_PACKAGE （Owner一括レビュー承認済み・未Freeze）  
**Required packages:** P01,P02,P03,P04 （Owner一括レビュー承認済み・未Freeze）  
**Trial:** NOT_STARTED  
**Gate07:** [07独立テスト指示書案](07_Ariadne_ENH-E11_G08_test_instruction.md) — DRAFT / NOT_FROZEN / TESTS_NOT_RUN（Owner一括レビュー承認済み・ただしOpen Decision残存、未Freeze）。  
**Baseline SHA:** 未固定（Coding Authorization時に取得）。  
**Authority/reference:** [Gate decomposition](../../40_operator_workflows/architecture_review/03_gate_decomposition.md)／[PREP-02 freeze](../../00_enhance_background/Revised_requirements_definition_documents/combined_review/117_20261117_prep02_common_contract_baseline_freeze.md)／[RD 10_32](../../00_enhance_background/Revised_requirements_definition_documents/10_requirements_definition/10_32_scientific_method_scope.md)／[DD 30_61](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_61_causal_domain_ports.md)／[DD 30_62](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_62_local_execution_publication.md)／[DD 30_63](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_63_causal_method_adapters.md)／[IF 23_41](../../00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design/23_41_cli_scientific_ports.md)／[IF 23_42](../../00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design/23_42_local_result_manifest_artifact.md)

**Owner review record:** 2026-11-18 JST、PREP-03 Final Auditの静的レビュー、G08のGate DAG・WORK_PACKAGE mode・Required packagesをOwner承認。06/07/Pxxの実装・科学的未決を補完して承認したものではない。NOT_FROZEN / CODING_NOT_AUTHORIZED / TESTS_NOT_RUNを維持。参照：[`PREP03_final_audit.md`](../PREP03_final_audit.md) §6。

## 0. Contract Boundary and PREP-03 Status

Gateの06は実装WHAT、07は独立Verification WHAT、40 Operatorは物理Test配置・実行HOW、999は唯一の正式Gate Verdict。P00はPlan、Pxxはbounded Coding Unitであり、Pxx/06の作成はGate PASS、Coding Authorization、Method Science PASS、07 Freezeを意味しない。

PREP-02のCommon Design BaselineはFreeze済み。**Gate Dependency/WORK_PACKAGE/Required Packagesの構成はOwner一括レビュー承認済み。ただし本Gate固有の未決Method config、実効Backend、独立Science Oracle、06/07/Pxxは引き続きDRAFT・NOT_FROZENで、実装開始不可。** 本文内の`Gxx PASS`は現在達成された状態ではない。

## 1. Gate Acceptance Claim and Scope

**受入命題:** Sharp/Fuzzy RDDとB0/B1 IV/2SLSを局所Estimand・弱IV AR集合付きで提供する。

**候補依存:** `G01`・`G02`のlatest canonical 999 PASS。この依存DAGはOwner一括レビューで承認済み。各上流Gateのlatest canonical 999 PASSは実行時に別途検証する。Issue追跡は999の代替でない。

**科学的失敗モードと未決事項:** B0 complier LATEとB1 structural slopeを区別。HC1 AR集合をfinite gridだけで判定しない。

**対象外:** 既存Product科学ABIの変更、Web/API/DB/Worker新規統合、G01のPublisherやGraphVersionを別実装すること、他Gate MethodをScopeなしに追加すること、顧客配布許可、現時点での正本文書昇格。

## 2. Class/Module Ownership and Canonical Signatures

既存Classと新規Design Classの区別は現物Sourceで確認すること。`30_61/62/63`のClass placement、Constructor fields、Method signatureがAuthority。明記のないConcrete引数型を創作せず、設計欠落ならFreeze前に解決する。

| Class / Port | Designed module | Method signature / source | Reuse |
|---|---|---|---|
| `RddAdapter` | `ariadne.scientific.causal_methods.quasi.RddAdapter` | `preflight(self, request: ValidatedMethodRequest)` → `EligibilityOutcome`; `execute(self, request: ValidatedMethodRequest, *, sink: StagingArtifactSink)` → `TypedScientificOutcome` | 既存Scientific Kernel再利用／追加Adapterの責務 |
| `EstimatorPort` | `ariadne.scientific.ports.causal.EstimatorPort` | estimate(self, request:ValidatedEstimatorRequest, *, sink:StagingArtifactSink) -> EffectOutcome | 既存/新規の共通Value・Port・Facade参照。重複実装しない |
| `InferenceEvidence` | `ariadne.causal.inference.contracts.InferenceEvidence` | validate_for(mode,method) | 既存/新規の共通Value・Port・Facade参照。重複実装しない |
| `WaldRatioAdapter` | `ariadne.scientific.causal_methods.iv.WaldRatioAdapter` | `preflight(self, request: ValidatedMethodRequest)` → `EligibilityOutcome`; `execute(self, request: ValidatedMethodRequest, *, sink: StagingArtifactSink)` → `TypedScientificOutcome` | 既存Scientific Kernel再利用／追加Adapterの責務 |
| `IdentificationOutcome` | `ariadne.causal.identification.contracts.IdentificationOutcome` | from_evidence(evidence:ValidatedIdentificationEvidence) -> IdentificationOutcome | 既存/新規の共通Value・Port・Facade参照。重複実装しない |
| `EstimatorRequest` | `ariadne.causal.inference.contracts.EstimatorRequest` | validate_against(self, identification:IdentificationOutcome, design:CausalDesign, policy:EstimandEligibilityPolicy) -> ValidatedEstimatorRequest | 既存/新規の共通Value・Port・Facade参照。重複実装しない |
| `TwoSlsAdapter` | `ariadne.scientific.causal_methods.iv.TwoSlsAdapter` | `preflight(self, request: ValidatedMethodRequest)` → `EligibilityOutcome`; `execute(self, request: ValidatedMethodRequest, *, sink: StagingArtifactSink)` → `TypedScientificOutcome` | 既存Scientific Kernel再利用／追加Adapterの責務 |
| `ARConfidenceSet` | `ariadne.causal.inference.confidence_sets.ARConfidenceSet` | from_components(level,components,evidence) / contains(beta:float) / to_payload()/from_payload(payload) | 既存/新規の共通Value・Port・Facade参照。重複実装しない |
| `EffectOutcome` | `ariadne.causal.inference.contracts.EffectOutcome` | validate_consistency() / to_result_payload() | 既存/新規の共通Value・Port・Facade参照。重複実装しない |
| `LocalCausalUseCase` | `ariadne.capabilities.causal.local_execution.LocalCausalUseCase` | preflight(self,spec:ValidatedStudy,context:LocalRunContext)->PreflightReport / run(self,spec:ValidatedStudy,context:LocalRunContext)->LocalRunOutcome | 既存/新規の共通Value・Port・Facade参照。重複実装しない |

**Port dependency:** Local CLI Composition Root → ValidatedStudy/ContentRef → `LocalCausalUseCase` → MethodCapabilityPort/Scientific Ports/Privacy/Publication → Method Adapter → shared `ariadne.causal.*` / `ariadne.scientific.*` Kernel。DomainからCLI ConcreteやWeb/DBへ逆依存しない。既存Product `ScientificCorePort`はBridge経由で同じ科学Kernelに接続する。

## 3. Bounded Work Packages and DAG

| Package | Responsibility | Primary Classes / Ports | Methods | Depends on Pxx |
|---|---|---|---|---|
| P01 | rdd sharp fuzzy | RddAdapter / EstimatorPort,InferenceEvidence | P3-M07,P3-M08 | NONE |
| P02 | wald late | WaldRatioAdapter / IdentificationOutcome,EstimatorRequest | P3-M09 | NONE |
| P03 | two sls ar | TwoSlsAdapter / ARConfidenceSet,InferenceEvidence,EffectOutcome | P3-M10,P3-M11 | P02 |
| P04 | rdd iv result | — / LocalCausalUseCase,EffectOutcome,InferenceEvidence,ARConfidenceSet | cross-cutting | P01,P02,P03 |

全PxxのScopeとClass/Method ownershipは別文書`06_G08_Pxx_*.md`に自己完結記述。上流Packageからの利用はPort/Value/Bridgeであり、別Packageが所有するMethodを複製しない。Package setはOwnerが変更し得るため**DRAFT**。

## 4. Method Requirements, Eligibility, Positive/Negative Science

| Method / estimand | DD proof ID | Positive / Negative | Independent reference | AC | status from RD |
|---|---|---|---|---|---|
| `P3-M07` Sharp RDD／cutoff局所効果 | `DD-E11-METH-P307` | DGP-015; NEG-023 | REF-Q03 | AC-D03, AC-P01, AC-P03, AC-I01, AC-I02, AC-Q03 | PLAN:G08 / OWNER_ESTIMATOR_INFERENCE_POLICY_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED |
| `P3-M08` Fuzzy RDD／cutoff局所complier効果 | `DD-E11-METH-P308` | DGP-016; NEG-006, NEG-023 | REF-Q03, REF-I03 | AC-D03, AC-P01, AC-P03, AC-I01, AC-I02, AC-Q03 | PLAN:G08 / OWNER_ESTIMATOR_INFERENCE_POLICY_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED |
| `P3-M09` Wald ratio／binary Z/A complier LAT | `DD-E11-METH-P309` | DGP-006; NEG-006, NEG-007 | REF-I03, REF-E07 | AC-D03, AC-P01, AC-P03, AC-P05, AC-D07 | PLAN:G08 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P3-M10` B0 just-identified 2SLS／binary Z/A | `DD-E11-METH-P310` | DGP-006, DGP-024; NEG-006, NEG-025 | REF-E07, REF-U01 | AC-D03, AC-P01, AC-P03, AC-P05, AC-A01, AC-A02, AC-A03, AC-A04, AC-A05, AC-I01, AC-I02 | PLAN:G08 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P3-M11` B1-A／LINEAR_IV_STRUCTURAL_COEFFICIENT | `DD-E11-METH-P311` | DGP-007, DGP-024; NEG-008, NEG-025 | REF-E08, REF-U01 | AC-D03, AC-P01, AC-P03, AC-P05, AC-A01, AC-A02, AC-A03, AC-A04, AC-A05, AC-I01, AC-I02 | PLAN:G08 / OWNER_TARGET_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED |

**Reference rule:** MethodごとのDGP/NEG/REF/ACを必須とする。Backend自身の結果は独立Referenceではない。当該GateのRD 10_32でBLOCKEDまたはPENDINGのMethodがある場合開発都合でMethodを削除せず、識別対象/実装方法/独立Science TestをOwner決定へ戻す。科学的定量判定はOwner採用FWER=.05とMethod別PilotからのK/R/MC-SE/Resource/coverageを07に具体化してから実測する。


**Owner採用 OD-05（2026-11-19）：** G08の5 Methodについて、既決Target/数理は変更せず、担当Pxxでそれぞれstrict versioned `Method Config / Question / Design / Output / Inference Profile`を独立に定義・登録する。Method固有の確認項目は「Sharp/Fuzzy RD cutoff/bandwidth/kernel/order、B0/B1二値Z/A/C設計、全実数の弱IV頑健AR集合、独立科学審査待ちのHC1 χ²(1)反転候補（未Freeze）、推論/退化条件」。条件付き必須Field、Backend effective API/version/optional extras、positive/invalid-config/wrong-target/unsupported-CI/negative-science fixtureとtyped reasonを固定する。未登録/未検証は`METHOD_PROFILE_UNAVAILABLE`等でfail-closed。単なる`config={}`、Backend default、未生成DGP/REF、K/R/MC-SE未実測をPASSとしない。これはProfile作成の**担当配分採用**であり、個々のSchema/Inference/科学Referenceの完成・Freeze・Coding Authorizationを意味しない。

## 5. Global Scientific, I/O and Compatibility Constraints

- PREP-02の共通F03/F04/F05/F06/F07は適用基準。JCS RFC8785、Source/Graph/ContentRef/Manifestの異なるhash domain、atomic no-clobber、Trusted Root/independent privacy、typed scientific statusを損なわない。
- 旧Product `causal-analysis-spec/2`、`ScientificCorePort.run_*`、Web/API/Worker/DB、旧CLI、既存Refutation/Sensitivity `run`の公開ABIを変更しない。CLIだけの新Scientific Kernel、別MethodRegistry、別GraphVersion writer、別Publisherを作らない。
- Scientific `Identification/Point/Inference/ScienceAcceptance`とTechnical outcomeは別軸。不適格なMethod、無識別、Unsupported CI、missing optional Backendは型付き負結果またはTechnical error。未実行をPASS、point-onlyをCI有り、Backend自身の出力を独立Oracleにしない。
- `LocalCausalUseCase`はstrict ValidatedStudyから各Portへ委譲し、Fileはstaging→atomic Publisher→independent readback。G05のPolicy認可前は個票禁止。

**このGate固有の実装判断:** B0 complier LATEとB1 structural slopeを区別。HC1 AR集合をfinite gridだけで判定しない。各PxxのPositive/NegativeとBackend/Inference/Estimand/Statusを実行前にSchema/Registryで照合する。

## 6. Gate Coding-side Verification and Candidate Assembly

- 各PxxはMethod/DGP/NEG/REF/DD、Class.Method signature、typed Status、Backend effective API/optional Dependency、必要な実OS/CLI、既存Product invariantをFocused Testで確認。物理Path/Commandは40 Operatorがcurrent checkoutをdiscover/collectする。
- 新Testは原則`tests/enhancement/enh_e11/g08/<layer>/`、layer=unit/contract/integration（ENH-E11はCLI-only）。もし現行ProductのFrontend/Browser Regressionがaffectedならその既存Suiteも現物から検証する。科学的真偽をDir名やmockのみで推定しない。
- 全required PxxがCheckpoint SHAとStatus Reportを残してからCandidate Assembly。Gate-wide self-verification後に**1つのFixed Trial Candidate SHA**を確定、別途Freezeされた07による独立Test Item/999を実行する。
- Test-side defectはBLOCKEDとしIndependent Test Agentはtest/productionを修理しない。G10の最終統合は各Gateの独立999を置換しない。

## 7. Freeze前のReview/Stop条件

1. OwnerがGate依存・Acceptance Boundary・WORK_PACKAGE/Pxx順序を採否する。
2. `10_32`のMethod config、Estimand、DGP、NEG、Reference、実効Backend/API/Inferenceの適格性を検証する。特に本Gateの未決事項 B0 complier LATEとB1 structural slopeを区別。HC1 AR集合をfinite gridだけで判定しない。
3. 06/PxxのClass.Field/Constructor/Signature/Result authorityと既存Source、共有Port/Bridgeを整合させ、必要な設計欠落を閉じる。
4. **既存Gate07 DRAFTを本06/Pxxと照合・修正し**、Method別AC/独立科学閾値・負例・固定Fixture/Runtime・No PASS条件を確定して06/07をともにFreezeする。
5. Baseline full SHA、上流canonical 999、Runtime/Lock/License preflight、Ownerの明示Coding Authorizationが揃うまで`CODING_NOT_AUTHORIZED`。不足時は`BLOCKED_CONTRACT_AMBIGUITY`。

**本Commitには実装変更・試験実行・Owner Freeze・Coding Authorization・Gate 999判定を含めない。**


## PREP-04.1 Method ownership matrix (DRAFT)
- P3-M07 Pxx P01 ESTIMATE/10_32 semantic target (not assigned canonical enum) Config(bandwidth, polynomial_order, kernel_spec_ref, cutoff), Design(running_variable, outcome, treatment, cutoff, continuity_assumption_ref, density_check_ref), DGP-015; NEG-023; REF-Q03; backend/Science not verified.
- P3-M08 Pxx P01 ESTIMATE/10_32 semantic target (not assigned canonical enum) Config(bandwidth, polynomial_order, kernel_spec_ref, cutoff, first_stage_diagnostic_ref), Design(running_variable, outcome, treatment, cutoff, local_iv_assumptions_ref, first_stage_evidence_ref), DGP-016; NEG-006, NEG-023; REF-Q03, REF-I03; backend/Science not verified.
- P3-M09 Pxx P02 ESTIMATE/LATE_COMPLIER Config(design_profile, first_stage_diagnostic_ref, variance_spec_ref), Design(instrument, treatment, outcome, instrument_binary, treatment_binary, adjustment_columns, iv_assumptions_ref), DGP-006; NEG-006, NEG-007; REF-I03, REF-E07; backend/Science not verified.
- P3-M10 Pxx P03 ESTIMATE/LATE_COMPLIER Config(design_profile, first_stage_diagnostic_ref, ar_statistic_spec_ref, covariance_spec_ref), Design(instrument, treatment, outcome, instrument_binary, treatment_binary, adjustment_columns, iv_assumptions_ref), DGP-006, DGP-024; NEG-006, NEG-025; REF-E07, REF-U01; backend/Science not verified.
- P3-M11 Pxx P03 ESTIMATE/LINEAR_IV_STRUCTURAL_COEFFICIENT Config(design_profile, first_stage_diagnostic_ref, ar_statistic_spec_ref, covariance_spec_ref), Design(instrument, treatment, outcome, instrument_binary, treatment_binary, controls, iv_assumptions_ref), DGP-007, DGP-024; NEG-008, NEG-025; REF-E08, REF-U01; backend/Science not verified.

## S02・DEC-S05-AR01：G08 Method ProfileとAR Authorityの正規境界

担当Methodは`P3-M07` Sharp RDD、`P3-M08` Fuzzy RDD、`P3-M09` Binary Wald、`P3-M10` B0 2SLS、`P3-M11` B1 2SLSの5件。`23_api_interface_design/schema_drafts/method_profiles/factored/e11_<kind>_factored_v1.json`の5 Profile Kind（method_config/question_profile/design_profile/output_profile/inference_profile）をshared core＋exact Method ID overlayへ再構成し、Dispatch Registry、200 Schema標準Draft202012/Blob SHA/正負例の検証なしには`METHOD_PROFILE_UNAVAILABLE`。Method別EstimandとInferenceを保つ。B0は二値Z/A・無調整complier LATE、B1は事前Cを含む構造的`LINEAR_IV_STRUCTURAL_COEFFICIENT`、Fuzzy RDはcutoff局所complier効果であり、名称だけでATE/ATT/CATEへのcast不可。

**DEC-S05-AR01（Owner A採用）**：全実数領域での弱IV robust Anderson–Rubin信頼集合（bounded/unbounded/disconnected/ALL_REAL、退化・EMPTY等の明示判定）は既承認必須。HC1 OLS係数＋χ²(1)漸近検定＋二次式反転という**具体的計算法は独立科学Reviewerの妥当性確認前の実装候補でありFreezeしていない**。本Pxx/06/07に既存のHC1記述があっても、Ownerがそれを最終承認したと解釈しない。レビュー済み数理導出、全実数位相/弱IV/zero first-stage/分散退化/coverage、独立Oracle/実効Backend、T2-T3事前登録とOwnerによる契約確定がない場合、G08の当該方法は`BLOCKED_SCIENCE_METHOD_NOT_FROZEN`でGate999 PASS禁止。Point estimatorの可用性からAR可用性を推論しない。P3-M09 WaldにはARが自動付帯しない。

共通`LocalRunContext(root,principal)`、`LocalPrivacyPolicyPort.authorize(*,study,root,principal,output_shape)`。署名Verifier/Policy Anchor・CLI row flag・Study `policy_ref`なし。G08は個票を公開しない。共通Scientific Kernelと既存Product v2を保護する。G10では41 Method全件の有効Science証拠が必要だが、推移的依存閉包のSHAが完全不変なら証拠再利用を認め、変更/不明分のみ再実行/BLOCK。
