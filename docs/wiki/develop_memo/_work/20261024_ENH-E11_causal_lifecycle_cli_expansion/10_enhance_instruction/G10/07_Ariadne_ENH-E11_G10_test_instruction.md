# Ariadne ENH-E11 G10 — 07 独立テスト指示書：41 Method横断再現性・CLI/Manifest・Regression

**Verification contract status: DRAFT / NOT_FROZEN / TESTS_NOT_RUN**
**Owner review: 2026-11-18 JST — PREP-03 audit and G10 Gate-level verification plan reviewed/accepted, with open Method/Profile/Evidence decisions preserved. This is NOT Contract Freeze, Independent Test execution, Gate999 PASS, or Coding Authorization.**
**Gate: G10 / Independent Test Agent / Trial01 NOT_STARTED**
**Dependencies: G01 PASS, G02 PASS, G03 PASS, G04 PASS, G05 PASS, G06 PASS, G07 PASS, G08 PASS, G09 PASS (canonical upstream 999)**
**Normative WHAT:** 本書のAC/Test Itemsのみ。テストの実physical path・command・runner discoveryは40 Operatorが所有。
**References:** [10_32 Scientific Method Scope](../../00_enhance_background/Revised_requirements_definition_documents/10_requirements_definition/10_32_scientific_method_scope.md) / [30_61 Domain/Ports](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_61_causal_domain_ports.md) / [30_62 Local Execution](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_62_local_execution_publication.md) / [30_63 Method Adapters](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_63_causal_method_adapters.md) / [23_41 Scientific Ports](../../00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design/23_41_cli_scientific_ports.md) / [23_42 Artifact](../../00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design/23_42_local_result_manifest_artifact.md)

## 0. Independent Gate claim

このGateがPASSしたと主張するには「G01〜G09の41 MethodとOperation/Estimand/Schema/Backend/Artifactを一貫して再実行でき、厳密なManifest/Checksum/Readback・科学証拠・旧v2回帰を統合検証する。」をFull Fixed Candidate SHAで、後述の全受入軸と独立科学的Referenceに照らして証明する。Pxx COMPLETE、CLI exit0、Source上のMethod名、mock-onlyは独立Gate/Science PASSではない。

## 1. Acceptance Criteria (each blocking)

- **AC01 Strict Method/Design/Estimand:** 受理されたMethod×Operation×Target×Question/Design/GraphVersion/HashとInference Policyのみ実行。unknown/mismatch/partial/unidentifiedはtyped negative。
- **AC02 Actual Science:** 各Methodの既知DGP・Negative・独立REF、Backend実測/現行推論API、明示Assumption/Point/UncertaintyとScience status。
- **AC03 Portable Result:** Graph/Effect/Diagnostic/ConfidenceSet/MethodConfig/Provenanceを正しくBundle/Manifest/Readerへ保存し、hash/readback/negativeを確認。
- **AC04 Compatibility/Safety:** G01 FS/Privacy/Atomic/JCSと旧Product v2のprotected interface/behaviorを壊さず、無言fallback/未認可出力がない。
- **AC05 Identity/Independent QA:** Source/lock/fixture SHA、科学事前登録、test-layer、実効環境、Test Item全証拠と正式999判定。

## 2. Required Test Items (file locations are NOT normative)

