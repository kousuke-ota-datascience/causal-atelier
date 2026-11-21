# DEC-NFR034 — Conditional future delivery, not retired (2026-11-22)

## 1. Decision and reason

**Owner correction:** Externally sold/customer-delivered Ariadne has **not been decided**, so `NFR-034` must not be `RETIRED` as though the obligation had been permanently abolished. Adopt `MUST / DEFERRED / UNVERIFIED / FUTURE` within the explicit lifecycle vocabulary of `10_00_overall_RD`.

**Semantics:**
- `MUST` is conditional normative strength **if** customer distribution is explicitly adopted; it imposes **no current E11 implementation, runtime check, customer recipient workflow, SBOM generator or Gate PASS requirement**.
- `DEFERRED` retains NFR-034 as a future candidate, **not** a commitment to commercialize Ariadne. It preserves awareness that an actual release may impose license conditions. Its details are to be respecified once the distribution model and package set are known.
- `UNVERIFIED` remains because no implementation/accepted future delivery workflow is evidenced. `FUTURE` correctly denotes that the current local CLI enhancement is not its delivery scope.
- Relevant internal software-use and OSS licensing obligations remain governed by existing company processes, not by new E11 code.

## 2. Supersession of inaccurate current-state documentation

Record `133_20261122_internal_scientist_scope_reassessment.md` said `RETIRED`. That **status conclusion is superseded here**, not retroactively erased. Its analysis that customer-specific approval services, legal release status and SBOM generation are outside the current internal CLI scope **remains valid**. Preserve historical records 131–133 for traceability.

**Current authoritative files corrected:** `10_requirements_definition/10_22_nfr_security_compatibility.md` NFR-034 row (Status `DEFERRED`, Delivery `FUTURE`), current requirement explanation, and `22_product_basic_design/22_13_deployment.md` disposition. The current `10_91_acceptance_conditions.md` already excludes customer delivery checks and remains correct.

## 3. Boundaries and verification

All agreed science and reproducibility requirements, including 41 Method target semantics, NFR-029–033, NFR-035–036, AR Method-specific verification, local FS/row privacy and legacy Product compatibility, are unaffected. No customer-delivery automation or Product multi-tenant features are authorized. PREP-05 independent full audit, tests, Contract Freeze and Coding Authorization are still outstanding. No Source/tests/lock/canonical production documents altered.
