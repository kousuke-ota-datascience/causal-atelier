# Ariadne ENH-E11 G04 — 07 独立テスト指示書：CATE/HTE・EconML・DRIV

**Verification contract status: DRAFT / NOT_FROZEN / TESTS_NOT_RUN**
**Owner review: 2026-11-18 JST — PREP-03 audit and G04 Gate-level verification plan reviewed/accepted, with open Method/Profile/Evidence decisions preserved. This is NOT Contract Freeze, Independent Test execution, Gate999 PASS, or Coding Authorization.**
**Gate: G04 / Independent Test Agent / Trial01 NOT_STARTED**
**Dependencies: G02 PASS, G03 PASS (canonical upstream 999)**
**Normative WHAT:** 本書のAC/Test Itemsのみ。テストの実physical path・command・runner discoveryは40 Operatorが所有。
**References:** [10_32 Scientific Method Scope](../../00_enhance_background/Revised_requirements_definition_documents/10_requirements_definition/10_32_scientific_method_scope.md) / [30_61 Domain/Ports](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_61_causal_domain_ports.md) / [30_62 Local Execution](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_62_local_execution_publication.md) / [30_63 Method Adapters](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_63_causal_method_adapters.md) / [23_41 Scientific Ports](../../00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design/23_41_cli_scientific_ports.md) / [23_42 Artifact](../../00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design/23_42_local_result_manifest_artifact.md)

## 0. Independent Gate claim

このGateがPASSしたと主張するには「非IV CATE七手法とDRIV条件付きIV構造係数を別Estimandとして提供し、点推定・区間推論・Science StatusをMethodごとに区別する。」をFull Fixed Candidate SHAで、後述の全受入軸と独立科学的Referenceに照らして証明する。Pxx COMPLETE、CLI exit0、Source上のMethod名、mock-onlyは独立Gate/Science PASSではない。

## 1. Acceptance Criteria (each blocking)

- **AC01 Strict Method/Design/Estimand:** 受理されたMethod×Operation×Target×Question/Design/GraphVersion/HashとInference Policyのみ実行。unknown/mismatch/partial/unidentifiedはtyped negative。
- **AC02 Actual Science:** 各Methodの既知DGP・Negative・独立REF、Backend実測/現行推論API、明示Assumption/Point/UncertaintyとScience status。
- **AC03 Portable Result:** Graph/Effect/Diagnostic/ConfidenceSet/MethodConfig/Provenanceを正しくBundle/Manifest/Readerへ保存し、hash/readback/negativeを確認。
- **AC04 Compatibility/Safety:** G01 FS/Privacy/Atomic/JCSと旧Product v2のprotected interface/behaviorを壊さず、無言fallback/未認可出力がない。
- **AC05 Identity/Independent QA:** Source/lock/fixture SHA、科学事前登録、test-layer、実効環境、Test Item全証拠と正式999判定。

## 2. Required Test Items (file locations are NOT normative)

| ID | Primary purpose | Primary verification layer | Required observable evidence |
|---|---|---|---|
| `G04-07-01` | CATE/DRIV Estimand・Inference Registry（cross-cutting） | unit/contract + required integration | Method-specific inference/point/confirmatory contract；適格positive/negative・typed Reason |
| `G04-07-02` | DML/CausalForest/DR推定器（P2-M01, P2-M02, P2-M03, P2-M04） | contract + real backend integration + independent reference | X/W/propensity/nuisance/forest/folds；適格positive/negative・typed Reason |
| `G04-07-03` | S/T/X-Learner（P2-M05, P2-M06, P2-M07） | contract + real backend integration + independent reference | counterfactual prediction・support/CI制限；適格positive/negative・typed Reason |
| `G04-07-04` | DRIV conditional IV slope（P2-M08） | contract + real backend integration + independent reference | Z/A/X/W・IV条件・weak/CI unavailable；適格positive/negative・typed Reason |
| `G04-07-05` | CATE typed Result/CLI統合（cross-cutting） | unit/contract + required integration | CATE/DRIV Resultのポータビリティとlegacy保護；適格positive/negative・typed Reason |
| `G04-07-06` | Whole Local CLI/Port/Artifact integration | contract + real CLI/FS integration | Strict Operation, Hash, Manifest, Reader, privacy, negative Error status |
| `G04-07-07` | Protected v2/upstream contracts | current actual legacy suite + E11 integration | Upstream 999 invariants, no old v2 CLI/Result change |
| `G04-07-08` | Independent Science/T2/T3 | independently verified reference + real backend integration | Method-specific DGP/NEG/REF, prereg K/R/seed/compute, predeclared quantitative decision |
| `001` | Candidate identity | repository provenance audit | Candidate full SHA, actual checkout, test-only diff classification |
| `999` | Formal Gate decision | independent 30 reports | All blocking items PASS, verified FAIL or BLOCKED and owner action |

