# 221 — Owner limited modification authorization for completed P02 Reader: DEC-G01-P03-P02-COMPAT-01

**Date:** 2026-11-23 JST  
**Decision:** `DEC-G01-P03-P02-COMPAT-01 = OWNER_APPROVED`  
**Owner instruction:** 「DEC-G01-P03-P02-COMPAT-01：P02 ReaderのGraphProvenance検証強化を限定承認する。こちらを承認する」  
**Decision category:** BOUNDED_COMPLETED_PACKAGE_COMPATIBILITY_EXCEPTION  
**Applies to:** G01/P03 typed GraphProvenance design A; integration with already completed G01/P02 Reader, not a wholesale P02 reimplementation  
**Normative contract proposal as of:** `c983c1541f8c7ad73b685b95be74b4ce7704ef3f` (formal AMD-E11-G01-P03-001 09 still NOT approved)  
**Historical approved S10:** `c37cd93d981a6d3777e20bd46b26bc3ae9b2c1f8`  
**Protected P01 PACKAGE_READY checkpoint:** `9bff61f0eae25236f95f31f2cd3e7c81291f0167`  
**Protected P02 PACKAGE_READY checkpoint:** `3a76a0aa1698037354b284ba7b5a875300473ce6`  
**Repo/branch:** `kousuke-ota-datascience/causal-atelier` / `feature/ariadne_mvp_e11`

## 1. Concrete authorization

The Owner authorizes, **once the AMD-E11-G01-P03-001 formal 09, new immutable S10 reFreeze and separate limited S11 are approved**, a narrow semantic readback enhancement of the completed P02 package to support the P03 typed GraphProvenance contract.

**Permitted source target:** `src/ariadne/interfaces/cli/local_causal/manifest_reader.py`, specifically `_validate_graph` and the minimally necessary Graph-to-Study/Manifest provenance checks, ideally by reusing a P03-owned pure typed GraphSemanticsValidator without duplicating independent semantic implementations.

**Permitted verification target:** the existing P02 enhancement integration tests under `tests/enhancement/enh_e11/g01/integration/test_local_publication.py` and any minimal adjacent G01/P03-focused test for the same semantic path, with regression coverage to preserve original P01/P02 behavior not conflicting with the newly approved Graph contract.

This permission includes rejecting graphs with `provenance={}` or wrong/missing/extra typed fields, mismatched Method/Backend/CI, missing/unsafe/stale source ContentRefs, incorrect Study/Manifest source joins, non-null invented Product GraphVersion IDs, invalid parent/cyclic references, and forged semantic/content-byte hashes, under the now stricter proposed P03/GRAPH04 rules. Readback must actually verify the trusted referenced source bytes when required by the final normative contract, not merely rehash the graph's supplied claims.

## 2. Non-authorized actions and compatibility

This **does not approve** changes to completed P02 Publisher, publication/atomic no-clobber, privacy policy/decision, Linux root/FD handling, run status or Marker, manifest/public wire/Port signatures, P01 codec or P01/P02 historical Package checkpoints. It does not authorize changing public Schema beyond the separately selected P03 A strategy, Product v2 GraphVersion semantics, scientific conclusions or G01_999 acceptance criteria.

A previously accepted Graph bundle using `provenance={}` might fail new readback. This is a deliberate *observable compatibility risk* of the newly selected P03 A contract; do not pretend it is bit-for-bit backward compatible. Keep pre-change checkpoint and evidence immutable; add new implementation/report/checkpoint trace for the targeted retrofit rather than overwriting `3a76a0aa1698037354b284ba7b5a875300473ce6`.

If actual implementation discovers that `manifest_reader.py` plus bounded test updates cannot enforce the required trusted file-byte rechecks without changing the protected P02 publisher/Port ABI, STOP and request a fresh Owner decision with concrete files and reason. No unbounded implementation permission.

## 3. Control-plane and trial boundary

This decision **only removes the completed-P02 modification authorization blocker**. It is not formal 09 approval for AMD-E11-G01-P03-001; not an S10 freeze; not a new S11 Coding Authorization; not a direction to edit code now. Current P03 Trial01 remains `BLOCKED_CONTRACT_AMBIGUITY / CODING_AUTHORIZATION_PENDING` until the exact formal authority sequence is completed.

Implementation only after separate S11 can execute on real Linux and record P02 scoped regressions plus P03 graph/provenance positive/negative cases, readback and Product v2 tests. Independent Science, S09, B02–B05, T2/T3 and G01_999 remain unchanged and unperformed here.

## 4. Next Owner decision

The proposed `AMD-E11-G01-P03-001` formal 09 amendment at `10_enhance_instruction/G01/09_ENH-E11_G01_AMD-E11-G01-P03-001_Gate_Contract_Amendment.md` must be expressly approved. After that, choose a full Git SHA for revised provisional S10 and separately authorize the new limited S11. No silent promotion.
