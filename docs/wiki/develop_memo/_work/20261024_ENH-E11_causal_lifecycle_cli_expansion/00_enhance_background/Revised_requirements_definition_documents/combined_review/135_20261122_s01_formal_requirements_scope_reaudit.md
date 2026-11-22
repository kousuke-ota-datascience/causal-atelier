# ENH-E11 / S01 — Formal Requirement and Scope Re-audit (2026-11-22)

**Record class:** enhancement-local review evidence (not a normative replacement, test result, contract freeze, or Coding Authorization).  
**Baseline:** `prototype/ariadne_mvp` HEAD `111f3f895a432e160a8528458f778def98819e14`, confirmed to equal the 2026-11-22 HANDOFF snapshot at review start.  
**Status:** `S01_REAUDIT_COMPLETED_WITH_DOCUMENT_FINDINGS / S02_OWNER_DECISIONS_PENDING / PREP05_FULL_INDEPENDENT_QA_NOT_RUN / CODING_NOT_AUTHORIZED`.  
**Changes:** this new review record only; source, tests, `pyproject.toml`, `uv.lock`, published canonical `docs/wiki/requirement_definition/`, and normative contracts not modified.

## 1. Audit universe and result

Parsed **all tabular FR/NFR/AR original requirement rows** across `10_10`–`10_18`, `10_20`–`10_22`, and `10_30`–`10_31` at baseline:
- **302 distinct requirement IDs**: FR=214, NFR=44, AR=44; zero duplicate IDs in these source tables.
- Historical pre-E11 requirements = 258 (FR=195, NFR=36, AR=27). Do **not** reclassify existing Product requirements as RETIRED merely because local E11 CLI does not implement Product Web/API/UI/RBAC.
- E11 issued = **44**: 19 FR (`FR-185`–`FR-203`), 8 NFR (`NFR-029`–`NFR-036`), 17 AR (`AR-028`–`AR-044`). **43 ACTIVE/UNVERIFIED/ENH-E11**, **one conditional MUST/DEFERRED/UNVERIFIED/FUTURE = NFR-034**. This corrects the historical baseline statements in RD03 and combined_review/133; combined_review/134 is the later authoritative Owner decision.
- Other existing `DEFERRED/FUTURE` requirements remain deferred (22 IDs: 14 FR plus 8 NFR), in addition to E11 NFR-034; not a mandate for E11 implementation.
- Existing ACTIVE/NOT_IMPLEMENTED requirements `FR-020`, `FR-145`, `NFR-023` are **existing Product gaps**, not implicit E11 deliverables. Other Product PARTIAL entries likewise remain existing Product/other-enhancement concerns.

Validated `doc01_review/rd03_review/96_rd03_formal_requirement_traceability.md`:
- **68 unique Scope IDs**: Phase1 21 / Phase2 18 / Phase3 19 / A0 X 10. Individual Owner-adopted R/Q/N/D dispositions remain intact. **D-only** rows (`P1-19`, `P3-18`, `X-01`, `X-02`, `X-03`, `X-07`, `X-08`) are **not initial E11 implementation obligations**. Mixed R/Q/N/D scope means implement/reuse/quality only the explicitly approved R/Q/N portion, not the D portion. `X-04` and `X-05` have the DEC06-approved bounded N portions; `X-09` and `X-10` exclude new Product integration.
- **41 unique approved Method IDs** (`P1-M01`–`P1-M20`, `P2-M01`–`P2-M08`, `P3-M01`–`P3-M13`); the standalone G01/P1-M06 schema is distinct from the **40 other Methods / 200 unverified draft profiles**. A draft schema is not evidence that a Method is implementable or scientifically accepted.
- **10 new E11 Concept UC** (`UC-01`–`UC-10`). `10_02_use_cases_e2e.md` separately describes **12 existing Product E2E scenarios** (`E2E-01`–`E2E-12`); these are distinct catalogs, **not** a contradiction in UC count.

## 2. Normative disposition recommendation by class

