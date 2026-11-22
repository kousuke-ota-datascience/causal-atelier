# ENH-E11 S09 author second-pass — Wire/Result/Graph/Privacy consistency corrections (2026-11-22)

**Scope:** Continuation of `164` from previous thread, based on prior HEAD `b5672879b6d2beb436b26fc6ab3393fa592c9cf8`.  
**Latest changed instruction-content snapshot:** `5d439f309bd99e5ff63f1db752c21fff4260b7e9`.  
**Immutable inventory:** `s09_post_reconciliation_document_snapshot_draft2.json`, 71 Gate 06/07/Pxx and 7 Operator entry prompts, 47 selected stock/Schema references with exact blob SHA. Source snapshot pre-dates its evidence-only commit; independent reviewer must still verify their own final target full SHA.  
**State:** `AUTHOR_SECOND_PASS_COMPLETED / NO_INDEPENDENT_S09_VERDICT / SCIENTIFIC_PROBES_NOT_RUN / S10_NOT_FROZEN / S11_CODING_NOT_AUTHORIZED`.

## 1. Documented contract defects and precise corrections

| Finding | Affected normative files | Direct cross-contract inconsistency | Corrective amendment |
| --- | --- | --- | --- |
| S09-R08 — Result and Status availability fields conflated | G04 06/P00–P04/07 (7), G07 06/P00/P01/P03/07 (5), G09 06/P00/P01/P03/07 (5): **17** active docs | Internal draft `e11_local_effect_result_v1.schema.json` requires nested `point.availability`, `point.value` and **typed object** `point.reason.code`; only `e11_local_status_v1.schema.json` has top-level `point_availability`. The previous S09 amendment improperly wrote Result top-level `point_availability=NOT_AVAILABLE`, which would be rejected by the strict Effect Schema. | Set `result.point.availability=NOT_AVAILABLE`, `result.point.value=null`, `result.point.reason.code=NON_SCALAR_TARGET` and **separate** `status.point_availability=NOT_AVAILABLE`. Preserve typed `cate_surface.json`, `event_time_effects.json`, `scm_gaps.json`, Method/Estimand and independent references. No Product public schema change. |
| S09-R09 — strict Study required field versus authorization failure code and old two-opt-in 07 case | G05 06/P00–P04/07: **7** docs | Current `e11_local_study_v1.schema.json` requires `privacy.row_export_requested:boolean`. Valid Study with value false is a Privacy refusal (exit3), but a **missing** field or invalid type is structural validation (exit2). Previous G05 instructions conflated omission and false as exit3; G05-07-POL01 still mentioned “Studyのみ・CLIのみ・両方false” despite the removed CLI confirmation. | Differentiate explicit false/privacy root/Method rejection (exit3) from missing/invalid required field and removed CLI option (exit2); no RowSource iteration or row bytes on any refusal; 07-POL01 now independently tests all cases, including deprecated flag. |
| S09-R10 — stale embedded Local Graph class spec persisted despite corrected appendix | G06 P01/P03 and G10 P03/P04: **4** docs | Embedded `GraphEvidence` introduction/field table still permitted Product GraphVersion IDs as current Local wire `version_id/parent_version_id`, contradicting strict `e11_local_graph_v1.schema.json` `const null` fields and stock 30_61/S02-06. This would instruct a coder to violate the schema even though a later appendix says not to. | Revise primary Class descriptions and fields, not merely append a disclaimer. For all current E11 Local Graphs, both Product Version fields are null; scientific parent is immutably traceable via provenance and ContentRef/hash. Product IDs stay inside the separate existing Product Bridge and remain protected by old v2 ABI tests. |
| S09-R11 — G05 post-rename failure test asserted an impossible invariant | G05 07 `G05-07-WR03` | A rename may succeed and then parent-fsync/readback may fail, leaving a destination directory and marker. The former case incorrectly required “未公開、marker無し” for every rename/disk failure, conflicting with `PUBLICATION_INDETERMINATE` contract (S02-07, 30_62, G01). | Separate pre-rename aborted publication (no final Run) from post-rename uncertain state (final path/marker **may exist**). Require no `COMPLETED` claim, no destructive retry/delete/overwrite, protected private staging and independent Reader re-verification. |

These are specific content-level contradictions with positive/negative consequences, not raw regex match counts. They were updated through GitHub documentation-only commits. The previous 164 record is preserved as a historical author-review snapshot rather than retrospectively rewritten to claim a passing audit.

## 2. Further patterned inspection

At the current branch revision, every one of the **71 active Gate 06/Pxx/07 files** was separately read for the limited high-risk pattern scan: Product GraphVersion real-ID-to-Local wire mapping, legacy Study-versus-CLI row opt-in, “both flags”, omitted Study field exit3, unconditional rerun of all 41, and related `GRAPH04` old wording. The hits requiring correction were in G06 P01/P03 and G10 P03/P04; 07-POL01 and Result/Status errors were found by additional Schema-aware targeted inspection. This scan **does not certify every source line**, complete signatures, actual Method JSON Schema Standard parity, or numerical scientific correctness.

