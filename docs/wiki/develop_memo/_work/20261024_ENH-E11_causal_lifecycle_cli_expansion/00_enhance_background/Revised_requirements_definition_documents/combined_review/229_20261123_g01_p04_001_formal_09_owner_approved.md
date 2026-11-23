# 229 — G01/P04 AMD-E11-G01-P04-001 formal 09 Owner approval

**Date:** 2026-11-23 JST  
**Decision ID:** `DEC-G01-P04-001-09-APPROVE-01`  
**State:** `FORMAL_09_OWNER_APPROVED / S10_REFREEZE_NOT_YET_APPROVED / S11_NOT_AUTHORIZED`  
**Owner instruction:** 「AMD-E11-G01-P04-001 の正式09承認 — 承認する。」

## Approved contract candidate

- Repository: `kousuke-ota-datascience/causal-atelier`
- Branch: `feature/ariadne_mvp_e11`
- Exact **pre-approval-record** amendment/content HEAD: `9a60a3aac2eae51a2a2d9d5b7c11c5f246825f9f`
- Formal contract amendment: `10_enhance_instruction/G01/09_ENH-E11_G01_AMD-E11-G01-P04-001_Gate_Contract_Amendment.md`
- Adopted method policy: `DEC-G01-P04-CI-ELIG-01=A`: conservative exhaustive enumeration of unordered (X,Y) and every S subset of remaining observed variables *before any FCI invocation*, with CI-family-specific sample/support checks, negative boundary tests, fail-closed on incomplete evaluation, no implicit fallback.
- Referenced docket: `combined_review/228_20261123_g01_p04_ci_eligibility_owner_decision_docket.md`
- Previous S10: `52e5c60176d6b72c91f839ef267f46657bd380b5`
- Previous stopped P04 START_SHA: `748deb4ba6287bbd1b71e233504c36c6f430e5b7`
- Protected P01 checkpoint: `9bff61f0eae25236f95f31f2cd3e7c81291f0167`
- Protected P03 checkpoint: `858c9f73366036a2d1445e558135cd521f611462`

## Approved file-level normative delta

At the approved content SHA the diff against stopped START_SHA was exactly:

1. `00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_63_causal_method_adapters.md` (modified).
2. `10_enhance_instruction/G01/06_G01_P04_fci_backend_oracle.md` (modified).
3. `10_enhance_instruction/G01/07_Ariadne_ENH-E11_G01_test_instruction.md` (modified).
4. `10_enhance_instruction/G01/09_ENH-E11_G01_AMD-E11-G01-P04-001_Gate_Contract_Amendment.md` (new).
5. `00_enhance_background/Revised_requirements_definition_documents/combined_review/228_20261123_g01_p04_ci_eligibility_owner_decision_docket.md` (new).

The approved change is strictly P1-M06 CI eligibility: the full finite candidate set and conservative per-family admissibility boundary. It does not modify existing P01/P03 implementation/checkpoints, P02/P05 code, `uv.lock`, public E11 wire/schema versions, Product v2, PAG/Graph semantics, BK non-null protection or G01_999 independent scientific acceptance. The conservative minimum expected cell count 5 is a **screening rule**, not a universal asymptotic guarantee. Exact maximum-p/compute cap and numerical-conditioning tolerance remain unapproved if they require normative quantitative values; incomplete or unreliable screening fails closed rather than inventing a PASS.

## Separate downstream decisions are still required

**This record is formal 09 only.** It must not be interpreted as either:

- Owner's independent revised G01-S10 Freeze approval of an **immutable final full Git commit SHA including this record**, or
- Owner's separate limited G01-S11 Coding Authorization at that frozen SHA.

The new commit created by recording this decision is a **candidate S10 SHA**, not an approved S10. Confirm its identity/ancestry and any intervening changes before requesting Owner freeze. No Coding Agent P04 resume, source implementation change, post-freeze contract rewrite or Gate999 PASS is authorized by this 09 approval alone.
