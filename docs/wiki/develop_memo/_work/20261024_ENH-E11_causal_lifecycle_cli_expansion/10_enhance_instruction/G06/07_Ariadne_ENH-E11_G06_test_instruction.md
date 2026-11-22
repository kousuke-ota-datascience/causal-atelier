# Ariadne ENH-E11 G06 — 07 独立テスト指示書：PCMCI・PCMCI+・LPCMCI

**DEC-PREPCODE-01=B（Owner 2026-11-22採用）：Gate別S09→S10→S11。** G06の独立S09監査は、先行Gate（G01）と共通E11 Wire/Port/Privacy/JCS/Publisher/Reader/Protected v2の変更影響閉包、およびG06自身の06/P00/Pxx/07/Method Profile/Backend/Scienceを対象とする。対象外Gateは全体SHA inventoryに保持し`NOT_REVIEWED`、未決の後続MethodはG06のCoding前無条件停止条件にしない。G06固有の独立S09 verdict→Owner G06-S10 Freeze→Owner G06-S11 Coding Authorizationを別々に取得する。**S11実行前にはG01_999の実PASSが必須**だが、S09文書監査の準備は先行Gateの実装中にも可能。実Adapter/FS/数値T2/T3/RegressionはG06の独立07/999で検証し、文書修正だけでPASSを付けない。現時点は`S09_NOT_RUN/S10_NOT_FROZEN/S11_NOT_AUTHORIZED`。

**Verification contract status: DRAFT / NOT_FROZEN / TESTS_NOT_RUN**
**Owner review: 2026-11-18 JST — PREP-03 audit and G06 Gate-level verification plan reviewed/accepted, with open Method/Profile/Evidence decisions preserved. This is NOT Contract Freeze, Independent Test execution, Gate999 PASS, or Coding Authorization.**
**Gate: G06 / Independent Test Agent / Trial01 NOT_STARTED**
**Dependencies: G01 PASS (canonical upstream 999)**
**Normative WHAT:** 本書のAC/Test Itemsのみ。テストの実physical path・command・runner discoveryは40 Operatorが所有。
**References:** [10_32 Scientific Method Scope](../../00_enhance_background/Revised_requirements_definition_documents/10_requirements_definition/10_32_scientific_method_scope.md) / [30_61 Domain/Ports](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_61_causal_domain_ports.md) / [30_62 Local Execution](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_62_local_execution_publication.md) / [30_63 Method Adapters](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_63_causal_method_adapters.md) / [23_41 Scientific Ports](../../00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design/23_41_cli_scientific_ports.md) / [23_42 Artifact](../../00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design/23_42_local_result_manifest_artifact.md)

## 0. Independent Gate claim

このGateがPASSしたと主張するには「TemporalDesignのlag/CI testとGraphのendpoint不確実性を失わず、Tigramite PCMCI/PCMCI+/LPCMCIの異なるGraph結果を保存・検証する。」をFull Fixed Candidate SHAで、後述の全受入軸と独立科学的Referenceに照らして証明する。Pxx COMPLETE、CLI exit0、Source上のMethod名、mock-onlyは独立Gate/Science PASSではない。

## 1. Acceptance Criteria (each blocking)

- **AC01 Strict Method/Design/Estimand:** 受理されたMethod×Operation×Target×Question/Design/Local Graph content hash・科学的親provenance/HashとInference Policyのみ実行。unknown/mismatch/partial/unidentifiedはtyped negative。
- **AC02 Actual Science:** 各Methodの既知DGP・Negative・独立REF、Backend実測/現行推論API、明示Assumption/Point/UncertaintyとScience status。
- **AC03 Portable Result:** Graph/Effect/Diagnostic/ConfidenceSet/MethodConfig/Provenanceを正しくBundle/Manifest/Readerへ保存し、hash/readback/negativeを確認。
- **AC04 Compatibility/Safety:** G01 FS/Privacy/Atomic/JCSと旧Product v2のprotected interface/behaviorを壊さず、無言fallback/未認可出力がない。
- **AC05 Identity/Independent QA:** Source/lock/fixture SHA、科学事前登録、test-layer、実効環境、Test Item全証拠と正式999判定。

## 2. Required Test Items (file locations are NOT normative)

