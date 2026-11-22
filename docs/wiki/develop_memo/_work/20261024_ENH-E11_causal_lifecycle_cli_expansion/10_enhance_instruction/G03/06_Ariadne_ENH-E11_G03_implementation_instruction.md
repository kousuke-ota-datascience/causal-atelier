# Ariadne ENH-E11 / G03 — 06 実装指示書

**DEC-PREPCODE-01=B（Owner 2026-11-22採用）：Gate別S09→S10→S11。** G03の独立S09監査は、先行Gate（G02）と共通E11 Wire/Port/Privacy/JCS/Publisher/Reader/Protected v2の変更影響閉包、およびG03自身の06/P00/Pxx/07/Method Profile/Backend/Scienceを対象とする。対象外Gateは全体SHA inventoryに保持し`NOT_REVIEWED`、未決の後続MethodはG03のCoding前無条件停止条件にしない。G03固有の独立S09 verdict→Owner G03-S10 Freeze→Owner G03-S11 Coding Authorizationを別々に取得する。**S11実行前にはG02_999の実PASSが必須**だが、S09文書監査の準備は先行Gateの実装中にも可能。実Adapter/FS/数値T2/T3/RegressionはG03の独立07/999で検証し、文書修正だけでPASSを付けない。現時点は`S09_NOT_RUN/S10_NOT_FROZEN/S11_NOT_AUTHORIZED`。

**Document class:** Gate Coding Contract — Reviewer DRAFT  
**Gate:** G03 — 正式Enhance Workflow Gate  
**Contract status:** DRAFT / NOT_FROZEN / CODING_NOT_AUTHORIZED  
**Depends on:** G02 PASS （Owner一括レビュー承認済み・未Freeze）  
**Execution mode:** WORK_PACKAGE （Owner一括レビュー承認済み・未Freeze）  
**Required packages:** P01,P02,P03,P04,P05,P06 （Owner一括レビュー承認済み・未Freeze）  
**Trial:** NOT_STARTED  
**Gate07:** [07独立テスト指示書案](07_Ariadne_ENH-E11_G03_test_instruction.md) — DRAFT / NOT_FROZEN / TESTS_NOT_RUN（Owner一括レビュー承認済み・ただしOpen Decision残存、未Freeze）。  
**Baseline SHA:** 未固定（Coding Authorization時に取得）。  
**Authority/reference:** [Gate decomposition](../../40_operator_workflows/architecture_review/03_gate_decomposition.md)／[PREP-02 freeze](../../00_enhance_background/Revised_requirements_definition_documents/combined_review/117_20261117_prep02_common_contract_baseline_freeze.md)／[RD 10_32](../../00_enhance_background/Revised_requirements_definition_documents/10_requirements_definition/10_32_scientific_method_scope.md)／[DD 30_61](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_61_causal_domain_ports.md)／[DD 30_62](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_62_local_execution_publication.md)／[DD 30_63](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_63_causal_method_adapters.md)／[IF 23_41](../../00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design/23_41_cli_scientific_ports.md)／[IF 23_42](../../00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design/23_42_local_result_manifest_artifact.md)

**Owner review record:** 2026-11-18 JST、PREP-03 Final Auditの静的レビュー、G03のGate DAG・WORK_PACKAGE mode・Required packagesをOwner承認。06/07/Pxxの実装・科学的未決を補完して承認したものではない。NOT_FROZEN / CODING_NOT_AUTHORIZED / TESTS_NOT_RUNを維持。参照：[`PREP03_final_audit.md`](../PREP03_final_audit.md) §6。

## 0. Contract Boundary and PREP-03 Status

Gateの06は実装WHAT、07は独立Verification WHAT、40 Operatorは物理Test配置・実行HOW、999は唯一の正式Gate Verdict。P00はPlan、Pxxはbounded Coding Unitであり、Pxx/06の作成はGate PASS、Coding Authorization、Method Science PASS、07 Freezeを意味しない。

PREP-02のCommon Design BaselineはFreeze済み。**Gate Dependency/WORK_PACKAGE/Required Packagesの構成はOwner一括レビュー承認済み。ただし本Gate固有の未決Method config、実効Backend、独立Science Oracle、06/07/Pxxは引き続きDRAFT・NOT_FROZENで、実装開始不可。** 本文内の`Gxx PASS`は現在達成された状態ではない。

## 1. Gate Acceptance Claim and Scope

