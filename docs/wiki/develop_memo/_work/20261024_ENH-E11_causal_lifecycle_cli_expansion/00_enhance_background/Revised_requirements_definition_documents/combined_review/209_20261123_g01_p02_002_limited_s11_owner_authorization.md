# 209 — G01/P02 amended-002 limited S11 Owner Coding Authorization

**Decision:** `DEC-G01-P02-002-S11-REAUTH-01`  
**Date:** 2026-11-23 JST  
**Owner decision:** `APPROVED`  
**Owner instruction (verbatim):** 「DEC-G01-P02-002-S11-REAUTH-01を承認する。AMD-E11-G01-P02-002に基づく暫定G01-S10凍結SHA 0e36d5d8ce5a4fb9880c4ecff07f4e2256cde492 を対象に、G01/P01〜P05の限定Coding Authorizationを再発行せよ。次の実行はG01/P02/Trial01とする。P01チェックポイント9bff61f0eae25236f95f31f2cd3e7c81291f0167を維持し、既承認の科学的・独立検証・G01_999受入条件は変更しない。」  
**Formal 09 prerequisite:** `205` Owner-approved AMD-E11-G01-P02-002  
**Provisional S10 reFreeze prerequisite:** `207` Owner-approved `0e36d5d8ce5a4fb9880c4ecff07f4e2256cde492`  
**New S11 authorization:** this distinct record, not previous 201  
**Repository:** `kousuke-ota-datascience/causal-atelier`  
**Branch:** `feature/ariadne_mvp_e11`  
**Immutable frozen normative full Git SHA:** `0e36d5d8ce5a4fb9880c4ecff07f4e2256cde492`  
**P01 PACKAGE_READY checkpoint:** `9bff61f0eae25236f95f31f2cd3e7c81291f0167`  
**uv.lock Git blob:** `2b83110e86b26b7969fbddf8f98a727370ae19f7`  
**Next permitted Coding Agent execution:** `GATE_ID=G01 PACKAGE_ID=P02 TRIAL_NO=01`

## 1. Exact grant, scope and preservation

The Owner grants a **new separate limited G01-S11 Coding Authorization**, sequentially after formal AMD-002 09 approval and S10 reFreeze, for the frozen G01/P01–P05 coding/developer-verification scope. The next **bounded work package is G01/P02/Trial01**. P01 is already implemented and PACKAGE_READY at `9bff61f0eae25236f95f31f2cd3e7c81291f0167`, and must not be redone or rewritten solely to resume P02.

Approved P02 WHAT is the exact frozen version of `10_enhance_instruction/G01/06_G01_P02_atomic_publication_reader.md`, its P05 integration interface in `06_G01_P05_cli_use_case_privacy.md`, the G01 `07_Ariadne_ENH-E11_G01_test_instruction.md`, and all five stock layers in `00_enhance_background/Revised_requirements_definition_documents/{10_requirements_definition,21_logical_data_design,22_product_basic_design,23_api_interface_design,30_detailed_design}/` at `0e36d5d8ce5a4fb9880c4ecff07f4e2256cde492`. The versioned public CLI ports, scientific/PAG meaning, local G01 aggregate-only scope, Product v2, lock and G01_999 independent acceptance remain unchanged.

Prior G01-S11 201 covers the previous privacy contract freeze `6df4b94de72a6ec8619f315e55ba7821e1eb157c` only and does not authorize the present amendment. Formal 09 `205` and provisional S10 `207` are not interchangeable with this S11.

## 2. Binding P02 privacy semantics and security

`PrivacyDecision` is an immutable transient typed value, **not** an issuer-attested or unforgeable credential. A separately constructed but exactly all-fields-equal Decision is equivalent and may be accepted **only when** the sink-owned Publisher itself validates actual staged Study bytes and JCS request hash, current secure root FD/device/inode/owner/mode/local FS, live effective UID, complete actual staged aggregate artifact inventory, and the trusted injected stateless privacy policy independently returns allowed and agrees in every declared field. No object identity/issuer token/signature/MAC is required or authorized. Missing, denied, mismatched, stale, conflicting run/hash/root/UID/shape or restricted row data must be refused before Manifest/Marker seal and rename. A caller-supplied `allowed=true` is not authority; no arbitrary policy substitution is permitted. Commit and independent Reader maintain existing rechecks.

## 3. Real environment preflight and behavior

The actual Coding Agent MUST verify branch, remote, current HEAD and worktree clean state, `0e36d5d8ce5a4fb9880c4ecff07f4e2256cde492` ancestry, post-freeze diff limited to approved management records, actual `uv.lock` Git blob and measured SHA-256, P01 checkpoint ancestry and Package-ready evidence, Trial01 without formal Gate FAIL/08, and no existing P02 checkpoint or unrelated source modifications. If verification fails, report BLOCKED with actual evidence, not assumed authorization. Avoid overwriting the Agent's previous Blocking reports.

Implement P02 secure Linux dirfd/ContentRef actual bytes, trusted root, stage/publisher/reader atomic same-FS no-clobber, fsync, typed PrivacyDecision/policy reconciliation, inventory/Study integrity and race/Reader negatives. Execute and report focused tests and genuine Linux FS proof. Only create a P02 checkpoint and official Package report after factual developer-level verification. Do not claim independent G01/S09/B02–B05/T2/T3/G01_999 PASS from S11, documentation or developer tests.

## 4. Change-control boundary

This S11 authorizes **implementation of the frozen WHAT**, not a new contract change. Any additional material inconsistency in RD/BD/LDD/IF/DD/06/07 requires formal 09 amendment, newly chosen full S10 SHA and distinct S11 again; no unilateral correction of frozen normative docs or public schema. No G02–G10, release or Product ABI change. Future P03/P04/P05 remain bounded by P00 dependencies and their own verification.
