# Ariadne ENH-E11 G03 — 07 独立テスト指示書：Native推定・IPW/AIPW・Refutation・Sensitivity

**Verification contract status: DRAFT / NOT_FROZEN / TESTS_NOT_RUN**
**Owner review: 2026-11-18 JST — PREP-03 audit and G03 Gate-level verification plan reviewed/accepted, with open Method/Profile/Evidence decisions preserved. This is NOT Contract Freeze, Independent Test execution, Gate999 PASS, or Coding Authorization.**
**Gate: G03 / Independent Test Agent / Trial01 NOT_STARTED**
**Dependencies: G02 PASS (canonical upstream 999)**
**Normative WHAT:** 本書のAC/Test Itemsのみ。テストの実physical path・command・runner discoveryは40 Operatorが所有。
**References:** [10_32 Scientific Method Scope](../../00_enhance_background/Revised_requirements_definition_documents/10_requirements_definition/10_32_scientific_method_scope.md) / [30_61 Domain/Ports](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_61_causal_domain_ports.md) / [30_62 Local Execution](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_62_local_execution_publication.md) / [30_63 Method Adapters](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_63_causal_method_adapters.md) / [23_41 Scientific Ports](../../00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design/23_41_cli_scientific_ports.md) / [23_42 Artifact](../../00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design/23_42_local_result_manifest_artifact.md)

## 0. Independent Gate claim

このGateがPASSしたと主張するには「既存Native Effectを再利用してATE/ATTと推論を区別し、重み診断・Refutation・Sensitivity・NCE/NCO・OLS RVを型付き提供する。」をFull Fixed Candidate SHAで、後述の全受入軸と独立科学的Referenceに照らして証明する。Pxx COMPLETE、CLI exit0、Source上のMethod名、mock-onlyは独立Gate/Science PASSではない。

## 1. Acceptance Criteria (each blocking)

- **AC01 Strict Method/Design/Estimand:** 受理されたMethod×Operation×Target×Question/Design/GraphVersion/HashとInference Policyのみ実行。unknown/mismatch/partial/unidentifiedはtyped negative。
- **AC02 Actual Science:** 各Methodの既知DGP・Negative・独立REF、Backend実測/現行推論API、明示Assumption/Point/UncertaintyとScience status。
- **AC03 Portable Result:** Graph/Effect/Diagnostic/ConfidenceSet/MethodConfig/Provenanceを正しくBundle/Manifest/Readerへ保存し、hash/readback/negativeを確認。
- **AC04 Compatibility/Safety:** G01 FS/Privacy/Atomic/JCSと旧Product v2のprotected interface/behaviorを壊さず、無言fallback/未認可出力がない。
- **AC05 Identity/Independent QA:** Source/lock/fixture SHA、科学事前登録、test-layer、実効環境、Test Item全証拠と正式999判定。

## 2. Required Test Items (file locations are NOT normative)

| ID | Primary purpose | Primary verification layer | Required observable evidence |
|---|---|---|---|
| `G03-07-01` | Randomized difference/OLS推定（P1-M08, P1-M09） | contract + real backend integration + independent reference | Estimand/contrast/varianceと既存数値実装；適格positive/negative・typed Reason |
| `G03-07-02` | IPW・AIPW推定とDiagnostics（P1-M10, P1-M11） | contract + real backend integration + independent reference | overlap/balance/ESS/propensity/nuisance/fold；適格positive/negative・typed Reason |
| `G03-07-03` | Placebo/Subset/RandomCC/Bootstrap（P1-M12, P1-M13, P1-M14, P1-M15） | contract + real backend integration + independent reference | base Effect hash/seed/subset/resampling；適格positive/negative・typed Reason |
| `G03-07-04` | Adjustment/Propensity sensitivity（P1-M16, P1-M17） | contract + real backend integration + independent reference | set変更/clip/trim/estimand変化；適格positive/negative・typed Reason |
| `G03-07-05` | Observed NCE/NCO・OLS RV（P1-M18, P1-M19, P1-M20） | contract + real backend integration + independent reference | 事前帰無opt-in、OLS partial R²・point RV(q=1)；適格positive/negative・typed Reason |
| `G03-07-06` | Whole Local CLI/Port/Artifact integration | contract + real CLI/FS integration | Strict Operation, Hash, Manifest, Reader, privacy, negative Error status |
| `G03-07-07` | Protected v2/upstream contracts | current actual legacy suite + E11 integration | Upstream 999 invariants, no old v2 CLI/Result change |
| `G03-07-08` | Independent Science/T2/T3 | independently verified reference + real backend integration | Method-specific DGP/NEG/REF, prereg K/R/seed/compute, predeclared quantitative decision |
| `001` | Candidate identity | repository provenance audit | Candidate full SHA, actual checkout, test-only diff classification |
| `999` | Formal Gate decision | independent 30 reports | All blocking items PASS, verified FAIL or BLOCKED and owner action |

