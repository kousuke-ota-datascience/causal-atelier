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


**Owner採用 OD-05（2026-11-19）：** G07の3 Methodについて、既決Target/数理は変更せず、担当Pxxでそれぞれstrict versioned `Method Config / Question / Design / Output / Inference Profile`を独立に定義・登録する。Method固有の確認項目は「DiD DID_2X2 positive / STAGGERED DEFERRED preflight rejection ATT、event-time reference cohort/period、cluster covariance、ITS介入時点のlevel/slope/HAC/serial dependence」。条件付き必須Field、Backend effective API/version/optional extras、positive/invalid-config/wrong-target/unsupported-CI/negative-science fixtureとtyped reasonを固定する。未登録/未検証は`METHOD_PROFILE_UNAVAILABLE`等でfail-closed。単なる`config={}`、Backend default、未生成DGP/REF、K/R/MC-SE未実測をPASSとしない。これはProfile作成の**担当配分採用**であり、個々のSchema/Inference/科学Referenceの完成・Freeze・Coding Authorizationを意味しない。

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

## S09 documented Event Study vector contract — P3-M05 (2026-11-22)

P3-M05 `ESTIMATE` has an **event-time/cohort effect vector**, not a scalar target. For an eligible Event Study run, `result.json` has nested `point.availability=NOT_AVAILABLE`, `point.value=null`, `point.reason.code=NON_SCALAR_TARGET`, while `status.json` has top-level `point_availability=NOT_AVAILABLE`; the Manifest must inventory `event_time_effects.json` conforming to `schema_drafts/internal_scientific/e11_event_time_effects_draft1.schema.json`. It binds `method_id=P3-M05`, `study_ref`, `reference_period`, `time_unit`, cohort/event-time keyed `effects`, inference availability/interval references and `pretrend_diagnostics_ref`. The designated reference period and cohort/time support must be predeclared; unique event-time/cohort keys, finite effects, no invalid pretrend concealment, and exact readback/hash/lineage are required. Do not synthesize a scalar ATT/ATE from the vector or substitute an AR confidence set. Other Methods (DiD/ITS) retain their distinct output/inference contracts.

**P00:** Stage P01 event-time output and P03 integration on the same candidate; require independent 07 coverage for vector/reference/cohort and serialization.

## S09-R12 P3-M06 ITS conditional component payload contract (2026-11-22; DRAFT)

P3-M06 Output: P3-M06 Method Config `effect_components` is `LEVEL` or `LEVEL_AND_SLOPE` (no implicit default). All technically completed eligible ESTIMATE runs publish both `result.json` and a typed `its_components.json` (`schema_drafts/internal_scientific/e11_its_components_draft1.schema.json`) through G01 Sink/Manifest/Marker/Reader. `LEVEL`: scalar Result `point.availability=AVAILABLE`, `point.value=β_L` at declared intervention t0, with sidecar `level` only, `slope=null` and no post-horizon effects. `LEVEL_AND_SLOPE`: result has `point.availability=NOT_AVAILABLE`, `point.value=null`, `point.reason.code=NON_SCALAR_TARGET`, while sidecar contains β_L, β_S and only predeclared post-horizon `τ(t0+h)=β_L+β_S h` values; if no predeclared horizon exists, do not invent one. `status.json` separately has top-level `point_availability` matching Result. Require non-row-only `observed_rows_included=false`, unique integer `h`, finite estimates, declared intervention date, Method/Study/Design references and immutable source hashes. Do not treat marginal component CIs as joint simultaneous coverage, invent covariance, or mark HAC/NW inference AVAILABLE before method-specific validity and independently validated science. If requested confirmatory inference is not valid, use typed unsupported/unavailable rather than fabricated interval. The common public Result Schema is unchanged; all additional output is a versioned internal artifact, not a Product API/DB migration.

**Package boundary:** P00 sequences P02 estimator/output construction before P03 publication; each 07 scenario must reference the same fixed candidate and independent reference.

## Owner A frozen scope decision — DEC-S09-P3M04-01 (2026-11-22, instruction DRAFT)

**Owner DEC-S09-P3M04-01=A (2026-11-22):** P3-M04 initial science-executable variant is only `design_variant=DID_2X2` for two-group/two-period ATT; `STAGGERED` is a recognized future Config variant with capability `DEFERRED`, **not RETIRED** and not an eligible science target. Valid syntax does not imply execution. After strict validation, Method-level scientific preflight must reject `STAGGERED` with typed `SCIENCE_CONTRACT_NOT_AVAILABLE` / `CAPABILITY_UNAVAILABLE` (CLI exit4), before calling PanelQuasiAdapter/Estimator/Backend or any row-materializing scientific source; do not publish a successful `result.json`, `manifest.json` or committed success marker for that request. Unknown variant/invalid type/missing required Config are input-Schema failures (exit2). Do not fall back to DID_2X2, a TWFE coefficient, or P3-M05 Event Study. Valid DID_2X2 still needs Design, unit/time support, pre-declared parallel trends and cluster-covariance eligibility and independent DGP-012/NEG/REF-Q01 verification; no backend/science acceptance is yet established. DGP-013 remains relevant to P3-M05 and possible later STAGGERED research, but is not P3-M04 initial executable positive.

**Gate/Package-specific instruction:** P00 Gate DAG: P01 owns P3-M04 early capability gate, P03 owns publication guard, 07 owns independent observation; no new Method count or Phase scope.
