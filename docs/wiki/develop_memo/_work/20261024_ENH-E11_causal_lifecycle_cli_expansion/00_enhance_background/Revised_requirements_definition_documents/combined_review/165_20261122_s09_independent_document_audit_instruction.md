# ENH-E11 S09 — Independent Document-Contract Audit Instruction (standalone / 2026-11-22)

**Audience:** Independent scientific-document/architecture reviewer, **not** the original author, Coding Agent or Reference author.  
**Execution authorization:** *Document review only.* Never execute Coding Agent, modify application source/tests/uv.lock/pyproject, declare Gate999 PASS, grant Owner Contract Freeze or Coding Authorization.  
**Prior conclusions are not evidence:** The author-produced `164` report and older `148/149/163` records may identify candidate findings, but the reviewer must independently derive and adjudicate every contract claim from frozen target documents.  
**State:** `REVIEW_INSTRUCTION_DRAFT / REVIEWER_NOT_LAUNCHED / INDEPENDENT_VERDICT_NOT_AVAILABLE`.

## 0. Required invocation and immutable identity

The operator must set:
```text
REPO=kousuke-ota-datascience/causal-atelier
BRANCH=prototype/ariadne_mvp
REVIEW_TARGET_FULL_SHA=<exact 40-character git commit pinned after all document changes>
REVIEWER_ID=<actual independent reviewer identifier>
REVIEW_RUN_ID=<unique review execution ID>
OUTPUT_EVIDENCE_DIR=<review-only path outside protected app source/tests>
```

At start: resolve `git rev-parse HEAD` and verify equality with `REVIEW_TARGET_FULL_SHA`; fail closed on mismatch or dirty tree in authoritative input. Record exact Git blob SHA for every file read. The latest author-maintained discovery index is `00_enhance_background/Revised_requirements_definition_documents/combined_review/s09_post_reconciliation_document_snapshot_draft8.json` (71 Gate docs, 7 Operator prompts, 200 original Method Profiles, 5 factored bundles, 13 public/internal Schemas including ITS, **98 active stock Markdown** across RD 22 / BD 18 / IF 31 (including Schema README guides) / DD 27, plus **8 supplementary FCI/Registry/Descriptor/Science references**; 34 prior selected stock entries remain separately for traceability). Its `source_full_commit_sha` is `2e529a38f1bc19afba9bec693a9a828bb7e1f9de`, a snapshot of normative content before this author-only inventory addition. This is a **discovery index**, not proof of correctness: `doc01_review/prior_drafts` is historical and excluded from active stock; re-enumerate the actual checkout and review all current source paths at the independently pinned final full SHA. `draft1.json`–`draft7.json` remain historical. Re-enumerate the checkout at the pinned Review target and verify that **all** 71 active 06/07/P00/Pxx and **seven** Operator prompts are covered. All factual claims must cite `path @ full SHA : line range` and observed bytes or cross-reference.

## 1. Source-of-truth and authority hierarchy

Use the Owner's explicit latest decisions as the scope authority:
- DEC-S02-01..08 (combined_review/137): sole Study opt-in, removed unshipped signed policy and CLI flag, lossless factored Method profiles, all-41 valid science evidence with affected-only rerun, bounded Parquet, Local Graph content-hash lineage, bounded G01 OS/FS, impact-based protected regression.
- DEC-S05-AR01 (150): **full-real** weak-IV robust AR confidence-set target frozen as a required scientific capability; **HC1/χ²(1) quadratic inversion is provisional** pending independent mathematical review, no final algorithm authority.
- DEC-S05-02/03 (156): independent reviewer process and isolated Linux environments approved; no runtime/probe pass follows merely from approval.
- Internal requirement stock: `Revised_requirements_definition_documents/10_requirements_definition/` including FR/AR/NFR/Method 10_31/10_32; `NFR-034=MUST/DEFERRED/UNVERIFIED/FUTURE` (potential future external delivery) and internal OSS obligations active.
- Architecture/class/IF stock under `22_product_basic_design/`, `23_api_interface_design/`, `30_detailed_design/`, including 23_41/42, 30_61/62/63.
- Current E11 public draft wire Schema and internal method/typed artifact Schema. A Schema draft is not adopted numerical Science, effective Backend or generated runtime code.
- The actual **individual** `10_enhance_instruction/G01`... `G10` 06/P00/Pxx/07 documents are normative WHAT for their Gate and Work Package once frozen. They must be **self-contained** and may not require an Agent to infer missing Field/Constructor/Method/pre/post/negatives from a historical review log.
- `40_operator_workflows/agent_entry_prompts/` owns entry/runner WHERE/HOW/test discovery and evidence, **not scientific semantics**. `999` is an independent Gate decision; no acceptance by Coding author alone.

