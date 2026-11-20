# Ariadne ENH-E11 G09 — 07 独立テスト指示書：Synthetic Control・Synthetic DiD

**Verification contract status: DRAFT / NOT_FROZEN / TESTS_NOT_RUN**
**Owner review: 2026-11-18 JST — PREP-03 audit and G09 Gate-level verification plan reviewed/accepted, with open Method/Profile/Evidence decisions preserved. This is NOT Contract Freeze, Independent Test execution, Gate999 PASS, or Coding Authorization.**
**Gate: G09 / Independent Test Agent / Trial01 NOT_STARTED**
**Dependencies: G01 PASS (canonical upstream 999)**
**Normative WHAT:** 本書のAC/Test Itemsのみ。テストの実physical path・command・runner discoveryは40 Operatorが所有。
**References:** [10_32 Scientific Method Scope](../../00_enhance_background/Revised_requirements_definition_documents/10_requirements_definition/10_32_scientific_method_scope.md) / [30_61 Domain/Ports](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_61_causal_domain_ports.md) / [30_62 Local Execution](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_62_local_execution_publication.md) / [30_63 Method Adapters](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_63_causal_method_adapters.md) / [23_41 Scientific Ports](../../00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design/23_41_cli_scientific_ports.md) / [23_42 Artifact](../../00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design/23_42_local_result_manifest_artifact.md)

## 0. Independent Gate claim

このGateがPASSしたと主張するには「汚染のないdonor/事前適合性を検査し、SCM point-only反事実ギャップとSDID panel平均効果の異なる対象を正確に記録する。」をFull Fixed Candidate SHAで、後述の全受入軸と独立科学的Referenceに照らして証明する。Pxx COMPLETE、CLI exit0、Source上のMethod名、mock-onlyは独立Gate/Science PASSではない。

## 1. Acceptance Criteria (each blocking)

- **AC01 Strict Method/Design/Estimand:** 受理されたMethod×Operation×Target×Question/Design/GraphVersion/HashとInference Policyのみ実行。unknown/mismatch/partial/unidentifiedはtyped negative。
- **AC02 Actual Science:** 各Methodの既知DGP・Negative・独立REF、Backend実測/現行推論API、明示Assumption/Point/UncertaintyとScience status。
- **AC03 Portable Result:** Graph/Effect/Diagnostic/ConfidenceSet/MethodConfig/Provenanceを正しくBundle/Manifest/Readerへ保存し、hash/readback/negativeを確認。
- **AC04 Compatibility/Safety:** G01 FS/Privacy/Atomic/JCSと旧Product v2のprotected interface/behaviorを壊さず、無言fallback/未認可出力がない。
- **AC05 Identity/Independent QA:** Source/lock/fixture SHA、科学事前登録、test-layer、実効環境、Test Item全証拠と正式999判定。

## 2. Required Test Items (file locations are NOT normative)

| ID | Primary purpose | Primary verification layer | Required observable evidence |
|---|---|---|---|
| `G09-07-01` | Donor pool/Panel Design（cross-cutting） | unit/contract + required integration | preperiod eligibility/contamination/treated unit；適格positive/negative・typed Reason |
| `G09-07-02` | Synthetic Control Adapter（P3-M12） | contract + real backend integration + independent reference | donor weights/RMSPE/placebo/point-only；適格positive/negative・typed Reason |
| `G09-07-03` | Synthetic DiD Adapter（P3-M13） | contract + real backend integration + independent reference | time/unit weights・panel ATT・inference；適格positive/negative・typed Reason |
| `G09-07-04` | SCM/SDID Result/CLI・独立科学（cross-cutting） | unit/contract + required integration | REF-Q04/Q05とnegative；適格positive/negative・typed Reason |
| `G09-07-05` | Whole Local CLI/Port/Artifact integration | contract + real CLI/FS integration | Strict Operation, Hash, Manifest, Reader, privacy, negative Error status |
| `G09-07-06` | Protected v2/upstream contracts | current actual legacy suite + E11 integration | Upstream 999 invariants, no old v2 CLI/Result change |
| `G09-07-07` | Independent Science/T2/T3 | independently verified reference + real backend integration | Method-specific DGP/NEG/REF, prereg K/R/seed/compute, predeclared quantitative decision |
| `001` | Candidate identity | repository provenance audit | Candidate full SHA, actual checkout, test-only diff classification |
| `999` | Formal Gate decision | independent 30 reports | All blocking items PASS, verified FAIL or BLOCKED and owner action |