Independent `S09` must still inspect all 71 instruction bodies and seven Operator prompts together with full stock 10/22/23/30, factored 200 Method Profiles, referenced Schema, Operation/Method dispatch, output/privacy and Gate WHAT/07/40 WHERE-HOW semantics. The separate reviewer instruction `165` now includes **nested Result point vs top-level Status**, exact Study required-field exit2/Privacy exit3, and evidence-stage separation.

## 3. Distinguish pre-coding scientific contract from post-coding Gate Science

A potential **control-plane interpretation hazard** was found. G01 07 expressly says quantitative T2/T3 can be planned and completed on a fixed implemented candidate after Coding Authorization but **must precede G01 Gate 999 Science PASS**. Earlier author report 164 inadvertently reads as though actual all-41 candidate-dependent T3 results must already exist before S10 and S11. That would create a circular prerequisite (post-code implementation tests required before authorization to write code).

The current sound distinction, without relaxing any Owner-approved acceptance criteria:
- **S09/S10 before S11:** Freeze stable scientific targets, identified Method/Operation/Estimand, correctly typed Result and internal Artifact output, strict specific Profiles, feasible Backend/API/inference policy and applicable independent DGP/NEG/REF reference plus planned positive/negative coverage, pre-registration and mathematical decisions including G08 robust AR algorithm. Unverified requirements remain explicitly BLOCKED and are not asserted as accepted.
- **S11:** Separate explicit scope-limited human Owner Coding Authorization on frozen eligible 06/Pxx/07.
- **After S11, for each Gate 999:** Real candidate implementation, actual execution/method fit, independent T2/T3 as applicable, adopted thresholds, FWER and source/fixture/Backend/reviewer SHA, protected regression and fixed-full-SHA evidence. Do not move actual post-code Gate PASS earlier.
- **S10-specific uncertainty:** Whether any particular independent preimplementation T2 pilot and all 41 executable Oracle fixtures are unconditional prerequisites for the **global** S10 versus Method/Gate-specific Freeze needs independent interpretation of existing Owner/OD/PREP decisions. Do **not** treat this author clarification as a unilateral authorization to skip independently required preflight review or accept missing scientific specs.

This distinction does not change DEC-S05-AR01: full-real weak-IV robust AR inference is required; HC1/χ² inversion remains a candidate pending independent scientific assessment. No actual quantitative Science PASS is claimed.

## 4. Remaining actual blockers

1. **Independent S09 reviewer not launched.** This assistant is the modifying author and cannot adjudicate its own amendments as independent approval. `165` is a ready reviewer instruction, not a review result.
2. **S05-B02/B03**: strict 200 Method Profile real standard Draft202012 validation and actual non-scalar/Manifest/Reader cross-file probes remain unexecuted at Python3.12/target checkout. Note that static AST parity is only an author-side preliminary result.
3. **S05-B04**: target Python3.12 isolated installed optional Backend fit/inference/CI probes for DoWhy/EconML/Tigramite unavailable in this chat. An approved Linux review environment exists as a *decision*, but is not connected/executed.
4. **S05-B05**: independently reviewed scientific Method references, true/negative fixtures, G08 asymptotic inversion validity and selected target-specific pre-registration remain incomplete. Candidate-dependent T3 is not a pre-code PASS.
5. **Unresolved scientific details** explicitly remain in G06 temporal lag/zero-lag conventions, G07 P3-M06 ITS level/slope and covariance, G09 P3-M13 SDID variance/inference. No invented algorithm or backend guarantee is permitted.
6. **No Owner S10 Freeze/S11 Authorization.** G01–G10 remain DRAFT; no Coding Agent or Gate999 execution was started.

## 5. Next ordered actions / owner checkpoint

- Independent Reviewer audits the **current full SHA** and records findings with per-file blob SHA, with a new snapshot/re-review for any further edits. If another formal Contradiction exists, fix the active normative body and re-review.
- In parallel, obtain approved isolated environment B02/B03/B04 and independent scientific reference/AR review evidence; do not require these tests to pretend to have run as a condition of writing clearer documentation.
- Establish pre-coding Science contract acceptance versus post-coding Gate999 numerical execution at S10, without changing target or weakening mandatory independent tests.
- Only then request Owner S10 Contract Freeze, followed by independent Owner S11 Coding Authorization.

**Owner decisions today:** None newly requested. All prior S02 B×8, DEC-S05-AR01=A, DEC-S05-02=A and DEC-S05-03=A are preserved. Escalate with explicit options only if a remaining inference/Backend/target issue cannot be resolved under existing authority.

**Hard no-claims:** `S09_INDEPENDENT_PASS`, `S05_RUNTIME_SCIENCE_PASS`, `G08_AR_HC1_FROZEN`, `S10_FROZEN`, `S11_CODING_AUTHORIZED`, `G01-G10_999_PASS`.
