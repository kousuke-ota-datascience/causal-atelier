# 187 — G01 revised limited S11 Coding Authorization (Owner decision)

**Decision ID:** `DEC-G01-P01-S11-REAUTH-01`  
**Decision:** `OWNER_APPROVED_REVISED_LIMITED_CODING_AUTHORIZATION`  
**Date:** 2026-11-23 JST  
**Human approval provenance:** The Owner explicitly replied 「承認する」 to the distinct proposed `DEC-G01-P01-S11-REAUTH-01` after the revised 09 contract approval and revised S10 were committed. This grants only the stated restricted coding scope, not scientific PASS, independent approval or other Gates.  
**Prerequisites:** 09 Owner approval `combined_review/185_20261123_g01_p01_amendment_09_owner_approved.md`, then revised S10 freeze `combined_review/186_20261123_g01_p01_revised_provisional_s10_owner_refreeze.md`. This separate record grants the new S11 **after** both.
**Immutable revised S10 full Git SHA:** `707f6aaac1df5393dbf762448c41db2f1c9dbf35`  
**Frozen uv.lock Git blob SHA:** `2b83110e86b26b7969fbddf8f98a727370ae19f7`  
**Repository and sole work branch:** `kousuke-ota-datascience/causal-atelier` — `feature/ariadne_mvp_e11`

## 1. Scope of new authorization

| Binding | Value |
| --- | --- |
| Project / Enhance | Ariadne / ENH-E11 |
| Gate | **G01 only** |
| Mode | WORK_PACKAGE |
| Packages | **P01,P02,P03,P04,P05 only** (P00 is not coding) |
| Normal first execution | `GATE_ID=G01 PACKAGE_ID=P01 TRIAL_NO=01`, subject to runtime evidence |
| Allowed | Assigned coding, focused/developer tests, Package checkpoint/report, evidence commit/push, then dependency-ordered packages and Candidate Assembly |
| Dependency order | `P01 → (P02,P03) → P04 → P05` |
| Assigned P01 implementation authority | Amended `10_enhance_instruction/G01/06_G01_P01_local_contract_codec.md` from new frozen full SHA above |
| Changed WHAT approval | `09_ENH-E11_G01_AMD-E11-G01-P01-001_Gate_Contract_Amendment.md` via 185 and 186 |
| Not authorized | G02–G10, production use, scientific PASS, Gate999 PASS, Product v2 ABI/CLI mutation, new row export, relaxed acceptance or changed backend/lock |

Original 179 (S10) and 180 (S11) apply to *old* frozen WHAT and cannot authorize the amended contract. Historical `NOT_FROZEN/NOT_AUTHORIZED` headers in frozen documents describe issuance state; current decision state is established by **185 + 186 + 187**, without rewriting immutable normative WHAT. Subsequent records 185/186/187 and approved administrative handoff/ledger commits may advance the branch **without** changing the frozen SHA. No unapproved change to effective source 06/Pxx/07/common scientific schema or lock is permitted.

## 2. Mandatory preflight on the actual coding machine

```bash
git branch --show-current
git status --porcelain
git rev-parse HEAD
git rev-parse 707f6aaac1df5393dbf762448c41db2f1c9dbf35^{commit}
git rev-parse 707f6aaac1df5393dbf762448c41db2f1c9dbf35:uv.lock
git hash-object uv.lock
sha256sum uv.lock
git diff --name-status 707f6aaac1df5393dbf762448c41db2f1c9dbf35 HEAD
git remote -v
```

Require correct feature branch, clean working tree, reachability of the new immutable S10 SHA, matching Git blob of current `uv.lock`, actual byte SHA256 recorded separately, and actual remote mapping to unchanged repository. Inspect all commits since revised S10: only Owner approvals 185/186/187, ledger and approved administrative handoff may precede new coding; any unapproved normative drift, missing authorization evidence or changed Trial status must fail closed.

Before selecting normal Trial01 route, inspect actual Trial records and confirm no formal G01 FAIL/08 remediation. Both prior Trial01 stops were **pre-implementation BLOCKED**, not formal Gate FAIL, and neither created a Package checkpoint. Do not reset/checkout/stash a dirty tree, falsify evidence, or convert a BLOCKED report into PASS. P01 Coding Agent must read **assigned P01 alone for implementation WHAT**; other 06/07/09/Owner records govern authorization/traceability, not permission to invent behavior.

If preflight passes, run `40_operator_workflows/agent_entry_prompts/10_normal_execution_02_work_package_coding_agent_prompt.md` with `GATE_ID=G01 PACKAGE_ID=P01 TRIAL_NO=01`; discover actual checkout test paths and record actual START_SHA, focused verification, checkpoint SHA, status and evidence. No assumed completed run from this authorization.

## 3. Unwaived acceptance and safety conditions

`DEC-G01-EXEC-01` continues to permit scoped G01 development before unavailable independent S09/B02/B04/B05 evidence **but not G01_999 acceptance**. All actual G01 S09, Python3.12 B02, Linux private FD/FS/Publisher/Reader B03, real fitted FCI fisherz/chisq/gsq B04, independent MAG/PAG/BK B05 including safe remedy and T2/T3, independent G01 07, Product v2 regressions and 999 remain mandatory. Current `G01_999=BLOCKED`, G02–G10 not authorized. Non-null BK including empty object must be rejected before FCI with `BACKEND_SEMANTICS_UNVERIFIED` / exit4 until independent science + stdout containment approval. No speculative graph scientific truth, no dummy Effect, no row release, no invalid FS publication.

## 4. Result

**`AMENDMENT_09=APPROVED` (185); `G01_REVISED_PROVISIONAL_S10=APPROVED` (186); `G01_REVISED_LIMITED_S11=APPROVED` (187).**

**`G01/P01/Trial01=AUTHORIZED_TO_RESTART_SUBJECT_TO_REAL_RUNTIME_PREFLIGHT`.** No package implementation, actual Linux preflight, focused tests or checkpoint have been observed from this chat; this authorization is not a completion claim.
