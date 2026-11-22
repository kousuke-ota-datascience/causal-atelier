# Ariadne ENH-E11 G02 — 07 独立テスト指示書：Identification・Eligibility・optional DoWhy

**DEC-PREPCODE-01=B（Owner 2026-11-22採用）：Gate別S09→S10→S11。** G02の独立S09監査は、先行Gate（G01）と共通E11 Wire/Port/Privacy/JCS/Publisher/Reader/Protected v2の変更影響閉包、およびG02自身の06/P00/Pxx/07/Method Profile/Backend/Scienceを対象とする。対象外Gateは全体SHA inventoryに保持し`NOT_REVIEWED`、未決の後続MethodはG02のCoding前無条件停止条件にしない。**G01_999の実PASS→独立G02 S09 verdict→Owner G02-S10 Freeze→Owner G02-S11 Coding Authorization**を各々確認するまでG02のCoding禁止。実Adapter/FS/数値T2/T3/RegressionはG02の独立07/999で検証し、文書修正だけでPASSを付けない。現時点は`S09_NOT_RUN/S10_NOT_FROZEN/S11_NOT_AUTHORIZED`。

**Verification contract status: DRAFT / NOT_FROZEN / TESTS_NOT_RUN**
**Owner review: 2026-11-18 JST — PREP-03 audit and G02 Gate-level verification plan reviewed/accepted, with open Method/Profile/Evidence decisions preserved. This is NOT Contract Freeze, Independent Test execution, Gate999 PASS, or Coding Authorization.**
**Gate: G02 / Independent Test Agent / Trial01 NOT_STARTED**
**Dependencies: G01 PASS (canonical upstream 999)**
**Normative WHAT:** 本書のAC/Test Itemsのみ。テストの実physical path・command・runner discoveryは40 Operatorが所有。
**References:** [10_32 Scientific Method Scope](../../00_enhance_background/Revised_requirements_definition_documents/10_requirements_definition/10_32_scientific_method_scope.md) / [30_61 Domain/Ports](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_61_causal_domain_ports.md) / [30_62 Local Execution](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_62_local_execution_publication.md) / [30_63 Method Adapters](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_63_causal_method_adapters.md) / [23_41 Scientific Ports](../../00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design/23_41_cli_scientific_ports.md) / [23_42 Artifact](../../00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design/23_42_local_result_manifest_artifact.md)

## 0. Independent Gate claim

このGateがPASSしたと主張するには「Native/DoWhyで識別可能性・非識別・Reviewを型付きで区別し、識別ProofとEstimandが適合しない推定を阻止する。限定線形FD-AはFrontdoor識別と数値推定を分離する。」をFull Fixed Candidate SHAで、後述の全受入軸と独立科学的Referenceに照らして証明する。Pxx COMPLETE、CLI exit0、Source上のMethod名、mock-onlyは独立Gate/Science PASSではない。

## 1. Acceptance Criteria (each blocking)

- **AC01 Strict Method/Design/Estimand:** 受理されたMethod×Operation×Target×Question/Design/GraphVersion/HashとInference Policyのみ実行。unknown/mismatch/partial/unidentifiedはtyped negative。
- **AC02 Actual Science:** 各Methodの既知DGP・Negative・独立REF、Backend実測/現行推論API、明示Assumption/Point/UncertaintyとScience status。
- **AC03 Portable Result:** Graph/Effect/Diagnostic/ConfidenceSet/MethodConfig/Provenanceを正しくBundle/Manifest/Readerへ保存し、hash/readback/negativeを確認。
- **AC04 Compatibility/Safety:** G01 FS/Privacy/Atomic/JCSと旧Product v2のprotected interface/behaviorを壊さず、無言fallback/未認可出力がない。
- **AC05 Identity/Independent QA:** Source/lock/fixture SHA、科学事前登録、test-layer、実効環境、Test Item全証拠と正式999判定。

## 2. Required Test Items (file locations are NOT normative)

