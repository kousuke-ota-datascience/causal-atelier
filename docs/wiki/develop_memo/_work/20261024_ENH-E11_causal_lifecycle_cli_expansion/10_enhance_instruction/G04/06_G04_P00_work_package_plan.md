# ENH-E11 G04 P00 — Work Package Plan (DRAFT)

**DEC-PREPCODE-01=B（Owner 2026-11-22採用）：Gate別S09→S10→S11。** G04の独立S09監査は、先行Gate（G02+G03）と共通E11 Wire/Port/Privacy/JCS/Publisher/Reader/Protected v2の変更影響閉包、およびG04自身の06/P00/Pxx/07/Method Profile/Backend/Scienceを対象とする。対象外Gateは全体SHA inventoryに保持し`NOT_REVIEWED`、未決の後続MethodはG04のCoding前無条件停止条件にしない。G04固有の独立S09 verdict→Owner G04-S10 Freeze→Owner G04-S11 Coding Authorizationを別々に取得する。**S11実行前にはG02_999・G03_999の実PASSが必須**だが、S09文書監査の準備は先行Gateの実装中にも可能。実Adapter/FS/数値T2/T3/RegressionはG04の独立07/999で検証し、文書修正だけでPASSを付けない。現時点は`S09_NOT_RUN/S10_NOT_FROZEN/S11_NOT_AUTHORIZED`。

**Gate:** G04 / Official Enhance Workflow Gate  
**Class:** Planning/Operator Artifact, not Coding Agent's normative package  
**Plan status:** OWNER_REVIEW_APPROVED / NOT_FROZEN / CODING_NOT_AUTHORIZED  
**Gate06:** [Implementation Contract](06_Ariadne_ENH-E11_G04_implementation_instruction.md)  
**Gate07:** [Independent Verification Draft](07_Ariadne_ENH-E11_G04_test_instruction.md) / DRAFT / NOT_FROZEN / TESTS_NOT_RUN  
**Owner-approved execution mode:** WORK_PACKAGE / P01,P02,P03,P04  
**Owner-approved upstream dependency:** G02 PASS, G03 PASS。2026-11-18 JST Owner一括レビューで承認。各上流canonical 999 PASSは未成立、Runtimeで別途検証する。

**Owner review:** PREP-03 Final AuditのOD-04（G04 Gate Dependency / Required Packages / Package DAG）を承認。Planの承認はGate06/07 Freeze、Owner Coding Authorization、Agent実行を許可しない。科学Method・Privacy Authority・Row Writer等のOpen Decisionを維持する。参照：[`PREP03_final_audit.md`](../PREP03_final_audit.md) §6。

## 1. Gate semantic acceptance

7種Non-IV CATEとDRIV IV異質効果を個別Estimand/Inferenceで提供する。

**主要不確実性:** Non-IV CATE、IV heterogeneous slope、B0 LATE、B1 linear slopeを同一視しない。G03依存はまとめReviewで検討。

## 2. Package ownership map

| Package | Scope | Required Pxx deps | Method | Package obligations |
|---|---|---|---|---|
| P01 | econml_dml_dr | NONE | P2-M01,P2-M02,P2-M03,P2-M04 | EconML版/APIとX/W、crossfit/nuisance/propensity、Estimator別InferenceAvailableを検証。 |
| P02 | s_t_x_learners | P01 | P2-M05,P2-M06,P2-M07 | 既存Outcome Model再利用。Treatment別support、counterfactual予測、point-only/CI明示。 |
| P03 | driv_iv_slope | P01 | P2-M08 | Z/A/X/WのIV relevancy/weak-IVと構造係数Targetを確認し、LATE/ATEへcastしない。 |
| P04 | cate_results | P01,P02,P03 | — | 8 Method Result/CI可用性/Local CLIを統合。G05承認前の個票出力禁止。 |


**Owner採用 OD-05（2026-11-19）：** G04の8 Methodについて、既決Target/数理は変更せず、担当Pxxでそれぞれstrict versioned `Method Config / Question / Design / Output / Inference Profile`を独立に定義・登録する。Method固有の確認項目は「EconML DML/DR/final learner、X/W roles、binary treatment、nuisance folds/seed、CATE inference point-only境界、DRIV theta_IV(x)とB0/B1分離」。条件付き必須Field、Backend effective API/version/optional extras、positive/invalid-config/wrong-target/unsupported-CI/negative-science fixtureとtyped reasonを固定する。未登録/未検証は`METHOD_PROFILE_UNAVAILABLE`等でfail-closed。単なる`config={}`、Backend default、未生成DGP/REF、K/R/MC-SE未実測をPASSとしない。これはProfile作成の**担当配分採用**であり、個々のSchema/Inference/科学Referenceの完成・Freeze・Coding Authorizationを意味しない。

## 3. Execution DAG and handoff

- `P01` <- NONE
- `P02` <- P01
- `P03` <- P01
- `P04` <- P01,P02,P03

Each Pxx→focused verification→20 Package Report→Checkpoint SHA。全required Package完了→Candidate Assembly→Gate-wide self-verification→single fixed candidate SHA→Independent 07→canonical 999。Package Completed≠ReadyForTest≠PASS。

## 4. Governance / Coding Authorization

