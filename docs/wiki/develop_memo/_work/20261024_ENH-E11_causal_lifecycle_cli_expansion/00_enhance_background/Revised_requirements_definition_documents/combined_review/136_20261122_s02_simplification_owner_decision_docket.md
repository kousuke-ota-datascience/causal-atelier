# ENH-E11 / S02 — Eight Simplification Decisions: Owner Decision Docket (2026-11-22)

**Record class:** UNAPPROVED decision proposal / change ledger draft; this file records candidates and reasoning, **not approval** or an amendment to normative 10/22/23/30/06/07.  
**S01:** `combined_review/135_20261122_s01_formal_requirements_scope_reaudit.md`.  
**Inspected baseline:** `111f3f895a432e160a8528458f778def98819e14` on `prototype/ariadne_mvp`; subsequent S01 commit contains a review record only.  
**Status:** `S02_OPTIONS_READY / OWNER_DECISION_REQUIRED / NO_NORMATIVE_CHANGES / NOT_FROZEN / CODING_NOT_AUTHORIZED`.

## 0. Invariants and decision discipline

Primary user: internal data scientist, local unprivileged Linux CLI, ext4/XFS owner-only trusted root. Keep the 41 adopted Methods / 68 Scope dispositions / 10 Concept UC, FR-185–203, NFR-029–033/035/036 and AR-028–044. E11 NFR-034 is **MUST/DEFERRED/UNVERIFIED/FUTURE** (conditional customer delivery); all current customer release workflows stay excluded. Preserve `causal-analysis-spec/2` and old Product Web/API/Worker/DB/GraphVersion/RBAC, old CLI ABI, scientific status and estimand distinctions, independent DGP/NEG/REF and FWER. Accepted science is not a candidate for unproved simplification.

**Choose each option explicitly:** `A=KEEP current`, `B=ADOPT bounded simplification`, `C=DEFER candidate and keep current until evidence` unless another description is given. Proposals below are **B recommendations**, each contingent on the stated proof. No option is already approved.

## 1. DEC-S02-01 — G05 double opt-in

**A (keep):** `Study.privacy.row_export_requested=true` AND CLI `--allow-row-level-export`.  
**B (propose):** one explicit Study field `privacy.row_export_requested` (default absent/false; no implicit true). Remove CLI flag, `LocalRunContext.cli_row_flag` and dual-flag Port condition. Make the Study field part of canonical request identity; apply privacy eligibility *before calling any row source iterator*, reject disallowed shapes/missing private root; keep no-row-value leakage into aggregate Result, Manifest, CLI, logs, plus `row_effects.parquet` behind G01 staging/publish/readback.  
**C:** retain A pending specific internal threat assessment.

**Reason B:** one user-authorized versioned Study decision is inspectable and reproducible. **Serious counterexample:** someone reuses a stored Study with `row_export_requested=true` during unattended execution and unintentionally produces rows. Private root prevents other UIDs but not same-UID processes or accidental internal disclosure. Accept B only if Owner accepts persistence of consent in an explicit Study as sufficient for internal local execution; consider A if fresh invocation confirmation is mandatory. No bypass of FR-195/NFR-031.

**Affected:** `10_13 FR-195`, `10_22 NFR-031` (acceptance intent retained), `23_41` CLI/Port, `23_42` manifest/row export, `e11_local_study_v1.schema.json`, `30_60`, `30_62`, G01/G05/G10 06/Pxx/07, 40 prompts. **Evidence:** schema positive/negative, source iterator zero pre-eligibility, root/ownership/FS negatives, no aggregate leak, request-hash replay identity.

## 2. DEC-S02-02 — Orphan signed-policy field and withdrawn schema

**A:** keep nullable `privacy.policy_ref` in new Study v1 and withdrawn `e11_local_row_export_policy_v1.schema.json`.  
**B (propose):** delete `privacy.policy_ref` from **not-yet-deployed new Study v1** and active DTO/semantic validator; remove withdrawn signed Policy schema from **active Schema Draft/registry** while retaining history in `combined_review/129/131/134` and Git history. Do not interpret a non-null legacy field as permission.  
**C:** defer until consumer/ABI inventory proves no consumer.

**Evidence:** Baseline `e11_local_study_v1.schema.json` allows an optional policy_ref (currently null-only semantic check); the row-policy Draft calls itself WITHDRAWN; baseline `src/ariadne/` contains no new `interfaces/cli/local_causal` implementation, so this is design-time wire revision, **not** migration of an implemented E11 wire. Still inventory examples, tests, docs, schema registry and old Product aliases. Preserve strict unknown-field rejection and unchanged Product v2.