| ID | Primary purpose | Primary verification layer | Required observable evidence |
|---|---|---|---|
| `G02-07-01` | Native randomized/backdoor識別（P1-M01, P1-M02） | contract + real backend integration + independent reference | Design/GraphVersion/Proof・IdentificationOutcome；適格positive/negative・typed Reason |
| `G02-07-02` | DoWhy optional backdoor/frontdoor/IV識別（P1-M03, P1-M04, P1-M05） | contract + real backend integration + independent reference | Effective API/Backend・Owner採用B0 conditional LATEと実効DoWhy IV証明、missing profileはtyped BLOCK；適格positive/negative・typed Reason |
| `G02-07-03` | FD-A限定線形two-stage推定（P1-M07） | contract + real backend integration + independent reference | single mediator・no direct path・独立数値Reference；適格positive/negative・typed Reason |
| `G02-07-04` | Identification→Estimator eligibility・Local CLI（cross-cutting） | unit/contract + required integration | Hash/Estimand/Proof/Reason・旧v2回帰；適格positive/negative・typed Reason |
| `G02-07-05` | Whole Local CLI/Port/Artifact integration | contract + real CLI/FS integration | Strict Operation, Hash, Manifest, Reader, privacy, negative Error status |
| `G02-07-06` | Protected v2/upstream contracts | current actual legacy suite + E11 integration | Upstream 999 invariants, no old v2 CLI/Result change |
| `G02-07-07` | Independent Science/T2/T3 | independently verified reference + real backend integration | Method-specific DGP/NEG/REF, prereg K/R/seed/compute, predeclared quantitative decision |
| `001` | Candidate identity | repository provenance audit | Candidate full SHA, actual checkout, test-only diff classification |
| `999` | Formal Gate decision | independent 30 reports | All blocking items PASS, verified FAIL or BLOCKED and owner action |

**Browser E2E:** 本E11 ScopeはCLI-firstで新規Web UIを実装しないため、当該Gateの新規Browser E2E blocking journeyは**N/A**。既存Productのaffected Browser journeyはRegression対象となり得る。将来UIを本GateScopeへ変更する場合は07の正式Amendment・再Freezeとcritical journey・command・environment・synchronization記述を先行させる。

## 3. Method-by-Method Scientific test obligations

| Method / DD-ID | Target | DGP/NEG / REF | Required evidence / decision |
|---|---|---|---|
| `P1-M01` / `DD-E11-METH-P101` | randomized identification | DGP-001; NEG-001, NEG-027 / REF-G01, REF-I01 | PLAN:G02 / CONFIG_AND_AC_PENDING / NOT_GENERATED / AC-D01, AC-D02, AC-D07；Method-specific science/CI未確定ならBLOCKED |
| `P1-M02` / `DD-E11-METH-P102` | backdoor ATE | DGP-002, DGP-021; NEG-002, NEG-003 / REF-G01, REF-I01 | PLAN:G02 / CONFIG_AND_AC_PENDING / NOT_GENERATED / AC-D01, AC-D02, AC-D07；Method-specific science/CI未確定ならBLOCKED |
| `P1-M03` / `DD-E11-METH-P103` | backdoor ATE | DGP-002, DGP-021; NEG-002, NEG-027 / REF-G01, REF-I01 | PLAN:G02 / CONFIG_AND_AC_PENDING / NOT_GENERATED / AC-D01, AC-D02, AC-D07；Method-specific science/CI未確定ならBLOCKED |
| `P1-M04` / `DD-E11-METH-P104` | frontdoor ATE | DGP-005; NEG-004 / REF-G01, REF-I02 | PLAN:G02 / CONFIG_AND_AC_PENDING / NOT_GENERATED / AC-D01, AC-D02, AC-D07；Method-specific science/CI未確定ならBLOCKED |
| `P1-M05` / `DD-E11-METH-P105` | B0 conditional `LATE_COMPLIER` identification | DGP-006; NEG-006, NEG-007 / REF-I03, REF-G01 | PLAN:G02 / OWNER_TARGET_ADOPTED_PROFILE_BACKEND_SCIENCE_PENDING / NOT_GENERATED / AC-D01, AC-D02, AC-D07；Method-specific science/CI未確定ならBLOCKED |
| `P1-M07` / `DD-E11-METH-P107` | restricted FD-A ATE | DGP-005; NEG-004, NEG-005 / REF-I02, REF-E04 | PLAN:G02 / OWNER_METHOD_ACCEPTED_TECH_AND_SCIENCE_BLOCKED / NOT_GENERATED / AC-D03, AC-P01, AC-P03, AC-I01, AC-I02；Method-specific science/CI未確定ならBLOCKED |

