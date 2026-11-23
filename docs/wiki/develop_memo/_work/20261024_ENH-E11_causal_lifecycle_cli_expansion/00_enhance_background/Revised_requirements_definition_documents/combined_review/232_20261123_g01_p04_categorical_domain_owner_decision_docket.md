# 232 — ENH-E11 G01/P04/Trial01 categorical-domain authority contract gap — Owner decision docket

**Date:** 2026-11-23 JST  
**Status:** `OWNER_DESIGN_AND_ELIGIBILITY_SEMANTICS_DECISION_PENDING / NON_NORMATIVE_DOCKET`  
**Proposed decision ID:** `DEC-G01-P04-CATEGORY-DOMAIN-01`  
**Classification:** `CONTRACT_DEFECT / CATEGORICAL_DOMAIN_AUTHORITY_UNDEFINED`  
**Blocked Agent START_SHA:** `56889493d101b6c3c3a13a37dcd7cfd713dbf73a`  
**Approved S10:** `a7003b359444af64cad0edbade0341243653a8bf`  
**Approved S11:** `DEC-G01-P04-001-S11-REAUTH-01`  
**Completed P01/P03 checkpoints:** `9bff61f0eae25236f95f31f2cd3e7c81291f0167` / `858c9f73366036a2d1445e558135cd521f611462`  
**P04 checkpoint:** none. Actual stopped Agent reports no changes.

> **This docket is NOT a formal 09 amendment or permission to modify the frozen design/06/07/schema, and does not alter approved scientific acceptance.** The explicit Owner scientific/strict-input decision must precede normative changes, S10 re-freeze and S11 reauthorization.

## 1. Verified underlying contradiction

At the approved S10, `23_api_interface_design/schema_drafts/e11_p1_m06_fci_design_profile_v1.schema.json` has `variables[].additionalProperties=false` and only `name`, `measurement_scale` as allowed/required properties. The other `e11_g01_design_evidence_profile.schema.json` currently shares the same structure. `e11_p1_m06_fci_method_config_v1.schema.json` declares CI family/alpha/depth/path/BK, but no category set. The public `e11_local_study_v1.schema.json` has Dataset/Design ContentRefs, not a category vocabulary. The Product LDD `21_11_entity_dataset_view.md` mentions `DatasetVersion.schema_json`, but there is no approved G01 Local Dataset binding to this Product DB authority or canonical category set in that document.

The previously Owner-approved `DEC-G01-P04-CI-ELIG-01=A` requires all distinct unordered X/Y pairs and all S subsets to be screened before FCI; for chisq/gsq, all **declared** X/Y/S category combinations, including absent strata, must be assessed with expected counts >=5 per declared cell and no automatic recoding. Without a declared universe `C_v`, inputs whose observed values are `{0,1}` cannot distinguish `C_v={0,1}` from `C_v={0,1,2}`. Inferring `C_v=unique(observed)` would silently replace the adopted rule and make absent declared strata unobservable.

This is a missing *input authority* in Method-specific Design/IF, not a defect whose solution can be obtained by accepting the current Backend's `np.unique` behavior or changing test expectations to match an implementation.

## 2. Owner decision — option A (recommended): category codes in P1-M06 strict internal Design evidence

Add a **Method-specific internal Design field** `category_codes` to each categorical `variables[]` entry in `e11_p1_m06_fci_design_profile_v1.schema.json`, and align the coexisting G01 internal Design profile if it is genuinely used in P1-M06 validation (avoid two divergent validators). Keep existing G01 Design's immutable `design_id`/question link, variable order, `measurement_scale`, assumptions and BK. Proposed exact semantic contract:

- If `measurement_scale = CATEGORICAL`, require `category_codes` as a nonempty array of **at least two distinct JSON integers**, in **strict ascending numerical order**. Negative integers are allowed; boolean, fractional, float-form number representations, string and null codes are rejected. Do not silently renumber or require contiguous codes. This is the **complete declared support universe** for that variable, not only observed values; its finite integers must be representable exactly by the selected Dataset reader and Backend/NumPy integer dtype (checked explicitly).
- If `measurement_scale = CONTINUOUS`, `category_codes` is **forbidden**. In the Method's `fisherz` mode, every variable must be continuous; in `chisq/gsq`, every variable must be categorical, preserving the existing no-mixed-scale rule.
- The order of variable entries must match verified Dataset column order one-to-one. For each categorical variable `v`, every observed Data value must be a strict exact integer member of its declared `category_codes`. Missing/NaN/Inf/bool/noninteger/undeclared code rejects before FCI. An unobserved declared code must **not** be removed from the universe.
- Each `(X,Y,S)` and **each declared Cartesian product of categories for S** gets a check; if an S-combination has zero observed rows, preflight rejects. For nonempty S=s, test the **full declared X-by-Y table**, including absent X/Y cells, with independence-null expected counts for every declared X/Y combination. Expected count <5, zero marginal/zero df, or unsupported stratum rejects. Use same rule for S=empty (single global table), so unobserved levels of X/Y cannot evade checks.
- The category declaration is a **scientific Design statement**, not a claim the observed sample covers it or that asymptotic p-values are guaranteed valid. The strict Design object is already byte/hash-bound by existing `Study.inputs.design` five-field ContentRef, and P03 source-ref provenance may point to it without adding a new public Study/Graph/Manifest field or changing Product v2. Altering the Design's source bytes intentionally changes that Design SHA and therefore the Study request hash; do not silently reuse a prior request hash.
- The internal profile URI/version should remain unchanged **only after** an explicit Owner compatibility decision on tightening the existing unshipped strict Design input profile. No claim of backward compatibility for previously accepted category-free categorical Design documents: such inputs become invalid. Existing continuous Design inputs retain the same legal properties.
- Category-code arrays are immutable input evidence, never individual-row output. Report only aggregate support diagnostics (and existing privacy-safe error codes); never leak row values in stdout/logs.