**Browser E2E:** 本E11 ScopeはCLI-firstで新規Web UIを実装しないため、当該Gateの新規Browser E2E blocking journeyは**N/A**。既存Productのaffected Browser journeyはRegression対象となり得る。将来UIを本GateScopeへ変更する場合は07の正式Amendment・再Freezeとcritical journey・command・environment・synchronization記述を先行させる。

## 3. Method-by-Method Scientific test obligations

| Method / DD-ID | Target | DGP/NEG / REF | Required evidence / decision |
|---|---|---|---|
| `P2-M01` / `DD-E11-METH-P201` | LinearDML CATE | DGP-003; NEG-011, NEG-012, NEG-013 / REF-E05 | PLAN:G04 / CONFIG_AND_AC_PENDING / NOT_GENERATED / AC-D01, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-I03；Method-specific science/CI未確定ならBLOCKED |
| `P2-M02` / `DD-E11-METH-P202` | CausalForestDML CATE | DGP-004; NEG-010, NEG-012, NEG-013 / REF-E05 | PLAN:G04 / CONFIG_AND_AC_PENDING / NOT_GENERATED / AC-D01, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-I03；Method-specific science/CI未確定ならBLOCKED |
| `P2-M03` / `DD-E11-METH-P203` | DRLearner CATE | DGP-003, DGP-004; NEG-011, NEG-012, NEG-013 / REF-E05, REF-E03 | PLAN:G04 / CONFIG_AND_AC_PENDING / NOT_GENERATED / AC-D01, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-I03；Method-specific science/CI未確定ならBLOCKED |
| `P2-M04` / `DD-E11-METH-P204` | ForestDRLearner CATE | DGP-004; NEG-010, NEG-011, NEG-013 / REF-E05, REF-E03 | PLAN:G04 / CONFIG_AND_AC_PENDING / NOT_GENERATED / AC-D01, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-I03；Method-specific science/CI未確定ならBLOCKED |
| `P2-M05` / `DD-E11-METH-P205` | S-Learner CATE | DGP-002, DGP-003; NEG-010, NEG-012, NEG-013 / REF-E05 | PLAN:G04 / CONFIG_AND_AC_PENDING / NOT_GENERATED / AC-D01, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-I03；Method-specific science/CI未確定ならBLOCKED |
| `P2-M06` / `DD-E11-METH-P206` | T-Learner CATE | DGP-003, DGP-004; NEG-010, NEG-013 / REF-E05 | PLAN:G04 / CONFIG_AND_AC_PENDING / NOT_GENERATED / AC-D01, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-I03；Method-specific science/CI未確定ならBLOCKED |
| `P2-M07` / `DD-E11-METH-P207` | X-Learner CATE | DGP-003, DGP-004; NEG-011, NEG-012, NEG-013 / REF-E05 | PLAN:G04 / CONFIG_AND_AC_PENDING / NOT_GENERATED / AC-D01, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-I03；Method-specific science/CI未確定ならBLOCKED |
| `P2-M08` / `DD-E11-METH-P208` | IV heterogeneous structural slope | DGP-008; NEG-009, NEG-012, NEG-013 / REF-E06 | PLAN:G04 / OWNER_TARGET_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED / AC-D01, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-I03；Method-specific science/CI未確定ならBLOCKED |