**Independent oracle and numerical rule:** DGP truthとEstimator/Backend outputは別Authority。Fixed generator/Reference SHA、既知EstimandとAssumptions、negative/statusを先に登録。Deterministic schema/JCS/roundtripは100%一致。Stochastic ScienceはT2 PilotとT3正式事前登録を分離し、多重性K/FWER=0.05、K/R/seed/threshold/computeは科学決定に基づきFreeze。未確定を推測で補完せず該当Test Item BLOCKED。

**G02-07-02 P1-M05 independent tests:** DoWhyのeffective runtime/APIとIV expression、正例DGP-006におけるB0二値Z/A/無調整＋宣言済みinstrument assumptionsとconditional `IdentificationOutcome`、NEG-006のfirst stage不十分、NEG-007のexclusion違反、B1/DRIV/ATE混同、missing monotonicity、wrong graph/hash、nonbinary instrument、missing Profile、unsupported backendのtyped negativeを独立に照合。IDENTIFYでは`identification.json`があること、Effect `result.json`・Estimator callがないことをreadback検証。Backend自身のIV labelは独立oracleではない。

**G02 Method Profile gate:** **OD-05採用:** G02のP1-M01〜05・P1-M07（計6 Method）はそれぞれstrict Method Config/Question/Design/Output/Inference Profileを定義・登録し、invalid config/Estimand/Backendとunsupported CIをtyped negativeにする。専用Schema/Backend実測/独立Oracleが未実装なら当該Methodは`METHOD_PROFILE_UNAVAILABLE`等でBLOCKED。採用済Targetの再決定を求めない。 テスト実行までは`TESTS_NOT_RUN`であり、07の記述だけをScience PASSとしない。

## 4. Verification operation, evidence and decision

- Fixed Trial Candidate SHAと実効checkoutが同じsemantic implementation stateか監査。上流Gateのcanonical 999 PASSとprotected contractをSource上の根拠で照合。
- 40 Test Agentは`tests/enhancement/enh_e11/<gate>/`を始点に、関連する`tests/product/`/`tests/integration/`等を現物から発見、test existence/collection/fixture/conftest/dependencies/runner/FS/backendを確認。07にhistorical filename/commandを固定しない。
- Test evidenceにはItem ID/DD ID、actual path/command、source/fixture/lock SHA、effective OS/FS/backend、Known truth/observed output、positive+negative、PASS/FAIL/BLOCKEDと原因を記録。Evidence commitとCandidate SHAを混同しない。
- Independent Test Agentはproduct/test code/runner/CI/06/07を修復しない。Product不変違反を実証したときFAIL、Test-side/UNKNOWN/Backend/独立Oracle不足でProduct判定不能ならBLOCKED。
- G01〜G10各Gateの999は独立であり、Methodごとの未実施・Science未検証・Protected Regression欠落がある限りGate PASS禁止。

## 5. Freeze前のOwner/Science review

P1-M05 Owner採用のB0条件付き`LATE_COMPLIER`をMethod Profile/Designで明示指定する。DoWhy内部IVラベルだけから推測せず、実効IV expression/Assumptions/Graph provenanceを照合する。

Method-specific strict Schema・positive/negative・独立Reference/推論Method/CI・threshold・Backend/License・Gate境界/depends/quant computeをレビューし、07をFreezeして初めて実行可能。現時点ではTest NOT_RUN、999 NOT_EXECUTED。


## PREP-04.1 Method-specific Independent Profile AC (DRAFT / NOT_FROZEN)