| ID | Primary purpose | Primary verification layer | Required observable evidence |
|---|---|---|---|
| `G06-07-01` | TemporalDesign・TIME_SERIES_GRAPH（cross-cutting） | unit/contract + required integration | time order/lag/endpoint schema；適格positive/negative・typed Reason |
| `G06-07-02` | PCMCI Adapter（P3-M01） | contract + real backend integration + independent reference | CI test/effective Tigramite/API/lag；適格positive/negative・typed Reason |
| `G06-07-03` | PCMCI+・LPCMCI Adapter（P3-M02, P3-M03） | contract + real backend integration + independent reference | contemporaneous/latent/circle endpoint Oracle；適格positive/negative・typed Reason |
| `G06-07-04` | Temporal CLI/Manifest/Readback（cross-cutting） | unit/contract + required integration | Local Graph hash/null Product version/科学的親provenance/lag roundtripとnon-null import negative；適格positive/negative・typed Reason |
| `G06-07-05` | Whole Local CLI/Port/Artifact integration | contract + real CLI/FS integration | Strict Operation, Hash, Manifest, Reader, privacy, negative Error status |
| `G06-07-06` | Protected v2/upstream contracts | current actual legacy suite + E11 integration | Upstream 999 invariants, no old v2 CLI/Result change |
| `G06-07-07` | Independent Science/T2/T3 | independently verified reference + real backend integration | Method-specific DGP/NEG/REF, prereg K/R/seed/compute, predeclared quantitative decision |
| `001` | Candidate identity | repository provenance audit | Candidate full SHA, actual checkout, test-only diff classification |
| `999` | Formal Gate decision | independent 30 reports | All blocking items PASS, verified FAIL or BLOCKED and owner action |

**Browser E2E:** 本E11 ScopeはCLI-firstで新規Web UIを実装しないため、当該Gateの新規Browser E2E blocking journeyは**N/A**。既存Productのaffected Browser journeyはRegression対象となり得る。将来UIを本GateScopeへ変更する場合は07の正式Amendment・再Freezeとcritical journey・command・environment・synchronization記述を先行させる。

## 3. Method-by-Method Scientific test obligations

| Method / DD-ID | Target | DGP/NEG / REF | Required evidence / decision |
|---|---|---|---|
| `P3-M01` / `DD-E11-METH-P301` | PCMCI | DGP-009; NEG-021 / REF-G03 | PLAN:G06 / CONFIG_AND_AC_PENDING / NOT_GENERATED / AC-D01, AC-G01, AC-G02, AC-G03, AC-G05；Method-specific science/CI未確定ならBLOCKED |
| `P3-M02` / `DD-E11-METH-P302` | PCMCI+ | DGP-009, DGP-010; NEG-021, NEG-028 / REF-G03, REF-G02 | PLAN:G06 / OWNER_ORACLE_PRINCIPLE_ACCEPTED_ORACLE_BLOCKED / NOT_GENERATED / AC-D01, AC-G01, AC-G02, AC-G03, AC-G04, AC-G06；Method-specific science/CI未確定ならBLOCKED |
| `P3-M03` / `DD-E11-METH-P303` | LPCMCI | DGP-011; NEG-021, NEG-028 / REF-G03, REF-G02 | PLAN:G06 / OWNER_ORACLE_PRINCIPLE_ACCEPTED_ORACLE_BLOCKED / NOT_GENERATED / AC-D01, AC-G01, AC-G02, AC-G03, AC-G04, AC-G06；Method-specific science/CI未確定ならBLOCKED |

**Independent oracle and numerical rule:** DGP truthとEstimator/Backend outputは別Authority。Fixed generator/Reference SHA、既知EstimandとAssumptions、negative/statusを先に登録。Deterministic schema/JCS/roundtripは100%一致。Stochastic ScienceはT2 PilotとT3正式事前登録を分離し、多重性K/FWER=0.05、K/R/seed/threshold/computeは科学決定に基づきFreeze。未確定を推測で補完せず該当Test Item BLOCKED。