| ID | Primary purpose | Primary verification layer | Required observable evidence |
|---|---|---|---|
| `G10-07-01` | 41 Method/strict Profile/Registry統合（cross-cutting） | unit/contract + required integration | P1=20,P2=8,P3=13の配置・availability；適格positive/negative・typed Reason |
| `G10-07-02` | 全Operation Manifest/Hash/Readback（cross-cutting） | unit/contract + required integration | source/fixture/environment/schema JCS/Checksum；適格positive/negative・typed Reason |
| `G10-07-03` | 全Gateと旧Product v2互換回帰（cross-cutting） | unit/contract + required integration | local CLI/Result/graph/Privacyの保護；適格positive/negative・typed Reason |
| `G10-07-04` | 独立科学Benchmark・Backend/License検証（cross-cutting） | unit/contract + required integration | Method-specific DGP/NEG/REF, T2/T3, delivery gate；適格positive/negative・typed Reason |
| `G10-07-05` | Whole Local CLI/Port/Artifact integration | contract + real CLI/FS integration | Strict Operation, Hash, Manifest, Reader, privacy, negative Error status |
| `G10-07-06` | Protected v2/upstream contracts | current actual legacy suite + E11 integration | Upstream 999 invariants, no old v2 CLI/Result change |
| `G10-07-07` | Independent Science/T2/T3 | independently verified reference + real backend integration | Method-specific DGP/NEG/REF, prereg K/R/seed/compute, predeclared quantitative decision |
| `001` | Candidate identity | repository provenance audit | Candidate full SHA, actual checkout, test-only diff classification |
| `999` | Formal Gate decision | independent 30 reports | All blocking items PASS, verified FAIL or BLOCKED and owner action |

**Browser E2E:** 本E11 ScopeはCLI-firstで新規Web UIを実装しないため、当該Gateの新規Browser E2E blocking journeyは**N/A**。既存Productのaffected Browser journeyはRegression対象となり得る。将来UIを本GateScopeへ変更する場合は07の正式Amendment・再Freezeとcritical journey・command・environment・synchronization記述を先行させる。

## 3. 41 Method independent scientific obligations — standalone G10 Verification contract

**対象:** G10自体は新Method IDを定義しない。しかしG10-07-04/G10-07-07は、上流G01〜G09で承認された全41 Methodのscientific evidence、current effective Backend、positive/negative、independent referenceと実際の再実行を検証する。Test AgentがGate06/Pxxや外部RDを読まなくても対象Method ID/DD/REF/ACを列挙できるよう、以下に全件保持する。Status列は**作成時点のDRAFT planning state**であり、実行結果・Gate PASS・現在のSource capabilityを意味しない。

