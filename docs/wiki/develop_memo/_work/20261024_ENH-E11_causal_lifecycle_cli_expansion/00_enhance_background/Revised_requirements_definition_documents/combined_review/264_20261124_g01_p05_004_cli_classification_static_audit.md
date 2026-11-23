# 264 — AMD-E11-G01-P05-004 static contract consistency audit

**Date:** 2026-11-24 JST
**Owner decision:** DEC-G01-P05-CLI-CLASSIFICATION-01=A_ADOPTED, docket 263
**State:** AUTHOR_STATIC_AUDIT_PREPARED / FORMAL_09_PENDING / S10_REFREEZE_PENDING / S11_REAUTH_PENDING
**Historical blocked START_SHA:** 94758d3964eb92fb7df3619f7c5d31d8d996862e
**Current immutable S10:** 47ecfe33f3daf91da8c589db589b21f628e4e23b

## 1. Authority and defect

RD 10_17 FR-203 and IF 23_41 §§1–2 distinguish legacy Product and new Local Scientific CLI. P05 06 §6.6 fixes the new registration and module path. G01 07-12 protects legacy behavior. The old classification assertion selects all targets starting ariadne.interfaces.cli. but requires exactly the five LOW_LEVEL_UTILITY names. Namespace membership does not imply low-level functional scope after ENH-E11. The new registration is required, not an implementation deviation. No change to RD/IF/DD, public CLI or scientific contracts is necessary.

## 2. Document and source correspondence

Read back P05 06 blob a4448e6dac9ac8505e8763cac821856c50cc858d, G01 07 blob 6af42b17a403756b237c1b4c4a546bff4ef11381 and AMD-004 blob c38dd6f6b86e37ae66d9da3bd9ec22822db267c8. All contain the same six fixed mappings (five legacy targets derived from START_SHA pyproject.toml, one new target from P05 §6.6). P05 06 is self-contained for the bounded implementation rule; 07 owns independent acceptance. The protected Product test remains byte-identical at blob 654d69aa52adbf1d54b6f12fb80851f630ed4568. Its helpers, LOW_LEVEL_UTILITY and the other two tests remain protected. The new exception permits only editing/renaming the classification test, not widening any production-code exception. Preserve AMD-001/002/003.

## 3. Predicate realizability

The proposed exact mapping equality uses the existing project.scripts parser and unchanged target-prefix selection; expected values are fixed independently of actual registrations. It requires no new import or production wrapper. Disjoint classification and equality of legacy expected names to LOW_LEVEL_UTILITY preserve semantic separation; exact targets imply the original :main suffix invariant.

An abstract mapping predicate was evaluated in an isolated JavaScript model during Author audit (not repository Python, not pytest, not an independent verification):
| Case | Expected | Abstract predicate |
| --- | --- | --- |
| Six approved mappings | accept | accept |
| Missing legacy registration | reject | reject |
| Missing Local registration | reject | reject |
| Redirected legacy target | reject | reject |
| Wrong Local target | reject | reject |
| Local redirected outside prefix | reject | reject |
| Extra unclassified in-prefix entry | reject | reject |

By equality, renames or legacy redirections outside the prefix also fail because a required key disappears. The predicate does not classify unrelated scripts outside the CLI prefix, consistent with original test scope. Do not infer new Local dependency reachability from legacy-only reachability checks. Real fixed-candidate source-diff verification, independent negative controls and actual affected-file/full regression runs remain required.

## 4. Scope and work preservation

Before this audit record, comparison from historical START_SHA was ahead 5 / behind 0, with only four document paths changed: docket 263, P05 06, Gate 07 and AMD-004. No source, test, lockfile, earlier Package record or upper design change. Author did not access or modify the Agent's uncommitted local source/tests/status report. Preserve them via verified recoverable copy including untracked work and non-destructive reconciliation after new S11; record historical START_SHA and new resume baseline separately. Do not assume a dirty worktree is a fresh clean start or reset it to the remote SHA. Existing local changes must be inventoried and revalidated against authorized scope.

P01–P04 checkpoints, public E11 Schema Versions, scientific meaning, Product behavior, independent science/FS/Reader/G01_999 acceptance and DEFERRED_PRODUCT_POLICY_BRIDGE UNFULFILLED remain protected. Agent-reported 19 focused pass and 225 pass/1 fail are historical evidence; no new pytest or executable implementation result is asserted.

## 5. Verdict

The specific classification conflict is resolvable with one protected test change under the approved design and preserved legacy invariants. Static audit only. Require separate formal 09 approval, exact SHA S10 refreeze and limited S11 reauthorization before the Agent edits that test or resumes implementation. No new checkpoint or Gate PASS.