**Browser E2E:** 本E11 ScopeはCLI-firstで新規Web UIを実装しないため、当該Gateの新規Browser E2E blocking journeyは**N/A**。既存Productのaffected Browser journeyはRegression対象となり得る。将来UIを本GateScopeへ変更する場合は07の正式Amendment・再Freezeとcritical journey・command・environment・synchronization記述を先行させる。

## 3. Method-by-Method Scientific test obligations

| Method / DD-ID | Target | DGP/NEG / REF | Required evidence / decision |
|---|---|---|---|
| `P3-M12` / `DD-E11-METH-P312` | treated-unit counterfactual gap | DGP-017; NEG-024 / REF-Q04 | PLAN:G09 / OWNER_BASELINE_ACCEPTED_POINT_ONLY_SCIENCE_PENDING / NOT_GENERATED / AC-D03, AC-P01, AC-P03, AC-Q04；Method-specific science/CI未確定ならBLOCKED |
| `P3-M13` / `DD-E11-METH-P313` | panel average effect | DGP-018; NEG-024 / REF-Q05 | PLAN:G09 / OWNER_ESTIMATOR_INFERENCE_POLICY_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED / AC-D03, AC-P01, AC-P03, AC-I01, AC-I02, AC-Q05；Method-specific science/CI未確定ならBLOCKED |

**Independent oracle and numerical rule:** DGP truthとEstimator/Backend outputは別Authority。Fixed generator/Reference SHA、既知EstimandとAssumptions、negative/statusを先に登録。Deterministic schema/JCS/roundtripは100%一致。Stochastic ScienceはT2 PilotとT3正式事前登録を分離し、多重性K/FWER=0.05、K/R/seed/threshold/computeは科学決定に基づきFreeze。未確定を推測で補完せず該当Test Item BLOCKED。


**Owner採用 OD-05（2026-11-19）：** G09の2 Methodについて、既決Target/数理は変更せず、担当Pxxでそれぞれstrict versioned `Method Config / Question / Design / Output / Inference Profile`を独立に定義・登録する。Method固有の確認項目は「SCM donor selection/preperiod fit/point-only、SDID unit/time weights/panel inference、contamination/supportとcounterfactual gap」。条件付き必須Field、Backend effective API/version/optional extras、positive/invalid-config/wrong-target/unsupported-CI/negative-science fixtureとtyped reasonを固定する。未登録/未検証は`METHOD_PROFILE_UNAVAILABLE`等でfail-closed。単なる`config={}`、Backend default、未生成DGP/REF、K/R/MC-SE未実測をPASSとしない。これはProfile作成の**担当配分採用**であり、個々のSchema/Inference/科学Referenceの完成・Freeze・Coding Authorizationを意味しない。

**Independent acceptance for every G09 Method:** valid config/Question/Design/output/Inference positive, extra unknown-property/missing conditional field/wrong target/Graph or DataRef hash/backend mismatch/unsupported CI negatives, deployed real backend API and independent DGP/REF must be separately evidenced. G01/G10 Gateway PASS must not infer scientific proof from schema shape.

## 4. Verification operation, evidence and decision

