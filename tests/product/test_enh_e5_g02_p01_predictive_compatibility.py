"""Focused compatibility inventory for ENH-E5 G02 P01.

This test is deliberately limited to the existing Predictive contract.  It
records the setup controls and their canonical specification destinations,
without assigning navigation stages to execution stages.
"""

from __future__ import annotations

from pathlib import Path

from ariadne.capabilities.predictive import PredictivePlanner
from ariadne.capabilities.predictive.validation import validate_predictive_specification


REPOSITORY = Path(__file__).parents[2]
PREDICTIVE_TOP_LEVEL_FIELDS = (
    "schema_version",
    "task_type",
    "prediction_question",
    "feature_spec",
    "split_spec",
    "preprocessing_spec",
    "model_spec",
    "tuning_spec",
    "evaluation_spec",
    "explanation_spec",
)


def _predictive_workspace() -> tuple[str, str]:
    html = (REPOSITORY / "frontend" / "index.html").read_text(encoding="utf-8")
    workspace = html.split('<section id="predictive"', 1)[1].split(
        '<section id="results"', 1
    )[0]
    return workspace, (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")


def test_current_predictive_controls_have_canonical_payload_destinations() -> None:
    """The existing setup controls all remain represented in the family spec."""
    workspace, javascript = _predictive_workspace()
    inventory = {
        "task_type": "task_type",
        "prediction_unit": "prediction_question",
        "target": "prediction_question",
        "prediction_time": "prediction_question",
        "horizon": "prediction_question",
        "intended_use": "prediction_question",
        "deployment_population": "prediction_question",
        "feature_columns": "feature_spec",
        "excluded_columns": "feature_spec",
        "split_strategy": "split_spec",
        "train_ratio": "split_spec",
        "validation_ratio": "split_spec",
        "test_ratio": "split_spec",
        "seed": "split_spec",
        "explanation_method": "explanation_spec",
        "explanation_sample_size": "explanation_spec",
        "local_explanations": "explanation_spec",
    }

    unmapped = [
        control for control in inventory
        if f'name="{control}"' not in workspace
        or inventory[control] not in PREDICTIVE_TOP_LEVEL_FIELDS
    ]
    assert unmapped == []
    assert "function predictiveFamilySpec()" in javascript
    assert all(f"{field}:" in javascript for field in PREDICTIVE_TOP_LEVEL_FIELDS)


def test_canonical_payload_and_runtime_plan_remain_deterministic(
    predictive_spec_factory,
) -> None:  # type: ignore[no-untyped-def]
    """The same valid input produces the same canonical payload and runtime plan."""
    specification = predictive_spec_factory()
    validated = validate_predictive_specification(specification)

    assert tuple(validated) == PREDICTIVE_TOP_LEVEL_FIELDS
    first = PredictivePlanner().build_full_plan(
        project_id="g02-p01-project",
        specification_id="g02-p01-specification",
        family_spec=validated,
    )
    second = PredictivePlanner().build_full_plan(
        project_id="g02-p01-project",
        specification_id="g02-p01-specification",
        family_spec=validated,
    )

    assert first.canonical_payload() == second.canonical_payload()
    assert first.plan_hash == second.plan_hash
    assert [stage.stage_key for stage in first.stages] == [
        "split", "prepare", "train", "evaluate",
    ]
