# ENH-E7 G04 Gate Contract Amendment 01 — Protected Regression Method

**Amendment ID:** `ENH-E7-G04-09-01`  
**Status:** EFFECTIVE_FOR_TRIAL02_AND_LATER  
**Authority:** G04 Gate Contract Amendment; it amends the verification method of frozen Gate 07 only.  
**Effective trial:** G04 Trial02  
**Human authority input:** 2026-08-15 failure-triage conclusion  
**Product-code change authorized by this amendment:** No

## 1. Facts / trigger evidence

1. G04 Trial01 Test Item 010 ran `.venv/bin/pytest -q` on fixed candidate
   `4f9efd1a738303fba49a245511faf7ca3ba333b7` and reported 9 failures.
2. The same nine node IDs were rerun against the G03-start predecessor, G02 Fixed
   Candidate `ba9fd568e20458468f18edf312100499bb03290d`; all nine failed again.
   The reproduction was `9 failed, 14 passed`.
3. Therefore no one of the nine failures is introduced by G04.  Each is a
   pre-existing baseline failure in the time axis.
4. The assertions are also obsolete or inconsistent with the current authoritative
   contract: ResultType/status design, FR-114 command idempotency, or the G02/G03
   canonical Analysis Family/Stage architecture.
5. G03 requires absence of the old global shell and duplicate navigation.  G04
   protects that architecture.  Restoring old DOM, independent Explore/Predictive
   workspaces, or old six-route tokens is not an admissible remediation.

Trial01 evidence and its `999` decision are historical evidence.  This amendment
does not revise them and does not convert their formal FAIL into PASS.

## 2. Amendment rationale

### 2.1 Defect in the original verification method

Frozen Gate 07 AC-G04-15 has the semantic claim:

> Project/domain/backend/API/persistence protected semantics regressionなし。

Its Test Item 010 method described this as `full regression`.  Trial01 interpreted
that method as an unconditional requirement that every repository pytest node pass.
That interpretation makes a pre-existing, non-authoritative assertion a G04 blocking
condition and is not a direct verification of the AC-G04-15 semantic claim.

### 2.2 Non-amendment boundary

This amendment does **not** weaken AC-G04-15, FR-114, ResultType/status semantics,
or the functional availability of Exploratory/Predictive analysis.  It replaces an
unscoped test-selection method with an explicit current protected regression set and
requires replacement verification for every exclusion.

## 3. Original contract and amended contract

| Aspect | Original Gate 07 contract | Amended contract for Trial02+ |
| --- | --- | --- |
| AC-G04-15 semantic claim | protected semantics regressionなし | **Unchanged** |
| Test Item 010 blocking method | repository-wide pytest all PASS, as interpreted in Trial01 | Current Protected Regression Set (CPRS) must all PASS; Known Baseline Exclusions are reported separately and do not decide AC-G04-15 |
| Old UI compatibility | broad suite could require old DOM/tokens | old global shell, independent Explore/Predictive workspace, and old six-route tokens must not be restored; canonical route behavior is verified directly |
| Command idempotency | unscoped suite admitted callers without a header | FR-114 remains mandatory; replacement tests must supply `Idempotency-Key` before asserting business semantics |

## 4. Amended semantics — Current Protected Regression Set (CPRS)

All CPRS members are blocking for AC-G04-15.  Test Item 010 in Trial02 shall state
the exact node IDs and command in its report; a passing aggregate count without the
member list is insufficient.

| CPRS member | Protected semantic | Required verification assets |
| --- | --- | --- |
| CPRS-01 G03 current surface architecture | three exclusive top-level surfaces; Family horizontal/Stage vertical; obsolete global shell and duplicate bindings absent | `test_enh_e7_g03_p01_*` through `p06_*`, plus G04 browser structural journey |
| CPRS-02 G01 current canonical Project semantics | `/projects`, create, selected Project lifecycle, Context/Data/Results ownership | `test_enh_e7_g01_p01_*` through `p07_*` |
| CPRS-03 G02 current canonical Analysis semantics | canonical Analysis Family/Stage route, mapped Causal/Exploratory/Predictive operation, legacy normalization, cross-surface history | `test_enh_e7_g02_p01_*` through `p06_*` and G04 Items 004–009 |
| CPRS-04 ENH-E6 Family/Stage semantics | transition authority and stage presentation | `test_enh_e6_g01_p01_navigation_transition.py`, `test_enh_e6_g01_p02_stage_presentation.py` |
| CPRS-05 current Project/domain/backend/API/persistence semantics | domain snapshot/state contract; canonical command/API error behavior; PostgreSQL persistence contract; archive, graph-outcome, Predictive execution and lineage semantics | existing current tests selected by semantic node ID, including the re-enabled replacements in section 5; `test_domain_and_snapshot.py` excluding obsolete node 01; `test_api_worker_e2e.py`; `test_postgres_contract.py` when its environment prerequisite is met |
| CPRS-06 G04 reintegration contract | root/project routing, PM selection, context/family/stage state, history, resource/operation regression | `test_enh_e7_g04_p01_*` through `p06_*` and required browser harnesses |

