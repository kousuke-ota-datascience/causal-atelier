# Ariadne ENH-E11 / G04 — 06 実装指示書

**Document class:** Gate Coding Contract — Reviewer DRAFT  
**Gate:** G04 — 正式Enhance Workflow Gate  
**Contract status:** DRAFT / NOT_FROZEN / CODING_NOT_AUTHORIZED  
**Depends on:** G02 PASS, G03 PASS （Owner一括レビュー承認済み・未Freeze）  
**Execution mode:** WORK_PACKAGE （Owner一括レビュー承認済み・未Freeze）  
**Required packages:** P01,P02,P03,P04 （Owner一括レビュー承認済み・未Freeze）  
**Trial:** NOT_STARTED  
**Gate07:** [07独立テスト指示書案](07_Ariadne_ENH-E11_G04_test_instruction.md) — DRAFT / NOT_FROZEN / TESTS_NOT_RUN（Owner一括レビュー承認済み・ただしOpen Decision残存、未Freeze）。  
**Baseline SHA:** 未固定（Coding Authorization時に取得）。  
**Authority/reference:** [Gate decomposition](../../40_operator_workflows/architecture_review/03_gate_decomposition.md)／[PREP-02 freeze](../../00_enhance_background/Revised_requirements_definition_documents/combined_review/117_20261117_prep02_common_contract_baseline_freeze.md)／[RD 10_32](../../00_enhance_background/Revised_requirements_definition_documents/10_requirements_definition/10_32_scientific_method_scope.md)／[DD 30_61](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_61_causal_domain_ports.md)／[DD 30_62](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_62_local_execution_publication.md)／[DD 30_63](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_63_causal_method_adapters.md)／[IF 23_41](../../00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design/23_41_cli_scientific_ports.md)／[IF 23_42](../../00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design/23_42_local_result_manifest_artifact.md)

**Owner review record:** 2026-11-18 JST、PREP-03 Final Auditの静的レビュー、G04のGate DAG・WORK_PACKAGE mode・Required packagesをOwner承認。06/07/Pxxの実装・科学的未決を補完して承認したものではない。NOT_FROZEN / CODING_NOT_AUTHORIZED / TESTS_NOT_RUNを維持。参照：[`PREP03_final_audit.md`](../PREP03_final_audit.md) §6。

## 0. Contract Boundary and PREP-03 Status

Gateの06は実装WHAT、07は独立Verification WHAT、40 Operatorは物理Test配置・実行HOW、999は唯一の正式Gate Verdict。P00はPlan、Pxxはbounded Coding Unitであり、Pxx/06の作成はGate PASS、Coding Authorization、Method Science PASS、07 Freezeを意味しない。

PREP-02のCommon Design BaselineはFreeze済み。**Gate Dependency/WORK_PACKAGE/Required Packagesの構成はOwner一括レビュー承認済み。ただし本Gate固有の未決Method config、実効Backend、独立Science Oracle、06/07/Pxxは引き続きDRAFT・NOT_FROZENで、実装開始不可。** 本文内の`Gxx PASS`は現在達成された状態ではない。

## 1. Gate Acceptance Claim and Scope

**受入命題:** 7種Non-IV CATEとDRIV IV異質効果を個別Estimand/Inferenceで提供する。

**候補依存:** `G02`のlatest canonical 999 PASS、`G03`のlatest canonical 999 PASS。この依存DAGはOwner一括レビューで承認済み。各上流Gateのlatest canonical 999 PASSは実行時に別途検証する。Issue追跡は999の代替でない。

**科学的失敗モードと未決事項:** Non-IV CATE、IV heterogeneous slope、B0 LATE、B1 linear slopeを同一視しない。G03依存はまとめReviewで検討。

**対象外:** 既存Product科学ABIの変更、Web/API/DB/Worker新規統合、G01のPublisherやGraphVersionを別実装すること、他Gate MethodをScopeなしに追加すること、顧客配布許可、現時点での正本文書昇格。

## 2. Class/Module Ownership and Canonical Signatures

既存Classと新規Design Classの区別は現物Sourceで確認すること。`30_61/62/63`のClass placement、Constructor fields、Method signatureがAuthority。明記のないConcrete引数型を創作せず、設計欠落ならFreeze前に解決する。

