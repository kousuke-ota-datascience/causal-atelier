# 268 — G01/Trial01 Candidate Assembly freeze authority Owner decision

**Date:** 2026-11-24 JST
**Decision ID:** DEC-G01-ASSEMBLY-FREEZE-AUTHORITY-01
**State:** OWNER_APPROVED_ASSEMBLY_FREEZE_AUTHORITY / ASSEMBLY_PREFLIGHT_RETRY_AUTHORIZED / CANDIDATE_NOT_FIXED / G01_999_NOT_PASSED
**Repository:** kousuke-ota-datascience/causal-atelier
**Branch:** feature/ariadne_mvp_e11
**Scope:** G01 / Trial01 / Candidate Assembly only
**Pre-record HEAD:** 0fca54747758cf0e02e5a48d8227e6c8759981fe
**Immutable S10:** 307404e01c43bb83a286986f8f6d124e53032509
**S10 authority:** DEC-G01-P05-004-S10-REFREEZE-01, combined_review/266
**Latest S11:** DEC-G01-P05-004-S11-REAUTH-01, combined_review/267, commit 7c15920ab46c46b3a084432736c2c32fbb087e92

## 1. Explicit Owner decision

> DEC-G01-ASSEMBLY-FREEZE-AUTHORITY-01はA案を採用する。G01/Trial01に限り、正式Owner S10承認記録266および凍結SHA 307404e01c43bb83a286986f8f6d124e53032509 をCandidate AssemblyのContract status: FROZEN条件を満たすAuthorityとする。Gate 06の旧状態表示は承認前の歴史的表示として扱う。Execution ModeおよびRequired packagesは引き続き正本Gate 06から解決する。既存S10/S11承認、AMD-001〜004、P01〜P05チェックポイント、実装契約、科学的意味、独立G01_999受入条件およびDEFERRED_PRODUCT_POLICY_BRIDGE未完了依存を維持する。本決定をGitHubに記録し、Candidate Assembly Agentへの再実行指示を提示せよ。他Gateの承認手順は変更しない。

## 2. Specific authority resolution

For this Assembly only, override the literal Gate 06 Contract status: FROZEN check in section 4 (v0.04 Candidate Assembly authority) of 40_operator_workflows/agent_entry_prompts/20_candidate_assembly_01_work_package_candidate_assembly_agent_prompt.md and the related stale-DRAFT stop in its S02 preflight, solely insofar as the historical status display conflicts with verified Owner S10/S11 records. The effective freeze condition is satisfied by record 266 and its exact frozen SHA after verifying their identity, ancestry and contract integrity. The Gate 06 DRAFT / NOT_FROZEN / CODING_NOT_AUTHORIZED text is historical, not a new denial. This is not permission to ignore a real missing approval, changed contract, SHA mismatch or other blocker.

Resolve exactly one canonical Gate 06, Execution Mode WORK_PACKAGE and Required packages P01,P02,P03,P04,P05 from it. Verify effective S10/S11 and amendment history AMD-001–004, including bounded exceptions. No new S10/S11, no coding authorization expansion, no amendment to frozen WHAT, no shared Prompt edit and no change for any other Gate or Trial.

## 3. Verified pre-record remote state

Remote HEAD matched 0fca54747758cf0e02e5a48d8227e6c8759981fe. S10 and latest S11 are ancestors (ahead 4 and 2 respectively, behind 0). Each canonical status report identifies G01/Trial01, the corresponding Package and PACKAGE_COMPLETE with the following implementation checkpoint; all are ancestors of pre-record HEAD.

| Package | Checkpoint | Ahead / behind |
| --- | --- | --- |
| P01 | 9bff61f0eae25236f95f31f2cd3e7c81291f0167 | 126 / 0 |
| P02 | 3a76a0aa1698037354b284ba7b5a875300473ce6 | 101 / 0 |
| P03 | 858c9f73366036a2d1445e558135cd521f611462 | 91 / 0 |
| P04 | 7dcf2061dae3c8832b2b3ec9be6900ad6ee7edb6 | 49 / 0 |
| P05 | 72bcd6acaab6caf48827bf2bb6cd5e249afd658b | 1 / 0 |

P05 checkpoint to pre-record HEAD changes only four evidence files: Gate implementation report detail, Trial progress report, P05 status and P05 checkpoint report. P05 reports 3 affected Product tests, 19 focused tests and 226 combined regression tests passed, plus five negative controls rejected. These are historical reported results, not new Assembly execution or independent verification.

## 4. Resume instructions and retained gates

Synchronize non-destructively, verify clean worktree and actual full HEAD, exact approved S10 ancestry, S11 history, all Package evidence and checkpoint ancestry, actual source/contract/lockfile integrity and authorized delta. Verify the only change after pre-record HEAD is this administrative decision (if any further changes, assess before proceeding). Preserve all previous checkpoints and evidence. Do not reimplement Packages or silently change source/contracts to pass Assembly.

Execute all remaining original Candidate Assembly requirements including Gate-wide integration/regression and impact/scope verification. Fix the candidate identity only after required checks, record actual full Fixed Trial Candidate SHA and canonical Gate-level Implementation Completion Report and READY_FOR_TEST only when warranted. Distinguish candidate SHA from subsequent evidence-record commit. Record actual commands/results, commit and push per original workflow. If blocked, report the precise unmet condition. Do not declare Gate PASS or independent scientific PASS.

Preserve independent S09, B02/B04, B05, physical FS/Reader, T2/T3, independent 07 and G01_999 acceptance obligations under DEC-G01-EXEC-01. DEFERRED_PRODUCT_POLICY_BRIDGE remains UNFULFILLED and its acceptance dependency is not waived. No new test execution, fixed candidate, READY_FOR_TEST or independent acceptance asserted by this Owner record.
