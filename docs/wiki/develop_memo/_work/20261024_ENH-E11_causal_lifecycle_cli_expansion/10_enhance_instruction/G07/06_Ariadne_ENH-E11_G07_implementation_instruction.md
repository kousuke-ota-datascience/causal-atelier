# Ariadne ENH-E11 / G07 — 06 実装指示書

**Document class:** Gate Coding Contract — Reviewer DRAFT  
**Gate:** G07 — 正式Enhance Workflow Gate  
**Contract status:** DRAFT / NOT_FROZEN / CODING_NOT_AUTHORIZED  
**Depends on:** G01 PASS, G02 PASS （Owner一括レビュー承認済み・未Freeze）  
**Execution mode:** WORK_PACKAGE （Owner一括レビュー承認済み・未Freeze）  
**Required packages:** P01,P02,P03 （Owner一括レビュー承認済み・未Freeze）  
**Trial:** NOT_STARTED  
**Gate07:** [07独立テスト指示書案](07_Ariadne_ENH-E11_G07_test_instruction.md) — DRAFT / NOT_FROZEN / TESTS_NOT_RUN（Owner一括レビュー承認済み・ただしOpen Decision残存、未Freeze）。  
**Baseline SHA:** 未固定（Coding Authorization時に取得）。  
**Authority/reference:** [Gate decomposition](../../40_operator_workflows/architecture_review/03_gate_decomposition.md)／[PREP-02 freeze](../../00_enhance_background/Revised_requirements_definition_documents/combined_review/117_20261117_prep02_common_contract_baseline_freeze.md)／[RD 10_32](../../00_enhance_background/Revised_requirements_definition_documents/10_requirements_definition/10_32_scientific_method_scope.md)／[DD 30_61](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_61_causal_domain_ports.md)／[DD 30_62](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_62_local_execution_publication.md)／[DD 30_63](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_63_causal_method_adapters.md)／[IF 23_41](../../00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design/23_41_cli_scientific_ports.md)／[IF 23_42](../../00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design/23_42_local_result_manifest_artifact.md)

**Owner review record:** 2026-11-18 JST、PREP-03 Final Auditの静的レビュー、G07のGate DAG・WORK_PACKAGE mode・Required packagesをOwner承認。06/07/Pxxの実装・科学的未決を補完して承認したものではない。NOT_FROZEN / CODING_NOT_AUTHORIZED / TESTS_NOT_RUNを維持。参照：[`PREP03_final_audit.md`](../PREP03_final_audit.md) §6。

## 0. Contract Boundary and PREP-03 Status

Gateの06は実装WHAT、07は独立Verification WHAT、40 Operatorは物理Test配置・実行HOW、999は唯一の正式Gate Verdict。P00はPlan、Pxxはbounded Coding Unitであり、Pxx/06の作成はGate PASS、Coding Authorization、Method Science PASS、07 Freezeを意味しない。

PREP-02のCommon Design BaselineはFreeze済み。**Gate Dependency/WORK_PACKAGE/Required Packagesの構成はOwner一括レビュー承認済み。ただし本Gate固有の未決Method config、実効Backend、独立Science Oracle、06/07/Pxxは引き続きDRAFT・NOT_FROZENで、実装開始不可。** 本文内の`Gxx PASS`は現在達成された状態ではない。

## 1. Gate Acceptance Claim and Scope

**受入命題:** DiD/Event/ITSをtiming・pretrend・cluster・serial correlation条件付きで実行する。

**候補依存:** `G01`・`G02`のlatest canonical 999 PASS。この依存DAGはOwner一括レビューで承認済み。各上流Gateのlatest canonical 999 PASSは実行時に別途検証する。Issue追跡は999の代替でない。

**科学的失敗モードと未決事項:** 2x2とstaggered DiDを同一TWFE ATTへ還元せず、ITSにiid SEを無検証適用しない。

**対象外:** 既存Product科学ABIの変更、Web/API/DB/Worker新規統合、G01のPublisherやGraphVersionを別実装すること、他Gate MethodをScopeなしに追加すること、顧客配布許可、現時点での正本文書昇格。

