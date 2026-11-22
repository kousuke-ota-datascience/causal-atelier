# Ariadne ENH-E11 G07 — 07 独立テスト指示書：DiD・Event Study・ITS

**Verification contract status: DRAFT / NOT_FROZEN / TESTS_NOT_RUN**
**Owner review: 2026-11-18 JST — PREP-03 audit and G07 Gate-level verification plan reviewed/accepted, with open Method/Profile/Evidence decisions preserved. This is NOT Contract Freeze, Independent Test execution, Gate999 PASS, or Coding Authorization.**
**Gate: G07 / Independent Test Agent / Trial01 NOT_STARTED**
**Dependencies: G01 PASS, G02 PASS (canonical upstream 999)**
**Normative WHAT:** 本書のAC/Test Itemsのみ。テストの実physical path・command・runner discoveryは40 Operatorが所有。
**References:** [10_32 Scientific Method Scope](../../00_enhance_background/Revised_requirements_definition_documents/10_requirements_definition/10_32_scientific_method_scope.md) / [30_61 Domain/Ports](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_61_causal_domain_ports.md) / [30_62 Local Execution](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_62_local_execution_publication.md) / [30_63 Method Adapters](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_63_causal_method_adapters.md) / [23_41 Scientific Ports](../../00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design/23_41_cli_scientific_ports.md) / [23_42 Artifact](../../00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design/23_42_local_result_manifest_artifact.md)

## 0. Independent Gate claim

このGateがPASSしたと主張するには「2×2/staggered DiD、cohort event-time効果、Interrupted Time Series水準/傾き変化を異なるDesign/Estimand/Inferenceとして提供する。」をFull Fixed Candidate SHAで、後述の全受入軸と独立科学的Referenceに照らして証明する。Pxx COMPLETE、CLI exit0、Source上のMethod名、mock-onlyは独立Gate/Science PASSではない。

## 1. Acceptance Criteria (each blocking)

- **AC01 Strict Method/Design/Estimand:** 受理されたMethod×Operation×Target×Question/Design/GraphVersion/HashとInference Policyのみ実行。unknown/mismatch/partial/unidentifiedはtyped negative。
- **AC02 Actual Science:** 各Methodの既知DGP・Negative・独立REF、Backend実測/現行推論API、明示Assumption/Point/UncertaintyとScience status。
- **AC03 Portable Result:** Graph/Effect/Diagnostic/ConfidenceSet/MethodConfig/Provenanceを正しくBundle/Manifest/Readerへ保存し、hash/readback/negativeを確認。
- **AC04 Compatibility/Safety:** G01 FS/Privacy/Atomic/JCSと旧Product v2のprotected interface/behaviorを壊さず、無言fallback/未認可出力がない。
- **AC05 Identity/Independent QA:** Source/lock/fixture SHA、科学事前登録、test-layer、実効環境、Test Item全証拠と正式999判定。

## 2. Required Test Items (file locations are NOT normative)

| ID | Primary purpose | Primary verification layer | Required observable evidence |
|---|---|---|---|
| `G07-07-01` | Panel/Timing/Quasi Design適格性（cross-cutting） | unit/contract + required integration | cohort/intervention time/reference period/cluster；適格positive/negative・typed Reason |
| `G07-07-02` | DiDとEvent Study Adapter（P3-M04, P3-M05） | contract + real backend integration + independent reference | 2×2/staggered区別、pretrend、cluster inference；適格positive/negative・typed Reason |
| `G07-07-03` | InterruptedTsAdapter（P3-M06） | contract + real backend integration + independent reference | level/slope、seasonality/autocorrelation/HAC；適格positive/negative・typed Reason |
| `G07-07-04` | Quasi Result/CLIと独立科学（cross-cutting） | unit/contract + required integration | REF-Q01/Q02、timing negatives、legacy；適格positive/negative・typed Reason |
| `G07-07-05` | Whole Local CLI/Port/Artifact integration | contract + real CLI/FS integration | Strict Operation, Hash, Manifest, Reader, privacy, negative Error status |
| `G07-07-06` | Protected v2/upstream contracts | current actual legacy suite + E11 integration | Upstream 999 invariants, no old v2 CLI/Result change |
| `G07-07-07` | Independent Science/T2/T3 | independently verified reference + real backend integration | Method-specific DGP/NEG/REF, prereg K/R/seed/compute, predeclared quantitative decision |
| `001` | Candidate identity | repository provenance audit | Candidate full SHA, actual checkout, test-only diff classification |
| `999` | Formal Gate decision | independent 30 reports | All blocking items PASS, verified FAIL or BLOCKED and owner action |

