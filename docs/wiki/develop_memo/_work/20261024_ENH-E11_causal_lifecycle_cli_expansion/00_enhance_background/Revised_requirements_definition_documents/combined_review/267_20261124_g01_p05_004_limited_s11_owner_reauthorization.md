# 267 — G01/P05/Trial01 limited S11 Owner reauthorization against AMD-004 S10

**Date:** 2026-11-24 JST
**Decision ID:** DEC-G01-P05-004-S11-REAUTH-01
**State:** S11_OWNER_APPROVED / G01_P05_TRIAL01_LIMITED_CONTINUATION_AUTHORIZED / BOUNDED_PRODUCT_CLASSIFICATION_TEST_EXCEPTION_AUTHORIZED / G01_999_NOT_PASSED / DEFERRED_PRODUCT_POLICY_BRIDGE_UNFULFILLED
**Repository:** kousuke-ota-datascience/causal-atelier
**Branch:** feature/ariadne_mvp_e11
**Immutable active G01-S10:** 307404e01c43bb83a286986f8f6d124e53032509
**S10 decision:** DEC-G01-P05-004-S10-REFREEZE-01, combined_review/266
**Formal 09 decision:** DEC-G01-P05-004-FORMAL09-APPROVAL, combined_review/265
**Adopted audit:** combined_review/264
**Historical START_SHA:** 94758d3964eb92fb7df3619f7c5d31d8d996862e
**Superseded S11:** DEC-G01-P05-003-S11-REAUTH-01 (record 262)

## 1. Explicit Owner decision

> DEC-G01-P05-004-S11-REAUTH-01を承認する。AMD-E11-G01-P05-004に基づく新G01-S10凍結SHA 307404e01c43bb83a286986f8f6d124e53032509 を対象に、G01/P05/Trial01限定Coding Authorizationを再発行せよ。AMD-001/002/003の既承認契約およびP02限定例外を維持し、追加限定例外としてtests/product/test_enh_e4_g07_p03_cli_boundary.pyのCLI分類テストのみの修正を認可する。既存5つのLOW_LEVEL_UTILITYと新Local lifecycle CLIを明示的に区別し、全対象登録名と正規登録先を厳密に検証すること。他のテスト・既存Product実装・P01チェックポイント9bff61f0eae25236f95f31f2cd3e7c81291f0167、P02チェックポイント3a76a0aa1698037354b284ba7b5a875300473ce6、P03チェックポイント858c9f73366036a2d1445e558135cd521f611462、P04チェックポイント7dcf2061dae3c8832b2b3ec9be6900ad6ee7edb6、公開E11 Schema Version、科学的意味、独立科学検証・G01_999受入条件、DEFERRED_PRODUCT_POLICY_BRIDGE未完了依存を維持する。Coding Agentの未コミット実装・テスト・状態報告を復元可能な形で保全し、破壊的操作を行わず同期・継続実行すること。歴史的START_SHAとRESUME_BASE_SHAを区別すること。S11承認記録をGitHubへ反映せよ。

**Disposition:** Issue limited continuation authorization solely for GATE_ID=G01 / PACKAGE_ID=P05 / TRIAL_NO=01 against the exact immutable S10 above. Preserve existing uncommitted work; do not restart from scratch. No unrelated Package or Gate authorization or independent acceptance waiver.

## 2. Verified pre-record Git state

Remote HEAD before issuance was 4a3d70238ea774d3d558fcedabe1f51858b6736b. Read S10 record 266 and confirmed frozen SHA and scope. Comparison from frozen S10 returned ahead 1 / behind 0, only record 266 added. Comparison from historical START_SHA returned ahead 8 / behind 0, only seven documentation paths changed: records 263–266, P05 06, G01 07, AMD-004 09. No source, test, lockfile or implementation report change in that remote comparison.

| Protected checkpoint | SHA | Comparison to pre-record HEAD |
| --- | --- | --- |
| P01 | 9bff61f0eae25236f95f31f2cd3e7c81291f0167 | ancestor; ahead 123 / behind 0 |
| P02 | 3a76a0aa1698037354b284ba7b5a875300473ce6 | ancestor; ahead 98 / behind 0 |
| P03 | 858c9f73366036a2d1445e558135cd521f611462 | ancestor; ahead 88 / behind 0 |
| P04 | 7dcf2061dae3c8832b2b3ec9be6900ad6ee7edb6 | ancestor; ahead 46 / behind 0 |

These are Git checks, not verification of the Agent's local work or executable behavior.

## 3. Authorized scope

