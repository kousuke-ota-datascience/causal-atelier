# 218 — G01/P03 GraphProvenance public contract gap — Owner decision

**Date:** 2026-11-23 JST  
**Status:** OWNER_DESIGN_DECISION_PENDING; NOT an approved 09/S10/S11  
**Decision ID:** DEC-G01-P03-PROVENANCE-01  
**Agent stop:** BLOCKED_CONTRACT_AMBIGUITY at 714da741d09b1722e0755bc97cbacc4fb6ad327d; P03 no code/checkpoint  
**Prior S10 normative SHA:** c37cd93d981a6d3777e20bd46b26bc3ae9b2c1f8  
**Protected P01/P02 checkpoints:** 9bff61f0eae25236f95f31f2cd3e7c81291f0167 / 3a76a0aa1698037354b284ba7b5a875300473ce6

## Direct findings

The checked-in public `23_api_interface_design/schema_drafts/e11_local_graph_v1.schema.json` has `provenance: {"type":"object"}` without nested required fields or hash joins. P03 06 §6.1, 6.3, 6.4 and DD `30_61` require preservation of scientific Method/Backend/CI/assumptions and scientific parent/source provenance, plus reference validation. IF `23_42` §5 requires source/hash preservation without specifying those nested keys. Both `version_id` and `parent_version_id` are fixed null in standalone Local Graph. The existing five-field ContentRef.sha256 hashes full artifact bytes, distinct from Graph.content_hash (JCS graph semantic projection excluding self-hash). No normative typed mapping from Graph.provenance to a parent or source ContentRef was found.

P02 PACKAGE_READY is independently recorded in the repository's G01 Trial01 report with checkpoint 3a76a0aa1698037354b284ba7b5a875300473ce6; P01 remains 9bff61f0eae25236f95f31f2cd3e7c81291f0167. No P03 work checkpoint was reported.

## Alternative A — recommended, requires Owner public-contract semantic approval

Define a strict typed **nested** `provenance` structure inside the existing `e11-local-graph/1` property, without new top-level Graph keys or new public schema version. Require and define exact method, effective backend, CI test and assumption representation, source ContentRefs and an optional scientific parent Graph ContentRef. The source refs reuse the established five-field ContentRef and are joined to actual validated Study and Manifest inputs for G01 (Question/Design/Dataset), with a precisely documented missing/nullability policy. A first standalone P1-M06 DISCOVER graph has no parent: parent=null; no fabricated Product GraphVersion ID. A real parent reference must resolve through a trusted root/ContentReferencePort to actual bytes satisfying ContentRef.sha256, and the referenced Graph's own content_hash must independently satisfy its semantic JCS projection. Reject absent/extra/inconsistent refs, unknown method/backend/CI, unsafe targets, wrong hash domain and false Product IDs. Preserve PAG endpoints, scientific ambiguity, Product v2, independent Science and G01_999.

This option **tightens the accepted values of an existing public JSON property**, and therefore requires Owner approval of that design choice before editing RD/LDD/BD/IF/DD, public Graph schema, P03 06 and G01 07. The Author then must settle exact key names/types and compatibility impact in the formal 09 before freezing, without treating this option narrative as an executable schema.

## Alternative B — not recommended

Keep provenance as unrestricted JSON and rely on Study/Manifest for source lineage. This avoids tightening nested public JSON but requires **explicit relaxation** of the currently approved P03/GRAPH04 graph-local scientific parent/source provenance round-trip guarantee. It is not a mere editorial correction and requires Owner approval and acceptance-impact analysis.

## Change process

If A is approved: inspect existing consumers and fixtures; define precise internal GraphProvenance value, public nested schema and cross-file validation at the proper abstraction; adjust requirements, logical data, basic design, IF/schema, DD 30_61, P03 06 and G01 07; limit P05 impacts to actual integration requirements. Preserve completed P01/P02 source/tests/checkpoints. Record a formal 09 amendment, obtain separate Owner formal 09 approval, new immutable full-SHA S10 freeze and separate new S11 before P03 resumes. Do not self-authorize an unspecified wire contract.

No normative Graph/06/07 files are changed by the present decision docket.
