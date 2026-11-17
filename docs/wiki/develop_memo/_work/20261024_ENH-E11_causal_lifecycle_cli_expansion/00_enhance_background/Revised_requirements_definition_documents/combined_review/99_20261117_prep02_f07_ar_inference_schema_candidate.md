# PREP-02 F07 — AR / inference / effect serialization contract candidate

- Date: 2026-11-17 JST
- Kind: FLOW / schema candidate + acceptance matrix; not final JSON Schema Freeze
- Owner-adopted discriminator for containing Result: `e11-local-effect-result/1` (DEC-PREP02-C)
- Status: CANDIDATE_PAYLOAD_AND_INVARIANTS / SCIENCE_TEST_NOT_RUN / INDEPENDENT_REVIEW_NOT_RUN

## 1. Separate scientific axes

| Axis | Contract and exclusion |
|---|---|
| Identification | `IDENTIFIED/NOT_IDENTIFIED/PARTIALLY_IDENTIFIED/REQUIRES_REVIEW/NOT_APPLICABLE`; cannot infer from successful Backend call |
| Point | `AVAILABLE` with finite JSON number, or `NOT_AVAILABLE/NOT_REQUESTED` with null + typed reason |
| Inference | `AVAILABLE` with exactly one typed valid CI or AR confidence set; `UNSUPPORTED/UNAVAILABLE/FAILED/NOT_REQUESTED` with no fabricated interval and typed reason |
| Science acceptance | `NOT_EVALUATED/PASS/FAIL/INCONCLUSIVE/BLOCKED/NOT_APPLICABLE`; this axis is independent from point/inference and from technical completion |
| Technical | `COMPLETED/VALIDATION_FAILED/CAPABILITY_UNAVAILABLE/EXECUTION_FAILED/PUBLICATION_FAILED`; scientific negative can be a technically completed run |

`science_acceptance=PASS` requires actual method-specific independent Gate 07 evidence, not a finite point or the presence of an AR interval.

## 2. Proposed tagged union for extended-real set

A mathematical endpoint must serialize as one of:
- `{"kind":"FINITE","value":x}`, x strictly finite JSON number
- `{"kind":"NEG_INFINITY"}` (lower endpoint only)
- `{"kind":"POS_INFINITY"}` (upper endpoint only)

Interval representation: `{"lower": endpoint, "upper": endpoint, "lower_closed": bool, "upper_closed": bool}`.

**Validation invariants (some require semantic code beyond JSON Schema):**

1. NEG_INFINITY only as lower and POS_INFINITY only as upper. Infinite endpoints are always open. Finite lower <= finite upper; equality only for one-point interval when both ends are closed.
2. Components canonicalized by lower endpoint, then upper; duplicate/overlapping intervals merge. Touching intervals merge exactly when the common endpoint belongs to at least one interval; if both exclude it, keep the single-point gap (DISCONNECTED).
3. Nonempty components are mandatory for normal `AVAILABLE` AR. Reject an empty set as a successful normal AR output **under the adopted E11 initial contract**; inversion/test failure must produce `FAILED + reason`. This is an E11 implementation policy, **not a claim that statistical confidence-set inversion can never mathematically yield an empty set**.
4. `ALL_REAL` iff the normalized union is (-∞,+∞). `DISCONNECTED` iff normalized component count >= 2. `UNBOUNDED` iff a single component has at least one infinite endpoint but is not ALL_REAL; otherwise `BOUNDED`.
5. `confidence_level` is a finite number strictly between 0 and 1. An `AR_CONFIDENCE_SET` must include a verified `inversion_evidence` ContentRef (confidence level, test statistic/critical value, grid/solver policy and diagnostic trace inside referenced artifact). Do not infer coverage from JSON validity.
6. `contains(beta)` accepts finite beta only; compare endpoints and closed flags exactly; null/NaN/Infinity inputs are not meaningful membership queries.
7. For `inference.availability = AVAILABLE`, require exactly one of `FINITE_INTERVAL` and `AR_CONFIDENCE_SET`, matching the Method's approved inference strategy. Other availability values force interval and confidence_set both null, reason non-null. `NOT_REQUESTED` may use a stable typed reason like `NOT_REQUESTED_BY_USER`; no success CI is implied.
8. Strict JSON serializer forbids bare NaN, Infinity, -Infinity, implicit int/float-string, unknown critical keys and Product v2 auto-coercion.

