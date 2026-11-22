# ENH-E11 S05-B03 — Cross-schema Author remediation and acceptance matrix

**Date:** 2026-11-22 JST  
**Authority:** AUTHOR_STATIC_CONTRACT_CHECK_AND_PATCH / no independent B03 verdict / no real ManifestReader execution / no Contract Freeze / no Coding Authorization.  
**Source:** current branch prototype/ariadne_mvp; re-pin after changes in the S09 snapshot. This note is a review/evidence record, not a canonical Product specification.

## A. Findings and implemented normative corrections

### B03-R01: Manifest technical status accepted arbitrary strings

- Before: e11_local_status_v1.schema.json limited status.technical_status to exactly COMPLETED, VALIDATION_FAILED, CAPABILITY_UNAVAILABLE, EXECUTION_FAILED, PUBLICATION_FAILED; e11_local_manifest_v1.schema.json had execution.technical_status = {type: string, minLength: 1}. Example bogus SUCCESS passed the Manifest field shape even though no legal Status envelope could represent it.
- After: Manifest execution.technical_status now uses the **identical 5-item enum**. This removes an unsupported Manifest state from the draft Schema.
- **Still semantic:** Per-run Manifest.execution.technical_status MUST equal Status.technical_status. For a correctly committed, independently read-back run both are COMPLETED. Enums alone cannot compare two separate files or prove a durable commit. G01/P02 and G10/P03 Reader and G01/G10 07 now explicitly include both negative cases.

### B03-R02: Internal scientific ContentRef relative_key path guard weaker than Public

- Before: Public Study/Result/Manifest ContentRef required a bounded relative key rejecting absolute, traversal, double separator, backslash and NUL; six internal Schema families declared a total of **21 nested ContentRefs** with only {type:string, minLength:1}. Path strings such as ../secret could pass those nested string shapes.
- After: Added the exact public relative_key regex to all **21 reference shapes**, with no field name/Schema ID change:
  - e11_cate_surface_draft1.schema.json (3 references)
  - e11_event_time_effects_draft1.schema.json (3)
  - e11_identification_proof_draft1.schema.json (6)
  - e11_its_components_draft1.schema.json (1)
  - e11_method_diagnostics_draft1.schema.json (3)
  - e11_scm_gaps_draft1.schema.json (5)
- **Bounded Author guard smoke:** expected accepted: study.json, predeclared/grid.json, outputs/its_components.json; expected rejected: ../secrets, artifact/../../secret, /absolute, nested//file, folder\\secret, NUL-containing key. Regex subset matched expected results; not a standard Python jsonschema test.
- **Still semantic/security:** Regex does not prove owner, fd identity, mount/local FS, symlink/race, existence, MIME, mode or content digest, nor prevent all normalized path aliases such as ./ if the Reader does not reject them. Actual safe dirfd/openat2 or per-component openat/O_NOFOLLOW validation remains mandatory. These patterns cannot be used to claim that an arbitrary external file is safe to read.

### B03-R03: Main-body 06/07 propagation

Updated current normative Gate documents, not simply historical notes:

1. G01/06_G01_P02_atomic_publication_reader.md: Reader sequence, exact status equality, internal key gate and safe FD requirements.
2. G01/07_Ariadne_ENH-E11_G01_test_instruction.md: B03 negatives in the 07 deterministic/contract matrix.
3. G10/06_G10_P03_replay_manifest.md: shared G01 Reader reuse and cross-artifact verification semantics.
4. G10/07_Ariadne_ENH-E11_G10_test_instruction.md: whole-bundle positive/negative cases, method-specific outputs and status/privacy.

No new Method scientific estimand, Backend version, inference method, public Result wire, Product v2 ABI or additional CLI policy flag was introduced.

## B. Actual Author static cross-schema comparison (19/19)

Independently read six actual public E11 Schema JSON files after R01 and 13 listed public/internal Schema IDs to confirm uniqueness. Compared these **specific** cross-JSON properties in the author V8 process:

| Group | Exact comparisons | Checked |
| --- | --- | ---: |
| Study/Manifest | operation enum, analysis_mode enum | 2/2 |
| Manifest/Status | technical_status enum | 1/1 |
| Status/Result | identification status, point availability, inference availability, science acceptance state enums | 4/4 |
| Run IDs | Study pattern vs Result, Status, Manifest, Marker | 4/4 |
| Schema dispatch | Study/Status/Result version constants vs Manifest.schema_dispatch | 3/3 |
| Request identity | Manifest.request_hash pattern vs Marker.request_hash pattern | 1/1 |
| ContentRef | Study.relative_key pattern vs Result and Manifest | 2/2 |
| Local Graph | version_id and parent_version_id strictly null | 2/2 |
| **Total** |  | **19/19** |

No mismatch observed in these 19 static comparisons. This proves neither Schema meta-validity nor cross-artifact instance validity.

## C. Independent B03 acceptance matrix: pre-code specification vs post-code evidence

