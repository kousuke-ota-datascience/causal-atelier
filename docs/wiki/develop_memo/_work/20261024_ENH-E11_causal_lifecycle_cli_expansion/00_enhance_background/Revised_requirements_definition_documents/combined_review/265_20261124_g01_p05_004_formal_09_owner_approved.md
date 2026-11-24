# 265 — G01/P05 AMD-E11-G01-P05-004 formal 09 Owner approval

**Date:** 2026-11-24 JST
**Decision ID:** DEC-G01-P05-004-FORMAL09-APPROVAL
**State:** FORMAL_09_OWNER_APPROVED / S10_REFREEZE_PENDING / S11_REAUTH_PENDING / P05_BLOCKED_UNDER_AMD004
**Branch:** feature/ariadne_mvp_e11
**Approved amendment:** AMD-E11-G01-P05-004
**Adopted static audit:** combined_review/264
**Design decision:** DEC-G01-P05-CLI-CLASSIFICATION-01=A (combined_review/263)
**Pre-record HEAD:** d0083f55f5cb1bbd30548be1b87d4f27fb92c4fe
**Historical Agent START_SHA:** 94758d3964eb92fb7df3619f7c5d31d8d996862e
**Current immutable S10 (unchanged):** 47ecfe33f3daf91da8c589db589b21f628e4e23b

## 1. Explicit Owner decision

> DEC-G01-P05-004-FORMAL09-APPROVALを承認する。AMD-E11-G01-P05-004を正式09として承認し、combined_review/264の静的整合性監査結果を採用する。既存Product回帰テストへの追加限定例外はtests/product/test_enh_e4_g07_p03_cli_boundary.pyのCLI分類テストのみとする。既存5つのLOW_LEVEL_UTILITYと新Local lifecycle CLIを明示的に区別し、全対象登録名と正規登録先を厳密に検証すること。他のテスト・既存Product実装・AMD-001/002/003の既承認契約・P01〜P04チェックポイント・公開E11 Schema Version・科学的意味・独立G01_999受入条件・DEFERRED_PRODUCT_POLICY_BRIDGE未完了依存を維持する。Coding Agentの未コミット実装を保全する。正式09承認記録をGitHubへ反映し、S10再凍結用の完全Git SHAを提示せよ。S10再凍結とS11再認可は別決裁とする。

AMD-004 is formally approved. Audit 264 is adopted as Author static evidence, not executable or independent verification. AMD-004 modifies only the protected CLI classification test exception and associated acceptance; AMD-001/002/003 remain binding.

## 2. Verified approval input

Remote HEAD before issuance matched d0083f55f5cb1bbd30548be1b87d4f27fb92c4fe. Read AMD-004 and audit 264. Comparison from historical Agent START_SHA returned ahead 6 / behind 0, with exactly five document paths: combined_review/263 and 264, P05 06, G01 07 and AMD-004 09. No source, test code, lockfile, earlier package record or upper design change was present in this remote diff.

## 3. Bounded additional test exception

Only following separate S10/S11 approval may the Agent edit or rename test_all_analysis_cli_scripts_are_explicitly_low_level_utilities in tests/product/test_enh_e4_g07_p03_cli_boundary.py. Preserve LOW_LEVEL_UTILITY, helpers and the other two tests, all other protected tests and existing Product production code. Explicitly distinguish five legacy low-level utilities and the new Local lifecycle CLI. Exact expected name-to-target mappings for all registrations targeting ariadne.interfaces.cli. are:

| Classification | Name | Target |
| --- | --- | --- |
| Legacy low-level | ariadne-discover | ariadne.interfaces.cli.discovery:main |
| Legacy low-level | ariadne-estimate | ariadne.interfaces.cli.estimation:main |
| Legacy low-level | ariadne-identify | ariadne.interfaces.cli.identification:main |
| Legacy low-level | ariadne-refute | ariadne.interfaces.cli.refutation:main |
| Legacy low-level | ariadne-sensitivity | ariadne.interfaces.cli.sensitivity:main |
| Local lifecycle | ariadne-causal-local | ariadne.interfaces.cli.local_causal.command:main |

Assert disjoint classes and legacy set equality to original LOW_LEVEL_UTILITY. Reject missing, renamed, redirected (including outside-prefix) and unclassified in-prefix entries. No candidate-derived expected map, prefix exclusion, skip/xfail or wrapper. Rerun affected file and all required focused and G01/Product regression suites; independent negative controls and source-diff verification remain required.

## 4. Work preservation and protected conditions

Agent's reported uncommitted implementation, tests and status report are not remotely inspected, modified or backed up by this action. Preserve a recoverable copy of tracked/staged/untracked changes before reconciliation; no destructive reset/clean or overwrite. Retain historical START_SHA separately from new synchronized resume baseline. Verify restored diff against authorized scope. Prior reported 19 focused pass and 225 pass/1 fail are historical, not fresh evidence.

Protected checkpoints:
- P01 9bff61f0eae25236f95f31f2cd3e7c81291f0167
- P02 3a76a0aa1698037354b284ba7b5a875300473ce6
- P03 858c9f73366036a2d1445e558135cd521f611462
- P04 7dcf2061dae3c8832b2b3ec9be6900ad6ee7edb6

Preserve AMD-001/002/003 including bounded P02 exception, public E11 Schema Versions, scientific meaning, existing Product behavior, uv.lock, independent science/FS/Reader and G01_999 acceptance. DEFERRED_PRODUCT_POLICY_BRIDGE remains UNFULFILLED.

## 5. Separate control-plane decisions

Formal 09 approval only. The resulting commit is the candidate for separate exact SHA S10 refreeze. It does not itself alter the current S10 or extend prior S11. Require distinct S10 and G01/P05/Trial01 limited S11 approvals, including non-destructive resume procedure, before implementation/test-code changes resume. No checkpoint or independent PASS asserted.
