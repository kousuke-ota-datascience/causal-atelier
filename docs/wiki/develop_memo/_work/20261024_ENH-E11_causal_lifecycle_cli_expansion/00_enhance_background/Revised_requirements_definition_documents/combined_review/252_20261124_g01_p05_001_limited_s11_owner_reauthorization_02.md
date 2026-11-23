# 252 — G01/P05/Trial01 limited S11 Owner reauthorization against AMD-001 S10

**Date:** 2026-11-24 JST  
**Decision ID:** `DEC-G01-P05-001-S11-REAUTH-02`  
**Decision status:** `S11_OWNER_APPROVED / G01_P05_TRIAL01_LIMITED_CODING_AUTHORIZED / DEFERRED_PRODUCT_POLICY_BRIDGE_UNFULFILLED / G01_999_NOT_PASSED`  
**Repository:** `kousuke-ota-datascience/causal-atelier`  
**Working branch:** `feature/ariadne_mvp_e11`  
**Immutable current G01-S10 SHA:** `d5b7fab759b27ed8427a46256bac5ac8231e0c77`  
**S10 Owner decision:** `DEC-G01-P05-001-S10-REFREEZE-01` (`combined_review/251_20261124_g01_p05_001_s10_owner_refreeze.md`)  
**Formal 09 amendment:** `AMD-E11-G01-P05-001`; formal approval `DEC-G01-P05-001-FORMAL09-APPROVAL` (`combined_review/250_20261123_g01_p05_001_formal_09_owner_approved.md`)  
**Earlier P05 S11:** `DEC-G01-P05-001-S11-REAUTH-01`, bound to superseded S10 `3ea759825810e95425a9e7557c3b2cc46b21157d` and not a substitute for this decision.

## 1. Explicit Owner decision and authorization scope

Owner expressly approved:

> DEC-G01-P05-001-S11-REAUTH-02を承認する。AMD-E11-G01-P05-001に基づく新G01-S10凍結SHA d5b7fab759b27ed8427a46256bac5ac8231e0c77 を対象に、G01/P05/Trial01限定Coding Authorizationを再発行せよ。P01チェックポイント9bff61f0eae25236f95f31f2cd3e7c81291f0167、P02チェックポイント3a76a0aa1698037354b284ba7b5a875300473ce6、P03チェックポイント858c9f73366036a2d1445e558135cd521f611462、P04チェックポイント7dcf2061dae3c8832b2b3ec9be6900ad6ee7edb6、公開E11 Schema Version、既承認の科学的意味、独立科学検証・G01_999受入条件、およびDEFERRED_PRODUCT_POLICY_BRIDGE未完了依存を維持する。

This is a **new, distinct, Owner-approved limited S11 Coding Authorization** for `GATE_ID=G01 / PACKAGE_ID=P05 / TRIAL_NO=01`, and **only** against the immutable S10 SHA `d5b7fab759b27ed8427a46256bac5ac8231e0c77`. It authorizes implementation and focused developer verification of that package under the approved AMD-001 contracts; it does not authorize work in completed P01–P04, changes to the public E11 wire, or independent Gate acceptance.

## 2. Verified pre-record state

Immediately before issuing this S11 record, the remote branch HEAD was `f2fa74ea54630dc6ec49e84cb938a33f08c14cbd`. Comparing the frozen S10 SHA to this HEAD showed `ahead=1, behind=0`; the **only** post-freeze change was the Owner S10 administrative attestation `combined_review/251_20261124_g01_p05_001_s10_owner_refreeze.md`. The S10 baseline contains the AMD-001 normative design and 06/07 amendments, Owner formal 09 record 250 and audit 249.

All protected checkpoints were verified ancestors of the pre-record branch HEAD:

| Package | Protected full Git SHA | Git ancestry comparison to pre-record HEAD |
| --- | --- | --- |
| P01 | `9bff61f0eae25236f95f31f2cd3e7c81291f0167` | ancestor, ahead 90, behind 0 |
| P02 | `3a76a0aa1698037354b284ba7b5a875300473ce6` | ancestor, ahead 65, behind 0 |
| P03 | `858c9f73366036a2d1445e558135cd521f611462` | ancestor, ahead 55, behind 0 |
| P04 | `7dcf2061dae3c8832b2b3ec9be6900ad6ee7edb6` | ancestor, ahead 13, behind 0 |

Ancestry confirms reachability only; Agent must separately verify actual Package status, focused test evidence, current source compatibility and no unapproved differences. No P05 implementation, current test PASS or P05 checkpoint is asserted by these checks.

## 3. Precisely authorized G01/P05 work

