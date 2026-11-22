# ENH-E11 S09 — Source Reference Integrity & G08 AR Candidate Author Semantic QA (2026-11-22)

**Type/authority:** `AUTHOR_BOUNDED_STATIC_QA`, not independent S09 review, not scientific/backend/Schema PASS, not S10 Freeze, not S11 Coding Authorization.  
**Review baseline:** `8563ed8a7ce73f778bfdc69f9a5494914d1e7856` (`DEC-S09-P3M04-01=A` propagated), then separate repair commits; latest G10 post-fix and G08 source content must be pinned by next review snapshot.  
**No new Owner decisions.** The A adoption for P3-M04 remains unchanged; DEC-S05-AR01=A retains full-real weak-IV AR confidence sets with HC1/χ² as an **unfrozen candidate**.

## 1. Bounded Markdown link integrity audit

At fixed checked-out GitHub branch source paths/tree, Author inspected every active G01–G10 `06/Pxx/07` Markdown source, seven Operator entry prompts, and 33 main stock RD/BD/IF/DD docs (not historical `prior_drafts`).

- 71 Gate files, **198** inline Markdown relative-link occurrences checked; per-Gate counts G01=24, G02=19, G03=19, G04=19, G05=18, G06=19, G07=19, G08=19, G09=19, G10=23. Four missing links found, all in G10 `06_G10_P04_science_benchmarks.md` source line 262.
- 7 Operator prompt files checked; **0** relative Markdown links of the included syntax, no missing links (not proof of referenced textual paths or actual agent functioning).
- 33 main stock RD/BD/IF/DD files: **50** inline Markdown relative links checked; no missing relative link. Breakdown RD selected 9 files/6 links, BD 18/19 links, IF 23_41/23_42 and DD 30_60–63 selected 6 files/25 links.
- **Total:** 111 Markdown files, 248 inline Markdown relative links observed, four broken targets found and corrected. Recheck of G10 post-fix: 8 files/23 links, **0 missing**. The other groups' link files were not modified by this link fix. All currently observed checked inline relative links resolve to a Git tree file/directory.
- **Former broken links:** in G10/P04 to `30_61_causal_domain_ports.md`, `30_62_local_execution_publication.md`, `../23_api_interface_design/23_41_cli_scientific_ports.md` and `../10_requirements_definition/10_32_scientific_method_scope.md`. They incorrectly resolved from the G10 directory. Replaced with correct `../../00_enhance_background/Revised_requirements_definition_documents/{30_detailed_design|23_api_interface_design|10_requirements_definition}/...` paths.
- **Scope limit:** inline Markdown `[label](relative_path)` only. Bare inline backtick paths, link fragment/heading anchors, HTML links, absolute HTTPS validity, dynamically generated Documentation links, source code import/file paths and symlink traversal are not validated by this limited check. No conclusion about full content or reviewer independence.

## 2. G08 AR source-of-truth contradiction corrected

The Owner accepted `DEC-S05-AR01=A`: retain full-real weak-IV-robust AR set and topology, but subject concrete HC1 OLS coefficient χ²(1) inversion to independent scientific review before algorithm Freeze. Previous amendments had appended this status while `G08/06_G08_P03_two_sls_ar.md` §4 and its embedded Mandatory Matrix still **instructed immediate HC1/χ²(1) algorithm implementation**. A coder could obey the embedded imperative and ignore the appendix, violating Method Freeze/approval authority.

Corrections to the primary G08 §4 instruction/Matrix:
1. State the mandatory WHAT as full-real weak-IV-robust set for approved B0/B1 targets.
2. State `Y−βA ~ Q+Z` HC1/χ² inversion, residualization and quadratic solver only as **unfrozen scientific-review candidate**, not executable method authority.
3. Preserve exact all-real tail, bounded/unbounded/disconnected/ALL_REAL and qualified EMPTY/variance/rank failure distinctions.
4. Explicitly fail-closed `BLOCKED_SCIENCE_METHOD_NOT_FROZEN` rather than selecting this candidate unilaterally.
5. Update historical OD-05/accepted allocation mentions in G08 main 06, P00, P01/P02/P03/P04 and 07 so that HC1 is not misread as already approved; 07 acceptance row now checks AR target and independent candidate review, not mandates an unapproved algorithm.

**Scientific author preflight only** is in `working_notes/20261122_s05_ar_hc1_candidate_author_mathematical_preflight.md`. In a local Python3.13.5/NumPy/Scipy/Statsmodels environment, author derived HC1 candidate inversion as a quadratic sign test restricted to strictly positive candidate variance and numerically reproduced bounded/disconnected/ALL_REAL using fixed seeds, independently checking 3×5 direct OLS+HC1 evaluation grid. This does not satisfy the 3.12 approved environment, reference independence, asymptotic weak-IV coverage, near-degenerate root verification or T2/T3, and does **not** freeze HC1.

## 3. Residual science/runtime independence and blockers

- S09: reviewer instruction `165` requires a separate reviewer/agent checking current full SHA (not this author), exact all 71+7 instruction/Operator sources and stock/scientific semantic constraints.
- S05-B02: Python3.12 `jsonschema.Draft202012Validator` 200 original vs factored fixtures/negative parity **not run in approved environment**. Author-side source blob parity is not equivalent to standard Validator.
- S05-B03: actual JSON/Manifest/Reader/Parquet payload strict validation/readback **not run**.
- S05-B04: DoWhy/EconML/Tigramite installed effective backend fit/API/CI and environment/lock probing **not run**.
- S05-B05: 41 independent DGP/negative/reference science, HC1 exact inference/weak-IV size and all-real degeneracies, independent AR reviewer, preregistered T2/T3 **not complete**. Postcode candidate T3 does not exist yet.
- No S10 Contract Freeze, S11 Coding Authorization or G01–G10 canonical Gate999 PASS.

## 4. Next bounded actions

1. Repin source Git tree inventory after G10/P04 link repair and G08 normative candidate wording repair; point independent reviewer `165` at the new SHA.
2. Where possible, run review-only deterministic documentation/Schema checks; preserve exact SHA and distinguish author static results from independent official validation.
3. Obtain separately approved Python3.12 runtime / independent scientific reference and reviewer capability before claiming S05/S09 PASS or preparing S10 approval. Continue documentation work otherwise.
4. Escalate to Owner **only** if an additional target/algorithm/operational decision cannot be unambiguously derived from existing approvals.