| Method | DD | DGP/NEG | Ref | AC | Status |
|---|---|---|---|---|---|
| `P1-M01` Native Randomized identification／A | `DD-E11-METH-P101` | DGP-001; NEG-001, NEG-027 | REF-G01, REF-I01 | AC-D01, AC-D02, AC-D07 | PLAN:G02 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P1-M02` Native Backdoor identification／ATE | `DD-E11-METH-P102` | DGP-002, DGP-021; NEG-002, NEG-003 | REF-G01, REF-I01 | AC-D01, AC-D02, AC-D07 | PLAN:G02 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P1-M03` DoWhy Backdoor identification／ATE候 | `DD-E11-METH-P103` | DGP-002, DGP-021; NEG-002, NEG-027 | REF-G01, REF-I01 | AC-D01, AC-D02, AC-D07 | PLAN:G02 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P1-M04` DoWhy Frontdoor identification／ATE | `DD-E11-METH-P104` | DGP-005; NEG-004 | REF-G01, REF-I02 | AC-D01, AC-D02, AC-D07 | PLAN:G02 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P1-M05` DoWhy IV identification／B0二値Z/A無調整complier LATE（条件付き識別） | `DD-E11-METH-P105` | DGP-006; NEG-006, NEG-007 | REF-I03, REF-G01 | AC-D01, AC-D02, AC-D07 | PLAN:G02 / OWNER_TARGET_ADOPTED_PROFILE_BACKEND_SCIENCE_PENDING / NOT_GENERATED |
| `P1-M06` FCI／PAGと等価類 | `DD-E11-METH-P106` | DGP-011, DGP-021; NEG-003, NEG-021, NEG-028 | REF-G02 | AC-D02, AC-G01, AC-G02, AC-G03, AC-G04, AC-G06 | PLAN:G01 / OWNER_ORACLE_PRINCIPLE_ACCEPTED_ORACLE_BLOCKED / NOT_GENERATED |
| `P1-M07` Frontdoor two-stage regression／ATE | `DD-E11-METH-P107` | DGP-005; NEG-004, NEG-005 | REF-I02, REF-E04 | AC-D03, AC-P01, AC-P03, AC-I01, AC-I02 | PLAN:G02 / OWNER_METHOD_ACCEPTED_TECH_AND_SCIENCE_BLOCKED / NOT_GENERATED |
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
| `P2-M01` LinearDML／CATE(x) | `DD-E11-METH-P201` | DGP-003; NEG-011, NEG-012, NEG-013 | REF-E05 | AC-D01, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-I03 | PLAN:G04 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P2-M02` CausalForestDML／CATE(x) | `DD-E11-METH-P202` | DGP-004; NEG-010, NEG-012, NEG-013 | REF-E05 | AC-D01, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-I03 | PLAN:G04 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P2-M03` DRLearner／CATE(x) | `DD-E11-METH-P203` | DGP-003, DGP-004; NEG-011, NEG-012, NEG-013 | REF-E05, REF-E03 | AC-D01, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-I03 | PLAN:G04 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P2-M04` ForestDRLearner／CATE(x) | `DD-E11-METH-P204` | DGP-004; NEG-010, NEG-011, NEG-013 | REF-E05, REF-E03 | AC-D01, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-I03 | PLAN:G04 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P2-M05` S-Learner／CATE(x) | `DD-E11-METH-P205` | DGP-002, DGP-003; NEG-010, NEG-012, NEG-013 | REF-E05 | AC-D01, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-I03 | PLAN:G04 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P2-M06` T-Learner／CATE(x) | `DD-E11-METH-P206` | DGP-003, DGP-004; NEG-010, NEG-013 | REF-E05 | AC-D01, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-I03 | PLAN:G04 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P2-M07` X-Learner／CATE(x) | `DD-E11-METH-P207` | DGP-003, DGP-004; NEG-011, NEG-012, NEG-013 | REF-E05 | AC-D01, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-I03 | PLAN:G04 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P2-M08` DRIV-A／CONDITIONAL_IV_STRUCTURAL_SLOPE | `DD-E11-METH-P208` | DGP-008; NEG-009, NEG-012, NEG-013 | REF-E06 | AC-D01, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-I03 | PLAN:G04 / OWNER_TARGET_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED |
| `P3-M01` PCMCI／time-lagged graph | `DD-E11-METH-P301` | DGP-009; NEG-021 | REF-G03 | AC-D01, AC-G01, AC-G02, AC-G03, AC-G05 | PLAN:G06 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P3-M02` PCMCI+／time-series CPDAG | `DD-E11-METH-P302` | DGP-009, DGP-010; NEG-021, NEG-028 | REF-G03, REF-G02 | AC-D01, AC-G01, AC-G02, AC-G03, AC-G04, AC-G06 | PLAN:G06 / OWNER_ORACLE_PRINCIPLE_ACCEPTED_ORACLE_BLOCKED / NOT_GENERATED |
| `P3-M03` LPCMCI／time-series PAG | `DD-E11-METH-P303` | DGP-011; NEG-021, NEG-028 | REF-G03, REF-G02 | AC-D01, AC-G01, AC-G02, AC-G03, AC-G04, AC-G06 | PLAN:G06 / OWNER_ORACLE_PRINCIPLE_ACCEPTED_ORACLE_BLOCKED / NOT_GENERATED |
| `P3-M04` DiD／ATT（2×2とstaggeredは別契約） | `DD-E11-METH-P304` | DGP-012, DGP-013; NEG-022 | REF-Q01 | AC-D03, AC-P01, AC-P03, AC-I01, AC-I02, AC-Q01 | PLAN:G07 / OWNER_ESTIMATOR_INFERENCE_POLICY_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED |
| `P3-M05` Event Study／event-time効果 | `DD-E11-METH-P305` | DGP-013; NEG-022 | REF-Q01 | AC-D03, AC-P01, AC-P03, AC-I01, AC-I02, AC-Q01 | PLAN:G07 / OWNER_ESTIMATOR_INFERENCE_POLICY_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED |
| `P3-M06` Interrupted Time Series／介入時点のlevel | `DD-E11-METH-P306` | DGP-014; NEG-023 | REF-Q02 | AC-D03, AC-P01, AC-P03, AC-I01, AC-I02, AC-Q02 | PLAN:G07 / OWNER_ESTIMATOR_INFERENCE_POLICY_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED |
| `P3-M07` Sharp RDD／cutoff局所効果 | `DD-E11-METH-P307` | DGP-015; NEG-023 | REF-Q03 | AC-D03, AC-P01, AC-P03, AC-I01, AC-I02, AC-Q03 | PLAN:G08 / OWNER_ESTIMATOR_INFERENCE_POLICY_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED |
| `P3-M08` Fuzzy RDD／cutoff局所complier効果 | `DD-E11-METH-P308` | DGP-016; NEG-006, NEG-023 | REF-Q03, REF-I03 | AC-D03, AC-P01, AC-P03, AC-I01, AC-I02, AC-Q03 | PLAN:G08 / OWNER_ESTIMATOR_INFERENCE_POLICY_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED |
| `P3-M09` Wald ratio／binary Z/A complier LAT | `DD-E11-METH-P309` | DGP-006; NEG-006, NEG-007 | REF-I03, REF-E07 | AC-D03, AC-P01, AC-P03, AC-P05, AC-D07 | PLAN:G08 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P3-M10` B0 just-identified 2SLS／binary Z/A | `DD-E11-METH-P310` | DGP-006, DGP-024; NEG-006, NEG-025 | REF-E07, REF-U01 | AC-D03, AC-P01, AC-P03, AC-P05, AC-A01, AC-A02, AC-A03, AC-A04, AC-A05, AC-I01, AC-I02 | PLAN:G08 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P3-M11` B1-A／LINEAR_IV_STRUCTURAL_COEFFICIENT | `DD-E11-METH-P311` | DGP-007, DGP-024; NEG-008, NEG-025 | REF-E08, REF-U01 | AC-D03, AC-P01, AC-P03, AC-P05, AC-A01, AC-A02, AC-A03, AC-A04, AC-A05, AC-I01, AC-I02 | PLAN:G08 / OWNER_TARGET_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED |
| `P3-M12` Synthetic Control／処置単位の時点別反実仮想ギャップ | `DD-E11-METH-P312` | DGP-017; NEG-024 | REF-Q04 | AC-D03, AC-P01, AC-P03, AC-Q04 | PLAN:G09 / OWNER_BASELINE_ACCEPTED_POINT_ONLY_SCIENCE_PENDING / NOT_GENERATED |
| `P3-M13` Synthetic DiD／panel平均介入効果 | `DD-E11-METH-P313` | DGP-018; NEG-024 | REF-Q05 | AC-D03, AC-P01, AC-P03, AC-I01, AC-I02, AC-Q05 | PLAN:G09 / OWNER_ESTIMATOR_INFERENCE_POLICY_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED |

