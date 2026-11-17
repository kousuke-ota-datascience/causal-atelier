# PREP-02 F04/F07 — Source-based Design Review and Corrective Findings

- Date: 2026-11-17 JST
- Type: FLOW / architecture + scientific contract **author self-review** (NOT independent architecture review)
- Branch/base SHA: `prototype/ariadne_mvp` / `41739f03dbdfa2e4f8b25e3ff42afb6d71d15941`
- Inputs: [F04 Port ADR](98_20261117_prep02_f04_port_boundary_adr_candidate.md), [F07 Inference ADR](99_20261117_prep02_f07_ar_inference_schema_candidate.md), [F07 draft schema](../23_api_interface_design/schema_drafts/e11_ar_inference_defs.schema.json), [Owner decisions](decisions/94_20261117_dec_prep02_owner_architecture_choices.md)
- Disposition: **REWORK_REQUIRED** (2 critical semantic mismatches and 5 blocking mechanical issues); no Source implementation in E11, no runtime or independent scientific evidence.

## 1. Findings and disposition

| ID | Severity | Verifiable observation | Proposed corrective contract | Status |
|---|---|---|---|---|
| REV-F07-01 | **HIGH** | `99` §2.3 and `30_61` §6/12 reject a normal successful empty AR confidence set; scientific literature describes legitimately **empty** AR inversions in overidentified settings. | Define generic typed AR set `EMPTY` as mathematical set state, `components=[]` with inversion evidence. **Method-specific** B0/B1 just-identified configurations may reject EMPTY as an invariant, rather than asserting a universal fact. Technical inversion failure remains `FAILED + reason` and is different from a computed empty set. Final adoption requires Science/Owner decision and Gate-specific test. | BLOCKING SCIENCE DECISION |
| REV-F07-02 | **HIGH** | `23_42` published Result example uses `uncertainty.confidence_level`, `reason` string, no `interval` but F07 `$defs/inferenceEvidence` requires `interval`, typed `reason`, and confidence level inside the selected interval/set. Ref examples use `id/sha256` while local ContentRef requires `identity/relative_key/sha256/media_type/schema_version`. | Align Study/Result/Manifest examples and actual JSON Schema to one envelope; remove or flag non-conformant examples; do not silently accept aliases. | BLOCKING SCHEMA ALIGNMENT |
| REV-F04-01 | **HIGH** | `30_62` Publisher constructor takes `root:Path`, but F04 Port candidate requires `TrustedLocalRoot`; a raw `Path` gives no durable owner/mount/dirfd security attestation. | Explicit `TrustedLocalRoot` capability handle created after OS/ACL/mount checks; consume verified handle rather than re-trusting a string; revalidate mutable root/mount facts at write/publication boundary. | BLOCKING PORT ALIGNMENT |
| REV-F04-02 | **HIGH** | `30_62` §4.5 permits “no-replace primitive **or** verified process-wide/exclusive FS lock”. Owner DEC-PREP02-B chose effective **atomic no-replace filesystem primitive**, not a process lock substitute. | Remove FS lock fallback from normative contract. Candidate Linux `renameat2(...RENAME_NOREPLACE)`; unsupported FS/API fail-closed. | BLOCKING ADOPTED DECISION CONFLICT |
| REV-F07-03 | MEDIUM | `e11_ar_inference_defs.schema.json` uses numbers and structural `oneOf`, but cannot enforce finite lower<=upper, interval union normalization, topology equality, confidence-level consistency, or evidence quality. | Explicit semantic validator/test contract, not claims of schema-only round-trip PASS. Add finite and boundary negative fixtures. | OPEN VALIDATOR |
| REV-F04-03 | MEDIUM | `Validated*Request` proposed as a type alone; direct construction by untrusted callers could skip eligibility/hash checks. | Validation factory must own constructor access or verify the full invariant again before adapter call; type hints alone are not a security/science proof. | OPEN CONSTRUCTION CONTRACT |
| REV-F06-01 | HIGH | `23_41` Study sample uses `inputs.*.path`; Domain `ContentRef` uses `relative_key` and `identity`. No explicit mapping or exact object schema. | Choose one strict canonical v1 wire shape (recommend `ContentRef` fields), define exact schema/decoder, disallow implicit `path` alias under E11 v1. | BLOCKING F06 |
| REV-F05-01 | HIGH | `euid == st_uid` and `0700/0600` are not enough to prove non-shared, non-delegated access where mount/ACL/user namespaces expose bytes; initial Owner Option A rejects unverified. | Trusted root proof includes path component ownership/modes, ACL, mountinfo ID/type, user namespace/CI/container/delegation evidence; unavailable proof = deny; no row materialization before authorization. | BLOCKING SECURITY PROOF |
| REV-F03-01 | MEDIUM | A no-replace rename alone guarantees replacement avoidance, not complete crash durability. The spec requires marker/manifest/artifacts and file/parent dir sync but proof points must be ordered. | Stable staging snapshot → verify → fsync files & staging dirs → renameat2 no-replace → fsync source/destination parent dirs → verified readback; ambiguous post-rename errors lead to readback/recovery, not destructive retry. | OPEN MECHANICAL CONTRACT |

