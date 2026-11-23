# 197 — G01/P01 post-implementation reverse alignment across RD/LDD/BD/IF

**Date:** 2026-11-23 JST  
**Status:** AUTHOR_DOCUMENT_RECONCILIATION_RECORDED / INDEPENDENT_AUDIT_NOT_RUN  
**Scope:** G01/P01 only, existing implementation contract → upstream stock documents (one-off exception requested by Owner).  
**Accepted P01 implementation checkpoint:** `9bff61f0eae25236f95f31f2cd3e7c81291f0167`  
**Authoritative technical basis for this audit:** `10_enhance_instruction/G01/06_G01_P01_local_contract_codec.md`; `30_detailed_design/30_60_cli_adapters.md` and `30_detailed_design/30_62_local_execution_publication.md`.  
**Prior P01 pre-change branch HEAD:** `de62870fb8526b2e7bad8ab4267e24d855fe3902`.  
**Reconciled upstream stock-document commit:** `e53e918697770c07e4f62dc83c11a13007ef77b5`.

## 1. Exception, scope and non-precedent

Normal normative control direction is **RD → LDD/BD → IF → DD → Coding Instructions 06 → tests 07 → implementation**. In this explicitly bounded **post-implementation P01** case, Owner directed `G01/P01のCoding Instructionと30_detailed_designを正本として、要件定義を修正`. This records a **one-time reverse traceability reconciliation**, not a general permission for coding to redefine or relax RD requirements. The old Requirement IDs/status/MUST grades and the independent Acceptance Criteria are unchanged. Where existing P01 behavior could be inconsistent with an existing hard Requirement, that would remain a defect subject to Owner decision, not be legitimized by reverse edits. No such Owner relaxation is assumed.

## 2. Exact source-of-truth hierarchy used here

- **Implemented P01 primary WHAT:** G01 `06_G01_P01_local_contract_codec.md` (strict validated Study, five-field ContentRef, deterministic JCS, immutable Manifest/evidence, G01 negative science code discriminator).
- **Stock DD authorities:** `30_60_cli_adapters.md` §9/§11/§12 for Decoder/ContentRef/LocalStudySpec, and `30_62_local_execution_publication.md` §4 for Manifest/evidence; neither file was edited in this P01-only reverse-alignment.
- **Reported implementation:** G01/Trial01 `20_implementation_reports/G01/Trial01/packages/E11-G01_01_P01__status.md`, PACKAGE_READY checkpoint `9bff61...`; report asserts 76 focused+Product regression tests passed, including 7 fixed RFC8785 positive byte vectors and synthetic negative bundles. **This is reported developer evidence, not an independent or fresh test run here.**
- **Control separation:** P01 pure typed validation cannot prove physical content identity, real Publisher/Reader, legitimate P04 science or G01_999 PASS; this separation is preserved in every revised upstream stock section.

## 3. Traceable cross-layer alignment

| Contract fact from P01 06 / 30_60 / 30_62 | Requirement refinements | LDD refinements | BD refinements | IF refinements |
| --- | --- | --- | --- | --- |
| e11-local-study/1 strict version and G01 DISCOVER/P1-M06/GRAPH_STRUCTURE input acceptance; no legacy implicit dispatch | `10_17` FR-201/203 | `21_40` typed invariants | `22_06`, `22_15` | `23_41` |
| Five-field ContentRef is lexical, actual root-bound bytes/FD belongs to P02/P05 | `10_20` NFR-029, `10_91` | `21_40` | `22_09`, `22_15` | `23_41`, `23_42` |
| JCS Study request hash, Graph semantic hash, artifact file-byte SHA and Marker Manifest-byte SHA are distinct | `10_20`, `10_91` | `21_25` | `22_09` | `23_42` |
| Manifest evidence factory checks Study↔Status↔lineage/descriptor pure joins; output Graph ref TrustedRoot-relative versus staged descriptor bundle-relative | `10_20`, `10_91` | `21_40` | `22_09`, `22_15` | `23_41`, `23_42` |
| Positive versus *synthetic* scientific-negative: closed singleton SCI_NO_ADMISSIBLE_PAG; no technical failure masquerade, real P04 negative scientific proof remains unverified | `10_17`, `10_91` | `21_40` | `22_06`, `22_09` | `23_41`, `23_42` |
| P01 is I/O-free; P02 secure FS, P03 Graph, P04 science and P05 integration/actual Status/Graph bytes | `10_20`, `10_91` | `21_40` | `22_09`, `22_15` | `23_41`, `23_42` |

**Revised stock documents (10 files):** `10_17_fr_api_cli.md`, `10_20_nfr_reproducibility.md`, `10_91_acceptance_conditions.md`, `21_25_value_canonicalization.md`, `21_40_integrity_constraints.md`, `22_06_family_causal.md`, `22_09_results_artifacts_lineage.md`, `22_15_schema_dependency.md`, `23_41_cli_scientific_ports.md`, `23_42_local_result_manifest_artifact.md`. Existing G01/P01 06, G01 07, 30_60/30_62 DD source of truth and P01 implementation source/tests remain unchanged in the P01 reconciliation commit.

## 4. Explicit residual risk and independent acceptance

The source-of-truth direction was reversed **only to synchronize text to an already implemented P01 contract**. This does not constitute independent science validity or assurance that the implementation is defect-free. Reported P01 P01 Test 76 PASS remains scoped to developer testing. Some constraints (especially true physical source ContentRefs, Graph science-negative provenance and secure publication) remain unimplemented or unverified until P02/P03/P04/P05 and independent G01 tests run.

Separate **G01/P02** contract amendment `AMD-E11-G01-P02-001` is still a proposed formal 09; its new Owner S10/S11 approvals are **not** inferred from this P01 reverse alignment. Because P01-upstream stock documents are now additionally modified, any future G01 S10 Freeze must pin the **final full Git SHA** that includes both the G01/P02 cross-layer work and this P01 exception record, and confirm no actual P01 06/code/test behavior drift.

## 5. Disposition

- `P01_IMPLEMENTATION_CHECKPOINT=HISTORICAL_PACKAGE_READY` at exact SHA `9bff61...`; keep intact, no redo solely for document reconciliation.
- `P01_06/07/30_60/30_62/SRC/TESTS=UNCHANGED_IN_P01_REVERSE_ALIGNMENT`.
- `RD/LDD/BD/IF=AUTHOR_RECONCILED` (not independent S09 PASS).
- `G01_P02_AMENDMENT_09=PROPOSED`, revised S10 and distinct S11 pending.
- `G01_999=NOT_PASSED`.

No new public JSON Schema, wire versions, Product v2 ABI, Method Science claims or acceptance relaxations were introduced.