**受入命題:** Native推定と4 Refutation・2 Sensitivity・NCE/NCO/RVをEffect lineage付きで実行する。

**候補依存:** `G02`のlatest canonical 999 PASS。この依存DAGはOwner一括レビューで承認済み。各上流Gateのlatest canonical 999 PASSは実行時に別途検証する。Issue追跡は999の代替でない。

**科学的失敗モードと未決事項:** 非有意NCE/NCOは無交絡証明ではない。RVは古典OLS限定。P1-M11のScience未確定を黙認しない。

**対象外:** 既存Product科学ABIの変更、Web/API/DB/Worker新規統合、G01のPublisherやGraphVersionを別実装すること、他Gate MethodをScopeなしに追加すること、顧客配布許可、現時点での正本文書昇格。

## 2. Class/Module Ownership and Canonical Signatures

既存Classと新規Design Classの区別は現物Sourceで確認すること。`30_61/62/63`のClass placement、Constructor fields、Method signatureがAuthority。明記のないConcrete引数型を創作せず、設計欠落ならFreeze前に解決する。

| Class / Port | Designed module | Method signature / source | Reuse |
|---|---|---|---|
| `NativeEffectAdapter` | `ariadne.scientific.causal_methods.estimation.NativeEffectAdapter` | `preflight(self, request: ValidatedMethodRequest)` → `EligibilityOutcome`; `execute(self, request: ValidatedMethodRequest, *, sink: StagingArtifactSink)` → `TypedScientificOutcome` | 既存Scientific Kernel再利用／追加Adapterの責務 |
| `EstimatorPort` | `ariadne.scientific.ports.causal.EstimatorPort` | estimate(self, request:ValidatedEstimatorRequest, *, sink:StagingArtifactSink) -> EffectOutcome | 既存/新規の共通Value・Port・Facade参照。重複実装しない |
| `EffectOutcome` | `ariadne.causal.inference.contracts.EffectOutcome` | validate_consistency() / to_result_payload() | 既存/新規の共通Value・Port・Facade参照。重複実装しない |
| `WeightingEffectAdapter` | `ariadne.scientific.causal_methods.estimation.WeightingEffectAdapter` | `preflight(self, request: ValidatedMethodRequest)` → `EligibilityOutcome`; `execute(self, request: ValidatedMethodRequest, *, sink: StagingArtifactSink)` → `TypedScientificOutcome` | 既存Scientific Kernel再利用／追加Adapterの責務 |
| `InferenceEvidence` | `ariadne.causal.inference.contracts.InferenceEvidence` | validate_for(mode,method) | 既存/新規の共通Value・Port・Facade参照。重複実装しない |
| `RefutationAdapter` | `ariadne.scientific.refutation.adapter.RefutationAdapter` | `run(self, input_: RefutationInput, output_dir: Path)` → `list[ScientificResultDescriptor]` | 既存公開API不変・Typed Bridgeを介して再利用 |
| `DiagnosticPort` | `ariadne.scientific.ports.causal.DiagnosticPort` | run(self, request:ValidatedDiagnosticRequest, *, sink:StagingArtifactSink) -> DiagnosticOutcome | 既存/新規の共通Value・Port・Facade参照。重複実装しない |
| `SensitivityAdapter` | `ariadne.scientific.sensitivity.adapter.SensitivityAdapter` | `run(self, input_: SensitivityInput, output_dir: Path)` → `list[ScientificResultDescriptor]` | 既存公開API不変・Typed Bridgeを介して再利用 |
| `ObservedNceAdapter` | `ariadne.scientific.causal_methods.negative_controls.ObservedNceAdapter` | `preflight(self, request: ValidatedMethodRequest)` → `EligibilityOutcome`; `execute(self, request: ValidatedMethodRequest, *, sink: StagingArtifactSink)` → `TypedScientificOutcome` | 既存Scientific Kernel再利用／追加Adapterの責務 |
| `ObservedNcoAdapter` | `ariadne.scientific.causal_methods.negative_controls.ObservedNcoAdapter` | `preflight(self, request: ValidatedMethodRequest)` → `EligibilityOutcome`; `execute(self, request: ValidatedMethodRequest, *, sink: StagingArtifactSink)` → `TypedScientificOutcome` | 既存Scientific Kernel再利用／追加Adapterの責務 |
| `OlsRvAdapter` | `ariadne.scientific.causal_methods.sensitivity.OlsRvAdapter` | `preflight(self, request: ValidatedMethodRequest)` → `EligibilityOutcome`; `execute(self, request: ValidatedMethodRequest, *, sink: StagingArtifactSink)` → `TypedScientificOutcome` | 既存Scientific Kernel再利用／追加Adapterの責務 |
| `LocalCausalUseCase` | `ariadne.capabilities.causal.local_execution.LocalCausalUseCase` | preflight(self,spec:ValidatedStudy,context:LocalRunContext)->PreflightReport / run(self,spec:ValidatedStudy,context:LocalRunContext)->LocalRunOutcome | 既存/新規の共通Value・Port・Facade参照。重複実装しない |
| `LocalRunManifest` | `ariadne.interfaces.cli.local_causal.manifest.LocalRunManifest` | to_canonical_bytes() | 既存/新規の共通Value・Port・Facade参照。重複実装しない |
| `LocalManifestReader` | `ariadne.interfaces.cli.local_causal.manifest_reader.LocalManifestReader` | read_run(trusted_root:TrustedLocalRoot,run_id:RunId) | 既存/新規の共通Value・Port・Facade参照。重複実装しない |

