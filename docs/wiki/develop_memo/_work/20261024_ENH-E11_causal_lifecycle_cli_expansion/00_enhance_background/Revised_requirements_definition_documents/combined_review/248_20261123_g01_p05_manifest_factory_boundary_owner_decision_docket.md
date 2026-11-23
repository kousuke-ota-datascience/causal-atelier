# 248 — G01/P05 Manifest construction dependency boundary: Owner decision docket

**Date:** 2026-11-23 JST  
**Status:** `CONTRACT_DEFECT_CONFIRMED / OWNER_ARCHITECTURE_DECISION_PENDING / P05_TRIAL01_BLOCKED`  
**Proposed decision:** `DEC-G01-P05-MANIFEST-BOUNDARY-01`  
**Active S10:** `3ea759825810e95425a9e7557c3b2cc46b21157d`  
**Existing S11:** `DEC-G01-P05-001-S11-REAUTH-01` (`dfa5a8767d0c0f50c86a627f88bcf72ef1b93999`)  
**Branch:** `feature/ariadne_mvp_e11`

## 1. Observed blocker and evidence

P05 Trial01 restarted at `dfa5a8767d0c0f50c86a627f88bcf72ef1b93999` and reported `BLOCKED_CONTRACT_AMBIGUITY` without implementation, test rerun, checkpoint, commit or push. P05 `06_G01_P05_cli_use_case_privacy.md` §6.4 directs Application-layer `LocalCausalUseCase.run` to construct P01 `ValidatedRunEvidence` and invoke `LocalRunManifest.from_run_evidence`. The completed P01 implementation locates both in `src/ariadne/interfaces/cli/local_causal/manifest.py`; `ValidatedRunEvidence` is nominally type-checked by that factory. P05 §6.1 and design `30_62_local_execution_publication.md` §1.2/1.3 prohibit Application depending on CLI concrete and mandate 11 injected Ports. The implemented P02 `ariadne.capabilities.causal.ports.local_io.LocalPublicationPort.seal(*,sink,manifest:ManifestValue,privacy)` requires an already constructed Manifest and does not offer a factory. No approved Application-visible Manifest factory Port or constructor dependency is defined.

Relevant frozen authorities:
- `30_detailed_design/30_62_local_execution_publication.md` §§1.1–1.5, 4.1–4.6: Application Port-only direction; exact 11 fields; P01 CLI Manifest owner; factory has no filesystem I/O.
- `23_api_interface_design/23_41_cli_scientific_ports.md` §§4–4.4: App Port/CLI Adapter dependency inversion and `LocalPublicationPort.begin/seal/publish` signatures.
- `23_api_interface_design/23_42_local_result_manifest_artifact.md` §9.1: CLI-owned Manifest value/serialization and Publisher-owned physical publication.
- `10_enhance_instruction/G01/06_G01_P01_local_contract_codec.md` §6.5: P01 owns `LocalRunManifest`, `ValidatedRunEvidence`, `RuntimeEvidence`, `ArtifactDescriptor` with strict pure joins.
- `10_enhance_instruction/G01/06_G01_P02_atomic_publication_reader.md` §6.3: P05-to-P01 factory assumption and existing P02 seal contract.
- `10_enhance_instruction/G01/06_G01_P05_cli_use_case_privacy.md` §§6.1,6.2,6.4: incompatible construction direction.
- `10_enhance_instruction/G01/07_Ariadne_ENH-E11_G01_test_instruction.md` G01-07-06/07: preserve actual values, independent Publisher and Reader verification.

The direct application import is not compliant, and making `seal` fabricate its own Manifest would contradict its frozen input contract and alter P02 responsibilities. This is a genuine *design-to-implementation instruction contract defect*, not evidence that completed P01/P02 code should be rewritten to suit P05.

## 2. Alternatives for Owner disposition