**Independent oracle and numerical rule:** DGP truthとEstimator/Backend outputは別Authority。Fixed generator/Reference SHA、既知EstimandとAssumptions、negative/statusを先に登録。Deterministic schema/JCS/roundtripは100%一致。Stochastic ScienceはT2 PilotとT3正式事前登録を分離し、多重性K/FWER=0.05、K/R/seed/threshold/computeは科学決定に基づきFreeze。未確定を推測で補完せず該当Test Item BLOCKED。


**Owner採用 OD-05（2026-11-19）：** G04の8 Methodについて、既決Target/数理は変更せず、担当Pxxでそれぞれstrict versioned `Method Config / Question / Design / Output / Inference Profile`を独立に定義・登録する。Method固有の確認項目は「EconML DML/DR/final learner、X/W roles、binary treatment、nuisance folds/seed、CATE inference point-only境界、DRIV theta_IV(x)とB0/B1分離」。条件付き必須Field、Backend effective API/version/optional extras、positive/invalid-config/wrong-target/unsupported-CI/negative-science fixtureとtyped reasonを固定する。未登録/未検証は`METHOD_PROFILE_UNAVAILABLE`等でfail-closed。単なる`config={}`、Backend default、未生成DGP/REF、K/R/MC-SE未実測をPASSとしない。これはProfile作成の**担当配分採用**であり、個々のSchema/Inference/科学Referenceの完成・Freeze・Coding Authorizationを意味しない。

**Independent acceptance for every G04 Method:** valid config/Question/Design/output/Inference positive, extra unknown-property/missing conditional field/wrong target/Graph or DataRef hash/backend mismatch/unsupported CI negatives, deployed real backend API and independent DGP/REF must be separately evidenced. G01/G10 Gateway PASS must not infer scientific proof from schema shape.

## 4. Verification operation, evidence and decision

- Fixed Trial Candidate SHAと実効checkoutが同じsemantic implementation stateか監査。上流Gateのcanonical 999 PASSとprotected contractをSource上の根拠で照合。
- 40 Test Agentは`tests/enhancement/enh_e11/<gate>/`を始点に、関連する`tests/product/`/`tests/integration/`等を現物から発見、test existence/collection/fixture/conftest/dependencies/runner/FS/backendを確認。07にhistorical filename/commandを固定しない。
- Test evidenceにはItem ID/DD ID、actual path/command、source/fixture/lock SHA、effective OS/FS/backend、Known truth/observed output、positive+negative、PASS/FAIL/BLOCKEDと原因を記録。Evidence commitとCandidate SHAを混同しない。
- Independent Test Agentはproduct/test code/runner/CI/06/07を修復しない。Product不変違反を実証したときFAIL、Test-side/UNKNOWN/Backend/独立Oracle不足でProduct判定不能ならBLOCKED。
- G01〜G10各Gateの999は独立であり、Methodごとの未実施・Science未検証・Protected Regression欠落がある限りGate PASS禁止。

## 5. Freeze前のOwner/Science review

DRIV=通常CATEの同一Target化、pointwise CI=simultaneous band扱い、unsupported CIの捏造を禁止。

Method-specific strict Schema・positive/negative・独立Reference/推論Method/CI・threshold・Backend/License・Gate境界/depends/quant computeをレビューし、07をFreezeして初めて実行可能。現時点ではTest NOT_RUN、999 NOT_EXECUTED。


## PREP-04.1 independent strict Method verification (DRAFT)

