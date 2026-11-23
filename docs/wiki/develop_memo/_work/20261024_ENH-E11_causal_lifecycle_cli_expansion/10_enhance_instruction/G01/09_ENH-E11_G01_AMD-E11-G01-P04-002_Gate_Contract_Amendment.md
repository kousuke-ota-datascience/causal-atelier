# AMD-E11-G01-P04-002 — declared categorical support domain for FCI preflight

**Date:** 2026-11-23 JST  
**Classification:** `CONTRACT_DEFECT / INTERNAL_METHOD_DESIGN_INPUT_COMPATIBILITY`  
**Gate/Package/Trial:** `G01/P04/Trial01`  
**Owner design choice:** `DEC-G01-P04-CATEGORY-DOMAIN-01=A_ADOPTED`  
**Status:** `AUTHOR_PREPARED_FORMAL_09_CANDIDATE / FORMAL_09_OWNER_PENDING / S10_REFREEZE_PENDING / S11_REAUTH_PENDING`  
**Agent last stopped START_SHA:** `56889493d101b6c3c3a13a37dcd7cfd713dbf73a` (`BLOCKED_CONTRACT_AMBIGUITY`; no P04 checkpoint)  
**Previous approved S10:** `a7003b359444af64cad0edbade0341243653a8bf`  
**Previous S11:** `DEC-G01-P04-001-S11-REAUTH-01` (not authorization for revised WHAT)  
**Protected P01:** `9bff61f0eae25236f95f31f2cd3e7c81291f0167`  
**Protected P03:** `858c9f73366036a2d1445e558135cd521f611462`

## 1. Root cause and authority

The owner-approved prior amendment `AMD-E11-G01-P04-001` and P04 §6.4 require categorical `chisq/gsq` to screen **all declared** category combinations for all X/Y/S triples *before* FCI fit, rejecting missing strata or any expected count below 5. However, the frozen strict internal P1-M06 Design schema had only `name`/`measurement_scale` in its variable entries, and no other approved Local Dataset or Study input supplied a category universe. Inferring a universe from observed `np.unique` would silently remove absent categories and breach the approved scientific rule.

This is a Method-specific **input authority gap** rooted in the strict IF Design evidence profile and propagated to DD and 06/07. It is not permission to copy the present Backend's permissive recoding into the scientific contract.

Owner selected A in `DEC-G01-P04-CATEGORY-DOMAIN-01` (record 233, docket 232), explicitly approving the necessary internal Design input-compatibility tightening and preservation of all publicly versioned E11 wires, P01/P03 checkpoints and G01_999.

## 2. Normative delta and exact owner boundaries

**Internal Design input:** `23_api_interface_design/schema_drafts/e11_p1_m06_fci_design_profile_v1.schema.json` in `Design.variables[]` now conditionally requires `category_codes` only for CATEGORICAL; forbids it for CONTINUOUS. `category_codes` is a distinct, ascending complete code universe with >=2 integer values; negative and noncontiguous codes are allowed. Draft 2020-12 Schema enforces shape, integer typing, conditional presence and uniqueness, while the input semantic validator must also enforce strict ascending order, exact encoded JSON integer-token semantics (standard JSON Schema `integer` alone is insufficient to distinguish `1` from `1.0`/`1e0`), backend representability, absence of bool, and no coercion. The earlier `e11_g01_design_evidence_profile.schema.json` is a historical draft, not an alternate P1-M06 dispatch option: fail closed if the active Method cannot resolve its dedicated strict validator.

**Dataset/Design integrity:** Join Design variable order/names to verified Dataset column order, require categorical observations be strict integer members of the *entire declared domain*, and preserve unobserved declared codes. For all X,Y,S in the previously approved exhaustive pre-FCI universe, inspect every declared S=s combination and all X/Y levels, rejecting unsupported strata/cells, degenerate marginals/df and null-independence expected count <5. Never shrink declared support to actually observed levels or rely on `causal-learn`'s `np.unique`. Incomplete checks are typed fail-closed, zero FCI calls, zero Graph/Marker, never a `SCI_NO_ADMISSIBLE_PAG` result.

