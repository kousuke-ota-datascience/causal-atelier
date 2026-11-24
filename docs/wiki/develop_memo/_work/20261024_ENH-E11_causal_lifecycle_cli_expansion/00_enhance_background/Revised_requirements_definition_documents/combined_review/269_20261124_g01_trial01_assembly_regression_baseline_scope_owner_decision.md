# 269 — G01/Trial01 Candidate Assembly regression baseline and scope Owner decisions

**Date:** 2026-11-24 JST
**Decision IDs:** DEC-G01-ASSEMBLY-REGRESSION-BASELINE-01; DEC-G01-ASSEMBLY-REGRESSION-SCOPE-01
**State:** OWNER_APPROVED_CONDITIONAL_BASELINE_DISPOSITION_AND_SCOPE / ASSEMBLY_RETRY_AUTHORIZED / CANDIDATE_NOT_FIXED / G01_999_NOT_PASSED
**Scope:** G01 / Trial01 only; no automatic application to other Gates or Trials
**Repository:** kousuke-ota-datascience/causal-atelier
**Branch:** feature/ariadne_mvp_e11
**Pre-record HEAD:** b05be3106341de38ecfe70a3dd58269768078c50
**Pre-P01 comparison baseline:** ff38f2248ed5b6355a0c61ce9a3f575b6db21305
**Immutable S10:** 307404e01c43bb83a286986f8f6d124e53032509
**Latest S11 record:** 7c15920ab46c46b3a084432736c2c32fbb087e92
**Prior Assembly freeze authority:** DEC-G01-ASSEMBLY-FREEZE-AUTHORITY-01, record 268

## 1. Explicit Owner decision

> DEC-G01-ASSEMBLY-REGRESSION-BASELINE-01およびDEC-G01-ASSEMBLY-REGRESSION-SCOPE-01を承認する。G01/Trial01に限り、既存LightGBM依存宣言テストのFAILを、Baselineでの同一FAIL再現、依存宣言の意味的不変性、未承認因果Runtime依存の追加がないことを確認した上でPRE_EXISTING_FAILUREとして記録し、ENH-E11による新規回帰と区別する。既存テストは変更・skip・xfailせず、技術的負債として追跡する。Frontendナビゲーションテストは変更影響閉包外であることを根拠にOUT_OF_SCOPE_FOR_G01とし、PASS扱いしない。他の関連Scientific Core・Product回帰は実測PASSを要求する。既存S10/S11、AMD-001〜004、P01〜P05チェックポイント、独立科学検証・G01_999受入条件およびDEFERRED_PRODUCT_POLICY_BRIDGE未完了依存を維持する。本決定をGitHubに記録し、Candidate Assembly Agentへの再実行指示を提示せよ。他Gateには自動適用しない。

## 2. Evidence at decision time

Remote HEAD matched the reported stopped Assembly HEAD. Record 268 was read back. P05 checkpoint to that HEAD differs only in four implementation evidence files and record 268.

Author compared pre-P01 baseline and stopped HEAD via repository reads:
- pyproject.toml: baseline blob 7c24ed729be1a31c15a173ef4510aa3ed961d0b9; current 85d7609116615f6de96258ba1594d3c53a1f5f3c. Removing the single approved ariadne-causal-local script line from current text gives exact baseline text.
- uv.lock: identical blob 2b83110e86b26b7969fbddf8f98a727370ae19f7.
- tests/product/test_enh_e5_g03_p03_causal_runtime_regression.py: identical blob 390196f5c77d8dde7481b7169f9334962c6113be.
- frontend/navigation_state.js: identical blob 66bfddd9c4a1db137a1bcb369025093ab5758.
- frontend/app.js: identical blob a75091db134d236bb6e4067ab9daaa0b4916da82.

The dependency test reads the entire TOML as lowercase text and checks lightgbm/dowhy/econml absence before its causal-source checks. LightGBM was added in predictive-advanced by ENH-E10 commit 488ba81d5d8d6177f0f0ac80b9dc43364fc32a06, before ENH-E11. Assembly Agent reports reproducing the same assertion on pre-P01 files. The navigation test runs node -e against the two frontend files and failed with FileNotFoundError; its behavior was not evaluated. Author has not executed these tests.