**A — recommended: Introduce an Application-facing Manifest construction Port with a CLI concrete Adapter.** Keep P01 factory and nominal `ValidatedRunEvidence` type untouched, P02 `LocalPublicationPort.seal` and concrete Publisher untouched, and existing published wire format unchanged. Define in an Application-owned Port module a typed, immutable and concrete-agnostic run-evidence input contract; no reference to `ariadne.interfaces.cli.*` is permitted in Application. Add an injected `manifest_factory` collaborator to `LocalCausalUseCase` constructor (12th Port), backed by a CLI adapter. The adapter translates independently validated Application-visible evidence to the existing P01 `ArtifactDescriptor`, `RuntimeEvidence`, `ValidatedRunEvidence`, invokes unchanged `LocalRunManifest.from_run_evidence`, and returns its result as the existing `ManifestValue` Protocol. No duplicate scientific or JCS validation authority; P01 factory still enforces strict canonical joins. Application passes the result to `publisher.seal(*,sink,manifest,privacy)`; P02 validates physical bytes/root/Privacy and independent Reader verifies committed output. Adapter must not invent runtime/science facts or synthesize scientific negatives. The precise Port name, type definition, constructor signature, mapping and failure semantics require coherent contract amendments.

**B — not recommended: relocate P01 DTO/factory into Application/shared module.** Changes protected P01 module/imports, test contracts and potentially P02/Reader dependencies. Higher completed-Package regression risk and approval obligations.

**C — not recommended: move Manifest assembly and all seal/publish steps to CLI composition root.** Separates the already approved Application `run` orchestration and readback ownership; broader contract and testing impact.

A changes an **internal published/authoritative Port/constructor contract** (not the external E11 JSON wire). It is therefore submitted to Owner, not silently implemented as an engineering convenience.

## 3. Conditional minimal amendment scope if A is approved

Before a new coding attempt, produce one bounded `AMD-E11-G01-P05-001` 09 amendment and reconcile:
1. `23_api_interface_design/23_41_cli_scientific_ports.md` — new internal Application Port/CLI Adapter boundary and signature;
2. `30_detailed_design/30_62_local_execution_publication.md` — UseCase constructor/fields and Manifest factory invocation direction; preserve P01 ownership of serialized schema;
3. `10_enhance_instruction/G01/06_G01_P05_cli_use_case_privacy.md` — use injected Port, no CLI import from Application;
4. `10_enhance_instruction/G01/07_Ariadne_ENH-E11_G01_test_instruction.md` — independently verify injection, P01 strict factory usage, non-bypass, missing/failing collaborator and unchanged P02/Reader checks;
5. Parent `06_Ariadne_ENH-E11_G01_implementation_instruction.md` and `06_G01_P00_work_package_plan.md` — only if exact normative constructor/Port cross-references require reconciliation;
6. `06_G01_P01_local_contract_codec.md`, `06_G01_P02_atomic_publication_reader.md`, and existing code/test/checkpoint files — **do not change** without a separately explicit approved exception; compatibility audit only.

The amendment must not change the external `e11-local-*/1` Schema Versions, six-field Descriptor, Status/Manifest/Marker wire, CLI v2, Privacy, FCI science, independent acceptance criteria or unresolved `DEFERRED_PRODUCT_POLICY_BRIDGE`. Existing P01 and P02 tests stay independently required. If inspection proves any completed-Package change unavoidable, suspend that part and request Owner approval with exact impact.

## 4. Mandatory control-plane sequence

This docket is **not** an approved amendment, S10 refreeze or Coding Authorization; P05 Trial01 remains stopped. Owner must first select A/B/C (recommended `DEC-G01-P05-MANIFEST-BOUNDARY-01=A`). After the Owner decision, implement and audit the amendment across applicable normative documents, then obtain separate explicit **formal 09 Owner approval**, then separately obtain **S10 refreeze** against an exact complete Git SHA, and then separately obtain **P05/Trial01 limited S11 reauthorization** against that revised S10. The earlier S11 `DEC-G01-P05-001-S11-REAUTH-01` cannot authorize coding against revised frozen contracts.

No P05 implementation, retroactive PASS or checkpoint is authorized by this decision docket. P04 checkpoint `7dcf2061dae3c8832b2b3ec9be6900ad6ee7edb6`, P03 `858c9f73366036a2d1445e558135cd521f611462`, P02 `3a76a0aa1698037354b284ba7b5a875300473ce6`, and all earlier approved science / independent `G01_999` obligations are preserved.
