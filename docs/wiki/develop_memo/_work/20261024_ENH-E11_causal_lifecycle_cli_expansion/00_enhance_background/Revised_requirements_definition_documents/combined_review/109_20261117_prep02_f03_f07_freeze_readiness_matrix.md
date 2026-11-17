# PREP-02 — F03/F04/F05/F06/F07 common Port/Schema Freeze readiness matrix

- Date: 2026-11-17 JST
- Type: FLOW / integrated design review, not an approval decision
- Scope: all common E11 Local architecture across 41 Methods; Method-specific 06/07 contracts remain Gate-scoped
- Owner decisions: DEC-PREP02 A/A/A are accepted; no change to Product/legacy lane
- **Overall state: DESIGN_REFINED / PORT_SCHEMA_NOT_FROZEN / INDEPENDENT_ARCH_REVIEW_NOT_RUN / CODING_NOT_AUTHORIZED**

## 1. Finding disposition / exit evidence

| Finding | Contract completed this iteration | Design issue / blocker | Mandatory evidence before Freeze | Current |
|---|---|---|---|---|
| F03 | Linux `renameat2(RENAME_NOREPLACE)` API, no fallback, staging + file/dirfsync, complete readback, EEXIST retry, post-rename indeterminate recovery | Tested FS/kernel/mount/errno mapping and trusted dirfd implementation absent | barrier concurrency, unsupported FS, injected crashes before/after rename/fsync, readback | DRAFTED / OPEN |
| F04 | Product/Local independent Ports, 5 Product methods and 4 ArtifactStore methods mapped, typed Protocol candidates + staging-only sink, trusted root updated in DD | Concrete DTO constructors/return types, error types, regression test suite and independent reviewer pending | mypy/static Port integration, Product v2/legacy Regression, all 41 Method registry matching | REVIEWED_BY_AUTHOR / OPEN |
| F05 | Threat model, UID/owner + ACL/mount/namespace checks, root capability, `S∧F∧P∧R∧C` row gate, private output | Source/authority of preauthorized Study policy; mount allowlist/ACL algorithm; deny-as-failure vs aggregate fallback | threat model security review, OS/mount/ACL negative tests, sentinel-row leak tests | DRAFTED / OPEN |
| F06 | 5 Owner-adopted discriminators + marker; 6 machine schema drafts; strict input dispatch; old-v2 isolation; error→exit candidate | exact canonical JSON bytes/hash, incomplete nested method-specific DTOs, row denial exit 2 vs 3, formal JSON Schema validation | real Draft2020-12 validation with fixtures, decoder Error/Version negative, legacy v2 regression | STATIC_SUBSET_QA_PASS / OPEN |
| F07 | tagged extended-real AR endpoints, 4-set topology draft, typed point/inference/science axes, schema embedded into Effect | **EMPTY** generic AR representation decision, Method-specific just-ID restriction, mathematical union semantics, independent numeric oracle | 4/5-topology decision, mathematical set property tests, independent weak-IV scientific tests, exact science acceptance policy | AUTHOR_FINDING_HIGH / OPEN |
| F12 | reviewer package with finding matrix and current source/draft links | No independent reviewer has assessed committed snapshot | independent written F03–F07 verdict against frozen SHA and documented corrections | NOT_RUN |

## 2. Proposed bounded Owner/Science decisions (not yet adopted)

| ID | Choice to ratify | Recommendation | Existing policy impacted |
|---|---|---|---|
| D-F07-EMPTY | A: Generic AR `EMPTY` is a valid mathematically computed set, while specific B0/B1 just-identified execution can reject EMPTY by Method-specific invariant. B: retain blanket EMPTY-as-failure policy. | **A**. Prevents treating a mathematically meaningful empty set as failed computation. Requires Science Reviewer; adjust `topology`, `components.minItems`, F07 acceptance and null reasons together | F07 draft only; no Owner adoption of EMPTY semantics yet |
| D-F05-POLICY | A: Verify separately bound preauthorized Study Policy artifact/authority; B: trust `row_export_authorized: true` in caller's Study YAML. | **A**, consistent with Owner's “preauthorized” AND requirement; finalize what constitutes authority on a single-UID host | DEC-PREP02-A unchanged |
| D-F06-CODEC | A: fix a strict versioned canonical JSON encoding (fully specified float/string/Unicode/ordering) with cross-runtime fixtures; B: reuse Product `hash_mapping(default=str)`. | **A**; B violates strict typed wire and risks collisions. Exact algorithm and dependencies to be reviewed | DEC-PREP02-C unchanged |
| D-F06-ROW-EXIT | A: privacy/authorization denial uses CLI exit 3 security class; B: classify as invalid config exit 2. | **A**, but only after consistent CLI error taxonomy and Owner signoff | New mechanical decision only |

## 3. Freeze/implementation sequencing

1. Owner/Science ratify F07 EMPTY and F05 Policy authority; fix F06 codec/Error/Schema completeness and validated DTO signatures; publish a single frozen Port+Schema snapshot SHA.
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
