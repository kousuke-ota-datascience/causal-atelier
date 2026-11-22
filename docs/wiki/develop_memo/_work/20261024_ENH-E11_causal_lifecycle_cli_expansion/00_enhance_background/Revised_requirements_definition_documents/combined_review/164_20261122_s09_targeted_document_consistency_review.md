# ENH-E11 / S09 — Targeted Cross-Document Consistency Review and Correction Ledger (2026-11-22)

**Scope:** Owner-adopted S02-01..08 simplifications, S03–S08 enhancement-local 10/23/30/06/Pxx/07/40 contract propagation.  
**Authority:** Owner DEC-S02 (combined_review/137), DEC-S05-AR01 (150), DEC-S05-02/03 (156).  
**Audit type/status:** `TARGETED_AUTHOR_SEMANTIC_RECONCILIATION_COMPLETE / INDEPENDENT_S09_NOT_RUN / S05_RUNTIME_SCIENCE_BLOCKED / S10_NOT_FROZEN / S11_CODING_NOT_AUTHORIZED`.  
**Source revision:** `prototype/ariadne_mvp`, post-edit candidate content at full commit `f639b3ed863b1b0175a6be44aa6b1177d880a2da`. An exact 71 Gate + 7 Operator + 14 selected authority document **blob inventory** is held in `s09_post_reconciliation_document_snapshot_draft1.json`; that inventory is **not** evidence that all semantic contracts passed independent review. It was created in the subsequent commit `cf4994800a8b6e0cbb57224b4aa6328801f67c64`.

## 1. Boundaries and prior state

The preceding `163_20261122_s02_eight_simplifications_instruction_crosswalk.md` records S03–S08 authoring across all 71 Gate instructions (20 06/07 plus 51 P00/Pxx), seven Operator entry prompts and related requirement/design stock. The prior `s02_document_verification_manifest_draft1.json` intentionally pins **pre-correction** blob SHAs and is historical, **not the latest executable instruction baseline**.

No implementation files, tests, dependency lock, official canonical Product requirement documents, Production/Web/API/DB, review agents or Gate 999 were modified or executed during this S09 document review. `S09` has **not** been performed by an independent reviewer, nor were backend/science/FS runtime probes executed.

## 2. Concrete contradictions corrected in current normative docs

| Finding | Document locations revised | Corrected executable meaning | Proof that still has to occur |
| --- | --- | --- | --- |
| S09-DOC-01 — G05 legacy double-opt-in survived in 'both ... flags' phrasing | G05 06, P00–P04, 07 (7 files) | **Single** `Study.privacy.row_export_requested=true` opt-in only. No extra CLI flag, signed `policy_ref`, third-party signer or Trust Store. Same-EUID private ext4/XFS root, Method RowSchema and row/byte/memory limits remain mandatory. | True/false/missing Study, missing flag rejection, no premature row iteration, actual private FS/Parquet/Reader negative tests. |
| S09-DOC-02 — G01 Local Graph ID table admitted Product IDs forbidden by the active Local schema | G01 P03, G01 07 and IF 23_41 (3 files) | `e11-local-graph/1` must always emit/read `version_id=null,parent_version_id=null`; scientific graph parent is immutable provenance/ContentRef/hash; existing Product GraphVersion ID is handled only by **separate existing Product compatibility bridge**, not E11 Local wire. | Strict current schema, non-null import negative, temporal/PAG semantics, existing Product graph ABI/parent tests. |
| S09-DOC-03 — G04 conditional effect function lacked a concrete non-scalar result contract in Gate instruction | G04 06/P00–P04/07 (7 files) | P2-M01–M08 require typed `cate_surface.json` on predeclared, **non-observed** grid and `result.json point.NOT_AVAILABLE / NON_SCALAR_TARGET`. P2-M08 is IV structural slope, not non-IV CATE. G05 separately controls person-level Parquet; `GRID_UNSPECIFIED` is a typed refusal. | Method-by-Method grid/estimand/lineage, no row leakage, real bundle/Reader and independent DGP/REF positive/negative. |
| S09-DOC-04 — G07 Event Study declared representation 'to be approved' despite B03/23_42 already specifying it | G07 06/P00/P01/P02/P03/07 (6 files) | P3-M05 Event Study publishes typed `event_time_effects.json`, with event-time/cohort/reference/pretrend semantics, separate `point.NOT_AVAILABLE`; P3-M04 DiD and P3-M06 ITS are different estimands and outputs. | Actual event-time/cohort/reference negative cases, vector-level Oracle and independent readback. ITS seasonality/HAC/inference configuration remains open. |
| S09-DOC-05 — G09 SCM time-indexed target not fully realized in package Result/Artifact interface | G09 06/P00/P01/P03/07 (5 files) | P3-M12 SCM publishes typed PRE+POST `scm_gaps.json` with observed/counterfactual/gap identity, donor/preperiod/objective references, scalar `point.NOT_AVAILABLE`, **point-only** inference. P3-M13 SDID retains distinct panel ATT. | PRE/POST, donor contamination, arithmetic, source/hash and no-fabricated-CI independent tests; SDID variance/API unresolved. |
| S09-DOC-06 — G06 temporal Graph clauses treated Local artifact ID as Product version parent | G06 P01/P03/07 (3 files) | Local Graph `version_id=parent_version_id=null`, parent scientific provenance/content hash; temporal lag/endpoint semantics remain lossless. Product IDs only in separate bridge. | Real Tigramite APIs, lag-sign/time ordering/endpoint oracle and strict negative imports. G06 time convention explicitly still un-frozen. |
| S09-DOC-07 — G08/30_63 AR algorithm asserted frozen HC1/χ² despite DEC-S05-AR01 Review First | G08 P00/P03/P04 and stock DD 30_63 (4 files) | Full-real-domain weak-IV-robust AR inference and set topology retained as **Owner-approved requirement**. HC1/χ²(1) OLS residual-test/inversion remains an **unfrozen candidate**, not a mandatory exact implementation, until independent mathematical-statistical adjudication. | Independent review derivation and asymptotic/degeneracy/topology/oracle/coverage; full real, no finite-grid truncation; T2/T3 prereg. |

