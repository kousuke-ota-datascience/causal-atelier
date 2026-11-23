# 216 — G01/P02-003 separate limited S11 Owner Coding Authorization

**Decision ID:** `DEC-G01-P02-003-S11-REAUTH-01`  
**Date:** 2026-11-23 JST  
**Decision status:** `OWNER_APPROVED / LIMITED_G01_S11_AUTHORIZED`  
**Owner instruction (verbatim):** 「DEC-G01-P02-003-S11-REAUTH-01を承認する。AMD-E11-G01-P02-003に基づく暫定G01-S10凍結SHA c37cd93d981a6d3777e20bd46b26bc3ae9b2c1f8 を対象に、G01/P01〜P05の限定Coding Authorizationを再発行せよ。次の実行対象はG01/P02/Trial01とする。P01チェックポイント9bff61f0eae25236f95f31f2cd3e7c81291f0167を維持し、既承認の科学的・独立検証・G01_999受入条件は変更しない。」  
**Repository:** `kousuke-ota-datascience/causal-atelier`; **branch:** `feature/ariadne_mvp_e11`  
**Frozen normative full Git SHA:** `c37cd93d981a6d3777e20bd46b26bc3ae9b2c1f8`  
**Formal 09 approved:** `combined_review/212_20261123_g01_p02_003_formal_09_owner_approved.md`  
**Revised provisional S10 reFrozen:** `combined_review/214_20261123_g01_p02_003_s10_owner_refreeze.md`  
**S11 decision docket:** `combined_review/215_20261123_g01_p02_003_limited_s11_decision_docket.md`  
**Existing P01 PACKAGE_READY checkpoint:** `9bff61f0eae25236f95f31f2cd3e7c81291f0167`  
**Frozen uv.lock Git blob:** `2b83110e86b26b7969fbddf8f98a727370ae19f7`  
**Next executable work:** `GATE_ID=G01 PACKAGE_ID=P02 TRIAL_NO=01`

## Scope and source authority

This is a separately granted **limited G01/P01–P05 Coding Authorization** for **implementation and developer verification**, beginning at P02/Trial01. P01 remains PACKAGE_READY at `9bff61f0eae25236f95f31f2cd3e7c81291f0167` and must not be reimplemented or modified absent a demonstrated additional defect and explicit change control. Future P03/P04/P05 require satisfying P00 dependencies and their own tests. No G02–G10, Product v2 ABI change, release or extra scientific method is approved.

Binding WHAT is the full immutable `c37cd93d981a6d3777e20bd46b26bc3ae9b2c1f8` version of the five revised stock layers `00_enhance_background/Revised_requirements_definition_documents/{10_requirements_definition,21_logical_data_design,22_product_basic_design,23_api_interface_design,30_detailed_design}/`, G01 `06_G01_P02_atomic_publication_reader.md`, related P05 `06`, Gate-wide `06`, G01 `07_Ariadne_ENH-E11_G01_test_instruction.md`, and `09_ENH-E11_G01_AMD-E11-G01-P02-003_Gate_Contract_Amendment.md`.

P02 Publisher must strictly verify the **actual** staged G01/P1-M06 Graph-negative `diagnostics.json` internal four-field payload (`run_id,operation,method_id,reason_codes`), singleton reason `SCI_NO_ADMISSIBLE_PAG`, exact run/reason joins to Status/Manifest, hashes, sizes, Graph-null and exact artifact inventory before Marker/rename. The independent Reader revalidates committed bytes. Schema-valid negative is **not** scientific evidence that a real PAG was impossible. P02 retains the separately approved PrivacyDecision **value-equivalence** contract plus independent publisher policy re-authorization. No public schema version, issuer signature, P01 reimplementation, G01 row export or scientific acceptance downgrade.

## Mandatory real Coding Agent preflight

Before editing code the Agent verifies current HEAD/branch/remote, clean worktree, `c37cd93d981a6d3777e20bd46b26bc3ae9b2c1f8` ancestry, only approved post-freeze administrative records, actual tracked `uv.lock` blob and worktree SHA-256, P01 checkpoint ancestor and PACKAGE_READY report, no P02 checkpoint, Trial01 no formal Gate FAIL/08, distinct Owner 09(212)→S10(214)→S11(this 216) for exactly `c37cd93d981a6d3777e20bd46b26bc3ae9b2c1f8`. A failed preflight is typed BLOCKED and no code changes may proceed on assumption. Do not use old S11 209 or post-freeze HEAD as the normative WHAT.

P02 tests must cover secure dirfd/TrustedRoot, content bytes, state transition, all relevant PrivacyDecision negative/positive cases including value-identical reconstruction, strict diagnostics `{}`/duplicate/wrong reason/mismatched run, Graph-positive inventory, no-clobber renameat2/fsync, concurrent run, crash/Reader validation on real Linux FS; protect P01 focused and Product v2 regression suites. Produce actual official Package status/checkpoint only when implementation and observed developer-level verification satisfy the frozen WHAT.

## Unwaived Gate barriers

No Owner approval here constitutes P02 tests PASS, independent science/S09/B02–B05/T2/T3, MAG/PAG reference, independent G01 07, G01_999 acceptance, or Product release. All remain separate. New frozen-WHAT contract ambiguity requires formal 09→revised S10→separate S11. Earlier approvals 205/207/209 remain historical for AMD-002, not the current AMD-003.