| Class / Port | Designed module | Method signature / source | Reuse |
|---|---|---|---|
| `EconmlCateAdapter` | `ariadne.scientific.causal_methods.heterogeneity.EconmlCateAdapter` | `preflight(self, request: ValidatedMethodRequest)` → `EligibilityOutcome`; `execute(self, request: ValidatedMethodRequest, *, sink: StagingArtifactSink)` → `TypedScientificOutcome` | 既存Scientific Kernel再利用／追加Adapterの責務 |
| `EstimatorPort` | `ariadne.scientific.ports.causal.EstimatorPort` | estimate(self, request:ValidatedEstimatorRequest, *, sink:StagingArtifactSink) -> EffectOutcome | 既存/新規の共通Value・Port・Facade参照。重複実装しない |
| `InferenceEvidence` | `ariadne.causal.inference.contracts.InferenceEvidence` | validate_for(mode,method) | 既存/新規の共通Value・Port・Facade参照。重複実装しない |
| `MetaLearnerAdapter` | `ariadne.scientific.causal_methods.heterogeneity.MetaLearnerAdapter` | `preflight(self, request: ValidatedMethodRequest)` → `EligibilityOutcome`; `execute(self, request: ValidatedMethodRequest, *, sink: StagingArtifactSink)` → `TypedScientificOutcome` | 既存Scientific Kernel再利用／追加Adapterの責務 |
| `EffectOutcome` | `ariadne.causal.inference.contracts.EffectOutcome` | validate_consistency() / to_result_payload() | 既存/新規の共通Value・Port・Facade参照。重複実装しない |
| `EconmlDrivAdapter` | `ariadne.scientific.causal_methods.heterogeneity.EconmlDrivAdapter` | `preflight(self, request: ValidatedMethodRequest)` → `EligibilityOutcome`; `execute(self, request: ValidatedMethodRequest, *, sink: StagingArtifactSink)` → `TypedScientificOutcome` | 既存Scientific Kernel再利用／追加Adapterの責務 |
| `IdentificationOutcome` | `ariadne.causal.identification.contracts.IdentificationOutcome` | from_evidence(evidence:ValidatedIdentificationEvidence) -> IdentificationOutcome | 既存/新規の共通Value・Port・Facade参照。重複実装しない |
| `EstimatorRequest` | `ariadne.causal.inference.contracts.EstimatorRequest` | validate_against(self, identification:IdentificationOutcome, design:CausalDesign, policy:EstimandEligibilityPolicy) -> ValidatedEstimatorRequest | 既存/新規の共通Value・Port・Facade参照。重複実装しない |
| `LocalCausalUseCase` | `ariadne.capabilities.causal.local_execution.LocalCausalUseCase` | preflight(self,spec:ValidatedStudy,context:LocalRunContext)->PreflightReport / run(self,spec:ValidatedStudy,context:LocalRunContext)->LocalRunOutcome | 既存/新規の共通Value・Port・Facade参照。重複実装しない |

**Port dependency:** Local CLI Composition Root → ValidatedStudy/ContentRef → `LocalCausalUseCase` → MethodCapabilityPort/Scientific Ports/Privacy/Publication → Method Adapter → shared `ariadne.causal.*` / `ariadne.scientific.*` Kernel。DomainからCLI ConcreteやWeb/DBへ逆依存しない。既存Product `ScientificCorePort`はBridge経由で同じ科学Kernelに接続する。

## 3. Bounded Work Packages and DAG

| Package | Responsibility | Primary Classes / Ports | Methods | Depends on Pxx |
|---|---|---|---|---|
| P01 | econml dml dr | EconmlCateAdapter / EstimatorPort,InferenceEvidence | P2-M01,P2-M02,P2-M03,P2-M04 | NONE |
| P02 | s t x learners | MetaLearnerAdapter / EstimatorPort,EffectOutcome | P2-M05,P2-M06,P2-M07 | P01 |
| P03 | driv iv slope | EconmlDrivAdapter / IdentificationOutcome,EstimatorRequest,InferenceEvidence | P2-M08 | P01 |
| P04 | cate results | — / LocalCausalUseCase,EffectOutcome,InferenceEvidence,EstimatorPort | cross-cutting | P01,P02,P03 |

