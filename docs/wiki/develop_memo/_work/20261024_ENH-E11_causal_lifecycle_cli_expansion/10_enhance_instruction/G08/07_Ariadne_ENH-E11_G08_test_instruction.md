# Ariadne ENH-E11 G08 — 07 独立テスト指示書：RDD・Wald/2SLS・Weak IV/AR

**Verification contract status: DRAFT / NOT_FROZEN / TESTS_NOT_RUN**
**Gate: G08 / Independent Test Agent / Trial01 NOT_STARTED**
**Dependencies: G01 PASS, G02 PASS (canonical upstream 999)**
**Normative WHAT:** 本書のAC/Test Itemsのみ。テストの実physical path・command・runner discoveryは40 Operatorが所有。
**References:** [10_32 Scientific Method Scope](../../00_enhance_background/Revised_requirements_definition_documents/10_requirements_definition/10_32_scientific_method_scope.md) / [30_61 Domain/Ports](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_61_causal_domain_ports.md) / [30_62 Local Execution](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_62_local_execution_publication.md) / [30_63 Method Adapters](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_63_causal_method_adapters.md) / [23_41 Scientific Ports](../../00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design/23_41_cli_scientific_ports.md) / [23_42 Artifact](../../00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design/23_42_local_result_manifest_artifact.md)

## 0. Independent Gate claim

このGateがPASSしたと主張するには「Sharp/Fuzzy RDD局所効果と、B0 binary Z/A complier LATE、B1指定Cの加法線形IV構造係数を分離し、weak IV時のAR反転集合を損失なく表現する。」をFull Fixed Candidate SHAで、後述の全受入軸と独立科学的Referenceに照らして証明する。Pxx COMPLETE、CLI exit0、Source上のMethod名、mock-onlyは独立Gate/Science PASSではない。

## 1. Acceptance Criteria (each blocking)

- **AC01 Strict Method/Design/Estimand:** 受理されたMethod×Operation×Target×Question/Design/GraphVersion/HashとInference Policyのみ実行。unknown/mismatch/partial/unidentifiedはtyped negative。
- **AC02 Actual Science:** 各Methodの既知DGP・Negative・独立REF、Backend実測/現行推論API、明示Assumption/Point/UncertaintyとScience status。
- **AC03 Portable Result:** Graph/Effect/Diagnostic/ConfidenceSet/MethodConfig/Provenanceを正しくBundle/Manifest/Readerへ保存し、hash/readback/negativeを確認。
- **AC04 Compatibility/Safety:** G01 FS/Privacy/Atomic/JCSと旧Product v2のprotected interface/behaviorを壊さず、無言fallback/未認可出力がない。
- **AC05 Identity/Independent QA:** Source/lock/fixture SHA、科学事前登録、test-layer、実効環境、Test Item全証拠と正式999判定。

## 2. Required Test Items (file locations are NOT normative)

| ID | Primary purpose | Primary verification layer | Required observable evidence |
|---|---|---|---|
| `G08-07-01` | RD/IV Design・Estimand適格性（cross-cutting） | unit/contract + required integration | cutoff/density/first-stage/B0/B1 target；適格positive/negative・typed Reason |
| `G08-07-02` | Sharp/Fuzzy RD Adapter（P3-M07, P3-M08） | contract + real backend integration + independent reference | bandwidth/local target/discontinuity/CI；適格positive/negative・typed Reason |
| `G08-07-03` | Wald・2SLS B0/B1（P3-M09, P3-M10, P3-M11） | contract + real backend integration + independent reference | binary Z/A、C、robust covariance/first stage；適格positive/negative・typed Reason |
| `G08-07-04` | Weak-IV HC1・AR set推論（cross-cutting） | unit/contract + required integration | bounded/unbounded/disconnected/empty/all-real AR set；適格positive/negative・typed Reason |
| `G08-07-05` | RD/IV CLI・Typed Result・科学（cross-cutting） | unit/contract + required integration | REF-Q03/E07/E08/U01とv2回帰；適格positive/negative・typed Reason |
| `G08-07-06` | Whole Local CLI/Port/Artifact integration | contract + real CLI/FS integration | Strict Operation, Hash, Manifest, Reader, privacy, negative Error status |
| `G08-07-07` | Protected v2/upstream contracts | current actual legacy suite + E11 integration | Upstream 999 invariants, no old v2 CLI/Result change |
| `G08-07-08` | Independent Science/T2/T3 | independently verified reference + real backend integration | Method-specific DGP/NEG/REF, prereg K/R/seed/compute, predeclared quantitative decision |
| `001` | Candidate identity | repository provenance audit | Candidate full SHA, actual checkout, test-only diff classification |
| `999` | Formal Gate decision | independent 30 reports | All blocking items PASS, verified FAIL or BLOCKED and owner action |

