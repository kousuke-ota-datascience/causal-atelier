# PREP-02 F06 — Semantic Schema/Codec consistency and digest-binding contract

- Date: 2026-11-17 JST
- Classification: FLOW / cross-schema mechanical design candidate
- Authority: Owner DEC-PREP02-C (five IDs) + DEC-PREP02-D (strict canonical JSON) and [shared Ports](112_20261117_prep02_f03_f07_shared_port_signature_contract.md)
- Status: `WIRE_INVARIANTS_SPECIFIED / FULL_JSON_SCHEMA_NOT_VERIFIED / CODEC_RUNTIME_NOT_RUN / NOT_FROZEN`

## 1. Hash objects are not interchangeable

| Key | Digest of | Include own hash field? | Reader proof |
|---|---|---|---|
| `ContentRef.sha256` | actual opened **file bytes** | N/A, external reference | trusted dirfd bytes and exact-size/hash check |
| `request_hash` | JCS encoding of *validated full logical Study object*, including version and stable user-declared content refs | No request_hash exists inside Study | strict Study decode then canonical encoding |
| `Graph.content_hash` | **semantic graph projection** without the `content_hash` field, encoded by JCS | **No**; prevents hash recursion | recompute over all other Graph fields, compare `Graph.content_hash` AND external `ContentRef.sha256` of full Graph file |
| `manifest.json` self hash | forbidden | N/A | Marker outside Manifest only |
| `_COMMITTED.json.manifest_sha256` | exact published `manifest.json` bytes | N/A | reader hashes actual file |
| `manifest.request_hash` | exact same verified request hash as Study | N/A | compare Marker, Manifest, Study-derived binding |

**Graph decision candidate:** preserve existing Graph JSON `content_hash` but explicitly define it as **semantic projection digest**, not a hash of the entire Graph JSON that includes itself. The latter would be self-referential and impossible as an ordinary direct SHA256 equality constraint. Full Graph file byte-level provenance is held by `ContentRef.sha256`; both hashes must be verified. This semantic-projection convention is a draft requiring Reviewer approval, not an Owner-decided new version.

## 2. Canonical codec key/number contract

- RFC8785 JCS is an engineering candidate under adopted strict canonicalization. No Unicode normalization; recursively sort object keys by UTF-16 code units, preserve array order, ECMAScript finite IEEE754 number representation; no BOM/space/trailing newline.
- Treat raw `1e20` as an IEEE754 Number only when conversion is well-defined and the typed validator permits it. **Do not universally reject every number >2^53 solely by `isSafeInteger`**, as some large integers are exactly representable doubles; instead prevent undetected precision loss of input integer tokens and require explicit numeric type/domain rules. Numeric strings are never implicitly coerced.
- JSON and YAML input must reject duplicate keys **before** object construction and before JCS hashing. YAML anchors/aliases and resource growth must be bounded; no arbitrary constructors.
- Distinguish source bytes from semantic object equality: YAML key/whitespace reformat may produce same Study request hash if semantic value unchanged, but source file ContentRef hash still reflects raw bytes.
- `canonical_codec_version` in Manifest is mandatory for E11 version1 candidate; do not add it to old Product v2 reader.

## 3. Cross-output semantic joins

Required equality checks (beyond isolated JSON Schema):
- `Study.run_id = Result.run_id = Status.run_id = Manifest.run_id = Marker.run_id`.
- `Manifest.request_hash = Marker.request_hash = JCS(Study)` digest.
- `Study.method.id = Result.method.id = Manifest.execution.method` (while a discover-only run may have no Effect Result; this must be handled by a **typed operation-specific bundle contract**, not by dummy Effect).
- `Study.operation = Manifest.operation`. A `DISCOVER` or `IDENTIFY` stage cannot fabricate an Effect Result merely to satisfy a blanket Manifest `schema_dispatch.result` requirement.
- `Study.input` ContentRefs map to Manifest.lineage and Result references without hash/identity/parent-version loss. Graph Edit produces new version and source ref, not in-place mutable content.
- `point.availability`, `uncertainty.availability`, `science_acceptance` and technical state are independent; a successful scientific-negative run may have no point/CI.
- E11 strict decoder rejects unknown versions and aliases but preserves legacy v2 path separately; error `phase` distinguishes input schema failure exit2 from persisted corrupted readback exit5.
- `artifact keys` are unique, safe relative POSIX paths; `stat` normal regular file only; readback same byte count/hash/permissions/media. Row classes denied without independently attested Study approval.

## 4. New blockers discovered by cross-schema review

| Finding | Present draft gap | Corrective obligation |
|---|---|---|
| **F06-GRAPH-HASH** | Graph JSON requires `content_hash` but no self-exclusion semantics | Adopt precise semantic-projection digest + separate full file ContentRef hash, or remove self hash before Freeze |
| **F06-OPERATION-BUNDLE** | Manifest draft unconditionally requires Result/Status schema dispatch even for discovery/identification with no effect | Define operation-discriminated artifact/Result schema and absence rules; no invented dummy Effect |
| **F06-METHOD-CONFIG** | Study `method.config` is arbitrary JSON object | Strict Method Registry `config_schema` dispatch and unknown-key rejection before eligible execution; descriptor version bound in Manifest |
| **F06-JOIN** | Isolated schema validation cannot ensure same RunId/Method/Estimand/provenance across files | Semantic cross-file validator plus positive/negative fixtures |
| **F06-ERROR-PHASE** | Earlier error table mapped `SCHEMA_INVALID` to one global exit2 | Keep `ErrorPhase` and map persisted corrupted run to exit5, input to exit2 |

## 5. Gate tests and disposition

F06-SEM01 graph semantic vs file digest; F06-SEM02 raw YAML format stable logical Study identity, signed policy scope stable; F06-SEM03 discover-only bundle no dummy effect; F06-SEM04 correlated mismatched IDs/method/graph hashes reject; F06-SEM05 method-specific unknown config keys reject; F06-SEM06 input SCHEMA_INVALID exit2 vs corrupted readback exit5; F06-SEM07 unknown/legacy version and codec fail-closed.

Do not Freeze five Schema files merely because they parse. **Method-specific 41 config schemas and per-operation payload envelopes are explicitly unresolved.** Independent Architecture Review plus actual schema/codec/reader cross-file tests remain mandatory.