**Independent acceptance algorithm:** 各Methodについて(1) 対応upstream latest canonical 999 PASS、(2) frozen Method Config/Backend/Estimand/Inference Profile、(3) independent validated DGP true value/Graph oracle/negative scenario、(4) source+lock+fixture SHA、(5) real effective backend/inference/seed/replicate、(6) observed vs expected and Method-specific status/Reason、(7) Result/Manifest/Reader readback、(8)旧Product invariant protectionを一対一に照合する。未実行・Oracle欠落・dependency不適格はそのMethodをBLOCKEDにする。

**Numerical decision:** T1 deterministic schema/hash/roundtrip and T2 Pilot and T3 confirmatory simulation are independent layers. Method-specific K (multiple comparisons), R (replications), MC-SE, confidence coverage, acceptance boundaries and compute budget must be preregistered before T3; adopted familywise error control is FWER=0.05. Do not infer K/R from this document, do not convert pilot tuning into confirmatory PASS, and do not use output from the backend under test as ground truth. Entire Test Item/Gate PASS requires all blocking proofs for the same Fixed Trial Candidate.

**Compatibility/Legal:** 上流G01〜G09のscience decisionをG10で上書きしない。G10は全41を横断再現し、Source/lock/Backend、SBOM/License、Legacy CLI Product v2のcurrent invariantを別々に検証。顧客別GPL等のLicense/Delivery判断を自動PASSしない。