- Implement `G01/P05/Trial01` using the frozen S10 normatives, especially `10_enhance_instruction/G01/06_G01_P05_cli_use_case_privacy.md`, `06_Ariadne_ENH-E11_G01_implementation_instruction.md`, and `07_Ariadne_ENH-E11_G01_test_instruction.md`, the IF `23_41_cli_scientific_ports.md`, DD `30_62_local_execution_publication.md`, and approved `AMD-E11-G01-P05-001`.
- Correct the architectural Manifest construction boundary as approved: Application-owned `LocalManifestFactoryPort.build(*,evidence:ManifestBuildEvidence)->ManifestValue`, the twelfth required immutable `LocalCausalUseCase` injection, and CLI-root-injected `LocalManifestFactoryAdapter`. Application must **not** import concrete `ariadne.interfaces.cli.*` classes. The concrete Adapter must translate neutral immutable evidence into P01 nominal `RuntimeEvidence`, `ArtifactDescriptor`, `ValidatedRunEvidence`, call the **unchanged** `LocalRunManifest.from_run_evidence`, and return `ManifestValue` without bypassing P01 validation.
- Preserve the completed P02 `LocalPublicationPort.seal(*,sink,manifest,privacy)` signature, exact six-field staged descriptors, fail-closed physical Privacy/FD/atomic publication, and independent Reader readback. `COMPLETED` requires verified committed output, not merely a staged candidate or a successful pure Manifest conversion.
- Keep P1-M06 `DISCOVER` Method registry/science/FCI, PAG uncertainty, Graph provenance, the positive-Graph versus genuinely justified negative-Graph inventory/typed reasons, explicit Backend evidence and no fabricated scientific-negative or independent PASS. Strict non-null BK remains fail-closed before FCI.
- Preserve all existing Product v2 CLI/Web/API/DB/Worker contracts and source. No public E11 `e11-local-*/1` Schema Version, `uv.lock`, completed Package contract, unrelated Gate scope or scientific meaning may change as incidental P05 integration work.

The authorized P05 new internal Port and CLI Adapter implementation are **P05-owned** and do not permit modification of protected P01–P04 source, instructions, tests or checkpoint history. If integration proves a change to any completed Package unavoidable, report exact evidence, affected tests and compatibility risks and request a separate Owner approval before the affected modification. Previously approved P01-specific exception is not a general waiver.

## 4. Independent verification and retained unfulfilled dependency

The new G01 07 Contract requires validation of the twelfth Port and CLI composition-root wiring, correct strict P01 factory delegation and no Application-to-CLI direct import, fail-closed bad evidence/descriptor/runtime/privacy/factory errors, actual stage/publish/Reader joins, and Product v2 regression. Existing P01–P04 focused tests are retained. No test result is presumed from this administrative authorization.

Independent real Python3.12/FCI/Backend and numeric/categorical CI screening, MAG/PAG/BK science, actual Linux FS/Reader/Privacy, T2/T3 and independent G01_999 approval remain mandatory. The previously selected `DEFERRED_PRODUCT_POLICY_BRIDGE` remains `UNFULFILLED`, not retired, not implemented, and still an unresolved dependency of the relevant G01_999 shared-policy acceptance item absent a separate Owner decision changing phasing. No P05 checkpoint or G01_999 PASS is granted by this S11.

## 5. Agent restart instructions and stop discipline

At restart, independently:

1. Fast-forward synchronize the designated `feature/ariadne_mvp_e11` branch and capture the **new actual full START_SHA**; ensure a clean worktree before edits.
2. Confirm exact frozen S10 SHA `d5b7fab759b27ed8427a46256bac5ac8231e0c77` is an ancestor; review **all** post-S10 differences, explicitly permitting only S10 administrative record 251 and this S11 record until new authorized coding has begun. Other changes are **not** made valid simply by being descendants.
3. Recheck `uv.lock` same Git blob and physical SHA-256 under frozen S10, current HEAD and working tree. The previously reported blob was `2b83110e86b26b7969fbddf8f98a727370ae19f7` and file SHA-256 `1d92a472fc3c750c90458a40ae5a09ba3feefbd3d99eee61b0cdbff00d31cffb`; do not assume those values without remeasurement.
4. Recheck P01/P02/P03/P04 ancestor relationships, protected package completion/verification reports, physical source compatibility and absence of an existing P05 checkpoint; inspect the effective 09/IF/DD/06/07 contracts in the frozen S10.
5. Only then execute scoped P05 implementation and focused/legacy regressions. Report exact commands, outcomes, changed paths, full checkpoint commit SHA, push result and any blocker, without inventing success or conflating independent Gate acceptance.

Unexpected contract divergence, public science/wire change, unavoidable completed Package modification, dependency inconsistency or unapproved post-freeze source diff requires fail-closed stop and Owner disposition before any affected change.

## 6. Change-control conclusion

This record is an **administrative S11 issuance only**, written after the immutable S10 freeze. The S10 target is still `d5b7fab759b27ed8427a46256bac5ac8231e0c77` and does not change to the S11-record commit SHA. This administrative commit does not modify a requirement, design, 06/07, implementation, test or prior checkpoint. S11 allows the coding Agent to start only after restart checks and cannot be construed as P05 implementation, test PASS, Product bridge completion, or G01_999 PASS.
