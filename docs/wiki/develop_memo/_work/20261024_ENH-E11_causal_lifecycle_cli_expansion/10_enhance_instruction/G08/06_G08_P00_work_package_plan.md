# ENH-E11 G08 P00 — Work Package Plan (DRAFT)

**Gate:** G08 / Official Enhance Workflow Gate  
**Class:** Planning/Operator Artifact, not Coding Agent's normative package  
**Plan status:** OWNER_REVIEW_APPROVED / NOT_FROZEN / CODING_NOT_AUTHORIZED  
**Gate06:** [Implementation Contract](06_Ariadne_ENH-E11_G08_implementation_instruction.md)  
**Gate07:** [Independent Verification Draft](07_Ariadne_ENH-E11_G08_test_instruction.md) / DRAFT / NOT_FROZEN / TESTS_NOT_RUN  
**Owner-approved execution mode:** WORK_PACKAGE / P01,P02,P03,P04  
**Owner-approved upstream dependency:** G01 PASS, G02 PASS。2026-11-18 JST Owner一括レビューで承認。各上流canonical 999 PASSは未成立、Runtimeで別途検証する。

**Owner review:** PREP-03 Final AuditのOD-04（G08 Gate Dependency / Required Packages / Package DAG）を承認。Planの承認はGate06/07 Freeze、Owner Coding Authorization、Agent実行を許可しない。科学Method・Privacy Authority・Row Writer等のOpen Decisionを維持する。参照：[`PREP03_final_audit.md`](../PREP03_final_audit.md) §6。

## 1. Gate semantic acceptance

Sharp/Fuzzy RDDとB0/B1 IV/2SLSを局所Estimand・弱IV AR集合付きで提供する。

**主要不確実性:** B0 complier LATEとB1 structural slopeを区別。HC1 AR集合をfinite gridだけで判定しない。

## 2. Package ownership map

| Package | Scope | Required Pxx deps | Method | Package obligations |
|---|---|---|---|---|
| P01 | rdd_sharp_fuzzy | NONE | P3-M07,P3-M08 | cutoff/bandwidth/densityとFuzzy first stage、RBC CI API availabilityを検証。 |
| P02 | wald_late | NONE | P3-M09 | 二値Z/A・B0無調整LATE、first-stage weak/zero、IV independence/exclusion/monotonicityは証明済みとしない。 |
| P03 | two_sls_ar | P02 | P3-M10,P3-M11 | B0 Q=[1], B1 Q=[1,C]。Y−βA~Q+ZのHC1 χ²(1)全実数AR反転は独立数学・統計Reviewer承認前の候補（未Freeze）。全実数領域AR信頼集合、数学的EMPTYと数値FAILEDの区別は承認済み要求。 |
| P04 | rdd_iv_result | P01,P02,P03 | — | RDD/IV別Result、bounded/unbounded/disconnected AR、独立Reference/Coverage/weak IV検証とReader。 |


**Owner採用 OD-05（2026-11-19）：** G08の5 Methodについて、既決Target/数理は変更せず、担当Pxxでそれぞれstrict versioned `Method Config / Question / Design / Output / Inference Profile`を独立に定義・登録する。Method固有の確認項目は「Sharp/Fuzzy RD cutoff/bandwidth/kernel/order、B0/B1二値Z/A/C設計、全実数の弱IV頑健AR集合、独立科学審査待ちのHC1 χ²(1)反転候補（未Freeze）、推論/退化条件」。条件付き必須Field、Backend effective API/version/optional extras、positive/invalid-config/wrong-target/unsupported-CI/negative-science fixtureとtyped reasonを固定する。未登録/未検証は`METHOD_PROFILE_UNAVAILABLE`等でfail-closed。単なる`config={}`、Backend default、未生成DGP/REF、K/R/MC-SE未実測をPASSとしない。これはProfile作成の**担当配分採用**であり、個々のSchema/Inference/科学Referenceの完成・Freeze・Coding Authorizationを意味しない。

