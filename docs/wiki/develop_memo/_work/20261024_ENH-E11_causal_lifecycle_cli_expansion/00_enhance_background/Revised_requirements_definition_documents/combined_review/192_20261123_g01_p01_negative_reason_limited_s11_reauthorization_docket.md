# 192 — DEC-G01-P01-S11-REAUTH-02: Revised G01 limited Coding Authorization docket

**Date:** 2026-11-23 JST  
**Status:** `OWNER_DECISION_PENDING`  
**Gate:** G01 / ENH-E11 / Ariadne  
**Decision sought:** A **new, distinct limited S11 Coding Authorization** after amended 09 AMD-002 approval and the new provisional S10 re-freeze.

## 1. Sequenced authorization evidence

- `190_20261123_g01_p01_negative_reason_09_owner_approved.md`: `DEC-G01-P01-REBASELINE-02 / FORMAL_09_AMENDMENT_APPROVAL=APPROVED`; owner approved `AMD-E11-G01-P01-002`.
- `191_20261123_g01_p01_negative_reason_revised_provisional_s10_refreeze.md`: new `G01-S10=APPROVED / RE_FROZEN`, full Git SHA `bcc1d797e1406e8816d12b725eeace07a181c702`.
- Prior 185/186/187 authorize only a **superseded** G01/P01 WHAT. None can serve as the current S11.
- Three pre-coding `G01/P01/Trial01` BLOCKED attempts are preserved; no formal FAIL/08, Package checkpoint or fixed Trial Candidate has been observed.

## 2. Exact proposed S11 scope

| Identity / guard | Proposed bound value |
| --- | --- |
| Source repository | `kousuke-ota-datascience/causal-atelier` |
| Working branch | `feature/ariadne_mvp_e11` |
| Immutable revised provisional S10 Git SHA | `bcc1d797e1406e8816d12b725eeace07a181c702` |
| Frozen `uv.lock` **Git blob** | `2b83110e86b26b7969fbddf8f98a727370ae19f7` |
| Gate | **G01 only** |
| Packages | **P01,P02,P03,P04,P05** (P00 plan only) |
| Trial | **01** iff actual runtime state has no formal G01 FAIL/08 trial transition |
| Allowed execution | Assigned G01 Coding Agent implementation, developer/focused tests, Package status report, checkpoint, approved feature-branch commits/push, then dependency-ordered P02/P03/P04/P05 and Candidate Assembly |
| Execution order | `P01 → (P02,P03) → P04 → P05` |
| First prompt | `40_operator_workflows/agent_entry_prompts/10_normal_execution_02_work_package_coding_agent_prompt.md` with `GATE_ID=G01 PACKAGE_ID=P01 TRIAL_NO=01` |
| Assigned coding WHAT | G01 `06_G01_P01_local_contract_codec.md` as frozen at `bcc1d797e1406e8816d12b725eeace07a181c702`. Do not reconstruct WHAT from 09, 07, other Packages or this approval |
| Not authorized | G02–G10, production/release, individual-row G01, Product v2 ABI changes, science PASS, Gate999 PASS, requirements/AC weakening, unreviewed normative amendments |

## 3. Mandatory actual-runtime preflight

On coding machine verify branch, clean working tree, actual START_SHA, reachability of pinned S10 commit, current `uv.lock` Git blob + independently measured byte SHA-256, approved remote repository, actual Trial state, new records 190/191 and a newly **approved** S11 record, and all post-S10 diffs. The branch **may** have newer post-freeze Owner/admin records but must show **zero unapproved changes to effective 06/Pxx/07/Schema/Method contracts and lock**. Preserve historical stops and their local files; never reset/stash/delete user changes merely to pass preflight.

Mandatory outstanding G01_999 obligations stay unchanged: scoped independent S09, B02 Python3.12 schema, B03 private Linux FD/Publisher/Reader, B04 actual FCI backend, B05 independent MAG/PAG/BK and T2/T3, G01 07, Product v2 regression, same fixed candidate. Non-null BK including empty object remains typed denied before FCI absent independently accepted science/stdout remedy. Graph-negative code `SCI_NO_ADMISSIBLE_PAG` is a reserved pure-contract value only; without P04 real validated science proof P05 must not publish a negative, regardless of matching strings.

## 4. Owner decision to be requested

**`DEC-G01-P01-S11-REAUTH-02`:** Approve the above **limited** coding authorization for `G01/P01–P05` only, bound to new S10 full Git SHA `bcc1d797e1406e8816d12b725eeace07a181c702`, unchanged lock and feature branch, preserving all G01_999 obligations.

If approved, write a new **independent** S11 Owner record (do not alter 187) and a new current Coding Agent handoff. This docket and DEC-G01-P01-REBASELINE-02 approval alone **do not authorize coding**.
