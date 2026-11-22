# ENH-E11 G07 P00 — Work Package Plan (DRAFT)

**Gate:** G07 / Official Enhance Workflow Gate  
**Class:** Planning/Operator Artifact, not Coding Agent's normative package  
**Plan status:** OWNER_REVIEW_APPROVED / NOT_FROZEN / CODING_NOT_AUTHORIZED  
**Gate06:** [Implementation Contract](06_Ariadne_ENH-E11_G07_implementation_instruction.md)  
**Gate07:** [Independent Verification Draft](07_Ariadne_ENH-E11_G07_test_instruction.md) / DRAFT / NOT_FROZEN / TESTS_NOT_RUN  
**Owner-approved execution mode:** WORK_PACKAGE / P01,P02,P03  
**Owner-approved upstream dependency:** G01 PASS, G02 PASS。2026-11-18 JST Owner一括レビューで承認。各上流canonical 999 PASSは未成立、Runtimeで別途検証する。

**Owner review:** PREP-03 Final AuditのOD-04（G07 Gate Dependency / Required Packages / Package DAG）を承認。Planの承認はGate06/07 Freeze、Owner Coding Authorization、Agent実行を許可しない。科学Method・Privacy Authority・Row Writer等のOpen Decisionを維持する。参照：[`PREP03_final_audit.md`](../PREP03_final_audit.md) §6。

## 1. Gate semantic acceptance

DiD/Event/ITSをtiming・pretrend・cluster・serial correlation条件付きで実行する。

**主要不確実性:** 2x2とstaggered DiDを同一TWFE ATTへ還元せず、ITSにiid SEを無検証適用しない。

## 2. Package ownership map

| Package | Scope | Required Pxx deps | Method | Package obligations |
|---|---|---|---|---|
| P01 | did_event | NONE | P3-M04,P3-M05 | Cohort/adoption timing/parallel trend/pretrend、reference period、cluster covarianceを保持。 |
| P02 | interrupted_ts | NONE | P3-M06 | Intervention level/slope、seasonality、serial covariance/HACのmethod-specific evidence。 |
| P03 | quasi_integration | P01,P02 | — | Panel/time index/Design不適格のtyped negative、Local Effect/Manifestと旧v2を統合。 |


**Owner採用 OD-05（2026-11-19）：** G07の3 Methodについて、既決Target/数理は変更せず、担当Pxxでそれぞれstrict versioned `Method Config / Question / Design / Output / Inference Profile`を独立に定義・登録する。Method固有の確認項目は「DiD 2x2 vs staggered ATT、event-time reference cohort/period、cluster covariance、ITS介入時点のlevel/slope/HAC/serial dependence」。条件付き必須Field、Backend effective API/version/optional extras、positive/invalid-config/wrong-target/unsupported-CI/negative-science fixtureとtyped reasonを固定する。未登録/未検証は`METHOD_PROFILE_UNAVAILABLE`等でfail-closed。単なる`config={}`、Backend default、未生成DGP/REF、K/R/MC-SE未実測をPASSとしない。これはProfile作成の**担当配分採用**であり、個々のSchema/Inference/科学Referenceの完成・Freeze・Coding Authorizationを意味しない。

## 3. Execution DAG and handoff

- `P01` <- NONE
- `P02` <- NONE
- `P03` <- P01,P02

Each Pxx→focused verification→20 Package Report→Checkpoint SHA。全required Package完了→Candidate Assembly→Gate-wide self-verification→single fixed candidate SHA→Independent 07→canonical 999。Package Completed≠ReadyForTest≠PASS。

## 4. Governance / Coding Authorization

P00は独立受入条件でも実装許可でもない。06/07 Freeze、Owner採用のPackage list/dependency、上流Gate canonical 999、実基準SHAとenvironment preflightが揃うまでPxxは実行禁止。Issue、Package結果、P00の状態を999代用にしない。

## PREP-04.1 integration preflight (DRAFT)
- P3-M04 owner P01: five strict profiles and DGP-012, DGP-013; NEG-022; REF-Q01; science/backend BLOCKED.
- P3-M05 owner P01: five strict profiles and DGP-013; NEG-022; REF-Q01; science/backend BLOCKED.
- P3-M06 owner P02: five strict profiles and DGP-014; NEG-023; REF-Q02; science/backend BLOCKED.

## S02簡素化・G07 Quasi Method/Vector Outputの規範

担当Methodは`P3-M04` DiD、`P3-M05` Event Study、`P3-M06` ITSの3件。`23_api_interface_design/schema_drafts/method_profiles/factored/e11_<kind>_factored_v1.json`の5 kind（method_config/question_profile/design_profile/output_profile/inference_profile）からshared＋Method overlayを単一strict Schemaとして再構築し、Dispatch Registry、Blob SHA/標準Draft202012/parity/Method別正負例の証拠がなければ`METHOD_PROFILE_UNAVAILABLE`。DiDの2x2/staggered、Event Studyのcohort/time/reference period、ITSのlevel/slope/HAC/autocorrelationを混同しない。P3-M05ではscalar `result.json`のpointを`NOT_AVAILABLE`とし、cohort×event-timeのtyped `event_time_effects.json`と独立Manifest/ContentRefを発行。推論は実Method/Backendで対応が証明された場合のみAVAILABLE、指定period前のpretrend/介入時点負例とCI shape/Graph・Study lineageを独立07で検証する。

Contextは`LocalRunContext(root,principal)`、Privacy Portは`authorize(*,study,root,principal,output_shape)`。署名Verifier/Policy Anchor・`cli_row_flag`・Study `policy_ref`・追加CLI opt-inを設けない。個票はG05だけがStudy `row_export_requested=true`と非root同一UID private ext4/XFS/Method別capsをANDしてG01 Sinkへ。旧Product v2と共通KernelのABIを保護、科学Oracleと実Backend/CIを未実行ならScience BLOCKED。全Product Suite無条件実行ではなく影響閉包で回帰を決定、不明なら実行またはBLOCK。
