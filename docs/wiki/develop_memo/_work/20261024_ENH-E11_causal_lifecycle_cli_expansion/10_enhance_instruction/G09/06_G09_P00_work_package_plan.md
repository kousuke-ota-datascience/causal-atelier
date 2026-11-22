# ENH-E11 G09 P00 — Work Package Plan (DRAFT)

**Gate:** G09 / Official Enhance Workflow Gate  
**Class:** Planning/Operator Artifact, not Coding Agent's normative package  
**Plan status:** OWNER_REVIEW_APPROVED / NOT_FROZEN / CODING_NOT_AUTHORIZED  
**Gate06:** [Implementation Contract](06_Ariadne_ENH-E11_G09_implementation_instruction.md)  
**Gate07:** [Independent Verification Draft](07_Ariadne_ENH-E11_G09_test_instruction.md) / DRAFT / NOT_FROZEN / TESTS_NOT_RUN  
**Owner-approved execution mode:** WORK_PACKAGE / P01,P02,P03  
**Owner-approved upstream dependency:** G01 PASS。2026-11-18 JST Owner一括レビューで承認。各上流canonical 999 PASSは未成立、Runtimeで別途検証する。

**Owner review:** PREP-03 Final AuditのOD-04（G09 Gate Dependency / Required Packages / Package DAG）を承認。Planの承認はGate06/07 Freeze、Owner Coding Authorization、Agent実行を許可しない。科学Method・Privacy Authority・Row Writer等のOpen Decisionを維持する。参照：[`PREP03_final_audit.md`](../PREP03_final_audit.md) §6。

## 1. Gate semantic acceptance

Donor Designに基づきSCM point-onlyとSDID point/inferenceを区別する。

**主要不確実性:** Donor汚染・pre-fit・time support負例必須。SCMに未検証CIを付けない。

## 2. Package ownership map

| Package | Scope | Required Pxx deps | Method | Package obligations |
|---|---|---|---|---|
| P01 | scm_point | NONE | P3-M12 | Donor weights/pre-treatment RMSPE/fit・counterfactual gap。SCMは初期point-only。 |
| P02 | sdid_estimator | P01 | P3-M13 | unit/time weights、panel support、Method固有Variance/SE、SCMとの区別。 |
| P03 | synthetic_bundle | P01,P02 | — | donor contamination/pretreatment diagnostics・placeboとResult Bundle/Reader/old v2。 |


**Owner採用 OD-05（2026-11-19）：** G09の2 Methodについて、既決Target/数理は変更せず、担当Pxxでそれぞれstrict versioned `Method Config / Question / Design / Output / Inference Profile`を独立に定義・登録する。Method固有の確認項目は「SCM donor selection/preperiod fit/point-only、SDID unit/time weights/panel inference、contamination/supportとcounterfactual gap」。条件付き必須Field、Backend effective API/version/optional extras、positive/invalid-config/wrong-target/unsupported-CI/negative-science fixtureとtyped reasonを固定する。未登録/未検証は`METHOD_PROFILE_UNAVAILABLE`等でfail-closed。単なる`config={}`、Backend default、未生成DGP/REF、K/R/MC-SE未実測をPASSとしない。これはProfile作成の**担当配分採用**であり、個々のSchema/Inference/科学Referenceの完成・Freeze・Coding Authorizationを意味しない。

## 3. Execution DAG and handoff

- `P01` <- NONE
- `P02` <- P01
- `P03` <- P01,P02

Each Pxx→focused verification→20 Package Report→Checkpoint SHA。全required Package完了→Candidate Assembly→Gate-wide self-verification→single fixed candidate SHA→Independent 07→canonical 999。Package Completed≠ReadyForTest≠PASS。

## 4. Governance / Coding Authorization

P00は独立受入条件でも実装許可でもない。06/07 Freeze、Owner採用のPackage list/dependency、上流Gate canonical 999、実基準SHAとenvironment preflightが揃うまでPxxは実行禁止。Issue、Package結果、P00の状態を999代用にしない。

## PREP-04.1 integration checks
- P3-M12 strict owner profile and DGP-017; NEG-024; REF-Q04 required; no runtime availability inference.
- P3-M13 strict owner profile and DGP-018; NEG-024; REF-Q05 required; no runtime availability inference.

## S02簡素化・G09 Synthetic Counterfactual Profileの規範

担当Methodは`P3-M12` Synthetic Controlと`P3-M13` Synthetic DiD。5 Profile Kindは`23_api_interface_design/schema_drafts/method_profiles/factored/e11_<kind>_factored_v1.json`（method_config/question_profile/design_profile/output_profile/inference_profile）のshared core＋Method ID overlayを厳密に再構築する。Dispatch Registry/Blob SHA/200 Draft202012 positive/negative parityの証拠がないMethodは`METHOD_PROFILE_UNAVAILABLE`でfail-closed。P3-M12 SCMは**point-only**でCIを捏造しない。scalar Result.pointは`NOT_AVAILABLE`、内部`scm_gaps.json`に処置単位の時点別観測値・合成反実仮想・gap・Donor/Preperiod/Weightの独立ContentRefs/Hashを保持し、各時点`gap=observed-counterfactual`と時系列順序・donor contamination負例を検査する。P3-M13 SDIDは別のpanel平均ATTでありSCMと同一Estimand/推論を仮定しない。Method適格性・独立数値Oracle・実Backend/inferenceは未検証。

Context`LocalRunContext(root,principal)`と`LocalPrivacyPolicyPort.authorize(*,study,root,principal,output_shape)`を使用。Studyの`privacy.row_export_requested=true`とnonroot同一UID/private ext4/XFS/Method RowSchema/capsのAND判定による個票出力はG05のみ。本Gateでは個票の直接公開禁止。追加CLI flag、署名Verifier/Anchor、Study`policy_ref`を導入せず、Graph VersionはLocal content hash（Product Version IDs=null）で扱う。旧Product ABIとScientific Kernel共有/影響回帰/Source SHA固定、typed status／Manifest Readerの独立確認を維持し、未実行のScienceをPASSとしない。