P00は独立受入条件でも実装許可でもない。06/07 Freeze、Owner採用のPackage list/dependency、上流Gate canonical 999、実基準SHAとenvironment preflightが揃うまでPxxは実行禁止。Issue、Package結果、P00の状態を999代用にしない。

## PREP-04.1 integration preflight (DRAFT)
- P2-M01 owner P01: all five strict profiles and DGP-003; NEG-011, NEG-012, NEG-013; REF-E05; no SCIENCE PASS from schema presence.
- P2-M02 owner P01: all five strict profiles and DGP-004; NEG-010, NEG-012, NEG-013; REF-E05; no SCIENCE PASS from schema presence.
- P2-M03 owner P01: all five strict profiles and DGP-003, DGP-004; NEG-011, NEG-012, NEG-013; REF-E05, REF-E03; no SCIENCE PASS from schema presence.
- P2-M04 owner P01: all five strict profiles and DGP-004; NEG-010, NEG-011, NEG-013; REF-E05, REF-E03; no SCIENCE PASS from schema presence.
- P2-M05 owner P02: all five strict profiles and DGP-002, DGP-003; NEG-010, NEG-012, NEG-013; REF-E05; no SCIENCE PASS from schema presence.
- P2-M06 owner P02: all five strict profiles and DGP-003, DGP-004; NEG-010, NEG-013; REF-E05; no SCIENCE PASS from schema presence.
- P2-M07 owner P02: all five strict profiles and DGP-003, DGP-004; NEG-011, NEG-012, NEG-013; REF-E05; no SCIENCE PASS from schema presence.
- P2-M08 owner P03: all five strict profiles and DGP-008; NEG-009, NEG-012, NEG-013; REF-E06; no SCIENCE PASS from schema presence.

## S02 / G04のSelf-contained Method・非スカラー出力契約（Owner承認）

対象`P2-M01〜P2-M08`の8件。5 Profile kindは`23_api_interface_design/schema_drafts/method_profiles/factored/e11_<kind>_factored_v1.json`（kind=method_config/question_profile/design_profile/output_profile/inference_profile）＋Method ID別overlayを再構成し、`e11_method_profile_dispatch_registry_draft1.json`で厳密dispatch/Blob SHA/Method正負例/標準Draft202012 Parityを確認。closed schema断片を`allOf`結合しない。未検証/unknown Methodには`METHOD_PROFILE_UNAVAILABLE`を返す。全8 MethodがEffect scalar `result.json`の`point=NOT_AVAILABLE`（ターゲットが関数であるため）と独立typed `cate_surface.json`をManifestに記載し、observed rowではない事前指定Design grid上の評価値・SHA・Method/Estimandを保存する。P2-M01〜07はnon-IV `NON_IV_CATE`、P2-M08は条件付きIV `CONDITIONAL_IV_STRUCTURAL_SLOPE`。両者を同一CATEと混同しない。個人レベル`X_i`やCATE値は公開しない。個票のbounded ParquetはG05のみが明示Study `row_export_requested=true`＋nonroot private ext4/XFS/Method別列行byte/memory capsで審査してG01 Sinkへ。共通SchemaはEconMLのmethod-specific inferenceを保証しない。

正規Context`LocalRunContext(root,principal)`とPrivacy Port`authorize(*,study,root,principal,output_shape)`。署名Verifier/Policy Anchor・Study`policy_ref`・追加CLI flagは撤廃。独立07は8 Methodの実Backend API、fitted inference、CI unsupportedをtyped、CATE grid mismatch/observed rows leak/IV target錯誤/Result scalar偽装/Manifest readback/hashの正負例を検査。既存KernelとProduct v2公開ABIを保護する。未実行をScience PASSにしない。

## S09 documented non-scalar output correction — P2-M01–M08 (2026-11-22)

The initial E11 output for each supported P2-M01–M08 `ESTIMATE` is a **non-scalar** conditional-effect function: P2-M01–07 = `NON_IV_CATE`; P2-M08 = `CONDITIONAL_IV_STRUCTURAL_SLOPE` (not ordinary CATE, B0 LATE or B1 coefficient). For a valid eligible run, `result.json` (`e11-local-effect-result/1`) must encode `point.availability=NOT_AVAILABLE`, `point.value=null`, and `point.reason.code=NON_SCALAR_TARGET` (not a top-level Result `point_availability` field); `status.json` separately reports `point_availability=NOT_AVAILABLE`; it must **not** present any fabricated scalar mean/ATE as the target. The Manifest inventories separate `cate_surface.json` with `schema_drafts/internal_scientific/e11_cate_surface_draft1.schema.json` semantics: method/estimand binding, immutable `predeclared_grid_ref`, `grid_origin`, unique typed `grid_key`, finite effects, inference availability and correct Study/source hashes. `observed_rows_included=false` is mandatory. Only predeclared **non-observed** design grid values are eligible; neither observed `X_i` nor individual effect rows may be placed there. User-specific row output remains a separate G05 Study-opt-in/private bounded Parquet path. If no admissible predeclared grid exists, fail with typed `GRID_UNSPECIFIED`, not an implicit training-data grid or empty-success file. JSON Schema shape is not proof of privacy or scientific correctness.

**P00 sequencing:** P01–P03 own numerical evaluation for their allocated Methods, P04 owns common typed Artifact/Bundle wiring. Required integration is a fixed-source `result.json`+`cate_surface.json` Manifest/Reader test; no individual-row disclosure.
