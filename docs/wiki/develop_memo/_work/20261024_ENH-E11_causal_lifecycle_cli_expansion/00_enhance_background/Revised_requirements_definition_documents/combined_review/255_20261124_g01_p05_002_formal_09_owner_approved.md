# 255 — G01/P05 AMD-E11-G01-P05-002 formal 09 Owner approval

**Date:** 2026-11-24 JST  
**Decision ID:** `DEC-G01-P05-002-FORMAL09-APPROVAL`  
**State:** `FORMAL_09_OWNER_APPROVED / S10_REFREEZE_PENDING / S11_REAUTH_PENDING / P05_TRIAL01_CODING_BLOCKED_UNDER_AMD002`  
**Repository:** `kousuke-ota-datascience/causal-atelier`  
**Branch:** `feature/ariadne_mvp_e11`  
**Amendment:** `10_enhance_instruction/G01/09_ENH-E11_G01_AMD-E11-G01-P05-002_Gate_Contract_Amendment.md`  
**Author static audit adopted:** `00_enhance_background/Revised_requirements_definition_documents/combined_review/254_20261124_g01_p05_002_abort_port_contract_static_audit.md`  
**Underlying Owner design decision:** `DEC-G01-P05-P02-ABORT-BOUNDARY-01=A` (`combined_review/253_20261124_g01_p05_prepublication_abort_owner_decision_docket.md`)  
**Immediately preceding branch HEAD:** `7b50c64e610980102ef1dc3a703b04a2b53c0257`  
**Current frozen G01-S10 (not changed by this decision):** `d5b7fab759b27ed8427a46256bac5ac8231e0c77`

## 1. Explicit Owner approval and authority

Owner approved `DEC-G01-P05-002-FORMAL09-APPROVAL` and expressly adopted `AMD-E11-G01-P05-002` as the **formal 09 G01/P05 amendment**, accepting the static document-concordance conclusions of `combined_review/254`. The approval explicitly limits the exception to completed P02 to addition of the internal `abort` operation on `LocalPublicationPort` and `LocalPublicationAdapter`, preserving existing `LocalArtifactPublisher.abort`, `begin/seal/publish`, P01–P04 instructions/implementation/checkpoint history, published E11 Schema Versions, existing scientific meaning, independent G01_999 acceptance, and `DEFERRED_PRODUCT_POLICY_BRIDGE` as unfulfilled. Owner explicitly withheld new S10 refreeze and S11 reauthorization as **separate decisions**.

The approved change is a narrow amendment to the internal Application-to-Publication Port lifecycle, not an alteration of public E11 wire, Product v2 behavior, P02 physical publication authority, or scientific contracts. Static audit adoption does not assert executable correctness, runtime FS proof, or independent science PASS.

## 2. Verified approval input

Immediately before this administrative record, GitHub branch HEAD was exactly `7b50c64e610980102ef1dc3a703b04a2b53c0257`. Comparing the last P05 S11 issuance commit `b64bb385cca120dd7af6154ea3cb87ae3b2b0ac3` with that HEAD returned `ahead=7 / behind=0` and exactly **seven** changed files:

1. `00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design/23_41_cli_scientific_ports.md`
2. `00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_62_local_execution_publication.md`
3. `00_enhance_background/Revised_requirements_definition_documents/combined_review/253_20261124_g01_p05_prepublication_abort_owner_decision_docket.md`
4. `00_enhance_background/Revised_requirements_definition_documents/combined_review/254_20261124_g01_p05_002_abort_port_contract_static_audit.md`
5. `10_enhance_instruction/G01/06_G01_P05_cli_use_case_privacy.md`
6. `10_enhance_instruction/G01/07_Ariadne_ENH-E11_G01_test_instruction.md`
7. `10_enhance_instruction/G01/09_ENH-E11_G01_AMD-E11-G01-P05-002_Gate_Contract_Amendment.md`