- Fixed Trial Candidate SHAと実効checkoutが同じsemantic implementation stateか監査。上流Gateのcanonical 999 PASSとprotected contractをSource上の根拠で照合。
- 40 Test Agentは`tests/enhancement/enh_e11/<gate>/`を始点に、関連する`tests/product/`/`tests/integration/`等を現物から発見、test existence/collection/fixture/conftest/dependencies/runner/FS/backendを確認。07にhistorical filename/commandを固定しない。
- Test evidenceにはItem ID/DD ID、actual path/command、source/fixture/lock SHA、effective OS/FS/backend、Known truth/observed output、positive+negative、PASS/FAIL/BLOCKEDと原因を記録。Evidence commitとCandidate SHAを混同しない。
- Independent Test Agentはproduct/test code/runner/CI/06/07を修復しない。Product不変違反を実証したときFAIL、Test-side/UNKNOWN/Backend/独立Oracle不足でProduct判定不能ならBLOCKED。
- G01〜G10各Gateの999は独立であり、Methodごとの未実施・Science未検証・Protected Regression欠落がある限りGate PASS禁止。

## 5. Freeze前のOwner/Science review

SCM point-onlyにCIを捏造、donor contamination、事後選択の無言許可を禁止。

Method-specific strict Schema・positive/negative・独立Reference/推論Method/CI・threshold・Backend/License・Gate境界/depends/quant computeをレビューし、07をFreezeして初めて実行可能。現時点ではTest NOT_RUN、999 NOT_EXECUTED。


## PREP-04.1 independent Method acceptance (NOT_FROZEN)

### P3-M12 (PREP-04.1 STRICT DRAFT / NOT_FROZEN)
- ESTIMATE target: 10_32 semantic target (not assigned canonical enum); Pxx owner=P01; SCM treated-unit gap and SDID panel-average effect are not interchangeable.
- Config required fields: weight_objective_spec_ref, preperiod_fit_spec_ref, donor_eligibility_spec_ref; types/const/ranges in method_config JSON Schema, no unknown keys/defaults; config={} fails.
- Question required: question_id/research_question/population/analysis_goal/estimand_family/contrast, matched against Study.
- Design required: design_id/question_id/design_kind; treated_unit, donor_units, time_index, preperiod_end, intervention_time, no_donor_contamination_ref; validate donor/treatment contamination, pre-period support, time ordering, upstream content hashes and panel eligibility.
- Positive output result.json/e11-local-effect-result/1; G01 hash/marker/manifest/Reader; privacy row output requires G05 approval. Negative case returns typed reason, not fake effect.
- Inference: SCM point-only; requested=false, confidence_level=null; no placebo interval.
- Independent DGP/NEG/REF DGP-017; NEG-024; REF-Q04 plus empty/unknown Config, wrong target/Time/Donor, pre-period leakage, missing upstream hash, backend unavailable, unsupported CI. Backend/License/independent oracle/K/R/FWER=.05/MC-SE/coverage not verified.


### P3-M13 (PREP-04.1 STRICT DRAFT / NOT_FROZEN)
- ESTIMATE target: 10_32 semantic target (not assigned canonical enum); Pxx owner=P02; SCM treated-unit gap and SDID panel-average effect are not interchangeable.
- Config required fields: unit_weights_spec_ref, time_weights_spec_ref, variance_spec_ref, donor_eligibility_spec_ref; types/const/ranges in method_config JSON Schema, no unknown keys/defaults; config={} fails.
- Question required: question_id/research_question/population/analysis_goal/estimand_family/contrast, matched against Study.
- Design required: design_id/question_id/design_kind; treated_units, donor_units, time_index, preperiod_end, intervention_time, panel_support_ref; validate donor/treatment contamination, pre-period support, time ordering, upstream content hashes and panel eligibility.
- Positive output result.json/e11-local-effect-result/1; G01 hash/marker/manifest/Reader; privacy row output requires G05 approval. Negative case returns typed reason, not fake effect.
- Inference: Requested confidence_level (0,1) is syntax only; SDID CI requires separately approved variance and independent coverage.
- Independent DGP/NEG/REF DGP-018; NEG-024; REF-Q05 plus empty/unknown Config, wrong target/Time/Donor, pre-period leakage, missing upstream hash, backend unavailable, unsupported CI. Backend/License/independent oracle/K/R/FWER=.05/MC-SE/coverage not verified.
