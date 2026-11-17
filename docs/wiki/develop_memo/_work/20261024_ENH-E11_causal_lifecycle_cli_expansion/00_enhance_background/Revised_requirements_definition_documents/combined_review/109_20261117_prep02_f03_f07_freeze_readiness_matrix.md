# PREP-02 — F03/F04/F05/F06/F07 common Port/Schema Freeze readiness matrix

- Date: 2026-11-17 JST
- Type: FLOW / integrated design review, not an approval decision
- Scope: all common E11 Local architecture across 41 Methods; Method-specific 06/07 contracts remain Gate-scoped
- Owner decisions: DEC-PREP02 A/A/A are accepted; no change to Product/legacy lane
- **LATEST PROCESS UPDATE (2026-11-17):** [117 PREP-02 Common Design Baseline Freeze](117_20261117_prep02_common_contract_baseline_freeze.md)を最新の工程判断とする。**Architecture Core/Port logical interface/Version/Hash/Privacy/Publish不変条件を限定Freezeし、PREP-03へ進む**。本表の過去の`NOT_FROZEN`や未レビュー証跡は**検査時点の履歴**であり、Ownerの独立レビュー承認を再提出させるGateではない。実装後のFS/Schema/Science検証、Method別06/07は後続Gateの責務。`CODING_NOT_AUTHORIZED`は継続。

## 1. Finding disposition / exit evidence

| Finding | Contract completed this iteration | Design issue / blocker | Mandatory evidence before Freeze | Current |
|---|---|---|---|---|
| F03 | Linux `renameat2(RENAME_NOREPLACE)` API, no fallback, staging + file/dirfsync, complete readback, EEXIST retry, post-rename indeterminate recovery | Tested FS/kernel/mount/errno mapping and trusted dirfd implementation absent | barrier concurrency, unsupported FS, injected crashes before/after rename/fsync, readback | DRAFTED / OPEN |
| F04 | Product/Local independent Ports, 5 Product methods and 4 ArtifactStore methods mapped, typed Protocol candidates + staging-only sink, trusted root updated in DD | Concrete DTO constructors/return types, error types, regression test suite and independent reviewer pending | mypy/static Port integration, Product v2/legacy Regression, all 41 Method registry matching | REVIEWED_BY_AUTHOR / OPEN |
| F05 | Owner A: independently verifiable preauthorized Study Policy bound to study/scope; UID/ACL/mount/namespace, `S∧F∧P∧R∧C` | Concrete Policy trust anchor/approval/expiry/revocation, mount allowlist/ACL algorithm remain unverified | Security review; policy spoof/root/ACL negative tests; sentinel-row leak tests | OWNER_POLICY_ADOPTED / MECHANISM_OPEN |
| F06 | Owner A: strict versioned Canonical JSON; suggested RFC8785 JCS implementation, exit3 for Privacy/Policy denial; five version IDs + marker | Exact JCS Python/ECMAScript conformance, full Method DTOs, formal Draft2020-12/legacy v2 negative tests remain | Golden UTF-8 bytes/hash vectors + independent codec; CLI exit3/legacy integration tests | OWNER_CHOICES_ADOPTED / MECHANISM_OPEN |
| F07 | Owner A: generic 5-topology AR (including mathematically EMPTY), distinct from failure; common and embedded Effect schema updated | Method-specific B0/B1 just-ID nonempty invariant, mathematical union, inversion proof and independent reference tests outstanding | EMPTY/other sets property tests, B0/B1 negative and weak-IV science oracle | OWNER_EMPTY_ADOPTED / SCIENCE_VALIDATION_OPEN |
| F12 | reviewer package with finding matrix and current source/draft links | No independent reviewer has assessed committed snapshot | independent written F03–F07 verdict against frozen SHA and documented corrections | NOT_RUN |

## 2. Owner-adopted four decisions (mechanical and scientific validation pending)

