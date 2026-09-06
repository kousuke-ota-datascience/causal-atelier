# ENH-E9 G03 Trial 01 Test Item 002 — Frontend contract and lineage regression

> **Document class:** Evidence Artifact

- Project / Enhancement / Gate / Trial: Ariadne / ENH-E9 / G03 / 01
- Status / Primary layer: PASS / FRONTEND_CONTRACT and API_INTEGRATION
- Fixed Trial Candidate SHA: `f11be531dc34b7fbbf6aa8f1d74aaf28e0205e35`
- Tested Repository State: `be891e92f288662a7f2d33f4845d8ab6e0e73ac4`
- 07 Contract: `10_enhance_instruction/G03/07_Ariadne_ENH-E9_G03_test_instruction.md` (FROZEN)
- Timestamp: 2026-09-06T07:56:00Z

## Purpose / exact command

AC1–AC7 and protected Graph → Identification → Estimation lineage; item 001 passed first.

```bash
node --check frontend/app.js
git diff --check
uv run pytest -q tests/enhancement/enh_e9/g03/frontend/test_identification_input_ergonomics.py tests/enhancement/enh_e9/g03/frontend/test_estimation_submission_regression.py tests/product/test_enh_e2_contract.py::test_graph_candidate_lifecycle_and_comparison_are_state_derived tests/product/test_enh_e2_contract.py::test_inference_rejects_missing_or_tampered_graph_outcome tests/product/test_enh_e5_g03_p02_identification_estimation_separation.py tests/product/test_enh_e5_g03_p03_causal_runtime_regression.py
```

Exit code: `0`.

```text
...............                                                          [100%]
15 passed in 6.49s
```

## Observed facts / evaluation

Focused checks verify Population/Comparator help, schema-authoritative Treatment options, stale Treatment clearing with notice, read-only Graph-projected Outcome, and Estimation submission from selected Identification lineage. Existing contracts verify Graph outcome protection, DRAFT/FIXED/immutability semantics, causal-question/estimation separation, and runtime operation/input matrix.

| AC | Result | Evidence |
|---|---|---|
| AC1–AC3 | PASS | Focused identification ergonomics tests |
| AC4–AC5 | PASS | Focused serialization/outcome projection tests and graph-outcome contract |
| AC6 | PASS | E2/E5 protected Graph and causal-question contracts |
| AC7 | PASS | Focused estimation lineage and E5 runtime regression |

Production, migration, dependency changes by Test Agent: NONE. Reproduce with the command above.