| ID | Contractual test obligation | Pre-code / S09 review deliverable | Real verification after Coding Authorization |
| --- | --- | --- | --- |
| B03-01 | Same run_id across Study/Manifest/Marker/Status/optional Result | fixed closed version and patterns | mutated mismatch rejected by real Reader |
| B03-02 | Marker exact-byte Manifest sha256 and request_hash, marker outside inventory | canonical hash-domain and path definition | recompute opened-FD SHA; tampered marker/Manifest rejected |
| B03-03 | Artifact inventory exact key, hash, byte length, media/privacy and no duplicate/missing/extra | inventory and expected Operation matrix | hash from opened file bytes, no unknown or duplicate payload |
| B03-04 | Manifest/Status identical typed technical_status | identical 5-valued enum and equality rule | invalid SUCCESS and mismatching COMPLETED/FAILED rejected |
| B03-05 | Schema dispatch / Operation discriminators | all six operations and positive/forbidden artifacts catalogued | no fabricated Result in DISCOVER/IDENTIFY; positive ESTIMATE requirements verified |
| B03-06 | Safe relative ContentRef across public/internal | same lexical guard; forbidden path vectors | actual private non-root FS dirfd, O_NOFOLLOW/race, owner/mode and SHA |
| B03-07 | Status/Result scientific envelopes | 4 exact status/discriminator enum pairs and typed null/reason contracts | point/uncertainty/identification/science fields cross-checked, false PASS rejected |
| B03-08 | Study-only G05 row opt-in | row_export_requested true only; deny/typed exit conditions; Method row schema and caps | no restricted Source reads or row bytes on deny; authorized real Parquet writer/readback |
| B03-09 | P2-M01..08 CATE vs DRIV estimand identity | typed cate_surface, predeclared non-observed grid, P2-M08 structural IV slope | grid identity, duplicate keys, no individual rows, Result non-scalar, CI availability evidence |
| B03-10 | P3-M05 Event Study | event_time_effects typed, reference period, cohort/time design, non-scalar Result | duplicate cohort x event_time rejected, pretrend evidence and ref period checked |
| B03-11 | P3-M06 ITS | LEVEL scalar beta_L; LEVEL_AND_SLOPE sidecar and non-scalar Result, predeclared h | beta_L/beta_S, h uniqueness, post-horizon arithmetic, false scalar/HAC CI rejected |
| B03-12 | P3-M12 SCM | scm_gaps time-indexed typed series, point NOT_AVAILABLE, no unvalidated interval | sorted pre/post, valid donor, gap=observed minus counterfactual within reviewed tolerance |
| B03-13 | G08 weak-IV AR confidence-set representation | full-real set topology/no bounded-grid proof, approved vs candidate method separated | all-real/disconnected/unbounded/degenerate independently serialized/read back; B05 separately verifies numeric validity |
| B03-14 | Atomic Publisher no false COMPLETE | state transition/no-clobber/indeterminate contract | real ext4/XFS same-FS rename/fsync/collision/crash/readback tests |
| B03-15 | Protected Product v2 | no public ABI change; separate Bridge for GraphVersion | actual existing v2 regression suite and new Local E11 suite both pass |

**Phase boundary:** S10 is a *pre-coding scientific/document contract freeze*. Before S10, all contracts, precise negative cases, owned Port/Class/signature/Reader behavior, target scientific rules and available independent design evidence must be reviewed; **an unimplemented E11 Publisher/Reader cannot supply real production E11 integration PASS before S11 authorization**. The real post-implementation obligations above are G01/G05/G07/G09/G10 07/999 and must not be prematurely claimed. This phase distinction is not a waiver of scientific algorithm review (e.g., G08 B05), actual Backend compatibility necessary for selecting a valid contract, or the requirement for independent S09 document audit. Owner-approved S10 authority remains necessary and its exact prerequisites must be determined without circular proof assumptions.

## D. Remaining evidence and freeze state

- **Static Author correction performed:** R01 Manifest enum + R02 21 internal reference pattern placements + R03 four Gate 06/07 norms, 19/19 bounded static source comparisons. **No real application code, test implementation, Python3.12 target validation, actual Reader, CI or backend execution.**
- **Formal B03 remains BLOCKED**, not a false PASS. Independent 07 after coding must reject deliberately corrupted fully-realized bundles. No protected Product code/tests/pyproject/uv.lock modified.
- **S09 independent verdict NOT_RUN**; all seven edited draft Schema blob SHA plus four Gate docs must be included in a newly pinned index. Reviewer must inspect actual code-readback security semantics and determine if any pre-code contract gap remains.
- **S05 B02/B04/B05 remain pending**; independent statistical AR method/coverage is separate from B03 codec representation. **S10 NOT_FROZEN / S11 NOT_AUTHORIZED**.

## E. B03-R04 — durable stock 23_42/30_62 alignment after R01–R03

Follow-up author consistency review found the new closed technical-status and internal-ContentRef contract had been propagated to four active G01/G10 06/07 Gate instructions, but the corresponding active stock design needed the same permanent explanatory contract. This is independent of the enhance-specific review chronology.

- Revised `23_api_interface_design/23_42_local_result_manifest_artifact.md` to specify the five admissible technical states, exact Manifest-versus-Status value equality, genuine completed-state/readback boundary, internal lexical ContentRef protection and independent FS/FD/hashing authority.
- Revised `30_detailed_design/30_62_local_execution_publication.md` in the Reader method section: verified run identity/operation/Method/schema-dispatch/Privacy, no acceptance of unknown/mismatched status, unsafe internal paths, duplicate keys, or unauthorized private artifact.
- Captured two unique changed stock document blobs in `combined_review/s09_post_reconciliation_document_snapshot_draft10.json` with **source_full_commit_sha `a3268a1cf104e28e4508744b87db3c49237bda27`**. Earlier snapshot draft9 is historical.
- These are normative design author edits only. Actual standard Schema validation and integration/independent Reader security evaluation remain unexecuted. No Owner decision or Pre-code Contract Freeze was implied.