### P1-M01: strict Profile authoring draft (PREP-04.1; NOT_FROZEN)
- **Operation / accepted Estimand:** `IDENTIFY` / existing randomized identification target; resolve exact family from legacy source evidence; Backend evidence `ENV-BASE` is an environment obligation, **not** an approved runtime backend selection.
- **Strict Method Config required fields (no defaults):** identification_rule:const(RANDOMIZED_ASSIGNMENT); `additionalProperties=false`; empty config invalid. Config↔Design↔Study must be compared semantically.
- **Question required:** question_id, research_question, population, analysis_goal=IDENTIFICATION, estimand_family, contrast. Study estimand and question estimand must match exactly; M05 population=compliers, contrast=A1−A0.
- **Design required:** design_id, question_id, design_kind, treatment, outcome, allocation_unit, randomization_evidence_ref. Assumption *references* are declarations, not empirical confirmation; validate identities, column roles, dataset support, graph/identification lineage.
- **Output (positive only):** identification.json proof; result.json and numeric Effect forbidden; manifest/status/commit/readback follow G01. Scientific negative may have no positive artifact and must carry typed reason.
- **Inference (Study.inference):** requested=false and confidence_level=null, no estimator/CI. Strict unknown-key rejection.
- **Evidence obligation:** positive DGP-001; negatives NEG-001, NEG-027 plus config={} / unknown-key / wrong-method / wrong-estimand / wrong-backend / missing-ref / unsupported-CI; independent REF-G01, REF-I01; AC-D01, AC-D02, AC-D07. All fixtures/Backend/threshold/Science are NOT_GENERATED/NOT_EVALUATED.
- **Unresolved (BLOCKED before Freeze):**
  - Treatment contrast and target-family equivalence must be checked against existing v2 randomized behavior
  - No empirical proof of randomized assignment is implied by declaration
- **Backend / Science:** independently pin distribution/version/API/License and normative DGP/NEG/REF, quantitative K/R/MC-SE/coverage AC before this Method's acceptance. Backend failure=CAPABILITY_UNAVAILABLE, missing profile=METHOD_PROFILE_UNAVAILABLE, invalid config=CONFIG_INVALID, semantic mismatch=METHOD_INCOMPATIBLE, unsupported interval=INFERENCE_UNAVAILABLE (where mapped by canonical status authority).


### P1-M02: strict Profile authoring draft (PREP-04.1; NOT_FROZEN)
- **Operation / accepted Estimand:** `IDENTIFY` / `ATE`; Backend evidence `ENV-BASE` is an environment obligation, **not** an approved runtime backend selection.
- **Strict Method Config required fields (no defaults):** identification_rule:const(GRAPH_BACKDOOR), adjustment_columns:array; `additionalProperties=false`; empty config invalid. Config↔Design↔Study must be compared semantically.
- **Question required:** question_id, research_question, population, analysis_goal=IDENTIFICATION, estimand_family, contrast. Study estimand and question estimand must match exactly; M05 population=compliers, contrast=A1−A0.
- **Design required:** design_id, question_id, design_kind, treatment, outcome, adjustment_columns, graph_evidence_ref, backdoor_proof_ref. Assumption *references* are declarations, not empirical confirmation; validate identities, column roles, dataset support, graph/identification lineage.
- **Output (positive only):** identification.json proof; result.json and numeric Effect forbidden; manifest/status/commit/readback follow G01. Scientific negative may have no positive artifact and must carry typed reason.
- **Inference (Study.inference):** requested=false and confidence_level=null, no estimator/CI. Strict unknown-key rejection.
- **Evidence obligation:** positive DGP-002,DGP-021; negatives NEG-002, NEG-003 plus config={} / unknown-key / wrong-method / wrong-estimand / wrong-backend / missing-ref / unsupported-CI; independent REF-G01, REF-I01; AC-D01, AC-D02, AC-D07. All fixtures/Backend/threshold/Science are NOT_GENERATED/NOT_EVALUATED.
- **Unresolved (BLOCKED before Freeze):**
  - Graph semantic validator must reject colliders and post-treatment adjustment; empty adjustment set is allowed only if graph-valid
- **Backend / Science:** independently pin distribution/version/API/License and normative DGP/NEG/REF, quantitative K/R/MC-SE/coverage AC before this Method's acceptance. Backend failure=CAPABILITY_UNAVAILABLE, missing profile=METHOD_PROFILE_UNAVAILABLE, invalid config=CONFIG_INVALID, semantic mismatch=METHOD_INCOMPATIBLE, unsupported interval=INFERENCE_UNAVAILABLE (where mapped by canonical status authority).


