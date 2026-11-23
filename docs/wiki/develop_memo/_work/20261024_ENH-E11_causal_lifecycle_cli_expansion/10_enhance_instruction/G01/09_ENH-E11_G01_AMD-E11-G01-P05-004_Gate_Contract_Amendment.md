# AMD-E11-G01-P05-004 — Explicit CLI classification and bounded legacy regression test exception

**Date:** 2026-11-24 JST
**Gate/Package/Trial:** G01/P05/Trial01
**Owner design decision:** DEC-G01-P05-CLI-CLASSIFICATION-01=A_ADOPTED (combined_review/263)
**State:** AUTHOR_PREPARED_FORMAL_09_CANDIDATE / FORMAL_09_PENDING / S10_REFREEZE_PENDING / S11_REAUTH_PENDING / P05_BLOCKED
**Last blocked START_SHA:** 94758d3964eb92fb7df3619f7c5d31d8d996862e
**Current immutable S10:** 47ecfe33f3daf91da8c589db589b21f628e4e23b
**Prior S11:** DEC-G01-P05-003-S11-REAUTH-01 (record 262); not authorization for the new protected-test exception.

## 1. Defect and authority

RD 10_17 FR-203 distinguishes existing Product and new Local Scientific CLI. IF 23_41 §§1–2 and P05 06 §6.6 require the separate ariadne-causal-local entrypoint with exact module binding. G01 07-12 protects legacy behavior. Existing Product test tests/product/test_enh_e4_g07_p03_cli_boundary.py (baseline blob 654d69aa52adbf1d54b6f12fb80851f630ed4568) conflates the ariadne.interfaces.cli. namespace with the five low-level utilities. Its exact set equality rejects the newly required sixth registration. This is an obsolete test classification assumption, not a reason to modify approved registration, hide it behind a wrapper or weaken legacy contracts.

Agent reported 19/19 P05 focused tests and 225 pass/1 fail in combined regression, with 11 existing fork warnings. Agent's implementation and status report remain uncommitted and were not inspected or executed by Author. No checkpoint or PASS claimed.

## 2. Precise amendment

After separate formal 09, S10 and S11 approvals, the sole additional protected-test exception permits modification (including rename) of test_all_analysis_cli_scripts_are_explicitly_low_level_utilities in tests/product/test_enh_e4_g07_p03_cli_boundary.py. Expected mapping constants may be local to this function. Preserve the existing LOW_LEVEL_UTILITY constant, all helpers, other two tests and all other legacy tests and Product production code.

The entire mapping of project.scripts entries with target prefix ariadne.interfaces.cli. must equal these independently fixed expected mappings:

| Classification | Name | Exact target |
| --- | --- | --- |
| Legacy low-level utility | ariadne-discover | ariadne.interfaces.cli.discovery:main |
| Legacy low-level utility | ariadne-estimate | ariadne.interfaces.cli.estimation:main |
| Legacy low-level utility | ariadne-identify | ariadne.interfaces.cli.identification:main |
| Legacy low-level utility | ariadne-refute | ariadne.interfaces.cli.refutation:main |
| Legacy low-level utility | ariadne-sensitivity | ariadne.interfaces.cli.sensitivity:main |
| Local lifecycle CLI | ariadne-causal-local | ariadne.interfaces.cli.local_causal.command:main |

Explicitly assert the legacy expected names equal the original LOW_LEVEL_UTILITY and the two classes are disjoint. Exact mapping equality preserves the :main suffix requirement and strengthens prior name-only equality. Reject missing/renamed/redirected entries, including redirection outside the prefix, or unclassified additional in-prefix registrations. No prefix exclusion, dynamic allowlist from candidate, skip/xfail or wrapper. Keep other legacy dependency reachability and manifest identity tests unchanged; no claim their existing scope verifies the new Local CLI. Existing G01 tests own its behavior.

## 3. Normative changes and acceptance

P05 06 §7 states the precise bounded implementation exception and preservation of uncommitted work. G01 07-12 specifies the six mappings, disjoint classes, negative controls and independent source-diff/actual regression evidence. No change to RD, logical data, basic design, IF/DD or P05 §6.6 registration. AMD-001/002/003 and their limited source exceptions remain binding. This amendment supersedes only the prior prohibition on changing this particular Product classification test, not the obligation to preserve old behavior.

Run the affected test file and all required P05 focused and G01/Product regression suites. Independently verify positive mapping and negative controls: missing old/new name, changed old/new target (including outside prefix), unexpected in-prefix name. No lowering of old assertions, other tests or independent G01_999 criteria. New negative controls may be evaluated in independent verification without expanding the protected-test edit scope.

## 4. Work preservation and restart

The Agent's uncommitted P05 source, tests and status report are not a checkpoint and must not be discarded. Before integration, inventory tracked/staged/untracked changes and preserve a recoverable copy including untracked work. Reconcile remote documentation-only commits on a clean separate baseline or with a verified reversible preservation workflow; do not reset --hard, clean or overwrite local implementation. Verify exact diff and unchanged original START_SHA ancestry, S10/S11, checkpoint/lockfile invariants and scope. Retain original execution START_SHA as historical; record new synchronized resume baseline separately. Restore/reconcile local changes, then perform only authorized remaining test modification and necessary P05 work within existing S11 scope. Actual commands, exit codes, results, status, checkpoint and push are required. Stop if conflict or additional protected change needs Owner decision.

## 5. Protected invariants and decision boundary

P01 9bff61f0eae25236f95f31f2cd3e7c81291f0167; P02 3a76a0aa1698037354b284ba7b5a875300473ce6; P03 858c9f73366036a2d1445e558135cd521f611462; P04 7dcf2061dae3c8832b2b3ec9be6900ad6ee7edb6. Preserve existing Product production code, public E11 Schema Versions, scientific meaning, privacy, actual FS/Reader, uv.lock, independent science and G01_999 acceptance. DEFERRED_PRODUCT_POLICY_BRIDGE remains UNFULFILLED. No source/test changes by this Author record. Formal 09 Owner approval, exact SHA S10 refreeze and separate limited S11 reauthorization remain required.
