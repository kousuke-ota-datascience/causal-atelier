# 242 — G01/P04 Method policy sharing vs completed Product v2 — Owner decision docket

**Date:** 2026-11-23 JST  
**Status:** `OWNER_ARCHITECTURE_AND_COMPLETED_PRODUCT_COMPATIBILITY_DECISION_PENDING / NON_NORMATIVE`  
**Decision requested:** `DEC-G01-P04-PRODUCT-POLICY-SHARING-01`  
**Classification:** `CONTRACT_SCOPE_CONFLICT / PRODUCT_V2_POLICY_SHARING`  
**Coding Agent START_SHA:** `99c33a661272d45bf72c8dee61ce1eb129a337dd`  
**Immutable G01-S10:** `cbfdbdd6b91f3a2f889fe9b62c2a4ab286da6132`  
**Approved S11:** `DEC-G01-P04-003-S11-REAUTH-01`  
**P01 checkpoint:** `9bff61f0eae25236f95f31f2cd3e7c81291f0167`  
**P03 checkpoint:** `858c9f73366036a2d1445e558135cd521f611462`  
**P04 checkpoint:** none

> Decision docket only: no frozen 30/06/07, completed Product v2 source code, public schema, or scientific rule is changed here. A new Owner architectural/scope decision is needed before normative changes or P04 coding resume.

## 1. Evidence and contract conflict

**Normative upstream authority at frozen S10:**
- `30_detailed_design/30_61_causal_domain_ports.md` requires shared pure `EstimandEligibilityPolicy`; the legacy `ScientificValidationService` is expressly to use the same policy by a compatible call, without blindly forcing new Estimands into legacy ATE/ATT enums.
- `30_detailed_design/30_62_local_execution_publication.md` §§2, 8 requires `MethodCapabilityRegistry` as the one Method×Estimand×Inference metadata authority, no independently competing `ESTIMATOR_CAPABILITIES` rule set, and Method/Backend/Inference-aware capability dispatch.
- `23_api_interface_design/23_41_cli_scientific_ports.md` requires existing Product scientific eligibility plus new Method Registry to share pure Domain policy while separating effective Backend availability.
- `10_enhance_instruction/G01/06_G01_P04_fci_backend_oracle.md` §§3,6.2 requires the same registry metadata and compatibility policy used by legacy `ScientificValidationService` via common pure policy, not a fork.
- The G01 Parent/Gate scope and limited S11 exclude modifications to existing Product v2 code/CLI/DB/worker and completed Packages, while retaining Product v2 regression.

**Actual current Product v2 code** (`src/ariadne/product/application/scientific_validation_service.py`, branch `feature/ariadne_mvp_e11`):
- `ScientificValidationService.validate_submission` calls `validate_analysis_spec`; for `ExecutionOperation.DISCOVERY` or `IDENTIFICATION` it rejects a present `input_result_id` and returns without the new Registry/policy.
- For downstream operations it verifies upstream Result existence, project, dataset, Graph and Result type, and in ESTIMATION calls `_validate_estimation`.
- `_validate_estimation` validates question-hash matching, Identification and Data Eligibility statuses/override and then `validate_estimator_compatibility`. The latter applies `ESTIMATOR_CAPABILITIES` for legacy names (difference_in_means, diff_in_means, ols, outcome_regression, ipw, aipw) with estimand/strategy, treatment/outcome types, adjustment and diagnostics. This is **not** a complete P1-M06 MethodRegistry or a compatible direct new-method `ValidatedCapabilityRequest` consumer.

**Analysis:** early return is not intrinsically a bug in the legacy operation workflow. A new Local CLI DISCOVER/P1-M06 request is not equivalent to legacy Product v2 DISCOVERY `validate_submission` and should not be routed into it. However, the frozen requirement that legacy estimator rules be canonicalized into a common pure policy/metadata authority requires either a bounded legacy code integration or an explicitly authorized staged implementation plan. Copying the legacy estimator table into a new registry while leaving both editable is a two-authority fork and fails the frozen architecture. Simply weakening 07 tests to skip policy equivalence is not acceptable.

## 2. Owner option A — bounded immediate Product v2 bridge (full frozen architecture; higher regression risk)

Authorize **separately scoped and specifically enumerated** changes in `src/ariadne/product/application/scientific_validation_service.py` plus an approved new common pure policy/module, only to extract/delegate legacy estimator compatibility metadata and checks without changing externally visible Product v2 operation semantics, method aliases, exceptions and failure classification. The new P1-M06 policy uses the same independent Method authority but retains distinct Local DISCOVER config/Backend/API eligibility; no direct legacy method call, no API/wire/DB changes, no Product CLI workflow redesign.

Require:
1. Complete before/after behavior characterization for existing Product v2 DISCOVERY/IDENTIFICATION/ESTIMATION, including early-return, invalid input_result_id, upstream lineage and legacy estimator methods, diagnostics, error types/messages/status.
2. One canonical policy/metadata owner and explicit bridging from legacy estimator names to their old exact eligibility meaning; no accidental P1-M06 registration under legacy IDs, no silent default/Backend fallback.
3. Product v2 regression tests with real old entrypoint, both pass/fail fixtures, and no changed downstream Product schema. If semantic equivalence cannot be established, stop and request a new Owner decision.
4. The already-approved P01/P03 checkpoints and completed P02 code remain untouched. Only the explicitly approved Product service bridge and common pure module may be touched. This is a new exception to S11 scope, needing a new formal 09/S10/S11 after final contract revision.