**Content identity and compatibility:** Existing `Study.inputs.design` full-byte SHA256 ContentRef is the reference authority. When Design bytes change due to this stricter internal method payload, ContentRef SHA and Study JCS-derived request_hash must be recalculated; P03 Graph provenance source ref remains exact verified Design Ref. Old category-free categorical Design input is *no longer admissible*, while unchanged valid continuous Design remains structurally admissible. No public `e11-local-*/1` field, wire version, marker, Product v2 contract or external schema migration is introduced.

**Scientific integrity:** Retain exhaustive pair/subset coverage from AMD-001, existing E>=5 count floor, non-null BK pre-FCI denial, conditional-independence assumptions as declared/not-proven, latent PAG uncertainty, endpoint/provenance fidelity, actual Backend validation and independent MAG/PAG + T2/T3 + G01_999 tests. Do not claim that declaration or arithmetic success guarantees scientific validity.

## 3. Exact changed files in this AMD-002 package

- **IF authority:** `00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design/schema_drafts/e11_p1_m06_fci_design_profile_v1.schema.json`
- **IF contract:** `00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design/23_41_cli_scientific_ports.md`
- **DD Method:** `00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_63_causal_method_adapters.md`
- **Coding P04:** `10_enhance_instruction/G01/06_G01_P04_fci_backend_oracle.md`
- **Independent G01 tests:** `10_enhance_instruction/G01/07_Ariadne_ENH-E11_G01_test_instruction.md`
- **Decision history only:** `combined_review/232_20261123_g01_p04_categorical_domain_owner_decision_docket.md`, `combined_review/233_20261123_g01_p04_category_domain_A_owner_adopted.md`
- This formal 09 proposal itself.

Reviewed unchanged: requirement/science scope `10_13`, `10_17`, `10_32`, `10_91`; logical data `21_11`, `21_40`, `21_41`; basic design `22_06`, `22_15`; public schema `e11_local_study_v1`; IF `23_42`; DD `30_61/30_62`; older general G01 Design draft (not selected for P1-M06); completed P01/P03 instructions and implementation; P02/P05 implementation; Product v2; `uv.lock`. Changes to another Gate/Method are not authorized.

## 4. Independent acceptance matrix

- Positive: valid categorical Domain `[0,1]` with adequately supported all-candidate combinations; valid noncontiguous `[0,2]` and negative codes if Dataset truly supports them; continuous Design without `category_codes`.
- Negative: category-free CATEGORICAL Design; CONTINUOUS with category field; `[0,0]`, unsorted, `1.0`/`1e0`, bool, decimal/string/null, unrepresentable code; Dataset codes outside declared universe, column order/name mismatch and missing/nonfinite observations.
- Missing declared code: Domain `[0,1,2]` with observed values `[0,1]` must not become a valid two-level domain; missing X/Y marginals and absent S=s full Cartesian combinations reject under existing AMD-001 eligibility policy.
- Hash integrity: verified actual Design bytes, ContentRef SHA and modified Study JCS request hash plus Graph provenance source refs; no acceptance based on stale source-ref hashes.
- No Backend FCI call, Graph, stage, Marker, science-negative or leak for all preflight failures. Preserve actual Python3.12 `fisherz/chisq/gsq` fit, independent MAG/PAG oracle, BK negatives, protected Product regressions and Gate999 evidence separately.

## 5. Impact / release control / unresolved matters

- **Completed P01/P03:** No changes to their code, tests, 06/07 or checkpoints. Generic ContentRef and Graph source-ref values remain contractually identical; new Design source bytes require newly verified input hashes and contract-focused regressions. Existing P02 Reader compatibility is governed by its own separate prior approval; this amendment neither expands nor reopens it.
- **P05:** No code or 06 changes. Trace unchanged error routing and verified Design source ref in later integration.
- **Other Gates:** No direct changes. The P1-M06 dedicated Design profile must not silently become a common 41-Method domain rule.
- **Residual scientific risks:** A fixed exhaustive-scan resource cap and numerical correlation-conditioning threshold remain unspecified; incomplete/uncertain checks still fail closed under AMD-001. No live fit or independent science PASS has been created by authoring this amendment.
- **Authorization:** This is an Author-prepared formal 09 **candidate only**. Owner must explicitly approve `AMD-E11-G01-P04-002` as a new formal 09, separately approve a revised complete immutable G01-S10 SHA after normative edits/approval record, and issue a distinct limited S11 before P04/Trial01 resumes. Prior S10/S11 do not cover this changed contract.
