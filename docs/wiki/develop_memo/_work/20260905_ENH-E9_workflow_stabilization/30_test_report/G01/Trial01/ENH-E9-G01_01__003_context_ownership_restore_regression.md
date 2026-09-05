# ENH-E9 G01 Trial 01 Test Item 003 — Context ownership and restore regression

> **Document class:** Evidence Artifact

- Project: Ariadne
- Enhancement / Gate / Trial: ENH-E9 / G01 / 01
- Status: PASS
- Primary test layer: FRONTEND_CONTRACT
- Fixed Trial Candidate SHA: `b01f16aaf612c84e7434d3ab492d1cbe1ca6d24b`
- Tested Repository State: `0711126e117b314b13c618d765d01676f3d9834b`
- Completion report: `20_implementation_reports/G01/Trial01/ENH-E9-G01_01__implementation_completion.md`
- 07 Contract: `10_enhance_instruction/G01/07_Ariadne_ENH-E9_G01_test_instruction.md` (FROZEN)
- Applicable 08: NONE
- Timestamp: 2026-09-05T14:58:52Z

## 1. Purpose / Acceptance mapping

- Covers AC: AC4
- Candidate identity audit: NO (see item 001)
- Protected Gate regression: G01 protected context/project ownership and restore semantics
- Transition Debt relation: NONE

## 2. Candidate identity evidence

Candidate identity is VALID under item 001; the tested-head difference is documentation-only.

## 3. Preconditions

The frozen 07 requires existing architecture/contract tests for AC4. The stage-contents assertion is excluded: it is unrelated to route/project authority or Research Context / Dataset Version / Analysis View ownership, restore, and invalidation semantics, and is absent already in the candidate parent.

## 4. Exact command
```bash
uv run pytest -q \
  tests/product/test_enh_e7_g01_p04_research_context_surface.py \
  tests/product/test_enh_e7_g01_p05_data_analysis_view_surface.py \
  tests/product/test_enh_e7_g02_p01_analysis_shell_context.py::test_context_header_has_read_only_project_and_restores_only_saved_selection \
  tests/product/test_enh_e7_g02_p01_analysis_shell_context.py::test_context_selection_updates_do_not_navigate_or_create_resources
```

## 5. Exit code
`0`

## 6. Raw relevant evidence
```text
......                                                                   [100%]
6 passed in 1.69s
```

## 7. Observed Facts

The selected existing contracts passed for read-only Current Project, saved context/dataset/view selection restoration, invalid-selection signaling, selection updates without navigation/create requests, Research Context lifecycle/usage surface, and fixed Analysis View cross-family input behavior.

## 8. Interpretation

These tests cover the AC4 protected semantics actually touched or adjacent to the candidate. No evidence indicates regression of route/project authority, ownership, or restore behavior.

## 9. Criterion evaluation
| Criterion | Expected | Observed | Result |
|---|---|---|---|
| AC4 project authority | Current Project remains read-only / non-navigating selection behavior | Contract assertions passed | PASS |
| AC4 context ownership and restore | Existing fixed-context lifecycle and saved selection restore remain intact | Contract assertions passed | PASS |
| AC4 dataset/view ownership | Existing fixed-view lifecycle and cross-family inputs remain intact | Contract assertions passed | PASS |

## 10. Source mutation audit

- Production code changed by Test Agent: NONE
- Automated test code changed by Test Agent: NONE
- Migration changed by Test Agent: NONE
- Dependency changed by Test Agent: NONE

## 11. Reproduction procedure

Run the exact pytest invocation above from repository root at the recorded tested state.

## 12. Result rationale

All six targeted protected-regression checks passed. The excluded unrelated baseline assertion cannot establish an AC4 regression and was not used to reinterpret the frozen contract.
