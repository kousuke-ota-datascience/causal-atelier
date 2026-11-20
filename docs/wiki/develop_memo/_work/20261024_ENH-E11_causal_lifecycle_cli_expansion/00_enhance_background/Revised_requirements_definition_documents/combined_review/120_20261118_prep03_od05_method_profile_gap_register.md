# PREP-03 / OD-05 — Method profile completion inventory and Gate authoring contract

**Owner決定（2026-11-19）:** OD-05のGate別Profile作成・配置方式をOwner採用済み。この表は41 Methodの範囲確認と40 Methodのプロフィール実装残務を示すが、個々のJSON Schema/independent Scienceは未作成。正式決定は[DEC-PREP03-OD01–05](122_20261119_dec_prep03_od01_od05_owner_adoption.md) §1/5。

**Class:** FLOW / evidence-backed readiness register and design gap routing. NOT 41 approved Method Configs or backend test evidence.  
**Inventory baseline:** 68fb0b64021cc9ff372a0a7e3f13a406638da08f, `10_32_scientific_method_scope.md`, `23_api_interface_design/schema_drafts/` filenames.  
**Status:** `OD-05_PARTIALLY_OPEN / MATH_ALREADY_ADOPTED / 40_DRAFTS_AUTHORED_SCIENCE_PENDING`.

## 1. Verifiable discovery boundary

Reviewed `schema_drafts/`: G01 `P1-M06` has `e11_p1_m06_fci_method_config_v1.schema.json`, `e11_p1_m06_fci_question_profile_v1.schema.json` and `e11_p1_m06_fci_design_profile_v1.schema.json`, plus older G01 FCI drafts. **No dedicated per-Method schema file for the other 40 IDs appears in this reviewed directory.** This does not establish that source code or other directories contain no alternative implementation, and does not mean the mathematical targets are undecided.

Catalog: G01=1, G02=6, G03=13, G04=8, G06=3, G07=3, G08=5, G09=2. `G05` is cross-cutting and introduces zero new scientific Method IDs; `G10` validates the same 41, not 41 additional Method APIs. For G02–G09, per-method strict configuration and negative tests are necessary before declaring availability. Current `10_32` PLAN/evidence state `NOT_GENERATED` is not PASS.

## 2. Required frozen Method Profile for every offered ID

| Contract component | Required concrete fields / verification | Failure |
|---|---|---|
| Registry descriptor | Method ID, one Operation, target Estimand family/population/contrast, valid analysis mode, selected Backend ID/profile, output type | unregistered ID or incompatible pair rejects before backend call |
| Method Config schema | versioned strict JSON Schema, required properties, types/number domains, no unknown keys, method defaults only if *explicitly* specified and approved | `METHOD_PROFILE_UNAVAILABLE` if absent; `CONFIG_INVALID` on invalid provided config |
| Question/Design evidence | roles Y/A/Z/M/X/W/C when applicable, graph kind/endpoint assumptions, temporal/panel/time/lag/cutoff/units, adjustment/support, target population | `METHOD_INCOMPATIBLE` or typed scientific negative; never guess |
| Dataset contract | column schema/units, missingness, effective sample support, binary/discrete/temporal ordering and instrument relevance/overlap, row privacy classification | typed reason; no silent drop or target change |
| Effective backend | optional extras, installed distribution/version, effective API signature, solver/seed/fold, no optional import before `load_adapter`, pinned config/lock evidence | `CAPABILITY_UNAVAILABLE`, never alternative method |
| Inference policy | point-only vs supported finite CI/AR set, requested EXPLORATORY/CONFIRMATORY, confidence level, sample covariance/cluster/HAC, weak-IV/DRIV constraints | `INFERENCE_UNAVAILABLE`; no invented confirmatory CI |
| Result/Bundle & negatives | strict portable output schema version, operation-specific required/forbidden artifacts, absence/null reasons, source lineage/hash, privacy and Reader round-trip | invalid shape or unavailable content cannot commit as success |
| Independent Science | predefined DGP/NEG/REF truth, effective library, deterministic acceptance, T2 pilot/T3 preregistered K/R/FWER=.05, MC-SE/coverage, independent oracle | Science ACCEPTANCE=NOT_EVALUATED until actual evidence |