## 2. Class/Module Ownership and Canonical Signatures

既存Classと新規Design Classの区別は現物Sourceで確認すること。`30_61/62/63`のClass placement、Constructor fields、Method signatureがAuthority。明記のないConcrete引数型を創作せず、設計欠落ならFreeze前に解決する。

| Class / Port | Designed module | Method signature / source | Reuse |
|---|---|---|---|
| `PanelQuasiAdapter` | `ariadne.scientific.causal_methods.quasi.PanelQuasiAdapter` | `preflight(self, request: ValidatedMethodRequest)` → `EligibilityOutcome`; `execute(self, request: ValidatedMethodRequest, *, sink: StagingArtifactSink)` → `TypedScientificOutcome` | 既存Scientific Kernel再利用／追加Adapterの責務 |
| `EstimatorPort` | `ariadne.scientific.ports.causal.EstimatorPort` | estimate(self, request:ValidatedEstimatorRequest, *, sink:StagingArtifactSink) -> EffectOutcome | 既存/新規の共通Value・Port・Facade参照。重複実装しない |
| `EstimatorRequest` | `ariadne.causal.inference.contracts.EstimatorRequest` | validate_against(self, identification:IdentificationOutcome, design:CausalDesign, policy:EstimandEligibilityPolicy) -> ValidatedEstimatorRequest | 既存/新規の共通Value・Port・Facade参照。重複実装しない |
| `InterruptedTsAdapter` | `ariadne.scientific.causal_methods.quasi.InterruptedTsAdapter` | `preflight(self, request: ValidatedMethodRequest)` → `EligibilityOutcome`; `execute(self, request: ValidatedMethodRequest, *, sink: StagingArtifactSink)` → `TypedScientificOutcome` | 既存Scientific Kernel再利用／追加Adapterの責務 |
| `InferenceEvidence` | `ariadne.causal.inference.contracts.InferenceEvidence` | validate_for(mode,method) | 既存/新規の共通Value・Port・Facade参照。重複実装しない |
| `LocalCausalUseCase` | `ariadne.capabilities.causal.local_execution.LocalCausalUseCase` | preflight(self,spec:ValidatedStudy,context:LocalRunContext)->PreflightReport / run(self,spec:ValidatedStudy,context:LocalRunContext)->LocalRunOutcome | 既存/新規の共通Value・Port・Facade参照。重複実装しない |
| `EffectOutcome` | `ariadne.causal.inference.contracts.EffectOutcome` | validate_consistency() / to_result_payload() | 既存/新規の共通Value・Port・Facade参照。重複実装しない |

**Port dependency:** Local CLI Composition Root → ValidatedStudy/ContentRef → `LocalCausalUseCase` → MethodCapabilityPort/Scientific Ports/Privacy/Publication → Method Adapter → shared `ariadne.causal.*` / `ariadne.scientific.*` Kernel。DomainからCLI ConcreteやWeb/DBへ逆依存しない。既存Product `ScientificCorePort`はBridge経由で同じ科学Kernelに接続する。

## 3. Bounded Work Packages and DAG

| Package | Responsibility | Primary Classes / Ports | Methods | Depends on Pxx |
|---|---|---|---|---|
| P01 | did event | PanelQuasiAdapter / EstimatorPort,EstimatorRequest | P3-M04,P3-M05 | NONE |
| P02 | interrupted ts | InterruptedTsAdapter / EstimatorPort,InferenceEvidence | P3-M06 | NONE |
| P03 | quasi integration | — / LocalCausalUseCase,EffectOutcome,InferenceEvidence | cross-cutting | P01,P02 |

全PxxのScopeとClass/Method ownershipは別文書`06_G07_Pxx_*.md`に自己完結記述。上流Packageからの利用はPort/Value/Bridgeであり、別Packageが所有するMethodを複製しない。Package setはOwnerが変更し得るため**DRAFT**。

## 4. Method Requirements, Eligibility, Positive/Negative Science

