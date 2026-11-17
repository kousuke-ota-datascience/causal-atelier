# ENH-E11 G01 / 06 実装指示書（PREP-03初稿・Coding未許可）

**Status:** `PREP03_G01_06_DRAFT / NOT_EXECUTABLE_INSTRUCTION_UNTIL_GATE_APPROVED`
**対象:** G01 — Local Question/Design/Graph ContextとP1-M06 FCI/PAG fidelity／version lineage（UC-01）。Gate 06 = このG01の**実装指示契約**。G06 Temporalの実装Groupとは別。

## 1. Authority / scope

- [PREP-02 Common Design Freeze](../../00_enhance_background/Revised_requirements_definition_documents/combined_review/117_20261117_prep02_common_contract_baseline_freeze.md)
- [Owner承認したG01〜G10 Planと科学的前提](../../working_notes/20261116_sr04_dec09_scope_requirements_architecture_gate_integrated_owner_approval.md)
- [G01 Graph/Method適格性](../../00_enhance_background/Revised_requirements_definition_documents/10_requirements_definition/10_32_scientific_method_scope.md)の`P1-M06`、[DD 30_61](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_61_e11_local_domain_ports.md)、[DD 30_63](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_63_e11_method_adapters.md)
- [CLI 23_41](../../00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design/23_41_e11_local_cli_scientific_ports.md)、[Result/Manifest 23_42](../../00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design/23_42_e11_local_result_manifest_artifact.md)、[7 Schema drafts](../../00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design/schema_drafts/README.md)
- Existing Product/CLI Source remains authority for unchanged legacy behavior, especially`causal-analysis-spec/2`. **No Product Web/API/DB/Worker, existing canonical requirements or unrelated Method implementation**.

## 2. Deliverables (separable work packages; within G01, not new Gate)

| WP | Implementation contract | Required dependencies/notes |
|---|---|---|
| **G01-WP01** Local Value / strict input | `ContentRef`, `ValidatedStudy`/ConfigDecoder, `GraphEvidence`/GraphVersion DTO with tagged endpoint and optional lag; strict Version/Method dispatch and no Product auto-conversion | Start with pure schema/value tests; reject duplicate YAML/JSON keys, raw path traversal, unsafe content references |
| **G01-WP02** Safe Local File / Manifest baseline | TrustedLocalRoot, ContentReferencePort, LocalPublicationPort/Reader, JCS codec, Marker→Manifest→Artifact verification; run_id collision and all error/exit phases | No-clobber `renameat2(RENAME_NOREPLACE)` Linux, same-FS/dirfd, fsync/crash semantics from baseline; safe readback; never claim commit before verified |
| **G01-WP03** Question/Design/Graph lineage | Question/Design input refs, immutable GraphVersion parent hash, Graph semantic projection SHA256 + external file raw bytes hash, graph edge endpoint/provenance semantics | CPDAG/PAG uncertainty preserved; no false DAG certainty; version edit creates new immutable identity |
| **G01-WP04** FCI Method P1-M06 Adapter | Eligible CI test/Data/Graph type preflight, FCI algorithm/backend selection and effective API checks, `PAG` result/metadata and typed scientific negative | P1-M06 only. No arbitrary unknown backend fallback; P1-M05 IV is G02, P3-M01..03 Temporal G06 |
| **G01-WP05** CLI integration / legacy compatibility | `DISCOVER` operation and Result/Status/Manifest published consistently; **no dummy Effect Result**; stdout/stderr sanitize; Product legacy CLI regressions | Policy-restricted row-level output excluded from G01; G05 owns independent authorization mechanism |

**Ordering:** WP01 (pure types/decoder) → WP02 (foundation file/marker) and WP03 (graph) → WP04 FCI → WP05 integration. Allow isolated unit design/test preparation before implementation authority; **do not execute or edit code on this draft alone**.

## 3. Fixed acceptance invariants

1. **Identity**: run id and source refs are bound throughout Study→Graph→Status→Manifest→Marker. `e11-local-*/1` discriminators and external raw bytes SHA preserved; Graph's internal semantic projection digest excludes its own `content_hash`.
2. **No false scientific interpretation**: FCI emits PAG uncertainty (circle, tail, arrowhead, bidirected when valid). Does not infer unique latent variable or identified effect from a two-variable DGP. `SCIENCE_PASS` requires independent Graph Oracle in 07, not FCI invocation.
3. **No false commit**: files staged under private root, atomic no-replace publish, parent fsync and verified readback; crash/collision never silently replaces committed run. CLI exit2 schema, exit3 privacy/input security, exit4 engine, exit5 publication/readback; scientific negative may complete with exit0 if complete evidence was published.
4. **Scope safety**: no row-level export in G01. If Study requests it, reject with exit3 (not hidden aggregate success). No credentials/private rows in stdout/log/Manifest. G01 can publish aggregate/graph artefacts only under the approved private root.
5. **No legacy regression**: `causal-analysis-spec/2` execution, current Product Graph and Manifest behavior unchanged; local Dispatch has explicit v1 selection only.

## 4. Gate-specific choices to finalize before G01 coding

- Backend FCI distribution/class, actual effective import API/profile and license obligations; CI test admissibility/metadata; missing dependency returns typed `CAPABILITY_UNAVAILABLE` without fallback.
- Precise G01 Graph/PAG semantic validation and Method P1-M06 strict config_schema (unknown keys rejected). The provided standalone schema drafts currently **do not** fully define Method config, provenance and Operation bundle; close these for G01 only.
- Finish JCS/Python cross-runtime conformance vectors and Graph/Manifest/Marker byte-level contracts in G01_07; adopt no new override of the common v1 wire.
- Decide if full target runtime supports Linux renameat2 no-replace on private mount; unsupported target is `NOT_SUPPORTED`, not a process-lock substitute.
- Prepare independent multivariable PAG Oracle with known equivalence class, CI-test assumptions, DGP-011 limitations; quantify adjacency/endpoint evaluation in G01_07.

## 5. Not authorized by this draft

No coding agent trial, package/uv.lock edits, filesystem publication deployment, claiming Science PASS, updating Source Implementation Status, canonical requirement promotion or closing unrelated Product gaps. Formal G01 entry/authorization is separate. G01_07 remains independent verification contract, not the coding-agent's self-attestation.