**Already decided:** 30_63 §§1–10, 10_32 and PREP02 F03–F07 define the scientific targets and architecture. Do not reopen ATE/ATT/LATE/DRIV/RDD/SCM target questions to fill a JSON Schema. A `config={}` placeholder is not an approved Method Profile.

## 3. Per-Method traceability (41/41)

| Method ID | Owner Gate | Operation | Current adopted method meaning (10_32) | Inspected dedicated schema status | Existing DGP/negative/reference obligation |
|---|---|---|---|---|---|
| `P1-M01` | G02 | IDENTIFY | Native Randomized identification／A | NO METHOD-SPECIFIC DRAFT FILE IN REVIEWED schema_drafts (not proof of absence elsewhere) | DGP-001; NEG-001, NEG-027; REF-G01, REF-I01 |
| `P1-M02` | G02 | IDENTIFY | Native Backdoor identification／ATE | NO METHOD-SPECIFIC DRAFT FILE IN REVIEWED schema_drafts (not proof of absence elsewhere) | DGP-002, DGP-021; NEG-002, NEG-003; REF-G01, REF-I01 |
| `P1-M03` | G02 | IDENTIFY | DoWhy Backdoor identification／ATE候 | NO METHOD-SPECIFIC DRAFT FILE IN REVIEWED schema_drafts (not proof of absence elsewhere) | DGP-002, DGP-021; NEG-002, NEG-027; REF-G01, REF-I01 |
| `P1-M04` | G02 | IDENTIFY | DoWhy Frontdoor identification／ATE | NO METHOD-SPECIFIC DRAFT FILE IN REVIEWED schema_drafts (not proof of absence elsewhere) | DGP-005; NEG-004; REF-G01, REF-I02 |
| `P1-M05` | G02 | IDENTIFY | DoWhy IV identification／B0条件付きcomplier LATE（OD-01採用済み） | NO METHOD-SPECIFIC DRAFT FILE IN REVIEWED schema_drafts (not proof of absence elsewhere) | DGP-006; NEG-006, NEG-007; REF-I03, REF-G01 |
| `P1-M06` | G01 | DISCOVER | FCI／PAGと等価類 | DRAFTS PRESENT (3 specific schema files; not runtime-verified) | DGP-011, DGP-021; NEG-003, NEG-021, NEG-028; REF-G02 |
| `P1-M07` | G02 | ESTIMATE | Frontdoor two-stage regression／ATE | NO METHOD-SPECIFIC DRAFT FILE IN REVIEWED schema_drafts (not proof of absence elsewhere) | DGP-005; NEG-004, NEG-005; REF-I02, REF-E04 |
| `P1-M08` | G03 | ESTIMATE | Native diff-in-means／ATE | NO METHOD-SPECIFIC DRAFT FILE IN REVIEWED schema_drafts (not proof of absence elsewhere) | DGP-001, DGP-022; NEG-001, NEG-010; REF-E01 |
| `P1-M09` | G03 | ESTIMATE | Native OLS／採用済み契約範囲のATE/ATT表現 | NO METHOD-SPECIFIC DRAFT FILE IN REVIEWED schema_drafts (not proof of absence elsewhere) | DGP-002, DGP-003; NEG-002, NEG-008, NEG-020; REF-E01, REF-I01 |
| `P1-M10` | G03 | ESTIMATE | Native IPW／ATE・ATT（別fixture） | NO METHOD-SPECIFIC DRAFT FILE IN REVIEWED schema_drafts (not proof of absence elsewhere) | DGP-002, DGP-003; NEG-010, NEG-018; REF-E02 |
| `P1-M11` | G03 | ESTIMATE | Native AIPW／ATE・ATT（別fixture） | NO METHOD-SPECIFIC DRAFT FILE IN REVIEWED schema_drafts (not proof of absence elsewhere) | DGP-002, DGP-003; NEG-010, NEG-011, NEG-012; REF-E03 |
| `P1-M12` | G03 | REFUTE | Placebo Treatment refutation／null診 | NO METHOD-SPECIFIC DRAFT FILE IN REVIEWED schema_drafts (not proof of absence elsewhere) | DGP-022; NEG-014; REF-R01 |
| `P1-M13` | G03 | REFUTE | Data Subset refutation／安定性 | NO METHOD-SPECIFIC DRAFT FILE IN REVIEWED schema_drafts (not proof of absence elsewhere) | DGP-001, DGP-002; NEG-015; REF-R01 |
| `P1-M14` | G03 | REFUTE | Random Common Cause refutation／摂動安 | NO METHOD-SPECIFIC DRAFT FILE IN REVIEWED schema_drafts (not proof of absence elsewhere) | DGP-002; NEG-017; REF-R01 |
| `P1-M15` | G03 | REFUTE | Bootstrap refutation／再標本化安定性 | NO METHOD-SPECIFIC DRAFT FILE IN REVIEWED schema_drafts (not proof of absence elsewhere) | DGP-001, DGP-002; NEG-016; REF-R01 |
| `P1-M16` | G03 | SENSITIVITY | Adjustment Set Sensitivity／設計変更 | NO METHOD-SPECIFIC DRAFT FILE IN REVIEWED schema_drafts (not proof of absence elsewhere) | DGP-021, DGP-002; NEG-002; REF-G01, REF-R01 |
| `P1-M17` | G03 | SENSITIVITY | Propensity Clipping Sensitivity／tr | NO METHOD-SPECIFIC DRAFT FILE IN REVIEWED schema_drafts (not proof of absence elsewhere) | DGP-002, DGP-023; NEG-010, NEG-018; REF-E02, REF-R01 |
| `P1-M18` | G03 | DIAGNOSE | Observed NCE null diagnostic／条件付き関 | NO METHOD-SPECIFIC DRAFT FILE IN REVIEWED schema_drafts (not proof of absence elsewhere) | DGP-019; NEG-019, NEG-026; REF-R02 |
| `P1-M19` | G03 | DIAGNOSE | Observed NCO null diagnostic／条件付き関 | NO METHOD-SPECIFIC DRAFT FILE IN REVIEWED schema_drafts (not proof of absence elsewhere) | DGP-019; NEG-019, NEG-026; REF-R02 |
| `P1-M20` | G03 | DIAGNOSE | OLS partial R² / RV sensitivity／指定 | NO METHOD-SPECIFIC DRAFT FILE IN REVIEWED schema_drafts (not proof of absence elsewhere) | DGP-020; NEG-020; REF-R03 |
| `P2-M01` | G04 | ESTIMATE | LinearDML／CATE(x) | NO METHOD-SPECIFIC DRAFT FILE IN REVIEWED schema_drafts (not proof of absence elsewhere) | DGP-003; NEG-011, NEG-012, NEG-013; REF-E05 |
| `P2-M02` | G04 | ESTIMATE | CausalForestDML／CATE(x) | NO METHOD-SPECIFIC DRAFT FILE IN REVIEWED schema_drafts (not proof of absence elsewhere) | DGP-004; NEG-010, NEG-012, NEG-013; REF-E05 |
| `P2-M03` | G04 | ESTIMATE | DRLearner／CATE(x) | NO METHOD-SPECIFIC DRAFT FILE IN REVIEWED schema_drafts (not proof of absence elsewhere) | DGP-003, DGP-004; NEG-011, NEG-012, NEG-013; REF-E05, REF-E03 |
| `P2-M04` | G04 | ESTIMATE | ForestDRLearner／CATE(x) | NO METHOD-SPECIFIC DRAFT FILE IN REVIEWED schema_drafts (not proof of absence elsewhere) | DGP-004; NEG-010, NEG-011, NEG-013; REF-E05, REF-E03 |
| `P2-M05` | G04 | ESTIMATE | S-Learner／CATE(x) | NO METHOD-SPECIFIC DRAFT FILE IN REVIEWED schema_drafts (not proof of absence elsewhere) | DGP-002, DGP-003; NEG-010, NEG-012, NEG-013; REF-E05 |
| `P2-M06` | G04 | ESTIMATE | T-Learner／CATE(x) | NO METHOD-SPECIFIC DRAFT FILE IN REVIEWED schema_drafts (not proof of absence elsewhere) | DGP-003, DGP-004; NEG-010, NEG-013; REF-E05 |
| `P2-M07` | G04 | ESTIMATE | X-Learner／CATE(x) | NO METHOD-SPECIFIC DRAFT FILE IN REVIEWED schema_drafts (not proof of absence elsewhere) | DGP-003, DGP-004; NEG-011, NEG-012, NEG-013; REF-E05 |
| `P2-M08` | G04 | ESTIMATE | DRIV-A／CONDITIONAL_IV_STRUCTURAL_SLOPE | NO METHOD-SPECIFIC DRAFT FILE IN REVIEWED schema_drafts (not proof of absence elsewhere) | DGP-008; NEG-009, NEG-012, NEG-013; REF-E06 |
| `P3-M01` | G06 | DISCOVER | PCMCI／time-lagged graph | NO METHOD-SPECIFIC DRAFT FILE IN REVIEWED schema_drafts (not proof of absence elsewhere) | DGP-009; NEG-021; REF-G03 |
| `P3-M02` | G06 | DISCOVER | PCMCI+／time-series CPDAG | NO METHOD-SPECIFIC DRAFT FILE IN REVIEWED schema_drafts (not proof of absence elsewhere) | DGP-009, DGP-010; NEG-021, NEG-028; REF-G03, REF-G02 |
| `P3-M03` | G06 | DISCOVER | LPCMCI／time-series PAG | NO METHOD-SPECIFIC DRAFT FILE IN REVIEWED schema_drafts (not proof of absence elsewhere) | DGP-011; NEG-021, NEG-028; REF-G03, REF-G02 |
| `P3-M04` | G07 | ESTIMATE | DiD／ATT（2×2とstaggeredは別契約） | NO METHOD-SPECIFIC DRAFT FILE IN REVIEWED schema_drafts (not proof of absence elsewhere) | DGP-012, DGP-013; NEG-022; REF-Q01 |
| `P3-M05` | G07 | ESTIMATE | Event Study／event-time効果 | NO METHOD-SPECIFIC DRAFT FILE IN REVIEWED schema_drafts (not proof of absence elsewhere) | DGP-013; NEG-022; REF-Q01 |
| `P3-M06` | G07 | ESTIMATE | Interrupted Time Series／介入時点のlevel | NO METHOD-SPECIFIC DRAFT FILE IN REVIEWED schema_drafts (not proof of absence elsewhere) | DGP-014; NEG-023; REF-Q02 |
| `P3-M07` | G08 | ESTIMATE | Sharp RDD／cutoff局所効果 | NO METHOD-SPECIFIC DRAFT FILE IN REVIEWED schema_drafts (not proof of absence elsewhere) | DGP-015; NEG-023; REF-Q03 |
| `P3-M08` | G08 | ESTIMATE | Fuzzy RDD／cutoff局所complier効果 | NO METHOD-SPECIFIC DRAFT FILE IN REVIEWED schema_drafts (not proof of absence elsewhere) | DGP-016; NEG-006, NEG-023; REF-Q03, REF-I03 |
| `P3-M09` | G08 | ESTIMATE | Wald ratio／binary Z/A complier LAT | NO METHOD-SPECIFIC DRAFT FILE IN REVIEWED schema_drafts (not proof of absence elsewhere) | DGP-006; NEG-006, NEG-007; REF-I03, REF-E07 |
| `P3-M10` | G08 | ESTIMATE | B0 just-identified 2SLS／binary Z/A | NO METHOD-SPECIFIC DRAFT FILE IN REVIEWED schema_drafts (not proof of absence elsewhere) | DGP-006, DGP-024; NEG-006, NEG-025; REF-E07, REF-U01 |
| `P3-M11` | G08 | ESTIMATE | B1-A／LINEAR_IV_STRUCTURAL_COEFFICIENT | NO METHOD-SPECIFIC DRAFT FILE IN REVIEWED schema_drafts (not proof of absence elsewhere) | DGP-007, DGP-024; NEG-008, NEG-025; REF-E08, REF-U01 |
| `P3-M12` | G09 | ESTIMATE | Synthetic Control／処置単位の時点別反実仮想ギャップ | NO METHOD-SPECIFIC DRAFT FILE IN REVIEWED schema_drafts (not proof of absence elsewhere) | DGP-017; NEG-024; REF-Q04 |
| `P3-M13` | G09 | ESTIMATE | Synthetic DiD／panel平均介入効果 | NO METHOD-SPECIFIC DRAFT FILE IN REVIEWED schema_drafts (not proof of absence elsewhere) | DGP-018; NEG-024; REF-Q05 |

