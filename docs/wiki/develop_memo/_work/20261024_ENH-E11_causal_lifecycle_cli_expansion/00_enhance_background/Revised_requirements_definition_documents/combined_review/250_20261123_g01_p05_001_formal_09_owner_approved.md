# 250 — G01/P05 AMD-E11-G01-P05-001 formal 09 Owner approval

**Date:** 2026-11-23 JST  
**Decision ID:** `DEC-G01-P05-001-FORMAL09-APPROVAL`  
**State:** `FORMAL_09_OWNER_APPROVED / S10_REFREEZE_PENDING / S11_REAUTH_PENDING / G01_P05_TRIAL01_NOT_AUTHORIZED_UNDER_AMD001`  
**Repository:** `kousuke-ota-datascience/causal-atelier`  
**Working branch:** `feature/ariadne_mvp_e11`  
**Amendment:** `10_enhance_instruction/G01/09_ENH-E11_G01_AMD-E11-G01-P05-001_Gate_Contract_Amendment.md`  
**Independent static author audit:** `00_enhance_background/Revised_requirements_definition_documents/combined_review/249_20261123_g01_p05_001_contract_consistency_static_audit.md`

## 1. Explicit Owner approval

On 2026-11-23 JST, Owner explicitly instructed:

> DEC-G01-P05-001-FORMAL09-APPROVALを承認する。AMD-E11-G01-P05-001を正式09として承認し、combined_review/249の静的整合性監査結果を採用する。P01〜P04の既存契約・実装・チェックポイント、公開E11 Schema Version、科学的意味、G01_999の独立受入条件、DEFERRED_PRODUCT_POLICY_BRIDGE未完了依存を維持する。正式09承認記録をGitHubへ反映し、次工程のS10再凍結に用いる完全Git SHAを提示せよ。S10再凍結・S11再認可はまだ実施しない。

**Decision:** `AMD-E11-G01-P05-001` is formally approved as a G01/P05 scoped contract amendment. The combined_review/249 **static document-concordance result** is adopted as author-review evidence; it is not executable integration verification, independent scientific evidence, or Gate PASS.

## 2. Verified pre-approval Git state

Immediately before adding this administrative approval record, branch HEAD was exactly:

`356e00f7436be27656690386186b1fb12f6a1b9d`.

The prior P05 S11 authorization commit was `dfa5a8767d0c0f50c86a627f88bcf72ef1b93999`. GitHub comparison from that commit to the pre-record HEAD returned `ahead=9`, `behind=0`, with **seven changed files**:

1. `00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design/23_41_cli_scientific_ports.md`
2. `00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_62_local_execution_publication.md`
3. `00_enhance_background/Revised_requirements_definition_documents/combined_review/248_20261123_g01_p05_manifest_factory_boundary_owner_decision_docket.md`
4. `00_enhance_background/Revised_requirements_definition_documents/combined_review/249_20261123_g01_p05_001_contract_consistency_static_audit.md`
5. `10_enhance_instruction/G01/06_G01_P05_cli_use_case_privacy.md`
6. `10_enhance_instruction/G01/07_Ariadne_ENH-E11_G01_test_instruction.md`
7. `10_enhance_instruction/G01/09_ENH-E11_G01_AMD-E11-G01-P05-001_Gate_Contract_Amendment.md`

The approved amendment and combined_review/249 both existed on this HEAD. No completed P01–P04 implementation/source/test/contract file is among the changed paths. This record is an administrative addition **after** that HEAD and must be included in the subsequent S10 candidate SHA.

## 3. Approved contract correction and scope

The G01/P05 stopped implementation had an incompatible dependency boundary: Application `LocalCausalUseCase` was required to call completed P01 CLI `LocalRunManifest.from_run_evidence` directly while Application was prohibited from importing CLI concrete and its constructor provided only eleven Ports; P02 `LocalPublicationPort.seal` correctly requires an existing `ManifestValue`.

Under `DEC-G01-P05-MANIFEST-BOUNDARY-01=A`, the approved solution is:

