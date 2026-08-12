"""Focused contract tests for ENH-E5 G04 P01."""

from __future__ import annotations

import pytest

from ariadne.capabilities.exploratory.view_compiler import AnalysisViewCompiler
from ariadne.product.application.navigation_catalog import CATALOG
from ariadne.product.domain.errors import FilterTypeMismatch


def _spec(condition: dict, *, cutoff: dict | None = None) -> dict:
    return {
        "schema_version": "analysis-view/1", "source_dataset_version_id": "dataset",
        "row_filter": [condition], "selected_columns": [], "derived_columns": [],
        "missing_value_policy": {}, "time_cutoff": cutoff, "sampling": None,
    }


def test_exploratory_navigation_has_the_exact_six_presentation_stages() -> None:
    exploratory = next(item for item in CATALOG if item.slug == "exploratory")
    assert [stage.slug for stage in exploratory.stages] == [
        "profile", "data-quality", "distribution", "relationships", "comparison", "findings",
    ]


@pytest.mark.parametrize(
    ("logical_type", "condition"),
    [
        ("BOOLEAN", {"column": "x", "operator": "EQ", "value": True}),
        ("INTEGER", {"column": "x", "operator": "GTE", "value": 1}),
        ("REAL", {"column": "x", "operator": "IN", "value": [1, 2.5]}),
        ("DATETIME", {"column": "x", "operator": "LT", "value": "2026-01-01T00:00:00Z"}),
        ("TEXT", {"column": "x", "operator": "NOT_IN", "value": ["a"]}),
        ("OTHER", {"column": "x", "operator": "IS_NULL"}),
    ],
)
def test_typed_filter_accepts_the_contract_matrix(logical_type: str, condition: dict) -> None:
    AnalysisViewCompiler().validate({"x": logical_type}, _spec(condition))


@pytest.mark.parametrize(
    ("logical_type", "condition"),
    [
        ("BOOLEAN", {"column": "x", "operator": "LT", "value": True}),
        ("INTEGER", {"column": "x", "operator": "EQ", "value": True}),
        ("REAL", {"column": "x", "operator": "EQ", "value": float("inf")}),
        ("DATETIME", {"column": "x", "operator": "EQ", "value": "not-a-date"}),
        ("TEXT", {"column": "x", "operator": "GT", "value": "a"}),
        ("OTHER", {"column": "x", "operator": "EQ", "value": "a"}),
        ("INTEGER", {"column": "x", "operator": "IN", "value": []}),
        ("INTEGER", {"column": "x", "operator": "IS_NULL", "value": None}),
    ],
)
def test_typed_filter_rejects_mismatches_with_the_required_code(logical_type: str, condition: dict) -> None:
    with pytest.raises(FilterTypeMismatch, match="FILTER_TYPE_MISMATCH"):
        AnalysisViewCompiler().validate({"x": logical_type}, _spec(condition))


def test_typed_filter_rejects_unknown_source_type_and_requires_datetime_time_cutoff() -> None:
    compiler = AnalysisViewCompiler()
    with pytest.raises(FilterTypeMismatch, match="FILTER_TYPE_MISMATCH"):
        compiler.validate({"x": "UNKNOWN"}, _spec({"column": "x", "operator": "EQ", "value": 1}))
    with pytest.raises(FilterTypeMismatch, match="FILTER_TYPE_MISMATCH"):
        compiler.validate({"x": "TEXT"}, _spec({"column": "x", "operator": "EQ", "value": "a"}, cutoff={"column": "x", "operator": "LTE", "value": "2026-01-01"}))
    compiler.validate({"x": "DATETIME"}, _spec({"column": "x", "operator": "EQ", "value": "2026-01-01"}, cutoff={"column": "x", "operator": "LTE", "value": "2026-01-01"}))
