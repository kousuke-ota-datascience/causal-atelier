# PREP-02 F06 — Strict RFC 8785 JCS canonical bytes golden vectors (engineering candidate)

- Owner adopted **strict versioned canonical JSON**, not specifically RFC 8785, in [DEC-PREP02-D](decisions/95_20261117_dec_prep02_four_owner_choices.md).
- Engineering candidate: [RFC 8785 JCS](https://www.rfc-editor.org/rfc/rfc8785.html), internal codec identifier `e11-json-jcs-rfc8785/1`. **Not frozen** or independently reviewed.
- Machine-readable fixture: [e11_jcs_golden_vectors.json](../23_api_interface_design/schema_drafts/e11_jcs_golden_vectors.json).
- **Authored vector check:** an ECMAScript-recursive canonicalization reference reproduces the seven expected literal byte strings. SHA256 shown below was computed from those strings; there is no E11 runtime Codec yet.

## 1. Byte-level rule

`request_hash = SHA256(UTF8(JCS(validated typed E11 Study JSON)))`. Follow RFC 8785 I-JSON, ECMAScript Number serialization, **UTF-16 code-unit sorting of object keys**, recursive objects, unchanged array order, UTF-8, no BOM/extra spaces/newline, no Unicode normalization, reject nonfinite numbers, duplicate source keys, unpaired surrogates and unknown Python objects. High-precision/unsafe integers must be rejected or represented as explicitly typed strings rather than silently rounded; raw parser must reject lossy token conversion. Existing `hash_mapping(default=str)` is prohibited.

`ContentRef.sha256` is computed from *raw verified file bytes*, **not** JCS-normalized data. Commit marker `manifest_sha256` is the digest of **actual saved Manifest bytes**; `manifest.request_hash` binds logical Study. Proposed Manifest field `canonical_codec_version=e11-json-jcs-rfc8785/1` is a mechanical draft; separate from five Owner-adopted E11 payload version IDs.

## 2. Prepared positive vectors

| ID | Intended distinction | Expected canonical JSON | SHA256 |
|---|---|---|---|
| JCS-01 | recursive key order | `{"a":1,"b":2}` | `43258cff783fe7036d8a43033f830adfc60ec037382473548ac742b888292777` |
| JCS-02 | nested keys and array order | `{"a":[3,1,2],"b":{"a":false,"x":null}}` | `fb4b9242c68ddb389a89f1c29290dacc45fe8856e495f8dfeb924208564fd66c` |
| JCS-03 | Unicode NFC | `{"name":"é"}` | `2f16b8477146a1b2ba7d6bb7cf7c9979c191cc2838a107dbf5f0d920b4cb3ba1` |
| JCS-04 | Unicode NFD | `{"name":"é"}` | `6a547588c4055916e090ed61467326046dd52810679d03bfb84d862a7123522e` |
| JCS-05 | numeric -0 / exponent | `{"n":0,"small":1e-7,"whole":100000000000000000000}` | `705f738a525b8cfabf278db1bdb8fa3a0097e3687820d26803274d05cf0d5a0e` |
| JCS-06 | escaped characters | `{"a":"x\ny","z":"\u0000"}` | `6830f6845782b6844062beda598a7f64a53b32263ad5213e26726c5519415ce3` |
| JCS-07 | UTF16 key order | `{"😀":"smile","":"private"}` | `52b750f422a4624687ca1a14d19c97b40bc7678a129cce462934c47b3227966a` |

NFC and NFD strings are **not** collapsed (JCS-03 and JCS-04 have different digests). JCS-07 tests UTF-16 ordering that differs from Unicode scalar-value sorting.

## 3. Negative vectors, limits and Freeze conditions

See the seven `negative` fixtures in the machine-readable file. To Freeze, run a **real standards-compliant JCS encoder/decoder** in Python and an independent ECMAScript reference and compare exact UTF-8 bytes + hashes across all fixtures. Validate YAML duplicate-key/type behavior before constructing typed JSON. Prove Version dispatch, Method DTO and manifest/marker byte relationship; old Product v2 readback unchanged. Test failed/invalid encodings never yield a committed bundle.

Current status: `VECTOR_DESIGN_PREPARED / E11_CODEC_IMPLEMENTATION_NOT_RUN / FORMAL_CONFORMANCE_NOT_RUN / INDEPENDENT_REVIEW_NOT_RUN`.
