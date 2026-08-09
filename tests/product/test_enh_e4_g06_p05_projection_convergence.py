"""Focused source-class projection checks for E4-G06 P05."""

from __future__ import annotations

import inspect

from ariadne.product.application.product_closure_service import ProductClosureService


def test_p05_project_edges_have_an_authority_source_class() -> None:
    source = inspect.getsource(ProductClosureService.project_lineage)
    assert 'source_class: str = "TYPED_STRUCTURAL"' in source
    assert 'source_class="GENERIC_ONLY"' in source


def test_p05_export_reuses_closure_instead_of_snapshot_synthesis() -> None:
    export = inspect.getsource(ProductClosureService.create_export)
    helper = inspect.getsource(ProductClosureService._export_lineage_references)
    assert "_export_lineage_references" in export
    assert "result_lineage" in helper
    assert "_synthetic_export_lineage" not in export
