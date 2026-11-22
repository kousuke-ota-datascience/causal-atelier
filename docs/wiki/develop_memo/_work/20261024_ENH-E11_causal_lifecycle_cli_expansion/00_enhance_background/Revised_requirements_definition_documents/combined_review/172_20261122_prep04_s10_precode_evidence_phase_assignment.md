# ENH-E11 PREP-04 → PREP-05 → PREP-06 → Coding Authorization: evidence phase assignment

**2026-11-23 G01 precedence notice — DEC-G01-EXEC-01 Owner adopted:** The G01-specific pre-S10/pre-S11 evidence requirements and the “next step” prescriptions below are **historical**, superseded **only for G01** by [177](177_20261123_dec_g01_exec01_owner_adopted_evidence_rephasing.md). Python3.12 B02/B04 and truly independent S09/B05 are **EXTERNAL_PENDING** and become mandatory before G01_999, not before **separately Owner-approved provisional G01-S10 → separately Owner-approved limited G01-S11**. Source-level Author contract reconciliation and an explicitly acknowledged exception ledger are the pre-S10 inputs. No actual Owner S10/S11 approval, science/VM evidence or Agent authorization is implied. Other Gates retain B.

**Date:** 2026-11-22 JST  
**Purpose:** Reconnect S01–S11 simplification back to original PREP-01..06 / Gate workflow and distinguish **pre-code design-authority evidence** from **post-authorization implementation acceptance**.  
**Status:** `DEC-PREPCODE-01_B_OWNER_ADOPTED / GATE_SCOPED_S09_S10_S11 / S09_INDEPENDENT_NOT_RUN / S10_NOT_FROZEN / S11_NOT_AUTHORIZED`.  
**Scope:** Design/control-plane clarification only; not a new Method scope, numeric threshold, signed Owner decision, production implementation, or independent scientific PASS.

## 1. Original control plane and implementation entry

| Original phase | S01–S11 mapping | Actual position |
| --- | --- | --- |
| PREP-01 requirement reconciliation | S01/S03 | owner simplification reflected in enhanced requirement drafts; after-S02 author document revision performed |
| PREP-02 common IF/architecture | S04 | amended, author-reviewed; independent final review not yet adjudicated |
| PREP-03 self-contained Gate06/P00/Pxx/07 and DAG | S06–S08 reference baseline | initial Owner static audit accepted; 71 Gate docs plus seven Operator entries updated after bounded simplification, remain draft |
| PREP-04.1 Method Profile / 04.2 local Row authority | S02/S04/S05 | 40×5 source/factored author material prepared; standard validation/real compatibility pending |
| PREP-04.3 Method/Backend/independent scientific Reference | S05 | principal unresolved pre-coding contract and environment work |
| PREP-04.4 cross-contract author finalization | S06/S07/S08/author S09 | source-level author reconciliation done; not independent audit |
| PREP-05 independent QA | Gate-scoped S09 + global impact inventory | 402 source paths indexed for global impact; G01 common+owned+upstream independent semantics **NOT_RUN** |
| PREP-06 Contract Freeze | Gate-scoped S10 | Owner explicitly adopted staged scope; G01 and all other Gates **NOT_FROZEN** |
| Owner Coding Authorization | S11 | none; Gate 01..10 06/07 remain unfrozen, no Coding Agent launch |
| Trial / Independent Test / Gate999 | after S11 | real candidate E11 app FS/Method tests unavailable before implementation |

Current G01 scope source: `combined_review/s09_g01_scoped_review_inventory_draft3.json` (initial 85 candidate paths: G01 11 owned incl 3 active FCI Schema, shared 69, impact sample 5 incl 1 historical non-dispatch FCI Schema; later Gate 317 NOT_REVIEWED). Actual independent Reviewer expands dependencies; no PASS.

Current active control index: `s09_post_reconciliation_document_snapshot_draft12.json`, 71 Gate + 7 Operator + 200 original Profile + 5 factored bundles + 13 schema + 98 stock + 8 supplemental source assets = 402 unique blobs. Selected 34 stock repeats the 98, not additive. Index SHA match is integrity **only**, not a semantic review.

## 2. PREP-04 / S05 blockers — separate genuinely pre-code and post-code observations