**Browser E2E:** 本E11 ScopeはCLI-firstで新規Web UIを実装しないため、当該Gateの新規Browser E2E blocking journeyは**N/A**。既存Productのaffected Browser journeyはRegression対象となり得る。将来UIを本GateScopeへ変更する場合は07の正式Amendment・再Freezeとcritical journey・command・environment・synchronization記述を先行させる。

## 3. Method-by-Method Scientific test obligations

| Method / DD-ID | Target | DGP/NEG / REF | Required evidence / decision |
|---|---|---|---|
| `P1-M08` / `DD-E11-METH-P108` | randomized diff-in-means ATE | DGP-001, DGP-022; NEG-001, NEG-010 / REF-E01 | PLAN:G03 / CONFIG_AND_AC_PENDING / NOT_GENERATED / AC-D03, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02；Method-specific science/CI未確定ならBLOCKED |
| `P1-M09` / `DD-E11-METH-P109` | OLS adopted ATE/ATT | DGP-002, DGP-003; NEG-002, NEG-008, NEG-020 / REF-E01, REF-I01 | PLAN:G03 / CONFIG_AND_AC_PENDING / NOT_GENERATED / AC-D03, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02；Method-specific science/CI未確定ならBLOCKED |
| `P1-M10` / `DD-E11-METH-P110` | IPW ATE/ATT | DGP-002, DGP-003; NEG-010, NEG-018 / REF-E02 | PLAN:G03 / CONFIG_AND_AC_PENDING / NOT_GENERATED / AC-D03, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-R05；Method-specific science/CI未確定ならBLOCKED |
| `P1-M11` / `DD-E11-METH-P111` | AIPW ATE/ATT | DGP-002, DGP-003; NEG-010, NEG-011, NEG-012 / REF-E03 | PLAN:G03 / BLOCKED / NOT_GENERATED / AC-D03, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02；Method-specific science/CI未確定ならBLOCKED |
| `P1-M12` / `DD-E11-METH-P112` | placebo treatment | DGP-022; NEG-014 / REF-R01 | PLAN:G03 / CONFIG_AND_AC_PENDING / NOT_GENERATED / AC-D01, AC-R01, AC-T01；Method-specific science/CI未確定ならBLOCKED |
| `P1-M13` / `DD-E11-METH-P113` | data subset | DGP-001, DGP-002; NEG-015 / REF-R01 | PLAN:G03 / CONFIG_AND_AC_PENDING / NOT_GENERATED / AC-D01, AC-D03, AC-R02；Method-specific science/CI未確定ならBLOCKED |
| `P1-M14` / `DD-E11-METH-P114` | random common cause | DGP-002; NEG-017 / REF-R01 | PLAN:G03 / CONFIG_AND_AC_PENDING / NOT_GENERATED / AC-D01, AC-D03, AC-R02；Method-specific science/CI未確定ならBLOCKED |
| `P1-M15` / `DD-E11-METH-P115` | bootstrap refutation | DGP-001, DGP-002; NEG-016 / REF-R01 | PLAN:G03 / CONFIG_AND_AC_PENDING / NOT_GENERATED / AC-D01, AC-D03, AC-R02；Method-specific science/CI未確定ならBLOCKED |
| `P1-M16` / `DD-E11-METH-P116` | adjustment set | DGP-021, DGP-002; NEG-002 / REF-G01, REF-R01 | PLAN:G03 / CONFIG_AND_AC_PENDING / NOT_GENERATED / AC-D01, AC-D02, AC-R02；Method-specific science/CI未確定ならBLOCKED |
| `P1-M17` / `DD-E11-METH-P117` | propensity clipping | DGP-002, DGP-023; NEG-010, NEG-018 / REF-E02, REF-R01 | PLAN:G03 / CONFIG_AND_AC_PENDING / NOT_GENERATED / AC-D03, AC-R05；Method-specific science/CI未確定ならBLOCKED |
| `P1-M18` / `DD-E11-METH-P118` | negative control exposure | DGP-019; NEG-019, NEG-026 / REF-R02 | PLAN:G03 / OWNER_METHOD_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED / AC-D01, AC-T01, AC-T02, AC-T03, AC-R03；Method-specific science/CI未確定ならBLOCKED |
| `P1-M19` / `DD-E11-METH-P119` | negative control outcome | DGP-019; NEG-019, NEG-026 / REF-R02 | PLAN:G03 / OWNER_METHOD_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED / AC-D01, AC-T01, AC-T02, AC-T03, AC-R03；Method-specific science/CI未確定ならBLOCKED |
| `P1-M20` / `DD-E11-METH-P120` | OLS partial R²、point RV(q=1) | DGP-020; NEG-020 / REF-R03 | PLAN:G03 / OWNER_METHOD_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED / AC-D01, AC-D03, AC-R04；Method-specific science/CI未確定ならBLOCKED |

