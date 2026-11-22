# ENH-E11 S09 — Third-pass Author Contract Remediation (G08 AR authority / G01 Local Graph)

**Date:** 2026-11-22 JST  
**Type:** `AUTHOR_TARGETED_SEMANTIC_QA_AND_CORRECTION`; **not** independent S09 acceptance, not B02–B05 runtime-science evidence, not PREP-06 Freeze, not Coding Authorization.  
**Source:** `kousuke-ota-datascience/causal-atelier` / `prototype/ariadne_mvp`. Owner decisions `DEC-S02-06` and `DEC-S05-AR01=A` already adopted; **no new Owner decision** was made in this author correction.

## 1. Scope of work and scope limitation

- Re-read 71 active G01–G10 Gate 06/P00/Pxx/07 bodies **for selected high-risk scientific/Privacy/Graph/G10 cross-contract terms**, and seven Operator entry prompts for selected authority/independence/test-discovery terms. This was a bounded Author inspection; it **did not** independently adjudicate every line/signature/acceptance condition in the 71 files.
- Previously `draft7` enumerated all active source blobs: 71 Gate + seven Operator + 200 original Method Schema + five factored + 13 local/scientific Schema + 98 active Stock Markdown + eight supplementary cross-contract references (the prior 34 selected stock items are a subset of 98). The blob inventory establishes file identity, **not** full semantic proof.
- During this third pass, directly conflicting primary authoring/DoD clauses were identified in five Gate documents. Revised normative main text, not just explanatory appendices. Other targeted scans did not establish a new independently validated contract PASS.

## 2. S09-R13 — G08 AR provisional algorithm must not be implicit normative default

**Owner authority:** `DEC-S05-AR01=A` preserves the mandatory, **full-real-domain weak-IV-robust Anderson–Rubin confidence-set target** for approved B0/B1 estimands. `Y-βA ~ Q+Z` with HC1/χ²(1) inversion is an **independent-math-review candidate**, not an adopted numerical algorithm. No finite-grid substitution or Owner-unapproved asymptotic/numeric choice.

**Observed active contradiction:** In four G08 Pxx normative bodies, a primary design sentence said `HC1 Anderson–Rubinは各候補βの...` as an unqualified implementation rule, and other primary phrases said `HC1 AR集合をfinite gridだけで判定しない` / required reference comparison of `HC1 confidence inversion`. Later text indicated a candidate status, but did not fully eliminate these earlier ambiguous imperative clauses.

**Affected authoritative files (4):**

1. `10_enhance_instruction/G08/06_G08_P01_rdd_sharp_fuzzy.md`
2. `10_enhance_instruction/G08/06_G08_P02_wald_late.md`
3. `10_enhance_instruction/G08/06_G08_P03_two_sls_ar.md`
4. `10_enhance_instruction/G08/06_G08_P04_rdd_iv_result.md`

**Remediation:** In each file, changed the three normative clauses, 12 occurrence-level fixes total. New main-body rule explicitly distinguishes (a) the required full-real robust AR set + topology from (b) unapproved HC1/χ²(1) candidate, which is **never a valid implicit implementation default**. Until reviewed and frozen, fail closed with `BLOCKED_SCIENCE_METHOD_NOT_FROZEN`; candidate-only test algebra/reference must not become a mandatory positive method outcome. Preserve all-real tail, disconnected/unbounded/degenerate distinctions, predeclared independent math review, no fake scientific PASS and no altered B0/B1 target.

**Bounded post-edit check:** All seven G08 current Gate bodies were read after repair. The exact pre-repair unqualified `HC1 Anderson–Rubinは各候補β` primary sentence now has zero matches in the seven; each of the four changed Pxx states the provisional status in the primary scientific boundary. This is **not** a proof that no other hidden contradictory clauses remain; independent reviewer must assess primary matrices, 06/07, stock 23/30, Method Registry and actual mathematical suitability.

