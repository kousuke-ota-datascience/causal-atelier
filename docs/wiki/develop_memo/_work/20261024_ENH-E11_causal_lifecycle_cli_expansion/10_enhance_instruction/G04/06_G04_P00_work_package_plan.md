# ENH-E11 G04 P00 — Work Package Plan (DRAFT)

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