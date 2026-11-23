# 186 — G01 Revised Provisional S10 Freeze: Owner Approval

**Decision ID:** `DEC-G01-P01-REBASELINE-01 / G01-S10-REFREEZE`  
**Decision:** `OWNER_APPROVED_REVISED_PROVISIONAL_S10`  
**Owner decision date:** 2026-11-23 JST  
**Human decision source:** Explicit Owner instruction: 「DEC-G01-P01-REBASELINE-01を承認する。09契約変更を正式承認し、指定SHAで暫定G01-S10を再Freezeせよ。その後、限定G01-S11再承認の判断に進め。」  
**Prerequisite formal 09 approval record:** `combined_review/185_20261123_g01_p01_amendment_09_owner_approved.md` (written at commit `3ec4936cc0f7bb7cac2d2a22b4b642a02049d7f1`).  
**Freeze status:** `APPROVED / PROVISIONAL_G01_S10_RE_FROZEN`  
**New frozen immutable complete source Git SHA:** **`707f6aaac1df5393dbf762448c41db2f1c9dbf35`**.  
**Approved amendment:** `AMD-E11-G01-P01-001` (formal `09` Contract Amendment).  
**Frozen `uv.lock` Git blob SHA:** `2b83110e86b26b7969fbddf8f98a727370ae19f7`.  
**Execution repository and branch:** `kousuke-ota-datascience/causal-atelier` / `feature/ariadne_mvp_e11`.  
**Next distinct required Owner decision:** **revised G01-S11 limited Coding Authorization**, not yet granted.

## 1. Immutable version binding and precedence

The specified **complete Git commit SHA** `707f6aaac1df5393dbf762448c41db2f1c9dbf35` is the normative revised G01-S10 freeze point. It contains revised primary P01 WHAT, aligned P02/P05 handoffs, G01 07 tests, 23_42/30_62 design, and the 09 proposed amendment/docket/ledger exactly as seen by the Owner at decision time. The *normative contract modification commit* `827ce97b6cc649fb694b210fdebf8a32f5d9ee96` is its ancestor. This S10 approval is binding to the **full commit `707f6aaac1df5393dbf762448c41db2f1c9dbf35`**, not a moving branch name or the later commit containing records `185/186`.

Original frozen S10 `a05fd072cbb82a7c6e43f45e7208e078f0784a2b` and Owner decision `179` remain historical; prior limited S11 `180` does not authorize the new implementation WHAT. The explicit positive formal 09 decision `185` supersedes *only the proposal/approval status* in frozen 09/183/184, not the approved normative implementation semantics. This record supersedes original `179` **for G01/P01–P05 revised contract freeze authority only**; it does not convert earlier unverified facts into PASS.

Commits made **after** `707f6aaac1df5393dbf762448c41db2f1c9dbf35` that add only historical/approval/administrative evidence (e.g., `185`, this `186`, or a future separately approved `187` limited S11) are allowed on the working branch **only after actual semantic diff confirms that effective frozen WHAT / 07 / common E11 schema / `uv.lock` did not drift**. Their inclusion in the branch does not change the immutable freeze SHA. Any subsequent normative code/contract/AC change before re-S11 requires formal impact and Owner approval, not automatic adoption.

## 2. Exact frozen scope

- **Gate:** `G01` only; **operation:** `DISCOVER`; **Method:** `P1-M06` with `causal-learn`.
- **Implementation Work Packages:** `P01,P02,P03,P04,P05`; `P00` is planning and not a coding package.
- **Order:** `P01 → (P02,P03) → P04 → P05`; Candidate Assembly only after `PACKAGE_READY` for required packages.
- **Normative contracts at new freeze SHA:** `10_enhance_instruction/G01/06_Ariadne_ENH-E11_G01_implementation_instruction.md`, `06_G01_P00_work_package_plan.md`, `06_G01_P01_local_contract_codec.md`, `06_G01_P02_atomic_publication_reader.md`, `06_G01_P03_pag_graph_version.md`, `06_G01_P04_fci_backend_oracle.md`, `06_G01_P05_cli_use_case_privacy.md`, `07_Ariadne_ENH-E11_G01_test_instruction.md`; adopted common 23_42/30_62/E11 schema and G01 profiles; operator 40 as current authorized branch-routing HOW only. No new schema/wire version or extra Method introduced.
- **Specific approved 09 amendment:** typed `ValidatedRunEvidence`, P01 Manifest projection/inventory/typed Ref joins, generated Graph trusted-root `runs/{run_id}/graph.json` versus bundle-root `graph.json`, `from_payload` only Manifest-local invariants, P02/P05/Reader owning real cross-file/FD checks, and preserved Graph-positive/scientific-negative status distinctions.