### Example, proposal only

```json
{
  "name": "treatment_group",
  "measurement_scale": "CATEGORICAL",
  "category_codes": [0, 1, 2]
}
```

If data contain `0,1` only, code 2 remains declared and the exhaustive all-level preflight fails closed when its corresponding expected cells/strata violate the approved floor; this is not license to redefine its domain as `[0,1]`.

**Minimal impact after approval:** source-of-authority detail in `23_api_interface_design` (internal schema and method-binding description), `30_detailed_design/30_63` Method preflight, `06_G01_P04` input parsing and preflight, `07_Ariadne_ENH-E11_G01_test_instruction.md` positive/negative expectations, one new formal `AMD-E11-G01-P04-002` 09 amendment. Requirement FR/AR scientific meaning and BD boundaries remain unchanged unless precise review discovers a contradiction. LDD need not acquire a public Property/Entity just to express an internal Method Design field.

## 3. Option B: separate metadata source — not recommended

Specify a distinct immutable, typed, ContentRef-verified category-domain descriptor supplied alongside Dataset/Design. However, current public Study only has `inputs.question/design/dataset` and no extra domain ContentRef, so independently supplying it requires new authoritative binding/wire or treating existing Design bytes as an envelope anyway. This creates unnecessary API/lineage complexity and probable public Study-schema version compatibility work. Do not infer a new `Study.inputs.category_domains` field without Owner public-contract approval.

**Option C (not acceptable as a quiet fix):** infer categories from observed unique values, implicitly discard unobserved codes, or eliminate chisq/gsq positive coverage. These **contradict** the approved all-declared-categories policy and must not be presented as editorial corrections.

## 4. Exact minimal test and compatibility matrix for adopted A if approved

| Case | Expected Method-profile / preflight outcome |
| --- | --- |
| Continuous variable with no category_codes, fisherz | Existing shape valid subject to all other checks |
| Categorical variable with category_codes [0,1] and fully supported balanced counts | Domain valid; eligible only if every conditioning triple/cell passes the approved count rule |
| Categorical variable without category_codes | Strict internal Design invalid before FCI |
| Categorical variable with category_codes [0,1,2] but observed only [0,1] | Domain is [0,1,2], fail closed on missing support, never silently shrink |
| Categorical category_codes [0,2] | Allowed as noncontiguous integer labels if all observed are members; no coercion/renumbering as authority |
| category_codes [0,0], descending, fractional, boolean or string codes | Schema/semantic reject before Backend |
| CONTINUOUS with category_codes field | Strict Design reject |
| Observed 3 when category_codes [0,1,2] | Strict Domain-vs-Data reject |
| S combination exists in declared Cartesian domain but has zero observations | Reject before Backend even if marginal counts adequate |
| FCI `depth=0`, but all-subsets strict screen finds unsupported S | Preflight reject; no premature Backend fit |
| Existing P01/P03 ContentRef/provenance hashes | No source code modifications authorized; regenerate correct *new* Design/Study hashes for new inputs and test identical bytes/hash joins |
| Preflight cannot exhaust entire finite domain or suffers resource cap | Typed unresolved/blocked; zero Backend invocation, zero output |

**Potential regression:** categorical Design documents previously valid under the strict older profile will be rejected. This is a scientifically material input-compatibility tightening and **requires explicit Owner choice** despite no new top-level public wire version. The standalone Local G01 lane has no evidenced completed P04 producer or published categorical outcomes; completed P01/P03 generic ContentRef and Graph types should need **no code changes** but downstream behavioral integration and affected fixtures require tests. Do not edit completed P01/P03 instructions or code to make an old fixture pass.

## 5. Approval and stop boundary

Decision requested: `DEC-G01-P04-CATEGORY-DOMAIN-01` Option A vs explicit alternative, including the proposed strict `category_codes` contract and acceptance/compatibility tightening. If approved, author the *precise* small schema/IF/DD/06/07 revisions and formal AMD-002 candidate, then obtain separate formal 09 Owner approval, a new complete immutable S10 Owner refreeze, and distinct S11 reauthorization. The previous S10 `a7003b359444af64cad0edbade0341243653a8bf` and S11 `DEC-G01-P04-001-S11-REAUTH-01` remain historical approvals, not permission to implement a changed contract. Until this new material question is decided, **P04 Trial01 stays BLOCKED_CONTRACT_AMBIGUITY**.

No FCI fit, independent 07/G01_999 science test, source implementation, regression or P04 checkpoint has been produced by this docket.
