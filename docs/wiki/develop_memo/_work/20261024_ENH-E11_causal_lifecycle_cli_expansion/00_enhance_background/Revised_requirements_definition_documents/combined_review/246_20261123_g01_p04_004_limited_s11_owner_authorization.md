# 246 — G01/P04 AMD-E11-G01-P04-004 limited S11 Owner Coding Authorization

**Date:** 2026-11-23 JST  
**Decision ID:** `DEC-G01-P04-004-S11-REAUTH-01`  
**State:** `S11_OWNER_APPROVED / G01_P04_TRIAL01_LIMITED_CODING_AUTHORIZED / DEFERRED_PRODUCT_POLICY_BRIDGE_UNFULFILLED / G01_999_NOT_PASSED`  
**Repository:** `kousuke-ota-datascience/causal-atelier`  
**Working branch:** `feature/ariadne_mvp_e11`

## 1. Explicit Owner directive and immutable authority

Owner explicitly approved:

> DEC-G01-P04-004-S11-REAUTH-01を承認する。AMD-E11-G01-P04-004に基づくG01-S10凍結SHA 3ea759825810e95425a9e7557c3b2cc46b21157d を対象に、G01/P04/Trial01の限定Coding Authorizationを再発行せよ。P01チェックポイント9bff61f0eae25236f95f31f2cd3e7c81291f0167、P03チェックポイント858c9f73366036a2d1445e558135cd521f611462、公開E11 Schema Version、既承認の科学的意味、独立科学検証・G01_999受入条件、およびDEFERRED_PRODUCT_POLICY_BRIDGEの未完了依存を維持する。

**Active immutable G01 S10 normative SHA:** `3ea759825810e95425a9e7557c3b2cc46b21157d`.

**Limited execution envelope:** `GATE_ID=G01`, `PACKAGE_ID=P04`, `TRIAL_NO=01` only. Prior `DEC-G01-P04-003-S11-REAUTH-01` is historical and does not authorize coding against the revised AMD-004 architecture staging contract.

## 2. Pre-authorization Git facts verified

Immediately before creating this S11 record, the remote branch HEAD was `971b4341f7b2342035d06a7ca937e335071361ba`. GitHub comparisons established:

| Baseline | SHA | Relationship to pre-record HEAD |
| --- | --- | --- |
| Revised G01-S10 | `3ea759825810e95425a9e7557c3b2cc46b21157d` | Ancestor, ahead 1, behind 0 |
| Protected P01 checkpoint | `9bff61f0eae25236f95f31f2cd3e7c81291f0167` | Ancestor, ahead 75, behind 0 |
| Protected P03 checkpoint | `858c9f73366036a2d1445e558135cd521f611462` | Ancestor, ahead 40, behind 0 |
| Previous G01-S10 | `cbfdbdd6b91f3a2f889fe9b62c2a4ab286da6132` | Ancestor, ahead 12, behind 0 |

The sole post-S10 difference before this record was the administrative `combined_review/245_20261123_g01_p04_004_s10_owner_refreeze.md`. The frozen S10 contains AMD-004 and formal 09 approval record `combined_review/244_20261123_g01_p04_004_formal_09_owner_approved.md`. This S11 record itself will be committed **after** the frozen tree and does not alter the frozen SHA.

## 3. Authorized Local P1-M06 implementation and tests

Implement **only** G01/P04/Trial01 under the frozen RD/IF/DD/06/07 and the sequence AMD-001/002/003/004:

- Single Local P1-M06 pure eligibility and Method metadata authority through `MethodCapabilityRegistry`, `MethodCapabilityPort.resolve(ValidatedCapabilityRequest)`, `DiscoveryPort.discover` and `FciDiscoveryAdapter`; effective Backend distribution/signature/optionals, strict Operation/Estimand/Design/Inference checks, no silent fallback or duplicate FCI.
- AMD-001 exhaustive unordered X/Y and all conditioning subsets S before any FCI invocation regardless of depth; complete preflight or typed fail-closed. No invented compute budget that weakens scientific coverage.
- AMD-002 `Design.variables[].category_codes` as complete declared categorical support, exact integer binding and no `np.unique` shrinkage; full declared strata, expected cell counts >=5, strict category-domain consistency.
- AMD-003 Fisher-Z float64 numerical preflight: positive definite correlation submatrices, `kappa2(R)*np.finfo(np.float64).eps <= 1e-6`, two-sided inverse residual maximum-row-sum infinity norm <= `1e-8`, finite intermediates and strict `abs(partial_r)<1`; all candidate pairs/subsets or pre-FCI technical/eligibility stop.
- No non-null BK passthrough, invalid Graph/PAG endpoint certainty, invented SCI_NO_ADMISSIBLE_PAG science-negative or row/staging leakage. Preserve immutable ContentRefs, Graph lineage, true `node_names`, PAG latent uncertainty and effective runtime FCI Backend checks.
- AMD-004 scoped policy sharing: G01/P04 Local method authority only. Existing `src/ariadne/product/application/scientific_validation_service.py`, `ESTIMATOR_CAPABILITIES`, legacy Product v2 CLI/Web/API/DB/Worker and all completed P01/P03 source/tests/06/07/checkpoints remain **untouched**. The old Product table is a legacy-only compatibility baseline, not a second Local P1-M06 Method Registry or permitted fallback. Do not claim an actual Product shared-policy delegate exists. Product v2 legacy regression and behavior stability remain independently testable obligations.

## 4. Explicit outstanding architecture and science obligations

`DEFERRED_PRODUCT_POLICY_BRIDGE` is **not implemented** and **not retired**. It requires a separate Owner-approved Product v2 migration scope and independently verified backward-compatible consumer integration into the final shared pure eligibility/Method authority. Its G01_999 shared-policy acceptance dependency stays explicitly **unfulfilled**, absent an additional formal Owner decision that changes acceptance phasing; this authorization does not change or waive the G01_999 criteria or assign a fictitious later Gate.

Independent actual Python3.12 Backend/FCI, MAG/PAG Oracle, latent/BK negatives, Product v2 regression, T2/T3 and G01_999 remain required; passing focused tests is not independent science PASS.

## 5. Trial restart and stop discipline

The previously stopped `Trial01` had START_SHA `99c33a661272d45bf72c8dee61ce1eb129a337dd`, no new P04 implementation or checkpoint. At actual Agent restart, verify current branch/remote, clean working tree, fresh START_SHA and its ancestry against approved S10 and protected P01/P03, ensure only authorized post-freeze administrative commits, verify `uv.lock` Git blob and physical bytes, installed Python3.12 / causal-learn API and no prior P04 checkpoint/remediation.

On a material unapproved contract ambiguity, unsupported Backend behavior, unexpected Product compatibility effect or scientific verification blocker, stop and report precise evidence before modifying the frozen WHAT. Do not create false checkpoints or PASS states.

On successful implementation report actual changes, test commands/results, exact new source checkpoint commit SHA and push confirmation. S11 administrative approval alone is **not** code execution, Backend fit, independent science acceptance or G01_999 PASS.