Retain AMD-001 Manifest Factory, AMD-002 publication failure boundaries and AMD-003 independent session identity/issuance and exact bounded P02 source exception. That exception remains confined to PublicationSessionToken and Port begin/abort in src/ariadne/capabilities/causal/ports/local_io.py; necessary imports, optional constructor issuer/session and private initialization, Adapter begin/abort in src/ariadne/interfaces/cli/local_causal/publication.py. Preserve concrete Publisher begin/stage_bytes/validate/commit/abort algorithms and Adapter seal/publish. No other completed-Package source/test/instruction changes.

AMD-004 adds only permission to edit or rename test_all_analysis_cli_scripts_are_explicitly_low_level_utilities in tests/product/test_enh_e4_g07_p03_cli_boundary.py. Explicit expected mappings may be local to that function. Preserve original LOW_LEVEL_UTILITY constant, all helpers, the other two tests, all other protected tests and existing Product production code.

| Classification | Name | Exact target |
| --- | --- | --- |
| Legacy low-level | ariadne-discover | ariadne.interfaces.cli.discovery:main |
| Legacy low-level | ariadne-estimate | ariadne.interfaces.cli.estimation:main |
| Legacy low-level | ariadne-identify | ariadne.interfaces.cli.identification:main |
| Legacy low-level | ariadne-refute | ariadne.interfaces.cli.refutation:main |
| Legacy low-level | ariadne-sensitivity | ariadne.interfaces.cli.sensitivity:main |
| Local lifecycle | ariadne-causal-local | ariadne.interfaces.cli.local_causal.command:main |

Assert legacy names equal LOW_LEVEL_UTILITY and both classifications are disjoint. Compare the full mapping of project.scripts targets beginning ariadne.interfaces.cli. to the six fixed mappings. Reject missing, renamed, redirected (including outside prefix) or extra in-prefix registrations. No dynamic expected map, prefix exclusion, skip/xfail or wrapper. No change to approved entrypoint registration or unrelated production code to satisfy the test.

## 4. Non-destructive resume

Use 40_operator_workflows/agent_entry_prompts/10_normal_execution_02_work_package_coding_agent_prompt.md with G01/P05/01, applying the AMD-004 continuation rules as the specific exception to a fresh clean-start preflight.

Before synchronization, inventory tracked/staged/untracked changes including the P05 status report and make a verified recoverable copy of all work. Author has not accessed or backed up that local work. Do not reset --hard, clean, discard or overwrite local changes. Use a clean separate baseline or verified reversible preservation workflow to reconcile remote documentation-only commits. Verify historical START_SHA ancestry, exact frozen S10 ancestry, exact administrative-only post-freeze changes 266/267 and prior checkpoint/lockfile invariants. Record actual synchronized RESUME_BASE_SHA separately from historical START_SHA; expected resume baseline is the commit recording this authorization if no further remote changes occur. Verify restored local diff against prior inventory and authorized scope, and reconcile status report without losing previous evidence. Stop on conflict or unexpected change requiring Owner decision. No blind replay or fresh implementation from scratch.

## 5. Verification and completion

Rerun affected Product test file, P05 focused tests and full required G01/Product regression suites. Record actual commands, exit codes, counts, warnings, environment and candidate identities. At minimum rerun the previously reported commands:
- .venv/bin/python -m pytest -q tests/product/test_enh_e4_g07_p03_cli_boundary.py
- .venv/bin/python -m pytest -q tests/enhancement/enh_e11/g01/integration/test_local_cli.py
- .venv/bin/python -m pytest -q tests/enhancement/enh_e11/g01 tests/product/test_cli_contract.py tests/product/test_enh_e4_g07_p03_cli_boundary.py tests/product/test_enh_e4_g04_result_artifact_contract.py tests/product/test_domain_and_snapshot.py

Prior Agent-reported 19 focused passes and 225 pass/1 fail are historical evidence. No fresh pytest or independent PASS is asserted. Verify protected-test source diff and all existing package completion criteria; independent negative controls remain mandatory under 07. Create official status/checkpoint records, commit and push only after actual authorized Package completion. If blocked, retain recoverable work and report precise cause.

Preserve public E11 Schema Versions, scientific meaning, privacy, no-clobber, independent Reader, Product behavior, uv.lock, physical FS/science verification, T2/T3 and independent G01_999 acceptance. DEFERRED_PRODUCT_POLICY_BRIDGE remains UNFULFILLED; no waiver. This S11 record does not alter the immutable frozen SHA, create a P05 checkpoint, perform local implementation or confer independent acceptance.