`CPRS-05` is not satisfied by merely omitting failing nodes.  Its Trial02 manifest
must name and pass replacement nodes for the four API business-semantic paths and
the ResultType/status contract below.  A PostgreSQL prerequisite that is unavailable
is BLOCKED, not SKIPPED/PASS.

## 5. Known Baseline Exclusions and mandatory replacement verification

The following exclusions are limited to Test Item 010's CPRS selection.  They do
not delete the tests, alter Trial01 evidence, or declare the underlying product
semantics optional.

| ID | Failure / baseline evidence | Inconsistency with current contract and exclusion reason | Replacement verification / re-enable condition |
| --- | --- | --- | --- |
| KBE-01 | `test_domain_and_snapshot.py::test_scientific_status_is_exact_design_contract`; FAIL on Trial01 and `ba9fd56` | exact old 20-value enum assertion excludes documented `TRAINED`, `TRAINED_WITH_WARNINGS`, `EVALUATED`, `INSUFFICIENT_TEST_SAMPLE`, `NOT_APPLICABLE`; it is not the current ResultType/status design | Synchronize expected statuses to the current ResultType/status design, preferably ResultType-specific. Re-enable when the revised node passes and rejects undocumented statuses. |
| KBE-02 | `test_enh_e2_contract.py::test_project_delete_is_idempotent_archive_and_all_new_writes_are_guarded`; Trial01 and `ba9fd56`: expected 202, got 400 | request omits required `Idempotency-Key`; it never reaches archive semantics. FR-114 must remain enforced | Add a header, assert 202, archive idempotence and guarded-write behavior. Re-enable when this header-valid business-semantic node passes. |
| KBE-03 | `test_enh_e2_contract.py::test_inference_rejects_missing_or_tampered_graph_outcome`; Trial01 and `ba9fd56`: expected 409, got 400 | request omits required `Idempotency-Key`; Graph outcome mismatch/required validation is not reached | Add a header and assert `GRAPH_OUTCOME_MISMATCH` (409) and `GRAPH_OUTCOME_REQUIRED` (422) as applicable. Re-enable when the header-valid node passes. |
| KBE-04 | `test_enh_e3_api_worker_e2e.py::test_research_context_to_cross_family_results_lineage_annotation_and_export`; Trial01 and `ba9fd56`: missing `execution_id` after 400 | Predictive execution submit omits required `Idempotency-Key`; no cross-family/lineage behavior is asserted after the API boundary | Add a header, assert 202 and `execution_id`, then execute the cross-family result/annotation/export lineage predicates. Re-enable when this E2E node passes. |
| KBE-05 | `test_enh_e3_api_worker_e2e.py::test_g6_frontend_closes_context_common_selectors_results_and_six_routes`; Trial01 and `ba9fd56`: old `data-route="explore"` absent | old six-token Project shell conflicts with G02 canonical Analysis Family/Stage routing and G03 obsolete-shell absence | Verify canonical `/projects/<id>/analysis/<family>/<stage>`, legacy URL normalization, and visible-root/state synchronization. Re-enable only as a rewritten canonical-route test; never by restoring old tokens. |
| KBE-06 | `test_exploratory_frontend_contract_e3.py::test_explore_workspace_is_an_explicit_non_causal_vertical_slice`; Trial01 and `ba9fd56`: `data-workspace="explore"` absent | independent Explore workspace is replaced by the G02 mapped Exploratory Family/Stage surface | Verify mapped Exploratory stage operability, non-causal terminology, deep link/reload and history in the canonical Analysis surface. Re-enable only with those predicates. |
| KBE-07 | `test_predictive_explanation_e3.py::test_api_worker_persists_explanation_model_card_artifacts_and_lineage`; Trial01 and `ba9fd56`: missing `execution_id` after 400 | Predictive execution submit omits required `Idempotency-Key`; explanation/model-card persistence is not reached | Add a header, then assert 202, execution, explanation/model-card artifacts, and lineage. Re-enable when the header-valid node passes. |
| KBE-08 | `test_predictive_frontend_contract_e3.py::test_predictive_workspace_exposes_complete_g5_backend_vertical_slice`; Trial01 and `ba9fd56`: independent `predictive` workspace absent | independent Predictive workspace is obsolete under G02 mapped Family/Stage architecture | Verify Predictive mapped stages, backend capability gating, non-causal terminology and canonical route behavior. Re-enable only as a mapped-stage test. |
| KBE-09 | `test_predictive_frontend_contract_e3.py::test_project_shell_recognizes_six_routes_and_restores_predictive_deep_links`; Trial01 and `ba9fd56`: old route tokens absent | old six-route token/restore implementation is not the current canonical routing contract | Verify canonical deep links, legacy normalization, reload, Back/Forward, visible surface and selected Family/Stage. Re-enable only as a canonical routing test. |