Historical decisions superseded narrowly by 137 remain historical facts, not current implementation requirements. Pre-S02 text copied into an active Pxx remains a contradiction even if a later append-only disclaimer tries to overrule it ambiguously.

## 2. Mandatory exhaustive document inventory

- All 20 current G01–G10 Gate `06_Ariadne_ENH-E11_G##_implementation_instruction.md` and `07_Ariadne_ENH-E11_G##_test_instruction.md`.
- All 51 current G01–G10 `06_G##_P00_*.md` through `Pxx`; actually discover all matching files rather than assuming every Gate has identical Pxx.
- Seven active `40_operator_workflows/agent_entry_prompts/` operational prompts: variable conventions, single Coding Agent, WP Coding Agent, Candidate Assembly, Independent Test, FAIL remediation, Gate Orchestrator; plus their README for discoverability (README does not count as one of seven).
- 10/22/23/30 stock contracts, Schema Draft README, public Study/Graph/Effect/Manifest/Status/Commit Marker and five kinds of factored per-Method Profiles (40 Methods × five kinds = **200 strict target validations**), Method dispatch Registry, P1-M06 specialized FCI profile, `internal_scientific/` typed artifacts and exact output inventory, and current G10 41-Method/10-UC Method matrix. The reviewer shall enumerate the actual file paths and missing/mismatched files rather than guessing from this outline.
- Real shared-Kernel Product v2 boundary source signatures may be inspected read-only if available to verify *declared design intent*; **do not claim execution/regression** from reading code.

No source file can be silently excluded because its textual contract appears repetitive or a previous static scan counted fewer matches.

## 3. Independent adversarial criteria (all required)

### A. Owners and scope (S02-01/02, NFR-034)
For G01, G05, G10 and cross-Gate Pxx, compare active CLI/Study `privacy.row_export_requested` single opt-in and exit/negative semantics. Verify **no active** `--allow-row-level-export`, `cli_row_flag`, `policy_ref`, `PolicyVerifier/Anchor`, signer, revoked policy, trust-store requirements. Current `e11-local-study/1` explicitly **requires** `privacy.row_export_requested`: a valid `false` row request is a Privacy denial (exit3), whereas omission/invalid datatype is strict Study validation (exit2); the removed CLI flag is an unknown option (exit2). All denied paths must have row iteration=0 and row bytes=0. Quotations that explicitly prohibit removed fields are *not* contradictions. Verify row source iteration=0 on refusal, nonroot same EUID and private ext4/XFS, Method-specific column/row/byte/memory budgets, no aggregate downgrade/leak. Verify internal/local-only delivery scope and no unconditional external-customer GPL release approval; equally reject blanket OSS compliance deferral.

### B. Method and Schema (S02-03/05)
For all 40 non-FCI Methods, map Method ID → Operation/Estimand/Backend/Inference/Question/Design/Config/Output Profile/DD/Pxx/07. Ensure shared+per-ID descriptors build **one strict Method-specific Schema**, not unsound `allOf` with `additionalProperties:false`; unsupported/missing/unknown config and `config={}` blanket acceptance fail closed. Check P1-M05 B0 `IDENTIFY` LATE target is not an effect estimate; P2-M08 conditional IV structural slope ≠ non-IV CATE; G04 `cate_surface.json` design-grid only; G07 P3-M05 `event_time_effects.json` event-time/cohort; G07 P3-M06 `effect_components=LEVEL` scalar β_L versus `LEVEL_AND_SLOPE` non-scalar β_L/β_S with required `its_components.json`, predeclared horizon/valid HAC and correct per-branch Result/Status; G09 P3-M12 `scm_gaps.json` PRE/POST point-only. Check the actual Effect Result Schema nesting: `result.json` has `point.availability=NOT_AVAILABLE`, `point.value=null` and `point.reason.code=NON_SCALAR_TARGET`; only `status.json` has top-level `point_availability=NOT_AVAILABLE`. Reject inventing Result top-level `point_availability`, bare-string `point.reason`, or a fabricated scalar. Verify Method/Study/Estimand/lineage, privacy row separation and Operation-specific Manifest required/forbidden map. Structural Schema alone is insufficient; explicitly distinguish evidence missing from semantic contradiction.