| Method / estimand | DD proof ID | Positive / Negative | Independent reference | AC | status from RD |
|---|---|---|---|---|---|
| `P3-M04` DiD／ATT（2×2とstaggeredは別契約） | `DD-E11-METH-P304` | DGP-012, DGP-013; NEG-022 | REF-Q01 | AC-D03, AC-P01, AC-P03, AC-I01, AC-I02, AC-Q01 | PLAN:G07 / OWNER_ESTIMATOR_INFERENCE_POLICY_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED |
| `P3-M05` Event Study／event-time効果 | `DD-E11-METH-P305` | DGP-013; NEG-022 | REF-Q01 | AC-D03, AC-P01, AC-P03, AC-I01, AC-I02, AC-Q01 | PLAN:G07 / OWNER_ESTIMATOR_INFERENCE_POLICY_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED |
| `P3-M06` Interrupted Time Series／介入時点のlevel | `DD-E11-METH-P306` | DGP-014; NEG-023 | REF-Q02 | AC-D03, AC-P01, AC-P03, AC-I01, AC-I02, AC-Q02 | PLAN:G07 / OWNER_ESTIMATOR_INFERENCE_POLICY_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED |

**Reference rule:** MethodごとのDGP/NEG/REF/ACを必須とする。Backend自身の結果は独立Referenceではない。当該GateのRD 10_32でBLOCKEDまたはPENDINGのMethodがある場合開発都合でMethodを削除せず、識別対象/実装方法/独立Science TestをOwner決定へ戻す。科学的定量判定はOwner採用FWER=.05とMethod別PilotからのK/R/MC-SE/Resource/coverageを07に具体化してから実測する。


**Owner採用 OD-05（2026-11-19）：** G07の3 Methodについて、既決Target/数理は変更せず、担当Pxxでそれぞれstrict versioned `Method Config / Question / Design / Output / Inference Profile`を独立に定義・登録する。Method固有の確認項目は「DiD 2x2 vs staggered ATT、event-time reference cohort/period、cluster covariance、ITS介入時点のlevel/slope/HAC/serial dependence」。条件付き必須Field、Backend effective API/version/optional extras、positive/invalid-config/wrong-target/unsupported-CI/negative-science fixtureとtyped reasonを固定する。未登録/未検証は`METHOD_PROFILE_UNAVAILABLE`等でfail-closed。単なる`config={}`、Backend default、未生成DGP/REF、K/R/MC-SE未実測をPASSとしない。これはProfile作成の**担当配分採用**であり、個々のSchema/Inference/科学Referenceの完成・Freeze・Coding Authorizationを意味しない。

## 5. Global Scientific, I/O and Compatibility Constraints

- PREP-02の共通F03/F04/F05/F06/F07は適用基準。JCS RFC8785、Source/Graph/ContentRef/Manifestの異なるhash domain、atomic no-clobber、Trusted Root/independent privacy、typed scientific statusを損なわない。
- 旧Product `causal-analysis-spec/2`、`ScientificCorePort.run_*`、Web/API/Worker/DB、旧CLI、既存Refutation/Sensitivity `run`の公開ABIを変更しない。CLIだけの新Scientific Kernel、別MethodRegistry、別GraphVersion writer、別Publisherを作らない。
- Scientific `Identification/Point/Inference/ScienceAcceptance`とTechnical outcomeは別軸。不適格なMethod、無識別、Unsupported CI、missing optional Backendは型付き負結果またはTechnical error。未実行をPASS、point-onlyをCI有り、Backend自身の出力を独立Oracleにしない。
- `LocalCausalUseCase`はstrict ValidatedStudyから各Portへ委譲し、Fileはstaging→atomic Publisher→independent readback。G05のPolicy認可前は個票禁止。

**このGate固有の実装判断:** 2x2とstaggered DiDを同一TWFE ATTへ還元せず、ITSにiid SEを無検証適用しない。各PxxのPositive/NegativeとBackend/Inference/Estimand/Statusを実行前にSchema/Registryで照合する。

