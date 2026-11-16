> **Historical audit (pre-RD-02 numbering).** New numbering and migration verification: [92_rd02_restructure_verification.md](92_rd02_restructure_verification.md). This historical file deliberately preserves the former filenames.

# ENH-E11 — Requirements/Design Split Verification

- Verification date: 2026-11-16 (JST)
- Source branch: `prototype/ariadne_mvp`
- Source snapshot commit: `3ba5fe2465ec591f0da7f998c21a5241984b73dc`
- Verification state: `STRUCTURAL_SPLIT_VERIFIED / FORMAL_E11_PUBLICATION_PENDING`
- Scope: lossless source copies, structural section/FR preservation, and E11 draft labeling; **not** scientific correctness, independent ADR review, formal requirement acceptance, or permission for Coding.

## 1. Exact source copies (Git blob identity)

All seven files under `_source_snapshots/` were compared to the same named file at `docs/wiki/requirement_definition/` on the working branch. Git blob SHA matches for each file.

| File | Git blob SHA |
|---|---|
| `00_product_concept_memo.md` | `da8d10b1f1631893529a92c8a45373e55aa9f005` |
| `10_requirements_definition.md` | `40b83f29c67b4a39f6db5393be7534c5e892d656` |
| `21_logical_data_design.md` | `72903b9ad48b5b7edabaa7bb1c2cace42aa46ce7` |
| `22_product_basic_design.md` | `87196f2f03a7f3367724bc05fb254d1a4d98109e` |
| `23_api_interface_design.md` | `131467f02222f105a49e6dfdbcec0f49cadb0f41` |
| `30_detailed_design.md` | `04d83541e55ab0364500afb4b92ef55c10785a0c` |
| `README.md` | `8fb2aacba111eb302ac71e19075e80a67dd9d989` |

These exact copies are not the split working drafts.

## 2. Structural split reconstruction

To verify content preservation, the source file's section body (beginning at its first `##`) was compared with split documents concatenated in numerical order, stripping only split document wrappers, repeated table headings and synthetic continuation labels and normalizing whitespace.

| Original | Baseline split files | Normalized characters | Result |
|---|---:|---:|---|
| `10_requirements_definition.md` | 14 | 58,214 | MATCH, after resolving historical relative hyperlinks to pinned source GitHub URLs |
| `21_logical_data_design.md` | 9 | 55,857 | MATCH |
| `22_product_basic_design.md` | 8 | 50,110 | MATCH |
| `23_api_interface_design.md` | 9 | 52,981 | MATCH |
| `30_detailed_design.md` | 10 | 57,394 | MATCH |

**Functional requirement integrity:** The source contains 195 `FR-*` Markdown table entries including suffix IDs. The seven split FR tables now contain 195 entries, in the same exact order and with identical line content as the source. An initial copied FR-001 row at six split boundaries was found and corrected in commit `291220163ba99ec61d2eea2abfada7bfb629ea8a`. No source FR row was deleted, duplicated or rewritten.

The rest of source frontmatter is preserved in `_source_snapshots/`; split files have new working-copy metadata and the overall documents have new responsibilities/entrypoints.

## 3. Additional working documents

- 4 new ENH-E11 semantic/interface/design drafts: RD `10_14`, LDD `21_09`, BD `22_08`, API `23_09`.
- 3 new class-level DD documents: `30_10` source-verified representative classes; `30_11` proposed E11 classes; `30_12` class-level documentation template and coverage gap register.
- Total: 50 baseline split docs + 7 new draft/verification design docs = 57 files across five type folders.

## 4. Approval and remaining work

| Area | Verified state |
|---|---|
| GitHub source copy and structural split | VERIFIED |
| DEC-SR04-09 scope/semantic/architecture-policy approval | Previously owner-approved (refer to DEC09) |
| New FR/NFR/AR numbering, clauses, statuses, trace and controlled publication | DRAFT / PENDING |
| Complete source-audited per-class physical design | PARTIAL (see `30_12`) |
| E11 class/module signatures, ports, versioned schemas, independent ADR review | PROPOSED / NOT FROZEN |
| Gate06/07 pre-registration and acceptance | NOT FROZEN / NOT RUN |
| Science, effective optional-runtime, legal delivery, Coding Authorization | NOT COMPLETED / NOT AUTHORIZED |

There were **no Python, configuration, migration, `pyproject.toml`, `uv.lock`, or original canonical requirement file changes** made in this documentation activity. Source correctness, numerical scientific performance, external engine capability and test evidence were not measured by a textual document split.

## 5. Next review

The next controlled publication review should reconcile the candidate `E11-F/N/A-*` clauses against **each of the approved 68 Scope rows**, Method registry, 10 UCs, current FR/NFR/AR, issue, acceptance and Gate trace before owner assignment of permanent IDs and approval SHA. The physical DD class inventory then requires full source review and independent architecture signoff rather than using proposed names as implemented facts.
