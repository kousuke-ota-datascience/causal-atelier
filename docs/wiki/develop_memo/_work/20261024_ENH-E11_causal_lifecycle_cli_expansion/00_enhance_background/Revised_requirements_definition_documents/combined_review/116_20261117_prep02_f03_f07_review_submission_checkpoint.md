# PREP-02 F03–F07 — Common Architecture Review submission checkpoint

- Date: 2026-11-17 JST
- Branch/Source baseline: `prototype/ariadne_mvp` @ `882f53d5d621fcbd32cc578c81abf69d1d063847`
- Type: FLOW / static integration QA and independent reviewer **submission input**
- **Disposition: DRAFT_CONTRACTS_INTEGRATED / STATIC_QA_PASS_WITH_LIMITS / INDEPENDENT_REVIEW_NOT_RUN / NO_FREEZE / NO_CODING_AUTHORIZATION**
- Owner authority: [DEC-PREP02 A/A/A](decisions/94_20261117_dec_prep02_owner_architecture_choices.md) and [DEC-PREP02-D A/A/A/A](decisions/95_20261117_dec_prep02_four_owner_choices.md). Owner choices not reopened.

## 1. Mechanical and scientific contract delivered

| Finding | Proposed contract / evidence | Design and review disposition |
|---|---|---|
| F03 | [104 no-replace/fsync](104_20261117_prep02_f03_atomic_publish_contract.md), [112 typed Port](112_20261117_prep02_f03_f07_shared_port_signature_contract.md), DD 30_62 aligned | Linux `renameat2(RENAME_NOREPLACE)` and readback specified. Runtime FS/kernel/mount support, crash and race proof NOT_RUN |
| F04 | [112 unified Port signatures](112_20261117_prep02_f03_f07_shared_port_signature_contract.md), [98 historical ADR](98_20261117_prep02_f04_port_boundary_adr_candidate.md), DD 30_61/62 aligned | Local Product separation; CLI decoder outside Application; concrete Façade vs internal Publisher class distinction explicit. Type-check, 41 Method config compat and legacy regression NOT_RUN |
| F05 | [113 independent Trust Anchor candidate](113_20261117_prep02_f05_policy_trust_anchor_candidate.md), [105 privacy](105_20261117_prep02_f05_trusted_root_privacy_contract.md) | Signed preauthorized Study Policy, privileged key store proposed; Study self-approval rejected. Admin authority/provision/revocation/ACL/mount tests and independent Security reviewer OPEN |
| F06 | [114 semantic digest/operation bundle](114_20261117_prep02_f06_schema_semantic_invariants.md), [106 version/codec/error](106_20261117_prep02_f06_dispatch_codec_error_contract.md), 7 [machine-readable Schema files](../23_api_interface_design/schema_drafts/README.md), [107 JCS vectors](107_20261117_prep02_jcs_codec_vectors.md) | Graph's semantic projection digest distinct from ContentRef file digest. Manifest's Result discriminator optional with Operation-aware validator. Formal Draft2020-12/JCS parser compatibility and Method41 config/schema/effective env NOT_RUN |
| F07 | [111 B0/B1 HC1 AR algebra and conditional nonempty](111_20261117_prep02_b0_b1_ar_science_method_contract.md), [115 synthetic parity](115_20261117_prep02_f07_f06_limited_numeric_qa.md) | B0 LATE vs B1 structural slope separated; generic EMPTY allowed. Just-ID nonempty requires gA≠0 and HC1 variance positive; zero first stage/rank/variance needs typed handling. Independent Science oracle and coverage NOT_RUN |
| F12 | [94 consolidated Architecture pack](94_20261117_prep02_architecture_review_package.md) | **Independent written verdict not collected** |

## 2. Static verification (author performed)

