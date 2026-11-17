# PREP-02 F06 — E11 v1 strict dispatcher, wire envelope, canonical bytes and errors freeze-preparation contract

- Date: 2026-11-17 JST
- Type: FLOW / machine-schema and DTO/Port compatibility draft
- Authority: [DEC-PREP02-C](decisions/94_20261117_dec_prep02_owner_architecture_choices.md) adopted five literal v1 identifiers
- Status: SCHEMA_DRAFT / DISPATCH_NOT_FROZEN / TESTS_NOT_RUN / INDEPENDENT_REVIEW_NOT_RUN

## 1. Discriminator table (normative Owner values; mechanical location draft)

| Artifact | Outer discriminator property | Exact accepted value | Parser |
|---|---|---|---|
| Local Study YAML (or JSON) | `schema_version` | `e11-local-study/1` | `E11StudyDecoder` |
| Graph JSON | `schema_version` | `e11-local-graph/1` | `E11GraphDecoder` |
| Effect Result JSON | `schema_version` | `e11-local-effect-result/1` | `E11EffectDecoder` |
| Manifest JSON | `manifest_version` | `e11-local-manifest/1` | `E11ManifestDecoder` |
| Status JSON | `schema_version` | `e11-local-status/1` | `E11StatusDecoder` |
| Commit marker | `marker_version` | `e11-commit/1` | `E11CommitMarkerDecoder` |

The five version **values** are Owner-adopted. Property name `manifest_version` matches existing `23_42` contract, marker is an additional non-circular reader guard. The strict decoder must require exactly one explicitly supplied expected identifier in the right slot: missing/null/unknown/legacy/wrong-kind discriminator = `VERSION_UNSUPPORTED` (different from correct-version malformed content = `SCHEMA_INVALID`). Do **not** invoke `CliManifest(manifest_version="2.0")` decoder as fallback for an E11 input and do not alter the existing v2 read path.

## 2. Canonical wire and ContentRef alignment

- Draft canonical ContentRef object: `{identity,relative_key,sha256,media_type,schema_version}`. `sha256` is lowercase 64-char hex. `relative_key` is a root-relative POSIX key; secure open is a separate F05/ContentRef obligation. `identity` is logical upstream identity and **is not** derived only from hash.
- Previous `23_41` example `inputs.question: {path,sha256}` and `23_42` example `design_ref:{id,sha256}` are **not** valid strict ContentRef wire representations. **Recommend replacing both examples** with canonical five-key form; no compatibility alias for new E11.
- Study input fields `inputs.question/design/dataset` required; `graph/identification` conditional on Operation. E11 validates method, Estimand and provenance hashes separately from JSON syntax.
- Default-free strict parser: YAML safe scalar/list/map, duplicate-key rejection, deep nesting/alias bounds, forbid arbitrary Python tags; canonical JSON strict no NaN/Infinity, keys and null types explicit. No implicit numeric-string coercion, no extra critical keys, unknown version fail-closed.
- `src/ariadne/infrastructure/config/hashing.py::hash_mapping()` currently uses `json.dumps(default=str,sort_keys=True,...)`. That is a **CURRENT Product helper**, **not** a valid strict E11 canonical identity implementation: unknown objects become strings, which loses type distinctions. Adopt a distinct versioned E11 canonical codec only after cross-language/float/Unicode/hash fixtures define its exact bytes; no change to Product helper without regression.
- Candidate hash identity: `sha256(canonical_json_utf8)` for a validated **logical** Study object and `sha256(actual_file_bytes)` for ContentRef raw artifacts. Canonical JSON version and string/float normalization are **unresolved**. Hash equality of file bytes is not a substitute for Design/Graph/Estimand identity.

## 3. Schema and Port boundary map