**Independent oracle and numerical rule:** DGP truthとEstimator/Backend outputは別Authority。Fixed generator/Reference SHA、既知EstimandとAssumptions、negative/statusを先に登録。Deterministic schema/JCS/roundtripは100%一致。Stochastic ScienceはT2 PilotとT3正式事前登録を分離し、多重性K/FWER=0.05、K/R/seed/threshold/computeは科学決定に基づきFreeze。未確定を推測で補完せず該当Test Item BLOCKED。


**Owner採用 OD-05（2026-11-19）：** G03の13 Methodについて、既決Target/数理は変更せず、担当Pxxでそれぞれstrict versioned `Method Config / Question / Design / Output / Inference Profile`を独立に定義・登録する。Method固有の確認項目は「OLS contrast/variance、IPW propensity/normalization/positivity、AIPW nuisance/crossfit/ATE-ATT score、Refutation resampling、NCE/NCO observed null、OLS RV q=1」。条件付き必須Field、Backend effective API/version/optional extras、positive/invalid-config/wrong-target/unsupported-CI/negative-science fixtureとtyped reasonを固定する。未登録/未検証は`METHOD_PROFILE_UNAVAILABLE`等でfail-closed。単なる`config={}`、Backend default、未生成DGP/REF、K/R/MC-SE未実測をPASSとしない。これはProfile作成の**担当配分採用**であり、個々のSchema/Inference/科学Referenceの完成・Freeze・Coding Authorizationを意味しない。

**Independent acceptance for every G03 Method:** valid config/Question/Design/output/Inference positive, extra unknown-property/missing conditional field/wrong target/Graph or DataRef hash/backend mismatch/unsupported CI negatives, deployed real backend API and independent DGP/REF must be separately evidenced. G01/G10 Gateway PASS must not infer scientific proof from schema shape.

## 4. Verification operation, evidence and decision

- Fixed Trial Candidate SHAと実効checkoutが同じsemantic implementation stateか監査。上流Gateのcanonical 999 PASSとprotected contractをSource上の根拠で照合。
- 40 Test Agentは`tests/enhancement/enh_e11/<gate>/`を始点に、関連する`tests/product/`/`tests/integration/`等を現物から発見、test existence/collection/fixture/conftest/dependencies/runner/FS/backendを確認。07にhistorical filename/commandを固定しない。
- Test evidenceにはItem ID/DD ID、actual path/command、source/fixture/lock SHA、effective OS/FS/backend、Known truth/observed output、positive+negative、PASS/FAIL/BLOCKEDと原因を記録。Evidence commitとCandidate SHAを混同しない。
- Independent Test Agentはproduct/test code/runner/CI/06/07を修復しない。Product不変違反を実証したときFAIL、Test-side/UNKNOWN/Backend/独立Oracle不足でProduct判定不能ならBLOCKED。
- G01〜G10各Gateの999は独立であり、Methodごとの未実施・Science未検証・Protected Regression欠落がある限りGate PASS禁止。

## 5. Freeze前のOwner/Science review

ATE/ATT重み混同、NCE/NCO帰無非棄却からの無交絡証明、OLS以外へのRV流用を禁止。

Method-specific strict Schema・positive/negative・独立Reference/推論Method/CI・threshold・Backend/License・Gate境界/depends/quant computeをレビューし、07をFreezeして初めて実行可能。現時点ではTest NOT_RUN、999 NOT_EXECUTED。


## PREP-04.1 independent acceptance per Method (DRAFT)