| Verification | Observed | What it is not |
|---|---|---|
| E11 JSON Schema parse and local refs | 7 schemas JSON-readable; **61 internal references / 0 missing** | full JSON Schema Draft2020-12 validator compliance |
| Generic AR vs embedded Effect `$defs` | exact ARConfidenceSet equality; EMPTY allowed and nonEMPTY empty list rejected in prior subset check | full set-topology proof and statistical coverage |
| Manifest decoder envelope | `schema_dispatch.result` admits explicit null; codec version `e11-json-jcs-rfc8785/1` required | valid operation bundles or actual codec implementation |
| Graph digest | schema description states digest over projection excluding own hash | runtime ContentRef/semantic digest verification |
| 41 Method inventory | `10_32` and `30_63` each contain **41 unique P1/P2/P3 Method IDs** | method_config schema/adapter/backend or science test completion |
| Modified document reference integrity | **15 main documents, 123 relative links, 0 broken** | all-repository link/anchor quality |
| AR numeric HC1 algebra | 8 β points each for B0 and B1 vs independent statsmodels OLS HC1; max absolute difference `7.105427357601002e-14` each | DGP coverage, production implementation, numerical root-domain certification |
| JCS fixtures | `hashlib.sha256(known canonical UTF-8 string)` matches **7/7** prepared digests | JCS conformance implementation tested across runtimes |

## 3. Independent Architecture Reviewer instructions (not review outcome)

Read one immutable GitHub SHA and trace F03–F07 across Port/Schema IF/DD/Security/Science. Record independently sourced findings: `finding_id, severity, source SHA/file/line, violated invariant, failure case, impact, fix, reviewer decision, evidence refs`. A reviewer shall not treat prepared self-review notes, SHA matching or syntactic Schema checks as independent approval.

Required review oracles:
1. F03 actual platform ABI and concurrent rename/no-clobber, fsync-after-rename fault and complete readback semantics; no fallback.
2. F04 compatible Python Protocols and validated typed constructors, no Product status conflation or legacy v2 regression.
3. F05 issuer/admin trust, key provenance/revocation and effective root ACL/mount/namespace; privacy deny exit3 and zero row bytes in temp files.
4. F06 JSON Schema Draft2020-12, safe YAML, JCS numeric/UTF-16 canonicalization, graph self-hash avoidance, operation-dependent Result presence, all output joins/errors, 41 Method config schema and DTO shape.
5. F07 HC1 test definition/calibration, conditional just-ID nonempty proof, rank/first-stage degeneracies, full-real-domain set inversion and Method-specific independent reference, valid-IV DGP/invalid-IV negatives.

## 4. Freeze blockers remaining, not waived

- **Architecture:** exact Class/Port module interfaces and ABI with tested implementation, external Product-v2 regression, F03/F05 Linux OS evidence.
- **Security:** actual authorized issuer, immutable admin trust-store provisioning/rotation/revocation and threat-model signoff; Ed25519 is engineering proposal not Owner-approved mechanism.
- **Schema:** complete operation-specific Bundle/Method41 config schemas, Graph semantic digest convention signoff, strict Codec reference implementation/cross-language checks, formal JSON Schema validation.
- **Science:** HC1 implementation and weak-IV AR numeric/coverage independent acceptance, handling of degeneracy/unknown tails, no substitute for per-Method Gate 07.
- **Process:** independent written F12 Architecture verdict and PREP01 remaining independent semantic/Class/API review.
- **No Product source, old `causal-analysis-spec/2`, `pyproject.toml`, `uv.lock`, original `docs/wiki/requirement_definition/` or E11 runtime implementation edited here.**

**Recommendation for next step:** independent F03–F07 Architecture/Security/Science review against a pinned exact branch SHA, with method-specific test acceptance deferred to authorized Gate 06/07. Do **not** mark PREP-02 PASS or permit coding from this static report.


## 5. Owner authorization to submit this checkpoint (2026-11-17)

[DEC-PREP02-E process approval](decisions/96_20261117_dec_prep02_independent_review_submission_authorization.md) authorizes independent review of this exact snapshot. [GitHub Issue #25](https://github.com/kousuke-ota-datascience/causal-atelier/issues/25) captures review scope, per-F03–F07 oracles, independent findings format, and test-evidence gaps. **Reviewer is not assigned and no independent verdict exists**. The original reviewer baseline remains `6dd45982e389ea57deabd4eef7871af3fe111aab`; this administration commit only records authorization and does not revise that frozen review snapshot.
