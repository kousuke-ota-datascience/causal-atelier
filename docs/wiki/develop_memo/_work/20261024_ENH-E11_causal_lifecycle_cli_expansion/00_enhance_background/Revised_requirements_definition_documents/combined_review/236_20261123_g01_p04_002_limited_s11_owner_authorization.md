# 236 — G01/P04 AMD-E11-G01-P04-002 limited S11 Owner Coding Authorization

**Date:** 2026-11-23 JST  
**Decision ID:** `DEC-G01-P04-002-S11-REAUTH-01`  
**State:** `S11_OWNER_APPROVED / G01_P04_TRIAL01_LIMITED_CODING_AUTHORIZED / INDEPENDENT_G01_999_NOT_PASSED`  
**Repository:** `kousuke-ota-datascience/causal-atelier`  
**Working branch:** `feature/ariadne_mvp_e11`

## 1. Owner directive and exact normative identity

Owner explicitly approved:

> DEC-G01-P04-002-S11-REAUTH-01を承認する。AMD-E11-G01-P04-002に基づくG01-S10凍結SHA 3a63caa2d58c76c7f4289593713ee5c437e4ec91 を対象に、G01/P04/Trial01の限定Coding Authorizationを再発行せよ。P01チェックポイント9bff61f0eae25236f95f31f2cd3e7c81291f0167、P03チェックポイント858c9f73366036a2d1445e558135cd521f611462、既承認の科学的意味、公開E11 Schema Version、独立科学検証・G01_999受入条件を維持する。

**Immutable G01-S10 normative contract SHA:** `3a63caa2d58c76c7f4289593713ee5c437e4ec91`.

**Authorization scope:** `GATE_ID=G01`, `PACKAGE_ID=P04`, `TRIAL_NO=01` only. The earlier S10 `a7003b359444af64cad0edbade0341243653a8bf` and S11 `DEC-G01-P04-001-S11-REAUTH-01` are historical, not the current implementation contract.

## 2. Verified control-plane prerequisites

Prior to this record, branch HEAD was exactly `bc679945f744c3d5f8ad0ff949ab6e66f99abddb`. Compare results:
- New S10 `3a63caa2d58c76c7f4289593713ee5c437e4ec91`: ancestor, ahead 1, behind 0. The sole post-freeze diff is `combined_review/235_20261123_g01_p04_002_s10_owner_refreeze.md`.
- Previous S10 `a7003b359444af64cad0edbade0341243653a8bf`: ancestor, ahead 12, behind 0.
- Protected P01 checkpoint `9bff61f0eae25236f95f31f2cd3e7c81291f0167`: ancestor, ahead 55, behind 0.
- Protected P03 checkpoint `858c9f73366036a2d1445e558135cd521f611462`: ancestor, ahead 20, behind 0.
- Relevant preceding decisions: `DEC-G01-P04-CATEGORY-DOMAIN-01=A`; formal 09 `DEC-G01-P04-002-09-APPROVE-01`, recorded in `combined_review/234_20261123_g01_p04_002_formal_09_owner_approved.md`; S10 `DEC-G01-P04-002-S10-REFREEZE-01`, recorded in `combined_review/235_20261123_g01_p04_002_s10_owner_refreeze.md`.

This approval-record commit is written after the frozen tree; it does not change the frozen normative SHA. A later branch HEAD must never silently replace the immutable S10 contract.

## 3. Authorized coding envelope

Implement **G01/P04/Trial01** only, following frozen `06_G01_P04_fci_backend_oracle.md`, `07_Ariadne_ENH-E11_G01_test_instruction.md`, Method DD `30_63_causal_method_adapters.md`, IF `23_41_cli_scientific_ports.md`, and strict internal Design `e11_p1_m06_fci_design_profile_v1.schema.json`, including formal amendments `AMD-E11-G01-P04-001` and `AMD-E11-G01-P04-002`.

- **Method domain validation:** CATEGORICAL Design variables require a complete strictly declared `category_codes` universe; CONTINUOUS forbids the field. Enforce integer-code exactness/ordering/Backend representability, ordered verified Dataset column identity and every observed value belonging to its declared domain. Never shrink declared levels to observed `np.unique`. Missing declared X/Y levels or S strata must remain part of the full declared support eligibility tests. Reject before Backend calls, with typed failure, no fabricated Graph/Marker/scientific-negative.
- **Previous A scientific contract:** Every unordered pair X/Y and every conditioning subset S (not limited by depth/max_path_length) is checked before FCI; fisherz sample/correlation reliability and chisq/gsq expected cell counts >=5 across all declared code strata, with no silent CI substitution. Incomplete, unaffordable or numerically unreliable assessment fails closed, never claims admissibility.
- **Backend and Graph fidelity:** Verify real Python3.12 and effective causal-learn FCI API, preserve `node_names`, exact endpoints and PAG uncertainty, verified immutable source ContentRefs, Graph provenance and dual-hash semantics, non-null BK fail-closed, private stdout/error routing and no unauthorized publications.
- **Developer verification:** Implement focused positive/negative/boundary tests consistent with frozen G01 07, enhancement-vs-regression placement and independent test separation. Report actual commands/output; a schema-only or mocked fit does not establish scientific PASS.
- **Scope exclusions:** Do not modify completed P01/P03 implementation, 06/07, tests or checkpoints without new explicit Owner approval. P02 and P05 changes are not authorized by this S11. Other Methods/Gates, public `e11-local-*/1` wire schemas, Product v2, `uv.lock` dependency choice and other preexisting Gate decisions are outside scope unless separately approved.
- **Science acceptance remains independent:** Preserve independent MAG/PAG Oracle, actual Backend/Linux evidence, BK negative tests, T2/T3, Product regressions and G01_999. No automatic G01_999 PASS or downstream Gate unlock. SCI_NO_ADMISSIBLE_PAG requires authentic scientific proof and cannot encode technical failure.

## 4. Trial execution and new blocker discipline

Before starting, Coding Agent must independently verify current remote and branch fast-forward, clean working tree, actual fresh START_SHA, ancestor relationships, frozen S10 tree and authorized-only administrative post-S10 differences, complete `uv.lock` blob and file-byte SHA-256, Python/backend effective imports/signatures, and prior P04 checkpoint/remediation state. GitHub authorization record does not substitute those machine-local checks.

This is the reauthorization of the previously stopped **Trial01**, not a new Trial02. If another material contract ambiguity, scope break, unapproved numerical criterion, source incompatibility, or scientific authority gap occurs, **stop and report** concrete evidence before changing the frozen WHAT; do not invent a policy, create a false implementation checkpoint, or switch Backend without authorization.

On legitimate completion, report changed files, commits/push result and full checkpoint SHA, focused tests and remaining independent science obligations. No runtime Agent tests, P04 commit, P04 checkpoint or G01_999 success is asserted by this administrative record.

## 5. Authorization semantic boundary

Status is `S11_OWNER_APPROVED / LIMITED_CODING_AUTHORIZED`. It is **not** S09 independent science acceptance, nor G01_999 PASS. Fixed resource upper bounds/numerical-stability tolerances that were not previously approved must not be fabricated; if strict positive eligibility cannot be decided without a new normative scientific policy, fail closed and escalate under the same change-management mechanism.
