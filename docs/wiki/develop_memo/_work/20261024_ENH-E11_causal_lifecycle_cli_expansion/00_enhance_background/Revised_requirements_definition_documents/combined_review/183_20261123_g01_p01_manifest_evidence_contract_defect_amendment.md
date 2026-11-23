# AMD-E11-G01-P01-001 — Manifest Evidence Factory Contract Defect / Impact and Restart

**Date:** 2026-11-23 JST  
**Classification:** `CONTRACT_DEFECT` / frozen G01/P01 implementation WHAT  
**Owner direction:** A案採用（既存のPackage分掌を維持して契約を補完する）。ドキュメント改訂を指示。**改訂後S10/S11の再承認とは別。**  
**State:** `AMENDMENT_PROPOSED / REVIEW_AND_OWNER_REFREEZE_REQUIRED`

## 1. Detection / preserved prior evidence

- Execution: `G01 / P01 / Trial01`, branch `feature/ariadne_mvp_e11`, `START_SHA=6ec2f59fa71b85aeff46daf0e6740b04281e8436`.
- Coding Agent reported `BLOCKED_CONTRACT_AMBIGUITY`: `ValidatedRunEvidence` and per-artifact upstream-reference join absent from assigned frozen P01 WHAT. No implementation/test/checkpoint/push. This report remains the historical stop, not a formal Gate FAIL and not `PACKAGE_READY`.
- Prior S10 full frozen commit `a05fd072cbb82a7c6e43f45e7208e078f0784a2b`, frozen `uv.lock` blob `2b83110e86b26b7969fbddf8f98a727370ae19f7`; original 179/180 human authorization records are retained unchanged.

## 2. Amendment / scope boundary

| Contract | Changed meaning or clarification |
| --- | --- |
| `06_G01_P01_local_contract_codec.md` | Self-contained exact immutable `ValidatedRunEvidence`, `RuntimeEvidence`, `ArtifactDescriptor` fields, typed G01 Study/Status projections; deterministic Manifest field origins; explicit Graph-positive/negative inventory and all-five-field Input/Graph Output joins; typed negative tests and DoD |
| `30_62_local_execution_publication.md` §4 | Stock design alignment: P01 pure projection, P02 physical FD/Reader, P03 Graph science, P05 execution; output Graph/Study input distinction |
| `23_42_local_result_manifest_artifact.md` §2 | G01-specific `manifest.lineage.graph` means generated output Graph ref; no wire schema addition, other Operations unaffected |
| G01 `06_P02` and `06_P05` | P02 stage descriptor→P05 typed evidence→P01 factory→P02 seal/publish/independent readback. No shifting P02 physical checks into P01 |
| G01 `07` | Clarify existing 07-06/07 pure and physical upstream join negatives; no new Gate or weakened threshold |

The Schema remains `e11-local-manifest/1`; an Artifact Descriptor has exactly `key,sha256,size_bytes,media_type,privacy_class,visibility`, no new wire `upstream_ref`. Only G01 `DISCOVER/P1-M06` is instantiated; future Gates' broader Method-specific semantics are neither inferred nor edited.

Preserved: strict RFC8785 JCS, actual byte hashes and marker/hash domains, positive/negative graph and backend distinction, non-null BK fail-closed before FCI until independent remedy, private Linux no-clobber publishing and separate Reader, no rows/Effect/Science PASS, unchanged Product v2 ABI and independent S09/B02/B03/B04/B05/T2/T3/07/999 obligations.

## 3. Risk and verification requirements

- **False success**: no `COMPLETED` external run before independent P02 Reader; candidate serialized technical status does not prove publication.
- **False lineage**: Study input graph is null; output Graph ref must join the staged `graph.json` descriptor, while physical provenance and Graph's semantic content hash are separate.
- **Invalid inventory**: exact DISCOVER success/negative sets, unique safe keys, no marker/manifest self-reference, no secret or row artifact; P01 pure negative tests and P02 real readback checks remain independent.
- **No new scientific assumptions**: Graph content hash is not the file-byte SHA; independent science oracle / T3 remains mandatory.
- **Source control**: use exact amendment commit and check all effective normative paths/uv.lock for unapproved drift against the original frozen S10; changed files listed in this record. Do not treat this amendment itself as a fresh freeze.

## 4. Decision boundary / operational restart

1. Reconcile changed P01/stock design/IF/P02/P05/07, including self-containment of the **assigned P01 alone**. This author-produced amendment is not an independent S09 PASS.
2. Record formal 09 `CONTRACT_DEFECT` impact review and immutable amended Git full SHA; verify `uv.lock` Git blob unchanged. Preserve blocked Trial01 evidence.
3. Request **new distinct Owner approvals**: provisional G01-S10 re-freeze of amended source, then limited G01-S11 re-authorization. The previous 179/180 **do not cover the amended WHAT**.
4. Only after those approvals, Coding Agent reruns actual preflight on `feature/ariadne_mvp_e11`, clean worktree/current HEAD, new normative SHA, lock and Trial identity. Resume `GATE_ID=G01 PACKAGE_ID=P01 TRIAL_NO=01` unless separate formal Trial state dictates otherwise.
5. G01_999 remains BLOCKED until actual independent acceptance evidence; no G02 launch.

**No code, tests, dependency lock or historical Owner approval records are changed by this documentation amendment.**
