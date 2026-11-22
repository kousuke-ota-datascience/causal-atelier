# ENH-E11 S05-A B01/B02 — 200 Profile factoring and parity evidence (2026-11-22)

**Baseline and latest review candidate:** 5cefb48633392f3754ff2062f8fd37d08293b204. **Status:** `B01_LOSSLESS_FACTORIZATION_200_200 / B02_STATIC_AST_IDENTITY_PASS_200_200 / B02_JS_SUBSET_POSITIVE_NEGATIVE_PASS / B02_INDEPENDENT_DRAFT202012_VALIDATOR_NOT_RUN / B03_B04_B05_PENDING / CODING_NOT_AUTHORIZED`.

## What was actually executed

1. Used connected GitHub fetch to **read every one** of the 200 original draft JSON files (40 Methods except P1-M06 × five kinds). Parsed 200 JSON ASTs, preserved exact original Git blob SHA, and grouped by kind.
2. For each of five kinds, extracted only exactly identical top-level JSON Schema keys and identical property constraints across all 40 into a `shared_schema`. Preserved all other keys, `required`, per-Method `$id`, `const`, `enum`, `if/then/else`, `oneOf`, `additionalProperties`, ranges, patterns, and scientific fields in per-Method overlay.
3. For each kind, reconstructed 40 complete JSON Schema objects from the shared/overlay representation and verified **normalized whole-JSON-AST exact equality 40/40**. All five kinds = 200/200 identity PASS. This is mathematical **instance-acceptance equivalence at JSON Schema level** for the same resolver and implementation: the reconstructed schema is literally the same schema object, not merely an approximate rewrite.
4. Independently cross-checked all 200 `source_blob_sha` fields against the live Git Tree object's corresponding source paths: **200/200 exact Git blob SHA matches, 0 missing/changed**, confirming source inputs at current review commit.
5. Executed a purpose-built **limited JS JSON Schema evaluator** in Code Mode over all 200 reconstructed schemas using the actual keywords present in this corpus (type/const/enum/properties/required/additionalProperties/min/max/exclusive/array/unique/oneOf/allOf/if/then/else/pattern). Results: **200 valid generated positives accepted; 200 missing-required rejected; 200 unknown extra fields rejected; 150 mutated const rejected; 22 conditional-inference negatives rejected; total 772 examples, 0 mismatches**. Generated instances are synthetic *shape fixtures*, not science datasets or Backend API calls.

## Factored artifacts

- `23_api_interface_design/schema_drafts/method_profiles/factored/e11_method_config_factored_v1.json`: 40 exact overlays; common `$schema,type,additionalProperties`.
- `.../e11_question_profile_factored_v1.json`: 40; common research question ID/text, population, contrast plus shape.
- `.../e11_design_profile_factored_v1.json`: 40; common design_id/question_id plus shape.
- `.../e11_output_profile_factored_v1.json`: 40; B03 typed artifact requirement maintained for all 8 P2 CATE, P3-M05 event vector, P3-M12 SCM gaps.
- `.../e11_inference_profile_factored_v1.json`: 40; Method-specific requested/CI/point-only constraints retained, 22 conditional negatives exercised.
- `e11_method_profile_dispatch_registry_draft1.json`: 200 entries dispatch to the factored bundle + specific Method overlay, with old per-file source schema as SHA-pinned comparison baseline. **No active production registry was changed.**

## What has NOT been executed

Formal independent Python `jsonschema.Draft202012Validator.check_schema` and original-vs-reconstructed runtime fixture parity test in the checked-out repository: runner `combined_review/tools/e11_profile_factor_compiler.py` has been authored for that purpose but **not executed** here (the container cannot access the complete GitHub checkout). This remains a **required B02 check before Freeze**. All 200 original drafts have structural incompleteness of some scientific/Backend/output contracts; identity only preserves those same limitations. Cross-asset Lineage/Method/Estimand/Inference and non-scalar B03 result payload semantics require independent validation. Backend/Reference tests belong to S05-B/C; old Product v2 and operator/06/07 document updates belong to S06–S09. No Source/Tests/uv.lock/pyproject/canonical requirement write.

**No claim of independent scientific PASSED, Gate999, Contract Freeze, or Coding Authorization is made.**
