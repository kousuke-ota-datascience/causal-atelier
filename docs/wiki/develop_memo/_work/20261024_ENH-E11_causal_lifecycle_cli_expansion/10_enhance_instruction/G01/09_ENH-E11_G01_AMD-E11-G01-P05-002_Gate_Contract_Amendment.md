# AMD-E11-G01-P05-002 — Pre-publication staging abort via Application Publication Port

**Date:** 2026-11-24 JST  
**Gate / Package / Trial:** `G01/P05/Trial01`  
**Classification:** `INTERNAL_PUBLICATION_PORT_ABORT_BOUNDARY / BOUNDED_COMPLETED_P02_EXCEPTION`  
**Owner design and scoped P02 exception decision:** `DEC-G01-P05-P02-ABORT-BOUNDARY-01=A_ADOPTED`  
**Status:** `AUTHOR_PREPARED_FORMAL_09_CANDIDATE / FORMAL_09_OWNER_APPROVAL_PENDING / S10_REFREEZE_PENDING / S11_REAUTH_PENDING / P05_TRIAL01_BLOCKED`  
**Last blocked Coding Agent START_SHA:** `b64bb385cca120dd7af6154ea3cb87ae3b2b0ac3`  
**Current immutable G01-S10:** `d5b7fab759b27ed8427a46256bac5ac8231e0c77`  
**Prior limited P05 S11:** `DEC-G01-P05-001-S11-REAUTH-02`, valid for the superseded contract only after this amendment is formally adopted  
**P02 protected checkpoint:** `3a76a0aa1698037354b284ba7b5a875300473ce6`  
**Decision docket:** `combined_review/253_20261124_g01_p05_prepublication_abort_owner_decision_docket.md`

## 1. Root cause and normative assessment

Application `LocalCausalUseCase.run` is contractually required to stop staging on any failure after `LocalPublicationPort.begin` but before publication. Existing P02 `LocalPublicationPort` exposes only `begin/seal/publish`, and the existing `StagingArtifactSink` exposes only `stage_bytes`. P02 CLI concrete `LocalArtifactPublisher.abort(reason)` exists but P05 Application must not import/dereference CLI `_Sink` or concrete Publisher. The completed P02 `LocalPublicationAdapter` has no abort facade method. This is a missing **application-to-publication lifecycle Port** operation, not a defect in the original Publisher's pre-publication abort algorithm, scientific semantics or public schemas. The failed experiment's previous 207 focused + Product tests and private ext4 staging observation establish existing behavior, not P05's unimplemented failure-path correctness.

Owner explicitly adopted docket 253 option A: add one internal `LocalPublicationPort.abort` operation and CLI `LocalPublicationAdapter.abort` forwarding to **unchanged** existing P02 `LocalArtifactPublisher.abort`. This is an express bounded exception to the completed P02 module surface, not a general P02 remediation authorization.

## 2. New internal application Port contract

~~~python
# ariadne.capabilities.causal.ports.local_io.LocalPublicationPort
def abort(self, *, sink: StagingArtifactSink, reason: str) -> None: ...
~~~

- `sink` must be exactly the original `begin`-returned `_Sink` bound to its run-scoped concrete Publisher; the concrete `LocalPublicationAdapter` must validate that identity plus the adapter's injected policy ownership before delegation. Reject fake sink, cross-policy, cross-run/cross-session substitution and invalid transitions. Preserve no shared mutable registration table or second publication transaction.
- `reason` is a bounded, nonsecret operational message: no row data, raw path or credential leakage. Do not add it to public Manifest/Status/Marker JSON.
- The existing `LocalArtifactPublisher.abort(reason)` remains the exclusive concrete cancellation authority, with its original state-transition and FD cleanup behavior unchanged. The operation releases handles and quarantines isolated private staging residue; it **does not** prove secure deletion of staging bytes or allow destruction of a final or potentially final run.
- Only `LocalPublicationPort` and `LocalPublicationAdapter` gain the additive operation. `LocalPublicationPort.begin/seal/publish` signatures, validation, PrivacyDecision binding and Reader are unchanged; `StagingArtifactSink.stage_bytes` is unchanged.

## 3. P05 call sequencing and failure classification

- If `preflight`, Policy authorize or `begin` fails before a sink exists, **no abort** is called.
- After successful `begin` and **strictly before invocation of `publish`**, failures in Discovery/FCI, staging bytes or Graph/Status/schema consistency, actual runtime probing, AMD-001 `LocalManifestFactoryPort.build`, or `seal` MUST lead to exactly one `publisher.abort(sink=original_sink,reason=sanitized_reason)` attempt. These are exceptions to the application transaction, not valid scientific-negative outcomes. No `COMPLETED`, Marker or final run is produced on this path.
- An error from `publish` (even if its local type looks like a pre-rename failure) MUST NOT trigger Application `abort`: the attempt to publish is already in progress and rename may have occurred or be indeterminate. P02's existing internal `commit` handles its own safe pre-rename abort and `PUBLICATION_INDETERMINATE` state. No state-based guess that `PUBLISHING` was safe, no deletion, manual retry or rewriting of a potentially committed run.
- If an abort attempt itself fails, report the cleanup fault separately as operational evidence without masking or recategorizing the original typed failure; do not claim successful abort or rollback. Existing CLI phase-dependent exit2/3/4/5 mapping stays unchanged.
- The original P02 concrete Publisher's abort behavior is not modified; if implementation reveals that its state guard is insufficient for the approved facade, stop and seek an additional specific Owner decision.