**Port dependency:** Local CLI Composition Root → ValidatedStudy/ContentRef → `LocalCausalUseCase` → MethodCapabilityPort/Scientific Ports/Privacy/Publication → Method Adapter → shared `ariadne.causal.*` / `ariadne.scientific.*` Kernel。DomainからCLI ConcreteやWeb/DBへ逆依存しない。既存Product `ScientificCorePort`はBridge経由で同じ科学Kernelに接続する。

## 3. Bounded Work Packages and DAG

| Package | Responsibility | Primary Classes / Ports | Methods | Depends on Pxx |
|---|---|---|---|---|
| P01 | native effects | NativeEffectAdapter / EstimatorPort,EffectOutcome | P1-M08,P1-M09 | NONE |
| P02 | weighting ipw aipw | WeightingEffectAdapter / EstimatorPort,InferenceEvidence | P1-M10,P1-M11 | P01 |
| P03 | refutation methods | RefutationAdapter / DiagnosticPort | P1-M12,P1-M13,P1-M14,P1-M15 | P01,P02 |
| P04 | sensitivity methods | SensitivityAdapter / DiagnosticPort | P1-M16,P1-M17 | P01,P02 |
| P05 | negative controls ols rv | ObservedNceAdapter,ObservedNcoAdapter,OlsRvAdapter / DiagnosticPort,InferenceEvidence | P1-M18,P1-M19,P1-M20 | P01 |
| P06 | diagnostics pipeline | — / LocalCausalUseCase,EffectOutcome,LocalRunManifest,LocalManifestReader | cross-cutting | P03,P04,P05 |

全PxxのScopeとClass/Method ownershipは別文書`06_G03_Pxx_*.md`に自己完結記述。上流Packageからの利用はPort/Value/Bridgeであり、別Packageが所有するMethodを複製しない。Package setはOwnerが変更し得るため**DRAFT**。

## 4. Method Requirements, Eligibility, Positive/Negative Science

