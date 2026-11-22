# ENH-E11 G03 P00 — Work Package Plan (DRAFT)

**DEC-PREPCODE-01=B（Owner 2026-11-22採用）：Gate別S09→S10→S11。** G03の独立S09監査は、先行Gate（G02）と共通E11 Wire/Port/Privacy/JCS/Publisher/Reader/Protected v2の変更影響閉包、およびG03自身の06/P00/Pxx/07/Method Profile/Backend/Scienceを対象とする。対象外Gateは全体SHA inventoryに保持し`NOT_REVIEWED`、未決の後続MethodはG03のCoding前無条件停止条件にしない。**G02_999の実PASS→独立G03 S09 verdict→Owner G03-S10 Freeze→Owner G03-S11 Coding Authorization**を各々確認するまでG03のCoding禁止。実Adapter/FS/数値T2/T3/RegressionはG03の独立07/999で検証し、文書修正だけでPASSを付けない。現時点は`S09_NOT_RUN/S10_NOT_FROZEN/S11_NOT_AUTHORIZED`。

**Gate:** G03 / Official Enhance Workflow Gate  
**Class:** Planning/Operator Artifact, not Coding Agent's normative package  
**Plan status:** OWNER_REVIEW_APPROVED / NOT_FROZEN / CODING_NOT_AUTHORIZED  
**Gate06:** [Implementation Contract](06_Ariadne_ENH-E11_G03_implementation_instruction.md)  
**Gate07:** [Independent Verification Draft](07_Ariadne_ENH-E11_G03_test_instruction.md) / DRAFT / NOT_FROZEN / TESTS_NOT_RUN  
**Owner-approved execution mode:** WORK_PACKAGE / P01,P02,P03,P04,P05,P06  
**Owner-approved upstream dependency:** G02 PASS。2026-11-18 JST Owner一括レビューで承認。各上流canonical 999 PASSは未成立、Runtimeで別途検証する。

**Owner review:** PREP-03 Final AuditのOD-04（G03 Gate Dependency / Required Packages / Package DAG）を承認。Planの承認はGate06/07 Freeze、Owner Coding Authorization、Agent実行を許可しない。科学Method・Privacy Authority・Row Writer等のOpen Decisionを維持する。参照：[`PREP03_final_audit.md`](../PREP03_final_audit.md) §6。

## 1. Gate semantic acceptance

Native推定と4 Refutation・2 Sensitivity・NCE/NCO/RVをEffect lineage付きで実行する。

**主要不確実性:** 非有意NCE/NCOは無交絡証明ではない。RVは古典OLS限定。P1-M11のScience未確定を黙認しない。

## 2. Package ownership map

| Package | Scope | Required Pxx deps | Method | Package obligations |
|---|---|---|---|---|
| P01 | native_effects | NONE | P1-M08,P1-M09 | 既存Treatment effect kernelのdiff-in-means/OLS再利用。割当/Target contrast/ATE-ATT区別。 |
| P02 | weighting_ipw_aipw | P01 | P1-M10,P1-M11 | 既存IPW/AIPWを共有しATE/ATT weight、ESS、balance、overlap、nuisance/seedを明示。 |
| P03 | refutation_methods | P01,P02 | P1-M12,P1-M13,P1-M14,P1-M15 | 既存run(input_,output_dir) API不変。M12/M13実装再利用、M14/M15不足Kernel追加、seedと元Effect hash必須。 |
| P04 | sensitivity_methods | P01,P02 | P1-M16,P1-M17 | 既存SensitivityAdapter.run公開ABI不変。Adjustment Set妥当性とPropensity Clippingによるtarget変化を保持。 |
| P05 | negative_controls_ols_rv | P01 | P1-M18,P1-M19,P1-M20 | 観測Z/W、事前帰無・opt-in・条件付き関連。OLS RV(q=1)は古典OLS coef/SE/df限定。 |
| P06 | diagnostics_pipeline | P03,P04,P05 | — | 13 MethodのREFUTE/SENSITIVITY/DIAGNOSE Bundleと旧Product v2回帰・Privacyを統合。 |


**Owner採用 OD-05（2026-11-19）：** G03の13 Methodについて、既決Target/数理は変更せず、担当Pxxでそれぞれstrict versioned `Method Config / Question / Design / Output / Inference Profile`を独立に定義・登録する。Method固有の確認項目は「OLS contrast/variance、IPW propensity/normalization/positivity、AIPW nuisance/crossfit/ATE-ATT score、Refutation resampling、NCE/NCO observed null、OLS RV q=1」。条件付き必須Field、Backend effective API/version/optional extras、positive/invalid-config/wrong-target/unsupported-CI/negative-science fixtureとtyped reasonを固定する。未登録/未検証は`METHOD_PROFILE_UNAVAILABLE`等でfail-closed。単なる`config={}`、Backend default、未生成DGP/REF、K/R/MC-SE未実測をPASSとしない。これはProfile作成の**担当配分採用**であり、個々のSchema/Inference/科学Referenceの完成・Freeze・Coding Authorizationを意味しない。