### P1-M08 — strict Method contract (PREP-04.1 DRAFT)
- Operation: ESTIMATE; target: ATE; owner: P01. Study/Question/Design/Estimand/Graph and content hashes must match.
- Config: REQUIRED variance_spec_ref, treatment_coding_ref; strict no unknown keys, no implicit defaults, config={} rejected. Exact type/const/domain constraints in its versioned method_config Schema.
- Question: question_id/research_question/population/analysis_goal/estimand_family/contrast all mandatory, typed, Study-consistent.
- Design: REQUIRED treatment, outcome, randomization_evidence_ref, allocation_unit plus design_id/question_id/design_kind; explicit roles, assumptions and support validated semantically, never inferred from label. Exact field types in its versioned design_profile Schema.
- Output positive: result.json/e11-local-effect-result/1; G01 Publisher/Reader/Manifest/Hash and privacy required. Typed scientific negative can omit positive artifact.
- Inference: true request syntax requires confidence_level (0,1), not scientific CI availability; false => null; confirmatory requires independently supported method and coverage, else INFERENCE_UNAVAILABLE.
- Independent positive/negative obligations: DGP-001, DGP-022; NEG-001, NEG-010; REF-E01; additionally config omitted/unknown/malformed, operation/target mismatch, upstream-hash mismatch, missing backend, unsupported inference, no silent fallback. SCIENCE DGP/NEG/REF are not generated.
- BLOCKED: actual backend API/version/licence, nuisance/variance algorithm where unsettled, exact K/R/MC-SE/FWER=.05/threshold and oracle. NOT_FROZEN, REGISTRY_NOT_IMPLEMENTED.


### P1-M09 — strict Method contract (PREP-04.1 DRAFT)
- Operation: ESTIMATE; target: 10_32 semantic target (not assigned canonical enum); owner: P01. Study/Question/Design/Estimand/Graph and content hashes must match.
- Config: REQUIRED linear_model_spec_ref, contrast_spec_ref, covariance_spec_ref; strict no unknown keys, no implicit defaults, config={} rejected. Exact type/const/domain constraints in its versioned method_config Schema.
- Question: question_id/research_question/population/analysis_goal/estimand_family/contrast all mandatory, typed, Study-consistent.
- Design: REQUIRED treatment, outcome, adjustment_columns, identification_evidence_ref plus design_id/question_id/design_kind; explicit roles, assumptions and support validated semantically, never inferred from label. Exact field types in its versioned design_profile Schema.
- Output positive: result.json/e11-local-effect-result/1; G01 Publisher/Reader/Manifest/Hash and privacy required. Typed scientific negative can omit positive artifact.
- Inference: true request syntax requires confidence_level (0,1), not scientific CI availability; false => null; confirmatory requires independently supported method and coverage, else INFERENCE_UNAVAILABLE.
- Independent positive/negative obligations: DGP-002, DGP-003; NEG-002, NEG-008, NEG-020; REF-E01, REF-I01; additionally config omitted/unknown/malformed, operation/target mismatch, upstream-hash mismatch, missing backend, unsupported inference, no silent fallback. SCIENCE DGP/NEG/REF are not generated.
- BLOCKED: actual backend API/version/licence, nuisance/variance algorithm where unsettled, exact K/R/MC-SE/FWER=.05/threshold and oracle. NOT_FROZEN, REGISTRY_NOT_IMPLEMENTED.


### P1-M10 — strict Method contract (PREP-04.1 DRAFT)
- Operation: ESTIMATE; target: 10_32 semantic target (not assigned canonical enum); owner: P02. Study/Question/Design/Estimand/Graph and content hashes must match.
- Config: REQUIRED propensity_model_ref, weight_normalization_spec_ref, positivity_diagnostic_ref; strict no unknown keys, no implicit defaults, config={} rejected. Exact type/const/domain constraints in its versioned method_config Schema.
- Question: question_id/research_question/population/analysis_goal/estimand_family/contrast all mandatory, typed, Study-consistent.
- Design: REQUIRED treatment, outcome, confounders, overlap_assumption_ref plus design_id/question_id/design_kind; explicit roles, assumptions and support validated semantically, never inferred from label. Exact field types in its versioned design_profile Schema.
- Output positive: result.json/e11-local-effect-result/1; G01 Publisher/Reader/Manifest/Hash and privacy required. Typed scientific negative can omit positive artifact.
- Inference: true request syntax requires confidence_level (0,1), not scientific CI availability; false => null; confirmatory requires independently supported method and coverage, else INFERENCE_UNAVAILABLE.
- Independent positive/negative obligations: DGP-002, DGP-003; NEG-010, NEG-018; REF-E02; additionally config omitted/unknown/malformed, operation/target mismatch, upstream-hash mismatch, missing backend, unsupported inference, no silent fallback. SCIENCE DGP/NEG/REF are not generated.
- BLOCKED: actual backend API/version/licence, nuisance/variance algorithm where unsettled, exact K/R/MC-SE/FWER=.05/threshold and oracle. NOT_FROZEN, REGISTRY_NOT_IMPLEMENTED.