- Define internal Application `LocalManifestFactoryPort.build(*,evidence:ManifestBuildEvidence)->ManifestValue`, with the immutable neutral evidence and runtime facts detailed in IF 23_41, DD 30_62, P05 06 and AMD-001.
- Inject `manifest_factory:LocalManifestFactoryPort` as the **twelfth required** `LocalCausalUseCase` constructor collaborator; all eleven existing Port responsibilities are unchanged.
- The CLI composition root wires `LocalManifestFactoryAdapter`. The Adapter translates neutral evidence into existing P01 nominal `RuntimeEvidence`, `ArtifactDescriptor` and `ValidatedRunEvidence`, then invokes unchanged `LocalRunManifest.from_run_evidence`. The Application does not import the CLI concrete module.
- The resulting `ManifestValue` is passed to unchanged P02 `LocalPublicationPort.seal(*,sink,manifest,privacy)`, followed by existing atomic publication and independent Reader verification.
- G01 07-06/07/11 explicitly tests Port direction, original P01 factory delegation, descriptor and provenance preservation, no validation bypass, fail-closed factory failures before seal, Product regressions and independent readback.

This approval changes only internal P05 construction wiring and corresponding normative docs; it does not grant permission to move or edit completed P01/P02 DTOs, P02 publisher/reader, P03/P04 sources or package checkpoints. If implementation reveals a necessary completed-Package modification, stop and request a separate explicit Owner decision with regression impact.

## 4. Explicit retained invariants and unfulfilled dependencies

- P02 checkpoint: `3a76a0aa1698037354b284ba7b5a875300473ce6`.
- P03 checkpoint: `858c9f73366036a2d1445e558135cd521f611462`.
- P04 checkpoint: `7dcf2061dae3c8832b2b3ec9be6900ad6ee7edb6`.
- Previously protected P01 checkpoint: `9bff61f0eae25236f95f31f2cd3e7c81291f0167`.
- Public E11 Schema Version and strict Study/Manifest/Status/Graph/ContentRef/Marker wires, six-field ArtifactDescriptor and P02 publication Port signatures remain unchanged.
- Strict FCI/PAG/Graph provenance, AMD-001/002/003/004 P04 scientific contracts, conservative CI / categorical domain / Fisher-Z preflight, no unjustified Graph-negative or scientific PASS, and no non-null BK passthrough remain unchanged.
- Independent Python3.12 Backend, real FS/Reader, independent MAG/PAG/FCI/BK, T2/T3 and protected Product v2 regression obligations continue to govern `G01_999`.
- `DEFERRED_PRODUCT_POLICY_BRIDGE` remains `UNFULFILLED`, not implemented or retired. Its shared-policy acceptance item is not PASS unless separately approved completion and independent Product regression occur or Owner separately and expressly changes acceptance phasing.

No `uv.lock`, Product v2 public API/DB/Worker/CLI contracts, other Gate/Package scope, completed checkpoint, public schema or science acceptance has been changed by this Owner formal-09 decision.

## 5. Control-plane boundary and next decision

**This is formal 09 approval only.** The prior immutable active S10 was `3ea759825810e95425a9e7557c3b2cc46b21157d`, and the previous P05 S11 `DEC-G01-P05-001-S11-REAUTH-01` was bound to it. Neither authorizes implementation against the new AMD-001 architecture contract before new explicit decisions.

The complete Git commit created by adding this 250 record is the **candidate** to be inspected and expressly approved as the new G01-S10 frozen SHA. This record itself is **not** an S10 refreeze, S11 coding authorization, P05 checkpoint, focused-test PASS or G01_999 PASS.

Next actions, in strict order:
1. Verify full resulting Git SHA includes updated IF/DD/P05 06/G01 07, AMD-001, combined_review/249 and this formal-09 record; confirm no unapproved additional changes.
2. Submit **separate** `DEC-G01-P05-001-S10-REFREEZE-01` for Owner decision against that exact full SHA.
3. Only after that explicit S10 approval, submit **separate** `DEC-G01-P05-001-S11-REAUTH-01` limited to `G01/P05/Trial01`.
4. Recheck branch/remote/worktree/lockfile/ancestry/checkpoints and package state at Coding Agent restart. Do not run P05 coding before steps 2–3.