### P1-M03: strict Profile authoring draft (PREP-04.1; NOT_FROZEN)
- **Operation / accepted Estimand:** `IDENTIFY` / `ATE`; Backend evidence `ENV-DOWHY` is an environment obligation, **not** an approved runtime backend selection.
- **Strict Method Config required fields (no defaults):** identification_rule:const(DOWHY_BACKDOOR), adjustment_columns:array; `additionalProperties=false`; empty config invalid. Config↔Design↔Study must be compared semantically.
- **Question required:** question_id, research_question, population, analysis_goal=IDENTIFICATION, estimand_family, contrast. Study estimand and question estimand must match exactly; M05 population=compliers, contrast=A1−A0.
- **Design required:** design_id, question_id, design_kind, treatment, outcome, adjustment_columns, graph_evidence_ref, backdoor_proof_ref. Assumption *references* are declarations, not empirical confirmation; validate identities, column roles, dataset support, graph/identification lineage.
- **Output (positive only):** identification.json proof; result.json and numeric Effect forbidden; manifest/status/commit/readback follow G01. Scientific negative may have no positive artifact and must carry typed reason.
- **Inference (Study.inference):** requested=false and confidence_level=null, no estimator/CI. Strict unknown-key rejection.
- **Evidence obligation:** positive DGP-002,DGP-021; negatives NEG-002, NEG-027 plus config={} / unknown-key / wrong-method / wrong-estimand / wrong-backend / missing-ref / unsupported-CI; independent REF-G01, REF-I01; AC-D01, AC-D02, AC-D07. All fixtures/Backend/threshold/Science are NOT_GENERATED/NOT_EVALUATED.
- **Unresolved (BLOCKED before Freeze):**
  - Pin effective DoWhy identify_effect signature, returned estimand proof and version; DoWhy display string is not proof
- **Backend / Science:** independently pin distribution/version/API/License and normative DGP/NEG/REF, quantitative K/R/MC-SE/coverage AC before this Method's acceptance. Backend failure=CAPABILITY_UNAVAILABLE, missing profile=METHOD_PROFILE_UNAVAILABLE, invalid config=CONFIG_INVALID, semantic mismatch=METHOD_INCOMPATIBLE, unsupported interval=INFERENCE_UNAVAILABLE (where mapped by canonical status authority).


### P1-M04: strict Profile authoring draft (PREP-04.1; NOT_FROZEN)
- **Operation / accepted Estimand:** `IDENTIFY` / `ATE`; Backend evidence `ENV-DOWHY` is an environment obligation, **not** an approved runtime backend selection.
- **Strict Method Config required fields (no defaults):** identification_rule:const(DOWHY_FRONTDOOR), mediator_column:string; `additionalProperties=false`; empty config invalid. Config↔Design↔Study must be compared semantically.
- **Question required:** question_id, research_question, population, analysis_goal=IDENTIFICATION, estimand_family, contrast. Study estimand and question estimand must match exactly; M05 population=compliers, contrast=A1−A0.
- **Design required:** design_id, question_id, design_kind, treatment, outcome, mediator, graph_evidence_ref, frontdoor_proof_ref. Assumption *references* are declarations, not empirical confirmation; validate identities, column roles, dataset support, graph/identification lineage.
- **Output (positive only):** identification.json proof; result.json and numeric Effect forbidden; manifest/status/commit/readback follow G01. Scientific negative may have no positive artifact and must carry typed reason.
- **Inference (Study.inference):** requested=false and confidence_level=null, no estimator/CI. Strict unknown-key rejection.
- **Evidence obligation:** positive DGP-005; negatives NEG-004 plus config={} / unknown-key / wrong-method / wrong-estimand / wrong-backend / missing-ref / unsupported-CI; independent REF-G01, REF-I02; AC-D01, AC-D02, AC-D07. All fixtures/Backend/threshold/Science are NOT_GENERATED/NOT_EVALUATED.
- **Unresolved (BLOCKED before Freeze):**
  - Frontdoor identification does not authorize linear two-stage effect calculation; test effective DoWhy API and conditions independently