**Owner採用 OD-05（2026-11-19）：** G06の3 Methodについて、既決Target/数理は変更せず、担当Pxxでそれぞれstrict versioned `Method Config / Question / Design / Output / Inference Profile`を独立に定義・登録する。Method固有の確認項目は「Tigramite CI test、lag sign/zero contemporaneous edge、time-index/order、PCMCI/PCMCI+/LPCMCI endpoint/latent/Graph proof」。条件付き必須Field、Backend effective API/version/optional extras、positive/invalid-config/wrong-target/unsupported-CI/negative-science fixtureとtyped reasonを固定する。未登録/未検証は`METHOD_PROFILE_UNAVAILABLE`等でfail-closed。単なる`config={}`、Backend default、未生成DGP/REF、K/R/MC-SE未実測をPASSとしない。これはProfile作成の**担当配分採用**であり、個々のSchema/Inference/科学Referenceの完成・Freeze・Coding Authorizationを意味しない。

**Independent acceptance for every G06 Method:** valid config/Question/Design/output/Inference positive, extra unknown-property/missing conditional field/wrong target/Graph or DataRef hash/backend mismatch/unsupported CI negatives, deployed real backend API and independent DGP/REF must be separately evidenced. G01/G10 Gateway PASS must not infer scientific proof from schema shape.

## 4. Verification operation, evidence and decision

- Fixed Trial Candidate SHAと実効checkoutが同じsemantic implementation stateか監査。上流Gateのcanonical 999 PASSとprotected contractをSource上の根拠で照合。
- 40 Test Agentは`tests/enhancement/enh_e11/<gate>/`を始点に、関連する`tests/product/`/`tests/integration/`等を現物から発見、test existence/collection/fixture/conftest/dependencies/runner/FS/backendを確認。07にhistorical filename/commandを固定しない。
- Test evidenceにはItem ID/DD ID、actual path/command、source/fixture/lock SHA、effective OS/FS/backend、Known truth/observed output、positive+negative、PASS/FAIL/BLOCKEDと原因を記録。Evidence commitとCandidate SHAを混同しない。
- Independent Test Agentはproduct/test code/runner/CI/06/07を修復しない。Product不変違反を実証したときFAIL、Test-side/UNKNOWN/Backend/独立Oracle不足でProduct判定不能ならBLOCKED。
- G01〜G10各Gateの999は独立であり、Methodごとの未実施・Science未検証・Protected Regression欠落がある限りGate PASS禁止。

## 5. Freeze前のOwner/Science review

lag0/lag>0混同、PAG/CPDAGのDAG化、時系列順序改変を禁止。

Method-specific strict Schema・positive/negative・独立Reference/推論Method/CI・threshold・Backend/License・Gate境界/depends/quant computeをレビューし、07をFreezeして初めて実行可能。現時点ではTest NOT_RUN、999 NOT_EXECUTED。


## PREP-04.1 independent strict Method verification (DRAFT)

### P3-M01 — strict Method contract (PREP-04.1 DRAFT / NOT_FROZEN)
- Method scope: DISCOVER / 10_32 semantic target (not assigned canonical enum); Pxx=P02; preserve 10_32 scientific target, do not cast alternative estimands.
- Config mandatory fields: ci_test_spec_ref, tau_min, tau_max, alpha; versioned method_config Schema restricts type/const/range and extra keys, config={} is rejected, no backend defaults.
- Question mandatory: question_id/research_question/population/analysis_goal/estimand_family/contrast; Study target and references cross-validated.
- Design mandatory: design_id/question_id/design_kind plus time_index, sampling_unit, observed_variables, temporal_ordering_ref, lag_convention_ref; validated data columns, roles, dataset support and assumption/Graph/temporal provenance. Declarations are not proof of causal truth. Exact types enforced by dedicated design_profile Schema.
- Positive output: graph.json/e11-local-graph/1, no result.json; status/marker/manifest and Reader hash/readback required; negative science typed and no fictitious positive.
- Inference: requested=false, confidence_level=null. CONFIRMATORY is not granted by schema syntax.
- Independent AC: DGP-009; NEG-021; REF-G03. Negative matrix includes empty/unknown/malformed config, wrong operation/target, missing/mismatched upstream hash, unsupported CI, unavailable backend and Method-specific NEG. Real backend and independent DGP/REF/K/R/MC-SE/FWER 0.05 remain NOT_VERIFIED.