### C. Local Graph and publication (S02-06/07)
Check all G01/G06 graph contracts against actual current `e11-local-graph/1` `version_id` and `parent_version_id` **const null**: no E11 wire exceptions allowing actual Product IDs. Validate content hash on semantic JCS Graph projection vs ContentRef full bytes, separate Product compatibility wrapper and existing GraphVersion writer, scientific parent provenance, PAG/CPDAG/lag/endpoint/fidelity. Verify bounded G01 atomic OS/Reader tests include owner EUID, private modes, dirfd/O_NOFOLLOW, same FS, race/no-clobber, post-rename `PUBLICATION_INDETERMINATE`, Marker/Reader tamper negatives. Reject unsupported power-loss durability guarantee inferred from SIGKILL or invented mandatory ACL/xattr/mount namespace attestation.

### D. Science and AR (S02-04/DEC-S05-AR01)
Check 41 Method registry covers P1=20, P2=8, P3=13, exactly one owner Gate each, DGP/NEG/independent REF, 07 AC, actual Backend/CI eligibility, S05 B02/B03/B04/B05 status accurately marked BLOCKED. In G08 P3-M10 B0 binary IV LATE and P3-M11 B1 structural slope, preserve full-real AR CI set bounded/unbounded/disconnected/ALL_REAL and admissible qualified EMPTY/undefined/degenerate reasoning; scalar point availability and AR availability independent. **Detect any active 'HC1/χ² algorithm adopted/frozen' language** despite DEC-S05-AR01, while preserving it as a reviewable candidate. No finite-grid shortcut, no unreviewed weak-IV confidence coverage.

### E. G10 evidence/reuse and regression (S02-04/08)
Test the words 'all 41 science evidence' and 'rerun' for semantic separation. All 41 need valid prior independent evidence, but rerun only changed/unknown transitive *behavior-affecting* dependencies. Closure must include code, shared kernel, schema/descriptors, policy, Python, lock, Backend, fixtures, reference, tests and AC. Unknown dependencies → rerun or BLOCK; no G10 waiver of upstream 999 or final cross-Gate integration. Product v2 protected ABI regression selection by evidence-based affected closure; unknown impact → test or BLOCK, not auto-PASS. Ensure no imposition of unconditional unrelated Product full-stack suite.

### F. 06/Pxx/07/40 independence and signatures
For each 06/Pxx enumerate owned Class/Module, Fields, Constructor, public signatures, pre/post, non-goals, Method-specific target and negative outcomes; cross-check 23/30 and adjacent Pxx without requiring the implementer to infer class behavior from a separate design memo. For each 07 verify independent WHAT/AC, oracle and failure semantics with no fixed historical physical test filename/command. Keep WHERE/HOW/current test discovery in 40; respect E9 enhancement-vs-regression lifecycle and unit/contract/integration layers. Detect duplicate implementation Kernel, Local ports, Product writers and unavailable optional dependencies advertised as installed.

## 4. Proof requirements and method

For each claimed PASS criterion provide:
1. Requirement/Owner decision ID and a concrete observed line excerpt from each relevant normative document, with full Git blob SHA.
2. Positive contract path and at least one counterexample/negative path, plus exact incompatible or missing clause when a finding exists.
3. A determination of whether issue is **active normative contradiction**, unresolved design/science/blocking evidence, historical superseded text, or harmless quoted prohibition.
4. Method/Package coverage count and a complete per-file audit inventory; no counting mere keywords as defects.
5. A description of the minimum independent reproducible verification necessary before S10.

