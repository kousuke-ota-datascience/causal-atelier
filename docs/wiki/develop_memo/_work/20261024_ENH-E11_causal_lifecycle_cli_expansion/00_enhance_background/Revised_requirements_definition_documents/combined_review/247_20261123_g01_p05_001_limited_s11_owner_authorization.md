# 247 — G01/P05 limited S11 Owner Coding Authorization

**Date:** 2026-11-23 JST  
**Decision ID:** `DEC-G01-P05-001-S11-REAUTH-01`  
**Decision status:** `S11_OWNER_APPROVED / G01_P05_TRIAL01_LIMITED_CODING_AUTHORIZED / DEFERRED_PRODUCT_POLICY_BRIDGE_UNFULFILLED / G01_999_NOT_PASSED`  
**Repository:** `kousuke-ota-datascience/causal-atelier`  
**Working branch:** `feature/ariadne_mvp_e11`  
**Immutable active G01-S10 contract SHA:** `3ea759825810e95425a9e7557c3b2cc46b21157d`

## 1. Explicit Owner decision

Owner expressly approved the following decision on 2026-11-23 JST:

> DEC-G01-P05-001-S11-REAUTH-01を承認する。現行G01-S10凍結SHA 3ea759825810e95425a9e7557c3b2cc46b21157d を対象に、G01/P05/Trial01の限定Coding Authorizationを再発行せよ。P02チェックポイント3a76a0aa1698037354b284ba7b5a875300473ce6、P03チェックポイント858c9f73366036a2d1445e558135cd521f611462、P04チェックポイント7dcf2061dae3c8832b2b3ec9be6900ad6ee7edb6、および既承認の科学的契約・公開E11 Schema Version・独立G01_999受入条件・DEFERRED_PRODUCT_POLICY_BRIDGE未完了依存を維持する。

This record issues **only** `GATE_ID=G01 / PACKAGE_ID=P05 / TRIAL_NO=01` Coding Authorization against the immutable S10 SHA above. It is a post-freeze administrative Owner authorization and does **not** change or replace the frozen contractual tree. Prior S11 authorizations bound to earlier S10 SHAs, and `DEC-G01-P04-004-S11-REAUTH-01` limited to P04, do **not** independently authorize P05.

## 2. Verified evidence before S11 issuance

The remote `feature/ariadne_mvp_e11` branch was at `93c2fcf71532d87049a8c184670b60c75420ae00` before this record was written. GitHub ancestry comparisons showed:

| Baseline | Exact SHA | Relation to pre-record HEAD |
| --- | --- | --- |
| Current G01-S10 | `3ea759825810e95425a9e7557c3b2cc46b21157d` | Ancestor; ahead 4, behind 0 |
| Protected P02 checkpoint | `3a76a0aa1698037354b284ba7b5a875300473ce6` | Ancestor; ahead 53, behind 0 |
| Protected P03 checkpoint | `858c9f73366036a2d1445e558135cd521f611462` | Ancestor; ahead 43, behind 0 |
| Protected P04 checkpoint | `7dcf2061dae3c8832b2b3ec9be6900ad6ee7edb6` | Ancestor; ahead 1, behind 0 |

S10-to-HEAD changes were the post-freeze P04 S10/S11 administrative records `245`/`246`, P04 implementation source/tests, and P04 package / trial progress evidence. The immediate P04 checkpoint-to-HEAD change is P04 implementation evidence. No new P05 checkpoint is claimed by this authorization. The stopped P05 attempt reported `START_SHA=93c2fcf71532d87049a8c184670b60c75420ae00`, no modified files, no P05 implementation, no focused verification and no P05 checkpoint. The Agent must independently recheck these facts at restart.

## 3. Exact authorized coding scope and authority hierarchy

Authorized work: implement and locally verify **G01/P05/Trial01 only**, under the frozen S10 requirement/design/interface/detail/06/07 hierarchy, including the following actual package instruction documents:

- `10_enhance_instruction/G01/06_G01_P05_cli_use_case_privacy.md`
- `10_enhance_instruction/G01/06_Ariadne_ENH-E11_G01_implementation_instruction.md`
- `10_enhance_instruction/G01/07_Ariadne_ENH-E11_G01_test_instruction.md`

P05 is the DISCOVER-only Local CLI/UseCase/Privacy integration and Product v2 regression package. It may integrate the already implemented P01 strict codecs/Manifest DTO, P02 TrustedRoot/FD-bound references/atomic Publisher/Reader, P03 PAG/GraphEvidence lineage and P04 selected P1-M06 FCI Method Registry/eligibility/Discovery Port, solely through their approved published internal contracts. Maintain strict version/method/operation/estimand, true runtime evidence, complete Graph/Manifest/Status joins, privacy fail-closed behavior, no row export, existing CLI exit semantics, no false scientific-negative publication for a technical error, no fabricated science PASS, and exact verified committed readback before completed outcomes.