Both the exact AMD-002 amendment and its static audit existed in that HEAD. The changed paths are limited to Owner docket, Author contracts, audit and amendment; no source, test, completed P02 06/07 or other completed package file was changed. This approval record is an administrative commit created **after** that HEAD; its resulting complete SHA should be used as the candidate for a separately authorized G01-S10 refreeze.

## 3. Approved bounded Port and Adapter amendment

**Internal Port signature** (new additive operation):

~~~python
def abort(self, *, sink: StagingArtifactSink, reason: str) -> None: ...
~~~

- `LocalPublicationAdapter.abort` must verify exact begin-produced `_Sink`, same owned run-scoped `LocalArtifactPublisher` and permission-policy identity, then delegate to the **existing unchanged** `LocalArtifactPublisher.abort(reason)`. Reject fake sink, cross-run/cross-policy substitution, repeated or invalid-state calls. Do not introduce an independent cleanup or publication engine.
- `LocalCausalUseCase` calls this Port only after a successful begin and **before invoking publish**, on failures during Discovery, staging, evidence validation, AMD-001 Manifest Factory building and `seal`. On a failure before begin there is no sink and no abort. After publish has been called, it must **not** issue Application-level abort, even if publish fails, because rename may have happened or be indeterminate. Existing Publisher handles its internal pre-rename abort and indeterminate outcomes.
- Concrete abort releases owned handles and quarantines private staging residue; it is not a guarantee of secure deletion, not final-run rollback, and never a mechanism for destructive cleanup of `COMMITTED/INDETERMINATE` runs.
- Preserve original typed/CLI exit failure when cleanup fails; a secondary nonsecret cleanup diagnostic may be reported, but no invented success, SCI-negative or G01_999 PASS.
- Preserve existing P02 `begin/seal/publish` signatures/bodies and all P02 concrete `LocalArtifactPublisher.abort` behavior. The bounded future source edits are **only** additive methods in `src/ariadne/capabilities/causal/ports/local_io.py` and `src/ariadne/interfaces/cli/local_causal/publication.py`. If other P02 source changes prove necessary, obtain another Owner decision before modifying them.

## 4. Explicit retained checkpoints and verification

- P01: `9bff61f0eae25236f95f31f2cd3e7c81291f0167`.
- P02: `3a76a0aa1698037354b284ba7b5a875300473ce6`.
- P03: `858c9f73366036a2d1445e558135cd521f611462`.
- P04: `7dcf2061dae3c8832b2b3ec9be6900ad6ee7edb6`.

Protected invariants include unmodified E11 published Schema Version, all scientific P1-M06/FCI/Graph/PAG semantics, privacy/row restrictions, atomic no-clobber publish, independent Reader, CLI exit classification, Product v2 compatibility, `uv.lock`, independent scientific and real-FS G01_999 acceptance, and `DEFERRED_PRODUCT_POLICY_BRIDGE=UNFULFILLED` as a pending architecture acceptance dependency. Existing 207-passing-test report is historical and does not establish the newly authorized Port behavior; independent verification must exercise the new abort path plus original P02/Product regressions on eligible FS.

## 5. Separate S10 and S11 control-plane decisions

**Formal 09 Owner approval is complete only.** The immutable active S10 remains `d5b7fab759b27ed8427a46256bac5ac8231e0c77` until a new, separately approved S10 refreeze. Earlier `DEC-G01-P05-001-S11-REAUTH-02` is not an authorization for P05 coding against AMD-002. No P02 additive source implementation or P05 coding begins under this document alone.

After verifying the full commit SHA created by recording this 255 approval, request a **new separate Owner S10 refreeze** against that exact SHA; only then request a **separate G01/P05/Trial01-limited S11 reauthorization** with the expressly bounded P02 Port/Adapter addition. P05 remains blocked until those decisions and Agent preflight checks. No P05 checkpoint, test PASS, new FS experiment, Product bridge completion or G01_999 PASS is claimed by the approval record.