**Browser E2E:** 本E11 ScopeはCLI-firstで新規Web UIを実装しないため、当該Gateの新規Browser E2E blocking journeyは**N/A**。既存Productのaffected Browser journeyはRegression対象となり得る。将来UIを本GateScopeへ変更する場合は07の正式Amendment・再Freezeとcritical journey・command・environment・synchronization記述を先行させる。

## 3. Method-by-Method Scientific test obligations

| Method / DD-ID | Target | DGP/NEG / REF | Required evidence / decision |
|---|---|---|---|
| `P3-M04` / `DD-E11-METH-P304` | DiD ATT | DGP-012, DGP-013; NEG-022 / REF-Q01 | PLAN:G07 / OWNER_ESTIMATOR_INFERENCE_POLICY_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED / AC-D03, AC-P01, AC-P03, AC-I01, AC-I02, AC-Q01；Method-specific science/CI未確定ならBLOCKED |
| `P3-M05` / `DD-E11-METH-P305` | Event Study | DGP-013; NEG-022 / REF-Q01 | PLAN:G07 / OWNER_ESTIMATOR_INFERENCE_POLICY_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED / AC-D03, AC-P01, AC-P03, AC-I01, AC-I02, AC-Q01；Method-specific science/CI未確定ならBLOCKED |
| `P3-M06` / `DD-E11-METH-P306` | level/slope change | DGP-014; NEG-023 / REF-Q02 | PLAN:G07 / OWNER_ESTIMATOR_INFERENCE_POLICY_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED / AC-D03, AC-P01, AC-P03, AC-I01, AC-I02, AC-Q02；Method-specific science/CI未確定ならBLOCKED |

**Independent oracle and numerical rule:** DGP truthとEstimator/Backend outputは別Authority。Fixed generator/Reference SHA、既知EstimandとAssumptions、negative/statusを先に登録。Deterministic schema/JCS/roundtripは100%一致。Stochastic ScienceはT2 PilotとT3正式事前登録を分離し、多重性K/FWER=0.05、K/R/seed/threshold/computeは科学決定に基づきFreeze。未確定を推測で補完せず該当Test Item BLOCKED。


**Owner採用 OD-05（2026-11-19）：** G07の3 Methodについて、既決Target/数理は変更せず、担当Pxxでそれぞれstrict versioned `Method Config / Question / Design / Output / Inference Profile`を独立に定義・登録する。Method固有の確認項目は「DiD 2x2 vs staggered ATT、event-time reference cohort/period、cluster covariance、ITS介入時点のlevel/slope/HAC/serial dependence」。条件付き必須Field、Backend effective API/version/optional extras、positive/invalid-config/wrong-target/unsupported-CI/negative-science fixtureとtyped reasonを固定する。未登録/未検証は`METHOD_PROFILE_UNAVAILABLE`等でfail-closed。単なる`config={}`、Backend default、未生成DGP/REF、K/R/MC-SE未実測をPASSとしない。これはProfile作成の**担当配分採用**であり、個々のSchema/Inference/科学Referenceの完成・Freeze・Coding Authorizationを意味しない。