## 3. Source integrity and non-waived G01_999 ledger

At freeze preparation the GitHub source inspection found the amended norm-content files identical from `827ce97b...` through `707f6aaac1df5393dbf762448c41db2f1c9dbf35`, while the later 09/184/ledger commit only added review/control records; current source lock blob matched the historical S10 blob. Historical `s09_post_reconciliation_document_snapshot_draft14.json` (402 paths) and `s09_g01_scoped_review_inventory_draft8.json` are **not** current parity or independent S09 approval. Future coding preflight must compare changed effective paths/meaning against this new frozen SHA and validate the observed runtime state.

**Mandatory before G01_999 PASS; not waived by this provisional S10:**

| Acceptance axis | Current status | Required |
| --- | --- | --- |
| Independent G01/common scoped S09 | `NOT_RUN / EXTERNAL_PENDING` | Independent reviewer evidence |
| B02 Python3.12 strict schema/FCI profiles | `NOT_RUN / EXTERNAL_PENDING` | Actual positive and negative validations |
| B03 Linux private FS / Publisher / Reader | `NOT_IMPLEMENTED / NOT_RUN` | Actual secure FD and atomic publication/readback |
| B04 effective `fisherz/chisq/gsq` fitted backend | `NOT_RUN / EXTERNAL_PENDING` | Actual API and environment/console validation |
| B05 independent MAG/PAG/BK science, T2/T3 | `NOT_ACCEPTED / EXTERNAL_PENDING` | Independent graph oracle and BK remedy plus required trials |
| G01 07 / 999 and Product v2 regression | `NOT_RUN` | Fixed Candidate SHA, actual independent tests |

Existing `DEC-G01-EXEC-01` allows implementation before S09/B02/B04/B05 scientific evidence **only** within G01 and after distinct S10/S11. Keep all non-null BK (including empty object) typed `BACKEND_SEMANTICS_UNVERIFIED` / CLI exit 4 before FCI until independent accepted remedy. No invented DAG/Effect, science PASS, private row export, no-clobber workaround or legacy v2 change. Other Gates remain unapproved.

## 4. Coding Authorization boundary

**This document alone does not authorize coding.** New revised S10 = **APPROVED**. New revised limited S11 = **OWNER_DECISION_PENDING**.

If Owner separately approves revised limited G01-S11, commit a **distinct new S11 approval record** binding to this exact frozen full SHA and unchanged `uv.lock` blob, specifying only `G01/P01–P05` implementation/developer tests/checkpoint reporting on `feature/ariadne_mvp_e11`, with all science/FS/Gate obligations still binding. A coding agent must read the **new** S10 and **new** S11 instead of accepting historical records `179/180` as if they authorized amended WHAT.

On actual coding runtime, confirm clean working tree, exact branch, current HEAD, reachability of `707f6aaac1df5393dbf762448c41db2f1c9dbf35`, frozen/current lock Git blob and exact bytes SHA256, and that all post-freeze differences are approval/admin only. Check Trial01 has not been superseded by a formal FAIL/remediation. **Restart normal `GATE_ID=G01 PACKAGE_ID=P01 TRIAL_NO=01` only after those checks and the separate S11 approval.** No immediate run is claimed here.

## 5. Preservation

Historical Trial01 `BLOCKED_CONTRACT_AMBIGUITY` and subsequent `BLOCKED_CODING_AUTHORIZATION` reports remain intact. No P01 implementation, focused verification, Package checkpoint or fixed Candidate SHA existed at these stops. This Owner authorization is not a cryptographic signature, independent Reviewer PASS or scientific/production release.
