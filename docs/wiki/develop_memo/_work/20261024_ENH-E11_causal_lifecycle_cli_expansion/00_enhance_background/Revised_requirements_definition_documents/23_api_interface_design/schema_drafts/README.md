# E11 Local v1 JSON Schema drafts — PREP-02

**Status: DRAFT / NOT_FROZEN / INDEPENDENT_REVIEW_NOT_RUN.** These schemas are not an implementation, runtime observation or acceptance PASS. Adopted Owner version strings are normative; field/union/codec details remain review candidates.

| Contract | Machine-readable draft | Version |
|---|---|---|
| Study | [e11_local_study_v1.schema.json](e11_local_study_v1.schema.json) | `e11-local-study/1` |
| Graph | [e11_local_graph_v1.schema.json](e11_local_graph_v1.schema.json) | `e11-local-graph/1` |
| Effect | [e11_local_effect_result_v1.schema.json](e11_local_effect_result_v1.schema.json) | `e11-local-effect-result/1` |
| Manifest | [e11_local_manifest_v1.schema.json](e11_local_manifest_v1.schema.json) | `e11-local-manifest/1` |
| Status | [e11_local_status_v1.schema.json](e11_local_status_v1.schema.json) | `e11-local-status/1` |
| Commit marker | [e11_local_commit_marker_v1.schema.json](e11_local_commit_marker_v1.schema.json) | `e11-commit/1` |
| AR/Inference definitions | [e11_ar_inference_defs.schema.json](e11_ar_inference_defs.schema.json) | Internal `$defs`, not an independent payload |

The Effect schema currently embeds the F07 AR/Inference draft `$defs`. This temporarily excludes `EMPTY` AR sets and **must not be frozen** until [REV-F07-01](../../combined_review/103_20261117_prep02_f04_f07_design_review_findings.md) is resolved. The separate [F06 contract](../../combined_review/106_20261117_prep02_f06_dispatch_codec_error_contract.md) fixes intended discriminator locations, old-v2 rejection and remaining canonicalization decisions. IDs/keys and required fields remain draft pending independent Architecture review.

The current schemas are structurally strict at top-level and some subobjects, but flexible method-specific `config`, `provenance`, `stochastic`, etc. are **intentionally not contract-complete**. Completing their typed definitions, duplicate artifact uniqueness, hash/cross-reference correctness, URI/path confinement, graph semantics and scientific inference is mandatory before Freeze. JSON Schema shape checking cannot prove scientific or OS security properties.