| Blocker | Must be reviewable before the relevant Coding Authorization | Can be observed only on implemented E11 candidate (later 07/999) | Current verified evidence and uncertainty |
| --- | --- | --- | --- |
| **B02** schema factoring/dispatch | approved 40×5 strict Method-specific source/factored JSON Schema meta-validity and structure/positive/negative source parity, no wrong-target acceptance; for **G01**, its separate FCI Profile must pass | actual 40 Method runtime registration, actual CLI rejection/positive flows, protected v2 integration | 200 source blob SHA and AST equality author evidence, 862 generated JS subset fixtures checks, no approved Python3.12 200-file Draft202012 run; `e11_profile_factor_compiler.py` runbook exists |
| **B03** Output/Manifest/Reader | complete Method/Operation/Result-vs-Status, exact File Inventory, ContentRef/root safety, scalar/non-scalar (CATE/Event/ITS/SCM), no-fabricated Effect, zero-row-unauthorized and fail-closed **contract**; construct independent *synthetic examples* and verify unshipped JSON shapes where possible | real `LocalManifestReader` / Publisher same-FD/permissions/hash/atomic no-clobber/readback, actual CATE/Event/ITS/SCM and Parquet outputs | B03 Author R01–R04 Schema/stock/G01/G10 reconciled, 19 cross-Schema comparisons, no actual E11 Reader/Bundle validation |
| **B04** target backend dependencies | pinned isolated Python3.12 resolver/distribution, import/signature, feasible **package-level tiny fitted positive/negative probes** for only relevant Gate/backend and agreed inference semantics. Optional ENV-COMBINED not mandatory | actual integrated E11 Adapter/Method fit, effective persisted CI, Graph/Result/Status/Backend fallback denial, final lock/regression | ENV-BASE, DOWHY, ECONML, TIGRAMITE profiles candidate-only; target environments not actually connected or probed |
| **B05** Method science | target/estimand/identification assumptions, algorithm definition and limitations, testable negative-state semantics, independently authored truth-oracle and data-generating specification, reference/evidence method independence, validated statistical acceptance *protocol*; AR full-real capability always retained and any exact HC1/chi-square algorithm cannot be assumed adopted | Method-specific actual candidate T1/T2 pilot and T3 confirmatory, K/R calibrated from T2 (or independent pre-code pilot when genuinely possible), observed bias/coverage/graph/AR topology and FWER with frozen confirmatory seeds | 41/41 proposed oracle designs; independently implemented references and fixture SHA **0/41**, quantitative threshold/K/R/seed fields **0/41**; G08 algorithm independently not reviewed. Exact numeric parameters are not invented; full T3 PASS cannot be pre-code |
| **B06** and S06–S08 | latest approved simplification in all affected normative RD/BD/IF/DD/Gate06/Pxx/07/Operator, self-contained WHAT and independent 07/999 evidence requests, no stale signed policy/double flag | actual published Test Agent discovery, collection, command/fixture/positive-negative results after Coding Authorization | 71+7 author-updated; S09 independent NOT_RUN |

**Important distinction:** Scientific *design approval* is not actual *scientific test PASS*. A real independent reference implementation can often be authored and pre-tested separately, even before Ariadne coding. T2 code-dependent calibration and T3 confirmation cannot be declared performed before there is executable candidate code. Any post-code estimation of K/R requires a **predeclared T2→preregistration→T3 protocol**, preserved test/seed independence, and reviewer approval; it cannot silently change frozen target/algorithm, reject nulls as PASS, or introduce post-hoc acceptance targets.

## 3. Source-level gaps in the 41-Method science registry

Directly inspected `independent_science_acceptance_registry_draft1.json` 41 records (41 unique Method IDs: G01=1, G02=6, G03=13, G04=8, G06=3, G07=3, G08=5, G09=2). As of the reviewed source:

- 41/41 have `independent_oracle_spec.oracle_algorithm_status=DESIGN_PROPOSAL_NOT_IMPLEMENTED`.
- **41/41** each have `independent_reference_path`, `reference_sha256`, `fixture_sha256`, `scientific_truth_expression` missing/null.
- **41/41** each have `quantitative_thresholds.{family_id,comparison_count_K,replications_R,mc_precision_target,bias_tolerance,coverage_tolerance,seed_schedule}` null.
- **41/41** each have `acceptance_plan.{repetitions_R,comparisons_K,mcse_max_epsilon,bias_tolerance,coverage_target,coverage_tolerance,seed_manifest_sha256,reference_impl_sha256,backend_lock_sha256}` null.
- 41/41 have `prereg_status=PENDING`, `test_observation=NOT_RUN`, `inference_mechanism_verified=false`.

The registry is an **author candidate design catalog**. It would be misleading to call these Method scientific numerical PASS. Conversely requiring all 41 post-implementation T3 reports **before the first Coding Authorization** would be a logical cycle.

## 4. PREP-05 / S09 audit exit (before S10)

An actual independent reviewer (not Author, not Reference constructor) must pin exact full Source SHA, inventory the live 402-source universe globally for impact analysis, and independently evaluate the **G01 common+owned+upstream dependency scope** first. The relevant 71 Gate/7 Operator/41 Method/200 Profile universe remains enumerated, but out-of-scope later Gate **semantic review** remains NOT_REVIEWED. G01 review must cover Owner S02 B×8 boundaries to the extent affecting common/G01, exact Method P1-M06, G01-specific strict Schema, Backend, Graph Oracle, Publisher/Reader, Privacy and protected v2 boundary. Every later Gate repeats scoped S09 on a pinned SHA and required transitive closure. Must distinguish `DOCUMENTARY_PASS` from `SCIENCE_CONTRACT_BLOCKED` and `RUNTIME_NOT_RUN`. Findings require original author correction, a **new** full target SHA and re-review. Static SHA, glossary, regex and author mathematical scratchpad are not independent QA acceptance.