## 6. Gate Coding-side Verification and Candidate Assembly

- 各PxxはMethod/DGP/NEG/REF/DD、Class.Method signature、typed Status、Backend effective API/optional Dependency、必要な実OS/CLI、既存Product invariantをFocused Testで確認。物理Path/Commandは40 Operatorがcurrent checkoutをdiscover/collectする。
- 新Testは原則`tests/enhancement/enh_e11/g07/<layer>/`、layer=unit/contract/integration（ENH-E11はCLI-only）。もし現行ProductのFrontend/Browser Regressionがaffectedならその既存Suiteも現物から検証する。科学的真偽をDir名やmockのみで推定しない。
- 全required PxxがCheckpoint SHAとStatus Reportを残してからCandidate Assembly。Gate-wide self-verification後に**1つのFixed Trial Candidate SHA**を確定、別途Freezeされた07による独立Test Item/999を実行する。
- Test-side defectはBLOCKEDとしIndependent Test Agentはtest/productionを修理しない。G10の最終統合は各Gateの独立999を置換しない。

## 7. Freeze前のReview/Stop条件

1. OwnerがGate依存・Acceptance Boundary・WORK_PACKAGE/Pxx順序を採否する。
2. `10_32`のMethod config、Estimand、DGP、NEG、Reference、実効Backend/API/Inferenceの適格性を検証する。特に本Gateの未決事項 2x2とstaggered DiDを同一TWFE ATTへ還元せず、ITSにiid SEを無検証適用しない。
3. 06/PxxのClass.Field/Constructor/Signature/Result authorityと既存Source、共有Port/Bridgeを整合させ、必要な設計欠落を閉じる。
4. **既存Gate07 DRAFTを本06/Pxxと照合・修正し**、Method別AC/独立科学閾値・負例・固定Fixture/Runtime・No PASS条件を確定して06/07をともにFreezeする。
5. Baseline full SHA、上流canonical 999、Runtime/Lock/License preflight、Ownerの明示Coding Authorizationが揃うまで`CODING_NOT_AUTHORIZED`。不足時は`BLOCKED_CONTRACT_AMBIGUITY`。

**本Commitには実装変更・試験実行・Owner Freeze・Coding Authorization・Gate 999判定を含めない。**


## PREP-04.1 Method ownership matrix (DRAFT)
- P3-M04 Pxx P01 ESTIMATE/ATT Config(design_variant, estimator_spec_ref, cluster_covariance_spec_ref), Design(unit_id, time_id, treatment, outcome, parallel_trends_assumption_ref), DGP-012, DGP-013; NEG-022; REF-Q01; backend/Science not verified.
- P3-M05 Pxx P01 ESTIMATE/10_32 semantic target (not assigned canonical enum) Config(event_window_start, event_window_end, reference_event_time, cohort_estimator_spec_ref, cluster_covariance_spec_ref), Design(unit_id, time_id, treatment, outcome, cohort_id, pretrend_assumption_ref), DGP-013; NEG-022; REF-Q01; backend/Science not verified.
- P3-M06 Pxx P02 ESTIMATE/10_32 semantic target (not assigned canonical enum) Config(effect_components, trend_spec_ref, serial_covariance_spec_ref), Design(time_index, outcome, intervention_time, seasonality_spec_ref, autocorrelation_evidence_ref), DGP-014; NEG-023; REF-Q02; backend/Science not verified.

## S02簡素化・G07 Quasi Method/Vector Outputの規範

担当Methodは`P3-M04` DiD、`P3-M05` Event Study、`P3-M06` ITSの3件。`23_api_interface_design/schema_drafts/method_profiles/factored/e11_<kind>_factored_v1.json`の5 kind（method_config/question_profile/design_profile/output_profile/inference_profile）からshared＋Method overlayを単一strict Schemaとして再構築し、Dispatch Registry、Blob SHA/標準Draft202012/parity/Method別正負例の証拠がなければ`METHOD_PROFILE_UNAVAILABLE`。DiDの2x2/staggered、Event Studyのcohort/time/reference period、ITSのlevel/slope/HAC/autocorrelationを混同しない。P3-M05ではscalar `result.json`のpointを`NOT_AVAILABLE`とし、cohort×event-timeのtyped `event_time_effects.json`と独立Manifest/ContentRefを発行。推論は実Method/Backendで対応が証明された場合のみAVAILABLE、指定period前のpretrend/介入時点負例とCI shape/Graph・Study lineageを独立07で検証する。

