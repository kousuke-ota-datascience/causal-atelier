"""Static P02 checks for active canonical structural lineage writers."""

from __future__ import annotations

import inspect

import pytest

from ariadne.product.application.exploratory_service import ExploratoryWorkspaceService
from ariadne.product.application.predictive_workflow_service import PredictiveWorkflowService
from ariadne.product.domain.lineage import LineageAuthority, classify_lineage_authority


@pytest.mark.parametrize(("family", "source", "relation", "target"), (
    ("EXPLORATORY", "DatasetVersion", "USED_INPUT", "Execution"),
    ("EXPLORATORY", "AnalysisView", "USED_INPUT", "Execution"),
    ("PREDICTIVE", "DatasetVersion", "USED_INPUT", "Execution"),
    ("PREDICTIVE", "AnalysisView", "USED_INPUT", "Execution"),
))
def test_p02_active_input_tuples_are_typed_structural(
    family: str, source: str, relation: str, target: str,
) -> None:
    assert family in {"EXPLORATORY", "PREDICTIVE"}
    assert classify_lineage_authority(source, relation, target) is LineageAuthority.TYPED_STRUCTURAL


def test_exploratory_canonical_return_has_no_structural_generic_writer() -> None:
    source = inspect.getsource(ExploratoryWorkspaceService.submit_execution)
    canonical_return = source.index("return canonical")
    canonical_section = source[:canonical_return]
    assert "self._add_lineage(" not in canonical_section


def test_predictive_canonical_submission_has_no_typed_input_generic_writers() -> None:
    source = inspect.getsource(PredictiveWorkflowService._canonical_submission)
    assert '("DatasetVersion", specification.dataset_version_id' not in source
    assert '"AnalysisView", family_snapshot["analysis_view"]["id"]' not in source


def test_causal_has_no_active_product_lineage_edge_writer() -> None:
    # Causal Product processing persists canonical Result/Artifact ownership;
    # this targeted audit guards against an active Causal LineageEdge writer.
    source = inspect.getsource(__import__("ariadne.product.application.execution_service", fromlist=["ExecutionService"]))
    assert "LineageEdgeOrm" not in source