## 3. Canonical examples (schematic, not verified scientific coverage)

**All real, AR inversion:** 
~~~json
{"confidence_level":0.95,"topology":"ALL_REAL","components":[{"lower":{"kind":"NEG_INFINITY"},"upper":{"kind":"POS_INFINITY"},"lower_closed":false,"upper_closed":false}],"inversion_evidence":{"identity":"ar-proof-1","relative_key":"diagnostics/ar-proof.json","sha256":"0000000000000000000000000000000000000000000000000000000000000000","media_type":"application/json","schema_version":null}}
~~~

**Disconnected two tails, lossless:**
~~~json
{"confidence_level":0.95,"topology":"DISCONNECTED","components":[{"lower":{"kind":"NEG_INFINITY"},"upper":{"kind":"FINITE","value":-1.25},"lower_closed":false,"upper_closed":true},{"lower":{"kind":"FINITE","value":1.75},"upper":{"kind":"POS_INFINITY"},"lower_closed":true,"upper_closed":false}],"inversion_evidence":{"identity":"ar-proof-2","relative_key":"diagnostics/ar-proof.json","sha256":"0000000000000000000000000000000000000000000000000000000000000000","media_type":"application/json","schema_version":null}}
~~~

**Unavailable inferential evidence:** `{"availability":"UNSUPPORTED","kind":null,"interval":null,"confidence_set":null,"reason":{"code":"INFERENCE_UNSUPPORTED"}}`. This must not silently become an invented finite interval or `science_acceptance=PASS`.

## 4. F07 acceptance tests to implement and run at authorized Gate

| ID | Oracle / rejection |
|---|---|
| F07-01 | ALL_REAL, bounded, unbounded, two-ray disconnected strict JSON decode→encode→decode preserves mathematical set |
| F07-02 | Interval sort/merge normalized; gap at both-open common endpoint remains disconnected |
| F07-03 | Open/closed boundary membership; finite singleton; negative infinity only lower; positive infinity only upper |
| F07-04 | NaN/Infinity literal, numeric strings, empty successful AR, inverted endpoints, incorrect topology reject |
| F07-05 | AVAILABLE requires kind/one payload/inversion ref; UNAVAILABLE/FAILED/UNSUPPORTED/NOT_REQUESTED force null evidence and typed reason |
| F07-06 | CI null + science acceptance != PASS; valid point and missing CI do not imply science acceptance |
| F07-07 | B0/B1 weak-IV AR inversion agrees with independent reference and method-specific coverage targets (separate Gate07; not passed by roundtrip) |
| F07-08 | Legacy `causal-analysis-spec/2` / `CliManifest(2.0)` decoding and payload unchanged; E11 explicit dispatcher rejects old version |

The machine-readable schema candidate under `23_api_interface_design/schema_drafts/e11_ar_inference_defs.schema.json` checks shape only. Interval ordering, canonical union, method inference eligibility, numeric coverage and reference provenance are additional semantic validators; their absence blocks F07 Freeze.

## 5. Pending review points

- Exact reason code registry, error-to-exit mapping, and the science result/Manifest schema composition need a unified F06/F07 review.
- Distinguish AR **mathematical-set shape** proof from **statistical coverage** proof. No independent reference implementation or Monte Carlo run was executed.
- Do not promote draft schema to a deployed API or publish it as final until coupled Port/DTO/Serializer contracts and independent review are complete.