**Independent acceptance for every G07 Method:** valid config/Question/Design/output/Inference positive, extra unknown-property/missing conditional field/wrong target/Graph or DataRef hash/backend mismatch/unsupported CI negatives, deployed real backend API and independent DGP/REF must be separately evidenced. G01/G10 Gateway PASS must not infer scientific proof from schema shape.

## 4. Verification operation, evidence and decision

- Fixed Trial Candidate SHAと実効checkoutが同じsemantic implementation stateか監査。上流Gateのcanonical 999 PASSとprotected contractをSource上の根拠で照合。
- 40 Test Agentは`tests/enhancement/enh_e11/<gate>/`を始点に、関連する`tests/product/`/`tests/integration/`等を現物から発見、test existence/collection/fixture/conftest/dependencies/runner/FS/backendを確認。07にhistorical filename/commandを固定しない。
- Test evidenceにはItem ID/DD ID、actual path/command、source/fixture/lock SHA、effective OS/FS/backend、Known truth/observed output、positive+negative、PASS/FAIL/BLOCKEDと原因を記録。Evidence commitとCandidate SHAを混同しない。
- Independent Test Agentはproduct/test code/runner/CI/06/07を修復しない。Product不変違反を実証したときFAIL、Test-side/UNKNOWN/Backend/独立Oracle不足でProduct判定不能ならBLOCKED。
- G01〜G10各Gateの999は独立であり、Methodごとの未実施・Science未検証・Protected Regression欠落がある限りGate PASS禁止。

## 5. Freeze前のOwner/Science review

staggered TWFEの無条件受容、pretrend非棄却を並行トレンド証明、ITS自己相関無視を禁止。

Method-specific strict Schema・positive/negative・独立Reference/推論Method/CI・threshold・Backend/License・Gate境界/depends/quant computeをレビューし、07をFreezeして初めて実行可能。現時点ではTest NOT_RUN、999 NOT_EXECUTED。


## PREP-04.1 independent strict Method verification (DRAFT)

### P3-M04 — strict Method contract (PREP-04.1 DRAFT / NOT_FROZEN)
- Scientific operation ESTIMATE, target=ATT, owner P01. Preserve DiD2x2/staggered/event-time/ITS/RD/B0/B1 distinct targets and Estimands; B0 LATE is not B1 structural IV coefficient.
- Config mandatory fields: design_variant, estimator_spec_ref, cluster_covariance_spec_ref. Strict type/const/domain as versioned method_config Schema, no unknown keys/defaults, reject config={}.
- Question mandatory: question_id, research_question, population, analysis_goal, estimand_family, contrast. Compare with Study/Design and upstream identification/graph hashes.
- Design mandatory: design_id, question_id, design_kind and unit_id, time_id, treatment, outcome, parallel_trends_assumption_ref. Panel units/cohorts/time, cutoff continuity, IV assumption declarations and first-stage support validated semantically; references do not establish assumptions as true.
- Output: positive result.json/e11-local-effect-result/1 and G01 Reader/Marker/Manifest/Hash. P3-M05 Event Study must write its already specified typed event_time_effects.json vector; ITS level/slope components retain their separate Method-specific output rules. Neither can be coerced to a scalar point.value or an AR confidence-set. Unavailable components require typed reason.
- Inference: requested=false/null or true/confidence-level(0,1) accepted as syntax only; actual method-specific finite/AR CI capability and coverage must be independently validated, otherwise INFERENCE_UNAVAILABLE. B0/B1 HC1 AR formula/authority discrepancy remains BLOCKED.
- Independent tests DGP-012, DGP-013; NEG-022; REF-Q01. In addition empty/unknown key/wrong type or target, wrong temporal/cohort/cutoff/IV roles, absent assumption refs, weak/rank-deficient first stage, backend mismatch, unsupported CI and mis-hashed upstream rejected. Do not turn scientific negatives into technical failures or fallback.
- OPEN: actual backend API/License, proven inferential procedure, independent DGP/NEG/REF and prespecified K/R/FWER 0.05/MC-SE/coverage decision. NOT_FROZEN.


