# 191 — ENH-E11 G01: Revised Provisional S10 Owner Re-Freeze (AMD-002)

**Decision ID:** `DEC-G01-P01-REBASELINE-02 / G01-S10-REFREEZE`  
**Owner approval:** `APPROVED / PROVISIONAL_G01_S10_RE_FROZEN`  
**Decision date:** 2026-11-23 JST  
**Owner instruction:** 「DEC-G01-P01-REBASELINE-02を承認する」 — this approves formal `AMD-E11-G01-P01-002` and **the proposed specific full SHA** for a revised provisional G01-S10 freeze.  
**Formal 09 prerequisite:** `combined_review/190_20261123_g01_p01_negative_reason_09_owner_approved.md` (commit `afe466eec3ce5e317cbaa24a1311263df4cc42ac`), separately recorded before this S10.  
**New immutable frozen full Git SHA:** **`bcc1d797e1406e8816d12b725eeace07a181c702`**  
**Previous S10 freeze:** `707f6aaac1df5393dbf762448c41db2f1c9dbf35` (186, historical for prior WHAT)  
**Original S10 freeze:** `a05fd072cbb82a7c6e43f45e7208e078f0784a2b` (179, historical)  
**Frozen `uv.lock` Git blob SHA:** `2b83110e86b26b7969fbddf8f98a727370ae19f7`  
**Repository / working branch:** `kousuke-ota-datascience/causal-atelier` / `feature/ariadne_mvp_e11`  
**Next independent Owner decision:** `DEC-G01-P01-S11-REAUTH-02` — NOT APPROVED in this document.

## 1. Freeze identity and hierarchy

The exactly selected **full commit** `bcc1d797e1406e8816d12b725eeace07a181c702` is the immutable G01-S10 normative source baseline. It contains the revised `06_G01_P01_local_contract_codec.md` §6.5.1a, the aligned G01/P04 and P05 `06`, G01 07 acceptance, IF 23_42, DD 30_62, the formal proposed 09 AMD-002 and Author impact record 189. The Owner's positive 09 approval in 190 **supersedes only historical 09 proposal-status wording**; it neither weakens nor changes scientific WHAT.

The branch may move ahead of the frozen SHA to preserve **post-freeze Owner approval 190, this record 191, append-only amendment ledger and a later separately approved S11/handoff**, but these administrative commits do not shift the frozen source identity. Prior to implementation, the Coding Agent must explicitly diff from this immutable SHA and reject any unapproved changes to normative 06/Pxx/07/common schema/Method profiles or `uv.lock`. Never claim branch HEAD must equal frozen SHA when later approval records exist; **actual START_SHA is the checked-out current HEAD**.

## 2. Exact limited G01 scope

- G01 **DISCOVER**, `P1-M06` / `causal-learn`, work-package dependency plan `P01 → (P02,P03) → P04 → P05`.
- Existing G01/common 06, `06_G01_P00_work_package_plan.md`, G01 P01–P05 06 and G01 07 remain normative at the complete frozen SHA; public status/manifest schemas stay unchanged.
- AMD-002 adds an exact G01 scientific-negative reason lexical boundary: only `SCI_NO_ADMISSIBLE_PAG` as the sole negative tuple and Status list; any technical, unknown, duplicate or mixed code fails closed. A P01 synthetic negative test is only pure type verification. No actual P04 scientific-negative producer has been established; the real P04/P05 must not generate negative without separate scientifically justified provenance.
- P01's data/Codec pure validation stays distinct from P02 secure FD/atomic Publisher/Reader, P03 PAG serialization, P04 valid science, P05 orchestration. No Product v2 modifications.

## 3. Preserved independent obligations

The Owner's prior `DEC-G01-EXEC-01` G01-only timing exception remains: independent S09, B02/B04 Python3.12 and B05 MAG/PAG/BK are **not required before G01 coding entry**, but all are required before G01_999 PASS, along with actual B03 Linux FS/Publisher/Reader, real fit and Science Oracle, T2/T3, independent 07, Product v2 regression and same-candidate evidence. Missing independent science/runtime evidence cannot be reported as PASS.

Until accepted independent MAG/PAG and stdout-containment remedy, **all non-null BK including empty object is rejected before FCI** with `BACKEND_SEMANTICS_UNVERIFIED` and CLI exit4. G01 aggregate only, no invented Graph/DAG/effect, no row export, no privacy/atomicity bypass. G02–G10 and release remain unauthorized.

## 4. Trial state and Coding Authorization

The 3 observed P01/Trial01 stops were pre-coding `BLOCKED_CONTRACT_AMBIGUITY` (twice) and `BLOCKED_CODING_AUTHORIZATION` (once), with **no checkpoint/focused test/formal FAIL/08 remediation** reported. Therefore `TRIAL_NO=01` remains the restart default, subject to actual Trial state verification on the coding machine. Preserve the three reports as history.

**This S10 freeze is not a Coding Authorization.** Record 187 authorized the *old* frozen WHAT and is not carried forward. **Until a subsequent distinct Owner-approved G01-S11 is recorded for this full SHA, the Coding Agent must return `BLOCKED_CODING_AUTHORIZATION` and must not implement.**

When separately approved, S11 may authorize only `G01/P01–P05` implementation/developer tests/checkpoint reporting/Candidate Assembly on `feature/ariadne_mvp_e11`; actual branch/root/lock/clean tree/contract/Trial preflight is still mandatory. No S09/07/999 PASS assumed.

## 5. Evidence limitations

This S10 record is a formal Owner decision about a proposed source contract, not an independent scientific review, a signature, an executed Python/FS check, an implementation checkpoint, or proof the real Coding Agent is running. The 190+191 decision chain supersedes earlier approval state only; historical records remain intact.