### P2-M01 — strict Method contract (PREP-04.1 DRAFT / NOT_FROZEN)
- Method scope: ESTIMATE / CATE; Pxx=P01; preserve 10_32 scientific target, do not cast alternative estimands.
- Config mandatory fields: model_y_ref, model_t_ref, cv_folds, final_model_ref; versioned method_config Schema restricts type/const/range and extra keys, config={} is rejected, no backend defaults.
- Question mandatory: question_id/research_question/population/analysis_goal/estimand_family/contrast; Study target and references cross-validated.
- Design mandatory: design_id/question_id/design_kind plus treatment, outcome, effect_modifiers, controls, unconfoundedness_ref; validated data columns, roles, dataset support and assumption/Graph/temporal provenance. Declarations are not proof of causal truth. Exact types enforced by dedicated design_profile Schema.
- Positive output: result.json/e11-local-effect-result/1, point may be unavailable; individual row outputs only by G05 authority; status/marker/manifest and Reader hash/readback required; negative science typed and no fictitious positive.
- Inference: requested=false/null or true/numeric (0,1); real CI needs compatible versioned backend and independent coverage; unsupported→INFERENCE_UNAVAILABLE. CONFIRMATORY is not granted by schema syntax.
- Independent AC: DGP-003; NEG-011, NEG-012, NEG-013; REF-E05. Negative matrix includes empty/unknown/malformed config, wrong operation/target, missing/mismatched upstream hash, unsupported CI, unavailable backend and Method-specific NEG. Real backend and independent DGP/REF/K/R/MC-SE/FWER 0.05 remain NOT_VERIFIED.


### P2-M02 — strict Method contract (PREP-04.1 DRAFT / NOT_FROZEN)
- Method scope: ESTIMATE / CATE; Pxx=P01; preserve 10_32 scientific target, do not cast alternative estimands.
- Config mandatory fields: model_y_ref, model_t_ref, cv_folds, n_estimators, min_leaf_size; versioned method_config Schema restricts type/const/range and extra keys, config={} is rejected, no backend defaults.
- Question mandatory: question_id/research_question/population/analysis_goal/estimand_family/contrast; Study target and references cross-validated.
- Design mandatory: design_id/question_id/design_kind plus treatment, outcome, effect_modifiers, controls, unconfoundedness_ref; validated data columns, roles, dataset support and assumption/Graph/temporal provenance. Declarations are not proof of causal truth. Exact types enforced by dedicated design_profile Schema.
- Positive output: result.json/e11-local-effect-result/1, point may be unavailable; individual row outputs only by G05 authority; status/marker/manifest and Reader hash/readback required; negative science typed and no fictitious positive.
- Inference: requested=false/null or true/numeric (0,1); real CI needs compatible versioned backend and independent coverage; unsupported→INFERENCE_UNAVAILABLE. CONFIRMATORY is not granted by schema syntax.
- Independent AC: DGP-004; NEG-010, NEG-012, NEG-013; REF-E05. Negative matrix includes empty/unknown/malformed config, wrong operation/target, missing/mismatched upstream hash, unsupported CI, unavailable backend and Method-specific NEG. Real backend and independent DGP/REF/K/R/MC-SE/FWER 0.05 remain NOT_VERIFIED.


### P2-M03 — strict Method contract (PREP-04.1 DRAFT / NOT_FROZEN)
- Method scope: ESTIMATE / CATE; Pxx=P01; preserve 10_32 scientific target, do not cast alternative estimands.
- Config mandatory fields: outcome_model_ref, propensity_model_ref, cv_folds; versioned method_config Schema restricts type/const/range and extra keys, config={} is rejected, no backend defaults.
- Question mandatory: question_id/research_question/population/analysis_goal/estimand_family/contrast; Study target and references cross-validated.
- Design mandatory: design_id/question_id/design_kind plus treatment, outcome, effect_modifiers, controls, unconfoundedness_ref; validated data columns, roles, dataset support and assumption/Graph/temporal provenance. Declarations are not proof of causal truth. Exact types enforced by dedicated design_profile Schema.
- Positive output: result.json/e11-local-effect-result/1, point may be unavailable; individual row outputs only by G05 authority; status/marker/manifest and Reader hash/readback required; negative science typed and no fictitious positive.
- Inference: requested=false/null or true/numeric (0,1); real CI needs compatible versioned backend and independent coverage; unsupported→INFERENCE_UNAVAILABLE. CONFIRMATORY is not granted by schema syntax.
- Independent AC: DGP-003, DGP-004; NEG-011, NEG-012, NEG-013; REF-E05, REF-E03. Negative matrix includes empty/unknown/malformed config, wrong operation/target, missing/mismatched upstream hash, unsupported CI, unavailable backend and Method-specific NEG. Real backend and independent DGP/REF/K/R/MC-SE/FWER 0.05 remain NOT_VERIFIED.


