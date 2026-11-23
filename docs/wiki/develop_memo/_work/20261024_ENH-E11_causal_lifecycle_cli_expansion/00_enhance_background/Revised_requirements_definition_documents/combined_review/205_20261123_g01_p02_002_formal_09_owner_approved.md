# 205 — AMD-E11-G01-P02-002 formal 09 Owner approval

**Date:** 2026-11-23 JST  
**Decision:** `AMD-E11-G01-P02-002 / FORMAL_09 = OWNER_APPROVED`  
**Verbatim Owner authorization:** 「AMD-E11-G01-P02-002を承認する」  
**Gate / Package / Trial:** G01 / P02 / Trial01  
**Category:** CONTRACT_DEFECT (privacy decision value equivalence)  
**Reviewed immutable amendment source full Git SHA:** `0e36d5d8ce5a4fb9880c4ecff07f4e2256cde492`  
**Previous approved provisional G01-S10 WHAT SHA:** `6df4b94de72a6ec8619f315e55ba7821e1eb157c`  
**Preserved P01 PACKAGE_READY checkpoint:** `9bff61f0eae25236f95f31f2cd3e7c81291f0167`  
**Repository/branch:** `kousuke-ota-datascience/causal-atelier` / `feature/ariadne_mvp_e11`  
**Frozen uv.lock blob:** `2b83110e86b26b7969fbddf8f98a727370ae19f7`

## 1. Owner-approved 09 contract meaning

The Owner explicitly approved `AMD-E11-G01-P02-002` after the Agent reported a second `BLOCKED_CONTRACT_AMBIGUITY`. Its normative source is `10_enhance_instruction/G01/09_ENH-E11_G01_AMD-E11-G01-P02-002_Gate_Contract_Amendment.md` and the five-layer reconciliation recorded in `combined_review/204_20261123_g01_p02_privacy_decision_value_equivalence_impact.md`, both as of `0e36d5d8ce5a4fb9880c4ecff07f4e2256cde492`.

`PrivacyDecision` remains a transient immutable value, **not a cryptographically authenticated authority/provenance credential**. Two independently constructed typed decisions with identical eight field values are equivalent. The Publisher accepts such an identical-value decision **only when** its *own injected trusted stateless local Policy* independently recomputes allow from the actually staged Study/JCS digest, same run/request identity, current secure TrustedRoot FD/UID and actual aggregate-only artifact inventory and the results match field-for-field. Missing/denied/stale/mismatched decision and policy denial or restricted row output fail closed before Marker/rename. A reconstructed identical value is not rejected for its origin alone. No additional issuer token, nonce, signer, object identity requirement or public schema change is approved.

This is a correction of the ambiguous earlier `forged decision` negative test target, not a weakening of physical root/UID/Policy/Reader authorization. The unchanged original `AMD-E11-G01-P02-001` and its historical Owner 198/S10 199/S11 201 remain valid for their **earlier** WHAT, but not as a current authorization for amended 002 WHAT.

## 2. Change impact, authority and preserved package

- Requirements: `10_22` / `10_91` (NFR-031 and acceptance condition).
- Logical data: `21_23` / `21_40` (structural decision equivalence).
- Basic design: `22_09` / `22_12` (trusted Publisher policy is final authority).
- API/interface: `23_41` / `23_42` (typed value equality, public signature/wire unchanged).
- Detailed design: `30_62` (same sink-owned publisher `validate(manifest,*,privacy)` and actual-stage re-evaluation).
- Implementation instruction: G01/P02 and P05 `06`.
- Independent test instruction: G01 `07` (positive original and value-identical reconstruction; negatives for mismatch/denied policy).

No P01 code/06/test or P03/P04 change was made. P01 checkpoint `9bff61f0eae25236f95f31f2cd3e7c81291f0167` is retained, and P02 has no implementation checkpoint. No independent real-FS/readback/FCI/G01_999 PASS is claimed.

## 3. Separate G01-S10/S11 barriers

**This Owner message explicitly approves only the formal 09 contract amendment.** It does not select or authorize a revised provisional G01-S10 freeze and does not issue a new limited G01-S11 Coding Authorization.

Proposed new S10 source for Owner consideration: immutable `0e36d5d8ce5a4fb9880c4ecff07f4e2256cde492`. It includes all amended normative and audit source before this administrative approval record. **Status: `NEW_S10_OWNER_DECISION_PENDING`.** After a separate Owner decision on the exact SHA, a **further separate new S11 authorization** is required for resumed G01/P02/Trial01 coding. Legacy 201 is not sufficient. No Gate FAIL/08 has occurred; Trial01 remains in force.

This approval record is a post-source administrative document; it does not retroactively change the fixed source SHA.
