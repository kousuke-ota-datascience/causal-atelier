# ENH-E11 PREP-02 — Independent Architecture Review Submission Pack (2026-11-17)

**Kind:** FLOW / REVIEW SUBMISSION PREPARATION — **NOT an Independent Review PASS**.
**Git baseline:** `66ce2037d3e983d63ff6db34acf5c60a51408d58` (`prototype/ariadne_mvp`). The Reviewer must record the exact reviewed commit and inspect live Source, not rely on this dossier alone.
**Owner decisions retained:** DEC01〜09、68 Scope / 41 Methods / 10 UC, DOC01 acceptance and IF/DD design-direction adoption. **Original canonical `docs/wiki/requirement_definition/` remains untouched until ALL E11 tests PASS.**
**Boundary:** CLI-only E11 Local; existing Product Web/API/DB/Worker, E9/E10 and `causal-analysis-spec/2` legacy are protected.
**Reviewed?:** NO. **Proposed ADR/schema freeze?:** NO. **Coding Authorized?:** NO.

## 1. Evidence Sources

| Evidence | Relevant scope | What it establishes |
| --- | --- | --- |
| [BD01 Findings](../bd01_review/90_architecture_consistency_review.md) | F01〜F13, 11 OPEN | Prior internal review, **not** independent sign-off |
| [DD01 Class audit](../dd01_review/92_class_contract_conformance.md) | 7-section physical design and partial remediation | Source-linked spec coverage, not runtime behavior |
| [CLI/Port IF](../23_api_interface_design/23_41_e11_local_cli_scientific_ports.md) | version/operation/Method/Status | PROPOSED, no Code |
| [Manifest/Publisher IF](../23_api_interface_design/23_42_e11_local_result_manifest_artifact.md) | AR set/Graph/Atomic/Privacy/readback | PROPOSED; FS fault tests not executed |
| [Domain Ports](../30_detailed_design/30_61_e11_local_domain_ports.md) | 7-section gaps and Existing Product Port crosswalk | Source-inspected, E11 Port unimplemented |
| [Local UseCase/Publisher DD](../30_detailed_design/30_62_e11_local_execution_publication.md) | 6 proposed classes, staged publication | Draft physical design; exact exceptions/schema pending |
| [Method41 allocation](../30_detailed_design/30_63_e11_method_adapters.md) | Method-to-backend target & limitations | No per-method Science PASS; adapter class specifications incomplete |
| [Environment/Delivery BD](../22_product_basic_design/22_13_deployment.md) | DEC08 profiles, lock and legal boundary | E11 extras missing from current pyproject/lock |
| [Flow migration manifest](../doc01_review/93_20261117_flow_migration_manifest.md) | 13 Flow relocations and original blobs | Structural migration, not full link/anchor PASS |
| [PREP execution evidence](93_20261117_prep01_prep02_execution_evidence.md) | Scope of checked Source and unresolved gaps | Audit trail only |

## 2. BD01 Finding disposition for PREP-02 (proposed, not Reviewer decision)