Contextは`LocalRunContext(root,principal)`、Privacy Portは`authorize(*,study,root,principal,output_shape)`。署名Verifier/Policy Anchor・`cli_row_flag`・Study `policy_ref`・追加CLI opt-inを設けない。個票はG05だけがStudy `row_export_requested=true`と非root同一UID private ext4/XFS/Method別capsをANDしてG01 Sinkへ。旧Product v2と共通KernelのABIを保護、科学Oracleと実Backend/CIを未実行ならScience BLOCKED。全Product Suite無条件実行ではなく影響閉包で回帰を決定、不明なら実行またはBLOCK。

## S09 documented Event Study vector contract — P3-M05 (2026-11-22)

P3-M05 `ESTIMATE` has an **event-time/cohort effect vector**, not a scalar target. For an eligible Event Study run, `result.json` has nested `point.availability=NOT_AVAILABLE`, `point.value=null`, `point.reason.code=NON_SCALAR_TARGET`, while `status.json` has top-level `point_availability=NOT_AVAILABLE`; the Manifest must inventory `event_time_effects.json` conforming to `schema_drafts/internal_scientific/e11_event_time_effects_draft1.schema.json`. It binds `method_id=P3-M05`, `study_ref`, `reference_period`, `time_unit`, cohort/event-time keyed `effects`, inference availability/interval references and `pretrend_diagnostics_ref`. The designated reference period and cohort/time support must be predeclared; unique event-time/cohort keys, finite effects, no invalid pretrend concealment, and exact readback/hash/lineage are required. Do not synthesize a scalar ATT/ATE from the vector or substitute an AR confidence set. Other Methods (DiD/ITS) retain their distinct output/inference contracts.

**Gate 06:** P01 implements Method-specific event-time evaluation and references; P03 owns Bundle/Result/Manifest consistency with G01 Sink/Reader. No unscoped Method or new public wire version.

## S09-R12 P3-M06 ITS conditional component payload contract (2026-11-22; DRAFT)

P3-M06 Output: P3-M06 Method Config `effect_components` is `LEVEL` or `LEVEL_AND_SLOPE` (no implicit default). All technically completed eligible ESTIMATE runs publish both `result.json` and a typed `its_components.json` (`schema_drafts/internal_scientific/e11_its_components_draft1.schema.json`) through G01 Sink/Manifest/Marker/Reader. `LEVEL`: scalar Result `point.availability=AVAILABLE`, `point.value=β_L` at declared intervention t0, with sidecar `level` only, `slope=null` and no post-horizon effects. `LEVEL_AND_SLOPE`: result has `point.availability=NOT_AVAILABLE`, `point.value=null`, `point.reason.code=NON_SCALAR_TARGET`, while sidecar contains β_L, β_S and only predeclared post-horizon `τ(t0+h)=β_L+β_S h` values; if no predeclared horizon exists, do not invent one. `status.json` separately has top-level `point_availability` matching Result. Require non-row-only `observed_rows_included=false`, unique integer `h`, finite estimates, declared intervention date, Method/Study/Design references and immutable source hashes. Do not treat marginal component CIs as joint simultaneous coverage, invent covariance, or mark HAC/NW inference AVAILABLE before method-specific validity and independently validated science. If requested confirmatory inference is not valid, use typed unsupported/unavailable rather than fabricated interval. The common public Result Schema is unchanged; all additional output is a versioned internal artifact, not a Product API/DB migration.

**Package boundary:** Gate06 requires P02 scientific component production and P03 common bundle integration; P01 DiD/Event Study does not own ITS numerical code.