Automated regex scans, JSON parse and AST schema inspection can help discovery but cannot replace separate semantic and scientific evaluation. The reviewer must run no newly authored science backend or protected source mutation. Use `NOT_VERIFIED` or `BLOCKED` rather than manufacturing PASS. No automatic approval of new inferential statistical method or scientific target.

## 5. Output artifacts and verdict

Produce three **read-only evidence artifacts** in the assigned review area (do not overwrite 06/07/Pxx):
1. `s09_independent_file_inventory.json`: `review_target_full_sha`, all exact blob SHAs, 71/7 counts, per-file `READ/NOT_READ` and findings refs.
2. `s09_independent_finding_ledger.md`: each finding ID/severity/owner requirement/actual source paths and quoted clause/positive/negative counterexample/required amendment/blocked state.
3. `s09_independent_verdict.md`: Reviewer ID, date, executed environment, immutable target, checks performed, all unresolved blockers and explicit `PASS/FAIL/BLOCKED` **for documentation semantic consistency only**.

`PASS` is permitted only when **all** required document scopes and independent criteria are examined, no active semantic contradiction remains, exact full SHA is fixed, and no structural authority gap remains. Missing target documents or inability to verify independent provenance = `BLOCKED`. Actual inconsistent instructions = `FAIL`. Runtime B02/B03/B04 and quantitative B05 Science/AR review blockers remain separately reported even after an S09 document-consistency PASS. **Distinguish pre-coding scientific contract readiness from post-coding Gate acceptance:** S10 freezes testable Method targets, valid profiles, inference semantics and independent reference/acceptance plans with sufficient preflight evidence; S11 separately authorizes coding; actual candidate-dependent T3 numerical coverage/accuracy and final 999 PASS necessarily follow candidate implementation and must not be claimed at S10. Do not silently waive independently required pre-implementation scientific review (especially G08 HC1/χ²), Backend feasibility or unresolved Method-specific inference. Whether every T2 pilot/oracle execution is mandatory before S10 must be explicitly checked against the latest Owner authority; lack of evidence remains BLOCKED and cannot be converted into an invented PASS. **S10 is not yet approved.**

Any correction is proposed in the findings only; the original author patches 06/Pxx/07 separately and obtains a **new target SHA plus a repeat audit**. Do not self-approve revisions. This report is not a human Owner's S10 Contract Freeze or S11 Coding Authorization.

## 6. Required response to Owner

Return an itemized summary of actual sources reviewed (71+7 and stock), active defects by severity, checks that could not be performed, science/environment blocker states, the exact `review_target_full_sha`, and separate statements of **S09 document verdict, S05 science/runtime status, S10 Freeze eligibility, and S11 permission**. If a material scientific change to the Owner-approved AR inferential target is proposed, present alternatives and counterevidence rather than silently substituting a weaker confidence interval.

### S09-R12 extra check — ITS conditional payload (2026-11-22)

The author separately reconciled P3-M06 Config (`LEVEL`/`LEVEL_AND_SLOPE`), original Method Output Profile, factored output overlay and descriptor catalog to require typed `its_components.json` (new internal draft; **not** a public Result version). Independent reviewer MUST check `schema_drafts/internal_scientific/e11_its_components_draft1.schema.json` and G07 P02/P03/07: β_L scalar only for declared `LEVEL`; 2-component LEVEL_AND_SLOPE has `point.availability=NOT_AVAILABLE`/`NON_SCALAR_TARGET`; all branches require typed component evidence; no invented post-horizon or joint CI; predeclared horizon reference, β_L + hβ_S arithmetic and Method/Study/Design hash consistency are mandatory. Confirm that one scalar result was not silently reused for the two-component estimand, and that the output-profile source/factored/registry/descriptor are byte/AST/parity consistent. Draft schema and author checks are not independent science PASS. If method-specific covariance/target eligibility is undecidable, report `BLOCKED` rather than choosing a default.

### S09-P3M04 Owner-A adopted scope — no remaining owner-choice blocker (2026-11-22)

