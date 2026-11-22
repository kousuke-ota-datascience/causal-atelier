# S05 — factored Output Profile structural candidate (40 Methods)

**Status: DRAFT / NOT registered in active Method Registry / NO runtime-science PASS.**

The 40 original `e11_p*_m*_output_profile_v1.schema.json` drafts were inspected on 2026-11-22. They all specify the same six required keys, `additionalProperties=false`, with constant Method ID, Operation, positive/forbidden artifact lists, result-schema discriminator, and `upstream_hashes_verified=true`. These constraints are represented by `e11_common_output_profile_v1.schema.json` (a six-field base plus a mutually exclusive 40-Method `oneOf` dispatch), with traceable entries in `e11_method_output_descriptor_catalog_v1.json`.

**Not a 200-Schema replacement:** remaining Config/Question/Design/Inference drafts have Method-specific science and vary substantively. Output schema proof is currently structural inspection, not successful independent JSON Schema validator positive/negative parity, Method Backend science, or v2 compatibility proof. Do not delete 40 source draft files or change the live method discovery/registry until these tests are run.

**Per-Method required parity tests:** accepted baseline fixture and wrong Method ID, wrong Operation, wrong/omitted required output, false `upstream_hashes_verified`, unknown extra field, malformed result type, and mismatched actual Operation artifact Bundle. Compare old and factored validators over all 40 on fixed SHA. If any disagreement, fail-closed and keep the old Method draft active. All scientific DGP/NEG/REF, inference and Backend checks remain separate, including SCM point-only and weak-IV AR sets.

**Authority:** DEC-S02 (137), 10_32 §5, 10_91 §12.3. This stage is structural refactoring preparation, not Coding Authorization.