A current report is not allowed to treat earlier `148/149` findings or the old `s02_document_verification_manifest_draft1.json` blob SHAs as evidence of *remaining* defects: those were prior snapshots and 71-file static candidate counts. This report identifies actual changed text and its state only, without asserting a new exhaustive independent audit or a successful 71-document semantic recheck.

## 3. Additional inspected sources without new owner decisions

- Targeted inspection of all G01–G10 Gate 06/07/Pxx documents, completing the remaining G07/P02 and G09/P02 reads in this pass; this is **author review/targeted structural-semantic search**, not independent acceptance of every line.
- Targeted inspection of seven Operator entry prompts and the prompt README showed current S02 single Study opt-in, factored Method profiles, G10 all-41 evidence with **affected-only rerun**, and fixed-SHA/independent-999 constraints. No conflicting active Operator requirement requiring unconditional all-41 rerun identified in the inspected passages.
- Review of five public/local wire drafts and typed internal `cate_surface`, `event_time_effects`, `scm_gaps` contracts: shape-only; no real artifact graph cross-readback performed.
- G03 Refutation/Sensitivity/Diagnosis retains `diagnostics.json` and no fake Effect result; G10 preserves all-41 evidence validity separately from change-dependent rerun. Those observations are not assertions of runtime validity.

## 4. Blocking findings (classification must not be relaxed)

| ID | Blocker | Release/Gate consequence | Next required evidence/action |
| --- | --- | --- | --- |
| BLK-S05-B02 | Actual Python 3.12 Draft202012 standard-validator verification of factored 40×5 Method profiles at fixed SHA, positive/negative and 200 original-vs-compiled parity **not run** | Method profile scientific availability cannot be declared; S10 not proven | Owner-approved isolated Linux Python 3.12 validation; archive full SHA, package/environment/fixture/result hashes. |
| BLK-S05-B03 | Real typed non-scalar Artifact cross-file readback, Method/Estimand/Study/Status/source/Manifest identities **not run** | Typed internal artifact/Reader contract unverified | Construct and independently verify actual CATE/Event Study/SCM and negative artifacts. |
| BLK-S05-B04 | DoWhy/EconML/Tigramite exact Python3.12 installed Backend fit/inference/CI APIs **not probed**; unpinned optional packages | No blanket Backend/API support promise | Separate isolated ENV-BASE/DOWHY/ECONML/TIGRAMITE fitted and negative probes and immutable resolution evidence. |
| BLK-S05-B05 | Forty-one independently accepted DGP/NEG/REF oracles, preregistered K/R/threshold/MC-SE/coverage and actual T2/T3 not complete; AR independent statistic review absent | No scientific PASS, no S10 Freeze; G08 AR exact algorithm not authorized | Independent math/statistics + 41 target-specific reference/acceptance evidence; escalate only material target/risk change. |
| BLK-S09-IND | 71 instructions, seven Operator prompts, 10/22/23/30/Schema source-of-truth and signatures not yet audited by a separate independent reviewer on **the final** full SHA | S09 independent QA PASS not issued | Separate clean-context reviewer with cross-reference/ABI/authority/WHAT-HOW/Method/negative inventory, sign-off and immutable evidence. |
| BLK-S10-SCI-DESIGN | G06 lag-time/contemporaneous convention, G07 ITS covariance and G09 SDID inference rules explicitly remain method-specific review/freeze inputs | Source documents describe uncertainties; no false freezing or silently chosen inference | Independent Method-specific scientific reference + target/backend preflight and documented contract resolution before relevant Gate freeze. |

The Owner previously approved an independent reviewer workflow and isolated Linux VM review environment, **not actual environment access or a completed review**. This chat can edit documentation via a connected GitHub repository but cannot launch the Owner's existing Linux VM or Codex CLI session. This is an execution blocker for actual runtime probes, not for the documentation amendments here.

## 5. Remaining control-plane sequence

1. **S09**: independent cross-document reviewer evaluates final content snapshot, including explicit corrections above, all 71 06/Pxx/07 and seven Operator entry prompts, current 10/22/23/30 and 5 public payload draft schemas, strict Method-specific profile dispatch, 41 DGP/NEG/REF and AR scientific target constraints. Any findings → patch → new immutable snapshot → re-review.
2. **S05 runtime/science closure in parallel** with documentation review on approved Linux/independent reviewer; impossible to claim accepted Science from planning artifacts.
3. **S10**: formal Owner Contract Freeze only upon completed independent document+science+backend evidence and exact-sha acceptance. An older pre-correction or author-only manifest is not a Freeze baseline.
4. **S11**: separate explicit scope-limited Owner Coding Authorization. Neither S02 adoption, S09 author corrections nor the existence of 06/07 provides that approval.

**Owner decision requested now:** None. Existing S02 B×8 and DEC-S05 A decisions remain in force. If independent AR review, actual Backend API or target-specific scientific validation produces a material new choice, report options and evidence; do not silently modify the accepted target.

**Do-not-claim:** `S05_PASS`, `S09_INDEPENDENT_PASS`, `S10_FROZEN`, `S11_CODING_AUTHORIZED`, `41_SCIENCE_ACCEPTED`, `BACKEND_VERIFIED`.
