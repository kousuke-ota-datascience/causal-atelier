# 200 — DEC-G01-P02-S11-REAUTH-01: revised limited G01 Coding Authorization docket

**Date:** 2026-11-23 JST  
**Status:** `OWNER_DECISION_PENDING`  
**Request:** Independent new limited G01-S11 Coding Authorization for revised P02 contract under `AMD-E11-G01-P02-001`.

## 1. Prerequisite sequence already complete

- **198** Owner formally approved AMD-E11-G01-P02-001 09, validating the corrected privacy authority and full RD/LDD/BD/IF/DD/06/07 alignment.
- **199** Owner separately re-froze provisional G01-S10 to **`6df4b94de72a6ec8619f315e55ba7821e1eb157c`**.
- The exact source commit is immutable. Later records 198–200 and 80 ledger are post-freeze administrative records. New S11 may not alter that normative source identity.
- Existing P01 checkpoint `9bff61f0eae25236f95f31f2cd3e7c81291f0167` is an ancestor of the new freeze and was confirmed `PACKAGE_READY`. The P02 pre-code stop `BLOCKED_CODING_AUTHORIZATION` was a correct hold; no P02 checkpoint/formal Gate FAIL/08 remediation exists.

## 2. Proposed limits of new Coding Authorization

| Guard | Exact proposed value |
| --- | --- |
| Repository | `kousuke-ota-datascience/causal-atelier` |
| Branch | `feature/ariadne_mvp_e11` |
| Frozen full normative Git SHA | `6df4b94de72a6ec8619f315e55ba7821e1eb157c` |
| uv.lock Git blob | `2b83110e86b26b7969fbddf8f98a727370ae19f7` |
| Gate | G01 only |
| Packages | G01/P01–P05 limited as already scoped, **next Package P02** |
| Trial | 01, subject to actual no-formal-FAIL/08 status |
| P01 dependency | Existing `PACKAGE_READY` checkpoint `9bff61f0eae25236f95f31f2cd3e7c81291f0167`; no reimplementation |
| Normal Agent Prompt | `40_operator_workflows/agent_entry_prompts/10_normal_execution_02_work_package_coding_agent_prompt.md` |
| First variables | `GATE_ID=G01 PACKAGE_ID=P02 TRIAL_NO=01` |
| Assigned P02 WHAT | `10_enhance_instruction/G01/06_G01_P02_atomic_publication_reader.md` at frozen SHA; aligned 23_41/23_42, 30_62, P05 and G01 07 govern cross-layer acceptance |
| Permitted | Implement P02 secure FD/input verification, Staging/Publisher/Reader, concrete PrivacyDecision binding/re-evaluation, focused developer & actual Linux FS tests, package report and approved feature branch checkpoint; subsequent packages by dependency only |
| Prohibited | G02–G10; P01 rewrite without new approval; changing approved normative contracts/lock/public wire/Product ABI; SCI/Gate999 PASS by assertion; release/production |

## 3. Mandatory live preflight

Actual Coding Agent verifies clean worktree, correct branch and remote, actual START_SHA and frozen SHA reachability, post-freeze diffs limited to approved administrative documents, uv.lock HEAD/worktree Git blob matches `2b83110e86b26b7969fbddf8f98a727370ae19f7`, independently measured lock byte SHA-256, 198/199 and **approved new independent S11 record**, normal Trial state, P01 checkpoint and no P02 checkpoint. Do not discard user work, overwrite the prior stop report or mistake a historical S11 (193) for permission under revised WHAT.

P02 must not trust a forged `PrivacyDecision.allowed`; pass the typed decision to the same sink-owned publisher validate(manifest,*,privacy), check actual staged bytes/Study JCS hash/root FD EUID/inventory and injected-policy reauthorization before marker/rename, then secure atomic no-clobber/readback. Tests must include cross-run/hash/root/UID/changed-inventory and denied-policy cases. No scientific-negative forgery, row publication in G01, public schema drift, or independent acceptance bypass.

## 4. Owner decision requested

**`DEC-G01-P02-S11-REAUTH-01`:** authorize a **new separate limited G01-S11** for `G01/P01–P05` with **next execution P02/Trial01**, bound to immutable S10 `6df4b94de72a6ec8619f315e55ba7821e1eb157c`, branch `feature/ariadne_mvp_e11`, lock blob above, preserved P01 checkpoint `9bff61f0eae25236f95f31f2cd3e7c81291f0167`, and all prior mandatory G01/07/999 tests.

If Owner approves, record a distinct positive S11 authorization (201) **before** issuing a new current P02 Coding Agent handoff. Without it, P02 remains `BLOCKED_CODING_AUTHORIZATION`.

## 5. Five-layer instruction parity audit (Owner supplementary instruction)

Owner explicitly requires cross-layer alignment of `10_enhance_instruction/{GATE_ID}/06_*.md` and `07_*.md` against RD/21 LDD/22 BD/23 IF/30 DD, all under the stated ENH-E11 relative base. The G01 P01/P02-specific reconciliation records are 197 and 195/196; new Gate-wide trace / no-unapproved-postfreeze-change control is `combined_review/202_20261123_g01_06_07_five_layer_contract_concordance_protocol.md`. Current immutable source remains `6df4b94de72a6ec8619f315e55ba7821e1eb157c`; new normative discrepancies must be handled through 09/S10/S11 and not edited after freeze without Owner approval. This audit is not independent S09 PASS.

## 6. Owner approval disposition (later event; docket retained as original decision input)

**APPROVED:** Owner explicitly wrote `DEC-G01-P02-S11-REAUTH-01 を承認する` on 2026-11-23 JST. Positive authorization authority is `combined_review/201_20261123_g01_p02_revised_limited_s11_owner_authorization.md`; current P02/Trial01 execution handoff is `combined_review/203_20261123_g01_p02_trial01_restart_handoff_after_s11.md`. This section supersedes the docket's issuance-time `OWNER_DECISION_PENDING` heading only; historical text remains unchanged. Frozen WHAT SHA is still `6df4b94de72a6ec8619f315e55ba7821e1eb157c`. Actual runtime preflight and independent Gate acceptance remain outstanding.