| Finding | Bucket | Present concrete contract/evidence | Blocking until / reviewer question |
| --- | --- | --- | --- |
| F03 Atomic artifact publication | **COMMON-ARCH BLOCKER** | IF23_42 §7/10, DD30_62 §4: trusted staging→Manifest/marker→no-clobber rename/readback | Select Linux no-replace implementation; demonstrate concurrent/FS fault, same-FS/crash/readback; Reviewer signoff |
| F04 Product/Local Port/DTO reuse | **COMMON-ARCH BLOCKER** | DD30_61 §10 Product ScientificCorePort/GraphVersion/ArtifactStore/Legacy CliManifest source mapping | Explicit newLocal Ports vs guarded bridge ADR, existing Product v2 regression scope and class 7 sections |
| F05 Local row export authorization | **COMMON-SECURITY BLOCKER** | BD22_12 §15; IF23_42 §8; DD30_62 §6 owner/UID/explicit flag | Define whether delegated/shared-volume export is supported; OS principal+mount negative tests; Security/Owner approval |
| F06 E11 vs legacy v2 Schema/dispatch | **COMMON-SCHEMA BLOCKER** | IF23_41 §2/3; DD30_61 §3; BD22_15 §18.1 | Fix actual JSON Schema, version discriminator, exact CLI signatures, unknown+old-version negative, no legacy conversion |
| F07 Typed effect/AR science state | **COMMON-SCHEMA BLOCKER** | IF23_42 §3/4; DD30_61 §6/7 | Exact Interval tagged-union/AR topology/CI-null semantics/roundtrip; independent numerical or property tests |
| F08 41 Method eligibility/CI | **REGISTRY COMMON + METHOD-GATE DETAIL** | DD30_63 41 Method IDs; SR04 A/F method registry and adopted D01〜08 | Registry discriminators common; each Method's estimand, scientific Oracle, backend effective API, AC/Monte Carlo frozen in its respective Gate07. P1-M05 target unresolved |
| F09 5 environment profiles | **ENV COMMON + METHOD-GATE RUNTIME** | BD22_13 §16.3; current `pyproject.toml` and `uv.lock` lack DoWhy/EconML/Tigramite/RD entries | Freeze extra names/version policy; fresh isolated+combined locked install/API probes during authorized dependency change; no claimed PASS now |
| F10 GPL / customer delivery | **DELIVERY-ONLY BLOCKER** | BD22_13 §16.2; DEC08 | Legal/SBOM per distributed artifact and recipient; not equated with internal Coding/Science PASS |
| F11 Product GAP-C01〜04 ownership | **SEPARATE PRODUCT BACKLOG** | DEC09-5, BD22_15 §18.1; newly discovered Project/Context membership/idempotency Source gap in IF23_10/BD22_12 | Product owner/workstream/acceptance dates; cannot auto-close via E11 Local. Not E11 Local Science acceptance |
| F12 Independent Architecture Review | **CROSS-CUTTING CODING BLOCKER** | This packet plus existing Stock design | Actual independent Reviewer assignment, fixed SHA, finding-by-finding written verdict and necessary correction |
| F13 Original canonical promotion | **RELEASE-PROMOTION BLOCKER** | Owner decision at `combined_review/decisions/93...` | Every ENH-E11 related test PASS before canonical copy; never treat PREP document review as substitution |

**Classification semantics:** "Method-Gate detail" means **deferred until the corresponding Gate's 06/07 Freeze**, not waived. "Delivery-only" is blocking for recipient-specific delivery, not for internal isolated research execution. "Separate Product" is not closed by E11. Common-architecture items must have a frozen, independently reviewed shared contract before initial Coding.

## 3. Proposed Owner/Architecture freeze choices (not adopted)

**DEC-PREP02-A — Local row-level export delegation:**

- **Option A (recommended):** Initial CLI supports non-delegated same-UID/owner-controlled local root only; default no row export, row output only with explicit CLI flag **and** preauthorized Study privacy policy and strict filesystem isolation. Shared/CI/container-root/delegated volumes are rejected unless a separately reviewed policy is added.
- **Option B:** Initial CLI supports delegated principals, shared mounts and CI exports subject to signed delegation, ACL/mount verification, dedicated audit, and additional negative cases. More attack surface and requires separate user/security roles.
- **Unchanged whichever option:** Product ProjectMembership is not invented for CLI; secret/row leakage forbidden; Customer Delivery Legal independent. Human Owner + Security judgment needed to Freeze an option.

**DEC-PREP02-B — No-replace publish primitive:**

- **Option A (recommended, Ubuntu/Linux baseline):** Require effective same-filesystem no-replace directory publication (e.g., Linux `renameat2(RENAME_NOREPLACE)` when available), all-or-none readback, explicit fail-closed on unsupported filesystems, including concurrent-process negative tests.
- **Option B:** Use an explicitly reviewed cross-process lock protocol plus atomic rename with no-clobber proof, durability/recovery and crash fault injection. Never accept only `exists()` then plain `rename()`; thread-only locks are insufficient for multiprocess agents.
- OS/Python ABI, EEXIST/ENOTSUP handling, directory fsync and fs-specific evidence are not frozen; Owner/Architecture decision required.

**DEC-PREP02-C — E11 Version namespace adoption:**

- **Option A (recommended):** Freeze `e11-local-study/1`, `e11-local-graph/1`, `e11-local-effect-result/1`, `e11-local-manifest/1`, `e11-local-status/1` **as existing IF design candidates**, with strict discriminator and documented JSON Schema/enum equality; fail closed for legacy/unknown.
- **Option B:** Adopt different version identifiers, requiring a full IF/DD/FR/negative fixture rebasing before Coding. No silent aliasing.
- Do not call schemas frozen until actual JSON Schema, Protocol signature and error contract artifacts are reviewed/approved.