## 6. Requirements-authority impact

The original FR-104/105 wording, "6 route-backed tabs" and their deep-link behavior,
must not be interpreted as requiring six peer DOM tabs or the historical
`context/data/explore/causal/predictive/results` token implementation.

The effective E7 requirements delta is amended alongside this document to preserve
the functional access/deep-link intent through this mapping:

| Original functional category | Current authoritative route/surface |
| --- | --- |
| Research Context | Project Management Research Context route |
| Data | Project Management Data route |
| Explore | canonical Analysis route, `EXPLORATORY` Family and catalog Stage |
| Causal | canonical Analysis route, `CAUSAL` Family and catalog Stage |
| Predictive | canonical Analysis route, `PREDICTIVE` Family and catalog Stage |
| Results | Project Management Results route |

Each destination remains route-addressable and must support the applicable direct
link, reload and Back/Forward semantics.  This is a clarification of information
architecture and verification authority, not an acceptance-criteria weakening.

## 7. Trial02 Gate 07 / Test Item plan application

For Trial02 and later, use frozen Gate 07 as amended by this document:

1. AC-G04-15 text and MUST severity remain unchanged.
2. Test Item 010 is renamed in its Trial02 report to
   `protected_current_regression_bundle` and covers CPRS-01 through CPRS-06.
3. Its exact command must enumerate the selected test node IDs or use a committed,
   versioned manifest that expands to those IDs.  It must report the manifest
   contents, exit code, result count, and environment prerequisites.
4. KBE-01 through KBE-09 are reported in a separate Known Baseline Exclusion table.
   They are non-blocking for AC-G04-15 only while their named replacement and
   re-enable condition are tracked.
5. G04 Items 004–009 retain their existing direct browser/API assertions.  They are
   not replaced by a source-token search.
6. Any failure in a CPRS member is a formal FAIL.  Missing manifest, unavailable
   required PostgreSQL prerequisite, or ambiguous replacement mapping is BLOCKED.

## 8. Trial02 entry conditions

- This amendment and the companion E7 requirements clarification are present and
  reviewed as the effective Trial02 authority.
- A versioned CPRS manifest or an equivalent exact-node command is prepared.
- KBE-01 through KBE-09 are listed in Test Item 010 with their replacement
  verification and re-enable condition; no silent deselection is permitted.
- Header-valid replacement tests exist for KBE-02, KBE-03, KBE-04 and KBE-07.
- ResultType/status replacement coverage exists for KBE-01.
- Canonical-route replacement coverage exists for KBE-05, KBE-06, KBE-08 and KBE-09.
- No Product code change is required by this amendment.  A Product change is only
  authorized by later independent evidence of a CPRS semantic failure.

## 9. Scope guard

- This amendment does not authorize Product, migration, or dependency changes.
  Trial02 preparation may add or revise verification assets only.
- No Trial01 report or Trial01 `999` decision is modified.
- No old global shell, independent Explore/Predictive workspace, old six-route token,
  or FR-114 relaxation is authorized.
