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


## Owner採用 D-F07-EMPTY / D-F05-POLICY / D-F06-CODEC・ROW-EXIT（2026-11-17）

- Generic AR Confidence Setは`EMPTY` topologyの0 componentを受理。Effect schemaへ同じ規則を複製して更新。Method別just-ID拒否は科学的検証に残る。
- Study側`privacy.policy_ref`は入力であり、それ単体は行出力許可ではない。事前Policyの権威・Scope・Policy digestの証明が必要。
- E11 strict canonicalizationはOwner採用済み方向性。RFC8785 JCSを技術候補とし、Manifestに`canonical_codec_version`を持つDraft、`default=str`は禁止。実装・クロス言語検証は残る。
- Privacy/authorization denialはExit 3。No silent aggregate-only fallback。

[Owner決定記録](../../combined_review/decisions/95_20261117_dec_prep02_four_owner_choices.md)。**Schema drafts**でありFreeze済みではない。


## F07 EMPTY and E11 Canonical Codec — Owner four-choice update

- [DEC-PREP02-D](../../combined_review/decisions/95_20261117_dec_prep02_four_owner_choices.md) adopted generic mathematically `EMPTY` AR confidence sets. The `e11_ar_inference_defs` and embedded Effect Result `$defs` both contain `EMPTY`/`components=[]` and require nonempty components for nonEMPTY topologies. Semantic set validation and just-ID Method-specific nonempty assertions are separate.
- Owner adopted an **independent strict canonical Codec**, not a specific implementation standard. RFC8785 JCS is the engineering candidate, with [7 positive / 7 negative golden vectors](e11_jcs_golden_vectors.json) and [design reasoning](../../combined_review/107_20261117_prep02_jcs_codec_vectors.md). Proposed `canonical_codec_version=e11-json-jcs-rfc8785/1` has been added to the Manifest Schema draft; Python↔ECMAScript bytes conformance is **not verified**.
- Privacy authorization denial = CLI exit3; Policy proof must derive from independent preauthorization authority. The Study's `privacy.policy_ref` is only a reference and not standalone authorization.
