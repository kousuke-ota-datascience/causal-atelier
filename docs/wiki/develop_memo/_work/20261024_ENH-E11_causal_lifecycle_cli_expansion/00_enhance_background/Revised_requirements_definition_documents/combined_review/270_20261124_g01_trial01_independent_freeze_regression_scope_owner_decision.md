# 270 — G01/Trial01 independent verification freeze authority and regression scope Owner decisions

**Date:** 2026-11-24 JST
**Decision IDs:** DEC-G01-INDEPENDENT-FREEZE-AUTHORITY-01; DEC-G01-INDEPENDENT-REGRESSION-SCOPE-01
**State:** OWNER_APPROVED_INDEPENDENT_PREFLIGHT_RETRY / FIXED_CANDIDATE_UNCHANGED / INDEPENDENT_TEST_NOT_RUN / PROMOTION_NOT_ALLOWED
**Scope:** G01 / Trial01 / independent verification only; no automatic application to other Gates or Trials
**Repository:** kousuke-ota-datascience/causal-atelier
**Branch:** feature/ariadne_mvp_e11
**Pre-record HEAD / historical TEST_START_SHA:** d0fc571c48d2dc3bf02e70ea4786d10db5394aa3
**Immutable S10:** 307404e01c43bb83a286986f8f6d124e53032509
**S10 authority:** DEC-G01-P05-004-S10-REFREEZE-01, record 266
**Latest S11:** DEC-G01-P05-004-S11-REAUTH-01, record 267, commit 7c15920ab46c46b3a084432736c2c32fbb087e92
**Fixed Trial Candidate:** 72bcd6acaab6caf48827bf2bb6cd5e249afd658b
**Pre-P01 comparison baseline:** ff38f2248ed5b6355a0c61ce9a3f575b6db21305

## 1. Explicit Owner decision

> DEC-G01-INDEPENDENT-FREEZE-AUTHORITY-01およびDEC-G01-INDEPENDENT-REGRESSION-SCOPE-01を承認する。G01/Trial01の独立検証に限り、正式S10承認記録266と凍結SHA 307404e01c43bb83a286986f8f6d124e53032509 を凍結状態のAuthorityとし、Gate 07の旧状態表示を承認前の歴史的表示として扱う。Fixed Trial Candidate SHA 72bcd6acaab6caf48827bf2bb6cd5e249afd658b を独立検証対象とし、Test Item 001から実行する。記録269の既存FAIL・変更影響範囲の判定方法を独立検証にも適用するが、Assembly結果の転記によるPASSは禁止し、Baseline同一FAIL、依存宣言不変、未承認因果Runtime依存の不存在、Frontend変更影響閉包外を独立に再確認すること。既存FAILおよび対象外テストをPASS扱いせず、技術的負債を維持する。既存S10/S11、AMD-001〜004、P01〜P05チェックポイント、独立S09、B02/B04、B05、実FS/Reader、T2/T3、Gate 07およびG01_999受入条件、DEFERRED_PRODUCT_POLICY_BRIDGE未完了依存を維持する。本決定をGitHubに記録し、Independent Test Agentへの再実行指示を提示せよ。他Gateへ自動適用しない。

## 2. Independent freeze authority

Apply this specific decision to the S02 preflight in 40_operator_workflows/agent_entry_prompts/30_independent_verification_01_test_agent_prompt.md (line 488 at pre-record HEAD) and any equivalent stale status-display check within that prompt. For G01/Trial01 only, the effective freeze condition is satisfied by verified record 266 and exact S10 SHA, not by the historical Gate 07 text DRAFT / NOT_FROZEN / TESTS_NOT_RUN. Historical statements of unapproved status in the frozen document/prompt do not override subsequent actual Owner decisions. TESTS_NOT_RUN remains factually true at this decision time. Do not rewrite Gate 07, freeze a new SHA or infer S09/Science PASS. Verify S10/S11 and full authorization chain, AMD-001–004, canonical Gate 07, fixed candidate and official READY_FOR_TEST Completion Report. A genuine missing approval, inconsistent identity or contract change remains a blocker.

This extends only the status-resolution method of Assembly record 268 to independent verification. It does not extend coding rights or permit changes to product/test code, dependencies, frozen AC or shared prompts.

## 3. Verified remote state before issuance

Remote HEAD matched d0fc571c48d2dc3bf02e70ea4786d10db5394aa3. S10 -> latest S11 comparison ahead 2/behind 0 (records 266/267 only); latest S11 -> fixed candidate ahead 1/behind 0 (11 implementation/test paths under P05); fixed candidate -> pre-record HEAD ahead 4/behind 0 (seven documentation paths only: records 268/269, Gate report detail, Trial progress, P05 status/checkpoint and Completion Report).