| Requirement class / scope | S01 proposed current disposition | Scientific, privacy, compatibility boundary |
| --- | --- | --- |
| 19 E11 FR (FR-185–203) | **KEEP ACTIVE**; deliver only approved R/Q/N, with D-only subscopes excluded | Scientific target, Graph/Identification/Estimator, diagnostics, CATE, temporal, quasi, IV, SCM, typed result, local execution, v2 protection. FR-195 retains practical local row privacy but does **not** itself prescribe two consent flags or corporate signing. |
| 7 E11 NFR (029–033,035–036) | **KEEP ACTIVE** | Provenance, atomic/no-false-success, local path and row security, optional dependency isolation, effective environments, independent science/FWER and legacy compatibility remain mandatory. Detailed *implementation mechanisms* may be simplified only if acceptance is preserved. |
| E11 NFR-034 | **KEEP MUST / DEFERRED / UNVERIFIED / FUTURE** | Conditional future recipient-specific license diligence, not a current Gate or a commitment to customer delivery. Internal OSS obligations remain in existing organization processes. |
| 17 E11 AR (028–044) | **KEEP ACTIVE** | All accepted Method/Estimand/negative/inference/weak-IV AR-set constraints remain. No reduction by user population assumption. |
| 258 historical Product rows | **KEEP existing row status/delivery**, no blanket E11 reclassification | Preexisting Product functionality and Product RBAC remains backward compatible; known Product gaps do not become E11 closure obligations. |
| 68 Scope rows | **KEEP DEC09 R/Q/N/D dispositions**; D-only explicitly outside current gate | 41 Method mapping, 10 E11 UC, 4 preexisting Product gaps, upstream scientific references remain separate. |
| Future customer governance and new Product integration | **NOT IN INITIAL E11**, with future requirement retained where NFR-034 applies | No new Product membership/roles, release approval, SBOM/legal-status fields, customer recipient workflow, Web/API/Worker/DB migration. |

**No additional RETIRED change proposed.** Retirement requires a positive Owner decision that the requirement itself is abolished; operational simplification is not equivalent to retiring the scientific or privacy requirement.

## 3. Concrete documentary and contract issues for S03–S09

1. **RD legend incomplete:** `10_00_overall_RD.md` `Delivery` legend lists BASELINE, ENH-E5, ENH-E7, ENH-E10 and FUTURE, but no **ENH-E11**, despite 43 ACTIVE E11 formal rows. Add `ENH-E11` without changing earlier Delivery semantics.
2. **Historical authority supersession:** `doc01_review/rd03_review/96_...` still states all 8 E11 NFR as ACTIVE; `combined_review/133` incorrectly states `NFR-034=RETIRED`; `combined_review/134` and the active `10_22` row are authoritative DEFERRED. Historical review records may remain immutable, but **current cross-contract/status matrices must not treat the former states as live**.
3. **Acceptance layering:** `10_91` §12 Product-wide E2E and ACTIVE obligations are not all E11 **new work**. `10_91` §12.1 is the Local E11 supplementary acceptance: 68 Scope, 41 Method, 10 UC, Source/Lock/Backend/DGP/NEG/REF, FWER, privacy, publication, v2 compatibility. Clarify Gate scope without deleting Product requirements.
4. **Reopened mechanisms not yet resolved:** `23_41`, `23_42`, `30_60`–`30_63` and G01/G05/G10 06/07 still include Study/CLI double opt-in, nullable `privacy.policy_ref`, redundant G10 Method rerun language, method-specific RowSchema and wide regression/fault matrices. These are **S02 options**, not approved removals.
5. **Pre-execution audit not equivalent to PASS:** Effective Backend/API/FS/Parquet, independent scientific reference, Method quantitative acceptance and current 06/Pxx/07 are still unverified/not frozen. Preserve fail-closed behavior.

## 4. Impacts and entry to S02

Source of truth for R/Q/N/D remains **DEC-SR04-09 Appendix A** and the RD03 68-row trace; for conditional NFR-034 status **combined_review/134** overrides combined_review/133. For the 8 options prepare Owner decisions with alternative, negative case, affected requirements/IF/DD/Schema/06/07 and specific proof needed. The approved decision ledger—not this review memo—will authorize downstream S03/S04 revisions.

**No Coding Agent, Independent Test Agent, Gate999, Source/test/lock change, Freeze or Coding Authorization performed.** 