**Browser E2E:** 本E11 ScopeはCLI-firstで新規Web UIを実装しないため、当該Gateの新規Browser E2E blocking journeyは**N/A**。既存Productのaffected Browser journeyはRegression対象となり得る。将来UIを本GateScopeへ変更する場合は07の正式Amendment・再Freezeとcritical journey・command・environment・synchronization記述を先行させる。

## 3. Method-by-Method Scientific test obligations

| Method / DD-ID | Target | DGP/NEG / REF | Required evidence / decision |
|---|---|---|---|
| `P3-M07` / `DD-E11-METH-P307` | Sharp RD local effect | DGP-015; NEG-023 / REF-Q03 | PLAN:G08 / OWNER_ESTIMATOR_INFERENCE_POLICY_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED / AC-D03, AC-P01, AC-P03, AC-I01, AC-I02, AC-Q03；Method-specific science/CI未確定ならBLOCKED |
| `P3-M08` / `DD-E11-METH-P308` | Fuzzy RD local complier effect | DGP-016; NEG-006, NEG-023 / REF-Q03, REF-I03 | PLAN:G08 / OWNER_ESTIMATOR_INFERENCE_POLICY_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED / AC-D03, AC-P01, AC-P03, AC-I01, AC-I02, AC-Q03；Method-specific science/CI未確定ならBLOCKED |
| `P3-M09` / `DD-E11-METH-P309` | B0 complier LATE reference | DGP-006; NEG-006, NEG-007 / REF-I03, REF-E07 | PLAN:G08 / CONFIG_AND_AC_PENDING / NOT_GENERATED / AC-D03, AC-P01, AC-P03, AC-P05, AC-D07；Method-specific science/CI未確定ならBLOCKED |
| `P3-M10` / `DD-E11-METH-P310` | B0 just-identified LATE | DGP-006, DGP-024; NEG-006, NEG-025 / REF-E07, REF-U01 | PLAN:G08 / CONFIG_AND_AC_PENDING / NOT_GENERATED / AC-D03, AC-P01, AC-P03, AC-P05, AC-A01, AC-A02, AC-A03, AC-A04, AC-A05, AC-I01, AC-I02；Method-specific science/CI未確定ならBLOCKED |
| `P3-M11` / `DD-E11-METH-P311` | B1 additive linear IV slope | DGP-007, DGP-024; NEG-008, NEG-025 / REF-E08, REF-U01 | PLAN:G08 / OWNER_TARGET_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED / AC-D03, AC-P01, AC-P03, AC-P05, AC-A01, AC-A02, AC-A03, AC-A04, AC-A05, AC-I01, AC-I02；Method-specific science/CI未確定ならBLOCKED |

**Independent oracle and numerical rule:** DGP truthとEstimator/Backend outputは別Authority。Fixed generator/Reference SHA、既知EstimandとAssumptions、negative/statusを先に登録。Deterministic schema/JCS/roundtripは100%一致。Stochastic ScienceはT2 PilotとT3正式事前登録を分離し、多重性K/FWER=0.05、K/R/seed/threshold/computeは科学決定に基づきFreeze。未確定を推測で補完せず該当Test Item BLOCKED。

## 4. Verification operation, evidence and decision

- Fixed Trial Candidate SHAと実効checkoutが同じsemantic implementation stateか監査。上流Gateのcanonical 999 PASSとprotected contractをSource上の根拠で照合。
- 40 Test Agentは`tests/enhancement/enh_e11/<gate>/`を始点に、関連する`tests/product/`/`tests/integration/`等を現物から発見、test existence/collection/fixture/conftest/dependencies/runner/FS/backendを確認。07にhistorical filename/commandを固定しない。
- Test evidenceにはItem ID/DD ID、actual path/command、source/fixture/lock SHA、effective OS/FS/backend、Known truth/observed output、positive+negative、PASS/FAIL/BLOCKEDと原因を記録。Evidence commitとCandidate SHAを混同しない。
- Independent Test Agentはproduct/test code/runner/CI/06/07を修復しない。Product不変違反を実証したときFAIL、Test-side/UNKNOWN/Backend/独立Oracle不足でProduct判定不能ならBLOCKED。
- G01〜G10各Gateの999は独立であり、Methodごとの未実施・Science未検証・Protected Regression欠落がある限りGate PASS禁止。

## 5. Freeze前のOwner/Science review

B0 LATEとB1 slopeの混同、weak IVで有限CI捏造、AR setの単一区間化を禁止。

Method-specific strict Schema・positive/negative・独立Reference/推論Method/CI・threshold・Backend/License・Gate境界/depends/quant computeをレビューし、07をFreezeして初めて実行可能。現時点ではTest NOT_RUN、999 NOT_EXECUTED。
