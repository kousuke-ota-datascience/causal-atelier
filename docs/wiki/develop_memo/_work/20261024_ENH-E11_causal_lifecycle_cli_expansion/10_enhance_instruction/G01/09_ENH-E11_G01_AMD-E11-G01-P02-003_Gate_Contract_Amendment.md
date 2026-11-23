# AMD-E11-G01-P02-003 — G01 DISCOVER negative diagnostic typed contract

**Date:** 2026-11-23 JST  
**Type:** CONTRACT_DEFECT  
**Status:** AUTHOR_CONTRACT_CORRECTED / FORMAL_09_OWNER_PENDING / S10_S11_PENDING  
**Gate/Package/Trial:** G01/P02/Trial01  
**Agent stop START_SHA:** 86d73c501f83eed2ce79b1fa949d6aacffc3f4a1; BLOCKED_CONTRACT_AMBIGUITY; P02 not implemented  
**Old frozen normative SHA:** 0e36d5d8ce5a4fb9880c4ecff07f4e2256cde492  
**New normative 11-file correction commit:** 1d54f4059f3f0cf101d8bee846087acba396ce0a  
**P01 checkpoint preserved:** 9bff61f0eae25236f95f31f2cd3e7c81291f0167

## 1. Defect

G01 P02/07 require a typed Graph-negative diagnostics.json and exact Status reason join, while existing contract specified only inventory/hash and SCI_NO_ADMISSIBLE_PAG reason in P01 Manifest. Empty JSON {} could match its physical hash and size but has no defined diagnostic meaning. Existing method_diagnostics draft1 is for P1-M12–20 REFUTE/SENSITIVITY/DIAGNOSE and does not apply to P1-M06 DISCOVER.

## 2. Minimal normatively required contract

An internal-only G01 DISCOVER/P1-M06 negative diagnostics.json object has EXACT required keys: run_id, operation, method_id, reason_codes. run_id matches Status and Manifest; operation is DISCOVER; method_id is P1-M06; reason_codes is exactly a one-element list with SCI_NO_ADMISSIBLE_PAG, equal to Status.reason_codes and the immutable P01 Manifest negative-reason evidence tuple. An internal JSON Schema is in 23_api_interface_design/schema_drafts/internal_scientific/e11_g01_discover_negative_diagnostics_draft1.schema.json. Strict UTF-8 JSON decode rejects duplicate keys, missing/extra keys and invalid types. No new public version or schema_dispatch key.

P02 final Publisher independently reopens staged actual bytes, checks SHA/size plus this typed profile, exact Status/Manifest run/reason, completed technical status, null Graph refs, exact study/status/diagnostics inventory and trusted privacy authority BEFORE Manifest/Marker seal and rename. Independent Reader repeats cross-file semantic verification on committed bytes. Graph-positive forbids diagnostics; technical/backend failures are not scientific-negative.

The typed payload is **not proof** of a real scientifically justified P04 negative. P05 can stage it only following a genuine P04 outcome; otherwise preserve an appropriate typed technical failure. Synthetic P01 fixtures do not establish scientific fact.

## 3. Exact change scope

Requirements 10_17/10_91; logical data 21_40; basic design 22_09/22_15; interface 23_42 plus new internal schema; detailed design 30_62; implementation instructions G01/P02 and P05 06; verification instruction G01 07. Public E11 versioned Study/Status/Graph/Manifest/Marker, Product v2, P01 code/06/checkpoint, P03/P04 contracts, lock, independent science/G01_999 acceptance remain unchanged. No code or FS tests executed.

## 4. Formal reauthorization required

This is an AUTHOR-PREPARED formal 09 candidate. Prior Owner 205 formal 09, 207 S10 and 209 S11 apply to previous WHAT 0e36d5d8ce5a4fb9880c4ecff07f4e2256cde492, not this correction. Owner must separately approve AMD-E11-G01-P02-003 formal 09, select final immutable revised S10 full SHA, then separately approve a new limited S11 before G01/P02/Trial01 implementation. P01 checkpoint 9bff61f0eae25236f95f31f2cd3e7c81291f0167 and Trial01 remain preserved; no formal Gate FAIL/08.