### P1-M11 — strict Method contract (PREP-04.1 DRAFT)
- Operation: ESTIMATE; target: 10_32 semantic target (not assigned canonical enum); owner: P02. Study/Question/Design/Estimand/Graph and content hashes must match.
- Config: REQUIRED propensity_model_ref, outcome_model_ref, crossfit_folds, variance_spec_ref; strict no unknown keys, no implicit defaults, config={} rejected. Exact type/const/domain constraints in its versioned method_config Schema.
- Question: question_id/research_question/population/analysis_goal/estimand_family/contrast all mandatory, typed, Study-consistent.
- Design: REQUIRED treatment, outcome, confounders, overlap_assumption_ref plus design_id/question_id/design_kind; explicit roles, assumptions and support validated semantically, never inferred from label. Exact field types in its versioned design_profile Schema.
- Output positive: result.json/e11-local-effect-result/1; G01 Publisher/Reader/Manifest/Hash and privacy required. Typed scientific negative can omit positive artifact.
- Inference: true request syntax requires confidence_level (0,1), not scientific CI availability; false => null; confirmatory requires independently supported method and coverage, else INFERENCE_UNAVAILABLE.
- Independent positive/negative obligations: DGP-002, DGP-003; NEG-010, NEG-011, NEG-012; REF-E03; additionally config omitted/unknown/malformed, operation/target mismatch, upstream-hash mismatch, missing backend, unsupported inference, no silent fallback. SCIENCE DGP/NEG/REF are not generated.
- BLOCKED: actual backend API/version/licence, nuisance/variance algorithm where unsettled, exact K/R/MC-SE/FWER=.05/threshold and oracle. NOT_FROZEN, REGISTRY_NOT_IMPLEMENTED.


### P1-M12 — strict Method contract (PREP-04.1 DRAFT)
- Operation: REFUTE; target: 10_32 semantic target (not assigned canonical enum); owner: P03. Study/Question/Design/Estimand/Graph and content hashes must match.
- Config: REQUIRED placebo_rule_ref, repetitions; strict no unknown keys, no implicit defaults, config={} rejected. Exact type/const/domain constraints in its versioned method_config Schema.
- Question: question_id/research_question/population/analysis_goal/estimand_family/contrast all mandatory, typed, Study-consistent.
- Design: REQUIRED base_effect_hash, design_evidence_ref, resampling_unit plus design_id/question_id/design_kind; explicit roles, assumptions and support validated semantically, never inferred from label. Exact field types in its versioned design_profile Schema.
- Output positive: diagnostics.json; no numeric effect result.json; G01 Publisher/Reader/Manifest/Hash and privacy required. Typed scientific negative can omit positive artifact.
- Inference: requested=false; confidence_level=null; confirmatory requires independently supported method and coverage, else INFERENCE_UNAVAILABLE.
- Independent positive/negative obligations: DGP-022; NEG-014; REF-R01; additionally config omitted/unknown/malformed, operation/target mismatch, upstream-hash mismatch, missing backend, unsupported inference, no silent fallback. SCIENCE DGP/NEG/REF are not generated.
- BLOCKED: actual backend API/version/licence, nuisance/variance algorithm where unsettled, exact K/R/MC-SE/FWER=.05/threshold and oracle. NOT_FROZEN, REGISTRY_NOT_IMPLEMENTED.


### P1-M13 — strict Method contract (PREP-04.1 DRAFT)
- Operation: REFUTE; target: 10_32 semantic target (not assigned canonical enum); owner: P03. Study/Question/Design/Estimand/Graph and content hashes must match.
- Config: REQUIRED subset_selection_ref, subset_fraction; strict no unknown keys, no implicit defaults, config={} rejected. Exact type/const/domain constraints in its versioned method_config Schema.
- Question: question_id/research_question/population/analysis_goal/estimand_family/contrast all mandatory, typed, Study-consistent.
- Design: REQUIRED base_effect_hash, design_evidence_ref, sampling_unit plus design_id/question_id/design_kind; explicit roles, assumptions and support validated semantically, never inferred from label. Exact field types in its versioned design_profile Schema.
- Output positive: diagnostics.json; no numeric effect result.json; G01 Publisher/Reader/Manifest/Hash and privacy required. Typed scientific negative can omit positive artifact.
- Inference: requested=false; confidence_level=null; confirmatory requires independently supported method and coverage, else INFERENCE_UNAVAILABLE.
- Independent positive/negative obligations: DGP-001, DGP-002; NEG-015; REF-R01; additionally config omitted/unknown/malformed, operation/target mismatch, upstream-hash mismatch, missing backend, unsupported inference, no silent fallback. SCIENCE DGP/NEG/REF are not generated.
- BLOCKED: actual backend API/version/licence, nuisance/variance algorithm where unsettled, exact K/R/MC-SE/FWER=.05/threshold and oracle. NOT_FROZEN, REGISTRY_NOT_IMPLEMENTED.


