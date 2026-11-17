# PREP-02 DEC-PREP02-D — Four Owner choices implementation-alignment QA

- Date: 2026-11-17 JST
- Branch baseline: `prototype/ariadne_mvp` @ `c452f513be67fac4484362b42d6c9318825173f8`
- Owner decision: [DEC-PREP02-D](decisions/95_20261117_dec_prep02_four_owner_choices.md)
- Classification: FLOW / author static review and limited schema validation only
- **Overall: OWNER_DECISIONS_APPLIED_4/4 / STATIC_SUBSET_QA_PASS / SCHEMA_PORT_NOT_FROZEN / INDEPENDENT_REVIEW_NOT_RUN**

## 1. Post-adoption audit

| Decision | Evidence of applied design change | Remaining Gate obligation |
|---|---|---|
| D-F07-EMPTY | `e11_ar_inference_defs.schema.json` and embedded Effect `$defs.arConfidenceSet` are byte-equivalent JSON Objects; each supports `EMPTY` with components=[] and rejects nonEMPTY with zero components | Formal JSON Schema Draft2020-12 validation, mathematical set normalization, B0/B1 Method-specific nonempty and AR statistical oracle |
| D-F05-POLICY | F05 policy contract and 30_62 require separately authorized `VerifiedStudyPolicyEvidence`; requester supplied `privacy.policy_ref` alone is not authorization | Specific trust anchor, preauthorization/revocation, OS ACL/mount security integration tests |
| D-F06-CODEC | RFC8785 JCS engineering candidate documented with 7 positive/7 negative prepared vectors; Manifest draft requires `canonical_codec_version=e11-json-jcs-rfc8785/1` | Actual Python/JCS conformance and independent ECMAScript byte/hash fixture tests, version dispatch and Product v2 regression |
| D-F06-ROW-EXIT | F06 Error map, CLI 23_41 and 30_62 DD updated: row/privacy authorization denial uses exit3; no silent aggregate downgrade | Real CLI exit/redaction/row file absence negative tests |

## 2. Limited structural test results

Executed in the authoring tool environment using a **subset structural JSON Schema evaluator**, not an installed formal Draft2020-12 library and not E11 production code.

| Test | Expected | Observed |
|---|---|---|
| generic EMPTY/components=[] | accept | accept |
| EMPTY + one interval | reject | reject |
| nonEMPTY BOUNDED + no intervals | reject | reject |
| nonEMPTY BOUNDED + finite interval | accept | accept |
| EMPTY without inversion_evidence | reject | reject |
| unsupported topology | reject | reject |
| AVAILABLE + EMPTY confidence set + reason null | accept | accept |
| FAILED + no set + typed reason | accept | accept |
| AVAILABLE with typed FAILED reason | reject | reject |
| FAILED with AR confidence set still present | reject | reject |

**10/10 expected outcomes.** No official JSON Schema meta-schema or interpreter compatibility PASS is claimed. Neither set topology semantic-normalization nor mathematical AR rejection/reference tests have been executed.

## 3. Reference integrity

- GitHub working-copy schema/manifest and markdown fetched after all changes. The two AR `$defs` subtrees match exactly.
- Exact adopted Version strings remain `e11-local-study/1`, `e11-local-graph/1`, `e11-local-effect-result/1`, `e11-local-manifest/1`, `e11-local-status/1`. Proposed separate codec version is **not** a sixth Product payload discriminator.
- 13 core affected Markdown documents: **102 relative file links checked, 0 broken**.
- Historical guidance “always reject EMPTY”, “privacy exit unresolved” and “Owner decision pending” updated in current design text. Earlier review finding text remains historical evidence with explicit Owner resolution appendix.

## 4. Residual PREP-02 blockers

1. F07 full mathematical confidence-set topology/normalization, B0/B1 just-ID scientific invariants, independent AR reference and coverage.
2. F05 preauthorized Policy Trust Anchor, attestation, privacy/ACL/mount/system integration proof, 3 exit behavior.
3. F06 formal JSON Schema + codec implementation and cross-runtime golden hashes; exact typed Method DTO and Source contract.
4. F03 true Linux no-replace filesystem/renameat2/fsync/postcrash negative integration tests, F04 Port typing & legacy regression.
5. F12 **independent** written Architecture Review, per-Finding exit verdict; no artificial independent approval.
6. PREP-01 also remains IN_PROGRESS; no E11 coding authorization and no original canonical promotion.

**No code/uv.lock/Product/legacy runtime/Original requirement_definition modified in response to these Owner four-choice approvals.**