| ID | Choice to ratify | Recommendation | Existing policy impacted |
|---|---|---|---|
| D-F07-EMPTY | A: Generic mathematical `EMPTY` with `components=[]`; Method-specific B0/B1 just-ID invariant separately. | **OWNER ADOPTED A**, see [DEC-PREP02-D](decisions/95_20261117_dec_prep02_four_owner_choices.md) | Mathematical/Science tests remain |
| D-F05-POLICY | A: Separately bound preauthorized Study Policy authority, not a self-declared boolean. | **OWNER ADOPTED A** | Trust anchor/approval protocol/negative proof remain |
| D-F06-CODEC | A: Independent strict versioned Canonical JSON, not Product default=str. | **OWNER ADOPTED A**; RFC8785 JCS candidate under review | Python/ECMAScript conformance and runtime fixtures remain |
| D-F06-ROW-EXIT | A: Privacy/authorization denial exits with CLI 3. | **OWNER ADOPTED A** | CLI behavior and redaction integration tests remain |

## 3. Freeze/implementation sequencing

1. **Owner decisions ratified (4/4, DEC-PREP02-D)**. Specify F05 Policy trust anchor, prove chosen strict Codec implementation/bytes, complete Method-specific DTO and B0/B1 EMPTY invariants; after review publish one frozen Port+Schema SHA.
2. Independent Architecture Reviewer assesses F03–F07 and F12 findings, exact Root/FS/Privacy threat model, scientific representability and old Product compatibility.
3. Execute required runtime FS/OS/schema smoke and per-Gate science acceptance at the correct authorized Gate; no stage is deemed PASS from this matrix.
4. PREP-01 remains open (class seven-section inventory and API runtime Contract checks). Full ENH-E11 scope is not reduced to initial Gate. Owner Coding Authorization is a separate explicit step.

## 4. References

- [F04/F07 Review](103_20261117_prep02_f04_f07_design_review_findings.md)
- [F03](104_20261117_prep02_f03_atomic_publish_contract.md), [F05](105_20261117_prep02_f05_trusted_root_privacy_contract.md), [F06](106_20261117_prep02_f06_dispatch_codec_error_contract.md)
- [Draft Schemas](../23_api_interface_design/schema_drafts/README.md)
- [Static subset QA](108_20261117_prep02_schema_static_subset_qa.md)
- [Prior F03/F05/F06 acceptance matrix](95_20261117_prep02_f03_f05_f06_acceptance_matrix.md)
- [Owner decision](decisions/94_20261117_dec_prep02_owner_architecture_choices.md)


## 5. Owner Decision Closure（2026-11-17）

The four decisions in §2 are now **OWNER_ADOPTED A/A/A/A**; [DEC-PREP02-D](decisions/95_20261117_dec_prep02_four_owner_choices.md). This closes **decision selection only**. Remaining blockers are technical/Scientific/Security review & Runtime proof. Generic AR `EMPTY` and B0/B1 scientific negative are distinguishable; Privacy denial CLI exit=3. Overall **NOT_FROZEN / CODING_NOT_AUTHORIZED**.


## 6. DEC-PREP02-D decision adoption trace and implementation conditions

Owner 2026-11-17 accepted all four A choices. See [Owner Decision record](decisions/95_20261117_dec_prep02_four_owner_choices.md). F07 Generic AR EMPTY wire updated in both schemas, D-F05 Policy reference requires independently authorized trust anchor, strict RFC8785 JCS is **engineering candidate** not an extra Owner ratification, D-F06-ROW-EXIT exit3 frozen as behavioral intention. Manifest `canonical_codec_version` is a draft machine-level field; await independent schema & cross-language validation. **Four Owner choices DONE, common Port/Schema Freeze NOT_DONE**.


## 7. Specific F03-F07 mechanical/scientific contract update（2026-11-17）

