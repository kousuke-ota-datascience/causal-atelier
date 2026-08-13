"""Focused regression and visualization-boundary checks for ENH-E5 G04 P03."""

from __future__ import annotations

import pytest
from sqlalchemy import func, select

from ariadne.capabilities.exploratory import ExploratoryPlanner
from ariadne.interfaces.web_api import dependencies
from ariadne.product.application.navigation_catalog import CATALOG
from ariadne.product.domain.analysis_view import validate_analysis_view_payload
from ariadne.product.domain.errors import InvalidSchema
from ariadne.product.persistence.orm_models import ExecutionOrm


_OPERATIONS = {
    "PROFILE": "profile",
    "DISTRIBUTION": "distribution",
    "ASSOCIATION": "association",
    "GROUP_SUMMARY": "aggregate",
    "TIME_TREND": "time_trend",
    "CHART": "chart",
}


def test_exploratory_runtime_operations_are_fixed_and_not_navigation_generated() -> None:
    planner = ExploratoryPlanner()
    assert set(_OPERATIONS) == {
        "PROFILE", "DISTRIBUTION", "ASSOCIATION", "GROUP_SUMMARY", "TIME_TREND", "CHART",
    }
    for operation, runner_name in _OPERATIONS.items():
        plan = planner.build_for_spec(
            project_id="project",
            specification_id="specification",
            family_spec={"schema_version": "exploratory-analysis-spec/1", "operation": operation},
        )
        assert plan.stages[0].stage_type.name == runner_name

    stages = next(item.stages for item in CATALOG if item.slug == "exploratory")
    for read_only_stage in ("data-quality", "findings"):
        assert read_only_stage in {stage.slug for stage in stages}
        with pytest.raises(ValueError, match="Unsupported exploratory operation"):
            planner.build_for_spec(
                project_id="project",
                specification_id="specification",
                family_spec={
                    "schema_version": "exploratory-analysis-spec/1",
                    "operation": read_only_stage.upper(),
                },
            )


@pytest.mark.anyio
async def test_read_only_navigation_surface_creates_no_execution(client) -> None:  # type: ignore[no-untyped-def]
    factory = dependencies._get_session_factory()
    with factory() as session:
        before = session.scalar(select(func.count()).select_from(ExecutionOrm))
    response = await client.get("/api/v1/navigation/analysis")
    assert response.status_code == 200
    exploratory = next(item for item in response.json()["families"] if item["slug"] == "exploratory")
    assert [item["slug"] for item in exploratory["stages"]][1] == "data-quality"
    assert [item["slug"] for item in exploratory["stages"]][-1] == "findings"
    with factory() as session:
        after = session.scalar(select(func.count()).select_from(ExecutionOrm))
    assert after == before


def test_analysis_view_rejects_visualization_and_panel_state() -> None:
    selection = {
        "schema_version": "analysis-view/1",
        "source_dataset_version_id": "dataset",
        "row_filter": [],
        "selected_columns": [],
        "derived_columns": [],
        "missing_value_policy": {},
        "time_cutoff": None,
        "sampling": None,
    }
    for state in ({"chart_encoding": {"mark": "point"}}, {"panel_layout": {}}, {"active_widget": "chart"}):
        with pytest.raises(InvalidSchema):
            validate_analysis_view_payload({**selection, **state})
