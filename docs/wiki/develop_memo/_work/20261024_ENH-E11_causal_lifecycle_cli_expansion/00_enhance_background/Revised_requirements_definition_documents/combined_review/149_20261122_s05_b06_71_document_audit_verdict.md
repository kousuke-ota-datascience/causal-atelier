# S05-D/B06 — 71-Document Gate Contract Static Audit (2026-11-22)

**Verdict: FAIL (BLOCKED for Freeze).** Complete **source-file coverage** for the 20 G01–G10 Gate 06/07 instructions and the 51 active Gate P00/Pxx work packages. This is a keyword-and-signature static scan plus previously inspected architecture, **not** the independent semantic review required in S09.

Source: `10_enhance_instruction/G01...G10` on branch `prototype/ariadne_mvp`. The source-specific SHA for all 71 files, the exact line numbers and excerpts of 117 static **candidate** occurrences are in `148_20261122_s05_b06_71_document_static_findings.json`. A match is not necessarily a distinct semantic defect; same boilerplate is repeated and must be fixed coherently rather than mechanically counted as 117 unrelated bugs.

## Search distribution

| Pattern | Matching lines | Distinct source files | Required Owner S02 consistency |
| --- | ---: | ---: | --- |
| REMOVED_CLI_FLAG | 11 | 9 | No removed CLI flag, Study policy_ref, signing anchor or Study+CLI opt-in as normative current E11 local CLI requirement |
| REMOVED_RUN_CONTEXT | 29 | 18 | No removed CLI flag, Study policy_ref, signing anchor or Study+CLI opt-in as normative current E11 local CLI requirement |
| REMOVED_STUDY_POLICY_FIELD | 14 | 9 | No removed CLI flag, Study policy_ref, signing anchor or Study+CLI opt-in as normative current E11 local CLI requirement |
| REMOVED_SIGNED_ANCHOR | 13 | 7 | No removed CLI flag, Study policy_ref, signing anchor or Study+CLI opt-in as normative current E11 local CLI requirement |
| DOUBLE_OPTIN | 61 | 19 | No removed CLI flag, Study policy_ref, signing anchor or Study+CLI opt-in as normative current E11 local CLI requirement |
| UNCONDITIONAL_REPLAY | 14 | 8 | All 41 valid independently accepted evidence; rerun only changed/invalid dependency closure, plus cross-Gate tests |

## Known **concrete** contradictions (not just keyword matches)

- **G01:** 06 still advertises `--allow-row-level-export`, `policy_ref:null`, `cli_row_flag`; P05 similarly retains removed CLI flag and policy API. G01 aggregate-only requirement is retained but expressed only through `Study.privacy.row_export_requested=false` and Method P1-M06 eligibility.
- **G05:** 06 and 07 plus P00/P01/P02/P03/P04 still require double opt-in despite S02-01 Study-only adoption, and some refer to the removed Study `policy_ref`. Private Linux nonroot same-EUID ext4/XFS + Method row schema + no row iteration before allow remain mandatory.
- **G02/G03/G04/G06/G07/G08/G09:** one or more Pxx common Application Context snippets still name `cli_row_flag` and/or `TrustedPolicyAnchor` which S02 removed for current E11 local CLI. This affects self-contained instructions even though those Gates do not produce row Parquet.
- **G10:** 06/07/Pxx promise unconditional *all-41 rerun* and double opt-in; must distinguish **all 41 valid independent DGP/NEG/REF evidence** from **only changed/affected reruns on verified transitive closure**.
- **P2-M01–08, P3-M05, P3-M12:** B03 added typed non-scalar scientific artifacts; G04/G07/G09 06/Pxx/07 need to preserve canonical Result `point.NOT_AVAILABLE` for non-scalar target and Manifest typed artifacts without individual-row disclosure.
- **B04:** DoWhy/EconML/Tigramite optional exact versions and real API/Inference under Python3.12 cannot be audited as `SUPPORTED` from Schema alone; `uv.lock` lacks these packages.
- **B05:** Reference IDs exist but independently compiled and pinned source + datasets + K/R/ε and T2/T3 evidence are absent, no Science PASS.
- **G08 scientific authority:** `combined_review/111` explicitly calls HC1 χ² quadratic AR implementation *proposed*; current 30_63 says adopted implementation. This is a separate scientific decision/independent referee reconciliation requiring explicit authority before G08 Freeze.

## Stage classification

S05-B01/B02: 200 structural AST/parity candidate PASS, independent standard Draft202012 Validator run still unverified.

S05-B05: 41 method oracle *specification candidates* (not 41 independent executable reference implementations), quantitative acceptance inputs are still null.

S05-B06: 71/71 active 06/07/Pxx files scanned; **FAIL as drafted**, but rewriting them is S06/S07 responsibility. S09 shall independently reread all, re-check 10 requirements → 22 architecture → 23 IF/schema → 30 class → 06/Pxx → 07/40; the present keyword scan is not S09 PASS.

**Current contract state:** `S05_BLOCKED / S06_NOT_AUTHORIZED_FOR_FREEZE / S09_NOT_RUN / S10_NOT_FROZEN / S11_CODING_NOT_AUTHORIZED`. Historical DEC records are preserved; do not edit accepted pre-S02 decisions as if they had never happened. No source/tests/lock/canonical requirement changes.