**Do not** modify completed P01/P02/P03/P04 package implementation, their 06/07 contracts or protected checkpoint history as incidental P05 work. If integration exposes an unavoidable defect in a completed Package, stop that affected change, document concrete evidence and compatibility/regression impact, and request separate Owner disposition. The previously approved P01-specific exception does not automatically extend to P02/P03/P04/P05. Do not update the existing Product v2 CLI/Web/API/DB/Worker, legacy `src/ariadne/product/application/scientific_validation_service.py`, or its `ESTIMATOR_CAPABILITIES` simply to make P05 tests pass. No E11 public schema/version, `uv.lock`, unapproved requirements, design, or new Gate scope may be changed under this S11.

## 4. Scientific, architecture, compatibility and acceptance obligations retained

- The effective P1-M06 Method/FCI preflight contract, including AMD-001 exhaustive all-X/Y/all-S CI screening, AMD-002 full declared categorical domain/expected counts, AMD-003 float64 Fisher-Z numeric eligibility, and AMD-004 scoped Local Method authority with no fictitious Product delegation, is unchanged.
- Non-null BK remains fail-closed before FCI invocation under the currently approved Backend constraints. Do not invent a scientific Graph-negative or `SCI_NO_ADMISSIBLE_PAG` producer; an actual Backend/Graph failure remains technical failure.
- Preserve immutable input/output ContentRefs, PAG endpoint uncertainty, actual node names, Graph evidence lineage, actual Backend distribution/version and runtime provenance; no graph-to-DAG or non-Effect-to-Effect escalation.
- Existing Product v2 behavior, public E11 Schema Version, independent verification and backward compatibility criteria remain unchanged.
- `DEFERRED_PRODUCT_POLICY_BRIDGE` is **UNFULFILLED**, not implemented, not retired, and not automatically moved to a fictitious later Gate. Completing the shared-policy G01_999 acceptance item requires the separately approved Product bridge with independent Product regression, or a separate formal Owner decision explicitly changing acceptance phasing. This S11 does not waive the dependency.
- Actual Python3.12 Backend/FCI, Linux FS/Reader, independent MAG/PAG/BK science, Product v2 regression, T2/T3 and independent G01_999 remain required for Gate acceptance. Focused Package tests or P05 checkpoint alone do not constitute Gate PASS.

## 5. Restart conditions, reporting and stop discipline

At Agent restart, independently verify all of:

1. Remote and local branch are the designated `feature/ariadne_mvp_e11` branch, fast-forward synced and the working tree is clean; capture a **new actual** full START_SHA.
2. Active S10 exact SHA `3ea759825810e95425a9e7557c3b2cc46b21157d` remains an ancestor; inspect all post-S10 differences and accept only authorized administrative/evidence and already approved P04 changes plus this S11 record. Do not assume all later branch modifications are authorized.
3. Verify the pinned `uv.lock` Git blob and physical bytes match the frozen contract; the stopped Agent previously reported Git blob `2b83110e86b26b7969fbddf8f98a727370ae19f7`, but this must be rechecked at the actual restart.
4. Verify P02, P03, P04 exact checkpoint ancestor relationships, Package evidence, applicable focused verification, actual current source compatibility, and the absence of a prior P05 checkpoint or material remediation.
5. Recheck effective Python3.12 / optional Backend availability as appropriate and distinguish deferred independent acceptance evidence from Package-entry blockers; do not manufacture successful test results.

If a material unapproved contract conflict, completed-Package modification, public API/science change, unexpected Product v2 compatibility impact, or unexpected authorization/snapshot mismatch appears, stop before making the affected change and request Owner decision. Do not replace frozen WHAT with observed implementation behavior.

On execution, write the actual P05 Package status/verification evidence, exact commands/results, full source checkpoint SHA and push confirmation if and only if achieved. If blocked, report evidence and leave the implementation/checkpoint untouched. This administrative S11 record is **authorization only**: it is not P05 implementation, test PASS, a P05 checkpoint, independent science verification or G01_999 PASS.

## 6. Change-control disposition

The reported blocker is solely missing P05-specific S11 under the current S10. No 09 contract amendment, revised S10 freeze, higher-level normative design change or 06/07 modification is warranted to remedy this authorization-only blocker. The historical S10 and P01–P04 records remain immutable; this post-freeze S11 record is the sole intended change.