**Tradeoff:** most closely fulfills the current frozen shared-policy contract now; requires direct changes to completed Product code and significant regression evidence. The old service's early return need not itself be changed if policy sharing is through estimation and pure shared metadata where applicable.

## 3. Owner option B — stage Product v2 integration; recommended to preserve completed Product (changes timing, not scientific target)

Split *policy definition/consolidation* from *legacy Product v2 consumer migration*. During G01/P04, define a reusable pure Method/Estimand compatibility/eligibility policy and the single canonical new Method metadata authority without copying legacy rules into an independently mutable new table; implement P1-M06 Local DISCOVER and its authorized focused tests. Existing `ScientificValidationService` retains its old validation path and existing `ESTIMATOR_CAPABILITIES` temporarily as a **legacy-only compatibility baseline**, not an alternative source for P1-M06 or newly introduced Methods. Do not claim that legacy service is already wired to the new policy. The specific integration of Product v2 into the common policy is **deferred**, not `RETIRED` or silently canceled, and requires a separately planned, explicit Owner authorization and Product full regression **before the architecture-wide shared-policy invariant can be declared fulfilled**.

Normative bounded changes upon approval:
- `30_61`, `30_62`, `23_41`: clarify intended final single shared policy and explicit **interim G01-only** Product isolation/migration deferral; do not erase the final DRY/single-authority architectural objective.
- P04 `06` §3,6.2: G01/P04 Local Registry and P1-M06 eligibility are in scope; no Product `ScientificValidationService` patch or false evidence of active reuse. Existing Product v2 estimator rules are old Product behavior to be *characterized and mapped* at later authorized integration. Do not fork a second mutable copy of legacy estimator policies under a competing registry.
- G01 `07`: require tests that local method checks are sourced from their own single pure Method authority, no other P1-M06 policy fork, legacy Product v2 behavior unchanged, and a separately tracked migration obligation; no fake assertion that legacy now invokes new policy.
- Formal AMD-004 must clearly set status `DEFERRED_PRODUCT_POLICY_BRIDGE` not `IMPLEMENTED`, identify an Owner-controlled integration Gate/dependency and ensure G01_999 criteria explicitly account for the deferral. **Caution:** if original G01_999 acceptance expressly requires immediate runtime shared-policy use by Product v2, Option B changes the acceptance scope/timing and needs explicit Owner approval—not mere Author clarification. It must not declare G01_999 PASS without independently verifying all applicable accepted criteria or explicitly amending them.
- No modification to Product service code, completed P01/P03, public E11 wire, scientific formulas/criteria, PAG, BK, FCI, numeric thresholds or backend behavior.

**Tradeoff:** smallest impact to completed Product and strictest regression isolation. It is a change to implementation phasing of an existing architecture requirement and must be explicitly accepted, including the final common-policy integration milestone. Not automatically authorized by a prior S11.

## 4. Option C — separate arbitrary copy (not acceptable)

Implement new `MethodCapabilityRegistry` with an independent copy of `ESTIMATOR_CAPABILITIES` and leave existing Product as-is, then claim the rules are shared because they happen to match today. This violates the one-authority requirement and accumulates silent divergence; it cannot be represented as a purely editorial fix.

## 5. Minimal impact and protected boundary

**Candidate normative files if A:** `30_61` / `30_62` / `23_41` as necessary to precisely specify the bridge and legacy compatibility, P04 `06`, G01 `07`, new formal `09_AMD004`; optional approved bounded Product service + new pure module source during authorized coding only.

**Candidate normative files if B:** `30_61` / `30_62` / `23_41`, P04 `06`, G01 `07`, formal `09_AMD004`; Product service source unchanged; completed P01/P03 and public Study/Graph/Manifest schemas unchanged.

No changes to RD/BD scientific semantics, all P1-M06 Fisher-Z/discrete categorical eligibility amendments AMD-001/002/003, public E11 Schema Version, `uv.lock`, Product v2 tests or completed package test/06/07 code without explicit new approval.

## 6. Pending decision / required control-plane sequence

Owner decision requested: `DEC-G01-P04-PRODUCT-POLICY-SHARING-01` Option **A immediate bounded bridge** or Option **B explicitly deferred legacy consumer migration with acceptance/dependency clarification**. Recommend B only if Owner agrees that no G01_999 claim of completed common-policy integration is allowed until a separately tracked, approved product integration occurs. If that invariant is a hard G01_999 acceptance, either choose A or separately amend the stage acceptance plan with accountable milestone.

After adoption of either change, prepare consistent superior design → 06 → 07 → new AMD-004 candidate, seek separate formal 09, new S10 immutable Git SHA Owner refreeze, separate S11 limited coding authorization. Prior frozen S10 `cbfdbdd6b91f3a2f889fe9b62c2a4ab286da6132` and S11 `DEC-G01-P04-003-S11-REAUTH-01` do **not** cover altered Product v2 integration semantics.

Coding Agent reports no P04 source change, focused verification, FCI fit, package checkpoint or push. A decision docket does not establish any of these.
