# ENH-E11 G02 P00 — Work Package Plan (DRAFT)

**DEC-PREPCODE-01=B（Owner 2026-11-22採用）：Gate別S09→S10→S11。** G02の独立S09監査は、先行Gate（G01）と共通E11 Wire/Port/Privacy/JCS/Publisher/Reader/Protected v2の変更影響閉包、およびG02自身の06/P00/Pxx/07/Method Profile/Backend/Scienceを対象とする。対象外Gateは全体SHA inventoryに保持し`NOT_REVIEWED`、未決の後続MethodはG02のCoding前無条件停止条件にしない。G02固有の独立S09 verdict→Owner G02-S10 Freeze→Owner G02-S11 Coding Authorizationを別々に取得する。**S11実行前にはG01_999の実PASSが必須**だが、S09文書監査の準備は先行Gateの実装中にも可能。実Adapter/FS/数値T2/T3/RegressionはG02の独立07/999で検証し、文書修正だけでPASSを付けない。現時点は`S09_NOT_RUN/S10_NOT_FROZEN/S11_NOT_AUTHORIZED`。

**Gate:** G02 / Official Enhance Workflow Gate  
**Class:** Planning/Operator Artifact, not Coding Agent's normative package  
**Plan status:** OWNER_REVIEW_APPROVED / NOT_FROZEN / CODING_NOT_AUTHORIZED  
**Gate06:** [Implementation Contract](06_Ariadne_ENH-E11_G02_implementation_instruction.md)  
**Gate07:** [Independent Verification Draft](07_Ariadne_ENH-E11_G02_test_instruction.md) / DRAFT / NOT_FROZEN / TESTS_NOT_RUN  
**Owner-approved execution mode:** WORK_PACKAGE / P01,P02,P03,P04  
**Owner-approved upstream dependency:** G01 PASS。2026-11-18 JST Owner一括レビューで承認。各上流canonical 999 PASSは未成立、Runtimeで別途検証する。

**Owner review:** PREP-03 Final AuditのOD-04（G02 Gate Dependency / Required Packages / Package DAG）を承認。Planの承認はGate06/07 Freeze、Owner Coding Authorization、Agent実行を許可しない。科学Method Profile/Backend・Privacy deployment等の未実装を維持する。参照：[`PREP03_final_audit.md`](../PREP03_final_audit.md) §6。

## 1. Gate semantic acceptance

Native/DoWhy識別、推定適格性、FD-A限定線形効果を安全に区別する。

**OD-05採用:** G02のP1-M01〜05・P1-M07（計6 Method）はそれぞれstrict Method Config/Question/Design/Output/Inference Profileを定義・登録し、invalid config/Estimand/Backendとunsupported CIをtyped negativeにする。専用Schema/Backend実測/独立Oracleが未実装なら当該Methodは`METHOD_PROFILE_UNAVAILABLE`等でBLOCKED。採用済Targetの再決定を求めない。

**主要不確実性:** P1-M05はOwner採用の`B0_BINARY_IV`・二値Z/A無調整complier `LATE_COMPLIER`の**条件付き識別のみ**。実効DoWhy IV式・Graph/Design仮定・Hashを明示的に検証し、display labelからLATEへcastしない。Method Profile/Backend/独立Scienceは未実証。 FD-A識別成立と数値推定成立は別。

## 2. Package ownership map

| Package | Scope | Required Pxx deps | Method | Package obligations |
|---|---|---|---|---|
| P01 | native_identification | NONE | P1-M01,P1-M02 | 既存randomized/backdoor識別・adjustment/Graph Validatorを再利用。非識別とProof/Upstream整合を厳格化。 |
| P02 | dowhy_identification | P01 | P1-M03,P1-M04,P1-M05 | DoWhy optional実効API/BackendとGraph/estimandを検証。IV内部labelをLATEへcastせず、P1-M05は明示的B0 conditional LATEのみ対象とし、専用Profile/API未検証はtyped BLOCKED。 |
| P03 | frontdoor_fd_a | P01,P02 | P1-M07 | 単一Mediator FD-Aの識別仮定と限定二段階線形数値を別契約で実装。一般Frontdoor Formulaへの拡張禁止。 |
| P04 | identification_dispatch | P01,P02,P03 | — | IDENTIFY/ESTIMATEのOperation別必須Bundleと未識別時Estimator未呼出、旧v2互換を実証。 |

## 3. Execution DAG and handoff

- `P01` <- NONE
- `P02` <- P01
- `P03` <- P01,P02
- `P04` <- P01,P02,P03

Each Pxx→focused verification→20 Package Report→Checkpoint SHA。全required Package完了→Candidate Assembly→Gate-wide self-verification→single fixed candidate SHA→Independent 07→canonical 999。Package Completed≠ReadyForTest≠PASS。