Reported historical results: 226 passed; expanded selection 268 passed / 2 failed; 11 fork warnings; baseline dependency reproduction 1 failed. Preserve these raw results.

## 3. Conditional PRE_EXISTING_FAILURE disposition

Only test_no_prohibited_causal_runtime_dependency_is_declared in tests/product/test_enh_e5_g03_p03_causal_runtime_regression.py qualifies, and only after verifying same failure on baseline and current candidate with comparable environment and full recorded assertion details; structured TOML dependency equality (all dependency declarations/groups/extras unchanged), lock identity and no unauthorized causal runtime dependency additions.

Because the original assertion stops before the source import checks, separately execute the original source checks for all three prohibited names and inspect the ENH-E11 changed causal runtime paths and their reachable dependency closure, including new subpackages, lazy/dynamic imports and provider boundaries as relevant. Verify no unauthorized runtime dependency additions, distinguish approved optional provider contracts from actual runtime reachability, and record actual evidence. A same first assertion is not proof that later invariants hold. If a new violation or unresolved impact exists, BLOCK rather than classify it as inherited.

Record raw FAIL and separate PRE_EXISTING_FAILURE disposition, not PASS. No modification, skip, xfail, dependency removal or broad waiver. Track debt TD-G01-LEGACY-DEPENDENCY-GUARD-01 in the Assembly report and this record: owner follow-up required to reconcile legacy project-wide string guard with predictive optional-dependency scope in separately authorized maintenance; OPEN, not resolved here.

## 4. OUT_OF_SCOPE_FOR_G01 disposition

Only test_navigation_route_change_has_no_execution_revision_metadata in the same test file may be excluded from required G01 execution, after verifying its frontend inputs, test and relevant dependency/impact closure remain unchanged. No frontend changes in the ENH-E11 comparison; direct test inputs have identical blobs as above. Record previous missing-node error and OUT_OF_SCOPE_FOR_G01, never PASS. No Node installation required solely for this excluded test. If impact changes or is uncertain, execute in a valid Node environment or BLOCK. Do not exclude the entire file: causal runtime operation stage/input matrix remains required.

## 5. Assembly retry and evidence

Synchronize cleanly and verify exact actual HEAD, only record 269 added after pre-record HEAD, S10/S11 ancestry, record 268, AMD-001–004, approved source/test delta, uv.lock physical hash, P01–P05 status and checkpoint ancestry. Preserve checkpoints P01 9bff61f0eae25236f95f31f2cd3e7c81291f0167; P02 3a76a0aa1698037354b284ba7b5a875300473ce6; P03 858c9f73366036a2d1445e558135cd521f611462; P04 7dcf2061dae3c8832b2b3ec9be6900ad6ee7edb6; P05 72bcd6acaab6caf48827bf2bb6cd5e249afd658b.

Run all other required G01, Scientific Core and impacted Product tests against the actual fixed candidate source. Explicit node-ID deselection of these two named cases from the required-pass run is permitted only as a transparent separate selection after recording their actual raw outcomes and satisfying sections 3–4; it is not skip/xfail or editing tests. The dependency test must be run separately on baseline and candidate. Report selection, raw results, separate dispositions, actual commands and exit codes; do not report a clean full-suite PASS. If all applicable requirements are met, continue original Assembly workflow, fix candidate SHA, issue canonical completion report and READY_FOR_TEST and commit/push evidence. If any remaining requirement fails or is unknown, stop.

## 6. Retained obligations

No modification to frozen 06/07, shared prompts, production source, tests, pyproject.toml or uv.lock by this decision. No new S10/S11 or AMD. Preserve all independent S09, B02/B04, B05, real FS/Reader, T2/T3, independent 07 and G01_999 acceptance obligations; the Assembly dispositions are not independent acceptance or automatic waiver for later stages. DEFERRED_PRODUCT_POLICY_BRIDGE remains UNFULFILLED. No actual Assembly execution, fixed candidate or READY_FOR_TEST asserted by this record.
