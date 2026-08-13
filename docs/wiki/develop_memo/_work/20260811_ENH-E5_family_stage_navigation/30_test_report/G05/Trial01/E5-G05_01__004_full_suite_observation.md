# ENH-E5 G05 Trial 01 — Test Item 004: Full-suite diagnostic observation

- Test item: `004_full_suite_observation`
- Verification purpose: Independent non-gating repository-wide regression observation.
- Test target: `ebc943d0401a838f429d1281b2e1a3863ca29bf4`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/pytest -q
```

## Observed output

```text
5 failed, 314 passed, 33 skipped, 1 warning in 92.01s
```

Failures:

1. `test_scientific_status_is_exact_design_contract`: expected enum set differs from repository runtime (`TRAINED`, `TRAINED_WITH_WARNINGS`, `EVALUATED`, `INSUFFICIENT_TEST_SAMPLE`, and `NOT_APPLICABLE` are additional values).
2. `test_project_delete_is_idempotent_archive_and_all_new_writes_are_guarded`: execution-batch create without `Idempotency-Key` receives 400 instead of the test's former 202 expectation.
3. `test_inference_rejects_missing_or_tampered_graph_outcome`: request without `Idempotency-Key` receives 400 before the test's former 409 expectation.
4. `test_research_context_to_cross_family_results_lineage_annotation_and_export`: predictive execution submission without `Idempotency-Key` has no `execution_id` because it is rejected.
5. `test_api_worker_persists_explanation_model_card_artifacts_and_lineage`: same missing-key predictive execution submission behavior.

## Result

**FAIL (non-gating diagnostic observation)**

The four missing-key observations are consistent with the frozen G05 mandatory rule `missing required key -> IDEMPOTENCY_KEY_REQUIRED`; they do not contradict the passing protected regression item. The ScientificStatus failure is outside the frozen G05 acceptance criteria and candidate diff scope. This item is retained as raw evidence and is not used to infer a product violation of an AC-G05 requirement.
