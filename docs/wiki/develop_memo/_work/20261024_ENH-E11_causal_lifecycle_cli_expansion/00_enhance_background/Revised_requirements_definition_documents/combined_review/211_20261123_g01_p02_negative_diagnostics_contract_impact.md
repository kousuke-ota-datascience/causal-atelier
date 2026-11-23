# 211 — G01/P02 Graph-negative diagnostics defect and impact audit

**Date:** 2026-11-23 JST  
**Status:** AUTHOR_CROSS_LAYER_ALIGNMENT_COMPLETE / OWNER_09_S10_S11_PENDING  
**Stop:** BLOCKED_CONTRACT_AMBIGUITY / 86d73c501f83eed2ce79b1fa949d6aacffc3f4a1 / no P02 checkpoint.  
**Old S10:** 0e36d5d8ce5a4fb9880c4ecff07f4e2256cde492; **P01 checkpoint:** 9bff61f0eae25236f95f31f2cd3e7c81291f0167.

## Evidence

P01 LocalRunManifest accepts strict Graph-negative inventory and the exact singleton SCI_NO_ADMISSIBLE_PAG reason tuple, but does not decode diagnostic JSON contents. Public e11-local-status/1 specifies reason_codes in the Status envelope, not diagnostics.json. The existing internal method-diagnostics draft covers other methods/operations, not G01/P1-M06/DISCOVER. Stored file hash/size cannot establish semantic correctness: an empty JSON object can match its own hash.

## Decision

Define a strict private G01 negative diagnostic: exactly run_id, operation=DISCOVER, method_id=P1-M06, reason_codes=[SCI_NO_ADMISSIBLE_PAG]. Require Status/Manifest run/reason equality, completed Status, null Graph, exact negative inventory and actual bytes. P02 Publisher verifies before marker/rename and Reader independently validates after commit. Genuine scientific-negativity remains the P04/independent science obligation, never proven by a synthetic DTO.

## Five-layer trace and regression

RD 10_17/10_91; LDD 21_40; BD 22_09/22_15; IF 23_42 and internal G01 schema; DD 30_62; G01/P02+P05 06; G01 07. These normative changes were committed at 1d54f4059f3f0cf101d8bee846087acba396ce0a. P01 source/tests/06, P03/P04 semantics, public schema and Product v2 are unchanged. P02 real Linux FS, Reader, independent science and G01_999 have not been executed.

## Control plane

New AMD-E11-G01-P02-003 09 Owner approval required, then new S10 freeze full SHA, then separate new S11. No authority to reuse 209 after changed WHAT. Trial01 and existing P01 PACKAGE_READY remain.
