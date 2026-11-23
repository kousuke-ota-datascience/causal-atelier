# 193 — ENH-E11 G01 revised limited S11 Coding Authorization (AMD-002)

**Date:** 2026-11-23 JST  
**Decision:** `DEC-G01-P01-S11-REAUTH-02` — **OWNER APPROVED**  
**Owner approval (verbatim):** 「DEC-G01-P01-S11-REAUTH-02を承認する。改訂後の暫定G01-S10凍結SHA bcc1d797e1406e8816d12b725eeace07a181c702 を対象に、G01/P01〜P05の限定Coding Authorizationを発行せよ。」  
**Scope:** `G01 / P01,P02,P03,P04,P05 / Trial01` subject to actual normal-Trial runtime verification  
**Branch:** `feature/ariadne_mvp_e11`  
**Repository:** `kousuke-ota-datascience/causal-atelier`  
**Frozen full Git SHA:** `bcc1d797e1406e8816d12b725eeace07a181c702`  
**Frozen uv.lock Git blob:** `2b83110e86b26b7969fbddf8f98a727370ae19f7`  
**Result:** `OWNER_APPROVED_REVISED_LIMITED_S11 / CODING_AUTHORIZED_SUBJECT_TO_RUNTIME_PREFLIGHT`

## 1. Distinct human authorization chain

1. **190:** `AMD-E11-G01-P01-002` formal 09 `CONTRACT_DEFECT` explicitly Owner-approved.
2. **191:** new provisional G01-S10 frozen to exact immutable full SHA `bcc1d797e1406e8816d12b725eeace07a181c702` — separately documented and approved.
3. **193 (this record):** subsequent distinct Owner **limited G01-S11**. Record `192` is the proposal docket and does not itself grant permission.

Old `179/180`, `185/186/187` and handoffs `181/188` remain historical for superseded source versions. They are preserved, not deleted or silently reinterpreted as AMD-002 authorization. Later administrative commits after `bcc1d797e1406e8816d12b725eeace07a181c702` do not move the frozen source identity; effective 06/Pxx/07/Schema/Method and lock must still match the approved source before coding.

## 2. Exact permitted actions

| Item | Authorization |
| --- | --- |
| Gate | G01 only |
| Operation and Method | DISCOVER / P1-M06, causal-learn |
| Packages | P01–P05 only; P00 is control plan |
| Work order | P01 -> (P02,P03) -> P04 -> P05 -> Candidate Assembly |
| Trial | 01, unless an actual formally recorded FAIL/08 has subsequently changed Trial state |
| First Agent | normal `40_operator_workflows/agent_entry_prompts/10_normal_execution_02_work_package_coding_agent_prompt.md`, variables `GATE_ID=G01 PACKAGE_ID=P01 TRIAL_NO=01` |
| Assigned P01 implementation WHAT | `10_enhance_instruction/G01/06_G01_P01_local_contract_codec.md` at frozen SHA |
| Allowed outputs | G01 scoped source implementation, developer/focused tests, Package status report, checkpoint, approved feature-branch commits/push; then dependency-approved package implementation and Assembly |
| Disallowed | G02–G10, Product v2 ABI/CLI changes, public wire schema drift, dependency/lock manipulation without formal approval, release/production, fictitious scientific PASS or Row output, unapproved AC reduction |

AMD-002 G01 negative reason vocabulary: syntactically only `SCI_NO_ADMISSIBLE_PAG` (exact singleton in P01 Evidence and Status) can be a *pure* negative candidate; matching technical errors must be rejected. This reserved code **does not establish an actual P04 science-negative event**. P04/P05 may not issue/publish it without actual method-specific proof. A valid uncertain or empty-edge PAG remains Graph-positive; no Backend error becomes scientific-negative merely by relabeling.

## 3. Mandatory runtime preflight

Coding Agent, on the *actual* approved Linux repository checkout, must check:

```bash
git branch --show-current
git status --porcelain
git rev-parse HEAD
git rev-parse bcc1d797e1406e8816d12b725eeace07a181c702^{commit}
git rev-parse bcc1d797e1406e8816d12b725eeace07a181c702:uv.lock
git hash-object uv.lock
sha256sum uv.lock
git diff --name-status bcc1d797e1406e8816d12b725eeace07a181c702 HEAD
git remote -v
```

Require exact `feature/ariadne_mvp_e11`, clean tree, correct remote, full frozen commit reachable, uv.lock HEAD and worktree Git blob identical to `2b83110e86b26b7969fbddf8f98a727370ae19f7`, separately measured bytes SHA256, and **no unapproved post-freeze normative 06/Pxx/07/common schema/Method/lock drift**. Admin approvals 190/191/193, docket 192, ledger and handoff are permissible after exact review; do **not** demand branch HEAD equals frozen SHA, and do not invent START_SHA. Check new Owner records 190/191/193, rather than previous 185/186/187 alone. Preserve three historical pre-code BLOCKED stop reports without reset/cleanup.

Verify current Trial01 record: no formal G01_999 FAIL / approved 08 remediation / checkpoint already created. If any preflight guard fails, stop with the appropriate `BLOCKED_*` and report evidence, without partial implementation.

## 4. Unwaived independent acceptance

G01 coding-only exception `DEC-G01-EXEC-01` persists. Independent S09, real Python3.12/B02, local Linux private FS/FD P02/Reader and B03, real FCI fisherz/chisq/gsq B04, independently reviewed MAG/PAG/BK B05 and T2/T3, independent G01 07/999, and Product v2 regressions remain mandatory **before G01_999 PASS**; none are claimed complete.

Non-null BK including empty object is still `BACKEND_SEMANTICS_UNVERIFIED` / exit4 before FCI absent independently established remedy. No fake DAG/Effect, no row release, no Product v2 mutations, no scientific or Gate PASS from a pure P01 test. Do not launch another Gate.

## 5. Current state

`AMD-002_09_APPROVED / G01_S10_RE_FROZEN / G01_S11_RE_AUTHORIZED / P01_TRIAL01_READY_FOR_RUNTIME_PREFLIGHT`.

**The decision record is not a claim that a Coding Agent, focus tests or Package checkpoint ran.** Current execution instructions are documented in `combined_review/194_20261123_g01_p01_trial01_restart_handoff_amd002.md`.