### P3-M02 — strict Method contract (PREP-04.1 DRAFT / NOT_FROZEN)
- Method scope: DISCOVER / 10_32 semantic target (not assigned canonical enum); Pxx=P02; preserve 10_32 scientific target, do not cast alternative estimands.
- Config mandatory fields: ci_test_spec_ref, tau_min, tau_max, alpha, contemporaneous_rules_ref; versioned method_config Schema restricts type/const/range and extra keys, config={} is rejected, no backend defaults.
- Question mandatory: question_id/research_question/population/analysis_goal/estimand_family/contrast; Study target and references cross-validated.
- Design mandatory: design_id/question_id/design_kind plus time_index, sampling_unit, observed_variables, temporal_ordering_ref, lag_convention_ref, endpoint_convention_ref; validated data columns, roles, dataset support and assumption/Graph/temporal provenance. Declarations are not proof of causal truth. Exact types enforced by dedicated design_profile Schema.
- Positive output: graph.json/e11-local-graph/1, no result.json; status/marker/manifest and Reader hash/readback required; negative science typed and no fictitious positive.
- Inference: requested=false, confidence_level=null. CONFIRMATORY is not granted by schema syntax.
- Independent AC: DGP-009, DGP-010; NEG-021, NEG-028; REF-G03, REF-G02. Negative matrix includes empty/unknown/malformed config, wrong operation/target, missing/mismatched upstream hash, unsupported CI, unavailable backend and Method-specific NEG. Real backend and independent DGP/REF/K/R/MC-SE/FWER 0.05 remain NOT_VERIFIED.


### P3-M03 — strict Method contract (PREP-04.1 DRAFT / NOT_FROZEN)
- Method scope: DISCOVER / 10_32 semantic target (not assigned canonical enum); Pxx=P02; preserve 10_32 scientific target, do not cast alternative estimands.
- Config mandatory fields: ci_test_spec_ref, tau_min, tau_max, alpha, latent_assumptions_ref; versioned method_config Schema restricts type/const/range and extra keys, config={} is rejected, no backend defaults.
- Question mandatory: question_id/research_question/population/analysis_goal/estimand_family/contrast; Study target and references cross-validated.
- Design mandatory: design_id/question_id/design_kind plus time_index, sampling_unit, observed_variables, temporal_ordering_ref, lag_convention_ref, endpoint_convention_ref; validated data columns, roles, dataset support and assumption/Graph/temporal provenance. Declarations are not proof of causal truth. Exact types enforced by dedicated design_profile Schema.
- Positive output: graph.json/e11-local-graph/1, no result.json; status/marker/manifest and Reader hash/readback required; negative science typed and no fictitious positive.
- Inference: requested=false, confidence_level=null. CONFIRMATORY is not granted by schema syntax.
- Independent AC: DGP-011; NEG-021, NEG-028; REF-G03, REF-G02. Negative matrix includes empty/unknown/malformed config, wrong operation/target, missing/mismatched upstream hash, unsupported CI, unavailable backend and Method-specific NEG. Real backend and independent DGP/REF/K/R/MC-SE/FWER 0.05 remain NOT_VERIFIED.


## S02簡素化・G06 Temporal GraphとMethod Profileの規範

担当Methodは`P3-M01` PCMCI、`P3-M02` PCMCI+、`P3-M03` LPCMCIの3件。5 Profile kind（method_config/question_profile/design_profile/output_profile/inference_profile）は`23_api_interface_design/schema_drafts/method_profiles/factored/e11_<kind>_factored_v1.json`のshared core＋exact Method ID overlayから再構成し、Dispatch Registry/200 Schema標準Draft202012/正負例/parityの確認が不足すれば`METHOD_PROFILE_UNAVAILABLE`でfail-closed。科学的契約は各Methodで異なり、time-lag端点の向き/ラグ0、PAG/CPDAG同値類、潜在交絡・CIテストの意味を厳格保存し、グラフ方向を自動確定しない。ENV-TIGRAMITEの実効Python3.12 APIと独立時系列Graph Oracleの実測は後続検証事項。

新Local Graphは内容hashとsource/parent科学由来を保持するがProduct GraphVersion DBはlookup/edit/write/FIXしない。`version_id=parent_version_id=null`のみ提供し、non-null importは未対応として拒否。共通`LocalRunContext(root,principal)`、`LocalPrivacyPolicyPort.authorize(*,study,root,principal,output_shape)`を利用し、署名Verifier/Policy Anchorと追加CLI flagを作らない。G06は個票を直接公開せず、旧Product v2のABIと共通Kernelを保護する。独立Testは時系列順序・PAG/CPDAG同値類・Graph hash/Manifest/readback・wrong Method/unsupported CIの負例を確認する。未実測をScience PASSとしない。