| Object | Schema draft | DTO/reader requirement |
|---|---|---|
| Study | `schema_drafts/e11_local_study_v1.schema.json` | `LocalConfigDecoder.decode_yaml` with strict version dispatch and validated Ref |
| Graph | `schema_drafts/e11_local_graph_v1.schema.json` | preserve PAG/CPDAG uncertainty and time/lag; semantic graph validator needed |
| Effect | `schema_drafts/e11_local_effect_result_v1.schema.json` | Point/Inference/Science separate axes; F07 AR definitions linked; independent Method inference |
| Manifest | `schema_drafts/e11_local_manifest_v1.schema.json` | no self-hash, relative artifacts, lineage, actual runtime; marker outside manifest list |
| Status | `schema_drafts/e11_local_status_v1.schema.json` | technical vs science axes, controlled stdout, no row contents |
| Marker | `schema_drafts/e11_local_commit_marker_v1.schema.json` | F03 marker manifest SHA256 + request hash, no circular reference |

All files are **drafts**, and a structural JSON Schema check cannot prove runtime OS integrity, scientific validity, statistical coverage or correct marker hashing.

## 4. Typed error registry and CLI exit map (candidate)

| Error reason | Category | CLI exit | Expected semantics |
|---|---|---:|---|
| `VERSION_UNSUPPORTED`, `SCHEMA_INVALID`, `METHOD_COMBINATION_UNSUPPORTED` | CONFIG | 2 | incorrect/mismatched local contract, no E11-to-legacy fallback |
| `INPUT_NOT_FOUND`, `INPUT_HASH_MISMATCH`, `PATH_CONFINEMENT_FAILED`, `ROOT_NOT_PRIVATE`, `ROOT_OWNER_MISMATCH`, `MOUNT_UNTRUSTED` | INPUT_SECURITY | 3 | unsafe or unverified input/output root, no trusted source |
| `CAPABILITY_UNAVAILABLE`, `BACKEND_API_MISMATCH`, `SCIENTIFIC_EXECUTION_FAILED` | BACKEND | 4 | optional module absent / API not supported / scientific computation technical exception |
| `RUN_ID_CONFLICT`, `ATOMIC_PUBLISH_UNAVAILABLE`, `MANIFEST_HASH_MISMATCH`, `ARTIFACT_HASH_MISMATCH`, `NOT_COMMITTED`, `STAGING_DURABILITY_FAILED`, `PUBLICATION_INDETERMINATE` | PUBLICATION | 5 | existing run not corrupted/overwritten; no false success |
| `PRIVACY_POLICY_UNVERIFIED`, `ROW_EXPORT_NOT_AUTHORIZED`, `ROW_EXPORT_COLUMNS_DENIED`, `ROW_EXPORT_LIMIT_EXCEEDED` | SECURITY | **unresolved (2 vs 3)** | explicit denied requested row export never silently published |

Scientific results such as `NOT_IDENTIFIED`, `PARTIALLY_IDENTIFIED`, `REQUIRES_REVIEW`, `INFERENCE_UNSUPPORTED`, `INFERENCE_EMPTY` must **not** be mapped mechanically to error exits; if packaged as a complete scientifically negative result, technical exit 0 is possible. Distinguish negative science from a syntactically invalid request. F07 EMPTY classification is pending Science/Owner review.

## 5. Freeze-negative and positive vectors

- Study duplicate YAML key, unknown tag, missing or wrong version; no alias for `path` at strict v1; confirmed canonical five-field ContentRef; invalid hash key/absolute path.
- Graph endpoint marks/lag loss and invalid node reference; effect finite/not finite, AR disconnected/topology/empty cases; status negative science and no positive science spoof.
- Manifest hash self-reference forbidden, duplicate/traversal key, missing runtime, wrong marker version or request hash, artifact bytes hash mismatch.
- v2 `causal-analysis-spec/2`/old `CliManifest` on E11 path rejected, legacy v2 reader still handles existing input untouched.
- Record actual serializer output bytes hash plus schema/codec version and run provenance, fixture sha and immutable Source SHA.

**Open freeze blockers:** canonical codec bytes, exact typed full schema composition and module Port signatures, privacy error exit map/policy authority, F07 EMPTY science rule, F03/F05 real system proof, independent Architecture Review. No coding or original canonical promotion.
