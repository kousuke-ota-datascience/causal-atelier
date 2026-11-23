# ENH-E11 G01 AMD-E11-G01-P01-001 Gate Contract Amendment

**Document class:** Derived Contract / formal 09 amendment candidate  
**Self-containment:** MUST — defect, replacement semantics, rebaseline and approval requirements specified here  
**Date:** 2026-11-23 JST  
**Amendment ID:** `AMD-E11-G01-P01-001`  
**Gate / Trial:** `G01 / Trial01`  
**Status:** `PROPOSED / AUTHOR_IMPACT_REVIEW_RECORDED / OWNER_APPROVAL_PENDING`  
**Owner evidence:** Owner adopted **A案** (preserve Package boundaries, fill contract omission) and directed documents to be revised. **This is not the revised-contract/S10/S11 approval.**  
**Initial frozen full commit:** `a05fd072cbb82a7c6e43f45e7208e078f0784a2b` (Owner record 179)  
**Amended normative content full commit:** `827ce97b6cc649fb694b210fdebf8a32f5d9ee96` (complete amended 06/Pxx/07 + stock design at this checkpoint; future administrative review commits do not retroactively change this content)  
**Frozen and current uv.lock Git blob:** `2b83110e86b26b7969fbddf8f98a727370ae19f7` (verified for amended source; distinct from bytes SHA-256)  
**Repository/branch:** `kousuke-ota-datascience/causal-atelier / feature/ariadne_mvp_e11`

- Affected Gate 06: `06_Ariadne_ENH-E11_G01_implementation_instruction.md` remains Gate-wide WHAT unchanged except previously authorized branch routing.
- Affected Work Packages: `06_G01_P01_local_contract_codec.md` (primary), `06_G01_P02_atomic_publication_reader.md`, `06_G01_P05_cli_use_case_privacy.md` (integration clarification). P03/P04 implementation WHAT unchanged.
- Affected 07: `07_Ariadne_ENH-E11_G01_test_instruction.md` (adds cases under existing Test IDs without reducing AC).
- Affected stock: `30_62_local_execution_publication.md` §4, `23_42_local_result_manifest_artifact.md` §2.
- Traceability: `00_enhance_background/80_contract_amendment_log.md`; supporting records `combined_review/183_...`, `184_...`.

## 1. Contract defect

G01/P01 Trial01 started at `6ec2f59fa71b85aeff46daf0e6740b04281e8436`. Coding Agent correctly returned `BLOCKED_CONTRACT_AMBIGUITY` **before implementation**: P01 §6.5 requires `LocalRunManifest.from_run_evidence(evidence:ValidatedRunEvidence)` and Artifact upstream-ref joins, but its assigned P01 standalone WHAT omitted the input type/required fields/join keys/rejection rules. It could not choose legal factory behavior without inventing a contract. No Package checkpoint, code, tests or formal Gate result. After documents were revised at `48cb24c...`, Coding Agent returned `BLOCKED_CODING_AUTHORIZATION` at that start SHA: old 179/180 approved only the earlier frozen WHAT. Both BLOCKED reports are preserved as historical operator evidence, not Gate formal FAIL.

A targeted Author follow-up found two related specification issues: output Graph `ContentRef.relative_key` should be TrustedRoot-relative `runs/{run_id}/graph.json` whereas the `ArtifactDescriptor.key` is bundle-relative `graph.json`; and `from_payload(manifest)` cannot verify Study/Status bytes it does not receive. Both have been explicitly separated/clarified in the amended normative content SHA stated above. This is **Author reasoning, not independently executed FS or S09 verification**.

## 2. Why 08 remediation is insufficient

No `G01_999=FAIL` has been issued. Coding never began; the defect belongs to frozen **primary** 06/P01 WHAT, not a defective implementation. An 08 FAIL-remediation contract would misclassify the state, invent a Trial escalation, and fail to correct the normative factory contract. Use formal 09 contract change, then new distinct Owner S10/S11 approvals and normal P01 Trial01 restart.

## 3. Before / after semantic change

| Concern | Before | After (author candidate) | Reason |
| --- | --- | --- | --- |
| Evidence factory input | `ValidatedRunEvidence` referenced without fields | Immutable typed `study/study_payload/status_payload/runtime/stochastic/artifact_descriptors/output_graph_ref/graph_negative_reason_codes/review_science_evidence_ref` | Eliminate assigned P01 implementation ambiguity |
| Artifact Descriptor | Exact-byte fields defined, upstream join not made executable | Exactly six wire keys; no added `upstream_ref`; joins are semantic value comparisons against Study/Status/lineage and Graph output | Preserve existing `e11-local-manifest/1` public wire version |
| Input lineage | Source ref equality implicit | All-five-field `question/design/dataset` equality with Study inputs; G01 input graph/identification null | Fail closed for false provenance |
| Output Graph lineage | Generated versus input Graph implicit | Generated output Graph ref is `manifest.lineage.graph`; TrustedRoot-relative `runs/{run_id}/graph.json`, joined to bundle-relative `graph.json` descriptor SHA/media; semantic hash distinct from exact byte SHA | Resolve actual root-relative path and hash domain |
| Status/candidate completion | `COMPLETED` versus Reader timing potentially unclear | Candidate Status/Manifest may encode `COMPLETED`, but published successful outcome only after actual independent Reader; Status manifest path exact | Avoid false publication success |
| Factory power | Unspecified whether `from_payload` proves external joins | `from_run_evidence` validates typed Study/Status values; `from_payload` validates only Manifest-local invariants; P02/P05/Reader physically verify cross-file data | Prevent input-free factory making impossible proof |
| Graph-negative | Reason/diagnostics rules qualitative | Exact negative artifact set, nonempty reason matching Status, no fake Effect/Science PASS | Deterministic acceptance and rejection |
| Scientific/runtime/Privacy | Existing requirements | Unchanged. No Backend/FS/Science self-proof, no row export, no B05 waiver | No weakening or scope expansion |