## 4. Governance / Coding Authorization

P00は独立受入条件でも実装許可でもない。06/07 Freeze、Owner採用のPackage list/dependency、上流Gate canonical 999、実基準SHAとenvironment preflightが揃うまでPxxは実行禁止。Issue、Package結果、P00の状態を999代用にしない。

## PREP-04.1 strict Method contract status (DRAFT / NOT_FROZEN)
- **P1-M01 / P01**: IDENTIFY; strict config required identification_rule; Design required treatment, outcome, allocation_unit, randomization_evidence_ref; DGP DGP-001, NEG-001/NEG-027, REF-G01/REF-I01; API/Science NOT_VERIFIED.
- **P1-M02 / P01**: IDENTIFY; strict config required identification_rule, adjustment_columns; Design required treatment, outcome, adjustment_columns, graph_evidence_ref, backdoor_proof_ref; DGP DGP-002,DGP-021, NEG-002/NEG-003, REF-G01/REF-I01; API/Science NOT_VERIFIED.
- **P1-M03 / P02**: IDENTIFY; strict config required identification_rule, adjustment_columns; Design required treatment, outcome, adjustment_columns, graph_evidence_ref, backdoor_proof_ref; DGP DGP-002,DGP-021, NEG-002/NEG-027, REF-G01/REF-I01; API/Science NOT_VERIFIED.
- **P1-M04 / P02**: IDENTIFY; strict config required identification_rule, mediator_column; Design required treatment, outcome, mediator, graph_evidence_ref, frontdoor_proof_ref; DGP DGP-005, NEG-004, REF-G01/REF-I02; API/Science NOT_VERIFIED.
- **P1-M05 / P02**: IDENTIFY; strict config required design_profile, monotonicity_direction; Design required treatment, outcome, instrument, treatment_binary, instrument_binary, adjustment_columns, monotonicity_direction, relevance_assumption_ref, independence_assumption_ref, exclusion_assumption_ref, monotonicity_assumption_ref, consistency_assumption_ref, graph_evidence_ref; DGP DGP-006, NEG-006/NEG-007, REF-I03/REF-G01; API/Science NOT_VERIFIED.
- **P1-M07 / P03**: ESTIMATE; strict config required estimation_rule, mediator_column, mediator_model_spec_ref, outcome_model_spec_ref; Design required treatment, outcome, mediator, frontdoor_proof_ref, no_direct_path_assumption_ref, linear_mediator_model_ref, linear_outcome_model_ref, graph_evidence_ref; DGP DGP-005, NEG-004/NEG-005, REF-I02/REF-E04; API/Science NOT_VERIFIED.
Schema files are under Revised IF23 schema_drafts/method_profiles. They are not yet runtime-registered; no invented backend signatures/CI. Actual independent 07 remains blocking.


## S02：担当Method Profile・共通署名の規範（G02 / Owner承認）

担当Methodは`P1-M01, P1-M02, P1-M03, P1-M04, P1-M05, P1-M07`。共通5 Profile Kind（method_config/question_profile/design_profile/output_profile/inference_profile）を`23_api_interface_design/schema_drafts/method_profiles/factored/e11_<kind>_factored_v1.json`から読み、exact Method IDのoverlayと共通Schemaを単一JSON Schemaに再構成する。Dispatch Registry `e11_method_profile_dispatch_registry_draft1.json`を照合し、Git Blob SHA・Draft202012 Schema・正例/負例が未確認なら`METHOD_PROFILE_UNAVAILABLE`でfail-closed。閉objectの別々の`allOf`合成で`additionalProperties:false`を破綻させない。Operation/Estimand/Backend/CI・DGP/NEG/REF/ACはMethodごとの科学契約に従い、共通化から科学Targetを推測しない。特にP1-M05はB0二値IV/無調整complier `LATE_COMPLIER`の条件付きIDENTIFY専用で数値Effectを生成しない。

`LocalRunContext(root:TrustedLocalRoot,principal:LocalPrincipal)`と`LocalPrivacyPolicyPort.authorize(*,study,root,principal,output_shape)`を共通署名とし、署名PolicyVerifier/Anchor・`cli_row_flag`・Study`privacy.policy_ref`は実装しない。G05以外では個票直接出力禁止、G05でもStudy `row_export_requested=true`と非root同一UID/private ext4/XFS・Method Schema/capsが全件必要。新Local GraphはProduct Version ID=null、content hashと科学由来を使い、Product DB GraphVersionをlookup/生成しない。既存Scientific Kernel・旧Product v2を保護し、回帰は影響閉包に基づいて選択、未知影響なら試験またはBLOCK。Method固有の実Backend/Inference・独立科学Referenceは未確認であり、Science PASSとはしない。