A pre-code S09 PASS can legitimately state that a **specified future runtime gate test is unexecuted**, provided that absence does not hide any undecided mandatory pre-code scientific contract. It cannot claim all B05 method scientific numerics accepted, that HC1/chi-square is approved, or that an unavailable optional Backend was successfully installed.

## 5. Gate-scoped Freeze — **Owner DEC-PREPCODE-01=B adopted on 2026-11-22**

The original handoff says S10 Owner **integrated Contract Freeze** followed by S11 **Gate-scoped** Coding Authorization. `G01/06_G01_P00` expressly says candidate T2/T3 and actual ext4/XFS tests are **not Coding Entry preconditions** but are mandatory for 07/999, while `combined_review/147` says all 41 independent reference/parameter fields must be populated before Contract Freeze. `combined_review/166` flags the same S10 ambiguity. Owner expressly resolved this interpretation as B in `173_20261122_dec_precode01_owner_gate_scoped_s09_s10_s11.md`; the A/B comparison below is kept for auditable history, but **B is now normative**.

- **Path A (historical, not adopted):** Keep **one global S10 Freeze** across G01–G10. All relevant pre-code Method-level scientific contracts and backend feasibility for 41 Methods must be accepted first, even when the first Coding Agent will only implement G01. Future runtime Gate999 remains after S11. Benefit: single integrated contract/version. Cost: all unrelated advanced Method contracts can delay even G01 start; the 41 reference and B04 backlog is currently large.
- **Path B (Owner-adopted current policy):** **Gate-scoped S09 independent document audit → Gate-scoped S10 Contract Freeze → Gate-scoped S11 Authorization**, with the **common E11 v1 wire/Port/Privacy/JCS/Gate DAG/legacy-compatibility invariants** independently reviewed and frozen before G01. The 402-path inventory remains the **global change-impact discovery scope**, but S09 **semantic sign-off** may be scoped to common baseline + the Gate's 06/Pxx/07/Method+Schema and actual upstream dependency closure; untouched future-Gate methods are not asserted to be reviewed, frozen, scientifically PASS or executable. Subsequent Gates require their own independent S09 review (plus any changed common/previously frozen dependencies) and explicit separate S10/S11. A Gate may start when **its own** precise pre-code Profile/Backend/science-target/negative/independent QA requirements and every **actually required upstream frozen/999 dependency** are satisfied, without claiming later-Gate B05 numerical PASS. G01 first owns only P1-M06 FCI, ENV-BASE, Graph/PAG scientific contract, foundational Publication/Reader and G01 06/Pxx/07. Any downstream Gate remains blocked by genuine dependencies and cannot reuse missing evidence. All 41 eventually require valid independent science evidence by G10; G10 must review the cross-Gate integrated closure. No Science/Privacy/Legacy acceptance is removed. **This option explicitly changes S09 and S10 scope together**, not just the name of the Freeze.
- **Safety invariant under either path:** separate immutable source/lock/test/fixture SHA; no false PASS; B05 G08 mandatory full-real AR set and algorithm authority must be resolved **before G08** Coding Authorization; no silent scientific/default changes; Owner explicitly approves each Scope Freeze and Coding Authorization; all mandated candidate T2/T3 and Gate999 must pass before the relevant Gate is accepted.

**Owner decision status:** `DEC-PREPCODE-01=B / ADOPTED`. Gate-scoped S09 and S10 apply, with globally inventoried shared invariants and per-Gate independent scope acceptance. This only changes sequencing; G01 S09, S10 and S11 are **NOT_RUN / NOT_FROZEN / NOT_AUTHORIZED**.

## 6. Executable next evidence sequence

1. **Owner B was adopted.** Use `173` as adopted scope authority; reconcile old global S09/S10 wording in active instructions and operator preflight. Do not ask the Owner to decide A/B again.
2. Pin final candidate Source SHA after any author correction, then launch a genuinely independent S09 Reviewer per `165`. **Under adopted Path B:** S09 independently reviews the shared normative baseline plus the current Gate, Method, Operator/Schema and real upstream closure, with all 402 inventoried for change-impact and future Gate scope. Every uncovered component stays NOT_REVIEWED; each Gate re-pins/extends S09 when its prerequisites mature. If reviewer reports failures, correct, re-pin and re-review.
3. Build minimum actual read-only **pre-code** evidence set for the **G01** Freeze scope first: B02 relevant Draft202012 validator, B04 target Python3.12 package-level feasibility, Method-specific independent oracle/negative/threshold and admissible inference design, B03 synthetic structural cross-contract checks; no fabricated implemented E11 Reader.
4. Owner **G01 S10** contract review/approval with explicit exclusions and list of post-S11 tests. No Code Authorization follows implicitly.
5. Owner **G01 S11**, then subsequent Gate-specific S11, authorize only eligible Gate/Pxx on immutable frozen 06/07 and verified *actual* upstream Gate999; execute Coding Agent → Trial → independent test → Gate999 and collect real T2/T3 as required.

This record adds no application code/tests, runtime lock or Product canonical docs.