### P3-M05 — strict Method contract (PREP-04.1 DRAFT / NOT_FROZEN)
- Scientific operation ESTIMATE, target=10_32 semantic target (not assigned canonical enum), owner P01. Preserve DiD2x2/staggered/event-time/ITS/RD/B0/B1 distinct targets and Estimands; B0 LATE is not B1 structural IV coefficient.
- Config mandatory fields: event_window_start, event_window_end, reference_event_time, cohort_estimator_spec_ref, cluster_covariance_spec_ref. Strict type/const/domain as versioned method_config Schema, no unknown keys/defaults, reject config={}.
- Question mandatory: question_id, research_question, population, analysis_goal, estimand_family, contrast. Compare with Study/Design and upstream identification/graph hashes.
- Design mandatory: design_id, question_id, design_kind and unit_id, time_id, treatment, outcome, cohort_id, pretrend_assumption_ref. Panel units/cohorts/time, cutoff continuity, IV assumption declarations and first-stage support validated semantically; references do not establish assumptions as true.
- Output: positive result.json/e11-local-effect-result/1 and G01 Reader/Marker/Manifest/Hash. P3-M05 Event Study must write its already specified typed event_time_effects.json vector; ITS level/slope components retain their separate Method-specific output rules. Neither can be coerced to a scalar point.value or an AR confidence-set. Unavailable components require typed reason.
- Inference: requested=false/null or true/confidence-level(0,1) accepted as syntax only; actual method-specific finite/AR CI capability and coverage must be independently validated, otherwise INFERENCE_UNAVAILABLE. B0/B1 HC1 AR formula/authority discrepancy remains BLOCKED.
- Independent tests DGP-013; NEG-022; REF-Q01. In addition empty/unknown key/wrong type or target, wrong temporal/cohort/cutoff/IV roles, absent assumption refs, weak/rank-deficient first stage, backend mismatch, unsupported CI and mis-hashed upstream rejected. Do not turn scientific negatives into technical failures or fallback.
- OPEN: actual backend API/License, proven inferential procedure, independent DGP/NEG/REF and prespecified K/R/FWER 0.05/MC-SE/coverage decision. NOT_FROZEN.


### P3-M06 — strict Method contract (PREP-04.1 DRAFT / NOT_FROZEN)
- Scientific operation ESTIMATE, target=10_32 semantic target (not assigned canonical enum), owner P02. Preserve DiD2x2/staggered/event-time/ITS/RD/B0/B1 distinct targets and Estimands; B0 LATE is not B1 structural IV coefficient.
- Config mandatory fields: effect_components, trend_spec_ref, serial_covariance_spec_ref. Strict type/const/domain as versioned method_config Schema, no unknown keys/defaults, reject config={}.
- Question mandatory: question_id, research_question, population, analysis_goal, estimand_family, contrast. Compare with Study/Design and upstream identification/graph hashes.
- Design mandatory: design_id, question_id, design_kind and time_index, outcome, intervention_time, seasonality_spec_ref, autocorrelation_evidence_ref. Panel units/cohorts/time, cutoff continuity, IV assumption declarations and first-stage support validated semantically; references do not establish assumptions as true.
- Output: positive result.json/e11-local-effect-result/1 and G01 Reader/Marker/Manifest/Hash. P3-M05 Event Study must write its already specified typed event_time_effects.json vector; ITS level/slope components retain their separate Method-specific output rules. Neither can be coerced to a scalar point.value or an AR confidence-set. Unavailable components require typed reason.
- Inference: requested=false/null or true/confidence-level(0,1) accepted as syntax only; actual method-specific finite/AR CI capability and coverage must be independently validated, otherwise INFERENCE_UNAVAILABLE. B0/B1 HC1 AR formula/authority discrepancy remains BLOCKED.
- Independent tests DGP-014; NEG-023; REF-Q02. In addition empty/unknown key/wrong type or target, wrong temporal/cohort/cutoff/IV roles, absent assumption refs, weak/rank-deficient first stage, backend mismatch, unsupported CI and mis-hashed upstream rejected. Do not turn scientific negatives into technical failures or fallback.
- OPEN: actual backend API/License, proven inferential procedure, independent DGP/NEG/REF and prespecified K/R/FWER 0.05/MC-SE/coverage decision. NOT_FROZEN.