## 4. Acceptance Criteria impact

| AC / DD | Before | After | Rationale |
| --- | --- | --- | --- |
| MAN01–03 / G01-07-04 | JCS/Manifest canonical and self-hash domain | Same AC; concrete pure factory projection and inventory checks | Operationalize existing requirements |
| MAN04–06 / G01-07-06,07 | Typed positive/negative bundles and Reader joins | Same AC; more exact invalid Ref/key/status/Method/Graph-negative cases | Increase test determinacy, do not relax |
| REF01–04 / G01-07-01/02 | lexical vs physical security split | Unchanged: P01 pure lexical; P02 real FS/FD/root | No fake physical validation |
| G01-07-05,08–12 / 999 | atomic publication, backend/PAG science, privacy, Product v2 regression | Unchanged; independent evidence remains obligatory | No accepted shortcut |

## 5. Protected passed-Gate impact

No prior G01 Gate PASS or published fixed Trial Candidate exists in these reported runs. No G02–G10 Coding Authorization is granted; no previously PASS Gate is asserted invalidated. Existing Product v2 CLI/Web/API/DB/Worker, scientific contracts, executable code and dependency lock must remain unchanged. Later Gates' possible interaction with the common manifest format is controlled by this existing unchanged public schema; they still require their independent Gate review.

## 6. Execution plan invalidation

- P00 invalidated: **NO** — dependency DAG remains `P01 → (P02,P03) → P04 → P05`.
- Package instructions invalidated by original defect: **P01**; **P02/P05** interface wording reconciled; **P03/P04** unchanged.
- Existing fixed Candidate invalidated: **N/A** — no P01 checkpoint and no fixed Trial Candidate.
- Prior Owner 179/180 as approval for amended WHAT: **INVALID**. Preserve records as historical, do not rewrite.
- Normal Trial01 execution is **BLOCKED** pending revised Freeze/Authorization, even if the agent sees amended docs at new HEAD.

## 7. Required rebaseline

- Revised primary 06/P01, P02/P05 handoffs, stock 30_62/23_42 and G01 07 are at immutable amended normative content SHA `827ce97b6cc649fb694b210fdebf8a32f5d9ee96`.
- Prior S10 `a05fd072...` is historical. A **new Owner S10 record** must pin the exact **full commit** selected at approval, including this 09 administrative amendment if present, and list changed normative blob SHAs plus any post-freeze administrative records. The 402-path global index draft14 and G01 scoped draft8 describe **historical frozen sources**; their old blob identities cannot be represented as current 402/402 parity. New freeze must explicitly account for this delta and not claim unperformed independent S09.
- `uv.lock` Git blob SHA stays `2b83110e86b26b7969fbddf8f98a727370ae19f7`; runtime must independently recheck current checkout and byte SHA. No `src/`, `tests/`, `pyproject.toml` edits in this amendment.
- Preserve G01-only `DEC-G01-EXEC-01`: independent S09/B02/B04/B05 and T2/T3/real FS/07/999 remain obligatory **before G01_999**, not blocking solely on external unavailability at Coding Entry. No test result is claimed by source/author review.

## 8. Trial handling

**Keep `G01/P01/Trial01`** after new authorization if actual Trial state has no formal Gate FAIL or remediation 08. The first two stops are pre-implementation BLOCKED and not `PACKAGE_READY`. Do not manufacture checkpoint or silently use `08` FAIL rework prompt. Re-run normal Work Package Coding Agent only once revised S10 and distinct revised S11 are recorded and current authorized branch/worktree/lock/contract identity are verified.

## 9. Re-approval evidence

- A案 policy and documentation-change command: **Owner adopted** in this conversation.
- This full formal 09 amendment **specific revised contract**: **OWNER APPROVAL PENDING**.
- New provisional G01-S10 **re-Freeze**: **OWNER APPROVAL PENDING**.
- New limited G01-S11 Coding Authorization: **separate Owner decision required after S10**, **NOT AUTHORIZED** for amended WHAT.
- Independent scoped S09 and all B02/B04/B05 / formal 07/999: **NOT_RUN / EXTERNAL_PENDING**, unchanged.

An Author impact audit and Owner approval do **not** constitute independent S09, Science PASS, runtime provenance, published marker validation, or package completion.

## 10. Amendment ledger / Git traceability

`00_enhance_background/80_contract_amendment_log.md` has the same Amendment ID, observed starting SHAs and status. Revised normative source content SHA is pinned above; this 09 document is subsequently added as a review/control artifact. Do not fabricate self-referential application commit SHA. Owner's new approval record must cite the actually selected full 40-hex commit when issued. Old `179/180` and reported blocked Trial01 records remain immutable.

## 11. Guardrail

No AC weakening, science oracle substitution, invented manifest publication evidence, lock drift, Product v2 ABI change or G02–G10 scope expansion is permitted. A new material discrepancy found in a real Coding/Reader/Science test triggers impact evaluation, not silent patching under previous Owner authorization.
