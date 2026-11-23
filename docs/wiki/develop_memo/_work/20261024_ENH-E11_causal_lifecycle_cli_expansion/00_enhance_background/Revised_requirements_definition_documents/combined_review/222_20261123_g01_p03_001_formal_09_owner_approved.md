# 222 — AMD-E11-G01-P03-001 formal 09 Owner approval

**Date:** 2026-11-23 JST  
**Decision:** `AMD-E11-G01-P03-001 / FORMAL_09 = OWNER_APPROVED`  
**Owner authorization (verbatim):** 「AMD-E11-G01-P03-001の正式09契約変更を承認する。DEC-G01-P03-PROVENANCE-01のA案とDEC-G01-P03-P02-COMPAT-01の限定変更許可を前提とし、既存P01/P02のチェックポイントと科学的・独立検証・G01_999受入条件を維持すること。」  
**Gate / Package / Trial:** G01 / P03 / Trial01  
**Category:** CONTRACT_DEFECT + PUBLIC_GRAPH_PROVENANCE_SEMANTIC_CONSTRAINT  
**Reviewed immutable source full Git SHA:** `52e5c60176d6b72c91f839ef267f46657bd380b5`  
**Normative five-layer + G01 06/07 revision commit:** `d0dbee56c806a0d8142492416fb3130f24456f0b`  
**Amendment/review alignment commit:** `c983c1541f8c7ad73b685b95be74b4ce7704ef3f`  
**Previous S10 frozen source:** `c37cd93d981a6d3777e20bd46b26bc3ae9b2c1f8`  
**P01 PACKAGE_READY checkpoint:** `9bff61f0eae25236f95f31f2cd3e7c81291f0167`  
**P02 PACKAGE_READY checkpoint:** `3a76a0aa1698037354b284ba7b5a875300473ce6`  
**uv.lock Git blob:** `2b83110e86b26b7969fbddf8f98a727370ae19f7`  
**Repository/branch:** `kousuke-ota-datascience/causal-atelier` / `feature/ariadne_mvp_e11`

## 1. Exact approved contract

Owner explicitly approves `AMD-E11-G01-P03-001` after previously approving A (`DEC-G01-P03-PROVENANCE-01`) and separately the bounded completed-P02 Reader compatibility exception (`DEC-G01-P03-P02-COMPAT-01`, record 221).

The contract preserves the existing `e11-local-graph/1` **top-level** shape and schema version, and tightens only the existing public `provenance` object's required structure to `method_id,backend,ci_test,assumptions,source_refs,parent_graph_ref`. Source refs are the existing five-field Question/Design/Dataset ContentRefs, which must equal the trusted Study and Manifest inputs and whose actual bytes must be verified at a trusted IO boundary; Method/Backend/CI match validated Study/Manifest, and first standalone G01 DISCOVER has parent Graph Ref null. A nonnull legitimate scientific successor parent has a trusted, independent full-file ContentRef digest and a separately validated internal Graph semantic JCS digest; self-parent/cycles, unsafe/stale refs, fake Product GraphVersion IDs and unexplained substitutions are rejected. Declared assumptions are **not** claims of independent scientific proof.

The semantic hash `Graph.content_hash=SHA256(JCS(Graph excluding content_hash))` remains distinct from `ContentRef.sha256=SHA256(exact completed graph.json bytes)`. Current Local Graph `version_id=parent_version_id=null` remains. No new public version/top-level field, Method-specific science relaxation or PAG-to-DAG coercion. Previous arbitrary-provenance payloads such as `provenance={}` can now become invalid; this is an explicitly reviewed **semantic compatibility tightening**, not a claim of unchanged acceptance.

## 2. Binding authority and impacted paths

- RD `10_17_fr_api_cli.md`, `10_91_acceptance_conditions.md`.
- LDD `21_40_integrity_constraints.md`.
- BD `22_06_family_causal.md`, `22_15_schema_dependency.md`.
- IF `23_42_local_result_manifest_artifact.md` and the existing public `schema_drafts/e11_local_graph_v1.schema.json`.
- DD `30_61_causal_domain_ports.md`.
- Coding 06 `06_G01_P03_pag_graph_version.md`.
- Independent Test 07 `07_Ariadne_ENH-E11_G01_test_instruction.md`.
- Formal 09 `09_ENH-E11_G01_AMD-E11-G01-P03-001_Gate_Contract_Amendment.md`; technical audits `218,219,220`; approved P02 compatibility `221`.

The limited P02 Reader modification permission is **not** a new authority to rewrite Publisher, FD/privacy/atomic publishing, P01, Product v2, or original P02 checkpoint. The old P01 `9bff61f0eae25236f95f31f2cd3e7c81291f0167` and P02 `3a76a0aa1698037354b284ba7b5a875300473ce6` remain preserved, as does Trial01 unless a separately established Gate FAIL/08 occurs.

## 3. Frozen WHAT vs current administrative HEAD

This Owner statement approves **formal 09 only**. Existing limited G01 S11 record 216 is bound to former immutable WHAT `c37cd93d981a6d3777e20bd46b26bc3ae9b2c1f8` and is insufficient for P03 implementation of amended provenance contract. A separate Owner `DEC-G01-P03-001-S10-REFREEZE-01` must choose the revised provisional G01-S10 full SHA (candidate: `52e5c60176d6b72c91f839ef267f46657bd380b5`), followed by an **independent new limited S11 Owner authorization** for G01/P03/Trial01. The S10 SHA is immutable even though this administrative record 222 and its docket are committed later.

No P03 code, P03 tests, P02 Reader retrofit, official P03 checkpoint, real FCI scientific validation, independent B02–B05/S09/G01_999 or Product release is claimed by this approval record.