## 4. Exact document edits and completed-Package boundary

Normative Author edits under this amendment:

1. `00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design/23_41_cli_scientific_ports.md` — Port method table and new §4.1b, internal lifecycle operation, ownership and no public-wire impact.
2. `00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_62_local_execution_publication.md` — §8.2 canonical signatures and new §8.2a; P05 abort window versus Publisher rename-uncertainty boundary.
3. `10_enhance_instruction/G01/06_G01_P05_cli_use_case_privacy.md` — §6.4 step 9 and §6.6a with exact Port call and error handling.
4. `10_enhance_instruction/G01/07_Ariadne_ENH-E11_G01_test_instruction.md` — independent G01-07-05/07/11 abort acceptance matrix, actual FS evidence and Product regressions.

**Explicit bounded completed-P02 exception for later coding, not performed here:**
- `src/ariadne/capabilities/causal/ports/local_io.py`: add only `LocalPublicationPort.abort(*,sink,reason)` Protocol method.
- `src/ariadne/interfaces/cli/local_causal/publication.py`: add only `LocalPublicationAdapter.abort(*,sink,reason)` validating the begin-created sink/policy and forwarding to the original `LocalArtifactPublisher.abort`.
- Preserve unchanged P02 concrete `LocalArtifactPublisher.abort` body, `begin/seal/publish` methods/signatures, `StagingArtifactSink`, P02 06/07 documents, P02 tests/checkpoint history, and completed P01/P03/P04. The previously completed P02 06 three-operation listing remains an historical description of its protected implementation; this **specific Owner-approved additive internal extension** is defined by IF 23_41 §4.1b and DD 30_62 §8.2a, not a license to rewrite that P02 instruction.
- No new source code or independent tests are executed under the Author-only amendment phase.

No changes required in requirements 10, logical data 21, basic design 22, public IF 23_42 bundle/marker definitions, P01/P02/P03/P04 06/07, P00 plan, or parent Gate 06; all remain substantively consistent on their existing abstraction levels.

## 5. Independent acceptance and regression impact

| Area | Required evidence under future coding/independent 07 |
| --- | --- |
| Pre-begin | `--check-only` and denied preflight/policy/begin create no staging; abort not invoked |
| Before publish | Failure in discovery, staging, Graph/status, Manifest Factory or seal calls Port abort exactly once on original sink; private stage/quarantine and FD release; no Marker/final run/false COMPLETE |
| Sink identity | Reject fake/structurally similar, cross-run, cross-root, wrong policy, repeated abort; other runs unaffected |
| Seal to publish | Pre-publish validated state abort can release/quarantine; no bypass of P02 policy/Manifest validations |
| Publish started | Any returned error, including unknown rename state, no **Application** abort; P02 own commit/indeterminate handling, no deletion/overwrite/false PASS |
| Errors | Preserve primary typed/exit category, record secondary cleanup fault without sensitive bytes |
| P02/legacy | Original begin/seal/publish, no-clobber, Privacy, Reader, actual ext4/XFS, protected Product v2 tests retain expectations and must be rerun |

This amendment makes no claim that the existing 207 passing tests cover these newly specified cases. Independent P05/G01_999 scientific and physical verification remain binding.

## 6. Retained invariants and release controls

Protected P01 `9bff61f0eae25236f95f31f2cd3e7c81291f0167`, P02 `3a76a0aa1698037354b284ba7b5a875300473ce6`, P03 `858c9f73366036a2d1445e558135cd521f611462` and P04 `7dcf2061dae3c8832b2b3ec9be6900ad6ee7edb6` checkpoints remain intact.

No change to five public E11 Schema Versions, public API/CLI, Study/Graph/Manifest/Status/Marker wire, six-field ArtifactDescriptor, Product v2 semantics, immutable atomic publication/no-clobber, Reader, Privacy, P1-M06 FCI/CI/PAG/typed scientific-negative rules, no unsupported non-null BK, optional Backend, `uv.lock`, T2/T3, or independent `G01_999` conditions. `DEFERRED_PRODUCT_POLICY_BRIDGE` remains `UNFULFILLED`, not retired or waived, and remains a relevant Gate acceptance dependency.

**CONTROL PLANE:** This is an **Author-prepared AMD-E11-G01-P05-002 formal-09 candidate**, *not* an Owner formal 09 approval, S10 refreeze, S11 reauthorization or Coding Authorization for source changes. The active immutable S10 is still `d5b7fab759b27ed8427a46256bac5ac8231e0c77`. An explicit new formal 09 approval, an exact SHA S10 refreeze, and a distinct P05/Trial01-limited S11 authorization are mandatory in that order before this Port extension is implemented. No P05 checkpoint, source change, test PASS, independent science approval or G01_999 PASS is claimed.
