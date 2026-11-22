# ENH-E11 S05-B02 — 200 Profile bounded instance smoke (Author only)

**Date:** 2026-11-22 JST  
**State:** AUTHOR_V8_SUBSET_CHECK_COMPLETED / S05_B02_FORMAL_DRAFT202012_BLOCKED / S09_INDEPENDENT_NOT_RUN.  
**Pinned normative content revision:** 2e529a38f1bc19afba9bec693a9a828bb7e1f9de, also captured in s09_post_reconciliation_document_snapshot_draft8.json. The current branch may have evidence-only commits after this revision; verify actual HEAD before later review.

## 1. What actually ran

Using the connected GitHub reader, the Author fetched all five factored Method Profile bundles (method_config, question_profile, design_profile, output_profile, inference_profile), each containing 40 Method overlays. In a transient V8/JavaScript review checker the shared schema and overlay were merged at the top level with a merged properties object and required-key set. **This is not a standard Draft 2020-12 validator.**

Supported checked keywords: type, const, enum, required, properties, additionalProperties=false, pattern, minLength, maxLength, minimum, maximum, exclusiveMinimum, exclusiveMaximum, minItems, maxItems, uniqueItems, items, allOf, anyOf, oneOf, if, then, else. The Author synthesized shape-conforming positive inputs from each profile and negative mutations. No actual 200-file Python/jsonschema execution occurred.

An initial generated-fixture bug yielded six nonconforming positive examples for P1-M12 through P1-M17 design_profile: base_effect_hash had been generated as a short string, violating the existing 64-character hex pattern. Fixed the fixture generator to produce 64 hex characters and reran the complete set. This was a **test generator defect**, not a Schema finding.

| Profile Kind | Positive accepted | Missing required rejected | Unknown key rejected | Wrong type/value rejected | Additional negatives |
| --- | ---: | ---: | ---: | ---: | --- |
| method_config | 40 | 40 | 40 | 40 | — |
| question_profile | 40 | 40 | 40 | 40 | — |
| design_profile | 40 | 40 | 40 | 40 | — |
| output_profile | 40 | 40 | 40 | 40 | 40 wrong Method ID rejected |
| inference_profile | 40 | 40 | 40 | 40 | 22 requested=true / confidence_level=null rejected |
| **Total** | **200** | **200** | **200** | **200** | **62** |

**Observed: 862 checks, zero mismatches in the bounded JS predicate.** Acceptance cases=200; denial cases=662. This does not imply a proof of full JSON Schema equivalence, scientific validity or Backend capability.

## 2. Cross-contract checking

Independently retrieved the 200-entry Dispatch Registry, 40-entry Method Output Descriptor Catalog, five factored bundle files and 200 original source blob SHA entries in the draft8 inventory.

- Exactly 200 unique Method × Kind dispatch entries. No absent/duplicate pair.
- 200 source Schema file names in Registry match each factored overlay source_file; all 200 source_blob_sha values match the original blob SHA **recorded** in draft8.
- Each of the 200 merged Profile shapes has required descriptors and strict top-level additionalProperties=false.
- All 40 Output Catalog entries match the factored Output Profile const fields: method_id, operation, positive_artifacts, forbidden_artifacts, portable_result_schema, upstream_hashes_verified.
- P3-M04: syntactic DID_2X2 and STAGGERED coexist, but Output Catalog marks only DID_2X2 positive and STAGGERED DEFERRED, SCIENCE_CONTRACT_NOT_AVAILABLE, CAPABILITY_UNAVAILABLE, CLI exit 4. Schema acceptance is not scientific Method availability.
- P3-M06: Output Profile/Catalog require both result.json and its_components.json; the Reader/hash/HAC/level-slope scientific contract remains unverified.

Fixed blob SHAs of inspected bundles: design ca121006489986f243a702503832aac726bc2b5c; inference 2e1d19086fc1a74628d7d898fc407d27fcbd0a62; method_config c745234dd8b56d2bb42cf9006299934685fda8d2; output 63f08051212a9f3030b3668a8c57ed3060bc6d78; question 5624a88216b74667b8b7a7187a548b63a7d38d4f; Dispatch 77d1a538a0a0aec7cfca0fa4d345ac14245d1419; Output Catalog ff5cd4e9bbc4b7b26ff54e9bee5a43837a0eb8b8.

## 3. Evidence boundary

**This result is AUTHOR PARTIAL STATIC EVIDENCE, not S05-B02 PASS.** The author checker is a subset evaluator, not jsonschema.Draft202012Validator.check_schema. It neither proves equivalence for all possible instances nor independently re-executes the full original-vs-compiled AST comparison. The source files themselves were not loaded into a usable 200-file Python checkout.

Local container runtime checked: Python 3.13.5 with jsonschema 4.26.0; Python 3.12 unavailable, and direct git ls-remote failed because github.com DNS could not resolve. The Owner-approved isolated Linux Python 3.12 runtime and a separate independent Reviewer were **not accessed or executed**.

The existing review-only tool combined_review/tools/e11_profile_factor_compiler.py is the actual standard-validator parity runner; its execution on fixed git checkout in the approved 3.12 review environment is still required, including exact installed versions, lock, source/fixtures SHA, generated positive/negative cases and full report hash.

Separately remain BLOCKED: S05-B03 actual Result/Status/Manifest/Reader and non-scalar artifact cross-readback; B04 real DoWhy/EconML/Tigramite fitted inference APIs; B05 independent Method Science and AR algorithm acceptance; S09 genuinely separate semantic review. S10 Contract Freeze and S11 Coding Authorization **not granted**. This check modifies no app source, tests, pyproject, uv.lock or canonical Product requirements.
