# 188 — G01/P01 Trial01 Coding Agent restart handoff (revised S10/S11)

> **SUPERSEDED AFTER THIRD PRE-CODING BLOCK (2026-11-23):** The 185/186/187 authorization chain and S10 SHA 707f6aa... below are HISTORICAL for the earlier G01/P01 WHAT. A further CONTRACT_DEFECT was recorded: AMD-E11-G01-P01-002 (Graph-negative reason code). Revised G01/P01, G01/P04, G01/P05, 07, stock design, and a new proposed 09 were written after that freeze. **Do not restart coding under the authorization or variables below.** A new distinct Owner approval of 09+re-S10 and subsequently a separate re-S11 are required, then the latest authorization handoff must be used. This warning is a control-plane annotation, not a change to the frozen implementation WHAT.


**Date:** 2026-11-23 JST  
**Status:** `RESTART_AUTHORIZED_SUBJECT_TO_RUNTIME_PREFLIGHT / NO_CODING_OBSERVED`  
**Current human authority:** `185` = formal 09 approved, `186` = revised provisional S10 approved, **`187` = separate revised limited S11 approved**. Old `179/180` and earlier `181` handoff are historical for superseded contract; their old source identity must not be used for restart.
**Approved immutable frozen full commit:** `707f6aaac1df5393dbf762448c41db2f1c9dbf35`.  
**Frozen uv.lock Git blob:** `2b83110e86b26b7969fbddf8f98a727370ae19f7`.  
**Repository/branch:** `kousuke-ota-datascience/causal-atelier` / `feature/ariadne_mvp_e11`.

## 1. Normal Work Package invocation

Use the instantiated prompt, not the workflow template:

```text
以下の実行時変数で、指定されたENH-E11 Coding Agent Promptを実行せよ。

GATE_ID=G01
PACKAGE_ID=P01
TRIAL_NO=01

Prompt:
docs/wiki/develop_memo/_work/20261024_ENH-E11_causal_lifecycle_cli_expansion/40_operator_workflows/agent_entry_prompts/10_normal_execution_02_work_package_coding_agent_prompt.md
```

The **only** assigned P01 implementation WHAT is `10_enhance_instruction/G01/06_G01_P01_local_contract_codec.md`, at the new approved S10. New exact `ValidatedRunEvidence` and Manifest/ref join semantics are in P01 §6.5. Do not import 09/07/P02/P05 as coding WHAT. 09 and records 185–187 establish amendment and permission only. Running the same prompt after the authority change does not make earlier stopped attempts a `PACKAGE_READY` checkpoint.

## 2. Before implementation on actual checkout

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

Check branch and clean worktree, exact frozen ref availability, current lock blob = frozen blob, and actual files' byte SHA256; remote alias `causal-atelier` must point to specified repository. Check **185/186/187** positive records. Inspect post-freeze diff for **only** 185–188, the ledger and other approved administrative changes before implementation; no unexpected effective 06/Pxx/07/common schema or `src/tests/pyproject/uv.lock` drift. Historical `NOT_AUTHORIZED` draft headers cannot negate positive later Owner records, but a substantive drift still blocks. If any check fails, report observed `BLOCKED_*` and do not clean or reset user work.

Confirm Trial01 is still normal WP execution (no formal G01_999 FAIL/08 remedial Trial), preserve the two earlier external `BLOCKED_CONTRACT_AMBIGUITY` and `BLOCKED_CODING_AUTHORIZATION` reports. Capture **actual** START_SHA; **do not set START_SHA to approved freeze SHA**. Then implement only assigned P01, run actual focused verification, checkpoint/report, and push to feature branch if successful. P01 completion ≠ G01 science PASS.

## 3. After P01

Only if P01 `PACKAGE_READY` with actual checkpoint and focused test evidence, use Orchestrator to release dependent P02/P03, followed by P04/P05 and Candidate Assembly. Independent 07/G01_999 require real FS/backend, independent MAG/PAG/BK science, Python3.12 B02/B04, B05 T2/T3 and legacy Product v2 regression; none is waived or presumed PASS. G02–G10 remain unauthorized.

**The entry document is a control-plane handoff, not a new scientific contract or proof of a running agent.**
