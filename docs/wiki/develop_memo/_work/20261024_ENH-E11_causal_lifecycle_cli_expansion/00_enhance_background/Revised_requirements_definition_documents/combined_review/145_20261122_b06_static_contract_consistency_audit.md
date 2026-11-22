# B06 — Static cross-contract consistency QA (2026-11-22)

**Review basis:** cbec5cd5d5abaae1fccbc2acbb0ef3ef1f1dd64a / branch prototype/ariadne_mvp. **Verdict: FAIL / BLOCKED**, not a Contract Freeze or a Test PASS. Full Code/Backend Science and Pxx cross-audit are not executed.

## What was actually inspected

- Source tree and exact Method profile registry: **200 unique source Schema paths all present**, 40 Methods × five types; no path missing. This is only inventory integrity.
- Catalog-to-common Output branch static equivalence for **40** Descriptor entries; eight CATE, one Event Study and one SCM internal artifact added. This is only schema object map identity, not runtime validation.
- 5 internal scientific artifact Drafts, 41 Method DGP/NEG/REF/AC Registry entries: **41/41 have planned IDs**, **41/41 still lack independent reference paths and preregistered numeric thresholds**.
- Formal requirement 10-series, targeted 22/23/30 and Gate-level 06/07 for **G01–G10 (20 files)**; representative high-risk G01/G05/G10 Pxx **6 files**. Entire 51 P00/Pxx content scan has NOT been performed; S09 covers that separately.

## Blocking findings

### QA-B03-01: BLOCKER — Output semantics

Evidence: 5 new internal typed artifacts and 10 altered Output descriptors are only structural drafts; Result/Manifest cross-file validators and independent semantics have not run.

Required resolution: Complete strict semantic validators for CATE grid/privacy, time vectors, SCM gaps and Point-only, 5 Identification Proof variants and 9 diagnostics; positive and negative fixtures, artifact readback and existing five public wire compatibility.

### QA-B04-01: BLOCKER — Effective Backend

Evidence: pyproject.toml and uv.lock lack DoWhy/EconML/Tigramite; selected version/signature/CI target Python3.12 not executed.

Required resolution: Select compatible isolated versions and run review-only API probe for ENV-BASE, DOWHY, ECONML, TIGRAMITE; no false BACKEND_AVAILABLE or CI inferential guarantees.

### QA-B01B02-01: BLOCKER — 200 Method Schema parity

Evidence: 200 distinct existing source Schema paths were found; compiler/reassembled schema equality test has not run; 40 Output candidates changed for 10 non-scalar cases.

Required resolution: Execute 200-schema meta/AST parity with fixed source SHA, verify target Method strict positive/negative instances and cross-file Method semantic validation, then replace source representation when proven.

### QA-B05-01: BLOCKER — Scientific acceptance

Evidence: 41 Method records have DGP/NEG/REF/AC IDs, but 41/41 have no independent reference implementation, Source+Fixture SHA and quantitative R/K/threshold/seed budgets; no actual science evidence.

Required resolution: Build independent reference fixtures and preregister target-specific K/R/FWER/coverage/bias/graph/topology/error/status and T2 pilot versus T3; no invented quantitative threshold.

### QA-B06-01: BLOCKER — G01 06/07 contracts

Evidence: G01 06 line 101 still exposes --allow-row-level-export; Study examples line 106/131 still policy_ref:null; G01-P05 cli_row_flag; G01 07 still checks removed flag.

Required resolution: S06/S07 replace entrypoint and Privacy Port signatures, Study examples and negatives, preserve aggregate-only G01 and old v2.

### QA-B06-02: BLOCKER — G05 06/Pxx/07

Evidence: G05 06 lines 5–8, G05 07 lines 5–8/59–63, P02/P03/P04 still require double Study+CLI opt-in and policy_ref; contradict DEC-S02 and new 23/30 contracts.

Required resolution: S06/S07 rewrite self-contained WP method signatures, per-run nonroot/root/row shape and single Study true/false positive-negative matrix.

### QA-B06-03: BLOCKER — G10 06/Pxx/07

Evidence: G10 06 still cli_row_flag and unconditional all-41 reexecution; G10 07 line 40 explicitly mandates actual rerun all; G10 P04/P05 double opt-in; incompatible with Owner-approved evidence reuse.

Required resolution: S06/S07 specify proof of transitive behavior-affecting dependency closure, all-41 valid independent evidence and affected-only rerun; unknown/changed => rerun/BLOCK; retain final candidate integration.

### QA-B06-04: BLOCKER — Method output wiring

Evidence: B03 added internal artifacts for 8 CATE, P3-M05, P3-M12 and new schema names, but corresponding G04/G07/G09 06/Pxx/07 still reflect legacy scalar point only in some places.

Required resolution: S06/S07 integrate required artifact inventory and independent acceptance, no unexpected public Schema version changes.

### QA-B06-05: PENDING — Full cross-contract coverage

Evidence: 20 Gate-level 06/07 inspected; 6 representative high-impact Pxx inspected; all 51 Gate P00/Pxx were enumerated but not all individually content-audited; 10/22/23/30 focus documents and Schema registries inspected.

Required resolution: S09 independent QA must inspect complete 51 P00/Pxx, 40 Operator and all relevant 22/23/30/10 RD/AR/AC and semantic data flows for contradictions.


## Decision

**S05 status:** `B03_TYPED_ARTIFACT_DRAFTS / B04_TARGET_ENV_BLOCKED / B01B02_COMPILER_READY_PARITY_NOT_RUN / B05_REFERENCE_IDS_TRACED_NO_QUANT_REF / B06_CROSS_CONTRACT_FAIL / S05_NOT_COMPLETE / S06_NOT_STARTED / S09_NOT_RUN / CODING_NOT_AUTHORIZED`.

This is **not** an Owner decision reopening accepted science; it is a technical inability to demonstrate compliance with those decisions. Correct current normative design text and new five E11 public wire types remain separate from outdated 06/07/Pxx Drafts until S06/S07. No agent, source, tests, pyproject, uv.lock, canonical promotion, Gate999, Freeze or Coding Authorization.
