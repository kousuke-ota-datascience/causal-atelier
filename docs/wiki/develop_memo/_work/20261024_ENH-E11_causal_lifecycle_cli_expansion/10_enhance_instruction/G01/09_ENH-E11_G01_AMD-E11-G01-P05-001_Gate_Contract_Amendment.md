# AMD-E11-G01-P05-001 — Manifest Factory dependency inversion for G01/P05

**Date:** 2026-11-23 JST  
**Gate/Package/Trial:** `G01/P05/Trial01`  
**Classification:** `INTERNAL_APPLICATION_PORT_ARCHITECTURE_CONTRACT_DEFECT`  
**Owner design choice:** `DEC-G01-P05-MANIFEST-BOUNDARY-01=A_ADOPTED`  
**State:** `AUTHOR_PREPARED_FORMAL_09_CANDIDATE / FORMAL_09_OWNER_APPROVAL_PENDING / S10_REFREEZE_PENDING / S11_REAUTH_PENDING`  
**Last stopped Coding START_SHA:** `dfa5a8767d0c0f50c86a627f88bcf72ef1b93999`  
**Active immutable S10 (not yet updated):** `3ea759825810e95425a9e7557c3b2cc46b21157d`  
**Previous S11:** `DEC-G01-P05-001-S11-REAUTH-01` (valid only against previous frozen contract)  
**Protected checkpoints:** P02 `3a76a0aa1698037354b284ba7b5a875300473ce6`; P03 `858c9f73366036a2d1445e558135cd521f611462`; P04 `7dcf2061dae3c8832b2b3ec9be6900ad6ee7edb6`; P05 none.

## 1. Root cause and approved choice

The existing G01/P05 §6.4 directs Application `LocalCausalUseCase.run` to build P01's `ValidatedRunEvidence` and call `LocalRunManifest.from_run_evidence`; both nominal CLI-owned classes are in the completed P01 `ariadne.interfaces.cli.local_causal.manifest` module. Higher-level DD 30_62 §1 and P05 §6.1 explicitly prohibit Application importing CLI concrete and pin eleven constructor Ports. Completed P02 `LocalPublicationPort.seal(*,sink,manifest,privacy)` requires an already-built `ManifestValue`. This is an architectural call-boundary defect in the approved P05 composition specification, not a reason to rewrite completed P01/P02 or to move strict scientific/wire validation into Application. Decision docket: `combined_review/248_20261123_g01_p05_manifest_factory_boundary_owner_decision_docket.md`.

Owner adopted alternative A, `DEC-G01-P05-MANIFEST-BOUNDARY-01`: introduce an Application-owned abstract Manifest construction Port, injected through the CLI composition root with a CLI concrete Adapter. Alternatives B (move P01 DTO/factory, protected completed-Package changes) and C (move publication orchestration out of Application) are rejected.

## 2. Normative internal Port and responsibilities

- **Application Port:** `ariadne.capabilities.causal.ports.manifest_factory.LocalManifestFactoryPort`, method `build(self, *, evidence:ManifestBuildEvidence)->ManifestValue`. Required twelfth immutable keyword-only `LocalCausalUseCase.__init__` dependency `manifest_factory`. Existing eleven injections and their meanings are unchanged.
- **Application value:** deeply immutable `ManifestBuildEvidence` with `study:ValidatedStudy`, `study_payload:Mapping[str,JsonValue]`, `status_payload:Mapping[str,JsonValue]`, `runtime:ManifestRuntimeFacts`, `stochastic:Mapping[str,JsonValue]`, `artifact_descriptors:tuple[ArtifactDescriptorView,...]`, `output_graph_ref:ContentRef|None`, `graph_negative_reason_codes:tuple[str,...]`, `review_science_evidence_ref:ContentRef|None`. `ManifestRuntimeFacts` fields: `repo_commit`, `dirty`, `python_version`, `platform`, `uv_lock_sha256`, `distributions`, `api_probes`. Mapping inputs are strict JSON-compatible frozen snapshots, with no mutable external aliases/nonfinite numbers. Artifact descriptor values are P02 stage-returned exact six-field descriptors; no new field or synthetic hash.
- **CLI concrete Adapter:** `ariadne.interfaces.cli.local_causal.manifest_factory.LocalManifestFactoryAdapter`. Composition root instantiates and injects it; it alone converts neutral evidence into existing P01 `RuntimeEvidence`, `ArtifactDescriptor`, nominal `ValidatedRunEvidence`, then calls unchanged P01 `LocalRunManifest.from_run_evidence` and returns `ManifestValue`. It must not create competing serialization/validation or bypass the nominal-type P01 constructor.
- **UseCase:** trusted input and Method/science verification → stage exact bytes via existing P02 sink → collect returned descriptors and complete actual runtime/science evidence → `manifest_factory.build(evidence=...)` → existing `publisher.seal(*,sink,manifest,privacy)` → publish → independent Reader. No direct imports from `ariadne.interfaces.cli.*` in Application; no staging/final filesystem access in Manifest Factory.
- **Failure:** missing Factory, mismatched graph/refs, invalid runtime/shape or P01 factory failure abort before seal/Marker/rename; never declare completion or fake SCI-negative. The original P01 factory's pure input/Status/Manifest joins, P02 real bytes/Privacy/atomic publication, and Reader's independent committed verification remain distinct authorities.

