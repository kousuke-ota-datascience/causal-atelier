# DEC-PREP02-D — F07 EMPTY / F05 Policy / F06 Codec・Row Exit Owner採用

- **Owner decision date:** 2026-11-17 JST (2026-11-17 02:47:33 UTC、user confirmation)
- **Decision authority:** User/Owner explicitly adopted **all four recommended Option A proposals** from [PREP-02 Freeze Readiness Matrix](../109_20261117_prep02_f03_f07_freeze_readiness_matrix.md).
- **Scope:** ENH-E11 Local CLI scientific/contracts. Supersedes pending Owner choice on these four points; does **not** reopen [DEC-PREP02 A/A/A](94_20261117_dec_prep02_owner_architecture_choices.md).
- **Status:** `OWNER_ADOPTED_4_OF_4 / SCHEMA_PORT_NOT_FROZEN / METHOD_SCIENCE_NOT_RUN / INDEPENDENT_REVIEW_NOT_RUN`.

## Adopted decisions

| Decision | Option | Owner-adopted rule | What is not automatically decided |
|---|---|---|---|
| **D-F07-EMPTY** | A | Generic AR confidence set may be **mathematically EMPTY** with `topology=EMPTY, components=[]`; successful test inversion with empty set is **not** automatically technical `FAILED`. For a just-identified B0/B1 configuration whose scientific assumptions imply nonempty AR set, EMPTY is rejected by a **Method-specific scientific invariant** and investigated, not accepted as a normal Method result. | Actual B0/B1 method assumptions, inversion test validity, confidence coverage and independent scientific oracle |
| **D-F05-POLICY** | A | Row-level export requires **separately bound, preauthorized Study policy evidence** with verifiable authority/provenance. A self-authored Study boolean or flag is not evidence of authorization. Keep Study request ∧ CLI flag ∧ verified policy ∧ private nondelegated OS root ∧ column/row restrictions. | Concrete policy signer/approval workflow, revocation and trusted store, mount/ACL attestation implementation |
| **D-F06-CODEC** | A | Define an E11-specific **strict, versioned canonical JSON** encoder and content hash with explicit numeric/string/Unicode/key-order rules and cross-runtime conformance vectors. Do **not** reuse Product `hash_mapping(default=str)` for E11 identity. | Exact chosen standard/algorithm is an **engineering design choice** subject to independent Port/Schema review, not an extra named Owner approval |
| **D-F06-ROW-EXIT** | A | Row-level export privacy/authorization **denial maps to CLI exit code 3** (input/security category), not config/schema code 2; forbid silent successful downgrade. | Actual CLI error types/implementation, external process invocation tests, logs/redaction acceptance |

## Scientific distinction for EMPTY

- `EMPTY` denotes a mathematically computed empty confidence set, with **valid inversion evidence** and `inference.availability=AVAILABLE`; it does not by itself imply a numerical failure or `science_acceptance=PASS`.
- `FAILED` denotes computation/validation failure to produce trustworthy inference, with `confidence_set=null` and a **typed reason**.
- Generic wire must be lossless for both states. Method-specific eligibility can reject EMPTY when justified by a proven particular just-identified construction.
- Evidence: [Davidson & MacKinnon, *Confidence sets based on inverting Anderson–Rubin tests*](https://academic.oup.com/ectj/article/17/2/S39/5056440) (paper: empty sets possible in overidentified setting, not in specified just-identified model); [Stata ivregress postestimation](https://www.stata.com/manuals/rivregresspostestimation.pdf) (distinguishes empty overidentified AR set from too-narrow inversion search bounds).

## Implementation and verification boundaries

1. Update shared `e11_ar_inference_defs.schema.json` **and embedded Effect Result schema** in lockstep, adding EMPTY branch with exactly zero components and retaining nonempty components for other topologies. Semantic topology/value/normalization remains code-validated.
2. Revise F07 analysis Contract, 30_61 Method/Class science contracts and 23_42 result design; accept EMPTY in generic Type/Codec but require Method-specific negative test for B0/B1.
3. Bind F05 to a separately authorized immutable policy artifact/authority, verify Study identity + allowed columns/max rows/root, check validity before staging rows. No boolean from user-supplied YAML is sufficient.
4. Implement F06 canonical codec with versioned bytes semantics and golden vectors, and set all privacy authorization failures to exit 3.
5. Owner decision approval is **not** Architecture Freeze or test PASS. Independent reviewers must inspect exact Source SHA, formal JSON Schema, FS/ACL/privilege implementation and relevant Science reference tests.

**Canonical original `docs/wiki/requirement_definition/` remains unchanged pending full ENH-E11 acceptance.**
