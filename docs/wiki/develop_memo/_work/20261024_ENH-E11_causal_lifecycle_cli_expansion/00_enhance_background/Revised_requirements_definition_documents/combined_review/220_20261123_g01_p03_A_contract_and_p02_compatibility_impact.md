# 220 — G01/P03 A-approved GraphProvenance cross-layer audit and P02 compatibility gate

**Date:** 2026-11-23 JST  
**Owner decision:** `DEC-G01-P03-PROVENANCE-01=A_APPROVED`  
**Formal 09 status:** DRAFT/OWNER_APPROVAL_PENDING  
**Revised normative files committed at:** `d0dbee56c806a0d8142492416fb3130f24456f0b`  
**Prior immutable S10:** `c37cd93d981a6d3777e20bd46b26bc3ae9b2c1f8`  
**Existing PACKAGE_READY checkpoints:** P01 `9bff61f0eae25236f95f31f2cd3e7c81291f0167`, P02 `3a76a0aa1698037354b284ba7b5a875300473ce6`

## Semantic authority hierarchy

RD requires lossless scientific provenance; LDD fixes identity and valid source/parent references; BD distinguishes Local immutable graph from Product GraphVersion; IF defines typed nested public provenance and unchanged public top-level version; DD owns pure vs physical validation boundary; P03 06 implements new GraphEvidence; G01 07 tests both positive cases and adversarial semantic mismatches.

## Exact nested key matrix

| Field | JSON Schema | G01 semantic binding |
|---|---|---|
| method_id | required nonempty string | P1-M06 equals Study.method.id/Manifest.execution.method |
| backend | required nonempty string | causal-learn equals Study.method.backend/Manifest.execution.backend |
| ci_test | required nonempty string or null | G01 must equal Study.method.config.indep_test; one of fisherz/chisq/gsq |
| assumptions | required unique list of nonempty strings | declared assumptions; **never a verified assumption claim**; review completeness with Design/Method |
| source_refs | required object: question/design/dataset each existing 5-field ContentRef | exactly equals Study.inputs and Manifest.lineage input refs; actual bytes via trusted ContentReferencePort |
| parent_graph_ref | required null or existing 5-field ContentRef | first standalone G01 null; real successor validates actual full Graph bytes SHA and internal semantic hash; reject self/cycle |

No new top-level Graph property or version is introduced. Local Product ID fields remain null. Graph.content_hash (JCS graph projection without self) and ContentRef.sha256 (exact completed Graph file bytes) are distinct.

## Safety and compatibility analysis

A public nested schema strictness change can reject old `provenance={}` data previously accepted. It is not valid to claim wire acceptance equivalence because the top-level schema_version is unchanged. Completed P02 Reader `src/ariadne/interfaces/cli/local_causal/manifest_reader.py::_validate_graph` currently checks only graph structure/provenance=dict/hash; the hardening must be enforced on independent readback as well. P03 new pure validator can be reused but cannot alone constitute verified P02 readback. Proposed targeted P02 changes would be Reader semantic Graph provenance cross-file validation plus focused regression, without changing Publisher FS/PrivacyDecision, P01 pure code, published marker, or package history.

**Mandatory separate Owner permission:** `DEC-G01-P03-P02-COMPAT-01` before modifying completed P02 code/tests. Choice: approve bounded P02 Reader repair (recommended) or retain historical Reader and explicitly make P03 strict readback Gate acceptance BLOCKED (not a viable final PASS). This is **not** implicitly included in A choice.

## Unverified areas

No actual existing released Graph bundles were inventoried for migration, and no source/test suite was executed by this Author revision. A full compatibility pass requires scanning accepted fixtures/consumers and validating E11 readback against the strict payload. Genuine P04 FCI negative/PAG truth, independent G01 07/S09/G01_999 remain unwaived.

## Current control plane

Owner A is adopted; drafted 5-layer+06/07 and Graph schema are on branch; `AMD-E11-G01-P03-001` formal09 not Owner-approved; new S10 and separate S11 not issued. No source change to P01/P02, and their checkpoints remain recorded.
