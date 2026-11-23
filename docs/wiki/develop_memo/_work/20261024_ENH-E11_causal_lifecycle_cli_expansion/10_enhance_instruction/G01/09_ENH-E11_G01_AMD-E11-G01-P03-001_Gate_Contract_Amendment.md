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