## 4. Gate-by-Gate concrete Profile completion focus

| Gate | Mandatory scope-specific profile clauses | Actual decision boundary |
|---|---|---|
| G01 | FCI CI test API, conditional independence tests, PAG endpoints, alpha/lag and Graph proof; existing 3 draft files | Verify draft schema vs adopted G01 06/07 and effective backend; do not infer PASS |
| G02 | Randomized/Backdoor graph proof, DoWhy effective IV/frontdoor graph and target, explicit FD-A single-mediator linear equations/assumptions, no unidentifiable effect | P1-M05 B0 conditional LATE target already Owner adopted; everything else starts with adopted identification semantics |
| G03 | OLS target/contrast/variance, IPW normalized weights and positivity, AIPW nuisance/cross-fitting/finite-sample inference, refutation/resampling method, NCE/NCO conditional null, RV q=1 | Method-specific nuisance/CI and statistic distribution choices vs required independent evidence |
| G04 | DML/DR/forest learner X/W roles, treatment encoding, nuisance/folds/seed, inference eligibility, individual CATE privacy; DRIV `CONDITIONAL_IV_STRUCTURAL_SLOPE` | Do not equate default EconML CI with approved inference; collect versioned API evidence |
| G05 | No new Method; HTE row release depends on scientific Effect/Inference evidence plus signed policy and writer profiles | OD-02/03 separate actual security architecture gaps |
| G06 | ordered time-index, lag sign/lag zero, conditional independence test, PCMCI/PCMCI+/LPCMCI endpoint conventions, latent interpretation | Effective Tigramite API and independent Graph equivalence oracle must be verified |
| G07 | DiD 2×2 vs staggered, event-time cohort/reference period, cluster robust covariance, ITS level/slope/autocorrelation/HAC | Respect already adopted estimator policy, fill only missing numeric inference/CI configuration |
| G08 | Sharp/Fuzzy RD bandwidth/kernel/order, B0 vs B1 Z/A/C design, robust HC1 AR full-real confidence set and degenerate cases | Reconcile historical 111 “proposed deterministic reference” vs 30_63 concrete implementation authority; independent REF still pending |
| G09 | SCM donor eligibility/preperiod fit/point-only, SDID time+unit weight and panel inference | Do not add SCM confidence intervals or let donor leakage pass validation |
| G10 | 41 Method registry/Operation/readback/legacy compatibility, fixed science/prereg/licensing/lock | Verification owner; no new Method Target |

