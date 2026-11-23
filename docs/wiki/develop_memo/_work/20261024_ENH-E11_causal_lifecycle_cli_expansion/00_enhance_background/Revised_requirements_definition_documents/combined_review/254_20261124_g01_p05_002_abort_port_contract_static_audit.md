# 254 — G01/P05 AMD-E11-G01-P05-002 static contract consistency audit

**Date:** 2026-11-24 JST  
**Owner design decision:** `DEC-G01-P05-P02-ABORT-BOUNDARY-01=A_ADOPTED`  
**Status:** `AUTHOR_STATIC_CONTRACT_AUDIT_PREPARED / FORMAL_09_PENDING / S10_REFREEZE_PENDING / S11_REAUTH_PENDING / P05_TRIAL01_BLOCKED`  
**Working branch:** `feature/ariadne_mvp_e11`  
**Current frozen S10 (not refrozen by this audit):** `d5b7fab759b27ed8427a46256bac5ac8231e0c77`  
**Author amendment candidate:** `10_enhance_instruction/G01/09_ENH-E11_G01_AMD-E11-G01-P05-002_Gate_Contract_Amendment.md`

## 1. Root cause and chosen repair

Under existing P05 06, a failed run after `LocalPublicationPort.begin` and before `publish` must abort its scoped staging. P02's Application `LocalPublicationPort` has only begin/seal/publish; `StagingArtifactSink` has only stage_bytes; the concrete Publisher already owns the necessary `abort(reason)`, but there is no legal Port call from Application. The design omission is an **exposure/binding gap**, not authorization to weaken failed-publication safety or rewrite P02's concrete state machine. Docket `combined_review/253` records competing A/B/C options. Owner expressly approved A plus the bounded completed-P02 implementation exception.

## 2. Document-level authority and static trace

| Authority | File | Amendment result |
| --- | --- | --- |
| Requirements/functional/scientific | `10_requirements_definition/` | Unchanged: no new function, Method semantics, negative-outcome policy or public exit reason |
| Logical data and product architecture | `21_logical_data_design/`, `22_product_basic_design/` | Unchanged: no stored payload, schema, external operation or Product DB/Worker change |
| Interface | `23_api_interface_design/23_41_cli_scientific_ports.md` §4.1b | Defines additive internal `LocalPublicationPort.abort(*,sink,reason)`, owned sink/policy binding, pre-publish-only caller window; existing begin/seal/publish remain normative |
| Existing publication interface | `23_api_interface_design/23_42_local_result_manifest_artifact.md` | Unchanged: existing abort/quarantine, no-clobber, Marker, Reader, indeterminate rules still apply |
| Detailed design | `30_detailed_design/30_62_local_execution_publication.md` §8.2/§8.2a | Normalizes four-operation internal facade and pre-publish exception path; leaves original concrete `LocalArtifactPublisher.abort` and full state machine unchanged |
| P05 Coding | `10_enhance_instruction/G01/06_G01_P05_cli_use_case_privacy.md` §6.4/§6.6a | Exact injected Port abort, once per failed successful begin before publish; explicit publication-entry boundary and typed exception retention |
| Independent verification | `10_enhance_instruction/G01/07_Ariadne_ENH-E11_G01_test_instruction.md` G01-07-05/07/11 | Positive/negative abort identity and state tests including real FS, secondary cleanup failure, rename/indeterminate non-cleanup and original Product/P02 regression |
| Formal amendment candidate | `10_enhance_instruction/G01/09_ENH-E11_G01_AMD-E11-G01-P05-002_Gate_Contract_Amendment.md` | Lists exact exceptional P02 changes and independent 09/S10/S11 sequence |

Parent `06_Ariadne_ENH-E11_G01_implementation_instruction.md` and P00 plan express Gate/Package responsibilities but no contradictory normative abort signature. Completed P02 `06_G01_P02_atomic_publication_reader.md` has the original three-operation facade signature and a concrete abort behavior; its 06 is intentionally immutable under the Owner's P02 exception scope. The **additive** fourth internal Port operation in IF 23_41 §4.1b and DD 30_62 §8.2a formally supplements only that historical facade listing. No existing P02 method is removed/reinterpreted and P02 06/07 files have not been revised.

