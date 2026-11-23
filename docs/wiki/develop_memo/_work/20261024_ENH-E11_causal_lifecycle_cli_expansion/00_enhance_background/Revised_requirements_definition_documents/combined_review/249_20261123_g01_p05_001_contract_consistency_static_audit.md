# 249 — G01/P05 AMD-E11-G01-P05-001 contract consistency static audit

**Date:** 2026-11-23 JST  
**Owner decision:** `DEC-G01-P05-MANIFEST-BOUNDARY-01=A`  
**Classification:** `AUTHOR_STATIC_CONTRACT_AUDIT`  
**Result:** `DOCUMENT_CONCORDANCE_PREPARED / FORMAL_09_PENDING / S10_REFREEZE_PENDING / S11_REAUTH_PENDING / P05_CODING_BLOCKED`  
**Working branch:** `feature/ariadne_mvp_e11`  
**Previous authorized S10:** `3ea759825810e95425a9e7557c3b2cc46b21157d`  
**Protected checkpoints:** P02 `3a76a0aa1698037354b284ba7b5a875300473ce6`; P03 `858c9f73366036a2d1445e558135cd521f611462`; P04 `7dcf2061dae3c8832b2b3ec9be6900ad6ee7edb6`.

## 1. Root-cause finding and selected correction

Original `30_62` / P05 06 promised a Port-only Application dependency graph and simultaneously directed Application to directly construct the P01 nominal `ValidatedRunEvidence` and call the CLI-only `LocalRunManifest.from_run_evidence`, without an injected Factory. P02 seal requires a completed Manifest. Completed P01 CLI DTO/factory and P02 Publisher are consistent with their own instructions. The defect is therefore in higher-level P05 integration/composition design; altering completed Packages to match the caller is not justified.

Owner selected a narrow dependency-inversion correction. New Application-owned `LocalManifestFactoryPort.build(*,evidence:ManifestBuildEvidence)->ManifestValue`, twelfth required injection into `LocalCausalUseCase`, and CLI-root-injected `LocalManifestFactoryAdapter` let Application pass neutral immutable validated facts to unchanged P01 nominal Factory while preserving unchanged P02 seal and Reader. Application code cannot import CLI concrete. Preserve exact six-field staged descriptors, existing runtime fields, Status and Graph provenance, P01 nominal-type and JCS validation, P02 real FD/Privacy/Marker and Reader proof.

## 2. Five-layer traceability and static checks

| Layer | Normative source | Static result |
| --- | --- | --- |
| Functional and scientific requirements | RD 10; BD 22; LDD 21 | Unchanged. No new operation, estimand, method, science oracle, scientific-negative producer or privacy permission |
| Interface | IF `23_41_cli_scientific_ports.md` §4.1a | New internal App Port, neutral evidence shape, CLI Adapter and unchanged P02 publication signature defined; published E11 wire unaffected |
| Detailed design | DD `30_62_local_execution_publication.md` §§1.2,1.3,1.8; §4 unchanged | Field table and canonical constructor now include twelfth Port; P01 remains owner of Manifest DTO and canonicalization |
| Coding | `06_G01_P05_cli_use_case_privacy.md` §§6.2,6.2a,6.4 | Direct P01 CLI DTO construction removed from Application step; stage-returned descriptors, validated status and actual runtime still required; injected Port drives concrete Factory |
| Independent verification | `07_Ariadne_ENH-E11_G01_test_instruction.md` G01-07-06/07/11 | Port wiring, no direct CLI import, nominal P01 factory delegation, negative failures before seal, actual FD/readback, science / Product regression constraints explicitly asserted |

Package plan `06_G01_P00_work_package_plan.md` and parent `06_Ariadne_ENH-E11_G01_implementation_instruction.md` contain P05 package scope and verification mapping but no contradictory eleven-Port fixed constructor signature; no unrelated edits required. Other IF `23_42` still defines P01 Manifest serialization and Publisher/Reader authority; no contradiction introduced. The new Port is *internal*, so an earlier statement that public wire/legacy product contracts are unchanged remains valid.

## 3. Compatibility and negative-path evidence disposition

- **Completed-Package protection:** No changes to completed P01/P02/P03/P04 06, 07, source, tests, or checkpoint records. P01's nominal `ValidatedRunEvidence` remains unchanged; P02 `LocalPublicationPort.seal` continues accepting `ManifestValue` and `PrivacyDecision`. Existing `ArtifactDescriptorView` was inspected: its six properties match the selected Port contract.
- **No approval to change P01/P02:** If P05 implementation exposes an unavoidable completed-Package defect, stop and seek separate Owner disposition and regression impact review. The P01 exception does not automatically apply.
- **External behavior protection:** No public `e11-local-*/1`, Manifest/Status/Graph/Marker wire version, six-field Descriptor, old Product v2 CLI/Web/API/DB/Worker, `uv.lock`, trust root/privacy authority or P1-M06 FCI/CI/scientific eligibility changes.
- **Test discipline:** Added independent test cases define required *future* behavior only. No tests were executed as part of this documentation amendment. Prior 207 focused+Product tests reported by the Coding Agent are historical, not a post-amendment verification result.
- **Open architecture dependency:** `DEFERRED_PRODUCT_POLICY_BRIDGE` remains unfulfilled and blocks its G01_999 shared-policy acceptance item absent a separately approved phasing decision. No independent G01_999 PASS claimed.
- **Residual integration risk:** Actual strict type conversion from neutral `ArtifactDescriptorView` and `ManifestRuntimeFacts` to P01's nominal immutable types, stage sequencing, and exceptions must be verified in P05 focused tests; static contract inspection is not executable evidence.

## 4. Change scope and readiness

Author-modified normative contracts: `23_41`, `30_62`, P05 `06`, G01 `07`. New candidate: `10_enhance_instruction/G01/09_ENH-E11_G01_AMD-E11-G01-P05-001_Gate_Contract_Amendment.md`. Earlier decision docket `combined_review/248` retained. This audit record `combined_review/249` is a non-normative review artifact.

**Verdict:** the specific dependency-boundary ambiguity is contractually resolved in the Author-prepared amendment candidate without modifying completed package contracts, public schema or scientific meaning. This is a **static document consistency audit**, not Owner formal 09 approval and not a test/implementation PASS. P05 Trial01 remains blocked until separate explicit formal 09 Owner approval, exact SHA S10 refreeze, and a separate G01/P05/Trial01 limited S11 reauthorization. No unearned PASS, checkpoint or authorization is asserted.
