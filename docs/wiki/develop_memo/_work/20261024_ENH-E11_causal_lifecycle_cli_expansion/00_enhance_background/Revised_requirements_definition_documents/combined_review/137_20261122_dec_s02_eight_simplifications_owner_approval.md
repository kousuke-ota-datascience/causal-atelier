# DEC-S02 — Eight bounded simplifications: Owner adoption (2026-11-22)

**Authority:** Human Owner's explicit message, 2026-11-22 10:39 JST: “S02: すべて推奨案を採用する”.  
**Decision input:** [S01 full FR/NFR/AR / Scope re-audit](135_20261122_s01_formal_requirements_scope_reaudit.md) and [S02 options, counterexamples, impacts and proof conditions](136_20261122_s02_simplification_owner_decision_docket.md).  
**Current status:** `OWNER_ADOPTED_ALL_B_OPTIONS / PROPAGATION_REQUIRED / INDEPENDENT_QA_NOT_RUN / CODING_NOT_AUTHORIZED`.  
**Repository snapshot before decision record:** `450a3ca10e8572c85fc13b252d5f339d22d7b79a` on `prototype/ariadne_mvp`.

## 1. Explicit decision ledger

| ID | Adopted | New implementation/design policy | Required evidence / no-go |
| --- | --- | --- | --- |
| S02-01 | **B ADOPTED** | One explicit opt-in, `Study.privacy.row_export_requested=true`, is the sole local CLI user confirmation; remove `--allow-row-level-export` and `cli_row_flag`. No row export by default; persist Study opt-in in request hash. | No row iterator before early eligibility; verified nonroot EUID private ext4/XFS root, Method-specific allowlist/schema/caps, no aggregate/log leak, no silent export. Accepted risk: reusing explicitly opted-in Study intentionally authorizes subsequent same-context row output; fail when referenced sources or identity mismatch. |
| S02-02 | **B ADOPTED** | Delete orphan nullable `privacy.policy_ref` from unshipped E11 `e11-local-study/1`, active DTO/validator/examples; remove withdrawn signed policy Schema from active discovery/registry (keep Git/decision record history). | Prove no deployed E11 wire or active consumer; strict unexpected-field rejection and old Product v2 ABI safety. |
| S02-03 | **B ADOPTED** | Factor 40×5 draft Method Schemas into shared strict structural shapes + versioned per-Method scientific descriptors/constraints; generate validated per-Method compatibility/validators rather than manually duplicate 200 shapes. | Per-Method strict Positive/Negative parity; explicit Operation/Estimand, Backend, inference availability, eligibility, artifacts. Unsupported CI, absent schema, config=\{\} blanket acceptance fail-closed. Existing DRAFT != scientific acceptance. |
| S02-04 | **B ADOPTED** | G10 may reuse independently accepted upstream Science evidence for all 41 Methods where verified transitive behavior-affecting dependency closure is unchanged; only changed/affected Methods and cross-gate interaction need rerun. | Full SHA records of each upstream Gate and G10, closure including shared code/lock/fixtures/Backend/reference/tests/policy. Unproved or changed closure => rerun or BLOCK. All 41 must retain valid independently accepted DGP/NEG/REF; FWER and T2/T3 remain. |
| S02-05 | **B ADOPTED** | Common bounded Parquet writer, schema factoring by scientifically compatible estimand/output families; method-specific allowlists, semantics and resource policy retained. | IV structural effect ≠ non-IV CATE; real row/column/byte/memory budget evidence; refuse unregistered Method; no row leakage. |
| S02-06 | **B ADOPTED** | New Local-only Graph uses content hash, immutable source/parent scientific provenance. No Product GraphVersion DB lookup/write/edit/FIX in E11. | Existing Product GraphVersion unchanged. Non-null imported Product refs are not fabricated nor accepted as verified without an expressly supported verified import; otherwise fail-closed. |
| S02-07 | **B ADOPTED** | Replace exhaustive G01 FS fault-permutation burden with bounded invariant-oriented OS/process/publication/Reader matrix and real ext4/XFS. | Atomic no-clobber, valid commit marker, `PUBLICATION_INDETERMINATE` on uncertain post-rename, no falsely completed bundle, all critical positive/negative transitions covered; don't claim power-loss durability merely from SIGKILL. |
| S02-08 | **B ADOPTED** | Pxx regression and excess Ports/Factories shall be reduced by evidence-based transitive change-impact, independent stable final-SHA integration/regression and actual existing shared-Kernel ABI comparison. | Full affected legacy suite on protected shared boundary changes; avoid duplicate scientific computation, preserve old v2 semantics, lazy optional imports, type-safe negatives. Unknown impact => test or BLOCK. |

All B decisions include the detailed guardrails and adversarial cases in [136](136_20261122_s02_simplification_owner_decision_docket.md); the present record **adopts** them rather than overwriting them.

## 2. Supersession and normative scope

This decision **explicitly and narrowly supersedes** former active initial-E11 design/06/07 clauses requiring: double Study+CLI row opt-in, `privacy.policy_ref` null-only reserved wire, per-Method duplicate schema files as the sole implementation form, mandatory G10 full 41-Method rerun regardless of immutable evidence, Product GraphVersion existence checks for purely local generated graphs, exhaustive redundant F03 fault-grid, full unaffected Product-stack regression per package, and unconsumed duplicate local Ports/Factories. It supersedes those *implementation mechanisms* wherever older PREP-02/F03–F07/OD or G01–G10 text conflicts. Historical approvals remain intact as historical records; source-of-truth active contracts must be revised at S03–S08.

No approved **scientific capability or target** is removed. 19 FR, 17 AR, seven current E11 NFR; 41 Method targets, 68 Scope R/Q/N/D, 10 E11 UC remain. `NFR-034=MUST/DEFERRED/UNVERIFIED/FUTURE` per record 134, with no current external customer delivery system. Existing Product v2, Web/API/Worker/DB, RBAC and Gap-C01–04 remain protected. No blanket suspension of internal OSS obligations.

## 3. Authorized next steps and explicit block conditions

- **S03**: Amend current enhancement-local requirements 10_00, 10_90, 10_91 and bounded FR-195/NFR-031 acceptance wording; no false claim that implementation is complete.
- **S04**: Propagate to 21/22/23/30 design and new E11 unpublished wire drafts; no invented APIs or classes.
- **S05**: Factor/verify 40 Method Profiles and actual backend/independent science references. Without per-Method parity and effective evidence, keep `METHOD_PROFILE_UNAVAILABLE` and Science `BLOCKED`.
- **S06–S08**: Reconcile every affected G01–G10 06/Pxx/07 and 40 operator instructions, maintaining Document Independency and proper WHAT/HOW/999 boundaries. Do not change source/tests/lock before Coding Authorization.
- **S09**: Independent cross-document, schema, DGP/NEG/REF, ABI, test-contract verification; findings prevent passing.
- **S10**: Owner Contract Freeze only with closure evidence.
- **S11**: Scope-limited Coding Authorization is an independent explicit Owner approval; no agent launch, implementation or Gate999 PASS implied by this record.

**This S02 approval is an actual Owner decision; conditional proof requirements are NOT automatically satisfied by approval.**
