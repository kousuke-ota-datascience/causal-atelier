# AMD-E11-G01-P04-004 — Local Method pure policy and deferred Product v2 consumer bridge

**Date:** 2026-11-23 JST  
**Gate / Package / Trial:** `G01/P04/Trial01`  
**Classification:** `ARCHITECTURE_SCOPE_AND_COMPATIBILITY_PHASING`  
**Owner decision:** `DEC-G01-P04-PRODUCT-POLICY-SHARING-01=B_ADOPTED`  
**State:** `AUTHOR_PREPARED_FORMAL_09_CANDIDATE / FORMAL_09_OWNER_APPROVAL_PENDING / S10_REFREEZE_PENDING / S11_REAUTH_PENDING`  
**Last stopped Coding Agent START_SHA:** `99c33a661272d45bf72c8dee61ce1eb129a337dd`  
**Previous G01-S10:** `cbfdbdd6b91f3a2f889fe9b62c2a4ab286da6132`  
**Previous S11:** `DEC-G01-P04-003-S11-REAUTH-01` (not authorization for this altered architecture timing)  
**Protected P01:** `9bff61f0eae25236f95f31f2cd3e7c81291f0167`  
**Protected P03:** `858c9f73366036a2d1445e558135cd521f611462`  
**P04 checkpoint:** none

## 1. Blocking root cause and normative hierarchy

G01/P04 `06` §6.2 required common pure Method eligibility policy shared between the Local `MethodCapabilityRegistry` and Product v2 `ScientificValidationService`. Superior contracts DD `30_61`, DD `30_62`, IF `23_41` likewise require eventual shared Method×Estimand policy and single metadata authority. However the S11 Coding envelope explicitly prohibits modifying Product v2. The actual existing `src/ariadne/product/application/scientific_validation_service.py` uses an existing `ESTIMATOR_CAPABILITIES` dictionary for legacy Estimation and directly returns after the Discovery/Identification input_result_id check. It does **not** already delegate to the new Local Registry. This existing Product behavior is evidence of a **real migration boundary**, not proof that the early return should be removed or P1-M06 routed through Product submission validation.

The prior contract was underdetermined concerning when/how legacy consumers must migrate while P04 remains scoped to Local. Docket `combined_review/242_20261123_g01_p04_product_v2_shared_policy_scope_decision_docket.md` evaluated an immediate bounded Product bridge (A), deferred Product consumer migration (B), and unacceptable duplicated-authority implementation (C). Owner explicitly adopted B in `DEC-G01-P04-PRODUCT-POLICY-SHARING-01`, documented in `combined_review/243_20261123_g01_p04_product_policy_sharing_B_owner_adopted.md`.

## 2. Normative split and migration state

### 2.1. Required NOW — G01/P04 Local scope

- Implement a **single** Local Method metadata and pure eligibility policy authority for `P1-M06/DISCOVER/GRAPH_STRUCTURE`, with its exact validated Operation, Method, Estimand, Design, CI, Inference and Backend restrictions. `MethodCapabilityPort.resolve(ValidatedCapabilityRequest)` validates the full request, and the concrete Registry verifies effective Backend distribution/API/probes with no defaults or fallback; `DiscoveryPort` and `FciDiscoveryAdapter` use the same validated capability. Separate capability availability from scientific eligibility.
- No second independently mutable Local P1-M06 compatibility table and no duplicate FCI implementation. Do not copy the legacy estimator table `ESTIMATOR_CAPABILITIES` to a new Registry and call it shared policy. The old Product table is used **only** by the unchanged Product v2 path as an interim behavior-preserving baseline.
- Product v2 `ScientificValidationService.validate_submission`, `ESTIMATOR_CAPABILITIES`, Product v2 CLI/Web/API/DB/Worker, legacy Product entrypoints and completed P01/P03 are **out of G01/P04 coding scope**. Do not invoke Product's `validate_submission` from Local P1-M06; legacy DISCOVERY/IDENTIFICATION early returns remain as-is. The Local Graph/Backend and scientific semantics cannot be decided by old Product estimator aliases or fallbacks.
- Verify genuine Local pure-policy/Registry/Adapter integration in focused tests, method/backend mismatch, disallowed inference/config, no fallback, no duplicate authority, no fake Method registration. Independently exercise existing Product v2 regressions/legacy entrypoints and confirm no unintended Product source or behavior change.

### 2.2. Required LATER — retained architecture objective

`DEFERRED_PRODUCT_POLICY_BRIDGE` is **unfulfilled, not retired and not implemented**. The Architecture-wide intended end-state remains one common pure policy/Method metadata authority used via a legacy-compatible bridge by Product v2's `ScientificValidationService`, without broadening legacy Operation/Estimand semantics or changing Product v2 wire/API/DB.

The deferred bridge requires:
1. An explicit **separate Owner-approved, scheduled/in-scope integration work package**; do not silently attach it to an unspecified Gate, treat it as a license for P04 to edit Product source, or presume that later Gates will absorb it.
2. A design mapping of legacy estimator aliases and existing `ESTIMATOR_CAPABILITIES` semantics onto the canonical pure policy/metadata, including the correct legacy `validate_submission` Discovery/Identification early-return, Estimation upstream Result/Graph/Dataset validation, exception and scientific status classification, overrides and exact accepted/rejected configurations.
3. Verifiable same-semantics Product v2 regression for all existing Operations and supported estimator configurations, and independent check that the actual legacy service **delegates** to the common policy. Until then, no statement that Product and Local share a single live runtime policy authority.

