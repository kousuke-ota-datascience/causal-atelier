# 203 — G01/P02 Trial01 executable Coding Agent restart handoff after revised S11

**Date:** 2026-11-23 JST  
**Status:** `P02_TRIAL01_CODING_AUTHORIZED / ACTUAL_RUNTIME_PREFLIGHT_PENDING`  
**Repo:** `kousuke-ota-datascience/causal-atelier`  
**Branch:** `feature/ariadne_mvp_e11`  
**Frozen G01-S10 normative source:** `6df4b94de72a6ec8619f315e55ba7821e1eb157c`  
**Current separate Owner S11 record:** `combined_review/201_20261123_g01_p02_revised_limited_s11_owner_authorization.md` (Git commit `483f014506c2d1bee8f6f7b94ef2e12c9ae830db`)  
**Formal 09 approval:** `198`  
**Revised S10 record:** `199`  
**S11 decision docket:** `200`; RD/LDD/BD/IF/DD-to-06/07 parity audit: `202`  
**Prior P01 dependency checkpoint:** `9bff61f0eae25236f95f31f2cd3e7c81291f0167`, existing PACKAGE_READY  
**P02 checkpoint:** NONE; no P02 code, official P02 package status or actual Linux FS tests yet  
**Approved lock blob:** `2b83110e86b26b7969fbddf8f98a727370ae19f7`  
**Previous Agent-observed uv.lock byte sha256 (must remeasure):** `1d92a472fc3c750c90458a40ae5a09ba3feefbd3d99eee61b0cdbff00d31cffb`

## 1. Exact Work Package Agent invocation

```text
以下の実行時変数で、下記の既存Work Package Coding Agent Promptを実行せよ。

GATE_ID=G01
PACKAGE_ID=P02
TRIAL_NO=01

実行対象:
docs/wiki/develop_memo/_work/20261024_ENH-E11_causal_lifecycle_cli_expansion/40_operator_workflows/agent_entry_prompts/10_normal_execution_02_work_package_coding_agent_prompt.md

対象リポジトリ:
kousuke-ota-datascience/causal-atelier
作業ブランチ:
feature/ariadne_mvp_e11

改訂後の暫定G01-S10凍結WHAT完全Git SHA:
6df4b94de72a6ec8619f315e55ba7821e1eb157c

承認記録（上記base配下）:
00_enhance_background/Revised_requirements_definition_documents/combined_review/198_20261123_g01_p02_formal_09_owner_approved.md
00_enhance_background/Revised_requirements_definition_documents/combined_review/199_20261123_g01_p02_revised_provisional_s10_owner_refreeze.md
00_enhance_background/Revised_requirements_definition_documents/combined_review/201_20261123_g01_p02_revised_limited_s11_owner_authorization.md

再開ハンドオフ:
00_enhance_background/Revised_requirements_definition_documents/combined_review/203_20261123_g01_p02_trial01_restart_handoff_after_s11.md

依存P01 PACKAGE_READYチェックポイント:
9bff61f0eae25236f95f31f2cd3e7c81291f0167

まずremote/branch、clean worktree、START_SHA、凍結WHAT以降の差分、
uv.lockのGit blobと実ファイルSHA256、Trial状態、
P01 PACKAGE_READYとP02未チェックポイントを実環境で確認せよ。
凍結後の差分は198/199/200/201/202/203/80の
Owner承認・監査・運用管理文書のみ許す。
初期状態が満たせなければBLOCKEDとして停止し、推測で修復しないこと。

実行契約は凍結SHA時点のG01/P02 06、
関連P05 06、G01 07、および5階層の上位要件・設計文書に従うこと。
過去のP02停止報告を保持し、P01は再実装しない。
G01/P02/Trial01の実装・focused verification・
実Linux FS検証・Package checkpoint/reportを実施せよ。
独立Science PASSやG01_999 PASSを自己宣言しないこと。
```

## 2. Exact relative base and cross-layer source

Base is `docs/wiki/develop_memo/_work/20261024_ENH-E11_causal_lifecycle_cli_expansion/`.

- Stock design source: `00_enhance_background/Revised_requirements_definition_documents/{10_requirements_definition,21_logical_data_design,22_product_basic_design,23_api_interface_design,30_detailed_design}/`
- Assigned P02: `10_enhance_instruction/G01/06_G01_P02_atomic_publication_reader.md`
- P05 cross-contract: `10_enhance_instruction/G01/06_G01_P05_cli_use_case_privacy.md`
- G01 07: `10_enhance_instruction/G01/07_Ariadne_ENH-E11_G01_test_instruction.md`
- Formal amendment: `10_enhance_instruction/G01/09_ENH-E11_G01_AMD-E11-G01-P02-001_Gate_Contract_Amendment.md`
- Gate-level 06 and Package P00 plan remain frozen at `6df4b94de72a6ec8619f315e55ba7821e1eb157c`.

In any conflict, stop and report exact file/section/blob; do not silently select a weaker source or edit frozen WHAT. S11 permits P02 implementation and developer tests **only within** frozen contract and existing G01 P00 dependency graph.

## 3. P02 critical implementation contract

- P01's immutable Study/ContentRef/JCS/Manifest values are pre-existing and must not be reimplemented; P02 owns physical FD/root and actual-byte verification plus local atomic Publisher/Reader.
- P05 authorizes the declared `DISCOVER_AGGREGATE_ONLY` output shape before staging, using current Study/TrustedRoot/Principal. The same immutable decision passes through `LocalPublicationPort.seal(*,sink,manifest,privacy)` to the sink-owned Publisher's `validate(manifest,*,privacy)`; Publisher **recomputes** policy from actual staged Study, real inventory and live root/UID and compares it to the supplied decision. Merely `allowed=True` is not sufficient.
- Deny wrong run/hash/Root FD even if path text equal/UID/Study/inventory, policy disagreement, missing/denied/forged decision and any G01 row artifact **before** Marker/rename; no misleading `COMPLETED` or SCI-negative status.
- Real Linux same-FS secure no-clobber renameat2, owner/mode, symlink/race, staging FD, fsync/Reader verification and indeterminate post-rename behavior are required. No file overwrite or unsafe cleanup.
- No G01 individual-row export, no G02–G10/legacy Product ABI modification, no invented P04 genuine science-negative proof.

## 4. Tests and status

P02 focused secure Root/FD/ContentRef, PrivacyDecision negative/positive, staged Inventory, process concurrency/no-clobber, fsync and independent Reader. Preserve P01 76 developer tests and Product v2 regressions. Record *actual* verification commands, output, test counts, failed cases, limitations and the implementation full SHA in P02 Package report; only create a checkpoint when factual P02 developer readiness is established. No independent G01_999 claim or made-up FS evidence.

Before Coding Agent execution, no local environment/worktree status is asserted here. The prior pre-code P02 `BLOCKED_CONTRACT_AMBIGUITY` then `BLOCKED_CODING_AUTHORIZATION` remain history; neither is a formal Gate FAIL/08 requiring Trial02.

## 5. Final authorization boundary

This handoff depends on Owner `DEC-G01-P02-S11-REAUTH-01` recorded in 201, *not* historical 193. The immutable frozen WHAT is `6df4b94de72a6ec8619f315e55ba7821e1eb157c`, **not the later Git HEAD used for administrative records**. A new contract defect requires Owner 09/new S10/separate S11 again. Independent B02–B05/S09/T2/T3/07/G01_999 and all Product v2 regression remain separate, unwaived acceptance.
