"""Focused read-side contract checks for E4-G06 P04."""

from __future__ import annotations

import inspect

from ariadne.product.application.predictive_workflow_service import PredictiveWorkflowService
from ariadne.product.application.product_closure_service import ProductClosureService


def test_p04_project_lineage_uses_canonical_execution_for_all_families() -> None:
    source = inspect.getsource(ProductClosureService.project_lineage)
    assert "canonical_execs" in source
    assert "family=row.analysis_family" in source
    assert '"AnalysisView", analysis_view_id, "USED_INPUT", "Execution"' in source
    assert '"Result", row.input_result_id, "USED_INPUT", "Execution"' in source
    assert "row.base_execution_id" in source


def test_p04_predictive_lineage_unions_typed_and_generic_only_reads() -> None:
    source = inspect.getsource(PredictiveWorkflowService.list_lineage)
    helper = inspect.getsource(PredictiveWorkflowService._canonical_typed_lineage)
    assert "_canonical_typed_lineage" in source
    assert "LineageAuthority.GENERIC_ONLY" in source
    for relation in (
        '"DatasetVersion", execution.dataset_version_id, "USED_INPUT", "Execution"',
        '"AnalysisView", analysis_view_id, "USED_INPUT", "Execution"',
        '"Execution", execution.execution_id, "GENERATED", "Result"',
        '"Result", artifact.result_id, "GENERATED", "Artifact"',
    ):
        assert relation in helper