## 3. Execution DAG and handoff

- `P01` <- NONE
- `P02` <- P01
- `P03` <- P01,P02
- `P04` <- P01,P02
- `P05` <- P01
- `P06` <- P03,P04,P05

Each Pxx→focused verification→20 Package Report→Checkpoint SHA。全required Package完了→Candidate Assembly→Gate-wide self-verification→single fixed candidate SHA→Independent 07→canonical 999。Package Completed≠ReadyForTest≠PASS。

## 4. Governance / Coding Authorization

P00は独立受入条件でも実装許可でもない。06/07 Freeze、Owner採用のPackage list/dependency、上流Gate canonical 999、実基準SHAとenvironment preflightが揃うまでPxxは実行禁止。Issue、Package結果、P00の状態を999代用にしない。

## PREP-04.1 integration guards (DRAFT)
- P1-M08 owner P01 strict five-profile validation, negative Science DGP-001, DGP-022; NEG-001, NEG-010; REF-E01.
- P1-M09 owner P01 strict five-profile validation, negative Science DGP-002, DGP-003; NEG-002, NEG-008, NEG-020; REF-E01, REF-I01.
- P1-M10 owner P02 strict five-profile validation, negative Science DGP-002, DGP-003; NEG-010, NEG-018; REF-E02.
- P1-M11 owner P02 strict five-profile validation, negative Science DGP-002, DGP-003; NEG-010, NEG-011, NEG-012; REF-E03.
- P1-M12 owner P03 strict five-profile validation, negative Science DGP-022; NEG-014; REF-R01.
- P1-M13 owner P03 strict five-profile validation, negative Science DGP-001, DGP-002; NEG-015; REF-R01.
- P1-M14 owner P03 strict five-profile validation, negative Science DGP-002; NEG-017; REF-R01.
- P1-M15 owner P03 strict five-profile validation, negative Science DGP-001, DGP-002; NEG-016; REF-R01.
- P1-M16 owner P04 strict five-profile validation, negative Science DGP-021, DGP-002; NEG-002; REF-G01, REF-R01.
- P1-M17 owner P04 strict five-profile validation, negative Science DGP-002, DGP-023; NEG-010, NEG-018; REF-E02, REF-R01.
- P1-M18 owner P05 strict five-profile validation, negative Science DGP-019; NEG-019, NEG-026; REF-R02.
- P1-M19 owner P05 strict five-profile validation, negative Science DGP-019; NEG-019, NEG-026; REF-R02.
- P1-M20 owner P05 strict five-profile validation, negative Science DGP-020; NEG-020; REF-R03.


## S02：担当Method Profile・共通署名の規範（G03 / Owner承認）

担当Methodは`P1-M08〜P1-M20`の13件。共通5 Profile Kind（method_config/question_profile/design_profile/output_profile/inference_profile）は`23_api_interface_design/schema_drafts/method_profiles/factored/e11_<kind>_factored_v1.json`のshared core＋Method ID overlayを再構成して使用する。`e11_method_profile_dispatch_registry_draft1.json`とsource Git blob SHAを照合し、200 Profileの標準Draft202012チェック・Method別正負例未確認なら`METHOD_PROFILE_UNAVAILABLE`でfail-closedする。Method別OperationはP1-M08〜11がESTIMATE、M12〜15がREFUTE、M16〜17がSENSITIVITY、M18〜20がDIAGNOSE。後3群は正規`diagnostics.json`であり、架空のEffect Resultを作らない。共通Schema化は各Method固有のATE/ATT/統計量/推論条件を緩和しない。閉objectの別`allOf`合成禁止。実Backend/CIと独立Science DGP/NEG/REF/ACは別途実証が必須。

`LocalRunContext(root:TrustedLocalRoot,principal:LocalPrincipal)`および`LocalPrivacyPolicyPort.authorize(*,study,root,principal,output_shape)`が正規署名。追加のCLI row flag・`cli_row_flag`・`privacy.policy_ref`・独立署名PolicyVerifier/Anchorを実装しない。G05のみStudy `row_export_requested=true`と非root同一UID/private ext4/XFS・Method Schema/capsのANDで個票中間出力可。E11 Local GraphはProduct GraphVersion ID=null、content hashで科学由来を維持。旧Product v2 ABIと共通Scientific Kernelを保護し、無関係Product回帰の全件無条件再試験を課さず、変更影響を証明できない場合は実行またはBLOCK。科学受入・Coding Authorizationは未実施。