### 2.3. G01_999 dependency is explicit, not waived

The prior G01_999 scientific/independent verification conditions (real FCI, MAG/PAG Oracle, BK, category/fisherz numeric/CI screening, OS/FS/Reader/Privacy, T2/T3 and Product regressions) remain unchanged. Separately, the **shared-policy integration architecture requirement is still unmet** while the Product bridge is DEFERRED. Its completion must be reported as `DEFERRED_PRODUCT_POLICY_BRIDGE / NOT_VERIFIED` and treated as a blocking dependency for **the relevant G01_999 acceptance item**, absent later explicit Owner-approved rephasing of that acceptance requirement. Do not claim `G01_999 PASS` solely because all Local P04 coding tests pass, and do not invent a new acceptance waiver.

This Owner choice defers implementation of one architecture dependency rather than retiring its requirement or automatically releasing downstream Gates. Its eventual integration stage and any acceptance rephasing need a separate explicit decision. In case of conflict, this scoped amendment sets the timing of legacy consumer migration but does **not** relax its final functionality or legacy compatibility.

## 3. Exact authorized changes and traceability

Changed normative documents:
1. `00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_61_causal_domain_ports.md`: permanent common pure eligibility and explicit G01-only deferred Product consumer connection.
2. `00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_62_local_execution_publication.md`: single Local Method authority, legacy table compatibility baseline, eventual single-Authority migration and G01_999 dependency.
3. `00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design/23_41_cli_scientific_ports.md`: Local Port dispatch and unchanged Product v2 call signatures; no false completed-bridge claim.
4. `10_enhance_instruction/G01/06_G01_P04_fci_backend_oracle.md`: P04 coding scope excludes legacy Product source; no duplicate new Policy tables; deferred dependency retained.
5. `10_enhance_instruction/G01/07_Ariadne_ENH-E11_G01_test_instruction.md`: Local pure-policy tests vs legacy Product behavior regressions and explicit unfulfilled G01_999 shared-policy item.

Decision evidence: non-normative `combined_review/242_20261123_g01_p04_product_v2_shared_policy_scope_decision_docket.md`, Owner record `combined_review/243_20261123_g01_p04_product_policy_sharing_B_owner_adopted.md`, plus this candidate.

Unchanged: RD scientific/functional requirements, LDD, BD, remaining IF/public Method schemas, completed P01/P03 instruction/code/tests/checkpoints, P02/P05 Product compatibility scope, `src/ariadne/product/application/scientific_validation_service.py`, Product v2 APIs and `ESTIMATOR_CAPABILITIES`, `uv.lock`, public E11 Schema Version, completed Product v2 entrypoints, other Methods/Gates and all FCI/PAG scientific semantics of AMD-001, AMD-002 and AMD-003.

## 4. Acceptance matrix and remaining risks

- **G01/P04 focused positive:** P1-M06 validated full capability request resolves and delegates to same pure Local eligibility authority; backend API/CI/config checks; FCI preflight/actual FCI fit according to previously frozen scientific contract. Local no duplicate mutable compatibility rule table.
- **Focused negative:** incompatible Method/Backend/Design/Inference rejected before FCI; legacy Product estimator ID is not an automatic valid P1-M06 Method; no silent fallback to Product or second Local registry, no Product source edits.
- **Product v2 preservation:** Existing Discovery/Identification early return, Estimation upstream lineage, legacy estimator aliases/parameter/type/strategy/overlap/adjustment semantics, existing failure classes and output wire behavior remain unchanged. Existing Product regression tests run, with evidence, and no tests weakened merely to match changes.
- **Deferred migration evidence:** actual Product v2 `ScientificValidationService` has **not** been rewired; record this as `DEFERRED_PRODUCT_POLICY_BRIDGE` with a separately owned follow-up and a concrete pending Owner decision on implementation timing/acceptance dependency. No G01_999 shared-policy PASS without accepted completion or formal rephasing.
- **Science:** Independent G01_999, MAG/PAG, Backend, category-domain, Fisher-Z numerical, BK and T2/T3 conditions remain prerequisites. No P04 checkpoint yet; no fit or independent science tests were performed by contract drafting.

## 5. Release control

**This document is an Author-prepared formal 09 candidate, not an already-approved 09.** Owner must separately approve `AMD-E11-G01-P04-004` formal 09. Then prepare new complete immutable Git SHA including 09 approval record, obtain separate Owner G01-S10 refreeze, and issue distinct S11 limited authorization for G01/P04/Trial01 at that SHA. Previous S10 `cbfdbdd6b91f3a2f889fe9b62c2a4ab286da6132` and S11 `DEC-G01-P04-003-S11-REAUTH-01` do not authorize new architecture staging semantics. No G01_999 acceptance, Product bridge completion, P04 Coding checkpoint or push is asserted.