## S02簡素化・G07 Quasi Method/Vector Outputの規範

担当Methodは`P3-M04` DiD、`P3-M05` Event Study、`P3-M06` ITSの3件。`23_api_interface_design/schema_drafts/method_profiles/factored/e11_<kind>_factored_v1.json`の5 kind（method_config/question_profile/design_profile/output_profile/inference_profile）からshared＋Method overlayを単一strict Schemaとして再構築し、Dispatch Registry、Blob SHA/標準Draft202012/parity/Method別正負例の証拠がなければ`METHOD_PROFILE_UNAVAILABLE`。DiDの2x2/staggered、Event Studyのcohort/time/reference period、ITSのlevel/slope/HAC/autocorrelationを混同しない。P3-M05ではscalar `result.json`のpointを`NOT_AVAILABLE`とし、cohort×event-timeのtyped `event_time_effects.json`と独立Manifest/ContentRefを発行。推論は実Method/Backendで対応が証明された場合のみAVAILABLE、指定period前のpretrend/介入時点負例とCI shape/Graph・Study lineageを独立07で検証する。

Contextは`LocalRunContext(root,principal)`、Privacy Portは`authorize(*,study,root,principal,output_shape)`。署名Verifier/Policy Anchor・`cli_row_flag`・Study `policy_ref`・追加CLI opt-inを設けない。個票はG05だけがStudy `row_export_requested=true`と非root同一UID private ext4/XFS/Method別capsをANDしてG01 Sinkへ。旧Product v2と共通KernelのABIを保護、科学Oracleと実Backend/CIを未実行ならScience BLOCKED。全Product Suite無条件実行ではなく影響閉包で回帰を決定、不明なら実行またはBLOCK。

## S09 documented Event Study vector contract — P3-M05 (2026-11-22)

P3-M05 `ESTIMATE` has an **event-time/cohort effect vector**, not a scalar target. For an eligible Event Study run, `result.json` has nested `point.availability=NOT_AVAILABLE`, `point.value=null`, `point.reason.code=NON_SCALAR_TARGET`, while `status.json` has top-level `point_availability=NOT_AVAILABLE`; the Manifest must inventory `event_time_effects.json` conforming to `schema_drafts/internal_scientific/e11_event_time_effects_draft1.schema.json`. It binds `method_id=P3-M05`, `study_ref`, `reference_period`, `time_unit`, cohort/event-time keyed `effects`, inference availability/interval references and `pretrend_diagnostics_ref`. The designated reference period and cohort/time support must be predeclared; unique event-time/cohort keys, finite effects, no invalid pretrend concealment, and exact readback/hash/lineage are required. Do not synthesize a scalar ATT/ATE from the vector or substitute an AR confidence set. Other Methods (DiD/ITS) retain their distinct output/inference contracts.

**Independent 07 required tests:** Positive fixed-truth event-time/cohort vector, predeclared reference period, correct `result.point.availability=NOT_AVAILABLE` / `result.point.reason.code=NON_SCALAR_TARGET` + typed artifact + full readback; negatives for omitted/tampered vector, duplicate cohort×time, shifted reference period, unsupported cohort/time, wrong Method/Study hash, fabricated scalar point or CI, and pretrend evidence omission. No independently fixed truth / negative fixture => BLOCKED.
