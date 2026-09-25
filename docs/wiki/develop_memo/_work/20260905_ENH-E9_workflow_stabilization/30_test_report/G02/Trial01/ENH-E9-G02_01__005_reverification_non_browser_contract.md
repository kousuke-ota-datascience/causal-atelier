# ENH-E9 G02 Trial 01 Test Item 005 — Reverification non-browser contract regression

> **Document class:** Evidence Artifact

- Status: PASS (FRONTEND_CONTRACT / API_INTEGRATION)
- Fixed Trial Candidate SHA: `8cf70523093efa53b59a7de2c655f9755dbceb8d`
- Tested Repository State: `7a142e306bc3c921e1b6be81e6f20e58ac223d80`
- 07 Contract: `10_enhance_instruction/G02/07_Ariadne_ENH-E9_G02_test_instruction.md` (FROZEN)
- Timestamp: 2026-09-06T05:14:21Z

## Purpose / command

AC1–AC8 non-browser primary proof; item 004 identity precondition passed.

```bash
node --check frontend/app.js
git diff --check
uv run pytest -q tests/enhancement/enh_e9/g02/frontend/test_discovery_copy_help_overflow.py tests/enhancement/enh_e9/g02/frontend/test_selection_comparison_clarity.py tests/enhancement/enh_e9/g02/frontend/test_adoption_feedback_export.py tests/product/test_enh_e2_contract.py::test_graph_candidate_lifecycle_and_comparison_are_state_derived tests/product/test_enh_e2_contract.py::test_inference_rejects_missing_or_tampered_graph_outcome tests/product/test_enh_e7_g02_p03_causal_stage_surface_migration.py
```

Exit code: `0`.

```text
...........                                                              [100%]
11 passed in 5.82s
```

## Facts / evaluation

Current migrated G02 contracts passed for Discovery purpose/help, local candidate overflow/identity, selection-only controls, comparison identity, persisted algorithm/parameter data, adoption feedback, and deterministic no-request Mermaid export. E2/E7 API contracts passed for comparison/adoption/fix, identity/lineage, DRAFT-FIXED, FIXED immutability, and Outcome lineage.

| AC | Result | Evidence |
|---|---|---|
| AC1–AC2 | PASS | P01 frontend contracts |
| AC3–AC5 | PASS | P02 frontend contracts |
| AC6–AC7 | PASS | P03 frontend contracts |
| AC8 | PASS | E2/E7 contract regressions |

Production, migration, dependency changes by Test Agent: NONE. Reproduce using the command above.