- **Backend / Science:** independently pin distribution/version/API/License and normative DGP/NEG/REF, quantitative K/R/MC-SE/coverage AC before this Method's acceptance. Backend failure=CAPABILITY_UNAVAILABLE, missing profile=METHOD_PROFILE_UNAVAILABLE, invalid config=CONFIG_INVALID, semantic mismatch=METHOD_INCOMPATIBLE, unsupported interval=INFERENCE_UNAVAILABLE (where mapped by canonical status authority).


### P1-M05: strict Profile authoring draft (PREP-04.1; NOT_FROZEN)
- **Operation / accepted Estimand:** `IDENTIFY` / `LATE_COMPLIER`; Backend evidence `ENV-DOWHY` is an environment obligation, **not** an approved runtime backend selection.
- **Strict Method Config required fields (no defaults):** design_profile:const(B0_BINARY_IV), monotonicity_direction:enum(NONDECREASING/NONINCREASING); `additionalProperties=false`; empty config invalid. Config↔Design↔Study must be compared semantically.
- **Question required:** question_id, research_question, population, analysis_goal=IDENTIFICATION, estimand_family, contrast. Study estimand and question estimand must match exactly; M05 population=compliers, contrast=A1−A0.
- **Design required:** design_id, question_id, design_kind, treatment, outcome, instrument, treatment_binary, instrument_binary, adjustment_columns, monotonicity_direction, relevance_assumption_ref, independence_assumption_ref, exclusion_assumption_ref, monotonicity_assumption_ref, consistency_assumption_ref, graph_evidence_ref. Assumption *references* are declarations, not empirical confirmation; validate identities, column roles, dataset support, graph/identification lineage.
- **Output (positive only):** identification.json proof; result.json and numeric Effect forbidden; manifest/status/commit/readback follow G01. Scientific negative may have no positive artifact and must carry typed reason.
- **Inference (Study.inference):** requested=false and confidence_level=null, no estimator/CI. Strict unknown-key rejection.
- **Evidence obligation:** positive DGP-006; negatives NEG-006, NEG-007 plus config={} / unknown-key / wrong-method / wrong-estimand / wrong-backend / missing-ref / unsupported-CI; independent REF-I03, REF-G01; AC-D01, AC-D02, AC-D07. All fixtures/Backend/threshold/Science are NOT_GENERATED/NOT_EVALUATED.
- **Unresolved (BLOCKED before Freeze):**
  - Observe first-stage nonzero: cannot be proved by declaration; distinguish weak-IV evidence from identification logic
  - DoWhy effective API and IV expression must be independently checked; no effect result.json
  - Study contrast A1-A0, population=compliers and cross-field direction consistency are semantic validation, not implied by this JSON
- **Backend / Science:** independently pin distribution/version/API/License and normative DGP/NEG/REF, quantitative K/R/MC-SE/coverage AC before this Method's acceptance. Backend failure=CAPABILITY_UNAVAILABLE, missing profile=METHOD_PROFILE_UNAVAILABLE, invalid config=CONFIG_INVALID, semantic mismatch=METHOD_INCOMPATIBLE, unsupported interval=INFERENCE_UNAVAILABLE (where mapped by canonical status authority).