## 2. Source evidence and epistemic status

**Direct Source:** Product `src/ariadne/product/ports/scientific_core.py` blob `ccf89d307d626e7b4c82fe3f919230bb781d7f6a` (5 Product methods and Product-only Status); `product/ports/artifact_store.py` blob `e5bb990f9b69ef68df46a1559560ffb67b64caaf` (no multi-file commit); `interfaces/cli/manifest.py` blob `97216eca9d777e97f7a5ebd4e248afd31c6b4de0` (legacy version).

**External primary technical reference:** [Linux renameat2(2), RENAME_NOREPLACE](https://man7.org/linux/man-pages/man2/renameat2.2.html): destination existing returns EEXIST, filesystem support is required; EXDEV disallows cross-mount operation. [Linux fsync(2)](https://man7.org/linux/man-pages/man2/fsync.2.html): syncing file data alone does not necessarily persist containing directory entry. Both are guarantees of documented interfaces, **not evidence on the target Ariadne filesystem**.

**Scientific external:** [Confidence sets based on inverting Anderson–Rubin tests, Econometrics Journal](https://academic.oup.com/ectj/article/17/2/S39/5056440): AR confidence sets can be empty in the paper's overidentified settings; just-identified case differs. This is evidence against universal “EMPTY is impossible”, not proof that a particular B0/B1 implementation should output EMPTY.

## 3. Proposed disposition and required owner/science review

1. **F04 recommendation:** maintain parallel Local typed Ports (no unsafe cast to Product). Align Publisher to TrustedLocalRoot and selected no-replace syscall policy. These changes preserve Owner A/A/A and can be drafted without a new policy vote.
2. **F07 recommendation:** add `EMPTY` as a generic mathematically valid AR set topology with `components=[]`; distinguish from computational `FAILED`. For currently scoped just-identified B0/B1, accept EMPTY only if independent scientific review decides the specified estimator/test can produce it. **Science/Owner ratification pending**; do not quietly override existing draft.
3. **F06 recommendation:** strict canonical ContentRef on study wire and no alias; ensure envelope names and schema discriminators consistent across five v1 schemas and commit marker.
4. Review outcome = `REWORK_REQUIRED` until signatures, wire schema/semantics, security+FS proof and independent Reviewer findings are resolved. This **author self-review** never substitutes for independent Architecture Reviewer.

## 4. Required reviewers and evidence

- Scientific reviewer: F07-01 and Method-specific AR eligibility; numerical oracle + empty-set test + B0/B1 test assumptions.
- Architecture reviewer: F04-01/02/03, F06-01 and Protocol/DTO wire consistency.
- Security reviewer: F03-01/F05-01 trusted root, no-replace, durability, race/ACL/namespace negative evidence.
- All findings: capture immutable source SHA, approval/disposition, test/fixture SHA, no self-declared independent PASS.
