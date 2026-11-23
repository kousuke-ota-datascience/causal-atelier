# 219 — G01/P03 typed GraphProvenance proposed field-level contract and completed P02 compatibility audit

**Date:** 2026-11-23 JST  
**Status:** AUTHOR_PREDECISION_TECHNICAL_AUDIT / OWNER_CHOICE_REQUIRED / NORMATIVE_FILES_UNMODIFIED  
**Owner decision:** DEC-G01-P03-PROVENANCE-01 (A or B), plus separately **P02 Reader compatibility approval** if changes to completed P02 become necessary  
**Evidence branch HEAD before docket:** a40bd3f26dec78a69d5103c5c2877386022817dc  
**Frozen S10:** c37cd93d981a6d3777e20bd46b26bc3ae9b2c1f8  
**Completed P01/P02 checkpoints:** 9bff61f0eae25236f95f31f2cd3e7c81291f0167 / 3a76a0aa1698037354b284ba7b5a875300473ce6

## 1. Inspected exact contracts and actual implementation

- The public draft `23_api_interface_design/schema_drafts/e11_local_graph_v1.schema.json` requires provenance but currently only sets `{"type":"object"}`: neither method nor backend/CI/assumptions/source-parent fields can be validated from it.
- Study current public `e11_local_study_v1.schema.json` includes `method={id,backend,config}` and input ContentRefs `question,design,dataset`, with `graph=null,identification=null` for G01. The existing G01 typed Study parser fixes method `P1-M06`, backend `causal-learn`.
- Manifest current public `e11_local_manifest_v1.schema.json` has `execution={method,backend,inference_config,...}`, and `lineage={question,design,dataset,graph,identification}`. For G01 standalone positive, Manifest.lineage.graph is the **newly produced output graph** ContentRef, not an input or parent.
- P03 06 §6.3 enforces E11 Local Graph Product fields `version_id=null`, `parent_version_id=null`; §6.4 says `Graph.content_hash` hashes the JCS semantic projection **without its own content_hash**, while external ContentRef SHA hashes full graph.json bytes.
- Completed P02's actual `src/ariadne/interfaces/cli/local_causal/manifest_reader.py` `_validate_graph` only checks `type(graph["provenance"]) is dict` and JCS digest, **not** method/backend/CI/assumptions or source/parent field structure. Current Reader also checks the Study method/backend against Manifest execution (not against Graph provenance). If IF/Schema become stricter without integrating this extra validation in the Reader, the P02 readback contract will diverge.
- `src/ariadne/interfaces/cli/local_causal/study.py` validates method.id/backend and input refs; no P03 GraphProvenance implementation exists at this STOP.
- P02 `PACKAGE_READY` status asserts 120 developer tests (38 P02 + 69 P01 + 13 Product), ext4 real FS; **not** independent Gate acceptance. This record does not reproduce those tests.

## 2. Precise proposed A vocabulary — not yet binding

Propose the existing top-level `provenance` property contain **exactly** the following logical keys in current G01 DISCOVER:

| Key | Candidate type | G01 validation and authority |
| --- | --- | --- |
| `method_id` | nonempty string, G01 const `P1-M06` | Equal `Study.method.id` and Manifest.execution.method |
| `backend` | nonempty string, G01 const `causal-learn` | Equal `Study.method.backend` and Manifest.execution.backend; do not infer installed actual distribution from string |
| `ci_test` | enum `fisherz`, `chisq`, `gsq` | Derive from validated Method Config using existing P04/G01 06 option naming, not from caller claims |
| `assumptions` | candidate deterministic typed list of scientific assumption identifiers, unique nonempty strings | Must tie to validated Question/Design/Method effective assumptions; **authority vocabulary/empty-versus-required still requires review** |
| `source_refs` | object with `question`, `design`, `dataset` each as established 5-field ContentRef | Exact value equality to Study.inputs and Manifest.lineage, then real-byte ContentRef hashes verified by trusted file adapter/P02 |
| `parent_graph_ref` | nullable existing 5-field ContentRef | `null` for first standalone G01 DISCOVER; if real scientific successor, verify referenced actual complete file bytes against ContentRef SHA and validate referenced internal Graph semantic hash through trusted reader, reject cycle/self-parent |

Current G01 graph top-level `version_id=parent_version_id=null` remains unchanged. Current G01 requires `temporal=null`, `kind=PAG`; no new public top-level Graph keys or new schema_version. These candidate nested keys are **not approved** by the Owner and may be altered based on config/Question/Design actual data. In particular, an arbitrary assumptions list cannot be treated as verified science; a field name alone is insufficient. Schema-only validation cannot prove real source bytes or provenance, and Graph `content_hash` cannot stand in for referenced file `sha256`.

## 3. Delineated verification path

1. GraphEvidence.from_canonical_json: pure strict JSON/structural validation, semantic content_hash, node/edge/lag and typed provenance; no actual file IO or false claims of source-byte verification.
2. ContentReferencePort / P02 physical boundary: trusted directory FD + actual bytes + size/hash for each referenced Source/Parent ContentRef; no caller-provided-only digest as proof. Avoid provenance self-reference (no parent self-ref/cyclic content-hash).
3. P05 composition/integration: same validated Study/Manifest configuration and source refs; no silent CI/backend substitution.
4. Reader after commit: independent verification of committed Graph payload AND cross-file method/backend/config/source provenance; after schema hardening existing P02 `_validate_graph` implementation does **not** meet this requirement. Need choose whether to extend P02 Reader itself (completed-Package change) or inject/reuse new P03 pure provenance validator through an explicit interface, with clear P02 compatibility/rollback tests.
5. Separate genuine science audit: FCI/PAG and CI correctness requires actual P04 evidence and independent MAG/PAG reference; valid provenance is not scientific truth.

## 4. Protected completed-Package boundary: material P02 regression risk

**P02 is already PACKAGE_READY.** Its public Reader contract allows `provenance={}` if all other Graph envelope checks pass. Restricting the nested public schema can make previously accepted local Graph bundles fail readback. Conversely, preserving current P02 Reader without a P03-aware semantic validator permits forged/stale Graph provenance. This is a **real compatibility decision**, not merely a clarification of implementation detail.

The Owner's general principle forbids unilateral changes to completed P02 code/06/07. Therefore this audit does not edit completed P02 source or frozen G01 07. Should an Owner approve A, the subsequent author must separately assess how existing P02 fixture/readback semantics and P01 manifest pure projection are kept coherent and **obtain explicit Owner approval before modifying completed P02** if that is unavoidable.

Product v2 GraphVersion IDs and semantically distinct Version service remain separate. No retroactive rewrite of P01/P02 checkpoint SHA, no overwrite of previous P02 test report, no invented data.

## 5. Recommended Owner decision decomposition

- **DEC-G01-P03-PROVENANCE-01:** adopt A, a typed provenance sub-schema within public Graph (preferred for existing P03/GRAPH04 meaning), or B, formal reduction of scientific parent/source graph-local meaning.
- **DEC-G01-P03-P02-COMPAT-01 (conditional):** approve minimal completed-P02 Reader/provenance verification extension and corresponding regression tests **only if** A cannot be implemented compatibly without touching its completed implementation. The exact method/edited files should be specified before this second decision; approving A alone is **not** blanket approval to rewrite P02.
- After precise schema, full RD/LDD/BD/IF/DD/06/07 consistency, independently approve `AMD-E11-G01-P03-001` formal 09, then exact immutable full SHA S10 reFreeze and separate limited S11.

No substantive normative decision, freeze or reauthorization has been made by creating this technical audit.
