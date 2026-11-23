# 201 — Revised G01/P02 limited S11 Owner Coding Authorization

**Decision ID:** `DEC-G01-P02-S11-REAUTH-01`  
**Status:** `OWNER_APPROVED / LIMITED_G01_S11_AUTHORIZED`  
**Date:** 2026-11-23 JST  
**Verbatim Owner approval:** 「`DEC-G01-P02-S11-REAUTH-01` を承認する」  
**Repo:** `kousuke-ota-datascience/causal-atelier`  
**Branch:** `feature/ariadne_mvp_e11`  
**Normative immutable revised provisional G01-S10 WHAT SHA:** `6df4b94de72a6ec8619f315e55ba7821e1eb157c`  
**Frozen uv.lock Git blob:** `2b83110e86b26b7969fbddf8f98a727370ae19f7`  
**Observed previous actual uv.lock byte SHA256 in Agent report:** `1d92a472fc3c750c90458a40ae5a09ba3feefbd3d99eee61b0cdbff00d31cffb` (must remeasure in runtime)  
**P01 existing Package-ready checkpoint:** `9bff61f0eae25236f95f31f2cd3e7c81291f0167`  
**Next execution:** `GATE_ID=G01 PACKAGE_ID=P02 TRIAL_NO=01`  
**Authority predecessors:** 198 (Owner-approved formal 09 AMD-E11-G01-P02-001), 199 (Owner-approved revised provisional G01-S10 freeze), 200 (separate S11 decision docket), 202 (five-layer RD/LDD/BD/IF/DD-to-06/07 audit).

## 1. Owner decision and its exact limits

The Owner explicitly approved the separately requested `DEC-G01-P02-S11-REAUTH-01` after the formal 09 (198) and revised S10 (199) were recorded and after the five-layer coding/test instruction consistency check (202). This grants **limited G01/P01–P05 Coding Authorization to execute the approved frozen WHAT and developer verification**, not approval to alter normative design. P01 is already `PACKAGE_READY` and is not to be reimplemented without a new demonstrated defect or explicit Owner change; **P02/Trial01 is the next bounded work package**. P03/P04/P05 remain subject to P00 dependency and individual verification. No G02–G10, product release, arbitrary wire ABI changes or additional science method work is authorized.

Historic Owner S11 record 193 was limited to previous S10 `bcc1d797e1406e8816d12b725eeace07a181c702`; it does **not** authorize the P02 AMD-001 amended source. This record is the **sole current new S11 authorization** anchored to immutable `6df4b94de72a6ec8619f315e55ba7821e1eb157c` plus its predecessor decisions. Later administrative Git commits do **not** change the frozen WHAT SHA.

## 2. Contract and evidence invariants

Use the exact files from frozen WHAT:

- `00_enhance_background/Revised_requirements_definition_documents/{10_requirements_definition,21_logical_data_design,22_product_basic_design,23_api_interface_design,30_detailed_design}/` for Requirement/LDD/BD/IF/DD stock semantics.
- `10_enhance_instruction/G01/06_Ariadne_ENH-E11_G01_implementation_instruction.md` and `06_G01_P00_work_package_plan.md` for Gate-wide and work-package sequencing.
- `10_enhance_instruction/G01/06_G01_P02_atomic_publication_reader.md` for the assigned P02 self-contained primary execution contract, cross-validating `06_G01_P05_cli_use_case_privacy.md` for interaction.
- `10_enhance_instruction/G01/07_Ariadne_ENH-E11_G01_test_instruction.md` for developer G01 focused tests and later independent acceptance.
- Formal 09 `10_enhance_instruction/G01/09_ENH-E11_G01_AMD-E11-G01-P02-001_Gate_Contract_Amendment.md` and audits 195/196/197/202 as authority trace, not a license to invent behavior.

P02 must implement `seal(*,sink,manifest,privacy)` delegation to **the same run-scoped sink-owned** `LocalArtifactPublisher.validate(manifest,*,privacy)`, not a second publisher or a dropped/forged decision. The Publisher independently rechecks staged exact Study/JCS request digest, live effective TrustedRoot FD/device/inode/owner/mode/FS, UID, complete staged inventory and injected stateless privacy Policy. Missing/denied/stale/cross-run/root/actor/unauthorized row data or mismatched decision must fail closed **before Marker/rename**. Recheck before commit and independent Reader after real no-clobber atomic publish. No G01 row export. Do not promote synthetic science-negative or a technical Backend failure into legitimate SCI_NO_ADMISSIBLE_PAG.

## 3. Mandatory actual runtime preflight

The Coding Agent, **not this approval document**, must verify:

1. Checked-out `feature/ariadne_mvp_e11`, correct repository/remote, clean worktree and actual execution START_SHA.
2. Frozen `6df4b94de72a6ec8619f315e55ba7821e1eb157c` is an ancestor of current HEAD; diff from frozen normative WHAT consists solely of approved administrative/Owner/audit records before coding. Later source/test commits require explicit run provenance and checkpoint.
3. Actual `uv.lock` tracked blob matches `2b83110e86b26b7969fbddf8f98a727370ae19f7`; actual worktree file bytes SHA256 are recomputed and compared to historic reported value, not assumed.
4. Formal 09 Owner approval 198, provisional S10 Owner freeze 199, **this new S11 201**, and scope/trace 200/202 all refer to the same immutable frozen WHAT.
5. Trial01 has no actual formal Gate FAIL or 08 remediation, P01 `9bff61f0eae25236f95f31f2cd3e7c81291f0167` is an ancestor and PACKAGE_READY report agrees; there is no P02 implementation checkpoint or an unreported conflicting change.
6. P02 developer test target and real Linux FD/FS capabilities are actually available. If any mandatory prerequisite is missing, use typed BLOCKED and report, do not proceed on nominal authorization alone.

## 4. Focused verification and checkpoint

Perform P02's secure root/ContentReferencePort actual-byte and race negatives, stage+Manifest/Marker+fsync/renameat2(RENAME_NOREPLACE), EEXIST/race/indeterminate readback, PrivacyDecision wrong run/hash/root/UID/inventory/policy and other G01 07-02/05/06/11 cases. Protect prior P01 focused and Product v2 regression tests. Record actual commands, exits, evidence and failures in official P02 Package report and checkpoint only on demonstrated developer-level readiness; do not claim independent G01_999 acceptance.

The independent G01 Linux FS proof, real Python3.12/FCI BK and Graph science, separate independent S09/07/B02–B05/T2/T3, and Product v2 regressions remain required for Gate PASS. The owner permission is **to code and test**, not to declare those completed.

## 5. Scope enforcement

Never edit frozen design, 06/07 contracts or `uv.lock` under this S11 without separate amendment approvals; do not force-update refs or overwrite P01 checkpoint/old stop reports. New material WHAT discrepancy must stop and enter the 09→S10→S11 cycle, not be silently implemented as a guessed requirement. P01 reverse alignment was an approved bounded documentation exception, not a rule for P02.

## 6. Current handoff

Use the new P02/Trial01 execution handoff 203 (recorded after this authorization) and the existing normal Work Package Coding Agent entry prompt under `40_operator_workflows/agent_entry_prompts/10_normal_execution_02_work_package_coding_agent_prompt.md`. P02 is released from **authorization-only BLOCKED**, subject to successful actual preflight; no runtime coding or tests were performed by this Owner approval record.