**OD-01/02/03/05（2026-11-19 Owner採用）との横断一致規範：**

- `P1-M05`はG02で`IDENTIFY`専用、明示的`B0_BINARY_IV` binary Z/A unadjusted `LATE_COMPLIER`条件付き識別。DoWhy IV internal label/`nonparametric-ate`だけでLATE証明とせず、宣言済みrelevance/exclusion/independence/monotonicity/consistency、Graph/Question/Design/Content hashとeffective APIを検証。`IDENTIFY`のEffect `result.json`は禁止。G08のB0数値推定/B1 slope/DRIVと混同しない。DGP-006、NEG-006/007、REF-I03/REF-G01は別科学Evidence。
- G05 restricted Row Parquetには独立admin-owned KeyStoreとEd25519 Policy Envelope、domain-separated JCS signature/run_id/Study approval digest/issuer role/expiry/revocation/column/row/byte limitsを全て検証した`VerifiedStudyPolicyEvidence`が必要。`RowEffectsParquetWriter`は`LocalPrivacyPolicy.authorize`の後でのみbounded row bytesをG01 StagingSinkへ作成し、G01 Publisher/Readerが唯一のpublication/readback Authority。実際の独立Approver／admin鍵Store管理者／失効・OS/Parquet検証が未配備ならRow ReleaseをBLOCKED、mock署名を本番許可としない。
- OD-05の40 Method専用Config/Question/Design/Output/Inference Profileは各Owner Gate（G02=6、G03=13、G04=8、G06=3、G07=3、G08=5、G09=2）で完成・登録されるまでは`METHOD_PROFILE_UNAVAILABLE`で該当Methodをfail-closed。P1-M06のG01 Draftを除く40件を`config={}`で一括許可しない。G10は全41 Methodの実Backend/Lock/独立DGP/NEG/REF/CI/Regressionを検証するのみ。
- 全決定は設計選択としてOwner採用済みであり、実Source/Test/uv.lock、実効Backend/独立Science、Contract Freeze、Coding Authorization、Customer LegalのPASSを意味しない。

**G10 independent negative obligations:** 41 Method Schema/Backend/Inferenceをsource+fixture SHAで照合し、P1-M05 B0/B1/DRIV誤分類、IDENTIFY result.json誤発行、G05偽Ed25519 signature/untrusted admin store、RowSource事前反復、revocation midrun/byte cap超過、missing Method Configをnegativeとする。実行とDeploy Authorityの独立Evidenceが未取得なら`BLOCKED`、Generator自身のResultはOracleではない。

## 4. Verification operation, evidence and decision

- Fixed Trial Candidate SHAと実効checkoutが同じsemantic implementation stateか監査。上流Gateのcanonical 999 PASSとprotected contractをSource上の根拠で照合。
- 40 Test Agentは`tests/enhancement/enh_e11/<gate>/`を始点に、関連する`tests/product/`/`tests/integration/`等を現物から発見、test existence/collection/fixture/conftest/dependencies/runner/FS/backendを確認。07にhistorical filename/commandを固定しない。
- Test evidenceにはItem ID/DD ID、actual path/command、source/fixture/lock SHA、effective OS/FS/backend、Known truth/observed output、positive+negative、PASS/FAIL/BLOCKEDと原因を記録。Evidence commitとCandidate SHAを混同しない。
- Independent Test Agentはproduct/test code/runner/CI/06/07を修復しない。Product不変違反を実証したときFAIL、Test-side/UNKNOWN/Backend/独立Oracle不足でProduct判定不能ならBLOCKED。
- G01〜G10各Gateの999は独立であり、Methodごとの未実施・Science未検証・Protected Regression欠落がある限りGate PASS禁止。

## 5. Freeze前のOwner/Science review

未PASS GateをG10単独でPASS扱いすること、統計Method一律閾値、法務未審査の配布許可を禁止。

Method-specific strict Schema・positive/negative・独立Reference/推論Method/CI・threshold・Backend/License・Gate境界/depends/quant computeをレビューし、07をFreezeして初めて実行可能。現時点ではTest NOT_RUN、999 NOT_EXECUTED。
