# AMD-E11-G01-P03-001 — GraphProvenance typed parent/source semantics (proposal)

**Date:** 2026-11-23 JST  
**Classification:** CONTRACT_DEFECT / PUBLIC_CONTRACT_SEMANTIC_DECISION  
**Status:** DECISION_CANDIDATE_ONLY / FORMAL_09_NOT_APPROVED  
**Gate/Package/Trial:** G01/P03/Trial01  
**Previous S10:** c37cd93d981a6d3777e20bd46b26bc3ae9b2c1f8; **observed Agent START_SHA:** 714da741d09b1722e0755bc97cbacc4fb6ad327d  
**Protected P01 and P02 checkpoints:** 9bff61f0eae25236f95f31f2cd3e7c81291f0167, 3a76a0aa1698037354b284ba7b5a875300473ce6

## Contract defect

P03 §6.1–6.4 requires GraphProvenance method/backend/CI/assumptions and verifiable parent/source references. Current e11-local-graph/1 schema defines provenance only as an object and neither IF 23_42 nor DD 30_61 specifies nested keys, hash target or exact rejection rules. Local version_id and parent_version_id are both strictly null. An implementation choice cannot be justified by the previous frozen WHAT.

## Pending Owner semantic decision

See `combined_review/218_20261123_g01_p03_graph_provenance_owner_design_docket.md`. Recommended A defines strictly typed nested provenance and real ContentRef source/parent hash joins inside the existing public property without new Graph top-level key/schema version. Alternative B formally relaxes GRAPH04 provenance guarantees and relies on Manifest lineage. These are **proposals**, not current normative requirements.

Upon Owner choice, draft precise schema, equality/nullable rules, backward-compatibility review and complete five-layer contract amendments; then submit formal 09, new S10 freeze and separate S11. Do not revise P01/P02 implemented code, 06/07, graph science or Product v2 without independent defect and authorization.

## 5. Owner decision — A adopted (post-candidate decision)

**Owner explicit direction on 2026-11-23:** 「A案（推奨）：既存 provenance 内に型付き契約を設け、実ContentRefと科学的親参照を検証する。こちらを採用する」。`DEC-G01-P03-PROVENANCE-01 = A_APPROVED`.

This Owner decision **approves the semantic strategy**, not the finished formal 09, not an automatic permission to edit completed P02 implementation, and not S10/S11. The author has now produced a complete, reviewable proposed normative package at commit `d0dbee56c806a0d8142492416fb3130f24456f0b`.

### Precisely proposed public GraphProvenance shape

The existing `e11-local-graph/1` top-level `provenance` object now declares `additionalProperties=false` and exactly these required keys, using already existing ContentRef 5-field definitions:

```json
{
  "method_id": "P1-M06",
  "backend": "causal-learn",
  "ci_test": "fisherz",
  "assumptions": [],
  "source_refs": {
    "question": {"identity":"...","relative_key":"...","sha256":"...","media_type":"...","schema_version":null},
    "design": {"identity":"...","relative_key":"...","sha256":"...","media_type":"...","schema_version":null},
    "dataset": {"identity":"...","relative_key":"...","sha256":"...","media_type":"...","schema_version":null}
  },
  "parent_graph_ref": null
}
```

Illustrative CI and ContentRefs above are placeholders, not actual references or evidence. In G01/P1-M06, CI must be exactly the validated Study Method `config.indep_test`, restricted to `fisherz/chisq/gsq`; method/backend agree with Study/Manifest; source_refs equal Study.inputs + Manifest.lineage for Question/Design/Dataset. `assumptions` lists unique *declared* assumption identifiers, **not** proven truth; empty array does not assert independent scientific verification and requires Method/Design provenance review for its adequacy. The first standalone G01 graph has a null parent; any later scientific successor must resolve an actual immutable parent Graph by a five-field ContentRef, validate actual full-file SHA256 and separately check its own Graph.content_hash over the parent's semantic JCS projection, and reject self/cycles. Local Product Graph Version IDs remain null.

### Original contract gap and scientific security preservation

The prior Graph Schema only had `provenance: {"type":"object"}`; P03/G01 07 nevertheless required parent/source method provenance verification. The new nested structure is a **publicly observable strictness change** to an existing property. The Author did not relax P03 scientific preservation, alter any top-level Graph wire field/version, coerce PAG to DAG, permit fabricated causal assumptions, or equate internal semantic graph hash to external actual-file hash.

### Cross-layer exact changed paths

- Requirement `10_17_fr_api_cli.md`, `10_91_acceptance_conditions.md`
- Logical data `21_40_integrity_constraints.md`
- Basic design `22_06_family_causal.md`, `22_15_schema_dependency.md`
- Interface `23_42_local_result_manifest_artifact.md`, `schema_drafts/e11_local_graph_v1.schema.json`
- Detailed design `30_61_causal_domain_ports.md`
- P03 Coding `06_G01_P03_pag_graph_version.md`
- G01 independent Test `07_Ariadne_ENH-E11_G01_test_instruction.md`

### Impact on previously complete packages — separate mandatory decision

P01 checkpoint `9bff61f0eae25236f95f31f2cd3e7c81291f0167` and P02 checkpoint `3a76a0aa1698037354b284ba7b5a875300473ce6` remain immutable and their code/tests unchanged. The P02 Reader currently enforces only `provenance is dict` plus valid internal Graph hash. Thus even if a P03 producer emits the new shape, the completed Reader would accept malicious or stale provenance after checksum recomputation. Existing previously valid graph bundles with `provenance={}` may now be rejected. Explicit Owner decision `DEC-G01-P03-P02-COMPAT-01` is required before modifying completed P02's `src/ariadne/interfaces/cli/local_causal/manifest_reader.py` and its focused tests for full readback parity. Do not retroactively declare the existing P02 checkpoint invalid or rewrite P02 without authorization. This is a bounded adapter/readback consistency repair, not an unrestricted P02 reimplementation.

### Approval sequence still pending

**Formal 09 Owner approval of `AMD-E11-G01-P03-001` remains PENDING**, after inspecting these exact changes and the P02 compatibility risk. Then select a revised provisional G01-S10 full Git SHA after all normative edits are finalized, and obtain a separately authorized G01-S11 before P03 coding. P02 Reader may only be edited following the additional explicit completed-Package compatibility authorization. No test was executed as part of this documentation revision.