## 3. Existing implementation cross-check and exact P02 exception boundary

Before documentation amendment, GitHub source checks established:
- `src/ariadne/capabilities/causal/ports/local_io.py`: `LocalPublicationPort` declares `begin/seal/publish` only.
- `src/ariadne/scientific/ports/artifacts.py`: `StagingArtifactSink` declares `stage_bytes` only.
- `src/ariadne/interfaces/cli/local_causal/publication.py`: `LocalArtifactPublisher.abort(reason)` already releases handles/quarantines private residue and rejects `COMMITTED/INDETERMINATE`. `LocalPublicationAdapter` has no abort method but already checks exact `_Sink` and publisher-policy ownership in `seal`.
- The concrete `commit` owns attempts to rename and may return `PUBLICATION_INDETERMINATE`; Application may not try abort after entering `publish`, even for apparently pre-rename errors. No inference from `PUBLISHING` alone is permitted.

Owner authorized *later, separately S11-authorized code changes* to **only** the additive `LocalPublicationPort.abort` Protocol method and `LocalPublicationAdapter.abort` method. Existing P02 `LocalArtifactPublisher.abort` implementation, `begin/seal/publish`, `StagingArtifactSink`, completed P02 06/07/test/checkpoint and P01/P03/P04 are protected. A necessary change beyond that envelope is a new blocker requiring further Owner approval.

## 4. Regression risk and acceptance verdict

- **P02 ABI/typing:** The Protocol adds a required method; concrete clients and injectors must wire the same Adapter. Existing callers of `begin/seal/publish` retain identical signatures. Static structural Protocol checks may surface mock conformance errors; tests must be updated only for truly P05-owned new tests, not by weakening P02 historical expectations.
- **Lifetime/isolation:** Validate exact begin-returned sink and same instance-owned Publisher/policy; prevent unrelated session abort, fake sink, repeated call, and leak of row/secret in reason.
- **Pre-publication failures:** Abort after Discovery, stage, Manifest Factory and seal rejection; no false Marker, rename, COMPLETED. Validate handle closure and quarantine rather than assuming deletion of bytes.
- **Post-publication uncertainty:** Once `publish` was called, all abort decisions remain internal P02 Publisher responsibilities; P05 must not invoke Port abort. No cleanup of indeterminate or potentially published run.
- **Failure correctness:** Original typed failure and CLI exit classification retained even if best-effort abort fails; cleanup diagnostics separate, no fabricated scientific-negative.
- **Scientific/security/legacy:** P1-M06 science, DAG/PAG/FCI constraints, explicit no-non-null-BK, privacy/no-row, true FS/Reader, Product v2 regression, T2/T3 and independent G01_999 conditions unchanged. `DEFERRED_PRODUCT_POLICY_BRIDGE` remains `UNFULFILLED`, with its acceptance dependency preserved.

**Audit verdict:** The specific missing pre-publication abort Port path is fully specified at the document-contract level through an additive internal facade operation and an explicit bounded completed-P02 exception, without moving publication authority or altering public/scientific requirements. However this is a **static documentation audit, not executable verification**. The P05 failure path and new facade method have not been implemented or tested. The earlier Coding Agent's 207-pass existing focused/Product run is historical and does not prove this addition.

## 5. Control plane

Current immutable G01-S10 stays `d5b7fab759b27ed8427a46256bac5ac8231e0c77` until a **new Owner S10 refreeze**. Previous P05 `DEC-G01-P05-001-S11-REAUTH-02` pertains to the previous contract and must not be treated as implementation authorization for AMD-E11-G01-P05-002. Obtain **separate Owner formal 09 approval** on AMD-002 and this audit, then **separate Owner S10 refreeze** on its exact immutable full SHA (including 09 record), then **distinct P05/Trial01 limited S11 reauthorization**. The S11 under the old freeze cannot be silently reused.

No coding, independent tests, P05 checkpoint or Git source modification is asserted. P01 `9bff61f0eae25236f95f31f2cd3e7c81291f0167`, P02 `3a76a0aa1698037354b284ba7b5a875300473ce6`, P03 `858c9f73366036a2d1445e558135cd521f611462`, P04 `7dcf2061dae3c8832b2b3ec9be6900ad6ee7edb6` remain protected.