## 3. Exact normative propagation

1. `00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design/23_41_cli_scientific_ports.md` §4.1a and Port table: internal signature, evidence, conversion Adapter, sequencing.
2. `00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_62_local_execution_publication.md` §§1.2/1.3/1.8: add twelfth constructor Port, preserve existing 11 and CLI P01 Manifest authority.
3. `10_enhance_instruction/G01/06_G01_P05_cli_use_case_privacy.md` §§6.2/6.2a/6.4: Port injection, neutral evidence, no Application-to-CLI import or direct P01 factory call.
4. `10_enhance_instruction/G01/07_Ariadne_ENH-E11_G01_test_instruction.md` G01-07-06/07/11: independent contract and negative integration verification.

Parent G01 06/P00 contain no competing fixed 11-Port constructor signature and their package ownership, dependency DAG and verification item mappings remain valid. Therefore they require no normative modifications. No requirement definition/LDD/BD or additional IF/DD document needs change: external behavior and their abstraction contracts are unchanged. Completed P01/P02/P03/P04 instructions and implementations remain untouched. The P01 exception is not used or extended.

## 4. Compatibility and acceptance matrix

| Case | Expected outcome |
| --- | --- |
| Valid actual stage-returned descriptors + valid neutral runtime and positive Graph | Adapter invokes original P01 factory, receives canonical ManifestValue, passes to unchanged P02 seal/Reader and checks complete Study/Status/Graph/Inventory joins |
| Missing `manifest_factory`, bad evidence/JSON/descriptor, wrong ref/hash/media, nonfinite/mutable data | Fail-closed before seal/Marker/rename; no false completed |
| Factory error / attempted bypass of P01 factory / Application import of CLI concrete | Reject with typed error; no direct dependency or duplicate codec |
| Actual P04 technical/backend error, unsupported BK, or unproven Graph-negative | No synthetic `SCI_NO_ADMISSIBLE_PAG`; no committed positive/negative fabricated result |
| Existing P01/P02/P03/P04 and Product v2 code/regressions | Source and contract unchanged, independently rerun appropriate focused tests |
| Real FS/FCI/PAG/MAG, BK, T2/T3, Product regressions and `DEFERRED_PRODUCT_POLICY_BRIDGE` | All prior independent G01_999 obligations preserved; no waiver or premature PASS |

No new external E11 Schema/Version, public API/CLI wire, Product v2 consumer integration, privacy policy, scientific eligibility, FCI numeric threshold, Graph/PAG semantics, or `uv.lock` change is authorized.

## 5. Formal release sequence and status

This is an **Author-prepared 09 candidate**, **not** a formal 09 Owner approval. Before resuming P05 implementation, require separately: (1) explicit formal 09 Owner approval for AMD-E11-G01-P05-001, (2) a new immutable complete normative SHA including Owner 09 approval and separate Owner S10 refreeze, (3) a separate P05/Trial01-limited S11 reauthorization tied to that exact S10 SHA, followed by Agent branch/lock/dependency checks. The previous S10/S11 are historical authority for the former contract only. This document neither grants Coding Authorization nor creates a P05 checkpoint, a developer test PASS, independent science verification, or G01_999 PASS.