Owner **explicitly adopted A** for `DEC-S09-P3M04-01` (2026-11-22), recorded in `working_notes/20261122_dec_s09_p3_m04_staggered_scope_and_output.md`. The latest `P3-M04` Config deliberately recognizes `design_variant=[DID_2X2,STAGGERED]` syntactically; **only DID_2X2 ATT is initial science-executable**, with scalar positive `result.json` when otherwise eligible. `STAGGERED` has capability `DEFERRED` (not retired); require scientific Method preflight typed `SCIENCE_CONTRACT_NOT_AVAILABLE`/`CAPABILITY_UNAVAILABLE` CLI exit4 before Estimator/Backend or scientific row materialization and without successful Effect Bundle, silent DID_2X2/TWFE or P3-M05 fallback. Invalid/unknown Config remains strict Schema exit2. The reviewer MUST verify scope fidelity across Stock 10_32/23_42/30_63, original/factored P3-M04 Config+Output, Method dispatch/Output Catalog, G07 06/P00/P01/P02/P03/07 and G10 06/P00–P05/07. A successful P3-M04 STAGGERED estimator, a mandatory staggered ATT(g,t) positive test in the initial Gate, or simply treating a syntactically valid Config as Method availability is **FAIL**. DGP-013 remains applicable for P3-M05 Event Study and future-only P3-M04 staggered research. This Owner decision **closes the Scope ambiguity**; it does not close Runtime B02–B05 or provide independent S09 evidence, S10 Freeze or S11 Coding Authorization.

### S09 G08 original-body authority and reference integrity cross-check (2026-11-22)

Do not rely solely on the appended `DEC-S05-AR01` paragraph. Re-examine the **primary normative processing steps** and duplicated mandatory-case matrix in G08/P03 §§4–6, plus historical OD-05 authoring-allocation wording across all seven G08 06/Pxx/07: mandatory target is full-real weak-IV-robust AR set; HC1 OLS χ²(1) inversion is an independent-math-reviewed **candidate**, not already selected Coding Algorithm. The author corrected a prior direct HC1 imperative in G08/P03 §4 and matrix at the `draft6` source SHA. Check for any further concealed conflicts; independently assess the algebra, assumptions, degeneration, all-real topology and reference. Author-only evidence in `working_notes/20261122_s05_ar_hc1_candidate_author_mathematical_preflight.md` derives HC1 quadratic inversion and checks 3 illustrative sets against direct Statsmodels HC1 calculations; **this is not independent mathematical acceptance or weak-IV size/coverage evidence**.

The bounded Markdown-link author audit `combined_review/168_20261122_s09_reference_integrity_and_g08_ar_candidate_author_review.md` found and corrected four G10/P04 links (71 Gate docs/198 relative links, 33 main stock docs/50 relative links, seven Operator prompts/zero relative Markdown links). Independent reviewer should recheck all links against actual checkout and distinguish inline links from bare paths, anchors and referenced schema artifacts. Do not upgrade author link checks to a complete semantic review.

### S09-R13/R14 third-pass author corrections (2026-11-22; must be independently checked)

The Author separately detected and patched main-body AR authority ambiguities in **four G08 Pxx** (P01/P02/P03/P04): the prior unconditional `HC1 Anderson–Rubinは` sentence and mandatory HC1-reference language could be read as algorithm adoption despite Owner `DEC-S05-AR01=A` treating HC1/χ²(1) as only a preliminary candidate. Current text MUST preserve mandatory full-real weak-IV-robust AR **target** while fail-closing `BLOCKED_SCIENCE_METHOD_NOT_FROZEN` rather than shipping any candidate before independently approved numerical Method Freeze. Independently inspect all seven G08 docs and stock 23/30, actual negative tests and mathematical appropriateness. See `combined_review/169_20261122_s09_third_pass_author_contract_remediation.md`.

The Author also corrected G01/P03 §10 checklist: **all** current `e11-local-graph/1` wires must have `version_id=parent_version_id=null`; scientific parent lineage uses immutable provenance/ContentRef/hash, and any real Product GraphVersion parent linkage exists only in the separate pre-existing compatibility bridge. Independently compare actual G01/G06/G10 Class and Schema against this requirement. The **five edited normative blobs** are re-pinned in `draft8`; the earlier `draft7` SHA index is historical. The Author's bounded scans are not independent S09 adjudication, and B02–B05 remain unverified. No S10/S11 authorization follows.
