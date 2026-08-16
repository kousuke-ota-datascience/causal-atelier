# G04 Trial02 Gate Decision

- Decision: PASS
- Fixed Trial Candidate full SHA: `d2d5a9a7f6df352d787c8d561fce937012eef854`
- Tested Repository State full SHA: `9e85e4a6a2365869b48e5bc6c0b0ac6845698869`
- Decision method: Gate 07 Test Items 001–010, with Test Item 010 applied by the effective Trial02 Gate Contract Amendment 09.

## Test Item summary

| Item | Result | Direct evidence |
| --- | --- | --- |
| 001 candidate_identity | PASS | Candidate resolved; candidate-to-HEAD diff is evidence-only reports. |
| 002 root_and_project_route_contract | PASS | G04 P01 `3 passed`; Chromium root/Project route checkpoints PASS. |
| 003 project_management_navigation_state | PASS | G04 P02 `3 passed`. |
| 004 analysis_context_family_stage_state | PASS | G04 P03 `4 passed`. |
| 005 cross_surface_history | PASS | G04 P04 `3 passed`; Chromium history scenarios PASS. |
| 006 legacy_resource_routing | PASS | G04 P05 `4 passed`. |
| 007 analysis_operation_regression | PASS | Header-valid archive/graph/Predictive/lineage replacements and operation predicates pass in CPRS. |
| 008 full_product_browser_journey | PASS | Five Chromium success scenarios PASS. |
| 009 history_reload_console_browser | PASS | reload/Back/Forward and no console/page errors. |
| 010 protected_current_regression_bundle | PASS | CPRS regular `89 passed`; browser PASS; PostgreSQL `4 passed`. |

## AC direct assertion / predicate summary

| AC | Supporting Test Item(s) | Direct predicate summary |
| --- | --- | --- |
| AC-G04-01 | 002, 008, 009 | `/` replaces to `/projects`; no duplicate-history path observed. |
| AC-G04-02 | 002, 008 | Project collection/new/overview route transitions and selected Project assertions. |
| AC-G04-03 | 003, 008 | PM URL, selected section, and exclusive visible PM root. |
| AC-G04-04 | 004 | Context selection/restoration does not rewrite Family/Stage state or create a default resource. |
| AC-G04-05 | 004, 008 | Catalog-derived default Stage, selected Family/Stage/content consistency, Family/Stage browser switches. |
| AC-G04-06 | 005, 008 | PM to canonical Analysis transition with Project identity retained. |
| AC-G04-07 | 005, 008 | Analysis to Project Management return with exclusive PM root. |
| AC-G04-08 | 005, 008 | Analysis to Results/Lineage transition and return history. |
| AC-G04-09 | 002, 005, 008, 009 | deep route/reload/Back/Forward synchronize URL, visible root, and Project state. |
| AC-G04-10 | 006, 010 | legacy analytical routes normalize to canonical Family/Stage behavior. |
| AC-G04-11 | 006 | resource-authoritative restore retains canonical semantics without backend/persistence change. |
| AC-G04-12 | 007, 008, 010 | Causal/Exploratory/Predictive operation semantics plus Data Quality read-only boundary. |
| AC-G04-13 | 003–006, 008, 010 | exactly one G03 top-level surface root; old global shell is not required or restored. |
| AC-G04-14 | 005, 008, 009 | no stale shell, duplicate transition, console, or page-error evidence in the required journey. |
| AC-G04-15 | 007, 010 | CPRS exact manifest passes all current protected semantics, including PostgreSQL prerequisite. |

## Facts

All Gate 07 blocking Test Items passed.  Test Item 010 uses the committed Trial02 CPRS manifest under Amendment 09: it preserves AC-G04-15's semantic claim and severity while replacing the Trial01 unscoped full-suite method.  The 9 historical Trial01 failures remain recorded unchanged and are traceable as KBE-01..09 with replacement nodes and re-enable conditions.

The current checkout is an evidence-only descendant of the Fixed Trial Candidate.  No Product, test, migration, or dependency code was modified during this independent verification; only the canonical Trial02 test reports were written.

## Interpretation

The fixed Trial Candidate satisfies every MUST AC with direct evidence.  No verified Product regression or required-environment blocker was observed.  Per Gate 07 decision semantics, the decision is PASS.

## Protected contract relation

This decision applies frozen Gate 07, with only Test Item 010's method amended for Trial02+ by `09_ENH-E7_G04_Trial02_Gate_Contract_Amendment.md`.  It neither changes AC-G04-15 nor revises the Trial01 formal FAIL.

## Reproduction procedure

Use the exact commands recorded in Items 002–010.  For protected regression, run `.venv/bin/python scripts/test/run_enh_e7_g04_trial02_cprs.py` and inspect `tests/product/manifests/enh_e7_g04_trial02_cprs.json`.

## Browser evidence

`test-results/browser_e2e/enh-e7-project-integration-evidence.json` reports all five scenarios PASS; the runner asserts an empty console/page-error collection and retains success screenshots.
