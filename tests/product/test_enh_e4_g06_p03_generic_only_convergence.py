"""Static policy-boundary checks for E4-G06 P03."""

from __future__ import annotations

import inspect

from ariadne.product.application.exploratory_service import ExploratoryWorkspaceService
from ariadne.product.application.predictive_workflow_service import PredictiveWorkflowService
from ariadne.product.application.product_closure_service import ProductClosureService
from ariadne.product.domain.lineage import LineageAuthority, classify_lineage_authority


def test_p03_approved_generic_only_tuples_remain_admitted() -> None:
    assert classify_lineage_authority(
        "Result", "MOTIVATED", "AnalysisSpecificationDraft",
    ) is LineageAuthority.GENERIC_ONLY
    assert classify_lineage_authority(
        "Project", "SELECTED", "Annotation",
    ) is LineageAuthority.GENERIC_ONLY


def test_p03_active_unapproved_writers_are_removed() -> None:
    predictive = inspect.getsource(PredictiveWorkflowService._canonical_submission)
    view_fix = inspect.getsource(ExploratoryWorkspaceService.fix_view)
    assert "_lineage(" not in predictive
    assert "_add_lineage(" not in view_fix


def test_p03_active_generic_only_writers_cannot_bypass_admission() -> None:
    exploratory_helper = inspect.getsource(ExploratoryWorkspaceService._add_lineage)
    annotation_writer = inspect.getsource(ProductClosureService.create_annotation)
    assert "assert_generic_lineage_allowed" in exploratory_helper
    assert "assert_generic_lineage_allowed" in annotation_writer