| Method / estimand | DD proof ID | Positive / Negative | Independent reference | AC | status from RD |
|---|---|---|---|---|---|
| `P1-M08` Native diff-in-means／ATE | `DD-E11-METH-P108` | DGP-001, DGP-022; NEG-001, NEG-010 | REF-E01 | AC-D03, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02 | PLAN:G03 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P1-M09` Native OLS／採用済み契約範囲のATE/ATT表現 | `DD-E11-METH-P109` | DGP-002, DGP-003; NEG-002, NEG-008, NEG-020 | REF-E01, REF-I01 | AC-D03, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02 | PLAN:G03 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P1-M10` Native IPW／ATE・ATT（別fixture） | `DD-E11-METH-P110` | DGP-002, DGP-003; NEG-010, NEG-018 | REF-E02 | AC-D03, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-R05 | PLAN:G03 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P1-M11` Native AIPW／ATE・ATT（別fixture） | `DD-E11-METH-P111` | DGP-002, DGP-003; NEG-010, NEG-011, NEG-012 | REF-E03 | AC-D03, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02 | PLAN:G03 / BLOCKED / NOT_GENERATED |
| `P1-M12` Placebo Treatment refutation／null診 | `DD-E11-METH-P112` | DGP-022; NEG-014 | REF-R01 | AC-D01, AC-R01, AC-T01 | PLAN:G03 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P1-M13` Data Subset refutation／安定性 | `DD-E11-METH-P113` | DGP-001, DGP-002; NEG-015 | REF-R01 | AC-D01, AC-D03, AC-R02 | PLAN:G03 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P1-M14` Random Common Cause refutation／摂動安 | `DD-E11-METH-P114` | DGP-002; NEG-017 | REF-R01 | AC-D01, AC-D03, AC-R02 | PLAN:G03 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P1-M15` Bootstrap refutation／再標本化安定性 | `DD-E11-METH-P115` | DGP-001, DGP-002; NEG-016 | REF-R01 | AC-D01, AC-D03, AC-R02 | PLAN:G03 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P1-M16` Adjustment Set Sensitivity／設計変更 | `DD-E11-METH-P116` | DGP-021, DGP-002; NEG-002 | REF-G01, REF-R01 | AC-D01, AC-D02, AC-R02 | PLAN:G03 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P1-M17` Propensity Clipping Sensitivity／tr | `DD-E11-METH-P117` | DGP-002, DGP-023; NEG-010, NEG-018 | REF-E02, REF-R01 | AC-D03, AC-R05 | PLAN:G03 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P1-M18` Observed NCE null diagnostic／条件付き関 | `DD-E11-METH-P118` | DGP-019; NEG-019, NEG-026 | REF-R02 | AC-D01, AC-T01, AC-T02, AC-T03, AC-R03 | PLAN:G03 / OWNER_METHOD_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED |
| `P1-M19` Observed NCO null diagnostic／条件付き関 | `DD-E11-METH-P119` | DGP-019; NEG-019, NEG-026 | REF-R02 | AC-D01, AC-T01, AC-T02, AC-T03, AC-R03 | PLAN:G03 / OWNER_METHOD_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED |
| `P1-M20` OLS partial R² / RV sensitivity／指定 | `DD-E11-METH-P120` | DGP-020; NEG-020 | REF-R03 | AC-D01, AC-D03, AC-R04 | PLAN:G03 / OWNER_METHOD_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED |

**Reference rule:** MethodごとのDGP/NEG/REF/ACを必須とする。Backend自身の結果は独立Referenceではない。当該GateのRD 10_32でBLOCKEDまたはPENDINGのMethodがある場合開発都合でMethodを削除せず、識別対象/実装方法/独立Science TestをOwner決定へ戻す。科学的定量判定はOwner採用FWER=.05とMethod別PilotからのK/R/MC-SE/Resource/coverageを07に具体化してから実測する。


**Owner採用 OD-05（2026-11-19）：** G03の13 Methodについて、既決Target/数理は変更せず、担当Pxxでそれぞれstrict versioned `Method Config / Question / Design / Output / Inference Profile`を独立に定義・登録する。Method固有の確認項目は「OLS contrast/variance、IPW propensity/normalization/positivity、AIPW nuisance/crossfit/ATE-ATT score、Refutation resampling、NCE/NCO observed null、OLS RV q=1」。条件付き必須Field、Backend effective API/version/optional extras、positive/invalid-config/wrong-target/unsupported-CI/negative-science fixtureとtyped reasonを固定する。未登録/未検証は`METHOD_PROFILE_UNAVAILABLE`等でfail-closed。単なる`config={}`、Backend default、未生成DGP/REF、K/R/MC-SE未実測をPASSとしない。これはProfile作成の**担当配分採用**であり、個々のSchema/Inference/科学Referenceの完成・Freeze・Coding Authorizationを意味しない。

## 5. Global Scientific, I/O and Compatibility Constraints

- PREP-02の共通F03/F04/F05/F06/F07は適用基準。JCS RFC8785、Source/Graph/ContentRef/Manifestの異なるhash domain、atomic no-clobber、Trusted Root/independent privacy、typed scientific statusを損なわない。
- 旧Product `causal-analysis-spec/2`、`ScientificCorePort.run_*`、Web/API/Worker/DB、旧CLI、既存Refutation/Sensitivity `run`の公開ABIを変更しない。CLIだけの新Scientific Kernel、別MethodRegistry、別GraphVersion writer、別Publisherを作らない。
- Scientific `Identification/Point/Inference/ScienceAcceptance`とTechnical outcomeは別軸。不適格なMethod、無識別、Unsupported CI、missing optional Backendは型付き負結果またはTechnical error。未実行をPASS、point-onlyをCI有り、Backend自身の出力を独立Oracleにしない。
- `LocalCausalUseCase`はstrict ValidatedStudyから各Portへ委譲し、Fileはstaging→atomic Publisher→independent readback。G05のPolicy認可前は個票禁止。

**このGate固有の実装判断:** 非有意NCE/NCOは無交絡証明ではない。RVは古典OLS限定。P1-M11のScience未確定を黙認しない。各PxxのPositive/NegativeとBackend/Inference/Estimand/Statusを実行前にSchema/Registryで照合する。

## 6. Gate Coding-side Verification and Candidate Assembly

- 各PxxはMethod/DGP/NEG/REF/DD、Class.Method signature、typed Status、Backend effective API/optional Dependency、必要な実OS/CLI、既存Product invariantをFocused Testで確認。物理Path/Commandは40 Operatorがcurrent checkoutをdiscover/collectする。
- 新Testは原則`tests/enhancement/enh_e11/g03/<layer>/`、layer=unit/contract/integration（ENH-E11はCLI-only）。もし現行ProductのFrontend/Browser Regressionがaffectedならその既存Suiteも現物から検証する。科学的真偽をDir名やmockのみで推定しない。
- 全required PxxがCheckpoint SHAとStatus Reportを残してからCandidate Assembly。Gate-wide self-verification後に**1つのFixed Trial Candidate SHA**を確定、別途Freezeされた07による独立Test Item/999を実行する。
- Test-side defectはBLOCKEDとしIndependent Test Agentはtest/productionを修理しない。G10の最終統合は各Gateの独立999を置換しない。

## 7. Freeze前のReview/Stop条件

1. OwnerがGate依存・Acceptance Boundary・WORK_PACKAGE/Pxx順序を採否する。
2. `10_32`のMethod config、Estimand、DGP、NEG、Reference、実効Backend/API/Inferenceの適格性を検証する。特に本Gateの未決事項 非有意NCE/NCOは無交絡証明ではない。RVは古典OLS限定。P1-M11のScience未確定を黙認しない。
3. 06/PxxのClass.Field/Constructor/Signature/Result authorityと既存Source、共有Port/Bridgeを整合させ、必要な設計欠落を閉じる。
4. **既存Gate07 DRAFTを本06/Pxxと照合・修正し**、Method別AC/独立科学閾値・負例・固定Fixture/Runtime・No PASS条件を確定して06/07をともにFreezeする。
5. Baseline full SHA、上流canonical 999、Runtime/Lock/License preflight、Ownerの明示Coding Authorizationが揃うまで`CODING_NOT_AUTHORIZED`。不足時は`BLOCKED_CONTRACT_AMBIGUITY`。

**本Commitには実装変更・試験実行・Owner Freeze・Coding Authorization・Gate 999判定を含めない。**


## PREP-04.1 13 Method contract inventory (DRAFT)
- P1-M08 [P01] ESTIMATE/ATE required config: variance_spec_ref, treatment_coding_ref; design: treatment, outcome, randomization_evidence_ref, allocation_unit; DGP-001, DGP-022; NEG-001, NEG-010; REF-E01; backend/science not verified.
- P1-M09 [P01] ESTIMATE/10_32 semantic target (not assigned canonical enum) required config: linear_model_spec_ref, contrast_spec_ref, covariance_spec_ref; design: treatment, outcome, adjustment_columns, identification_evidence_ref; DGP-002, DGP-003; NEG-002, NEG-008, NEG-020; REF-E01, REF-I01; backend/science not verified.
- P1-M10 [P02] ESTIMATE/10_32 semantic target (not assigned canonical enum) required config: propensity_model_ref, weight_normalization_spec_ref, positivity_diagnostic_ref; design: treatment, outcome, confounders, overlap_assumption_ref; DGP-002, DGP-003; NEG-010, NEG-018; REF-E02; backend/science not verified.
- P1-M11 [P02] ESTIMATE/10_32 semantic target (not assigned canonical enum) required config: propensity_model_ref, outcome_model_ref, crossfit_folds, variance_spec_ref; design: treatment, outcome, confounders, overlap_assumption_ref; DGP-002, DGP-003; NEG-010, NEG-011, NEG-012; REF-E03; backend/science not verified.
- P1-M12 [P03] REFUTE/10_32 semantic target (not assigned canonical enum) required config: placebo_rule_ref, repetitions; design: base_effect_hash, design_evidence_ref, resampling_unit; DGP-022; NEG-014; REF-R01; backend/science not verified.
- P1-M13 [P03] REFUTE/10_32 semantic target (not assigned canonical enum) required config: subset_selection_ref, subset_fraction; design: base_effect_hash, design_evidence_ref, sampling_unit; DGP-001, DGP-002; NEG-015; REF-R01; backend/science not verified.
- P1-M14 [P03] REFUTE/10_32 semantic target (not assigned canonical enum) required config: perturbation_generator_ref, repetitions; design: base_effect_hash, design_evidence_ref, perturbation_scope_ref; DGP-002; NEG-017; REF-R01; backend/science not verified.
- P1-M15 [P03] REFUTE/10_32 semantic target (not assigned canonical enum) required config: resampling_unit, resamples; design: base_effect_hash, design_evidence_ref, resampling_unit; DGP-001, DGP-002; NEG-016; REF-R01; backend/science not verified.
- P1-M16 [P04] SENSITIVITY/10_32 semantic target (not assigned canonical enum) required config: candidate_adjustment_sets, design_check_rule_ref; design: base_effect_hash, graph_evidence_ref, candidate_adjustment_sets; DGP-021, DGP-002; NEG-002; REF-G01, REF-R01; backend/science not verified.
- P1-M17 [P04] SENSITIVITY/10_32 semantic target (not assigned canonical enum) required config: clip_lower, clip_upper, diagnostic_spec_ref; design: base_effect_hash, propensity_evidence_ref, overlap_assumption_ref; DGP-002, DGP-023; NEG-010, NEG-018; REF-E02, REF-R01; backend/science not verified.
- P1-M18 [P05] DIAGNOSE/10_32 semantic target (not assigned canonical enum) required config: negative_control_exposure, explicit_opt_in, null_diagnostic_spec_ref; design: outcome, treatment, negative_control_exposure, null_assumption_ref, adjustment_columns; DGP-019; NEG-019, NEG-026; REF-R02; backend/science not verified.
- P1-M19 [P05] DIAGNOSE/10_32 semantic target (not assigned canonical enum) required config: negative_control_outcome, explicit_opt_in, null_diagnostic_spec_ref; design: outcome, treatment, negative_control_outcome, null_assumption_ref, adjustment_columns; DGP-019; NEG-019, NEG-026; REF-R02; backend/science not verified.
- P1-M20 [P05] DIAGNOSE/10_32 semantic target (not assigned canonical enum) required config: q, ols_model_spec_ref, target_coefficient_ref, variance_kind; design: outcome, treatment, ols_fit_evidence_ref, degrees_of_freedom; DGP-020; NEG-020; REF-R03; backend/science not verified.


## S02：担当Method Profile・共通署名の規範（G03 / Owner承認）

担当Methodは`P1-M08〜P1-M20`の13件。共通5 Profile Kind（method_config/question_profile/design_profile/output_profile/inference_profile）は`23_api_interface_design/schema_drafts/method_profiles/factored/e11_<kind>_factored_v1.json`のshared core＋Method ID overlayを再構成して使用する。`e11_method_profile_dispatch_registry_draft1.json`とsource Git blob SHAを照合し、200 Profileの標準Draft202012チェック・Method別正負例未確認なら`METHOD_PROFILE_UNAVAILABLE`でfail-closedする。Method別OperationはP1-M08〜11がESTIMATE、M12〜15がREFUTE、M16〜17がSENSITIVITY、M18〜20がDIAGNOSE。後3群は正規`diagnostics.json`であり、架空のEffect Resultを作らない。共通Schema化は各Method固有のATE/ATT/統計量/推論条件を緩和しない。閉objectの別`allOf`合成禁止。実Backend/CIと独立Science DGP/NEG/REF/ACは別途実証が必須。

`LocalRunContext(root:TrustedLocalRoot,principal:LocalPrincipal)`および`LocalPrivacyPolicyPort.authorize(*,study,root,principal,output_shape)`が正規署名。追加のCLI row flag・`cli_row_flag`・`privacy.policy_ref`・独立署名PolicyVerifier/Anchorを実装しない。G05のみStudy `row_export_requested=true`と非root同一UID/private ext4/XFS・Method Schema/capsのANDで個票中間出力可。E11 Local GraphはProduct GraphVersion ID=null、content hashで科学由来を維持。旧Product v2 ABIと共通Scientific Kernelを保護し、無関係Product回帰の全件無条件再試験を課さず、変更影響を証明できない場合は実行またはBLOCK。科学受入・Coding Authorizationは未実施。