### P1-M07: strict Profile authoring draft (PREP-04.1; NOT_FROZEN)
- **Operation / accepted Estimand:** `ESTIMATE` / `ATE`; Backend evidence `ENV-DOWHY` is an environment obligation, **not** an approved runtime backend selection.
- **Strict Method Config required fields (no defaults):** estimation_rule:const(FD_A_LINEAR_COEFFICIENT_PRODUCT), mediator_column:string, mediator_model_spec_ref:string, outcome_model_spec_ref:string; `additionalProperties=false`; empty config invalid. Config↔Design↔Study must be compared semantically.
- **Question required:** question_id, research_question, population, analysis_goal=EFFECT_ESTIMATION, estimand_family, contrast. Study estimand and question estimand must match exactly; M05 population=compliers, contrast=A1−A0.
- **Design required:** design_id, question_id, design_kind, treatment, outcome, mediator, frontdoor_proof_ref, no_direct_path_assumption_ref, linear_mediator_model_ref, linear_outcome_model_ref, graph_evidence_ref. Assumption *references* are declarations, not empirical confirmation; validate identities, column roles, dataset support, graph/identification lineage.
- **Output (positive only):** result.json with e11-local-effect-result/1; do not produce unsupported CI; manifest/status/commit/readback follow G01. Scientific negative may have no positive artifact and must carry typed reason.
- **Inference (Study.inference):** requested=false → confidence_level=null; requested=true → confidence_level∈(0,1), execution requires an independently approved effective Method-specific CI otherwise INFERENCE_UNAVAILABLE; never promote to CONFIRMATORY. Strict unknown-key rejection.
- **Evidence obligation:** positive DGP-005; negatives NEG-004, NEG-005 plus config={} / unknown-key / wrong-method / wrong-estimand / wrong-backend / missing-ref / unsupported-CI; independent REF-I02, REF-E04; AC-D03, AC-P01, AC-P03, AC-I01, AC-I02. All fixtures/Backend/threshold/Science are NOT_GENERATED/NOT_EVALUATED.
- **Unresolved (BLOCKED before Freeze):**
  - Fix and independently verify precise mediator/outcome regressions including covariates and interaction exclusions
  - Finite-sample variance, interval method, bootstrap validity and selected backend signature require independent science/runtime evidence
- **Backend / Science:** independently pin distribution/version/API/License and normative DGP/NEG/REF, quantitative K/R/MC-SE/coverage AC before this Method's acceptance. Backend failure=CAPABILITY_UNAVAILABLE, missing profile=METHOD_PROFILE_UNAVAILABLE, invalid config=CONFIG_INVALID, semantic mismatch=METHOD_INCOMPATIBLE, unsupported interval=INFERENCE_UNAVAILABLE (where mapped by canonical status authority).

**Blocking independent status:** No positive Science PASS before real backend, independent reference, DGP/NEG fixtures, versioned effective API, K/R/MC-SE/coverage thresholds and legacy regression evidence. Verification of JSON shape alone is insufficient.


## S02：担当Method Profile・共通署名の規範（G02 / Owner承認）

担当Methodは`P1-M01, P1-M02, P1-M03, P1-M04, P1-M05, P1-M07`。共通5 Profile Kind（method_config/question_profile/design_profile/output_profile/inference_profile）を`23_api_interface_design/schema_drafts/method_profiles/factored/e11_<kind>_factored_v1.json`から読み、exact Method IDのoverlayと共通Schemaを単一JSON Schemaに再構成する。Dispatch Registry `e11_method_profile_dispatch_registry_draft1.json`を照合し、Git Blob SHA・Draft202012 Schema・正例/負例が未確認なら`METHOD_PROFILE_UNAVAILABLE`でfail-closed。閉objectの別々の`allOf`合成で`additionalProperties:false`を破綻させない。Operation/Estimand/Backend/CI・DGP/NEG/REF/ACはMethodごとの科学契約に従い、共通化から科学Targetを推測しない。特にP1-M05はB0二値IV/無調整complier `LATE_COMPLIER`の条件付きIDENTIFY専用で数値Effectを生成しない。

`LocalRunContext(root:TrustedLocalRoot,principal:LocalPrincipal)`と`LocalPrivacyPolicyPort.authorize(*,study,root,principal,output_shape)`を共通署名とし、署名PolicyVerifier/Anchor・`cli_row_flag`・Study`privacy.policy_ref`は実装しない。G05以外では個票直接出力禁止、G05でもStudy `row_export_requested=true`と非root同一UID/private ext4/XFS・Method Schema/capsが全件必要。新Local GraphはProduct Version ID=null、content hashと科学由来を使い、Product DB GraphVersionをlookup/生成しない。既存Scientific Kernel・旧Product v2を保護し、回帰は影響閉包に基づいて選択、未知影響なら試験またはBLOCK。Method固有の実Backend/Inference・独立科学Referenceは未確認であり、Science PASSとはしない。