Gate 07 blob 6af42b17a403756b237c1b4c4a546bff4ef11381 identical at S10, fixed candidate and pre-record HEAD. Canonical Completion Report 20_implementation_reports/G01/Trial01/E11-G01_01__implementation_completion.md identifies G01/Trial01, WORK_PACKAGE, READY_FOR_TEST and the exact fixed candidate above. Assembly reported 268 passed / 0 failed / 2 deselected / 11 warnings for selected required set; these are historical coding-side evidence, not independent results. Author has not run Test Item 001 or independent tests.

Preserved Package checkpoint identities: P01 9bff61f0eae25236f95f31f2cd3e7c81291f0167; P02 3a76a0aa1698037354b284ba7b5a875300473ce6; P03 858c9f73366036a2d1445e558135cd521f611462; P04 7dcf2061dae3c8832b2b3ec9be6900ad6ee7edb6; P05 72bcd6acaab6caf48827bf2bb6cd5e249afd658b.

## 4. Independent regression disposition

Apply the methods and conditions of record 269 sections 3–4 to independent G01/Trial01 regression verification, not its Assembly outcomes. Independently reconstruct and record the evidence from the fixed candidate and pre-P01 baseline in comparable environments.

Only test_no_prohibited_causal_runtime_dependency_is_declared in tests/product/test_enh_e5_g03_p03_causal_runtime_regression.py may receive PRE_EXISTING_FAILURE, after independently reproducing the same LightGBM assertion on both baseline and candidate, comparing structured TOML dependency declarations/groups/extras and lock identity, separately executing the original source import checks for lightgbm/dowhy/econml that the failed assertion prevented, and verifying no unauthorized causal-runtime dependency additions across changed modules/reachable closure, including relevant lazy/dynamic imports and provider boundaries. Preserve raw FAIL; not PASS. TD-G01-LEGACY-DEPENDENCY-GUARD-01 remains OPEN. No source/test edit, skip/xfail, dependency removal or general waiver. New violations or unknown impact cannot receive inherited disposition.

Only test_navigation_route_change_has_no_execution_revision_metadata in that file may receive OUT_OF_SCOPE_FOR_G01 after independently verifying unchanged frontend inputs, test and relevant dependency/impact closure. Preserve previous missing-node failure as history; not PASS. If impact is uncertain, execute in a valid environment or BLOCK. Do not exclude the whole file; causal runtime operation stage/input matrix remains required. Explicit node-ID deselection from the required-pass run of these two cases alone is permitted after their respective conditions and dispositions are established and documented. Dependency test is separately executed on baseline and candidate. Other applicable G01, Scientific Core and Product regressions require actual independent PASS. Do not label the whole suite unconditionally PASS.

## 5. Retry execution and decision boundary

Synchronize cleanly and confirm the new actual TEST_START_SHA; preserve historical stopped TEST_START_SHA separately. Verify only this administrative record was added after pre-record HEAD (if any further changes, audit before proceeding), and candidate-to-current changes are approved documentation only. Read current Owner decisions and Completion Report from the synchronized branch, but execute product/test verification against the exact fixed candidate using the original prompt's checkout/identity rules. Do not confuse administrative/evidence HEAD with tested candidate. Record source, test/fixture, lock, environment and actual commands/exit/results. Confirm protected checkpoints and effective frozen contract. Begin formal Test Item 001 candidate identity audit; only after its requirements pass proceed to 002–013 under Gate 07, with independent evidence and correct PASS/FAIL/BLOCKED classifications. No invented results; no transfer of Assembly PASS. Follow original evidence report/commit/push and 999 decision procedure.

All mandatory independent S09, B02/B04, B05, real FS/Reader, T2/T3, Gate 07 and G01_999 obligations remain intact. DEC-G01-EXEC-01 permits independent evidence to be collected after coding, not waived. Keep non-null BK fail-closed before FCI until independently verified remedy; no fabricated scientific PASS. DEFERRED_PRODUCT_POLICY_BRIDGE remains UNFULFILLED and a final acceptance dependency. Distinguish prerequisite/environment blockers from demonstrated product violations per 07/999; no Gate PASS if mandatory obligations remain unmet. Promotion remains prohibited unless actual acceptance conditions are satisfied.

No change to S10/S11, fixed candidate, implementation, tests, frozen documents or shared prompts; no new AMD, Assembly, coding execution, independent test execution or Gate decision by this record.