### P2-M04 — strict Method contract (PREP-04.1 DRAFT / NOT_FROZEN)
- Method scope: ESTIMATE / CATE; Pxx=P01; preserve 10_32 scientific target, do not cast alternative estimands.
- Config mandatory fields: outcome_model_ref, propensity_model_ref, cv_folds, n_estimators, min_leaf_size; versioned method_config Schema restricts type/const/range and extra keys, config={} is rejected, no backend defaults.
- Question mandatory: question_id/research_question/population/analysis_goal/estimand_family/contrast; Study target and references cross-validated.
- Design mandatory: design_id/question_id/design_kind plus treatment, outcome, effect_modifiers, controls, unconfoundedness_ref; validated data columns, roles, dataset support and assumption/Graph/temporal provenance. Declarations are not proof of causal truth. Exact types enforced by dedicated design_profile Schema.
- Positive output: result.json/e11-local-effect-result/1, point may be unavailable; individual row outputs only by G05 authority; status/marker/manifest and Reader hash/readback required; negative science typed and no fictitious positive.
- Inference: requested=false/null or true/numeric (0,1); real CI needs compatible versioned backend and independent coverage; unsupported→INFERENCE_UNAVAILABLE. CONFIRMATORY is not granted by schema syntax.
- Independent AC: DGP-004; NEG-010, NEG-011, NEG-013; REF-E05, REF-E03. Negative matrix includes empty/unknown/malformed config, wrong operation/target, missing/mismatched upstream hash, unsupported CI, unavailable backend and Method-specific NEG. Real backend and independent DGP/REF/K/R/MC-SE/FWER 0.05 remain NOT_VERIFIED.


### P2-M05 — strict Method contract (PREP-04.1 DRAFT / NOT_FROZEN)
- Method scope: ESTIMATE / CATE; Pxx=P02; preserve 10_32 scientific target, do not cast alternative estimands.
- Config mandatory fields: outcome_model_ref, counterfactual_prediction_rule_ref; versioned method_config Schema restricts type/const/range and extra keys, config={} is rejected, no backend defaults.
- Question mandatory: question_id/research_question/population/analysis_goal/estimand_family/contrast; Study target and references cross-validated.
- Design mandatory: design_id/question_id/design_kind plus treatment, outcome, effect_modifiers, controls, unconfoundedness_ref; validated data columns, roles, dataset support and assumption/Graph/temporal provenance. Declarations are not proof of causal truth. Exact types enforced by dedicated design_profile Schema.
- Positive output: result.json/e11-local-effect-result/1, point may be unavailable; individual row outputs only by G05 authority; status/marker/manifest and Reader hash/readback required; negative science typed and no fictitious positive.
- Inference: requested=false/null or true/numeric (0,1); real CI needs compatible versioned backend and independent coverage; unsupported→INFERENCE_UNAVAILABLE. CONFIRMATORY is not granted by schema syntax.
- Independent AC: DGP-002, DGP-003; NEG-010, NEG-012, NEG-013; REF-E05. Negative matrix includes empty/unknown/malformed config, wrong operation/target, missing/mismatched upstream hash, unsupported CI, unavailable backend and Method-specific NEG. Real backend and independent DGP/REF/K/R/MC-SE/FWER 0.05 remain NOT_VERIFIED.


### P2-M06 — strict Method contract (PREP-04.1 DRAFT / NOT_FROZEN)
- Method scope: ESTIMATE / CATE; Pxx=P02; preserve 10_32 scientific target, do not cast alternative estimands.
- Config mandatory fields: treated_model_ref, control_model_ref; versioned method_config Schema restricts type/const/range and extra keys, config={} is rejected, no backend defaults.
- Question mandatory: question_id/research_question/population/analysis_goal/estimand_family/contrast; Study target and references cross-validated.
- Design mandatory: design_id/question_id/design_kind plus treatment, outcome, effect_modifiers, controls, unconfoundedness_ref; validated data columns, roles, dataset support and assumption/Graph/temporal provenance. Declarations are not proof of causal truth. Exact types enforced by dedicated design_profile Schema.
- Positive output: result.json/e11-local-effect-result/1, point may be unavailable; individual row outputs only by G05 authority; status/marker/manifest and Reader hash/readback required; negative science typed and no fictitious positive.
- Inference: requested=false/null or true/numeric (0,1); real CI needs compatible versioned backend and independent coverage; unsupported→INFERENCE_UNAVAILABLE. CONFIRMATORY is not granted by schema syntax.
- Independent AC: DGP-003, DGP-004; NEG-010, NEG-013; REF-E05. Negative matrix includes empty/unknown/malformed config, wrong operation/target, missing/mismatched upstream hash, unsupported CI, unavailable backend and Method-specific NEG. Real backend and independent DGP/REF/K/R/MC-SE/FWER 0.05 remain NOT_VERIFIED.


