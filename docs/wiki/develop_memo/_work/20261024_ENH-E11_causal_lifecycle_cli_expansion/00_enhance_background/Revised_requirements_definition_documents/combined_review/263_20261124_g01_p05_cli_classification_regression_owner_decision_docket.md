# 263 — G01/P05 CLI classification regression: Owner decision docket

**Date:** 2026-11-24 JST
**State:** BLOCKED_IMPLEMENTATION / PROTECTED_PRODUCT_TEST_EXCEPTION_OWNER_DECISION_PENDING
**Proposed decision:** DEC-G01-P05-CLI-CLASSIFICATION-01
**Verified remote HEAD / Agent START_SHA:** 94758d3964eb92fb7df3619f7c5d31d8d996862e
**Active S10:** 47ecfe33f3daf91da8c589db589b21f628e4e23b
**S11:** DEC-G01-P05-003-S11-REAUTH-01, d693b4f89d1214b9e4c586aa2d0cbf266398bbbe

## Evidence and authority

At START_SHA, pyproject.toml lines 31–40 declares the five legacy scientific CLI mappings and Product API/worker. tests/product/test_enh_e4_g07_p03_cli_boundary.py blob 654d69aa52adbf1d54b6f12fb80851f630ed4568 defines LOW_LEVEL_UTILITY and test_all_analysis_cli_scripts_are_explicitly_low_level_utilities: it selects every script target starting ariadne.interfaces.cli. and asserts exact equality of names to LOW_LEVEL_UTILITY, then requires :main suffix. The other two tests enforce legacy CLI dependency reachability and portable CliManifest persistent-identity exclusion.

RD 10_17 FR-203 explicitly distinguishes legacy Product and new Local Scientific CLI while preserving legacy contracts and Review/Override. IF 23_41 §§1–2 defines a separate Local CLI boundary and ariadne-causal-local public syntax. P05 06 §6.6 explicitly requires ariadne-causal-local = ariadne.interfaces.cli.local_causal.command:main, preserving old entrypoints. G01 07-12 protects legacy behavior, DB/Web/Worker, and unrelated Methods. These authorities do not require the entire CLI namespace to remain exclusively low-level. The old assertion conflates implementation namespace and functional classification. Changing registration to evade its prefix would violate the approved placement or defeat the guard.

Agent reports uncommitted P05 implementation; 19 focused pass, 225 regression pass/1 fail, 11 existing fork warnings. This is reported evidence, not independently executed or remotely inspected implementation. No P05 checkpoint, commit or push reported.

## Options

A (recommended): explicitly classify the five old low-level utilities and the one approved Local lifecycle CLI. Authorize only modification of the one existing classification test in tests/product/test_enh_e4_g07_p03_cli_boundary.py, including renaming it if necessary to describe the new invariant. Preserve LOW_LEVEL_UTILITY exactly, and both other tests unchanged. Assert exhaustive equality of CLI-prefix registration names to LOW_LEVEL_UTILITY union the explicit singleton ariadne-causal-local; require exact approved target for new CLI; preserve exact legacy mappings and :main suffix; reject unclassified additions. No prefix exclusion, blanket skip, xfail or dynamic allowlist from actual registrations. No change to production code beyond existing P05 authorization. New G01 integration tests continue to test new CLI actual behavior; do not make this old test a duplicate lifecycle integration suite.

Concrete expected mapping for legacy entries, from START_SHA:
- ariadne-discover -> ariadne.interfaces.cli.discovery:main
- ariadne-estimate -> ariadne.interfaces.cli.estimation:main
- ariadne-identify -> ariadne.interfaces.cli.identification:main
- ariadne-refute -> ariadne.interfaces.cli.refutation:main
- ariadne-sensitivity -> ariadne.interfaces.cli.sensitivity:main
- approved separate lifecycle entry: ariadne-causal-local -> ariadne.interfaces.cli.local_causal.command:main

A single explicit expected mapping equality plus unchanged LOW_LEVEL_UTILITY and explicit disjoint classification satisfies all of these. Retain old :main assertion (or stronger exact mapping equality). Missing/renamed/redirected legacy CLI, wrong new target, unexpected CLI-prefix registration all fail. Existing reachability and manifest tests retain their scope and bodies. Do not claim a global dependency scan of new Local CLI from the legacy reachability test; new Local boundary is tested by G01 requirements.

B: register a wrapper outside the CLI namespace to preserve old test. Reject: violates approved exact module binding or hides new entrypoint from exhaustive classification; unnecessary production indirection.
C: ignore/skip failing test or add new Local CLI to LOW_LEVEL_UTILITY. Reject: loses or misrepresents classification boundary.

## Minimal normative scope after Owner approval

No changes needed to RD, logical data, basic design, IF/DD or P05 §6.6 registration. Amend G01 07-12 to define exhaustive explicit classification and retained legacy invariants; add narrow exception reference in P05 06 regression/scope section only if needed to resolve protected-test prohibition, plus AMD-E11-G01-P05-004 recording precise test exception and static audit. Historical AMDs, S10/S11 records and completed package instructions untouched. No change to old Product source, other tests, P01–P04 checkpoints, public E11 schemas, scientific contracts, dependency lock or independent G01_999 requirements. DEFERRED_PRODUCT_POLICY_BRIDGE remains UNFULFILLED.

After approval, separate formal 09/S10/S11 decisions per existing change control. Agent's uncommitted work must be preserved, not reset/stashed blindly or treated as a checkpoint; verify exact diff and reconcile new remote administrative commits before resuming. Rerun specific test file and full reported focused/regression commands against final candidate; only actual all-pass and other package conditions permit checkpoint. No independent acceptance waiver. No code or tests changed by this docket. Owner decision required for the protected Product test exception.