### P1-M14 — strict Method contract (PREP-04.1 DRAFT)
- Operation: REFUTE; target: 10_32 semantic target (not assigned canonical enum); owner: P03. Study/Question/Design/Estimand/Graph and content hashes must match.
- Config: REQUIRED perturbation_generator_ref, repetitions; strict no unknown keys, no implicit defaults, config={} rejected. Exact type/const/domain constraints in its versioned method_config Schema.
- Question: question_id/research_question/population/analysis_goal/estimand_family/contrast all mandatory, typed, Study-consistent.
- Design: REQUIRED base_effect_hash, design_evidence_ref, perturbation_scope_ref plus design_id/question_id/design_kind; explicit roles, assumptions and support validated semantically, never inferred from label. Exact field types in its versioned design_profile Schema.
- Output positive: diagnostics.json; no numeric effect result.json; G01 Publisher/Reader/Manifest/Hash and privacy required. Typed scientific negative can omit positive artifact.
- Inference: requested=false; confidence_level=null; confirmatory requires independently supported method and coverage, else INFERENCE_UNAVAILABLE.
- Independent positive/negative obligations: DGP-002; NEG-017; REF-R01; additionally config omitted/unknown/malformed, operation/target mismatch, upstream-hash mismatch, missing backend, unsupported inference, no silent fallback. SCIENCE DGP/NEG/REF are not generated.
- BLOCKED: actual backend API/version/licence, nuisance/variance algorithm where unsettled, exact K/R/MC-SE/FWER=.05/threshold and oracle. NOT_FROZEN, REGISTRY_NOT_IMPLEMENTED.


### P1-M15 — strict Method contract (PREP-04.1 DRAFT)
- Operation: REFUTE; target: 10_32 semantic target (not assigned canonical enum); owner: P03. Study/Question/Design/Estimand/Graph and content hashes must match.
- Config: REQUIRED resampling_unit, resamples; strict no unknown keys, no implicit defaults, config={} rejected. Exact type/const/domain constraints in its versioned method_config Schema.
- Question: question_id/research_question/population/analysis_goal/estimand_family/contrast all mandatory, typed, Study-consistent.
- Design: REQUIRED base_effect_hash, design_evidence_ref, resampling_unit plus design_id/question_id/design_kind; explicit roles, assumptions and support validated semantically, never inferred from label. Exact field types in its versioned design_profile Schema.
- Output positive: diagnostics.json; no numeric effect result.json; G01 Publisher/Reader/Manifest/Hash and privacy required. Typed scientific negative can omit positive artifact.
- Inference: requested=false; confidence_level=null; confirmatory requires independently supported method and coverage, else INFERENCE_UNAVAILABLE.
- Independent positive/negative obligations: DGP-001, DGP-002; NEG-016; REF-R01; additionally config omitted/unknown/malformed, operation/target mismatch, upstream-hash mismatch, missing backend, unsupported inference, no silent fallback. SCIENCE DGP/NEG/REF are not generated.
- BLOCKED: actual backend API/version/licence, nuisance/variance algorithm where unsettled, exact K/R/MC-SE/FWER=.05/threshold and oracle. NOT_FROZEN, REGISTRY_NOT_IMPLEMENTED.


### P1-M16 — strict Method contract (PREP-04.1 DRAFT)
- Operation: SENSITIVITY; target: 10_32 semantic target (not assigned canonical enum); owner: P04. Study/Question/Design/Estimand/Graph and content hashes must match.
- Config: REQUIRED candidate_adjustment_sets, design_check_rule_ref; strict no unknown keys, no implicit defaults, config={} rejected. Exact type/const/domain constraints in its versioned method_config Schema.
- Question: question_id/research_question/population/analysis_goal/estimand_family/contrast all mandatory, typed, Study-consistent.
- Design: REQUIRED base_effect_hash, graph_evidence_ref, candidate_adjustment_sets plus design_id/question_id/design_kind; explicit roles, assumptions and support validated semantically, never inferred from label. Exact field types in its versioned design_profile Schema.
- Output positive: diagnostics.json; no numeric effect result.json; G01 Publisher/Reader/Manifest/Hash and privacy required. Typed scientific negative can omit positive artifact.
- Inference: requested=false; confidence_level=null; confirmatory requires independently supported method and coverage, else INFERENCE_UNAVAILABLE.
- Independent positive/negative obligations: DGP-021, DGP-002; NEG-002; REF-G01, REF-R01; additionally config omitted/unknown/malformed, operation/target mismatch, upstream-hash mismatch, missing backend, unsupported inference, no silent fallback. SCIENCE DGP/NEG/REF are not generated.
- BLOCKED: actual backend API/version/licence, nuisance/variance algorithm where unsettled, exact K/R/MC-SE/FWER=.05/threshold and oracle. NOT_FROZEN, REGISTRY_NOT_IMPLEMENTED.