**Required independent negatives:** A Coding Agent must not accept HC1 as already frozen; `BLOCKED_SCIENCE_METHOD_NOT_FROZEN` must gate the actual unapproved inference method. After separate algorithmic approval, independent reference must test full-real topology, weak/near-zero instrument, variance degeneracy/rank and calibrated size/coverage under applicable designs. Neither author preflight nor this correction closes B05.

## 3. S09-R14 — G01 Local GraphVersion completion criterion

**Owner authority:** `DEC-S02-06` requires current E11 Local-only `e11-local-graph/1` to retain `version_id=null`, `parent_version_id=null`; scientific parents use immutable provenance/ContentRef/hash. The existing Product GraphVersion compatibility bridge is separate and must preserve the existing Product v2 ABI.

**Observed active ambiguity:** `10_enhance_instruction/G01/06_G01_P03_pag_graph_version.md` §10 (previous line 138) said `Standalone version_id=null,parent_version_id=null and optional real Product parent lineage retained`, potentially admitting Product IDs in a non-standalone E11 Local Graph despite §3/strict Schema requiring both `const null` for **all** current E11 Local Graph instances.

**Remediation:** DoD now explicitly requires both `null` in **all E11 Local Graph wire instances**, rejects non-null imports, retains scientific parent lineage only by immutable provenance/ContentRef/hash and confines optional Product parent/version linkage to the **separate existing Product bridge**. The independent Reviewer must check GraphEvidence internal field/table versus wire strictness, current schema `e11_local_graph_v1.schema.json`, G01/G06/G10 06/07 and protected Product ABI. This repairs text ambiguity but is **not** a real Graph/Reader/product regression run.

## 4. Residual tasks and non-claims

- **S09 independent:** `NOT_RUN`. The author is not permitted to sign off its own changes. Reviewer must pin a new final commit SHA and re-enumerate all 71+7 and active Stock, 200/5 Method profile pairs/overlays, 13 drafts and FCI/dispatch/output catalog. See `165_20261122_s09_independent_document_audit_instruction.md`. The author-scanned 71+7 alone cannot yield an independent verdict.
- **S05-B02:** 200 standard `jsonschema.Draft202012Validator` source-vs-reconstructed and positive/negative tests on Owner-approved isolated Python 3.12 not performed here. A separate local Python 3.13 environment is available but **not** the approved 3.12/lock target or a 200-proof.
- **S05-B03:** true cross-artifact Result/Status/Manifest/Marker/Reader strict hash/scientific referential/typed non-scalar readback `NOT_RUN`.
- **S05-B04:** isolated DoWhy/EconML/Tigramite fitted API and confidence interval tests `NOT_RUN`.
- **S05-B05:** 41 independently accepted reference oracles, G08 exact AR algorithm/coverage/degeneracy review, residual G06 temporal conventions/G07 ITS inference/G09 SDID variance, preregistered pilot metrics remain `BLOCKED`. Candidate-dependent Gate999 T3 legitimately belongs **after** coding and does not create a pre-code circular dependency.
- **S10:** `NOT_FROZEN`. **S11:** `CODING_NOT_AUTHORIZED`. The normative documents were updated; no protected app Source, Tests, pyproject, uv.lock or Product canonical requirements were modified by this correction.

## 5. Next execution boundary

1. Regenerate source index from the **new** Git Tree after five normative amendments; update reviewer 165 to the new draft and record the immutable target source SHA. The new index is for evidence discovery only.
2. Independent S09 document reviewer evaluates full pinned content. Any finding requires Author normative patch, re-pin and independent re-review. Do not label author scan as independent review.
3. S05-B02–B05 continue in an actually available Owner-approved isolated environment and with a genuinely separate Reviewer. Evidence must include real source/lock/fixture/reviewer identity. Escalate to Owner only if actual scientific alternatives change adopted estimands/inference guarantees or separate S10/S11 approval becomes appropriate.