**Affected:** `23_41`, `23_42`, `30_60/62`, Study schema + withdrawn Draft/README, G01/G05/G10 06/07. If an actual consumer is found, revert to C and plan explicit version compatibility.

## 3. DEC-S02-03 — 40×5 = 200 Method Profile Drafts

**A:** keep 200 separately maintained Draft JSON Schema documents.  
**B (propose):** extract identical structural `Config/Question/Design/Output/Inference` shapes into common strict schema definitions; store per-Method **explicit versioned descriptors/constraints** (method_id, operation, estimand, covariates, eligibility, available inference, required/forbidden artifacts, backend API and negative states); generate/compile strict method-specific validators and freeze their snapshot/hash before Gate coding. A generator must fail-closed on unrecognized Method, unsupported CI, absent profile, and invalid config; no `config={}` catch-all.  
**C:** maintain 200 until per-Method structural/behavioral parity proved.

**Observed examples:** `P2-M01/M02/M08 output_profile` have identical shapes except method_id; `P3-M10/M11 inference_profile` share conditional requested/CI structure, but `P3-M12 SCM` forces `requested=false` and `confidence_level=null` — **do not claim all 200 are equivalent**. Comparatively test each Method's original schema and the new compiled validator with accepted positive and deliberately invalid negative fixtures; where old drafts are scientifically incomplete, independent Method evidence is still mandatory.

**Affected:** `23_api_interface_design/schema_drafts/method_profiles/*`, `23_41`, `30_61/63`, G02–G10 06/Pxx/07, 40 Registry/Operator; S05 Method preflight. **No change to 41 Method scope or science acceptance.**

## 4. DEC-S02-04 — G10 41 Method rerun versus evidence reuse

**A:** G10 reruns every DGP/NEG/REF scientific test for all 41 Methods on the final candidate.  
**B (propose):** G10 independently **verifies evidence for all 41** and reruns changed/affected Methods and cross-Gate interactions; reuse canonical upstream independent 999/Science evidence only if the *transitive behavior-affecting dependency closure* (Method source, shared kernel/validator/serializer, effective backend/runtime, lock, fixture, reference, parameters and acceptance algorithm) is byte-for-byte unchanged or a justified equivalence is independently demonstrated. Full candidate SHA is always recorded and all upstream full SHAs remain traceable.  
**C:** keep A until a reliable dependency/impact model exists.

**Critical counterexample:** later G08/G09/G10 code necessarily changes the **repository full SHA**, so an exact full-commit-SHA-equality rule makes legitimate evidence reuse impossible. Conversely, reusing an upstream PASS after shared `MethodRegistry`, JCS, Estimator kernel, seed, Backend or manifest changes is invalid even if Method's own file did not change. Construct closure hashes/immutable evidence index, dependency DAG and automated invalidate/retest rules. Any unproven closure → rerun or BLOCK; never waive T2/T3 or independent known-truth reference.

**Affected:** G10 06/P04/P05/07, G01–G09 evidence metadata and canonical 999 references, `22_16`, `23_41`, `30_90`, 40 Operator. Preserve NFR-035, AR-044 and final candidate-specific integration/compatibility proof.

## 5. DEC-S02-05 — G05 CATE individual RowSchema and resource limit

**A:** all method-specific RowSchema/caps as separate author-maintained definitions.  
**B (propose):** common bounded Parquet writer, row identity, privacy-safe fields and resource limits; reuse a common RowSchema **only within scientifically compatible estimand/output families**, with explicit Method-specific permitted fields, target labels, row identity, inference types and exclusions (especially IV structural effect vs non-IV CATE); establish numeric row/column/byte/memory limits from real runtime budgets, streaming or chunked materialization and test coverage, not invented defaults.  
**C:** defer until eight CATE/DRIV output contracts and actual Parquet capability verified.

**Counterexample:** a shared schema that merges non-IV CATE(x) and conditional IV structural slope can silently mislabel outcomes and leak sensitive nuisance data; a permissive limit can cause resource exhaustion. Deny export before row iteration if no registered Method output shape. FR-193/194/195, NFR-031/035 maintained.

**Affected:** G04/G05 06/Pxx/07, `23_42`, `30_62/63`, G10 cross-operation Manifest validation.

## 6. DEC-S02-06 — Local Graph and Product GraphVersion