### P1-M17 — strict Method contract (PREP-04.1 DRAFT)
- Operation: SENSITIVITY; target: 10_32 semantic target (not assigned canonical enum); owner: P04. Study/Question/Design/Estimand/Graph and content hashes must match.
- Config: REQUIRED clip_lower, clip_upper, diagnostic_spec_ref; strict no unknown keys, no implicit defaults, config={} rejected. Exact type/const/domain constraints in its versioned method_config Schema.
- Question: question_id/research_question/population/analysis_goal/estimand_family/contrast all mandatory, typed, Study-consistent.
- Design: REQUIRED base_effect_hash, propensity_evidence_ref, overlap_assumption_ref plus design_id/question_id/design_kind; explicit roles, assumptions and support validated semantically, never inferred from label. Exact field types in its versioned design_profile Schema.
- Output positive: diagnostics.json; no numeric effect result.json; G01 Publisher/Reader/Manifest/Hash and privacy required. Typed scientific negative can omit positive artifact.
- Inference: requested=false; confidence_level=null; confirmatory requires independently supported method and coverage, else INFERENCE_UNAVAILABLE.
- Independent positive/negative obligations: DGP-002, DGP-023; NEG-010, NEG-018; REF-E02, REF-R01; additionally config omitted/unknown/malformed, operation/target mismatch, upstream-hash mismatch, missing backend, unsupported inference, no silent fallback. SCIENCE DGP/NEG/REF are not generated.
- BLOCKED: actual backend API/version/licence, nuisance/variance algorithm where unsettled, exact K/R/MC-SE/FWER=.05/threshold and oracle. NOT_FROZEN, REGISTRY_NOT_IMPLEMENTED.


### P1-M18 — strict Method contract (PREP-04.1 DRAFT)
- Operation: DIAGNOSE; target: 10_32 semantic target (not assigned canonical enum); owner: P05. Study/Question/Design/Estimand/Graph and content hashes must match.
- Config: REQUIRED negative_control_exposure, explicit_opt_in, null_diagnostic_spec_ref; strict no unknown keys, no implicit defaults, config={} rejected. Exact type/const/domain constraints in its versioned method_config Schema.
- Question: question_id/research_question/population/analysis_goal/estimand_family/contrast all mandatory, typed, Study-consistent.
- Design: REQUIRED outcome, treatment, negative_control_exposure, null_assumption_ref, adjustment_columns plus design_id/question_id/design_kind; explicit roles, assumptions and support validated semantically, never inferred from label. Exact field types in its versioned design_profile Schema.
- Output positive: diagnostics.json; no numeric effect result.json; G01 Publisher/Reader/Manifest/Hash and privacy required. Typed scientific negative can omit positive artifact.
- Inference: requested=false; confidence_level=null; confirmatory requires independently supported method and coverage, else INFERENCE_UNAVAILABLE.
- Independent positive/negative obligations: DGP-019; NEG-019, NEG-026; REF-R02; additionally config omitted/unknown/malformed, operation/target mismatch, upstream-hash mismatch, missing backend, unsupported inference, no silent fallback. SCIENCE DGP/NEG/REF are not generated.
- BLOCKED: actual backend API/version/licence, nuisance/variance algorithm where unsettled, exact K/R/MC-SE/FWER=.05/threshold and oracle. NOT_FROZEN, REGISTRY_NOT_IMPLEMENTED.