## 4. Independent Reviewer verification request

1. Take HEAD snapshot SHA and exact file/Blob checksums, verify against Source and adopted Owner decisions. Record reviewer and independence from authoring team.
2. Inspect F03/F04/F05/F06/F07 common blocking contracts, including Current vs Proposed ports and Product/Local separation. Record both positive and negative observations; actual code not yet present.
3. Review 41 Method registry discriminators and classify what may defer to individual Gate07, especially P1-M05; verify Method IDs and estimand targets cannot silently collide.
4. Ensure F09 environment acceptance is separated from Source static pyproject/lock and legal. Record pre-Coding isolated probe evidence if any; do not claim missing libraries installed.
5. Evaluate F10/F11/F13 as explicit non-E11-coding boundaries while preserving their future obligations.
6. Return each finding as `ACCEPT_FOR_CODING` / `REQUIRES_CORRECTION` / `DEFER_WITH_DEPENDENCY` with finding-specific rationale, referenced SHA, Owner decision and test evidence. No overall PASS if common Blocker remains.

## 5. Review and gate state

`PREP02_REVIEW_PACKAGE_PREPARED / OWNER_FREEZE_CHOICES_PENDING / INDEPENDENT_REVIEW_NOT_RUN / SCHEMA_PORT_NOT_FROZEN / SCIENCE_AND_ENV_NOT_VERIFIED / CODING_NOT_AUTHORIZED`.

This package is a review input, **not** an independent review artifact or Owner approval. PREP-02 remains IN_PROGRESS.


## 6. Owner decisions adopted (2026-11-17; supersedes the pending status in §3/5)

**DEC-PREP02-A/B/C = Option A / Option A / Option A, ADOPTED by Owner.** Decision authority and residual obligations: [DEC-PREP02 record](decisions/94_20261117_dec_prep02_owner_architecture_choices.md). In §3, options are preserved as historical review alternatives, **not current pending choices**. Explicitly: non-delegated same-UID local row export, Linux same-FS atomic no-replace publish with fail-closed unsupported filesystem, and strict E11 version namespace are approved policy. F03/F05/F06 remain OPEN for actual schema, port, security, runtime proof and independent reviewer. The §5 token `OWNER_FREEZE_CHOICES_PENDING` was the state when originally authored, now superseded by `OWNER_CHOICES_ADOPTED / PORT_SCHEMA_NOT_FROZEN / INDEPENDENT_REVIEW_NOT_RUN / CODING_NOT_AUTHORIZED`. Reviewer must inspect decision record and exact latest commit SHA; this update itself is not a review PASS.



## 7. F04/F07 shared contract resolution input (2026-11-17)

- F04: [Product/Local Port + DTO ADR candidate](98_20261117_prep02_f04_port_boundary_adr_candidate.md)。Existing Product ScientificCorePort（5 methods）、ScientificResultDescriptor、ArtifactStorePort（4 methods）、CliManifest v2に対し、E11 Local Protocol/DTOの隔離、staging sink、explicit pure-computation reuse condition、negative casesを記載。
- F07: [AR/Inference serialization + scientific-state ADR candidate](99_20261117_prep02_f07_ar_inference_schema_candidate.md) と [machine-readable internal JSON Schema $defs draft](../23_api_interface_design/schema_drafts/e11_ar_inference_defs.schema.json)。Extended-real tagged endpoint、interval normalization、ALL_REAL/DISCONNECTED/UNBOUNDED/BOUNDED topology、typed non-availability reason、Science Acceptance独立を具体化。
- Reconciled Stock: `30_61` `11/12、`23_41` `9、`23_42` `12、`22_15` `18.3。Reviewer must validate identical meaning and still audit exact Protocol method/error signatures, schema composition into Result/Manifest, F03/F05/F06 runtime proof, Product v2 regression and Science Oracle.
- **Disposition:** DESIGN_SPEC_DRAFTED / SCHEMA_PORT_NOT_FROZEN / INDEPENDENT_REVIEW_NOT_RUN / CODING_NOT_AUTHORIZED. This is a reviewer *input*, not self-approval.