## 5. Work allocation and readiness semantics

1. Implement the approved strict **config/Question/Design/output profiles in the corresponding Gxx package**, not in a new CLI-only Scientific Kernel; keep MethodRegistry as the only acceptance authority.
2. Every Method's **positive + invalid-config + wrong-Estimand + negative-science + unavailable-backend + unsupported-CI** fixtures must be listed in the responsible Pxx and independent 07. DGP/NEG/REF names are currently verification obligations, not generated test datasets.
3. The 36 G02–G10 Pxx retain existing `Depends on Pxx`, class ownership and gate status. Profiles required by one Method do not automatically block an unrelated Gate Package.
4. Treat **method-config construction as coding/design implementation work**, not 40 new Owner decisions. Escalate only a missing statistical choice that affects meaning/inference and is not actually fixed by source-of-truth design.
5. **Important authority reconciliation:** the PREP02 F07 analysis `111_...` describes the HC1 quadratic realization as an engineering proposal, whereas 30_63 describes HC1/χ²(1) as intended implementation. Before G08 Freeze, explicitly reconcile whether Owner-adopted design includes that exact reference formula, without undoing the already adopted AR full-real confidence-set semantics. An independent numerical oracle is still necessary.

**Disposition:** `COVERAGE_REGISTER_COMPLETE / 40_METHOD_SPECIFIC_DRAFTS_NOT_LOCATED_IN_INSPECTED_FOLDER / RUNTIME_AND_SCIENCE_NOT_VERIFIED / OD-05_CONTRACT_FILL_PENDING`. The per-method work must be closed in self-contained 06/07/Pxx before any affected Gate Freeze; this document is not an execution instruction.

## PREP-04.1 2026-11-21 amendment

40 Method×5 strict internal JSON Schema Drafts authored; owner 06/Pxx/07 instructions across G02–G09 updated. Old P1-M05 target-unknown wording corrected to the Owner-adopted B0 conditional LATE. NOT_FROZEN: versioned backend API, science DGP/REF, numerical/CI AC, status alignment and independent validation not complete. This is authoring coverage, not independent scientific PASS.
