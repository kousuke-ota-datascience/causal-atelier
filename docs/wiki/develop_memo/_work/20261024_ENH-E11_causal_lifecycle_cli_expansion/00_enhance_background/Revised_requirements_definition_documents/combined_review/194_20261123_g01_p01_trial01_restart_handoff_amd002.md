# 194 — Current G01/P01 Trial01 restart handoff after AMD-002 S11

> **P02 CONTRACT CHANGE — HISTORICAL HANDOFF:** P02 Trial01 was blocked at `4248ca24204ed8ede27527191b1a53d9ced1ff5a` owing to the PrivacyDecision handoff ambiguity; see AMD-E11-G01-P02-001 and 195. Historical S10 `bcc1d797e1406e8816d12b725eeace07a181c702` / S11 record193 do NOT authorize amended P02 WHAT. Do not restart P02 until formal new 09 Owner approval, new S10 freeze and separate new S11 are recorded. P01 ready checkpoint `9bff61f0eae25236f95f31f2cd3e7c81291f0167` is preserved. The remainder of this document is prior-version evidence, not current P02 coding authority.


**Date:** 2026-11-23 JST  
**Status:** `AUTHORIZED_TO_RESTART_SUBJECT_TO_ACTUAL_RUNTIME_PREFLIGHT`  
**Approval authority:** **190 (formal 09 AMD-002) → 191 (new revised S10) → 193 (new distinct limited S11)**. Prior 185/186/187 and 181/188 concern earlier contract baselines and are not active entry authority.  
**New fixed revised S10 full SHA:** `bcc1d797e1406e8816d12b725eeace07a181c702`  
**Frozen uv.lock Git blob:** `2b83110e86b26b7969fbddf8f98a727370ae19f7`  
**Repository/branch:** `kousuke-ota-datascience/causal-atelier` / `feature/ariadne_mvp_e11`

## 1. Single next Agent launch

After syncing the actual worktree to the approved latest branch state (without destructive reset of user work), invoke the **existing instantiated normal Work Package Coding Agent Prompt** with:

```text
GATE_ID=G01
PACKAGE_ID=P01
TRIAL_NO=01

Prompt:
docs/wiki/develop_memo/_work/20261024_ENH-E11_causal_lifecycle_cli_expansion/40_operator_workflows/agent_entry_prompts/10_normal_execution_02_work_package_coding_agent_prompt.md
```

**Authorized WHAT:** exactly assigned `10_enhance_instruction/G01/06_G01_P01_local_contract_codec.md` at frozen SHA `bcc1d797e1406e8816d12b725eeace07a181c702`. The new §6.5.1a defines an explicit closed Graph-negative reason code. Do not reconstruct P01 implementation semantics from other Pxx/07/09 or the governance records; they govern integration, test acceptance, and human authorization. The original three pre-coding BLOCKED stops are not a formal FAIL/08 and do not increment Trial automatically.

## 2. Concrete preflight / authorization binding

Before any code changes, check:

- `git branch --show-current`: `feature/ariadne_mvp_e11`; `git status --porcelain`: clean; `git rev-parse HEAD`: record actual `START_SHA`.
- `git rev-parse bcc1d797e1406e8816d12b725eeace07a181c702^{commit}` succeeds; freeze SHA is *not* identical to moving branch HEAD after administrative Owner records.
- `git rev-parse HEAD:uv.lock` and `git hash-object uv.lock` both equal `2b83110e86b26b7969fbddf8f98a727370ae19f7`; separately record `sha256sum uv.lock`.
- `git diff --name-status bcc1d797e1406e8816d12b725eeace07a181c702 HEAD` and any intervening commits: **only approved administrative 190/191/192/193/194, ledger, historical handoff annotations before coding**; no changed active 06/Pxx/07/Method/Schema/lock. Check actual remote points to authorized repository.
- Confirm actual approved Owner documents 190,191,193; old 185–187 alone are insufficient.
- Confirm Trial01 state not superseded by actual Gate999 FAIL/08 or a P01 checkpoint. Preserve the three prior BLOCKED reports.

If any preflight fails, report a real `BLOCKED_*` instead of guessing, altering contractual WHAT or deleting existing reports.

## 3. Scoped implementation and evidence

If preflight passes, implement **P01 only** and run focused/developer verification with actual collected tests. Report actual START_SHA, tests (or honestly BLOCKED verification), Package result and checkpoint SHA. Commit/push only the authorized G01 package and evidence to the feature branch. Do not claim full G01_999 PASS. G01 P02/P03 can start only after P01 PACKAGE_READY and dependency evidence, then P04/P05 and Candidate Assembly in dependency order.

## 4. Non-waived scientific obligations

The reserved G01 negative code `SCI_NO_ADMISSIBLE_PAG` is a synthetic P01 structural fixture only until a genuine P04 science proof exists; never transform Backend failure/low power/invalid BK/malformed Graph into a science-negative published bundle. All independent S09/B02/B03/B04/B05/T2/T3/07/999 and Product v2 regression remain mandatory. G02–G10 not authorized.

**This handoff is an execution instruction, not a record that Coding Agent actually executed.**
