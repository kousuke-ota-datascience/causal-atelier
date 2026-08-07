from __future__ import annotations

import pandas as pd
import pytest

from ariadne.capabilities.exploratory import ExploratoryPlanner, register_exploratory_runners
from ariadne.product.workflow.executor import GenericExecutor
from ariadne.product.workflow.runner_registry import StageRunnerRegistry


@pytest.mark.parametrize(
    ("operation", "extra", "result_type"),
    [
        ("PROFILE", {}, "DATA_PROFILE_RESULT"),
        ("DISTRIBUTION", {"columns": ["sales"]}, "DISTRIBUTION_RESULT"),
        ("ASSOCIATION", {"columns": ["sales", "units"]}, "ASSOCIATION_RESULT"),
        ("GROUP_SUMMARY", {"grouping": ["group"], "aggregation": {"method": "MEAN", "column": "sales"}}, "GROUP_SUMMARY_RESULT"),
        ("TIME_TREND", {"grouping": ["date"], "aggregation": {"method": "SUM", "column": "sales"}}, "GROUP_SUMMARY_RESULT"),
        ("CHART", {"chart_encoding": {"mark": "point", "x": "units", "y": "sales"}}, "CHART_RESULT"),
    ],
)
@pytest.mark.requirement("FR-023", "FR-024", "FR-026", "FR-027", "FR-029", "FR-030", "FR-033")
def test_exploratory_operations_are_registered_typed_and_non_causal(
    operation: str, extra: dict, result_type: str,  # type: ignore[type-arg]
) -> None:
    frame = pd.DataFrame({
        "group": ["A", "A", "B", "B"], "date": ["d1", "d2", "d1", "d2"],
        "sales": [10.0, 12.0, 20.0, 18.0], "units": [1, 2, 3, 4],
    })
    spec = {"schema_version": "exploratory-analysis-spec/1", "operation": operation, **extra}
    registry = StageRunnerRegistry(); register_exploratory_runners(registry)
    plan = ExploratoryPlanner().build_for_spec(
        project_id="project", specification_id="spec", family_spec=spec
    )
    outcome = GenericExecutor(registry).execute(
        "execution", plan, external_inputs={plan.stages[0].stage_key: {"frame": frame}}
    )
    assert outcome.status == "SUCCEEDED"
    result = outcome.results[0]
    assert result.result_type == result_type
    assert result.schema_version.startswith("exploratory-")
    assert result.summary["analysis_label"] == "EXPLORATORY"
    serialized = str(result).lower()
    assert "treatment effect" not in serialized and "causes" not in serialized
    if operation == "CHART":
        assert outcome.artifacts[0].media_type == "application/vnd.vegalite.v5+json"
