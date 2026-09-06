# ENH-E9 G02 Trial 01 Test Item 002 — Non-browser interaction and contract regression

> **Document class:** Evidence Artifact

- Project / Enhancement / Gate / Trial: Ariadne / ENH-E9 / G02 / 01
- Status / Primary layer: PASS / FRONTEND_CONTRACT and API_INTEGRATION
- Fixed Trial Candidate SHA: `8cf70523093efa53b59a7de2c655f9755dbceb8d`
- Tested Repository State: `6355ce9252a896c5907ac465b102e959c5b481f7`
- Completion report: `20_implementation_reports/G02/Trial01/ENH-E9-G02_01__implementation_completion.md`
- 07 Contract: `10_enhance_instruction/G02/07_Ariadne_ENH-E9_G02_test_instruction.md` (FROZEN)
- Applicable 08: NONE
- Timestamp: 2026-09-06T01:13:54Z

## Purpose / acceptance mapping

- Covers AC1–AC8 as frozen-07 non-browser primary proof; candidate identity audit NO (item 001).
- Protected regression: Graph Candidate identity/lineage/lifecycle/outcome semantics.

## Preconditions and exact command

Item 001 passed. Frozen 07 mandates this static/unit/API order before Browser E2E.

```bash
node --check frontend/app.js
git diff --check
uv run pytest -q tests/product/test_enh_e9_g02_p01_discovery_copy_help_overflow.py tests/product/test_enh_e9_g02_p02_selection_comparison_clarity.py tests/product/test_enh_e9_g02_p03_adoption_feedback_export.py tests/product/test_enh_e2_contract.py::test_graph_candidate_lifecycle_and_comparison_are_state_derived tests/product/test_enh_e2_contract.py::test_inference_rejects_missing_or_tampered_graph_outcome tests/product/test_enh_e7_g02_p03_causal_stage_surface_migration.py
```

Exit code: `0`.

```text
...........                                                              [100%]
11 passed in 4.93s
```

## Facts and interpretation

Syntax and whitespace checks passed. Focused tests passed for Discovery purpose/help and local candidate overflow; selection-only controls; current comparison identification and persisted algorithm/parameter summary; modal-local adoption feedback; deterministic no-request Mermaid export. Existing API/contract regressions passed for Graph Candidate lifecycle/comparison, invalid outcome rejection, and causal stage presentation.

| Criterion | Expected | Observed | Result |
|---|---|---|---|
| AC1–AC2 | Discovery clarity, local overflow, identity | P01 contracts passed | PASS |
| AC3–AC5 | Selection-only, current comparison, authoritative data | P02 contracts passed | PASS |
| AC6–AC7 | Adoption feedback and no-mutation Mermaid | P03 contracts passed | PASS |
| AC8 | Identity/lineage/DRAFT-FIXED/FIXED/outcome | E2/E7 contracts passed | PASS |

## Mutation audit / reproduction / rationale

- Production, automated test, migration, dependency changes by Test Agent: NONE.
- Reproduce with the exact command above at the tested state.
- All non-browser blocking primary proofs pass; frozen 07 still requires item 003 Browser E2E last.