### P2-M07 — strict Method contract (PREP-04.1 DRAFT / NOT_FROZEN)
- Method scope: ESTIMATE / CATE; Pxx=P02; preserve 10_32 scientific target, do not cast alternative estimands.
- Config mandatory fields: treated_model_ref, control_model_ref, cross_arm_weight_model_ref; versioned method_config Schema restricts type/const/range and extra keys, config={} is rejected, no backend defaults.
- Question mandatory: question_id/research_question/population/analysis_goal/estimand_family/contrast; Study target and references cross-validated.
- Design mandatory: design_id/question_id/design_kind plus treatment, outcome, effect_modifiers, controls, unconfoundedness_ref; validated data columns, roles, dataset support and assumption/Graph/temporal provenance. Declarations are not proof of causal truth. Exact types enforced by dedicated design_profile Schema.
- Positive output: result.json/e11-local-effect-result/1, point may be unavailable; individual row outputs only by G05 authority; status/marker/manifest and Reader hash/readback required; negative science typed and no fictitious positive.
- Inference: requested=false/null or true/numeric (0,1); real CI needs compatible versioned backend and independent coverage; unsupported→INFERENCE_UNAVAILABLE. CONFIRMATORY is not granted by schema syntax.
- Independent AC: DGP-003, DGP-004; NEG-011, NEG-012, NEG-013; REF-E05. Negative matrix includes empty/unknown/malformed config, wrong operation/target, missing/mismatched upstream hash, unsupported CI, unavailable backend and Method-specific NEG. Real backend and independent DGP/REF/K/R/MC-SE/FWER 0.05 remain NOT_VERIFIED.


### P2-M08 — strict Method contract (PREP-04.1 DRAFT / NOT_FROZEN)
- Method scope: ESTIMATE / CONDITIONAL_IV_STRUCTURAL_SLOPE; Pxx=P03; preserve 10_32 scientific target, do not cast alternative estimands.
- Config mandatory fields: outcome_model_ref, treatment_model_ref, instrument_model_ref, cv_folds; versioned method_config Schema restricts type/const/range and extra keys, config={} is rejected, no backend defaults.
- Question mandatory: question_id/research_question/population/analysis_goal/estimand_family/contrast; Study target and references cross-validated.
- Design mandatory: design_id/question_id/design_kind plus treatment, outcome, instrument, effect_modifiers, controls, iv_assumptions_ref; validated data columns, roles, dataset support and assumption/Graph/temporal provenance. Declarations are not proof of causal truth. Exact types enforced by dedicated design_profile Schema.
- Positive output: result.json/e11-local-effect-result/1, point may be unavailable; individual row outputs only by G05 authority; status/marker/manifest and Reader hash/readback required; negative science typed and no fictitious positive.
- Inference: requested=false/null or true/numeric (0,1); real CI needs compatible versioned backend and independent coverage; unsupported→INFERENCE_UNAVAILABLE. CONFIRMATORY is not granted by schema syntax.
- Independent AC: DGP-008; NEG-009, NEG-012, NEG-013; REF-E06. Negative matrix includes empty/unknown/malformed config, wrong operation/target, missing/mismatched upstream hash, unsupported CI, unavailable backend and Method-specific NEG. Real backend and independent DGP/REF/K/R/MC-SE/FWER 0.05 remain NOT_VERIFIED.


## S02 / G04のSelf-contained Method・非スカラー出力契約（Owner承認）

