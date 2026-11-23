# 234 — ENH-E11 G01/P04 AMD-E11-G01-P04-002 formal 09 Owner approval

**Decision ID:** `DEC-G01-P04-002-09-APPROVE-01`  
**Date:** 2026-11-23 JST  
**State:** `FORMAL_09_OWNER_APPROVED / NEW_S10_NOT_YET_APPROVED / NEW_S11_NOT_AUTHORIZED`  
**Repository:** `kousuke-ota-datascience/causal-atelier`  
**Branch:** `feature/ariadne_mvp_e11`

## 1. Explicit Owner decision

Owner explicitly authorized:

> AMD-E11-G01-P04-002の正式09改訂案を承認する。DEC-G01-P04-CATEGORY-DOMAIN-01=Aに基づくP1-M06内部Design Profileのcategory_codes追加と、IF・DD・G01/P04 Coding Instruction・G01 Test Instructionの修正を正式契約として承認せよ。P01/P03チェックポイント、既承認の科学的意味、公開E11 Schema Version、独立科学検証・G01_999受入条件は維持する。

**Approved exact contract content commit before this approval record:** `6e409cc87007be1df2e7aab58c59688c8693344d`  
**Formal amendment:** `10_enhance_instruction/G01/09_ENH-E11_G01_AMD-E11-G01-P04-002_Gate_Contract_Amendment.md`  
**Prior adopted design decision:** `DEC-G01-P04-CATEGORY-DOMAIN-01=A`, recorded in `combined_review/233_20261123_g01_p04_category_domain_A_owner_adopted.md` and decision docket `232`.

## 2. Approved normative change — bounded to G01/P1-M06

The strict **internal** P1-M06 Design evidence profile now conditionally requires full `variables[].category_codes` for `measurement_scale=CATEGORICAL`, while forbidding it for CONTINUOUS. This is the complete declared universe, not an observed-data unique set. Require >=2 distinct ascending, exactly represented integer codes and strict Dataset membership; absent declared levels and zero-row conditioning strata remain in the prior approved exhaustive all-X/Y/S pre-FCI screening. Preserve expected-count floor 5 for both chisq/gsq, no automatic recoding, incomplete-check fail closed, valid Graph/PAG uncertainty and scientific-negative integrity. Do not infer all assumptions scientifically verified.

Owner explicitly approved the bounded **internal Design input compatibility tightening**: category-free categorical Design documents previously structurally admitted are now invalid for P1-M06. This change does **not** add/change a public E11 Study/Graph/Manifest/ContentRef field or `e11-local-*/1` wire version, does not change Product v2 and does not permit silently reusing stale Design hash or Study request_hash.

## 3. Verified exact diff and checkpoint integrity

At approval, the branch HEAD was precisely `6e409cc87007be1df2e7aab58c59688c8693344d`. Compared with blocked Agent START_SHA `56889493d101b6c3c3a13a37dcd7cfd713dbf73a`, the diff was precisely eight files:

1. `00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design/23_41_cli_scientific_ports.md` (updated)
2. `00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design/schema_drafts/e11_p1_m06_fci_design_profile_v1.schema.json` (updated)
3. `00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_63_causal_method_adapters.md` (updated)
4. `10_enhance_instruction/G01/06_G01_P04_fci_backend_oracle.md` (updated)
5. `10_enhance_instruction/G01/07_Ariadne_ENH-E11_G01_test_instruction.md` (updated)
6. `10_enhance_instruction/G01/09_ENH-E11_G01_AMD-E11-G01-P04-002_Gate_Contract_Amendment.md` (new)
7. `00_enhance_background/Revised_requirements_definition_documents/combined_review/232_20261123_g01_p04_categorical_domain_owner_decision_docket.md` (new)
8. `00_enhance_background/Revised_requirements_definition_documents/combined_review/233_20261123_g01_p04_category_domain_A_owner_adopted.md` (new).

Compare HEAD against P01 `9bff61f0eae25236f95f31f2cd3e7c81291f0167`, P03 `858c9f73366036a2d1445e558135cd521f611462` and prior S10 `a7003b359444af64cad0edbade0341243653a8bf` showed all as ancestors with behind 0. The amendment does not authorize changes to completed P01/P03 code, 06/07/tests/checkpoint, nor P02/P05 behavior, `uv.lock`, public Schema Version or other Gates.

## 4. Unchanged science, independent verification and control-plane obligations

Preserve approved `AMD-E11-G01-P04-001` exhaustive CI screening, all prior FCI scientific qualification, latent PAG endpoint semantics, actual Python3.12/backend verification, non-null BK semantics fail-closed, independent MAG/PAG Oracle, scientific positive/negative gates, T2/T3 science, Product v2 regressions, and independent G01_999 acceptance. Formal 09 approval alone is **not** science PASS.

**Separate next decisions:** Owner must approve revised G01-S10 freeze on a **new exact complete immutable commit SHA including this approval record**, and then issue a **separate** scoped G01/P04/Trial01 S11 reauthorization. Previous S10 `a7003b359444af64cad0edbade0341243653a8bf` and S11 `DEC-G01-P04-001-S11-REAUTH-01` remain historical, not authority for changed `category_codes` contract. This approval record's own commit will change branch HEAD but will not retrospectively alter the approved content SHA.

No P04 focused tests, FCI fit, implementation checkpoint, push from Coding Agent, or independent G01_999 science PASS is claimed by this approval.
