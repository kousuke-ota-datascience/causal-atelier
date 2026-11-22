# ENH-E11 S02-01..08 — Requirements / Design / 06-07-Pxx / 40 cross-document amendment ledger

**Updated 2026-11-22 JST.** Source HEAD before this evidence-only commit: `ceb3a45bc4982c03811b17111f7e043537da8142`. Baseline before documentation amendment: `324412e3837d56d62a18b831c3c60010d6bec7c0`.

**Status:** `S03_S04_BOUNDED_REQUIREMENT_DESIGN_RECONCILED / S06_S07_71_DOCUMENTS_REVISED / S08_7_OPERATOR_ENTRY_PROMPTS_REVISED / STATIC_SCREEN_DONE / S09_INDEPENDENT_REVIEW_NOT_RUN / S10_NOT_FROZEN / S11_CODING_NOT_AUTHORIZED`. The edited documents remain DRAFT. Authoring and keyword-based inspection are not acceptance evidence, and no runtime/backend/independent science test has run as part of this simplified-requirements documentation task.

## Authoring inventory

- G01–G10 **20 Gate 06/07 and 51 P00/Pxx** = 71 updated in their actual normative execution documents (each Pxx preserves owner Gate and package-specific Method and Class responsibility).
- `40_operator_workflows/agent_entry_prompts/` **7 control prompts**, `README_40.md` and `README_40_agent_entry_prompts.md` updated. The old claim "only G01 instruction files exist" was corrected. No S11 agent invoked.
- Additional bounded stock corrections: `10_31` AR-040 (nondegenerate B0/B1 cannot be EMPTY; distinguish undefined/degenerate) and AR-043 (Local immutable scientific content-hash revision vs existing Product GraphVersion); `30_61` GraphEvidence local null Version semantics / DD GRAPH04. Other 10/23/30 stocks were inspected and already contained S02 simplification clauses from preceding updates.
- Machine inventory `s02_document_verification_manifest_draft1.json` gives exact Git **blob SHA** for 71+7 and key upstream stock references; it is an immutable baseline for S09 review, not proof of content correctness.

## 8 Owner simplifications — explicit trace

| Decision | Normative requirement/architecture interpretation | Instructions updated | Independent acceptance still required |
| --- | --- | --- | --- |
| S02-01 | Study `privacy.row_export_requested=true` sole E11 row-release opt-in; no CLI row confirmation flag | G01/G05/G10 06, 07, all Pxx and G02–G09 cross-cutting Context; 40 | Study true/false/missing, G01 aggregate only, early zero iteration/bytes, Root/Method validations |
| S02-02 | Unshipped Study `privacy.policy_ref` removed; no Ed25519/PolicyAnchor/independent signer in initial Local row release | G01/G02–G10 Pxx actual Context/Constructor/Port/signatures + 40 | Strict unknown-field/flag rejection; actual no active verifier dependencies; Product v2 unaffected |
| S02-03 | 40 Methods × 5 lossless factored Profile kinds with exact Method overlay; per-Method science constraints retained | G02/G03/G04/G06/G07/G08/G09 06/Pxx/07; G10 register/dispatch; 40 | Standard Draft202012 200 original vs rebuilt fixture parity, target-specific methods and negatives; absent => fail-closed |
| S02-04 | G10 must have valid independent science evidence for all 41; rerun only changed/unknown transitive scientific dependencies; full final cross-Gate integration remains | G10 06/07/P00..P05, 40 independent/candidate/orchestration | Correct SHA closure graph incl code/lock/ref/fixtures/Backend/Policy/AC; changed and unknown negatives |
| S02-05 | Shared bounded RowWriter and scientifically compatible schema families, not unbounded individual export | G05 06/07/P00..P04, G04/G07/G09 and 40 | Verified ordered Method column allowlist/rows/bytes/memory and no row leakage; actual Parquet/Reader |
| S02-06 | E11 Local Graph immutable scientific content hash and parent evidence; no Product GraphVersion database integration | AR-043 10_31, 30_61, G01 + G06 + cross-Gate 06/07/Pxx and 40 | null Product Version fields; nonnull import negative; preserved PAG/CPDAG/lag |
| S02-07 | G01 FS tests bounded by critical publisher/reader invariants, not exhaustive fault permutations or power-loss assertions | G01 06/07/P00..P05, 40 | Real ext4/XFS/UID/dirfd/rename/failure/readback, no false commit |
| S02-08 | Existing Product regression scope selected by justified transitive change-impact, not unconditional complete suite | all Gate 06/07/Pxx, 40; G10 | Unknown impact => run affected tests or BLOCK; unchanged ABI and final fixed-SHA integration |

`NFR-034` retains `MUST/DEFERRED/UNVERIFIED/FUTURE` for uncommitted external customer delivery; internal OSS license obligations are active, without adding a new License Governance service.

## Science/API and output distinctions that must survive simplification

- G02 P1-M05 B0 binary IV conditional **IDENTIFY-only** complier LATE, not DoWhy label cast or an effect estimate.
- G04 eight P2 estimators emit non-scalar `cate_surface.json` with Method/Estimand-distinct design grid and no observed-row content. P2-M08 conditional IV structural slope is **not** ordinary non-IV CATE.
- G07 P3-M05 emits event-time/cohort vector `event_time_effects.json`, not invented scalar effect.
- G08 P3-M10 B0 vs P3-M11 B1 retain distinct LATE/structural slope targets; the full-real AR requirement remains Owner approved. HC1+chi-square realization remains **provisional** until DEC-S05-AR01 independent statistical review.
- G09 P3-M12 SCM `scm_gaps.json` time vector remains point-only; P3-M13 SDID is a separate panel ATT target.
- Each Method retains DGP/NEG/REF/AC and actual Backend/CI acceptance; a schema description is not numerical truth.

## Static author review vs independent audit

The author compared each of 71 Gate instruction sources for legacy active `cli_row_flag`, additional CLI row flag, signed PolicyVerifier/Anchor, `Study+CLI` double-opt-in and G10 unconditional all-41 rerun. The active normative old clauses were rewritten; intentional prohibitions/unknown-field negatives can still quote removed strings. This is **a pattern-and-targeted review, not S09 independent audit**, nor proof of complete semantic consistency. The previous 117 candidate occurrences were a pre-amendment static scan, not a count of remaining defects. Reviewer must read **all** 71 Gate docs, 7 prompts, relevant 10/23/30 and schema registries at the exact full SHA, check cross-file class signatures and 06/07 WHAT/Pxx document independence, probe positive/negative declarative examples and report every contradiction.

**Deferred runtime work by Owner instruction for present stage:** B02 actual Python Draft202012 200-file validator, B04 Python3.12 separate effective Backend probes, B05 independent 41 Science oracles/pilots. These do **not** block drafting S03–S08 but prevent claiming verified Science or S10 Contract Freeze. No source, tests, pyproject, uv.lock, official canon or coding agent was changed/invoked.