### P1-M19 — strict Method contract (PREP-04.1 DRAFT)
- Operation: DIAGNOSE; target: 10_32 semantic target (not assigned canonical enum); owner: P05. Study/Question/Design/Estimand/Graph and content hashes must match.
- Config: REQUIRED negative_control_outcome, explicit_opt_in, null_diagnostic_spec_ref; strict no unknown keys, no implicit defaults, config={} rejected. Exact type/const/domain constraints in its versioned method_config Schema.
- Question: question_id/research_question/population/analysis_goal/estimand_family/contrast all mandatory, typed, Study-consistent.
- Design: REQUIRED outcome, treatment, negative_control_outcome, null_assumption_ref, adjustment_columns plus design_id/question_id/design_kind; explicit roles, assumptions and support validated semantically, never inferred from label. Exact field types in its versioned design_profile Schema.
- Output positive: diagnostics.json; no numeric effect result.json; G01 Publisher/Reader/Manifest/Hash and privacy required. Typed scientific negative can omit positive artifact.
- Inference: requested=false; confidence_level=null; confirmatory requires independently supported method and coverage, else INFERENCE_UNAVAILABLE.
- Independent positive/negative obligations: DGP-019; NEG-019, NEG-026; REF-R02; additionally config omitted/unknown/malformed, operation/target mismatch, upstream-hash mismatch, missing backend, unsupported inference, no silent fallback. SCIENCE DGP/NEG/REF are not generated.
- BLOCKED: actual backend API/version/licence, nuisance/variance algorithm where unsettled, exact K/R/MC-SE/FWER=.05/threshold and oracle. NOT_FROZEN, REGISTRY_NOT_IMPLEMENTED.


### P1-M20 — strict Method contract (PREP-04.1 DRAFT)
- Operation: DIAGNOSE; target: 10_32 semantic target (not assigned canonical enum); owner: P05. Study/Question/Design/Estimand/Graph and content hashes must match.
- Config: REQUIRED q, ols_model_spec_ref, target_coefficient_ref, variance_kind; strict no unknown keys, no implicit defaults, config={} rejected. Exact type/const/domain constraints in its versioned method_config Schema.
- Question: question_id/research_question/population/analysis_goal/estimand_family/contrast all mandatory, typed, Study-consistent.
- Design: REQUIRED outcome, treatment, ols_fit_evidence_ref, degrees_of_freedom plus design_id/question_id/design_kind; explicit roles, assumptions and support validated semantically, never inferred from label. Exact field types in its versioned design_profile Schema.
- Output positive: diagnostics.json; no numeric effect result.json; G01 Publisher/Reader/Manifest/Hash and privacy required. Typed scientific negative can omit positive artifact.
- Inference: requested=false; confidence_level=null; confirmatory requires independently supported method and coverage, else INFERENCE_UNAVAILABLE.
- Independent positive/negative obligations: DGP-020; NEG-020; REF-R03; additionally config omitted/unknown/malformed, operation/target mismatch, upstream-hash mismatch, missing backend, unsupported inference, no silent fallback. SCIENCE DGP/NEG/REF are not generated.
- BLOCKED: actual backend API/version/licence, nuisance/variance algorithm where unsettled, exact K/R/MC-SE/FWER=.05/threshold and oracle. NOT_FROZEN, REGISTRY_NOT_IMPLEMENTED.

Independent backend and science PASS not yet evidenced.


## S02：担当Method Profile・共通署名の規範（G03 / Owner承認）

担当Methodは`P1-M08〜P1-M20`の13件。共通5 Profile Kind（method_config/question_profile/design_profile/output_profile/inference_profile）は`23_api_interface_design/schema_drafts/method_profiles/factored/e11_<kind>_factored_v1.json`のshared core＋Method ID overlayを再構成して使用する。`e11_method_profile_dispatch_registry_draft1.json`とsource Git blob SHAを照合し、200 Profileの標準Draft202012チェック・Method別正負例未確認なら`METHOD_PROFILE_UNAVAILABLE`でfail-closedする。Method別OperationはP1-M08〜11がESTIMATE、M12〜15がREFUTE、M16〜17がSENSITIVITY、M18〜20がDIAGNOSE。後3群は正規`diagnostics.json`であり、架空のEffect Resultを作らない。共通Schema化は各Method固有のATE/ATT/統計量/推論条件を緩和しない。閉objectの別`allOf`合成禁止。実Backend/CIと独立Science DGP/NEG/REF/ACは別途実証が必須。

`LocalRunContext(root:TrustedLocalRoot,principal:LocalPrincipal)`および`LocalPrivacyPolicyPort.authorize(*,study,root,principal,output_shape)`が正規署名。追加のCLI row flag・`cli_row_flag`・`privacy.policy_ref`・独立署名PolicyVerifier/Anchorを実装しない。G05のみStudy `row_export_requested=true`と非root同一UID/private ext4/XFS・Method Schema/capsのANDで個票中間出力可。E11 Local GraphはProduct GraphVersion ID=null、content hashで科学由来を維持。旧Product v2 ABIと共通Scientific Kernelを保護し、無関係Product回帰の全件無条件再試験を課さず、変更影響を証明できない場合は実行またはBLOCK。科学受入・Coding Authorizationは未実施。