全PxxのScopeとClass/Method ownershipは別文書`06_G04_Pxx_*.md`に自己完結記述。上流Packageからの利用はPort/Value/Bridgeであり、別Packageが所有するMethodを複製しない。Package setはOwnerが変更し得るため**DRAFT**。

## 4. Method Requirements, Eligibility, Positive/Negative Science

| Method / estimand | DD proof ID | Positive / Negative | Independent reference | AC | status from RD |
|---|---|---|---|---|---|
| `P2-M01` LinearDML／CATE(x) | `DD-E11-METH-P201` | DGP-003; NEG-011, NEG-012, NEG-013 | REF-E05 | AC-D01, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-I03 | PLAN:G04 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P2-M02` CausalForestDML／CATE(x) | `DD-E11-METH-P202` | DGP-004; NEG-010, NEG-012, NEG-013 | REF-E05 | AC-D01, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-I03 | PLAN:G04 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P2-M03` DRLearner／CATE(x) | `DD-E11-METH-P203` | DGP-003, DGP-004; NEG-011, NEG-012, NEG-013 | REF-E05, REF-E03 | AC-D01, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-I03 | PLAN:G04 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P2-M04` ForestDRLearner／CATE(x) | `DD-E11-METH-P204` | DGP-004; NEG-010, NEG-011, NEG-013 | REF-E05, REF-E03 | AC-D01, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-I03 | PLAN:G04 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P2-M05` S-Learner／CATE(x) | `DD-E11-METH-P205` | DGP-002, DGP-003; NEG-010, NEG-012, NEG-013 | REF-E05 | AC-D01, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-I03 | PLAN:G04 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P2-M06` T-Learner／CATE(x) | `DD-E11-METH-P206` | DGP-003, DGP-004; NEG-010, NEG-013 | REF-E05 | AC-D01, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-I03 | PLAN:G04 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P2-M07` X-Learner／CATE(x) | `DD-E11-METH-P207` | DGP-003, DGP-004; NEG-011, NEG-012, NEG-013 | REF-E05 | AC-D01, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-I03 | PLAN:G04 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P2-M08` DRIV-A／CONDITIONAL_IV_STRUCTURAL_SLOPE | `DD-E11-METH-P208` | DGP-008; NEG-009, NEG-012, NEG-013 | REF-E06 | AC-D01, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-I03 | PLAN:G04 / OWNER_TARGET_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED |

**Reference rule:** MethodごとのDGP/NEG/REF/ACを必須とする。Backend自身の結果は独立Referenceではない。当該GateのRD 10_32でBLOCKEDまたはPENDINGのMethodがある場合開発都合でMethodを削除せず、識別対象/実装方法/独立Science TestをOwner決定へ戻す。科学的定量判定はOwner採用FWER=.05とMethod別PilotからのK/R/MC-SE/Resource/coverageを07に具体化してから実測する。


**Owner採用 OD-05（2026-11-19）：** G04の8 Methodについて、既決Target/数理は変更せず、担当Pxxでそれぞれstrict versioned `Method Config / Question / Design / Output / Inference Profile`を独立に定義・登録する。Method固有の確認項目は「EconML DML/DR/final learner、X/W roles、binary treatment、nuisance folds/seed、CATE inference point-only境界、DRIV theta_IV(x)とB0/B1分離」。条件付き必須Field、Backend effective API/version/optional extras、positive/invalid-config/wrong-target/unsupported-CI/negative-science fixtureとtyped reasonを固定する。未登録/未検証は`METHOD_PROFILE_UNAVAILABLE`等でfail-closed。単なる`config={}`、Backend default、未生成DGP/REF、K/R/MC-SE未実測をPASSとしない。これはProfile作成の**担当配分採用**であり、個々のSchema/Inference/科学Referenceの完成・Freeze・Coding Authorizationを意味しない。

## 5. Global Scientific, I/O and Compatibility Constraints

- PREP-02の共通F03/F04/F05/F06/F07は適用基準。JCS RFC8785、Source/Graph/ContentRef/Manifestの異なるhash domain、atomic no-clobber、Trusted Root/independent privacy、typed scientific statusを損なわない。
- 旧Product `causal-analysis-spec/2`、`ScientificCorePort.run_*`、Web/API/Worker/DB、旧CLI、既存Refutation/Sensitivity `run`の公開ABIを変更しない。CLIだけの新Scientific Kernel、別MethodRegistry、別GraphVersion writer、別Publisherを作らない。
- Scientific `Identification/Point/Inference/ScienceAcceptance`とTechnical outcomeは別軸。不適格なMethod、無識別、Unsupported CI、missing optional Backendは型付き負結果またはTechnical error。未実行をPASS、point-onlyをCI有り、Backend自身の出力を独立Oracleにしない。
- `LocalCausalUseCase`はstrict ValidatedStudyから各Portへ委譲し、Fileはstaging→atomic Publisher→independent readback。G05のPolicy認可前は個票禁止。

**このGate固有の実装判断:** Non-IV CATE、IV heterogeneous slope、B0 LATE、B1 linear slopeを同一視しない。G03依存はまとめReviewで検討。各PxxのPositive/NegativeとBackend/Inference/Estimand/Statusを実行前にSchema/Registryで照合する。

## 6. Gate Coding-side Verification and Candidate Assembly

- 各PxxはMethod/DGP/NEG/REF/DD、Class.Method signature、typed Status、Backend effective API/optional Dependency、必要な実OS/CLI、既存Product invariantをFocused Testで確認。物理Path/Commandは40 Operatorがcurrent checkoutをdiscover/collectする。
- 新Testは原則`tests/enhancement/enh_e11/g04/<layer>/`、layer=unit/contract/integration（ENH-E11はCLI-only）。もし現行ProductのFrontend/Browser Regressionがaffectedならその既存Suiteも現物から検証する。科学的真偽をDir名やmockのみで推定しない。
- 全required PxxがCheckpoint SHAとStatus Reportを残してからCandidate Assembly。Gate-wide self-verification後に**1つのFixed Trial Candidate SHA**を確定、別途Freezeされた07による独立Test Item/999を実行する。
- Test-side defectはBLOCKEDとしIndependent Test Agentはtest/productionを修理しない。G10の最終統合は各Gateの独立999を置換しない。

## 7. Freeze前のReview/Stop条件

1. OwnerがGate依存・Acceptance Boundary・WORK_PACKAGE/Pxx順序を採否する。
2. `10_32`のMethod config、Estimand、DGP、NEG、Reference、実効Backend/API/Inferenceの適格性を検証する。特に本Gateの未決事項 Non-IV CATE、IV heterogeneous slope、B0 LATE、B1 linear slopeを同一視しない。G03依存はまとめReviewで検討。
3. 06/PxxのClass.Field/Constructor/Signature/Result authorityと既存Source、共有Port/Bridgeを整合させ、必要な設計欠落を閉じる。
4. **既存Gate07 DRAFTを本06/Pxxと照合・修正し**、Method別AC/独立科学閾値・負例・固定Fixture/Runtime・No PASS条件を確定して06/07をともにFreezeする。
5. Baseline full SHA、上流canonical 999、Runtime/Lock/License preflight、Ownerの明示Coding Authorizationが揃うまで`CODING_NOT_AUTHORIZED`。不足時は`BLOCKED_CONTRACT_AMBIGUITY`。

**本Commitには実装変更・試験実行・Owner Freeze・Coding Authorization・Gate 999判定を含めない。**


## PREP-04.1 Method ownership matrix (DRAFT)
- P2-M01 Pxx P01 ESTIMATE/CATE Config(model_y_ref, model_t_ref, cv_folds, final_model_ref), Design(treatment, outcome, effect_modifiers, controls, unconfoundedness_ref), DGP-003; NEG-011, NEG-012, NEG-013; REF-E05; Backend/Science BLOCKED.
- P2-M02 Pxx P01 ESTIMATE/CATE Config(model_y_ref, model_t_ref, cv_folds, n_estimators, min_leaf_size), Design(treatment, outcome, effect_modifiers, controls, unconfoundedness_ref), DGP-004; NEG-010, NEG-012, NEG-013; REF-E05; Backend/Science BLOCKED.
- P2-M03 Pxx P01 ESTIMATE/CATE Config(outcome_model_ref, propensity_model_ref, cv_folds), Design(treatment, outcome, effect_modifiers, controls, unconfoundedness_ref), DGP-003, DGP-004; NEG-011, NEG-012, NEG-013; REF-E05, REF-E03; Backend/Science BLOCKED.
- P2-M04 Pxx P01 ESTIMATE/CATE Config(outcome_model_ref, propensity_model_ref, cv_folds, n_estimators, min_leaf_size), Design(treatment, outcome, effect_modifiers, controls, unconfoundedness_ref), DGP-004; NEG-010, NEG-011, NEG-013; REF-E05, REF-E03; Backend/Science BLOCKED.
- P2-M05 Pxx P02 ESTIMATE/CATE Config(outcome_model_ref, counterfactual_prediction_rule_ref), Design(treatment, outcome, effect_modifiers, controls, unconfoundedness_ref), DGP-002, DGP-003; NEG-010, NEG-012, NEG-013; REF-E05; Backend/Science BLOCKED.
- P2-M06 Pxx P02 ESTIMATE/CATE Config(treated_model_ref, control_model_ref), Design(treatment, outcome, effect_modifiers, controls, unconfoundedness_ref), DGP-003, DGP-004; NEG-010, NEG-013; REF-E05; Backend/Science BLOCKED.
- P2-M07 Pxx P02 ESTIMATE/CATE Config(treated_model_ref, control_model_ref, cross_arm_weight_model_ref), Design(treatment, outcome, effect_modifiers, controls, unconfoundedness_ref), DGP-003, DGP-004; NEG-011, NEG-012, NEG-013; REF-E05; Backend/Science BLOCKED.
- P2-M08 Pxx P03 ESTIMATE/CONDITIONAL_IV_STRUCTURAL_SLOPE Config(outcome_model_ref, treatment_model_ref, instrument_model_ref, cv_folds), Design(treatment, outcome, instrument, effect_modifiers, controls, iv_assumptions_ref), DGP-008; NEG-009, NEG-012, NEG-013; REF-E06; Backend/Science BLOCKED.

## S02 / G04のSelf-contained Method・非スカラー出力契約（Owner承認）

対象`P2-M01〜P2-M08`の8件。5 Profile kindは`23_api_interface_design/schema_drafts/method_profiles/factored/e11_<kind>_factored_v1.json`（kind=method_config/question_profile/design_profile/output_profile/inference_profile）＋Method ID別overlayを再構成し、`e11_method_profile_dispatch_registry_draft1.json`で厳密dispatch/Blob SHA/Method正負例/標準Draft202012 Parityを確認。closed schema断片を`allOf`結合しない。未検証/unknown Methodには`METHOD_PROFILE_UNAVAILABLE`を返す。全8 MethodがEffect scalar `result.json`の`point=NOT_AVAILABLE`（ターゲットが関数であるため）と独立typed `cate_surface.json`をManifestに記載し、observed rowではない事前指定Design grid上の評価値・SHA・Method/Estimandを保存する。P2-M01〜07はnon-IV `NON_IV_CATE`、P2-M08は条件付きIV `CONDITIONAL_IV_STRUCTURAL_SLOPE`。両者を同一CATEと混同しない。個人レベル`X_i`やCATE値は公開しない。個票のbounded ParquetはG05のみが明示Study `row_export_requested=true`＋nonroot private ext4/XFS/Method別列行byte/memory capsで審査してG01 Sinkへ。共通SchemaはEconMLのmethod-specific inferenceを保証しない。

正規Context`LocalRunContext(root,principal)`とPrivacy Port`authorize(*,study,root,principal,output_shape)`。署名Verifier/Policy Anchor・Study`policy_ref`・追加CLI flagは撤廃。独立07は8 Methodの実Backend API、fitted inference、CI unsupportedをtyped、CATE grid mismatch/observed rows leak/IV target錯誤/Result scalar偽装/Manifest readback/hashの正負例を検査。既存KernelとProduct v2公開ABIを保護する。未実行をScience PASSにしない。