## 3. Execution DAG and handoff

- `P01` <- NONE
- `P02` <- NONE
- `P03` <- P02
- `P04` <- P01,P02,P03

Each Pxx→focused verification→20 Package Report→Checkpoint SHA。全required Package完了→Candidate Assembly→Gate-wide self-verification→single fixed candidate SHA→Independent 07→canonical 999。Package Completed≠ReadyForTest≠PASS。

## 4. Governance / Coding Authorization

P00は独立受入条件でも実装許可でもない。06/07 Freeze、Owner採用のPackage list/dependency、上流Gate canonical 999、実基準SHAとenvironment preflightが揃うまでPxxは実行禁止。Issue、Package結果、P00の状態を999代用にしない。

## PREP-04.1 integration preflight (DRAFT)
- P3-M07 owner P01: five strict profiles and DGP-015; NEG-023; REF-Q03; science/backend BLOCKED.
- P3-M08 owner P01: five strict profiles and DGP-016; NEG-006, NEG-023; REF-Q03, REF-I03; science/backend BLOCKED.
- P3-M09 owner P02: five strict profiles and DGP-006; NEG-006, NEG-007; REF-I03, REF-E07; science/backend BLOCKED.
- P3-M10 owner P03: five strict profiles and DGP-006, DGP-024; NEG-006, NEG-025; REF-E07, REF-U01; science/backend BLOCKED.
- P3-M11 owner P03: five strict profiles and DGP-007, DGP-024; NEG-008, NEG-025; REF-E08, REF-U01; science/backend BLOCKED.

## S02・DEC-S05-AR01：G08 Method ProfileとAR Authorityの正規境界

担当Methodは`P3-M07` Sharp RDD、`P3-M08` Fuzzy RDD、`P3-M09` Binary Wald、`P3-M10` B0 2SLS、`P3-M11` B1 2SLSの5件。`23_api_interface_design/schema_drafts/method_profiles/factored/e11_<kind>_factored_v1.json`の5 Profile Kind（method_config/question_profile/design_profile/output_profile/inference_profile）をshared core＋exact Method ID overlayへ再構成し、Dispatch Registry、200 Schema標準Draft202012/Blob SHA/正負例の検証なしには`METHOD_PROFILE_UNAVAILABLE`。Method別EstimandとInferenceを保つ。B0は二値Z/A・無調整complier LATE、B1は事前Cを含む構造的`LINEAR_IV_STRUCTURAL_COEFFICIENT`、Fuzzy RDはcutoff局所complier効果であり、名称だけでATE/ATT/CATEへのcast不可。

**DEC-S05-AR01（Owner A採用）**：全実数領域での弱IV robust Anderson–Rubin信頼集合（bounded/unbounded/disconnected/ALL_REAL、退化・EMPTY等の明示判定）は既承認必須。HC1 OLS係数＋χ²(1)漸近検定＋二次式反転という**具体的計算法は独立科学Reviewerの妥当性確認前の実装候補でありFreezeしていない**。本Pxx/06/07に既存のHC1記述があっても、Ownerがそれを最終承認したと解釈しない。レビュー済み数理導出、全実数位相/弱IV/zero first-stage/分散退化/coverage、独立Oracle/実効Backend、T2-T3事前登録とOwnerによる契約確定がない場合、G08の当該方法は`BLOCKED_SCIENCE_METHOD_NOT_FROZEN`でGate999 PASS禁止。Point estimatorの可用性からAR可用性を推論しない。P3-M09 WaldにはARが自動付帯しない。

共通`LocalRunContext(root,principal)`、`LocalPrivacyPolicyPort.authorize(*,study,root,principal,output_shape)`。署名Verifier/Policy Anchor・CLI row flag・Study `policy_ref`なし。G08は個票を公開しない。共通Scientific Kernelと既存Product v2を保護する。G10では41 Method全件の有効Science証拠が必要だが、推移的依存閉包のSHAが完全不変なら証拠再利用を認め、変更/不明分のみ再実行/BLOCK。
