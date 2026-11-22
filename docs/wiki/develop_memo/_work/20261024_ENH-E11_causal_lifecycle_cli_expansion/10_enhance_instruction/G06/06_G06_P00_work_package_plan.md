# ENH-E11 G06 P00 — Work Package Plan (DRAFT)

**DEC-PREPCODE-01=B（Owner 2026-11-22採用）：Gate別S09→S10→S11。** G06の独立S09監査は、先行Gate（G01）と共通E11 Wire/Port/Privacy/JCS/Publisher/Reader/Protected v2の変更影響閉包、およびG06自身の06/P00/Pxx/07/Method Profile/Backend/Scienceを対象とする。対象外Gateは全体SHA inventoryに保持し`NOT_REVIEWED`、未決の後続MethodはG06のCoding前無条件停止条件にしない。G06固有の独立S09 verdict→Owner G06-S10 Freeze→Owner G06-S11 Coding Authorizationを別々に取得する。**S11実行前にはG01_999の実PASSが必須**だが、S09文書監査の準備は先行Gateの実装中にも可能。実Adapter/FS/数値T2/T3/RegressionはG06の独立07/999で検証し、文書修正だけでPASSを付けない。現時点は`S09_NOT_RUN/S10_NOT_FROZEN/S11_NOT_AUTHORIZED`。

**Gate:** G06 / Official Enhance Workflow Gate  
**Class:** Planning/Operator Artifact, not Coding Agent's normative package  
**Plan status:** OWNER_REVIEW_APPROVED / NOT_FROZEN / CODING_NOT_AUTHORIZED  
**Gate06:** [Implementation Contract](06_Ariadne_ENH-E11_G06_implementation_instruction.md)  
**Gate07:** [Independent Verification Draft](07_Ariadne_ENH-E11_G06_test_instruction.md) / DRAFT / NOT_FROZEN / TESTS_NOT_RUN  
**Owner-approved execution mode:** WORK_PACKAGE / P01,P02,P03  
**Owner-approved upstream dependency:** G01 PASS。2026-11-18 JST Owner一括レビューで承認。各上流canonical 999 PASSは未成立、Runtimeで別途検証する。

**Owner review:** PREP-03 Final AuditのOD-04（G06 Gate Dependency / Required Packages / Package DAG）を承認。Planの承認はGate06/07 Freeze、Owner Coding Authorization、Agent実行を許可しない。科学Method・Privacy Authority・Row Writer等のOpen Decisionを維持する。参照：[`PREP03_final_audit.md`](../PREP03_final_audit.md) §6。

## 1. Gate semantic acceptance

Temporal Graphのlag/endpoint不確実性を保持しPCMCI系をMethod別に実行する。

**主要不確実性:** time index/lag sign、contemporaneous/latentと独立Graph oracle必須。PAGをDAGへ勝手に変換しない。

## 2. Package ownership map

| Package | Scope | Required Pxx deps | Method | Package obligations |
|---|---|---|---|---|
| P01 | temporal_graph | NONE | — | G01 GraphValueを再利用しTemporalConvention/lag sign/time order/CI条件を検証。 |
| P02 | pcmci_adapters | P01 | P3-M01,P3-M02,P3-M03 | Tigramite lazy import、effective API、PCMCI+/LPCMCI endpoint/latent/lag、DGP oracle。 |
| P03 | temporal_bundle | P01,P02 | — | TIME_SERIES_GRAPH/Graph lossless hash/readbackとFCI旧Graphへの回帰。 |


**Owner採用 OD-05（2026-11-19）：** G06の3 Methodについて、既決Target/数理は変更せず、担当Pxxでそれぞれstrict versioned `Method Config / Question / Design / Output / Inference Profile`を独立に定義・登録する。Method固有の確認項目は「Tigramite CI test、lag sign/zero contemporaneous edge、time-index/order、PCMCI/PCMCI+/LPCMCI endpoint/latent/Graph proof」。条件付き必須Field、Backend effective API/version/optional extras、positive/invalid-config/wrong-target/unsupported-CI/negative-science fixtureとtyped reasonを固定する。未登録/未検証は`METHOD_PROFILE_UNAVAILABLE`等でfail-closed。単なる`config={}`、Backend default、未生成DGP/REF、K/R/MC-SE未実測をPASSとしない。これはProfile作成の**担当配分採用**であり、個々のSchema/Inference/科学Referenceの完成・Freeze・Coding Authorizationを意味しない。

## 3. Execution DAG and handoff

- `P01` <- NONE
- `P02` <- P01
- `P03` <- P01,P02

Each Pxx→focused verification→20 Package Report→Checkpoint SHA。全required Package完了→Candidate Assembly→Gate-wide self-verification→single fixed candidate SHA→Independent 07→canonical 999。Package Completed≠ReadyForTest≠PASS。

## 4. Governance / Coding Authorization

P00は独立受入条件でも実装許可でもない。06/07 Freeze、Owner採用のPackage list/dependency、上流Gate canonical 999、実基準SHAとenvironment preflightが揃うまでPxxは実行禁止。Issue、Package結果、P00の状態を999代用にしない。

## PREP-04.1 integration preflight (DRAFT)
- P3-M01 owner P02: all five strict profiles and DGP-009; NEG-021; REF-G03; no SCIENCE PASS from schema presence.
- P3-M02 owner P02: all five strict profiles and DGP-009, DGP-010; NEG-021, NEG-028; REF-G03, REF-G02; no SCIENCE PASS from schema presence.
- P3-M03 owner P02: all five strict profiles and DGP-011; NEG-021, NEG-028; REF-G03, REF-G02; no SCIENCE PASS from schema presence.

## S02簡素化・G06 Temporal GraphとMethod Profileの規範

担当Methodは`P3-M01` PCMCI、`P3-M02` PCMCI+、`P3-M03` LPCMCIの3件。5 Profile kind（method_config/question_profile/design_profile/output_profile/inference_profile）は`23_api_interface_design/schema_drafts/method_profiles/factored/e11_<kind>_factored_v1.json`のshared core＋exact Method ID overlayから再構成し、Dispatch Registry/200 Schema標準Draft202012/正負例/parityの確認が不足すれば`METHOD_PROFILE_UNAVAILABLE`でfail-closed。科学的契約は各Methodで異なり、time-lag端点の向き/ラグ0、PAG/CPDAG同値類、潜在交絡・CIテストの意味を厳格保存し、グラフ方向を自動確定しない。ENV-TIGRAMITEの実効Python3.12 APIと独立時系列Graph Oracleの実測は後続検証事項。

新Local Graphは内容hashとsource/parent科学由来を保持するがProduct GraphVersion DBはlookup/edit/write/FIXしない。`version_id=parent_version_id=null`のみ提供し、non-null importは未対応として拒否。共通`LocalRunContext(root,principal)`、`LocalPrivacyPolicyPort.authorize(*,study,root,principal,output_shape)`を利用し、署名Verifier/Policy Anchorと追加CLI flagを作らない。G06は個票を直接公開せず、旧Product v2のABIと共通Kernelを保護する。独立Testは時系列順序・PAG/CPDAG同値類・Graph hash/Manifest/readback・wrong Method/unsupported CIの負例を確認する。未実測をScience PASSとしない。
