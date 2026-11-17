# PREP-02 — Draft Schema static structural and vector check (2026-11-17)

- Kind: FLOW / static schema test evidence; **not** Draft 2020-12 meta-schema certification and **not** E11 product runtime test
- Branch: `prototype/ariadne_mvp` (review input latest SHA at test time)
- Checks: GitHub readback of six standalone draft schemas; each parsed as JSON; local `$defs` references resolved; basic keyword subset interpreted (type, const, enum, required, additionalProperties, pattern, numeric constraints, allOf/oneOf/if-then-else).
- **Implementation:** ad-hoc JavaScript subset validator executed in authoring environment; not a committed or formal JSON Schema validator. Do not use this to assert compliance with all Draft 2020-12 semantics.

## 1. Structural check

| Object | Local refs | Unresolved refs | JSON parse |
|---|---:|---:|---|
| Study | 7 | 0 | PASS |
| Graph | 1 | 0 | PASS |
| Effect | 31 | 0 | PASS |
| Manifest | 8 | 0 | PASS |
| Status | 0 | 0 | PASS |
| Commit Marker | 0 | 0 | PASS |
| **Total** | **47** | **0** | **6/6** |

All six exact Version identifiers match Owner-adopted values and the Marker contract, as declared by the schema files. F07's separate `e11_ar_inference_defs.schema.json` was previously parsed with 11 `$defs` and 0 unresolved local refs.

## 2. Positive and negative vectors — subset static check

| Case | Expected | Observed |
|---|---|---|
| Study well-formed v1 | ACCEPT | ACCEPT |
| Graph PAG with CIRCLE-ARROW endpoint | ACCEPT | ACCEPT |
| Result JSON example in 23_42 | ACCEPT | ACCEPT |
| Manifest with content refs | ACCEPT | ACCEPT |
| Status JSON example in 23_41 | ACCEPT | ACCEPT |
| Commit marker canonical identity | ACCEPT | ACCEPT |
| Legacy `causal-analysis-spec/2` on Study decoder | REJECT | REJECT |
| `../secret` ContentRef relative key | REJECT | REJECT |
| Old `{path,sha256}` alias in strict v1 | REJECT | REJECT |
| Extra Study root field | REJECT | REJECT |
| Unrecognized Graph endpoint mark | REJECT | REJECT |
| Unavailable Point with non-null value | REJECT | REJECT |
| `AVAILABLE` inference without payload | REJECT | REJECT |
| String `"Infinity"` as numeric Point | REJECT | REJECT |
| Marker hash with incorrect length | REJECT | REJECT |
| Manifest artifact path traversal | REJECT | REJECT |
| Unknown Status discriminator version | REJECT | REJECT |

**Result: 17/17 expected-vs-observed matches in a restricted structural subset.** Each positive has a synthetic or documentation fixture; synthetic zero SHA256 is syntax-valid but not actual bytes-integrity evidence.

## 3. Explicitly not verified

- Full Draft 2020-12 meta-schema test with a standards-compliant library; YAML safe parsing and duplicate keys; canonical UTF-8 bytes and hashing; exact command-line ABI.
- F07 mathematical set normalization; topology derivation; finite interval ordering; AR `EMPTY` choice; numerical weak-IV coverage, Type I error, independent reference and Method-specific inference.
- Atomic no-replace and post-crash fsync durability; private ACL/mount/user namespace policy; effective Parquet row/column restrictions and confidentiality; malicious boundary/race.
- Product legacy v2 runtime regression; Source-to-wire DTO equality for every dynamic Method; Independent Architecture Review verdict.
- Read-only documentation link check found two directory targets `schema_drafts/`; these are replaced with explicit `schema_drafts/README.md` to allow exact path checks.

**Status: STATIC_SUBSET_QA_PASS / SCHEMA_FREEZE_BLOCKED / RUNTIME_NOT_RUN / INDEPENDENT_REVIEW_NOT_RUN.**