**A:** retain optional `version_id/parent_version_id` semantics with existence/lineage validation whenever supplied.  
**B (propose):** for **new Local-only Graph**, use scientific Graph content hash, source/content refs, upstream provenance and immutable local revision evidence; no Product DB query, Product GraphVersion write/edit/FIX service or fabricated ID. Preserve Product's existing GraphVersion semantics and leave optional Product refs as provenance for a future explicitly scoped import/interoperability path, with unsupported cross-Product validation fail-closed.  
**C:** keep full A until a real local-to-Product interop use case is approved.

**Counterexample:** dropping refs globally would corrupt imported Graph lineage and break old Product; accepting unverified non-null refs as valid Product IDs fabricates provenance. Locally created Graph refs should be null unless an approved and validated import exists.

**Affected:** `23_42` Graph JSON, `e11_local_graph_v1.schema.json`, `30_61/62`, G01/G02/G06 06/07; old Product GraphVersion remains unmodified. Retain FR-185/186, AR-028/043.

## 7. DEC-S02-07 — G01 F03 fault-grid

**A:** all currently planned crash/fsync/partial publication fault permutations blocking.  
**B (propose):** minimal **behavioral invariant-based** independent test matrix: fail before staging, during stage/serialize, after seal before publish, after directory rename/before durability confirmation, before/after commit marker, Reader on corrupt/missing/hash-mismatched bundles, no-clobber/retry; run selected real ext4 and XFS with user-level process termination and injected failure. Keep required fsync/rename ordering and explicit `PUBLICATION_INDETERMINATE` for post-rename uncertain state; don't claim power-loss proof from user-process SIGKILL simulation.  
**C:** keep A until test equivalence review.

**Counterexample:** trimming all post-rename checks allows a marker/manifest combination that advertises success but lacks validated bytes; Reader and fail-closed state must remain independently covered. NFR-030 remains MUST.

**Affected:** G01 06/P02/07, `22_16`, `23_42`, `30_62`, G05/G10 integration cases.

## 8. DEC-S02-08 — Pxx Product regression and excess Port/Factory

**A:** rerun full unaffected Product stack in each package and retain all speculative abstract Ports/Factories.  
**B (propose):** *change-impact-driven* unit/contract/CLI/backend integration regression at each Pxx, at a fixed candidate run affected Product API/CLI/Core v2 tests and Gate-wide integration tests; full legacy suite when evidence shows a protected shared boundary changed, not by blanket omission. Remove only demonstrably unconsumed E11-only Port/Factory layers (e.g., duplicate publication/bridge) after comparing real `src/ariadne/product/ports/scientific_core.py`, `scientific/core_adapter.py`, current `src/ariadne/causal/*` and new Port signatures. No duplicate estimation kernel; preserve lazy optional import, typed negative, Product v2 API and NFR-036.  
**C:** keep A pending API/ABI/dep-closure and test discovery.

**Counterexample:** a shared scientific-kernel modification may alter old Product behavior without changing Web routes; impact analysis must include transitive dependencies and serialization, not just modified path prefixes. Regression runs with evidence of the final SHA remain mandatory.

**Affected:** G01–G10 06/Pxx/07, `22_16`, `23_41`, `30_60/61/62/63`, 40 Operator/candidate assembly.

## 9. Owner selection and implementation guardrails

| Decision | Recommended | Non-negotiable additional condition |
| --- | --- | --- |
| S02-01 double opt-in | B conditional | explicit Study persisted consent considered enough; default off, early deny and no leak |
| S02-02 orphan policy schema | B conditional | no active consumer/ABI; strict unknown-key and version consistency |
| S02-03 200 schemas | B conditional | per-Method validation parity and independent science |
| S02-04 G10 repeated science | B conditional | dependency closure proof; otherwise rerun/BLOCK |
| S02-05 CATE RowSchema | B conditional | scientific estimand families separate, real bounded resource evidence |
| S02-06 Local Graph/Product refs | B conditional | no Product mutation; imported ref fail-closed |
| S02-07 F03 fault matrix | B conditional | complete no-false-success invariants, real FS |
| S02-08 Product regression/Ports | B conditional | transitive impact-regression and no duplicated core |

**Post-Owner decision only:** create Change Ledger with explicit accepted option/Owner timestamp/which prior decisions it supersedes. S03 requirements → S04 BD/IF/DD → S05 Method/Backend/Reference preflight → S06 06/Pxx → S07 07 → S08 Operator → S09 independent QA → S10 Owner Freeze → S11 Gate-scoped Coding Authorization. S03 or below cannot be marked frozen until explicit choices and proof obligations are incorporated.

No Source, tests, lock, canonical requirements, normative contracts, Coding/Independent Test Agent, Gate999 or scientific runtime execution modified by this proposal.
