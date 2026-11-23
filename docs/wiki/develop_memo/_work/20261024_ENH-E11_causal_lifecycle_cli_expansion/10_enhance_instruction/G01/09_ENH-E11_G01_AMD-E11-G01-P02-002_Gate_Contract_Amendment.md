# AMD-E11-G01-P02-002 — Local PrivacyDecision value equivalence and publisher authority

**Gate / Package / Trial:** G01 / P02 / Trial01  
**Type:** CONTRACT_DEFECT (post-S10 freeze)  
**Status:** AUTHOR_REVISED / FORMAL_09_OWNER_APPROVAL_PENDING / NEW_S10_S11_PENDING  
**Date:** 2026-11-23 JST  
**Previous approved amendment:** AMD-E11-G01-P02-001 / Owner 198, freeze 199, S11 201  
**Previous approved G01-S10 immutable normative source:** `6df4b94de72a6ec8619f315e55ba7821e1eb157c`  
**Observed P02 Agent START_SHA:** `06726b522faf939c8ea34193d1861bd786092776`  
**P01 existing PACKAGE_READY checkpoint:** `9bff61f0eae25236f95f31f2cd3e7c81291f0167`  
**First changed normative source commit:** `940eb2dd7b37e47327e7ee8bf9e60fdaaad85a21`  
**uv.lock Git blob:** `2b83110e86b26b7969fbddf8f98a727370ae19f7`

## 1. Observed blocker and root cause

The P02 Coding Agent stopped before code with `BLOCKED_CONTRACT_AMBIGUITY`. The previous approved P02 §6.3 and 07 required reject of 'forged' PrivacyDecision, while the actual mechanism (the same immutable value forwarded to the same sink-owned Publisher, and **trusted independent stateless policy re-evaluation** of current staged Study/root/UID/artifacts) does not distinguish an independently instantiated **fully value-identical** Decision from a policy-created object. There was no issuer identity/nonce/signature/token. Therefore the previous 07's word `forged` ambiguously included both detectable conflicting values and indistinguishable equal values.

No P02 code, official package checkpoint or real P02 FS tests existed at stop. User reported 76 P01 focused/Product CLI regression tests PASS, EUID1000/ext4 directory checks; **do not confuse those with P02 developer/independent FS PASS**. User report is external Agent evidence, not an independently rerun test.

## 2. Canonical resolution (no new authorization architecture)

`PrivacyDecision` is a **private immutable value**, not an unforgeable bearer credential or issuer proof. Its equivalence is **structural equality over all declared fields** (`allowed,run_id,request_hash,root_identity,principal_uid,classification,row_export_requested,output_shape`). Separately instantiated but value-identical well-formed Decision MUST be accepted **if and only if** the Publisher independently verifies true staged Study bytes/JCS run/hash, current trusted root FD and EUID, exact inventory and its **own trusted injected stateless Policy** recomputation returns `allowed=true` and all decision fields match. The Publisher does not accept caller's Boolean or caller-controlled Policy as authority.

Reject absent/denied/malformed/mismatched/stale/foreign run/hash/root/UID/classification/output shape, Study or inventory mutation, disallowed row and Policy recomputation denial before Manifest/Marker/rename. `forged` now refers to detectable mismatch/policy-bypass attempts, **not an exactly identical reconstruction**. No object `is` check, provenance verification, new MAC/signature/issuer registry/policy anchor; same root FD/UID/FS safety and readback still apply.

## 3. Five-layer impact and 06/07 matrix

| Layer | Changed files | Nature |
| --- | --- | --- |
| Requirement | `10_22`, `10_91` | NFR-031 and acceptance test *meaning* clarified; no requirement ID/status/strength relaxation |
| LDD | `21_23`, `21_40` | ephemeral value equality and invariant, not a new DB entity |
| BD | `22_09`, `22_12` | Publisher final authority and explicitly absent issuer attestation |
| IF | `23_41`, `23_42` | field-value equality, trusted Policy, no public Port/wire changes |
| DD | `30_62` | concrete Publisher seal/validate sequence, recompute decision, field-by-field equality |
| Coding | G01 `06_G01_P02`, `06_G01_P05` | exact handling of identical reconstruction, meaningful forged negatives |
| Test | G01 `07_Ariadne_ENH-E11_G01_test_instruction.md` | positive original **and identical reconstruction**; negative changed fields, policy disagreement and untrusted policy injection |

This is a **bounded CONTRACT_DEFECT correction** of the previous AMD-001 meaning, not a redesign. It makes no changes to G01 P01/P03/P04, public local Study/Status/Graph/Manifest/Marker/ArtifactDescriptor version or schema, Product v2, individual-row/G05 output rights, scientific negative or Graph/PAG validity requirements. Existing independently computed Reviewer/FS/Science evidence remains unperformed.

## 4. Sequential control-plane disposition

The prior formal 09 `198`, frozen S10 `199` and separate S11 `201` **remain historic, valid for prior WHAT** but cannot authorize implementing this changed test/implementation meaning. Present document is a formal **09 candidate**, not a self-authorized approval. Owner must explicitly decide `DEC-G01-P02-EQUIVALENCE-09-S10-01` to approve AMD-E11-G01-P02-002 and freeze the final **full Git SHA** after all contract/audit documents are committed. Then obtain a separately approved limited **G01-S11** for this new exact SHA. Existing `Trial01` and P01 checkpoint remain preserved; no observed Gate999 FAIL/08 remediation means no automatic Trial02.

Do not assert this report provides a verified P02 implementation, successful Linux atomic publication, independent test or G01_999 PASS.