- [112 Cross-Port signatures & ErrorPhase](112_20261117_prep02_f03_f07_shared_port_signature_contract.md)：common validated object types, Publisher/Reader signatures, phase-aware CLI exit. `phase` distinguishes input Schema invalid exit2 vs stored readback invalid exit5.
- [113 F05 Trust Anchor](113_20261117_prep02_f05_policy_trust_anchor_candidate.md)：admin-bound verification key + signed preauthorized policy proposed; actual provisioning/key revocation/independent Security review OPEN. Same-UID self-approved policy remains invalid.
- [114 F06 Schema semantic joins](114_20261117_prep02_f06_schema_semantic_invariants.md)：Graph self-hash recursion resolved as projection-hash **candidate**; Manifest Effect discriminator may be null for non-Effect operations (with operation-specific validator required). 41 Method config schemas still OPEN.
- [111 F07 B0/B1 AR](111_20261117_prep02_b0_b1_ar_science_method_contract.md)：proposed HC1 AR statistic/quadratic inversion and conditional just-ID nonempty property; [115 limited numerical parity](115_20261117_prep02_f07_f06_limited_numeric_qa.md) shows B0/B1 8-point max difference ~7.1e-14 with statsmodels OLS HC1; **no Monte Carlo/Science PASS**.

**Gate:** common Mechanical/Scientific design has concrete review contracts. Exact FS, Security trust, schema/codec/Method41 runtime and F12 independent Architecture Review are outstanding. `PREP02_IN_PROGRESS / NO_FREEZE / NO_CODING_AUTHORIZATION`.


## 8. Pre-Freeze common review contract checkpoint

[116 reviewer checkpoint](116_20261117_prep02_f03_f07_review_submission_checkpoint.md) integrates [111 Science](111_20261117_prep02_b0_b1_ar_science_method_contract.md), [112 Port](112_20261117_prep02_f03_f07_shared_port_signature_contract.md), [113 Policy trust](113_20261117_prep02_f05_policy_trust_anchor_candidate.md), [114 Schema/Hash joins](114_20261117_prep02_f06_schema_semantic_invariants.md), [115 numerical/static QA](115_20261117_prep02_f07_f06_limited_numeric_qa.md). F04 App receives ValidatedStudy via CLI decoder; F06 Graph self-hash fixed as excluded-field semantic projection **candidate**, Manifest non-Effect Result discriminator null **with operation validator**. B0/B1 HC1 algebra has only limited statsmodels synthetic parity; still requires independent reference/coverage/degeneracy testing. Ed25519 admin Trust Anchor is an **engineering candidate**, not a new Owner decision. Overall **CONTRACTS_REFINED / PREP02_IN_PROGRESS / PORT_SCHEMA_NOT_FROZEN / F12_INDEPENDENT_REVIEW_NOT_RUN / CODING_NOT_AUTHORIZED**.


## 9. Independent review handoff — Owner authorized (2026-11-17)

[DEC-PREP02-E](decisions/96_20261117_dec_prep02_independent_review_submission_authorization.md) records Owner approval **to submit**, not approval of F03–F07 technical correctness or Freeze. [GitHub Issue #25](https://github.com/kousuke-ota-datascience/causal-atelier/issues/25) is **OPEN / REVIEWER_UNASSIGNED / INDEPENDENT_VERDICT_NOT_RUN**. Reviewer baseline: `6dd45982e389ea57deabd4eef7871af3fe111aab`. Each F03–F07 and F12 must receive separately evidenced independent disposition. `PREP02_IN_PROGRESS / PORT_SCHEMA_NOT_FROZEN / CODING_NOT_AUTHORIZED`.


## 10. Owner attestation of independent review completion (2026-11-17)

User states independent review has finished and approves it. [DEC-PREP02-F](decisions/97_20261117_dec_prep02_owner_independent_review_completion_attestation.md) records that **Owner approval is acknowledged**. However [Issue #25](https://github.com/kousuke-ota-datascience/causal-atelier/issues/25) had no reviewer findings, per-F03–F07 verdict, or assignment when checked; completion remains **independently unverified**, including possible off-platform work. Reviewer evidence/source SHA and dispositions must be reconciled prior to any Freeze. `OWNER_ATTESTED / REVIEW_EVIDENCE_PENDING / F12_UNVERIFIED / NO_FREEZE / NO_CODING_AUTHORIZATION`.
