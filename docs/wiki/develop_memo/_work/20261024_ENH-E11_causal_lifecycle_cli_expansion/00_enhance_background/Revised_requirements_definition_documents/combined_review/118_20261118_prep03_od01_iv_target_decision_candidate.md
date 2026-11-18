# PREP-03 / OD-01 — DoWhy IV target decision candidate

**Document class:** FLOW / Owner decision proposal; NOT normative stock design, NOT authorization.  
**Baseline:** 68fb0b64021cc9ff372a0a7e3f13a406638da08f / `prototype/ariadne_mvp`  
**State:** `OD-01_OPEN / TARGET_UNRESOLVED / G02_P02_NOT_FROZEN`

## 1. Immutable upstream decisions and issue

- `P1-M05` is DoWhy IV **IDENTIFY** only, never numerical ESTIMATE. 10_32 assigns DGP-006; NEG-006/007; REF-I03, REF-G01; no adopted concrete target.
- DoWhy's IV candidate/nonparametric-ATE display is not a proof of Ariadne LATE. Actual DoWhy API and IV expression must be validated at the effective pinned runtime version; backend labels cannot set causal Target. [DoWhy API](https://www.pywhy.org/dowhy/main/dowhy.html).
- G08 already distinguishes **B0** binary `Z/A` unadjusted `LATE_COMPLIER` (P3-M09/M10), **B1** covariate-adjusted `LINEAR_IV_STRUCTURAL_COEFFICIENT` (P3-M11). G04 DRIV `CONDITIONAL_IV_STRUCTURAL_SLOPE` is separate. Do not merge these.

## 2. Owner choice

| Option | Exact adopted scope if selected | Advantages / costs |
|---|---|---|
| **A (recommended)** | `P1-M05` identifies only **explicitly selected B0 LATE_COMPLIER** as conditional identification evidence; no numeric point | Reuses adopted B0, matches assigned DGP-006/REF-I03; imposes narrow strict design requirements |
| B | `P1-M05` accepts explicit B0 **or** B1 typed profiles; no implicit backend selection | Broader functionality but requires new B1 DGP/NEG/REF mapping, input profile and scope amendment |
| C | `P1-M05` returns only IV-candidate evidence with `REQUIRES_REVIEW`, never `IDENTIFIED` | Safest with uncertain backend semantics but cannot satisfy full positive identification AC without formal scope/AC change |

**No option is deemed Owner-approved by the preceding PREP-03 consolidated review.** Option A is a concrete proposal, not an assertion that DoWhy intrinsically identifies LATE from graph alone.

## 3. Proposed Option A implementation semantics

**Target and input:** Method ID `P1-M05`, Operation `IDENTIFY`, `EstimandRef.family=LATE_COMPLIER`, population `compliers`, treatment contrast A1−A0, `design_profile=B0_BINARY_IV`. Require exactly one binary excluded instrument `Z`, binary treatment `A`, specified intervention/outcome, unadjusted B0, nonzero first stage and prespecified IV independence, exclusion, monotonicity direction and consistency/SUTVA assumptions with explicit Design provenance. Assumptions must be declared and validated for structural consistency; their empirical truth is **not** established merely by a passing Graph validator.

**Proof:** On eligible conditional design and effective compatible DoWhy IV expression, return `IdentificationOutcome` bound to Question/Design/Graph/Content hashes with `IDENTIFIED` as a *conditional-on-assumptions* claim. Record assumption identifiers, provenance and supported target explicitly; do not cast backend default `nonparametric-ate` to LATE. If the effective IV API cannot support that proof mapping, refuse with `METHOD_INCOMPATIBLE` / `CAPABILITY_UNAVAILABLE`.

**Rejection:** absent/other Target ⇒ `IDENTIFICATION_TARGET_UNRESOLVED`; invalid Graph or IV design ⇒ `NOT_IDENTIFIED` or `REQUIRES_REVIEW` plus reason; weak/zero relevance ⇒ typed limitation and no eligible numeric effect/CI. Distinguish weak-IV statistical evidence from logically false graph assumptions. No silent B1 or DRIV fallback.

**Artifact:** IDENTIFY writes `study.json`, `status.json`, `identification.json`, `manifest.json`, `_COMMITTED.json` only if technically committed. **No** `result.json` and no estimator call. G08 alone owns B0 estimator/weak-IV inference.

**Test:** DGP-006 and independent REF-I03/REF-G01; NEG-006 relevance, NEG-007 invalid instrument, false/missing monotonicity, wrong target B1/ATE, nonbinary Z/A, changed hash, old v2 compatibility. Positive test proves *implementation adherence to conditional assumptions*, not that untestable assumptions are true in reality.

## 4. Normative propagation AFTER Owner adoption

1. Update the `P1-M05` entry in `10_32_scientific_method_scope.md` and `30_63_causal_method_adapters.md` with selected target/eligibility/status. Keep all Method41 IDs.
2. Align strict Method Config/Question/Design/Profile Schema and `23_41` typed dispatch; keep `30_61 IdentificationOutcome` and existing Product ABI unchanged.
3. Inline selected rules and positive/negative AC into `G02 06 / G02 P02 / G02 07 / G10 P04 / G10 07`, then re-audit Document Independency.
4. Continue `OD-01_OPEN` until this specific option is authorized. **No Gate Freeze / Coding Authorization / Science PASS**.