対象`P2-M01〜P2-M08`の8件。5 Profile kindは`23_api_interface_design/schema_drafts/method_profiles/factored/e11_<kind>_factored_v1.json`（kind=method_config/question_profile/design_profile/output_profile/inference_profile）＋Method ID別overlayを再構成し、`e11_method_profile_dispatch_registry_draft1.json`で厳密dispatch/Blob SHA/Method正負例/標準Draft202012 Parityを確認。closed schema断片を`allOf`結合しない。未検証/unknown Methodには`METHOD_PROFILE_UNAVAILABLE`を返す。全8 MethodがEffect scalar `result.json`の`point=NOT_AVAILABLE`（ターゲットが関数であるため）と独立typed `cate_surface.json`をManifestに記載し、observed rowではない事前指定Design grid上の評価値・SHA・Method/Estimandを保存する。P2-M01〜07はnon-IV `NON_IV_CATE`、P2-M08は条件付きIV `CONDITIONAL_IV_STRUCTURAL_SLOPE`。両者を同一CATEと混同しない。個人レベル`X_i`やCATE値は公開しない。個票のbounded ParquetはG05のみが明示Study `row_export_requested=true`＋nonroot private ext4/XFS/Method別列行byte/memory capsで審査してG01 Sinkへ。共通SchemaはEconMLのmethod-specific inferenceを保証しない。

正規Context`LocalRunContext(root,principal)`とPrivacy Port`authorize(*,study,root,principal,output_shape)`。署名Verifier/Policy Anchor・Study`policy_ref`・追加CLI flagは撤廃。独立07は8 Methodの実Backend API、fitted inference、CI unsupportedをtyped、CATE grid mismatch/observed rows leak/IV target錯誤/Result scalar偽装/Manifest readback/hashの正負例を検査。既存KernelとProduct v2公開ABIを保護する。未実行をScience PASSにしない。

## S09 documented non-scalar output correction — P2-M01–M08 (2026-11-22)

The initial E11 output for each supported P2-M01–M08 `ESTIMATE` is a **non-scalar** conditional-effect function: P2-M01–07 = `NON_IV_CATE`; P2-M08 = `CONDITIONAL_IV_STRUCTURAL_SLOPE` (not ordinary CATE, B0 LATE or B1 coefficient). For a valid eligible run, `result.json` (`e11-local-effect-result/1`) must encode `point.availability=NOT_AVAILABLE`, `point.value=null`, and `point.reason.code=NON_SCALAR_TARGET` (not a top-level Result `point_availability` field); `status.json` separately reports `point_availability=NOT_AVAILABLE`; it must **not** present any fabricated scalar mean/ATE as the target. The Manifest inventories separate `cate_surface.json` with `schema_drafts/internal_scientific/e11_cate_surface_draft1.schema.json` semantics: method/estimand binding, immutable `predeclared_grid_ref`, `grid_origin`, unique typed `grid_key`, finite effects, inference availability and correct Study/source hashes. `observed_rows_included=false` is mandatory. Only predeclared **non-observed** design grid values are eligible; neither observed `X_i` nor individual effect rows may be placed there. User-specific row output remains a separate G05 Study-opt-in/private bounded Parquet path. If no admissible predeclared grid exists, fail with typed `GRID_UNSPECIFIED`, not an implicit training-data grid or empty-success file. JSON Schema shape is not proof of privacy or scientific correctness.

**G04 independent 07 mandatory observable cases:** For each P2-M01–M08, compare non-observed predeclared grid values against independent target/Reference; inspect actual `result.json(point.availability=NOT_AVAILABLE, point.value=null, point.reason.code=NON_SCALAR_TARGET)` + `cate_surface.json` + Manifest/Marker/Reader hashes, Method/Estimand/grid/Study lineage and typed pointwise CI availability. Negative: missing/changed grid, duplicates/nonfinite, observed-row `X_i` or person-specific effects, DRIV mislabeled non-IV CATE, fabricated scalar/CI, absent or tampered Artifact, and aggregate/row privacy leak. Any missing real evidence is BLOCKED, not PASS.
